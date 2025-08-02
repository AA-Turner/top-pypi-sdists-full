"""
Main controller for generating catalog from inventory data.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .collectors import (
    FileMetadataCollector,
    LatestObjectsCollector,
    PartitionMetadataCollector,
)
from .logging_manager import LoggingManager
from .metadata_builder import InventoryMetadataBuilder


class InventoryCatalogGenerator:
    """Main application controller coordinating all inventory analysis components"""

    def __init__(self, inventory_dir=None):
        """
        Initialize the catalog generator.

        Args:
            inventory_dir: Directory where inventory reports are stored.
                           If None, uses the default location.
        """
        self.logger = LoggingManager.setup()
        self.inventory_dir = inventory_dir

    def generate_inventory_profile(
        self,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
        output_path: str = "comprehensive_summary_v2.json",
        partitions_only: bool = False,
        filemeta_only: bool = False,
        include_latest_objects: bool = False,
        latest_objects_limit: int = 5,
    ) -> Dict[str, Any]:
        """Run the profiler and generate a comprehensive storage inventory summary"""
        self.logger.info("Script started. Output: %s", output_path)
        self.logger.info(
            "Using inventory directory: %s", self.inventory_dir or "default location"
        )

        # Create the metadata builder
        builder = InventoryMetadataBuilder(self.logger, self.inventory_dir)
        builder.initialize_metadata(include_prefixes)

        # Register collectors based on user options
        if not partitions_only:
            builder.register_collector(
                FileMetadataCollector(self.logger, self.inventory_dir)
            )

        if not filemeta_only:
            builder.register_collector(
                PartitionMetadataCollector(self.logger, self.inventory_dir)
            )

        if include_latest_objects:
            builder.register_collector(
                LatestObjectsCollector(
                    self.logger, self.inventory_dir, latest_objects_limit
                )
            )

        # Build the metadata
        metadata = builder.build(include_prefixes, exclude_prefixes)

        # Write output file
        Path(output_path).write_text(json.dumps(metadata, indent=2), encoding="utf-8")

        self.logger.info(
            "✅ Wrote comprehensive prefix summary for %d prefixes → %s",
            len(metadata),
            Path(output_path).resolve(),
        )
        self.logger.info("⚡ Finished with DuckDB + PyArrow (fast path)")

        return metadata
