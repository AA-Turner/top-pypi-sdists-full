from inspect import getdoc

import pytest

from igwn_segments import _segments_c, _segments_py


def deep_getattr(obj, name):
    for attr in name.split("."):
        obj = getattr(obj, attr)
    return obj


@pytest.mark.parametrize(
    "key",
    [
        "infinity",
        "segment.connects",
        "segment.disjoint",
        "segment.intersects",
        "segment",
        "segmentlist.coalesce",
        "segmentlist.contract",
        "segmentlist.extent",
        "segmentlist.find",
        "segmentlist.intersects_segment",
        "segmentlist.intersects",
        "segmentlist.protract",
        "segmentlist.shift",
        "segmentlist.value_slice_to_index",
        "segmentlist",
    ],
)
def test_docstrings_match(key):
    """Test that docstrings match between the C and Python implementations."""
    doc_c, doc_py = [
        getdoc(deep_getattr(mod, key)) for mod in [_segments_c, _segments_py]
    ]
    assert doc_c == doc_py
