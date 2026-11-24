"""The BAA gate: under HIPAA mode only vendors with a Business Associate Agreement are reached.

Each test fails without the gate: the swap (no stand-in → the Groq model would run), the seam
refusal (the TypeSafe decision / image call would dispatch), capture mode (it used to skip every
spend gate, so a gated call was captured as if it would run), the own-key refusal, and the
OpenAI retention switches.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.providers import baa_gate
from matrx_ai.providers import free_tier_models as ftm
from matrx_ai.providers.request_capture import capturing_provider_request
from matrx_ai.providers.unified_client import UnifiedAIClient


class _Policy:
    reason = "org"
    organization_id = "org-hipaa"
    chat_standin_model = "claude-haiku-5-5"
    stt_standin_model = ""
    own_keys_ok = False
    _covered = {("anthropic", "chat"), ("openai", "chat"), ("openai", "embedding")}

    def covers(self, vendor: str, interaction: str) -> bool:
        return (vendor, interaction) in self._covered


class _Emitter:
    def __init__(self) -> None:
        self.infos: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload)


def _caps(interaction: str = "turn", **kw: Any) -> SimpleNamespace:
    base = dict(interaction=interaction, produces_image=False, produces_video=False, produces_audio=False,
                produces_text=True, supports_audio_input=False, supports_text_input=True)
    base.update(kw)
    return SimpleNamespace(**base)


def _profile(model: str, vendor: str, interaction: str = "turn", **kw: Any) -> SimpleNamespace:
    return SimpleNamespace(model_name=model, vendor=vendor, provider_name=vendor, route_kind="offering",
                           served_via=None, capabilities=_caps(interaction, **kw.pop("caps", {})), **kw)


@pytest.fixture
def ctx(monkeypatch: pytest.MonkeyPatch) -> SimpleNamespace:
    c = SimpleNamespace(user_id="u-1", request_id="r-1", emitter=_Emitter(), metadata={})
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: c)
    baa_gate._told.clear()
    return c


@pytest.fixture
def gated(ctx: SimpleNamespace):
    async def host(_ctx: Any) -> _Policy:
        return _Policy()

    baa_gate.set_baa_policy_host(host)
    yield _Policy()
    baa_gate.set_baa_policy_host(None)


@pytest.fixture
def ungated(ctx: SimpleNamespace):
    async def host(_ctx: Any) -> None:
        return None

    baa_gate.set_baa_policy_host(host)
    yield
    baa_gate.set_baa_policy_host(None)


@pytest.fixture(autouse=True)
def _catalog(monkeypatch: pytest.MonkeyPatch):
    rows = {"claude-haiku-5-5": SimpleNamespace(name="claude-haiku-5-5", common_name="Claude Haiku 5.5",
                                                 cost_rating=2, is_premium=False, metadata={})}

    async def _load(name: str):
        return rows.get(name)

    monkeypatch.setattr(ftm, "_load", _load)


@pytest.mark.asyncio
async def test_gated_groq_chat_swaps_to_the_standin_and_says_so(gated, ctx):
    config = SimpleNamespace(model="llama-groq", offering_id="off-1", runtime_offering_id=None, metadata={})
    assert await baa_gate.swap_for_baa(config, _profile("llama-groq", "groq")) is True
    assert config.model == "claude-haiku-5-5"
    assert config.offering_id is None
    assert config.metadata["model_swap_reason"] == "hipaa"
    assert len(ctx.emitter.infos) == 1
    assert "not covered in HIPAA mode" in ctx.emitter.infos[0].user_message


@pytest.mark.asyncio
async def test_ungated_groq_chat_is_untouched(ungated, ctx):
    config = SimpleNamespace(model="llama-groq", offering_id=None, runtime_offering_id=None, metadata={})
    assert await baa_gate.swap_for_baa(config, _profile("llama-groq", "groq")) is False
    assert config.model == "llama-groq"
    await baa_gate.admit_baa(_profile("llama-groq", "groq"))


@pytest.mark.asyncio
async def test_standin_above_the_free_tier_ceiling_is_refused(gated, ctx, monkeypatch):
    ftm.set_free_tier_policy_resolver(lambda c: ftm.FreeTierPolicy(tier="guest", max_cost_rating=1))
    try:
        config = SimpleNamespace(model="llama-groq", offering_id=None, runtime_offering_id=None, metadata={})
        with pytest.raises(baa_gate.BaaRefusedError):
            await baa_gate.swap_for_baa(config, _profile("llama-groq", "groq"))
        assert config.model == "llama-groq"
    finally:
        ftm.set_free_tier_policy_resolver(None)


@pytest.mark.asyncio
async def test_gated_typesafe_decision_is_refused_not_swapped(gated, ctx):
    profile = _profile("typesafe-decide", "typesafe", "decision")
    config = SimpleNamespace(model="typesafe-decide", offering_id=None, runtime_offering_id=None, metadata={})
    assert await baa_gate.swap_for_baa(config, profile) is False
    with pytest.raises(baa_gate.BaaRefusedError) as err:
        await baa_gate.admit_baa(profile)
    assert err.value.code == "hipaa_not_covered"
    assert "TypeSafe" not in err.value.message  # never the vendor's name in the person's sentence
    assert err.value.vendor == "typesafe"


@pytest.mark.asyncio
async def test_gated_openai_image_generation_is_refused(gated, ctx):
    with pytest.raises(baa_gate.BaaRefusedError):
        await baa_gate.admit_baa(_profile("gpt-image", "openai", caps={"produces_image": True}))


@pytest.mark.asyncio
async def test_gated_device_route_is_refused(gated, ctx):
    profile = _profile("local-llama", "anthropic")
    profile.route_kind = "device"
    with pytest.raises(baa_gate.BaaRefusedError):
        await baa_gate.admit_baa(profile)


@pytest.mark.asyncio
async def test_gated_call_in_capture_mode_is_still_refused_and_never_dispatched(gated, ctx):
    dispatched: list[bool] = []

    async def dispatch() -> Any:
        dispatched.append(True)
        return None

    with capturing_provider_request():
        with pytest.raises(baa_gate.BaaRefusedError):
            await UnifiedAIClient._dispatch_with_billing_net(
                dispatch, profile=_profile("llama-groq", "groq"), firewall_checked=True
            )
    assert dispatched == []


@pytest.mark.asyncio
async def test_unreadable_hipaa_status_refuses(ctx):
    async def host(_ctx: Any) -> Any:
        raise RuntimeError("db down")

    baa_gate.set_baa_policy_host(host)
    try:
        with pytest.raises(baa_gate.BaaRefusedError):
            await baa_gate.admit_baa(_profile("claude", "anthropic"))
    finally:
        baa_gate.set_baa_policy_host(None)


@pytest.mark.asyncio
async def test_own_key_is_refused_when_not_attested(gated, ctx, monkeypatch):
    monkeypatch.setattr("matrx_ai.providers.keys.last_resolved_key_source", lambda: "own")
    with pytest.raises(baa_gate.BaaRefusedError):
        await baa_gate.refuse_own_key_if_gated(_profile("claude", "anthropic"))


@pytest.mark.asyncio
async def test_openai_covered_call_loses_retention_and_hosted_tools(gated, ctx):
    config = SimpleNamespace(model="gpt", store=None, extended_prompt_cache=True,
                             internal_web_search=True, internal_x_search=None, internal_url_context=None)
    changed = await baa_gate.apply_baa_features(config, _profile("gpt", "openai"))
    assert config.store is False
    assert config.extended_prompt_cache is False
    assert config.internal_web_search is None
    assert set(changed) == {"store", "extended_prompt_cache", "internal_web_search"}


@pytest.mark.asyncio
async def test_gated_audio_with_no_stt_standin_is_refused(gated, ctx):
    with pytest.raises(baa_gate.BaaRefusedError):
        await baa_gate.stt_standin_or_refuse()


@pytest.mark.asyncio
async def test_reroute_never_offers_an_uncovered_vendor(gated, ctx):
    assert await baa_gate.covered_sibling_filter("groq") is False
    assert await baa_gate.covered_sibling_filter("anthropic") is True


@pytest.mark.asyncio
async def test_the_hipaa_stand_in_runs_this_turn_only(gated, ctx):
    """CGU-10 IMG8 #2: the BAA swap had the free-tier swap's shape — the stand-in and the cleared pin
    were stored with the chat. Red when ``swap_for_baa`` drops its ``begin_model_this_turn_only``."""
    from matrx_ai.config.unified_config import UnifiedConfig

    config = UnifiedConfig(model="llama-groq", offering_id="off-1", messages=[])
    assert await baa_gate.swap_for_baa(config, _profile("llama-groq", "groq")) is True
    assert config.model == "claude-haiku-5-5"
    stored = config.to_storage_dict()
    assert stored["model"] == "llama-groq"
    assert stored["config"].get("offering_id") == "off-1"


@pytest.mark.asyncio
async def test_gated_transcription_runs_on_the_stt_standin_when_one_is_set(ctx, monkeypatch):
    class _WithStandin(_Policy):
        stt_standin_model = "covered-stt"

    async def host(_ctx: Any) -> _Policy:
        return _WithStandin()

    baa_gate.set_baa_policy_host(host)
    try:
        groq = _profile("whisper-large-v3-turbo", "groq")
        assert await baa_gate.stt_model_for_baa(groq) == "covered-stt"
    finally:
        baa_gate.set_baa_policy_host(None)


@pytest.mark.asyncio
async def test_gated_transcription_with_no_standin_is_left_for_the_seam_to_refuse(gated, ctx):
    caps = dict(supports_audio_input=True, supports_text_input=False, produces_text=True)
    groq = _profile("whisper-large-v3-turbo", "groq", caps=caps)
    assert await baa_gate.stt_model_for_baa(groq) is None
    with pytest.raises(baa_gate.BaaRefusedError):
        await baa_gate.admit_baa(groq)


@pytest.mark.asyncio
async def test_ungated_transcription_is_untouched(ungated, ctx):
    assert await baa_gate.stt_model_for_baa(_profile("whisper-large-v3-turbo", "groq")) is None
