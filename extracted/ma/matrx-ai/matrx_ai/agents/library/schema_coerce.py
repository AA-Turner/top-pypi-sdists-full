"""SchemaCoerceAgent — strict text-to-Pydantic-schema coercion primitive.

The canonical example of an inline (hardcoded) ``NamedAgent``. Lives in
the library because every consumer can use it: when something
upstream produces output that *should* fit a schema but doesn't (a
malformed JSON, a paragraph of prose, a partially-fenced block, an
extracted PDF chunk), hand the raw text plus your target Pydantic class
to :meth:`SchemaCoerceAgent.coerce` and either:

  * Get a typed instance of your schema back (when the data is genuinely
    present in the input), OR
  * Get a structured ``SchemaCoerceErrorResponse`` describing exactly
    what's missing — the agent is forbidden from inventing values.

Design notes
------------

* The agent's class-level ``Output`` is left ``None`` because the output
  schema is dynamic — it depends on what the caller passes. Auto-parsing
  via ``run_agent``'s ``json_schema`` is therefore disabled for this
  agent. The :meth:`coerce` classmethod owns the schema-injection +
  parse path explicitly.
* The error envelope is signalled by a sentinel key (``_coerce_error``)
  the agent is instructed to use. That avoids any ambiguity between "a
  schema with a field literally called error" and "the rescue path".
* The system prompt is intentionally strict about hallucination — every
  value in a success response must be traceable to the input text. That
  is what differentiates this agent from a free-form rewriter.
"""

from __future__ import annotations

import json
from typing import Any, Generic, TypeVar

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from matrx_ai.agents.executor import extract_json_block
from matrx_ai.agents.named import InlineAgentSource, NamedAgent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.config.usage_config import AggregatedUsage, TokenUsage

ParsedT = TypeVar("ParsedT", bound=BaseModel)


# ---------------------------------------------------------------------------
# Result types
# ---------------------------------------------------------------------------


class SchemaCoerceErrorResponse(BaseModel):
    """Structured "I cannot produce the requested schema" response.

    The agent emits a JSON object with the shape::

        {
          "_coerce_error": "<concise reason>",
          "_missing_fields": ["dotted.path", ...],
          "_notes": "<optional clarifying detail>"
        }

    when the input text genuinely lacks data needed by the target schema.
    Hallucinated fillers are forbidden by the system prompt.
    """

    error: str = Field(alias="_coerce_error")
    missing_fields: list[str] = Field(default_factory=list, alias="_missing_fields")
    notes: str = Field(default="", alias="_notes")

    model_config = ConfigDict(populate_by_name=True, extra="ignore")


class SchemaCoerceResult(BaseModel, Generic[ParsedT]):
    """Outcome of :meth:`SchemaCoerceAgent.coerce`.

    The caller inspects the three optional payload fields in priority
    order:

    1. ``parsed`` is set    -> success, use it
    2. ``coerce_error`` is set -> the agent reported genuine missing data
    3. ``parse_error`` is set  -> the model's response was unusable
                                  (neither a valid schema instance nor a
                                  valid error envelope). The raw output
                                  has already been printed in red via
                                  vcprint when this happens.

    All three slots are mutually exclusive on the success path.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    success: bool
    raw_output: str = ""
    parsed: ParsedT | None = None
    coerce_error: SchemaCoerceErrorResponse | None = None
    parse_error: str | None = None
    usage: dict[str, Any] = Field(default_factory=dict)
    usage_aggregated: AggregatedUsage | None = None
    usage_history: list[TokenUsage] = Field(default_factory=list)
    model_id: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Agent definition
# ---------------------------------------------------------------------------


_DEFAULT_MODEL = "claude-haiku-4-5"

_SYSTEM_PROMPT = """You are a strict data coercion engine.

You receive two things:
  1. A JSON Schema (``target_schema_json``) describing the structure the
     caller needs.
  2. A piece of raw input text (``raw_text``) — possibly malformed JSON,
     possibly free-form prose, possibly partially-extracted output. The
     caller does NOT know what shape it is in.

Your job is to extract data from the raw input and emit a JSON object
that conforms exactly to the target schema. Or, when the data is
genuinely not present, to refuse with a structured error envelope.

Strict rules — follow ALL of them:

1. NEVER hallucinate. Every value you emit MUST be traceable to the raw
   input text. If a required schema field has no corresponding evidence
   in the input, you MUST refuse — see the error envelope below. Do not
   guess, do not paraphrase to fill a gap, do not insert "TBD",
   "unknown", "N/A", placeholder strings, or empty strings to make the
   shape pass.

2. Preserve original wording, numbers, identifiers, and units exactly.
   Coerce types where the schema demands it (e.g. a numeric string ->
   number) but never alter the underlying value.

3. Return ONE JSON object only. No markdown fences. No leading or
   trailing prose. No commentary. The first character of your response
   must be ``{`` and the last character must be ``}``.

4. If the schema permits optional fields (no ``required`` entry covering
   them), populate them ONLY when the input clearly contains the value.
   Omit them otherwise.

5. If the input contains MORE data than the schema asks for, ignore the
   extras silently — return only the requested shape.

Two output shapes are valid:

A. SUCCESS — input has everything required:
   Return a JSON object that validates against the provided target
   schema. No extra keys.

B. UNABLE — input is missing required data:
   Return EXACTLY this shape (note the leading underscores — they are
   the sentinel that distinguishes this envelope from a real schema):

       {
         "_coerce_error": "<one short sentence: why you cannot fulfil>",
         "_missing_fields": ["<dotted.path.to.required.field>", ...],
         "_notes": "<optional clarifying detail, may be empty>"
       }

Choose shape B when ANY required field of the target schema lacks
supporting evidence in the input. Do not partially fill required fields
with invented data and emit shape A.
"""


_USER_TEMPLATE = """Target schema name: {{target_schema_name}}

Target JSON schema:
{{target_schema_json}}

Raw input to coerce:
---
{{raw_text}}
---

Return one JSON object — either a valid instance of the target schema, or the {"_coerce_error": ..., "_missing_fields": [...], "_notes": ...} envelope. Nothing else."""


class SchemaCoerceInputs(BaseModel):
    """Variables consumed by the SchemaCoerceAgent template."""

    raw_text: str
    target_schema_json: str
    target_schema_name: str = ""


class SchemaCoerceAgent(NamedAgent[SchemaCoerceInputs, BaseModel]):
    """Coerce loose text into a Pydantic schema, or report missing data.

    Primary public entry point is :meth:`coerce` — it accepts a Pydantic
    class directly and handles JSON-schema generation, dynamic parsing,
    and the dual-path success/error response. Calling :meth:`run` works
    too (because this is a normal NamedAgent) but bypasses the dynamic
    schema injection, so callers must build the variables themselves and
    parse the raw output by hand.
    """

    name = "schema_coerce"
    source = InlineAgentSource(
        config_dict={
            "model": _DEFAULT_MODEL,
            "system_instruction": _SYSTEM_PROMPT,
            "messages": [
                {"role": "user", "content": _USER_TEMPLATE},
            ],
            "temperature": 0.0,
        },
        name="SchemaCoerceAgent",
        variable_defaults={
            "raw_text": AgentVariable(name="raw_text", required=True),
            "target_schema_json": AgentVariable(name="target_schema_json", required=True),
            "target_schema_name": AgentVariable(name="target_schema_name", required=False),
        },
    )
    Inputs = SchemaCoerceInputs

    @classmethod
    async def coerce(
        cls,
        *,
        text: str,
        schema: type[ParsedT],
        config_overrides: LLMParams | dict[str, Any] | None = None,
        label: str | None = None,
    ) -> SchemaCoerceResult[ParsedT]:
        """Run the agent against ``text`` with ``schema`` as the target.

        Args:
            text: Raw input — anything string-shaped. Malformed JSON,
                  prose, fragments, OCR output, etc.
            schema: A Pydantic ``BaseModel`` subclass. Its
                  ``model_json_schema()`` is fed to the agent.
            config_overrides: Optional per-call LLM parameter overrides
                  (model, temperature, max_output_tokens, etc.). Useful
                  for swapping in a stronger model when the default
                  haiku-class model isn't reliable enough for the
                  schema's complexity.
            label: Optional sub-agent label for ``child_agent_context``.

        Returns:
            ``SchemaCoerceResult[ParsedT]`` — see that class's docstring
            for the three mutually-exclusive payload fields.
        """
        if not isinstance(text, str):
            raise TypeError(
                f"SchemaCoerceAgent.coerce(text=...) expects str, got {type(text).__name__}."
            )
        if not isinstance(schema, type) or not issubclass(schema, BaseModel):
            raise TypeError(
                "SchemaCoerceAgent.coerce(schema=...) expects a Pydantic BaseModel subclass."
            )

        schema_dict = schema.model_json_schema()
        schema_name = schema.__name__

        inputs = cls.Inputs(
            raw_text=text,
            target_schema_json=json.dumps(schema_dict, indent=2),
            target_schema_name=schema_name,
        )

        run_result = await cls.run(
            inputs=inputs,
            config_overrides=config_overrides,
            label=label or f"schema_coerce[{schema_name}]",
        )

        out: SchemaCoerceResult[ParsedT] = SchemaCoerceResult(
            success=False,
            raw_output=run_result.output or "",
            usage=dict(run_result.usage),
            usage_aggregated=run_result.usage_aggregated,
            usage_history=list(run_result.usage_history),
            model_id=run_result.model_id,
            metadata=dict(run_result.metadata),
        )

        if not run_result.success:
            out.parse_error = f"Agent execution failed: {run_result.error or 'unknown error'}"
            return out

        return cls._parse_dual_path(
            raw_output=run_result.output or "",
            schema=schema,
            schema_name=schema_name,
            out=out,
        )

    @classmethod
    def _parse_dual_path(
        cls,
        *,
        raw_output: str,
        schema: type[ParsedT],
        schema_name: str,
        out: SchemaCoerceResult[ParsedT],
    ) -> SchemaCoerceResult[ParsedT]:
        candidate = extract_json_block(raw_output)
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError as exc:
            vcprint(
                raw_output,
                f"[SchemaCoerceAgent:{schema_name}] Error Parsing Agent Response",
                color="red",
            )
            out.parse_error = f"JSONDecodeError: {exc.msg} (line {exc.lineno}, col {exc.colno})"
            return out

        if not isinstance(data, dict):
            vcprint(
                raw_output,
                f"[SchemaCoerceAgent:{schema_name}] "
                f"Expected JSON object, got {type(data).__name__}",
                color="red",
            )
            out.parse_error = f"Expected JSON object at the top level, got {type(data).__name__}"
            return out

        if "_coerce_error" in data:
            try:
                out.coerce_error = SchemaCoerceErrorResponse.model_validate(data)
                return out
            except ValidationError as exc:
                vcprint(
                    raw_output,
                    f"[SchemaCoerceAgent:{schema_name}] Malformed _coerce_error envelope",
                    color="red",
                )
                out.parse_error = f"Malformed coerce-error envelope: {exc.errors()}"
                return out

        try:
            out.parsed = schema.model_validate(data)
            out.success = True
            return out
        except ValidationError as exc:
            vcprint(
                raw_output,
                f"[SchemaCoerceAgent:{schema_name}] Output did not validate against {schema_name}",
                color="red",
            )
            out.parse_error = f"ValidationError against {schema_name}: {exc.errors()}"
            return out
