"""Test the module."""
import pytest

from atcf_data_parser import get_dataframe


@pytest.mark.vcr()
def test_get_dataframe():
    """Test some simple math."""
    url = "https://ftp.nhc.noaa.gov/atcf/aid_public/aep182023.dat.gz"
    df = get_dataframe(url)
    assert len(df) > 100
