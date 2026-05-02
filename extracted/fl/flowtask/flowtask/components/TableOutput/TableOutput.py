from typing import Set, Union
from collections.abc import Callable
import asyncio
import logging
import json
from sqlalchemy.exc import NoSuchTableError
import pandas as pd
from datamodel.typedefs.types import AttrDict
from querysource.outputs.tables import (
    PgOutput,
    MysqlOutput,
    SaOutput,
    RethinkOutput,
    BigQueryOutput,
    MongoDBOutput
)
from querysource.outputs.tables.TableOutput.documentdb import (
    DocumentDBOutput
)
from ...exceptions import (
    ComponentError,
    DataNotFound
)
from ..flow import FlowComponent
from ...utils.functions import is_empty
from ...interfaces.credentials import CredentialsInterface


class TableOutput(FlowComponent, CredentialsInterface):
    """
    TableOutput

    Overview

        The TableOutput class is a component for copying data to SQL tables using Pandas and SQLAlchemy features. It supports
        various SQL flavors such as PostgreSQL, MySQL, and SQLAlchemy. The class handles data type detection, data transformation,
        and the INSERT-UPDATE mechanism.

    :widths: auto

        | _pk              |   No     | A list of primary keys for the table.                                                            |
        | _fk              |   No     | The foreign key for the table.                                                                   |
        | data             |   Yes    | The data to be copied to the table.                                                              |
        | _engine          |   Yes    | The database engine used for the SQL operations.                                                 |
        | _columns         |   No     | A list of columns in the table.                                                                  |
        | _schema          |   No     | The schema of the table.                                                                         |
        | _constraint      |   No     | A list of constraints for the table.                                                             |
        | _dsn             |   Yes    | The data source name (DSN) for the database connection.                                          |
        | flavor           |   Yes    | The SQL flavor for the database, defaults to "postgresql".                                       |
        | multi            |   No     | A flag indicating if multiple DataFrame transformations are supported, defaults to False.        |

        Returns:
            DataFrame: The data that was copied to the table.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          TableOutput:
          tablename: business_hours
          flavor: postgres
          schema: banco_chile
          pk:
          - store_id
          - weekday
          if_exists: append
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self._pk = []
        self._fk: str = None
        self._engine = None
        self._columns: list = []
        self._schema: str = kwargs.pop('schema', None)
        self.multi_schema: bool = kwargs.pop('multi_schema', False)
        self._constraint: list = None
        dsn = kwargs.get('dsn', None)
        self.data = kwargs.get('data', None)
        self.tablename = kwargs.pop('tablename', None)
        self.only_update = kwargs.pop('only_update', False)
        self.use_cache = kwargs.pop('use_cache', True)
        self._jsonb_columns: Set[str] = set(kwargs.pop('jsonb_columns', []) or [])
        if self.tablename is None:
            self.tablename = kwargs.pop('table', None)
        if dsn is not None and dsn.startswith('postgres:'):
            dsn = dsn.replace('postgres:', 'postgresql:')
        # DB Flavor
        self.flavor: str = kwargs.pop('flavor', 'postgresql')
        self.multi: bool = bool(kwargs.pop('multi', False))
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        # get DSN:
        self._dsn = self.get_env_value(dsn, default=dsn)

    def constraints(self):
        return self._constraint

    def get_schema(self):
        return self._schema

    def foreign_keys(self):
        return self._fk

    def primary_keys(self):
        return self._pk

    @property
    def jsonb_columns(self) -> Set[str]:
        return self._jsonb_columns

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            if is_empty(self.data):
                raise DataNotFound(
                    "Previous Data was Not Found"
                )
        await super(TableOutput, self).start(**kwargs)
        args = {}
        if hasattr(self, "do_update"):
            args = {"do_update": self.do_update}
        if hasattr(self, "use_merge"):
            args["use_merge"] = self.use_merge
        if hasattr(self, 'only_update'):
            args["only_update"] = self.only_update
        if self.flavor in ("postgres", "postgresql"):
            self._engine = PgOutput(
                parent=self,
                external=False,
                use_cache=self.use_cache,
                jsonb_columns=self._jsonb_columns,
                **args
            )
        elif self.flavor == "mysql":
            self._engine = MysqlOutput(parent=self, dsn=self._dsn, external=False)
        elif self.flavor == "sqlalchemy":
            self._engine = SaOutput(parent=self, dsn=self._dsn, external=False)
        elif self.flavor in ("rethinkdb", "rethink"):
            self._engine = RethinkOutput(parent=self, external=True)
        elif self.flavor in ("bigquery", "bq"):
            self._engine = BigQueryOutput(parent=self, external=True, **args)
        elif self.flavor in ("mongodb", "mongo"):
            self._engine = MongoDBOutput(parent=self, external=True)
        elif self.flavor in ("documentdb", "docdb"):
            self._engine = DocumentDBOutput(parent=self, external=True)
        else:
            raise ComponentError(
                f"TableOutput: unsupported DB flavor: {self.flavor}"
            )
        if self.data is None:
            raise DataNotFound(
                "TableOutput: Data missing"
            )
        elif isinstance(self.data, pd.DataFrame):
            if self._schema is None and hasattr(self, "schema_column"):
                # split the dataframe based on the "schema_column" and declared as "multiple":
                self.multi = True
                self.multi_schema = True
                schema_column = self.schema_column
                unique_values = self.data[schema_column].unique()
                result = {}
                for value in unique_values:
                    result[value] = self.data[self.data[schema_column] == value]
                self.data = result
                return True
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
                else:
                    # this is an special column from RethinkDB
                    # rethinkdb.ast.RqlTzinfo
                    if column == "inserted_at":
                        try:
                            self.data[column] = pd.to_datetime(
                                self.data[column],
                                format="%Y-%m-%dT%H:%M:%S.%f%z",
                                cache=True,
                                utc=True,
                            )
                        except ValueError:
                            self.data[column] = pd.to_datetime(
                                self.data[column],
                                # format='%Y-%m-%d %H:%M:%S.%f+%z',
                                cache=True,
                                utc=True,
                            )
        elif self.multi is True:
            # iteration over every Pandas DT:
            try:
                result = self.data.items()
            except Exception as err:
                raise ComponentError(
                    f"Invalid Result type for Multiple: {err}"
                ) from err
            for name, rs in result:
                if hasattr(self, name):
                    el = getattr(self, name)
                    print(el)
                    if not isinstance(rs, pd.DataFrame):
                        raise ComponentError(
                            "Invalid origin Dataset: not a Dataframe"
                        )
        return True

    async def close(self):
        """Closing Operations."""
        try:
            await self._engine.close()
        except Exception as err:
            logging.error(err)

    def _normalize_bigquery_json_columns(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        For BigQuery, we no longer convert dict/list to JSON strings here.
        BigQuery.py handles the conversion correctly when using NDJSON loader.
        This function now just ensures None/NaN values are properly handled.
        """
        if dataframe is None or dataframe.empty:
            return dataframe

        # Only normalize null values - keep dict/list as-is
        def normalize_nulls(value):
            if value is None:
                return None
            try:
                if pd.isna(value):
                    return None
            except (ValueError, TypeError):
                # value is array/list/dict, not NaN
                pass
            return value

        # Apply null normalization to object columns
        for col in dataframe.columns:
            if dataframe[col].dtype == "object":
                dataframe[col] = dataframe[col].apply(normalize_nulls)

        return dataframe

    async def table_output(self, elem, datasource):
        # get info
        options = {"chunksize": 100}
        table = elem.tablename
        try:
            schema = elem.schema
        except AttributeError:
            if self._schema:
                schema = self._schema
            else:
                schema = 'public'
        # starting metric:
        try:
            data = {"NUM_ROWS": datasource.shape[0], "NUM_COLUMNS": datasource.shape[1]}
            self.add_metric(f"{schema}.{table}", data)
        except Exception:
            pass
        if self._engine.is_external is False:
            options["schema"] = schema
            if hasattr(elem, "sql_options"):
                options = {**options, **elem.sql_options}
            if hasattr(elem, "pk") or hasattr(elem, "constraint"):
                options["index"] = False
            if hasattr(elem, "if_exists"):
                options["if_exists"] = elem.if_exists
            else:
                options["if_exists"] = "append"
            # define index:
            try:
                self._pk = elem.pk
                options["index_label"] = self._pk
            except AttributeError:
                self._pk = []
            # set the upsert method:
            options["method"] = self._engine.db_upsert
            if hasattr(elem, "foreign_key"):
                self._fk = elem.foreign_key
            else:
                self._fk = None
            if hasattr(elem, "constraint"):
                self._constraint = elem.constraint
            else:
                self._constraint = None
            self._columns = list(datasource.columns)
            self._engine.columns = self._columns
            self._schema = schema
            # add metrics for Table Output
            try:
                u = datasource.select_dtypes(include=["object", "string"])
                replacement_values = u.replace(["<NA>", "None"], None)
                datasource[u.columns] = replacement_values
            except ValueError as ex:
                self._logger.warning(
                    f"Column mismatch: {len(u.columns)} vs {len(replacement_values.columns)}, error: {ex}"
                )
            try:
                datasource.to_sql(name=table, con=self._engine.engine(), **options)
                logging.debug(f":: Saving Table Data {schema}.{table} ...")
                return True
            except NoSuchTableError as exc:
                raise ComponentError(f"There is no Table {table}: {exc}") from exc
            except Exception as exc:
                raise ComponentError(f"{exc}") from exc
        else:
            # Using Engine External method write:
            on_conflict = 'replace'
            if hasattr(elem, 'if_exists'):
                on_conflict = elem.if_exists

            if self.flavor in ('bigquery', 'bq'):
                datasource = self._normalize_bigquery_json_columns(datasource)

            # Configuración para BigQuery MERGE
            kwargs = {
                'table': table,
                'schema': schema,
                'data': datasource,
                'on_conflict': on_conflict,
            }

            # Si es BigQuery y tiene PK definidas, agregar configuración de MERGE
            if self.flavor in ('bigquery', 'bq'):
                if hasattr(elem, 'pk'):
                    kwargs['pk'] = elem.pk
                    self._logger.debug(f"Using primary keys for merge: {elem.pk}")
                if hasattr(elem, 'use_merge'):
                    kwargs['use_merge'] = elem.use_merge
                    self._logger.debug(f"MERGE enabled: {elem.use_merge}")

            await self._engine.db_upsert(**kwargs)

    async def run(self):
        """Run TableOutput."""
        try:
            self._result = None
            if self.multi is False:
                # set the number of rows:
                self._variables["{self.StepName}_NUMROWS"] = len(self.data.index)
                await self.table_output(self, self.data)
                self._result = self.data
                try:
                    self.add_metric("ROWS_SAVED", len(self.data.index))
                except (TypeError, ValueError):
                    pass
                return self._result
            else:
                # running in multi Mode
                try:
                    result = self.data.items()
                except Exception as err:
                    raise ComponentError(
                        f"Invalid Result type for Multiple: {err}"
                    ) from err
                for name, rs in result:
                    if self.multi_schema is False:
                        try:
                            el = getattr(self, name)
                            obj = AttrDict(el)
                        except AttributeError:
                            continue
                    else:
                        obj = self
                        self._schema = name
                    await self.table_output(obj, rs)
                    # set the number of rows:
                    self._variables[f"{self.StepName}_{name}_NUMROWS"] = len(rs.index)
                # return the same dataframe
                self._result = self.data
                try:
                    self.add_metric(
                        "ROWS_SAVED", self._engine.result()
                    )
                except Exception as err:
                    logging.error(err)
                return self._result
        except ValueError as err:
            raise ComponentError(f"Value Error: {err}") from err
        except Exception as err:
            raise ComponentError(f"TableOutput: {err}") from err
