"""Ingestion module for EmDash."""

from .orchestrator import IngestionOrchestrator
from .repository import RepositoryManager
from .change_detector import ChangeDetector, ChangedFiles

__all__ = ["IngestionOrchestrator", "RepositoryManager", "ChangeDetector", "ChangedFiles"]
