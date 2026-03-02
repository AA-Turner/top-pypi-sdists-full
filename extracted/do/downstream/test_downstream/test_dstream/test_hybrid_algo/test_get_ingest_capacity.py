import pytest

from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


@pytest.mark.parametrize("S", [4 << i for i in range(4)])
def test_singleton1(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )

    assert algo.get_ingest_capacity(S) is None


@pytest.mark.parametrize("S", [4 << i for i in range(4)])
def test_singleton2(S: int):
    algo = algo_class(
        0,
        dstream.tilted_algo,
        1,
    )

    actual = algo.get_ingest_capacity(S)
    expected = dstream.tilted_algo.get_ingest_capacity(S)
    assert actual == expected

    assert actual > 0
    assert algo.has_ingest_capacity(S, actual - 1)
    assert not algo.has_ingest_capacity(S, actual)


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple1(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )

    actual = algo.get_ingest_capacity(S)
    expected = 2 * dstream.stretched_algo.get_ingest_capacity(S // 2) + 1
    assert actual == expected

    assert actual > 0
    assert algo.has_ingest_capacity(S, actual - 1)
    assert not algo.has_ingest_capacity(S, actual)


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple2(S: int):
    algo = algo_class(
        0,
        dstream.stretched_algo,
        1,
        dstream.steady_algo,
        2,
    )

    actual = algo.get_ingest_capacity(S)
    expected = 2 * dstream.stretched_algo.get_ingest_capacity(S // 2)
    assert actual == expected

    assert actual > 0
    assert algo.has_ingest_capacity(S, actual - 1)
    assert not algo.has_ingest_capacity(S, actual)


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_complex(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        2,
        dstream.stretched_algo,
        3,
        dstream.steady_algo,
        4,
    )
    actual = algo.get_ingest_capacity(S)
    expected = 4 * dstream.stretched_algo.get_ingest_capacity(S // 4) + 2
    assert actual == expected

    assert actual > 0
    assert algo.has_ingest_capacity(S, actual - 1)
    assert not algo.has_ingest_capacity(S, actual)
