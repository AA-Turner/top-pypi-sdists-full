import enum
from typing import Self, override

import pydantic
import sqlalchemy as sa
import yaml

from bir_mcp.hashicorp import ConsulKeyValue
from bir_mcp.utils import set_ssl_cert_file_from_cadata


class Driver(enum.StrEnum):
    oracle = enum.auto()
    postgresql = enum.auto()
    mysql = enum.auto()

    @property
    def name_and_package(self):
        match self:
            case Driver.oracle:
                return "oracle+oracledb"
            case Driver.postgresql:
                return "postgresql+psycopg"
            case Driver.mysql:
                return "mysql+mysqlconnector"

        assert False


class SqlConnection(pydantic.BaseModel):
    driver: Driver
    host: str
    port: int
    database: str | None = None
    username: str
    password: str
    parameters: dict[str, str] | None = None

    @property
    def url(self) -> sa.URL:
        url = sa.URL.create(
            drivername=self.driver.name_and_package,
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            database=self.database,
            query=self.parameters or {},
        )
        return url

    def get_engine(self) -> sa.Engine:
        engine = sa.create_engine(self.url)
        return engine


class SqlContext(pydantic.BaseModel):
    # May need to remove this line for case sensitive table names.
    model_config = pydantic.ConfigDict(str_to_lower=True)

    name: str | None = None
    connection_name: str | None = None
    connection: SqlConnection | None = None
    schema_tables: list[str] = []


class SystemManagedConfig(pydantic.BaseModel):
    gitlab_private_token: str | None = None
    grafana_username: str | None = None
    grafana_password: str | None = None
    grafana_token: str | None = None
    jira_token: str | None = None
    confluence_token: str | None = None
    sonarqube_token: str | None = None
    gitlab_url: str = "https://gitlab.kapitalbank.az"
    grafana_url: str = "https://yuno.kapitalbank.az"
    jira_url: str = "https://jira-support.kapitalbank.az"
    confluence_url: str = "https://confluence.kapitalbank.az"
    sonarqube_url: str = "https://sonarqube.kapitalbank.az"
    ca_file: str | None = None
    sql_connections: dict[str, SqlConnection] = {}
    sql_contexts: list[SqlContext] = []

    def get_grafana_token_or_auth(self) -> str | tuple[str, str] | None:
        if self.grafana_token:
            return self.grafana_token

        if self.grafana_username and self.grafana_password:
            return self.grafana_username, self.grafana_password

        return None

    @classmethod
    def from_consul(
        cls, consul_host: str, consul_key: str, consul_token: str | None = None
    ) -> Self:
        consul_key_value = ConsulKeyValue(host=consul_host, key=consul_key, token=consul_token)
        value = consul_key_value.load()
        config = yaml.safe_load(value)
        config = cls(**config)
        return config

    @override
    def model_post_init(self, context) -> None:
        if self.ca_file:
            set_ssl_cert_file_from_cadata(self.ca_file)

        for sql_context in self.sql_contexts:
            if not sql_context.connection:
                sql_context.connection = self.sql_connections[sql_context.connection_name]
