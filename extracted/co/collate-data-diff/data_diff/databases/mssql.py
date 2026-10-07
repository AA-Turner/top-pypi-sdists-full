from typing import Any, ClassVar, Dict, Optional, Type

import attrs

from data_diff.databases.base import (
    CHECKSUM_HEXDIGITS,
    CHECKSUM_OFFSET,
    TIMESTAMP_PRECISION_POS,
    QueryError,
    ThreadedDatabase,
    import_helper,
    ConnectError,
    BaseDialect,
)
from data_diff.abcs.database_types import (
    JSON,
    ColType,
    ColType_UUID,
    NumericType,
    StringType,
    Timestamp,
    TimestampTZ,
    DbPath,
    Float,
    Decimal,
    Integer,
    TemporalType,
    Native_UUID,
    Text,
    Boolean,
    Date,
    Time,
)
from data_diff.schema import RawColumnInfo

DEFAULT_ODBC_DRIVER = "ODBC Driver 18 for SQL Server"
# Binary, so it never compares or sorts anything differently; text is only converted with it
UTF8_COLLATION = "Latin1_General_100_BIN2_UTF8"


@import_helper("mssql")
def import_mssql():
    import pyodbc

    return pyodbc


@attrs.define(frozen=False)
class Dialect(BaseDialect):
    name = "MsSQL"
    ROUNDS_ON_PREC_LOSS = True
    # Set on connecting: the UTF-8 collation to hash text in, or "" where the server has none (before 2019)
    utf8_collation: Optional[str] = None
    SUPPORTS_PRIMARY_KEY: ClassVar[bool] = True
    SUPPORTS_INDEXES = True
    TYPE_CLASSES = {
        # Timestamps
        "datetimeoffset": TimestampTZ,
        "datetime": Timestamp,
        "datetime2": Timestamp,
        "smalldatetime": Timestamp,
        "date": Date,
        "time": Time,
        # Numbers
        "float": Float,
        "real": Float,
        "decimal": Decimal,
        "numeric": Decimal,
        "money": Decimal,
        "smallmoney": Decimal,
        # int
        "int": Integer,
        "bigint": Integer,
        "tinyint": Integer,
        "smallint": Integer,
        # Text
        "varchar": Text,
        "char": Text,
        "text": Text,
        "ntext": Text,
        "nvarchar": Text,
        "nchar": Text,
        "binary": Text,
        "varbinary": Text,
        "xml": Text,
        # UUID
        "uniqueidentifier": Native_UUID,
        # Bool
        "bit": Boolean,
        # JSON
        "json": JSON,
    }

    def quote(self, s: str) -> str:
        return f"[{s}]"

    def parse_type(self, table_path: DbPath, info: RawColumnInfo) -> ColType:
        coltype = super().parse_type(table_path, info)
        if info.data_type in ("char", "nchar"):
            return attrs.evolve(coltype, padded=True)
        return coltype

    def normalize_value_by_type(self, value: str, coltype: ColType) -> str:
        if isinstance(coltype, StringType) and not isinstance(coltype, ColType_UUID):
            if coltype.padded:
                # Other databases' char types drop the padding (Postgres, MySQL) or have none (Snowflake)
                value = f"RTRIM({value})"
            if self.utf8_collation:
                # Text is hashed as UTF-8 elsewhere. A plain varchar takes the database's code page, which can't
                # hold every nvarchar character ('Łukasz' became 'Lukasz') and hashes non-ASCII differently.
                return f"CONVERT(VARCHAR(MAX), CONVERT(NVARCHAR(MAX), {value}) COLLATE {self.utf8_collation})"
            return self.to_string(value)
        return super().normalize_value_by_type(value, coltype)

    def _convert_db_precision_to_digits(self, p: int) -> int:
        # normalize_number casts a float to decimal from its exact binary value, so like PostgreSQL and DuckDB,
        # compare two fewer digits than the binary precision nominally holds: REAL 100.98 is 100.9800034.
        return max(super()._convert_db_precision_to_digits(p) - 2, 0)

    def set_timezone_to_utc(self) -> str:
        raise NotImplementedError("MsSQL does not support a session timezone setting.")

    def current_timestamp(self) -> str:
        return "GETDATE()"

    def current_database(self) -> str:
        return "DB_NAME()"

    def current_schema(self) -> str:
        return """default_schema_name
        FROM sys.database_principals
        WHERE name = CURRENT_USER"""

    def to_string(self, s: str) -> str:
        # Both convert(varchar(max), …) and convert(text, …) do work.
        return f"CONVERT(VARCHAR(MAX), {s})"

    def type_repr(self, t) -> str:
        try:
            return {bool: "bit", str: "text"}[t]
        except KeyError:
            return super().type_repr(t)

    def random(self) -> str:
        return "rand()"

    def is_distinct_from(self, a: str, b: str) -> str:
        # IS (NOT) DISTINCT FROM is available only since SQLServer 2022.
        # See: https://stackoverflow.com/a/18684859/857383
        return f"(({a}<>{b} OR {a} IS NULL OR {b} IS NULL) AND NOT({a} IS NULL AND {b} IS NULL))"

    def limit_select(
        self,
        select_query: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        has_order_by: Optional[bool] = None,
    ) -> str:
        if offset:
            raise NotImplementedError("No support for OFFSET in query")
        result = ""
        if not has_order_by:
            result += "ORDER BY 1"

        result += f" OFFSET 0 ROWS FETCH NEXT {limit} ROWS ONLY"

        # mssql requires that subquery columns are all aliased, so
        # don't wrap in an outer select
        return f"{select_query} {result}"

    def constant_values(self, rows) -> str:
        values = ", ".join("(%s)" % ", ".join(self._constant_value(v) for v in row) for row in rows)
        return f"VALUES {values}"

    def normalize_timestamp(self, value: str, coltype: TemporalType) -> str:
        if isinstance(coltype, Date):
            return f"CONVERT(VARCHAR(10), {value}, 23)"  # yyyy-mm-dd, as the other dialects render dates

        if isinstance(coltype, Time):
            # hh:mi:ss.ffffff, rounded to the column's precision like the other dialects' times
            return f"CONVERT(VARCHAR(15), CAST(CAST({value} AS TIME({min(coltype.precision, 6)})) AS TIME(6)))"

        if isinstance(coltype, TimestampTZ):
            # There is no session time zone to set to UTC (see set_timezone_to_utc), so convert each value
            value = f"SWITCHOFFSET({value}, '+00:00')"

        # Style 121 is yyyy-mm-dd hh:mi:ss.fffffff. CONVERT rather than FORMAT(), which runs on the CLR and is
        # far slower, and which left the fraction unpadded (".123" where the other dialects give ".123000").
        if coltype.rounds and coltype.precision <= 6:
            # Casting down to the precision rounds; casting back up to 6 digits pads with zeros
            timestamp6 = f"CAST(CAST({value} AS DATETIME2({coltype.precision})) AS DATETIME2(6))"
            return f"CONVERT(VARCHAR(26), {timestamp6}, 121)"

        precision = min(coltype.precision, 6)
        timestamp7 = f"CONVERT(VARCHAR(27), CAST({value} AS DATETIME2(7)), 121)"
        return f"LEFT({timestamp7}, {TIMESTAMP_PRECISION_POS + precision}) + REPLICATE('0', {6 - precision})"

    def normalize_number(self, value: str, coltype: NumericType) -> str:
        # CAST rounds half away from zero, like the other dialects. FORMAT(value, 'N2') added grouping separators
        # in the session's culture ("1,234.50"), and precision 0 went through FLOOR, which truncates.
        return f"CONVERT(VARCHAR(40), CAST({value} AS DECIMAL(38, {coltype.precision})))"

    def md5_as_int(self, s: str) -> str:
        return f"convert(bigint, convert(varbinary, '0x' + RIGHT(CONVERT(NVARCHAR(32), HashBytes('MD5', {s}), 2), {CHECKSUM_HEXDIGITS}), 1)) - {CHECKSUM_OFFSET}"

    def md5_as_hex(self, s: str) -> str:
        return f"HashBytes('MD5', {s})"


@attrs.define(frozen=False, init=False, kw_only=True)
class MsSQL(ThreadedDatabase):
    DIALECT_CLASS: ClassVar[Type[BaseDialect]] = Dialect
    CONNECT_URI_HELP = "mssql://<user>:<password>@<host>/<database>/<schema>"
    CONNECT_URI_PARAMS = ["database", "schema"]

    default_database: str
    _args: Dict[str, Any]
    _mssql: Any

    def __init__(self, host, port, user, password, *, database, thread_count, **kw) -> None:
        super().__init__(thread_count=thread_count)

        # A separate keyword rather than `driver`: in a connection dict that name is
        # already consumed by connect_with_dict as the *scheme*. Reading it off `kw`
        # also covers the URI entry point, whose query params land there too.
        odbc_driver = kw.pop("odbc_driver", None) or DEFAULT_ODBC_DRIVER

        args = dict(server=host, port=port, database=database, user=user, password=password, **kw)
        self._args = {k: v for k, v in args.items() if v is not None}
        # Only FreeTDS splits a `DOMAIN\user` login and negotiates NTLM. msodbcsql
        # offers it as a SQL login name, which SQL Server rejects with 18456 - and a
        # backslash is illegal in a SQL login, so such an account can only ever be a
        # Windows one. Hard-coding the driver made domain accounts undiffable.
        self._args["driver"] = "{%s}" % odbc_driver

        # Kept as a default rather than removed: setups with self-signed certificates
        # already depend on it, and dropping it fails them with
        # "SSL Provider: certificate verify failed". Now overridable by the caller.
        self._args.setdefault("TrustServerCertificate", "yes")

        try:
            self.default_database = self._args["database"]
            self.default_schema = self._args["schema"]
        except KeyError:
            raise ValueError("Specify a default database and schema.")

        self._mssql = None

    def create_connection(self):
        self._mssql = import_mssql()
        try:
            connection = self._mssql.connect(**self._args)
        except self._mssql.Error as error:
            raise ConnectError(*error.args) from error
        if self.dialect.utf8_collation is None:
            self.dialect.utf8_collation = self._find_utf8_collation(connection)
        return connection

    def _find_utf8_collation(self, connection) -> str:
        # UTF-8 collations came with SQL Server 2019 (and Azure SQL); before that, text keeps the code page
        cursor = connection.cursor()
        try:
            cursor.execute(f"SELECT CONVERT(VARCHAR(1), N'x' COLLATE {UTF8_COLLATION})").fetchall()
        except self._mssql.Error:
            return ""
        finally:
            cursor.close()
        return UTF8_COLLATION

    def select_table_schema(self, path: DbPath) -> str:
        """Provide SQL for selecting the table schema as (name, type, date_prec, num_prec)"""
        database, schema, name = self._normalize_table_path(path)
        # Metadata identifiers follow the catalog collation, so use their canonical case for case-sensitive catalogs.
        info_schema_path = ["INFORMATION_SCHEMA", "COLUMNS"]
        if database:
            info_schema_path.insert(0, database)
        quoted_info_schema_path = ".".join(self.dialect.quote(identifier) for identifier in info_schema_path)

        return (
            "SELECT [COLUMN_NAME], [DATA_TYPE], [DATETIME_PRECISION], [NUMERIC_PRECISION], [NUMERIC_SCALE], "
            "[COLLATION_NAME] "
            f"FROM {quoted_info_schema_path} "
            f"WHERE [TABLE_NAME] = '{name}' AND [TABLE_SCHEMA] = '{schema}'"
        )

    def _normalize_table_path(self, path: DbPath) -> DbPath:
        if len(path) == 1:
            return self.default_database, self.default_schema, path[0]
        elif len(path) == 2:
            return self.default_database, path[0], path[1]
        elif len(path) == 3:
            return path

        raise ValueError(
            f"{self.name}: Bad table path for {self}: '{'.'.join(path)}'. Expected format: table, schema.table, or database.schema.table"
        )

    def _query_cursor(self, c, sql_code: str):
        try:
            return super()._query_cursor(c, sql_code)
        except self._mssql.DatabaseError as e:
            raise QueryError(e)
