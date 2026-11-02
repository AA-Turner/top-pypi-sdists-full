"""Tests for retry integration in GitHubActionsProvider."""

import json
import subprocess
from types import SimpleNamespace
from unittest.mock import Mock, patch

import pytest

from agentic_devtools.cli.ci import github_provider
from agentic_devtools.cli.ci.cooldown import CooldownRecord
from agentic_devtools.cli.ci.exceptions import ProviderRateLimitError
from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider, _gh_api
from agentic_devtools.cli.ci.read_token_pool import ReadCredential, ReadTokenPool
from agentic_devtools.cli.ci.retry import RetryableError

_DEFAULT = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
_TEAM = "TEAM_SWICA_CLASSIC_REPO_WORKFLOW_PAT"


class TestRetryIntegration:
    """Tests verifying provider methods use retry_with_backoff and honor rate limits."""

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_retries_on_rate_limit(self, mock_run_safe, mock_sleep) -> None:
        """Provider raises ProviderRateLimitError after exhausting retries on rate limit."""

        class _RateLimitResult:
            returncode = 1
            stdout = ""
            stderr = "HTTP 429: rate limit exceeded"

        mock_run_safe.return_value = _RateLimitResult()

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(ProviderRateLimitError):
            provider.list_pr_files(42)

        # Should have retried (default 5 retries + 1 initial = 6 calls)
        assert mock_run_safe.call_count == 6

    @patch("agentic_devtools.cli.ci.retry.time.sleep")
    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_retries_on_server_error(self, mock_run_safe, mock_sleep) -> None:
        """Provider retries on 500/502/503/504 errors."""

        class _ServerError:
            returncode = 1
            stdout = ""
            stderr = "502 Bad Gateway"

        mock_run_safe.return_value = _ServerError()

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(RetryableError) as exc_info:
            provider.list_reviews(1)
        assert exc_info.value.is_rate_limit is False

        assert mock_run_safe.call_count == 6

    @patch("agentic_devtools.cli.ci.github_provider.run_safe")
    def test_non_retryable_error_propagates(self, mock_run_safe) -> None:
        """Non-retryable errors (e.g., 404) propagate immediately."""

        class _NotFoundResult:
            returncode = 1
            stdout = ""
            stderr = "HTTP 404: Not Found"

        mock_run_safe.return_value = _NotFoundResult()

        provider = GitHubActionsProvider(repo="owner/repo")
        with pytest.raises(RuntimeError, match="GitHub API error"):
            provider.list_pr_files(999)

        assert mock_run_safe.call_count == 1


def test_inventory_deadline_bounds_credential_failover(monkeypatch: pytest.MonkeyPatch) -> None:
    first = ReadCredential("FIRST_PAT", "first-token", "first")
    second = ReadCredential("SECOND_PAT", "second-token", "second")
    pool = Mock()
    pool.repo = "o/r"
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    selected: list[tuple[str, set[str]]] = []
    credentials = iter([first, second, None])

    def select(resource: str, *, excluded: set[str], **_kwargs: object) -> ReadCredential | None:
        selected.append((resource, set(excluded)))
        return next(credentials)

    pool.select.side_effect = select
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda **_kwargs: pool)
    now = [0.0]
    timeouts: list[int] = []

    def run_safe(*_args, timeout: int, **_kwargs) -> SimpleNamespace:
        timeouts.append(timeout)
        now[0] += 30 if len(timeouts) == 1 else 90
        return SimpleNamespace(
            returncode=1,
            stdout="HTTP/1.1 403 Forbidden\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n",
            stderr="",
        )

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=run_safe) as mock_run_safe,
        pytest.raises(github_provider._InventoryDeadlineExceeded),
    ):
        _gh_api(
            "/repos/o/r",
            timeout_seconds=150,
            _deadline=120.0,
            _monotonic=lambda: now[0],
        )

    assert timeouts == [120, 90]
    assert now[0] == 120.0
    assert selected == [
        ("rest", set()),
        ("rest", {first.secret_name}),
    ]
    assert mock_run_safe.call_count == 2
    assert pool.mark_rate_limited.call_count == 2


@pytest.mark.parametrize(("now", "expected_selections"), [(120.0, 0), (119.5, 1)])
def test_inventory_deadline_prevents_subprocess_without_one_second_remaining(
    monkeypatch: pytest.MonkeyPatch,
    now: float,
    expected_selections: int,
) -> None:
    credential = ReadCredential("FIRST_PAT", "first-token", "first")
    pool = Mock()
    pool.repo = "o/r"
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    pool.select.return_value = credential
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda **_kwargs: pool)

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe") as run_safe,
        pytest.raises(github_provider._InventoryDeadlineExceeded),
    ):
        _gh_api("/repos/o/r", _deadline=120.0, _monotonic=lambda: now)

    assert pool.select.call_count == expected_selections
    run_safe.assert_not_called()


def test_inventory_deadline_translates_expired_subprocess_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    pool = Mock()
    pool.repo = "o/r"
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    pool.select.return_value = ReadCredential("FIRST_PAT", "first-token", "first")
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda **_kwargs: pool)
    now = [0.0]

    def run_safe(command: list[str], *, timeout: int, **_kwargs) -> None:
        assert timeout == 10
        now[0] = 10.0
        raise subprocess.TimeoutExpired(command, timeout)

    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=run_safe) as mock_run_safe,
        pytest.raises(github_provider._InventoryDeadlineExceeded),
    ):
        _gh_api(
            "/repos/o/r",
            timeout_seconds=20,
            _deadline=10.0,
            _monotonic=lambda: now[0],
        )

    mock_run_safe.assert_called_once()
    assert pool.select.call_count == 1
    assert pool.select.call_args.args == ("rest",)
    pool.mark_rate_limited.assert_not_called()


def test_gh_api_without_deadline_preserves_read_token_failover(monkeypatch: pytest.MonkeyPatch) -> None:
    first = ReadCredential("FIRST_PAT", "first-token", "first")
    second = ReadCredential("SECOND_PAT", "second-token", "second")
    pool = Mock()
    pool.repo = "o/r"
    pool.default_token = "default-token"
    pool.default_identity = "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT"
    pool.default_is_active = False
    selected: list[tuple[str, set[str]]] = []
    credentials = iter([first, second, None])

    def select(resource: str, *, excluded: set[str]) -> ReadCredential | None:
        selected.append((resource, set(excluded)))
        return next(credentials)

    pool.select.side_effect = select
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda: pool)
    limited = SimpleNamespace(
        returncode=1,
        stdout="HTTP/1.1 403 Forbidden\nRetry-After: 45\nX-RateLimit-Remaining: 0\n\n",
        stderr="",
    )
    success = SimpleNamespace(returncode=0, stdout="{}", stderr="")
    with (
        patch.dict(
            "os.environ",
            {
                "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT": "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": "DEFAULT_CLASSIC_REPO_WORKFLOW_PAT",
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=[limited, limited, success]) as run_safe,
    ):
        assert _gh_api("/repos/o/r", timeout_seconds=37) == "{}"

    assert [call.kwargs["env"]["GH_TOKEN"] for call in run_safe.call_args_list] == [
        "first-token",
        "second-token",
        "default-token",
    ]
    assert [call.kwargs["timeout"] for call in run_safe.call_args_list] == [37, 37, 37]
    assert selected == [
        ("rest", set()),
        ("rest", {first.secret_name}),
        ("rest", {first.secret_name, second.secret_name}),
    ]
    assert pool.mark_rate_limited.call_count == 2
    assert [call.args[0] for call in pool.mark_rate_limited.call_args_list] == [
        first.secret_name,
        second.secret_name,
    ]
    assert all(call.args[1].is_rate_limit for call in pool.mark_rate_limited.call_args_list)
    assert pool.record_remaining.call_count == 3


def test_inventory_deadline_bounds_real_pool_cooldown_revalidation(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token"}))
    monkeypatch.setenv(_DEFAULT, "default-token")
    monkeypatch.setenv("GH_TOKEN", "default-token")
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", _DEFAULT)
    now = [0.0]
    expire_during_revalidation = [False]

    def run_safe(command: list[str], *, env: dict[str, str], **_kwargs: object) -> SimpleNamespace:
        if expire_during_revalidation[0]:
            now[0] = 30.0
        endpoint = command[2]
        payload = (
            {"login": "default-user" if env["GH_TOKEN"] == "default-token" else "team-user"}
            if endpoint == "/user"
            else {}
        )
        return SimpleNamespace(
            returncode=0,
            stdout=f"HTTP/1.1 200 OK\n\n{json.dumps(payload)}",
            stderr="",
        )

    with (
        patch(
            "agentic_devtools.cli.ci.cooldown.read_cooldowns",
            return_value={f"github:{_TEAM}": CooldownRecord(resume_at=0.0)},
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=run_safe) as runner,
    ):
        pool = github_provider._get_read_token_pool()
        assert isinstance(pool, ReadTokenPool)
        assert not pool._candidates
        expire_during_revalidation[0] = True
        runner.reset_mock()

        with pytest.raises(github_provider._InventoryDeadlineExceeded):
            _gh_api("/repos/o/r/inventory", _deadline=30.0, _monotonic=lambda: now[0])

    runner.assert_called_once()
    assert runner.call_args.args[0][2] == "/user"


def test_fractional_timeout_during_cached_revalidation_recovers_credential(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL", None)
    monkeypatch.setattr(github_provider, "_READ_TOKEN_POOL_REPO", "")
    monkeypatch.setenv("GITHUB_REPOSITORY", "o/r")
    monkeypatch.setenv("AGDT_GITHUB_SECRETS_JSON", json.dumps({_TEAM: "team-token"}))
    monkeypatch.setenv(_DEFAULT, "default-token")
    monkeypatch.setenv("GH_TOKEN", "default-token")
    monkeypatch.setenv("AI_PR_LOOP_CREDENTIAL_IDENTITY", _DEFAULT)
    monotonic = [0.0]
    wall_clock = [99.0]
    monkeypatch.setattr("agentic_devtools.cli.ci.read_token_pool.time.time", lambda: wall_clock[0])
    calls: list[tuple[str, str, int]] = []
    interrupt_revalidation = [True]

    def run_safe(command: list[str], *, env: dict[str, str], timeout: int, **_kwargs: object) -> SimpleNamespace:
        endpoint = command[2]
        token = env["GH_TOKEN"]
        calls.append((endpoint, token, timeout))
        if endpoint == "/user" and token == "team-token" and interrupt_revalidation[0]:
            interrupt_revalidation[0] = False
            monotonic[0] = 1.0
            raise subprocess.TimeoutExpired(command, timeout)
        payload = {"login": "default-user" if token == "default-token" else "team-user"}
        stdout = f"HTTP/1.1 200 OK\n\n{json.dumps(payload) if endpoint == '/user' else '{}'}"
        return SimpleNamespace(returncode=0, stdout=stdout, stderr="")

    with (
        patch(
            "agentic_devtools.cli.ci.cooldown.read_cooldowns",
            return_value={f"github:{_TEAM}": CooldownRecord(resume_at=100.0)},
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=run_safe) as runner,
    ):
        pool = github_provider._get_read_token_pool()
        assert isinstance(pool, ReadTokenPool)
        assert pool.candidate_names == ()
        calls.clear()
        runner.reset_mock()
        wall_clock[0] = 101.0

        with pytest.raises(github_provider._InventoryDeadlineExceeded):
            _gh_api(
                "/repos/o/r/inventory",
                timeout_seconds=10,
                _deadline=1.5,
                _monotonic=lambda: monotonic[0],
            )

        assert 1.5 - monotonic[0] == 0.5
        assert calls == [("/user", "team-token", 1)]
        assert _TEAM not in pool._excluded_pool_identities
        assert pool._cooldown_deadlines[_TEAM] == 100.0

        assert (
            _gh_api(
                "/repos/o/r/inventory",
                timeout_seconds=10,
                _deadline=11.0,
                _monotonic=lambda: monotonic[0],
            )
            == "{}"
        )

    assert pool.candidate_names == (_TEAM,)
    assert [endpoint for endpoint, token, _ in calls if token == "team-token"] == [
        "/user",
        "/user",
        "/repos/o/r",
        "/repos/o/r/inventory",
    ]
    assert runner.call_count == 4


def test_inventory_deadline_after_default_rate_limit_preserves_local_cooldown(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    pool = Mock()
    pool.repo = "o/r"
    pool.select.return_value = None
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = _DEFAULT
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda **_kwargs: pool)
    now = [0.0]

    def rate_limited(*_args: object, **_kwargs: object) -> SimpleNamespace:
        now[0] = 10.0
        return SimpleNamespace(
            returncode=1,
            stdout="HTTP/1.1 403 Forbidden\nRetry-After: 30\nX-RateLimit-Remaining: 0\n\n",
            stderr="",
        )

    with (
        patch.dict(
            "os.environ",
            {
                _DEFAULT: "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": _DEFAULT,
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=rate_limited) as runner,
        pytest.raises(github_provider._InventoryDeadlineExceeded),
    ):
        _gh_api("/repos/o/r", _deadline=10.0, _monotonic=lambda: now[0])

    runner.assert_called_once()
    pool.mark_rate_limited.assert_called_once()
    assert pool.mark_rate_limited.call_args.args[0] == _DEFAULT
    assert not pool.mark_rate_limited.call_args.kwargs
    pool.select.assert_called_once()


def test_inventory_deadline_after_server_error_prevents_credential_retry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    credential = ReadCredential(_TEAM, "team-token", "team-user")
    pool = Mock()
    pool.repo = "o/r"
    pool.select.return_value = credential
    pool.default_is_active = False
    pool.default_token = "default-token"
    pool.default_identity = _DEFAULT
    monkeypatch.setattr(github_provider, "_get_read_token_pool", lambda **_kwargs: pool)
    now = [0.0]

    def server_error(*_args: object, **_kwargs: object) -> SimpleNamespace:
        now[0] = 10.0
        return SimpleNamespace(returncode=1, stdout="HTTP/1.1 503 Service Unavailable\n\n", stderr="")

    with (
        patch.dict(
            "os.environ",
            {
                _DEFAULT: "default-token",
                "GH_TOKEN": "default-token",
                "AI_PR_LOOP_CREDENTIAL_IDENTITY": _DEFAULT,
            },
            clear=False,
        ),
        patch("agentic_devtools.cli.ci.github_provider.run_safe", side_effect=server_error) as runner,
        pytest.raises(github_provider._InventoryDeadlineExceeded),
    ):
        _gh_api("/repos/o/r", _deadline=10.0, _monotonic=lambda: now[0])

    runner.assert_called_once()
    pool.select.assert_called_once()
    pool.mark_rate_limited.assert_not_called()
