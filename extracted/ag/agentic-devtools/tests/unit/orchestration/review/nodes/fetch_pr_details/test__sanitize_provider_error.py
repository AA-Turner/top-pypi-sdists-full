from __future__ import annotations

import subprocess

import pytest

from agentic_devtools.orchestration.review.nodes.fetch_pr_details import _sanitize_provider_error


@pytest.mark.parametrize(
    ("error", "expected"),
    [
        (RuntimeError("token missing: private-value"), "credentials are missing"),
        (RuntimeError("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT is not set"), "credentials are missing"),
        (RuntimeError("HTTP 403"), "authorization failed"),
        (RuntimeError("HTTP 403 forbidden"), "authorization failed"),
        (RuntimeError("HTTP 404"), "not found"),
        (RuntimeError("HTTP 404 not found"), "not found"),
        (RuntimeError("HTTP 429 rate limit"), "rate limited"),
        (RuntimeError("processed 1429 rows"), "verify provider settings"),
        (RuntimeError("processed 403 rows"), "verify provider settings"),
        (RuntimeError("loaded 404 records"), "verify provider settings"),
        (RuntimeError("path is required"), "verify provider settings"),
        (RuntimeError("429 - too many requests"), "rate limited"),
        (RuntimeError("HTTP 503 service unavailable"), "temporarily unavailable"),
        (RuntimeError("processed 5030 rows"), "verify provider settings"),
        (subprocess.TimeoutExpired("gh", 1), "timed out"),
        (RuntimeError("malformed provider response"), "malformed pull-request details"),
        (RuntimeError("unexpected failure"), "verify provider settings"),
    ],
)
def test_sanitize_provider_error_classifies_without_exposing_details(error, expected) -> None:
    result = _sanitize_provider_error(error)

    assert expected in result
    assert "private-value" not in result


def test_sanitize_provider_error_handles_system_exit() -> None:
    result = _sanitize_provider_error(SystemExit("token missing"))

    assert "credentials are missing" in result
