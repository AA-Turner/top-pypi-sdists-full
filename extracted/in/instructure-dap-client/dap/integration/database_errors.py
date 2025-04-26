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
