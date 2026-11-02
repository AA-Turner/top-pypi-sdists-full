"""``data.parse_json`` + ``data.stringify_json`` — JSON I/O primitives.

Needed because a surprising number of HTTP endpoints serve JSON as
``text/plain``, and LLM outputs are often JSON-in-a-string. Without these,
every workflow ends up writing the same ``data.transform`` expression with a
``json.loads`` proxy (which the sandbox doesn't allow anyway).

``lenient`` reads an AI's reply: the JSON inside a fence, after prose, or with a small syntax
slip, through the host's ONE LLM-JSON funnel (``matrx_graph.llm_json``). When it had to repair
anything the step says so in its run log — a reply that needed reading never passes as clean.

Node Result System: parse failure is a node Failure (``code='parse_failed'``)
— branch-on-parse-failure is an ERROR edge, never a payload boolean. The
success payload is the canonical ``Value`` archetype (``value`` carries the
parsed JSON). Stringify is strict — non-serializable input is a programming
error, not a runtime condition to route around.
"""

from __future__ import annotations

import json
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.llm_json import LlmJsonExtractorMissing, extract_llm_json

from matrx_graph.types.canonical_payloads import Value
from matrx_graph.content_ir.well_known import TextValue
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras

# ---------------------------------------------------------------------------
# parse_json
# ---------------------------------------------------------------------------


class ParseJsonInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(description="JSON-encoded string to parse.")


class ParseJsonConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    lenient: bool = Field(
        default=False,
        description="Read an AI's reply: find the JSON inside a code fence or prose, and "
        "repair small syntax slips. Off = the text must be exactly JSON.",
        json_schema_extra=field_extras(widget="toggle"),
    )
    schema_definition: dict[str, JsonValue] | None = Field(
        default=None,
        description="Lenient only: the JSON Schema the value must fit (its type and required "
        "keys pick the right block when the reply holds several).",
        json_schema_extra=field_extras(widget="json"),
    )


def _strict(text: str) -> tuple[bool, JsonValue]:
    try:
        return True, json.loads(text)
    except json.JSONDecodeError:
        return False, None


class ParseJsonExecutor:
    """Parse JSON text. A parse failure is a node Failure (route it with an
    ERROR edge or let it park) — never a silent ok=false payload."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.parse_json",
        category=NodeCategory.DATA,
        display_name="Text to Data",
        description="Turn data stored as text into real, usable data.",
        input_schema=ParseJsonInput,
        input_kind="text",
        output_schema=Value[JsonValue],
        config_schema=ParseJsonConfig,
        output_kind="value",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="braces",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ParseJsonInput,
        config: ParseJsonConfig,
    ) -> NodeResult[Value[JsonValue]]:
        if not config.lenient:
            try:
                return success(Value[JsonValue](value=json.loads(inputs.text)))
            except json.JSONDecodeError as e:
                return failure("parse_failed", f"{type(e).__name__}: {e}")

        schema = config.schema_definition
        clean, value = _strict(inputs.text.strip())
        if clean and schema is None:
            return success(Value[JsonValue](value=value))
        try:
            found = extract_llm_json(inputs.text, schema)
        except LlmJsonExtractorMissing as e:
            return failure("parse_unavailable", str(e))
        if not found.ok:
            return failure("parse_failed", f"No JSON found in the text: {found.reason}")
        if not (clean and found.value == value):
            picked = (
                f" It held {found.candidates} JSON blocks; the first that fits was used."
                if found.candidates > 1
                else ""
            )
            await ctx.warn(
                "parse_json.repaired",
                "The text was not plain JSON, so its JSON was read out of it (a code fence, "
                "surrounding prose or a syntax slip)." + picked,
                payload={"text_head": inputs.text[:300]},
            )
        return success(Value[JsonValue](value=found.value))


# ---------------------------------------------------------------------------
# stringify_json
# ---------------------------------------------------------------------------


class StringifyJsonInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    value: JsonValue = Field(description="Any JSON-serializable value.")


class StringifyJsonConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    indent: int | None = Field(
        default=None,
        ge=0,
        le=8,
        description="Pretty-print indent. None = compact single-line output.",
    )
    sort_keys: bool = Field(
        default=False, description="Sort object keys alphabetically in the output."
    )
    ascii_only: bool = Field(
        default=False,
        description=(
            "Write every non-ASCII letter as a \\u escape (\"Über\" becomes \"\\u00dcber\"). "
            "Off: letters are written as themselves."
        ),
    )


#: ``data.stringify_json`` answers with the well-known ``text`` kind itself
#: (§4.4: reuse, never re-mint) — the same one-shape alias ``text.join`` uses.
StringifyJsonOutput = TextValue


class StringifyJsonExecutor:
    """Serialize a JSON-able value to a string. Strict — fails on bad input."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.stringify_json",
        category=NodeCategory.DATA,
        display_name="Data to Text",
        description="Turn data into plain text so it can be stored or sent.",
        input_schema=StringifyJsonInput,
        input_kind="value",
        output_schema=StringifyJsonOutput,
        config_schema=StringifyJsonConfig,
        # `text` since its 2026-08-21 object re-seed ({"text": str}) — the exact
        # shape of StringifyJsonOutput (see text.join for the same repoint).
        output_kind="text",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="braces",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: StringifyJsonInput,
        config: StringifyJsonConfig,
    ) -> NodeResult[StringifyJsonOutput]:
        _ = ctx
        try:
            # Real Unicode by default (2026-10-27): escaped output hid É/Ü from a later
            # casefold or search; ``ascii_only`` keeps the escaped form when a consumer needs it.
            text = json.dumps(
                inputs.value,
                indent=config.indent,
                sort_keys=config.sort_keys,
                ensure_ascii=config.ascii_only,
            )
        except (TypeError, ValueError) as e:
            # Strict by design — non-serializable input is an authoring error,
            # surfaced as a structured node Failure with a stable code.
            return failure("stringify_failed", f"{type(e).__name__}: {e}")
        return success(StringifyJsonOutput(text=text))
