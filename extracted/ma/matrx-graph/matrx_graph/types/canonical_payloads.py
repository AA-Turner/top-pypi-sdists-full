"""Canonical payload archetypes (Standardized Node Result System, Layer 2).

Recurring payload STRUCTURES are expressed one way system-wide. A node whose
success payload matches an archetype MUST use it (parameterized or subclassed)
instead of a bespoke shape; a node that is *almost* an archetype extends the
payload INSIDE it (subclass the item / subclass the archetype additively) —
it never spawns a new archetype. Keep this set small and closed: add one only
when it demonstrably increases uniformity across many nodes.

The discriminator field is ``archetype`` — deliberately NOT ``kind``, which
is triple-booked on this platform (content_ir.kind_definition slugs, EdgeKind
on the wire, and the Matrx Envelope ``kind`` sentinel that
``matrx_graph.references`` detects generically inside payloads). Each
archetype also has a matching generic kind_definition slug (``items``,
``page``, ``value``, ``operation_result``, ``bulk_result``) so UIs can key
rendering off the out-of-band ``output_kind`` channel; nodes adopting an
archetype should declare that slug as their ``output_kind`` unless a more
specific domain kind exists.

Evolution rule: additive only — add optional fields; never rename, remove,
or repurpose a core field.
"""

from __future__ import annotations

from typing import Any, Generic, Literal, TypeVar

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_graph.types.result import NodeError

ItemT = TypeVar("ItemT")


class BasePayload(BaseModel):
    """Base for every archetype payload. ``extra="forbid"`` — a payload's
    shape is its contract; unknown keys are authoring bugs, not data."""

    model_config = ConfigDict(extra="forbid")


class Items(BasePayload, Generic[ItemT]):
    """Canonical list result — "the node produced N things"."""

    archetype: Literal["items"] = "items"
    items: list[ItemT]
    count: int = Field(
        default=-1,
        description="len(items); auto-derived when not provided.",
    )

    @model_validator(mode="after")
    def _derive_count(self) -> Items[ItemT]:
        if self.count < 0:
            object.__setattr__(self, "count", len(self.items))
        return self


class Page(BasePayload, Generic[ItemT]):
    """Canonical paginated list — a bounded window over a larger result."""

    archetype: Literal["page"] = "page"
    items: list[ItemT]
    total: int
    page: int
    limit: int
    has_more: bool = False


class Value(BasePayload, Generic[ItemT]):
    """Canonical scalar wrapper — "the node computed one value"."""

    archetype: Literal["value"] = Field(
        default="value",
        description="Canonical payload discriminator for a single computed value.",
    )
    value: ItemT = Field(description="The computed value produced by the node.")


class OperationResult(BasePayload):
    """Canonical action acknowledgment — "the node did a thing to a thing".

    ``action`` uses a small stable vocabulary: created | updated | deleted |
    executed | sent | scheduled | noop (extend additively, never rename).
    """

    archetype: Literal["operation_result"] = "operation_result"
    action: str
    id: str | None = None
    message: str | None = None


class BulkItem(BaseModel):
    """One item of a partial-failure bulk operation. Nested ``error`` reuses
    the canonical NodeError (the top-level reserved-field ban applies only to
    the payload root)."""

    model_config = ConfigDict(extra="forbid")

    index: int
    status: Literal["succeeded", "failed"]
    value: Any = None
    item_error: NodeError | None = None


class BulkResult(BasePayload):
    """Canonical partial-failure bulk outcome — "N attempted, some failed".

    For operations a node performs internally over many units (bulk insert,
    multi-file ingest). Distinct from engine-level fan-out
    (``on_item_failure='hole'`` + control.gather), which handles per-NODE
    item failures — a node that loops internally reports per-unit outcomes
    here instead of inventing failures-list shapes.
    """

    archetype: Literal["bulk_result"] = "bulk_result"
    items: list[BulkItem]
    succeeded: int = Field(default=-1, description="auto-derived when not provided")
    failed: int = Field(default=-1, description="auto-derived when not provided")

    @model_validator(mode="after")
    def _derive_counts(self) -> BulkResult:
        if self.succeeded < 0:
            object.__setattr__(
                self, "succeeded", sum(1 for i in self.items if i.status == "succeeded")
            )
        if self.failed < 0:
            object.__setattr__(self, "failed", sum(1 for i in self.items if i.status == "failed"))
        return self


# Archetype slug ↔ model, for guards and kind registration.
ARCHETYPES: dict[str, type[BasePayload]] = {
    "items": Items,
    "page": Page,
    "value": Value,
    "operation_result": OperationResult,
    "bulk_result": BulkResult,
}
