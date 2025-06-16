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

import decimal
import sqlalchemy

from . import types
from .array import ARRAY as PGARRAY
from .base import _DECIMAL_TYPES
from .base import _FLOAT_TYPES
from .base import _INT_TYPES
from .base import PGDialect
from sqlalchemy import exc
from sqlalchemy import types as sqltypes
from sqlalchemy import util
if sqlalchemy.__version__ >= '2.0.0':
    from sqlalchemy.engine import processors
else:
    from sqlalchemy import processors

_server_side_id = util.counter()


class _PsycopgNumeric(sqltypes.Numeric):
    def bind_processor(self, dialect):
        return None

    def result_processor(self, dialect, coltype):
        if self.asdecimal:
            if coltype in _FLOAT_TYPES:
                return processors.to_decimal_processor_factory(
                    decimal.Decimal, self._effective_decimal_return_scale
                )
            elif coltype in _DECIMAL_TYPES or coltype in _INT_TYPES:
                # psycopg returns Decimal natively for 1700
                return None
            else:
                raise exc.InvalidRequestError(
                    "Unknown PG numeric type: %d" % coltype
                )
        else:
            if coltype in _FLOAT_TYPES:
                # psycopg returns float natively for 701
                return None
            elif coltype in _DECIMAL_TYPES or coltype in _INT_TYPES:
                return processors.to_float
            else:
                raise exc.InvalidRequestError(
                    "Unknown PG numeric type: %d" % coltype
                )


class _PsycopgFloat(_PsycopgNumeric):
    __visit_name__ = "float"


class _PsycopgARRAY(PGARRAY):
    render_bind_cast = True


class _PGDialect_common_psycopg(PGDialect):
    supports_statement_cache = True
    supports_server_side_cursors = True

    colspecs = util.update_copy(
        PGDialect.colspecs,
        {
            sqltypes.Numeric: _PsycopgNumeric,
            sqltypes.Float: _PsycopgFloat,
            sqltypes.ARRAY: _PsycopgARRAY,
            sqltypes.TIMESTAMP: types.TIMESTAMP,
            sqltypes.TIME: types.TIME,
            sqltypes.Interval: types.INTERVAL,
        },
    )

    def __init__(self, client_encoding=None, **kwargs):
        PGDialect.__init__(self, **kwargs)
        self.client_encoding = client_encoding

    def create_connect_args(self, url):
        opts = url.translate_connect_args(username="user", database="dbname")

        if opts or url.query:
            if not opts:
                opts = {}
            if "port" in opts:
                opts["port"] = int(opts["port"])
            opts.update(url.query)
            return ([], opts)
        else:
            # no connection arguments whatsoever; psycopg2.connect()
            # requires that "dsn" be present as a blank string.
            return ([""], opts)

    def do_ping(self, dbapi_connection):
        cursor = None
        before_autocommit = dbapi_connection.autocommit

        if not before_autocommit:
            dbapi_connection.autocommit = True
        cursor = dbapi_connection.cursor()
        try:
            cursor.execute(self._dialect_specific_select_one)
        finally:
            cursor.close()
            if not before_autocommit and not dbapi_connection.closed:
                dbapi_connection.autocommit = before_autocommit

        return True
