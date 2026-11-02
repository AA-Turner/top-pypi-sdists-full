"""Tests for the immutable filtered dispatch-state snapshot model."""

import pytest

from agentic_devtools.cli.ci.dispatch_state_codec import DispatchStateEnvelope, DispatchStateSnapshot


def test_snapshot_is_frozen_and_copies_nested_records() -> None:
    legacy = {"key": {"nested": [{"value": 1}]}}
    canonical = {"identity": {"metadata": {"nested": [2]}}}
    envelope = DispatchStateEnvelope(2, legacy, canonical)
    snapshot = DispatchStateSnapshot(legacy, canonical, envelope)

    legacy["key"]["nested"][0]["value"] = 3
    canonical["identity"]["metadata"]["nested"].append(4)

    assert snapshot.records["key"]["nested"][0]["value"] == 1
    assert snapshot.canonical_records["identity"]["metadata"]["nested"] == (2,)
    assert snapshot.envelope.canonical_records["identity"]["metadata"]["nested"] == (2,)
    with pytest.raises(TypeError):
        snapshot.records["key"]["nested"][0]["value"] = 5  # type: ignore[index]
