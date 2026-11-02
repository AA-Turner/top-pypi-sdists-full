"""Deterministic Content IR contracts — the ABI/drift-detection spine.

THE LAW (Arman, ruled 2026-08-18/20 — plan of record
``common-docs/systems/architecture/content-ir/FEATURE.md``): every value
crossing a named boundary is a kind instance and SAYS SO ITSELF — ``__kind`` is
part of the data, a declared model field (``content_ir.model.KindModel``),
exactly as ``"object": "charge"`` is part of every Stripe payload. This module
once stated the opposite ("must not inject __kind into business payloads");
that doctrine produced payloads whose identity evaporated the moment they left
their row, and is DEAD. Stripping survives at exactly two doors — agent prompts
and external egress (``content_ir.markers.strip_kind_markers``) — plus the
ingestion gate's legacy shim (``reduce_for_ingestion``: the marker is removed
only where a closed pre-kinds model would fatally reject it).

WHAT THIS MODULE STILL IS — and it is being KEPT: the deterministic ABI
contract for node/tool/agent I/O boundaries. ``contract_from_model`` derives an
exact fingerprint contract from a pydantic schema so the platform can detect
SCHEMA DRIFT (change a field, the hash changes, the change is visible). What
changed (2026-08-20): contracts no longer masquerade as declarations —
``NodeRegistry.register`` does not stamp fingerprint slugs into specs (an
undeclared node is undeclared; settlement's runtime propagation reads the
payload's own ``__kind`` instead), and the contract rows are being evicted from
the shape registry into their own store. A contract is a type signature; a kind
is a declared shape. Big difference — that was the whole point.
"""

from __future__ import annotations

import hashlib
import json
import re
from enum import StrEnum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.content_ir.markers import strip_kind_markers
from matrx_graph.executor.schema_validation import validate_instance

ValueT = TypeVar("ValueT")


class ContractFamily(StrEnum):
    ACTION_IO = "action_io"
    TOOL_IO = "tool_io"
    WORKFLOW_IO = "workflow_io"
    AGENT_IO = "agent_io"


class ContractDirection(StrEnum):
    INPUT = "input"
    OUTPUT = "output"


class ContractVerdict(BaseModel):
    model_config = ConfigDict(frozen=True)

    checked: bool
    errors: list[str] = Field(default_factory=list)

    @property
    def ok(self) -> bool | None:
        return not self.errors if self.checked else None


class KindedValue(BaseModel, Generic[ValueT]):
    """Logical typed envelope; ``value`` is never rewritten or decorated."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    kind: str
    version: int = 1
    value: ValueT
    checked: bool = False
    errors: list[str] = Field(default_factory=list)


class ContractDefinition(BaseModel):
    """Publisher-ready representation of one data-only Content IR kind."""

    model_config = ConfigDict(frozen=True)

    kind: str
    label: str
    family: ContractFamily
    direction: ContractDirection
    source_name: str
    source_id: str | None = None
    json_schema: dict[str, Any]
    fingerprint: str
    version: int = 1

    def metadata(self) -> dict[str, Any]:
        # No `data_only` key: the render-monitoring exemption for machine
        # contract families (action_io/tool_io/workflow_io) is derived purely
        # from `family` by `content_ir.evaluate_kind_activation` — the manual
        # per-row flag was eradicated 2026-08-27 (see `scripts/_kind_family.py`
        # and `scripts/check_kind_family_law.py`).
        return {
            "family": self.family.value,
            "direction": self.direction.value,
            "source_name": self.source_name,
            "source_id": self.source_id,
            "generated": True,
            "fingerprint": self.fingerprint,
        }


def contract_kind_slug(
    family: ContractFamily | str,
    source_name: str,
    direction: ContractDirection | str,
) -> str:
    """Create a readable, stable slug and disambiguate normalized names."""

    family_value = ContractFamily(family).value
    direction_value = ContractDirection(direction).value
    normalized = re.sub(r"[^a-z0-9]+", "_", source_name.lower()).strip("_") or "unnamed"
    digest = hashlib.sha256(source_name.encode("utf-8")).hexdigest()[:8]
    return f"{family_value}_{normalized}_{digest}_{direction_value}"


def schema_fingerprint(schema: dict[str, Any]) -> str:
    canonical = json.dumps(schema, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def contract_definition(
    *,
    family: ContractFamily | str,
    source_name: str,
    direction: ContractDirection | str,
    json_schema: dict[str, Any],
    label: str | None = None,
    version: int = 1,
    source_id: str | None = None,
) -> ContractDefinition:
    family_value = ContractFamily(family)
    direction_value = ContractDirection(direction)
    return ContractDefinition(
        kind=contract_kind_slug(family_value, source_name, direction_value),
        label=label or f"{source_name} {direction_value.value}",
        family=family_value,
        direction=direction_value,
        source_name=source_name,
        source_id=source_id,
        json_schema=json_schema,
        fingerprint=schema_fingerprint(json_schema),
        version=version,
    )


def contract_from_model(
    *,
    family: ContractFamily | str,
    source_name: str,
    direction: ContractDirection | str,
    model: type[BaseModel],
    label: str | None = None,
    source_id: str | None = None,
) -> ContractDefinition:
    return contract_definition(
        family=family,
        source_name=source_name,
        direction=direction,
        json_schema=model.model_json_schema(),
        label=label,
        source_id=source_id,
    )


def check_schema(value: Any, schema: dict[str, Any] | None) -> ContractVerdict:
    """Shadow-check a value, keeping SKIPPED distinct from PASS.

    VALIDATION TOLERANCE, NEVER STORAGE. A producer bound to a kind answers in
    the BLOCK shape (markers at every depth); most registered schemas are the
    WIRE export, which does not declare them. So a LOCAL copy is reduced
    (``strip_kind_markers``, schema-aware — a kind that declares ``__kind`` for
    real keeps it) purely to run the check. The reduced value never leaves this
    function: only a verdict does. The caller's artifact is untouched, and it
    keeps its marker, because ``__kind`` is part of the data
    (KINDS_EVERYWHERE_PLAN §4.2).
    """

    if not isinstance(schema, dict):
        return ContractVerdict(checked=False)
    try:
        value = strip_kind_markers(value, schema)
        return ContractVerdict(checked=True, errors=validate_instance(schema, value))
    except Exception:
        # A malformed producer schema is a platform defect, not a payload
        # failure. Shadow validation must stay fail-open and report SKIPPED.
        return ContractVerdict(checked=False)


def envelope(
    *,
    definition: ContractDefinition,
    value: ValueT,
    verdict: ContractVerdict,
) -> KindedValue[ValueT]:
    return KindedValue(
        kind=definition.kind,
        version=definition.version,
        value=value,
        checked=verdict.checked,
        errors=verdict.errors,
    )


def example_from_schema(schema: dict[str, Any]) -> Any:
    """Build a deterministic schema-shaped seed example for data-only kinds.

    This is intentionally conservative: it resolves local Pydantic ``$defs``
    references and satisfies common scalar bounds. Publishers must validate
    the result and omit it when an exotic schema cannot be synthesized.
    """

    defs = schema.get("$defs") if isinstance(schema.get("$defs"), dict) else {}

    def build(node: Any, seen: frozenset[str] = frozenset()) -> Any:
        if not isinstance(node, dict):
            return None
        ref = node.get("$ref")
        if isinstance(ref, str) and ref.startswith("#/$defs/"):
            key = ref.rsplit("/", 1)[-1]
            if key in seen:
                return None
            return build(defs.get(key), seen | {key})
        if "const" in node:
            return node["const"]
        enum = node.get("enum")
        if isinstance(enum, list) and enum:
            return enum[0]
        if "default" in node:
            return node["default"]
        for union_key in ("oneOf", "anyOf"):
            options = node.get(union_key)
            if isinstance(options, list) and options:
                non_null = [item for item in options if item.get("type") != "null"]
                return build((non_null or options)[0], seen)
        node_type = node.get("type")
        if isinstance(node_type, list):
            node_type = next((item for item in node_type if item != "null"), "null")
        if node_type == "object" or isinstance(node.get("properties"), dict):
            properties = node.get("properties") or {}
            required = node.get("required")
            keys = required if isinstance(required, list) else list(properties)
            return {key: build(properties.get(key, {}), seen) for key in keys}
        if node_type == "array":
            count = max(int(node.get("minItems", 0) or 0), 0)
            return [build(node.get("items", {}), seen) for _ in range(count)]
        if node_type == "string":
            # `format` is an assertion under strict validators (pg_jsonschema
            # asserts it; Python's default posture is annotate-only) — emit a
            # canonical valid value so the same example passes BOTH.
            fmt = node.get("format")
            format_values = {
                "date": "2026-01-01",
                "date-time": "2026-01-01T00:00:00Z",
                "time": "00:00:00",
                "duration": "P1D",
                "email": "user@example.com",
                "idn-email": "user@example.com",
                "hostname": "example.com",
                "idn-hostname": "example.com",
                "ipv4": "127.0.0.1",
                "ipv6": "::1",
                "uri": "https://example.com/",
                "uri-reference": "https://example.com/",
                "iri": "https://example.com/",
                "iri-reference": "https://example.com/",
                "uuid": "00000000-0000-0000-0000-000000000000",
                "json-pointer": "/x",
                "relative-json-pointer": "0",
                "regex": "^x$",
            }
            if isinstance(fmt, str) and fmt in format_values:
                return format_values[fmt]
            minimum = max(int(node.get("minLength", 0) or 0), 0)
            if node.get("pattern") and minimum == 0:
                minimum = 1
            if minimum == 0:
                # '' is valid JSON, but storage layers coerce empty strings to
                # NULL on the jsonb read path (matrx-orm JSONBField.to_python),
                # which then violates NOT NULL example columns. Emit a
                # non-empty sample unless the schema forbids one.
                max_length = node.get("maxLength")
                if max_length is None or int(max_length) >= 1:
                    minimum = 1
            return "x" * minimum
        if node_type == "integer":
            if "exclusiveMinimum" in node:
                return int(node["exclusiveMinimum"]) + 1
            return int(node.get("minimum", 0) or 0)
        if node_type == "number":
            if "exclusiveMinimum" in node:
                return float(node["exclusiveMinimum"]) + 1.0
            return float(node.get("minimum", 0) or 0)
        if node_type == "boolean":
            return False
        if node_type == "null":
            return None
        return None

    return build(schema)
