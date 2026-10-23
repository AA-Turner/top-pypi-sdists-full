"""A model call on the person's own key costs the platform nothing (owner ruling 2026-10-15 #6)."""

from __future__ import annotations

from types import SimpleNamespace

from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.providers import keys


def _ctx(api_keys: dict[str, str], *, own: tuple[str, ...] = ()) -> SimpleNamespace:
    """A context whose ``own`` values came from the person's vault (fingerprinted)."""
    return SimpleNamespace(
        api_keys=api_keys,
        own_api_key_fingerprints=frozenset(keys.key_fingerprint(v) for v in own),
    )


def _usage() -> TokenUsage:
    return TokenUsage(input_tokens=1000, output_tokens=1000, matrx_model_name="m", api="openai")


def test_a_key_from_the_persons_vault_zero_rates_the_call(monkeypatch) -> None:
    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)
    token = set_app_context(_ctx({"OPENAI_API_KEY": "sk-own"}, own=("sk-own",)))
    try:
        assert keys.resolve_api_key("OPENAI_API_KEY") == "sk-own"
        assert keys.last_resolved_key_source() == "own"
        usage = _usage()
        keys.mark_usage_key_source(usage)
        assert usage.metadata.get(keys.OWN_KEY_USAGE_FLAG) is True
        assert usage.calculate_cost() == 0.0
    finally:
        clear_app_context(token)


def test_a_platform_key_is_charged(monkeypatch) -> None:
    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-platform")
    token = set_app_context(_ctx({}))
    try:
        assert keys.resolve_api_key("OPENAI_API_KEY") == "sk-platform"
        assert keys.last_resolved_key_source() == "platform"
        usage = _usage()
        keys.mark_usage_key_source(usage)
        assert keys.OWN_KEY_USAGE_FLAG not in usage.metadata
    finally:
        clear_app_context(token)


class _Adapter:
    client = keys.keyed_provider_client("OPENAI_API_KEY", factory=lambda api_key: ("client", api_key))


def test_the_preflight_carries_the_key_source_back_from_its_worker_thread(monkeypatch) -> None:
    """The real dispatch resolves keys inside asyncio.to_thread; a ContextVar set
    there dies with the thread's copied context unless prepare carries it back."""
    import asyncio

    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-platform")

    async def run(api_keys: dict[str, str]) -> tuple[str | None, object]:
        token = set_app_context(_ctx(api_keys, own=tuple(api_keys.values())))
        try:
            adapter = _Adapter()
            await keys.prepare_provider_clients(adapter)
            usage = _usage()
            keys.mark_usage_key_source(usage)
            return keys.last_resolved_key_source(), (adapter.client, usage.calculate_cost())
        finally:
            clear_app_context(token)

    source, (client, cost) = asyncio.run(run({"OPENAI_API_KEY": "sk-own"}))
    assert source == "own"
    assert client == ("client", "sk-own")
    assert cost == 0.0
    source, (client, _) = asyncio.run(run({}))
    assert source == "platform"
    assert client == ("client", "sk-platform")


def test_concurrent_requests_on_one_shared_adapter_keep_their_own_keys(monkeypatch) -> None:
    """Adapters are process-shared: a person's key and ours, preflighted in
    overlapping tasks, must each dispatch on the client built for THEIR key."""
    import asyncio

    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-platform")
    shared = _Adapter()
    own_prepared = asyncio.Event()
    platform_prepared = asyncio.Event()

    async def own_turn() -> object:
        token = set_app_context(_ctx({"OPENAI_API_KEY": "sk-own"}, own=("sk-own",)))
        try:
            await keys.prepare_provider_clients(shared)
            own_prepared.set()
            await platform_prepared.wait()  # the other request re-keys the shared memo
            return shared.client, keys.last_resolved_key_source()
        finally:
            clear_app_context(token)

    async def platform_turn() -> object:
        await own_prepared.wait()
        token = set_app_context(_ctx({}))
        try:
            await keys.prepare_provider_clients(shared)
            platform_prepared.set()
            return shared.client, keys.last_resolved_key_source()
        finally:
            clear_app_context(token)

    async def both():
        return await asyncio.gather(own_turn(), platform_turn())

    (own_client, own_source), (platform_client, platform_source) = asyncio.run(both())
    assert own_client == ("client", "sk-own") and own_source == "own"
    assert platform_client == ("client", "sk-platform") and platform_source == "platform"


def test_a_platform_key_copied_into_api_keys_is_still_ours_and_charges(monkeypatch) -> None:
    """BLOCKER class (review 2026-10-22): judges / qc_judge copy OUR env key into
    AppContext.api_keys. Where a key is found never makes it the person's."""
    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-platform-env")
    platform = keys.resolve_api_key("ANTHROPIC_API_KEY")
    token = set_app_context(_ctx({"ANTHROPIC_API_KEY": platform}))  # no vault fingerprint
    try:
        assert keys.resolve_api_key("ANTHROPIC_API_KEY") == "sk-platform-env"
        assert keys.last_resolved_key_source() == "platform"
        usage = _usage()
        keys.mark_usage_key_source(usage)
        assert keys.OWN_KEY_USAGE_FLAG not in usage.metadata
        assert (usage.calculate_cost() or 0) > 0 or usage.calculate_cost() is None
    finally:
        clear_app_context(token)


def test_a_dispatch_never_inherits_an_earlier_calls_own_source(monkeypatch) -> None:
    """MAJOR 2: dispatches with no provider client (decisions, embeddings, rerank…) must not
    read the "own" an earlier own-key call left in the same (or a parent) context."""
    import asyncio

    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)

    async def run() -> TokenUsage:
        token = set_app_context(_ctx({"OPENAI_API_KEY": "sk-own"}, own=("sk-own",)))
        try:
            await keys.prepare_provider_clients(_Adapter())
            assert keys.last_resolved_key_source() == "own"

            async def child() -> TokenUsage:  # a child task copies this context
                keys.begin_dispatch_key_scope()  # the dispatch seam's first act
                usage = _usage()
                keys.mark_usage_key_source(usage)
                return usage

            return await asyncio.create_task(child())
        finally:
            clear_app_context(token)

    usage = asyncio.run(run())
    assert keys.OWN_KEY_USAGE_FLAG not in usage.metadata


def test_tools_never_spend_the_persons_key(monkeypatch) -> None:
    """MAJOR 3: a paid tool's internal model call runs on OUR key and charges."""
    monkeypatch.setattr(keys, "get_api_key_resolver", lambda: None)
    monkeypatch.setenv("OPENAI_API_KEY", "sk-platform")
    token = set_app_context(_ctx({"OPENAI_API_KEY": "sk-own"}, own=("sk-own",)))
    try:
        with keys.platform_keys_only():
            assert keys.resolve_api_key("OPENAI_API_KEY") == "sk-platform"
            assert keys.last_resolved_key_source() == "platform"
        assert keys.resolve_api_key("OPENAI_API_KEY") == "sk-own"
        assert keys.last_resolved_key_source() == "own"
    finally:
        clear_app_context(token)


def test_a_system_run_never_carries_the_persons_own_keys() -> None:
    """MAJOR 3: system work spawned in an own-key turn (any actor) spends our keys."""
    from matrx_connect.context.app_context import AppContext, _derive_system_identity

    ambient = AppContext(
        emitter=None,
        user_id="person-1",
        api_keys={"OPENAI_API_KEY": "sk-own", "EXTRA": "sk-injected"},
        own_api_key_fingerprints=frozenset({keys.key_fingerprint("sk-own")}),
    )
    for actor in ("person-1", "someone-else"):
        sys_ctx = _derive_system_identity(
            ambient, feature="t", user_id=actor, organization_id="org-1", source_app=None, overrides={}
        )
        assert "OPENAI_API_KEY" not in sys_ctx.api_keys
        assert sys_ctx.api_keys.get("EXTRA") == "sk-injected"
        assert sys_ctx.own_api_key_fingerprints == frozenset()
    assert "sk-own" not in repr(ambient)
