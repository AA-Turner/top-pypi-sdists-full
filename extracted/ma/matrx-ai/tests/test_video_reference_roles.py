"""Forcing-function tests for video-generation reference roles.

Each video translator must put every roled input on its provider's NATIVE field
(first frame, last frame, asset/style references, the clip to extend or
restyle, the lip-sync audio), and every role, count, name or camera move the
model or route cannot take must be REFUSED by name before the paid call.

Contract: ``matrx_ai/media/video_reference_roles.py``; row in
``common-docs/systems/agents/typed-messages/FEATURE.md`` (Video generation).
"""

from __future__ import annotations

import base64
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config.media_config import AudioContent, ImageContent, VideoContent
from matrx_ai.config.unified_content import TextContent
from matrx_ai.media.image_reference_roles import ImageRoleCompatibilityError
from matrx_ai.media.video_reference_roles import (
    camera_to_kling,
    collect_video_references,
    enforce_video_roles,
    validate_camera_control,
)

PNG_B64 = base64.b64encode(b"\x89PNG\r\n\x1a\nfake").decode()
MP4_B64 = base64.b64encode(b"\x00\x00\x00\x18ftypmp42fake").decode()


def _img(
    role: str | None = None, key: str = "a", name: str | None = None, legacy: str | None = None
) -> ImageContent:
    return ImageContent(
        base64_data=PNG_B64,
        mime_type="image/png",
        url=f"https://cdn.example.com/{key}.png",
        role=role,
        name=name,
        metadata={"role": legacy} if legacy else {},
    )


def _vid(role: str | None = None, key: str = "v", name: str | None = None) -> VideoContent:
    return VideoContent(
        base64_data=MP4_B64,
        mime_type="video/mp4",
        url=f"https://cdn.example.com/{key}.mp4",
        role=role,
        name=name,
    )


def _aud(role: str | None = None, key: str = "s") -> AudioContent:
    return AudioContent(url=f"https://cdn.example.com/{key}.mp3", mime_type="audio/mpeg", role=role)


def _config(model: str, *parts: Any, prompt: str = "A bottle rises from the sand", **extra: Any) -> Any:
    message = SimpleNamespace(role="user", content=[TextContent(text=prompt), *parts])
    base = dict(
        model=model,
        messages=[message],
        image_input=None,
        image_inputs=None,
        reference_images=None,
        last_frame_image=None,
        frame_images=None,
        video_input=None,
        video_action=None,
        camera_control=None,
        system_instruction=None,
    )
    base.update(extra)
    return SimpleNamespace(**base)


def _profile(model: str, image: dict[str, int], video: dict[str, int] | None = None) -> Any:
    return SimpleNamespace(
        model_name=model,
        controls=None,
        capabilities=SimpleNamespace(
            image_reference_limits=image, video_reference_limits=video or {}
        ),
    )


VEO_IMAGE = {"first_frame": 1, "last_frame": 1, "asset": 3, "total": 3}
VEO_VIDEO = {"extend": 1, "named": 3}
VEO_TRANSPORT = {"first_frame", "last_frame", "asset", "style", "extend", "named"}


def _refs(*parts: Any) -> dict[str, list[Any]]:
    return collect_video_references([SimpleNamespace(role="user", content=list(parts))])


# --------------------------------------------------------------------------
# Vocabulary + the gate
# --------------------------------------------------------------------------


def test_unknown_video_and_audio_roles_raise_at_construction():
    with pytest.raises(ValueError, match="video reference role"):
        _vid("first_frame")
    with pytest.raises(ValueError, match="audio reference role"):
        _aud("extend")
    with pytest.raises(ValueError, match="usable tag"):
        _img("asset", name="two words")
    assert _img("asset", name="@hero").name == "hero"


def test_legacy_metadata_tags_fold_into_typed_roles():
    refs = _refs(_img(None, "s", legacy="start_image"), _img(None, "e", legacy="end_image"))
    assert [c.url for c in refs["first_frame"]] == ["https://cdn.example.com/s.png"]
    assert [c.url for c in refs["last_frame"]] == ["https://cdn.example.com/e.png"]


def test_gate_refuses_style_on_veo_naming_role_and_model():
    with pytest.raises(ImageRoleCompatibilityError) as err:
        enforce_video_roles(
            _refs(_img("style")), image_limits=VEO_IMAGE, video_limits=VEO_VIDEO,
            transport=VEO_TRANSPORT, model="veo-3.1-generate-preview",
        )
    assert err.value.role == "style"
    assert "veo-3.1-generate-preview" in str(err.value) and "Style" in str(err.value)


def test_gate_refuses_an_image_generation_role_on_a_video_model():
    with pytest.raises(ImageRoleCompatibilityError, match="image-generation role"):
        enforce_video_roles(
            _refs(_img("subject")), image_limits=VEO_IMAGE, video_limits=VEO_VIDEO,
            transport=VEO_TRANSPORT, model="veo",
        )


def test_gate_refuses_a_role_the_route_cannot_carry():
    with pytest.raises(ImageRoleCompatibilityError, match="route"):
        enforce_video_roles(
            _refs(_vid("restyle")), image_limits={}, video_limits={"restyle": 1},
            transport={"first_frame"}, model="m",
        )


def test_gate_refuses_over_count_and_over_total():
    with pytest.raises(ImageRoleCompatibilityError, match="at most 1 First frame"):
        enforce_video_roles(
            _refs(_img("first_frame", "a"), _img("first_frame", "b")),
            image_limits=VEO_IMAGE, video_limits={}, transport=VEO_TRANSPORT, model="m",
        )
    with pytest.raises(ImageRoleCompatibilityError, match="in total"):
        enforce_video_roles(
            _refs(_img("first_frame"), *[_img("asset", str(i)) for i in range(3)]),
            image_limits=VEO_IMAGE, video_limits={}, transport=VEO_TRANSPORT, model="m",
        )


def test_gate_refuses_a_last_frame_without_a_first_frame():
    with pytest.raises(ImageRoleCompatibilityError, match="First frame to travel from"):
        enforce_video_roles(
            _refs(_img("last_frame")), image_limits=VEO_IMAGE, video_limits={},
            transport=VEO_TRANSPORT, model="m",
        )


def test_gate_refuses_names_where_no_named_elements_and_duplicate_names():
    with pytest.raises(ImageRoleCompatibilityError, match="named references"):
        enforce_video_roles(
            _refs(_img("asset", name="hero")), image_limits={"asset": 3},
            video_limits={}, transport={"asset"}, model="kling",
        )
    with pytest.raises(ImageRoleCompatibilityError, match="(?i)Two references are named @hero"):
        enforce_video_roles(
            _refs(_img("asset", "a", name="hero"), _img("asset", "b", name="Hero")),
            image_limits=VEO_IMAGE, video_limits=VEO_VIDEO, transport=VEO_TRANSPORT, model="m",
        )


def test_gate_refuses_camera_control_on_a_route_without_camera_moves():
    with pytest.raises(ImageRoleCompatibilityError, match="camera control"):
        enforce_video_roles(
            {}, image_limits=VEO_IMAGE, video_limits=VEO_VIDEO, transport=VEO_TRANSPORT,
            model="veo", camera_control={"moves": ["pan_left"]},
        )


def test_gate_passes_a_fitting_request():
    enforce_video_roles(
        _refs(_img("first_frame"), _img("last_frame", "l"), _img("asset", "x", name="hero")),
        image_limits=VEO_IMAGE, video_limits=VEO_VIDEO, transport=VEO_TRANSPORT, model="veo",
    )


def test_camera_control_validates_and_maps_per_vendor():
    cam = validate_camera_control({"moves": ["pan_left"], "strength": 0.3})
    assert camera_to_kling(cam) == {
        "type": "simple",
        "config": {"horizontal": 0, "vertical": 0, "pan": -3, "tilt": 0, "roll": 0, "zoom": 0},
    }
    with pytest.raises(ValueError, match="Unknown camera move"):
        validate_camera_control({"moves": ["spin_wildly"]})
    with pytest.raises(ValueError, match="exactly one axis"):
        camera_to_kling({"moves": ["pan_left", "zoom_in"]})


def test_roles_and_names_survive_storage_round_trip_and_the_parts_validate_them():
    from matrx_ai.config.media_config import reconstruct_media_content
    from matrx_ai.db.message_parts import AudioMediaPart, ImageMediaPart, VideoMediaPart

    for block, part in (
        (_img("asset", name="hero"), ImageMediaPart),
        (_vid("extend", name="take1"), VideoMediaPart),
        (_aud("lip_sync"), AudioMediaPart),
    ):
        stored = block.to_storage_dict()
        stored.pop("base64_data", None)
        back = reconstruct_media_content(stored)
        assert back.role == block.role and getattr(back, "name", None) == getattr(block, "name", None)
        assert part.model_validate(stored).role == block.role
    with pytest.raises(ValueError):
        VideoMediaPart.model_validate({"type": "media", "kind": "video", "url": "u", "role": "zoom"})


def test_capability_vocabulary_accepts_video_limits_and_rejects_bad_ones():
    from matrx_ai.providers.capability_vocabulary import normalize_capabilities

    ok = normalize_capabilities({"video_reference_roles": {"extend": 1, "named": 3}})
    assert not ok.rejections
    bad = normalize_capabilities({"video_reference_roles": {"zoom": 1, "extend": -1}})
    assert len(bad.rejections) == 2


def test_resolver_carries_video_limits_from_the_offering_override():
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    model = SimpleNamespace(
        name="veo", capabilities={"input": ["text", "image"], "output": ["video"]}
    )
    caps = resolve_model_capabilities(
        model,
        capabilities_override={
            "image_reference_roles": VEO_IMAGE,
            "video_reference_roles": VEO_VIDEO,
        },
    )
    assert caps.image_reference_limits == VEO_IMAGE
    assert caps.video_reference_limits == VEO_VIDEO


# --------------------------------------------------------------------------
# Veo (Gemini API): image / lastFrame / referenceImages / source.video
# --------------------------------------------------------------------------


def _veo_kwargs(monkeypatch, *parts: Any) -> dict[str, Any]:
    from matrx_ai.providers.google.google_video_api import GoogleVideoGeneration

    gen = GoogleVideoGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    return gen._build_kwargs(_config("veo-3.1-generate-preview", *parts), _profile("veo", VEO_IMAGE))


def test_veo_maps_first_last_asset_and_extend_to_native_fields(monkeypatch):
    kwargs = _veo_kwargs(
        monkeypatch,
        _img("first_frame", "first"),
        _img("last_frame", "last"),
        _img("asset", "bottle", name="bottle"),
        _vid("extend", "take1"),
    )
    config = kwargs["config"]
    # The SDK refuses a top-level image beside `source`: the frame rides in it.
    assert "image" not in kwargs and kwargs["source"].image is not None
    assert config.last_frame is not None
    assert len(config.reference_images) == 1
    assert str(config.reference_images[0].reference_type).endswith("ASSET")
    assert kwargs["source"].video is not None
    assert "@bottle is reference image 1." in kwargs["source"].prompt
    assert config.person_generation == "ALLOW_ADULT"


def test_veo_style_reference_rides_reference_type_style(monkeypatch):
    kwargs = _veo_kwargs(monkeypatch, _img("style", "look"))
    assert str(kwargs["config"].reference_images[0].reference_type).endswith("STYLE")


def test_veo_an_unreadable_first_frame_raises_never_drops(monkeypatch):
    broken = ImageContent(url="https://cdn.example.com/x.png", role="first_frame")
    with pytest.raises(ValueError, match="First frame image could not be read"):
        _veo_kwargs(monkeypatch, broken)


# --------------------------------------------------------------------------
# Replicate descriptors: Veo, Kling, Runway, Luma, MiniMax, Seedance
# --------------------------------------------------------------------------


def _replicate(slug: str, *parts: Any, monkeypatch, **extra: Any) -> dict[str, Any]:
    from matrx_ai.providers.base_media import BaseMediaGeneration
    from matrx_ai.providers.replicate.model_descriptors import get_descriptor

    monkeypatch.setattr(BaseMediaGeneration, "_outbound_params", staticmethod(lambda *a, **k: {}))
    return get_descriptor(slug).build_input(_config(slug, *parts, **extra), None)


def test_replicate_veo_keys_are_the_real_schema(monkeypatch):
    out = _replicate(
        "google/veo-3.1",
        _img("first_frame", "f"), _img("last_frame", "l"), _img("asset", "a"),
        monkeypatch=monkeypatch,
    )
    assert out["image"] == "https://cdn.example.com/f.png"
    assert out["last_frame"] == "https://cdn.example.com/l.png"
    assert out["reference_images"] == ["https://cdn.example.com/a.png"]
    assert "last_frame_image" not in out


def test_kling_first_and_last_frame_are_start_and_end_image(monkeypatch):
    out = _replicate(
        "kwaivgi/kling-v3-video", _img("first_frame", "f"), _img("last_frame", "l"),
        monkeypatch=monkeypatch,
    )
    assert out["start_image"] == "https://cdn.example.com/f.png"
    assert out["end_image"] == "https://cdn.example.com/l.png"


def test_kling_lip_sync_puts_clip_and_speech_on_their_endpoint_fields(monkeypatch):
    out = _replicate(
        "kwaivgi/kling-lip-sync", _vid("restyle", "face"), _aud("lip_sync", "line"),
        monkeypatch=monkeypatch, prompt="",
    )
    assert out["video_url"] == "https://cdn.example.com/face.mp4"
    assert out["audio_file"] == "https://cdn.example.com/line.mp3"


def test_runway_first_frame_is_image_and_aleph_restyles_video(monkeypatch):
    out = _replicate("runwayml/gen-4.5", _img("first_frame", "f"), monkeypatch=monkeypatch)
    assert out == {"prompt": "A bottle rises from the sand", "image": "https://cdn.example.com/f.png"}
    aleph = _replicate(
        "runwayml/gen4-aleph", _vid("restyle", "clip"), _img("style", "look"),
        monkeypatch=monkeypatch,
    )
    assert aleph["video"] == "https://cdn.example.com/clip.mp4"
    assert aleph["reference_image"] == "https://cdn.example.com/look.png"


def test_luma_keyframes_and_camera_concepts(monkeypatch):
    out = _replicate(
        "luma/ray-2-720p", _img("first_frame", "f"), _img("last_frame", "l"),
        monkeypatch=monkeypatch, camera_control={"moves": ["orbit_left", "zoom_in"]},
    )
    assert out["start_image"] == "https://cdn.example.com/f.png"
    assert out["end_image"] == "https://cdn.example.com/l.png"
    assert out["concepts"] == ["orbit_left", "zoom_in"]


def test_minimax_first_frame_and_untagged_image_falls_back_to_it(monkeypatch):
    out = _replicate("minimax/hailuo-2.3", _img(None, "plain"), monkeypatch=monkeypatch)
    assert out["first_frame_image"] == "https://cdn.example.com/plain.png"


def test_seedance_named_refs_videos_and_lip_sync_audio(monkeypatch):
    out = _replicate(
        "bytedance/seedance-2.0",
        _img("asset", "hero", name="hero"),
        _img("style", "look", name="look"),
        _vid("restyle", "motion"),
        _aud("lip_sync", "line"),
        monkeypatch=monkeypatch,
    )
    assert out["reference_images"] == [
        "https://cdn.example.com/hero.png",
        "https://cdn.example.com/look.png",
    ]
    assert out["reference_videos"] == ["https://cdn.example.com/motion.mp4"]
    assert out["reference_audios"] == ["https://cdn.example.com/line.mp3"]
    assert "@hero is reference image 1." in out["prompt"]
    assert "@look is style reference image 2." in out["prompt"]


def test_replicate_video_transport_is_the_descriptor_role_map():
    from matrx_ai.providers.replicate.replicate_video_api import ReplicateVideoGeneration

    gen = ReplicateVideoGeneration()
    assert gen.video_role_transport(SimpleNamespace(model="minimax/hailuo-2.3")) == {"first_frame"}
    assert "camera_control" in gen.video_role_transport(SimpleNamespace(model="luma/ray-2-720p"))


# --------------------------------------------------------------------------
# Sora, xAI, Together
# --------------------------------------------------------------------------


def test_xai_first_frame_assets_and_restyle(monkeypatch):
    from matrx_ai.providers.xai.xai_video_api import XAIVideoGeneration

    gen = XAIVideoGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    kwargs = gen._build_kwargs(
        _config("grok-imagine-video", _img("first_frame", "f"), _img("asset", "a"), _vid("restyle", "c")),
        _profile("grok", {}),
    )
    assert kwargs["image_url"] == "https://cdn.example.com/f.png"
    assert kwargs["reference_image_urls"] == ["https://cdn.example.com/a.png"]
    assert kwargs["video_url"] == "https://cdn.example.com/c.mp4"
    assert gen._is_extend is False


def test_together_first_last_and_assets(monkeypatch):
    from matrx_ai.providers.together.together_video_api import TogetherVideoGeneration

    gen = TogetherVideoGeneration()
    monkeypatch.setattr(
        gen, "_outbound_params", lambda controls, cfg, extra_canonical=None, **k: dict(extra_canonical)
    )
    kwargs = gen._build_kwargs(
        _config("kwaivgI/kling-2.1-pro", _img("first_frame", "f"), _img("last_frame", "l")),
        _profile("kling", {}),
    )
    assert kwargs["media"] == {"image": "https://cdn.example.com/f.png"}
    assert kwargs["frame_images"] == [{"image": "https://cdn.example.com/l.png", "frame_number": -1}]


def test_sora_transport_is_first_frame_only():
    from matrx_ai.providers.openai.openai_video_api import OpenAIVideoGeneration

    assert OpenAIVideoGeneration().video_role_transport(SimpleNamespace()) == {"first_frame"}


# --------------------------------------------------------------------------
# The refusal happens BEFORE the paid call; image models refuse video roles
# --------------------------------------------------------------------------


def _stub(modality: str, calls: list[Any]):
    from matrx_ai.providers.base_media import BaseMediaGeneration

    class _Gen(BaseMediaGeneration):
        provider = "stub"

        def _build_kwargs(self, unified_config, profile):
            calls.append("build")
            return {}

        def _call_provider(self, kwargs):
            calls.append("paid")

        def _extract_assets(self, raw):
            return []

        def _classify_error(self, exc):
            return None

    _Gen.modality = modality
    return _Gen()


@pytest.mark.asyncio
async def test_video_execute_refuses_before_any_provider_call():
    calls: list[Any] = []
    with pytest.raises(ImageRoleCompatibilityError, match="First frame"):
        await _stub("video", calls).execute(
            _config("stub-video", _img("first_frame")), _profile("stub-video", {})
        )
    assert calls == []


@pytest.mark.asyncio
async def test_image_model_refuses_a_video_role_before_any_provider_call():
    calls: list[Any] = []
    with pytest.raises(ImageRoleCompatibilityError, match="generates images"):
        await _stub("image", calls).execute(
            _config("stub-image", _vid("extend")), _profile("stub-image", {})
        )
    with pytest.raises(ImageRoleCompatibilityError, match="First frame"):
        await _stub("image", calls).execute(
            _config("stub-image", _img("first_frame")), _profile("stub-image", {"subject": 3})
        )
    assert calls == []
