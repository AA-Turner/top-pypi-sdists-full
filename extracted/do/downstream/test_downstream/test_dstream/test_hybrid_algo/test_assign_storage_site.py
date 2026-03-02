import pytest

from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


@pytest.mark.parametrize("S", [4 << i for i in range(4)])
def test_singleton(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )

    actual = [algo.assign_storage_site(S, T) for T in range(20)]
    expected = [
        dstream.steady_algo.assign_storage_site(S, T) for T in range(20)
    ]

    assert actual == expected


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )

    actual = [algo.assign_storage_site(S, T) for T in range(S)]
    assert sorted(actual) == sorted(range(S))


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
    actual = [algo.assign_storage_site(S, T) for T in range(S)]
    assert sorted(actual) == sorted(range(S))
