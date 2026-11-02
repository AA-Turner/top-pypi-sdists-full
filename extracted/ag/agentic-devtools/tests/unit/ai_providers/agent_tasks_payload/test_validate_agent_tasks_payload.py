import json
from pathlib import Path

import pytest

from agentic_devtools.ai_providers import REQUIRED_CUSTOM_AGENT, validate_agent_tasks_payload

_FIXTURE_ROOT = Path(__file__).resolve().parents[3] / "fixtures" / "agent_tasks" / "payload"
_AVAILABILITY_EVIDENCE_PATH = (
    Path(__file__).resolve().parents[3] / "fixtures" / "ai_providers" / "availability" / "evidence.json"
)
_PROBE_EVIDENCE_PATH = _FIXTURE_ROOT / "probe-response-evidence.json"


def _valid_payload() -> dict[str, object]:
    return json.loads((_FIXTURE_ROOT / "golden-request-valid.json").read_text(encoding="utf-8"))


def test_validate_agent_tasks_payload_accepts_golden_request() -> None:
    validate_agent_tasks_payload(_valid_payload())


@pytest.mark.parametrize(
    "fixture_name",
    [
        "golden-request-invalid-model.json",
        "golden-request-invalid-agent.json",
        "golden-request-nonexistent-base-ref.json",
    ],
)
def test_validation_order_fixtures_preserve_recorded_remote_outcomes(
    fixture_name: str,
) -> None:
    payload = json.loads((_FIXTURE_ROOT / fixture_name).read_text(encoding="utf-8"))
    recorded = json.loads(_PROBE_EVIDENCE_PATH.read_text(encoding="utf-8"))[fixture_name]
    available_matrix = json.loads(_AVAILABILITY_EVIDENCE_PATH.read_text(encoding="utf-8"))["matrix"]

    if fixture_name != "golden-request-invalid-agent.json":
        validate_agent_tasks_payload(payload)
    assert recorded["status_code"] in {400, 412}
    assert recorded["status_code"] == recorded["expected_status_code"]
    assert recorded["task_count_delta"] == 0
    assert recorded["credit_count_delta"] == 0
    assert recorded["new_task_ids"] == []
    assert recorded["model"] == payload["model"]
    if fixture_name != "golden-request-invalid-model.json":
        assert available_matrix[payload["model"]] == "available"
    if payload["custom_agent"] != REQUIRED_CUSTOM_AGENT:
        assert fixture_name == "golden-request-invalid-agent.json"


@pytest.mark.parametrize(
    "mutator",
    [
        lambda payload: payload.pop("head_ref"),
        lambda payload: payload.pop("create_pull_request"),
        lambda payload: payload.update({"unexpected": True}),
    ],
)
def test_validate_agent_tasks_payload_rejects_missing_or_extra_fields(mutator) -> None:
    payload = _valid_payload()
    mutator(payload)

    with pytest.raises(ValueError):
        validate_agent_tasks_payload(payload)


def test_validate_agent_tasks_payload_rejects_non_mapping() -> None:
    with pytest.raises(TypeError, match="payload must be a mapping"):
        validate_agent_tasks_payload([])  # type: ignore[arg-type]


def test_validate_agent_tasks_payload_does_not_default_or_coerce_create_pull_request() -> None:
    for value in [True, 1, "false"]:
        payload = _valid_payload()
        payload["create_pull_request"] = value

        with pytest.raises((TypeError, ValueError)):
            validate_agent_tasks_payload(payload)
