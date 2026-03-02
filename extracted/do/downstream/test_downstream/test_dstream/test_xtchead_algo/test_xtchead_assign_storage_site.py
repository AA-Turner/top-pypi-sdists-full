import functools
import itertools as it
from random import randrange as rand
import typing

import pytest

from downstream.dstream import xtchead_algo as algo


def validate_xtchead_site_selection(
    fn: typing.Callable,
) -> typing.Callable:
    """Decorator to validate pre- and post-conditions on site selection."""

    @functools.wraps(fn)
    def wrapper(S: int, T: int) -> typing.Optional[int]:
        assert S.bit_count() == 1  # Assert S is a power of two
        assert 0 <= T  # Assert T is non-negative
        res = fn(S, T)
        assert res is None or 0 <= res < S  # Assert valid output
        return res

    return wrapper


site_selection = validate_xtchead_site_selection(algo.assign_storage_site)


def test_xtchead_site_selection8():
    # fmt: off
    actual = (site_selection(8, T) for T in it.count())
    expected = [
        0, 1, 4, 2, 5, 6, 7, 3,  # T 0-7
        None, None, None, None, None, None, None, 4,  # T 8-15
        None, None, None, None, None, None, None, None,  # T 16-23
        None, None, None, None, None, None, None, 5,  # T 24-31
        None, None, None, None, None, None, None, None, # T 32-39
        None, None, None, None, None, None, None, None, # T 40-47
        None, None, None, None, None, None, None, None, # T 48-55
        None, None, None, None, None, None, None, 6, # T 56-63
        None, None, None, None, None, None, None, None, # T 64-71
        None, None, None, None, None, None, None, None, # T 72-79
        None, None, None, None, None, None, None, None, # T 80-87
        None, None, None, None, None, None, None, None, # T 88-95
        None, None, None, None, None, None, None, None, # T 96-103
        None, None, None, None, None, None, None, None, # T 104-111
        None, None, None, None, None, None, None, None, # T 112-119
        None, None, None, None, None, None, None, 7, # T 120-127
        None, None, None, None, None, None, None, None, # T 128-135
        None, None, None, None, None, None, None, None, # T 136-143
        None, None, None, None, None, None, None, None, # T 144-151
        None, None, None, None, None, None, None, None, # T 152-159
        None, None, None, None, None, None, None, None, # T 160-167
        None, None, None, None, None, None, None, None, # T 168-175
        None, None, None, None, None, None, None, None, # T 176-183
        None, None, None, None, None, None, None, None, # T 184-191
        None, None, None, None, None, None, None, None, # T 192-199
        None, None, None, None, None, None, None, None, # T 200-207
        None, None, None, None, None, None, None, None, # T 208-215
        None, None, None, None, None, None, None, None, # T 216-223
        None, None, None, None, None, None, None, None, # T 224-231
        None, None, None, None, None, None, None, None, # T 232-239
        None, None, None, None, None, None, None, None, # T 240-247
        None, None, None, None, None, None, None, None, # T 248-255
        None, None, None, None, None, None, None, None, # T 256-263
        None, None, None, None, None, None, None, None, # T 264-271
        None, None, None, None, None, None, None, None, # T 272-279
        None, None, None, None, None, None, None, None, # T 280-287
        None, None, None, None, None, None, None, None, # T 288-295
        None, None, None, None, None, None, None, None, # T 296-303
        None, None, None, None, None, None, None, None, # T 304-311
        None, None, None, None, None, None, None, None, # T 312-319
        None, None, None, None, None, None, None, None, # T 320-327
        None, None, None, None, None, None, None, None, # T 328-335
        None, None, None, None, None, None, None, None, # T 336-343
        None, None, None, None, None, None, None, None, # T 344-351
        None, None, None, None, None, None, None, None, # T 352-359
        None, None, None, None, None, None, None, None, # T 360-367
        None, None, None, None, None, None, None, None, # T 368-375
        None, None, None, None, None, None, None, None, # T 376-383
        None, None, None, None, None, None, None, None, # T 384-391
        None, None, None, None, None, None, None, None, # T 392-399
        None, None, None, None, None, None, None, None, # T 400-407
        None, None, None, None, None, None, None, None, # T 408-415
        None, None, None, None, None, None, None, None, # T 416-423
        None, None, None, None, None, None, None, None, # T 424-431
        None, None, None, None, None, None, None, None, # T 432-439
        None, None, None, None, None, None, None, None, # T 440-447
        None, None, None, None, None, None, None, None, # T 448-455
        None, None, None, None, None, None, None, None, # T 456-463
        None, None, None, None, None, None, None, None, # T 464-471
        None, None, None, None, None, None, None, None, # T 472-479
        None, None, None, None, None, None, None, None, # T 480-487
        None, None, None, None, None, None, None, None, # T 488-495
        None, None, None, None, None, None, None, None, # T 496-503
        None, None, None, None, None, None, None, 2, # T 504-511
        None, None, None, None, None, None, None, None, # T 512-519

    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_xtchead_site_selection16():
    # fmt: off
    actual = (site_selection(16, T) for T in it.count())
    expected = [
        0, 1, 5, 2, 6, 7, 8, 3,  # T 0-7
        9, 10, 11, 12, 13, 14, 15, 4,  # T 8-15
        None, None, None, None, None, None, None, None,  # T 16-23
        None, None, None, None, None, None, None, 5,  # T 24-31
    ]
    assert all(x == y for x, y in zip(actual, expected))


def test_xtchead_site_selection_fuzz():
    testS = (1 << s for s in range(1, 33))
    testT = it.chain(range(10**5), (rand(2**128) for _ in range(10**5)))
    for S, T in it.product(testS, testT):
        site_selection(S, T)  # Validated via wrapper


@pytest.mark.parametrize("S", [1 << s for s in range(1, 21)])
def test_xtchead_site_selection_epoch0(S: int):
    actual = {site_selection(S, T) for T in range(S)}
    expected = set(range(S))
    assert actual == expected


def test_xtchead_site_selection_exceeds_capacity():
    with pytest.raises(ValueError):
        algo.assign_storage_site(7, 7)
