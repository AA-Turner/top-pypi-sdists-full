import enum
import functools
from typing import Type


@functools.lru_cache(None)  # Cache all calls to this function
def get_enum_value_type(enum_cls: Type[enum.Enum]) -> type:
    """Get the type of the enum value.
    Requires that all enum member values have the same type;
    otherwise raises a TypeError.
    Returns `None` if the enum has no members.

    Note: if an enum contains both float and int members, then this function will return `float`.

    Parameters
    ----------
    enum_cls
        The enum class

    Returns
    -------
    type
        The type of the enum member values.

    Raises
    ------
    ValueError
        If `enum_cls` has no members.
    TypeError
        If `enum_cls` has members of heterogeneous types, then a TypeError is raised.
    """
    typ = None
    for x in enum_cls:
        if typ is None:
            typ = type(x.value)
            continue
        if issubclass(type(x.value), typ):
            continue
        if issubclass(type(x.value), int) and issubclass(typ, float):
            # Effectively treat ints as a subclass of floats
            continue
        if issubclass(typ, int) and issubclass(type(x.value), float):
            # Same as above, but we encountered the int first
            typ = type(x.value)
            continue
        if issubclass(typ, type(x.value)):
            # One is a subclass of the other. In this case, swap it
            typ = type(x.value)
            continue
        raise TypeError(
            f"Enum {enum_cls.__name__} has members of heterogeneous types ({typ.__name__} and {type(x.value).__name__}); all members must have the same type."
        )
    if typ is None:
        raise ValueError(f"Enum {enum_cls.__name__} has no members")
    return typ
