from types import MappingProxyType

import pytest

from agentic_devtools.ai_providers.serialization import freeze_json


def test_freeze_json():
    original = {
        "a": [1, 2, {"b": "c"}],
        "token": "secret_value",
        "api-key": "hidden",
        "nested": {"api_key": "hidden", "safe": True, "tokenizer-settings": "keep"},
    }

    frozen = freeze_json(original)

    assert isinstance(frozen, MappingProxyType)
    assert frozen["token"] == "<redacted>"
    assert frozen["api-key"] == "<redacted>"
    assert isinstance(frozen["a"], tuple)
    assert frozen["nested"]["api_key"] == "<redacted>"
    assert frozen["nested"]["tokenizer-settings"] == "keep"
    assert frozen["nested"]["safe"] is True
    assert isinstance(frozen["a"][2], MappingProxyType)


def test_freeze_json_camel_case_credential_keys():
    frozen = freeze_json(
        {
            "accessToken": "secret",
            "refreshToken": "other-secret",
            "clientSecret": "hidden",
            "apiKey": "key-value",
            "tokenizerSettings": "keep",
        }
    )
    assert frozen["accessToken"] == "<redacted>"
    assert frozen["refreshToken"] == "<redacted>"
    assert frozen["clientSecret"] == "<redacted>"
    assert frozen["apiKey"] == "<redacted>"
    assert frozen["tokenizerSettings"] == "keep"


def test_freeze_json_rejects_non_finite_floats():
    with pytest.raises(ValueError, match="Non-finite float values are not valid JSON"):
        freeze_json({"value": float("nan")})

    with pytest.raises(ValueError, match="Non-finite float values are not valid JSON"):
        freeze_json({"value": float("inf")})

    with pytest.raises(ValueError, match="Non-finite float values are not valid JSON"):
        freeze_json({"value": float("-inf")})


def test_freeze_json_accepts_finite_floats():
    frozen = freeze_json({"pi": 3.14, "zero": 0.0})
    assert frozen["pi"] == 3.14
    assert frozen["zero"] == 0.0


def test_freeze_json_rejects_non_json_values():
    with pytest.raises(TypeError, match="Unsupported JSON value type: set"):
        freeze_json({"bad": {1, 2}})

    with pytest.raises(TypeError, match="JSON object keys must be strings"):
        freeze_json({1: "bad"})
