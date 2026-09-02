from typing import Any, ClassVar, Optional, Union
from datetime import datetime, timezone
from datamodel import BaseModel, Field
from asyncpg.exceptions import UniqueViolationError
from asyncdb import AsyncDB
from asyncdb.utils.types import Entity
from navconfig.logging import logging
from querysource.conf import default_dsn, async_default_dsn
from querysource.outputs.tables import PgOutput


class AbstractPayload(BaseModel):
    """Abstract Payload Model.

    Common fields implemented by any Object in NetworkNinja Payloads.
    """
    orgid: int
    inserted_at: datetime = Field(required=False, default=datetime.now)
    _pgoutput: ClassVar[Optional[Any]] = None

    def __post_init__(self):
        super().__post_init__()
        object.__setattr__(self, '_pgoutput', PgOutput(
            dsn=async_default_dsn,
            use_async=True
        ))

    def ensure_timezone(self, dt: Union[datetime, None]) -> Union[datetime, None]:
        """Ensure a datetime has timezone information."""
        if dt is None:
            return None
        if isinstance(dt, datetime.datetime) and dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt

    async def sync(self, **kwargs):
        """
        Sync the Object with the Database
        """
        return await self.upsert_record(**kwargs)

    async def upsert_record(self, **kwargs):
        """Upsert Record to Database.
        """
        # output = PgOutput(dsn=async_default_dsn, use_async=True)
        # Synchronize self object into the database using Upsert.
        fields = self.columns()
        # remove from column list the "_pgoutput" field
        fields.pop('_pgoutput', None)
        pk = kwargs.get('pk', [])
        if not pk:
            for _, field in fields.items():
                if field.primary_key:
                    pk.append(field.name)
        async with self._pgoutput as conn:
            try:
                if self.Meta.name:
                    return await conn.do_upsert(
                        self,
                        table_name=self.Meta.name,
                        schema=self.Meta.schema,
                        primary_keys=pk,
                        use_conn=conn.get_connection()
                    )
                else:
                    logging.warning(
                        f"Unable to Upsert NetworkNinja record: {self.Meta}"
                    )
                    return None
            except Exception as e:
                logging.error(
                    f"Error Upserting Record: {e}"
                )
                return None

    async def _sync_object(self, conn: Any):
        pass

    async def on_sync(self, conn: Any, upsert: bool = True):
        """
        Sync Current Object with the Database.
        """
        await self._sync_object(conn)

    async def save(self, conn: Any, pk: Union[str, list] = None, **kwargs):
        """
        Save the Object to the Database.
        """
        if isinstance(pk, str):
            pk = [pk]
        # Create a string with the WHERE clause (a = 1 AND b = 2)
        conditions = [f"{k} = ${i+1}" for i, k in enumerate(pk)]
        _where = " AND ".join(conditions)
        _values = [getattr(self, k) for k in pk]
        qry = f"SELECT EXISTS (SELECT 1 FROM {self.Meta.schema}.{self.Meta.name} WHERE {_where})"
        # print('QUERY INSERT > ', qry, _values)
        try:
            exists = await conn.fetchval(qry, *_values)
        except Exception as e:
            print('ERROR EXISTS > ', e)
            exists = False
        # print('EXISTS > ', exists, type(exists))
        if exists:
            # Making an Upsert:
            return await self.upsert_record(pk=pk, **kwargs)
        else:
            # Doing a Faster insert:
            logging.debug(
                f"Inserting new record: {self.Meta.schema}.{self.Meta.name}"
            )
            return await self.insert_record(conn)

    async def insert_record(self, conn: Any, **kwargs):
        """Insert Record to Database.
        """
        # Convert all objects in dataclass into a INSERT statement
        columns = self.get_fields()
        # remove from column list the "_pgoutput" field
        columns = [col for col in columns if col != '_pgoutput']
        cols = ",".join(columns)
        data = self.to_dict(as_values=True)
        # print('DATA > ', data)
        data.pop('_pgoutput', None)
        _values = ', '.join([f"${i+1}" for i, _ in enumerate(columns)])
        insert = f"INSERT INTO {self.Meta.schema}.{self.Meta.name}({cols}) VALUES({_values})"
        try:
            # Convert data dictionary into a list, ordered by column list:
            source = [data.get(col) for col in columns]
            stmt = await conn.engine().prepare(insert)
            result = await stmt.fetchrow(*source, timeout=2)
            # logging.debug(f"Result: {result}, Status: {stmt.get_statusmsg()}")
            return True
        except Exception as e:
            logging.error(
                f"Error Inserting Record: {e}"
            )
            return False

    async def update_many(
        self,
        objects: list,
        primary_keys: list = None,
        **kwargs
    ):
        """Upsert Several Records in Database.
        """
        output = PgOutput(dsn=async_default_dsn, use_async=True)
        # Synchronize self object into the database using Upsert.
        if not primary_keys:
            fields = self.columns()
            pk = []
            for _, field in fields.items():
                if field.primary_key:
                    pk.append(field.name)
        else:
            pk = primary_keys
        async with output as conn:
            try:
                if self.Meta.name:
                    await conn.upsert_many(
                        objects,
                        table_name=self.Meta.name,
                        schema=self.Meta.schema,
                        primary_keys=pk,
                        # use_conn=conn.get_connection()
                    )
                    return True
                else:
                    logging.warning(
                        f"Unable to Upsert NetworkNinja record: {self.Meta}"
                    )
                    return None
            except Exception as e:
                logging.error(
                    f"Error Upserting Record: {e}"
                )
                return None
