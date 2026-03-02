import opytional as opyt
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

    expected = [
        *range(S_),
        *(
            opyt.apply_if(base_algo.assign_storage_site(S, T), lpad.__add__)
            for T in range(
                min(
                    2 * S_,
                    opyt.or_value(base_algo.get_ingest_capacity(S), 2 * S_),
                ),
            )
        ),
    ]
    actual = [
        algo.assign_storage_site(S_, T)
        for T in range(
            min(3 * S_, opyt.or_value(algo.get_ingest_capacity(S_), 3 * S_)),
        )
    ]
    assert expected == actual
