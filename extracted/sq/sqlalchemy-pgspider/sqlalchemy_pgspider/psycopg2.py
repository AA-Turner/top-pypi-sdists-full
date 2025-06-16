# sqlalchemy-pgspider/psycopg2.py
# Copyright (C) 2023 Toshiba Corporation
#
# This module is for connecting to PGSpider with SQLAlchemy.
# SQLAlchemy: https://www.sqlalchemy.org/
# 
# It is a subclass of PGDialect_psycopg2 and most of its functionality is 
# implemented in the parent class.
# 
# This is the MIT license: http://www.opensource.org/licenses/mit-license.php
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons
# to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
import re

from sqlalchemy.dialects.postgresql.psycopg2 import PGDialect_psycopg2


class PGSpiderDialect_psycopg2(PGDialect_psycopg2):
    supports_statement_cache = True

    def _get_server_version_info(self, connection):
        v = connection.exec_driver_sql("select pg_catalog.version()").scalar()
        m = re.match(
            r".*(?:PGSpider|PostgreSQL|EnterpriseDB) "
            r"(\d+)\.?(\d+)?(?:\.(\d+))?(?:\.\d+)?(?:devel|beta)?",
            v,
        )
        if not m:
            raise AssertionError(
                "Could not determine version from string '%s'" % v
            )
        return tuple([int(x) for x in m.group(1, 2, 3) if x is not None])
