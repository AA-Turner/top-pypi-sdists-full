"""SDK dynamic-prompt: resolve helper (gating, controller call, fail-open) + composition."""

import asyncio
from types import SimpleNamespace
from typing import Any, Optional

import pytest

from xpander_sdk.modules.backend.frameworks import agno


class _Instr:
    def __init__(
        self,
        enabled: bool = False,
        code: Optional[str] = None,
        position: str = "after",
    ) -> None:
        self.dynamic_prompt_enabled = enabled
        self.dynamic_prompt_code = code
        self.dynamic_prompt_position = position


def _agent(instr: Optional[_Instr]) -> SimpleNamespace:
    return SimpleNamespace(id="agent-1", configuration=object(), instructions=instr)


@pytest.mark.asyncio
async def test_skips_when_disabled_or_empty() -> None:
    assert await agno._aget_dynamic_prompt_text(_agent(None)) == ""
    assert await agno._aget_dynamic_prompt_text(_agent(_Instr(False, "code"))) == ""
    assert await agno._aget_dynamic_prompt_text(_agent(_Instr(True, "   "))) == ""


@pytest.mark.asyncio
async def test_calls_controller_and_returns_text(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict = {}

    class _Client:
        def __init__(self, configuration: Any = None) -> None:
            pass

        async def make_request(
            self, path: str, method: str = "GET", **kwargs: Any
        ) -> Any:
            captured["path"] = path
            captured["method"] = method
            return {"text": "live context"}

    monkeypatch.setattr(agno, "APIClient", _Client)
    text = await agno._aget_dynamic_prompt_text(_agent(_Instr(True, "def x(): pass")))
    assert text == "live context"
    assert captured["path"] == "/tools/agent-1/dynamic-prompt"
    assert captured["method"] == "POST"


@pytest.mark.asyncio
async def test_fails_open_on_controller_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Client:
        def __init__(self, configuration: Any = None) -> None:
            pass

        async def make_request(
            self, path: str, method: str = "GET", **kwargs: Any
        ) -> Any:
            raise RuntimeError("controller down")

    monkeypatch.setattr(agno, "APIClient", _Client)
    text = await agno._aget_dynamic_prompt_text(_agent(_Instr(True, "def x(): pass")))
    assert text == ""


@pytest.mark.asyncio
async def test_missing_text_key_returns_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class _Client:
        def __init__(self, configuration: Any = None) -> None:
            pass

        async def make_request(
            self, path: str, method: str = "GET", **kwargs: Any
        ) -> Any:
            return {}

    monkeypatch.setattr(agno, "APIClient", _Client)
    agent = _agent(_Instr(True, "def x(): pass"))
    assert await agno._aget_dynamic_prompt_text(agent) == ""


@pytest.mark.asyncio
async def test_fails_open_when_controller_stalls(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(agno, "DYNAMIC_PROMPT_RESOLVE_TIMEOUT_SECONDS", 0.01)

    class _Client:
        def __init__(self, configuration: Any = None) -> None:
            pass

        async def make_request(
            self, path: str, method: str = "GET", **kwargs: Any
        ) -> Any:
            await asyncio.sleep(1)
            return {"text": "too late"}

    monkeypatch.setattr(agno, "APIClient", _Client)
    text = await agno._aget_dynamic_prompt_text(_agent(_Instr(True, "def x(): pass")))
    assert text == ""


def test_compose_appends_after_by_default() -> None:
    assert agno._compose_dynamic_prompt("BASE", "DYN", "after") == "BASE\n\nDYN"


def test_compose_prepends_before() -> None:
    assert agno._compose_dynamic_prompt("BASE", "DYN", "before") == "DYN\n\nBASE"


def test_compose_unknown_position_defaults_to_after() -> None:
    assert agno._compose_dynamic_prompt("BASE", "DYN", "sideways") == "BASE\n\nDYN"


def test_compose_empty_dynamic_text_returns_base_unchanged() -> None:
    assert agno._compose_dynamic_prompt("BASE", "", "before") == "BASE"
