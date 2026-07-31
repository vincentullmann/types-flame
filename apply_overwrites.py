"""Apply handwritten overlays onto auto-generated stubs."""
from __future__ import annotations

import argparse
from pathlib import Path

import libcst as cst
from libcst.codemod import CodemodContext
from libcst.codemod.visitors import ApplyTypeAnnotationsVisitor


ROOT = Path(__file__).parent


def merge_stubs(base_file: Path, overlay_file: Path, output_file: Path) -> None:
    base = cst.parse_module(base_file.read_text())
    overlay = cst.parse_module(overlay_file.read_text())

    context = CodemodContext()
    ApplyTypeAnnotationsVisitor.store_stub_in_context(
        context,
        overlay,
        overwrite_existing_annotations=True,
    )
    merged = ApplyTypeAnnotationsVisitor(context).transform_module(base)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(merged.code)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "base",
        nargs="?",
        type=Path,
        default=ROOT / "flame-stubs" / "__init__.pyi",
        help="Generated stub file",
    )
    parser.add_argument(
        "overlay",
        nargs="?",
        type=Path,
        default=ROOT / "overwrites.pyi",
        help="Handwritten overlay stub",
    )
    parser.add_argument(
        "output",
        nargs="?",
        type=Path,
        default=ROOT / "flame-stubs/__init__.pyi",
        help="Merged output path",
    )
    args = parser.parse_args()

    merge_stubs(args.base, args.overlay, args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
