"""Jira hierarchy detector stub.

Raises ``NotImplementedError`` on all methods per NFR-003.
Reserved for future Jira sub-task / epic-link hierarchy detection.
"""

from __future__ import annotations

from agentic_devtools.hierarchy.detector import HierarchyDetector
from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata

_JIRA_NOT_IMPLEMENTED_MSG = (
    "Jira hierarchy detection is not yet implemented. See NFR-003 in the spec nesting infrastructure specification."
)


class JiraHierarchyDetector(HierarchyDetector):
    """Stub Jira hierarchy detector that raises NotImplementedError.

    All methods raise ``NotImplementedError`` to satisfy NFR-003's requirement
    for a stubbed Jira implementation. This class will be replaced with a real
    implementation when Jira hierarchy support is added.
    """

    def detect_parent(self, issue_number: int) -> int | None:
        """Detect parent — not implemented for Jira."""
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def detect_children(self, issue_number: int) -> list[tuple[int, str]]:
        """Detect children — not implemented for Jira."""
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def classify(self, issue_number: int) -> HierarchyLevel:
        """Classify — not implemented for Jira."""
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)

    def build_metadata(self, issue_number: int) -> HierarchyMetadata:
        """Build metadata — not implemented for Jira."""
        raise NotImplementedError(_JIRA_NOT_IMPLEMENTED_MSG)
