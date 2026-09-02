"""Built-in NamedAgents that ship with matrx-ai.

These are reusable, hardcoded-in-code agents — defined entirely as
``NamedAgent`` subclasses with ``InlineAgentSource`` configurations — so
any host application can call them without first registering anything in
the database. Each one solves a small, generic problem cleanly enough
that it earns a permanent home in the library.

Current residents:

  * ``SchemaCoerceAgent`` — strict text-to-Pydantic-schema coercion. Pair
    with ``run_agent``'s parse-failure path: when the primary attempt to
    validate a model response fails, hand the raw text + your target
    schema to ``SchemaCoerceAgent.coerce()`` and either get a clean
    typed instance back or a structured "data is genuinely missing"
    error envelope. Never hallucinates fillers.
"""

from __future__ import annotations

from matrx_ai.agents.library.schema_coerce import (
    SchemaCoerceAgent,
    SchemaCoerceErrorResponse,
    SchemaCoerceInputs,
    SchemaCoerceResult,
)

__all__ = [
    "SchemaCoerceAgent",
    "SchemaCoerceErrorResponse",
    "SchemaCoerceInputs",
    "SchemaCoerceResult",
]
