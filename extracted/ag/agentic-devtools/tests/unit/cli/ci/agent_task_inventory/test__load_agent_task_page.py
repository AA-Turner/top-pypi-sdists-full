"""Tests for single-page retrieval edge cases."""

import json
import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import _load_agent_task_page

PROVIDER = "agentic_devtools.cli.ci.github_provider._run_readonly_gh_command"


def test_successful_command_with_error_body_is_still_failure() -> None:
    response = subprocess.CompletedProcess(["gh"], 0, '{"status":500}', "")
    with patch(PROVIDER, return_value=response):
        result, count = _load_agent_task_page("endpoint", page=1, pr_number=42)
    assert count is None
    assert result.http_status == 500
    assert result.failure_category == "provider_unavailable"


@pytest.mark.parametrize(
    ("attributes", "payload_status", "diagnostic", "category"),
    [
        ({"status_code": 200}, 404, 404, "http_not_found"),
        ({"http_status": 404, "status_code": 403}, 200, 404, "http_not_found"),
        ({"status_code": 200}, "success", 200, "malformed_response"),
        ({"http_status": "bad", "status_code": 200}, 404, 404, "http_not_found"),
    ],
)
def test_page_status_precedence(
    attributes: dict[str, object], payload_status: object, diagnostic: int, category: str
) -> None:
    response = subprocess.CompletedProcess(["gh"], 0, json.dumps({"tasks": [], "status": payload_status}), "")
    for name, value in attributes.items():
        setattr(response, name, value)
    with patch(PROVIDER, return_value=response):
        result, count = _load_agent_task_page("endpoint", page=1, pr_number=42)
    assert count is None
    assert result.http_status == diagnostic
    assert result.failure_category == category
    assert not result.complete


@pytest.mark.parametrize("key", ["error", "errors", "message"])
def test_page_error_markers_fail_closed(key: str) -> None:
    response = subprocess.CompletedProcess(["gh"], 0, json.dumps({"tasks": [], key: None}), "")
    with patch(PROVIDER, return_value=response):
        result, count = _load_agent_task_page("endpoint", page=1, pr_number=42)
    assert count is None
    assert result.failure_category == "malformed_response"
    assert not result.complete


def test_reads_structured_status_from_exception() -> None:
    failure = PermissionError("denied")
    setattr(failure, "status_code", 403)
    with patch(PROVIDER, side_effect=failure):
        result, count = _load_agent_task_page("endpoint", page=1, pr_number=42)
    assert count is None
    assert result.http_status == 403
    assert result.failure_category == "permission"


def test_empty_successful_page_preserves_raw_count() -> None:
    response = subprocess.CompletedProcess(["gh"], 0, "[]", "")
    setattr(response, "status_code", 200)
    with patch(PROVIDER, return_value=response):
        result, count = _load_agent_task_page("endpoint", page=1, pr_number=42)
    assert result.complete
    assert count == 0


def test_empty_page_with_null_transport_status_fails_closed() -> None:
    response = subprocess.CompletedProcess(["gh"], 0, "[]", "")
    setattr(response, "status_code", None)
    with patch(PROVIDER, return_value=response):
        result, count = _load_agent_task_page("endpoint", page=1, pr_number=42)
    assert count is None
    assert result.failure_category == "malformed_response"
    assert result.availability == "unavailable"
