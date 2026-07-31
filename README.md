# Types Flame

This package provides stubs for Autodesk Flame.
The major and minor version number of this package corresponds to the Flame version.
However the patch version might change to account for fixes in the stubs.

## Installation

```
pip install types-flame
```

## Generation

### Step 1: generate `out/auto_generated.pyi`

Append the hook dir to the `DL_PYTHON_HOOK_PATH`.
launch flame

### Step 2: add overlay

```sh
uv run apply_overwrites.py out/auto_generated.pyi overwrites.pyi flame-stubs/__init__.pyi
```
