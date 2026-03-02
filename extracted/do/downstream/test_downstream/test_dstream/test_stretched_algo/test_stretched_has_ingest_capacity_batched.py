import numpy as np

from downstream.dstream import stretched_algo as algo


def test_stretched_has_ingest_capacity_batched_fuzz1():
    Ts = np.random.randint(np.iinfo(np.uint64).max, dtype=np.uint64, size=500)
    Ss = 1 << np.random.randint(63, size=500, dtype=np.uint64)

    expected = np.array(
        [algo.has_ingest_capacity(S, T) for S, T in zip(Ss, Ts)], dtype=bool
    )

    actual = algo.has_ingest_capacity_batched(Ss, Ts)
    np.testing.assert_array_equal(actual, expected)

    actual = np.array(
        [
            algo.has_ingest_capacity_batched(S, T).item()
            for S, T in zip(Ss, Ts)
        ],
        dtype=bool,
    )
    np.testing.assert_array_equal(actual, expected)


def test_stretched_has_ingest_capacity_batched_fuzz2():
    Ts = np.random.randint(np.iinfo(np.uint64).max, dtype=np.uint64, size=500)
    S = 1 << np.random.randint(63, dtype=np.uint64)

    expected = np.array(
        [algo.has_ingest_capacity(S, T) for T in Ts], dtype=bool
    )

    actual = algo.has_ingest_capacity_batched(S, Ts)
    np.testing.assert_array_equal(actual, expected)

    actual = np.array(
        [algo.has_ingest_capacity_batched(S, T) for T in Ts], dtype=bool
    )
    np.testing.assert_array_equal(actual, expected)


def test_stretched_has_ingest_capacity_batched_fuzz3():
    T = np.random.randint(np.iinfo(np.uint64).max, dtype=np.uint64)
    Ss = 1 << np.random.randint(63, size=500, dtype=np.uint64)

    expected = np.array(
        [algo.has_ingest_capacity(S, T) for S in Ss], dtype=bool
    )

    actual = algo.has_ingest_capacity_batched(Ss, T)
    np.testing.assert_array_equal(actual, expected)

    actual = np.array(
        [algo.has_ingest_capacity_batched(S, T) for S in Ss], dtype=bool
    )
    np.testing.assert_array_equal(actual, expected)


def test_stretched_has_ingest_capacity_batched_empty():
    empty = np.array([], dtype=int)
    assert algo.has_ingest_capacity_batched(empty, empty).size == 0
    assert algo.has_ingest_capacity_batched(2, empty).size == 0
    assert algo.has_ingest_capacity_batched([2], empty).size == 0
    assert algo.has_ingest_capacity_batched(empty, 100).size == 0
    assert algo.has_ingest_capacity_batched(empty, [100]).size == 0
