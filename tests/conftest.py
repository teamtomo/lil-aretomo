from pathlib import Path

import pytest


@pytest.fixture
def test_data_dir() -> Path:
    return Path(__file__).parent / 'test_data'


@pytest.fixture
def aln_file(test_data_dir) -> Path:
    return test_data_dir / 'example.aln'
