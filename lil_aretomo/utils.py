import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

import numpy as np


def prepare_alignment_directory(
        tilt_series_file: Path,
        tilt_angles: List[float],
        output_directory: Path
):
    output_directory.mkdir(exist_ok=True, parents=True)

    # Establish filenames/paths
    tilt_series_filename = tilt_series_file.with_suffix('.mrc').name
    linked_tilt_series_file = output_directory / tilt_series_filename
    rawtlt_file = output_directory / f'{tilt_series_file.stem}.rawtlt'

    # Link tilt series into output directory and write tilt angles into text file
    force_symlink(tilt_series_file.absolute(), linked_tilt_series_file)
    np.savetxt(rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')
    return linked_tilt_series_file


def align_tilt_series_aretomo(
        tilt_series_file: Path,
        output_directory: Path,
        binning: float,
        aretomo_executable: Path,
        nominal_rotation_angle: bool or float,
        local_alignments: bool,
        n_patches_xy: Tuple[int, int],
        thickness_for_alignment: float,
        correct_tilt_angle_offset: bool
):
    output_file_name = Path(
        f'{output_directory}/{tilt_series_file.stem}_aln{tilt_series_file.suffix}')

    aretomo = 'AreTomo' if aretomo_executable is None else str(aretomo_executable)
    command = [
        f'{aretomo}',
        '-InMrc', f'{tilt_series_file}',
        '-OutMrc', f'{output_file_name}',
        '-OutBin', f'{binning}',
        '-AngFile', f'{output_directory}/{tilt_series_file.stem}.rawtlt',
        '-AlignZ', f'{thickness_for_alignment}',
        '-VolZ', '0',
        '-OutXF', '1',
        '-DarkTol', '0.01',
    ]

    if nominal_rotation_angle is not None:
        command.append('-TiltAxis')
        command.append(f'{nominal_rotation_angle}')

    if local_alignments is True:
        command.append('-Patch')
        command.append(f'{n_patches_xy[0]}')
        command.append(f'{n_patches_xy[1]}')

    if correct_tilt_angle_offset:
        command.append('-TiltCor')
        command.append('1')

    subprocess.run(command)

    # Rename .tlt
    tlt_file_name = Path(f'{output_directory}/{tilt_series_file.stem}_aln.tlt')
    new_tlt_stem = tlt_file_name.stem[:-4]
    new_output_name_tlt = Path(f'{output_directory}/{new_tlt_stem}').with_suffix('.tlt')
    tlt_file_name.rename(new_output_name_tlt)


def find_binning_factor(
        pixel_size: float,
        target_pixel_size: float
) -> int:
    # Find closest binning to reach target pixel size
    factors = 2 ** np.arange(7)
    binned_pixel_sizes = factors * pixel_size
    delta_pixel = np.abs(binned_pixel_sizes - target_pixel_size)
    binning = factors[np.argmin(delta_pixel)]
    return binning


def force_symlink(src: Path, link_name: Path):
    """Force creation of a symbolic link, removing any existing file."""
    if link_name.exists():
        os.remove(link_name)
    os.symlink(src, link_name)


def check_aretomo_availability():
    """Check for an installation of AreTomo on the PATH."""
    return shutil.which('AreTomo') is not None
