from __future__ import annotations

import logging
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class BaseEnum(Enum):
    """
    Base class for enums.

    This class can be used to build an Enum from a list of values,
    providing the missing functionality and handling unknown values without raising.

    Example:
    ```
    class MyEnum(str, BaseEnum):
        VALUE_1 = "value1"
        VALUE_2 = "value2"
        VALUE_3 = "value3"
        UNKNOWN = "unknown" # Required to be defined when using BaseEnum

    class SomeModel(BaseModel):
        my_enum: MyEnum

    SomeModel(my_enum="value1")
    SomeModel(my_enum="value4")  # will be mapped to UNKNOWN
    ```
    """

    @classmethod
    def _unknown_member(cls):
        # Expect subclasses to define UNKNOWN
        try:
            return cls["UNKNOWN"]
        except Exception as e:
            for m in cls:
                if m.name.upper() == "UNKNOWN":
                    return m
            raise AttributeError(f"{cls.__name__} must define an UNKNOWN member") from e

    @classmethod
    def _missing_(cls, value: Any):
        for member in cls:  # type: ignore
            mv = member.value
            if member.name == "UNKNOWN":
                continue

            if mv == value:
                return member

        logger.warning(
            f"[SDK/Enum] {cls.__name__} received unknown enum value: {value!r}, "
            f"mapped to UNKNOWN. Please check the enum definition and include the member if necessary."
        )
        return cls._unknown_member()
