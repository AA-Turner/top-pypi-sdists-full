import json
from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

from agentic_devtools.ai_providers import AGENT_TASKS_VALIDATION_ORDER, AgentTasksPayload

_FIXTURE_ROOT = Path(__file__).resolve().parents[3] / "fixtures" / "agent_tasks" / "payload"


def _fixture(name: str) -> dict[str, object]:
    return json.loads((_FIXTURE_ROOT / name).read_text(encoding="utf-8"))


def _payload_kwargs() -> dict[str, object]:
    return _fixture("golden-request-valid.json")


def test_agent_tasks_payload_is_frozen_and_matches_golden_fixture() -> None:
    payload = AgentTasksPayload(**_payload_kwargs())  # type: ignore[arg-type]

    assert payload.to_dict() == _fixture("golden-request-valid.json")
    assert AGENT_TASKS_VALIDATION_ORDER == ("model", "custom_agent", "base_ref")

    with pytest.raises(FrozenInstanceError):
        payload.prompt = "changed"  # type: ignore[misc]


def test_agent_tasks_payload_does_not_own_serialization_or_verification_gates() -> None:
    source = Path(__file__).resolve().parents[4] / "agentic_devtools" / "ai_providers" / "agent_tasks_payload.py"

    source_text = source.read_text(encoding="utf-8")
    assert not any(f"V{number}" in source_text for number in range(1, 7))
    assert "serialize_prompt" not in source_text
    assert "select_model" not in source_text
    assert "dispatch_policy" not in source_text


@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        ("prompt", "", ValueError),
        ("prompt", None, TypeError),
        ("model", "", ValueError),
        ("model", None, TypeError),
        ("base_ref", "", ValueError),
        ("base_ref", None, TypeError),
        ("head_ref", "", ValueError),
        ("head_ref", None, TypeError),
        ("custom_agent", 1, TypeError),
        ("custom_agent", "wrong-agent", ValueError),
        ("create_pull_request", True, ValueError),
        ("create_pull_request", 0, TypeError),
    ],
)
def test_agent_tasks_payload_rejects_invalid_field(field: str, value: object, error: type[Exception]) -> None:
    kwargs = _payload_kwargs()
    kwargs[field] = value

    with pytest.raises(error):
        AgentTasksPayload(**kwargs)  # type: ignore[arg-type]
