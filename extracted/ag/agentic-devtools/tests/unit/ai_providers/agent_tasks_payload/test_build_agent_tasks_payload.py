import json
from pathlib import Path

from agentic_devtools.ai_providers import (
    AGENT_TASKS_ENDPOINT_TEMPLATE,
    AGENT_TASKS_HTTP_METHOD,
    REQUIRED_CUSTOM_AGENT,
    build_agent_tasks_payload,
)

_FIXTURE_ROOT = Path(__file__).resolve().parents[3] / "fixtures" / "agent_tasks" / "payload"


def test_build_agent_tasks_payload_matches_golden_request() -> None:
    expected = json.loads((_FIXTURE_ROOT / "golden-request-valid.json").read_text(encoding="utf-8"))

    actual = build_agent_tasks_payload(
        expected["prompt"],
        expected["model"],
        expected["base_ref"],
        expected["head_ref"],
    )

    assert actual == expected
    assert list(actual) == [
        "prompt",
        "custom_agent",
        "model",
        "base_ref",
        "head_ref",
        "create_pull_request",
    ]
    assert actual["custom_agent"] == REQUIRED_CUSTOM_AGENT
    assert actual["create_pull_request"] is False
    assert isinstance(actual["prompt"], str) and actual["prompt"]
    assert isinstance(actual["custom_agent"], str) and actual["custom_agent"]
    assert isinstance(actual["model"], str) and actual["model"]
    assert isinstance(actual["base_ref"], str) and actual["base_ref"]
    assert isinstance(actual["head_ref"], str) and actual["head_ref"]
    assert type(actual["create_pull_request"]) is bool
    assert AGENT_TASKS_HTTP_METHOD == "POST"
    assert AGENT_TASKS_ENDPOINT_TEMPLATE.format(owner="octo", repo="demo") == "/agents/repos/octo/demo/tasks"


def test_build_agent_tasks_payload_relays_unicode_prompt_without_normalization() -> None:
    prompt = 'NFC: \u00e9 | NFD: e\u0301\n\n"quoted" [brackets]  repeated   spaces\ntrailing\n'

    payload = build_agent_tasks_payload(prompt, "gpt-5-mini", "main", "feature")
    decoded = json.loads(json.dumps(payload, ensure_ascii=False))["prompt"]

    assert decoded == prompt
