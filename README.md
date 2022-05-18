# li'l AreTomo

A lightweight (w)rapper for [AreTomo](https://www.biorxiv.org/content/10.1101/2022.02.15.480593v1).

see the script in example directory for the kind of input script you need to run this.

## Installation

It is recommended to install into a fresh virtual environment.

```sh
pip install lil_aretomo
```

### For developers

We use pre-commit to ensure code style and formatting remains consistent.

To install the package in editable mode development dependencies

```sh
pip install -e .[dev]
pre-commit install
```

Flake8, black and isort will then run automatically on each commit.
