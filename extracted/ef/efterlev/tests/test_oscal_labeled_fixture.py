"""Labeled-fixture conformance test (v0.1.106 OSCAL arc step 2).

Companion to `test_validate_oscal_poam.py`. The validator tests ensure the
generator-of-the-moment is schema-conformant. THIS test guards a checked-in,
3PAO-inspectable artifact at `evals/fixtures/csp-starter-cfn/oscal/labeled-
poam-v0.1.106.json` — derived from the csp-starter-cfn maintainer-validation
fixture (Phase 2 lite, v0.1.81).

Why both: a 3PAO who downloads efterlev wants to see "what does an OSCAL
POA&M from this tool actually look like?" without running it. The labeled
fixture answers that. This test ensures it stays valid as the schema /
generator evolve. Refresh procedure documented in evals/OSCAL_CONFORMANCE.md.
"""

from __future__ import annotations

import json
from pathlib import Path

from efterlev.primitives.validate import (
    ValidateOscalFedrampRulesInput,
    ValidateOscalPoamInput,
    validate_oscal_fedramp_rules,
    validate_oscal_poam,
)

_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "evals/fixtures/csp-starter-cfn/oscal/labeled-poam-v0.1.106.json"
)


def test_labeled_fixture_exists_on_disk() -> None:
    """The labeled fixture must be present — guards against accidental deletion."""
    assert _FIXTURE_PATH.is_file(), (
        f"Labeled OSCAL fixture missing at {_FIXTURE_PATH}. Refresh per evals/OSCAL_CONFORMANCE.md."
    )


def test_labeled_fixture_validates_against_schema() -> None:
    """The committed labeled fixture must pass OSCAL 1.0.4 schema validation.

    If this fails after a generator change: regenerate the fixture (see
    evals/OSCAL_CONFORMANCE.md) and commit the update with the version bump.
    """
    document = json.loads(_FIXTURE_PATH.read_text())
    result = validate_oscal_poam(ValidateOscalPoamInput(oscal_document=document))
    assert result.valid, (
        f"Labeled fixture failed OSCAL schema validation. "
        f"Errors: {[(e.path, e.message) for e in result.errors]}"
    )


def test_labeled_fixture_passes_fedramp_rules() -> None:
    """v0.1.107 gate: the labeled fixture must satisfy every FedRAMP rule.

    Catches regressions in the rule layer against the canonical 3PAO-
    inspectable artifact (e.g., adding a new rule that the existing
    fixture violates — fix the generator, regenerate, recommit).
    """
    document = json.loads(_FIXTURE_PATH.read_text())
    result = validate_oscal_fedramp_rules(ValidateOscalFedrampRulesInput(oscal_document=document))
    assert result.valid, (
        f"Labeled fixture failed FedRAMP rule layer. "
        f"Violations: {[(v.rule_id, v.path, v.message) for v in result.violations]}"
    )


def test_labeled_fixture_has_expected_shape() -> None:
    """Sanity check on the fixture's known structural counts.

    These numbers come from the v0.1.106 generation (see CHANGELOG). If the
    fixture is regenerated with different inputs, update these expectations.
    """
    document = json.loads(_FIXTURE_PATH.read_text())
    poam = document["plan-of-action-and-milestones"]
    assert len(poam["poam-items"]) == 6
    assert len(poam["risks"]) == 12
    assert len(poam["observations"]) == 6
    assert poam["metadata"]["oscal-version"] == "1.0.4"
