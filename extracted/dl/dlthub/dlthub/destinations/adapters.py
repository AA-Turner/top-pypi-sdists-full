"""This module collects all destination adapters present in `impl` namespace"""

from dlthub.destinations.impl.iceberg.iceberg_adapter import iceberg_adapter, iceberg_partition

__all__ = [
    "iceberg_adapter",
    "iceberg_partition",
]
