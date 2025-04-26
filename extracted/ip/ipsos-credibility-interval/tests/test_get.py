"""Test the get function."""
from ipsos_credibility_interval import get


def _round(v):
    return round(v, 1)


def test_get(tmpdir):
    """Test the table of results outlined by the Ipsos white paper."""
    assert _round(get(2000)) == 2.5
    assert _round(get(1500)) == 2.9
    assert _round(get(1000)) == 3.5
    assert _round(get(750)) == 4.1
    assert _round(get(500)) == 5.0
    assert _round(get(350)) == 6.0
    assert _round(get(200)) == 7.9
    assert _round(get(100)) == 11.2


def test_examples():
    """Test the examples in the docs."""
    assert _round(get(1000, confidence_level=0.99)) == 4.6
    assert _round(get(1000, weight=1.5)) == 3.8
