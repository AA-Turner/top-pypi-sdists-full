import types

import pytest

from novita_sandbox.code_interpreter import AsyncSandbox, Sandbox


def test_code_interpreter_sandbox_create_dispatches_to_legacy_for_legacy_domain(monkeypatch):
    calls = []
    sentinel = object()

    class LegacySandbox:
        @classmethod
        def create(cls, *args, **kwargs):
            calls.append((args, kwargs))
            return sentinel

    monkeypatch.setattr(
        "novita_sandbox.code_interpreter.code_interpreter_sync.legacy_code_interpreter",
        lambda: types.SimpleNamespace(Sandbox=LegacySandbox),
        raising=False,
    )

    result = Sandbox.create("base", domain="sandbox.novita.ai", timeout=1)

    assert result is sentinel
    assert calls == [
        (
            ("base",),
            {
                "auto_pause": None,
                "domain": "sandbox.novita.ai",
                "envs": None,
                "metadata": None,
                "node_id": None,
                "secure": True,
                "timeout": 1,
            },
        )
    ]


def test_code_interpreter_sandbox_connect_dispatches_to_legacy_for_legacy_domain(monkeypatch):
    calls = []
    sentinel = object()

    class LegacySandbox:
        @classmethod
        def connect(cls, *args, **kwargs):
            calls.append((args, kwargs))
            return sentinel

    monkeypatch.setattr(
        "novita_sandbox.code_interpreter.code_interpreter_sync.legacy_code_interpreter",
        lambda: types.SimpleNamespace(Sandbox=LegacySandbox),
        raising=False,
    )

    result = Sandbox.connect("sandbox-id", domain="sandbox.novita.ai", timeout=1)

    assert result is sentinel
    assert calls == [
        (
            ("sandbox-id",),
            {
                "domain": "sandbox.novita.ai",
                "timeout": 1,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_code_interpreter_sandbox_create_dispatches_to_legacy_for_legacy_domain(monkeypatch):
    calls = []
    sentinel = object()

    class LegacyAsyncSandbox:
        @classmethod
        async def create(cls, *args, **kwargs):
            calls.append((args, kwargs))
            return sentinel

    monkeypatch.setattr(
        "novita_sandbox.code_interpreter.code_interpreter_async.legacy_code_interpreter",
        lambda: types.SimpleNamespace(AsyncSandbox=LegacyAsyncSandbox),
        raising=False,
    )

    result = await AsyncSandbox.create("base", domain="sandbox.novita.ai", timeout=1)

    assert result is sentinel
    assert calls == [
        (
            ("base",),
            {
                "auto_pause": None,
                "domain": "sandbox.novita.ai",
                "envs": None,
                "metadata": None,
                "node_id": None,
                "secure": True,
                "timeout": 1,
            },
        )
    ]


@pytest.mark.asyncio
async def test_async_code_interpreter_sandbox_connect_dispatches_to_legacy_for_legacy_domain(monkeypatch):
    calls = []
    sentinel = object()

    class LegacyAsyncSandbox:
        @classmethod
        async def connect(cls, *args, **kwargs):
            calls.append((args, kwargs))
            return sentinel

    monkeypatch.setattr(
        "novita_sandbox.code_interpreter.code_interpreter_async.legacy_code_interpreter",
        lambda: types.SimpleNamespace(AsyncSandbox=LegacyAsyncSandbox),
        raising=False,
    )

    result = await AsyncSandbox.connect(
        "sandbox-id", domain="sandbox.novita.ai", timeout=1
    )

    assert result is sentinel
    assert calls == [
        (
            ("sandbox-id",),
            {
                "domain": "sandbox.novita.ai",
                "timeout": 1,
            },
        )
    ]
