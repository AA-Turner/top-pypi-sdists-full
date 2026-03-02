from downstream.dstream import hybrid_0_tiltedxtc_1_circular_2_algo as algo


def test_smoke():
    S = 32
    actual = [algo.assign_storage_site(S, T) for T in range(S)]
    assert sorted(actual) == [*range(S)]
