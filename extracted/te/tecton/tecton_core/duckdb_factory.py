import logging
import tempfile
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing import Optional

from tecton_core import _gen_version
from tecton_core import conf


if TYPE_CHECKING:
    from duckdb import DuckDBPyConnection

"""
Factory code for creating DuckDB connections.
"""

logger = logging.getLogger(__name__)


def get_ext_version():
    return "latest" if _gen_version.VERSION == "99.99.99" else _gen_version.VERSION


_home_dir_override: Optional[str] = None


def set_home_dir_override(value: Optional[str]) -> None:
    global _home_dir_override
    _home_dir_override = value


@dataclass
# Example: DuckDBConfig(memory_limit='1GB', num_threads=4)
class DuckDBConfig:
    memory_limit_in_bytes: Optional[int] = None  # Memory limit for DuckDB
    num_threads: Optional[int] = None  # Number of threads for DuckDB
    use_unique_extension_path: bool = False  # Use unique extension path for each connection, this is needed when we can multiple Ray tasks on the same machine and want to separate them.


def run_duckdb_sql_with_retry(connection, sql_str, max_retries=3, wait_seconds=2):
    try:
        import duckdb
    except ImportError:
        msg = (
            "Couldn't initialize DuckDB connection. "
            "Please install DuckDB dependencies by executing `pip install tecton[rift]`."
        )
        raise RuntimeError(msg)

    retries = 0
    while retries < max_retries:
        try:
            connection.sql(sql_str)
            return
        except duckdb.IOException as e:
            retries += 1
            if retries < max_retries:
                time.sleep(wait_seconds)
            else:
                logger.fatal(f"Duckdb Sql {sql_str} Failed after {max_retries} retries.")
                raise


def create_connection(duckdb_config: Optional[DuckDBConfig] = None) -> "DuckDBPyConnection":
    """
    Create a new instance of DuckDBPyConnection.
    """
    try:
        import duckdb
    except ImportError:
        msg = (
            "Couldn't initialize DuckDB connection. "
            "Please install DuckDB dependencies by executing `pip install tecton[rift]`."
        )
        raise RuntimeError(msg)

    conn_config = {}
    if conf.get_or_none("DUCKDB_EXTENSION_REPO"):
        conn_config["allow_unsigned_extensions"] = "true"

    if conf.get_bool("DUCKDB_PERSIST_DB"):
        connection = duckdb.connect("duckdb.db", config=conn_config)
    else:
        connection = duckdb.connect(config=conn_config)

    # Initialize the DuckDB connection
    if _home_dir_override:
        connection.sql(f"SET home_directory='{_home_dir_override}'")

    # TODO(liangqi): Remove this once we move to packaging extensions into Python package.
    if duckdb_config and duckdb_config.use_unique_extension_path:
        # Use mkdtemp instead of TemporaryDirectory to keep the directory alive after the function. We cannot set
        # `delete=False` for TemporaryDirectory until Python 3.12
        temporary_extension_directory = tempfile.mkdtemp(suffix="duckdb_ext_directory_")
        connection.sql(f"SET extension_directory = '{temporary_extension_directory}'")

    connection.sql("INSTALL httpfs;")
    run_duckdb_sql_with_retry(connection, "LOAD httpfs;")
    connection.sql(f"SET http_retries='{conf.get_or_raise('DUCKDB_HTTP_RETRIES')}'")

    if conf.get_bool("DUCKDB_DISK_SPILLING_ENABLED"):
        # The directory will be deleted when the TemporaryDirectory object is destroyed even if we don't call
        # __enter__. This means as long as we store the object somewhere the directory will live as the context and
        # will be cleaned up at interpreter exit.
        temporary_directory = tempfile.TemporaryDirectory(suffix=".tecton_duckdb")
        connection.sql(f"SET temp_directory = '{temporary_directory.name}'")

    duckdb_memory_limit = (
        f"{duckdb_config.memory_limit_in_bytes // 1024 // 1024}MB"
        if duckdb_config and duckdb_config.memory_limit_in_bytes
        else conf.get_or_none("DUCKDB_MEMORY_LIMIT")
    )
    if duckdb_memory_limit:
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"Setting duckdb memory limit to {duckdb_memory_limit}")

        connection.sql(f"SET memory_limit='{duckdb_memory_limit}'")

    num_duckdb_threads = (
        duckdb_config.num_threads
        if duckdb_config and duckdb_config.num_threads
        else conf.get_or_none("DUCKDB_NTHREADS")
    )
    if num_duckdb_threads:
        connection.sql(f"SET threads TO {num_duckdb_threads};")
        if conf.get_bool("DUCKDB_DEBUG"):
            print(f"Setting duckdb threads to {num_duckdb_threads}")

    # Workaround for pypika not supporting the // operator
    connection.sql("CREATE OR REPLACE MACRO _tecton_int_div(a, b) AS a // b")
    extension_repo = conf.get_or_none("DUCKDB_EXTENSION_REPO")
    if extension_repo:
        versioned_extension_repo = extension_repo.format(version=get_ext_version())
        connection.sql(f"SET custom_extension_repository='{versioned_extension_repo}'")
        if conf.get_bool("DUCKDB_ALLOW_CACHE_EXTENSION"):
            # Allow using local cached version of extension
            connection.sql("INSTALL tecton")
        else:
            # Always download the latest version of the duckdb extension
            connection.sql("FORCE INSTALL tecton")
        run_duckdb_sql_with_retry(connection, "LOAD tecton")

    connection.sql("SET TimeZone='UTC'")

    return connection
