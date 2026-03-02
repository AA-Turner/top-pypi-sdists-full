from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def test_singleton():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )

    assert [*map(algo._get_algo_index, range(10))] == [0] * 10


def test_simple():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )
    assert [*map(algo._get_algo_index, range(10))] == [0, 1] * 5


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
    assert [*map(algo._get_algo_index, range(12))] == [0, 0, 1, 2] * 3
