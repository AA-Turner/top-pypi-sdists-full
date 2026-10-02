"""row_hash_fixture.json（front / admin の Node 実装向け contract fixture）が SDK 実装と一致すること。"""
import json
import pathlib

from agenticstar_platform.audit.action_audit import _row_hash

FIXTURE = pathlib.Path(__file__).resolve().parents[2] / "agenticstar_platform" / "audit" / "row_hash_fixture.json"


def test_fixture_matches_implementation():
    data = json.loads(FIXTURE.read_text())
    assert data["cases"], "fixture must not be empty"
    for case in data["cases"]:
        assert _row_hash(case["fields"]) == case["row_hash"], case["name"]
    names = {c["name"] for c in data["cases"]}
    assert {"legacy_tool_access", "tool_effect_30", "gate_resolved_human", "delivery_acked_front", "numbers_normalized"} <= names
