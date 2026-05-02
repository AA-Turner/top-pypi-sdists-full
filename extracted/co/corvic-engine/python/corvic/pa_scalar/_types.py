import datetime
import decimal
from collections.abc import Mapping, Sequence
from typing import Any, Protocol, TypeAlias

import pyarrow as pa

PyValue: TypeAlias = (
    bool
    | int
    | str
    | float
    | bytes
    | None
    | datetime.datetime
    | datetime.timedelta
    | datetime.time
    | datetime.date
    | decimal.Decimal
    | Sequence["PyValue"]
    | Mapping[str, "PyValue"]
)
"""Return type of as_py to narrow its nominal Any to expected types.

Separate from definition of as_py as PyValue describes the
observed return types but this is different from the nominal
typing of as_py which returns Any.
"""


# pa.Scalar is generic but its type constraint is not very useful
# because it cannot be inferred to anything besides Unknown.
# Instead, just define what we need from any "Scalar" structurally
# and avoid nominal typing altogether.
class Scalar(Protocol):
    @property
    def type(self) -> pa.DataType: ...

    def equals(self, other: "Scalar") -> bool: ...

    def as_py(self) -> Any: ...
