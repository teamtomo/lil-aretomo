from pathlib import Path


class AreTomoOutput:
    def __init__(self, tilt_series_file: Path, reconstruction_file: Path):
        self.tilt_series_file: Path = tilt_series_file
        self.reconstruction_file: Path = reconstruction_file

    @property
    def directory(self) -> Path:
        return self.tilt_series_file.parent

    @property
    def basename(self) -> str:
        return self.tilt_series_file.stem

    @property
    def aln_file(self) -> Path:
        return self.directory / f'{self.basename}.aln'
	
    @property
    def contains_alignment_results(self) -> bool:
        return self.aln_file.exists() 
