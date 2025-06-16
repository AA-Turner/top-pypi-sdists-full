#
# This software is part of the DenodoConnect component collection.
#
# Copyright (c) 2025 Denodo Technologies (https://www.denodo.com)
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
from typing import Any, Sequence, Optional

from adbc_driver_manager.dbapi import Cursor as ADBCDBAPICursor
from sqlalchemy.engine import default
from sqlalchemy.engine.interfaces import DBAPICursor, _DBAPIMultiExecuteParams, _DBAPISingleExecuteParams, \
    _DBAPICursorDescription


class FlightSQLDenodoCursor(DBAPICursor):

    def __init__(self, wrapped: ADBCDBAPICursor):
        self._wrapped = wrapped

    def __getattr__(self, key: str) -> Any:
        return self._wrapped.__getattr__(key)

    def callproc(self, procname: str, parameters: Sequence[Any] = ...) -> Any:
        return self._wrapped.callproc(procname, parameters)

    def close(self) -> None:
        self._wrapped.close()

    @property
    def description(self) -> _DBAPICursorDescription:
        return self._wrapped.description

    def execute(self, operation: Any, parameters: Optional[_DBAPISingleExecuteParams] = None) -> Any:
        return self._wrapped.execute(operation, parameters)

    def executemany(self, operation: Any, parameters: _DBAPIMultiExecuteParams) -> Any:
        return self._wrapped.executemany(operation, parameters)

    def fetchall(self) -> Sequence[Any]:
        data_df = self._wrapped.fetch_df()
        return list(data_df.itertuples(index=False, name=None))

    def fetchmany(self, size: int = ...) -> Sequence[Any]:
        return self._wrapped.fetchmany(size)

    def fetchone(self) -> Optional[Any]:
        return self._wrapped.fetchone()

    def nextset(self) -> Optional[bool]:
        return self._wrapped.nextset()

    @property
    def rowcount(self) -> int:
        return self._wrapped.rowcount

    def setinputsizes(self, sizes: Sequence[Any]) -> None:
        self._wrapped.setinputsizes(sizes)

    def setoutputsize(self, size: Any, column: Any) -> None:
        self._wrapped.setoutputsize(size, column)


class FlightSQLDenodoExecutionContext(default.DefaultExecutionContext):

    def create_cursor(self) -> DBAPICursor:
        cursor = super().create_cursor()
        if isinstance(cursor, ADBCDBAPICursor):
            cursor = FlightSQLDenodoCursor(cursor)
        return cursor
