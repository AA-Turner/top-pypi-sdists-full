# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

# a error logger for UDF jobs
import abc
from typing import TYPE_CHECKING

import attrs

from geneva.debug.error_store import ErrorStore
from geneva.table import TableReference

if TYPE_CHECKING:
    from geneva.debug.error_store import ErrorRecord


class ErrorLogger(abc.ABC):
    """Abstract interface for logging UDF execution errors"""

    @abc.abstractmethod
    def log_error(self, error: "ErrorRecord") -> None:
        """Log an error record

        Parameters
        ----------
        error : ErrorRecord
            The error record to log
        """
        ...

    @abc.abstractmethod
    def log_errors(self, errors: list["ErrorRecord"]) -> None:
        """Log multiple error records in bulk

        Parameters
        ----------
        errors : list[ErrorRecord]
            The error records to log
        """
        ...


class NoOpErrorLogger(ErrorLogger):
    """No-op error logger that discards all errors"""

    def log_error(self, error: "ErrorRecord") -> None:
        pass

    def log_errors(self, errors: list["ErrorRecord"]) -> None:
        pass


@attrs.define
class TableErrorLogger(ErrorLogger):
    """Error logger using ErrorStore (Lance table-based storage)"""

    from geneva.debug.error_store import ErrorStore

    table_ref: TableReference = attrs.field()

    _error_store: ErrorStore | None = attrs.field(default=None)  # type: ignore[name-defined]

    @property
    def _store(self) -> ErrorStore:
        if not self._error_store:
            db = self.table_ref.open_db()
            self._error_store = ErrorStore(db)
        return self._error_store

    def log_error(self, error: "ErrorRecord") -> None:
        """Log error record to error store table"""
        self._store.log_error(error)

    def log_errors(self, errors: list["ErrorRecord"]) -> None:
        """Log multiple error records in bulk"""
        self._store.log_errors(errors)
