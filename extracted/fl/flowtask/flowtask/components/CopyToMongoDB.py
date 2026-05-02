import asyncio
from collections.abc import Callable
import math
import pandas as pd
import pymongo
from asyncdb import AsyncDB
from asyncdb.exceptions import (
    StatementError,
    DataError
)
from querysource.conf import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_DATABASE,
    DOCUMENTDB_HOSTNAME,
    DOCUMENTDB_PORT,
    DOCUMENTDB_DATABASE,
    DOCUMENTDB_USERNAME,
    DOCUMENTDB_PASSWORD,
    DOCUMENTDB_TLSFILE,
)
from .CopyTo import CopyTo
from ..interfaces.dataframes import PandasDataframe
from ..exceptions import (
    ComponentError,
    DataNotFound
)

class CopyToMongoDB(CopyTo, PandasDataframe):
    """
    CopyToMongo.

    Overview
        This component allows copying data into a MongoDB collection,
        using write functionality from AsyncDB MongoDB driver.

    :widths: auto

    | tablename    |   Yes    | Name of the collection in                              |
    |              |          | MongoDB                                                |
    | schema       |   Yes    | Name of the database                                   |
    |              |          | where the collection is located                        |
    | truncate     |   Yes    | If true, the collection will be emptied                |
    |              |          | before copying new data                                |
    | use_buffer   |   No     | When activated, optimizes performance                  |
    |              |          | for large volumes of data                              |
    | key_field    |   No     | Field to use as unique identifier                      |
    |              |          | for upsert operations                                  |


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CopyToMongoDB:
          schema: hisense
          tablename: product_availability
          dbtype: documentdb
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
        self.tablename: str = ""  # collection name in MongoDB
        self.schema: str = ""     # database name in MongoDB
        self.pk: list = kwargs.get('pk', [])
        self.use_chunks = False
        self._chunksize: int = kwargs.get('chunksize', 1000)
        self._connection: Callable = None
        self.dbtype: str = kwargs.get('dbtype', 'mongo')
        self.key_field: str = kwargs.get('key_field', '_id')
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
        self._driver: str = 'mongo'

    def get_connection(
        self,
        driver: str = 'mongo',
        dsn: str = None,
        params: dict = None,
        **kwargs
    ) -> Callable:
        """Useful for internal connections of QS.
        """
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.get_running_loop()
        if params:
            credentials = params
        if self.dbtype == 'mongo':
            credentials: dict = {
                "host": MONGO_HOST,
                "port": int(MONGO_PORT),
                "database": MONGO_DATABASE
            }
            if MONGO_USER:
                credentials.update({
                    "username": MONGO_USER,
                    "password": MONGO_PASSWORD
                })
        elif self.dbtype == 'documentdb':
            credentials: dict = {
                "host": DOCUMENTDB_HOSTNAME,
                "port": int(DOCUMENTDB_PORT),
                "database": DOCUMENTDB_DATABASE,
                "username": DOCUMENTDB_USERNAME,
                "password": DOCUMENTDB_PASSWORD,
                "tlsCAFile": DOCUMENTDB_TLSFILE,
                "ssl": True,
                "dbtype": "documentdb"
            }
        return AsyncDB(
            'mongo',
            dsn=dsn,
            params=credentials,
            loop=loop,
            timeout=60,
            **kwargs
        )

    def default_connection(self):
        """default_connection.
        Default Connection to MongoDB.
        """
        try:
            credentials = {}
            if self.credentials:
                credentials = self.credentials
            else:
                if self._driver == 'mongo':
                    if self.dbtype == 'mongo':
                        credentials: dict = {
                            "host": MONGO_HOST,
                            "port": int(MONGO_PORT),
                            "database": MONGO_DATABASE
                        }
                        if MONGO_USER:
                            credentials.update({
                                "username": MONGO_USER,
                                "password": MONGO_PASSWORD
                            })
                    elif self.dbtype == 'documentdb':
                        credentials: dict = {
                            "host": DOCUMENTDB_HOSTNAME,
                            "port": int(DOCUMENTDB_PORT),
                            "database": DOCUMENTDB_DATABASE,
                            "username": DOCUMENTDB_USERNAME,
                            "password": DOCUMENTDB_PASSWORD,
                            "tlsCAFile": DOCUMENTDB_TLSFILE,
                            "dbtype": "documentdb",
                            "ssl": True
                        }
            self._connection = AsyncDB(
                self._driver,
                params=credentials,
                loop=self._loop,
                timeout=60
            )
            return self._connection
        except Exception as err:
            raise ComponentError(
                f"Error configuring MongoDB Connection: {err!s}"
            ) from err

    async def _create_table(self):
        """Create a Collection in MongoDB if it doesn't exist."""
        try:
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                db = await conn._select_database()
                collection = db[self.tablename]
                # MongoDB creates collections automatically when data is inserted
                # No explicit creation needed
                # but: we can create a index if a PK instruction is added.
                if isinstance(self.pk, str):
                    index_keys = [(self.pk, pymongo.ASCENDING)]
                elif isinstance(self.pk, list):
                    index_keys = [(field, pymongo.ASCENDING) for field in self.pk]
                else:
                    raise ValueError("self.pk must be a string or list of strings.")
                try:
                    index_name = await collection.create_index(index_keys, unique=True)
                    self._logger.info(f"Unique index ensured: {index_name}")
                    return index_name
                except pymongo.errors.OperationFailure as e:
                    self._logger.warning(f"Failed to create unique index: {e}")
        except Exception as err:
            raise ComponentError(
                f"Error creating MongoDB collection: {err}"
            ) from err

    async def _truncate_table(self):
        """Truncate the MongoDB collection."""
        async with await self._connection.connection() as conn:
            await conn.use(self.schema)
            await conn.execute(
                collection_name=self.tablename,
                operation='delete_many',
                filter={}
            )

    async def _copy_dataframe(self):
        """Copy a pandas DataFrame to MongoDB."""
        try:
            # Clean NA values from string fields
            str_cols = self.data.select_dtypes(include=["string", "object"])
            if not str_cols.empty:
                self.data[str_cols.columns] = str_cols.astype(object).where(
                    pd.notnull(str_cols), None
                )

            # Clean datetime fields
            datetime_cols = self.data.select_dtypes(include=['datetime64[ns]'])
            if not datetime_cols.empty:
                for col in datetime_cols.columns:
                    self.data[col] = self.data[col].apply(
                        lambda x: x.isoformat() if pd.notnull(x) else None
                    )

            # Convert DataFrame to list of dictionaries
            data_records = self.data.to_dict(orient='records')

            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await conn.write(
                    data=data_records,
                    collection=self.tablename,
                    database=self.schema,
                    key_field=self.key_field,
                    if_exists="replace",
                    use_pandas=True
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
        """Copy an iterable to MongoDB."""
        try:
            async with await self._connection.connection() as conn:
                await conn.use(self.schema)
                await conn.write(
                    data=self.data,
                    collection=self.tablename,
                    database=self.schema,
                    key_field=self.key_field,
                    use_pandas=False,
                    if_exists="replace"
                )
        except Exception as err:
            raise ComponentError(
                f"Error copying iterable to MongoDB: {err}"
            ) from err
