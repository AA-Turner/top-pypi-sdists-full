import threading
from pathlib import Path
from typing import Any, Optional, Union

import duckdb
from loguru import logger

from gable.cli.helpers.data_asset_s3.logger import log_debug

_thread_local = threading.local()


class ResilientDuckDB:
    """
    A resilient wrapper for DuckDB connections that handles connection failures
    gracefully with automatic reconnection and retry logic.

    Unlike traditional client-server databases, DuckDB runs in-process and doesn't
    provide built-in connection pooling. This wrapper encapsulates connection
    health management and provides a safe, predictable interface.
    """

    def __init__(
        self,
        db_path: Optional[Union[str, Path]] = None,
        max_retries: int = 2,
        retry_delay: float = 0.1,
    ):
        """
        Initialize a resilient DuckDB connection wrapper.

        Args:
            db_path: Path to the DuckDB database file
            max_retries: Maximum number of retry attempts for failed operations
            retry_delay: Delay between retry attempts in seconds
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.db_path = db_path
        self._conn: Optional[duckdb.DuckDBPyConnection] = None
        self._setup_connection()

    def _setup_connection(self) -> None:
        """Initialize a new DuckDB connection with required extensions."""
        try:
            if self.db_path is not None:
                self._conn = duckdb.connect(self.db_path)
            else:
                self._conn = duckdb.connect()
            self._conn.query("INSTALL httpfs; LOAD httpfs;")
            self._conn.query(
                "CREATE OR REPLACE SECRET secret (TYPE s3,PROVIDER credential_chain);"
            )
        except Exception as e:
            logger.error(f"Failed to setup DuckDB connection: {e}")
            raise

    def _reset_connection(self, reason: str = "unknown") -> None:
        """Reset the connection due to an error."""
        log_debug(f"[DuckDB Connection] Resetting connection due to {reason}")
        try:
            if self._conn:
                self._conn.close()
        except Exception as e:
            logger.debug(f"Error closing connection: {e}")

        self._conn = None
        self._setup_connection()

    def _execute_with_retry(self, operation_name: str, *args, **kwargs) -> Any:
        """
        Execute an operation with automatic retry on connection failures.

        Args:
            operation_name: The name of the operation to execute ('query', 'execute', 'register')
            *args: Arguments to pass to the operation
            **kwargs: Keyword arguments to pass to the operation

        Returns:
            The result of the operation

        Raises:
            Exception: If the operation fails after all retry attempts
        """
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if self._conn is None:
                    self._setup_connection()

                # Get the operation from the current connection
                if operation_name == "query":
                    op = self._conn.query  # type: ignore
                elif operation_name == "execute":
                    op = self._conn.execute  # type: ignore
                elif operation_name == "register":
                    op = self._conn.register  # type: ignore
                else:
                    raise ValueError(f"Unknown operation: {operation_name}")

                return op(*args, **kwargs)

            except (duckdb.Error, Exception) as e:
                last_exception = e
                self._reset_connection(f"operation failure: {e}")

                if attempt < self.max_retries:
                    logger.debug(
                        f"DuckDB operation failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}"
                    )

                    # Add a small delay before retrying to avoid overwhelming the system
                    import time

                    time.sleep(self.retry_delay)
                else:
                    logger.error(
                        f"DuckDB operation failed after {self.max_retries + 1} attempts: {e}"
                    )
                    raise last_exception

    def query(self, query: str, *args, **kwargs):
        """Execute a query with automatic retry on failures."""
        return self._execute_with_retry("query", query, *args, **kwargs)

    def execute(self, query: str, *args, **kwargs):
        """Execute a statement with automatic retry on failures."""
        return self._execute_with_retry("execute", query, *args, **kwargs)

    def register(self, name: str, obj, *args, **kwargs):
        """Register an object with automatic retry on failures."""
        return self._execute_with_retry("register", name, obj, *args, **kwargs)

    def close(self) -> None:
        """Close the connection."""
        try:
            if self._conn:
                self._conn.close()
        except Exception as e:
            logger.debug(f"Error closing connection: {e}")
        finally:
            self._conn = None

    @property
    def connection(self) -> duckdb.DuckDBPyConnection:
        """Get the underlying DuckDB connection."""
        if self._conn is None:
            self._setup_connection()
        return self._conn  # type: ignore


def get_resilient_duckdb(
    is_shared_thread: bool = True, db_path: Optional[Union[str, Path]] = None
) -> ResilientDuckDB:
    """
    Get a thread-local resilient DuckDB wrapper.

    Returns:
        ResilientDuckDB instance for the current thread
    """
    if is_shared_thread:
        if not hasattr(_thread_local, "resilient_duckdb"):
            _thread_local.resilient_duckdb = ResilientDuckDB(db_path=db_path)

        return _thread_local.resilient_duckdb
    else:
        return ResilientDuckDB(db_path=db_path)
