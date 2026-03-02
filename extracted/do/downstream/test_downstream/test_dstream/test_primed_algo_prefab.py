from downstream import dstream


def test_primed_0pad0_circular_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_compressing_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_steady_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_sticky_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_stretched_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_stretchedxtc_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_tilted_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad0_tiltedxtc_algo_smoke():
    S = 32 + 0
    assert [
        dstream.primed_0pad0_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_circular_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_compressing_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_steady_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_sticky_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_stretched_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_stretchedxtc_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_tilted_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad4_tiltedxtc_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_0pad4_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_circular_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_compressing_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_steady_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_sticky_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_stretched_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_stretchedxtc_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_tilted_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad8_tiltedxtc_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_0pad8_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_circular_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_compressing_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_steady_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_sticky_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_stretched_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_stretchedxtc_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_tilted_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad16_tiltedxtc_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_0pad16_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_circular_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_compressing_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_steady_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_sticky_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_stretched_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_stretchedxtc_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_tilted_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_0pad32_tiltedxtc_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_0pad32_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_circular_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_compressing_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_steady_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_sticky_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_stretched_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_stretchedxtc_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_tilted_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_4pad0_tiltedxtc_algo_smoke():
    S = 32 + 4
    assert [
        dstream.primed_4pad0_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_circular_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_compressing_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_steady_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_sticky_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_stretched_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_stretchedxtc_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_tilted_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_8pad0_tiltedxtc_algo_smoke():
    S = 32 + 8
    assert [
        dstream.primed_8pad0_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_circular_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_compressing_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_steady_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_sticky_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_stretched_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_stretchedxtc_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_tilted_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_16pad0_tiltedxtc_algo_smoke():
    S = 32 + 16
    assert [
        dstream.primed_16pad0_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_circular_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_circular_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_compressing_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_compressing_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_hybrid_0_steady_1_stretched_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_hybrid_0_steady_1_stretched_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_hybrid_0_steady_1_stretchedxtc_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_hybrid_0_steady_1_stretchedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_hybrid_0_steady_1_tilted_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_hybrid_0_steady_1_tilted_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_hybrid_0_steady_1_tiltedxtc_2_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_hybrid_0_steady_1_tiltedxtc_2_algo.assign_storage_site(
            S, T
        )
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_steady_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_steady_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_sticky_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_sticky_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_stretched_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_stretched_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_stretchedxtc_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_stretchedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_tilted_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_tilted_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]


def test_primed_32pad0_tiltedxtc_algo_smoke():
    S = 32 + 32
    assert [
        dstream.primed_32pad0_tiltedxtc_algo.assign_storage_site(S, T)
        for T in range(S)
    ] == [*range(S)]
