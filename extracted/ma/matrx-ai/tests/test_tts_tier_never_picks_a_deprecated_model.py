"""A TTS quality tier never routes a call onto a deprecated or retired model.

Live 2026-11-16: every saved podcast asks ``tts_quality="high_quality"``; the audio agents pin the
live gemini-3.8-flash-tts, whose offering carried no tier tag, so the catalog picked the vendor's
``high_quality`` offering — the DEPRECATED gemini-2.5-pro-preview-tts (premium) — and a free
account's podcast was refused at its audio step. The host-catalog branch of
``resolve_tts_call_profile`` already skipped deprecated rows; ``AiCatalogManager.tts_offering``
(the DB-backed branch every server call takes) did not.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.catalog.manager import AiCatalogManager


def _manager() -> AiCatalogManager:
    mgr = object.__new__(AiCatalogManager)  # never the process singleton
    mgr._init()
    mgr._endpoints = {"ep-google": SimpleNamespace(vendor="google", is_active=True)}

    def offering(oid: str, model_id: str, tiers: list[str], is_default: bool) -> SimpleNamespace:
        return SimpleNamespace(
            id=oid, model_id=model_id, endpoint_id="ep-google", is_available=True, priority=100,
            metadata={"tts": {"quality_tiers": tiers, "is_default": is_default}},
        )

    mgr._offerings = {
        "off-old": offering("off-old", "m-old", ["high_quality"], True),
        "off-live": offering("off-live", "m-live", ["high_quality", "fast"], False),
        "off-retired": offering("off-retired", "m-retired", ["high_quality"], True),
    }
    mgr._model_state = {
        "m-old": {"name": "gemini-2.5-pro-preview-tts", "is_deprecated": True, "retired_at": None},
        "m-live": {"name": "gemini-3.8-flash-tts", "is_deprecated": False, "retired_at": None},
        "m-retired": {"name": "old-retired-tts", "is_deprecated": False, "retired_at": "2026-10-01"},
    }
    return mgr


def test_high_quality_tier_skips_deprecated_and_retired_models() -> None:
    picked = _manager().tts_offering("google", "high_quality")
    assert picked is not None and picked.id == "off-live", picked


def test_no_live_model_in_the_tier_answers_none_never_a_deprecated_one() -> None:
    mgr = _manager()
    del mgr._offerings["off-live"]
    assert mgr.tts_offering("google", "high_quality") is None
