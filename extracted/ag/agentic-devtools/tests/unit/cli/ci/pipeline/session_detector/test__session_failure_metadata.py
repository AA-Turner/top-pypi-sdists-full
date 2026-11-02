from types import SimpleNamespace

import pytest

from agentic_devtools.cli.ci.pipeline.session_detector import _session_failure_metadata


def test_classifies_explicit_http_status() -> None:
    error = RuntimeError("provider unavailable")
    error.__dict__["status_code"] = 404
    category, status = _session_failure_metadata(error)
    assert category.value == "http_not_found"
    assert status == 404


def test_classifies_unstructured_provider_failure() -> None:
    category, status = _session_failure_metadata(RuntimeError("offline"))
    assert category.value == "provider_unavailable"
    assert status is None


@pytest.mark.parametrize("status", [404, 401, 403, 500])
def test_does_not_infer_root_cause_from_error_text(status: int) -> None:
    category, numeric_status = _session_failure_metadata(RuntimeError(f"HTTP {status}"))
    assert category.value == "provider_unavailable"
    assert numeric_status is None


@pytest.mark.parametrize(
    ("status", "category"), [(401, "authentication"), (403, "permission"), (500, "provider_unavailable")]
)
def test_prefers_structured_status(status: int, category: str) -> None:
    error = RuntimeError("HTTP 404")
    setattr(error, "status_code", status)
    result_category, result_status = _session_failure_metadata(error)
    assert result_category.value == category
    assert result_status == status


def test_reads_response_status_without_accepting_boolean_status() -> None:
    error = RuntimeError("offline")
    setattr(error, "status_code", True)
    setattr(error, "response", SimpleNamespace(status_code=403))
    category, status = _session_failure_metadata(error)
    assert category.value == "permission"
    assert status == 403
