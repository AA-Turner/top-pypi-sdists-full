import asyncio
from collections.abc import Callable
import math
import pandas as pd
from asyncdb import AsyncDB
from asyncdb.exceptions import (
    StatementError,
    DataError
)
from .CopyTo import CopyTo
from ..interfaces.dataframes import PandasDataframe
from ..exceptions import (
    ComponentError,
    DataNotFound
)
from ..conf import (
    RT_DRIVER,
    RT_HOST,
    RT_PORT,
    RT_USER,
    RT_PASSWORD,
    RT_DATABASE
)


class CopyToRethink(CopyTo, PandasDataframe):
    """
    CopyToRethink.

    Overview

        This component allows copy data into a RethinkDB table,
        Copy into main rethinkdb using write functionality.

       :widths: auto


    | tablename    |   Yes    | Name of the table in                                   |
    |              |          | the database                                           |
    | schema       |   Yes    | Name of the schema                                     |
    |              |          | where is to the table, alias: database                 |
    | truncate     |   Yes    | This option indicates if the component should empty    |
    |              |          | before coping the new data to the table. If set to true|
    |              |          | the table will be truncated before saving the new data.|
    | use_buffer   |   No     | When activated, this option allows optimizing the      |
    |              |          | performance of the task, when dealing with large       |
    |              |          | volumes of data.                                       |
    | credentials  |   No     | Supporting manual rethinkdb credentials                |
    |              |          |                                                        |
    | datasource   |   No     | Using a Datasource instead manual credentials          |
    |              |          |                                                        |


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CopyToRethink:
          tablename: product_availability
          schema: bose
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
        self._chunksize: int = kwargs.pop('chunksize', 10)
        self._connection: Callable = None
        try:
            self.multi = bool(kwargs["multi"])
            del kwargs["multi"]
        except KeyError:
            self.multi = False
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )
        self._driver: str = RT_DRIVER

    def default_connection(self):
        """default_connection.

        Default Connection to RethinkDB.
        """
        try:
            kwargs: dict = {
                "host": RT_HOST,
                "port": int(RT_PORT),
                "db": RT_DATABASE,
                "user": RT_USER,
                "password": RT_PASSWORD
            }
            self._connection = AsyncDB(
                RT_DRIVER,
                params=kwargs,
                loop=self._loop,
                **kwargs
            )
            return self._connection
        except Exception as err:
            raise ComponentError(
                f"Error configuring Pg Connection: {err!s}"
            ) from err

    # Function to clean invalid float values
    def clean_floats(self, data):
        def sanitize_value(value):
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                return None  # Replace invalid floats with None or other default
            return value

        if isinstance(data, dict):
            return {k: sanitize_value(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.clean_floats(item) for item in data]
        return data

    async def _create_table(self):
        # Create a Table using Model
        async with await self._connection.connection() as conn:
            await conn.use(self.schema)
            await self._connection.create_table(
                table=self.tablename
            )

    async def _truncate_table(self):
        async with await self._connection.connection() as conn:
            await conn.use(self.schema)
            await self._connection.delete(
                table=self.tablename
            )

    async def _copy_dataframe(self):
        # saving directly the dataframe with write
        try:
            # can remove NAT from str fields:
            u = self.data.select_dtypes(include=["string"])
            if not u.empty:
                self.data[u.columns] = u.astype(object).where(
                    pd.notnull(u), None
                )
            # Convert the DataFrame to list of dictionaries and clean it
            data_records = self.data.to_dict(orient='records')
            cleaned_data = self.clean_floats(data_records)
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await self._connection.write(
                    table=self.tablename,
                    data=cleaned_data,
                    batch_size=self._chunksize,
                    on_conflict="replace",
                    changes=True,
                    durability="soft",
                )
        except StatementError as err:
            raise ComponentError(
                f"Statement error: {err}"
            ) from err
        except DataError as err:
            raise ComponentError(
                f"Data error: {err}"
            ) from err
        except Exception as err:
            raise ComponentError(
                f"{self.StepName} Error: {err!s}"
            ) from err

    async def _copy_iterable(self):
        """Copy an iterable to RethinkDB."""
        try:
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await conn.write(
                    data=self.data,
                    table=self.tablename,
                    database=self.schema,
                    batch_size=self._chunksize,
                    on_conflict="replace",
                    changes=True,
                    durability="soft",
                )
        except Exception as err:
            raise ComponentError(
                f"Error copying iterable to RethinkDB: {err}"
            ) from err
