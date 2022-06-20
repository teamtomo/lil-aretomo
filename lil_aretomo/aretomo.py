from pathlib import Path
from typing import List, Optional, Tuple
from rich.console import Console

from .utils import (
    prepare_alignment_directory,
    align_tilt_series_aretomo,
    find_binning_factor,
    check_aretomo_availability,
    thickness_ang2pix,
)

console = Console(record=True)

def run_aretomo_alignment(
        tilt_series_file: Path,
        tilt_angles: List[float],
        pixel_size: float,
        output_directory: Path,
        aretomo_executable: Optional[Path] = None,
        local_align: Optional[bool] = False,
        target_pixel_size: Optional[float] = 10,
        nominal_rotation_angle: Optional[float] = None,
        n_patches_xy: Optional[Tuple[int, int]] = (5, 4),
        thickness_for_alignment: Optional[float] = 1500,
        correct_tilt_angle_offset: Optional[bool] = False,
        gpu_ids: Optional[Tuple[int,...]] = None	
):
    """Run aretomo alignment on a single tilt-series
    
    Parameters
    ----------
    
    tilt_series_file: file containing tilt-series images
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    output_directory: tilt-series directory.
    (optional) aretomo_executable: path to the AreTomo executable file
    (optional) local_align: carry out local tilt series alignments? Yes or no, default is no. 
    (optional) target_pixel_size: the ideal pixel size at which TSA is carried out. Default is 10A
    (optional) nominal_rotation_angle: initial estimate for the rotation angle of the tilt
    axis. AreTomo does not need this information but it might help.
    (optional) n_patches_xy: if local_align is True, AreTomo will carry out patch tracking. 
    Specify the number of patches in X and Y here as tuple. Default is 5 in X,4 in Y.
    (optional) thickness_for_alignment: thickness in Z in Ang for which AreTomo will use in the alignment.
    This is useful is there is a lot of empty space at the top and bottom of your tomogram.
    See AreTomo manual for full explanation: this sets -AlignZ. Default is 1500.
    (optional) correct_tilt_angle_offset: Apply tilt angle offset correction, yes or no.
    Default is no. See AreTomo manual for full explanation: yes; adds the -TiltCor 1 argument
    (optional) gpu_ids: If you wish to run in parallel over multiple GPUs, enter GPU IDs as tuple e.g. 0 1 2 3
    """
    if check_aretomo_availability() is False:
        e = 'AreTomo is not available for use. Load AreTomo so it can be called from the terminal via: AreTomo.'
        console.log(f'ERROR: {e}')
        raise RuntimeError(e)

    tilt_series_file = prepare_alignment_directory(
        tilt_series_file=tilt_series_file,
        tilt_angles=tilt_angles,
        output_directory=output_directory
    )

    binning = find_binning_factor(
        pixel_size=pixel_size,
        target_pixel_size=target_pixel_size
    )
    
    thickness_for_alignment = thickness_ang2pix(
        pixel_size=pixel_size,
        thickness_for_alignment=thickness_for_alignment
    )

    align_tilt_series_aretomo(
        tilt_series_file=tilt_series_file,
        output_directory=output_directory,
        binning=binning,
        aretomo_executable=aretomo_executable,
        nominal_rotation_angle=nominal_rotation_angle,
        local_alignments=local_align,
        n_patches_xy=n_patches_xy,
        thickness_for_alignment=thickness_for_alignment,
        correct_tilt_angle_offset=correct_tilt_angle_offset,
        gpu_ids=gpu_ids
    )
