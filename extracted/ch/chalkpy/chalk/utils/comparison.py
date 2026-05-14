from typing import Union


def floats_are_close(
    a: Union[float, int],
    b: Union[float, int],
    rel_tolerance: float = 1e-6,
    abs_tolerance: float = 1e-12,
) -> bool:
    """Check if two numeric values are close within the given tolerances.

    Parameters
    ----------
    a
        First value to compare.
    b
        Second value to compare.
    rel_tolerance
        Relative tolerance. Values are considered equal if
        `abs(a - b) <= rel_tolerance * max(abs(a), abs(b))`.
    abs_tolerance
        Absolute tolerance. Values are considered equal if
        `abs(a - b) <= abs_tolerance`.

    Returns
    -------
    bool
        True if values are considered equal (either tolerance is met), False otherwise.
    """
    a_float = float(a)
    b_float = float(b)

    # Handle NaN cases
    if a_float != a_float and b_float != b_float:  # Both NaN
        return True
    if a_float != a_float or b_float != b_float:  # One is NaN
        return False

    # Exact match short circuit
    if a_float == b_float:
        return True

    diff = abs(a_float - b_float)
    # Either tolerance being met counts as a match
    if diff <= abs_tolerance:
        return True
    if diff <= rel_tolerance * max(abs(a_float), abs(b_float)):
        return True

    return False
