import numpy as np
from nose.tools import assert_raises

import euxfel_bunch_pattern as bp

def test_get_charge():
    a = np.arange(16)
    np.testing.assert_array_equal(bp.get_charge(a), bp.CHARGE_VALUES)

    # Higher bits shouldn't interfere with the charges
    np.testing.assert_array_equal(bp.get_charge(a + (0xff << 4)),
                                  bp.CHARGE_VALUES)

def test_indices_at_destination():
    a = np.arange(9) << 18
    res = bp.indices_at_destination(a, bp.DESTINATION_T4D)
    np.testing.assert_array_equal(res, [4])

    with assert_raises(ValueError):
        # Only DESTINATION_ constants can be used
        bp.indices_at_destination(a, bp.PHOTON_LINE_DEFLECTION)

    with assert_raises(ValueError):
        bp.indices_at_destination(a, bp.DESTINATION_MASK)

def test_indices_at_sase():
    a = np.array([bp.DESTINATION_T4D, bp.DESTINATION_T5D,
                  bp.DESTINATION_T4D + bp.PHOTON_LINE_DEFLECTION])

    np.testing.assert_array_equal(bp.indices_at_sase(a, 1), [0])
    np.testing.assert_array_equal(bp.indices_at_sase(a, 2), [1])
    np.testing.assert_array_equal(bp.indices_at_sase(a, 3), [2])

    with assert_raises(ValueError):
        bp.indices_at_sase(a, 4)
