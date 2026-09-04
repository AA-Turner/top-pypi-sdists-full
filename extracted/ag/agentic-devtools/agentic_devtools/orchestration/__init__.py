"""LangGraph orchestration module for AGDT.

This package provides the foundational LangGraph integration for AGDT's
workflow orchestration, including state schemas, graph builders, checkpoint
configuration, and a pilot workflow implementation.

This is ADR-013 Phase 1: LangGraph manages orchestration checkpoint state
while the existing JSON-based CLI state continues to operate in parallel.
"""

from .checkpointing import get_checkpointer
from .graph_builder import build_work_on_issue_graph
from .pilot_workflow import error_handler_node, get_mermaid_diagram
from .state_schema import WorkOnIssueEvent, WorkOnIssueState
from .trio_config import (
    AdjudicationPolicy,
    AdjudicationResult,
    Phase,
    PointVerdict,
    ReviewCap,
    ReviewCapViolation,
    RoleAssignment,
    RoleDiversityViolation,
    RotationPolicy,
    RoundAssignments,
    TrioConfig,
    TrioConfigValidationError,
    load_trio_config,
    parse_adjudication_response,
    resolve_round_assignments,
    validate_review_budget,
    validate_round_assignments,
    validate_trio_config,
)

__all__ = [
    "WorkOnIssueEvent",
    "WorkOnIssueState",
    "build_work_on_issue_graph",
    "error_handler_node",
    "get_checkpointer",
    "get_mermaid_diagram",
    "AdjudicationPolicy",
    "AdjudicationResult",
    "Phase",
    "PointVerdict",
    "RoundAssignments",
    "ReviewCap",
    "ReviewCapViolation",
    "RoleAssignment",
    "RoleDiversityViolation",
    "RotationPolicy",
    "TrioConfig",
    "TrioConfigValidationError",
    "load_trio_config",
    "parse_adjudication_response",
    "resolve_round_assignments",
    "validate_review_budget",
    "validate_round_assignments",
    "validate_trio_config",
]
