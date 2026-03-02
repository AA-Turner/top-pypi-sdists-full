import numpy as np
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

    with pytest.raises(NotImplementedError):
        actual = algo.assign_storage_site_batched(S, np.arange(100))
        expected = dstream.steady_algo.assign_storage_site_batched(
            S, np.arange(100)
        )

        assert (actual == expected).all()


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )

    with pytest.raises(NotImplementedError):
        actual = algo.assign_storage_site_batched(S, np.arange(S))
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
    with pytest.raises(NotImplementedError):
        actual = algo.assign_storage_site_batched(S, np.arange(S))
        assert sorted(actual) == sorted(range(S))
