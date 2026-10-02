#
# Copyright 2024-2026 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from enum import Enum
from typing import Type, TypeVar

from datarobot.utils import camelize, underscorize


class EnumAPIRepresentationConverter(Enum):
    def to_api_representation(self) -> str:
        return camelize(self.name.lower())

    @classmethod
    def from_api_representation(cls: Type[ENUM_TYPE], enum_string: str) -> ENUM_TYPE:
        enum_string = underscorize(enum_string).upper()
        for enum_value in cls:
            if enum_string == enum_value.name:
                return enum_value
        msg = (
            f"Enum string {enum_string} is invalid. Valid values are "
            f"{[enum_value.to_api_representation() for enum_value in cls]}"
        )
        raise ValueError(msg)

    def to_string(self) -> str:
        return self.name

    @classmethod
    def from_string(cls: Type[ENUM_TYPE], enum_value_string: str) -> ENUM_TYPE:
        for enum_value in list(cls):
            if enum_value.name == enum_value_string:
                return enum_value
        raise ValueError("Enum: {!r} has no value: {!r}".format(cls, enum_value_string))


ENUM_TYPE = TypeVar("ENUM_TYPE", bound="EnumAPIRepresentationConverter")
