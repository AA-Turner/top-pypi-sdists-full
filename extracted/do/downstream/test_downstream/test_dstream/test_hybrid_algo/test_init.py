from downstream import dstream
from downstream.dstream import hybrid_algo as algo_class


def test_singleton():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
    )
    assert algo._algos == [dstream.steady_algo]
    assert algo._fenceposts == [0, 1]
    assert algo._chunk_algo_indices == [0]
    assert algo.__name__ == "hybrid_0_steady_1_algo"


def test_simple():
    algo = algo_class(
        0,
        dstream.steady_algo,
        1,
        dstream.stretched_algo,
        2,
    )
    assert algo._algos == [dstream.steady_algo, dstream.stretched_algo]
    assert algo._fenceposts == [0, 1, 2]
    assert algo._chunk_algo_indices == [0, 1]
    assert algo.__name__ == "hybrid_0_steady_1_stretched_2_algo"


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
    assert algo._algos == [
        dstream.steady_algo,
        dstream.stretched_algo,
        dstream.steady_algo,
    ]
    assert algo._fenceposts == [0, 2, 3, 4]
    assert algo._chunk_algo_indices == [0, 0, 1, 2]
    assert algo.__name__ == "hybrid_0_steady_2_stretched_3_steady_4_algo"
