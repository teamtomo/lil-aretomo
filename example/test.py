from pathlib import Path
import run_aretomo_global_alignment

TEST_DATA_DIR = Path('../test/')

run_patch_tracking_based_alignment(
    tilt_series_file=TEST_DATA_DIR / 'TS_121.st',
    tilt_angles=TEST_DATA_DIR / 'TS_121.rawtlt',
    pixel_size=1.329,
    output_directory=TEST_DATA_DIR / 'output',
    exe='/s/ems/s/AreTomo/v1.1.0/AreTomo_1.1.0_Cuda114_03-24-2022'
)
