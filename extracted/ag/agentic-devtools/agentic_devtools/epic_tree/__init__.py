"""Public API for epic-tree schema validation, models, and loading.

This package provides functions and types for validating epic-tree JSON
documents against the versioned JSON Schema (Draft 2019-09), typed Pydantic
models for the document structure, and a loader that parses JSON files into
those models with aggregated validation errors.
"""

from .config import EpicTreeConfig, load_epic_tree_config
from .dependencies import (
    build_combined_graph,
    build_dependency_graph,
    build_hierarchy_edges,
    detect_cycles,
    topological_sort,
    topological_sort_graph,
)
from .errors import (
    CATEGORY_CYCLE_DETECTED,
    CATEGORY_DEPTH_EXCEEDED,
    CATEGORY_DISALLOWED_ISSUE_TYPE,
    CATEGORY_DISALLOWED_LABEL,
    CATEGORY_DUPLICATE_REF,
    CATEGORY_INVALID_REF_FORMAT,
    CATEGORY_MISSING_BODY_SECTION,
    CATEGORY_UNRESOLVED_REFERENCE,
    ConfigError,
    EpicTreeLoadError,
    EpicTreeValidationError,
    UnresolvedRefError,
    ValidationReport,
    ValidationReportEntry,
    VersionMismatchError,
)
from .loader import load_epic_tree
from .models import EpicNode, EpicTree, FeatureNode, IssueNode, SubtaskNode
from .normalization_models import (
    EpicTreeHierarchyLevel,
    NormalizationResult,
    NormalizationWarning,
    derive_epic_tree_hierarchy_level,
)
from .normalizer import normalize_tree
from .ordering import creation_sequence, get_sibling_position, resolve_sibling_order
from .schema import SCHEMA_PATH, load_schema
from .validator import check_schema_version, validate_epic_tree

__all__ = [
    "CATEGORY_CYCLE_DETECTED",
    "CATEGORY_DEPTH_EXCEEDED",
    "CATEGORY_DISALLOWED_ISSUE_TYPE",
    "CATEGORY_DISALLOWED_LABEL",
    "CATEGORY_DUPLICATE_REF",
    "CATEGORY_INVALID_REF_FORMAT",
    "CATEGORY_MISSING_BODY_SECTION",
    "CATEGORY_UNRESOLVED_REFERENCE",
    "ConfigError",
    "EpicNode",
    "EpicTree",
    "EpicTreeConfig",
    "EpicTreeHierarchyLevel",
    "EpicTreeLoadError",
    "EpicTreeValidationError",
    "FeatureNode",
    "IssueNode",
    "NormalizationResult",
    "NormalizationWarning",
    "SCHEMA_PATH",
    "SubtaskNode",
    "UnresolvedRefError",
    "ValidationReport",
    "ValidationReportEntry",
    "VersionMismatchError",
    "build_combined_graph",
    "build_dependency_graph",
    "build_hierarchy_edges",
    "check_schema_version",
    "creation_sequence",
    "derive_epic_tree_hierarchy_level",
    "detect_cycles",
    "get_sibling_position",
    "load_epic_tree",
    "load_epic_tree_config",
    "load_schema",
    "normalize_tree",
    "resolve_sibling_order",
    "topological_sort",
    "topological_sort_graph",
    "validate_epic_tree",
]
