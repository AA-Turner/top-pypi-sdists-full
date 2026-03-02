import contextlib

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

    for T in range(10000):
        assert algo.has_ingest_capacity(S, T)


@pytest.mark.parametrize("S", [4 << i for i in range(4)])
def test_singleton2(S: int):
    algo = algo_class(
        0,
        dstream.tilted_algo,
        1,
    )

    assert algo.has_ingest_capacity(S, 0)
    for T in range(10000):
        expected = dstream.tilted_algo.has_ingest_capacity(S, T)
        actual = algo.has_ingest_capacity(S, T)
        assert actual == expected


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple1(S: int):
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )

    assert algo.has_ingest_capacity(S, 0)
    for T in range(10000):
        expected = [pytest.raises(ValueError), contextlib.nullcontext()][
            algo.has_ingest_capacity(S, T)
        ]
        with expected:
            for i in range(min(T, 10)):
                algo.assign_storage_site(S, T - i)


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple2(S: int):
    algo = algo_class(
        0,
        dstream.stretched_algo,
        1,
        dstream.steady_algo,
        2,
    )

    assert algo.has_ingest_capacity(S, 0)
    for T in range(10000):
        expected = [pytest.raises(ValueError), contextlib.nullcontext()][
            algo.has_ingest_capacity(S, T)
        ]
        with expected:
            for i in range(min(T, 10)):
                algo.assign_storage_site(S, T - i)


@pytest.mark.parametrize("S", [8 << i for i in range(4)])
def test_simple3(S: int):
    algo = algo_class(
        0,
        dstream.stretched_algo,
        1,
        dstream.tilted_algo,
        2,
    )

    assert algo.has_ingest_capacity(S, 0)
    for T in range(10000):
        expected = [pytest.raises(ValueError), contextlib.nullcontext()][
            algo.has_ingest_capacity(S, T)
        ]
        with expected:
            for i in range(min(T, 10)):
                algo.assign_storage_site(S, T - i)


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
    assert algo.has_ingest_capacity(S, 0)
    for T in range(10000):
        expected = [pytest.raises(ValueError), contextlib.nullcontext()][
            algo.has_ingest_capacity(S, T)
        ]
        with expected:
            for i in range(min(T, 10)):
                algo.assign_storage_site(S, T - i)
