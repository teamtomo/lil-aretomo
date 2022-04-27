import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict

import numpy as np

def prepare_imod_directory(
        tilt_series_file: Path, tilt_angles: List[float], imod_directory: Path
):
    root_name = tilt_series_file.stem
    imod_directory.mkdir(exist_ok=True, parents=True)

    tilt_series_file_for_imod = imod_directory / tilt_series_file.name
    force_symlink(tilt_series_file.absolute(), tilt_series_file_for_imod)

    rawtlt_file = imod_directory / f'{root_name}.rawtlt'
    np.savetxt(rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')

def force_symlink(src: Path, link_name: Path):
    """Force creation of a symbolic link, removing any existing file."""
    if link_name.exists():
        os.remove(link_name)
    os.symlink(src, link_name)
