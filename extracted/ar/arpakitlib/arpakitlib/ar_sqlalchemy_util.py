# arpakit
import asyncio
import logging
from datetime import timedelta, datetime
from typing import Any, Collection
from urllib.parse import quote_plus
from uuid import uuid4

import sqlalchemy
from sqlalchemy import create_engine, QueuePool, text, func, inspect, AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm.session import Session

from arpakitlib.ar_datetime_util import now_utc_dt

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def generate_sqlalchemy_url(
        *,
        base: str = "postgresql",
        user: str | None = None,
        password: str | None = None,
        host: str | None = "127.0.0.1",
        port: int | None = 5432,
        database: str | None = None,
        **query_params
) -> str | None:
    if host is None or port is None:
        return None

    auth_part = ""
    if user and password:
        auth_part = f"{quote_plus(user)}:{quote_plus(password)}@"
    elif user:
        auth_part = f"{quote_plus(user)}@"

    if base.startswith("sqlite"):
        host_part = ""
    else:
        host_part = f"{host}"
        if port:
            host_part += f":{port}"

    database_part = f"/{database}" if database else ""
    if base.startswith("sqlite") and database:
        database_part = f"/{database}"

    query_part = ""
    if query_params:
        query_items = [f"{key}={quote_plus(str(value))}" for key, value in query_params.items()]
        query_part = f"?{'&'.join(query_items)}"

    return f"{base}://{auth_part}{host_part}{database_part}{query_part}"


class BaseDBM(DeclarativeBase):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    _bus_data: dict[str, Any] | None = None

    @property
    def bus_data(self) -> dict[str, Any]:
        if self._bus_data is None:
            self._bus_data = {}
        return self._bus_data

    def simple_dict(
            self,
            *,
            need_include_columns: bool = True,
            need_include_sd_properties: bool = True,
            include_columns: Collection[str] | None = None,
            exclude_columns: Collection[str] | None = None,
            include_sd_properties: Collection[str] | None = None,
            exclude_sd_properties: Collection[str] | None = None,
            include_columns_and_sd_properties: Collection[str] | None = None,
            kwargs: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        if exclude_columns is None:
            exclude_columns = set()
        if exclude_sd_properties is None:
            exclude_sd_properties = set()

        res = {}

        if need_include_columns:
            for c in inspect(self).mapper.column_attrs:
                if include_columns_and_sd_properties is not None and c.key not in include_columns_and_sd_properties:
                    continue
                if include_columns is not None and c.key not in include_columns:
                    continue
                if c.key in exclude_columns:
                    continue
                value = getattr(self, c.key)
                res[c.key] = value

        if need_include_sd_properties:
            for attr_name in dir(self):
                if not attr_name.startswith("sdp_") or not isinstance(getattr(type(self), attr_name, None), property):
                    continue

                sd_property_name = attr_name.removeprefix("sdp_")

                if (
                        include_columns_and_sd_properties is not None
                        and sd_property_name not in include_columns_and_sd_properties
                ):
                    continue
                if include_sd_properties is not None and sd_property_name not in include_sd_properties:
                    continue
                if sd_property_name in exclude_sd_properties:
                    continue

                res[sd_property_name] = getattr(self, attr_name)

        if kwargs is not None:
            res.update(kwargs)

        return res


class SQLAlchemyDb:
    def __init__(
            self,
            *,
            sync_db_url: str | None = "postgresql://arpakitlib:arpakitlib@localhost:50517/arpakitlib",
            async_db_url: str | None = "postgresql+asyncpg://arpakitlib:arpakitlib@localhost:50517/arpakitlib",
            db_echo: bool = False,
            base_dbm: type[BaseDBM] | None = None,
            db_models: list[Any] | None = None,
    ):
        self._logger = logging.getLogger(self.__class__.__name__)

        self.db_url = sync_db_url
        if self.db_url is not None:
            self.engine = create_engine(
                url=sync_db_url,
                echo=db_echo,
                pool_size=10,
                max_overflow=10,
                poolclass=QueuePool,
                pool_timeout=timedelta(seconds=30).total_seconds(),
            )
        self.sessionmaker = sessionmaker(bind=self.engine)
        self.func_new_session_counter = 0

        self.async_db_url = async_db_url
        if self.async_db_url is not None:
            self.async_engine = create_async_engine(
                url=async_db_url,
                echo=db_echo,
                pool_size=10,
                max_overflow=10,
                poolclass=AsyncAdaptedQueuePool,
                pool_timeout=timedelta(seconds=30).total_seconds()
            )
        self.async_sessionmaker = async_sessionmaker(bind=self.async_engine)
        self.func_new_async_session_counter = 0

        self.base_dbm = base_dbm
        self.db_models = db_models

    def is_table_exists(self, table_name: str) -> bool:
        with self.engine.connect() as connection:
            inspector = inspect(connection)
            return table_name in inspector.get_table_names()

    def drop_celery_tables(self):
        with self.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS celery_tasksetmeta CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS celery_taskmeta CASCADE;"))
            connection.commit()
        self._logger.info("celery tables were dropped")

    def remove_celery_tables_data(self):
        if not self.is_table_exists("celery_tasksetmeta"):
            self._logger.info("table celery_tasksetmeta not exists")
            return
        with self.engine.connect() as connection:
            connection.execute(text("DELETE FROM celery_tasksetmeta;"))
            connection.execute(text("DELETE FROM celery_taskmeta;"))
            connection.commit()
        self._logger.info("celery tables data were removed")

    def drop_alembic_tables(self):
        with self.engine.connect() as connection:
            connection.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
            connection.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
            connection.commit()
        self._logger.info("alembic_version tables were dropped")

    def remove_alembic_tables_data(self):
        if not self.is_table_exists("alembic_version"):
            self._logger.info("table alembic_version not exists")
            return
        with self.engine.connect() as connection:
            connection.execute(text("DELETE FROM alembic_version;"))
            connection.commit()
        self._logger.info("alembic tables data were removed")

    def init(self):
        self.base_dbm.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("inited")

    def drop(self):
        self.base_dbm.metadata.drop_all(bind=self.engine, checkfirst=True)
        self._logger.info("dropped")

    def reinit(self):
        self.base_dbm.metadata.drop_all(bind=self.engine, checkfirst=True)
        self.base_dbm.metadata.create_all(bind=self.engine, checkfirst=True)
        self._logger.info("reinited")

    def reinit_all(self):
        self.reinit()
        self.remove_alembic_tables_data()
        self.remove_celery_tables_data()
        self._logger.info("all reinited")

    def check_conn(self):
        self.engine.connect()
        self._logger.info("db conn is good")

    def new_session(self, **kwargs) -> Session:
        self.func_new_session_counter += 1
        return self.sessionmaker(**kwargs)

    def new_async_session(self, **kwargs) -> AsyncSession:
        self.func_new_async_session_counter += 1
        return self.async_sessionmaker(**kwargs)

    def is_conn_good(self) -> bool:
        try:
            self.check_conn()
        except Exception as e:
            self._logger.error(e)
            return False
        return True

    def generate_unique_id(self, *, class_dbm: Any):
        with self.new_session() as session:
            res: int = session.query(func.max(class_dbm.id)).scalar()
            while session.query(class_dbm).filter(class_dbm.id == res).first() is not None:
                res += 1
        return res

    def generate_unique_long_id(self, *, class_dbm: Any):
        with self.new_session() as session:
            res: str = str(uuid4())
            while session.query(class_dbm).filter(class_dbm.long_id == res).first() is not None:
                res = str(uuid4())
        return res

    def generate_creation_dt(self) -> datetime:
        return now_utc_dt()

    async def async_get_table_name_to_amount(self) -> dict[str, int]:
        res = {}

        async with self.new_async_session() as async_session:
            for table_name, table in BaseDBM.metadata.tables.items():
                res[table_name] = await async_session.scalar(
                    sqlalchemy.select(
                        sqlalchemy.func.count(1)
                    ).select_from(table)
                )

        return res

    def get_table_name_to_amount(self) -> dict[str, int]:
        res = {}

        with self.new_session() as session:
            for table_name, table in BaseDBM.metadata.tables.items():
                res[table_name] = session.scalar(
                    sqlalchemy.select(
                        sqlalchemy.func.count(1)
                    ).select_from(table)
                )

        return res


def get_string_info_from_declarative_base(class_: type[DeclarativeBase]):
    res = f"Db Models: {len(class_.__subclasses__())}"
    for i, cls in enumerate(class_.__subclasses__()):
        res += f"\n{i + 1}. {cls.__name__}"
    return res


def __example():
    pass


async def __async_example():
    pass


if __name__ == '__main__':
    __example()
    asyncio.run(__async_example())
