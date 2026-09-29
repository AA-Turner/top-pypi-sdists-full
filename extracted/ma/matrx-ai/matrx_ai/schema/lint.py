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
    WideningBudget,
    dedupe_combinator_branches,
    enforce_additional_properties_false,
    enforce_all_required,
    hoist_discriminator_first,
    is_map_node,
    is_object_node,
    is_root_object,
    make_array_items_explicit,
    nullable_enum_violations,
    rewrite_const_as_enum,
    split_enum_from_type_union,
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

    # additionalProperties:false is a HARD WIRE rule for both OpenAI strict and
    # Anthropic; all-required is hard for OpenAI only (Anthropic accepts a partial
    # `required` list, measured 2026-08-24). Both are WIRE concerns: since
    # 2026-09-28 every translator's first step (`make_portable`) closes objects
    # and widens optional fields to required-and-nullable on the wire, so an
    # authored schema is reported here as WARNINGS, never refused — and the stored
    # schema stays the author's, which the answer is pruned back to and checked
    # against (schema.answer_contract). It is NOT a
    # lever for the Anthropic compiled-grammar budget (see
    # matrx_ai.schema.grammar_budget for what was measured and rejected).
    if root_object and ({"openai", "anthropic"} & want):
        for path, node in object_nodes:
            props = node.get("properties")
            prop_keys = list(props.keys()) if isinstance(props, dict) else []

            if is_map_node(node):
                # A dynamic-key map is kept as a map in the portable contract
                # (Gemini expresses it; the answer is validated against it). The
                # strict providers' translators narrow it to {} and record a
                # finding — so it is a WARNING about what those providers will
                # enforce, never a reason to refuse the schema.
                strict = [p for p in ("openai", "anthropic") if p in want]
                if strict:
                    findings.append(
                        SchemaFinding(
                            provider=strict[0],
                            severity="warning",
                            path=path,
                            message=(
                                "Dynamic-key map (additionalProperties is a schema/true): "
                                f"{' and '.join(strict)} cannot express it and will receive it "
                                "narrowed to an empty object. Declare the entries as an array "
                                "of {key, value} objects to keep them enforced everywhere."
                            ),
                        )
                    )
            elif node.get("additionalProperties") is not False:
                # 🚨 NOT an error since 2026-09-28. Every provider translator's
                # FIRST step is ``make_portable`` (closed objects, all-required,
                # optional fields widened to nullable), so an authored schema that
                # leaves an object open or a field optional reaches every provider
                # in the shape it accepts. Refusing it forced authors to STORE the
                # portable copy — which says every optional field is "required and
                # may be null", so the dispatch seam could never prune a provider's
                # nulls back to the author's absence (SCHEMA-TRANSLATION.md §13).
                findings.append(
                    SchemaFinding(
                        provider="openai" if "openai" in want else "anthropic",
                        severity="warning",
                        path=path,
                        message=(
                            'Open object (no "additionalProperties": false): the provider '
                            "translators close it on the wire; the stored schema keeps "
                            "the author's contract and the answer is checked against it."
                        ),
                    )
                )

            required = node.get("required")
            req_set = set(required) if isinstance(required, list) else set()
            missing = [k for k in prop_keys if k not in req_set]
            if missing:
                findings.append(
                    SchemaFinding(
                        provider="openai" if "openai" in want else "anthropic",
                        severity="warning",
                        path=path,
                        message=(
                            f"Optional fields {missing}: strict providers receive them "
                            "required-and-nullable (the translator widens them on the "
                            "wire), and a null answer is pruned back to the absence the "
                            "author declared before any consumer reads it. Keep them "
                            "optional here — never store the widened copy."
                        ),
                    )
                )

    # A nullable enum spelled as a type ARRAY — every Pydantic Optional[SomeEnum].
    # Anthropic refused it live, 2026-09-28: "output_config.format.schema: Invalid
    # schema: Enum value 'victim' does not match declared type '['string',
    # 'null']'" — the lint returned an empty report for it. A WARNING, not an
    # error, by the same rule as the two above: `make_portable` (every
    # translator's first step) rewrites it losslessly to
    # `anyOf: [{type, enum}, {type: null}]`, so refusing it would be a new
    # blocking gate on authoring for a shape the wire never carries. OpenAI and
    # Gemini accept the rewritten form too (measured, see widen_to_nullable).
    if "anthropic" in want:
        for path in nullable_enum_violations(schema):
            findings.append(
                SchemaFinding(
                    provider="anthropic",
                    severity="warning",
                    path=path,
                    message=(
                        "An enum/const beside a type ARRAY (or a null member its type "
                        "refuses) is rejected by Anthropic (\"Enum value … does not match "
                        "declared type\"). The translators send it as anyOf: "
                        '[{"type": T, "enum": [...]}, {"type": "null"}] — spell it that '
                        "way here to match the wire."
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


def make_portable(
    schema: dict[str, Any],
    *,
    budget: WideningBudget | None = None,
    notes: list[str] | None = None,
) -> dict[str, Any]:
    """THE shared first step of every provider translator: the author's schema,
    with every ``const`` spelled ``enum: [X]`` and every duplicate combinator
    branch dropped, then closed (``additionalProperties: false`` on every object,
    maps kept), every property listed in ``required`` with each OPTIONAL one
    expressed as required-and-nullable where ``budget`` allows and forced (and
    named in ``notes``) where it does not, and ``__kind`` hoisted first.

    Idempotent: a schema that already went through it comes out unchanged, so a
    translator may receive either the author's schema or a stored portable copy.
    The author's schema is what travels on the wire envelope and what the answer
    is checked against; this is what each translator derives from it.

    The two lossless rewrites run on EVERY schema, object-root or not, and they
    live here — in the one step all seven translators share — because both were
    measured refusing live contracts on providers that had no copy of the rule
    (SCHEMA-TRANSLATION-VERIFY.md, F5 and F7, 2026-09-28):

    * ``rewrite_const_as_enum`` — ``{"const": "flashcard_set"}`` with no ``type``
      is a hard ``400 invalid_json_schema`` on OpenAI ("In
      context=('properties','__kind'), schema must have a 'type' key"), and 78
      live bound contracts — the ``__kind`` marker the platform's own law
      requires on every schema — were unbindable there while only Google's
      translator called the function this module already exported. ``enum: [X]``
      is the identical constraint (``pins_one_value`` still sees it, so ``__kind``
      is still forced and never widened to nullable) and it is what Gemini's
      decoder actually honors, so the marker and its ONE allowed value survive
      to the wire and in the answer exactly as declared.
    * :func:`dedupe_combinator_branches` — a union is the most expensive thing
      in a constrained grammar and a duplicated branch buys nothing.
    """
    schema = rewrite_const_as_enum(schema)
    # After the const rewrite, so `{"type": ["T","null"], "const": X}` — now
    # `enum: [X]` beside a type array — is split too. Lossless; see
    # split_enum_from_type_union for the live refusal it removes.
    schema = split_enum_from_type_union(schema)
    schema = dedupe_combinator_branches(schema)
    # An array with no item schema is refused by name on OpenAI strict ("array
    # schema missing items"); `items: {}` says the same thing explicitly, so every
    # provider's own rules can then decide what its element becomes.
    schema = make_array_items_explicit(schema)
    if not is_root_object(schema):
        return schema
    out = enforce_additional_properties_false(split_enum_from_type_union(schema), maps="keep")
    enforce_all_required(out, express_optional_as_nullable=True, notes=notes, budget=budget)
    return hoist_discriminator_first(out)


def _make_portable(schema: dict[str, Any]) -> dict[str, Any]:
    """A copy massaged to satisfy all three providers: additionalProperties:false
    on every object + required = all property keys on every object. Gemini
    ignores the extra keywords.

    NOTE: this deliberately KEEPS advisory validation keywords (minItems,
    maxItems, pattern, …). The platform saves the richest possible schema; a
    keyword that only SOME providers reject (e.g. Cerebras) is stripped at that
    provider's request boundary (see strip_unsupported_keywords + the OpenAI-
    compatible response_format builder), NOT baked out of the stored schema."""
    # A dynamic-key map stays a map HERE: this portable copy is also the contract
    # the answer is validated against, and Gemini expresses maps natively. The
    # strict providers (Anthropic, OpenAI) narrow a map at their own boundary and
    # say so — narrowing it here silently emptied every map for every provider.
    # Keep the lint report's portable copy on the same lossless nullable-enum
    # path as every translator. Without this, the report named Anthropic's
    # refusal but returned the original type-array form to its caller.
    out = split_enum_from_type_union(schema)
    out = enforce_additional_properties_false(out, maps="keep")
    # required + NULLABLE, never required alone. This copy is what the answer is
    # VALIDATED against, so forcing an optional field here refused an answer the
    # author's own schema allows — 2,865 live schemas force a real business field
    # (`gap_description` exists to be set only when there is a gap). Nullable
    # carries "absent", so the portable contract admits exactly what the declared
    # one does; `prune_optional_nulls` turns those nulls back into absence for a
    # reader that wants the author's shape.
    enforce_all_required(out, express_optional_as_nullable=True)
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
    "make_portable",
]
