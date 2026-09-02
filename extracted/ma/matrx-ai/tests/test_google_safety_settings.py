from __future__ import annotations

import json
from pathlib import Path

from google.genai import types

from matrx_ai.config import (
    ImageContent,
    MessageList,
    TextContent,
    UnifiedConfig,
    UnifiedMessage,
)
from matrx_ai.providers.google.google_image_api import GoogleImageGeneration
from matrx_ai.providers.google.google_video_api import GoogleVideoGeneration
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.testing.profile_factory import make_profile


def _config(model: str) -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        messages=MessageList(
            _messages=[
                UnifiedMessage(
                    role="user",
                    content=[TextContent(text="Explain the supplied material.")],
                )
            ]
        ),
    )


def _assert_every_adjustable_filter_is_off(
    safety_settings: list[types.SafetySetting] | None,
) -> None:
    assert safety_settings is not None
    by_category = {setting.category: setting.threshold for setting in safety_settings}
    assert by_category == {
        types.HarmCategory.HARM_CATEGORY_HARASSMENT: types.HarmBlockThreshold.OFF,
        types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: types.HarmBlockThreshold.OFF,
        types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: types.HarmBlockThreshold.OFF,
        types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: types.HarmBlockThreshold.OFF,
    }


def test_google_chat_always_sends_lowest_adjustable_safety_settings() -> None:
    profile = make_profile(
        model_name="gemini-3.5-flash-lite",
        wire_format="google_chat",
        vendor="google",
    )

    built = GoogleTranslator().to_google(
        _config("gemini-3.5-flash-lite"),
        profile,
    )

    _assert_every_adjustable_filter_is_off(built["config"].safety_settings)


def test_native_google_image_always_sends_lowest_adjustable_safety_settings() -> None:
    profile = make_profile(
        model_name="gemini-3.1-flash-image",
        wire_format="google_image",
        vendor="google",
        capabilities={
            "input": ["text", "image"],
            "output": ["image"],
            "features": [],
            "interaction": "turn",
            "multilingual": True,
        },
    )
    client = object.__new__(GoogleImageGeneration)
    client.translator = GoogleTranslator()
    client._is_imagen_call = False

    built = client._build_kwargs(
        _config("gemini-3.1-flash-image"),
        profile,
    )

    _assert_every_adjustable_filter_is_off(built["config"].safety_settings)


def test_native_google_image_repairs_retired_half_k_wire_alias(caplog) -> None:
    profile = make_profile(
        model_name="gemini-3.1-flash-image",
        wire_format="google_image",
        vendor="google",
        rules={
            "resolution": {
                "supported": True,
                "provider_key": "image_size",
                "value_map": {"0.5k": "0.5K"},
            }
        },
        capabilities={
            "input": ["text", "image"],
            "output": ["image"],
            "features": [],
            "interaction": "turn",
            "multilingual": True,
        },
    )
    client = object.__new__(GoogleImageGeneration)
    client.translator = GoogleTranslator()
    client._is_imagen_call = False
    config = _config("gemini-3.1-flash-image")
    config.resolution = "0.5k"

    built = client._build_kwargs(config, profile)

    assert built["config"].image_config.image_size == "512"
    assert "Retired image_size '0.5K'" in caplog.text


def test_native_google_image_repairs_half_k_to_supported_one_k(caplog) -> None:
    profile = make_profile(
        model_name="gemini-3-pro-image",
        wire_format="google_image",
        vendor="google",
        rules={
            "resolution": {
                "supported": True,
                "provider_key": "image_size",
                "value_map": {"0.5k": "0.5K"},
            }
        },
    )
    client = object.__new__(GoogleImageGeneration)
    client.translator = GoogleTranslator()
    client._is_imagen_call = False
    config = _config("gemini-3-pro-image")
    config.resolution = "0.5k"

    built = client._build_kwargs(config, profile)

    assert built["config"].image_config.image_size == "1K"
    assert "model-supported equivalent '1K'" in caplog.text


def test_google_tts_omits_unsupported_safety_settings() -> None:
    profile = make_profile(
        model_name="gemini-3.1-flash-tts-preview",
        wire_format="google_chat",
        vendor="google",
        capabilities={
            "input": ["text"],
            "output": ["audio"],
            "features": [],
            "interaction": "turn",
            "multilingual": True,
        },
    )

    built = GoogleTranslator().to_google(
        _config("gemini-3.1-flash-tts-preview"),
        profile,
    )

    assert not built["config"].safety_settings


def test_veo_text_generation_pins_least_restrictive_person_setting() -> None:
    profile = make_profile(
        model_name="veo-3.1-generate-preview",
        wire_format="google_video",
        vendor="google",
        capabilities={
            "input": ["text", "image"],
            "output": ["video"],
            "features": [],
            "interaction": "job",
            "multilingual": True,
        },
    )
    client = object.__new__(GoogleVideoGeneration)
    client.translator = GoogleTranslator()

    built = client._build_kwargs(
        _config("veo-3.1-generate-preview"),
        profile,
    )

    assert built["config"].person_generation == "ALLOW_ALL"
    assert built["config"].duration_seconds == 8


def test_veo_image_generation_pins_least_restrictive_supported_person_setting() -> None:
    profile = make_profile(
        model_name="veo-3.1-generate-preview",
        wire_format="google_video",
        vendor="google",
        capabilities={
            "input": ["text", "image"],
            "output": ["video"],
            "features": [],
            "interaction": "job",
            "multilingual": True,
        },
    )
    client = object.__new__(GoogleVideoGeneration)
    client.translator = GoogleTranslator()
    config = _config("veo-3.1-generate-preview")
    config.image_input = ImageContent(
        base64_data="aW1hZ2U=",
        mime_type="image/png",
    )

    built = client._build_kwargs(config, profile)

    assert built["config"].person_generation == "ALLOW_ADULT"


def test_imagen_catalog_fixture_pins_lowest_supported_safety_posture() -> None:
    fixture = (
        Path(__file__).parent
        / "fixtures"
        / "media_family_rules"
        / "google_image__v2.json"
    )
    rules = json.loads(fixture.read_text(encoding="utf-8"))["rules"]

    assert rules["safety_filter_level"]["const"] == "BLOCK_ONLY_HIGH"
    assert rules["person_generation"]["const"] == "ALLOW_ALL"
