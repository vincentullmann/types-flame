# Types Flame

This package provides stubs for Autodesk Flame.
The major and minor version number of this package corresponds to the Flame version.
However the patch version might change to account for fixes in the stubs.

## Installation

```sh
pip install types-flame
```

## Generation

### Step 1: generate docs from flame

Append the `src/hook` dir to the `DL_PYTHON_HOOK_PATH`.
launch flame

This generates `out/auto_generated.pyi`

### Step 2: load and parse the online docs

```sh
# download the html files
./scrips/download_docs.sh

# parse them
uv run scripts/parse_docs.py
```

this generates `out/from_docs.pyi`

### Step 3: combine the stubs

```sh
uv run scripts/apply_overwrites.py -i out/auto_generated.pyi -i out/from_docs.pyi -i in/overwrites.pyi -o flame-stubs/__init__.pyi
```
