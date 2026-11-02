from datetime import datetime
from typing import Sequence, TypeAlias, cast

from shortuuid import uuid

from .._util.instances import get_instances, track_instance

PARAM_PREFIX = "param_"

ParamValue: TypeAlias = (
    int | float | bool | str | datetime | Sequence[int | float | bool | str]
)
"""Type alias for parameter values (scalar or sequence of scalars)."""


class Param(str):
    """Parameter that can be bound from inputs."""

    _id: str
    _default: ParamValue

    def __new__(cls, default: ParamValue) -> "Param":
        # assign a unique id
        id = f"{PARAM_PREFIX}{uuid()}"

        # create the string instance
        instance = super().__new__(cls, f"${id}")

        # bind instance fars
        instance._id = id
        instance._default = default

        # track and return instance
        track_instance("param", instance)
        return instance

    @property
    def id(self) -> str:
        """Unique id (automatically generated)."""
        return self._id

    @property
    def default(self) -> ParamValue:
        """Default value."""
        return self._default

    def _is_numeric(self) -> bool:
        """Is this a numeric parameter?"""
        return isinstance(self.default, (int | float))

    def _is_bool(self) -> bool:
        """Is this a boolean parameter?"""
        return isinstance(self.default, bool)

    def _is_string(self) -> bool:
        """Is this a string parameter?"""
        return isinstance(self.default, str)

    def _is_datetime(self) -> bool:
        """Is this a datetime parameter?"""
        return isinstance(self.default, datetime)

    def __repr__(self) -> str:
        return f"Param(default={self.default})"

    @classmethod
    def _get_all(cls) -> list["Param"]:
        """Get all parameters."""
        return cast(list["Param"], get_instances("param"))
