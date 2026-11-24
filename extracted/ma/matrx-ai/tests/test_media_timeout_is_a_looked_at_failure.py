"""A media call that times out before the provider answers has nothing to bill but DID get looked at.

Live 2026-11-16: replicate/veo ReadTimeout filed ``provider_billing_capture_missing`` once a minute,
because the media base never marked the failure as billing-checked.
"""

from __future__ import annotations

import asyncio
import types

import httpx
import pytest

from matrx_ai.config import UnifiedConfig
from matrx_ai.providers import base_media
from matrx_ai.providers.base_media import BaseMediaGeneration
from matrx_ai.providers.errors import (
    report_unbilled_provider_failure,
    was_billing_checked,
)


class _TimingOut(BaseMediaGeneration):
    provider = "replicate"
    modality = "video"

    def _build_kwargs(self, *a):
        return {}

    def _call_provider(self, *a):
        raise httpx.ReadTimeout("")

    def _extract_assets(self, *a):
        return []

    def _classify_error(self, exc):
        return None

    def _telemetry_url(self, *a):
        return ""


def test_media_timeout_before_the_provider_answers_is_marked_checked(monkeypatch):
    ctx = types.SimpleNamespace(emitter=None, is_minor=False)
    import matrx_ai.context.app_context as ac

    monkeypatch.setattr(ac, "get_app_context", lambda: ctx)

    async def _noop(*a, **k):
        return None

    monkeypatch.setattr(base_media, "emit_explicit_context_analysis", _noop)
    monkeypatch.setattr(base_media, "stamp_call_meta", lambda **k: None)

    gen = _TimingOut()
    with pytest.raises(httpx.ReadTimeout) as caught:
        asyncio.run(gen._execute_to_completion(UnifiedConfig(model="m", messages=[]), None))
    exc = caught.value
    assert was_billing_checked(exc)
    assert report_unbilled_provider_failure(exc, provider="replicate", model="m") is False
