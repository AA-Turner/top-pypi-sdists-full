#
# GAMS - General Algebraic Modeling System Python API
#
# Copyright (c) 2017-2025 GAMS Development Corp. <support@gams.com>
# Copyright (c) 2017-2025 GAMS Software GmbH <support@gams.com>
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

import pandas as pd
from gams.connect.agents._sqlconnectors._databasehandler import DatabaseConnector


class SQLAlchemyConnector(DatabaseConnector):
    SUPPORTED_INSERT_METHODS = ["default"]

    def connect(self, connection_details, connection_args, **kwargs) -> None:
        import sqlalchemy

        con_str = sqlalchemy.engine.URL.create(**connection_details)
        self._engine = sqlalchemy.create_engine(con_str, **connection_args)
        self._conn = self._engine.connect()

    def create_transaction(self) -> None:
        self._conn.begin()

    def read_table(self, sql_query: str, read_sql_args: dict) -> pd.DataFrame:
        return pd.read_sql(sql=sql_query, con=self._conn, **read_sql_args)

    def _execute_write(
        self,
        df: pd.DataFrame,
        writeFunction_args: dict,
    ):
        to_sql_args = {
            key: writeFunction_args[key]
            for key in ["name", "schema", "if_exists", "index"]
        }
        to_sql_args.update(writeFunction_args["toSQLArguments"])
        df.to_sql(con=self._conn, **to_sql_args)

    def commit(self):
        self._conn.commit()

    def rollback(self):
        self._conn.rollback()

    def close(self):
        self._engine.dispose()

    def _check_table_exists(self, tableName, schema):
        pass

    def _create_table(self, df, tableName, schema, ifExists, **kwargs):
        pass

    def _insert_data(self, df, writeFunction_args):
        pass
