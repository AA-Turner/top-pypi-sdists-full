"""Defect 30 / 31 guard: the stored request snapshot IS the payload handed to the SDK.

``chat.request_snapshot.request_payload`` was captured early in ``execute()``.
Anything that rewrites the request afterwards (Anthropic's grammar ladder
appending the answer contract to ``system``, SDK-drift routing into
``extra_body``) left the stored snapshot different from what was sent.

For every chat adapter this test captures an EARLY payload (as ``execute()``
does), then drives the adapter's SDK-handing method with a DIFFERENT final
payload against a fake SDK client that records the kwargs it receives, and
asserts the stored snapshot equals those kwargs. A second test pins, by AST,
that every chat SDK call site asks for the re-capture and no media / speech /
STT site does.
"""

from __future__ import annotations

import ast
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.orchestrator.execution_state import (
    ExecutionState,
    clear_execution_state,
    set_execution_state,
)
from matrx_ai.providers.snapshot import capture_request_payload, wire_json

PROVIDERS = Path(__file__).resolve().parents[1] / "matrx_ai" / "providers"


class _Sent(Exception):
    """Raised by the fake SDK after recording what it received."""


def _recorder(sink: list[dict[str, Any]]):
    async def _create(**kwargs: Any):
        sink.append(kwargs)
        raise _Sent

    return _create


def _chat_client(sink):
    return SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=_recorder(sink))))


def _anthropic():
    from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

    chat = object.__new__(AnthropicChat)
    chat.debug = False
    return chat


def _openai():
    from matrx_ai.providers.openai.openai_api import OpenAIChat

    chat = object.__new__(OpenAIChat)
    chat.debug = False
    return chat


def _bare(cls_path: str, **attrs: Any):
    module, name = cls_path.rsplit(".", 1)
    cls = getattr(__import__(module, fromlist=[name]), name)
    chat = object.__new__(cls)
    chat.debug = False
    for k, v in attrs.items():
        setattr(chat, k, v)
    return chat


def _final(streaming: bool) -> dict[str, Any]:
    return {
        "model": "m",
        "system": "base system\n\nANSWER_CONTRACT appended by the grammar ladder",
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 16,
        "stream": streaming,
    }


# (id, builder, streaming, how to attach the fake SDK, method call)
def _cases():
    ns = "non_streaming"
    st = "streaming"
    yield "anthropic-" + ns, _anthropic, False, "anthropic"
    yield "anthropic-" + st, _anthropic, True, "anthropic"
    yield "openai-" + ns, _openai, False, "openai"
    yield "openai-" + st, _openai, True, "openai"
    for name, path, extra in (
        ("cerebras", "matrx_ai.providers.cerebras.cerebras_api.CerebrasChat", {}),
        ("groq", "matrx_ai.providers.groq.groq_api.GroqChat", {}),
        ("together", "matrx_ai.providers.together.together_api.TogetherChat", {}),
        (
            "generic_openai",
            "matrx_ai.providers.generic_openai.generic_openai_api.GenericOpenAIChat",
            {"provider_name": "generic_openai", "endpoint_name": "[GENERIC]"},
        ),
        (
            "moonshot",
            "matrx_ai.providers.moonshot.moonshot_api.MoonshotChat",
            {"provider_name": "moonshot", "endpoint_name": "[MOONSHOT]"},
        ),
    ):
        for streaming in (False, True):
            yield f"{name}-{st if streaming else ns}", (lambda p=path, e=extra: _bare(p, **e)), streaming, "chat"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("builder", "streaming", "sdk"),
    [pytest.param(b, s, k, id=i) for i, b, s, k in _cases()],
)
async def test_stored_snapshot_equals_what_the_sdk_received(builder, streaming, sdk) -> None:
    sink: list[dict[str, Any]] = []
    chat = builder()
    emitter = SimpleNamespace()
    if sdk == "anthropic":
        chat.client = SimpleNamespace(messages=SimpleNamespace(create=_recorder(sink), stream=_sync_recorder(sink)))
    elif sdk == "openai":
        chat.client = SimpleNamespace(
            responses=SimpleNamespace(create=_recorder(sink), stream=_sync_recorder(sink))
        )
    else:
        chat.client = _chat_client(sink)

    state = ExecutionState()
    token = set_execution_state(state)
    try:
        # What execute() captured BEFORE late rewrites.
        capture_request_payload({"model": "m", "system": "base system"}, provider="x")
        state.snapshot_provider = "kept-provider"
        final = _final(streaming)
        method = chat._execute_streaming if streaming else chat._execute_non_streaming
        args: tuple[Any, ...] = (final, emitter, "m")
        if sdk == "chat" and streaming and hasattr(chat, "provider_name") and chat.provider_name in (
            "generic_openai",
            "moonshot",
        ):
            args = (final, emitter, "m", "m")
        with pytest.raises(BaseException) as excinfo:  # noqa: PT011 — _Sent or its wrapper
            await method(*args)
        del excinfo
        assert sink, "the fake SDK was never called"
        sent = sink[-1]
        if sdk == "openai" and streaming:
            sent = sent["extra_body"]  # OpenAI streams the wire body through extra_body
        assert wire_json(state.snapshot_payload) == wire_json(sent)
        assert state.snapshot_provider == "kept-provider"
    finally:
        clear_execution_state(token)


def _sync_recorder(sink: list[dict[str, Any]]):
    def _create(*args: Any, **kwargs: Any):
        sink.append(kwargs)
        raise _Sent

    return _create


def _route_calls(path: Path):
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and getattr(node.func, "id", getattr(node.func, "attr", None)) == "route_undeclared_params"
        ):
            wants = any(k.arg == "snapshot" and getattr(k.value, "value", None) is True for k in node.keywords)
            yield ast.unparse(node.args[0]), wants


CHAT_FILES = [
    "anthropic/anthropic_api.py",
    "openai/openai_api.py",
    "cerebras/cerebras_api.py",
    "groq/groq_api.py",
    "together/together_api.py",
    "xai/xai_api.py",
    "generic_openai/generic_openai_api.py",
    "google/google_api.py",
]
NOT_CHAT_CALLEES = ("audio.speech.create", "_tts_stream")


@pytest.mark.parametrize("rel", CHAT_FILES)
def test_every_chat_sdk_call_asks_for_the_final_capture(rel: str) -> None:
    calls = list(_route_calls(PROVIDERS / rel))
    assert calls, f"{rel}: no route_undeclared_params call found"
    for callee, wants in calls:
        is_chat = not any(t in callee for t in NOT_CHAT_CALLEES)
        assert wants == is_chat, f"{rel}: {callee} snapshot={wants}, expected {is_chat}"


def test_media_and_stt_sites_never_overwrite_the_chat_snapshot() -> None:
    offenders = []
    for path in PROVIDERS.rglob("*.py"):
        if "tests" in path.parts or path.name == "sdk_drift.py":
            continue
        if str(path.relative_to(PROVIDERS)) in CHAT_FILES:
            continue
        offenders += [f"{path.name}: {c}" for c, w in _route_calls(path) if w]
    assert not offenders, offenders


def test_moonshot_is_a_chat_adapter_that_captures_with_its_own_label() -> None:
    """Moonshot reuses the generic adapter, whose execute() captures the payload."""
    from matrx_ai.providers.generic_openai.generic_openai_api import GenericOpenAIChat
    from matrx_ai.providers.moonshot.moonshot_api import MoonshotChat

    assert issubclass(MoonshotChat, GenericOpenAIChat)
    assert "execute" not in vars(MoonshotChat)
    src = (PROVIDERS / "generic_openai" / "generic_openai_api.py").read_text()
    assert "provider=self.provider_name" in src
