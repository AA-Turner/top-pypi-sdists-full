from agentic_devtools.ai_providers.copilot import _validate_base_url


def test_validate_base_url_strips_trailing_slash() -> None:
    assert _validate_base_url("https://api.github.com/") == "https://api.github.com"
