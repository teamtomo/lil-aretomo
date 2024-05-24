import subprocess
from os import PathLike
from pathlib import Path
from typing import Optional, Tuple, Sequence

import numpy as np

from .output import AreTomoOutput
from .utils import check_aretomo_on_path, prepare_output_directory, get_aretomo_command


def align_tilt_series(
        tilt_series: np.ndarray,
        tilt_angles: Sequence[float],
        pixel_size: float,
        basename: str,
        output_directory: PathLike,
        sample_thickness_nanometers: float = 200,
        do_local_alignments: bool = False,
        n_patches_xy: Optional[Tuple[int, int]] = None,
        output_pixel_size: Optional[float] = 10,
        nominal_rotation_angle: Optional[float] = None,
        correct_tilt_angle_offset: bool = False,
        gpu_ids: Optional[Sequence[int]] = None,
        skip_if_completed: bool = False,
        executable: Optional[str]='AreTomo'
) -> AreTomoOutput:
    """Align a single-axis tilt-series using AreTomo.

    Parameters
    ----------
    tilt_series: (n, y, x) array of tilt images.
    tilt_angles: nominal stage tilt angles.
    pixel_size: 2D pixel spacing in Angstroms per pixel.
    basename: basename for output files.
    output_directory: directory for output files.
    sample_thickness_nanometers: expected thickness of the sample in nanometers.
    do_local_alignments: flag controlling whether or not local alignments are performed.
    output_pixel_size: pixel size of the reconstructed tomogram.
    nominal_rotation_angle: (optional) estimate of the angle between the Y-axis and the tilt-axis.
        CCW is positive.
    n_patches_xy: number of patches in each dimension to use for local alignments.
    correct_tilt_angle_offset: flag controlling whether or not to correct for sample tilt in the output.
    gpu_ids: integer ids for GPUs on the system (zero indexed).
    skip_if_completed: skip alignment if previous results found.
    """
    if check_aretomo_on_path(executable) is False:
        raise RuntimeError("AreTomo executable was not found. \
        Put 'AreTomo' on the PATH to proceed.")
    if do_local_alignments is True and n_patches_xy is None:
        raise RuntimeError('Must set n_patches_xy to perform local alignments')
    output_directory = Path(output_directory)
    tilt_series_file, tilt_angle_file = prepare_output_directory(
        tilt_series=tilt_series,
        tilt_angles=tilt_angles,
        basename=basename,
        pixel_size=pixel_size,
        directory=output_directory,
    )
    reconstruction_file = output_directory / f'{basename}_reconstruction.mrc'
    command = get_aretomo_command(
        tilt_series_file=tilt_series_file,
        tilt_angle_file=tilt_angle_file,
        reconstruction_file=reconstruction_file,
        nominal_tilt_axis_angle=nominal_rotation_angle,
        expected_sample_thickness_px=int((sample_thickness_nanometers * 10) // pixel_size),
        binning_factor=output_pixel_size / pixel_size,
        correct_tilt_angle_offset=correct_tilt_angle_offset,
        do_local_alignments=do_local_alignments,
        n_patches_xy=n_patches_xy,
        gpu_ids=gpu_ids,
        executable=executable
    )
    aretomo_output = AreTomoOutput(tilt_series_file=tilt_series_file, reconstruction_file=reconstruction_file)
    if aretomo_output.contains_alignment_results is False or skip_if_completed is False:
        with open(output_directory / 'log.txt', mode='w') as log:
            subprocess.run(command, stdout=log, stderr=log)
        if aretomo_output.contains_alignment_results is False:
            raise RuntimeError(f'{basename} failed to align correctly.')
    return aretomo_output

