"""
Data loading functionality for storage inventory files.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

import pyarrow as pa

from .cache_manager import InventoryCacheManager
from .constants import StorageInventoryConstants
from .duckdb_connection import get_resilient_duckdb


class InventoryDataLoader:
    """Handles loading data from storage inventory files"""

    def __init__(self, logger, inventory_dir=None):
        """
        Initialize the data loader.

        Args:
            logger: Logger instance
            inventory_dir: Directory where inventory reports are stored.
                           If None, uses the default location.
        """
        self.logger = logger
        self.inventory_dir = inventory_dir or self._get_default_inventory_dir()
        self.cache_manager = InventoryCacheManager()

    def _get_default_inventory_dir(self) -> str:
        """
        Determine the default inventory directory based on environment variables or Linux standards.

        Following Linux FHS (Filesystem Hierarchy Standard) conventions:
        - /var/lib/{app_name} for system-wide data
        - ~/.local/share/{app_name} for user data
        - Current working directory for backward compatibility with original implementation

        Returns:
            str: Path to the default inventory directory
        """
        # First check if an environment variable is set
        if "INVENTORY_REPORTS_DIR" in os.environ:
            return os.environ["INVENTORY_REPORTS_DIR"]

        # For system-wide installation
        system_dir = Path("/var/lib/inventory-reports")
        if system_dir.exists() and system_dir.is_dir():
            return str(system_dir)

        # For user installation
        user_dir = Path.home() / ".local" / "share" / "inventory-reports"
        if user_dir.exists() and user_dir.is_dir():
            return str(user_dir)

        # For backward compatibility with original implementation,
        # return the current working directory where the script is run
        cwd = os.getcwd()
        self.logger.info(f"Using current working directory for inventory files: {cwd}")
        return cwd

    def _get_csv_column_prefix(self, inventory_files: Dict[str, List[str]]) -> str:
        """Get the column prefix for csv inventory files.
        This is used to avoid the issue where the column name is 'column00' instead of 'column0'
        """
        resilient_duckdb = get_resilient_duckdb(
            db_path=":memory:", is_shared_thread=False
        )
        column_prefix = "column"
        try:
            if (
                "csv_gz_files" in inventory_files
                and len(inventory_files["csv_gz_files"]) > 0
            ):
                sniff_result = resilient_duckdb.execute(
                    f"""SELECT Columns FROM sniff_csv('{inventory_files["csv_gz_files"][0]}', sample_size = 1)"""
                ).fetchone()
                sniffed_column_name = sniff_result[0][0].get("name")
                if sniffed_column_name == "column00":
                    column_prefix = "column0"
        except Exception as e:
            self.logger.error(f"Error sniffing CSV file: {str(e)}")
        finally:
            resilient_duckdb.close()
        return column_prefix

    def find_inventory_files(self) -> Dict[str, List[str]]:
        """Find all inventory CSV.GZ or .PARQUET files in the inventory directory"""
        # Check cache first
        cached_files = self.cache_manager.get_inventory_files(self.inventory_dir)
        if cached_files is not None:
            self.logger.info(
                "Using %d cached .csv.gz inventory files", len(cached_files)
            )
            return cached_files  # type: ignore

        # If not in cache, find files and cache them
        inventory_path = Path(self.inventory_dir)
        csv_gz_files = [str(f) for f in inventory_path.glob("**/*.csv.gz")]
        parquet_files = [str(f) for f in inventory_path.glob("**/*.parquet")]

        files = {
            "csv_gz_files": csv_gz_files,
            "parquet_files": parquet_files,
        }

        if not files:
            self.logger.error("No inventory files found in %s", self.inventory_dir)
        else:
            self.logger.info(
                "Discovered %d .csv.gz and %d .parquet files for metadata summary.",
                len(csv_gz_files),
                len(parquet_files),
            )

        # Cache the results
        self.cache_manager.cache_inventory_files(self.inventory_dir, files)  # type: ignore

        return files

    def build_duckdb_query(
        self,
        inventory_files: Dict[str, List[str]],
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> str:
        """Build a DuckDB query to extract data from inventory files"""

        exclude_clause = " AND ".join(
            [
                f"NOT Key LIKE '%{x}%'"
                for x in StorageInventoryConstants.EXCLUDE_KEYS
                + (exclude_prefixes or [])
            ]
        )

        if include_prefixes is None or len(include_prefixes) == 0:
            prefix_clause = ""
        elif len(include_prefixes) == 1:
            prefix = include_prefixes[0]
            prefix_clause = f"Key LIKE '{prefix}/%' AND "
        else:
            pattern = "^(" + "|".join(re.escape(p) for p in include_prefixes) + ")/"
            prefix_clause = f"REGEXP_MATCHES(Key, '{pattern}') AND "

        if (
            "parquet_files" in inventory_files
            and len(inventory_files["parquet_files"]) > 0
        ):
            query = f"""
                SELECT Key FROM read_parquet({inventory_files["parquet_files"]})
                WHERE {prefix_clause}{exclude_clause} AND CAST(Size AS BIGINT) > 0
            """
        elif (
            "csv_gz_files" in inventory_files
            and len(inventory_files["csv_gz_files"]) > 0
        ):
            column_prefix = self._get_csv_column_prefix(inventory_files)
            self.logger.debug(f"Using column prefix: {column_prefix}")
            query = f"""
                SELECT {column_prefix}1 as Key FROM read_csv_auto({inventory_files["csv_gz_files"]})
                WHERE {prefix_clause}{exclude_clause} AND CAST({column_prefix}2 AS BIGINT) > 0
            """
        else:
            raise ValueError("No inventory files found")

        return query

    def load_keys(
        self,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> List[str]:
        """Load keys from inventory files with optional prefix filtering"""
        inventory_files = self.find_inventory_files()
        if not inventory_files or all(
            len(files) == 0 for files in inventory_files.values()
        ):
            return []

        query = self.build_duckdb_query(
            inventory_files, include_prefixes, exclude_prefixes
        )

        try:
            # Use resilient connection wrapper
            resilient_duckdb = get_resilient_duckdb(
                db_path=":memory:", is_shared_thread=False
            )
            keys = resilient_duckdb.execute(query).fetchall()
            keys = [k[0] for k in keys]
        except Exception as e:
            self.logger.error(f"Error loading keys: {str(e)}")
            return []
        finally:
            resilient_duckdb.close()  # type: ignore

        self.logger.info("Loaded %d keys for processing", len(keys))
        return keys

    def load_file_metadata(
        self,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> pa.Table:
        """Load file metadata from inventory files as an Arrow table"""
        cache_key = self.inventory_dir
        if include_prefixes is not None:
            cache_key += f"_prefixes_{'_'.join(include_prefixes)}"
        if exclude_prefixes is not None:
            cache_key += f"_exclude_prefixes_{'_'.join(exclude_prefixes)}"

        # Check cache first
        cached_records = self.cache_manager.get_file_records(cache_key)
        if cached_records is not None:
            self.logger.info(
                "Using cached file records with %d rows", cached_records.num_rows
            )
            return cached_records

        # If not in cache, load data and cache it
        inventory_files = self.find_inventory_files()
        if not inventory_files or all(
            len(files) == 0 for files in inventory_files.values()
        ):
            return pa.table([])

        exclude_clause = " AND ".join(
            [
                f"NOT Key LIKE '%{x}%'"
                for x in StorageInventoryConstants.EXCLUDE_KEYS
                + (exclude_prefixes or [])
            ]
        )

        if include_prefixes and len(include_prefixes) > 0:
            prefix_patterns = [f"Key LIKE '{p}/%'" for p in include_prefixes]
            prefix_clause = f" AND ({' OR '.join(prefix_patterns)})"
        else:
            prefix_clause = ""

        # Build query based on available file types
        if (
            "parquet_files" in inventory_files
            and len(inventory_files["parquet_files"]) > 0
        ):
            query = f"""
                SELECT key as Key,
                       CAST(size AS BIGINT) AS Size,
                       last_modified_date as LastModifiedDate
                FROM read_parquet({inventory_files["parquet_files"]})
                WHERE {exclude_clause}{prefix_clause} AND CAST(size AS BIGINT) > 0
            """
        elif (
            "csv_gz_files" in inventory_files
            and len(inventory_files["csv_gz_files"]) > 0
        ):
            column_prefix = self._get_csv_column_prefix(inventory_files)
            self.logger.debug(f"Using column prefix: {column_prefix}")
            query = f"""
                SELECT 
                    {column_prefix}1 as Key,
                    CAST({column_prefix}2 AS BIGINT) AS Size,
                    {column_prefix}3 as LastModifiedDate
                FROM read_csv_auto({inventory_files["csv_gz_files"]})
                WHERE {exclude_clause}{prefix_clause} 
                AND CAST({column_prefix}2 AS BIGINT) > 0
            """
        else:
            return pa.table([])

        try:
            # Use resilient connection wrapper
            resilient_duckdb = get_resilient_duckdb(
                db_path=":memory:", is_shared_thread=False
            )
            arrow_table = resilient_duckdb.execute(query).arrow()
            self.logger.info("Loaded %d file records.", arrow_table.num_rows)

            # Cache the results
            self.cache_manager.cache_file_records(cache_key, arrow_table)

            return arrow_table
        except Exception as e:
            self.logger.error(f"Error loading file metadata: {str(e)}")
            return pa.table([])
        finally:
            resilient_duckdb.close()  # type: ignore

    def get_latest_objects(
        self,
        prefix: str,
        exclude_prefixes: Optional[List[str]] = None,
        limit: int = 5,
    ) -> pa.Table:
        """
        Retrieve the latest N objects for a specific prefix based on LastModifiedDate.

        Args:
            prefix: The prefix to filter objects by
            limit: Maximum number of objects to return (default: 5)

        Returns:
            Arrow table containing the latest objects with their metadata
        """
        # Generate a cache key for this query
        cache_key = f"latest_objects_{self.inventory_dir}_{prefix}_{limit}_{'_'.join(exclude_prefixes or [])}"
        cached_result = self.cache_manager.get_query_result(cache_key)
        if cached_result is not None:
            self.logger.info(f"Using cached latest objects for prefix '{prefix}'")
            return cached_result

        # If not in cache, query the data
        arrow_table = self.load_file_metadata([prefix], exclude_prefixes)
        if arrow_table.num_rows == 0:
            self.logger.warning(f"No objects found for prefix: {prefix}")
            return pa.table([])

        # Use DuckDB to query the Arrow table directly for the latest objects
        query = f"""
            SELECT *
            FROM arrow_table
            WHERE Key LIKE '{prefix}/%'
            ORDER BY LastModifiedDate DESC
            LIMIT {limit}
        """

        try:
            # Use resilient connection wrapper
            resilient_duckdb = get_resilient_duckdb(
                db_path=":memory:", is_shared_thread=False
            )
            resilient_duckdb.register("arrow_table", arrow_table)
            result = resilient_duckdb.execute(query).arrow()

            count = result.num_rows
            self.logger.info(f"Retrieved {count} latest objects for prefix '{prefix}'")

            # Cache the result
            self.cache_manager.cache_query_result(cache_key, result)

            return result
        except Exception as e:
            self.logger.error(
                f"Error retrieving latest objects for prefix '{prefix}': {str(e)}"
            )
            return pa.table([])
        finally:
            resilient_duckdb.close()  # type: ignore
