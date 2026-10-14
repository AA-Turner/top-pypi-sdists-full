"""Shared return_type coercion for the AI-backed read helpers.

The recorded query carries the type the test author expects back. The endpoint
answers in whatever shape it likes, so the binding coerces locally — a query
recorded as a number must reach a numeric assertion as a number, not as "42".

An unrecognised return_type raises rather than passing the value through: a typo
in a recorded return_type would otherwise silently degrade to string comparison.
An absent one (None or empty) is not a typo — nothing was recorded, so the
string default applies.
"""
RETURN_TYPES = ("string", "number", "boolean")

#: THE ONE truthy vocabulary for a boolean read. Every caller reads a boolean through
#: this coercion, `check_until_condition` included; there is no second copy.
_TRUTHY = frozenset({"true", "yes", "1", "passed", "met"})


def coerce(value, return_type):
    """Coerce an extracted value to the recorded return_type.

    An absent return_type (None or empty) means everything is a string.
    """
    if not return_type:
        return "" if value is None else str(value)
    if return_type not in RETURN_TYPES:
        raise ValueError(
            f"unknown return_type {return_type!r}; expected one of {list(RETURN_TYPES)}"
        )
    if return_type == "string":
        return "" if value is None else str(value)
    if return_type == "boolean":
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in _TRUTHY
    # number
    if isinstance(value, bool):
        raise ValueError(f"cannot read {value!r} as a number")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"cannot read {value!r} as a number") from None
