
from html5rdf.filters.optionaltags import Filter


def test_empty():
    assert list(Filter([])) == []
