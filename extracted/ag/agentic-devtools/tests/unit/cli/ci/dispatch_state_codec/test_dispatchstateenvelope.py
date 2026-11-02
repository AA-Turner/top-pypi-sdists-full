"""Tests for the immutable dispatch-state envelope model."""

from typing import Any, cast

import pytest

from agentic_devtools.cli.ci.dispatch_state_codec import DispatchStateEnvelope


def test_preserves_and_freezes_the_complete_v2_envelope() -> None:
    legacy = {"key": {"evidence": {"items": [1, {"value": "legacy"}]}}}
    canonical = {"identity": {"opaque": {"items": [1, {"value": "canonical"}]}}}
    envelope = DispatchStateEnvelope(2, legacy, canonical)

    cast(Any, legacy)["key"]["evidence"]["items"][1]["value"] = "changed"
    canonical["identity"]["opaque"]["items"].append(2)

    assert envelope.to_dict() == {
        "version": 2,
        "records": {"key": {"evidence": {"items": [1, {"value": "legacy"}]}}},
        "canonical_records": {"identity": {"opaque": {"items": [1, {"value": "canonical"}]}}},
    }
    with pytest.raises(TypeError):
        cast(Any, envelope.canonical_records["identity"]["opaque"]["items"])[0] = 9
    with pytest.raises(AttributeError):
        envelope.canonical_records["identity"]["opaque"]["items"].append(2)  # type: ignore[attr-defined]


def test_round_trips_flat_and_v1_envelope_shapes() -> None:
    records = {"key": {"state": "intent"}}

    assert DispatchStateEnvelope(None, records).to_dict() == records
    assert DispatchStateEnvelope(1, records).to_dict() == {"version": 1, "records": records}


def test_rejects_non_json_values() -> None:
    with pytest.raises(ValueError, match="JSON"):
        DispatchStateEnvelope(2, {"key": {"value": object()}}, {})


@pytest.mark.parametrize("version", [True, 3])
def test_rejects_invalid_versions(version: object) -> None:
    with pytest.raises(ValueError, match="version"):
        DispatchStateEnvelope(cast(Any, version), {}, {})


def test_rejects_canonical_records_outside_v2() -> None:
    with pytest.raises(ValueError, match="v2"):
        DispatchStateEnvelope(1, {}, {"key": {}})


def test_rejects_non_json_record_mappings() -> None:
    with pytest.raises(ValueError, match="object keys"):
        DispatchStateEnvelope(2, cast(Any, {1: {}}), {})
    with pytest.raises(ValueError, match="records must be an object"):
        DispatchStateEnvelope(2, cast(Any, []), {})
