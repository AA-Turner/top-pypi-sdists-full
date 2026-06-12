import doctest
import math
import pickle
import random

import pytest

from igwn_segments import _segments_c, _segments_py, segmentlistdict

from . import verifyutils

pytestmark = pytest.mark.parametrize(
    "segments",
    [
        pytest.param(_segments_c, id="C"),
        pytest.param(_segments_py, id="Python"),
    ],
)


#
#  How many times to repeat the algebraic tests
#


algebra_repeats = 8000
algebra_listlength = 200


#
# Some useful code.
#


@pytest.fixture
def set1(segments):
    return (
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
        segments.segment(-2, 2),
    )


@pytest.fixture
def set2(segments):
    return (
        segments.segment(-4, -3),
        segments.segment(-4, -2),
        segments.segment(-4, 0),
        segments.segment(-4, 2),
        segments.segment(-4, 4),
        segments.segment(-2, 4),
        segments.segment(0, 4),
        segments.segment(2, 4),
        segments.segment(3, 4),
        segments.segment(-2, 2),
        segments.segment(-1, 1),
        segments.segment(-segments.infinity(), segments.infinity()),
        segments.segment(0, segments.infinity()),
        segments.segment(-segments.infinity(), 0),
    )


#
# Define the components of the test suite.
#


def test_doctests(segments):
    """Run doctests."""
    doctest.testmod(segments, raise_on_error=True, verbose=True)


class TestInfinity:
    def test_math(self, segments):
        a = segments.infinity()
        assert -a == -a
        assert -a < 0
        assert -a < a
        assert 0 > -a
        assert 0 < a
        assert a > -a
        assert a > 0
        assert a == a

    def test__cmp__(self, segments):
        try:
            cmp()
        except NameError:
            # Python 3 does not have cmp() builtin
            def cmp(a, b):
                return (a > b) - (a < b)

        a = segments.infinity()
        assert cmp(-a, -a) == 0
        assert cmp(-a, 0) == -1
        assert cmp(-a, a) == -1
        assert cmp(0, -a) == 1
        assert cmp(0, a) == -1
        assert cmp(a, -a) == 1
        assert cmp(a, 0) == 1
        assert cmp(a, a) == 0

    def test__add__(self, segments):
        a = segments.infinity()
        b = segments.infinity()
        assert (a) + (10) == b
        assert (a) + (-10) == b
        assert (-a) + (10) == -b
        assert (-a) + (-10) == -b
        assert (10) + (a) == b
        assert (-10) + (a) == b
        assert (10) + (-a) == -b
        assert (-10) + (-a) == -b
        assert (a) + (a) == b
        assert (-a) + (-a) == -b

    def test__sub__(self, segments):
        a = segments.infinity()
        b = segments.infinity()
        assert (a) - (10) == b
        assert (a) - (-10) == b
        assert (-a) - (10) == -b
        assert (-a) - (-10) == -b
        assert (10) - (a) == -b
        assert (-10) - (a) == -b
        assert (10) - (-a) == b
        assert (-10) - (-a) == b
        assert (a) - (a) == b
        assert (-a) - (-a) == -b
        assert (a) - (-a) == b
        assert (-a) - (a) == -b

    def test__float__(self, segments):
        a = segments.infinity()
        b = -segments.infinity()
        assert math.isinf(a)
        assert math.isinf(b)


class TestSegment:
    def test__new__(self, segments):
        assert tuple(segments.segment(-2, 2)) == (-2, 2)
        assert tuple(segments.segment(2, -2)) == (-2, 2)
        assert tuple(segments.segment(-segments.infinity(), 2)) == (
            -segments.infinity(),
            2,
        )
        assert tuple(segments.segment(2, -segments.infinity())) == (
            -segments.infinity(),
            2,
        )
        assert tuple(segments.segment(segments.infinity(), 2)) == (
            2,
            segments.infinity(),
        )
        assert tuple(segments.segment(2, segments.infinity())) == (
            2,
            segments.infinity(),
        )
        assert tuple(segments.segment(-segments.infinity(), segments.infinity())) == (
            -segments.infinity(),
            segments.infinity(),
        )

    def test__abs__(self, segments, set2):
        results = (
            1,
            2,
            4,
            6,
            8,
            6,
            4,
            2,
            1,
            4,
            2,
            segments.infinity(),
            segments.infinity(),
            segments.infinity(),
        )
        for r, a in zip(results, set2):
            assert abs(a) == r

    def test_intersects(self, segments, set1, set2):
        results = (
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            True,
            True,
            True,
            True,
            True,
        )
        for r, a, b in zip(results, set1, set2):
            assert a.intersects(b) == r

    def test_connects(self, segments, set1, set2):
        results = (
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            True,
            False,
            False,
            False,
            False,
            False,
            False,
        )
        for r, a, b in zip(results, set1, set2):
            assert a.connects(b) == r

    def test__contains__(self, segments, set1, set2):
        results = (
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            True,
            True,
            False,
            False,
            False,
        )
        for r, a, b in zip(results, set1, set2):
            assert a.__contains__(b) == r
        assert [1, 2] in segments.segment(0, 4)
        assert [1, 6] not in segments.segment(0, 4)
        assert [-1, 2] not in segments.segment(0, 4)
        assert [-1, 6] not in segments.segment(0, 4)
        assert 2 in segments.segment(0, 4)

        # Paraphrasing the documentation for
        # glue.segment.__contains__ in ligo/segments.py: if a is a
        # segment or a sequence of length two, then `a in b` tests
        # if `b[0] <= a[0] <= a[1] <= b[1]`. Otherwise, `a in b`
        # tests if `b[0] <= a <= b[1]`. The following four tests
        # happen to work and return False in Python 2, but they
        # raise a TypeError in Python 3 because Python does not
        # permit comparisons of numbers with sequences. The
        # exception message is "'<' not supported between instances
        # of 'list' and 'int'".

        with pytest.raises(TypeError):
            [] in segments.segment(0, 4)
        with pytest.raises(TypeError):
            [0] in segments.segment(0, 4)
        with pytest.raises(TypeError):
            [2] in segments.segment(0, 4)
        with pytest.raises(TypeError):
            [1, 2, 3] in segments.segment(0, 4)

    def test_disjoint(self, segments, set1, set2):
        results = (+1, 0, 0, 0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0)
        for r, a, b in zip(results, set1, set2):
            assert a.disjoint(b) == r

    def test_contract(self, segments, set2):
        results = (
            segments.segment(-5, -2),
            segments.segment(-4, -2),
            segments.segment(-2, -2),
            segments.segment(-2, 0),
            segments.segment(-2, 2),
            segments.segment(0, 2),
            segments.segment(2, 2),
            segments.segment(2, 4),
            segments.segment(2, 5),
            segments.segment(0, 0),
            segments.segment(-1, 1),
            segments.segment(-segments.infinity(), segments.infinity()),
            segments.segment(2, segments.infinity()),
            segments.segment(-segments.infinity(), -2),
        )
        for r, a in zip(results, set2):
            assert a.contract(2) == r

    def test_typesafety(self, segments):
        x = "segments.segment(10, 20)"
        # unused variable
        # y = "(20, 30)"
        z = "None"

        for op in ("|", "&", "-", "^"):
            for arg1, arg2 in ((x, z), (z, x)):
                expr = f"{arg1} {op} {arg2}"
                with pytest.raises(TypeError):
                    eval(expr)
        # FIXME:  this doesn't work, should it?
        # self.assertEqual(
        #     eval(f"{x} | {y}"), segments.segmentlist([segments.segment(10, 30)])
        # )


class TestSegmentlist:
    def test__sub__(self, segments):
        assert segments.segmentlist([]) - segments.segmentlist(
            []
        ) == segments.segmentlist([])
        assert segments.segmentlist([]) - segments.segmentlist(
            [segments.segment(-1, 1)]
        ) == segments.segmentlist([])
        assert segments.segmentlist([segments.segment(-1, 1)]) - segments.segmentlist(
            [segments.segment(-1, 1)]
        ) == segments.segmentlist([])
        assert segments.segmentlist([]) == segments.segmentlist(
            [segments.segment(-1, 1)]
        ) - segments.segmentlist([segments.segment(-1, 1)])
        # # This next test fails, but I don't know that that's not OK yet
        # assert segments.segmentlist([]) == segments.segmentlist(
        #     [segments.segment(0, 0)]
        # ) - segments.segmentlist([segments.segment(0, 0)])

        assert segments.segmentlist([segments.segment(0, 1)]) - segments.segmentlist(
            [segments.segment(2, 3)]
        ) == segments.segmentlist([segments.segment(0, 1)])
        assert segments.segmentlist([segments.segment(0, 1)]) - segments.segmentlist(
            [segments.segment(2, 3), segments.segment(4, 5)]
        ) == segments.segmentlist([segments.segment(0, 1)])
        assert segments.segmentlist(
            [segments.segment(0, 1), segments.segment(2, 3)]
        ) - segments.segmentlist([segments.segment(2, 3)]) == segments.segmentlist(
            [segments.segment(0, 1)]
        )
        assert segments.segmentlist(
            [segments.segment(0, 1), segments.segment(2, 3)]
        ) - segments.segmentlist([segments.segment(0, 1)]) == segments.segmentlist(
            [segments.segment(2, 3)]
        )
        assert segments.segmentlist(
            [segments.segment(0, 1), segments.segment(2, 3), segments.segment(4, 5)]
        ) - segments.segmentlist([segments.segment(2, 3)]) == segments.segmentlist(
            [segments.segment(0, 1), segments.segment(4, 5)]
        )

        assert segments.segmentlist([segments.segment(0, 2)]) - segments.segmentlist(
            [segments.segment(1, 2)]
        ) == segments.segmentlist([segments.segment(0, 1)])
        assert segments.segmentlist([segments.segment(0, 2)]) - segments.segmentlist(
            [
                segments.segment(0, 0.8),
                segments.segment(0.9, 1.0),
                segments.segment(1.8, 2),
            ]
        ) == segments.segmentlist(
            [segments.segment(0.8, 0.9), segments.segment(1.0, 1.8)]
        )

        assert segments.segmentlist([segments.segment(-10, 10)]) - segments.segmentlist(
            [segments.segment(-15, -5)]
        ) == segments.segmentlist([segments.segment(-5, 10)])
        assert segments.segmentlist([segments.segment(-10, 10)]) - segments.segmentlist(
            [segments.segment(-5, 5)]
        ) == segments.segmentlist([segments.segment(-10, -5), segments.segment(5, 10)])
        assert segments.segmentlist([segments.segment(-10, 10)]) - segments.segmentlist(
            [segments.segment(5, 15)]
        ) == segments.segmentlist([segments.segment(-10, 5)])

        assert segments.segmentlist(
            [
                segments.segment(0, 10),
                segments.segment(20, 30),
                segments.segment(40, 50),
            ]
        ) - segments.segmentlist([segments.segment(5, 45)]) == segments.segmentlist(
            [segments.segment(0, 5), segments.segment(45, 50)]
        )

    def test__invert__(self, segments):
        assert ~segments.segmentlist([]) == segments.segmentlist(
            [segments.segment(-segments.infinity(), segments.infinity())]
        )
        assert ~segments.segmentlist(
            [segments.segment(-segments.infinity(), segments.infinity())]
        ) == segments.segmentlist([])
        assert ~segments.segmentlist([segments.segment(-5, 5)]) == segments.segmentlist(
            [
                segments.segment(-segments.infinity(), -5),
                segments.segment(5, segments.infinity()),
            ]
        )

    def test__and__(self, segments):
        for _ in range(algebra_repeats):
            a = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            b = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            c = a & b
            # make sure __and__ and __sub__ have the
            # correct relationship to one another
            assert a - (a - b) == c
            assert b - (b - a) == c

    def test__or__(self, segments):
        for i in range(algebra_repeats):
            a = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            b = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            c = a | b
            # make sure c is coalesced
            assert verifyutils.iscoalesced(c)
            # make sure c contains all of a
            assert c & a == a
            # make sure c contains all of b
            assert c & b == b
            # make sure c contains nothing except a and b
            assert c - a - b == segments.segmentlist([])

    def test__xor__(self, segments):
        for i in range(algebra_repeats):
            a = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            b = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            c = a ^ b
            # c contains nothing that can be found in
            # the intersection of a and b
            assert not c.intersects(a & b)
            # c contains nothing that cannot be found
            # in either a or b
            assert c - a - b == segments.segmentlist([])
            # that c + the intersection of a and b
            # leaves no part of either a or b
            # unconvered
            assert a - (c | a & b) == segments.segmentlist([])
            assert b - (c | a & b) == segments.segmentlist([])

    def test_protract(self, segments):
        assert segments.segmentlist(
            [segments.segment(3, 7), segments.segment(13, 17)]
        ).protract(3) == segments.segmentlist([segments.segment(0, 20)])

        # confirm that .protract() preserves the type of the
        # segment objects
        class MyCustomSegment(segments.segment):
            pass

        class MyCustomSegmentList(segments.segmentlist):
            def coalesce(self):
                # must override for test, but don't have to
                # implement because test case is too simple
                return self

        assert MyCustomSegment is type(
            MyCustomSegmentList([MyCustomSegment(0, 10)]).protract(1)[0]
        )

    def test_contract(self, segments):
        assert segments.segmentlist(
            [segments.segment(3, 7), segments.segment(13, 17)]
        ).contract(-3) == segments.segmentlist([segments.segment(0, 20)])

        # confirm that .contract() preserves the type of the
        # segment objects
        class MyCustomSegment(segments.segment):
            pass

        class MyCustomSegmentList(segments.segmentlist):
            def coalesce(self):
                # must override for test, but don't have to
                # implement because test case is too simple
                return self

        assert MyCustomSegment is type(
            MyCustomSegmentList([MyCustomSegment(0, 10)]).contract(1)[0]
        )

    def test_intersects(self, segments):
        for i in range(algebra_repeats):
            a = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            b = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            c = a - b
            d = a & b
            if len(c):
                assert not c.intersects(b)
            if len(d):
                assert d.intersects(a)
                assert d.intersects(b)
                assert a.intersects(b)

    def test_extent(self, segments):
        assert segments.segmentlist([(1, 0)]).extent() == segments.segment(0, 1)

    def test_coalesce(self, segments):
        # check that mixed-type coalescing works
        x = segments.segmentlist(
            [segments.segment(1, 2), segments.segment(3, 4), (2, 3)]
        )
        assert x.coalesce() == segments.segmentlist([segments.segment(1, 4)])

        # try a bunch of random segment lists
        for i in range(algebra_repeats):
            a = verifyutils.random_uncoalesced_list(
                random.randint(1, algebra_listlength), segments
            )
            b = segments.segmentlist(a[:]).coalesce()
            assert verifyutils.iscoalesced(b)
            for seg in a:
                assert seg in b
            for seg in a:
                b -= segments.segmentlist([seg])
            assert b == segments.segmentlist([])

    def test_typesafety(self, segments):
        w = "segments.segmentlist([segments.segment(0, 10), segments.segment(20, 30)])"
        # unused variable
        # x = "segments.segment(10, 20)"
        y = "[(10, 20)]"
        z = "None"

        for op in ("|", "&", "-", "^"):
            for arg1, arg2 in (
                # FIXME:  how should these behave?
                # (w, x), (x, w),
                (w, z),
                (z, w),
            ):
                expr = f"{arg1} {op} {arg2}"
                with pytest.raises(TypeError):
                    eval(expr)
        assert eval(f"{w} | {y}") == segments.segmentlist([segments.segment(0, 30)])


class TestSegmentlistdict:
    @staticmethod
    def random_coalesced_segmentlistdict(n, segments):
        seglists = segmentlistdict()
        for key in map(chr, range(65, 65 + n)):
            seglists[key] = verifyutils.random_coalesced_list(
                random.randint(1, algebra_listlength), segments
            )
        return seglists

    def test_extent_all(self, segments):
        a = segmentlistdict(
            {
                "H1": segments.segmentlist(),
                "L1": segments.segmentlist([segments.segment(25, 35)]),
            }
        )
        assert a.extent_all() == segments.segment(25, 35)

    def test_intersects(self, segments):
        a = segmentlistdict(
            {
                "H1": segments.segmentlist(
                    [segments.segment(0, 10), segments.segment(20, 30)]
                )
            }
        )
        b = segmentlistdict(
            {
                "H1": segments.segmentlist([segments.segment(5, 15)]),
                "L1": segments.segmentlist([segments.segment(25, 35)]),
            }
        )
        c = segmentlistdict(
            {
                "V1": segments.segmentlist(
                    [segments.segment(7, 13), segments.segment(27, 40)]
                )
            }
        )

        assert a.intersects(b)
        assert b.intersects(a)
        assert a.intersects(a)
        assert not a.intersects(c)
        assert not b.intersects(segmentlistdict({}))
        assert not segmentlistdict({}).intersects(segmentlistdict({}))

        assert not a.intersects_all(b)
        assert b.intersects_all(a)

        assert a.all_intersects(b)
        assert not b.all_intersects(a)

        assert not a.all_intersects_all(b)

    def test_pickle(self, segments):
        a = segmentlistdict(
            {
                "H1": segments.segmentlist(
                    [segments.segment(0, 10), segments.segment(20, 30)]
                )
            }
        )
        a.offsets["H1"] = 10.0
        pickle.loads(pickle.dumps(a, protocol=0)) == a
        pickle.loads(pickle.dumps(a, protocol=1)) == a
        pickle.loads(pickle.dumps(a, protocol=2)) == a

    def test_vote(self, segments):
        seglists = self.random_coalesced_segmentlistdict(15, segments)
        seglists.vote(seglists, 6)

    def test_intersection(self, segments):
        seglists = self.random_coalesced_segmentlistdict(15, segments)
        keys = ("A", "B", "C", "D")
        seglists.intersection(keys)
