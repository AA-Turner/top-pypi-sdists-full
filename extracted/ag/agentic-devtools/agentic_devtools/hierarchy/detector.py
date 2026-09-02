"""Abstract base class for hierarchy detection.

Defines the ``HierarchyDetector`` ABC that concrete implementations
(GitHub, Jira) must subclass. Follows the ``CIPlatformProvider`` pattern
used elsewhere in agentic-devtools.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class HierarchyDetector(ABC):
    """Abstract base class for detecting issue hierarchy relationships.

    Concrete implementations must query their respective issue tracking
    platform (GitHub, Jira, etc.) to discover parent/child relationships
    and classify issues into hierarchy levels.
    """

    @abstractmethod
    def detect_parent(self, issue_number: int) -> int | None:
        """Detect the parent issue number for the given issue.

        Args:
            issue_number: The issue to check for a parent.

        Returns:
            The parent issue number, or None if the issue has no parent.
        """

    @abstractmethod
    def detect_children(self, issue_number: int) -> list[tuple[int, str]]:
        """Detect child issues for the given issue.

        Args:
            issue_number: The issue to check for children.

        Returns:
            List of (issue_number, title) tuples for each child, ordered.
        """

    @abstractmethod
    def classify(self, issue_number: int) -> HierarchyLevel:
        """Classify the issue into a hierarchy level.

        Args:
            issue_number: The issue to classify.

        Returns:
            The hierarchy level (EPIC, FEATURE, TASK, or STANDALONE).
        """

    @abstractmethod
    def build_metadata(self, issue_number: int) -> HierarchyMetadata:
        """Build full hierarchy metadata for the given issue.

        Combines parent detection, child detection, and classification
        into a complete HierarchyMetadata instance.

        Args:
            issue_number: The issue to build metadata for.

        Returns:
            Complete HierarchyMetadata for the issue.
        """
