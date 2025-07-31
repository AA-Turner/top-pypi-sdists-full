from dataclasses import dataclass
from typing import Optional
import warnings

from _qwak_proto.qwak.feature_store.sources.batch_pb2 import (
    BatchSource as ProtoBatchSource,
    SnowflakeSource as ProtoSnowflakeSource,
)
from _qwak_proto.qwak.feature_store.sources.data_source_pb2 import (
    DataSourceSpec as ProtoDataSourceSpec,
)
from qwak.exceptions import QwakException
from qwak.feature_store.data_sources.batch._batch import BaseBatchSource

warnings.simplefilter("once", DeprecationWarning)


@dataclass
class SnowflakeSource(BaseBatchSource):
    host: str
    username_secret_name: str
    database: str
    schema: str
    warehouse: str
    password_secret_name: Optional[str] = None
    pem_private_key_secret_name: Optional[str] = None
    table: Optional[str] = None
    query: Optional[str] = None
    repository: Optional[str] = None

    def __post_init__(self):
        self._validate()

    def _validate(self):
        if not self.username_secret_name:
            raise QwakException("username_secret_name must be set!")

        if not self.database:
            raise QwakException("database must be set!")

        if not self.schema:
            raise QwakException("schema must be set!")

        if self.password_secret_name:
            warnings.warn(
                "Snowflake basic authentication is deprecated and should not be used. Use key-pair authentication instead.",
                DeprecationWarning,
            )

        no_unique_source_exception_message = "Only one of query or table may be set"
        has_table = bool(self.table)
        has_query = bool(self.query)
        no_source_set = not (has_table or has_query)
        both_source_set = has_table and has_query
        if no_source_set or both_source_set:
            raise QwakException(no_unique_source_exception_message)

        no_unique_auth_exception_message = "Exactly one of 'password_secret_name' or 'pem_private_key_secret_name' must be set"
        has_password_secret = bool(self.password_secret_name)
        has_pem_private_key_secret = bool(self.pem_private_key_secret_name)
        no_auth_set = not (has_password_secret or has_pem_private_key_secret)
        both_auth_set = has_password_secret and has_pem_private_key_secret
        if no_auth_set or both_auth_set:
            raise QwakException(no_unique_auth_exception_message)

    def _to_proto(self, artifact_url: Optional[str] = None):
        return ProtoDataSourceSpec(
            data_source_repository_name=self.repository,
            batch_source=ProtoBatchSource(
                name=self.name,
                description=self.description,
                date_created_column=self.date_created_column,
                snowflakeSource=ProtoSnowflakeSource(
                    host=self.host,
                    username_secret_name=self.username_secret_name,
                    password_secret_name=self.password_secret_name,
                    pem_private_key_secret_name=self.pem_private_key_secret_name,
                    database=self.database,
                    schema=self.schema,
                    warehouse=self.warehouse,
                    table=self.table,
                    query=self.query,
                ),
            ),
        )

    @classmethod
    def _from_proto(cls, proto):
        snowflake = proto.snowflakeSource
        return cls(
            name=proto.name,
            date_created_column=proto.date_created_column,
            description=proto.description,
            host=snowflake.host,
            username_secret_name=snowflake.username_secret_name,
            password_secret_name=snowflake.password_secret_name,
            pem_private_key_secret_name=snowflake.pem_private_key_secret_name,
            database=snowflake.database,
            schema=snowflake.schema,
            warehouse=snowflake.warehouse,
            table=snowflake.table,
            query=snowflake.query,
        )
