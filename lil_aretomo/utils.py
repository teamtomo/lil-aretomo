import shutil
import os
from pathlib import Path
from typing import List, Tuple, Optional, Sequence

import mrcfile
import numpy as np
import pandas as pd


def prepare_output_directory(
        directory: Path,
        tilt_series: np.ndarray,
        tilt_angles: List[float],
        basename: str,
        pixel_size: float,
) -> Tuple[Path, Path]:
    """Create an output directory and write input files for AreTomo."""
    directory.mkdir(exist_ok=True, parents=True)

    tilt_series_file = directory / f'{basename}.mrc'
    data_on_disk_shape = None
    if tilt_series_file.exists():
        with mrcfile.open(tilt_series_file, header_only=True) as mrc:
            data_on_disk_shape = (mrc.header.nz, mrc.header.ny, mrc.header.nx)
    if not np.array_equal(tilt_series.shape, data_on_disk_shape):
        mrcfile.write(
            tilt_series_file,
            tilt_series.astype(np.float32),
            voxel_size=(pixel_size, pixel_size, 1),
            overwrite=True
        )

    rawtlt_file = directory / f'{basename}.rawtlt'
    np.savetxt(rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')

    return tilt_series_file, rawtlt_file


def get_aretomo_command(
        tilt_series_file: Path,
        tilt_angle_file: Path,
        reconstruction_file: Path,
        expected_sample_thickness_px: int,
        binning_factor: float,
        correct_tilt_angle_offset: bool = True,
        nominal_tilt_axis_angle: Optional[float] = None,
        do_local_alignments: bool = True,
        n_patches_xy: Optional[Tuple[int, int]] = None,
        gpu_ids: Optional[Sequence[int]] = None,
        executable: Optional[str] = 'AreTomo',
) -> List[str]:
    """Generate a command which can be used to run AreTomo."""
    command = [
        f'{executable}',
        '-InMrc', f'{tilt_series_file}',
        '-OutMrc', f'{reconstruction_file}',
        '-OutBin', f'{binning_factor:.3f}',
        '-AngFile', f'{tilt_angle_file}',
        '-AlignZ', f'{expected_sample_thickness_px}',
        '-VolZ', f'{int(1.5 * expected_sample_thickness_px)}',
        '-DarkTol', '0.00000000000000001',  # this ensures bad images are not automatically removed
    ]
    if nominal_tilt_axis_angle is not None:
        command += ['-TiltAxis', f'{nominal_tilt_axis_angle}']
    if do_local_alignments is True:
        command += ['-Patch', f'{n_patches_xy[0]}', f'{n_patches_xy[1]}']
    if correct_tilt_angle_offset is True:
        command += ['-TiltCor', '1']
    if gpu_ids is not None:
        command += ['-Gpu'] + [f'{gpu_id}' for gpu_id in gpu_ids]
    return command


def check_aretomo_on_path(executable: Optional[str] = 'AreTomo'):
    """Check the PATH for AreTomo."""
    return shutil.which(executable) is not None


def read_aln(filename: os.PathLike) -> pd.DataFrame:
    """Read an AreTomo .aln file"""
    with open(filename, 'r') as f:
        lines_starting_with_hash = 0
        for line in f.readlines():
            if line.startswith('#'):
                lines_starting_with_hash += 1
            else:
                break
    lines_to_skip = lines_starting_with_hash - 1
    df = pd.read_csv(filename, header='infer', skiprows=lines_to_skip, delimiter=r'\s+')

    # '#' character in header line is parsed as a column name
    # drop empty column on the far right and shift column names to the left by 1
    column_names = list(df.columns)
    df.drop(df.columns[len(df.columns) - 1], axis=1, inplace=True)
    df.columns = column_names[1:]
    return df
