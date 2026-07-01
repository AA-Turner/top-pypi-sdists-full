#
# This software is part of the DenodoConnect component collection.
#
# Copyright (c) 2025 Denodo Technologies (https://www.denodo.com)
#
# This module is based on SQLAlchemy's dialect for PostgreSQL:
#
# Copyright (C) 2005-2025 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# Licensed under the MIT License.
# You may not use this file except in compliance with the License.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
from __future__ import annotations

import datetime as dt
from typing import Any
from typing import Optional
from typing import Type
from typing import TYPE_CHECKING

from sqlalchemy.sql import sqltypes
from sqlalchemy.sql import type_api

if TYPE_CHECKING:
    from sqlalchemy.engine.interfaces import Dialect
    from sqlalchemy.sql.type_api import _LiteralProcessorType
    from sqlalchemy.sql.type_api import TypeEngine

_DECIMAL_TYPES = (1231, 1700)
_FLOAT_TYPES = (700, 701, 1021, 1022)
_INT_TYPES = (20, 21, 23, 26, 1005, 1007, 1016)


class TIMESTAMP(sqltypes.TIMESTAMP):
    """Provide the PostgreSQL TIMESTAMP type."""

    __visit_name__ = "TIMESTAMP"

    def __init__(
        self, timezone: bool = False, precision: Optional[int] = None
    ) -> None:
        """Construct a TIMESTAMP.

        :param timezone: boolean value if timezone present, default False
        :param precision: optional integer precision value

         .. versionadded:: 1.4

        """
        super().__init__(timezone=timezone)
        self.precision = precision


class TIME(sqltypes.TIME):
    """PostgreSQL TIME type."""

    __visit_name__ = "TIME"

    def __init__(
        self, timezone: bool = False, precision: Optional[int] = None
    ) -> None:
        """Construct a TIME.

        :param timezone: boolean value if timezone present, default False
        :param precision: optional integer precision value

         .. versionadded:: 1.4

        """
        super().__init__(timezone=timezone)
        self.precision = precision


class INTERVAL(type_api.NativeForEmulated, sqltypes._AbstractInterval):
    """PostgreSQL INTERVAL type."""

    __visit_name__ = "INTERVAL"
    native = True

    def __init__(
        self, precision: Optional[int] = None, fields: Optional[str] = None
    ) -> None:
        """Construct an INTERVAL.

        :param precision: optional integer precision value
        :param fields: string fields specifier.  allows storage of fields
         to be limited, such as ``"YEAR"``, ``"MONTH"``, ``"DAY TO HOUR"``,
         etc.

         .. versionadded:: 1.2

        """
        self.precision = precision
        self.fields = fields

    @classmethod
    def adapt_emulated_to_native(
        cls, interval: sqltypes.Interval, **kw: Any  # type: ignore[override]
    ) -> INTERVAL:
        return INTERVAL(precision=interval.second_precision)

    @property
    def _type_affinity(self) -> Type[sqltypes.Interval]:
        return sqltypes.Interval

    def as_generic(self, allow_nulltype: bool = False) -> sqltypes.Interval:
        return sqltypes.Interval(native=True, second_precision=self.precision)

    @property
    def python_type(self) -> Type[dt.timedelta]:
        return dt.timedelta

    def literal_processor(
        self, dialect: Dialect
    ) -> Optional[_LiteralProcessorType[dt.timedelta]]:
        def process(value: dt.timedelta) -> str:
            return f"make_interval(secs=>{value.total_seconds()})"

        return process



class BIT(sqltypes.TypeEngine[int]):
    __visit_name__ = "BIT"

    def __init__(self) -> None:
        self.length = 1

