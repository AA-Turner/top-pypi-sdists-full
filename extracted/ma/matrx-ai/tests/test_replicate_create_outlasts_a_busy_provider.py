"""A Replicate media prediction is created without a held POST, then polled to a deadline knob.

Live 2026-11-16 (system_error fd9ee1bb, podcast ``video_0``): ``replicate.async_run`` held the create
POST open with ``Prefer: wait`` under the library's own 60.5 s read window, so a video render raised
``httpx.ReadTimeout`` on the create while the prediction kept running (and billing) at Replicate; the
timeout was reported as a text-model timeout ("very long prompts or high token limits") and retried.

The HTTP layer is mocked with an ``httpx.MockTransport`` behind the real ``replicate.Client``: a
request carrying ``Prefer: wait`` times out (what a long render does to a held POST); a plain create
returns at once and the prediction finishes on later GETs.
"""

from __future__ import annotations

import asyncio

import httpx
import pytest
import replicate

from matrx_ai.providers.replicate import client as rc
from matrx_ai.providers.replicate.replicate_image_api import ReplicateImageGeneration
from matrx_ai.providers.replicate.replicate_video_api import ReplicateVideoGeneration

OUT = "https://replicate.delivery/xezq/out.mp4"


def _prediction(status: str, output=None) -> dict:
    return {
        "id": "p1",
        "model": "o/m",
        "version": "v1",
        "status": status,
        "input": {},
        "output": output,
        "logs": "",
        "error": None,
        "metrics": {},
        "created_at": "2026-11-16T00:00:00Z",
        "urls": {"get": "https://api.replicate.com/v1/predictions/p1",
                 "cancel": "https://api.replicate.com/v1/predictions/p1/cancel"},
    }


class _Replicate:
    """The Replicate HTTP API, for one prediction that needs ``polls_to_finish`` GETs."""

    def __init__(self, polls_to_finish: int | None):
        self.polls_to_finish = polls_to_finish
        self.gets = 0
        self.creates: list[httpx.Request] = []
        self.cancelled = False

    def __call__(self, request: httpx.Request) -> httpx.Response:
        path = request.url.path
        if request.method == "POST" and path.endswith("/predictions"):
            self.creates.append(request)
            if "prefer" in request.headers:
                raise httpx.ReadTimeout("held create outlasted its read window", request=request)
            return httpx.Response(201, json=_prediction("starting"))
        if request.method == "POST" and path.endswith("/cancel"):
            self.cancelled = True
            return httpx.Response(200, json=_prediction("canceled"))
        if request.method == "GET" and path.endswith("/predictions/p1"):
            self.gets += 1
            if self.polls_to_finish is not None and self.gets >= self.polls_to_finish:
                return httpx.Response(200, json=_prediction("succeeded", OUT))
            return httpx.Response(200, json=_prediction("processing"))
        return httpx.Response(404, json={"detail": f"unexpected {request.method} {path}"})


@pytest.fixture
def api(monkeypatch):
    def _install(polls_to_finish: int | None) -> _Replicate:
        fake = _Replicate(polls_to_finish)
        client = replicate.Client(
            api_token="test", timeout=rc.REPLICATE_HTTP_TIMEOUT, transport=httpx.MockTransport(fake)
        )
        monkeypatch.setattr(rc, "get_replicate_client", lambda: client)
        monkeypatch.setattr(rc, "REPLICATE_POLL_INTERVAL_S", 0.0, raising=False)

        async def _slot():
            return None

        import matrx_ai.providers.replicate.rate_limit as rl

        monkeypatch.setattr(rl, "acquire_replicate_slot", _slot)
        return fake

    return _install


async def _generate(gen, kwargs):
    created = await gen._call_provider(kwargs)
    return await gen._poll_if_long_running(created)


@pytest.mark.parametrize("cls", [ReplicateImageGeneration, ReplicateVideoGeneration])
def test_a_long_render_is_created_then_polled_never_held_open(api, cls):
    fake = api(polls_to_finish=5)
    out = asyncio.run(_generate(cls(), {"ref": "o/m", "input": {"prompt": "x"}}))
    assert len(fake.creates) == 1
    assert "prefer" not in fake.creates[0].headers
    assert fake.gets == 5
    assert str(out) == OUT


def test_a_render_past_its_deadline_is_cancelled_and_named(api, monkeypatch):
    fake = api(polls_to_finish=None)
    ticks = iter(range(0, 10_000, 100))
    created = asyncio.run(rc.create_prediction(rc.get_replicate_client(), "o/m", {}))
    with pytest.raises(rc.ReplicatePredictionTimeout) as caught:
        asyncio.run(rc.await_prediction(
            created, modality="video", ref="o/m", deadline_s=900, clock=lambda: next(ticks)
        ))
    assert fake.cancelled
    info = caught.value.error_info
    assert info.error_type == "media_generation_timeout"
    assert info.is_retryable is False
    assert "video" in info.user_message and "15 minutes" in info.user_message
    assert "token" not in info.user_message and "prompt" not in info.user_message


def test_the_deadline_is_a_knob_per_modality(monkeypatch):
    import matrx_ai.knobs as knobs

    seen = []
    monkeypatch.setattr(
        knobs, "package_knob_number",
        lambda feature, key, mirror, **k: seen.append((feature, key)) or mirror,
    )
    assert rc.replicate_deadline_seconds("video") == rc.REPLICATE_VIDEO_DEADLINE_MIRROR
    assert rc.replicate_deadline_seconds("image") == rc.REPLICATE_IMAGE_DEADLINE_MIRROR
    assert seen == [
        ("ai.media_providers", "replicate_video_deadline_seconds"),
        ("ai.media_providers", "replicate_image_deadline_seconds"),
    ]


def test_a_media_transport_timeout_never_blames_prompts_or_token_limits(monkeypatch):
    import types

    from matrx_ai.config import UnifiedConfig
    from matrx_ai.providers import base_media

    ctx = types.SimpleNamespace(emitter=None, is_minor=False)
    import matrx_ai.context.app_context as ac

    monkeypatch.setattr(ac, "get_app_context", lambda: ctx)

    async def _noop(*a, **k):
        return None

    monkeypatch.setattr(base_media, "emit_explicit_context_analysis", _noop)
    monkeypatch.setattr(base_media, "stamp_call_meta", lambda **k: None)

    class _Slow(ReplicateVideoGeneration):
        def _build_kwargs(self, *a):
            return {"ref": "o/m", "input": {}}

        async def _call_provider(self, kwargs):
            raise httpx.ReadTimeout("create timed out")

    with pytest.raises(httpx.ReadTimeout) as caught:
        asyncio.run(_Slow()._execute_to_completion(UnifiedConfig(model="m", messages=[]), None))
    msg = caught.value.error_info.user_message
    assert "video" in msg and "replicate" in msg
    assert "token" not in msg and "prompt" not in msg
