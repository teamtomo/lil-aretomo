from os import PathLike
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional
from unittest.mock import _patch_dict
import typer

import subprocess

from .utils import (
    prepare_imod_directory,
    run_batchrun,
    find_binning_factor
)


def run_aretomo_alignment(
        tilt_series_file: Path,
        tilt_angles: List[float],
        pixel_size: float,
        output_directory: Path,
	    exe: Path,
        local_align: Optional[bool] = False,
        target_pixel_size: Optional[float] = 10,
	    nominal_rotation_angle: Optional[float] = None,
        patch_in_x: Optional[float] = 5,
        patch_in_y: Optional[float] = 4,
        correct_tilt_angle_offset: Optional[bool] = False
):
    """Run aretomo alignment on a single tilt-series
    
    Parameters
    ----------
    
    tilt_series_file: file containing tilt-series images
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    output_directory: tilt-series directory for IMOD.
    exe: path to the AreTomo executable file
    (optional) local_align: carry out local tilt series alignments? Yes or no, default is no
    (optional) target_pixel_size: the ideal pixel size at which TSA is carried out. Default is 10A
    (optional) nominal_rotation_angle: initial estimate for the rotation angle of the tilt
    axis. AreTomo does not need this information but it might help.
    (optional) patch_in_x: if local_align is True, AreTomo will carry out patch tracking. 
    Specify the number of patches in X here. Default is 5.
    (optional) patch_in_y: same as above, but in Y. Default is 4. 
    (optional) correct_tilt_angle_offset: Apply tilt angle offset correction, yes or no.
    Default is no. See AreTomo manual for full explanation: yes adds the -TiltCor 1 argument.
    
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
	    nominal_rotation_angle=nominal_rotation_angle,
        local_align=local_align,
        patch_in_x=patch_in_x,
        patch_in_y=patch_in_y,
        correct_tilt_angle_offset=correct_tilt_angle_offset
    )
