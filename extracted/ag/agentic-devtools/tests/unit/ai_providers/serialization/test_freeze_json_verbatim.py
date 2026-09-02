from types import MappingProxyType

import pytest

from agentic_devtools.ai_providers.serialization import freeze_json_verbatim


def test_freeze_json_verbatim_preserves_credential_keys():
    original = {
        "token": "transport-secret",
        "accessToken": "bearer-value",
        "api_key": "raw-key",
        "nested": {"refresh_token": "r-token", "safe": [1, 2]},
    }

    frozen = freeze_json_verbatim(original)

    assert isinstance(frozen, MappingProxyType)
    assert frozen["token"] == "transport-secret"
    assert frozen["accessToken"] == "bearer-value"
    assert frozen["api_key"] == "raw-key"
    assert frozen["nested"]["refresh_token"] == "r-token"
    assert frozen["nested"]["safe"] == (1, 2)


def test_freeze_json_verbatim_is_immutable():
    original: dict[str, object] = {"items": [1, 2, 3]}
    frozen = freeze_json_verbatim(original)

    assert isinstance(frozen["items"], tuple)
    with pytest.raises((TypeError, AttributeError)):
        frozen["items"] = (4,)  # type: ignore[index]

    original["items"] = [99]
    assert frozen["items"] == (1, 2, 3)


def test_freeze_json_verbatim_rejects_non_finite_floats():
    with pytest.raises(ValueError, match="Non-finite float values are not valid JSON"):
        freeze_json_verbatim({"value": float("nan")})


def test_freeze_json_verbatim_rejects_non_string_keys():
    with pytest.raises(TypeError, match="JSON object keys must be strings"):
        freeze_json_verbatim({1: "bad"})  # type: ignore[dict-item]
