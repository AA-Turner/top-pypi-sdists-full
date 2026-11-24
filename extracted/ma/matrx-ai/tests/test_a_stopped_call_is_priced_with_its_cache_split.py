"""A stopped call's estimate is priced the way the provider bills it: the cache split, never all full input.

Live walk 2026-11-16 (General Chat, "Explain in detail how rivers form deltas."): a Stop with no provider
usage (conversation 382ab36b) was billed 48,138 input tokens at the full $2/M = $0.096276, while a Stop a
moment later on the same prompt WITH provider usage (6361efa3) was 2,945 uncached + 37,458 cache-read
tokens = $0.009716. The estimate priced the cached system + tools prefix at the full input price.

Lead's ruling (2026-11-16, option A, made in Arman's absence — he may overrule it): the cache-marked
prefix (system + tool declarations, the prefix the cache plan tracks) counts as a CACHE READ when the
cache plan saw that prefix sent within its cache life, otherwise as a 5-MINUTE CACHE WRITE; the rest is
uncached input; the note names the branch. These drive the REAL dispatch seam.

Second ruling (lead, 2026-11-16, also in Arman's absence — he may overrule it): a prefix not POSITIVELY
known to have been written is priced at 1x uncached, never 1.25x — a stopped call never costs more than
the full uncached price. The 5-minute write rate applies only when this send was positively the first to
send that prefix within its cache life. The "seen recently" memory is shared across workers through the
existing shared cache tier (``matrx_utils.cache``), the key living exactly the cache life.

Third ruling (lead, 2026-11-17, same terms), after a cost adversary broke the shared memory: the evidence is
PER SEND (another person's later send never changes this send's price); the shared key's scope is exactly
the provider's cache scope (environment + vendor + API-key fingerprint + model + prefix); the key is set only
after the provider ACCEPTED the call (its stream started or it answered); the send never waits on the store.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_utils.cache import configure_cache, reset_cache_runtime

from matrx_ai.config import ModelPricing, PricingTier, TokenUsage
from matrx_ai.config import cache_plan
from matrx_ai.config.cache_plan import reset_for_tests
from matrx_ai.config.context_preflight import estimate_prompt_tokens
from matrx_ai.config.context_trim import estimate_budget_tokens
from matrx_ai.providers.errors import get_billed_usage

from matrx_ai.providers.errors import attach_billed_usage
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

SYSTEM = "You are a careful geography tutor who explains processes step by step. " * 400  # ~29k chars
TAIL = "This conversation's own instructions: answer in plain English. " * 20  # rides after the prefix

INPUT, OUTPUT, CACHE_READ, CACHE_WRITE_5M = 2.0, 10.0, 0.1, 2.5  # the live offering's catalog prices


class _Emitter:
    def __init__(self) -> None:
        self.text = ""

    def get_turn_text(self) -> str:
        return self.text


class _SharedStore:
    """The shared cache tier as every worker sees it (``matrx_utils.cache.CacheBackend``)."""

    def __init__(self) -> None:
        self.keys: dict[str, tuple[bytes, int]] = {}

    async def get(self, key: str) -> bytes | None:
        hit = self.keys.get(key)
        return hit[0] if hit else None

    async def set(self, key: str, value: bytes, ttl_ms: int) -> None:
        self.keys[key] = (value, ttl_ms)

    async def delete(self, *keys: str) -> None:
        for key in keys:
            self.keys.pop(key, None)

    async def delete_prefix(self, prefix: str) -> int:
        return 0

    async def publish(self, channel: str, message: bytes) -> None:
        return None

    async def subscribe(self, channel: str):  # pragma: no cover - never subscribed here
        yield b""


class _HangingStore(_SharedStore):
    """A shared store that never answers (a slow or stuck Valkey)."""

    def __init__(self) -> None:
        super().__init__()
        self.started = 0
        self.ended = 0

    async def get(self, key: str) -> bytes | None:
        self.started += 1
        try:
            await asyncio.Event().wait()
            return None  # pragma: no cover - never answers
        finally:
            self.ended += 1


KEY_A, KEY_B = "fingerprint-of-key-a", "fingerprint-of-key-b"


@pytest.fixture(autouse=True)
def _fresh(monkeypatch):
    reset_for_tests()
    reset_cache_runtime()
    configure_cache(url=None)  # no shared store unless a test configures one
    monkeypatch.setattr("matrx_ai.providers.keys.prepared_key_fingerprint", lambda: _KEY[0])
    _KEY[0] = KEY_A
    yield
    reset_for_tests()
    reset_cache_runtime()


_KEY = [KEY_A]


class _Send:
    """One provider call through the REAL dispatch seam, under one API key."""

    def __init__(self, config: Any, *, key: str | None = KEY_A, partial: TokenUsage | None = None) -> None:
        self.config, self.key, self.partial = config, key, partial
        self.emitter = _Emitter()
        self.dispatched = asyncio.Event()
        self.release = asyncio.Event()
        self.fail: BaseException | None = None
        self.task: asyncio.Task | None = None

    async def start(self) -> None:
        profile = make_profile(model_name="stop-test-model", wire_format="openai_chat")

        async def dispatch() -> Any:
            try:
                self.dispatched.set()
                if self.fail is not None:
                    raise self.fail
                await self.release.wait()
                return SimpleNamespace(usage=None, messages=None)
            except asyncio.CancelledError as cancel:
                attach_billed_usage(cancel, self.partial)
                raise

        ctx = AppContext(emitter=self.emitter, user_id="u", request_id="r", conversation_id="c")  # type: ignore[arg-type]
        token = set_app_context(ctx)
        _KEY[0] = self.key
        try:
            self.task = asyncio.ensure_future(
                UnifiedAIClient._dispatch_admitted(dispatch, profile=profile, provider_client=None, config=self.config)
            )
            await self.dispatched.wait()
        finally:
            clear_app_context(token)
        await asyncio.sleep(0.01)  # the detached store lookup answers

    def streams(self) -> None:
        self.emitter.text = "Deltas form where a river slows as it meets still water."

    async def completes(self) -> None:
        self.release.set()
        await self.task
        await asyncio.sleep(0.01)  # the detached record lands

    async def stops(self) -> TokenUsage:
        self.task.cancel()
        try:
            await self.task
        except asyncio.CancelledError as exc:
            await asyncio.sleep(0.01)
            return get_billed_usage(exc)
        raise AssertionError("the stopped call did not raise its cancellation")


def _pricing() -> dict[str, ModelPricing]:
    return {
        "test-offering:stop-test-model": ModelPricing(
            model_name="stop-test-model",
            api="openai",
            tiers=[
                PricingTier(
                    max_tokens=None,
                    input_price=INPUT,
                    output_price=OUTPUT,
                    cached_input_price=CACHE_READ,
                    cache_hit_price=CACHE_READ,
                    cache_write_5m_price=CACHE_WRITE_5M,
                    cache_write_1h_price=4.0,
                )
            ],
        )
    }


def _config(**extra: object) -> SimpleNamespace:
    return SimpleNamespace(
        model="stop-test-model", system_instruction=SYSTEM, conversation_instructions=TAIL, messages=[], **extra
    )


def _split(config: SimpleNamespace) -> tuple[int, int, int]:
    prompt = estimate_prompt_tokens(config)
    prefix = estimate_budget_tokens(len(SYSTEM), "prose")
    assert 0 < prefix < prompt
    return prompt, prefix, prompt - prefix


async def _warm(config: Any, *, key: str = KEY_A) -> None:
    """An earlier ACCEPTED send of the same scope, inside the cache life."""
    earlier = _Send(config, key=key)
    await earlier.start()
    await earlier.completes()


@pytest.mark.asyncio
async def test_a_prefix_an_earlier_accepted_send_wrote_is_billed_as_a_cache_read():
    configure_cache(backend=_SharedStore())
    config = _config()
    await _warm(config)
    _prompt, prefix, rest = _split(config)
    send = _Send(config)
    await send.start()
    usage = await send.stops()
    assert usage.cached_input_tokens == prefix, "a warm prefix is read from cache, never billed as full input"
    assert usage.input_tokens == rest
    assert usage.cache_write_tokens == 0
    assert "cache read" in usage.metadata["usage_estimated"]
    assert usage.calculate_cost(_pricing()) == pytest.approx((rest * INPUT + prefix * CACHE_READ) / 1_000_000)


@pytest.mark.asyncio
async def test_a_writers_price_is_never_changed_by_a_later_readers_send():
    """(a) A sends first (a write) and streams; B sends the same prefix (a read); A stops: A paid a write."""
    configure_cache(backend=_SharedStore())
    config = _config()
    _prompt, prefix, rest = _split(config)
    a = _Send(config)
    await a.start()
    a.streams()  # A's stream has started: the provider accepted A
    b = _Send(config)
    await b.start()
    await b.completes()
    usage = await a.stops()
    # Lead ruling 2026-11-17 (A): a write is priced at 1x uncached, never 1.25x — a stopped call never costs more
    # than full uncached, whoever else shares the key. B's later read still never turns A into a read.
    assert usage.cache_write_tokens == 0, "a stopped call's prefix is never priced at the 1.25x write rate"
    assert usage.cached_input_tokens == 0, "A's own send was first; B's later read never changes it"
    assert "first sent" in usage.metadata["usage_estimated"]
    expected = ((rest + prefix) * INPUT + usage.output_tokens * OUTPUT) / 1_000_000
    assert usage.calculate_cost(_pricing()) == pytest.approx(expected)


@pytest.mark.asyncio
async def test_a_send_that_fails_before_the_provider_records_nothing():
    """(b) a send refused before the provider sets no shared key, and its own state stays unknown."""
    store = _SharedStore()
    configure_cache(backend=store)
    failing = _Send(_config())
    failing.fail = ConnectionError("could not reach the provider")
    await failing.start()
    with pytest.raises(ConnectionError):
        await failing.task
    await asyncio.sleep(0.01)
    stopped_early = _Send(_config())
    await stopped_early.start()
    usage = await stopped_early.stops()  # stopped before its stream started
    assert store.keys == {}, "only an ACCEPTED call records its prefix"
    assert usage.cache_write_tokens == 0 and usage.cached_input_tokens == 0


@pytest.mark.asyncio
async def test_two_api_keys_never_share_a_cache_scope():
    """(c) the provider caches per workspace of the key: another key's send is not evidence."""
    configure_cache(backend=_SharedStore())
    config = _config()
    await _warm(config, key=KEY_A)
    send = _Send(config, key=KEY_B)
    await send.start()
    usage = await send.stops()
    assert usage.cached_input_tokens == 0, "key A warming its cache says nothing of key B's"
    assert cache_plan.prefix_scope_digest(config, vendor="anthropic", key_fingerprint=KEY_A) != (
        cache_plan.prefix_scope_digest(config, vendor="anthropic", key_fingerprint=KEY_B)
    )
    assert cache_plan.prefix_scope_digest(config, vendor="anthropic", key_fingerprint=KEY_A) != (
        cache_plan.prefix_scope_digest(config, vendor="openai", key_fingerprint=KEY_A)
    )


@pytest.mark.asyncio
async def test_one_key_on_two_stages_is_one_cache_scope(monkeypatch):
    """Cost adversary pass 3: the provider's cache is the key's workspace, not our stage. A dev and a prod process
    on ONE key share it, so dev's warm prefix is prod's cache read, never a 1.25x write."""
    import matrx_utils.runtime_env as runtime_env

    config = _config()
    monkeypatch.setattr(runtime_env, "declared_stage", lambda: "dev")
    dev = cache_plan.prefix_scope_digest(config, vendor="anthropic", key_fingerprint=KEY_A)
    monkeypatch.setattr(runtime_env, "declared_stage", lambda: "prod")
    prod = cache_plan.prefix_scope_digest(config, vendor="anthropic", key_fingerprint=KEY_A)
    assert dev == prod, "one key is one provider cache, whatever stage sent it"


@pytest.mark.asyncio
async def test_an_unknown_prefix_never_costs_more_than_full_uncached_input():
    config = _config()  # no shared store: nothing positively known
    prompt, _prefix, _rest = _split(config)
    send = _Send(config)
    await send.start()
    send.streams()
    usage = await send.stops()
    assert usage.cache_write_tokens == 0, "an unknown prefix is never priced as a write"
    assert usage.cached_input_tokens == 0
    assert usage.input_tokens == prompt
    assert "unknown" in usage.metadata["usage_estimated"]
    assert usage.calculate_cost(_pricing()) <= (prompt * INPUT + 2000 * OUTPUT) / 1_000_000


@pytest.mark.asyncio
async def test_no_key_fingerprint_means_no_evidence():
    store = _SharedStore()
    configure_cache(backend=store)
    config = _config()
    send = _Send(config, key=None)
    await send.start()
    send.streams()
    usage = await send.stops()
    assert store.keys == {} and usage.cache_write_tokens == 0 and usage.cached_input_tokens == 0


@pytest.mark.asyncio
async def test_the_shared_key_lives_exactly_the_cache_life():
    from matrx_ai.config.cache_marks import ANTHROPIC_CACHE_TIER_SECS

    store = _SharedStore()
    configure_cache(backend=store)
    await _warm(_config())
    assert [ttl for _v, ttl in store.keys.values()] == [ANTHROPIC_CACHE_TIER_SECS["5m"] * 1000]


@pytest.mark.asyncio
async def test_a_send_never_waits_on_the_shared_store():
    store = _HangingStore()
    configure_cache(backend=store)
    send = _Send(_config())
    await send.start()
    await asyncio.wait_for(send.completes(), timeout=0.05)  # far inside the store's 150 ms bound
    assert store.started == 1 and store.ended == 0, "the call finished while the store lookup was still pending"


@pytest.mark.asyncio
async def test_a_send_with_no_cache_marks_is_all_uncached_input():
    configure_cache(backend=_SharedStore())
    config = _config(prompt_cache_marks="none")
    await _warm(config)
    prompt, _prefix, _rest = _split(config)
    send = _Send(config)
    await send.start()
    usage = await send.stops()
    assert usage.input_tokens == prompt
    assert usage.cached_input_tokens == 0 and usage.cache_write_tokens == 0
    assert usage.calculate_cost(_pricing()) == pytest.approx(prompt * INPUT / 1_000_000)


@pytest.mark.asyncio
async def test_an_adapter_usage_with_no_input_gets_the_same_split():
    configure_cache(backend=_SharedStore())
    config = _config()
    await _warm(config)
    _prompt, prefix, rest = _split(config)
    partial = TokenUsage(input_tokens=0, output_tokens=0, matrx_model_name="stop-test-model", api="openai")
    send = _Send(config, partial=partial)
    await send.start()
    usage = await send.stops()
    assert usage is partial
    assert usage.cached_input_tokens == prefix and usage.input_tokens == rest


def test_cache_write_tokens_survive_adding_usages():
    a = TokenUsage(input_tokens=100, output_tokens=0, cache_write_5m_tokens=80)
    b = TokenUsage(input_tokens=10, output_tokens=0)
    assert (a + b).cache_write_tokens == 80


@pytest.mark.asyncio
async def test_preparing_a_send_records_nothing_before_the_provider_accepts():
    """(b) the send boundary runs before the provider sees anything: it never records the prefix."""
    from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
    from matrx_ai.config.context_trim import TrimPolicy
    from matrx_ai.config.send_boundary import STAGE_LOOP, prepare_for_send

    store = _SharedStore()
    configure_cache(backend=store)
    config = UnifiedConfig(
        model="stop-test-model",
        system_instruction=SYSTEM,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="How do rivers form deltas?")])],
    )
    await prepare_for_send(config, stage=STAGE_LOOP, conversation_id="conv-1", policy=TrimPolicy())
    await asyncio.sleep(0.02)
    assert store.keys == {}, "a prepared send that never reached the provider must set no shared key"
