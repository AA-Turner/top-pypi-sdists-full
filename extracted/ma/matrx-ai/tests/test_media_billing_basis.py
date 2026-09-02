"""Regression tests for basis-aware media-generation billing.

Guards the bug where a token-priced media model (pricing tier with NO
``usage_basis``) was billed the synthetic ``1_000_000`` output-token sentinel,
turning ``output_price`` ($/1M tokens) into a flat $/image charge — a
~1,000,000× overcharge (gpt-image-2 billed $30 for a ~$0.17 image).

Invariants locked in:
  - token-priced tier (no usage_basis) + provider usage  → bill REAL tokens
  - synthetic-basis tier (image_output, …)               → bill synthetic units
  - token-priced tier + NO provider usage                → cost 0, never 1M×
"""

from __future__ import annotations

import asyncio
import types

import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.config import usage_config as uc
from matrx_ai.config.usage_config import (
    ModelPricing,
    PricingTier,
    TokenUsage,
    build_character_billed_usage,
)
from matrx_ai.providers.base_media import BaseMediaGeneration, GeneratedAsset
from matrx_ai.providers.google.google_image_api import GoogleImageGeneration
from matrx_ai.providers.openai.openai_image_api import OpenAIImageGeneration


@pytest.fixture
def warm_pricing():
    """Install a known pricing lookup; restore the real cache afterwards."""
    saved = uc._pricing_lookup_cache
    saved_warned = set(uc._billing_warned)
    uc._billing_warned.clear()
    uc._pricing_lookup_cache = {
        # token-priced (no usage_basis) — the previously-buggy shape
        "gpt-image-2": ModelPricing(
            "gpt-image-2",
            "openai",
            [
                PricingTier(
                    None,
                    input_price=8,
                    output_price=30,
                    cached_input_price=2,
                    usage_basis=None,
                    component_prices={
                        "input.text": 5,
                        "input.image": 8,
                        "cached_input.text": 1.25,
                        "cached_input.image": 2,
                        "output.image": 30,
                    },
                )
            ],
        ),
        "gemini-2.5-flash-image": ModelPricing(
            "gemini-2.5-flash-image",
            "google",
            [
                PricingTier(
                    None,
                    input_price=0.3,
                    output_price=30,
                    cached_input_price=0.075,
                    usage_basis=None,
                )
            ],
        ),
        # synthetic per-image — must stay exactly $output_price/image
        "imagen-4.0-generate-001": ModelPricing(
            "imagen-4.0-generate-001",
            "google",
            [
                PricingTier(
                    None,
                    input_price=0,
                    output_price=0.04,
                    cached_input_price=0,
                    usage_basis="image_output",
                )
            ],
        ),
        "gemini-3-pro-image-preview": ModelPricing(
            "gemini-3-pro-image-preview",
            "google",
            [
                PricingTier(
                    None,
                    input_price=2,
                    output_price=0.134,
                    cached_input_price=0.2,
                    usage_basis="image_output",
                )
            ],
        ),
        # character-billed TTS ($/1M chars)
        "tts-1": ModelPricing(
            "tts-1",
            "openai",
            [
                PricingTier(
                    None,
                    input_price=15,
                    output_price=0,
                    cached_input_price=0,
                    usage_basis="character_input",
                )
            ],
        ),
        # token-priced TTS on a usage-less endpoint — must NOT silently bill $0-ish
        "legacy-token-tts": ModelPricing(
            "legacy-token-tts",
            "openai",
            [
                PricingTier(
                    None, input_price=0.6, output_price=12, cached_input_price=0, usage_basis=None
                )
            ],
        ),
    }
    try:
        yield
    finally:
        uc._pricing_lookup_cache = saved
        uc._billing_warned.clear()
        uc._billing_warned.update(saved_warned)


def _cfg(model: str) -> UnifiedConfig:
    return UnifiedConfig(model=model, messages=[])


def test_gpt_image_2_bills_real_tokens_not_per_image(warm_pricing):
    oi = OpenAIImageGeneration()
    raw = types.SimpleNamespace(
        usage=types.SimpleNamespace(
            input_tokens=669,
            output_tokens=5488,
            input_tokens_details=types.SimpleNamespace(
                text_tokens=669, image_tokens=0, cached_tokens=0
            ),
            output_tokens_details=types.SimpleNamespace(image_tokens=5488),
        ),
        id="resp",
    )
    usage = oi._build_usage(
        _cfg("gpt-image-2"), {"size": "1536x1024"}, raw, [GeneratedAsset(data=b"x")]
    )
    cost = usage.calculate_cost()

    assert usage.input_tokens == 669
    assert usage.output_tokens == 5488
    assert usage.metadata["billing_kind"] == "provider_tokens"
    assert usage.raw_usage is not None
    assert usage.billing_components == {
        "input.text": 669,
        "input.image": 0,
        "output.image": 5488,
    }
    # Text and image tokens have distinct rates — and neither is a flat $30.
    assert cost == pytest.approx(669 * 5 / 1e6 + 5488 * 30 / 1e6)
    assert 0.16 < cost < 0.18


def test_gpt_image_2_prices_text_and_image_input_components(warm_pricing):
    raw = types.SimpleNamespace(
        usage=types.SimpleNamespace(
            input_tokens=1_200,
            output_tokens=196,
            input_tokens_details=types.SimpleNamespace(
                text_tokens=200, image_tokens=1_000, cached_tokens=0
            ),
            output_tokens_details=types.SimpleNamespace(image_tokens=196),
        ),
        id="resp",
    )
    usage = OpenAIImageGeneration()._build_usage(
        _cfg("gpt-image-2"), {"size": "1024x1024"}, raw, [GeneratedAsset(data=b"x")]
    )

    assert usage.calculate_cost() == pytest.approx(
        (200 * 5 + 1_000 * 8 + 196 * 30) / 1e6
    )


def test_gpt_image_2_mixed_cached_input_remains_unknown(warm_pricing):
    raw = types.SimpleNamespace(
        usage=types.SimpleNamespace(
            input_tokens=1_300,
            output_tokens=196,
            input_tokens_details=types.SimpleNamespace(
                text_tokens=200, image_tokens=1_100, cached_tokens=100
            ),
            output_tokens_details=types.SimpleNamespace(image_tokens=196),
        )
    )
    usage = OpenAIImageGeneration()._build_usage(
        _cfg("gpt-image-2"), {}, raw, [GeneratedAsset(data=b"x")]
    )

    assert usage.billing_components["unallocated.cached_input"] == 100
    assert usage.calculate_cost() is None
    assert usage.metadata["cost_reconciliation"] == "unknown_component_allocation"


def test_cost_lookup_prefers_exact_offering_over_model_name(warm_pricing):
    uc._pricing_lookup_cache["replicate-offering"] = ModelPricing(
        "gpt-image-2",
        "replicate",
        [PricingTier(None, 0, 0.05, 0, usage_basis="image_output")],
    )
    usage = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name="gpt-image-2",
        api="replicate",
        offering_id="replicate-offering",
    )

    assert usage.calculate_cost() == pytest.approx(0.05)


def test_recorded_offering_miss_never_falls_back_to_model_price(warm_pricing):
    usage = TokenUsage(
        input_tokens=0,
        output_tokens=1_000_000,
        matrx_model_name="gpt-image-2",
        api="replicate",
        offering_id="missing-recorded-offering",
    )

    assert usage.calculate_cost() is None


def test_unpinned_preferred_media_route_bills_resolved_offering(warm_pricing):
    openai_pricing = uc._pricing_lookup_cache["gpt-image-2"]
    uc._pricing_lookup_cache.pop("gpt-image-2")
    uc._pricing_lookup_cache["openai-preferred-offering"] = openai_pricing
    uc._pricing_lookup_cache["replicate-offering"] = ModelPricing(
        "gpt-image-2",
        "replicate",
        [PricingTier(None, 0, 0.05, 0, usage_basis="image_output")],
    )
    raw = types.SimpleNamespace(
        usage=types.SimpleNamespace(
            input_tokens=100,
            output_tokens=196,
            input_tokens_details=types.SimpleNamespace(
                text_tokens=100, image_tokens=0, cached_tokens=0
            ),
            output_tokens_details=types.SimpleNamespace(image_tokens=196),
        )
    )

    usage = OpenAIImageGeneration()._build_usage(
        _cfg("gpt-image-2"),
        {},
        raw,
        [GeneratedAsset(data=b"x")],
        offering_id="openai-preferred-offering",
        model_name="gpt-image-2",
    )

    assert usage.offering_id == "openai-preferred-offering"
    assert usage.metadata["billing_kind"] == "provider_tokens"
    assert usage.calculate_cost() == pytest.approx((100 * 5 + 196 * 30) / 1e6)


def test_imagen_synthetic_per_image_unchanged(warm_pricing):
    class _Imagen(GoogleImageGeneration):
        def __init__(self):
            self._is_imagen_call = True

    usage = _Imagen()._build_usage(
        _cfg("imagen-4.0-generate-001"), {}, types.SimpleNamespace(), [GeneratedAsset(data=b"x")]
    )
    assert usage.metadata["billing_kind"] == "synthetic:image_output"
    assert usage.calculate_cost() == pytest.approx(0.04)


def test_gemini_native_token_priced_bills_real_usage(warm_pricing):
    class _GemNative(GoogleImageGeneration):
        def __init__(self):
            self._is_imagen_call = False

    raw = types.SimpleNamespace(
        usage_metadata=types.SimpleNamespace(
            prompt_token_count=15, candidates_token_count=1290, cached_content_token_count=0
        )
    )
    usage = _GemNative()._build_usage(
        _cfg("gemini-2.5-flash-image"), {}, raw, [GeneratedAsset(data=b"x")]
    )
    assert usage.metadata["billing_kind"] == "provider_tokens"
    # ~$0.04 (1290 output tokens @ $30/1M), NOT $30.
    assert usage.calculate_cost() == pytest.approx(15 * 0.3 / 1e6 + 1290 * 30 / 1e6)


def test_gemini_per_image_tier_bills_per_image(warm_pricing):
    """gemini-3-pro carries usage_basis=image_output → flat $0.134/image."""

    class _GemNative(GoogleImageGeneration):
        def __init__(self):
            self._is_imagen_call = False

    raw = types.SimpleNamespace(
        usage_metadata=types.SimpleNamespace(
            prompt_token_count=15, candidates_token_count=1290, cached_content_token_count=0
        )
    )
    usage = _GemNative()._build_usage(
        _cfg("gemini-3-pro-image-preview"), {}, raw, [GeneratedAsset(data=b"x")]
    )
    assert usage.metadata["billing_kind"] == "synthetic:image_output"
    assert usage.calculate_cost() == pytest.approx(0.134)


def test_token_priced_without_usage_fails_loud_not_overcharge(warm_pricing):
    """No usage_basis AND no provider usage stays unknown, never 0 or 1M×."""

    class _Dummy(BaseMediaGeneration):
        provider = "openai"
        modality = "image"
        starting_message = ""

        def _build_kwargs(self, *a):
            return {}

        def _call_provider(self, *a):
            return None

        def _extract_assets(self, *a):
            return []

        def _classify_error(self, exc):
            return None

        def _telemetry_url(self, *a):
            return ""

    usage = _Dummy()._build_usage(
        _cfg("gpt-image-2"), {}, types.SimpleNamespace(), [GeneratedAsset(data=b"x")]
    )
    assert usage.output_tokens == 0
    assert usage.metadata["billing_kind"] == "uncomputable_no_basis_no_usage"
    assert usage.metadata["cost_reconciliation"] == "unknown_missing_provider_usage"
    assert usage.calculate_cost() is None
    assert usage.metadata["pricing_snapshot"]["input_price"] == 8.0


def test_gpt_image_missing_input_details_stays_unknown(warm_pricing):
    raw = types.SimpleNamespace(
        usage=types.SimpleNamespace(
            input_tokens=700,
            output_tokens=196,
            input_tokens_details=None,
            output_tokens_details=types.SimpleNamespace(image_tokens=196),
        )
    )

    usage = OpenAIImageGeneration()._build_usage(
        _cfg("gpt-image-2"), {}, raw, [GeneratedAsset(data=b"x")]
    )

    assert usage.billing_components["unallocated.input"] == 700
    assert usage.calculate_cost() is None


# --------------------------------------------------------------------------- #
# Audio / TTS — character billing
# --------------------------------------------------------------------------- #


def test_character_billed_tts_costs_per_character(warm_pricing):
    usage = build_character_billed_usage(
        characters=1000, matrx_model_name="tts-1", provider_model_name="tts-1", api="openai"
    )
    assert usage.input_tokens == 1000
    assert usage.metadata["billing_kind"] == "synthetic:character_input"
    assert usage.metadata["input_characters"] == 1000
    # 1000 chars @ $15/1M chars = $0.015 — NOT $0.
    assert usage.calculate_cost() == pytest.approx(0.015)


def test_token_priced_tts_without_usage_fails_loud_not_zero_silent(warm_pricing):
    """A token-priced TTS model on a usage-less endpoint can't be billed from
    chars → 0 billable tokens + a recorded char count + a loud warning."""
    usage = build_character_billed_usage(
        characters=1000,
        matrx_model_name="legacy-token-tts",
        provider_model_name="legacy-token-tts",
        api="openai",
    )
    assert usage.input_tokens == 0
    assert usage.metadata["billing_kind"] == "uncomputable_tts_no_usage"
    assert usage.metadata["input_characters"] == 1000  # preserved for reconciliation
    assert usage.calculate_cost() == 0.0


def test_calculate_cost_warns_on_missing_billable_units(warm_pricing):
    """character_input tier but input_tokens=0 → cost 0 AND a one-time warning."""
    uc._billing_warned.clear()
    z = TokenUsage(input_tokens=0, output_tokens=0, matrx_model_name="tts-1", api="openai")
    assert z.calculate_cost() == 0.0
    assert any("tts-1" in k for k in uc._billing_warned)


def test_calculate_cost_warns_on_unknown_usage_basis(warm_pricing):
    # A basis that is NOT in USAGE_BASIS_SPECS — the formula would apply the wrong unit.
    uc._pricing_lookup_cache["weird"] = ModelPricing(
        "weird",
        "xai",
        [
            PricingTier(
                None, input_price=0.05, output_price=0, cached_input_price=0, usage_basis="furlong"
            )
        ],
    )
    uc._billing_warned.clear()
    u = TokenUsage(input_tokens=10, output_tokens=0, matrx_model_name="weird", api="xai")
    u.calculate_cost()
    assert any("weird" in k for k in uc._billing_warned)


# --------------------------------------------------------------------------- #
# Computed synthetic units — megapixel + video-second
# --------------------------------------------------------------------------- #


class _MediaStub(BaseMediaGeneration):
    """Minimal concrete media generator for unit tests."""

    def __init__(self, provider: str, modality: str):
        self.provider = provider
        self.modality = modality
        self.starting_message = ""

    def _build_kwargs(self, *a):
        return {}

    def _call_provider(self, *a):
        return None

    def _extract_assets(self, *a):
        return []

    def _classify_error(self, exc):
        return None

    def _telemetry_url(self, *a):
        return ""


def test_megapixel_billing_uses_real_pixels(warm_pricing):
    uc._pricing_lookup_cache["mp-model"] = ModelPricing(
        "mp-model",
        "together",
        [
            PricingTier(
                None,
                input_price=0,
                output_price=0.03,
                cached_input_price=0,
                usage_basis="megapixel_output",
            )
        ],
    )
    gen = _MediaStub("together", "image")
    # 1536×1024 = 1.57 MP → $0.03 × 1.57 ≈ $0.0472 (NOT a flat $0.03/image).
    usage = gen._build_usage(
        _cfg("mp-model"),
        {"width": 1536, "height": 1024},
        types.SimpleNamespace(),
        [GeneratedAsset(data=b"x")],
    )
    assert usage.output_tokens == 1536 * 1024
    assert usage.metadata["billing_kind"] == "synthetic:megapixel_output"
    assert usage.calculate_cost() == pytest.approx(1536 * 1024 / 1e6 * 0.03)


def test_video_second_billing_uses_real_duration(warm_pricing):
    uc._pricing_lookup_cache["vid-model"] = ModelPricing(
        "vid-model",
        "google",
        [
            PricingTier(
                None,
                input_price=0,
                output_price=0.4,
                cached_input_price=0,
                usage_basis="video_second_output",
            )
        ],
    )
    gen = _MediaStub("google", "video")
    cfg = UnifiedConfig(model="vid-model", messages=[], duration_seconds=5)
    # 5 seconds × $0.40/s = $2.00 (NOT a flat $0.40 treating the clip as 1 second).
    usage = gen._build_usage(cfg, {}, types.SimpleNamespace(), [GeneratedAsset(data=b"x")])
    assert usage.output_tokens == 5 * 1_000_000
    assert usage.calculate_cost() == pytest.approx(2.0)


def test_video_second_without_duration_falls_back_and_screams(warm_pricing):
    uc._pricing_lookup_cache["vid-model"] = ModelPricing(
        "vid-model",
        "google",
        [
            PricingTier(
                None,
                input_price=0,
                output_price=0.4,
                cached_input_price=0,
                usage_basis="video_second_output",
            )
        ],
    )
    uc._billing_warned.clear()
    gen = _MediaStub("google", "video")
    cfg = UnifiedConfig(model="vid-model", messages=[])  # no duration_seconds
    usage = gen._build_usage(cfg, {}, types.SimpleNamespace(), [GeneratedAsset(data=b"x")])
    # Best-effort per-asset fallback (1×1M), NOT $0 — and a loud warning fired.
    assert usage.output_tokens == 1_000_000
    assert any("vid-model" in k for k in uc._billing_warned)


def test_video_second_billing_reads_nested_provider_config(warm_pricing):
    uc._pricing_lookup_cache["vid-model"] = ModelPricing(
        "vid-model", "google",
        [PricingTier(None, 0, 0.4, 0, usage_basis="video_second_output")],
    )
    gen = _MediaStub("google", "video")
    cfg = UnifiedConfig(model="vid-model", messages=[])
    provider_config = types.SimpleNamespace(duration_seconds=8)

    usage = gen._build_usage(
        cfg, {"config": provider_config}, types.SimpleNamespace(),
        [GeneratedAsset(data=b"x")],
    )

    assert usage.output_tokens == 8 * 1_000_000
    assert usage.calculate_cost() == pytest.approx(3.2)


@pytest.mark.asyncio
async def test_missing_billing_unit_creates_structured_error(monkeypatch, warm_pricing):
    captured: list[dict[str, object]] = []

    async def record_error(_error: BaseException, **fields: object) -> None:
        captured.append(fields)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda _name: record_error)
    gen = _MediaStub("google", "video")
    cfg = UnifiedConfig(model="vid-model", messages=[])
    uc._pricing_lookup_cache["vid-model"] = ModelPricing(
        "vid-model", "google",
        [PricingTier(None, 0, 0.4, 0, usage_basis="video_second_output")],
    )

    gen._build_usage(cfg, {}, types.SimpleNamespace(), [GeneratedAsset(data=b"x")])
    await asyncio.sleep(0)

    assert captured[0]["kind"] == uc.MISSING_BILLING_UNIT_KIND
    assert captured[0]["route"] == "media/billing"


# --------------------------------------------------------------------------- #
# Pricing validator — catches every bug class from this work
# --------------------------------------------------------------------------- #


def _caps(name: str, **kw):
    """Capability object from the model's declared jsonb — the only source."""
    from types import SimpleNamespace

    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    return resolve_model_capabilities(
        SimpleNamespace(
            name=name,
            capabilities={
                "input": kw.get("input", ["text"]),
                "output": kw.get("output", ["text"]),
                "features": kw.get("features", []),
                "interaction": kw.get("interaction", "turn"),
            },
        )
    )


def test_validator_flags_media_model_missing_basis():
    from matrx_ai.config.usage_config import validate_model_pricing

    issues = validate_model_pricing(
        "some-tts",
        "elevenlabs_chat",
        _caps("some-tts", output=["audio"]),
        [{"input_price": 60, "output_price": 0}],
        token_billed=False,
    )
    assert any(i.code == "missing_basis" and i.severity == "error" for i in issues)


def test_validator_flags_character_price_scale_bug():
    from matrx_ai.config.usage_config import validate_model_pricing

    # $/char (0.00006) instead of $/1M-char — the ElevenLabs 1e6× bug.
    issues = validate_model_pricing(
        "eleven",
        "elevenlabs_chat",
        _caps("eleven", output=["audio"]),
        [{"input_price": 0.00006, "output_price": 0, "usage_basis": "character_input"}],
        token_billed=False,
    )
    assert any(i.code == "char_price_scale" and i.severity == "error" for i in issues)


def test_validator_flags_unknown_basis():
    from matrx_ai.config.usage_config import validate_model_pricing

    issues = validate_model_pricing(
        "x",
        "xai_realtime",
        _caps("x", input=["audio", "text"], output=["audio", "text"], interaction="realtime"),
        [{"input_price": 0.05, "usage_basis": "furlong"}],
        token_billed=False,
    )
    assert any(i.code == "unknown_basis" and i.severity == "error" for i in issues)


def test_validator_flags_speech_to_text_missing_basis():
    """An STT model (audio in, text out, no tools) bills by duration — it needs an
    explicit usage_basis exactly like a TTS model does."""
    from matrx_ai.config.usage_config import validate_model_pricing

    issues = validate_model_pricing(
        "whisper-large-v3",
        "groq_chat",
        _caps("whisper-large-v3", input=["audio"], output=["text"]),
        [{"input_price": 0.04, "output_price": 0}],
        token_billed=False,
    )
    assert any(i.code == "missing_basis" and i.severity == "error" for i in issues)


def test_validator_does_not_flag_a_chat_model_that_hears():
    """A multimodal chat model accepts audio but bills on real text tokens — it must
    NOT be treated as a media model."""
    from matrx_ai.config.usage_config import validate_model_pricing

    issues = validate_model_pricing(
        "gemini-2.5-flash",
        "google_chat",
        _caps(
            "gemini-2.5-flash",
            input=["text", "image", "audio"],
            output=["text"],
            features=["function_calling"],
        ),
        [{"input_price": 0.3, "output_price": 2.5}],
        token_billed=False,
    )
    assert not [i for i in issues if i.severity == "error"]


def test_validator_passes_correct_models():
    from matrx_ai.config.usage_config import validate_model_pricing

    # token-billed image route (openai_image) — OK with no basis
    assert not [
        i
        for i in validate_model_pricing(
            "gpt-image-2",
            "openai_image",
            _caps("gpt-image-2", input=["image", "text"], output=["image"]),
            [{"input_price": 8, "output_price": 30}],
            token_billed=True,
        )
        if i.severity == "error"
    ]
    # Gemini's chat-shaped native image model also bills on tokens (it emits text too).
    assert not [
        i
        for i in validate_model_pricing(
            "gemini-2.5-flash-image",
            "google_image",
            _caps("gemini-2.5-flash-image", input=["image", "text"], output=["image", "text"]),
            [{"input_price": 2, "output_price": 12}],
            token_billed=True,
        )
        if i.severity == "error"
    ]
    # correct character_input
    assert not [
        i
        for i in validate_model_pricing(
            "tts-1",
            "openai_chat",
            _caps("tts-1", output=["audio"]),
            [{"input_price": 15, "output_price": 0, "usage_basis": "character_input"}],
            token_billed=False,
        )
        if i.severity == "error"
    ]
    # correct per-image (Imagen shares google_image but emits image bytes only)
    assert not [
        i
        for i in validate_model_pricing(
            "imagen",
            "google_image",
            _caps("imagen", input=["image", "text"], output=["image"]),
            [{"input_price": 0, "output_price": 0.04, "usage_basis": "image_output"}],
            token_billed=False,
        )
        if i.severity == "error"
    ]


def test_validator_flags_imagen_missing_basis_despite_shared_google_image_route():
    """Imagen shares the google_image wire route with the token-billed native Gemini
    image models. The route CANNOT decide billing — only the recorded
    ``ai.offering.token_billed`` flag can. Imagen's offering has it false, so a
    missing usage_basis is still an error."""
    from matrx_ai.config.usage_config import validate_model_pricing

    issues = validate_model_pricing(
        "imagen-4.0-generate-001",
        "google_image",
        _caps("imagen-4.0-generate-001", input=["image", "text"], output=["image"]),
        [{"input_price": 0, "output_price": 0.04}],
        token_billed=False,
    )
    assert any(i.code == "missing_basis" and i.severity == "error" for i in issues)


def test_token_billed_is_a_recorded_fact_not_a_route_guess():
    """Two models on the SAME wire route with the SAME capabilities and NO usage_basis
    disagree purely on the recorded flag. Nothing about the route or the capability
    shape may be allowed to decide it."""
    from matrx_ai.config.usage_config import validate_model_pricing

    caps = _caps("x", input=["image", "text"], output=["image"])
    pricing = [{"input_price": 8, "output_price": 30}]

    assert [
        i
        for i in validate_model_pricing(
            "guess-me", "openai_image", caps, pricing, token_billed=False
        )
        if i.code == "missing_basis"
    ]
    assert not [
        i
        for i in validate_model_pricing(
            "guess-me", "openai_image", caps, pricing, token_billed=True
        )
        if i.code == "missing_basis"
    ]
