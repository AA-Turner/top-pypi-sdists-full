from __future__ import annotations  # Required for type hinting in class methods

from collections import defaultdict
# import paramiko
# from sshtunnel import SSHTunnelForwarder
from os.path import expanduser
from typing import Optional

import mysql.connector
from logger_local.MetaLogger import MetaLogger

from .constants_src import LOGGER_CONNECTOR_CODE_OBJECT
from .cursor import Cursor
from .utils import (get_sql_hostname, get_sql_password, get_sql_username, get_sql_port)

# get_ssh_hostname, get_ssh_username, get_ssh_port, get_private_key_file_path)

connections_pool = defaultdict(dict)  # TODO: test multiple users

home = expanduser('~')


# TODO Can we add hostname, IPv4, IPv6, sql statement? Can we have the same message format in all cases?
class Connector(metaclass=MetaLogger, object=LOGGER_CONNECTOR_CODE_OBJECT):
    @staticmethod
    def connect(schema_name: str, *, user: str = get_sql_username(), ignore_cache: bool = False) -> Connector:
        if ignore_cache and schema_name in connections_pool[user]:
            connections_pool[user].pop(schema_name)

        if connections_pool[user].get(schema_name):
            # is_connected is too slow & apparently very rarely needed.
            # We may develop our is_connected with cache & timeout.
            connector = None
            if connections_pool[user][schema_name].connection.is_connected():
                connector = connections_pool[user][schema_name]
            else:
                # reconnect
                connections_pool[user][schema_name].connection.reconnect()
            #     # TODO We should develop retry mechanism to support password rotation and small network issues.
            #     if connections_pool[user][schema_name].connection.is_connected():
            #         connector = connections_pool[user][schema_name]
            #     else:
            #         connector = Connector(schema_name)
            #         Connector.logger.warning("Reconnect failed, returning a new connection",
            #                                  object={'old connection': connections_pool[user][schema_name],
            #                                          'new connection': connector})
            #         connections_pool[user][schema_name] = connector

        else:
            connector = Connector(schema_name)

        return connector

    def __init__(self, schema_name: str, *,
                 host: str = get_sql_hostname(),
                 user: str = get_sql_username(),
                 password: str = get_sql_password(),
                 port: str = get_sql_port()) -> None:
        # ssh_host: str = get_ssh_hostname()) -> None:
        self.host = host
        self.schema = schema_name
        self.user = user
        self.password = password
        self.port = port
        # TODO: installing crypto cause serverless to fail. We should add it as extra to setup.py
        # self.ssh_host = ssh_host
        # self.ssh_user = None
        # self.ssh_port = None
        # if self.ssh_host:
        #     ssh_user: str = get_ssh_username()
        #     ssh_port: str = get_ssh_port()
        #     self.ssh_user = ssh_user
        #     self.ssh_port = ssh_port
        #     print("home=" + home)
        #     print(get_private_key_file_path())
        #     self.private_key = paramiko.RSAKey.from_private_key_file(home + get_private_key_file_path())

        # Checking host suffix
        # TODO: move to sdk.get_sql_hostname
        # TODO Allow in (prod1 environment_name or when we have SSH_HOSTNAME) also to connect to localhost or 127.0.0.1
        if not (self.host.endswith("circ.zone") or self.host.endswith("circlez.ai")):
            self.logger.warning(
                f"Your RDS_HOSTNAME={self.host} which is not what is expected")
        self.connection: mysql.connector = None
        self._cursor: Optional[Cursor] = None
        self._connect_to_db()
        connections_pool[user][schema_name] = self

    def reconnect(self) -> None:
        # Called when the connection is lost
        self.connection.reconnect()
        self._cursor = self.cursor(close_previous=True)
        self.set_schema(self.schema)

    def _connect_to_db(self):
        # if not self.ssh_host:
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.schema,
            port=self.port
        )
        self.logger.info(f"Connected to the database: {self.database_info()}")
        self._cursor = self.connection.cursor()
        self.set_schema(self.schema)
        # else:
        #     # SSH Tunneling
        #     try:
        #         self.tunnel = SSHTunnelForwarder(
        #             (self.ssh_host, int(self.ssh_port)),
        #             ssh_username=self.ssh_user,
        #             ssh_pkey=self.private_key,
        #             remote_bind_address=(self.host, int(self.port)),
        #             local_bind_address=('127.0.0.1',)
        #         )
        #         self.tunnel.start()
        #         self.logger.info(f"SSH tunnel started successfully: {self.tunnel.local_bind_port}")
        #
        #         self.connection = mysql.connector.connect(
        #             user=self.user,
        #             password=self.password,
        #             host='127.0.0.1',
        #             database=self.schema,
        #             port=self.tunnel.local_bind_port
        #         )
        #         self.logger.info(f"Connected to the database via SSH tunnel: {self.database_info()}")
        #         self._cursor = self.connection.cursor()
        #         self.set_schema(self.schema)
        #     except Exception as exception:
        #         self.logger.exception(f"Failed to connect to the database via SSH tunnel: {exception}")
        #         if self.tunnel:
        #             self.tunnel.stop()
        #         raise exception

    def database_info(self) -> str:
        database_info_str = f"host={self.host}, user={self.user}, schema={self.schema}, port={self.port}"
        return database_info_str

    def close(self) -> None:
        try:
            if self._cursor:
                self._cursor.close()
                self.logger.info(f"Cursor closed successfully for schema: {self.schema}")
        except Exception as exception:
            self.logger.error(object={"exception": exception})
        connections_pool[self.user].pop(self.schema, None)
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.logger.info("Connection closed successfully.")

    def cursor(self, *, close_previous: bool = True, cache_previous: bool = False, dictionary: bool = None,
               buffered: bool = None, raw: bool = None,
               prepared: bool = None, named_tuple: bool = None, cursor_class=None) -> Cursor:
        # if cache_previous and self._cursor:
        #     cursor_instance = self._cursor
        #     return cursor_instance
        # if close_previous and self._cursor:
        #     self._cursor.close()

        cursor_instance = Cursor(self.connection.cursor(
            dictionary=dictionary, buffered=buffered, raw=raw, prepared=prepared,
            cursor_class=cursor_class))
        # named_tuple=named_tuple, cursor_class=cursor_class))  named_tuple is deprecated from mysql-connector-python 9.3.0

        # self._cursor = cursor_instance
        return cursor_instance

    def commit(self) -> None:
        self.connection.commit()

    def set_schema(self, new_schema: Optional[str]) -> None:
        if not new_schema:
            return
        if self.schema == new_schema:
            return

        if self._cursor and self.connection and self.connection.is_connected():
            use_query = f"USE `{new_schema}`;"
            self._cursor.execute(use_query)
            connections_pool[self.user][new_schema] = self
            connections_pool[self.user].pop(self.schema, None)
            self.schema = new_schema
            self.logger.info(f"Switched to schema: {new_schema}")
        else:
            raise Exception(
                "Connection is not established. The database will be used on the next connect.")

    def rollback(self):
        self.connection.rollback()

    def start_transaction(self):
        self.connection.start_transaction()
