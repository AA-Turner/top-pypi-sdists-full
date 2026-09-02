"""Provider-aware output-schema linting.

A structured-output schema must satisfy the INTERSECTION of what OpenAI,
Anthropic, and Google Gemini actually accept — "valid JSON Schema" is not
enough. The per-provider rules are owned by the three translators
(``providers/{openai,anthropic,google}/translator.py``) and the shared pure
rules in ``matrx_ai.schema.rules``. This module REPORTS against those rules
instead of silently transforming a schema, so a caller can fix it *before*
persisting an agent that a provider would 400 on at runtime — killing the whole
class of "shipped an agent whose schema a provider rejects".

Two entry points:
- ``lint_output_schema(schema, providers=...)`` → findings + a
  ``portable_schema`` massaged to satisfy all three providers.
- ``check_sample_against_schema(sample, schema)`` → does the declared sample
  output actually validate against the declared output schema?

Consumed by the Agent Service ``validate_schema`` / ``create_structured``
actions and (retrofit) by the agent_factory build path. Nothing here raises.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from matrx_ai.schema.rules import (
    enforce_additional_properties_false,
    enforce_all_required,
    hoist_discriminator_first,
    is_object_node,
    is_root_object,
)

Provider = Literal["openai", "anthropic", "google"]
ALL_PROVIDERS: tuple[Provider, ...] = ("openai", "anthropic", "google")


class SchemaFinding(BaseModel):
    # "structural" or one of the provider names. Plain str (not the Provider
    # literal) so the structural bucket fits the same field.
    provider: str
    severity: Literal["error", "warning"]
    path: str
    message: str


class SchemaLintReport(BaseModel):
    ok: bool
    providers: list[str]
    findings: list[SchemaFinding] = Field(default_factory=list)
    # The input massaged to satisfy OpenAI strict + Anthropic + Gemini (object
    # root + additionalProperties:false + every property required on every
    # object). None when the root is not an object (not derivable).
    portable_schema: dict[str, Any] | None = None

    @property
    def errors(self) -> list[SchemaFinding]:
        return [f for f in self.findings if f.severity == "error"]

    @property
    def warnings(self) -> list[SchemaFinding]:
        return [f for f in self.findings if f.severity == "warning"]


def _walk_objects(node: Any, path: str) -> list[tuple[str, dict[str, Any]]]:
    """Every object-typed node in the schema, with a JSON-pointer-ish path."""
    out: list[tuple[str, dict[str, Any]]] = []
    if isinstance(node, dict):
        if is_object_node(node):
            out.append((path, node))
        props = node.get("properties")
        if isinstance(props, dict):
            for key, value in props.items():
                out.extend(_walk_objects(value, f"{path}/properties/{key}"))
        items = node.get("items")
        if isinstance(items, dict):
            out.extend(_walk_objects(items, f"{path}/items"))
        elif isinstance(items, list):
            for idx, item in enumerate(items):
                out.extend(_walk_objects(item, f"{path}/items/{idx}"))
        for comb in ("anyOf", "oneOf", "allOf"):
            arr = node.get(comb)
            if isinstance(arr, list):
                for idx, item in enumerate(arr):
                    out.extend(_walk_objects(item, f"{path}/{comb}/{idx}"))
        defs = node.get("$defs") or node.get("definitions")
        if isinstance(defs, dict):
            for key, value in defs.items():
                out.extend(_walk_objects(value, f"{path}/$defs/{key}"))
    return out


def _contains_ref(node: Any) -> bool:
    if isinstance(node, dict):
        if "$ref" in node:
            return True
        return any(_contains_ref(v) for v in node.values())
    if isinstance(node, list):
        return any(_contains_ref(item) for item in node)
    return False


def lint_output_schema(
    schema: Any,
    *,
    providers: tuple[Provider, ...] = ALL_PROVIDERS,
) -> SchemaLintReport:
    """Lint an output schema against each provider's structured-output rules.
    ``ok`` is True iff there are no ``error`` findings for the requested
    providers. ``warnings`` never flip ``ok``."""
    want = set(providers)
    findings: list[SchemaFinding] = []

    if not isinstance(schema, dict):
        findings.append(
            SchemaFinding(
                provider="structural",
                severity="error",
                path="#",
                message="Output schema must be a JSON object (a dict).",
            )
        )
        return SchemaLintReport(ok=False, providers=list(providers), findings=findings)

    root_object = is_root_object(schema)
    if not root_object:
        findings.append(
            SchemaFinding(
                provider="structural",
                severity="error",
                path="#",
                message=(
                    f"Schema root must be an object (got type={schema.get('type')!r}). "
                    "OpenAI, Anthropic, and Gemini all require an object root for "
                    'structured output. Wrap your value, e.g. {"type":"object",'
                    '"properties":{"items":<your schema>},"required":["items"]}.'
                ),
            )
        )

    object_nodes = _walk_objects(schema, "#") if root_object else []

    # additionalProperties:false is a HARD rule for both OpenAI strict and
    # Anthropic. All-required is hard for OpenAI only — Anthropic accepts a
    # partial `required` list (measured against the live compiler 2026-08-24,
    # correcting this module's original claim). The platform still enforces it
    # everywhere so ONE portable schema satisfies every provider; it is NOT a
    # lever for the Anthropic compiled-grammar budget (see
    # matrx_ai.schema.grammar_budget for what was measured and rejected).
    if root_object and ({"openai", "anthropic"} & want):
        for path, node in object_nodes:
            props = node.get("properties")
            prop_keys = list(props.keys()) if isinstance(props, dict) else []

            if node.get("additionalProperties") is not False:
                if "openai" in want:
                    findings.append(
                        SchemaFinding(
                            provider="openai",
                            severity="error",
                            path=path,
                            message='OpenAI strict json_schema requires "additionalProperties": false on every object.',
                        )
                    )
                if "anthropic" in want:
                    findings.append(
                        SchemaFinding(
                            provider="anthropic",
                            severity="error",
                            path=path,
                            message='Anthropic requires "additionalProperties": false on every object (server-validated).',
                        )
                    )

            required = node.get("required")
            req_set = set(required) if isinstance(required, list) else set()
            missing = [k for k in prop_keys if k not in req_set]
            if missing:
                if "openai" in want:
                    findings.append(
                        SchemaFinding(
                            provider="openai",
                            severity="error",
                            path=path,
                            message=(
                                'OpenAI strict requires EVERY property in "required" '
                                f"(missing: {missing}). Express optional fields as a "
                                '["<type>","null"] union, not by omission.'
                            ),
                        )
                    )
                if "anthropic" in want:
                    findings.append(
                        SchemaFinding(
                            provider="anthropic",
                            severity="error",
                            path=path,
                            message=(
                                "Anthropic tolerates a partial \"required\" list (measured "
                                "live 2026-08-24), but the platform still lists every "
                                "property so ONE portable schema satisfies OpenAI strict "
                                f"too (missing: {missing}). Express optional fields as a "
                                '["<type>","null"] union rather than by omission.'
                            ),
                        )
                    )

    # Gemini: object root is the hard rule (else structured output is silently
    # omitted). $ref/$defs may not resolve in its restricted subset — a
    # portability warning, not a hard error.
    if (
        "google" in want
        and root_object
        and ("$defs" in schema or "definitions" in schema or _contains_ref(schema))
    ):
        findings.append(
            SchemaFinding(
                provider="google",
                severity="warning",
                path="#",
                message="Gemini's restricted schema subset may not resolve $ref/$defs — inline definitions for portability.",
            )
        )

    portable = _make_portable(schema) if root_object else None
    has_error = any(f.severity == "error" for f in findings)
    return SchemaLintReport(
        ok=not has_error,
        providers=list(providers),
        findings=findings,
        portable_schema=portable,
    )


def _make_portable(schema: dict[str, Any]) -> dict[str, Any]:
    """A copy massaged to satisfy all three providers: additionalProperties:false
    on every object + required = all property keys on every object. Gemini
    ignores the extra keywords.

    NOTE: this deliberately KEEPS advisory validation keywords (minItems,
    maxItems, pattern, …). The platform saves the richest possible schema; a
    keyword that only SOME providers reject (e.g. Cerebras) is stripped at that
    provider's request boundary (see strip_unsupported_keywords + the OpenAI-
    compatible response_format builder), NOT baked out of the stored schema."""
    out = enforce_additional_properties_false(schema)
    enforce_all_required(out)
    # The discriminator must be the FIRST key the model emits, or a live
    # surface cannot route a streaming payload until the run is over. Schema
    # property order IS wire order for a constrained decoder, and it does not
    # survive a jsonb round-trip (see hoist_discriminator_first). Re-hoist here
    # so every consumer of portable_schema — response_format_for_kind included
    # — hands the provider a __kind-first schema.
    return hoist_discriminator_first(out)


def check_sample_against_schema(sample: Any, schema: Any) -> list[SchemaFinding]:
    """Does the declared sample output actually validate against the declared
    output schema? (Arman's explicit requirement.) Empty list = consistent.
    Never raises."""
    if not isinstance(schema, dict):
        return [
            SchemaFinding(
                provider="structural",
                severity="error",
                path="#",
                message="Cannot check sample: output schema is not an object.",
            )
        ]
    try:
        import jsonschema
    except ImportError:  # pragma: no cover - jsonschema is a hard dep here
        return []
    try:
        jsonschema.validate(instance=sample, schema=schema)
    except jsonschema.ValidationError as exc:
        loc = "#/" + "/".join(str(p) for p in exc.absolute_path) if exc.absolute_path else "#"
        return [
            SchemaFinding(
                provider="structural",
                severity="error",
                path=loc,
                message=f"Sample does not satisfy the output schema: {exc.message}",
            )
        ]
    except jsonschema.SchemaError as exc:
        return [
            SchemaFinding(
                provider="structural",
                severity="error",
                path="#",
                message=f"Output schema is itself invalid JSON Schema: {exc.message}",
            )
        ]
    return []


__all__ = [
    "ALL_PROVIDERS",
    "Provider",
    "SchemaFinding",
    "SchemaLintReport",
    "check_sample_against_schema",
    "lint_output_schema",
]
