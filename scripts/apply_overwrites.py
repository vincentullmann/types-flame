"""Apply handwritten overlays onto auto-generated stubs."""
from __future__ import annotations

import argparse
from pathlib import Path

import libcst as cst
from libcst.codemod import CodemodContext
from libcst.codemod.visitors import ApplyTypeAnnotationsVisitor

ROOT = Path(__file__).parent.parent


def merge_stubs(base: cst.Module, overlay: cst.Module) -> cst.Module:
    context = CodemodContext()
    ApplyTypeAnnotationsVisitor.store_stub_in_context(
        context,
        overlay,
        overwrite_existing_annotations=True,
    )
    return ApplyTypeAnnotationsVisitor(context).transform_module(base)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-b",
        "--base",
        nargs="?",
        type=Path,
        default=ROOT / "out/auto_generated.pyi",
        help="auto-generated stub file",
    )
    parser.add_argument(
        "-i",
        "--overlays",
        action="append",
        type=Path,
        help="overlays to apply",
    )
    parser.add_argument(
        "-o",
        "--output",
        nargs="?",
        type=Path,
        default=ROOT / "flame-stubs/__init__.pyi",
        help="merged output path",
    )
    args = parser.parse_args()

    #######################################
    print("load base:", args.base)
    result = cst.parse_module(args.base.read_text())

    for path in args.overlays:
        print(f"apply {path}")
        overlay = cst.parse_module(path.read_text())
        result = merge_stubs(result, overlay)

    output = args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result.code)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
