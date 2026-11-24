"""The platform key source seam (step 3 of ``resolve_api_key``).

No source injected = the environment, byte for byte as before. A source replaces only
the environment step: a person's own key still wins, and ``prepare_provider_clients``
awaits the source's freshness check once per dispatch.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.providers import keys

NAME = "SEAM_TEST_PROVIDER_API_KEY"


class _Source:
    def __init__(self, values: dict[str, str], *, refuse: set[str] | None = None) -> None:
        self.values = values
        self.refuse = refuse or set()
        self.fresh_calls = 0

    def get(self, name: str) -> str | None:
        if name in self.refuse:
            raise keys.ApiKeyNotFoundError(f"platform vault holds {name} but this server cannot read it")
        return self.values.get(name)

    async def ensure_fresh(self) -> None:
        self.fresh_calls += 1


@pytest.fixture(autouse=True)
def _no_host_resolver(monkeypatch):
    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)


def test_no_source_reads_the_environment_as_today(monkeypatch) -> None:
    monkeypatch.setattr(keys, "get_platform_key_source", lambda: None)
    monkeypatch.setenv(NAME, "from-env")
    assert keys.resolve_api_key(NAME) == "from-env"
    assert keys.last_resolved_key_source() == "platform"
    monkeypatch.delenv(NAME)
    assert keys.resolve_api_key(NAME) is None


def test_a_source_replaces_the_environment_step(monkeypatch) -> None:
    source = _Source({NAME: "from-source"})
    monkeypatch.setattr(keys, "get_platform_key_source", lambda: source)
    monkeypatch.setenv(NAME, "from-env")
    assert keys.resolve_api_key(NAME) == "from-source"
    assert keys.last_resolved_key_source() == "platform"


def test_the_persons_own_key_still_beats_the_source(monkeypatch) -> None:
    source = _Source({NAME: "from-source"})
    monkeypatch.setattr(keys, "get_platform_key_source", lambda: source)
    ctx = SimpleNamespace(api_keys={NAME: "own"}, own_api_key_fingerprints=frozenset({keys.key_fingerprint("own")}))
    token = set_app_context(ctx)
    try:
        assert keys.resolve_api_key(NAME) == "own"
        assert keys.last_resolved_key_source() == "own"
    finally:
        clear_app_context(token)


def test_a_refusal_by_the_source_is_never_the_environment_copy(monkeypatch) -> None:
    source = _Source({}, refuse={NAME})
    monkeypatch.setattr(keys, "get_platform_key_source", lambda: source)
    monkeypatch.setenv(NAME, "from-env")
    with pytest.raises(keys.ApiKeyNotFoundError, match=NAME):
        keys.resolve_api_key(NAME)


def test_prepare_awaits_ensure_fresh_once(monkeypatch) -> None:
    source = _Source({})
    monkeypatch.setattr(keys, "get_platform_key_source", lambda: source)
    asyncio.run(keys.prepare_provider_clients(object()))
    assert source.fresh_calls == 1


def test_configure_registers_the_source() -> None:
    import matrx_ai
    from matrx_ai._ext import get_ext, has_ext

    previous = get_ext("platform_key_source") if has_ext("platform_key_source") else None
    source = _Source({})
    try:
        matrx_ai.configure(platform_key_source=source)
        assert keys.get_platform_key_source() is source
    finally:
        matrx_ai.configure(platform_key_source=previous)


def test_ensure_fresh_raising_from_another_event_loop_never_stops_the_dispatch(monkeypatch) -> None:
    """A foreign-loop RuntimeError from the host's freshness check is announced; the call path carries on."""

    class _Foreign(_Source):
        async def ensure_fresh(self) -> None:
            raise RuntimeError("Task got Future attached to a different loop")

    source = _Foreign({NAME: "from-source"})
    monkeypatch.setattr(keys, "get_platform_key_source", lambda: source)
    asyncio.run(keys.prepare_provider_clients(object()))  # must not raise
    assert keys.resolve_api_key(NAME) == "from-source"  # and resolution still answers from the snapshot


def test_the_probe_key_never_uses_a_persons_own_key(monkeypatch) -> None:
    from matrx_ai.providers import structured_output_probe as probe

    monkeypatch.setattr(keys, "get_platform_key_source", lambda: None)
    monkeypatch.setenv(NAME, "platform-copy")
    own = "own-copy"
    ctx = SimpleNamespace(api_keys={NAME: own}, own_api_key_fingerprints=frozenset({keys.key_fingerprint(own)}))
    token = set_app_context(ctx)
    try:
        assert probe._key(NAME) == "platform-copy"
    finally:
        clear_app_context(token)
