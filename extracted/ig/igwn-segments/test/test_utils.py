import itertools
import random
from functools import reduce
from io import StringIO

import pytest

import igwn_segments as segments
from igwn_segments import utils as segments_utils

from . import verifyutils

#
#  How many times to repeat the algebraic tests
#


algebra_repeats = 8000
algebra_listlength = 200


def test_fromsegwizard():
    """
    Test segwizard parsing.
    """
    data = StringIO("""# This is a comment
 # This is another comment
	# Again a comment
1  10 100 90
2 110 120 10# Here's a comment
3 125 130 5 # Another one

4   0 200 200""")
    correct = segments.segmentlist(
        [
            segments.segment(10, 100),
            segments.segment(110, 120),
            segments.segment(125, 130),
            segments.segment(0, 200),
        ]
    )
    assert segments_utils.fromsegwizard(data, strict=True) == correct


def test_tofromseqwizard():
    """
    Check that the segwizard writing routine's output is parsed
    correctly.
    """
    data = StringIO()
    correct = segments.segmentlist(
        [
            segments.segment(10, 100),
            segments.segment(110, 120),
            segments.segment(125, 130),
            segments.segment(0, 200),
        ]
    )
    segments_utils.tosegwizard(data, correct)
    data.seek(0)
    assert segments_utils.fromsegwizard(data, strict=True) == correct


def test_vote():
    """
    Test vote().
    """
    for i in range(algebra_repeats):
        seglists = []
        for j in range(random.randint(0, 10)):
            seglists.append(
                verifyutils.random_coalesced_list(algebra_listlength, segments)
            )
        n = random.randint(0, len(seglists))
        correct = reduce(
            lambda x, y: x | y,
            (
                votes and reduce(lambda a, b: a & b, votes) or segments.segmentlist()
                for votes in itertools.combinations(seglists, n)
            ),
            segments.segmentlist(),
        )
        assert segments_utils.vote(seglists, n) == correct


def test_fromlalcache(tmp_path):
    """
    Test fromlalcache().
    """
    pytest.importorskip("lal")
    cache = tmp_path / "cache.lcf"
    cache.write_text(
        """
A B 1000000000 100 A-B-1000000000-100.txt
A B 1000000100 100 A-B-1000000100-100.txt
A B 1000000200 800 A-B-1000000200-800.txt
""".strip()
    )
    with cache.open() as file:
        segs = segments_utils.fromlalcache(file)
    assert segs == segments.segmentlist(
        [
            segments.segment(1000000000, 1000000100),
            segments.segment(1000000100, 1000000200),
            segments.segment(1000000200, 1000001000),
        ]
    )
