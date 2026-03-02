from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def test_singleton():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )

    expected = [0] * 9
    assert [
        algo._get_span_offset(T, index=0) for T in range(1, 10)
    ] == expected


def test_simple():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )
    expected = [0] * 9
    assert [
        algo._get_span_offset(T, index=0) for T in range(2, 20, 2)
    ] == expected
    expected = [*range(1, 10)]
    assert [
        algo._get_span_offset(T, index=1) for T in range(2, 20, 2)
    ] == expected


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
    expected = [0] * 9
    assert [
        algo._get_span_offset(T, index=0) for T in range(4, 40, 4)
    ] == expected
    expected = [*range(2, 20, 2)]
    assert [
        algo._get_span_offset(T, index=1) for T in range(4, 40, 4)
    ] == expected
    expected = [*range(3, 30, 3)]
    assert [
        algo._get_span_offset(T, index=2) for T in range(4, 40, 4)
    ] == expected
