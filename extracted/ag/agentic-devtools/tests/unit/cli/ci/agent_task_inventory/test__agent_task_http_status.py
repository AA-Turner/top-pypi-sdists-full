"""Tests for structured HTTP status extraction."""

from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.agent_task_inventory import _agent_task_http_status


@pytest.mark.parametrize("attribute", ["http_status", "status_code", "status"])
@pytest.mark.parametrize("status", [401, "403"])
def test_accepts_structured_attributes(attribute, status) -> None:
    assert _agent_task_http_status(SimpleNamespace(**{attribute: status})) == int(status)


@pytest.mark.parametrize("status", [None, True, False, 99, 600, 404.0, "not-404", "٤٠٤", ""])
def test_ignores_invalid_structured_status(status) -> None:
    assert _agent_task_http_status(SimpleNamespace(status_code=status, stdout="")) is None


@pytest.mark.parametrize("stdout", ["", "{", "null", "[]", 42, None])
def test_ignores_malformed_or_absent_json(stdout) -> None:
    assert _agent_task_http_status(SimpleNamespace(stdout=stdout)) is None


def test_explicit_attribute_precedes_json() -> None:
    assert _agent_task_http_status(SimpleNamespace(status_code=403, stdout='{"status":404}')) == 403


def test_reads_json_status() -> None:
    assert _agent_task_http_status(SimpleNamespace(stdout='{"status":"404"}')) == 404


def test_reads_status_from_nested_response() -> None:
    exception = RuntimeError("request failed")
    setattr(exception, "response", SimpleNamespace(status_code=403))
    assert _agent_task_http_status(exception) == 403


def test_direct_status_precedes_nested_response() -> None:
    response = SimpleNamespace(status_code=401, response=SimpleNamespace(status_code=403))
    assert _agent_task_http_status(response) == 401
