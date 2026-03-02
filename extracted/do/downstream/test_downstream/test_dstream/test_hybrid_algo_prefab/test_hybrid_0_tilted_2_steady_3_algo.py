from downstream.dstream import hybrid_0_tilted_2_steady_3_algo as algo


def test_smoke():
    S = 48
    actual = [algo.assign_storage_site(S, T) for T in range(S)]
    assert sorted(actual) == [*range(S)]
