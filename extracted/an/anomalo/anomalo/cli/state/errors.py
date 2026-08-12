from __future__ import annotations

import sys
from collections.abc import Sequence
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


class ConflictingTableFilters(StateMachineError):
    def __init__(self, flags: Sequence[str]):
        self.flags = flags

    def __str__(self) -> str:
        verb = "applies" if len(self.flags) == 1 else "apply"
        return f"{', '.join(self.flags)} only {verb} when no table references are given"


class UnknownTableLabels(StateMachineError):
    def __init__(self, labels: Sequence[str]):
        self.labels = labels

    def __str__(self) -> str:
        noun = "label" if len(self.labels) == 1 else "labels"
        names = ", ".join(f'"{label}"' for label in self.labels)
        return f"No such table {noun}: {names}"


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
