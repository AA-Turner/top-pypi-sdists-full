import logging
import warnings
from typing import Any
from typing import Callable
from typing import List
from typing import Optional
from typing import Union
from urllib.parse import urlparse

import attrs
import pandas
import pyarrow
import sqlparse


try:
    import snowflake.connector
    from snowflake.connector import pandas_tools
    from snowflake.connector.constants import FIELD_TYPES
except ModuleNotFoundError:
    msg = "Snowflake dependencies not found. To install required packages for Snowflake integration, run: pip install 'tecton[snowflake]'"
    raise ModuleNotFoundError(msg)

from tecton_core import conf
from tecton_core.errors import TectonInternalError
from tecton_core.errors import TectonValidationError
from tecton_core.query.dialect import Dialect
from tecton_core.query.errors import SQLCompilationError
from tecton_core.query.errors import UserDefinedTransformationError
from tecton_core.query.node_interface import NodeRef
from tecton_core.query.node_utils import get_batch_data_sources
from tecton_core.query.query_tree_compute import ComputeMonitor
from tecton_core.query.query_tree_compute import SQLCompute
from tecton_core.schema import Schema
from tecton_core.schema_validation import CastError
from tecton_core.schema_validation import cast
from tecton_core.schema_validation import tecton_schema_to_arrow_schema
from tecton_core.secret_management import SecretResolver
from tecton_core.snowflake_context import SnowflakeContext
from tecton_core.snowflake_context import decrypt_private_key
from tecton_core.specs import SnowflakeSourceSpec
from tecton_core.time_utils import convert_pandas_df_for_snowflake_upload


_SNOWFLAKE_HOST_SUFFIX = ".snowflakecomputing.com"


def _map_snowflake_pa_type(dtype_producer: Callable[[Any], pyarrow.DataType]) -> Callable[[Any], pyarrow.DataType]:
    def wrapper(arg):
        dtype = dtype_producer(arg)
        if isinstance(dtype, pyarrow.TimestampType):
            return pyarrow.timestamp(unit=dtype.unit, tz="UTC")
        return dtype

    return wrapper


_SNOWFLAKE_TYPE_TO_PA_TYPE = [_map_snowflake_pa_type(e.pa_type) for e in FIELD_TYPES]


def _get_single_field(sources: List[SnowflakeSourceSpec], field_name: str) -> str:
    values = set()
    for spec in sources:
        field = getattr(spec, field_name)
        if field is None:
            msg = f"`{field_name}` field must be specified for a Snowflake data source"
            raise TectonValidationError(msg, can_drop_traceback=True)
        values.add(field)
    if len(values) != 1:
        msg = f"Conflicting values for `{field_name}` among Snowflake data sources: {values}"
        raise TectonValidationError(msg, can_drop_traceback=True)
    return values.pop()


@attrs.define
class SnowflakeAuthConfig:
    user: Optional[str] = None
    private_key: Optional[str] = None
    private_key_passphrase: Optional[str] = None
    password: Optional[str] = None

    def __attrs_post_init__(self):
        if not self.user:
            msg = "Snowflake user not configured. Instructions at https://docs.tecton.ai/docs/setting-up-tecton/connecting-data-sources/connect-data-sources-to-spark/connecting-to-snowflake-using-spark"
            raise TectonValidationError(msg, can_drop_traceback=True)

        if self.private_key and self.password:
            msg = (
                "Both private_key and password provided, only one authentication method can be used. "
                + "Private key is recommended as password-based authentication is deprecated."
            )
            raise TectonValidationError(msg)

        if not self.private_key and not self.password:
            msg = (
                "An authentication method must be provided for Snowflake source configuration. "
                + "See https://docs.tecton.ai/docs/setting-up-tecton/connecting-data-sources/connect-data-sources-to-rift/connect-to-snowflake"
            )
            raise TectonValidationError(msg, can_drop_traceback=True)

        if self.password and not self.private_key:
            warnings.warn(
                "Password-based authentication is deprecated. Please migrate to private key authentication. "
                + "https://docs.tecton.ai/docs/setting-up-tecton/connecting-data-sources/connect-data-sources-to-rift/connect-to-snowflake"
            )


def _get_snowflake_auth_config(
    sources: List[SnowflakeSourceSpec], secret_resolver: Optional[SecretResolver]
) -> SnowflakeAuthConfig:
    user = None
    private_key = None
    private_key_passphrase = None
    password = None

    for source in sources:
        if source.user:
            if secret_resolver is None:
                msg = "Missing a secret resolver."
                raise TectonInternalError(msg)
            user = secret_resolver.resolve(source.user)
            if source.private_key:
                private_key = secret_resolver.resolve(source.private_key)
            if source.private_key_passphrase:
                private_key_passphrase = secret_resolver.resolve(source.private_key_passphrase)
            if source.password:
                password = secret_resolver.resolve(source.password)
            break

    if user is None:
        user = conf.get_or_none("SNOWFLAKE_USER")
    # Only try to get auth method from environment if neither was provided in source config
    if private_key is None and password is None:
        private_key = conf.get_or_none("SNOWFLAKE_PRIVATE_KEY")
        if private_key is None:
            password = conf.get_or_none("SNOWFLAKE_PASSWORD")
    if private_key_passphrase is None:
        private_key_passphrase = conf.get_or_none("SNOWFLAKE_PRIVATE_KEY_PASSPHRASE")

    return SnowflakeAuthConfig(
        user=user, password=password, private_key=private_key, private_key_passphrase=private_key_passphrase
    )


def create_snowflake_connection(
    root: NodeRef, secret_resolver: Optional[SecretResolver]
) -> snowflake.connector.SnowflakeConnection:
    snowflake_sources: List[SnowflakeSourceSpec] = get_batch_data_sources(root, SnowflakeSourceSpec)

    # TODO: Only one Snowflake connection is currently supported, but eventually we should support multiple.
    auth_config = _get_snowflake_auth_config(snowflake_sources, secret_resolver)

    if not auth_config.user:
        msg = "Snowflake user not configured. Instructions at https://docs.tecton.ai/docs/setting-up-tecton/connecting-data-sources/connect-data-sources-to-spark/connecting-to-snowflake-using-spark"
        raise TectonValidationError(msg, can_drop_traceback=True)

    url = _get_single_field(snowflake_sources, "url")
    host = urlparse(url).hostname
    if not host.endswith(_SNOWFLAKE_HOST_SUFFIX):
        msg = f"Snowflake URL host must end in {_SNOWFLAKE_HOST_SUFFIX}, but was {url}"
        raise TectonValidationError(msg, can_drop_traceback=True)
    account = host[: -len(_SNOWFLAKE_HOST_SUFFIX)]

    warehouse = _get_single_field(snowflake_sources, "warehouse")

    # The "database" parameter is not needed by the query itself,
    # but it's useful for error retrieval.
    # See `self.session.table_function("information_schema.query_history")` below.
    database = _get_single_field(snowflake_sources, "database")

    # Needed for register temp tables
    schema = _get_single_field(snowflake_sources, "schema")

    # Build connection parameters based on authentication method
    connection_params = {
        "user": auth_config.user,
        "account": account,
        "warehouse": warehouse,
        "schema": schema,
        "database": database,
    }

    if auth_config.private_key:
        decrypted_private_key = decrypt_private_key(auth_config.private_key, auth_config.private_key_passphrase)
        connection_params["private_key"] = decrypted_private_key
    elif auth_config.password:
        connection_params["password"] = auth_config.password

    return snowflake.connector.connect(**connection_params)


@attrs.define
class SnowflakeCompute(SQLCompute):
    connection: snowflake.connector.SnowflakeConnection
    is_debug: bool = attrs.field(init=False)

    def __attrs_post_init__(self):
        self.is_debug = conf.get_bool("DUCKDB_DEBUG")

    @staticmethod
    def is_context_initialized() -> bool:
        return SnowflakeContext.is_initialized()

    @staticmethod
    def from_context() -> "SnowflakeCompute":
        return SnowflakeCompute(connection=SnowflakeContext.get_instance().get_connection())

    @staticmethod
    def for_connection(connection: snowflake.connector.SnowflakeConnection) -> "SnowflakeCompute":
        return SnowflakeCompute(connection=connection)

    @staticmethod
    def for_query_tree(root: NodeRef, secret_resolver: Optional[SecretResolver]) -> "SnowflakeCompute":
        """Initializes a connection based on the warehouse/url specified in the batch sources in the tree, and the
        user/password from tecton.conf.
        """
        return SnowflakeCompute.for_connection(create_snowflake_connection(root, secret_resolver))

    def run_sql(
        self,
        sql_string: str,
        return_dataframe: bool = False,
        expected_output_schema: Optional[Schema] = None,
        monitor: Optional[ComputeMonitor] = None,
        checkpoint_as: Optional[str] = None,
    ) -> Optional[pyarrow.RecordBatchReader]:
        sql_string = sqlparse.format(sql_string, reindent=True)
        if self.is_debug:
            logging.warning(f"SNOWFLAKE QT: run SQL {sql_string}")

        if monitor:
            monitor.set_query(sql_string)

        # ToDo: implement progress logging via ComputeMonitor

        cursor = self.connection.cursor()
        cursor.execute("ALTER SESSION SET TIMEZONE = 'UTC'")
        try:
            cursor.execute(sql_string)
        except snowflake.connector.DatabaseError as exc:
            if "SQL compilation error" in exc.msg:
                raise SQLCompilationError(exc.msg.replace("\n", " "), sql_string) from None

            msg = f"Snowflake query failed with: {exc.msg}"
            raise UserDefinedTransformationError(msg) from None

        if not return_dataframe:
            return

        table_it = cursor.fetch_arrow_batches()

        if expected_output_schema:
            output_schema = tecton_schema_to_arrow_schema(expected_output_schema)
        else:
            fields = [
                pyarrow.field(
                    column_metadata.name, _SNOWFLAKE_TYPE_TO_PA_TYPE[column_metadata.type_code](column_metadata)
                )
                for column_metadata in cursor.describe(sql_string)
            ]
            output_schema = pyarrow.schema(fields)

        def batch_iterator():
            for table in table_it:
                try:
                    table = cast(table, output_schema)
                except CastError as e:
                    raise CastError("Error evaluating Snowflake transformation: " + str(e)) from None
                table = self._post_process(table)
                for batch in table.to_batches(1_000_000):
                    yield batch

        res = pyarrow.RecordBatchReader.from_batches(output_schema, batch_iterator())
        return monitor.monitored_arrow_reader(res) if monitor else res

    @staticmethod
    def _post_process(table: pyarrow.Table) -> pyarrow.Table:
        """Fixes Snowflake output before it can be returned"""

        def unquote(field_name: str) -> str:
            """If a column name was quoted, remove the enclosing quotes. Otherwise, return the original column name.

            The Snowpark schema may contain either quoted or unquoted identifiers. In general, Unified Tecton uses
            quoted identifiers. However, certain queries (e.g. a data source scan) do a SELECT *, which results
            in unquoted identifiers. The Pandas dataframe will not have quoted identifiers, and so sometimes need
            to strip the surrounding double quotes.

            NOTE: that an unquoted column name cannot contain double quotes, so it is safe to return the original
            column name if it is not wrapped in double quotes.
            See https://docs.snowflake.com/en/sql-reference/identifiers-syntax for more details.

            NOTE: The condition (field_name[0] == field_name[-1] == '"') is not actually accurate.
            For example if a user has a column that starts and ends with a double quote, and we do a SELECT *, that column will be returned as an unquoted
            identifier. However, this condition will mistakenly consider it a quoted identifier and strip the
            surrounding double quotes, which is wrong. In order to correctly address this, we would need to
            know whether the identifier was quoted or unquoted. However, this case is sufficiently rare that
            we will ignore it for now.

            """
            return field_name[1:-1] if field_name[0] == field_name[-1] == '"' else field_name

        unquoted_names = [unquote(field.name) for field in table.schema]
        processed = table.rename_columns(unquoted_names)

        return processed

    def get_dialect(self) -> Dialect:
        return Dialect.SNOWFLAKE

    def register_temp_table_from_pandas(self, table_name: str, pandas_df: pandas.DataFrame) -> None:
        # Not quoting identifiers / keeping the upload case-insensitive to be consistent with the query tree sql
        # generation logic, which is also case-insensitive. (i.e. will upper case selected fields).
        df_to_write = pandas_df.copy()
        convert_pandas_df_for_snowflake_upload(df_to_write)
        # Note: setting overwrite=True requires extra permissions to `alter table {} rename to {}`
        # renaming a table requires the CREATE TABLE privilege on the schema for the table.
        # https://docs.snowflake.com/en/sql-reference/sql/alter-table
        # table_name should already be unique within it's session since it's based on the dataframe id
        pandas_tools.write_pandas(
            conn=self.connection,
            df=df_to_write,
            table_name=table_name,
            auto_create_table=True,
            table_type="temporary",
            quote_identifiers=True,  # TODO: Remove as part of Snowflake removal
            overwrite=False,
            use_logical_type=True,
        )

    def register_temp_table(
        self, table_name: str, table_or_reader: Union[pyarrow.Table, pyarrow.RecordBatchReader]
    ) -> None:
        types_mapper = {pyarrow.int64(): pandas.Int64Dtype()}
        if isinstance(table_or_reader, pyarrow.RecordBatchReader):
            to_pandas = table_or_reader.read_pandas
        else:
            to_pandas = table_or_reader.to_pandas
        self.register_temp_table_from_pandas(table_name, to_pandas(types_mapper=types_mapper.get))

    def unregister_temp_table(self, table_name: str) -> None:
        raise NotImplementedError
