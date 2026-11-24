"""A provider 404 that names the voice says the voice is gone, never "model or endpoint ... retired or renamed".

Live 2026-11-17: Cartesia answered 404 ``voice_not_found`` for a person's chosen voice; the classifier flattened it to
"The requested cartesia model or endpoint was not found" and the person was told to look at a model that was fine.
"""

from matrx_ai.providers.errors import classify_provider_error


class _ClientReported(Exception):
    status_code = 404


def test_cartesia_voice_404_is_named_a_voice():
    info = classify_provider_error("cartesia", _ClientReported("[voice_not_found] The requested voice was not found."))
    assert info.error_type == "voice_not_found"
    assert "voice" in info.user_message and "model or endpoint" not in info.user_message
    assert info.is_retryable is False


def test_a_model_404_is_still_a_model_404():
    info = classify_provider_error("cartesia", _ClientReported("[not_found] model sonic-9 does not exist"))
    assert info.error_type == "not_found"
    assert "not available" in info.user_message and "voice" not in info.user_message
