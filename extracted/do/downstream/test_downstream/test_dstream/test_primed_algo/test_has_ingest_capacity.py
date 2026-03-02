import pytest

from downstream import dstream
from downstream.dstream import primed_algo as algo_class


@pytest.mark.parametrize(
    "base_algo",
    [
        dstream.circular_algo,
        dstream.compressing_algo,
        dstream.sticky_algo,
        dstream.hybrid_0_steady_1_tilted_2_algo,
        dstream.hybrid_0_steady_1_tiltedxtc_2_algo,
        dstream.stretched_algo,
        dstream.stretchedxtc_algo,
        dstream.tilted_algo,
        dstream.tiltedxtc_algo,
    ],
)
@pytest.mark.parametrize("lpad", [0, 4, 8])
@pytest.mark.parametrize("rpad", [0, 4, 8])
@pytest.mark.parametrize("S", [4 << i for i in range(4)])
def test_vs_base(base_algo: object, lpad: int, rpad: int, S: int):
    algo = algo_class(algo=base_algo, lpad=lpad, rpad=rpad)
    S_ = S + lpad + rpad

    actual = algo.get_ingest_capacity(S_)
    if actual is None:
        assert algo.has_ingest_capacity(S_, 424242424242424)
    else:
        assert algo.has_ingest_capacity(S_, actual - 1)
        assert not algo.has_ingest_capacity(S_, actual)
