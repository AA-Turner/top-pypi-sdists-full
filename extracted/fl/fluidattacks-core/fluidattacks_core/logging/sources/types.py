from abc import ABC, abstractmethod


class SourceStrategy(ABC):
    @staticmethod
    @abstractmethod
    def detect() -> bool:
        """Detect if the current runtime is using this source."""

    @staticmethod
    @abstractmethod
    def log_metadata() -> dict[str, str]:
        """Get the metadata to be added to the log record."""
