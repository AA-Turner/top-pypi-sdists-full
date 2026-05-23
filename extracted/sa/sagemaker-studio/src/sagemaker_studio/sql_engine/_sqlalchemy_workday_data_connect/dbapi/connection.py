"""DB-API 2.0 Connection for Workday Data Connect.

Creates a trino connection using DataServiceConfig and SDEAuth internally.
"""

import trino

from .auth import DataServiceConfig, SDEAuth
from .cursor import Cursor
from .exceptions import InterfaceError


class Connection:
    """DB-API 2.0 Connection that wraps a trino connection with Workday auth."""

    def __init__(
        self,
        host,
        port,
        client_id,
        isu,
        token_endpoint,
        private_key,
        catalog=None,
        schema=None,
        include_path_prefix=None,
        session_properties=None,
        **kwargs
    ):
        properties = {
            "host": host,
            "port": str(port),
            "client_id": client_id,
            "isu": isu,
            "token_endpoint": token_endpoint,
            "private_key": private_key,
        }
        if catalog:
            properties["catalog"] = catalog
        if schema:
            properties["schema"] = schema
        if include_path_prefix is not None:
            properties["include_path_prefix"] = str(include_path_prefix)
        if session_properties:
            properties["session_properties"] = session_properties

        self._config = DataServiceConfig(properties)
        self._auth = SDEAuth(self._config)
        self._closed = False

        session_props = self._config.session_properties
        self._trino_conn = trino.dbapi.connect(
            host=self._config.host,
            port=self._config.port,
            catalog=self._config.catalog,
            schema=self._config.schema,
            http_scheme="https",
            auth=self._auth,
            session_properties=session_props,
        )

    @property
    def schema(self):
        return self._trino_conn.schema

    @property
    def transaction(self):
        return self._trino_conn.transaction

    def cursor(self):
        if self._closed:
            raise InterfaceError("Connection is closed")
        return Cursor(self._trino_conn.cursor())

    def commit(self):
        self._trino_conn.commit()

    def rollback(self):
        self._trino_conn.rollback()

    def close(self):
        if not self._closed:
            self._trino_conn.close()
            self._closed = True
