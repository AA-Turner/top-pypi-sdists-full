import os
from collections.abc import Callable
from abc import abstractmethod
import asyncio
from decimal import Decimal
import numpy as np
import pandas as pd
import datetime
from ..utils import SafeDict
from .flow import FlowComponent
from ..exceptions import (
    ComponentError,
    DataNotFound,
)
from ..interfaces.qs import QSSupport


dtypes = {
    "varchar": str,
    "character varying": str,
    "string": str,
    "object": str,
    "int": int,
    "int4": int,
    "integer": int,
    "bigint": np.int64,
    "int64": np.int64,
    "uint64": np.int64,
    "Int8": int,
    "float64": Decimal,
    "float": Decimal,
    "boolean": bool,
    "bool": bool,
    "datetime64[ns]": datetime.datetime,
    "date": datetime.date,
}

class CopyTo(QSSupport, FlowComponent):
    """
    CopyTo.

    Abstract Class for Copying (saving) a Pandas Dataframe onto a Resource
    (example: Copy to PostgreSQL).

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CopyTo:
          # attributes here
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
        self.pk = []
        self.truncate: bool = False
        self.data = None
        self._engine = None
        self.tablename: str = ""
        self.schema: str = ""
        self.use_chunks = False
        self.chunksize = None
        self._connection: Callable = None
        self._driver: str = kwargs.pop('driver', 'pg')
        self.multi = bool(kwargs.pop('multi', False))
        self._naive_columns: list = kwargs.pop('naive_tz', [])
        self._json_columns: list = kwargs.pop('json_columns', [])
        self._vector_columns: list = kwargs.pop('vector_columns', [])
        self._array_columns: list = kwargs.pop('array_columns', [])
        self._binary_columns: list = kwargs.pop('binary_columns', [])
        self._atomic: bool = kwargs.pop('atomic', False)
        super(CopyTo, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if hasattr(self, 'credentials'):
            self.processing_credentials()
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError(
                "CopyTo: Data Was Not Found"
            )
        for attr, value in self.__dict__.items():
            if isinstance(value, str):
                val = value.format_map(SafeDict(**self._variables))
                object.__setattr__(self, attr, val)
        if not self.schema:
            try:
                self.schema = self._program
            except (ValueError, AttributeError, TypeError) as ex:
                raise ComponentError(
                    "CopyTo: Schema name not defined."
                ) from ex
        # Getting the connection, DSN or credentials:
        self._connection = await self.create_connection(
            driver=self._driver
        )

    async def close(self):
        """Close the connection to Database."""
        try:
            if self._connection:
                await self._connection.close()
                self._logger.info(
                    "CopyTo: Connection closed."
                )
        except Exception as err:
            self._logger.error(
                f"CopyTo: Error closing connection: {err}"
            )

    @abstractmethod
    async def _create_table(self):
        pass

    @abstractmethod
    async def _truncate_table(self):
        pass

    @abstractmethod
    async def _copy_dataframe(self):
        pass

    @abstractmethod
    async def _copy_iterable(self):
        pass

    async def run(self):
        """Run Copy into table functionality."""
        self._result = None
        if self.data is None:
            raise DataNotFound(
                f"{self.__name__} Error: No data in Dataframe"
            )
        if isinstance(self.data, pd.DataFrame) and self.data.empty:
            raise DataNotFound(
                f"{self.__name__} Error: No data in Dataframe"
            )
        # Pass through data to next component.
        self._result = self.data
        if isinstance(self.data, pd.DataFrame):
            columns = list(self.data.columns)
            self.add_metric("NUM_ROWS", self.data.shape[0])
            self.add_metric("NUM_COLUMNS", self.data.shape[1])
            if self._debug:
                print(f"Debugging: {self.__name__} ===")
                for column in columns:
                    t = self.data[column].dtype
                    print(column, "->", t, "->", self.data[column].iloc[0])
        elif isinstance(self.data, list):
            columns = list(self.data[0].keys())
            self.add_metric("NUM_ROWS", len(self.data))
            self.add_metric("NUM_COLUMNS", len(columns))
        else:
            self.add_metric("DATA_SIZE", len(self.data))
        if hasattr(self, "create_table"):
            # Create a Table using Model
            self._logger.debug(
                f":: Creating table: {self.schema}.{self.tablename}"
            )
            await self._create_table()
        if self.truncate is True:
            if self._debug:
                self._logger.debug(
                    f"Truncating table: {self.schema}.{self.tablename}"
                )
            await self._truncate_table()
        if isinstance(self.data, pd.DataFrame):
            # insert data directly into table
            columns = list(self.data.columns)
            await self._copy_dataframe()
        else:
            # insert data using iterable
            await self._copy_iterable()
        self._logger.debug(
            f"{self.__name__}: Saving results into: {self.schema}.{self.tablename}"
        )
        # returning this
        # passing through
        return self._result
