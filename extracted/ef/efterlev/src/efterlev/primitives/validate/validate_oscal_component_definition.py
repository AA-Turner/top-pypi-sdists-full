"""`validate_oscal_component_definition` — OSCAL 1.0.4 CD JSON-schema gate.

Sibling to `validate_oscal_poam` (v0.1.106). Same PCRE-tolerant pattern
keyword (Python stdlib `re` doesn't support `\\p{...}` Unicode property
escapes used in OSCAL); standard regex (UUIDs, identifiers) is enforced.

If/when a third OSCAL kind ships, factor out the shared logic into
`_validate_against_vendored_schema(document, schema_relative_path)` —
not worth the abstraction at 2 callers (premature DRY).
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
from efterlev.primitives.validate.validate_oscal_poam import OscalValidationError

_SCHEMA_RELATIVE_PATH = "catalogs/oscal/oscal_component_schema_v1.0.4.json"


def _load_vendored_schema() -> dict[str, Any]:
    """Load the OSCAL 1.0.4 component-definition schema."""
    repo_root = Path(__file__).resolve().parents[4]
    schema_path = repo_root / _SCHEMA_RELATIVE_PATH
    if not schema_path.is_file():
        raise FileNotFoundError(
            f"OSCAL component-definition schema not found at {schema_path}. "
            f"Re-vendor from https://raw.githubusercontent.com/usnistgov/OSCAL/"
            f"v1.0.4/json/schema/oscal_component_schema.json"
        )
    schema: dict[str, Any] = json.loads(schema_path.read_text())
    return schema


def _pcre_safe_pattern(validator: Any, patrn: str, instance: Any, schema: Any) -> Any:
    """Same pattern-keyword override as validate_oscal_poam — see that
    module's docstring for the PCRE-tolerance rationale.
    """
    if not validator.is_type(instance, "string"):
        return
    try:
        compiled = re.compile(patrn)
    except re.error:
        return
    if not compiled.search(instance):
        yield ValidationError(f"{instance!r} does not match {patrn!r}")


# Composition via `validators.extend()` — same rationale as the POA&M
# validator: jsonschema deprecates subclassing in 4.18+; this is the
# documented forward-compatible alternative.
PcreTolerantValidator = validators.extend(
    Draft7Validator,
    validators={"pattern": _pcre_safe_pattern},
)


class ValidateOscalComponentDefinitionInput(BaseModel):
    """Input: an OSCAL component-definition document as a Python dict."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    oscal_document: dict[str, Any]


class ValidateOscalComponentDefinitionOutput(BaseModel):
    """Output: pass/fail + the full list of violations."""

    model_config = ConfigDict(frozen=True)

    valid: bool
    errors: list[OscalValidationError] = Field(default_factory=list)
    schema_id: str


@primitive(capability="validate", side_effects=False, version="0.1.0", deterministic=True)
def validate_oscal_component_definition(
    input: ValidateOscalComponentDefinitionInput,
) -> ValidateOscalComponentDefinitionOutput:
    """Validate an OSCAL CD JSON dict against the vendored NIST schema.

    Same surfacing semantics as `validate_oscal_poam`: returns ALL
    violations (no early-exit).
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
    return ValidateOscalComponentDefinitionOutput(
        valid=not errors,
        errors=errors,
        schema_id=str(schema.get("$id", "unknown")),
    )
