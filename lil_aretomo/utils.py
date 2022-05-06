import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict

import numpy as np

def prepare_imod_directory(
        tilt_series_file: Path, 
        tilt_angles: List[float], 
        imod_directory: Path
):
    ts_dir_name = tilt_series_file.stem
    imod_directory.mkdir(exist_ok=True, parents=True)

    tilt_series_file_for_imod = imod_directory / tilt_series_file.name
    force_symlink(tilt_series_file.absolute(), tilt_series_file_for_imod)

    rawtlt_file = imod_directory / f'{ts_dir_name}.rawtlt'
    np.savetxt(rawtlt_file, tilt_angles, fmt='%.2f', delimiter='')
    
#####

def run_batchrun(
        tilt_series_file: Path, 
        imod_directory: Path, 
        binning: float
):
        
    #Rename file .mrc if .st    
    if tilt_series_file.suffix == '.st':
         tilt_series_file = tilt_series_file.rename(tilt_series_file.with_suffix('.mrc'))
    
    output_file_name = Path(f'{tilt_series_file.stem}_aln{tilt_series_file.suffix}')
    
    #with tempfile.TemporaryDirectory() as temporary_directory:
        
	#Run Global AreTomo
        aretomo_command = [
            f'{str(exe)}',
            '-InMrc', f'{tilt_series_file}',
            '-OutMrc', f'{output_file_name}', 
            '-OutBin', f'{binning}',
	    '-AngFile', f'{tilt_series_file.stem}.rawtlt',
	    '-VolZ', f'0',
	    '-OutXF', f'1'
        ]
        subprocess.run(batchrun_command)
	
	#Rename .tlt
        new_output_stem = output_file_name.stem[:-4]
	new_output_name_tlt = Path(new_output_stem).with_suffix('.tlt')
	output_file_name.rename(new_output_name_tlt)
	
#####

def find_binning_factor(
    pixel_size: float
    target_pixel_size: float
) -> int:
    #Find closest IMOD binning to reach target pixel size
    factors = 2 ** np.arange(7)
    binned_pixel_sizes = factors * pixel_size
    delta_pixel = np.abs(binned_pixel_sizes - target_pixel_size)
    binning = factors[np.argmin(delta_pixel)]
    return binning	





