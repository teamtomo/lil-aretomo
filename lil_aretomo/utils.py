import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Tuple

import mrcfile
import numpy as np
import pandas as pd


def prepare_alignment_directory(
        output_directory: Path,
        tilt_series: np.ndarray,
        tilt_angles: List[float],
        basename: str
):
    output_directory.mkdir(exist_ok=True, parents=True)

    # Establish filenames/paths
    tilt_series_file = output_directory / f'{basename}.mrc'
    rawtlt_file = output_directory / f'{basename}.rawtlt'

    # Write tilt-series and stage angles into output directory
    mrcfile.write(tilt_series_file, tilt_series.astype(np.float32))
    np.savetxt(rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')
    return linked_tilt_series_file


def align_tilt_series_aretomo(
        tilt_series: np.ndarray,
        output_directory: Path,
        binning: float,
        aretomo_executable: Path,
        nominal_rotation_angle: bool or float,
        local_alignments: bool,
        n_patches_xy: Tuple[int, int],
        thickness_for_alignment: int,
        correct_tilt_angle_offset: bool,
        gpu_ids: None or Tuple[int, ...]
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
        '-DarkTol', '0.01',  # this ensures bad images are not automatically removed
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

    if gpu_ids is not None:
        command.append('-Gpu')
        for gpu in gpu_ids:
            command.append(f'{gpu}')

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


def thickness_ang2pix(
        pixel_size: float,
        thickness_for_alignment: float
) -> int:
    thickness_for_alignment = round(thickness_for_alignment / pixel_size)
    return thickness_for_alignment


def read_aln(filename: os.PathLike) -> pd.DataFrame:
    """Read an AreTomo .aln file"""
    df = pd.read_csv(filename, header='infer', skiprows=2, delimiter=r'\s+')

    # '#' character in header line is parsed as a column name
    # drop empty column on the far right and shift column names to the left by 1
    column_names = list(df.columns)
    df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
    df.columns = column_names[1:]
    return df
