"""Level-aware artifact profiles for hierarchical specs.

Implements FR-008: different hierarchy levels produce different sets
of spec artifacts. Epics exclude tasks.md (children ARE the tasks),
features get the full suite, and tasks inherit parent context.
"""

from __future__ import annotations

import copy

from agentic_devtools.hierarchy.models import ArtifactProfile, HierarchyLevel

# Full artifact set for reference
_ALL_ARTIFACTS = [
    "spec.md",
    "plan.md",
    "tasks.md",
    "research.md",
    "generated/analysis-report.md",
]

# Profile definitions per level
_PROFILES: dict[HierarchyLevel, ArtifactProfile] = {
    HierarchyLevel.EPIC: ArtifactProfile(
        level=HierarchyLevel.EPIC,
        included_artifacts=["spec.md", "plan.md", "research.md", "generated/analysis-report.md"],
        excluded_artifacts=["tasks.md"],
        inherited_context=[],
    ),
    HierarchyLevel.FEATURE: ArtifactProfile(
        level=HierarchyLevel.FEATURE,
        included_artifacts=list(_ALL_ARTIFACTS),
        excluded_artifacts=[],
        inherited_context=[],
    ),
    HierarchyLevel.TASK: ArtifactProfile(
        level=HierarchyLevel.TASK,
        included_artifacts=["tasks.md"],
        excluded_artifacts=["spec.md", "plan.md", "research.md", "generated/analysis-report.md"],
        inherited_context=["spec.md", "plan.md"],
    ),
    HierarchyLevel.STANDALONE: ArtifactProfile(
        level=HierarchyLevel.STANDALONE,
        included_artifacts=list(_ALL_ARTIFACTS),
        excluded_artifacts=[],
        inherited_context=[],
    ),
}


def get_artifact_profile(level: HierarchyLevel) -> ArtifactProfile:
    """Get the artifact profile for a hierarchy level.

    Args:
        level: The hierarchy level to get the profile for.

    Returns:
        ArtifactProfile defining included/excluded artifacts and inherited context.

    Raises:
        ValueError: If the level is not a valid HierarchyLevel.
    """
    if not isinstance(level, HierarchyLevel):
        msg = f"Expected HierarchyLevel, got {type(level).__name__}"
        raise ValueError(msg)

    return copy.deepcopy(_PROFILES[level])
