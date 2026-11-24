"""A private repository read without a token is the caller's input, never a platform failure.

Live (system_error 752f1b71, 2026-11-21): git_ingest on a private GitHub repository failed with
``fatal: could not read Username for 'https://github.com'`` and was filed as
``tool_execution_failed`` (error_type ``execution``, retryable). It is now a typed refusal
(``auth_required``) that the executor treats as expected and that tells the model to pass a token.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

pytest.importorskip("gitingest")

from matrx_ai.tools import executor
from matrx_ai.tools.implementations import code_ingest

_GIT_LOGIN_PROMPT = (
    "Command failed: git ls-remote https://github.com/owner/private refs/tags/main*\n"
    "Error: fatal: could not read Username for 'https://github.com': No such device or address"
)


class _Emitter:
    async def send_data(self, *a, **k) -> None:  # pragma: no cover - progress only
        return None

    def __getattr__(self, _name):
        async def _noop(*a, **k):
            return None

        return _noop


def _ctx():
    return SimpleNamespace(emitter=_Emitter(), call_id="call-1")


def _run(monkeypatch, exc: Exception, **args):
    def _raise(*a, **k):
        raise exc

    monkeypatch.setattr(code_ingest, "_ingest", _raise)
    monkeypatch.setattr(code_ingest, "get_active_sandbox", lambda: None)
    monkeypatch.setattr(code_ingest.shutil, "which", lambda _n: "/usr/bin/git")
    return asyncio.run(
        code_ingest.git_ingest({"source": "https://github.com/owner/private", **args}, _ctx())
    )


def test_a_login_prompt_is_an_auth_required_refusal(monkeypatch) -> None:
    result = _run(monkeypatch, RuntimeError(_GIT_LOGIN_PROMPT))
    assert result.success is False
    assert result.error.error_type == "auth_required"
    assert result.error.refusal is True
    assert "token" in (result.error.suggested_action or "")
    assert executor._is_expected_domain_failure(
        tool_name="git_ingest", error_type=result.error.error_type, message=result.error.message
    )


def test_any_other_clone_failure_stays_a_filed_execution_error(monkeypatch) -> None:
    result = _run(monkeypatch, RuntimeError("fatal: unable to access: Could not resolve host"))
    assert result.error.error_type == "execution"
    assert not executor._is_expected_domain_failure(
        tool_name="git_ingest", error_type="execution", message=result.error.message
    )
