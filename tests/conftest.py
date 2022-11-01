from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir() -> Path:
    return Path(__file__).parent / 'test_data'


@pytest.fixture
def aln_file_v1_2_0(test_data_dir) -> Path:
    return test_data_dir / 'example_v1_2_0.aln'


@pytest.fixture
def aln_file_v1_3_0(test_data_dir) -> Path:
    return test_data_dir / 'example_v1_3_0.aln'
