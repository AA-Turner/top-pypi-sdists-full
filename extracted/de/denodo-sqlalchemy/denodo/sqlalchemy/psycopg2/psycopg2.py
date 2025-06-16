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

import logging
import re

from ._psycopg_common import _PGDialect_common_psycopg
from sqlalchemy import util, exc

logger = logging.getLogger("denodo.sqlalchemy.psycopg2")


EXECUTEMANY_VALUES = util.symbol("executemany_values", canonical=0)
EXECUTEMANY_VALUES_PLUS_BATCH = util.symbol("executemany_values_plus_batch", canonical=1)


class PGDialect_psycopg2(_PGDialect_common_psycopg):
    driver = "psycopg2"

    supports_statement_cache = True
    supports_server_side_cursors = True

    # set to true based on psycopg2 version
    supports_sane_multi_rowcount = False
    psycopg2_version = (0, 0)

    use_insertmanyvalues = True
    use_insertmanyvalues_wo_returning = True

    returns_native_bytes = False

    colspecs = util.update_copy(_PGDialect_common_psycopg.colspecs)

    def __init__(self, executemany_mode="values_only", executemany_batch_page_size=100, **kwargs):

        _PGDialect_common_psycopg.__init__(self, **kwargs)

        # Parse executemany_mode argument, allowing it to be only one of the
        # symbol names
        self.executemany_mode = parse_user_argument(
            executemany_mode,
            {
                EXECUTEMANY_VALUES: ["values_only"],
                EXECUTEMANY_VALUES_PLUS_BATCH: ["values_plus_batch", "values"],
            },
            "executemany_mode",
        )

        self.executemany_batch_page_size = executemany_batch_page_size

        if self.dbapi and hasattr(self.dbapi, "__version__"):
            m = re.match(r"(\d+)\.(\d+)(?:\.(\d+))?", self.dbapi.__version__)
            if m:
                self.psycopg2_version = tuple(
                    int(x) for x in m.group(1, 2, 3) if x is not None
                )

            if self.psycopg2_version < (2, 7):
                raise ImportError(
                    "psycopg2 version 2.7 or higher is required."
                )

    def initialize(self, connection):
        super().initialize(connection)
        self.supports_sane_multi_rowcount = (
            self.executemany_mode is not EXECUTEMANY_VALUES_PLUS_BATCH
        )

    @classmethod
    def dbapi(cls):         # SQLAlchemy < 2.0
        return cls.import_dbapi()

    @classmethod
    def import_dbapi(cls):  # SQLAlchemy >= 2.0
        import psycopg2

        return psycopg2

    @util.memoized_property
    def _psycopg2_extensions(cls):
        from psycopg2 import extensions

        return extensions

    @util.memoized_property
    def _psycopg2_extras(cls):
        from psycopg2 import extras

        return extras

    def on_connect(self):
        extras = self._psycopg2_extras

        fns = []
        if self.client_encoding is not None:

            def on_connect(dbapi_conn):
                dbapi_conn.set_client_encoding(self.client_encoding)

            fns.append(on_connect)

        if self.dbapi:

            def on_connect(dbapi_conn):
                extras.register_uuid(None, dbapi_conn)

            fns.append(on_connect)

        if fns:

            def on_connect(dbapi_conn):
                for fn in fns:
                    fn(dbapi_conn)

            return on_connect
        else:
            return None

    def do_executemany(self, cursor, statement, parameters, context=None):
        if self.executemany_mode is EXECUTEMANY_VALUES_PLUS_BATCH:
            if self.executemany_batch_page_size:
                kwargs = {"page_size": self.executemany_batch_page_size}
            else:
                kwargs = {}
            self._psycopg2_extras.execute_batch(
                cursor, statement, parameters, **kwargs
            )
        else:
            cursor.executemany(statement, parameters)

    def is_disconnect(self, e, connection, cursor):
        if isinstance(e, self.dbapi.Error):
            # check the "closed" flag.  this might not be
            # present on old psycopg2 versions.   Also,
            # this flag doesn't actually help in a lot of disconnect
            # situations, so don't rely on it.
            if getattr(connection, "closed", False):
                return True

            # checks based on strings.  in the case that .closed
            # didn't cut it, fall back onto these.
            str_e = str(e).partition("\n")[0]
            for msg in self._is_disconnect_messages:
                idx = str_e.find(msg)
                if idx >= 0 and '"' not in str_e[:idx]:
                    return True
        return False

    @util.memoized_property
    def _is_disconnect_messages(self):
        return (
            # these error messages from libpq: interfaces/libpq/fe-misc.c
            # and interfaces/libpq/fe-secure.c.
            "terminating connection",
            "closed the connection",
            "connection not open",
            "could not receive data from server",
            "could not send data to server",
            # psycopg2 client errors, psycopg2/connection.h,
            # psycopg2/cursor.h
            "connection already closed",
            "cursor already closed",
            # not sure where this path is originally from, it may
            # be obsolete.   It really says "losed", not "closed".
            "losed the connection unexpectedly",
            # these can occur in newer SSL
            "connection has been closed unexpectedly",
            "SSL error: decryption failed or bad record mac",
            "SSL SYSCALL error: Bad file descriptor",
            "SSL SYSCALL error: EOF detected",
            "SSL SYSCALL error: Operation timed out",
            "SSL SYSCALL error: Bad address",
            # This can occur in OpenSSL 1 when an unexpected EOF occurs.
            # https://www.openssl.org/docs/man1.1.1/man3/SSL_get_error.html#BUGS
            # It may also occur in newer OpenSSL for a non-recoverable I/O
            # error as a result of a system call that does not set 'errno'
            # in libc.
            "SSL SYSCALL error: Success",
        )


dialect = PGDialect_psycopg2


# Brought from SQLAlchemy 1.4.x for compatibility with SQLAlchemy 2.0 environments
def parse_user_argument(arg, choices, name, resolve_symbol_names=False):
    for sym, choice in choices.items():
        if arg is sym:
            return sym
        elif resolve_symbol_names and arg == sym.name:
            return sym
        elif arg in choice:
            return sym

    if arg is None:
        return None
    raise exc.ArgumentError("Invalid value for '%s': %r" % (name, arg))
