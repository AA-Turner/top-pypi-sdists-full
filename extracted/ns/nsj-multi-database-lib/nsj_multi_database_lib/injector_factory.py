import os

from sqlalchemy.engine.base import Connection
from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase


class InjectorFactory(NsjInjectorFactoryBase):

    _use_external_db: bool
    _use_external_db_with_default_credentials: bool

    def __init__(
        self, use_external_db=False, use_external_db_with_default_credentials=False
    ) -> None:
        self._use_external_db = use_external_db
        self._use_external_db_with_default_credentials = (
            use_external_db_with_default_credentials
        )
        super().__init__()

    def __enter__(self):
        from nsj_multi_database_lib.db_pool_config import (
            create_external_pool,
            create_external_pool_with_default_credentials,
            create_test_pool,
            create_erpsql_pool,
        )

        if os.getenv("ENV", "").lower() == "erp_sql":
            pool = create_erpsql_pool()
            self._db_connection = pool.connect()
        elif self._use_external_db_with_default_credentials:
            pool = create_external_pool_with_default_credentials()
            self._db_connection = pool.connect()
        elif self._use_external_db:
            pool = create_external_pool()
            self._db_connection = pool.connect()
            # TODO Rever: Ajustando a codificação para UTF8
            # self._db_connection.execute("set client_encoding = 'UTF-8'")
        else:
            self._db_connection = create_test_pool().connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_connection.close()

    def db_adapter(self):
        from nsj_gcf_utils.db_adapter2 import DBAdapter2

        return DBAdapter2(self._db_connection)
