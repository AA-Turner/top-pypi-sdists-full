"""GitHub hierarchy detector using the sub-issues API.

Wraps the existing ``GitHubHierarchyDetector`` from
``agentic_devtools.cli.speckit.hierarchy_detector`` and adapts its output
to the ``agentic_devtools.hierarchy`` model types.
"""

from __future__ import annotations

from agentic_devtools.cli.speckit.hierarchy import HierarchyLevel as SpeckitHierarchyLevel
from agentic_devtools.cli.speckit.hierarchy_detector import (
    GitHubHierarchyDetector as SpeckitGitHubDetector,
)
from agentic_devtools.hierarchy.detector import HierarchyDetector
from agentic_devtools.hierarchy.models import (
    ChildInfo,
    HierarchyLevel,
    HierarchyMetadata,
)

# Depth constants matching FR-009
_MAX_HIERARCHY_DEPTH = 3  # Epic(0) → Feature(1) → Task(2)

# Map existing speckit levels to hierarchy package levels
_LEVEL_MAP: dict[SpeckitHierarchyLevel, HierarchyLevel] = {
    SpeckitHierarchyLevel.EPIC: HierarchyLevel.EPIC,
    SpeckitHierarchyLevel.FEATURE: HierarchyLevel.FEATURE,
    SpeckitHierarchyLevel.TASK: HierarchyLevel.TASK,
}


class GitHubHierarchyDetector(HierarchyDetector):
    """GitHub hierarchy detector using the sub-issues API.

    Delegates to the existing speckit GitHubHierarchyDetector for API calls,
    then maps results to the hierarchy package's model types.

    Args:
        owner: GitHub repository owner.
        repo: GitHub repository name.
    """

    def __init__(self, owner: str, repo: str) -> None:
        self.owner = owner
        self.repo = repo
        self._detector = SpeckitGitHubDetector(owner=owner, repo=repo)

    def detect_parent(self, issue_number: int) -> int | None:
        """Detect the parent issue number via GraphQL.

        Returns:
            Parent issue number, or None if no parent in same repo.
        """
        node = self._detector.build_hierarchy_tree(self.owner, self.repo, issue_number)
        if node.parent is not None:
            try:
                return int(node.parent)
            except (ValueError, TypeError):
                pass
        return None

    def detect_children(self, issue_number: int) -> list[tuple[int, str]]:
        """Detect child issues via REST + GraphQL fallback.

        Returns:
            Ordered list of (issue_number, title) tuples.
        """
        node = self._detector.build_hierarchy_tree(self.owner, self.repo, issue_number)
        result: list[tuple[int, str]] = []
        for child in node.children:
            try:
                child_num = int(child.key)
                result.append((child_num, child.title))
            except (ValueError, TypeError):
                continue
        return result

    def classify(self, issue_number: int) -> HierarchyLevel:
        """Classify the issue by delegating to the underlying speckit detector.

        Returns:
            STANDALONE (no parent, no children), or the mapped level from the
            speckit hierarchy detector (EPIC, FEATURE, or TASK). Unknown speckit
            levels default to TASK.
        """
        node = self._detector.build_hierarchy_tree(self.owner, self.repo, issue_number)

        has_parent = node.parent is not None
        has_children = len(node.children) > 0

        if not has_parent and not has_children:
            return HierarchyLevel.STANDALONE

        speckit_level = node.level
        return _LEVEL_MAP.get(speckit_level, HierarchyLevel.TASK)

    def build_metadata(self, issue_number: int) -> HierarchyMetadata:
        """Build full hierarchy metadata for the given issue.

        Combines detection and classification into a complete
        HierarchyMetadata instance.
        """
        node = self._detector.build_hierarchy_tree(self.owner, self.repo, issue_number)

        has_parent = node.parent is not None
        has_children = len(node.children) > 0

        if not has_parent and not has_children:
            level = HierarchyLevel.STANDALONE
        else:
            speckit_level = node.level
            level = _LEVEL_MAP.get(speckit_level, HierarchyLevel.TASK)

        parent_number: int | None = None
        if node.parent is not None:
            try:
                parent_number = int(node.parent)
            except (ValueError, TypeError):
                parent_number = None

        children: list[ChildInfo] = []
        informational_children: list[ChildInfo] = []
        depth_capped = level == HierarchyLevel.TASK and has_children

        for child in node.children:
            try:
                child_num = int(child.key)
                info = ChildInfo(number=child_num, title=child.title, order=child.order)
                if depth_capped:
                    informational_children.append(info)
                else:
                    children.append(info)
            except (ValueError, TypeError):
                continue

        return HierarchyMetadata(
            level=level,
            parent=parent_number,
            children=children,
            informational_children=informational_children,
        )

    def validate_repository_access(self) -> None:
        """Verify that the configured repository is accessible.

        Delegates to the underlying speckit detector so that a missing,
        private, or mis-named repository raises an error before per-issue
        queries begin.

        Raises:
            HierarchyValidationError: If the repository cannot be accessed.
        """
        self._detector.validate_repository_access()
