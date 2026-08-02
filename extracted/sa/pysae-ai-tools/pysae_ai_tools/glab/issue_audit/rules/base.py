"""Base class for audit rules.

Each rule implements three phases:
- diagnose: detect problems (fast, no external calls ideally)
- enrich: resolve fixes, set fixable=True/False (may call Claude/API)
- build_actions: produce plan actions from enriched violations
"""

from abc import ABC, abstractmethod
from typing import Any

from ....common.glab.models import GitLabIssue
from ..diagnostic import IssueReport, RuleContext, Violation


class Rule(ABC):
    """Base class for an audit rule."""

    name: str  # e.g. "labels", "required_labels"
    display_name: str  # e.g. "Labels projet"
    color: str = "#6c757d"  # hex color for UI charts

    @abstractmethod
    def diagnose(self, issue: GitLabIssue, ctx: RuleContext) -> list[Violation]:
        """Detect problems. Returns violations with fixable=None."""

    def enrich(self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext) -> None:
        """Resolve a violation: set fixable, fix, method. Mutates in-place."""
        violation.fixable = False

    def build_actions(
        self, violation: Violation, report: IssueReport, issue_data: GitLabIssue, ctx: RuleContext
    ) -> list[dict[str, Any]]:
        """Build plan actions for a fixable violation."""
        return []

    @property
    def fix_types(self) -> dict[str, str]:
        """Map of fix_type key -> display name for this rule's fixes."""
        return {}
