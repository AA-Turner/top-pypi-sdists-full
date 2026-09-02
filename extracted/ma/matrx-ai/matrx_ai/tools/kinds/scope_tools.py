"""Kind for the ``scope_system`` tool result (KIND_TOOL_LEDGER, ``lead-w2c``).

The tool has two result families: the four render actions
(overview/expand_scope/expand_scope_type/expand_context_item) produce ONE
rendered context document (previously returned as a bare top-level string —
reshaped into ``context``, the `math_calculate` precedent: a bare scalar cannot
carry ``__kind``), and `apply` returns the DB function's batch receipt
(organization_id / applied / results).
"""

from __future__ import annotations

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "scope_system_result",
    label="Scope System Result",
    family="scope_system",
    example={"context": "# Organization scopes\n- region: …", "organization_id": None},
    maturity="placeholder",
)
class ScopeSystemResult(KindModel):
    #: render actions — the rendered scope-context tier.
    context: str | None = None
    #: `apply` — the atomic batch receipt from `scope_system_apply`.
    organization_id: str | None = None
    applied: int | None = None
    results: list[dict] | None = None
