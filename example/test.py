from pathlib import Path

import numpy as np

from lil_aretomo.aretomo import align_tilt_series

TEST_DATA_DIR = Path(__file__).parent.parent / 'test'

align_tilt_series(
    tilt_angles=np.arange(-42,51,3),
    tilt_series_file=TEST_DATA_DIR / 'TS_121.st',
    pixel_size=1.329,
    output_directory=TEST_DATA_DIR / 'output',
    aretomo_executable='/s/ems/s/AreTomo/v1.1.0/AreTomo_1.1.0_Cuda114_03-24-2022',
    do_local_alignments=True,
    #n_patches_xy=(5,6),
    sample_thickness_nanometers=600,
)
