"""Generate type stubs from Flame HTML API docs under docs/.

Pipeline:
  HTML pages  --html_to_api-->  ApiModel  --api_to_module-->  libcst Module  -->  .pyi
"""
from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from html import unescape
from pathlib import Path

import libcst as cst
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "out/docs"
OUT = ROOT / "out/from_docs.pyi"

TYPE_MAP = {
    "str": "str",
    "string": "str",
    "unicode": "str",
    "bool": "bool",
    "boolean": "bool",
    "int": "int",
    "integer": "int",
    "float": "float",
    "tuple": "tuple",
    "list": "list",
    "dict": "dict",
    "nonetype": "Any | None",
    "none": "Any | None",
}
CLASS_ALIASES = {
    "PyMediaHubTabFiles": "PyMediaHubFilesTab",
    "PyMediaHubFileTabOptions": "PyMediaHubFilesTabOptions",
}
KNOWN_CLASSES = {
    "PyActionNode",
    "PyAudioTrack",
    "PyBatch",
    "PyBatchIteration",
    "PyClip",
    "PyClipNode",
    "PyCoCompass",
    "PyCoNode",
    "PyCompassNode",
    "PyDesktop",
    "PyFolder",
    "PyGMaskTracerNode",
    "PyLensDistortionNode",
    "PyLibrary",
    "PyMarker",
    "PyMediaHub",
    "PyMediaHubFilesTab",
    "PyMediaHubFilesTabOptions",
    "PyMediaHubTab",
    "PyNode",
    "PyOFXNode",
    "PyPaintNode",
    "PyProject",
    "PyReel",
    "PyReelGroup",
    "PySegment",
    "PySequence",
    "PyTimelineFX",
    "PyTimewarpNode",
    "PyTimewarpTimelineFX",
    "PyTrack",
    "PyTypeLayer",
    "PyTypeNode",
    "PyTypeTimelineFX",
    "PyVersion",
    "PyWorkspace",
    "PyWriteFileNode",
}
BASES = {
    "PyMediaHubFilesTab": "PyMediaHubTab",
    "PyTimewarpTimelineFX": "PyTimelineFX",
    "PyTypeTimelineFX": "PyTimelineFX",
}

DL_ATTR_RE = re.compile(
    r"^(?P<name>[A-Za-z_][\w]*)\s*\((?:type|class)\s+'(?:flame\.)?(?P<type>[^']+)'\)\s*$"
)
TABLE_CMD_RE = re.compile(
    r"^(?:flame\.)?(?P<cls>Py[A-Za-z_][\w]*)\s*>\s*\.(?P<name>[A-Za-z_][\w]*)$"
)
PY_CLASS_RE = re.compile(r"\bPy[A-Za-z_][\w]*\b")
MEDIAHUB_ATTR_RE = re.compile(r"^flame\.mediahub\.(?P<name>[A-Za-z_][\w]*)$")


# ---------------------------------------------------------------------------
# Intermediate model (HTML → X)
# ---------------------------------------------------------------------------


@dataclass
class Attr:
    type: str
    doc: str = ""


@dataclass
class Method:
    returns: str
    params: list[tuple[str, str]] = field(default_factory=list)  # (name, type)
    doc: str = ""


@dataclass
class ClassModel:
    name: str
    bases: list[str] = field(default_factory=list)
    doc: str = ""
    attrs: dict[str, Attr] = field(default_factory=dict)
    methods: dict[str, Method] = field(default_factory=dict)

    def merge_attr(self, name: str, attr: Attr) -> None:
        existing = self.attrs.get(name)
        if existing is None:
            self.attrs[name] = attr
            return
        # Last write wins for type; keep the best docstring we have seen.
        existing.type = attr.type
        if attr.doc and (not existing.doc or len(attr.doc) > len(existing.doc)):
            existing.doc = attr.doc

    def merge_method(self, name: str, method: Method) -> None:
        existing = self.methods.get(name)
        if existing is None:
            self.methods[name] = method
            return
        existing.returns = method.returns
        existing.params = method.params
        if method.doc and (not existing.doc or len(method.doc) > len(existing.doc)):
            existing.doc = method.doc


@dataclass
class ApiModel:
    classes: dict[str, ClassModel] = field(default_factory=dict)
    module_attrs: dict[str, Attr] = field(default_factory=dict)
    # Occurrence counts for Batch/Action common-attr pruning
    section_counts: dict[str, Counter[str]] = field(default_factory=lambda: defaultdict(Counter))

    def cls(self, name: str) -> ClassModel:
        if name not in self.classes:
            self.classes[name] = ClassModel(name=name)
        return self.classes[name]


# ---------------------------------------------------------------------------
# HTML helpers
# ---------------------------------------------------------------------------


def normalize_class(name: str) -> str:
    return CLASS_ALIASES.get(name.strip(), name.strip())


def normalize_type(raw: str) -> str:
    raw = re.sub(r"<[^>]+>", "", unescape(raw)).strip()
    if not raw:
        return "Any"
    if m := re.match(r"(Py[A-Za-z_][\w]*)", raw):
        return normalize_class(m.group(1))
    return TYPE_MAP.get(raw.split()[0].lower(), "Any")


def clean_doc(text: str) -> str:
    """Flatten HTML prose into a compact docstring body."""
    text = unescape(text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    # Drop trailing "Value range:" blocks — noisy in stubs
    text = re.split(r"\n?\s*Value [Rr]ange:\s*", text, maxsplit=1)[0]
    return text.strip()


def text_of(node: Tag | None) -> str:
    return node.get_text(" ", strip=True) if node else ""


def classes_from_heading(heading: str) -> list[str]:
    heading = unescape(heading)
    if m := re.search(r"\(([^)]+)\)", heading):
        found = [normalize_class(c) for c in PY_CLASS_RE.findall(m.group(1))]
        if found:
            return found
    return [normalize_class(c) for c in PY_CLASS_RE.findall(heading)]


def section_slug(heading: str) -> str:
    name = re.sub(r"\s+Attributes\s*$", "", unescape(heading), flags=re.I)
    return re.sub(r"[^A-Za-z0-9]+", "", name.replace("&", "And"))


def is_synthetic_conode(cls: str) -> bool:
    return cls.startswith("PyCo") and len(cls) > 4 and cls[4].isupper() and cls != "PyCoNode"


def section_nodes_after(heading: Tag) -> list:
    start: Tag = heading
    if heading.parent and heading.parent.name == "div" and "head-block" in (heading.parent.get("class") or []):
        start = heading.parent
    chunks = []
    for sib in start.next_siblings:
        if not isinstance(sib, Tag):
            chunks.append(sib)
            continue
        if sib.name in {"h1", "h2"}:
            break
        if sib.name == "div" and (
            "head-block" in (sib.get("class") or []) or "related-links" in (sib.get("class") or [])
        ):
            break
        chunks.append(sib)
    return chunks


def dd_doc(dt: Tag) -> str:
    dd = dt.find_next_sibling("dd")
    if dd is None:
        return ""
    # Prefer <p> bodies; fall back to full dd text
    parts = [p.get_text(" ", strip=True) for p in dd.find_all("p", recursive=False)]
    return clean_doc("\n\n".join(parts) if parts else text_of(dd))


def parse_dl_attrs(root: Tag | BeautifulSoup) -> list[tuple[str | None, str, str, str]]:
    """Return (owner_class|None, name, type, doc)."""
    out: list[tuple[str | None, str, str, str]] = []
    for dt in root.find_all("dt"):
        code = dt.find("code")
        if not code:
            continue
        m = DL_ATTR_RE.match(text_of(code))
        if not m:
            continue
        out.append((None, m.group("name"), normalize_type(m.group("type")), dd_doc(dt)))
    return out


def table_headers(table: Tag) -> list[str]:
    rows = table.find_all("tr")
    if not rows:
        return []
    return [text_of(c).lower() for c in rows[0].find_all(["th", "td"])]


def parse_attr_table(table: Tag) -> list[tuple[str | None, str, str, str]]:
    """Return (owner_class|None, name, type, doc) from Command/Property + Type tables."""
    headers = table_headers(table)
    if "type" not in headers:
        return []
    type_idx = headers.index("type")
    desc_idx = next((i for i, h in enumerate(headers) if h in {"description", "desc"}), None)
    out: list[tuple[str | None, str, str, str]] = []
    for tr in table.find_all("tr")[1:]:
        cells = tr.find_all(["td", "th"])
        if len(cells) <= type_idx:
            continue
        cmd = text_of(cells[0])
        typ = normalize_type(text_of(cells[type_idx]))
        doc = clean_doc(text_of(cells[desc_idx])) if desc_idx is not None and desc_idx < len(cells) else ""
        if m := TABLE_CMD_RE.match(cmd):
            out.append((normalize_class(m.group("cls")), m.group("name"), typ, doc))
        elif re.fullmatch(r"[A-Za-z_][\w]*", cmd):
            out.append((None, cmd, typ, doc))
    return out


def parse_method_table(table: Tag) -> list[tuple[str, Method]]:
    if table_headers(table) != ["command", "description"]:
        return []
    out: list[tuple[str, Method]] = []
    for tr in table.find_all("tr")[1:]:
        cells = tr.find_all(["td", "th"])
        if len(cells) < 2:
            continue
        name = text_of(cells[0])
        desc = text_of(cells[1])
        if not re.fullmatch(r"[A-Za-z_][\w]*", name):
            continue
        low = desc.lower()
        if name.startswith("get_") and "path" in name:
            ret, params = "str", []
        elif name.startswith("set_"):
            ret, params = "bool", [("path", "str")]
        elif "returns true" in low:
            ret, params = "bool", []
        else:
            ret, params = "Any", [("*args", "Any"), ("**kwargs", "Any")]
        out.append((name, Method(returns=ret, params=params, doc=clean_doc(desc))))
    return out


def page_kind(path: Path, soup: BeautifulSoup) -> str | None:
    title = text_of(soup.title)
    h1 = text_of(soup.find("h1"))
    blob = f"{path.name} {title} {h1}"
    if "Batch_Nodes_Attributes" in path.name or "PyNode: Batch Nodes" in blob:
        return "PyNode"
    if "Action_Nodes_Attributes" in path.name or "PyCoNode: Action Nodes" in blob:
        return "PyCoNode"
    return None


# ---------------------------------------------------------------------------
# HTML → ApiModel
# ---------------------------------------------------------------------------


def html_to_api(docs_dir: Path) -> ApiModel:
    api = ApiModel()
    for path in sorted(docs_dir.glob("*.html")):
        _ingest_page(api, path)
    _finalize(api)
    return api


def _ingest_page(api: ApiModel, path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        return
    soup = BeautifulSoup(text, "html.parser")
    kind = page_kind(path, soup)
    body = soup.find(class_="body_content") or soup

    for heading in body.find_all(["h1", "h2"]):
        heading_text = text_of(heading)
        targets = classes_from_heading(heading_text)
        specialized: str | None = None

        if kind and heading.name == "h2":
            slug = section_slug(heading_text)
            specialized = (
                f"Py{slug}Node" if kind == "PyNode" and slug else f"PyCo{slug}" if slug else None
            )
            # Don't clobber real API classes documented on their own pages.
            if specialized in KNOWN_CLASSES:
                specialized = None
            targets = [kind]
        elif not targets:
            targets = classes_from_heading(text_of(soup.title) or path.stem)

        section = BeautifulSoup("".join(str(c) for c in section_nodes_after(heading)), "html.parser")
        section_attrs: dict[str, Attr] = {}

        for owner, name, typ, doc in parse_dl_attrs(section):
            section_attrs[name] = Attr(typ, doc)

        for table in section.find_all("table"):
            for owner, name, typ, doc in parse_attr_table(table):
                attr = Attr(typ, doc)
                if owner and len(targets) > 1 and owner in targets:
                    for cls in targets:
                        api.cls(cls).merge_attr(name, attr)
                    section_attrs[name] = attr
                elif owner:
                    api.cls(owner).merge_attr(name, attr)
                else:
                    section_attrs[name] = attr
            for name, method in parse_method_table(table):
                for cls in targets:
                    api.cls(cls).merge_method(name, method)

        for cls in targets:
            for name, attr in section_attrs.items():
                api.cls(cls).merge_attr(name, attr)
            if kind and heading.name == "h2":
                for name in section_attrs:
                    api.section_counts[kind][name] += 1

        if specialized and section_attrs:
            for name, attr in section_attrs.items():
                api.cls(specialized).merge_attr(name, attr)

        # Class-level docstring from the first intro <p> under an h1
        if heading.name == "h1" and targets:
            intro = heading.find_next_sibling("p")
            if intro is None and heading.parent and heading.parent.name == "div":
                intro = heading.parent.find_next_sibling("p")
            if intro and not api.cls(targets[0]).doc:
                api.cls(targets[0]).doc = clean_doc(text_of(intro))

    if path.name == "type_python_pymediahub.html":
        for table in soup.find_all("table"):
            for tr in table.find_all("tr")[1:]:
                cells = tr.find_all(["td", "th"])
                if len(cells) < 2:
                    continue
                if m := MEDIAHUB_ATTR_RE.match(text_of(cells[0])):
                    doc = clean_doc(text_of(cells[2])) if len(cells) > 2 else ""
                    api.cls("PyMediaHub").merge_attr(
                        m.group("name"), Attr(normalize_type(text_of(cells[1])), doc)
                    )


def _common_names(counts: Counter[str]) -> set[str]:
    if not counts:
        return set()
    max_occ = max(counts.values())
    return {n for n, c in counts.items() if c >= max(1, int(max_occ * 0.8))}


def _prune_synthetics(api: ApiModel, base: str, common: set[str]) -> None:
    for name in list(api.classes):
        if name in KNOWN_CLASSES or name == base:
            continue
        if base == "PyNode":
            if is_synthetic_conode(name) or not (name.startswith("Py") and name.endswith("Node")):
                continue
        elif base == "PyCoNode":
            if not is_synthetic_conode(name):
                continue
        else:
            continue
        model = api.classes[name]
        model.attrs = {k: v for k, v in model.attrs.items() if k not in common}
        if not model.attrs and not model.methods:
            del api.classes[name]


def _finalize(api: ApiModel) -> None:
    for base, counts in (("PyNode", api.section_counts.get("PyNode")), ("PyCoNode", api.section_counts.get("PyCoNode"))):
        if base not in api.classes or not counts:
            continue
        common = _common_names(counts)
        api.classes[base].attrs = {k: v for k, v in api.classes[base].attrs.items() if k in common}
        _prune_synthetics(api, base, common)

    # Infer bases
    for name, model in api.classes.items():
        if model.bases:
            continue
        if name in BASES:
            model.bases = [BASES[name]]
        elif name not in KNOWN_CLASSES:
            if is_synthetic_conode(name):
                model.bases = ["PyCoNode"]
            elif name.endswith("Node") and name != "PyNode":
                model.bases = ["PyNode"]

    # PyTime is referenced but undocumented as its own page
    referenced = any(
        a.type == "PyTime" for c in api.classes.values() for a in c.attrs.values()
    )
    if referenced and "PyTime" not in api.classes:
        api.classes["PyTime"] = ClassModel(name="PyTime")

    if "PyMediaHub" in api.classes:
        api.module_attrs["mediahub"] = Attr("PyMediaHub", "MediaHub module entry point.")

    # Drop empties
    for name in list(api.classes):
        m = api.classes[name]
        if not m.attrs and not m.methods and name != "PyTime":
            del api.classes[name]


# ---------------------------------------------------------------------------
# ApiModel → libcst Module
# ---------------------------------------------------------------------------


def _docstring_node(doc: str, *, depth: int = 1) -> cst.SimpleStatementLine:
    """Build a docstring statement.

    ``depth`` is the IndentedBlock nesting of the statement (1=class body,
    2=method body). Continuation lines must include that indent because
    libcst only prefixes the first physical line.
    """
    pad = "    " * depth
    lines = doc.strip().splitlines()
    if len(lines) == 1 and len(lines[0]) <= 72 and '"""' not in lines[0]:
        literal = f'"""{lines[0]}"""'
    else:
        inner = "\n".join(f"{pad}{line}" if line.strip() else "" for line in lines)
        literal = f'"""\n{inner}\n{pad}"""'
    return cst.SimpleStatementLine([cst.Expr(cst.SimpleString(literal))])


def _ann_assign(name: str, typ: str) -> cst.SimpleStatementLine:
    return cst.parse_statement(f"{name}: {typ}")


def _method_def(name: str, method: Method) -> cst.FunctionDef:
    params = [cst.Param(name=cst.Name("self"))]
    for pname, ptype in method.params:
        if pname.startswith("**"):
            params.append(
                cst.Param(
                    name=cst.Name(pname[2:]),
                    star="**",
                    annotation=cst.Annotation(cst.parse_expression(ptype)),
                )
            )
        elif pname.startswith("*"):
            params.append(
                cst.Param(
                    name=cst.Name(pname[1:]),
                    star="*",
                    annotation=cst.Annotation(cst.parse_expression(ptype)),
                )
            )
        else:
            params.append(
                cst.Param(
                    name=cst.Name(pname),
                    annotation=cst.Annotation(cst.parse_expression(ptype)),
                )
            )
    body: list[cst.BaseStatement] = []
    if method.doc:
        body.append(_docstring_node(method.doc, depth=2))
    body.append(cst.SimpleStatementLine([cst.Expr(cst.Ellipsis())]))
    return cst.FunctionDef(
        name=cst.Name(name),
        params=cst.Parameters(params=params),
        body=cst.IndentedBlock(body),
        returns=cst.Annotation(cst.parse_expression(method.returns)),
    )


def _class_def(model: ClassModel) -> cst.ClassDef:
    bases = [cst.Arg(cst.Name(b)) for b in model.bases]
    body: list[cst.BaseStatement] = []
    if model.doc:
        body.append(_docstring_node(model.doc, depth=1))
    for name in sorted(model.attrs):
        attr = model.attrs[name]
        body.append(_ann_assign(name, attr.type))
        if attr.doc:
            body.append(_docstring_node(attr.doc, depth=1))
    for name in sorted(model.methods):
        body.append(_method_def(name, model.methods[name]))
    if not body:
        body.append(cst.SimpleStatementLine([cst.Expr(cst.Ellipsis())]))
    return cst.ClassDef(
        name=cst.Name(model.name),
        bases=bases,
        body=cst.IndentedBlock(body),
    )


def _sort_key(name: str) -> tuple[int, str]:
    if name in {"PyNode", "PyCoNode", "PyMediaHubTab"}:
        return (0, name)
    if name in KNOWN_CLASSES or name == "PyTime":
        return (1, name)
    return (2, name)


def api_to_module(api: ApiModel) -> cst.Module:
    header = (
        '"""Type stubs generated from Autodesk Flame HTML docs under docs/.\n'
        "\n"
        "For comparison with overwrites.pyi / flame-stubs — not applied automatically.\n"
        '"""'
    )
    body: list[cst.BaseStatement] = [
        cst.SimpleStatementLine([cst.Expr(cst.SimpleString(header))]),
        cst.SimpleStatementLine(
            [cst.ImportFrom(module=cst.Name("typing"), names=[cst.ImportAlias(cst.Name("Any"))])]
        ),
        cst.EmptyLine(),
    ]

    for name in sorted(api.classes, key=_sort_key):
        body.append(_class_def(api.classes[name]))
        body.append(cst.EmptyLine())

    for name in sorted(api.module_attrs):
        attr = api.module_attrs[name]
        body.append(_ann_assign(name, attr.type))
        if attr.doc:
            body.append(_docstring_node(attr.doc))

    return cst.Module(body=body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs", type=Path, default=DOCS)
    parser.add_argument("--output", type=Path, default=OUT)
    args = parser.parse_args()

    api = html_to_api(args.docs)
    module = api_to_module(api)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(module.code, encoding="utf-8")

    n_attrs = sum(len(c.attrs) for c in api.classes.values())
    n_docs = sum(1 for c in api.classes.values() for a in c.attrs.values() if a.doc)
    print(f"Wrote {args.output} ({len(api.classes)} classes, {n_attrs} attrs, {n_docs} with docs)")


if __name__ == "__main__":
    main()
