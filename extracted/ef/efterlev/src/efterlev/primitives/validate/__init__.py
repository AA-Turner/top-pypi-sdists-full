"""Validate primitives — schema and rule conformance for emitted artifacts.

Two layers for OSCAL POA&M output:

- `validate_oscal_poam` (v0.1.106) — vendored NIST OSCAL 1.0.4 JSON schema.
  Catches structural bugs (required fields, types, UUID format).
- `validate_oscal_fedramp_rules` (v0.1.107) — Python-native subset of GSA
  fedramp-automation rules. Catches FedRAMP-specific shape constraints
  (severity / status enumerations, evidence-link presence, baseline
  identifiers, FedRAMP-accepted OSCAL versions).

Run both in pipeline for full FedRAMP-targeted conformance.
"""

from __future__ import annotations

from efterlev.primitives.validate.validate_oscal_component_definition import (
    ValidateOscalComponentDefinitionInput,
    ValidateOscalComponentDefinitionOutput,
    validate_oscal_component_definition,
)
from efterlev.primitives.validate.validate_oscal_fedramp_rules import (
    FedrampRuleViolation,
    ValidateOscalFedrampRulesInput,
    ValidateOscalFedrampRulesOutput,
    validate_oscal_fedramp_rules,
)
from efterlev.primitives.validate.validate_oscal_poam import (
    OscalValidationError,
    ValidateOscalPoamInput,
    ValidateOscalPoamOutput,
    validate_oscal_poam,
)

__all__ = [
    "FedrampRuleViolation",
    "OscalValidationError",
    "ValidateOscalComponentDefinitionInput",
    "ValidateOscalComponentDefinitionOutput",
    "ValidateOscalFedrampRulesInput",
    "ValidateOscalFedrampRulesOutput",
    "ValidateOscalPoamInput",
    "ValidateOscalPoamOutput",
    "validate_oscal_component_definition",
    "validate_oscal_fedramp_rules",
    "validate_oscal_poam",
]
