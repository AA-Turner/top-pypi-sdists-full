from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def test_singleton():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )

    assert [algo._get_adj_T(T, index=0) for T in range(10)] == [*range(10)]


def test_simple():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )
    expected = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5]
    assert [algo._get_adj_T(T, index=0) for T in range(10)] == expected

    expected = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]
    assert [algo._get_adj_T(T, index=1) for T in range(10)] == expected


def test_complex1():
    algo = algo_class(
        0,
        dstream.steady_algo,
        2,
        dstream.stretched_algo,
        3,
        dstream.steady_algo,
        4,
    )
    expected = [0, 1, 2, 2, 2, 3, 4, 4, 4, 5]
    assert [algo._get_adj_T(T, index=0) for T in range(10)] == expected

    expected = [0, 0, 0, 1, 1, 1, 1, 2, 2, 2]
    assert [algo._get_adj_T(T, index=1) for T in range(10)] == expected

    expected = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2]
    assert [algo._get_adj_T(T, index=2) for T in range(10)] == expected


def test_complex2():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        3,
        dstream.steady_algo,
        4,
    )
    expected = [0, 1, 1, 1, 1, 2, 2, 2, 2, 3]
    assert [algo._get_adj_T(T, index=0) for T in range(10)] == expected

    expected = [0, 0, 1, 2, 2, 2, 3, 4, 4, 4]
    assert [algo._get_adj_T(T, index=1) for T in range(10)] == expected

    expected = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2]
    assert [algo._get_adj_T(T, index=2) for T in range(10)] == expected
