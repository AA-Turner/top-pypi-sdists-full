from copy import deepcopy
import random
import types

import numpy as np
import opytional as opyt
import pytest

from downstream.dstream import steady_algo, stretched_algo, tilted_algo
from downstream.dsurf import Surface


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32])
def test_Surface(algo: types.ModuleType, S: int) -> None:
    surface = Surface(algo, S)
    assert surface.T == 0
    assert [*surface] == [None] * surface.S
    assert [*surface.lookup()] == [None] * surface.S

    for T in range(100):
        site = surface.ingest_one(T)
        if site is not None:
            assert surface[site] == T
        assert [*surface] == [*surface.lookup()]
        assert [*zip(surface.lookup(), surface)] == [
            *surface.lookup_zip_items()
        ]


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32, np.empty(32, dtype=np.uint32)])
@pytest.mark.parametrize("step_size", [1, 5, 25, 50])
def test_Surface_ingest_many(
    algo: types.ModuleType, S: int, step_size: int
) -> None:
    single_surface = Surface(algo, S)
    multi_surface = Surface(algo, S)
    num_iterations = min(
        (
            opyt.apply_if_or_value(
                algo.get_ingest_capacity(single_surface.S),
                lambda x: x // step_size // 2,
                100,
            ),
            100,
        )
    )
    for T in range(num_iterations):
        for i in range(step_size):
            single_surface.ingest_one(T * step_size + i)
        multi_surface.ingest_many(step_size, lambda x: x)
        assert single_surface == multi_surface


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32, np.empty(32, dtype=np.uint32)])
def test_Surface_ingest_none(algo: types.ModuleType, S: int):
    surf = Surface(algo, S)
    for T in range(100):
        surf.ingest_one(T)
        new_surf = deepcopy(surf)
        new_surf.ingest_many(0, lambda _: None)
        assert new_surf == surf


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [8, 16, 32, np.empty(32, dtype=np.uint32)])
def test_ingest_cap(algo: types.ModuleType, S: int):
    surf = Surface(algo, S)
    cap = algo.get_ingest_capacity(surf.S)
    if cap is None:
        return
    with pytest.raises(AssertionError):
        Surface(algo, S).ingest_many(cap + 1, lambda _: 1)
    surf.ingest_many(cap, lambda _: 1)
    with pytest.raises(AssertionError):
        surf.ingest_one(1)


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("S", [32, np.empty(32, dtype=np.uint32)])
@pytest.mark.parametrize("step_size", [1, 5, 25, 50])
def test_ingest_items_relative_times(
    algo: types.ModuleType, S: int, step_size: int
):
    surf_absolute = Surface(algo, S)
    surf_relative = Surface(algo, S)
    for T in range(100):
        surf_absolute.ingest_many(step_size, lambda x: x)
        surf_relative.ingest_many(
            step_size, lambda x: T * step_size + x, use_relative_time=True
        )
        assert surf_absolute == surf_relative


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("item_bitwidth", [1, 2, 4, 8, 16, 64])
@pytest.mark.parametrize("S", [32, np.zeros(32, dtype=np.uint64)])
def test_serialization_unsigned(
    algo: types.ModuleType,
    item_bitwidth: int,
    S: int,
):
    S = deepcopy(S)
    surf = Surface(algo, S)
    if None in surf:
        with pytest.raises(NotImplementedError):
            surf.to_hex(item_bitwidth=item_bitwidth)
    else:
        assert (
            Surface.from_hex(
                surf.to_hex(item_bitwidth=item_bitwidth),
                algo,
                S=surf.S,
                storage_bitwidth=item_bitwidth * surf.S,
            )
            == surf
        )

    max_val = 2**item_bitwidth - 1
    surf.ingest_many(surf.S * 3, lambda x: random.randint(0, max_val))
    assert (
        Surface.from_hex(
            surf.to_hex(item_bitwidth=item_bitwidth),
            algo,
            S=surf.S,
            storage_bitwidth=item_bitwidth * surf.S,
        )
        == surf
    )

    surf.ingest_many(surf.S, lambda x: x % max_val)
    assert (
        Surface.from_hex(
            surf.to_hex(item_bitwidth=item_bitwidth),
            algo,
            S=surf.S,
            storage_bitwidth=item_bitwidth * surf.S,
        )
        == surf
    )


@pytest.mark.parametrize("algo", [steady_algo, stretched_algo, tilted_algo])
@pytest.mark.parametrize("item_bitwidth", [8, 16, 64])
@pytest.mark.parametrize("S", [32, np.zeros(32, dtype=np.int64)])
def test_serialization_signed(
    algo: types.ModuleType,
    item_bitwidth: int,
    S: int,
):
    S = deepcopy(S)
    surf = Surface(algo, S)
    if None in surf:
        with pytest.raises(NotImplementedError):
            surf.to_hex(item_bitwidth=item_bitwidth)
    else:
        assert (
            Surface.from_hex(
                surf.to_hex(item_bitwidth=item_bitwidth),
                algo,
                S=surf.S,
                storage_bitwidth=item_bitwidth * surf.S,
            )
            == surf
        )

    min_val = -(2 ** (item_bitwidth - 1))
    max_val = 2 ** (item_bitwidth - 1) - 1
    surf.ingest_many(surf.S * 3, lambda x: random.randint(min_val, max_val))
    if min(surf) < 0:
        with pytest.raises(NotImplementedError):
            surf.to_hex(item_bitwidth=item_bitwidth)


@pytest.mark.parametrize("item_bitwidth", [64])
@pytest.mark.parametrize("dstream_T_bitwidth", [4, 8, 16, 64])
def test_to_hex(item_bitwidth: int, dstream_T_bitwidth: int):

    item_strings = [
        "000000000000aafe",
        "123456789abc0def",
        "000000005619ab3d",
        "000000000000008a",
    ]
    T_string = "000000000000feb1"
    test_surface = Surface(
        steady_algo, [0xAAFE, 0x123456789ABC0DEF, 0x5619AB3D, 0x8A], 0xFEB1
    )

    expected_item_strings = [x[-(item_bitwidth // 4) :] for x in item_strings]
    expected_T_string = T_string[-(dstream_T_bitwidth // 4) :]
    assert int(expected_T_string, base=16) == int(
        hex(int(T_string, base=16) % 2**dstream_T_bitwidth), base=16
    )
    if int(test_surface.T).bit_length() > dstream_T_bitwidth:
        with pytest.raises(ValueError):
            test_surface.to_hex(
                item_bitwidth=item_bitwidth, T_bitwidth=dstream_T_bitwidth
            )
    else:
        assert test_surface.to_hex(
            item_bitwidth=item_bitwidth, T_bitwidth=dstream_T_bitwidth
        ) == (expected_T_string + "".join(expected_item_strings))
