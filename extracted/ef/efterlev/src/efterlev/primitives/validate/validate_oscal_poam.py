"""`validate_oscal_poam` primitive — OSCAL 1.0.4 POA&M JSON schema conformance.

Companion gate to `generate_poam_oscal` (v0.1.105). The generator emits an
OSCAL POA&M JSON document; this primitive validates that document against the
vendored NIST OSCAL 1.0.4 POA&M JSON schema and surfaces structural errors
(missing required fields, malformed UUIDs, bad enum values, type mismatches).

Why this gate exists: OSCAL is a publish-and-pray output. Once we hand a
3PAO an OSCAL POA&M, schema-conformance failures show up as "your tool is
broken" — not as "interesting feedback." A pre-emit validation step catches
those failures before they ever reach a 3PAO.

Scope at v0.1.106: pure JSON-schema validation (jsonschema lib, deterministic,
fast, no external services). FedRAMP-specific Schematron rules layer on top
in v0.1.107 (GSA fedramp-automation rule set).
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator, validators
from jsonschema.exceptions import ValidationError
from pydantic import BaseModel, ConfigDict, Field

from efterlev.primitives.base import primitive

# Vendored schema location. Frozen at OSCAL 1.0.4 to match the generator's
# emit version (see generate_poam_oscal._OSCAL_VERSION). When the generator
# bumps OSCAL versions, vendor the corresponding schema here too.
_SCHEMA_RELATIVE_PATH = "catalogs/oscal/oscal_poam_schema_v1.0.4.json"


def _pcre_safe_pattern(validator: Any, patrn: str, instance: Any, schema: Any) -> Any:
    """Pattern-keyword override that tolerates PCRE Unicode property escapes.

    OSCAL schemas use `\\p{L}` etc. for markdown/text shape constraints —
    valid PCRE/XSD regex but unsupported by Python's stdlib `re` module.
    Patterns that re.compile cleanly (UUIDs, identifiers, etc.) are still
    enforced; un-parseable patterns are skipped silently. The result is a
    structural-conformance gate that catches everything except unicode-class
    text-shape rules. Schematron (v0.1.107) will catch those.
    """
    if not validator.is_type(instance, "string"):
        return
    try:
        compiled = re.compile(patrn)
    except re.error:
        return
    if not compiled.search(instance):
        yield ValidationError(f"{instance!r} does not match {patrn!r}")


# jsonschema's `validators.extend()` is the documented composition API for
# overriding keyword handlers without subclassing a validator class (which
# `jsonschema` deprecated as not-public-API in 4.18+; future versions will
# make it an error). Composition is equivalent: a new validator type with the
# overridden `pattern` handler.
PcreTolerantValidator = validators.extend(
    Draft7Validator,
    validators={"pattern": _pcre_safe_pattern},
)


def _load_vendored_schema() -> dict[str, Any]:
    """Load the OSCAL 1.0.4 POA&M JSON schema from the repo's catalogs/."""
    repo_root = Path(__file__).resolve().parents[4]
    schema_path = repo_root / _SCHEMA_RELATIVE_PATH
    if not schema_path.is_file():
        raise FileNotFoundError(
            f"OSCAL POA&M schema not found at {schema_path}. "
            f"Re-vendor from https://raw.githubusercontent.com/usnistgov/OSCAL/"
            f"v1.0.4/json/schema/oscal_poam_schema.json"
        )
    schema: dict[str, Any] = json.loads(schema_path.read_text())
    return schema


class ValidateOscalPoamInput(BaseModel):
    """Input: an OSCAL POA&M document as a Python dict (the generator's output shape)."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    oscal_document: dict[str, Any]


class OscalValidationError(BaseModel):
    """One JSON-schema violation, surfaced for human + machine consumption."""

    model_config = ConfigDict(frozen=True)

    # JSON pointer to the offending path (e.g., "plan-of-action-and-milestones.uuid").
    path: str
    # Human-readable message from jsonschema (kept verbatim; jsonschema's
    # messages are the canonical reference).
    message: str
    # Schema-side rule that was violated ("required", "pattern", "enum", etc.).
    validator: str


class ValidateOscalPoamOutput(BaseModel):
    """Output: pass/fail + the full list of violations."""

    model_config = ConfigDict(frozen=True)

    valid: bool
    errors: list[OscalValidationError] = Field(default_factory=list)
    # Schema metadata for traceability — which schema version was applied.
    schema_id: str


@primitive(capability="validate", side_effects=False, version="0.1.0", deterministic=True)
def validate_oscal_poam(input: ValidateOscalPoamInput) -> ValidateOscalPoamOutput:
    """Validate an OSCAL POA&M JSON dict against the vendored NIST schema.

    Returns `valid=True` with empty errors on conformance; `valid=False` with
    the full error list (no early-exit) on any violation. We surface ALL errors
    rather than first-fail because OSCAL documents tend to have correlated
    issues — the maintainer wants to fix them in one pass.
    """
    schema = _load_vendored_schema()
    validator = PcreTolerantValidator(schema)
    errors: list[OscalValidationError] = []
    for err in validator.iter_errors(input.oscal_document):
        errors.append(
            OscalValidationError(
                path=".".join(str(p) for p in err.absolute_path) or "<root>",
                message=err.message,
                validator=err.validator or "unknown",
            )
        )
    return ValidateOscalPoamOutput(
        valid=not errors,
        errors=errors,
        schema_id=str(schema.get("$id", "unknown")),
    )
