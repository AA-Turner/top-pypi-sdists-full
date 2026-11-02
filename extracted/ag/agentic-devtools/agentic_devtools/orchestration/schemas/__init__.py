"""Structured LLM output schemas for the orchestration engine.

This package provides Pydantic v2 models for all LLM response types used
across both the PR review and work-on-issue workflows. It includes:

- Top-level output types organized into three domain subpackages
- JSON Schema export for LLM structured output mode (OpenAI/Anthropic)
- Validation utilities with fallback parsing for common LLM deviations
- Example fixture factories for testing

Public API:
    Models:
        - ConfidenceScore (annotated float type)
        - EscalationReason, StopCondition (shared)
        - CodeSuggestion, FileReviewFinding, FileReviewResult,
          PerFileReviewError, ReviewDecision, ReviewSummary (review)
        - ImplementationPlan, PlanTask, TaskDependency, RiskAssessment,
          ChecklistItem, TestFailureDiagnosis, RepairAction,
          ImplementationSummary, QualityGateResult (work-on-issue)

    Enums:
        - Severity, Verdict, EscalationCategory, QualityGateName

    Utilities:
        - validate_llm_output() — parse and validate raw LLM responses
        - export_json_schema() — export JSON Schema for structured output
        - SchemaValidationError — raised on validation failure
"""

from ._confidence import ConfidenceScore
from ._enums import EscalationCategory, QualityGateName, Severity, Verdict
from ._export import export_json_schema
from ._validation import SchemaValidationError, validate_llm_output
from .review import (
    CodeSuggestion,
    FileReviewFinding,
    FileReviewResult,
    PerFileReviewError,
    ReviewDecision,
    ReviewSummary,
)
from .shared import EscalationReason, StopCondition
from .work_on_issue import (
    ChecklistItem,
    ImplementationPlan,
    ImplementationSummary,
    PlanTask,
    QualityGateResult,
    RepairAction,
    RiskAssessment,
    TaskDependency,
    TestFailureDiagnosis,
)

__all__ = [
    # Enums
    "EscalationCategory",
    "QualityGateName",
    "Severity",
    "Verdict",
    # Shared
    "ConfidenceScore",
    "EscalationReason",
    "StopCondition",
    # Review
    "CodeSuggestion",
    "FileReviewFinding",
    "FileReviewResult",
    "PerFileReviewError",
    "ReviewDecision",
    "ReviewSummary",
    # Work-on-Issue
    "ChecklistItem",
    "ImplementationPlan",
    "ImplementationSummary",
    "PlanTask",
    "QualityGateResult",
    "RepairAction",
    "RiskAssessment",
    "TaskDependency",
    "TestFailureDiagnosis",
    # Utilities
    "SchemaValidationError",
    "export_json_schema",
    "validate_llm_output",
]
