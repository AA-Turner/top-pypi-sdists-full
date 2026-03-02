import pytest

from downstream._auxlib._inverse_mod_n import inverse_mod_n


def test_inverse_mod_n_valid():
    # Test valid cases: e is a power of 2 and n is odd.

    # For e=2 and n=3: 2*2 % 3 == 1.
    assert inverse_mod_n(2, 3) == 2

    # For e=4 and n=7: 4*2 % 7 == 1.
    assert inverse_mod_n(4, 7) == 2

    # For e=8 and n=15: 8*2 % 15 == 1.
    assert inverse_mod_n(8, 15) == 2

    # For e=1 and n=3: inverse is 1.
    assert inverse_mod_n(1, 3) == 1

    # General odd n (not n+1 power of 2):
    # For e=2 and n=5: 2*3 % 5 == 1.
    assert inverse_mod_n(2, 5) == 3

    # For e=4 and n=9: 4*7 % 9 == 28 % 9 == 1.
    assert inverse_mod_n(4, 9) == 7

    # For e=1 and n=5: inverse is 1.
    assert inverse_mod_n(1, 5) == 1

    # For e=8 and n=9: 8*8 % 9 == 64 % 9 == 1.
    assert inverse_mod_n(8, 9) == 8


def test_invalid_e():
    # Test that if e is not a power of 2, a ValueError is raised.
    with pytest.raises(ValueError):
        inverse_mod_n(3, 7)


def test_invalid_n():
    # Test that if n is even, a ValueError is raised.
    with pytest.raises(ValueError):
        inverse_mod_n(2, 6)
    with pytest.raises(ValueError):
        inverse_mod_n(4, 8)
