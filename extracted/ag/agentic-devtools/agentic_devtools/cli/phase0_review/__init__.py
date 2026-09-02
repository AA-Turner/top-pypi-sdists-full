"""Public API for the Phase 0 factual-review package."""

from agentic_devtools.cli.phase0_review.async_commands import phase0_review_async
from agentic_devtools.cli.phase0_review.commands import (
    inject_phase0_checklist,
    phase0_review_command,
    run_review,
)
from agentic_devtools.cli.phase0_review.comparison import compare_content
from agentic_devtools.cli.phase0_review.contract import (
    ContractResult,
    load_contract,
    validate_integrity,
    validate_paths,
    validate_schema,
)
from agentic_devtools.cli.phase0_review.drift_check import run_drift_check
from agentic_devtools.cli.phase0_review.helpers import (
    StructuralResult,
    frontmatter_validate,
    structural_compare,
)
from agentic_devtools.cli.phase0_review.report import Finding, render_report

__all__ = [
    "ContractResult",
    "Finding",
    "StructuralResult",
    "compare_content",
    "frontmatter_validate",
    "inject_phase0_checklist",
    "load_contract",
    "phase0_review_async",
    "phase0_review_command",
    "render_report",
    "run_drift_check",
    "run_review",
    "structural_compare",
    "validate_integrity",
    "validate_paths",
    "validate_schema",
]
