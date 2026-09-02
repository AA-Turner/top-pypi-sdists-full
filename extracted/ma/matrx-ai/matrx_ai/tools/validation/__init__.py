"""Tool drift validation — public API.

The lightweight pieces (the engine, the schema canonicaliser, the finding
types) import only ``pydantic`` and the in-process registry, so they can be used
in tests and tooling without a database. The live-DB orchestration lives in
:mod:`matrx_ai.tools.validation.runner` and is imported lazily by callers that
actually need to hit the database.
"""
from __future__ import annotations

from matrx_ai.tools.validation.engine import (
    DbTool,
    Finding,
    FindingKind,
    Severity,
    ValidationReport,
    validate,
)
from matrx_ai.tools.validation.schema import (
    CanonParam,
    canon_db_params,
    canon_model_params,
)

__all__ = [
    "validate",
    "ValidationReport",
    "Finding",
    "FindingKind",
    "Severity",
    "DbTool",
    "CanonParam",
    "canon_db_params",
    "canon_model_params",
]
