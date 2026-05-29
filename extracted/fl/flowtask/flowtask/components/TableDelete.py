import asyncio

# logging system
import logging
import datetime
from decimal import Decimal
from typing import Any
from collections.abc import Callable
import pandas as pd
import numpy as np
from asyncdb.exceptions import NoDataFound
from asyncdb.models import Model
from asyncdb.drivers.pg import pg

# for database
from querysource.conf import (
    sqlalchemy_url,
    default_dsn,
    DB_STATEMENT_TIMEOUT,
    DB_SESSION_TIMEOUT,
    DB_KEEPALIVE_IDLE,
)
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from ..exceptions import ComponentError, DataNotFound
from ..utils import AttrDict
from ..interfaces.flow import FlowComponent
from ..interfaces.qs import QSSupport


dtypes = {
    "varchar": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "int64": int,
    "uint64": int,
    "Int64Dtype": np.int64,
    "Int64": int,
    "Int32": int,
    "Int16": int,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "datetime64[ns, UTC]": datetime.datetime,
}


class TableDelete(QSSupport, FlowComponent):
    """
    TableDelete

    Overview

        The TableDelete class is a component for deleting rows from a SQL table based on specified primary keys. It uses
        Pandas DataFrames to identify rows to delete and performs the deletion using SQLAlchemy and asyncpg.

    :widths: auto

        | flavor           |   No     | The database flavor, defaults to "postgresql".                                                    |
        | pk               |   Yes    | A list of primary key columns to identify rows for deletion.                                      |
        | data             |   Yes    | The data containing rows to be deleted, can be a Pandas DataFrame or other supported format.      |
        | _engine          |   No     | The SQLAlchemy engine for database connections.                                                   |
        | tablename        |   Yes    | The name of the table from which rows will be deleted.                                            |
        | schema           |   No     | The schema name, defaults to an empty string.                                                     |
        | _dsn             |   No     | The Data Source Name for the database connection.                                                 |
        | multi            |   No     | A flag indicating if multiple DataFrame deletions are supported, defaults to False.               |

    Return

        The methods in this class manage the deletion of rows from a SQL table based on primary keys, including initialization,
        execution, and result handling. It ensures proper handling of database connections and provides metrics on the deleted rows.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          TableDelete:
          tablename: totem_heartbeats
          flavor: postgres
          schema: banco_chile
          pk:
          - hearbeat_id
        ```
    """
    _version = "1.0.0"

    flavor: str = "postgresql"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.pk = []
        self.data: Any = None
        self._engine = None
        self.tablename = ""
        self.schema = ""
        dsn = kwargs.get('dsn', '')
        if dsn and dsn.startswith('postgres:'):
            dsn = dsn.replace('postgres:', 'postgresql:')
        self._dsn = self.get_config_value(dsn, dsn)
        self.multi = bool(kwargs.pop('multi', False))
        self._driver: str = kwargs.pop('driver', 'pg')
        super(TableDelete, self).__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    def get_engine(self, dsn: str = None):
        if not dsn:
            dsn = sqlalchemy_url
        try:
            self._engine = create_engine(dsn, echo=False, poolclass=NullPool)
            self._session = Session(bind=self._engine)
        except Exception as err:
            logging.exception(err)

    async def start(self, **kwargs):
        """Get Pandas Dataframe."""
        self.data = None
        if self.previous:
            self.data = self.input
        else:
            raise NoDataFound("TableDelete: Data missing")
        await super().start(**kwargs)
        try:
            # getting sqlAlchemy engine
            self.get_engine(dsn=self._dsn)
        except Exception as err:
            raise ComponentError(f"Connection Error: {err}") from err
        if self.data is None:
            raise NoDataFound("TableDelete: Data missing")
        elif isinstance(self.data, pd.DataFrame):
            # detect data type for colums
            columns = list(self.data.columns)
            for column in columns:
                t = self.data[column].dtype
                if isinstance(t, pd.core.dtypes.dtypes.DatetimeTZDtype):
                    self.data[column] = pd.to_datetime(
                        self.data[column],
                        format="%Y-%m-%dT%H:%M:%S.%f%z",
                        cache=True,
                        utc=True,
                    )
                    self.data[column].dt.tz_convert("UTC")
                elif str(t) == "datetime64[ns]":
                    tmp_data = self.data.copy()
                    tmp_data[column] = pd.to_datetime(
                        self.data[column],
                        format="%Y-%m-%dT%H:%M:%S.%f%z",
                        cache=True,
                        utc=True,
                    )
                    self.data = tmp_data.copy()
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    "Invalid Result type for Attribute Multiple: {err}"
                ) from err
            for name, rs in result:
                el = getattr(self, name)
                if not isinstance(rs, pd.DataFrame):
                    raise ComponentError("Invalid Resultset: not a Dataframe")
        else:
            # incompatible datasource:
            raise DataNotFound("TableDelete: Incompatible Data Source")

    async def close(self):
        """Closing Operations."""
        if self._engine:
            try:
                self._engine.dispose()
            except Exception:
                pass

    async def table_delete(self, elem, df):
        """Running the process of Upsert-delete."""
        pk = elem.pk
        options = {
            "if_exists": "append",
            "index_label": pk,
            "index": False,
            "method": "multi",
        }
        if hasattr(elem, "sql_options"):
            options = {**options, **elem.sql_options}
        tablename = elem.tablename
        try:
            schema_name = elem.schema
        except AttributeError:
            schema_name = "public"
        options["schema"] = schema_name
        cols = []
        for field_name in pk:
            datatype = df.dtypes[field_name]
            dtype_key = f"{datatype!s}"
            try:
                t = dtypes[dtype_key]
            except KeyError:
                logging.warning(
                    f"TableDelete: Unknown dtype '{dtype_key}' for column "
                    f"'{field_name}', defaulting to str"
                )
                t = str
            # Use None default so the model can be instantiated without arguments
            # (needed for schema introspection to generate the CREATE TABLE SQL)
            cols.append((field_name, t, None))
        # make a intermediate model:
        try:
            cls = Model.make_model(
                name=f"{tablename!s}_deleted", schema=schema_name, fields=cols
            )
        except Exception as err:
            logging.exception(
                f"TableDelete: Error creating DB Model for {tablename}: {err}"
            )
            return False
        result = None
        if sql := cls.model(dialect="sql"):
            print("SQL is: ", sql)
            deltable = text(
                f"DROP TABLE IF EXISTS {schema_name}.{tablename!s}_deleted;"
            )
            qry = text(sql)
            try:
                with self._engine.begin() as connection:
                    connection.execute(deltable)
                    result = connection.execute(qry)
                logging.debug(f"Created Temp Table: {cls!s}")
            except Exception as error:
                raise ComponentError(f"Error on Table creation: {error}") from error
        else:
            raise ComponentError("Cannot Create TEMP Table")

        # table exists: copy data into table:
        new = df[pk].copy()
        with self._engine.begin() as connection:
            new.to_sql(f"{tablename!s}_deleted", con=connection, **options)
        # data is on temp Table, deleted
        columns = ", ".join(pk)
        # TODO: using an EXISTS instead IN to speed-up delete
        delete = f"""DELETE FROM {schema_name!s}.{tablename!s} WHERE ({columns})
        IN (SELECT {columns} FROM {schema_name}.{tablename!s}_deleted)"""
        print(delete)
        connection = await self.create_connection()
        try:
            async with await connection.connection() as conn:
                try:
                    result, error = await conn.execute(sentence=delete)
                    print("TableDelete: ", result)
                    self.add_metric("TABLE_DELETED", result)
                    if error:
                        raise ComponentError(
                            f"Error Deleting Data: {error}"
                        )
                    if error:
                        raise ComponentError(
                            f"Error on TableDelete: {error}"
                        )
                except Exception as err:
                    logging.error(err)
                finally:
                    # at now, delete the table:
                    drop = f"DROP TABLE IF EXISTS {schema_name}.{tablename!s}_deleted"
                    result, error = await conn.execute(sentence=drop)
        finally:
            await connection.close()

    async def run(self):
        """Run TableDelete."""
        if self.multi is False:
            # set the number of rows:
            numrows = len(self.data.index)
            self._variables[f"{self.StepName}_NUMROWS"] = numrows
            await self.table_delete(self, self.data)
            self._result = self.data
            return True
        else:
            # running in multi Mode
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    "Invalid Result type for Attribute Multiple: {err}"
                ) from err
            for name, rs in result:
                try:
                    el = getattr(self, name)
                except AttributeError:
                    continue
                await self.table_delete(AttrDict(el), rs)
            # return the same dataframe
            self._result = self.data
            return True
