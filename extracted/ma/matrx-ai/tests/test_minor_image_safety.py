"""Unit tests pinning the child image content-safety filter (WP13).

Structural guarantee: for a MINOR image request, a provider that cannot enforce
a filter REFUSES before the paid call; a provider that can enforce one tightens
its params; adults and non-image modalities are never touched. The refusal
carries a non-retryable RetryableError so the orchestrator surfaces it verbatim.
"""

from __future__ import annotations

import pytest
from matrx_connect.context.app_context import (
    AppContext,
    clear_app_context,
    set_app_context,
)

from matrx_ai.providers.base_media import BaseMediaGeneration, MinorImageBlockedError


class _StubConfig:
    model = "some-image-model"


class _FilterableImage(BaseMediaGeneration):
    provider = "stub"
    modality = "image"
    supports_minor_safe_image = True

    def _build_kwargs(self, unified_config, profile):  # pragma: no cover - unused
        return {}

    def _call_provider(self, kwargs):  # pragma: no cover - unused
        return None

    def _extract_assets(self, raw):  # pragma: no cover - unused
        return []

    def _classify_error(self, exc):  # pragma: no cover - unused
        return None

    def _apply_minor_image_overrides(self, kwargs, unified_config, profile):
        kwargs["safety"] = "strict"


class _UnfilterableImage(_FilterableImage):
    supports_minor_safe_image = False


class _VideoGen(_FilterableImage):
    modality = "video"
    supports_minor_safe_image = False


class _CantGuaranteeImage(_FilterableImage):
    def _apply_minor_image_overrides(self, kwargs, unified_config, profile):
        raise RuntimeError("provider rejected the safe setting")


def _set_minor(is_minor: bool):
    return set_app_context(AppContext(emitter=None, user_id="u1", is_minor=is_minor))


def test_minor_on_unfilterable_provider_is_blocked():
    token = _set_minor(True)
    try:
        with pytest.raises(MinorImageBlockedError) as ei:
            _UnfilterableImage()._enforce_minor_image_safety({}, _StubConfig(), None)
        # Rides the streaming error path as a NON-retryable, FE-surfaceable error.
        assert ei.value.error_info.is_retryable is False
        assert ei.value.error_info.error_type == "minor_image_generation_blocked"
        assert ei.value.error_info.user_message
    finally:
        clear_app_context(token)


def test_minor_on_filterable_provider_gets_strict_params():
    token = _set_minor(True)
    try:
        kwargs: dict = {}
        _FilterableImage()._enforce_minor_image_safety(kwargs, _StubConfig(), None)
        assert kwargs["safety"] == "strict"
    finally:
        clear_app_context(token)


def test_override_failure_blocks_rather_than_leaking():
    """If the strict override can't be applied, we BLOCK — never let an
    unfiltered image reach a minor."""
    token = _set_minor(True)
    try:
        with pytest.raises(MinorImageBlockedError):
            _CantGuaranteeImage()._enforce_minor_image_safety({}, _StubConfig(), None)
    finally:
        clear_app_context(token)


def test_adult_is_untouched():
    token = _set_minor(False)
    try:
        kwargs: dict = {}
        # Even an unfilterable provider is fine for an adult.
        _UnfilterableImage()._enforce_minor_image_safety(kwargs, _StubConfig(), None)
        assert kwargs == {}
    finally:
        clear_app_context(token)


def test_no_context_is_treated_as_adult():
    # No AppContext set at all → not a minor request, never blocks.
    kwargs: dict = {}
    _UnfilterableImage()._enforce_minor_image_safety(kwargs, _StubConfig(), None)
    assert kwargs == {}


def test_non_image_modality_never_blocked():
    token = _set_minor(True)
    try:
        kwargs: dict = {}
        # A video generator that can't enforce a minor-safe filter is still
        # never blocked or mutated — enforcement is image-scope only.
        _VideoGen()._enforce_minor_image_safety(kwargs, _StubConfig(), None)
        assert kwargs == {}
    finally:
        clear_app_context(token)


# ─────────── Google text/chat output moderation (safety_settings) ───────────


def _google_thresholds():
    from google.genai import types

    from matrx_ai.providers.google.translator import safety_settings_for_request

    return {str(s.threshold) for s in safety_settings_for_request()}, types


def test_google_text_safety_strict_for_minor():
    token = _set_minor(True)
    try:
        thresholds, types = _google_thresholds()
        # Minor → every adjustable category BLOCK_LOW_AND_ABOVE (nothing OFF).
        assert thresholds == {str(types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE)}
    finally:
        clear_app_context(token)


def test_google_text_safety_low_for_adult():
    token = _set_minor(False)
    try:
        thresholds, types = _google_thresholds()
        assert thresholds == {str(types.HarmBlockThreshold.OFF)}
    finally:
        clear_app_context(token)


def test_google_text_safety_low_without_context():
    # No AppContext set → adult (low) posture, never raises.
    thresholds, types = _google_thresholds()
    assert thresholds == {str(types.HarmBlockThreshold.OFF)}
