from typing import Optional


class DatabaseError(Exception):
    """
    Generic exception class. Do not use it for raising any error, but use specific derived class.
    """


class NonExistingTableError(DatabaseError):
    def __init__(self, schema: str, table_name: str) -> None:
        super().__init__(f"table `{table_name}` does not exist in schema `{schema}`")


class TableAlreadyExistsError(DatabaseError):
    def __init__(self, table_name: str, schema: Optional[str]) -> None:
        super().__init__(f"table `{table_name}` already exists in schema `{schema}`")


class DatabaseConnectionError(DatabaseError):
    """
    Raised when connection cannot be established with database.
    """


class DatabaseProtocolError(DatabaseError):
    """
    Raised when connection cannot be established with database due to invalid protocol issue.
    """


class SchemaVersionMismatchError(DatabaseError):
    def __init__(self, expected_version: int, actual_version: int) -> None:
        super().__init__(
            f"schema version mismatch; expected: {expected_version}, got: {actual_version}"
        )


class MissingMetaActionInSync(DatabaseError):
    def __init__(self, missing_column_name: str, field_names: tuple) -> None:
        super().__init__(
            f"Missing column: '{missing_column_name}' in downloaded data. Columns: {field_names}"
        )


class NonFiniteNumericValueError(DatabaseError):
    """
    Raised when the source data holds a floating-point value that the target database
    cannot store, i.e. ``inf``, ``-inf`` or ``nan``.

    SQL Server and MySQL reject non-finite values in a floating-point column; the
    driver aborts the whole batch, so the table cannot be loaded while such a value is
    present. PostgreSQL stores them as ``Infinity``/``NaN``.

    Records are dispatched to the database in batches of ``pysqlsync.base.BATCH_SIZE``
    (100,000), so in a table of more than one batch the records preceding the offending
    one have already been written by the time it is read.

    :param retry_needs_empty_table: Whether those already-written records prevent the
        operation from being retried as-is. An insert would collide with them, and
        since the table is never registered as initialized ``dropdb`` refuses it too,
        so they have to be removed by hand; this is pre-existing behaviour for any
        mid-load failure, not specific to this error. An upsert overwrites them
        instead, and can simply be re-run.
    """

    namespace: str
    table_name: str
    column_name: str
    value: float
    dialect: str
    primary_key_name: Optional[str]
    primary_key_value: Optional[object]
    retry_needs_empty_table: bool

    def __init__(
        self,
        namespace: str,
        table_name: str,
        column_name: str,
        value: float,
        dialect: str,
        primary_key_name: Optional[str] = None,
        primary_key_value: Optional[object] = None,
        retry_needs_empty_table: bool = False,
    ) -> None:
        self.namespace = namespace
        self.table_name = table_name
        self.column_name = column_name
        self.value = value
        self.dialect = dialect
        self.primary_key_name = primary_key_name
        self.primary_key_value = primary_key_value
        self.retry_needs_empty_table = retry_needs_empty_table

        if primary_key_name is not None and primary_key_value is not None:
            record_ref = f", record {primary_key_name}={primary_key_value}"
        else:
            record_ref = ""

        if retry_needs_empty_table:
            recovery = (
                " Records read before this one may already have been written to "
                "the table; drop or empty it manually before retrying initdb."
            )
        else:
            recovery = ""

        super().__init__(
            f"The source data holds the value '{value}' in column '{column_name}' of "
            f"table `{namespace}.{table_name}`{record_ref}. "
            f"A {dialect} floating-point column cannot store inf, -inf or NaN, so this "
            f"record cannot be replicated and the operation has been stopped. "
            f"Please contact Instructure support quoting the table, column and record "
            f"above, so that the source data can be corrected.{recovery}"
        )
