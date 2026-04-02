import sys
from functools import wraps
from typing import Any


class StateMachineError(Exception):
    def __str__(self) -> str:
        return "Internal error"


def handle_state_errors(f):
    @wraps(f)
    def _wrapper(*args: Any, **kwargs: Any):
        try:
            return f(*args, **kwargs)
        except StateMachineError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    return _wrapper


class InvalidFile(StateMachineError):
    def __init__(self, filename: str, details: str):
        self.filename = filename
        self.details = details

    def __str__(self) -> str:
        return f"{self.filename}: {self.details}"


class TableRefError(StateMachineError):
    def __init__(self, table_ref: str):
        self.table_ref = table_ref


class InvalidTableRef(TableRefError):
    def __str__(self) -> str:
        return f'"{self.table_ref}" is not a valid fully-qualified table reference'


class TableNotFound(TableRefError):
    def __str__(self) -> str:
        return f'Table "{self.table_ref}" not found'


class CheckNotFound(TableRefError):
    def __init__(self, table_ref: str, check_ref: str):
        super().__init__(table_ref)
        self.check_ref = check_ref

    def __str__(self) -> str:
        return f'Check "{self.check_ref}" not found on table "{self.table_ref}"'
