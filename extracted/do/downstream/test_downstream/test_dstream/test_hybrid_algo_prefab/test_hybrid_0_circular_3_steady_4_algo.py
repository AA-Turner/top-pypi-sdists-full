from downstream.dstream import hybrid_0_circular_3_steady_4_algo as algo


def test_smoke():
    S = 64
    actual = [algo.assign_storage_site(S, T) for T in range(S)]
    assert sorted(actual) == [*range(S)]
