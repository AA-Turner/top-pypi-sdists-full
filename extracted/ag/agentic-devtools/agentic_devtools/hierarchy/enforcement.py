"""Parent-first processing enforcement for hierarchical specs.

Implements FR-005: the system MUST reject speckit pipeline triggers for
issues whose parent has not been specked yet. Uses a two-stage directory
lookup (hierarchical path → legacy flat path) to determine parent completion.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from agentic_devtools.hierarchy.models import HierarchyLevel, HierarchyMetadata


class EnforcementAction(Enum):
    """Outcome of parent-first enforcement check."""

    ALLOW = "allow"
    REJECT = "reject"


@dataclass
class EnforcementResult:
    """Result of a parent-first enforcement check.

    Attributes:
        action: Whether to allow or reject the trigger.
        reason: Human-readable explanation of the decision.
        parent_issue: The parent issue number (None if no parent).
        parent_path: Path to the parent's spec directory if found.
    """

    action: EnforcementAction
    reason: str
    parent_issue: int | None = None
    parent_path: Path | None = None

    @property
    def allowed(self) -> bool:
        """Whether the trigger is allowed to proceed."""
        return self.action == EnforcementAction.ALLOW


def check_parent_specked(
    parent_issue: int,
    specs_root: Path,
    *,
    ancestors: list[int] | None = None,
) -> tuple[bool, Path | None]:
    """Check whether a parent issue has been specked using two-stage lookup.

    Stage 1: Check hierarchical nested path (e.g., specs/100/101/).
    Stage 2: Check legacy flat path (e.g., specs/100-*/).

    Args:
        parent_issue: The parent issue number.
        specs_root: Root path of the specs directory.
        ancestors: Optional list of ancestor issue numbers for hierarchical
                   path resolution (grandparent → parent order).

    Returns:
        Tuple of (is_specked, path_found). path_found is the directory path
        if found, None otherwise.
    """
    # Stage 1: Hierarchical path
    if ancestors:
        parent_base = specs_root.joinpath(*[str(a) for a in ancestors])
        hierarchical_path = parent_base / str(parent_issue)
        if hierarchical_path.is_dir():
            return (True, hierarchical_path)

        for match_path in parent_base.glob(f"{parent_issue}-*"):
            if match_path.is_dir():
                return (True, match_path)
    else:
        # Direct child of root
        hierarchical_path = specs_root / str(parent_issue)
        if hierarchical_path.is_dir():
            return (True, hierarchical_path)

    # Stage 2: Legacy flat path (specs/{number}-*/)
    for match_path in specs_root.glob(f"{parent_issue}-*"):
        if match_path.is_dir():
            return (True, match_path)

    return (False, None)


def reject_trigger(
    issue_number: int,
    parent_issue: int,
    *,
    owner: str = "",
    repo: str = "",
) -> str:
    """Generate a rejection comment for an issue whose parent is unspecked.

    Args:
        issue_number: The child issue being rejected.
        parent_issue: The unspecked parent issue.
        owner: Repository owner (for comment formatting).
        repo: Repository name (for comment formatting).

    Returns:
        Rejection comment text to post on the issue.
    """
    parent_ref = f"#{parent_issue}"
    if owner and repo:
        parent_ref = f"{owner}/{repo}#{parent_issue}"

    return (
        f"⚠️ **SpecKit trigger rejected** for #{issue_number}: "
        f"This issue's parent ({parent_ref}) "
        f"has not been specked yet.\n\n"
        f"The parent issue must complete its speckit pipeline before child "
        f"issues can be processed. Once the parent's spec is complete, "
        f"re-apply the `speckit` label to this issue.\n\n"
        f"_This comment was posted by the SpecKit hierarchy enforcement system._"
    )


def enforce_parent_specked(
    issue_number: int,
    metadata: HierarchyMetadata,
    specs_root: Path,
    *,
    ancestors: list[int] | None = None,
) -> EnforcementResult:
    """Enforce parent-first processing order.

    Checks whether the parent issue (if any) has been specked. Returns
    an EnforcementResult indicating whether to allow or reject the trigger.

    Args:
        issue_number: The issue being triggered.
        metadata: Hierarchy metadata for the issue.
        specs_root: Root path of the specs directory.
        ancestors: Optional list of ancestor issue numbers.

    Returns:
        EnforcementResult with the enforcement decision.
    """
    # Standalone issues or top-level epics: always allow
    if metadata.level == HierarchyLevel.STANDALONE:
        return EnforcementResult(
            action=EnforcementAction.ALLOW,
            reason="Standalone issue — no parent enforcement needed.",
        )

    if metadata.parent is None:
        return EnforcementResult(
            action=EnforcementAction.ALLOW,
            reason="Top-level issue — no parent to check.",
        )

    # Check if parent has been specked
    is_specked, parent_path = check_parent_specked(
        metadata.parent,
        specs_root,
        ancestors=ancestors,
    )

    if is_specked:
        return EnforcementResult(
            action=EnforcementAction.ALLOW,
            reason=f"Parent #{metadata.parent} has been specked.",
            parent_issue=metadata.parent,
            parent_path=parent_path,
        )

    return EnforcementResult(
        action=EnforcementAction.REJECT,
        reason=f"Parent #{metadata.parent} has not been specked yet.",
        parent_issue=metadata.parent,
    )
