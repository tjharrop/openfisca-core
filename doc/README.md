# openfisca-core reference documentation

Source of the [openfisca-core reference documentation](https://openfisca.readthedocs.io/).

## Installing

Preferably work within a virtual environment. To set one up, you can use [pew](https://github.com/berdario/pew).

```sh
cd doc
pip install -r requirements.txt
pip install sphinx-autobuild
```

## Usage

### From reStructuredText to markdown

To convert `.rst` files to `.md` files, you need to install [pandoc](http://pandoc.org/installing.html) on your system.

Then, run:
```sh
pandoc your_file.rst -f rst -t markdown -o your_file.md
```

### From reStructuredText to `.html`

Build `.html` documentation from `.rst` files and serve it on `<http://127.0.0.1:8000>`:

```sh
sphinx-autobuild source build
```
