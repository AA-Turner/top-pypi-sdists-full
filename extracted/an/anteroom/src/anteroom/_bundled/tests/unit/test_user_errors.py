from __future__ import annotations

from anteroom.services.user_errors import build_user_error, format_user_error, normalize_error_text


def test_build_user_error_adds_display_message_and_suggestion() -> None:
    payload = build_user_error(
        "Cannot connect to API (3 attempts).",
        code="connection_error",
        retryable=True,
        base_url="http://localhost:11434/v1",
    )

    assert payload["retryable"] is True
    assert payload["suggestion"] == "Check AI_CHAT_BASE_URL (http://localhost:11434/v1)"
    assert payload["display_message"] == (
        "Cannot connect to API (3 attempts). — Check AI_CHAT_BASE_URL (http://localhost:11434/v1)"
    )


def test_format_user_error_collapses_multiline_traceback() -> None:
    text = """Traceback (most recent call last):\n  File \"x.py\", line 1, in <module>\nRuntimeError: boom"""
    assert format_user_error(text) == "RuntimeError: boom"


def test_normalize_error_text_collapses_whitespace() -> None:
    assert normalize_error_text("  bad   request\n\nfrom  provider  ") == "bad request from provider"
