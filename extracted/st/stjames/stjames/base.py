"""Provide shared model and validation helpers."""

from enum import Enum
from typing import Annotated, Any, Callable, Hashable, TypeVar

import numpy as np
import pydantic

_T = TypeVar("_T")


def round_float(round_to: int) -> Callable[[float], float]:
    """Return a function that rounds a float to a given number of decimal places.

    Args:
        round_to: number of decimal places to retain
    """

    def inner_round(v: float) -> float:
        return round(v, round_to)

    return inner_round


def round_optional_float(round_to: int) -> Callable[[float | None], float | None]:
    """Create a validator that rounds an optional float to a given number of decimal places.

    Args:
        round_to: number of decimal places to retain
    """

    def rounder(value: float | None) -> float | None:
        if value is None:
            return None
        return round(value, round_to)

    return rounder


class Base(pydantic.BaseModel):
    """Base model with automatic numpy array coercion."""

    @pydantic.field_validator("*", mode="before")
    @classmethod
    def coerce_numpy(cls, val: _T) -> _T | list[Any]:
        """Convert NumPy arrays to lists before model validation.

        Args:
            val: input value to coerce

        Returns:
            list for an array, or original value
        """
        if isinstance(val, np.ndarray):
            return val.tolist()

        return val

    def model_dump(self, *, exclude_none: bool = True, **kwargs: Any) -> dict[str, Any]:
        """Serialize the model while omitting null fields by default.

        Args:
            exclude_none: omit fields with null values when true
            kwargs: additional Pydantic serialization options

        Returns:
            serialized model data
        """
        return super().model_dump(exclude_none=exclude_none, **kwargs)


class LowercaseStrEnum(str, Enum):
    """Enum where hyphens, underscores, and case are ignored."""

    @classmethod
    def _missing_(cls, value: object) -> str | None:
        for member in cls:
            if isinstance(value, str):
                if member.lower().replace("-", "").replace("_", "") == value.lower().replace("-", "").replace("_", ""):
                    return member
        return None


# cf. https://github.com/pydantic/pydantic-core/pull/820#issuecomment-1670475909
_H = TypeVar("_H", bound=Hashable)


def _validate_unique_list(v: list[_H]) -> list[_H]:
    if len(v) != len(set(v)):
        raise ValueError("this list must be unique, and isn't!")
    return v


UniqueList = Annotated[list[_H], pydantic.AfterValidator(_validate_unique_list)]
