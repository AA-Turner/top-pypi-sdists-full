import pytest

from agentic_devtools.cli.ci.comment_format import normalize_ai_pr_loop_comment


@pytest.mark.parametrize(
    ("body", "expected"),
    [
        ("legacy", "legacy"),
        ("legacy\n\n🤖 AI PR Loop ·", "legacy"),
        ("quoted\n🤖 AI PR Loop ·\ntext", "quoted\n🤖 AI PR Loop ·\ntext"),
    ],
)
def test_normalizes_only_the_exact_terminal_suffix(body: str, expected: str) -> None:
    assert normalize_ai_pr_loop_comment(body) == expected


@pytest.mark.parametrize(
    "body",
    [
        "legacy\n🤖 AI PR Loop ·",
        "legacy\n\n🤖 AI PR Loop ·\n\n🤖 AI PR Loop ·",
        "state\n🤖 AI PR Loop ·\n\n🤖 AI PR Loop ·",
        "state\n🤖 AI PR Loop · \n\n🤖 AI PR Loop ·",
    ],
)
def test_rejects_malformed_terminal_suffix(body: str) -> None:
    assert normalize_ai_pr_loop_comment(body) is None


def test_preserves_quoted_label_before_valid_suffix() -> None:
    body = "state\n> 🤖 AI PR Loop ·\n\n🤖 AI PR Loop ·"

    assert normalize_ai_pr_loop_comment(body) == "state\n> 🤖 AI PR Loop ·"


def test_rejects_terminal_suffix_with_trailing_whitespace() -> None:
    assert normalize_ai_pr_loop_comment("state\n\n🤖 AI PR Loop · ") is None


def test_rejects_non_string_body() -> None:
    assert normalize_ai_pr_loop_comment(None) is None  # type: ignore[arg-type]
