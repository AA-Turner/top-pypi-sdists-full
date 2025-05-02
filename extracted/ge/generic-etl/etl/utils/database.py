import os
from typing import Dict, Optional, Tuple, Union

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine

BASICS = {
    "sqlite": {"delete": "DELETE FROM {table}"},
    "postgres": {"delete": "DELETE FROM {table}"},
}


import logging

logger = logging.getLogger(__name__)


class Database:
    target_host: str = ""
    engine: Optional[Engine] = None
    host_type: str = ""

    def __init__(self, secrets: dict, host: str):
        """Init function"""
        self.secrets = secrets
        self.target_host = host

    def __enter__(self):
        """Entry context, sets engine"""
        host_type, engine = self._get_connection_string()
        self.engine = engine
        self.host_type = host_type
        return self

    def __exit__(self, type, value, traceback):
        """Exit context, disposes engine"""
        if self.engine:
            try:
                self.engine.dispose()
            except AttributeError:
                self.engine.close()

    def execute(
        self,
        sql: Optional[str] = None,
        basic: Optional[str] = None,
        table: Optional[str] = None,
    ) -> Optional[pd.DataFrame]:
        """Execute SQL

        param :optional sql, str: SQL to run--could point to sql file
        param :optional basic, str: Baisc command to run
        param :optional table, str: Table to target

        Returns :Optional[pd.DataFrame]: Dataframe of data
        """
        df = None
        if basic:
            sql: str = BASICS.get(self.host_type, {}).get(basic, None)
            sql = sql.format(table=table)

        if os.path.exists(os.path.dirname(sql)):
            with open(sql, "r") as f:
                sql = " ".join([line.strip() for line in f if line.strip()])

        try:
            df = pd.read_sql(sql, self.engine)
        except Exception as ex:
            logger.error(ex)
            logger.info("continuing...")

        return df

    def _get_connection_string(self) -> Tuple[str, Engine]:
        """Returns correct engine

        Returns :Tuple(str,Engine): host type and engine
        """
        print(self.target_host)
        if self.target_host not in self.secrets.keys():
            raise KeyError(f"Missing {self.target_host} in secrets")

        info = self.secrets.get(self.target_host)
        if "postgres" in info["type"]:
            username, password, host, port, database = (
                info.get("username", None),
                info.get("password", None),
                info.get("host", None),
                info.get("port", None),
                info.get("database", None),
            )
            return "postgres", create_engine(
                f"postgresql://{username}:{password}@{host}:{port}/{database}"
            )
        elif "oracle" in info["type"]:
            import cx_Oracle

            username, password, host, port, service_name, db_alias = (
                info.get("username", None),
                info.get("password", None),
                info.get("host", None),
                info.get("port", None),
                info.get("service_name", None),
                info.get("db_alias", None),
            )
            cx_Oracle.makedsn(host, port, service_name=service_name)
            connection = cx_Oracle.connect(username, password, db_alias)
            return "oracle", connection
        elif "odbc" in info["type"]:
            username, password, host, port, database, driver_path, driver_type = (
                info.get("username", None),
                info.get("password", None),
                info.get("host", None),
                info.get("port", None),
                info.get("database", None),
                info.get("driver_path", None),
                info.get("driver_type", None),
            )

            return "odbc", create_engine(
                f"""{driver_type}://{username}:{password}@{host}/{database}?driver={driver_path}&port={port}&odbc_options='TDS_Version=8.0'"""
            )
        elif "mssql" in info["type"]:
            username, password, port, dsn = (
                info.get("username", None),
                info.get("password", None),
                info.get("port", None),
                info.get("dsn", None),
            )
            return "myssql", create_engine(
                f"mssql+pyodbc://{username}:{password}@{dsn}"
            )
        elif "mysql" in info["type"]:
            username, password, host, port, database = (
                info.get("username", None),
                info.get("password", None),
                info.get("host", None),
                info.get("port", None),
                info.get("database", None),
            )
            return "mysql", create_engine(
                f"mysql://{username}:{password}@{host}:{port}/{database}"
            )
        elif "sqlite" in info["type"]:
            dbfile = info.get("dbfile", None)
            return "sqlite", create_engine(f"sqlite:///{os.path.abspath(dbfile)}")
        else:
            raise NotImplementedError(f"{info['type']} is not supported yet")
