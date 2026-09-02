from agentic_devtools.ai_providers.availability import build_default_matrix


def test_build_default_matrix_matches_canonical_inventory() -> None:
    matrix = build_default_matrix()

    assert matrix == {
        "claude-opus-5": "available",
        "claude-sonnet-5": "available",
        "mai-code-1.1-flash": "available",
        "gpt-5.6-luna": "available",
        "gemini-3.1-pro-preview": "rejected",
        "claude-opus-4.8": "rejected",
        "claude-opus-4.6": "rejected",
        "claude-sonnet-4.6": "excluded",
        "gemini-3.6-flash": "excluded",
        "gpt-5.4-mini": "excluded",
    }
