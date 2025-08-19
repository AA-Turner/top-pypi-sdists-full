"""
Concrete metadata collector implementations for the inventory metadata builder.
"""

import datetime
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

from tqdm import tqdm

from .cache_manager import InventoryCacheManager
from .data_loader import InventoryDataLoader
from .metadata_builder import MetadataCollector
from .summarizers import InventoryMetadataSummarizer, PartitionSummarizer


class FileMetadataCollector(MetadataCollector):
    """Collector for file-level metadata like counts, sizes, and types"""

    def __init__(self, logger, inventory_dir=None):
        """
        Initialize the FileMetadataCollector

        Args:
            logger: Logger instance
            inventory_dir: Directory where inventory reports are stored
        """
        super().__init__(logger, inventory_dir)
        self.summarizer = InventoryMetadataSummarizer(logger, inventory_dir)
        self.cache_manager = InventoryCacheManager()

    def collect(
        self,
        metadata: Dict[str, Dict[str, Any]],
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> None:
        """
        Collect file-level metadata and add it to the metadata dictionary

        Args:
            metadata: Dictionary to add metadata to
            prefixes: Optional list of prefixes to limit collection to
        """
        self.logger.info("Collecting file metadata")

        # Generate a cache key based on prefixes
        incl_prefixes_str = (
            "_".join(sorted(include_prefixes)) if include_prefixes else "all"
        )
        excl_prefixes_str = (
            "_".join(sorted(exclude_prefixes)) if exclude_prefixes else ""
        )
        cache_key = f"file_metadata_{self.inventory_dir}_{incl_prefixes_str}_{excl_prefixes_str}"

        # Check if we have cached results
        cached_result = self.cache_manager.get_query_result(cache_key)
        if cached_result is not None:
            self.logger.info("Using cached file metadata")
            file_metadata = cached_result
        else:
            # Get file metadata (no parallelization)
            file_metadata = self.summarizer.analyze_inventory(
                include_prefixes, exclude_prefixes
            )

            # Cache the results
            self.cache_manager.cache_query_result(cache_key, file_metadata)

        # If metadata is empty, initialize with discovered prefixes
        if not metadata and file_metadata:
            for prefix in file_metadata:
                metadata[prefix] = {}

        # Add file metadata to existing prefixes
        for prefix, prefix_metadata in file_metadata.items():
            if prefix not in metadata:
                metadata[prefix] = {}
            metadata[prefix].update(prefix_metadata)

        self.logger.info(
            "File metadata collection complete for %d prefixes", len(file_metadata)
        )


class PartitionMetadataCollector(MetadataCollector):
    """Collector for partition-level metadata like partition keys and schemes"""

    def __init__(self, logger, inventory_dir=None):
        super().__init__(logger, inventory_dir)
        self.summarizer = PartitionSummarizer(logger, inventory_dir)
        self.cache_manager = InventoryCacheManager()

    def collect(
        self,
        metadata: Dict[str, Dict[str, Any]],
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> None:
        """
        Collect partition metadata and add it to the metadata dictionary

        Args:
            metadata: Dictionary to add metadata to
            prefixes: Optional list of prefixes to limit collection to
        """
        self.logger.info("Collecting partition metadata")

        # Generate a cache key based on prefixes
        incl_prefixes_str = (
            "_".join(sorted(include_prefixes)) if include_prefixes else "all"
        )
        excl_prefixes_str = (
            "_".join(sorted(exclude_prefixes)) if exclude_prefixes else ""
        )
        cache_key = f"partition_metadata_{self.inventory_dir}_{incl_prefixes_str}_{excl_prefixes_str}"

        # Check if we have cached results
        cached_result = self.cache_manager.get_query_result(cache_key)
        if cached_result is not None:
            self.logger.info("Using cached partition metadata")
            partition_metadata = cached_result
        else:
            # Instead of discovering prefixes again, use the ones already in metadata
            # This ensures we analyze all prefixes found during file metadata collection
            existing_prefixes = list(metadata.keys()) if metadata else None

            # If both file-discovered prefixes and user-specified prefixes exist, use their intersection
            if existing_prefixes and include_prefixes:
                prefixes_to_analyze = [
                    p for p in existing_prefixes if p in include_prefixes
                ]
                self.logger.info(
                    f"Analyzing {len(prefixes_to_analyze)} prefixes that exist in both file metadata and user-specified list"
                )
            elif existing_prefixes:
                prefixes_to_analyze = existing_prefixes
                self.logger.info(
                    f"Analyzing all {len(prefixes_to_analyze)} prefixes found in file metadata"
                )
            else:
                prefixes_to_analyze = include_prefixes
                self.logger.info(
                    f"No existing metadata prefixes found, using user-specified prefixes"
                )

            # Get partition metadata using the existing prefixes
            partition_metadata = self.summarizer.analyze_inventory(
                include_prefixes=prefixes_to_analyze, exclude_prefixes=exclude_prefixes
            )

            # Cache the results
            self.cache_manager.cache_query_result(cache_key, partition_metadata)

        # If metadata is empty, initialize with discovered prefixes
        if not metadata and partition_metadata:
            for prefix in partition_metadata:
                metadata[prefix] = {}

        # Add partition metadata to existing prefixes
        for prefix, prefix_metadata in partition_metadata.items():
            if prefix not in metadata:
                metadata[prefix] = {}
            metadata[prefix].update(prefix_metadata)

        self.logger.info(
            "Partition metadata collection complete for %d prefixes",
            len(partition_metadata),
        )


class LatestObjectsCollector(MetadataCollector):
    """Collector for the latest N objects for each prefix"""

    def __init__(self, logger, inventory_dir=None, limit: int = 5):
        super().__init__(logger, inventory_dir)
        self.data_loader = InventoryDataLoader(logger, inventory_dir)
        self.limit = limit
        self.cache_manager = InventoryCacheManager()

    def _process_prefix_batch(
        self,
        metadata: Dict[str, Dict[str, Any]],
        prefixes: List[str],
        exclude_prefixes: Optional[List[str]] = None,
        t: Optional[tqdm] = None,
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Process a batch of prefixes in parallel"""
        results = {}

        def process_single_prefix(prefix: str) -> tuple[str, List[Dict[str, Any]]]:
            if prefix not in metadata:
                self.logger.warning(
                    f"Skip collecting latest objects: prefix {prefix} not in metadata"
                )
                return prefix, []

            self.logger.info(f"Collecting latest objects for prefix: {prefix}")

            # Generate a cache key
            cache_key = f"latest_objects_formatted_{self.inventory_dir}_{prefix}_{self.limit}_{'_'.join(exclude_prefixes or [])}"
            cached_objects = self.cache_manager.get_query_result(cache_key)

            if cached_objects is not None:
                self.logger.info(
                    f"Using cached formatted latest objects for prefix: {prefix}"
                )
                return prefix, cached_objects

            arrow_table = self.data_loader.get_latest_objects(
                prefix, exclude_prefixes=exclude_prefixes, limit=self.limit
            )

            if arrow_table.num_rows == 0:
                self.logger.warning(f"No objects found for prefix: {prefix}")
                return prefix, []

            # Convert Arrow table to list of dictionaries
            latest_objects = []
            for i in range(arrow_table.num_rows):
                raw_key = arrow_table["Key"][i].as_py()
                decoded_key = urllib.parse.unquote(raw_key)
                last_modified_iso = arrow_table["LastModifiedDate"][i].as_py()

                if isinstance(last_modified_iso, str):
                    try:
                        last_modified_datetime = datetime.datetime.fromisoformat(
                            last_modified_iso.replace("Z", "+00:00")
                        )
                        last_modified = last_modified_datetime.strftime(
                            "%Y-%m-%d %H:%M:%S UTC"
                        )
                    except ValueError:
                        last_modified = last_modified_iso
                else:
                    last_modified = str(last_modified_iso)

                row = {
                    "key": decoded_key,
                    "raw_key": raw_key,  # Keep the original key for S3 operations
                    "size_bytes": arrow_table["Size"][i].as_py(),
                    "last_modified": last_modified,
                }
                latest_objects.append(row)

            # Cache the results
            self.cache_manager.cache_query_result(cache_key, latest_objects)

            self.logger.info(
                f"Added {len(latest_objects)} latest objects to prefix {prefix}"
            )
            return prefix, latest_objects

        # Process prefixes in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            # Submit all tasks at once
            future_to_prefix = {
                executor.submit(process_single_prefix, prefix): prefix
                for prefix in prefixes
            }

            # Process results as they complete
            for future in as_completed(future_to_prefix):
                try:
                    prefix, objects = future.result()
                    if objects:  # Only add non-empty results
                        results[prefix] = objects
                except Exception as e:
                    prefix = future_to_prefix[future]
                    self.logger.error(f"Error processing prefix {prefix}: {str(e)}")
                finally:
                    if t:
                        t.update()  # type: ignore

        return results

    def collect(
        self,
        metadata: Dict[str, Dict[str, Any]],
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> None:
        """
        Collect the latest objects for each prefix and add to the metadata dictionary

        Args:
            metadata: Dictionary to add metadata to
            prefixes: Optional list of prefixes to limit collection to
        """
        self.logger.info(f"Collecting latest {self.limit} objects per prefix")

        # If prefixes not specified, use keys from metadata
        collect_prefixes = (
            include_prefixes if include_prefixes else list(metadata.keys())
        )

        # Process prefixes in batches to optimize memory usage
        t = tqdm(total=len(collect_prefixes), desc="Processing prefixes")
        batch_size = 25
        try:
            for i in range(0, len(collect_prefixes), batch_size):
                batch = collect_prefixes[i : i + batch_size]
                batch_results = self._process_prefix_batch(
                    metadata, batch, exclude_prefixes, t
                )

                # Update metadata with batch results
                for prefix, objects in batch_results.items():
                    if prefix not in metadata:
                        metadata[prefix] = {}
                    metadata[prefix]["latest_objects"] = objects
        except Exception as e:
            self.logger.error(f"Error collecting latest objects: {str(e)}")
            raise e
        finally:
            t.close()

        self.logger.info(
            "Latest objects collection complete for %d prefixes", len(collect_prefixes)
        )
