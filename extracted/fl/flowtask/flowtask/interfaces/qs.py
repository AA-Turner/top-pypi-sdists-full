"""
QS Support.


Adding support for Querysource related functions as datasource support to components.
"""
import os
from collections.abc import Callable
from abc import ABC
import asyncio
from importlib import import_module
from typing import Any
from navconfig import config
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from asyncdb import AsyncDB
from asyncdb.drivers.pg import pg
from asyncdb.exceptions import NoDataFound
from querysource.exceptions import DataNotFound as NoData
from querysource.queries.qs import QS
from querysource.datasources.drivers import BaseDriver
from querysource.conf import (
    default_dsn,
    sqlalchemy_url,
    DB_TIMEOUT,
    DB_STATEMENT_TIMEOUT,
    DB_SESSION_TIMEOUT,
    DB_KEEPALIVE_IDLE,
    POSTGRES_TIMEOUT,
    BIGQUERY_CREDENTIALS,
    BIGQUERY_PROJECT_ID
)
import pandas as pd
import numpy as np
from ..exceptions import (
    ConfigError,
    ComponentError,
    DataNotFound,
)
from ..utils import cPrint

class QSSupport(ABC):
    """QSSupport.

    Adding Support for Querysource parameters.
    """
    use_sqlalchemy: bool = False

    def get_config_value(self, key_name, default: str = None):
        if key_name is None:
            return default
        if val := os.getenv(str(key_name)):
            return val
        if val := config.get(str(key_name), default):
            return val
        else:
            # TODO: get from replacing masks or memecached
            return key_name

    def processing_credentials(self):
        if self.credentials:
            for key, value in self.credentials.items():
                default = getattr(self, key, value)
                try:
                    val = self.get_config_value(
                        key_name=value, default=default
                    )
                    self.credentials[key] = val
                except (TypeError, KeyError) as err:
                    raise ConfigError(
                        f"{__name__}: Wrong or missing Credentials"
                    ) from err
        return self.credentials

    def set_datatypes(self):
        if self.datatypes:
            dtypes = {}
            for field, dtype in self.datatypes.items():
                if dtype == "uint8":
                    dtypes[field] = np.uint8
                elif dtype == "uint16":
                    dtypes[field] = np.uint16
                elif dtype == "uint32":
                    dtypes[field] = np.uint32
                elif dtype == "int8":
                    dtypes[field] = np.int8
                elif dtype == "int16":
                    dtypes[field] = np.int16
                elif dtype == "int32":
                    dtypes[field] = np.int32
                elif dtype == "float":
                    dtypes[field] = float
                elif dtype == "float32":
                    dtypes[field] = float
                elif dtype in ("varchar", "str"):
                    dtypes[field] = str
                elif dtype == "string":
                    dtypes[field] = "string"
                else:
                    # invalid datatype
                    self._logger.warning(
                        f"Invalid DataType value: {field} for field {dtype}"
                    )
                    continue
            self._dtypes = dtypes

    def get_connection(
        self,
        driver: str = 'pg',
        dsn: str = None,
        params: dict = None,
        **kwargs
    ) -> Callable:
        """Useful for internal connections of QS.
        """
        args = {}
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.get_running_loop()
        if driver == 'pg':
            args: dict = {
                "min_size": 2,
                "server_settings": {
                    "application_name": "FlowTask:QS",
                    "client_min_messages": "notice",
                    "jit": "off",
                    "statement_timeout": f"{DB_STATEMENT_TIMEOUT}",
                    "idle_session_timeout": f"{DB_SESSION_TIMEOUT}",
                    "effective_cache_size": "2147483647",
                    "tcp_keepalives_idle": f"{DB_KEEPALIVE_IDLE}",
                },
                "timeout": int(POSTGRES_TIMEOUT),
                **kwargs
            }
        if dsn:
            return AsyncDB(
                driver,
                dsn=dsn,
                loop=loop,
                **args
            )
        elif params:
            return AsyncDB(
                driver,
                params=params,
                loop=loop,
                **args
            )
        if not dsn and not params:
            return self.default_connection()

    def default_connection(self, dsn: str = None):
        try:
            timeout = int(DB_TIMEOUT)
        except TypeError:
            timeout = 360
        if not dsn:
            dsn = default_dsn
        try:
            if self._driver == 'pg':
                kwargs: dict = {
                    "min_size": 2,
                    "server_settings": {
                        "application_name": "FlowTask:CopyToPg",
                        "client_min_messages": "notice",
                        "jit": "off",
                        "statement_timeout": f"{DB_STATEMENT_TIMEOUT}",
                        "idle_session_timeout": f"{DB_SESSION_TIMEOUT}",
                        "effective_cache_size": "2147483647",
                        "tcp_keepalives_idle": f"{DB_KEEPALIVE_IDLE}",
                    },
                    "timeout": timeout,
                }
                loop = asyncio.get_event_loop()
                self._connection = pg(dsn=dsn, loop=loop, **kwargs)
                return self._connection
            if self._driver == 'bigquery':
                self.credentials: dict = {
                    "credentials": BIGQUERY_CREDENTIALS,
                    "project_id": BIGQUERY_PROJECT_ID
                }
            return AsyncDB(
                self._driver,
                dsn=dsn,
                params=self.credentials
            )
        except Exception as err:
            raise ComponentError(
                f"Error configuring Pg Connection: {err!s}"
            ) from err

    def get_driver(self, driver) -> BaseDriver:
        """Getting a Database Driver from Datasource Drivers.
        """
        # load dynamically
        clspath = f'querysource.datasources.drivers.{driver}'
        clsname = f'{driver}Driver'
        try:
            self._dsmodule = import_module(clspath)
            return getattr(self._dsmodule, clsname)
        except (AttributeError, ImportError) as ex:
            raise RuntimeError(
                f"QS: There is no Driver {driver}: {ex}"
            ) from ex

    async def get_datasource(self, name: str):
        """get_datasource.

        Get the datasource from the database.
        """
        try:
            db = self.default_connection()
            async with await db.connection() as conn:
                sql = f"SELECT * FROM public.datasources WHERE name = '{name}'"
                row, error = await conn.queryrow(sql)
                if error:
                    self._logger.warning(f'DS Error: {error}')
                    return False
                try:
                    driver = self.get_driver(row['driver'])
                    # TODO: encrypting credentials in database:
                    if row['dsn']:
                        data = {
                            "dsn": row['dsn']
                        }
                    else:
                        try:
                            data = {
                                **dict(row['params']),
                            }
                        except TypeError:
                            data = dict(row['params'])
                        for key, val in row.get('credentials', {}).items():
                            data[key] = self.get_config_value(
                                key_name=val,
                                default=val
                            )
                        for key, val in row.get('params', {}).items():
                            data[key] = self.get_config_value(
                                key_name=val,
                                default=val
                            )
                    return driver(**data)
                except Exception as ex:  # pylint: disable=W0703
                    self._logger.error(ex)
                    return False
        except Exception as exc:
            self._logger.error(exc)
            return False

    def get_sqlalchemy_connection(self, dsn: str = None):
        # TODO: migrate to async engine
        if not dsn:
            dsn = sqlalchemy_url
        self._engine = create_engine(dsn, echo=False, poolclass=NullPool)
        self._connection = Session(self._engine)
        return self._connection

    async def create_connection(self, driver: str = 'pg'):
        if hasattr(self, "credentials"):
            return self.get_connection(
                driver=driver,
                params=self.credentials
            )
        elif hasattr(self, 'dsn'):
            dsn = self.get_config_value(self.dsn, self.dsn)
            if self.use_sqlalchemy is True:
                if dsn.startswith('postgres:'):
                    dsn = dsn.replace('postgres:', 'postgresql:')
                    return self.get_sqlalchemy_connection(
                        dsn=dsn
                    )
            return self.get_connection(
                driver=self._driver,
                dsn=dsn
            )
        elif hasattr(self, "datasource"):
            datasource = await self.get_datasource(name=self.datasource)
            if datasource.driver_type == 'asyncdb':
                driver = datasource.driver
                return AsyncDB(
                    driver,
                    dsn=datasource.dsn,
                    params=datasource.params()
                )
            else:
                raise ConfigError(
                    f"Invalid Datasource type {datasource.driver_type} for {self.datasource}"
                )
        else:
            return self.default_connection()

    async def get_qs(self, slug, conditions: dict = None):
        result: Any = []
        if not conditions:
            conditions = self.conditions
        try:
            qry = QS(
                slug=slug,
                conditions=conditions,
                loop=asyncio.get_event_loop(),
                lazy=True
            )
            self.add_metric("QS CONDITIONS", conditions)
            await qry.build_provider()
        except (NoData, NoDataFound) as err:
            raise DataNotFound(f"{err!s}") from err
        except Exception as err:
            raise ComponentError(f"{err}") from err
        try:
            res, error = await qry.query()
            if not res:
                raise DataNotFound(f"{slug}: Data Not Found")
            if error:
                if isinstance(error, BaseException):
                    raise error
                else:
                    raise ComponentError(f"Error on Query: {error}")
            result = result + [dict(row) for row in res]
            return result
        except (NoData, DataNotFound, NoDataFound) as err:
            raise DataNotFound(f"{err!s}") from err
        except Exception as err:
            raise ComponentError(f"Error on Query: {err}") from err
        finally:
            try:
                await qry.close()
            except Exception as ex:  # pylint: disable=W0703
                self._logger.warning(ex)
            del qry

    async def get_dataframe(self, result, infer_types: bool = False):
        self.set_datatypes()
        try:
            if self.as_objects is True:
                df = pd.DataFrame(result, dtype=object)
            else:
                df = pd.DataFrame(result, dtype=str)
        except Exception as err:
            self._logger.exception(err, stack_info=True)
            raise ComponentError(f"Unable to create Pandas DataFrame {err}") from err
        # Attempt to infer better dtypes for object columns.
        if infer_types is True:
            try:
                self._logger.debug("Auto-inferencing of Data Types")
                df.infer_objects()
                df = df.convert_dtypes(convert_string=self.to_string)
            except Exception as err:
                self.logger.error(f"QS Error: {err}")
        if self._dtypes:
            for column, dtype in self._dtypes.items():
                self._logger.notice(f"Set Column {column} to type {dtype}")
                try:
                    df[column] = df[column].astype(dtype)
                except (ValueError, TypeError):
                    self._logger.warning(
                        f"Failed to convert column {column} to type {dtype}"
                    )
        if self._debug is True:
            cPrint("Data Types:")
            print(df.dtypes)
        if hasattr(self, "drop_empty"):
            df.dropna(axis=1, how="all", inplace=True)
            df.dropna(axis=0, how="all", inplace=True)
        if hasattr(self, "dropna"):
            df.dropna(subset=self.dropna, how="all", inplace=True)
        if (
            hasattr(self, "clean_strings") and getattr(self, "clean_strings", False) is True
        ):
            u = df.select_dtypes(include=["object", "string"])
            df[u.columns] = u.fillna("")
        numrows = len(df.index)
        self.add_metric("NUMROWS", numrows)
        return df
