"""
Cache manager for inventory report data.
Provides centralized caching of inventory files and data to avoid redundant operations.
"""

from typing import Any, Dict, List, Optional, Set

import pyarrow as pa


class InventoryCacheManager:
    """
    Singleton cache manager for inventory data.

    Maintains caches for:
    - Discovered inventory file paths
    - Loaded file records
    - Query results

    This eliminates redundant file discovery and data loading operations
    across different collectors.
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InventoryCacheManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Initialize the cache manager"""
        # Cache of inventory file paths by directory
        self.inventory_files_cache: Dict[str, List[str]] = {}

        # Cache of loaded file records (Arrow tables) by directory
        self.file_records_cache: Dict[str, pa.Table] = {}

        # Cache for DuckDB query results
        self.query_results_cache: Dict[str, Any] = {}

        # Set of prefixes discovered in the inventory
        self.discovered_prefixes: Set[str] = set()

    def get_inventory_files(self, inventory_dir: str) -> Optional[List[str]]:
        """
        Get cached inventory files for a directory

        Args:
            inventory_dir: Directory path

        Returns:
            List of file paths or None if not cached
        """
        return self.inventory_files_cache.get(inventory_dir)

    def cache_inventory_files(self, inventory_dir: str, file_paths: List[str]) -> None:
        """
        Cache inventory files for a directory

        Args:
            inventory_dir: Directory path
            file_paths: List of file paths to cache
        """
        self.inventory_files_cache[inventory_dir] = file_paths

    def get_file_records(self, inventory_dir: str) -> Optional[pa.Table]:
        """
        Get cached file records for a directory

        Args:
            inventory_dir: Directory path

        Returns:
            Arrow table of file records or None if not cached
        """
        return self.file_records_cache.get(inventory_dir)

    def cache_file_records(self, inventory_dir: str, records: pa.Table) -> None:
        """
        Cache file records for a directory

        Args:
            inventory_dir: Directory path
            records: Arrow table of file records
        """
        self.file_records_cache[inventory_dir] = records

    def get_query_result(self, query_key: str) -> Optional[Any]:
        """
        Get cached query result

        Args:
            query_key: Unique key for the query

        Returns:
            Cached result or None if not cached
        """
        return self.query_results_cache.get(query_key)

    def cache_query_result(self, query_key: str, result: Any) -> None:
        """
        Cache query result

        Args:
            query_key: Unique key for the query
            result: Query result to cache
        """
        self.query_results_cache[query_key] = result

    def add_discovered_prefixes(self, prefixes: Set[str]) -> None:
        """
        Add discovered prefixes to the cache

        Args:
            prefixes: Set of prefixes to add
        """
        self.discovered_prefixes.update(prefixes)

    def get_discovered_prefixes(self) -> Set[str]:
        """
        Get all discovered prefixes

        Returns:
            Set of discovered prefixes
        """
        return self.discovered_prefixes

    def clear(self) -> None:
        """Clear all caches"""
        self.inventory_files_cache.clear()
        self.file_records_cache.clear()
        self.query_results_cache.clear()
        self.discovered_prefixes.clear()
