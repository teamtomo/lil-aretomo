import pandas as pd

from lil_aretomo.utils import read_aln


def test_read_aln(aln_file_v1_2_0, aln_file_v1_3_0):
    """Check that aln files are correctly parsed."""
    for aln_file in (aln_file_v1_2_0, aln_file_v1_3_0):
        df = read_aln(aln_file)
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (41, 10)
        expected_columns = [
            'SEC', 'ROT', 'GMAG', 'TX', 'TY', 'SMEAN', 'SFIT', 'SCALE', 'BASE', 'TILT'
        ]
    assert all(col in df.columns for col in expected_columns)
