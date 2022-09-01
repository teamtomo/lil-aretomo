# li'l AreTomo

A lightweight Python API for [AreTomo](https://www.biorxiv.org/content/10.1101/2022.02.15.480593v1).

## Installation

It is recommended to install into a fresh virtual environment.

```sh
pip install lil_aretomo
```

## Usage

```python
import numpy as np
import mrcfile
from lil_aretomo import align_tilt_series

tilt_series = mrcfile.read('my_tilt_series.mrc')

align_tilt_series(
    tilt_series=tilt_series,
    tilt_angles=np.linspace(-60, 60, 41),
    pixel_size=1.35,  # angstroms per pixel
    sample_thickness_nanometers=2000,  # angstroms
    correct_tilt_angle_offset=True,
    basename='TS_01',  # basename for files passed to AreTomo
    output_directory='TS_01_AreTomo',
    skip_if_completed=False # set to True to skip if results from a previous alignment are present
)
```

### For developers

We use pre-commit to ensure code style and formatting remains consistent.

To install the package in editable mode development dependencies

```sh
pip install -e .[dev]
pre-commit install
```

Flake8, black and isort will then run automatically on each commit.
