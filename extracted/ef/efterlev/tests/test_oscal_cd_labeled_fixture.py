"""Labeled-fixture conformance test for CD (v0.1.108 OSCAL arc step 4).

Sibling to `test_oscal_labeled_fixture.py` (POA&M version). Same
3PAO-inspectable pattern: a checked-in artifact derived from the
csp-starter-cfn Phase 2 lite verdicts, schema-validated on every PR.
"""

from __future__ import annotations

import json
from pathlib import Path

from efterlev.primitives.validate import (
    ValidateOscalComponentDefinitionInput,
    validate_oscal_component_definition,
)

_FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "evals/fixtures/csp-starter-cfn/oscal/labeled-component-definition-v0.1.108.json"
)


def test_labeled_cd_fixture_exists_on_disk() -> None:
    assert _FIXTURE_PATH.is_file(), (
        f"Labeled OSCAL CD fixture missing at {_FIXTURE_PATH}. "
        f"Run scripts/regenerate_oscal_cd_labeled_fixture.py."
    )


def test_labeled_cd_fixture_validates_against_schema() -> None:
    """The committed CD fixture must pass OSCAL 1.0.4 schema validation."""
    document = json.loads(_FIXTURE_PATH.read_text())
    result = validate_oscal_component_definition(
        ValidateOscalComponentDefinitionInput(oscal_document=document)
    )
    assert result.valid, (
        f"Labeled CD fixture failed schema validation. "
        f"Errors: {[(e.path, e.message) for e in result.errors]}"
    )


def test_labeled_cd_fixture_has_expected_shape() -> None:
    """Sanity check on the fixture's known structural counts."""
    document = json.loads(_FIXTURE_PATH.read_text())
    cd = document["component-definition"]
    assert cd["metadata"]["oscal-version"] == "1.0.4"
    assert len(cd["components"]) == 1
    component = cd["components"][0]
    assert component["type"] == "service"
    assert len(component["control-implementations"]) == 1
    assert len(component["control-implementations"][0]["implemented-requirements"]) == 12
