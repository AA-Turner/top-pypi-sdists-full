"""Checks of the values customer code passes to the SDK (table and column names, form labels, a decimal's precision, a
file's path), as they are checked on Fivetran: a string takes `str` or UTF-8 `bytes` but not a lone surrogate, an integer
takes anything with `__index__` inside its range, `None` means "not set".
Customers see the exceptions this raises, so the in-process runtime raises the same ones, with the same messages.
"""
import operator

_NOT_A_STRING = "bad argument type for built-in operation"


def text(value, *, unset_if_none=True):
    """A string field set from `value`. `None` leaves the field unset (an empty string) when set in a constructor."""
    if value is None and unset_if_none:
        return ""
    if isinstance(value, str):
        return value.encode("utf-8").decode("utf-8")
    if isinstance(value, bytes):
        return value.decode("utf-8")
    raise TypeError(_NOT_A_STRING)


def map_key(value):
    """A key of a `map<string, ...>` field: like a string, but `None` is an error."""
    return text(value, unset_if_none=False)


def optional_text(value):
    """A string field with presence, set from a constructor argument: `None` leaves it absent."""
    return None if value is None else text(value)


def integer(value, *, bits, signed, unset_if_none=True):
    """An integer field. `None` in a constructor leaves it at 0; assigned to an attribute it is an error."""
    if value is None and unset_if_none:
        return 0
    number = operator.index(value)
    low, high = (-(1 << (bits - 1)), (1 << (bits - 1)) - 1) if signed else (0, (1 << bits) - 1)
    if number < low or number > high:
        # the error names the object it was given when the number fits a C long, and the number itself otherwise
        # (and for a negative value in an unsigned field).
        fits_long = -(1 << 63) <= number < (1 << 63)
        shown = value if fits_long and (signed or number >= 0) else number
        raise ValueError(f"Value out of range: {shown}")
    return number


def boolean(value):
    """A bool field set from a constructor argument: any integer is taken, `None` leaves it unset."""
    if value is None:
        return None
    number = operator.index(value)
    if number < -(1 << 63) or number >= (1 << 63):
        raise OverflowError("Python int too large to convert to C long")
    return bool(number)


def enum(value, names):
    """An enum field set from a constructor argument: an integer in the int32 range, or the name of a value."""
    if value is None:
        return 0
    if isinstance(value, str):
        if value in names:
            return names[value]
        # the whole string is looked up, but the error words it cut at the first NUL (a C string)
        raise ValueError(f'unknown enum label "{value.split(chr(0))[0]}"')
    return integer(value, bits=32, signed=True)


def byte_string(value, *, unset_if_none=True):
    """A bytes field: only `bytes`. `None` in a constructor leaves it empty; inside a map it is an error."""
    if value is None and unset_if_none:
        return b""
    if not isinstance(value, bytes):
        raise TypeError(f"expected bytes, {type(value).__name__} found")
    return value
