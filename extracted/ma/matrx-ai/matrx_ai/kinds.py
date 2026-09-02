"""Shape system — bind an LLM's structured output to a platform kind.

``response_format_for_kind(slug)`` resolves a ``content_ir.kind_definition``
slug through the shared kind catalog (``matrx_graph.kinds`` — matrx-ai depends
on matrx-graph, never the reverse) and returns a ``ResponseFormatJsonSchema``
built from the kind's ``emitted_json_schema``. One line binds an agent to a
Shape:

    config.response_format = await response_format_for_kind("flashcard_set")

The kind is the CANONICAL declaration: the same schema the frontend renders
against and the workflow scheduler validates against, so the model's output,
the validator, and the renderer can never drift.

The kind's emitted schema is run through the ``matrx_ai.schema`` lint gate and
its ``portable_schema`` is used (additionalProperties:false + all-required on
every object node, ``__kind`` re-hoisted first), so the binding satisfies OpenAI
strict + Anthropic + Gemini. ``$defs`` are deliberately LEFT IN PLACE — an
earlier version of this note claimed they were inlined; they are not, and
inlining them would not help, because providers expand ``$ref`` themselves
(measured 2026-08-24, ``matrx_ai.schema.grammar_budget``).

Failure posture mirrors the catalog — unknown slug / missing schema returns
``None`` after the catalog's loud log (platform defect, not user input); a
schema the gate cannot make portable also returns ``None`` LOUDLY (an
unenforceable response_format silently degrades to prose, which is worse than
no binding).
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_graph.content_ir.envelope import KIND_KEY
from matrx_graph.contract_kinds import (
    ContractDefinition,
    ContractDirection,
    ContractFamily,
    contract_definition,
)
from matrx_graph.kinds import get_kind

from matrx_ai.config.response_format import (
    OutputSchemaEnvelope,
    ResponseFormatJsonSchema,
)
from matrx_ai.schema.lint import lint_output_schema

logger = logging.getLogger(__name__)


def agent_output_contract(
    agent_id: str,
    output_schema: dict[str, Any],
    *,
    version: int = 1,
    label: str | None = None,
) -> ContractDefinition:
    """Build the stable data-only kind for one agent's structured output."""
    schema = output_schema.get("schema")
    if not isinstance(schema, dict):
        schema = output_schema
    return contract_definition(
        family=ContractFamily.AGENT_IO,
        source_name=agent_id,
        direction=ContractDirection.OUTPUT,
        json_schema=schema,
        label=label or f"Agent {agent_id} output",
        version=version,
        source_id=agent_id,
    )


# Kinds that name a FORMAT, not a structure. Every one of them is a registered
# row, and every one of them is unbindable by construction: their schema is a
# bare scalar (``text``, ``string``), the "any value" empty schema (``json``),
# or the run ENVELOPE rather than the answer (``agent_result``). Asking
# ``response_format_for_kind`` for one is not a defect to scream about — it is
# a declaration that says "free-form", so callers that bind opportunistically
# (a Mandate's declared output kind, a workflow node's declared output kind)
# check membership FIRST and skip quietly. Everything else that fails to bind
# still screams, because it is a kind that SHOULD have been enforceable.
GENERIC_KINDS: frozenset[str] = frozenset(
    {"json", "text", "string", "string_list", "markdown", "any", "agent_result"}
)


def is_bindable_kind(slug: str | None) -> bool:
    """Whether ``slug`` names a structure an LLM can be bound to answer in.

    False for a missing slug and for every :data:`GENERIC_KINDS` member. True
    is a claim that the binding is WORTH attempting, not that it will succeed —
    ``response_format_for_kind`` still owns the portability verdict and still
    screams when a structural kind cannot be made provider-portable.
    """
    return bool(slug) and slug not in GENERIC_KINDS


async def response_format_for_kind(slug: str) -> ResponseFormatJsonSchema | None:
    """Build a json_schema response_format from a registered kind, or None."""
    entry = await get_kind(slug)
    if entry is None or entry.json_schema is None:
        # get_kind already logged the platform defect (unregistered / no schema).
        # NOTE: {} is a REGISTERED schema ("any value") — it falls through to
        # the portable gate below and declines there, loudly.
        return None
    report = lint_output_schema(entry.json_schema)
    schema = report.portable_schema if report.portable_schema is not None else None
    if schema is None and report.ok:
        schema = entry.json_schema
    if schema is None:
        logger.error(
            "response_format_for_kind: kind '%s' emitted_json_schema cannot be "
            "made provider-portable — binding SKIPPED. Fix the kind's schema. "
            "Findings: %s",
            slug,
            [
                f"{f.provider} {f.path}: {f.message}"
                for f in report.findings
                if f.severity == "error"
            ],
        )
        return None
    return ResponseFormatJsonSchema(
        type="json_schema",
        json_schema=OutputSchemaEnvelope.model_validate(
            {"name": slug, "schema": discriminator_first(schema, slug), "strict": True}
        ),
    )


def discriminator_first(schema: dict[str, Any], slug: str) -> dict[str, Any]:
    """Return ``schema`` with ``__kind`` declared as its FIRST root property.

    WHY ORDER MATTERS, and why this is a WIRE concern and not a registry one.

    A bound agent streams an UNFENCED JSON document: no fence, no XML tag,
    nothing for a detector to recognize it by except the document itself. The
    ONE thing that can type it early is its own ``__kind`` — and only if
    ``__kind`` arrives FIRST, because the recognizer reads the first key and
    nothing else (``block_detector.root_kind_declaration``). A ``__kind`` at
    the end of the object announces the kind after the user has already
    watched the raw JSON accumulate, which is exactly the defect Arman
    reported on 2026-08-21.

    The registry cannot carry that order: ``emitted_json_schema`` is a
    ``jsonb`` column and Postgres normalises object key order on write, so
    property order is DESTROYED at rest no matter what is stored. Order is
    therefore reconstructed here, at the wire, beside the other wire
    adaptation this binder already performs (portable/strict) — the same
    doctrine the kind_sdk strict-schema decision settled: the registry stays
    canonical JSON Schema and the wire adapts it.

    Order is necessary and NOT sufficient: providers are free to emit keys in
    any order, so the agent's own instructions must carry an EXAMPLE whose
    first key is ``__kind`` (Arman, 2026-08-23). That example lives with the
    agent in the database, where an agent's definition belongs; this function
    makes the schema agree with it rather than contradict it.

    Non-object roots (root-form kinds — a scalar or array root) are returned
    untouched: there is no first key to be first.
    """
    if not isinstance(schema, dict) or schema.get("type") != "object":
        return schema
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        return schema
    declared = properties.get(KIND_KEY)
    discriminator: dict[str, Any] = {
        "type": "string",
        "const": slug,
        "description": (
            f"Always the literal '{slug}'. Emit this key FIRST, before every "
            "other key, so the platform can recognize and start rendering "
            "this answer while it is still streaming."
        ),
    }
    if isinstance(declared, dict):
        # Keep whatever the registered schema said (title, examples), but the
        # const and the description are this wire's business.
        discriminator = {**declared, **discriminator}
    reordered = {KIND_KEY: discriminator}
    for key, value in properties.items():
        if key != KIND_KEY:
            reordered[key] = value
    required = [KIND_KEY] + [
        key for key in schema.get("required") or [] if key != KIND_KEY
    ]
    return {**schema, "properties": reordered, "required": required}
