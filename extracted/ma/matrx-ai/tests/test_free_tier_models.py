"""The free-tier model ceiling: guests and free accounts never run a premium model.

Forcing tests for FREE-ALLOWANCE.md attack A1 (premium model through /ai/chat or /ai/manual by a
guest): the swap must happen at the ONE place every chat/media call resolves its model
(``UnifiedAIClient._execute_dispatch``), keyed on the request's tier — never on the client's
choice — and the paid-call seam must refuse a premium model that has no stand-in.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.providers import free_tier_models as ftm

ROWS: dict[str, SimpleNamespace] = {}


def _row(name: str, rating: int | None, *, guest: str | None = None, mid: str | None = None,
         premium: bool = False, metadata: dict[str, Any] | None = None,
         capabilities: dict[str, Any] | None = None) -> SimpleNamespace:
    row = SimpleNamespace(
        id=f"id-{name}", name=name, common_name=name.title(), cost_rating=rating,
        guest_fallback_id=f"id-{guest}" if guest else None,
        mid_fallback_id=f"id-{mid}" if mid else None,
        is_premium=premium, metadata=metadata or {},
        capabilities=capabilities or {"input": ["text"], "output": ["text"], "interaction": "turn"},
    )
    ROWS[name] = row
    ROWS[row.id] = row
    return row


_row("haiku", 1)
_row("flash", 3)
_row("flash-lite", 1)
_row("sonnet", 5, guest="haiku", mid="haiku")
_row("opus", 4, guest="haiku", mid="sonnet", premium=True)
_row("opus-max", 6, guest="haiku", mid="sonnet")
_row("image-premium", 5)
_row("local-unrated", None)
_row("allowed-anyway", 5, metadata={"free_tier": "allow"})
# The live catalog's Gemini image rows (ai.model_definition, 2026-11-02): the CALL shape is
# "turn" like any chat model; only ``capabilities.output`` says they make images.
_GEMINI_IMAGE_CAPS = {"input": ["text", "image"], "output": ["image", "text"],
                      "features": ["web_search", "image_generation"], "interaction": "turn",
                      "multilingual": True}
_row("gemini-3.1-flash-image", 1, capabilities=_GEMINI_IMAGE_CAPS)
_row("gemini-3-pro-image", 1, premium=True, capabilities=_GEMINI_IMAGE_CAPS)
_row("gemini-3-pro-image-fb", 1, premium=True, mid="gemini-3.1-flash-image",
     guest="gemini-3.1-flash-image", capabilities=_GEMINI_IMAGE_CAPS)
_row("image-fb-to-chat", 1, premium=True, mid="flash", guest="flash-lite",
     capabilities=_GEMINI_IMAGE_CAPS)

# The rows a free account's podcast died on (live run 7a1ca3ff, 2026-11-16): premium media models
# with NO declared fallback. Same provider + same inputs/outputs is what may stand in.
_TTS = {"input": ["text"], "output": ["audio"], "interaction": "turn"}
_VIDEO = {"input": ["text", "image"], "output": ["video"], "interaction": "turn"}
for _n, _r, _p, _c, _prov in (
    ("gem-2.5-pro-tts", 5, True, _TTS, "google"),
    ("gem-2.5-flash-tts", 4, False, _TTS, "google"),
    ("gem-3.8-flash-tts", 4, False, _TTS, "google"),
    ("gem-3.8-flash-lite-tts", 3, False, _TTS, "google"),
    ("gem-music", 2, False, {"input": ["text"], "output": ["audio", "text"], "interaction": "turn"}, "google"),
    ("other-tts", 1, False, _TTS, "openai"),
    ("vid-fast", 1, True, _VIDEO, "google"),
    ("vid-lite", 1, False, _VIDEO, "google"),
    ("vid-t2v-only", 1, False, {"input": ["text"], "output": ["video"], "interaction": "turn"}, "google"),
    ("lonely-premium-video", 5, True, _VIDEO, "nobody-else"),
):
    _row(_n, _r, premium=_p, capabilities=_c).provider_id = _prov
ROWS["gem-2.5-flash-tts"].is_deprecated = False

GUEST = ftm.FreeTierPolicy(tier="guest", max_cost_rating=3, default_model="flash-lite")
FREE = ftm.FreeTierPolicy(tier="free", max_cost_rating=4, default_model="flash")


@pytest.fixture(autouse=True)
def _catalog(monkeypatch: pytest.MonkeyPatch):
    async def _load(name_or_id: str):
        return ROWS.get(name_or_id)

    async def _all():
        return list({id(r): r for r in ROWS.values()}.values())

    monkeypatch.setattr(ftm, "_load", _load)
    monkeypatch.setattr(ftm, "_all_models", _all)
    ftm._told.clear()
    yield
    ftm.set_free_tier_policy_resolver(None)


class _Emitter:
    def __init__(self) -> None:
        self.infos: list[Any] = []

    async def send_info(self, payload: Any) -> None:
        self.infos.append(payload)


def _ctx(policy: ftm.FreeTierPolicy | None, **kw: Any) -> SimpleNamespace:
    ctx = SimpleNamespace(user_id="u-1", request_id=kw.get("request_id", "r-1"), emitter=_Emitter(),
                          policy=policy)
    ftm.set_free_tier_policy_resolver(lambda c: c.policy)
    return ctx


@pytest.mark.asyncio
async def test_guest_premium_swaps_to_its_guest_fallback():
    assert await ftm.free_tier_target("sonnet", GUEST) == ("haiku", "")


@pytest.mark.asyncio
async def test_free_account_fallback_above_ceiling_goes_to_the_default():
    # opus-max's mid fallback is sonnet (5) — still premium for free (4) → the default model.
    assert await ftm.free_tier_target("opus-max", FREE) == ("flash", "")


@pytest.mark.asyncio
async def test_premium_flag_counts_even_within_the_rating():
    assert await ftm.free_tier_target("opus", FREE) == ("flash", "")  # mid=sonnet is premium too
    assert await ftm.free_tier_target("opus", GUEST) == ("haiku", "")


@pytest.mark.asyncio
async def test_within_ceiling_and_overrides_run_as_asked():
    assert await ftm.free_tier_target("flash", GUEST) is None
    assert await ftm.free_tier_target("allowed-anyway", GUEST) is None


@pytest.mark.asyncio
async def test_unrated_turn_model_is_premium_but_unrated_single_call_is_not():
    assert await ftm.free_tier_target("local-unrated", GUEST) == ("flash-lite", "")
    assert await ftm.free_tier_target("local-unrated", GUEST, interaction="single") is None


@pytest.mark.asyncio
async def test_unrated_turn_media_model_follows_the_unrated_policy_knob():
    """e68a653c1 exempted unrated media from the knob, so grok-imagine-image-2.0 and the
    ElevenLabs music / sound / speech-to-speech rows (null cost_rating, not is_premium,
    ``interaction: "turn"``) ran free for free-tier accounts. Unrated is premium under the
    default policy whatever the modality; with no image stand-in it is refused, never
    chat-answered; turning the knob off lets it run."""
    _row("unrated-image", None, capabilities={"input": ["text"], "output": ["image"], "interaction": "turn"})
    for policy in (GUEST, FREE):
        assert ftm.is_premium_for(ROWS["unrated-image"], policy) is True
        target = await ftm.free_tier_target("unrated-image", policy)
        assert target is not None and target[0] == "", target
    relaxed = ftm.FreeTierPolicy(tier="free", max_cost_rating=4, default_model="flash", unrated_is_premium=False)
    assert ftm.is_premium_for(ROWS["unrated-image"], relaxed) is False


@pytest.mark.asyncio
async def test_premium_media_model_with_no_stand_in_is_never_answered_by_a_chat_model():
    target = await ftm.free_tier_target("image-premium", GUEST, interaction="single")
    assert target is not None and target[0] == ""


@pytest.mark.asyncio
async def test_turn_shaped_image_model_is_never_answered_by_the_chat_default():
    """Live 2026-11-02 (workflow runs d38f7bcc…, 5088a12b…): a free account's
    ``gemini-3-pro-image`` step (premium, no fallback, ``interaction: "turn"``) was swapped to
    the tier's default CHAT model; it answered in prose and the step failed "provider returned
    no images". A premium image model with no image stand-in is refused, never chat-answered."""
    for policy in (GUEST, FREE):
        target = await ftm.free_tier_target("gemini-3-pro-image", policy)
        assert target is not None and target[0] == "", target


@pytest.mark.asyncio
async def test_image_model_fallback_must_make_images_too():
    assert await ftm.free_tier_target("gemini-3-pro-image-fb", FREE) == ("gemini-3.1-flash-image", "")
    assert await ftm.free_tier_target("gemini-3-pro-image-fb", GUEST) == ("gemini-3.1-flash-image", "")
    # A catalog fallback that points an image model at a chat model is ignored.
    target = await ftm.free_tier_target("image-fb-to-chat", FREE)
    assert target is not None and target[0] == ""


@pytest.mark.asyncio
async def test_dispatch_swap_leaves_a_turn_shaped_image_model_alone(monkeypatch):
    ctx = _ctx(FREE)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = SimpleNamespace(model="gemini-3-pro-image", offering_id=None,
                             runtime_offering_id=None, metadata={})
    profile = SimpleNamespace(model_name="gemini-3-pro-image",
                              capabilities=SimpleNamespace(interaction="turn", produces_image=True))
    assert await ftm.swap_for_free_tier(config, profile) is False
    assert config.model == "gemini-3-pro-image"
    assert ctx.emitter.infos == []


@pytest.mark.asyncio
async def test_swap_rewrites_config_drops_the_offering_pin_and_says_so_once(monkeypatch):
    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = SimpleNamespace(model="sonnet", offering_id="off-1", runtime_offering_id=None, metadata={},
                             model_picked_by_person=True)
    profile = SimpleNamespace(model_name="sonnet", capabilities=SimpleNamespace(interaction="turn"))
    assert await ftm.swap_for_free_tier(config, profile) is True
    assert config.model == "haiku" and config.offering_id is None
    assert config.metadata["original_model"] == "sonnet"
    config2 = SimpleNamespace(model="sonnet", offering_id=None, runtime_offering_id=None, metadata={},
                              model_picked_by_person=True)
    assert await ftm.swap_for_free_tier(config2, profile) is True  # a later turn of the same request
    assert len(ctx.emitter.infos) == 1
    info = ctx.emitter.infos[0]
    assert info.code == ftm.MODEL_SWAPPED_INFO_CODE
    assert info.user_message == "Ran on Haiku. Sign up free for Sonnet."


@pytest.mark.asyncio
async def test_paid_person_is_never_swapped(monkeypatch):
    ctx = _ctx(None)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = SimpleNamespace(model="opus-max", metadata={})
    profile = SimpleNamespace(model_name="opus-max", capabilities=SimpleNamespace(interaction="turn"))
    assert await ftm.swap_for_free_tier(config, profile) is False
    assert config.model == "opus-max"


@pytest.mark.asyncio
async def test_seam_backstop_refuses_premium_without_stand_in(monkeypatch):
    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    profile = SimpleNamespace(model_name="image-premium", model_id="id-image-premium",
                              model_cost_rating=5, capabilities=SimpleNamespace(interaction="single"))
    with pytest.raises(ftm.FreeTierModelRefusedError) as err:
        await ftm.admit_free_tier_model(profile)
    assert err.value.is_caller_refusal and err.value.fix_action == "sign_up"
    ok = SimpleNamespace(model_name="haiku", model_id="id-haiku", model_cost_rating=1,
                         capabilities=SimpleNamespace(interaction="turn"))
    await ftm.admit_free_tier_model(ok)


@pytest.mark.asyncio
async def test_execute_dispatch_swaps_before_anything_runs(monkeypatch):
    """The class guard: the client's model (``ai_model_id`` on /ai/chat and /ai/manual) reaches
    ``_execute_dispatch`` unswapped; the dispatch must re-resolve onto the stand-in. Red before the
    swap was wired there (the profile was resolved once, on the client's model)."""
    import matrx_ai.catalog.resolve as resolve_mod
    from matrx_ai.providers.unified_client import UnifiedAIClient

    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    asked: list[str] = []

    class _Stop(Exception):
        pass

    async def _resolve(model: str, *_a: Any, **_k: Any):
        asked.append(model)
        if len(asked) > 1:
            raise _Stop
        return SimpleNamespace(model_name=model, model_cost_rating=ROWS[model].cost_rating,
                               capabilities=SimpleNamespace(interaction="turn"))

    monkeypatch.setattr(resolve_mod, "resolve_tts_call_profile", _resolve)
    config = SimpleNamespace(model="sonnet", offering_id=None, runtime_offering_id=None,
                             routing_offering_id=None, tts_quality=None, metadata={})
    request = SimpleNamespace(config=config, debug=False)
    client = UnifiedAIClient.__new__(UnifiedAIClient)
    with pytest.raises(_Stop):
        await client._execute_dispatch(request)  # type: ignore[arg-type]
    assert asked == ["sonnet", "haiku"]


@pytest.mark.asyncio
async def test_seam_backstop_admits_a_device_served_run(monkeypatch):
    """A run on the person's own computer (route_kind "device") costs 0.0 and spends nobody's
    money, so the free-tier ceiling never refuses it — whatever the model's cost rating."""
    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    premium = dict(model_name="image-premium", model_id="id-image-premium", model_cost_rating=5,
                   capabilities=SimpleNamespace(interaction="turn"))
    with pytest.raises(ftm.FreeTierModelRefusedError):  # the same model in the cloud is refused
        await ftm.admit_free_tier_model(SimpleNamespace(**premium))
    device = SimpleNamespace(**premium, route_kind="device", served_via=object())
    await ftm.admit_free_tier_model(device)


@pytest.mark.asyncio
async def test_the_stand_in_runs_this_turn_only_and_the_chat_keeps_its_model_and_pin(monkeypatch):
    """CGU-10 IMG8 #2 (scratch run): the swap wrote ``config.model`` and cleared the pin on the STORED
    config, so the chat was saved on the stand-in with no pin and every later turn stayed there, even
    after an upgrade. The stand-in now answers this turn only. Red when the swap drops its
    ``begin_model_this_turn_only``."""
    from matrx_ai.config.unified_config import UnifiedConfig

    ctx = _ctx(GUEST)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = UnifiedConfig(model="sonnet", offering_id="off-1", messages=[])
    profile = SimpleNamespace(model_name="sonnet", capabilities=SimpleNamespace(interaction="turn"))
    assert await ftm.swap_for_free_tier(config, profile) is True
    assert config.model == "haiku" and config.offering_id is None  # this turn runs on the stand-in
    stored = config.to_storage_dict()
    assert stored["model"] == "sonnet", f"the stand-in was stored as the chat's model: {stored['model']!r}"
    assert stored["config"].get("offering_id") == "off-1", "the swap erased the person's pin from the chat"
    assert config.end_model_this_turn_only() is True  # the resolver's next-turn start
    assert (config.model, config.offering_id) == ("sonnet", "off-1")


@pytest.mark.asyncio
async def test_a_premium_media_model_with_no_declared_fallback_runs_on_its_nearest_sibling():
    """The podcast that died at its audio step: the platform picked the voice and clip models, the
    free tier may not run them, and no fallback was declared. Same provider, same inputs/outputs,
    same family first, highest rating under the line — never a refusal while one exists."""
    assert await ftm.free_tier_target("gem-2.5-pro-tts", FREE) == ("gem-2.5-flash-tts", "")
    assert await ftm.free_tier_target("gem-2.5-pro-tts", GUEST) == ("gem-3.8-flash-lite-tts", "")
    assert await ftm.free_tier_target("vid-fast", FREE) == ("vid-lite", "")


@pytest.mark.asyncio
async def test_the_automatic_stand_in_is_never_another_provider_or_another_shape():
    target = await ftm.free_tier_target("lonely-premium-video", FREE)
    assert target is not None and target[0] == ""
    for name in ("gem-2.5-pro-tts", "vid-fast"):
        chosen = (await ftm.free_tier_target(name, FREE))[0]
        assert chosen not in {"gem-music", "other-tts", "vid-t2v-only"}


def test_the_refusal_sentence_never_names_a_model():
    err = ftm.FreeTierModelRefusedError(model_name="gemini-2.5-pro-preview-tts", tier="free", user_id="u")
    assert "gemini" not in err.message and "gemini" not in err.error_info.user_message
    assert "needs a paid plan" in err.message
    assert err.envelope()["model_name"] == "gemini-2.5-pro-preview-tts"


# 2026-11-18: a guest's podcast voice. The live ``gemini-3.8-flash-tts`` (rating 4) declares the
# guest fallback ``gemini-3.8-flash-lite-tts``, which has NO linked voices: the chosen voice was
# refused at the voice step. A TTS stand-in must carry the original's voices.
for _n, _r, _kw in (
    ("vt-main", 4, {"guest": "vt-lite", "mid": "vt-lite"}),
    ("vt-lite", 3, {}),
    ("vt-alt", 2, {}),
    ("vt-solo", 4, {"guest": "vt-solo-lite"}),
    ("vt-solo-lite", 3, {}),
):
    _row(_n, _r, capabilities=_TTS, **_kw).provider_id = "voiced" if _n != "vt-solo" and _n != "vt-solo-lite" else "solo"
_VOICES = {"vt-main": {"orus", "kore"}, "vt-alt": {"orus", "kore", "puck"}, "vt-solo": {"orus"}}


@pytest.fixture
def _voiced(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(ftm, "_voice_ids", lambda row: frozenset(_VOICES.get(row.name, ())), raising=False)


@pytest.mark.asyncio
async def test_a_tts_stand_in_must_carry_the_voices_else_the_next_in_ceiling_model_that_does(_voiced):
    # vt-lite is the declared guest fallback but has no voices -> skipped; vt-alt carries them.
    assert await ftm.free_tier_target("vt-main", GUEST) == ("vt-alt", "")


@pytest.mark.asyncio
async def test_a_tts_with_no_voiced_stand_in_is_refused_at_the_start_not_voiceless(_voiced):
    target = await ftm.free_tier_target("vt-solo", GUEST)
    assert target is not None and target[0] == ""


@pytest.mark.asyncio
async def test_a_model_the_person_never_picked_is_swapped_silently(monkeypatch):
    """Arman, 2026-11-20: a guest who just opened chat was told "Ran on Claude Haiku 5.5. Sign up free for
    Claude Opus 5.5." about a model they never chose. The stand-in still answers; nothing is said and no
    sentence is saved on the answer."""
    ctx = _ctx(GUEST)
    ctx.metadata = {}
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    config = SimpleNamespace(model="sonnet", offering_id=None, runtime_offering_id=None, metadata={})
    profile = SimpleNamespace(model_name="sonnet", capabilities=SimpleNamespace(interaction="turn"))
    assert await ftm.swap_for_free_tier(config, profile) is True
    assert config.model == "haiku"
    assert ctx.emitter.infos == []
    assert ftm.MODEL_SWAP_NOTE_KEY not in ctx.metadata


_row("rerank-unrated", None, capabilities={"input": ["text"], "output": ["text"], "interaction": "rerank"})


@pytest.mark.asyncio
async def test_a_direct_seam_route_without_capabilities_takes_the_call_shape_from_the_catalog(monkeypatch):
    """A rerank's hand-built route carries no ``capabilities``; the backstop read that absence as a chat
    turn, so an unrated rerank model counted as premium and a free account was refused. The catalog row
    says ``rerank`` and that is what decides."""
    ctx = _ctx(FREE)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    route = SimpleNamespace(vendor="cohere", model_name="rerank-unrated", endpoint_id="cohere-rerank",
                            base_url="", offering_metadata={})
    await ftm.admit_free_tier_model(route, in_admitted_run=False)


@pytest.mark.asyncio
async def test_a_direct_fastino_extraction_is_never_refused_as_a_premium_chat_turn(monkeypatch):
    """Live 2026-11-20: a free account's transcript autolabel (``FastinoExtraction.extract`` with no
    catalog profile, model ``fastino/gliner2-base-v1`` — no catalog row by that name) was refused
    "needs a paid plan" 15 times. The direct route declares it is an extraction."""
    from matrx_ai.providers import guardrail_gate
    from matrx_ai.providers.fastino import fastino_api
    from matrx_ai.providers.unified_client import UnifiedAIClient

    ctx = _ctx(FREE)
    monkeypatch.setattr("matrx_ai.context.app_context.try_get_app_context", lambda: ctx)
    seen: list[Any] = []

    async def _net(dispatch, *, profile, quote):  # noqa: ANN001
        seen.append(profile)
        await ftm.admit_free_tier_model(profile, in_admitted_run=False)
        return "ran"

    monkeypatch.setattr(UnifiedAIClient, "_dispatch_with_billing_net", staticmethod(_net))
    monkeypatch.setattr(fastino_api, "gliner2_url", lambda: "https://example.invalid")
    monkeypatch.setattr(guardrail_gate, "quote_tokens", lambda *a, **k: None)
    out = await fastino_api.FastinoExtraction().extract("hello", ["person"], model_class="fastino/gliner2-base-v1")
    assert out == "ran"
    assert seen[0].capabilities.interaction == "extraction"
