"""Forcing-function tests for image-generation reference roles.

Each translator must put every roled reference image on its provider's NATIVE
field (or, for a flat image list, on the list with an "Image N is the ..."
legend), and every role/count the model or route cannot take must be REFUSED
by name before the paid call — never silently dropped.

Contract: ``matrx_ai/media/image_reference_roles.py``; row in
``common-docs/systems/agents/typed-messages/FEATURE.md`` (Image generation).
"""

from __future__ import annotations

import base64
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.config.media_config import ImageContent
from matrx_ai.config.unified_content import TextContent
from matrx_ai.media.image_reference_roles import (
    ImageRoleCompatibilityError,
    collect_role_images,
    enforce_image_roles,
)

PNG_B64 = base64.b64encode(b"\x89PNG\r\n\x1a\nfake").decode()


def _img(role: str | None = None, name: str = "a") -> ImageContent:
    return ImageContent(
        base64_data=PNG_B64,
        mime_type="image/png",
        url=f"https://cdn.example.com/{name}.png",
        role=role,
    )


def _config(model: str, *images: ImageContent, prompt: str = "A bottle on a beach") -> Any:
    message = SimpleNamespace(role="user", content=[TextContent(text=prompt), *images])
    return SimpleNamespace(
        model=model,
        messages=[message],
        image_input=None,
        image_inputs=None,
        mask=None,
        reference_images=None,
        last_frame_image=None,
        system_instruction=None,
        partial_images=None,
        image_loras=None,
    )


def _profile(model: str, limits: dict[str, int]) -> Any:
    return SimpleNamespace(
        model_name=model,
        controls=None,
        capabilities=SimpleNamespace(image_reference_limits=limits),
    )


GEMINI_LIMITS = {"subject": 10, "character": 4, "style": 14, "edit_target": 1, "total": 14}


# --------------------------------------------------------------------------
# The gate
# --------------------------------------------------------------------------


def test_gate_refuses_a_role_the_model_cannot_take_naming_role_and_model():
    roles = collect_role_images([SimpleNamespace(role="user", content=[_img("mask")])])
    with pytest.raises(ImageRoleCompatibilityError) as err:
        enforce_image_roles(
            roles, limits=GEMINI_LIMITS, transport={"mask"}, model="gemini-3.1-flash-image"
        )
    assert err.value.role == "mask"
    assert "gemini-3.1-flash-image" in str(err.value)
    assert "Mask" in str(err.value)


def test_gate_refuses_a_role_the_route_cannot_carry():
    roles = collect_role_images([SimpleNamespace(role="user", content=[_img("style")])])
    with pytest.raises(ImageRoleCompatibilityError, match="route"):
        enforce_image_roles(roles, limits={"style": 3}, transport=set(), model="m")


def test_gate_refuses_over_the_per_role_count():
    roles = collect_role_images(
        [SimpleNamespace(role="user", content=[_img("character", str(i)) for i in range(5)])]
    )
    with pytest.raises(ImageRoleCompatibilityError, match="at most 4 Character"):
        enforce_image_roles(
            roles, limits=GEMINI_LIMITS, transport={"character"}, model="gemini-3.1-flash-image"
        )


def test_gate_refuses_over_the_total():
    images = [_img("subject", f"s{i}") for i in range(3)] + [_img("style", "t")]
    roles = collect_role_images([SimpleNamespace(role="user", content=images)])
    with pytest.raises(ImageRoleCompatibilityError, match="at most 3 reference images in total"):
        enforce_image_roles(
            roles,
            limits={"subject": 3, "style": 3, "total": 3},
            transport={"subject", "style"},
            model="gemini-2.5-flash-image",
        )


def test_gate_refuses_a_mask_with_nothing_to_mask():
    roles = collect_role_images([SimpleNamespace(role="user", content=[_img("mask")])])
    with pytest.raises(ImageRoleCompatibilityError, match="Edit this"):
        enforce_image_roles(roles, limits={"mask": 1}, transport={"mask"}, model="gpt-image-2")


def test_gate_passes_a_fitting_request():
    roles = collect_role_images(
        [SimpleNamespace(role="user", content=[_img("subject"), _img("style", "b")])]
    )
    enforce_image_roles(
        roles, limits=GEMINI_LIMITS, transport={"subject", "style"}, model="gemini-3.1-flash-image"
    )


def test_unknown_role_is_refused_at_construction_never_downgraded():
    with pytest.raises(ValueError, match="Unknown image reference role"):
        ImageContent(url="https://x/y.png", role="background")


def test_role_survives_storage_round_trip_and_the_part_validates_it():
    from matrx_ai.config.media_config import reconstruct_media_content
    from matrx_ai.db.message_parts import ImageMediaPart

    stored = _img("style").to_storage_dict()
    assert stored["role"] == "style"
    assert reconstruct_media_content(stored).role == "style"
    assert ImageMediaPart(url="https://x/y.png", role="edit_target").role == "edit_target"
    with pytest.raises(ValueError):
        ImageMediaPart(url="https://x/y.png", role="background")


# --------------------------------------------------------------------------
# The catalog: limits are data on capabilities, validated on write
# --------------------------------------------------------------------------


def test_capability_vocabulary_accepts_limits_and_rejects_bad_ones():
    from matrx_ai.providers.capability_vocabulary import normalize_capabilities

    good = normalize_capabilities({"image_reference_roles": {"subject": 6, "total": 14}})
    assert good.ok
    bad = normalize_capabilities({"image_reference_roles": {"background": 1, "style": -1}})
    assert not bad.ok
    assert any("background" in r for r in bad.rejections)
    assert any("style" in r for r in bad.rejections)


def test_resolver_carries_limits_with_offering_override_winning():
    from matrx_ai.providers.resolved_capabilities import resolve_model_capabilities

    model = SimpleNamespace(
        name="m",
        capabilities={
            "input": ["text", "image"],
            "output": ["image"],
            "interaction": "single",
            "image_reference_roles": {"subject": 6},
        },
    )
    assert resolve_model_capabilities(model).image_reference_limits == {"subject": 6}
    overridden = resolve_model_capabilities(
        model, capabilities_override={"image_reference_roles": {"style": 2}}
    )
    assert overridden.image_reference_limits == {"style": 2}


# --------------------------------------------------------------------------
# Google — Gemini native (interleaved labels) and Imagen (text-only: refuse)
# --------------------------------------------------------------------------


def _google_kwargs(model: str, *images: ImageContent, monkeypatch) -> dict[str, Any]:
    from matrx_ai.providers.google.google_image_api import GoogleImageGeneration

    gen = GoogleImageGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    return gen._build_kwargs(_config(model, *images), _profile(model, GEMINI_LIMITS))


def test_gemini_native_labels_each_reference_immediately_before_its_image(monkeypatch):
    from google.genai import types

    kwargs = _google_kwargs(
        "gemini-3.1-flash-image",
        _img("style", "style"),
        _img("subject", "product"),
        _img(None, "plain"),
        monkeypatch=monkeypatch,
    )
    contents = kwargs["contents"]
    assert contents[0] == "A bottle on a beach"
    # Vocabulary order: subject before style; each label precedes its image.
    assert contents[1].startswith("Image 1 is the subject reference")
    assert isinstance(contents[2], types.Part)
    assert contents[3].startswith("Image 2 is the style reference")
    assert isinstance(contents[4], types.Part)
    # The plain image is still sent — never dropped.
    assert isinstance(contents[5], types.Part)
    assert len(contents) == 6


def test_gemini_native_transport_excludes_mask_and_composition(monkeypatch):
    from matrx_ai.providers.google.google_image_api import GoogleImageGeneration

    gen = GoogleImageGeneration()
    config = _config("gemini-3-pro-image", _img("composition_control"))
    with pytest.raises(ImageRoleCompatibilityError) as err:
        gen.enforce_image_reference_roles(
            config, _profile("gemini-3-pro-image", {**GEMINI_LIMITS, "composition_control": 1})
        )
    assert err.value.role == "composition_control"


def test_imagen_refuses_every_role_by_name():
    from matrx_ai.providers.google.google_image_api import GoogleImageGeneration

    gen = GoogleImageGeneration()
    config = _config("imagen-4.0-generate-001", _img("subject"))
    with pytest.raises(ImageRoleCompatibilityError, match="imagen-4.0-generate-001"):
        gen.enforce_image_reference_roles(config, _profile("imagen-4.0-generate-001", {}))


# --------------------------------------------------------------------------
# OpenAI images.edit — image list (edit target first), mask, input_fidelity
# --------------------------------------------------------------------------


def _openai_kwargs(model: str, *images: ImageContent, monkeypatch) -> dict[str, Any]:
    from matrx_ai.providers.openai.openai_image_api import OpenAIImageGeneration

    gen = OpenAIImageGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    return gen._build_kwargs(_config(model, *images), _profile(model, {}))


def test_openai_edit_target_is_image_one_and_mask_rides_mask(monkeypatch):
    kwargs = _openai_kwargs(
        "gpt-image-2",
        _img("style", "style"),
        _img("mask", "mask"),
        _img("edit_target", "base"),
        monkeypatch=monkeypatch,
    )
    assert kwargs["_is_edit"] is True
    assert isinstance(kwargs["image"], list) and len(kwargs["image"]) == 2
    assert "mask" in kwargs
    assert "Image 1 is the image to edit" in kwargs["prompt"]
    assert "Image 2 is the style reference" in kwargs["prompt"]
    # gpt-image-2 is always high fidelity: the parameter must be omitted.
    assert "input_fidelity" not in kwargs


def test_openai_identity_reference_asks_for_high_fidelity_on_gpt_image_1x(monkeypatch):
    kwargs = _openai_kwargs("gpt-image-1.5", _img("subject"), monkeypatch=monkeypatch)
    assert kwargs["input_fidelity"] == "high"
    mini = _openai_kwargs("gpt-image-1-mini", _img("subject"), monkeypatch=monkeypatch)
    assert "input_fidelity" not in mini


def test_openai_refuses_composition_control():
    from matrx_ai.providers.openai.openai_image_api import OpenAIImageGeneration

    config = _config("gpt-image-2", _img("composition_control"))
    with pytest.raises(ImageRoleCompatibilityError):
        OpenAIImageGeneration().enforce_image_reference_roles(
            config, _profile("gpt-image-2", {"composition_control": 1})
        )


# --------------------------------------------------------------------------
# Replicate — FLUX 2 one list, Ideogram native image/mask/style list
# --------------------------------------------------------------------------


def _replicate_input(slug: str, *images: ImageContent, monkeypatch) -> dict[str, Any]:
    from matrx_ai.providers.base_media import BaseMediaGeneration
    from matrx_ai.providers.replicate.model_descriptors import get_descriptor

    monkeypatch.setattr(BaseMediaGeneration, "_outbound_params", staticmethod(lambda *a, **k: {}))
    return get_descriptor(slug).build_input(_config(slug, *images), None)


def test_flux2_puts_roled_references_on_input_images_with_a_legend(monkeypatch):
    out = _replicate_input(
        "black-forest-labs/flux-2-pro",
        _img("style", "style"),
        _img("subject", "product"),
        monkeypatch=monkeypatch,
    )
    assert out["input_images"] == [
        "https://cdn.example.com/product.png",
        "https://cdn.example.com/style.png",
    ]
    assert "image_input" not in out and "reference_images" not in out
    assert "Image 1 is the subject reference" in out["prompt"]


def test_ideogram_maps_to_native_image_mask_and_style_list(monkeypatch):
    out = _replicate_input(
        "ideogram-ai/ideogram-v3-turbo",
        _img("edit_target", "base"),
        _img("mask", "mask"),
        _img("style", "style"),
        monkeypatch=monkeypatch,
    )
    assert out["image"] == "https://cdn.example.com/base.png"
    assert out["mask"] == "https://cdn.example.com/mask.png"
    assert out["style_reference_images"] == ["https://cdn.example.com/style.png"]


def test_replicate_transport_is_the_descriptor_role_map():
    from matrx_ai.providers.replicate.replicate_image_api import ReplicateImageGeneration

    gen = ReplicateImageGeneration()
    ideogram = gen.image_role_transport(SimpleNamespace(model="ideogram-ai/ideogram-v3"))
    assert ideogram == {"edit_target", "mask", "style"}
    assert gen.image_role_transport(SimpleNamespace(model="google/imagen-4")) == frozenset()


# --------------------------------------------------------------------------
# Together + xAI
# --------------------------------------------------------------------------


def test_together_maps_edit_target_and_refs_and_refuses_when_rules_drop_them(monkeypatch):
    from matrx_ai.providers.together.together_image_api import TogetherImageGeneration

    gen = TogetherImageGeneration()
    monkeypatch.setattr(
        gen, "_outbound_params", lambda controls, cfg, extra_canonical=None, **k: dict(extra_canonical)
    )
    config = _config("black-forest-labs/FLUX.1-kontext-max", _img("edit_target", "base"), _img("style", "s"))
    kwargs = gen._build_kwargs(config, _profile("m", {}))
    assert kwargs["image_url"] == "https://cdn.example.com/base.png"
    assert kwargs["reference_images"][0] == "https://cdn.example.com/s.png"
    assert "Image 1 is the style reference" in kwargs["prompt"]

    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    with pytest.raises(ImageRoleCompatibilityError, match="Together"):
        gen._build_kwargs(config, _profile("m", {}))


def test_xai_puts_roled_images_first_in_image_urls(monkeypatch):
    from matrx_ai.providers.xai.xai_image_api import XAIImageGeneration

    gen = XAIImageGeneration()
    monkeypatch.setattr(gen, "_outbound_params", lambda *a, **k: {})
    kwargs = gen._build_kwargs(
        _config("grok-imagine-image", _img("subject", "p"), _img("edit_target", "b")),
        _profile("grok-imagine-image", {}),
    )
    assert kwargs["image_urls"][:2] == [
        "https://cdn.example.com/b.png",
        "https://cdn.example.com/p.png",
    ]


# --------------------------------------------------------------------------
# The refusal happens BEFORE the paid call
# --------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_execute_refuses_before_any_provider_call():
    from matrx_ai.providers.base_media import BaseMediaGeneration

    calls: list[Any] = []

    class _Gen(BaseMediaGeneration):
        provider = "stub"
        modality = "image"

        def _build_kwargs(self, unified_config, profile):
            calls.append("build")
            return {}

        def _call_provider(self, kwargs):
            calls.append("paid")

        def _extract_assets(self, raw):
            return []

        def _classify_error(self, exc):
            return None

    with pytest.raises(ImageRoleCompatibilityError):
        await _Gen().execute(_config("stub-model", _img("style")), _profile("stub-model", {}))
    assert calls == []
