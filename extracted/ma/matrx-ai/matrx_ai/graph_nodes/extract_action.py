"""``ai.extract`` — intelligent parsing and validation of text via LLM.

This node is the 'incredibly powerful analyzation node'. It inspects any unstructured text
(like a previous LLM's raw output), extracts exactly what you need based on instructions,
and returns a structured, predictable payload that downstream nodes can natively branch on.
"""

from __future__ import annotations

import json

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.mandates import (
    WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    step_metadata,
)


class ExtractInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    # REQUIRED, like ai.llm.chat. This field used to default to "gpt-4o-mini":
    # an author (or the Masterwork Conductor, which reads this schema as the
    # truth) copied the default, the provider call produced zero tokens, and
    # the node reported "no output text" instead of the real cause
    # (2026-09-10; the model row exists but is not primary, and the call still
    # failed — the executor's own error is what must surface). A schema default
    # that names a model is a lie with a shelf life — the picker is the source.
    model: str = Field(
        min_length=1,
        description="Model to use for extraction — pick one from the live catalog.",
        json_schema_extra=field_extras(widget="model_picker"),
    )
    text: str = Field(
        min_length=1,
        description="The unstructured text to analyze/extract from (e.g., previous LLM output).",
        json_schema_extra=field_extras(widget="textarea"),
    )
    instruction: str = Field(
        min_length=1,
        description="Clear instructions on what to extract (e.g. 'Extract the final math answer as an integer').",
    )
    # Author-supplied JSON Schema — arbitrary JSON by definition.
    schema_definition: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Optional JSON Schema defining the exact structure to extract. If empty, the LLM will just output a JSON object matching the instruction.",
    )


class ExtractOutput(BaseModel):
    # CLOSED on purpose (Arman's ruling, 2026-08-21): the model-authored keys
    # live in ``extracted_data`` and NOWHERE else. This node used to ALSO
    # splice those same keys onto the root (``**data``) so an author could
    # write ``{{node.vendor}}`` instead of ``{{node.extracted_data.vendor}}``.
    # That was duplication that broke the kind contract — the registered kind
    # forbids undeclared fields, so every real run recorded
    # ``output_kind_ok=false``, and it would have become a hard execution
    # failure the day workflow_io enforcement turns on. Undeclared keys never
    # live at the root; they live in a declared map. Nothing is lost: the whole
    # object is, and always was, in ``extracted_data``.
    # Failure semantics live in the NodeResult envelope — never as payload flags.
    model_config = ConfigDict(extra="forbid")

    # Model-authored extraction — genuinely dynamic JSON, held in ONE declared
    # field whose value type says so.
    extracted_data: dict[str, JsonValue] = Field(default_factory=dict)
    raw_response: str


@register_node(
    name="ai.extract",
    display_name="Extract with AI",
    description="Use AI to pull structured information out of text.",
    category=NodeCategory.LLM,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ExtractInput,
    output_schema=ExtractOutput,
    output_kind="ai_extract_result",
    icon="search",
    tags=("ai", "extract", "analyze", "parse"),
)
async def ai_extract(ctx: NodeExecutionContext, inputs: ExtractInput) -> NodeResult[ExtractOutput]:
    from matrx_ai.catalog.host_catalog import get_model_catalog
    from matrx_ai.config import UnifiedConfig
    from matrx_ai.graph_nodes.shared import _extract_usage, normalize_completed_result
    from matrx_ai.orchestrator.executor import execute_ai_request

    # Pre-flight: an unknown model is a NAMED failure, never an empty answer.
    catalog = get_model_catalog()
    if catalog is not None and await catalog.get_model(inputs.model) is None:
        return failure(
            "model_unknown",
            f"ai.extract: model '{inputs.model}' is not in the model catalog. "
            "Pick a model from the model picker (the catalog is the only source of model names).",
            details={"model": inputs.model},
        )

    # Force the LLM to only output JSON
    system_prompt = f"You are a strict data extraction analyzer. \n{inputs.instruction}\n"
    if inputs.schema_definition:
        system_prompt += f"You MUST output valid JSON exactly matching this schema:\n{json.dumps(inputs.schema_definition)}\n"
    else:
        system_prompt += "You MUST output a valid JSON object. Do not wrap it in markdown block quotes. Just the raw JSON object."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": inputs.text},
    ]

    # No forced temperature: a node has no business hard-coding a sampling
    # opinion, and several catalog models (the Claude 5 family) REJECT the
    # parameter outright — 2026-09-10 every Opus 5 extract step died with
    # "`temperature` is deprecated for this model". The offering's catalog
    # controls own which parameters travel; the node sends only what it needs.
    overrides = {
        "model": inputs.model,
        "messages": messages,
    }

    if inputs.schema_definition:
        # Use native structured outputs for flawless extraction
        overrides["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": "extraction",
                "schema": inputs.schema_definition,
                "strict": True,
            },
        }

    config = UnifiedConfig.from_dict(overrides)

    completed = await execute_ai_request(
        config,
        max_iterations=1,
        max_retries_per_iteration=2,
        metadata=step_metadata(None, spec_type="ai.extract"),
        mandate_key=WORKFLOW_STEP_INTELLIGENCE_MANDATE,
    )

    # Cost convention: this is a PAID call — every failure carries the billed
    # usage under details["usage"] so the scheduler's cost settlement records
    # the spend (category=LLM gates the settlement).
    usage = _extract_usage(getattr(completed, "total_usage", None)).model_dump(mode="json")

    # A failed turn (provider error, routing error, loop guard) fails the node
    # with the orchestrator's own reason — never "no output text to parse".
    normalized = normalize_completed_result(completed)
    if normalized.status == "error":
        return normalized  # type: ignore[return-value]

    final_text = completed.request.config.get_last_output()
    if not final_text:
        return failure(
            "extract_parse_failed",
            "ai.extract: the model returned no output text to parse.",
            details={"raw_response": "", "usage": usage},
        )

    # Strip markdown code blocks if the LLM hallucinated them despite instructions
    clean_text = final_text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.startswith("```"):
        clean_text = clean_text[3:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    clean_text = clean_text.strip()

    try:
        data = json.loads(clean_text)
    except json.JSONDecodeError as e:
        # A node that cannot produce its artifact FAILS — never a payload with
        # a false flag. The raw snippet lets an ERROR-edge handler (or a human)
        # see what the model actually said.
        return failure(
            "extract_parse_failed",
            f"ai.extract: model output is not valid JSON ({e}).",
            details={"raw_response": final_text[:2000], "usage": usage},
        )

    if not isinstance(data, dict):
        return failure(
            "extract_parse_failed",
            f"ai.extract: model output parsed to {type(data).__name__}, expected a JSON object.",
            details={"raw_response": final_text[:2000], "usage": usage},
        )

    # The extracted object travels in its declared field. Address it as
    # ``extracted_data.<key>`` downstream.
    return success(ExtractOutput(raw_response=final_text, extracted_data=data))
