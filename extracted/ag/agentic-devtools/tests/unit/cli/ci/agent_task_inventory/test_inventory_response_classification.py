"""Tests for Agent Tasks page response classification."""

import json
import subprocess
from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import _classify_agent_task_page_response


def _response(payload: object, *, returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(
        args=["gh", "api"],
        returncode=returncode,
        stdout=json.dumps(payload),
        stderr="",
    )


def test_classifies_top_level_list_response() -> None:
    tasks = [{"id": "task-1"}]

    assert _classify_agent_task_page_response(_response(tasks), pr_number=42) == tasks


def test_classifies_tasks_object_response() -> None:
    tasks = [{"id": "task-1"}]

    assert _classify_agent_task_page_response(_response({"tasks": tasks}), pr_number=42) == tasks


def test_classifies_valid_empty_response() -> None:
    assert _classify_agent_task_page_response(_response({"tasks": []}), pr_number=42) == []


@pytest.mark.parametrize("key", ["error", "errors", "message"])
@pytest.mark.parametrize("value", [None, "", False, [], {}])
def test_rejects_error_markers_regardless_of_value(key: str, value: object) -> None:
    assert _classify_agent_task_page_response(_response({"tasks": [], key: value}), pr_number=42) is None


@pytest.mark.parametrize("status", [200, 204, 299, "200", "204"])
def test_accepts_success_body_status(status: int | str) -> None:
    assert _classify_agent_task_page_response(_response({"tasks": [], "status": status}), pr_number=42) == []


@pytest.mark.parametrize("status", [None, True, 99, 600, 404.0, "success", "failed", "", "٤٠٤", [], {}])
def test_rejects_malformed_body_status(status: object) -> None:
    assert _classify_agent_task_page_response(_response({"tasks": [], "status": status}), pr_number=42) is None


@pytest.mark.parametrize(
    ("transport", "body_status"),
    [
        ({"status_code": 200}, 404),
        ({"status_code": 404}, 200),
        ({"http_status": "bad", "status_code": 200}, 404),
        ({"status_code": 200}, "ok"),
        ({"status": 302}, None),
        ({"status_code": None}, 200),
        ({"response": SimpleNamespace(status_code=404)}, 200),
    ],
)
def test_rejects_any_bad_status_candidate(transport: dict[str, object], body_status: object) -> None:
    response = _response({"tasks": [], "status": body_status})
    for name, value in transport.items():
        setattr(response, name, value)
    assert _classify_agent_task_page_response(response, pr_number=42) is None


@pytest.mark.parametrize("payload", [None, {}, {"tasks": None}, {"tasks": "not-a-list"}])
def test_rejects_malformed_payload_shapes(payload: object) -> None:
    assert _classify_agent_task_page_response(_response(payload), pr_number=42) is None


def test_rejects_nonzero_command_result(caplog: pytest.LogCaptureFixture) -> None:
    response = _response([{"id": "task-1"}], returncode=1)

    assert _classify_agent_task_page_response(response, pr_number=42) is None
    assert "PR #42: Agent Tasks REST inventory exited with code 1" in caplog.text


def test_malformed_json_raises_for_loader_mapping() -> None:
    response = subprocess.CompletedProcess(args=["gh", "api"], returncode=0, stdout="{", stderr="")

    with pytest.raises(json.JSONDecodeError):
        _classify_agent_task_page_response(response, pr_number=42)
