from pathlib import Path
from lil_aretomo.aretomo import run_aretomo_alignment

import numpy as np

TEST_DATA_DIR = Path(__file__).parent.parent / 'test'

run_aretomo_alignment(
    tilt_series_file=TEST_DATA_DIR / 'TS_121.st',
    tilt_angles=np.arange(-42,51,3),
    pixel_size=1.329,
    output_directory=TEST_DATA_DIR / 'output',
    exe='/s/ems/s/AreTomo/v1.1.0/AreTomo_1.1.0_Cuda114_03-24-2022',
    local_align=True,
    patch_in_x=6,
    patch_in_y=4,
    correct_tilt_angle_offset=True
)
