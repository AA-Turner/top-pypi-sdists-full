import pytest

from agentic_devtools.cli.ci.comment_format import format_ai_pr_loop_comment


def test_appends_exact_terminal_label() -> None:
    assert format_ai_pr_loop_comment("body") == "body\n\n🤖 AI PR Loop ·"


def test_does_not_duplicate_existing_terminal_label() -> None:
    assert format_ai_pr_loop_comment("body\n\n🤖 AI PR Loop ·") == "body\n\n🤖 AI PR Loop ·"


def test_preserves_quoted_label_in_freeform_body() -> None:
    body = "Quoted review:\n> 🤖 AI PR Loop ·"

    assert format_ai_pr_loop_comment(body) == f"{body}\n\n🤖 AI PR Loop ·"


def test_rejects_non_string_body() -> None:
    with pytest.raises(TypeError, match="body must be a string"):
        format_ai_pr_loop_comment(None)  # type: ignore[arg-type]


def test_rejects_malformed_terminal_label() -> None:
    with pytest.raises(ValueError, match="malformed terminal label"):
        format_ai_pr_loop_comment("body\n🤖 AI PR Loop ·")
