#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025
"""Module containing Source interface class."""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PipelineDto:
    """Standardized pipeline data transfer object to use in codegen."""

    pipeline_config: dict
    pipeline_rules: dict
    library_definitions: dict


class Source(ABC):
    """Interface for flow definition sources."""

    @abstractmethod
    def load(self) -> PipelineDto:
        """Here we should return source data as intermediate format."""
