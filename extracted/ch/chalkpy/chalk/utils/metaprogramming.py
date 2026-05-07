import types
from typing import Any, Type


# A sentinel object to detect if a parameter is supplied or not.
# Use a class to give it a better repr.
class _MISSING_TYPE:
    def __repr__(self):
        return "<MISSING>"


MISSING = _MISSING_TYPE()


def set_new_attribute(cls: Type, name: str, value: Any):
    # Set an attribute, or raise a ValueError if the attribute is already set
    if name in cls.__dict__:
        raise ValueError(f"Attribute '{name}' is already set")
    if isinstance(value, types.FunctionType):
        value.__qualname__ = f"{cls.__qualname__}.{value.__name__}"
    setattr(cls, name, value)
