from downstream.dstream import hybrid_0_circular_11_steady_12_algo as algo


def test_smoke():
    S = 48
    actual = [algo.assign_storage_site(S, T) for T in range(S)]
    assert sorted(actual) == [*range(S)]
