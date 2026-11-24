"""Replicate Veo 3.1 only ever receives resolution/duration values it accepts.

system_error 64269738 / c7c98b1b (2026-11-10): Replicate answered 422 —
``duration`` must be 4/6/8 and ``resolution`` must be 720p/1080p — because the
google/veo-3.1* offerings declared no ``accepts`` vocabulary, so the caller's
value (5s, 480p, ...) went out untouched. The offerings now declare
``accepts`` (catalog data, ai.offering.override.params); this pins that the
control engine snaps duration to the nearest accepted value and drops an
unaccepted resolution (loud Adjustment) instead of sending it.
"""

from __future__ import annotations

import pytest

from matrx_ai.catalog.host_catalog import CatalogModel, build_catalog_call_profile

VEO_RULES = {
    "resolution": {
        "accepts": ["720p", "1080p"],
        "supported": True,
        "ui_values": ["720p", "1080p"],
    },
    "duration_seconds": {
        "accepts": [4, 6, 8],
        "supported": True,
        "ui_values": [4, 6, 8],
        "provider_key": "duration",
    },
}


def _controls(rules):
    model = CatalogModel(
        {
            "id": "veo",
            "name": "google/veo-3.1-fast",
            "wire_format": "replicate_video",
            "control_rules": rules,
        }
    )
    return build_catalog_call_profile(model).controls


@pytest.mark.parametrize(
    ("asked", "sent"),
    [(5, 6), (10, 8), (1, 4), (6, 6)],
)
def test_duration_is_snapped_to_an_accepted_value(asked, sent):
    params, _ = _controls(VEO_RULES).outbound({"duration_seconds": asked}, context={})
    assert params["duration"] == sent


@pytest.mark.parametrize("asked", ["480p", "4k"])
def test_unaccepted_resolution_is_never_sent_and_is_voiced(asked):
    params, adjustments = _controls(VEO_RULES).outbound({"resolution": asked}, context={})
    assert "resolution" not in params
    assert any(a.key == "resolution" and a.action == "dropped" for a in adjustments)


def test_accepted_values_pass_through():
    params, adjustments = _controls(VEO_RULES).outbound(
        {"duration_seconds": 8, "resolution": "1080p"}, context={}
    )
    assert params == {"duration": 8, "resolution": "1080p"}
    assert adjustments == []


def test_without_accepts_the_bad_value_would_go_out():
    """The pre-fix catalog shape: proves the test above is the load-bearing one."""
    bare = {"duration_seconds": {"supported": True, "provider_key": "duration"}}
    params, _ = _controls(bare).outbound({"duration_seconds": 5}, context={})
    assert params["duration"] == 5
