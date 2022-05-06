from os import PathLike
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
import typer

import subprocess

from utils import (
    prepare_imod_directory,
    run_batchrun,
    find_binning_factor
)


def run_aretomo_global_alignment(
        tilt_series_file: Path,
        tilt_angles: List[float],
        pixel_size: float,
        output_directory: Path,
	exe: Path,
        target_pixel_size: Optional[float] = 10,
	nominal_rotation_angle: Optional[float] = None
):
    """Run aretomo alignment on a single tilt-series
    
    Parameters
    ----------
    
    tilt_series_file: file containing tilt-series images
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    output_directory: tilt-series directory for IMOD.
    exe: path to the AreTomo executable file
    (optional) nominal_rotation_angle: initial estimate for the rotation angle of the tilt
    axis. AreTomo does not need this information but it might help.
    """

    prepare_imod_directory(
        tilt_series_file=tilt_series_file,
        tilt_angles=tilt_angles,
        imod_directory=output_directory
    )
    
    binning=find_binning_factor(
        pixel_size=pixel_size,
        target_pixel_size=target_pixel_size
    )
    
    run_batchrun(
        tilt_series_file=tilt_series_file,
        imod_directory=output_directory,
	binning=binning,
        exe=exe,
	nominal_rotation_angle=nominal_rotation_angle
    )




