import json
from unittest.mock import patch

import pytest

from agentic_devtools.adapters.pull_request_details import _github_api_json
from agentic_devtools.cli.ci.credential_roles import DEFAULT_CLASSIC_REPO_WORKFLOW_PAT
from agentic_devtools.cli.ci.retry import RetryableError


def test_github_api_json_rejects_invalid_response() -> None:
    with patch("agentic_devtools.adapters.pull_request_details._gh_api", return_value="not-json"):
        with pytest.raises(RuntimeError, match="invalid JSON"):
            _github_api_json("/bad")


def test_github_api_json_uses_paginated_parser_for_paginated_calls() -> None:
    with (
        patch("agentic_devtools.adapters.pull_request_details._gh_api", return_value="[]"),
        patch(
            "agentic_devtools.adapters.pull_request_details._parse_paginated_json",
            return_value=[{"id": 1}],
        ) as parser,
    ):
        assert _github_api_json("/items", paginate=True) == [{"id": 1}]
    parser.assert_called_once_with("[]")


def test_github_api_json_rejects_invalid_paginated_response() -> None:
    with (
        patch("agentic_devtools.adapters.pull_request_details._gh_api", return_value="not-json"),
        patch(
            "agentic_devtools.adapters.pull_request_details._parse_paginated_json",
            side_effect=json.JSONDecodeError("bad json", "not-json", 0),
        ),
        patch("agentic_devtools.cli.ci.retry.time.sleep"),
    ):
        with pytest.raises(RuntimeError, match="invalid JSON"):
            _github_api_json("/bad", paginate=True)


def test_github_api_json_retries_transient_invalid_paginated_json() -> None:
    with (
        patch("agentic_devtools.adapters.pull_request_details._gh_api", return_value="[]"),
        patch(
            "agentic_devtools.adapters.pull_request_details._parse_paginated_json",
            side_effect=[json.JSONDecodeError("bad json", "[]", 0), [{"id": 1}]],
        ) as parser,
        patch("agentic_devtools.cli.ci.retry.time.sleep"),
    ):
        assert _github_api_json("/items", paginate=True) == [{"id": 1}]
    assert parser.call_count == 2


def test_github_api_json_retries_retryable_errors() -> None:
    with (
        patch(
            "agentic_devtools.adapters.pull_request_details._gh_api",
            side_effect=[RetryableError("temporary outage"), '{"ok": true}'],
        ) as gh_api,
        patch("agentic_devtools.cli.ci.retry.time.sleep"),
    ):
        assert _github_api_json("/items") == {"ok": True}
    assert gh_api.call_count == 2


def test_github_api_json_passes_the_configured_repository_token() -> None:
    with patch(
        "agentic_devtools.adapters.pull_request_details._gh_api",
        return_value='{"ok": true}',
    ) as gh_api:
        assert _github_api_json("/items") == {"ok": True}

    assert gh_api.call_args.kwargs["token"] == "test-workflow-token"
    assert gh_api.call_args.kwargs["credential_identity"] == DEFAULT_CLASSIC_REPO_WORKFLOW_PAT


def test_github_api_json_requires_the_configured_repository_token(monkeypatch) -> None:
    monkeypatch.delenv(DEFAULT_CLASSIC_REPO_WORKFLOW_PAT)
    with (
        patch("agentic_devtools.adapters.pull_request_details._gh_api") as gh_api,
        pytest.raises(RuntimeError, match=DEFAULT_CLASSIC_REPO_WORKFLOW_PAT),
    ):
        _github_api_json("/items")
    gh_api.assert_not_called()


def test_github_api_json_converts_exhausted_retryable_error_to_runtime_error() -> None:
    with (
        patch(
            "agentic_devtools.adapters.pull_request_details._gh_api",
            return_value="not-json",
        ) as gh_api,
        patch(
            "agentic_devtools.adapters.pull_request_details._parse_paginated_json",
            side_effect=json.JSONDecodeError("bad json", "not-json", 0),
        ),
        patch("agentic_devtools.cli.ci.retry.time.sleep"),
    ):
        with pytest.raises(RuntimeError, match="invalid JSON"):
            _github_api_json("/items", paginate=True)
    assert gh_api.call_count == 6


def test_github_api_json_shares_single_retry_budget_across_transport_and_parse_failures() -> None:
    """A transport RetryableError and a subsequent invalid-JSON response must share one retry budget."""
    with (
        patch(
            "agentic_devtools.adapters.pull_request_details._gh_api",
            side_effect=[RetryableError("temporary outage"), "not-json", "[]"],
        ) as gh_api,
        patch(
            "agentic_devtools.adapters.pull_request_details._parse_paginated_json",
            side_effect=[json.JSONDecodeError("bad json", "not-json", 0), [{"id": 1}]],
        ),
        patch("agentic_devtools.cli.ci.retry.time.sleep"),
    ):
        assert _github_api_json("/items", paginate=True) == [{"id": 1}]
    # Exactly three underlying calls (one transport retry + one parse retry), not 3 * 6.
    assert gh_api.call_count == 3
