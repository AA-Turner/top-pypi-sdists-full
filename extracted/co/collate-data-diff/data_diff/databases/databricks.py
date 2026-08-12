import math
from typing import Any, ClassVar, Dict, Sequence, Type
import logging

import attrs

from data_diff.abcs.database_types import (
    Date,
    Integer,
    Float,
    Decimal,
    Timestamp,
    Text,
    TemporalType,
    NumericType,
    DbPath,
    ColType,
    UnknownColType,
    Boolean,
)
from data_diff.databases.base import (
    MD5_HEXDIGITS,
    CHECKSUM_HEXDIGITS,
    CHECKSUM_OFFSET,
    BaseDialect,
    ThreadedDatabase,
    import_helper,
    parse_table_name,
)
from data_diff.schema import RawColumnInfo


@import_helper(text="You can install it using 'pip install databricks-sql-connector'")
def import_databricks():
    import databricks.sql

    return databricks


@import_helper(text="You can install it using 'pip install databricks-sdk'")
def import_databricks_sdk():
    from databricks.sdk.core import Config, oauth_service_principal

    return Config, oauth_service_principal


AUTH_PAT = "pat"
AUTH_OAUTH_M2M = "oauth-m2m"
AUTH_AZURE_SP_M2M = "azure-sp-m2m"


@attrs.define(frozen=False)
class Dialect(BaseDialect):
    name = "Databricks"
    ROUNDS_ON_PREC_LOSS = True
    TYPE_CLASSES = {
        # Numbers
        "INT": Integer,
        "SMALLINT": Integer,
        "TINYINT": Integer,
        "BIGINT": Integer,
        "FLOAT": Float,
        "DOUBLE": Float,
        "DECIMAL": Decimal,
        # Timestamps
        "TIMESTAMP": Timestamp,
        "TIMESTAMP_NTZ": Timestamp,
        "DATE": Date,
        # Text
        "STRING": Text,
        "VARCHAR": Text,
        # Boolean
        "BOOLEAN": Boolean,
    }

    def type_repr(self, t) -> str:
        try:
            return {str: "STRING"}[t]
        except KeyError:
            return super().type_repr(t)

    def quote(self, s: str) -> str:
        return f"`{s}`"

    def to_string(self, s: str) -> str:
        return f"cast({s} as string)"

    def _convert_db_precision_to_digits(self, p: int) -> int:
        # Subtracting 2 due to wierd precision issues
        return max(super()._convert_db_precision_to_digits(p) - 2, 0)

    def set_timezone_to_utc(self) -> str:
        return "SET TIME ZONE 'UTC'"

    def parse_table_name(self, name: str) -> DbPath:
        path = parse_table_name(name)
        return tuple(i for i in path if i is not None)

    def md5_as_int(self, s: str) -> str:
        return f"cast(conv(substr(md5({s}), {1 + MD5_HEXDIGITS - CHECKSUM_HEXDIGITS}), 16, 10) as decimal(38, 0)) - {CHECKSUM_OFFSET}"

    def md5_as_hex(self, s: str) -> str:
        return f"md5({s})"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        """Databricks timestamp contains no more than 6 digits in precision"""
        try:
            is_date = coltype.is_date
        except:
            is_date = False
        if isinstance(coltype, Date) or is_date:
            return f"date_format({value}, 'yyyy-MM-dd')"
        if coltype.rounds:
            # cast to timestamp due to unix_micros() requiring timestamp
            timestamp = f"cast(round(unix_micros(cast({value} as timestamp)) / 1000000, {coltype.precision}) * 1000000 as bigint)"
            return f"date_format(timestamp_micros({timestamp}), 'yyyy-MM-dd HH:mm:ss.SSSSSS')"

        precision_format = "S" * coltype.precision + "0" * (6 - coltype.precision)
        return f"date_format({value}, 'yyyy-MM-dd HH:mm:ss.{precision_format}')"

    def normalize_number(self, value: str, coltype: NumericType) -> str:
        value = f"cast({value} as decimal(38, {coltype.precision}))"
        if coltype.precision > 0:
            value = f"format_number({value}, {coltype.precision})"
        return f"replace({self.to_string(value)}, ',', '')"

    def normalize_boolean(self, value: str, _coltype: Boolean) -> str:
        return self.to_string(f"cast ({value} as int)")


@attrs.define(frozen=False, init=False, kw_only=True)
class Databricks(ThreadedDatabase):
    DIALECT_CLASS: ClassVar[Type[BaseDialect]] = Dialect
    CONNECT_URI_HELP = "databricks://:<access_token>@<server_hostname>/<http_path>"
    CONNECT_URI_PARAMS = ["catalog", "schema"]

    catalog: str
    _args: Dict[str, Any]

    def __init__(self, *, thread_count, **kw) -> None:
        super().__init__(thread_count=thread_count)
        logging.getLogger("databricks.sql").setLevel(logging.WARNING)

        self._args = kw
        self.default_schema = kw.get("schema", "default")
        self.catalog = kw.get("catalog", "hive_metastore")

    def _require(self, key: str) -> str:
        value = self._args.get(key)
        if not value:
            auth_method = self._args.get("auth_method", AUTH_PAT)
            raise ValueError(f"{self.name}: '{key}' is required for auth_method '{auth_method}'")
        return value

    def _pat_kwargs(self) -> Dict[str, Any]:
        return {"access_token": self._require("access_token")}

    def _oauth_m2m_kwargs(self) -> Dict[str, Any]:
        Config, oauth_service_principal = import_databricks_sdk()
        hostname = self._args["server_hostname"]
        client_id = self._require("databricks_client_id")
        client_secret = self._require("databricks_client_secret")

        def credentials_provider():
            provider = oauth_service_principal(
                Config(host=f"https://{hostname}", client_id=client_id, client_secret=client_secret)
            )
            if provider is None:
                raise ConnectionError(f"{self.name}: OAuth is not available on {hostname}")
            return provider

        return {"credentials_provider": credentials_provider}

    def _azure_sp_m2m_kwargs(self) -> Dict[str, Any]:
        return {
            "auth_type": AUTH_AZURE_SP_M2M,
            "azure_client_id": self._require("azure_client_id"),
            "azure_client_secret": self._require("azure_client_secret"),
            "azure_tenant_id": self._require("azure_tenant_id"),
        }

    def _auth_kwargs(self) -> Dict[str, Any]:
        """Credential kwargs for ``databricks.sql.connect``.

        Raises:
            ValueError: on an unknown ``auth_method`` or a missing credential.
        """
        # Callables cannot travel in the connection config: `Connect` caches on
        # json.dumps of it. Providers are built here, from plain strings.
        auth_method = self._args.get("auth_method", AUTH_PAT)
        builder = {
            AUTH_PAT: self._pat_kwargs,
            AUTH_OAUTH_M2M: self._oauth_m2m_kwargs,
            AUTH_AZURE_SP_M2M: self._azure_sp_m2m_kwargs,
        }.get(auth_method)
        if builder is None:
            raise ValueError(
                f"{self.name}: unknown auth_method '{auth_method}'. "
                f"Expected one of {AUTH_PAT}, {AUTH_OAUTH_M2M}, {AUTH_AZURE_SP_M2M}"
            )
        return builder()

    def create_connection(self):
        databricks = import_databricks()

        try:
            return databricks.sql.connect(
                server_hostname=self._args["server_hostname"],
                http_path=self._args["http_path"],
                catalog=self.catalog,
                **self._auth_kwargs(),
            )
        except databricks.sql.exc.Error as e:
            raise ConnectionError(*e.args) from e

    def query_table_schema(self, path: DbPath) -> Dict[str, RawColumnInfo]:
        # Databricks has INFORMATION_SCHEMA only for Databricks Runtime, not for Databricks SQL.
        # https://docs.databricks.com/spark/latest/spark-sql/language-manual/information-schema/columns.html
        # So, to obtain information about schema, we should use another approach.

        conn = self.create_connection()

        catalog, schema, table = self._normalize_table_path(path)
        with conn.cursor() as cursor:
            cursor.columns(catalog_name=catalog, schema_name=schema, table_name=table)
            try:
                rows = cursor.fetchall()
            finally:
                conn.close()
            if not rows:
                raise RuntimeError(f"{self.name}: Table '{'.'.join(path)}' does not exist, or has no columns")

            d = {
                r.COLUMN_NAME: RawColumnInfo(
                    column_name=r.COLUMN_NAME, data_type=r.TYPE_NAME, numeric_precision=r.DECIMAL_DIGITS
                )
                for r in rows
            }
            assert len(d) == len(rows)
            return d

    # def select_table_schema(self, path: DbPath) -> str:
    #     """Provide SQL for selecting the table schema as (name, type, date_prec, num_prec)"""
    #     database, schema, name = self._normalize_table_path(path)
    #     info_schema_path = ["information_schema", "columns"]
    #     if database:
    #         info_schema_path.insert(0, database)

    #     return (
    #         "SELECT column_name, data_type, datetime_precision, numeric_precision, numeric_scale "
    #         f"FROM {'.'.join(info_schema_path)} "
    #         f"WHERE table_name = '{name}' AND table_schema = '{schema}'"
    #     )

    def _process_table_schema(
        self, path: DbPath, raw_schema: Dict[str, RawColumnInfo], filter_columns: Sequence[str], where: str = None
    ):
        accept = {i.lower() for i in filter_columns}
        col_infos = [row for name, row in raw_schema.items() if name.lower() in accept]

        resulted_rows = []
        for info in col_infos:
            raw_data_type = info.data_type
            row_type = info.data_type.split("(")[0]
            info = attrs.evolve(info, data_type=row_type)
            type_cls = self.dialect.TYPE_CLASSES.get(row_type, UnknownColType)

            if issubclass(type_cls, Integer):
                info = attrs.evolve(info, numeric_scale=0)

            elif issubclass(type_cls, Float):
                numeric_precision = math.ceil(info.numeric_precision / math.log(2, 10))
                info = attrs.evolve(info, numeric_precision=numeric_precision)

            elif issubclass(type_cls, Decimal):
                items = raw_data_type[8:].rstrip(")").split(",")
                numeric_precision, numeric_scale = int(items[0]), int(items[1])
                info = attrs.evolve(
                    info,
                    numeric_precision=numeric_precision,
                    numeric_scale=numeric_scale,
                )

            elif issubclass(type_cls, Timestamp):
                info = attrs.evolve(
                    info,
                    datetime_precision=info.numeric_precision,
                    numeric_precision=None,
                )

            else:
                info = attrs.evolve(info, numeric_precision=None)

            resulted_rows.append(info)

        col_dict: Dict[str, ColType] = {info.column_name: self.dialect.parse_type(path, info) for info in resulted_rows}

        self._refine_coltypes(path, col_dict, where)
        return col_dict

    @property
    def is_autocommit(self) -> bool:
        return True

    def _normalize_table_path(self, path: DbPath) -> DbPath:
        if len(path) == 1:
            return self.catalog, self.default_schema, path[0]
        elif len(path) == 2:
            return self.catalog, path[0], path[1]
        elif len(path) == 3:
            return path

        raise ValueError(
            f"{self.name}: Bad table path for {self}: '{'.'.join(path)}'. Expected format: table, schema.table, or catalog.schema.table"
        )
