"""Exact-parity tests for the MEDIA catalog processors (B2-media).

Each processor in catalog/processors.py is an exact port of a legacy media
translator's irreducible arithmetic. The dimension ports are held against the
LIVE ``providers/_media_dims.py`` helpers (which survive the flip — the google
chat translator still consumes them); the per-provider ports are held against
literal expected grids transcribed from the deleted param blocks
(openai/translator.py image+video, together_image_api._derive_wh,
xai_image_api, model_descriptors, google/translator.py _derive_image_size).
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.processors import (
    ProcessorContext,
    flux_safety_tolerance,
    google_imagen_size,
    media_cast,
    media_count,
    media_dims,
    openai_image_gen_only,
    openai_partial_images,
    xai_image_resolution,
)


def _ctx(config: dict[str, Any] | None = None, extra: dict[str, Any] | None = None):
    return ProcessorContext(
        key="aspect_ratio", config=config or {}, adjustments=[], extra=extra or {}
    )


_DIM_GRID = [
    # (width, height, aspect_ratio)
    (None, None, None),
    (1024, 1024, None),
    (2048, 1152, None),
    (640, 480, "9:16"),  # explicit wh wins over aspect
    (None, None, "1:1"),
    (None, None, "16:9"),
    (None, None, "9:16"),
    (None, None, "21:9"),
    (None, None, "4:3"),
    (None, None, "3:2"),
    (None, None, "7:5"),  # not in the table — arithmetic branch
    (None, None, "5:7"),
    (None, None, "19.5:9"),  # unparseable ints -> (None, None)
    (1024, None, "16:9"),  # width without height -> aspect path
]


def _cfg_ns(width, height, aspect):
    return SimpleNamespace(
        width=width, height=height, aspect_ratio=aspect, duration_seconds=None
    )


@pytest.mark.parametrize("width,height,aspect", _DIM_GRID)
def test_media_dims_size_matches_media_dims_helpers(width, height, aspect):
    from matrx_ai.providers._media_dims import derive_size_string

    canonical = {"width": width, "height": height, "aspect_ratio": aspect}
    params: dict[str, Any] = {}
    media_dims(canonical, params, _ctx({"mode": "size"}))
    assert params.get("size") == derive_size_string(_cfg_ns(width, height, aspect))


@pytest.mark.parametrize("width,height,aspect", _DIM_GRID)
def test_media_dims_aspect_matches_media_dims_helpers(width, height, aspect):
    from matrx_ai.providers._media_dims import derive_aspect_ratio

    canonical = {"width": width, "height": height, "aspect_ratio": aspect}
    params: dict[str, Any] = {}
    media_dims(canonical, params, _ctx({"mode": "aspect_ratio"}))
    assert params.get("aspect_ratio") == derive_aspect_ratio(_cfg_ns(width, height, aspect))


def test_media_dims_size_default_only_on_generate():
    cfg = {"mode": "size", "default": "1024x1024", "default_operations": ["generate"]}
    params: dict[str, Any] = {}
    media_dims({}, params, _ctx(cfg, extra={"operation": "generate"}))
    assert params == {"size": "1024x1024"}
    params = {}
    media_dims({}, params, _ctx(cfg, extra={"operation": "edit"}))
    assert params == {}
    # No operation in context defaults to "generate".
    params = {}
    media_dims({}, params, _ctx(cfg))
    assert params == {"size": "1024x1024"}


# Transcribed from TogetherImageGeneration._derive_wh (anchor-1024 short edge,
# 16-multiples) + the explicit-wins branch of _build_kwargs.
_ANCHOR1024_EXPECTED = {
    None: (1024, 1024),
    "1:1": (1024, 1024),
    "16:9": (1824, 1024),
    "9:16": (1024, 1824),
    "4:3": (1360, 1024),
    "3:4": (1024, 1360),
    "21:9": (2384, 1024),
    "3:2": (1536, 1024),
    "junk": (1024, 1024),
}


@pytest.mark.parametrize("aspect,expected", sorted(_ANCHOR1024_EXPECTED.items(), key=str))
def test_media_dims_wh_anchor1024(aspect, expected):
    params: dict[str, Any] = {}
    media_dims(
        {"aspect_ratio": aspect}, params, _ctx({"mode": "wh", "arithmetic": "anchor1024"})
    )
    assert (params["width"], params["height"]) == expected


def test_media_dims_wh_explicit_wins():
    params: dict[str, Any] = {}
    media_dims(
        {"width": 640, "height": 480, "aspect_ratio": "16:9"},
        params,
        _ctx({"mode": "wh", "arithmetic": "anchor1024"}),
    )
    assert params == {"width": 640, "height": 480}


def test_media_dims_aspect_allowed_fallback():
    cfg = {"mode": "aspect_ratio", "allowed": ["16:9", "9:16"], "default": "16:9", "fallback": "16:9"}
    for aspect, expected in [
        (None, "16:9"),  # unset -> default (google video: derive or "16:9")
        ("16:9", "16:9"),
        ("9:16", "9:16"),
        ("4:3", "16:9"),  # gated -> fallback
    ]:
        params: dict[str, Any] = {}
        media_dims({"aspect_ratio": aspect}, params, _ctx(dict(cfg)))
        assert params.get("aspect_ratio") == expected, aspect


def test_media_dims_aspect_default_without_fallback():
    # replicate gpt-image: `derive or "1:1"` then gate — a SET-but-unsupported
    # ratio is dropped, an UNSET one becomes "1:1".
    cfg = {"mode": "aspect_ratio", "allowed": ["1:1", "3:2", "2:3"], "default": "1:1"}
    for aspect, expected in [
        (None, "1:1"),
        ("3:2", "3:2"),
        ("16:9", None),  # gated miss -> omitted
    ]:
        params: dict[str, Any] = {}
        media_dims({"aspect_ratio": aspect}, params, _ctx(dict(cfg)))
        assert params.get("aspect_ratio") == expected, aspect


def test_media_dims_aspect_allowed_drop_without_fallback():
    # xai video: `if config.aspect_ratio in (...)` — miss means omit, no derive.
    cfg = {"mode": "aspect_ratio", "derive": False, "allowed": ["1:1", "16:9"]}
    params: dict[str, Any] = {}
    media_dims({"aspect_ratio": "7:5", "width": 512, "height": 512}, params, _ctx(dict(cfg)))
    assert params == {}
    params = {}
    media_dims({"width": 1024, "height": 1024}, params, _ctx(dict(cfg)))
    assert params == {}  # derive=False never invents a ratio


# Transcribed from OpenAITranslator.to_openai_video_generate/_derive_video_size.
_SORA_EXPECTED = [
    # (width, height, aspect, resolution) -> size
    (None, None, None, None, "1280x720"),
    (None, None, None, "1080p", "1920x1080"),
    (None, None, "9:16", None, "1024x1536"),  # table hit (code truth)
    (None, None, "9:19.5", "720p", "720x1280"),  # unparseable -> grid portrait
    (None, None, "9:19.5", "1080p", "1080x1920"),
    (None, None, "9:19.5", "1024p", "1024x1792"),
    (1792, 1024, None, None, "1792x1024"),
]


@pytest.mark.parametrize("width,height,aspect,resolution,expected", _SORA_EXPECTED)
def test_media_dims_sora_size(width, height, aspect, resolution, expected):
    params: dict[str, Any] = {}
    media_dims(
        {"width": width, "height": height, "aspect_ratio": aspect, "resolution": resolution},
        params,
        _ctx({"mode": "sora_size"}),
    )
    assert params["size"] == expected


def test_media_count_always_send_and_clamp():
    for raw, expected in [(None, 1), (0, 1), (1, 1), (4, 4), (12, 10)]:
        params: dict[str, Any] = {}
        media_count(
            {"count": raw} if raw is not None else {},
            params,
            _ctx({"target": "n", "max": 10}),
        )
        assert params == {"n": expected}, raw


def test_media_count_omit_at_or_below():
    # replicate flux: `if config.count and config.count > 1: num_outputs=min(count,4)`
    cfg = {"target": "num_outputs", "max": 4, "omit_at_or_below": 1}
    for raw, expected in [(None, None), (1, None), (2, 2), (9, 4)]:
        params: dict[str, Any] = {}
        media_count({"count": raw} if raw is not None else {}, params, _ctx(dict(cfg)))
        assert params.get("num_outputs") == expected, raw


def test_media_cast_str_and_ceiling():
    # sora generate: seconds = str(int(duration_seconds))
    params: dict[str, Any] = {}
    ctx = _ctx({"source": "duration_seconds", "target": "seconds", "to": "str"})
    media_cast({"duration_seconds": 8}, params, ctx)
    assert params == {"seconds": "8"}
    # sora extend: str(min(20, int(x)))
    params = {}
    ctx = _ctx({"source": "duration_seconds", "target": "seconds", "to": "str", "max": 20})
    media_cast({"duration_seconds": 45}, params, ctx)
    assert params == {"seconds": "20"}
    # together video guidance: int()
    params = {}
    ctx = _ctx({"source": "guidance_scale", "target": "guidance_scale"})
    media_cast({"guidance_scale": 7.5}, params, ctx)
    assert params == {"guidance_scale": 7}
    # unset -> omitted
    params = {}
    media_cast({}, params, ctx)
    assert params == {}


def test_openai_image_gen_only():
    # generate: moderation explicit wins, else default "low"; edit: never sent.
    params: dict[str, Any] = {}
    openai_image_gen_only({}, params, _ctx({"default": "low"}, {"operation": "generate"}))
    assert params == {"moderation": "low"}
    params = {}
    openai_image_gen_only(
        {"moderation": "auto"}, params, _ctx({"default": "low"}, {"operation": "generate"})
    )
    assert params == {"moderation": "auto"}
    params = {}
    openai_image_gen_only(
        {"moderation": "auto", "background": "opaque"},
        params,
        _ctx({"default": "low"}, {"operation": "edit"}),
    )
    assert params == {}
    # background passthrough on generate; transparent stripped only when the
    # per-offering flag says so (gpt-image-2).
    params = {}
    openai_image_gen_only(
        {"background": "transparent"}, params, _ctx({"default": "low"}, {"operation": "generate"})
    )
    assert params == {"moderation": "low", "background": "transparent"}
    params = {}
    openai_image_gen_only(
        {"background": "transparent"},
        params,
        _ctx({"default": "low", "background_transparent_drop": True}, {"operation": "generate"}),
    )
    assert params == {"moderation": "low"}
    params = {}
    openai_image_gen_only(
        {"background": "opaque"},
        params,
        _ctx({"default": "low", "background_transparent_drop": True}, {"operation": "generate"}),
    )
    assert params == {"moderation": "low", "background": "opaque"}


def test_openai_partial_images():
    params: dict[str, Any] = {}
    openai_partial_images({"partial_images": 2}, params, _ctx())
    assert params == {"partial_images": 2, "stream": True}
    for canonical in ({}, {"partial_images": 0}):
        params = {}
        openai_partial_images(canonical, params, _ctx())
        assert params == {}


def test_flux_safety_tolerance():
    params: dict[str, Any] = {}
    flux_safety_tolerance({}, params, _ctx(extra={"has_image_input": True}))
    assert params == {"safety_tolerance": 2}
    params = {}
    flux_safety_tolerance({}, params, _ctx(extra={}))
    assert params == {"safety_tolerance": 5}


def test_xai_image_resolution():
    for canonical, expected in [
        ({"resolution": "1k"}, "1k"),
        ({"resolution": "2k"}, "2k"),
        ({"resolution": "4k", "width": 2048}, "2k"),  # not 1k/2k -> width tiers
        ({"width": 2048}, "2k"),
        ({"width": 1024}, "1k"),
        ({}, None),
    ]:
        params: dict[str, Any] = {}
        xai_image_resolution(canonical, params, _ctx())
        assert params.get("resolution") == expected, canonical


def test_google_imagen_size():
    for canonical, expected in [
        ({"resolution": "1k"}, "1K"),
        ({"resolution": "2k"}, "2K"),
        ({"resolution": "720p"}, "1K"),
        ({"resolution": "1080p"}, "1K"),
        ({"resolution": "4k"}, "2K"),
        ({"resolution": "480p", "width": 2048}, "2K"),  # unmapped tier -> width
        ({"width": 2048}, "2K"),
        ({"width": 1024}, "1K"),
        ({}, None),
    ]:
        params: dict[str, Any] = {}
        google_imagen_size(canonical, params, _ctx())
        assert params.get("image_size") == expected, canonical
