"""Kuzu database connection management."""

from __future__ import annotations

import os
import json
import time
from pathlib import Path
from typing import Optional, Generator, Any, TYPE_CHECKING
from contextlib import contextmanager

# Lazy import for kuzu - it's an optional dependency
try:
    import kuzu
    KUZU_AVAILABLE = True
except ImportError:
    kuzu = None  # type: ignore
    KUZU_AVAILABLE = False

from ..core.config import KuzuConfig, get_config
from ..core.exceptions import DatabaseConnectionError
from ..utils.logger import log


# Lock file constants
LOCK_FILE_NAME = "kuzu.lock"
LOCK_STALE_SECONDS = 1800  # 30 minutes for long operations like indexing
LOCK_WRITE_TIMEOUT = 60  # Wait up to 60 seconds to acquire write lock


def _require_kuzu():
    """Check that kuzu is available, raise helpful error if not."""
    if not KUZU_AVAILABLE:
        raise ImportError(
            "Kuzu graph database is not installed. "
            "Install with: pip install 'emdash-ai[graph]'\n"
            "Or: pip install kuzu"
        )


class KuzuQueryResult:
    """Wrapper for Kuzu query results providing Neo4j-compatible API."""

    def __init__(self, result: kuzu.QueryResult):
        self._result = result
        self._columns = result.get_column_names()
        self._rows: list[dict] = []
        self._consumed = False

    def _consume(self):
        """Consume all results into memory."""
        if not self._consumed:
            while self._result.has_next():
                values = self._result.get_next()
                self._rows.append(dict(zip(self._columns, values)))
            self._consumed = True

    def single(self) -> Optional[dict]:
        """Return single result (Neo4j-compatible API)."""
        self._consume()
        return self._rows[0] if self._rows else None

    def __iter__(self):
        """Iterate over results."""
        self._consume()
        return iter(self._rows)

    def __len__(self):
        """Return number of results."""
        self._consume()
        return len(self._rows)


class KuzuSessionWrapper:
    """Wrapper providing Neo4j-compatible session API for Kuzu."""

    def __init__(self, conn: kuzu.Connection):
        self._conn = conn

    def run(self, query: str, **parameters) -> KuzuQueryResult:
        """Execute query with Neo4j-compatible API.

        Args:
            query: Cypher query
            **parameters: Query parameters as keyword arguments

        Returns:
            KuzuQueryResult with Neo4j-compatible methods
        """
        try:
            result = self._conn.execute(query, parameters or {})
            return KuzuQueryResult(result)
        except Exception as e:
            raise DatabaseConnectionError(f"Query execution failed: {e}")


class KuzuConnection:
    """Manages Kuzu embedded database connections."""

    def __init__(self, config: Optional[KuzuConfig] = None):
        """Initialize Kuzu connection.

        Args:
            config: Kuzu configuration. If None, loads from environment.
        """
        if config is None:
            config = get_config().kuzu

        self.config = config
        self._db: Optional[kuzu.Database] = None
        self._conn: Optional[kuzu.Connection] = None

    def connect(self, max_retries: int = 3, retry_delay: float = 0.5):
        """Establish connection to Kuzu database.

        Uses retry logic with exponential backoff to handle transient lock issues.

        Args:
            max_retries: Maximum number of connection attempts
            retry_delay: Initial delay between retries (doubles each attempt)

        Returns:
            Kuzu connection instance

        Raises:
            DatabaseConnectionError: If connection fails after all retries
            ImportError: If kuzu is not installed
        """
        _require_kuzu()

        if self._conn is not None:
            return self._conn

        import time

        last_error = None
        for attempt in range(max_retries):
            try:
                # Ensure database directory exists
                db_path = Path(self.config.database_path)
                db_path.parent.mkdir(parents=True, exist_ok=True)

                if attempt == 0:
                    log.info(f"Connecting to Kuzu database at {self.config.database_path}")
                else:
                    log.info(f"Retrying Kuzu connection (attempt {attempt + 1}/{max_retries})")

                self._db = kuzu.Database(str(db_path), read_only=self.config.read_only)
                self._conn = kuzu.Connection(self._db)

                # Test connection
                result = self._conn.execute("RETURN 1 AS num")
                result.get_next()

                log.info("Successfully connected to Kuzu database")
                return self._conn

            except Exception as e:
                last_error = e
                error_str = str(e).lower()

                # Check if it's a lock error that might be transient
                if "lock" in error_str or "could not set lock" in error_str:
                    if attempt < max_retries - 1:
                        delay = retry_delay * (2 ** attempt)
                        log.warning(f"Database lock conflict, retrying in {delay:.1f}s...")
                        time.sleep(delay)
                        continue

                # Non-retryable error or max retries reached
                break

        raise DatabaseConnectionError(f"Failed to connect to Kuzu: {last_error}")

    def close(self):
        """Close the Kuzu connection."""
        if self._conn is not None:
            log.info("Closing Kuzu connection")
            self._conn = None
        if self._db is not None:
            self._db = None

    def execute(self, query: str, parameters: Optional[dict] = None) -> list[dict]:
        """Execute a read query and return results as list of dicts.

        Args:
            query: Cypher query to execute
            parameters: Query parameters

        Returns:
            List of result dictionaries
        """
        conn = self.connect()
        params = parameters or {}

        # Kuzu requires exact parameter match - filter to only params used in query
        import re
        used_params = set(re.findall(r'\$(\w+)', query))
        filtered_params = {k: v for k, v in params.items() if k in used_params}

        try:
            result = conn.execute(query, filtered_params)
            columns = result.get_column_names()
            rows = []
            while result.has_next():
                values = result.get_next()
                rows.append(dict(zip(columns, values)))
            return rows
        except Exception as e:
            raise DatabaseConnectionError(f"Query execution failed: {e}")

    def execute_write(self, query: str, parameters: Optional[dict] = None) -> None:
        """Execute a write query.

        Args:
            query: Cypher query to execute
            parameters: Query parameters
        """
        conn = self.connect()
        params = parameters or {}

        # Kuzu requires exact parameter match - filter to only params used in query
        # Look for $param_name patterns in the query
        import re
        used_params = set(re.findall(r'\$(\w+)', query))
        filtered_params = {k: v for k, v in params.items() if k in used_params}

        try:
            conn.execute(query, filtered_params)
        except Exception as e:
            # Debug: log detailed info when there's an error
            error_str = str(e)
            if "not found" in error_str.lower():
                log.warning(f"KUZU DEBUG - Error: {e}")
                log.warning(f"KUZU DEBUG - Query: {repr(query)}")
                log.warning(f"KUZU DEBUG - Used params: {used_params}")
                log.warning(f"KUZU DEBUG - Filtered params: {list(filtered_params.keys())}")
            raise DatabaseConnectionError(f"Write query failed: {e}")

    @contextmanager
    def session(self) -> Generator[KuzuSessionWrapper, None, None]:
        """Create a context-managed Kuzu session.

        Note: Kuzu doesn't have separate sessions like Neo4j.
        This returns a wrapper for API compatibility with Neo4j-style code.

        Yields:
            KuzuSessionWrapper with Neo4j-compatible run() method

        Example:
            with connection.session() as session:
                result = session.run("MATCH (n) RETURN count(n)")
                record = result.single()
        """
        conn = self.connect()
        try:
            yield KuzuSessionWrapper(conn)
        finally:
            pass  # Kuzu connection persists

    @contextmanager
    def transaction(self) -> Generator[kuzu.Connection, None, None]:
        """Create a context-managed transaction.

        Note: Kuzu has automatic transaction management.
        This is provided for API compatibility.

        Yields:
            Kuzu connection
        """
        conn = self.connect()
        try:
            yield conn
        except Exception as e:
            raise

    def verify_connection(self) -> bool:
        """Verify that the connection works.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            conn = self.connect()
            result = conn.execute("RETURN 1 AS num")
            result.get_next()
            return True
        except Exception as e:
            log.error(f"Connection verification failed: {e}")
            return False

    def get_database_info(self) -> dict:
        """Get information about the Kuzu database.

        Returns:
            Dictionary with database information including specific node counts
        """
        conn = self.connect()

        # Get total node count
        result = conn.execute("MATCH (n) RETURN count(n) AS node_count")
        node_count = result.get_next()[0] if result.has_next() else 0

        # Get relationship count
        result = conn.execute("MATCH ()-[r]->() RETURN count(r) AS rel_count")
        rel_count = result.get_next()[0] if result.has_next() else 0

        # Get node table names (labels)
        # show_tables() returns: [id, name, type, database_name, comment]
        result = conn.execute("CALL show_tables() RETURN *")
        tables = []
        labels = []
        rel_types = []
        while result.has_next():
            row = result.get_next()
            # row format: [id, name, type, database_name, comment]
            table_name = row[1] if len(row) > 1 else str(row[0])
            table_type = row[2] if len(row) > 2 else "NODE"
            tables.append(table_name)
            if table_type == "NODE":
                labels.append(table_name)
            elif table_type == "REL":
                rel_types.append(table_name)

        # Get specific node counts for index status
        file_count = 0
        function_count = 0
        class_count = 0
        community_count = 0

        try:
            if "File" in labels:
                result = conn.execute("MATCH (n:File) RETURN count(n)")
                file_count = result.get_next()[0] if result.has_next() else 0
        except Exception:
            pass

        try:
            if "Function" in labels:
                result = conn.execute("MATCH (n:Function) RETURN count(n)")
                function_count = result.get_next()[0] if result.has_next() else 0
        except Exception:
            pass

        try:
            if "Class" in labels:
                result = conn.execute("MATCH (n:Class) RETURN count(n)")
                class_count = result.get_next()[0] if result.has_next() else 0
        except Exception:
            pass

        try:
            if "Community" in labels:
                result = conn.execute("MATCH (n:Community) RETURN count(n)")
                community_count = result.get_next()[0] if result.has_next() else 0
        except Exception:
            pass

        return {
            "node_count": node_count,
            "relationship_count": rel_count,
            "labels": labels,
            "relationship_types": rel_types,
            "file_count": file_count,
            "function_count": function_count,
            "class_count": class_count,
            "community_count": community_count,
        }

    def clear_database(self):
        """Clear all nodes and relationships from the database.

        Warning: This will delete all data!
        """
        log.warning("Clearing database - all data will be deleted!")
        conn = self.connect()

        # Get all tables and drop them
        result = conn.execute("CALL show_tables() RETURN *")
        tables = []
        while result.has_next():
            row = result.get_next()
            tables.append((row[0], row[1] if len(row) > 1 else "NODE"))

        # Drop relationship tables first, then node tables
        for table_name, table_type in tables:
            if table_type == "REL":
                try:
                    conn.execute(f"DROP TABLE {table_name}")
                except Exception:
                    pass

        for table_name, table_type in tables:
            if table_type == "NODE":
                try:
                    conn.execute(f"DROP TABLE {table_name}")
                except Exception:
                    pass

        log.info("Database cleared successfully")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global connection instance
_connection: Optional[KuzuConnection] = None
_connection_lock = None  # Will be initialized on first use


def _get_lock():
    """Get or create the connection lock."""
    global _connection_lock
    if _connection_lock is None:
        import threading
        _connection_lock = threading.Lock()
    return _connection_lock


def get_connection() -> KuzuConnection:
    """Get the global Kuzu connection instance.

    Thread-safe singleton pattern ensures only one connection exists per process.
    The connection is lazily initialized on first use.
    """
    global _connection

    # Fast path: connection already exists
    if _connection is not None:
        return _connection

    # Slow path: need to create connection (thread-safe)
    with _get_lock():
        # Double-check after acquiring lock
        if _connection is None:
            _connection = KuzuConnection()
            # Eagerly connect to catch issues early
            try:
                _connection.connect()
            except DatabaseConnectionError as e:
                log.warning(f"Failed to connect on initialization: {e}")
                # Still return the connection - it will retry on next execute()
        return _connection


def set_connection(connection: KuzuConnection):
    """Set the global Kuzu connection instance."""
    global _connection
    with _get_lock():
        if _connection is not None:
            _connection.close()
        _connection = connection


def configure_for_repo(repo_root: Path) -> KuzuConnection:
    """Configure and return a connection for a specific repository.

    Sets the database path to {repo_root}/.emdash/index/kuzu_db.
    This ensures each repository has its own isolated database.

    Args:
        repo_root: Path to the repository root

    Returns:
        KuzuConnection configured for this repo
    """
    global _connection

    repo_root = Path(repo_root).resolve()
    db_path = repo_root / ".emdash" / "kuzu_db"

    with _get_lock():
        # Close existing connection if any
        if _connection is not None:
            _connection.close()

        # Create new connection with repo-specific path
        config = KuzuConfig(database_path=str(db_path))
        _connection = KuzuConnection(config)

        log.info(f"Configured database for repo: {repo_root}")
        log.info(f"Database path: {db_path}")

        return _connection


def close_connection():
    """Close and clear the global connection.

    Call this when shutting down or before running tests that need fresh state.
    """
    global _connection
    with _get_lock():
        if _connection is not None:
            _connection.close()
            _connection = None
            log.debug("Global connection closed")


# Read-only connection for concurrent access
_read_connection: Optional[KuzuConnection] = None
_read_connection_lock = None


def _get_read_lock():
    """Get or create the read connection lock."""
    global _read_connection_lock
    if _read_connection_lock is None:
        import threading
        _read_connection_lock = threading.Lock()
    return _read_connection_lock


def get_read_connection() -> KuzuConnection:
    """Get a read-only connection for queries.

    Read-only connections can coexist with other read-only connections
    and with a single write connection. Use this for all query operations
    to avoid lock conflicts with write operations.

    Returns:
        KuzuConnection configured for read-only access
    """
    global _read_connection

    # Fast path
    if _read_connection is not None:
        return _read_connection

    # Slow path: create read-only connection
    with _get_read_lock():
        if _read_connection is None:
            # Get base config and override to read-only
            base_config = get_config().kuzu
            config = KuzuConfig(
                database_path=base_config.database_path,
                read_only=True
            )
            _read_connection = KuzuConnection(config)
            try:
                _read_connection.connect()
                log.debug("Created read-only connection")
            except DatabaseConnectionError as e:
                log.warning(f"Failed to create read-only connection: {e}")
        return _read_connection


def close_read_connection():
    """Close the global read-only connection."""
    global _read_connection
    with _get_read_lock():
        if _read_connection is not None:
            _read_connection.close()
            _read_connection = None
            log.debug("Read-only connection closed")


def get_write_connection() -> KuzuConnection:
    """Get a write connection with lock acquisition.

    This is an alias for get_connection() but makes the intent clear
    that write access is needed.

    Returns:
        KuzuConnection configured for read-write access
    """
    return get_connection()


# Lock file management for write coordination
def _get_lock_file_path() -> Path:
    """Get the path to the lock file."""
    config = get_config().kuzu
    db_path = Path(config.database_path)
    return db_path.parent / LOCK_FILE_NAME


def _is_process_alive(pid: int) -> bool:
    """Check if a process with the given PID is still running."""
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def _is_lock_stale(lock_info: dict) -> bool:
    """Check if a lock file is stale (old or dead process)."""
    pid = lock_info.get("pid")
    timestamp = lock_info.get("timestamp", 0)

    # Check if process is dead
    if pid and not _is_process_alive(pid):
        log.debug(f"Lock held by dead process {pid}")
        return True

    # Check if lock is too old
    age = time.time() - timestamp
    if age > LOCK_STALE_SECONDS:
        log.debug(f"Lock is stale ({age:.0f}s old)")
        return True

    return False


def acquire_write_lock(operation: str = "write") -> bool:
    """Attempt to acquire the write lock.

    Args:
        operation: Name of the operation (for logging)

    Returns:
        True if lock was acquired, False otherwise
    """
    lock_path = _get_lock_file_path()
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    # Check for existing lock
    if lock_path.exists():
        try:
            lock_info = json.loads(lock_path.read_text())
            if not _is_lock_stale(lock_info):
                holder_op = lock_info.get("operation", "unknown")
                holder_pid = lock_info.get("pid", "?")
                log.warning(f"Database locked by {holder_op} (PID {holder_pid})")
                return False
            # Stale lock - remove it
            log.info("Removing stale lock file")
            lock_path.unlink(missing_ok=True)
        except (json.JSONDecodeError, IOError):
            # Corrupted lock file - remove it
            lock_path.unlink(missing_ok=True)

    # Create lock file
    lock_info = {
        "pid": os.getpid(),
        "timestamp": time.time(),
        "operation": operation,
    }
    lock_path.write_text(json.dumps(lock_info))
    log.debug(f"Acquired write lock for {operation}")
    return True


def release_write_lock():
    """Release the write lock if held by this process."""
    lock_path = _get_lock_file_path()
    if lock_path.exists():
        try:
            lock_info = json.loads(lock_path.read_text())
            if lock_info.get("pid") == os.getpid():
                lock_path.unlink(missing_ok=True)
                log.debug("Released write lock")
        except (json.JSONDecodeError, IOError):
            pass


def wait_for_write_lock(operation: str = "write", timeout: float = LOCK_WRITE_TIMEOUT) -> bool:
    """Wait to acquire the write lock with timeout.

    Args:
        operation: Name of the operation (for logging)
        timeout: Maximum seconds to wait

    Returns:
        True if lock was acquired, False if timeout
    """
    start = time.time()
    attempt = 0

    while time.time() - start < timeout:
        if acquire_write_lock(operation):
            return True

        attempt += 1
        delay = min(1.0 * (1.5 ** attempt), 5.0)  # Exponential backoff, max 5s
        remaining = timeout - (time.time() - start)

        if remaining > delay:
            log.info(f"Waiting for database lock ({remaining:.0f}s remaining)...")
            time.sleep(delay)
        else:
            break

    return False


@contextmanager
def write_lock_context(operation: str = "write", timeout: float = LOCK_WRITE_TIMEOUT):
    """Context manager for write operations with lock management.

    Usage:
        with write_lock_context("indexing"):
            # perform write operations

    Raises:
        DatabaseConnectionError if lock cannot be acquired
    """
    if not wait_for_write_lock(operation, timeout):
        raise DatabaseConnectionError(
            f"Could not acquire database lock for {operation}. "
            "Another process may be writing to the database."
        )
    try:
        yield
    finally:
        release_write_lock()
