"""
Metadata builder module implementing a Builder pattern for inventory metadata collection.
This allows for modular, configurable, and extensible metadata generation.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class MetadataCollector(ABC):
    """Abstract base class for metadata collectors"""

    def __init__(self, logger, inventory_dir=None):
        """
        Initialize a metadata collector

        Args:
            logger: Logger instance
            inventory_dir: Directory where inventory reports are stored
        """
        self.logger = logger
        self.inventory_dir = inventory_dir

    @abstractmethod
    def collect(
        self,
        metadata: Dict[str, Dict[str, Any]],
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> None:
        """
        Collect metadata and add it to the metadata dictionary

        Args:
            metadata: Dictionary to add metadata to, structured as {prefix: {metadata_key: value}}
            prefixes: Optional list of prefixes to limit collection to
        """


class InventoryMetadataBuilder:
    """
    Builder for inventory metadata.

    Follows the Builder pattern to assemble metadata from multiple collectors.
    Each collector is responsible for a specific aspect of the metadata.
    """

    def __init__(self, logger, inventory_dir=None):
        """
        Initialize the metadata builder

        Args:
            logger: Logger instance
            inventory_dir: Directory where inventory reports are stored
        """
        self.logger = logger
        self.inventory_dir = inventory_dir
        self.collectors = []
        self.metadata = {}

    def register_collector(
        self, collector: MetadataCollector
    ) -> "InventoryMetadataBuilder":
        """
        Register a metadata collector

        Args:
            collector: The collector to register

        Returns:
            self, for method chaining
        """
        self.collectors.append(collector)
        self.logger.info(f"Registered collector: {collector.__class__.__name__}")
        return self

    def initialize_metadata(
        self, prefixes: Optional[List[str]] = None
    ) -> "InventoryMetadataBuilder":
        """
        Initialize the metadata dictionary with empty entries for each prefix

        Args:
            prefixes: Optional list of prefixes to initialize

        Returns:
            self, for method chaining
        """
        # If no prefixes are provided, collectors will determine them
        if prefixes:
            self.metadata = {prefix: {} for prefix in prefixes}
        else:
            self.metadata = {}

        return self

    def build(
        self,
        include_prefixes: Optional[List[str]] = None,
        exclude_prefixes: Optional[List[str]] = None,
    ) -> Dict[str, Dict[str, Any]]:
        """
        Build the metadata by running all registered collectors

        Args:
            prefixes: Optional list of prefixes to limit collection to

        Returns:
            Complete metadata dictionary
        """
        self.logger.info("Building metadata with %d collectors", len(self.collectors))

        # Initialize metadata if not already done
        if not self.metadata:
            self.initialize_metadata(include_prefixes)

        # Run each collector sequentially
        for collector in self.collectors:
            try:
                collector.collect(self.metadata, include_prefixes, exclude_prefixes)
            except Exception as e:
                self.logger.error(
                    f"Error in collector {collector.__class__.__name__}: {str(e)}"
                )

        self.logger.info("Metadata build complete for %d prefixes", len(self.metadata))
        return self.metadata
