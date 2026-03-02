import pytest

from downstream.dstream import stretched_algo as algo


def stretched_has_ingest_capacity_naive(S: int, T: int) -> bool:
    ingest_capacity = algo.get_ingest_capacity(S)
    return ingest_capacity is None or T < ingest_capacity


@pytest.mark.parametrize("S", [1, 2, 3, 4, 5, 8, 16, 32, 64, 128, 256, 512])
def test_stretched_has_ingest_capacity_vs_naive(S: int):
    for T in range(2**16):
        actual = algo.has_ingest_capacity(S, T)
        expected = stretched_has_ingest_capacity_naive(S, T)
        assert actual == expected
