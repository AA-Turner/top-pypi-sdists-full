from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Dict, Mapping, NewType, Sequence, Tuple, Type, Union

import pyarrow as pa

__all__ = ["TPrimitive", "ChalkStructType"]


class ChalkStructType(type):
    __chalk_type_hints__: Dict[str, Type[TPrimitive]]  # pyright: ignore[reportUninitializedInstanceVariable]

    def __new__(cls, name: str, bases: Tuple[Type], annotations: Dict[str, Type[TPrimitive]]):
        instance = super().__new__(cls, name, bases, annotations)
        instance.__chalk_type_hints__ = annotations
        return instance


TPrimitiveArrowScalar = NewType("TPrimitiveArrowScalar", pa.Scalar)  # pyright: ignore[reportGeneralTypeIssues]
"""
`pa.Scalar` is used for internal logic inside of many primitive-transforming functions.
In order to prevent accidental misuse of an internal scalar value with an actual output,
`TPrimitiveArrowScalar` is declared as a newtype.
"""

TPrimitive = Union[
    None,
    str,
    int,
    float,
    bool,
    date,
    datetime,
    time,
    timedelta,
    Sequence["TPrimitive"],
    Mapping[str, "TPrimitive"],
    Mapping["TPrimitive", "TPrimitive"],
    ChalkStructType,
    TPrimitiveArrowScalar,
]
