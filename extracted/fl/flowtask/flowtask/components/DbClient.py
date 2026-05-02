from abc import ABC
from typing import Union, Optional
from pathlib import PurePath
import aiofiles
import pandas
from asyncdb.drivers.base import BaseDriver
from asyncdb.exceptions import NoDataFound
from navconfig.logging import logging
from ..utils import cPrint
from ..utils.functions import is_empty, as_boolean
from ..exceptions import ComponentError, FileError, DataNotFound
from ..interfaces import DBInterface


class DbClient(DBInterface):
    """
    DbClient.

    Abstract base class for database clients using AsyncDB.

    Provides common methods for connecting to a database, executing queries,
    and handling results.

    Inherits from the `DBInterface` interface.

    .. note::
    This class is intended to be subclassed by specific database client implementations.

    .. table:: Properties
    :widths: auto

    +--------------------+----------+--------------------------------------------------------------------------------+
    | Name               | Required | Description                                                                    |
    +--------------------+----------+--------------------------------------------------------------------------------+
    | driver             |   Yes    | Database driver to use (e.g., "pg" for PostgreSQL).                            |
    +--------------------+----------+--------------------------------------------------------------------------------+
    | credentials        |   Yes    | Dictionary containing database connection credentials (user, password, etc.).  |
    |                    |          | Defined by the `_credentials` class attribute.                                 |
    +--------------------+----------+--------------------------------------------------------------------------------+
    | raw_result         |    No    | Boolean flag indicating whether to return raw query results or convert them    |
    |                    |          | to dictionaries (defaults to False).                                           |
    +--------------------+----------+--------------------------------------------------------------------------------+
    | infer_types        |    No    | Boolean flag indicating whether to infer data types for pandas DataFrames      |
    |                    |          | created from query results (defaults to False).                                |
    +--------------------+----------+--------------------------------------------------------------------------------+
    | as_dataframe       |    No    | Boolean flag indicating whether to convert query results to a pandas DataFrame |
    |                    |          | (defaults to True).                                                            |
    +--------------------+----------+--------------------------------------------------------------------------------+
    | as_string          |    No    | Boolean flag indicating whether to convert object columns in DataFrames        |
    |                    |          | to strings (defaults to False). Converting to strings requires type            |
    |                    |          | inference (set `infer_types` to True if used).                                 |
    +--------------------+----------+--------------------------------------------------------------------------------+

    .. returns::
    varies
        The return value of the `_query` method depends on the `raw_result` and `as_dataframe` properties:
            * If `raw_result` is True: Returns the raw result object specific to the database driver.
            * If `raw_result` is False and `as_dataframe` is True: Returns a pandas DataFrame containing the query results.
            * If `raw_result` is False and `as_dataframe` is False: Returns a list of dictionaries representing the query results.
        Raises exceptions for errors during execution (e.g., `DataNotFound`, `ComponentError`).
    """  # noqa
    _credentials = {
        "user": str,
        "password": str,
        "host": str,
        "port": int,
        "database": str,
    }

    def __init__(
        self,
        *args,
        **kwargs
    ) -> None:
        self.raw_result: bool = kwargs.pop("raw_result", False)
        self.infer_types: bool = as_boolean(kwargs.pop("infer_types", False))
        self.as_dataframe: bool = as_boolean(kwargs.pop("as_dataframe", True))
        # using "string" instead objects in pandas
        self.as_string: bool = as_boolean(kwargs.pop("as_string", False))
        super().__init__(*args, **kwargs)
        if self.as_string is True:
            self.infer_types = True
        # any other argument
        self._args = kwargs

    async def open_sqlfile(self, file: PurePath, **kwargs) -> str:
        if file.exists() and file.is_file():
            content = None
            # open SQL File:
            async with aiofiles.open(file, "r+") as afp:
                content = await afp.read()
                # check if we need to replace masks
            if hasattr(self, "masks"):
                content = self.mask_replacement(content)
            if self.use_template is True:
                content = self._templateparser.from_string(content, kwargs)
            return content
        else:
            raise FileError(
                f"{__name__}: Missing SQL File: {file}"
            )

    async def close(self, connection: BaseDriver = None) -> None:
        if not connection:
            connection = self._connection
        try:
            if connection is not None:
                await connection.close()
        except Exception as err:  # pylint: disable=W0703
            logging.error(
                f"DbClient Closing error: {err}"
            )

    async def _query(
        self, query: Union[str, dict], connection: BaseDriver = None
    ) -> Union[list, dict]:
        if not connection:
            connection = self._connection
        try:
            if isinstance(query, dict):
                result, error = await connection.query(**query)
                print('RESULT > ', result, error)
            else:
                result, error = await connection.query(query)
            if error:
                raise ComponentError(
                    f"DbClient: Query Error: {error}"
                )
            if self.raw_result is True:
                return result
            else:  # converting to dict
                result = [dict(row) for row in result]
                return result
        except (DataNotFound, NoDataFound) as err:
            raise DataNotFound("DbClient: Data not found") from err
        except Exception as err:
            raise ComponentError(f"{err}") from err

    async def get_dataframe(self, result):
        try:
            df = pandas.DataFrame(result)
        except Exception as err:  # pylint: disable=W0703
            logging.exception(err, stack_info=True)
        # Attempt to infer better dtypes for object columns.
        if is_empty(df):
            raise DataNotFound("DbClient: Data not Found")
        df.infer_objects()
        if self.infer_types is True:
            df = df.convert_dtypes(convert_string=self.as_string)
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
        return df
