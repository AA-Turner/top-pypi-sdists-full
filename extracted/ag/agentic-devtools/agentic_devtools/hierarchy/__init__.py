"""Hierarchy infrastructure for SpecKit nested spec management.

Provides core models, detection ABCs, metadata I/O, parent-first enforcement,
nested filesystem path resolution, cascade triggering, and level-aware artifact
profiles for hierarchical spec nesting.
"""

from agentic_devtools.hierarchy.artifact_profiles import get_artifact_profile
from agentic_devtools.hierarchy.cascade import CascadeProcessor, CascadeResult
from agentic_devtools.hierarchy.detector import HierarchyDetector
from agentic_devtools.hierarchy.enforcement import (
    EnforcementResult,
    check_parent_specked,
    enforce_parent_specked,
    reject_trigger,
)
from agentic_devtools.hierarchy.jira_detector import JiraHierarchyDetector
from agentic_devtools.hierarchy.metadata_io import read_hierarchy_yml, write_hierarchy_yml
from agentic_devtools.hierarchy.models import (
    ArtifactProfile,
    CascadeDirection,
    CascadeEvent,
    HierarchyLevel,
    HierarchyMetadata,
)
from agentic_devtools.hierarchy.path_resolver import resolve_spec_path

__all__ = [
    "ArtifactProfile",
    "CascadeDirection",
    "CascadeEvent",
    "CascadeProcessor",
    "CascadeResult",
    "EnforcementResult",
    "HierarchyDetector",
    "HierarchyLevel",
    "HierarchyMetadata",
    "JiraHierarchyDetector",
    "check_parent_specked",
    "enforce_parent_specked",
    "get_artifact_profile",
    "read_hierarchy_yml",
    "reject_trigger",
    "resolve_spec_path",
    "write_hierarchy_yml",
]
