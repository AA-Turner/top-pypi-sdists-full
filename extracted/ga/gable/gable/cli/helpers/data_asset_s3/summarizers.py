"""
Summarizer classes for inventory metadata analysis.
"""

import random
import re
import time
import urllib.parse
from typing import Any, Dict, List, Optional

import pyarrow.compute as pc
from tqdm import tqdm

from .cache_manager import InventoryCacheManager
from .data_loader import InventoryDataLoader
from .file_processor import InventoryFileProcessor
from .partition_analyzer import PartitionAnalyzer


class InventoryMetadataSummarizer:
    """Summarizes file-level metadata by prefix from storage inventory"""

    def __init__(self, logger, inventory_dir=None):
        """
        Initialize the file metadata summarizer.

        Args:
            logger: Logger instance
            inventory_dir: Directory where inventory reports are stored.
                           If None, uses the default location.
        """
        self.logger = logger
        self.loader = InventoryDataLoader(logger, inventory_dir)
        self.processor = InventoryFileProcessor(logger)

    def analyze_inventory(
        self,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Generate file metadata summary for all specified prefixes"""
        # Load file metadata
        arrow_table = self.loader.load_file_metadata(include_prefixes, exclude_prefixes)
        if arrow_table.num_rows == 0:
            return {}

        # Enrich with derived columns
        enriched_table = self.processor.enrich_metadata_table(arrow_table)

        # Get unique prefixes for processing
        all_prefixes = enriched_table["prefix"].to_pandas().unique().tolist()

        if include_prefixes:
            prefixes_set = set(include_prefixes)
            use_prefixes = [p for p in all_prefixes if p in prefixes_set]
        else:
            use_prefixes = all_prefixes

        # Generate summaries for each prefix
        result = {}
        for prefix in use_prefixes:
            result[prefix] = self.processor.create_prefix_summary(
                enriched_table, prefix
            )

        return result


class PartitionSummarizer:
    """Summarizes partition metadata by prefix from storage inventory"""

    def __init__(self, logger, inventory_dir=None):
        """
        Initialize the partition summarizer.

        Args:
            logger: Logger instance
            inventory_dir: Directory where inventory reports are stored.
                           If None, uses the default location.
        """
        self.logger = logger
        self.inventory_dir = inventory_dir

    def analyze_inventory(
        self,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
        max_key_for_performance: int = 200000,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Analyze partition metadata for the inventory.

        Args:
            prefixes: Optional list of prefixes to analyze

        Returns:
            Dictionary of partition metadata by prefix
        """
        start_time = time.time()

        # Check if we have cached results for these prefixes
        cache_manager = InventoryCacheManager()
        incl_prefixes_str = (
            "_".join(sorted(include_prefixes)) if include_prefixes else "all"
        )
        excl_prefixes_str = (
            "_".join(sorted(exclude_prefixes)) if exclude_prefixes else ""
        )
        cache_key = f"partition_analysis_{self.inventory_dir}_{incl_prefixes_str}_{excl_prefixes_str}"
        cached_results = cache_manager.get_query_result(cache_key)
        if cached_results is not None:
            self.logger.info("Using cached partition analysis results")
            return cached_results

        # Load all relevant keys
        loader = InventoryDataLoader(self.logger, self.inventory_dir)
        keys = loader.load_keys(include_prefixes, exclude_prefixes)

        if not keys:
            self.logger.warning("No keys found for partition analysis")
            return {}

        self.logger.info("Loaded %d keys for processing", len(keys))

        total_keys = len(keys)

        # OPTIMIZATION: Use fixed sampling for large datasets to avoid performance issues
        # This dramatically speeds up processing with minimal impact on results
        if total_keys > max_key_for_performance:
            random.seed(42)  # Use a fixed seed for reproducibility
            sampling_rate = max_key_for_performance / total_keys
            self.logger.info(
                f"Using {sampling_rate:.1%} sampling to process {max_key_for_performance} of {total_keys} keys"
            )
            sampled_keys = random.sample(keys, max_key_for_performance)
        else:
            # If dataset is small enough, use all keys
            self.logger.info(f"Processing all {total_keys} keys (no sampling needed)")
            sampled_keys = keys

        # If prefixes are explicitly provided, use those directly instead of rediscovering
        candidate_prefixes = set()
        if include_prefixes:
            self.logger.info(
                f"Using {len(include_prefixes)} explicitly specified prefixes instead of discovering"
            )
            candidate_prefixes = set(include_prefixes)
        else:
            # Only do prefix detection if no prefixes were explicitly provided
            self.logger.info("Starting prefix detection...")

            # Fast prefix detection
            # Use a small fixed sample specifically for prefix detection
            prefix_sample_size = min(
                50000, len(keys)
            )  # 50K keys max for prefix detection
            prefix_detection_sample = (
                random.sample(keys, prefix_sample_size)
                if len(keys) > prefix_sample_size
                else keys
            )

            # Process in smaller batches to avoid memory issues
            t = tqdm(total=len(prefix_detection_sample), desc="Prefix detection")
            BATCH_SIZE = 10000
            for i in range(0, len(prefix_detection_sample), BATCH_SIZE):
                batch = prefix_detection_sample[i : i + BATCH_SIZE]
                for k in batch:
                    if "/" in k:
                        candidate_prefixes.add(k.split("/")[0])
                    t.update()

            t.close()
            self.logger.info(
                f"Prefix detection complete. Found {len(candidate_prefixes)} candidate prefixes"
            )

        # For very large datasets, process in two phases:
        # 1. Quick scan to identify prefixes that actually have partitions
        # 2. Detailed analysis of only those prefixes with partitions
        partition_pattern = r"([^=/]+)=([^=/]+)"
        prefixes_with_partitions = []

        # Phase 1: Quick scan with minimal sampling for each prefix
        self.logger.info("Starting quick scan for partitions...")
        prefix_count = len(candidate_prefixes)

        # Limit to a sample of prefixes if there are many
        if prefix_count > 1000:
            self.logger.info(
                f"Sampling {1000} of {prefix_count} prefixes for quick scan"
            )
            candidate_prefixes = sorted(list(candidate_prefixes))
            random.seed(42)
            candidate_prefixes = random.sample(candidate_prefixes, 1000)

        for i, prefix in tqdm(
            enumerate(candidate_prefixes),
            desc="Quick scan for partitions",
            total=len(candidate_prefixes),
        ):
            # Get a minimal sample of keys for this prefix
            prefix_keys = []
            for key in sampled_keys:
                if key.startswith(f"{prefix}/"):
                    prefix_keys.append(key)
                    if (
                        len(prefix_keys) >= 10
                    ):  # Only need a few keys to detect partitions
                        break

            # Check both raw and URL-decoded keys for partition patterns
            has_partitions = False
            for k in prefix_keys:
                # Check raw key
                if re.search(partition_pattern, k):
                    has_partitions = True
                    break

                # Also check URL-decoded key (in case of keys like 'key%3Dvalue')
                decoded_key = urllib.parse.unquote(k)
                if decoded_key != k and re.search(partition_pattern, decoded_key):
                    has_partitions = True
                    break

            if has_partitions:
                prefixes_with_partitions.append(prefix)

        self.logger.info(
            f"Found {len(prefixes_with_partitions)} prefixes with partitions out of {len(candidate_prefixes)} candidates"
        )

        # Phase 2: Process only prefixes with partitions
        results = {}
        all_prefixes = sorted(prefixes_with_partitions)
        total_prefixes = len(all_prefixes)

        # If there are too many prefixes with partitions, sample them
        MAX_PREFIXES_TO_ANALYZE = 500  # Limit detailed analysis to a reasonable number
        if total_prefixes > MAX_PREFIXES_TO_ANALYZE:
            self.logger.info(
                f"Limiting detailed analysis to {MAX_PREFIXES_TO_ANALYZE} of {total_prefixes} partitioned prefixes"
            )
            random.seed(42)
            all_prefixes = random.sample(all_prefixes, MAX_PREFIXES_TO_ANALYZE)
            total_prefixes = len(all_prefixes)

        # Process prefixes in batches for better progress reporting
        self.logger.info(
            f"Starting detailed partition analysis for {total_prefixes} prefixes"
        )

        for idx, prefix in tqdm(
            enumerate(all_prefixes, 1),
            desc="Detailed partition analysis",
            total=total_prefixes,
        ):
            try:
                # Use a timeout mechanism to prevent hanging on a single prefix
                start_time_prefix = time.time()
                prefix_results = self._analyze_prefix_partitions_fast(
                    prefix, sampled_keys, idx, total_prefixes
                )

                # Check for timeout
                if time.time() - start_time_prefix > 5.0:  # 5 second timeout per prefix
                    self.logger.warning(
                        f"Analysis for prefix {prefix} took too long ({time.time() - start_time_prefix:.1f}s)"
                    )

                if prefix_results:
                    results[prefix] = prefix_results
            except Exception as e:
                self.logger.error(
                    f"Error analyzing partitions for prefix {prefix}: {str(e)}"
                )

        # Cache results for future use
        cache_manager.cache_query_result(cache_key, results)

        elapsed = time.time() - start_time
        self.logger.info(f"Partition analysis completed in {elapsed:.2f} seconds")

        return results

    def _analyze_prefix_partitions_fast(
        self, prefix: str, all_keys: List[str], idx: int, total_prefixes: int
    ) -> Optional[Dict[str, Any]]:
        """
        Fast partition analysis for a specific prefix using sampling.

        Args:
            prefix: The prefix to analyze
            all_keys: List of all keys
            idx: The current prefix index (for logging)
            total_prefixes: Total number of prefixes (for logging)

        Returns:
            Dictionary of partition metadata or None if no partitions
        """
        # Filter keys for just this prefix - optimized to stop after finding enough
        prefix_keys = []
        prefix_pattern = f"{prefix}/"
        MAX_KEYS_FOR_ANALYSIS = 100  # Significantly reduce this for speed

        for key in all_keys:
            if key.startswith(prefix_pattern):
                prefix_keys.append(key)
                if len(prefix_keys) >= MAX_KEYS_FOR_ANALYSIS:
                    break

        if not prefix_keys:
            return None

        # Extract partition keys and values - use a fixed small sample
        partition_pattern = r"([^=/]+)=([^=/]+)"
        partitions_data = {}

        # If too many keys, sample down to a reasonable number
        if len(prefix_keys) > 50:
            random.seed(prefix)
            prefix_keys = random.sample(prefix_keys, 50)

        for key in prefix_keys:
            # Try both raw and URL-decoded keys
            keys_to_check = [key]

            # Add URL-decoded version if different
            decoded_key = urllib.parse.unquote(key)
            if decoded_key != key:
                keys_to_check.append(decoded_key)

            for k in keys_to_check:
                for match in re.finditer(partition_pattern, k):
                    p_key, p_value = match.group(1), match.group(2)
                    if p_key not in partitions_data:
                        partitions_data[p_key] = set()
                    partitions_data[p_key].add(p_value)

        if not partitions_data:
            return None

        # Determine partition schemes and ranges
        partition_keys = list(partitions_data.keys())
        partition_scheme = {}
        partition_values = {}

        for p_key, values in partitions_data.items():
            # Convert set to list for min/max operations
            values_list = list(values)

            # Determine scheme (numeric or string)
            if all(
                re.match(r"^\d+$", v) for v in list(values)[: min(100, len(values))]
            ):
                scheme = "numeric"
            else:
                scheme = "string"

            partition_scheme[p_key] = scheme

            # Calculate min/max
            partition_values[p_key] = {
                "min_value": min(values_list),
                "max_value": max(values_list),
            }

        # Determine partition hierarchy
        # Use the first key as a template
        sample_key = prefix_keys[0]
        hierarchy_parts = []

        # Try with both raw and URL-decoded keys
        keys_to_check = [sample_key]
        decoded_key = urllib.parse.unquote(sample_key)
        if decoded_key != sample_key:
            keys_to_check.append(decoded_key)

        # Try to find partition pattern in any of the keys
        for key_to_check in keys_to_check:
            for match in re.finditer(partition_pattern, key_to_check):
                p_key = match.group(1)
                hierarchy_parts.append(f"{p_key}={{}}")

            if hierarchy_parts:
                break  # Stop if we found a hierarchy pattern

        # If we still don't have a hierarchy, try to construct one from the partition keys
        if not hierarchy_parts and partition_keys:
            hierarchy_parts = [f"{key}={{}}" for key in partition_keys]

        partition_hierarchy = "/".join(hierarchy_parts) if hierarchy_parts else None

        # Compile results
        return {
            "partition_keys": partition_keys,
            "partition_scheme": partition_scheme,
            "partition_hierarchy": partition_hierarchy,
            "partitions": partition_values,
        }
