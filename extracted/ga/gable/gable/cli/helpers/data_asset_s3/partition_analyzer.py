"""
Partition analysis functionality for storage inventory files.
"""

import re
from typing import Any, Dict, List, Tuple

import numpy as np

from .constants import StorageInventoryConstants
from .utils import Utils


class PartitionAnalyzer:
    """Analyzes partition information from storage keys"""

    def __init__(self, logger):
        self.logger = logger

    def extract_partition_info(self, key: str) -> Tuple[str, List[Tuple[str, str]]]:
        """Extract prefix and partition key-value pairs from a storage key"""
        parts = key.split("/", 1)
        prefix = parts[0]
        partition_path = parts[1] if len(parts) > 1 else ""
        partition_pairs = StorageInventoryConstants.PARTITION_REGEX.findall(
            partition_path
        )
        return prefix, partition_pairs

    def collect_partition_values(
        self, keys: List[str]
    ) -> Dict[str, Dict[str, List[str]]]:
        """Collect partition values by prefix and key"""
        from collections import defaultdict

        prefix_partitions = defaultdict(lambda: defaultdict(list))

        for key in keys:
            key_clean = key.replace("%3D", "=")
            prefix, pairs = self.extract_partition_info(key_clean)

            for k, v in pairs:
                # Robustly decode partition value
                v_decoded = Utils.fully_decode(v)

                # Skip dynamic partition variables
                if v_decoded.strip().lower() in {
                    "${hiveconf:from_ds}",
                    "${hiveconf:from_ds}".lower(),
                }:
                    continue

                prefix_partitions[prefix][k].append(v_decoded)

        return {prefix: dict(inner) for prefix, inner in prefix_partitions.items()}

    def analyze_partition_values(
        self, values: List[str], key: str
    ) -> Tuple[str, Dict[str, Any]]:
        """Analyze partition values to determine type and summary stats"""
        # For forced min/max keys
        if key in StorageInventoryConstants.FORCE_MINMAX_KEYS:
            scheme = "date" if key == "ds" else "numeric"
            min_val = min(values)
            max_val = max(values)
            return scheme, {"min_value": min_val, "max_value": max_val}

        # Try to determine if values are numeric
        try:
            floats = np.array([float(x) for x in values])
            is_numeric = True
        except Exception:
            is_numeric = False

        # Check if values look like dates
        if all(re.match(r"^\d{4}-\d{2}-\d{2}$", x) for x in values):
            return "date", {"min_date": min(values), "max_date": max(values)}

        # Handle numeric values
        elif is_numeric:
            min_val = min(values, key=lambda x: float(x))
            max_val = max(values, key=lambda x: float(x))
            return "numeric", {"min_value": min_val, "max_value": max_val}

        # Handle categorical values
        else:
            uniques = sorted(set(values))
            if len(uniques) > StorageInventoryConstants.DISTINCT_CAP:
                uniques = uniques[:10] + ["…"] + uniques[-10:]
            return "categorical", {"distinct_values": uniques}

    def determine_hierarchy(
        self, keys: List[str], prefix: str, partition_keys: List[str]
    ) -> str:
        """Determine the partition hierarchy for a prefix"""
        # Try to find a sample key
        sample_key = next((k for k in keys if k.startswith(prefix + "/")), None)

        if sample_key:
            key_clean = sample_key.replace("%3D", "=")
            parts = key_clean.split("/", 1)
            partition_path = parts[1] if len(parts) > 1 else ""
            pairs = StorageInventoryConstants.PARTITION_REGEX.findall(partition_path)

            if pairs:
                return "/".join(f"{k}={{}}" for k, _ in pairs)

        # Fallback to using partition keys
        if partition_keys:
            return "/".join(f"{k}={{}}" for k in partition_keys)

        return ""
