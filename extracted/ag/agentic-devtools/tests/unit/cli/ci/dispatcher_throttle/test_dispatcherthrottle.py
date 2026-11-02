"""Tests for the DispatcherThrottle class."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from agentic_devtools.cli.ci import dispatcher_throttle
from agentic_devtools.cli.ci.dispatcher_throttle import DispatcherThrottle


def _response(
    *,
    status: int = 200,
    headers: dict[str, str] | None = None,
    body: object | None = None,
    exit_code: int = 0,
    newline: str = "\r\n",
) -> subprocess.CompletedProcess[bytes]:
    reason = {200: "OK", 403: "Forbidden", 429: "Too Many Requests"}[status]
    # gh prints the status with LF and the server's headers with CRLF locally.
    header_block = f"HTTP/2.0 {status} {reason}\n"
    header_block += f"Content-Type: application/json; charset=utf-8{newline}"
    if headers:
        header_block += "".join(f"{name}: {value}{newline}" for name, value in headers.items())
    stderr = f"gh: {body if isinstance(body, str) else 'API request failed'}\n" if exit_code else ""
    payload = body if isinstance(body, str) else json.dumps(body if body is not None else {"workflow_runs": []})
    stdout = header_block + newline + payload
    return subprocess.CompletedProcess(["gh"], exit_code, stdout=stdout.encode("utf-8"), stderr=stderr.encode("utf-8"))


def test_retries_secondary_limit_using_fallback_when_primary_quota_remains(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    run = Mock(
        side_effect=[
            _response(
                status=403,
                headers={"X-RateLimit-Remaining": "42", "X-RateLimit-Reset": "1001"},
                body={"message": "You have exceeded a secondary rate limit."},
                exit_code=1,
            ),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)
    output = tmp_path / "github-output"

    throttled = DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(output),
    )

    assert not throttled
    assert output.read_text(encoding="utf-8") == "throttled=false\n"
    assert sleeps == [60]
    assert run.call_args_list[0].args[0] == [
        "gh",
        "api",
        "/repos/swai-factory/agentic-devtools/actions/workflows/ai-pr-loop-throttler.yml/runs?per_page=1&branch=main",
        "--include",
    ]
    run.assert_called()


def test_uses_pooled_runner_for_readonly_throttle_lookup(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from agentic_devtools.cli.ci import github_provider

    endpoint = (
        "/repos/swai-factory/agentic-devtools/actions/workflows/ai-pr-loop-throttler.yml/runs?per_page=1&branch=main"
    )
    response = subprocess.CompletedProcess(
        ["gh"],
        0,
        stdout='HTTP/2.0 200 OK\nContent-Type: application/json\n\n{"workflow_runs": []}',
        stderr="",
    )
    pooled_runner = Mock(return_value=response)
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT":"default"}')
    monkeypatch.setattr(github_provider, "_run_readonly_gh_command", pooled_runner)
    monkeypatch.setattr(dispatcher_throttle, "run_safe", Mock(side_effect=AssertionError("bypassed read pool")))
    output = tmp_path / "github-output"

    assert not DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(output),
    )

    pooled_runner.assert_called_once_with(
        ["api", endpoint, "--include"],
        resource="rest",
        return_rate_limit_result=True,
        runner=dispatcher_throttle.run_safe,
    )
    assert output.read_text(encoding="utf-8") == "throttled=false\n"


def test_cross_repository_throttle_lookup_retries_without_local_read_pool(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from agentic_devtools.cli.ci import github_provider

    pool = Mock()
    pool.repo = "owner/current"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_token = "default-token"
    pool.select.return_value = SimpleNamespace(secret_name="alternate", token="alternate-token")
    rate_limited_bytes = _response(
        status=403,
        headers={"X-RateLimit-Remaining": "42", "X-RateLimit-Reset": "1001"},
        body={"message": "You have exceeded a secondary rate limit."},
        exit_code=1,
    )
    rate_limited = subprocess.CompletedProcess(
        ["gh"],
        rate_limited_bytes.returncode,
        stdout=rate_limited_bytes.stdout.decode("utf-8"),
        stderr=rate_limited_bytes.stderr.decode("utf-8"),
    )
    successful_bytes = _response()
    successful = subprocess.CompletedProcess(
        ["gh"],
        successful_bytes.returncode,
        stdout=successful_bytes.stdout.decode("utf-8"),
        stderr=successful_bytes.stderr.decode("utf-8"),
    )
    runner = Mock(side_effect=[rate_limited, successful])
    sleeps: list[float] = []
    monkeypatch.setenv("GITHUB_REPOSITORY", "owner/current")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", "{}")
    monkeypatch.setenv("DEFAULT_CLASSIC_REPO_WORKFLOW_PAT", "default-token")
    monkeypatch.setenv("GH_TOKEN", "default-token")
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT")
    monkeypatch.setattr(github_provider, "_get_read_token_pool", Mock(return_value=pool))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", runner)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)
    output = tmp_path / "github-output"

    assert not DispatcherThrottle().check(repository="owner/other", default_branch="main", output_path=str(output))

    command = [
        "gh",
        "api",
        "/repos/owner/other/actions/workflows/ai-pr-loop-throttler.yml/runs?per_page=1&branch=main",
        "--include",
    ]
    assert runner.call_count == 2
    assert all(call.args[0] == command for call in runner.call_args_list)
    assert sleeps == [60]
    pool.select.assert_not_called()
    assert runner.call_args.kwargs["env"]["GH_TOKEN"] == "default-token"
    assert output.read_text(encoding="utf-8") == "throttled=false\n"


def test_pooled_non_rate_limit_error_uses_text_diagnostics(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from agentic_devtools.cli.ci import github_provider

    response = subprocess.CompletedProcess(
        ["gh"],
        1,
        stdout=(
            'HTTP/2.0 403 Forbidden\nx-ratelimit-remaining: 42\n\n{"message":"Resource not accessible by integration"}'
        ),
        stderr="gh: Resource not accessible by integration",
    )
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT":"default"}')
    monkeypatch.setattr(github_provider, "_run_readonly_gh_command", Mock(return_value=response))
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match="Resource not accessible by integration"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )
    assert not output.exists()


def test_pooled_rate_limit_fails_closed_with_scheduler_diagnostic(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    from agentic_devtools.cli.ci import github_provider

    error = github_provider.ProviderRateLimitError(is_rate_limit=True, credential_identity="TEAM_PAT")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", '{"DEFAULT_CLASSIC_REPO_WORKFLOW_PAT":"default"}')
    monkeypatch.setattr(github_provider, "_run_readonly_gh_command", Mock(side_effect=error))
    output = tmp_path / "github-output"

    with pytest.raises(github_provider.ProviderRateLimitError):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    assert not output.exists()


@pytest.mark.parametrize("newline", ["\r\n", "\n"])
def test_parses_include_response_without_verbose(monkeypatch: pytest.MonkeyPatch, newline: str) -> None:
    last_run = {"status": "completed", "conclusion": "success", "updated_at": "2026-10-15T12:00:00Z"}
    run = Mock(return_value=_response(body={"workflow_runs": [last_run]}, newline=newline))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)

    assert DispatcherThrottle()._lookup_last_run("owner/repo", "main") == last_run
    command = run.call_args.args[0]
    assert "--include" in command
    assert "--verbose" not in command
    assert run.call_args.kwargs == {"capture_output": True, "text": False, "shell": False}


@pytest.mark.parametrize("stdout", [None, b"", b"HTTP/2.0 200 OK\r\nContent-Type: application/json\r\n"])
def test_retries_response_without_body_separator(monkeypatch: pytest.MonkeyPatch, stdout: bytes | None) -> None:
    run = Mock(side_effect=[subprocess.CompletedProcess(["gh"], 0, stdout=stdout, stderr=None), _response()])
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    assert DispatcherThrottle()._lookup_last_run("owner/repo", "main") == {}
    assert sleeps == [60]
    assert run.call_count == 2


def test_retries_429_without_message_evidence(monkeypatch: pytest.MonkeyPatch) -> None:
    run = Mock(
        side_effect=[
            _response(status=429, headers={"Retry-After": "2"}, body={}, exit_code=1),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    assert DispatcherThrottle()._lookup_last_run("owner/repo", "main") == {}
    assert sleeps == [2]


def test_parses_headers_separately_from_body_and_stderr() -> None:
    header_block = "HTTP/2.0 403 Forbidden\nX-RateLimit-Remaining: 0\r\nUnexpected line\r\nRetry-After: 2"

    assert DispatcherThrottle._parse_diagnostics(header_block, "warning\n gh: Forbidden (HTTP 403)\n") == (
        403,
        {"x-ratelimit-remaining": "0", "retry-after": "2"},
        "gh: Forbidden (HTTP 403)",
    )


def test_uses_reset_after_primary_quota_is_exhausted(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    run = Mock(
        side_effect=[
            _response(
                status=403,
                headers={"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1700003600"},
                body={"message": "Forbidden"},
                exit_code=1,
            ),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1_700_000_000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(tmp_path / "github-output"),
    )

    assert sleeps == [3601]


def test_recognizes_zero_primary_quota_with_leading_zeroes(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    run = Mock(
        side_effect=[
            _response(
                status=403,
                headers={"X-RateLimit-Remaining": "00", "X-RateLimit-Reset": "1001"},
                body={"message": "Forbidden"},
                exit_code=1,
            ),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(tmp_path / "github-output"),
    )

    assert sleeps == [2]


@pytest.mark.parametrize(
    ("retry_after", "expected_delay"),
    [
        ("2", 2),
        ("Wed, 14 Oct 2026 23:13:20 GMT", 3600),
    ],
)
@pytest.mark.parametrize("status", [403, 429])
def test_honors_retry_after(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    retry_after: str,
    expected_delay: int,
    status: int,
) -> None:
    current_epoch = 1_792_016_000
    run = Mock(
        side_effect=[
            _response(
                status=status,
                headers={"Retry-After": retry_after, "X-RateLimit-Remaining": "42"},
                body={"message": "You have exceeded a secondary rate limit."},
                exit_code=1,
            ),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: current_epoch)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(tmp_path / "github-output"),
    )

    assert sleeps == [expected_delay]


@pytest.mark.parametrize(
    ("recovered_run", "expected_throttled"),
    [
        ({"workflow_runs": []}, False),
        (
            {
                "workflow_runs": [
                    {
                        "status": "completed",
                        "conclusion": "success",
                        "updated_at": datetime.fromtimestamp(1000 - 30, UTC).isoformat(),
                    }
                ]
            },
            True,
        ),
    ],
)
def test_retries_blank_successful_response_and_uses_recovered_run(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    recovered_run: dict[str, object],
    expected_throttled: bool,
) -> None:
    run = Mock(side_effect=[_response(body="", headers={"Retry-After": "2"}), _response(body=recovered_run)])
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)
    output = tmp_path / "github-output"

    throttled = DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(output),
    )

    assert throttled is expected_throttled
    assert output.read_text(encoding="utf-8") == f"throttled={str(expected_throttled).lower()}\n"
    assert run.call_count == 2
    assert sleeps == [2]


def test_retries_blank_response_until_final_allowed_attempt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    run = Mock(side_effect=[_response(body=" "), _response(body="\n"), _response()])
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(tmp_path / "github-output"),
    )

    assert run.call_count == dispatcher_throttle.MAX_ATTEMPTS
    assert sleeps == [60, 60]


def test_ignores_stderr_trace_headers_for_complete_include_response(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    response = _response()
    response.stderr = (
        b"< HTTP/2.0 301 Moved Permanently\n"
        b"< Content-Length: 256\n"
        b"< Retry-After: 3600\n"
        b"< X-RateLimit-Remaining: 0\n"
        b"<\n" + response.stderr
    )
    run = Mock(return_value=response)
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)
    output = tmp_path / "github-output"

    throttled = DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(output),
    )

    assert not throttled
    assert output.read_text(encoding="utf-8") == "throttled=false\n"
    run.assert_called_once()
    assert sleeps == []
    assert DispatcherThrottle._parse_diagnostics(
        "HTTP/2.0 200 OK\nContent-Type: application/json; charset=utf-8",
        response.stderr.decode("utf-8"),
    ) == (200, {"content-type": "application/json; charset=utf-8"}, None)


def test_retries_truncated_successful_response(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    body = '{"workflow_runs":'
    run = Mock(
        side_effect=[
            _response(body=body, headers={"Content-Length": str(len(body.encode("utf-8")) + 20)}),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    throttled = DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(tmp_path / "github-output"),
    )

    assert not throttled
    assert run.call_count == 2
    assert sleeps == [60]


def test_complete_crlf_response_is_not_classified_as_truncated(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    body = b'{\r\n  "workflow_runs": []\r\n}\r\n'
    run = Mock(
        return_value=subprocess.CompletedProcess(
            ["gh"],
            0,
            stdout=f"HTTP/2.0 200 OK\nContent-Length: {len(body)}\r\n\r\n".encode() + body,
            stderr=b"",
        )
    )
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    output = tmp_path / "github-output"

    assert not DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(output),
    )

    run.assert_called_once()
    assert run.call_args.kwargs["text"] is False
    assert output.read_text(encoding="utf-8") == "throttled=false\n"


def test_invalid_response_encoding_fails_closed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    run = Mock(return_value=subprocess.CompletedProcess(["gh"], 0, stdout=b"HTTP/2.0 200 OK\n\n\xff", stderr=b""))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match="throttle state is unknown.*scheduler wake-up was not handled"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    run.assert_called_once()
    assert not output.exists()


def test_retries_truncated_response_with_unbounded_content_length(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    run = Mock(
        side_effect=[
            _response(body="{}", headers={"Content-Length": "9" * 5000}),
            _response(),
        ]
    )
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    throttled = DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="main",
        output_path=str(tmp_path / "github-output"),
    )

    assert not throttled
    assert run.call_count == 2
    assert sleeps == [60]


@pytest.mark.parametrize(
    "content_length",
    [
        pytest.param("not-a-length", id="not-numeric"),
        pytest.param("１２３", id="non-ascii"),
        pytest.param("8", id="exact-length"),
        pytest.param("0008", id="leading-zeros"),
        pytest.param("7", id="shorter-than-body"),
        pytest.param("0" * 5000, id="many-leading-zeros"),
    ],
)
def test_does_not_retry_malformed_json_without_proven_truncation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    content_length: str,
) -> None:
    run = Mock(
        return_value=_response(
            body="not json",
            headers={"Content-Length": content_length},
        )
    )
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match="without a JSON response"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    run.assert_called_once()
    assert not output.exists()


def test_blank_and_rate_limit_responses_share_retry_budget(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    rate_limit_response = _response(
        status=403,
        headers={"X-RateLimit-Remaining": "1"},
        body={"message": "secondary rate limit"},
        exit_code=1,
    )
    run = Mock(side_effect=[_response(body=""), rate_limit_response, _response(body="")])
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match="throttle state is unknown.*scheduler wake-up was not handled"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    assert run.call_count == dispatcher_throttle.MAX_ATTEMPTS
    assert sleeps == [60, 60]
    assert not output.exists()


@pytest.mark.parametrize(
    ("last_run", "expected"),
    [
        ({"status": "in_progress", "updated_at": "1970-01-01T00:16:10"}, True),
        ({"status": "completed", "conclusion": "failure", "updated_at": "1970-01-01T00:16:10"}, False),
        (
            {
                "status": "completed",
                "conclusion": "success",
                "updated_at": datetime.fromtimestamp(1000 - 30, UTC).isoformat(),
            },
            True,
        ),
        (
            {
                "status": "completed",
                "conclusion": "success",
                "updated_at": datetime.fromtimestamp(1000 - 61, UTC).isoformat(),
            },
            False,
        ),
        ({"updated_at": "1970-01-01T00:16:10"}, True),
    ],
)
def test_throttle_decision_for_last_run(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, last_run: dict[str, object], expected: bool
) -> None:
    run = Mock(return_value=_response(body={"workflow_runs": [last_run]}))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    output = tmp_path / "github-output"

    throttled = DispatcherThrottle().check(
        repository="swai-factory/agentic-devtools",
        default_branch="feature/a",
        output_path=str(output),
    )

    assert throttled is expected
    assert output.read_text(encoding="utf-8") == f"throttled={str(expected).lower()}\n"
    assert run.call_args.args[0][-2].endswith("branch=feature%2Fa")


@pytest.mark.parametrize(
    ("repository", "default_branch", "message"),
    [
        ("owner/repo/extra", "main", "owner/repo"),
        ("/repo", "main", "owner/repo"),
        ("owner/repo", "", "default_branch"),
    ],
)
def test_validates_lookup_identifiers(tmp_path: Path, repository: str, default_branch: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        DispatcherThrottle().check(
            repository=repository,
            default_branch=default_branch,
            output_path=str(tmp_path / "github-output"),
        )


@pytest.mark.parametrize("remaining", ["42", "invalid"])
def test_fails_on_non_rate_limit_403(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, remaining: str) -> None:
    monkeypatch.setattr(
        dispatcher_throttle,
        "run_safe",
        Mock(
            return_value=_response(
                status=403,
                headers={"X-RateLimit-Remaining": remaining},
                body="gh: Resource not accessible by integration",
                exit_code=1,
            )
        ),
    )

    with pytest.raises(RuntimeError, match="Resource not accessible by integration"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(tmp_path / "github-output"),
        )


def test_fails_on_non_rate_limit_without_gh_diagnostic(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setattr(
        dispatcher_throttle,
        "run_safe",
        Mock(return_value=subprocess.CompletedProcess(["gh"], 1, stdout=b"", stderr=b"< HTTP/2.0 500 Error\n")),
    )

    with pytest.raises(RuntimeError, match="non-rate-limit API error"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(tmp_path / "github-output"),
        )


def test_fails_after_maximum_rate_limit_attempts(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    rate_limit_response = _response(
        status=403,
        headers={"X-RateLimit-Remaining": "1"},
        body={"message": "secondary rate limit"},
        exit_code=1,
    )
    run = Mock(return_value=rate_limit_response)
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    with pytest.raises(dispatcher_throttle.ProviderRateLimitError):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(tmp_path / "github-output"),
        )

    assert run.call_count == 3
    assert sleeps == [60, 60]


def test_fails_when_retry_delay_exceeds_retry_deadline(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    run = Mock(
        return_value=_response(
            status=403,
            headers={"Retry-After": "21000"},
            body={"message": "secondary rate limit"},
            exit_code=1,
        )
    )
    clock = iter([1000, 1001, 1002])
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: next(clock))
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)

    with pytest.raises(dispatcher_throttle.ProviderRateLimitError):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(tmp_path / "github-output"),
        )

    assert sleeps == []


def test_does_not_retry_early_when_retry_after_exceeds_numeric_range(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    run = Mock(
        return_value=_response(
            status=403,
            headers={"Retry-After": "9" * 400},
            body={"message": "secondary rate limit"},
            exit_code=1,
        )
    )
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", Mock())

    with pytest.raises(ValueError, match="timing"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(tmp_path / "github-output"),
        )

    run.assert_called_once()


@pytest.mark.parametrize(
    ("stdout", "message"),
    [
        ("not json", "without a JSON response"),
        ("[]", "invalid JSON response"),
        ("{}", "missing workflow_runs"),
        ('{"workflow_runs": {}}', "invalid workflow_runs"),
        ('{"workflow_runs": [null]}', "invalid workflow run"),
        ('{"workflow_runs": [{}]}', "invalid updated_at"),
    ],
)
def test_rejects_invalid_lookup_responses(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, stdout: str, message: str
) -> None:
    run = Mock(return_value=_response(body=stdout))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match=message):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    run.assert_called_once()
    assert not output.exists()


def test_fails_after_maximum_blank_response_attempts_without_output(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    run = Mock(return_value=_response(body=""))
    sleeps: list[float] = []
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", sleeps.append)
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match="throttle state is unknown.*scheduler wake-up was not handled"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    assert run.call_count == dispatcher_throttle.MAX_ATTEMPTS
    assert sleeps == [60, 60]
    assert not output.exists()


def test_fails_when_successful_response_retry_exceeds_retry_deadline(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    run = Mock(return_value=_response(body="", headers={"Retry-After": "21001"}))
    monkeypatch.setattr(dispatcher_throttle, "run_safe", run)
    monkeypatch.setattr(dispatcher_throttle.time, "time", lambda: 1000)
    monkeypatch.setattr(dispatcher_throttle.time, "sleep", Mock())
    output = tmp_path / "github-output"

    with pytest.raises(RuntimeError, match="exceeds the bounded retry window"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(output),
        )

    run.assert_called_once()
    assert not output.exists()


@pytest.mark.parametrize("updated_at", [5, "not-a-timestamp"])
def test_rejects_invalid_run_timestamp(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, updated_at: object) -> None:
    monkeypatch.setattr(
        dispatcher_throttle,
        "run_safe",
        Mock(return_value=_response(body={"workflow_runs": [{"updated_at": updated_at}]})),
    )

    with pytest.raises(RuntimeError, match="invalid updated_at"):
        DispatcherThrottle().check(
            repository="swai-factory/agentic-devtools",
            default_branch="main",
            output_path=str(tmp_path / "github-output"),
        )
    with pytest.raises(RuntimeError, match="invalid updated_at"):
        DispatcherThrottle()._is_throttled({"updated_at": updated_at})
