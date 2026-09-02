from agentic_devtools.ai_providers.availability import _looks_like_invalid_model_response


def test__looks_like_invalid_model_response_matches_model_rejections() -> None:
    assert _looks_like_invalid_model_response("Invalid model: claude-opus-4.8")
    assert _looks_like_invalid_model_response("model was unavailable for this API")
    assert not _looks_like_invalid_model_response("custom_agent is invalid")


def test__looks_like_invalid_model_response_ignores_partial_identifier_matches() -> None:
    assert not _looks_like_invalid_model_response("invalid model_config for this request")
    assert not _looks_like_invalid_model_response("custom_agent_model not found")
