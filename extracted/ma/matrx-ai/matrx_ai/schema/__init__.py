"""Structured-output schema rules + provider-aware linting.

Light, dependency-free (no provider SDK, no DB config) so it can run anywhere —
the Agent Service schema gate, the agent_factory build path, or a standalone
check. The recursive ``additionalProperties:false`` enforcement here is the
single source of truth the provider translators delegate to.
"""

from matrx_ai.schema.grammar_budget import (
    GRAMMAR_TOO_LARGE_MARKER,
    binds_structured_output,
    is_grammar_too_large,
)
from matrx_ai.schema.lint import (
    ALL_PROVIDERS,
    Provider,
    SchemaFinding,
    SchemaLintReport,
    check_sample_against_schema,
    lint_output_schema,
)
from matrx_ai.schema.rules import (
    enforce_additional_properties_false,
    enforce_all_required,
    is_object_node,
    is_root_object,
)

__all__ = [
    "ALL_PROVIDERS",
    "GRAMMAR_TOO_LARGE_MARKER",
    "binds_structured_output",
    "Provider",
    "SchemaFinding",
    "SchemaLintReport",
    "check_sample_against_schema",
    "enforce_additional_properties_false",
    "enforce_all_required",
    "is_grammar_too_large",
    "is_object_node",
    "is_root_object",
    "lint_output_schema",
]
