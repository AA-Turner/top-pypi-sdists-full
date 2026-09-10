from __future__ import annotations

import hashlib
import http.server
import io
import json
import os
import socket
import stat
import threading
import subprocess
import sys
import textwrap
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest

from runlayer_cli import aiwatch_credential

_REQUEST_DEVICE_TOKEN = aiwatch_credential.request_device_token
_FINGERPRINT = hashlib.sha256(b"rlk_secret").hexdigest()


class _Response:
    def __init__(self, body: bytes) -> None:
        self.body = body

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def read(self, size: int = -1) -> bytes:
        return self.body if size < 0 else self.body[:size]


@pytest.fixture(autouse=True)
def helper_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: tmp_path))
    monkeypatch.setattr(
        aiwatch_credential,
        "read_managed_config",
        lambda: {"host": "https://t.example.com"},
    )
    monkeypatch.delenv(aiwatch_credential.HOST_ENV_VAR, raising=False)
    return tmp_path


def _write_credential(home: Path, value: str = "rlk_secret\n") -> Path:
    path = aiwatch_credential.credential_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value)
    return path


def _cache_path(home: Path) -> Path:
    return aiwatch_credential.token_cache_path(aiwatch_credential.credential_path(home))


def _write_cache(home: Path, payload: str | bytes) -> Path:
    path = _cache_path(home)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = payload.encode() if isinstance(payload, str) else payload
    path.write_bytes(data)
    path.chmod(0o600)
    return path


def _run_main_with_urlopen(
    monkeypatch: pytest.MonkeyPatch,
    urlopen: Callable[..., Any],
    *,
    monotonic: Callable[[], float] | None = None,
    started_at: float | None = None,
    clock: Callable[[], float] | None = None,
    client: str = "claude",
) -> int:
    def request(
        host: str,
        credential: str,
        *,
        budget: float,
    ) -> aiwatch_credential.DeviceToken:
        kwargs: dict[str, object] = {
            "urlopen": urlopen,
            "budget": budget,
        }
        if monotonic is not None:
            kwargs["monotonic"] = monotonic
        return _REQUEST_DEVICE_TOKEN(
            host,
            credential,
            **kwargs,  # type: ignore[arg-type]
        )

    monkeypatch.setattr(aiwatch_credential, "request_device_token", request)
    return aiwatch_credential.main(
        [client], started_at=started_at, clock=clock or time.time
    )


def test_cache_hit_prints_cached_token_without_request(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    cache = _write_cache(
        helper_home,
        json.dumps(
            {
                "token": "rlt_cached",
                "expires_at": now + 600,
                "credential_sha256": _FINGERPRINT,
            }
        ),
    )
    before = cache.read_bytes()
    monkeypatch.setattr(aiwatch_credential, "read_managed_config", lambda: {})

    exit_code = _run_main_with_urlopen(monkeypatch, pytest.fail, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_cached"
    assert captured.err == ""
    assert cache.read_bytes() == before


def test_success_prints_token_and_sends_exchange_request(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    requests: list[tuple[urllib.request.Request, float]] = []

    def urlopen(request: urllib.request.Request, *, timeout: float) -> _Response:
        requests.append((request, timeout))
        return _Response(
            b'{"token":"rlt_x","expires_at":"2026-09-04T10:00:00Z",'
            b'"expires_in_seconds":900}'
        )

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_x"
    assert captured.err == ""
    assert len(requests) == 1
    request, timeout = requests[0]
    assert request.full_url == (
        "https://t.example.com/api/v1/llm-gateway/device-tokens"
    )
    assert request.method == "POST"
    assert request.data == b"{}"
    assert request.get_header("Authorization") == "Bearer rlk_secret"
    assert request.get_header("Content-type") == "application/json"
    assert request.get_header("Accept") == "application/json"
    assert request.get_header("User-agent").startswith("runlayer-aiwatch/")
    assert 0 < timeout <= 5.0
    cache = _cache_path(helper_home)
    assert json.loads(cache.read_text()) == {
        "token": "rlt_x",
        "expires_at": int(now + 900),
        "credential_sha256": _FINGERPRINT,
    }
    if os.name == "posix":
        assert stat.S_IMODE(cache.stat().st_mode) == 0o600


@pytest.mark.parametrize(
    "remaining",
    [
        aiwatch_credential.CLIENT_REFRESH_INTERVAL_SECONDS,
        aiwatch_credential.CLIENT_REFRESH_INTERVAL_SECONDS - 1,
    ],
)
def test_cache_with_less_than_one_refresh_interval_left_mints_and_rewrites(
    remaining: int,
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    cache = _write_cache(
        helper_home,
        json.dumps(
            {
                "token": "rlt_cached",
                "expires_at": now + remaining,
                "credential_sha256": _FINGERPRINT,
            }
        ),
    )
    calls = 0

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        return _Response(b'{"token":"rlt_new","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_new"
    assert captured.err == ""
    assert calls == 1
    assert json.loads(cache.read_text()) == {
        "token": "rlt_new",
        "expires_at": int(now + 900),
        "credential_sha256": _FINGERPRINT,
    }


def test_cache_with_more_than_one_refresh_interval_left_is_served(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    _write_cache(
        helper_home,
        json.dumps(
            {
                "token": "rlt_cached",
                "expires_at": now + 241,
                "credential_sha256": _FINGERPRINT,
            }
        ),
    )

    exit_code = _run_main_with_urlopen(monkeypatch, pytest.fail, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_cached"
    assert captured.err == ""


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(b'{"token":"rlt_x","expires_at":1699999999}', id="expired"),
        pytest.param(b"not-json", id="not-json"),
        pytest.param(b"[]", id="not-object"),
        pytest.param(b'{"token":"rlt_x"}', id="missing-expiry"),
        pytest.param(b'{"token":"rlt_x","expires_at":"soon"}', id="string-expiry"),
        pytest.param(b'{"token":"rlt_x","expires_at":true}', id="boolean-expiry"),
        pytest.param(b'{"token":"a b","expires_at":9e18}', id="whitespace-token"),
        pytest.param(b'{"token":"","expires_at":9e18}', id="empty-token"),
        pytest.param(b"", id="empty"),
        pytest.param(
            b'{"token":"rlt_x","expires_at":9e18,"pad":"'
            + b"x" * aiwatch_credential.MAX_CREDENTIAL_BYTES
            + b'"}',
            id="oversized",
        ),
        pytest.param(b"\xff\xfe", id="invalid-utf8"),
    ],
)
def test_expired_or_malformed_cache_falls_through_to_mint(
    payload: bytes,
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    cache = _write_cache(helper_home, payload)
    calls = 0

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        return _Response(b'{"token":"rlt_new","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_new"
    assert captured.err == ""
    assert calls == 1
    assert json.loads(cache.read_text()) == {
        "token": "rlt_new",
        "expires_at": int(now + 900),
        "credential_sha256": _FINGERPRINT,
    }


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_symlinked_cache_is_ignored_and_never_followed(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    target = helper_home / "cache-target"
    target_content = json.dumps(
        {
            "token": "rlt_cached",
            "expires_at": now + 900,
            "credential_sha256": _FINGERPRINT,
        }
    ).encode()
    target.write_bytes(target_content)
    cache = _cache_path(helper_home)
    cache.symlink_to(target)
    calls = 0

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        return _Response(b'{"token":"rlt_new","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_new"
    assert captured.err == ""
    assert calls == 1
    assert stat.S_ISREG(cache.lstat().st_mode)
    assert target.read_bytes() == target_content


def test_mint_writes_cache_0600_without_leftover_temp_file(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    cache = _cache_path(helper_home)

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        return _Response(b'{"token":"rlt_new","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_new"
    assert captured.err == ""
    assert not list(cache.parent.glob(".llm-routing-token.*.tmp"))
    assert json.loads(cache.read_text()) == {
        "token": "rlt_new",
        "expires_at": int(now + 900),
        "credential_sha256": _FINGERPRINT,
    }
    if os.name == "posix":
        assert stat.S_IMODE(cache.stat().st_mode) == 0o600


def test_cache_write_failure_still_prints_token(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    cache = _cache_path(helper_home)

    def fail_write(
        _path: Path, _token: str, _expires_at: float, *, credential: str
    ) -> None:
        del credential
        raise PermissionError("denied")

    monkeypatch.setattr(aiwatch_credential, "write_token_cache", fail_write)

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        return _Response(b'{"token":"rlt_new","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_new"
    assert captured.err == (
        f"aiwatch credential claude: cannot write LLM routing token cache at "
        f"{cache} (PermissionError)\n"
    )


def test_claude_and_codex_share_one_cache(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_credential(helper_home)
    calls = 0

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        return _Response(b'{"token":"rlt_shared","expires_in_seconds":900}')

    claude_exit = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)
    claude_output = capsys.readouterr()
    codex_exit = _run_main_with_urlopen(
        monkeypatch,
        pytest.fail,
        clock=lambda: now,
        client="codex",
    )
    codex_output = capsys.readouterr()

    assert claude_exit == 0
    assert codex_exit == 0
    assert claude_output.out == "rlt_shared"
    assert codex_output.out == "rlt_shared"
    assert claude_output.err == ""
    assert codex_output.err == ""
    assert calls == 1
    cache = _cache_path(helper_home)
    assert list(cache.parent.glob(aiwatch_credential.TOKEN_CACHE_FILENAME)) == [cache]


def test_missing_credential_with_fresh_cache_still_fails(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    now = 1_700_000_000.0
    _write_cache(
        helper_home,
        json.dumps(
            {
                "token": "rlt_cached",
                "expires_at": now + 900,
                "credential_sha256": _FINGERPRINT,
            }
        ),
    )

    exit_code = _run_main_with_urlopen(monkeypatch, pytest.fail, clock=lambda: now)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert str(aiwatch_credential.credential_path(helper_home)) in captured.err


def test_budget_is_anchored_at_process_start(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Codex kills the helper timeout_ms after exec; startup eats the same budget."""
    _write_credential(helper_home)
    timeouts: list[float] = []

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        timeouts.append(timeout)
        return _Response(b'{"token":"rlt_x","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(
        monkeypatch, urlopen, started_at=time.time() - 4.0
    )
    assert exit_code == 0
    assert capsys.readouterr().out == "rlt_x"
    assert 0 < timeouts[0] <= 1.05
    _cache_path(helper_home).unlink()

    exit_code = _run_main_with_urlopen(
        monkeypatch, urlopen, started_at=time.time() - 60.0
    )
    assert exit_code == 0
    assert timeouts[1] == pytest.approx(aiwatch_credential._MIN_BUDGET_SECONDS)


def test_budget_charges_prepare_and_file_reads(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Truststore injection runs inside the kill window; the request budget must shrink by it."""
    _write_credential(helper_home)
    timeouts: list[float] = []
    clock_now = [1_000.0]

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        timeouts.append(timeout)
        return _Response(b'{"token":"rlt_x","expires_in_seconds":900}')

    def prepare() -> None:
        clock_now[0] += 3.0

    def request(
        host: str, credential: str, *, budget: float
    ) -> aiwatch_credential.DeviceToken:
        return _REQUEST_DEVICE_TOKEN(host, credential, urlopen=urlopen, budget=budget)

    monkeypatch.setattr(aiwatch_credential, "request_device_token", request)
    exit_code = aiwatch_credential.main(
        ["claude"],
        prepare=prepare,
        started_at=clock_now[0],
        clock=lambda: clock_now[0],
    )
    assert exit_code == 0
    assert 0 < timeouts[0] <= 2.05


def test_cache_minted_by_a_previous_credential_is_ignored(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A rotation between the helper's credential read and its cache write must not stick."""
    _write_credential(helper_home)
    now = time.time()
    _write_cache(
        helper_home,
        json.dumps(
            {
                "token": "rlt_old",
                "expires_at": now + 900,
                "credential_sha256": hashlib.sha256(b"rlk_previous").hexdigest(),
            }
        ),
    )
    mints: list[str] = []

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        mints.append("mint")
        return _Response(b'{"token":"rlt_new","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen, clock=lambda: now)

    assert exit_code == 0
    assert mints == ["mint"]
    assert (
        json.loads(_cache_path(helper_home).read_text())["credential_sha256"]
        == _FINGERPRINT
    )


def test_http_401_is_not_retried_and_redacts_credential(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    calls = 0

    def urlopen(request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        raise urllib.error.HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            {},
            io.BytesIO(b'{"detail":"unknown\\ndevice key rlk_secret"}'),
        )

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err.count("\n") == 1
    assert "HTTP 401" in captured.err
    assert "unknown device key" in captured.err
    assert "rlk_secret" not in captured.err
    assert calls == 1


def test_http_429_is_not_retried(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    calls = 0

    def urlopen(request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        raise urllib.error.HTTPError(
            request.full_url,
            429,
            "Too Many Requests",
            {},
            io.BytesIO(b'{"detail":"rate limited"}'),
        )

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "HTTP 429" in captured.err
    assert calls == 1


def test_transport_error_then_success_retries_once(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    timeouts: list[float] = []

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        timeouts.append(timeout)
        if len(timeouts) == 1:
            raise urllib.error.URLError("refused")
        return _Response(b'{"token":"rlt_x","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == "rlt_x"
    assert captured.err == ""
    assert len(timeouts) == 2
    assert 0 < timeouts[1] <= 5.0


def test_transport_error_twice_fails_after_one_retry(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    calls = 0

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        raise OSError("connection failed")

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "device token exchange failed" in captured.err
    assert calls == 2


def test_timeout_with_no_budget_left_is_not_retried(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    calls = 0
    times: Iterator[float] = iter((0.0, 0.0, 4.6))

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        nonlocal calls
        calls += 1
        raise socket.timeout()

    exit_code = _run_main_with_urlopen(
        monkeypatch,
        urlopen,
        monotonic=lambda: next(times),
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert calls == 1


@pytest.mark.parametrize(
    "value",
    [None, "a b\n", "", "x" * (aiwatch_credential.MAX_CREDENTIAL_BYTES + 1) + "\n"],
)
def test_missing_or_malformed_credential_fails_without_request(
    value: str | None,
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    if value is not None:
        _write_credential(helper_home, value)
    urlopen = pytest.fail

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert str(aiwatch_credential.credential_path(helper_home)) in captured.err


@pytest.mark.skipif(os.name != "posix", reason="requires POSIX symlinks")
def test_symlinked_credential_fails_without_request(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    target = helper_home / "target"
    target.write_text("rlk_secret\n")
    path = aiwatch_credential.credential_path(helper_home)
    path.parent.mkdir(parents=True)
    path.symlink_to(target)

    exit_code = _run_main_with_urlopen(monkeypatch, pytest.fail)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "symlink" in captured.err


@pytest.mark.parametrize(
    ("host", "allowed"),
    [
        ("http://t.example.com", False),
        ("http://127.0.0.1:8000", True),
        ("http://localhost:8000", True),
        ("ftp://t.example.com", False),
    ],
)
def test_cleartext_exchange_host_is_refused_unless_loopback(
    host: str,
    allowed: bool,
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    monkeypatch.setattr(
        aiwatch_credential, "read_managed_config", lambda: {"host": host}
    )
    urls: list[str] = []

    def urlopen(request: urllib.request.Request, *, timeout: float) -> _Response:
        urls.append(request.full_url)
        return _Response(b'{"token":"rlt_x","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    if allowed:
        assert exit_code == 0
        assert urls == [f"{host}/api/v1/llm-gateway/device-tokens"]
    else:
        assert exit_code == 1
        assert urls == []
        assert "https" in captured.err


def test_missing_host_fails_and_environment_host_is_normalized(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    monkeypatch.setattr(aiwatch_credential, "read_managed_config", lambda: {})

    exit_code = _run_main_with_urlopen(monkeypatch, pytest.fail)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "no Runlayer host configured" in captured.err

    urls: list[str] = []
    monkeypatch.setenv(aiwatch_credential.HOST_ENV_VAR, "t.example.com/")

    def urlopen(request: urllib.request.Request, *, timeout: float) -> _Response:
        urls.append(request.full_url)
        return _Response(b'{"token":"rlt_x","expires_in_seconds":900}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    assert exit_code == 0
    assert capsys.readouterr().out == "rlt_x"
    assert urls == ["https://t.example.com/api/v1/llm-gateway/device-tokens"]


@pytest.mark.parametrize("argv", [[], ["gemini"], ["claude", "extra"]])
def test_bad_argv_prints_usage_without_request(
    argv: list[str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(aiwatch_credential, "request_device_token", pytest.fail)

    exit_code = aiwatch_credential.main(argv)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == (
        "aiwatch credential: usage: aiwatch credential <claude|codex>\n"
    )


@pytest.mark.parametrize(
    "body",
    [
        b"{}",
        b'{"token":""}',
        b'{"token":"a b"}',
        b'{"token":"rlt_x"}',
        b'{"token":"rlt_x","expires_in_seconds":0}',
        b'{"token":"rlt_x","expires_in_seconds":true}',
        b"not-json",
    ],
)
def test_invalid_success_body_fails(
    body: bytes,
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        return _Response(body)

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "invalid token" in captured.err


def test_redirect_is_not_followed_and_never_forwards_the_credential() -> None:
    hits: list[tuple[str, str, str | None]] = []

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802 - http.server contract
            hits.append(("POST", self.path, self.headers.get("Authorization")))
            self.send_response(302)
            self.send_header("Location", f"http://127.0.0.1:{port}/collect")
            self.send_header("Content-Length", "0")
            self.end_headers()

        def do_GET(self) -> None:  # noqa: N802 - http.server contract
            hits.append(("GET", self.path, self.headers.get("Authorization")))
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *_args: object) -> None:
            return None

    server = http.server.HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with pytest.raises(aiwatch_credential.CredentialHelperError) as excinfo:
            aiwatch_credential.request_device_token(
                f"http://127.0.0.1:{port}", "rlk_secret"
            )
    finally:
        server.shutdown()
        server.server_close()

    assert "HTTP 302" in str(excinfo.value)
    assert "rlk_secret" not in str(excinfo.value)
    assert hits == [("POST", "/api/v1/llm-gateway/device-tokens", "Bearer rlk_secret")]


def test_oversized_error_body_drops_detail(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    detail = "x" * (aiwatch_credential._MAX_RESPONSE_BYTES + 1)

    def urlopen(request: urllib.request.Request, *, timeout: float) -> _Response:
        raise urllib.error.HTTPError(
            request.full_url,
            401,
            "Unauthorized",
            {},
            io.BytesIO(b'{"detail":"' + detail.encode() + b'"}'),
        )

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert (
        captured.err
        == "aiwatch credential claude: device token exchange failed: HTTP 401\n"
    )


def test_prepare_failure_is_one_stderr_line(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    monkeypatch.setattr(aiwatch_credential, "request_device_token", pytest.fail)

    def prepare() -> None:
        raise RuntimeError("truststore unavailable")

    exit_code = aiwatch_credential.main(["codex"], prepare=prepare)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err == (
        "aiwatch credential codex: credential helper failed (RuntimeError)\n"
    )


def test_oversized_success_body_fails(
    helper_home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _write_credential(helper_home)
    padding = "x" * (aiwatch_credential._MAX_RESPONSE_BYTES + 1)

    def urlopen(_request: urllib.request.Request, *, timeout: float) -> _Response:
        return _Response(b'{"token":"rlt_x","pad":"' + padding.encode() + b'"}')

    exit_code = _run_main_with_urlopen(monkeypatch, urlopen)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert "oversized" in captured.err


def test_credential_subcommand_dispatches_before_typer(tmp_path: Path) -> None:
    home = tmp_path / "empty-home"
    home.mkdir()
    probe = textwrap.dedent(
        """
        import sys
        sys.argv = ["aiwatch", "credential", "claude"]
        from runlayer_cli.aiwatch import main
        main()
        """
    )
    env = os.environ.copy()
    env["HOME"] = str(home)
    env.pop(aiwatch_credential.HOST_ENV_VAR, None)

    result = subprocess.run(
        [sys.executable, "-c", probe],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert result.stdout == ""
    assert "no LLM routing credential" in result.stderr
