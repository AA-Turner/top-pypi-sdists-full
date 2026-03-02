from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def test_singleton():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )

    assert [*map(algo._get_span_scale, range(1, 10))] == [*range(1, 10)]


def test_simple1():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )
    assert [*map(algo._get_span_scale, range(2, 20, 2))] == [*range(1, 10)]


def test_simple2():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
        dstream.tilted_algo,
        3,
    )
    assert [*map(algo._get_span_scale, range(3, 30, 3))] == [*range(1, 10)]


def test_complex():
    algo = algo_class(
        0,
        dstream.steady_algo,
        2,
        dstream.stretched_algo,
        3,
        dstream.steady_algo,
        4,
    )
    assert [*map(algo._get_span_scale, range(4, 40, 4))] == [*range(1, 10)]
