"""Tests for _neutralize_copilot_mentions()."""

from agentic_devtools.cli.ci.github_provider import _neutralize_copilot_mentions


def test_neutralizes_case_insensitive_copilot_mentions() -> None:
    assert _neutralize_copilot_mentions("Ask @Copilot and @COPILOT") == "Ask @\u200bcopilot and @\u200bcopilot"


def test_preserves_text_without_copilot_mentions() -> None:
    assert _neutralize_copilot_mentions("Ordinary review bookkeeping") == "Ordinary review bookkeeping"


def test_preserves_mentions_inside_suggestion_fences() -> None:
    body = 'Prose @copilot\n```suggestion\nmention = "@copilot"\n```\nMore @Copilot prose'

    assert _neutralize_copilot_mentions(body) == (
        'Prose @\u200bcopilot\n```suggestion\nmention = "@copilot"\n```\nMore @\u200bcopilot prose'
    )


def test_preserves_list_nested_suggestion_fence_payload() -> None:
    body = '1. Apply this suggestion:\n\n    ```suggestion\n    mention = "@copilot"\n    ```\nOutside @copilot'

    assert _neutralize_copilot_mentions(body) == (
        '1. Apply this suggestion:\n\n    ```suggestion\n    mention = "@copilot"\n    ```\nOutside @\u200bcopilot'
    )


def test_preserves_mentions_inside_tilde_fences() -> None:
    body = "Prose @copilot\n~~~python\nmention = '@copilot'\n~~~"

    assert _neutralize_copilot_mentions(body) == "Prose @\u200bcopilot\n~~~python\nmention = '@copilot'\n~~~"


def test_preserves_mentions_inside_fences_with_indented_closing_delimiters() -> None:
    body = '```suggestion\nmention = "@copilot"\n  ```'

    assert _neutralize_copilot_mentions(body) == body


def test_preserves_mentions_in_suggestion_after_empty_fence() -> None:
    body = "```\n```\n```suggestion\nmention = '@copilot'\n```"

    assert _neutralize_copilot_mentions(body) == body


def test_does_not_close_fence_on_mismatched_or_invalid_delimiters() -> None:
    body = "````suggestion\n~~~\n```\n```` not-close\nmention = '@copilot'\n`````"

    assert _neutralize_copilot_mentions(body) == body


def test_preserves_mentions_in_unclosed_fence() -> None:
    body = "~~~python\nmention = '@copilot'"

    assert _neutralize_copilot_mentions(body) == body


def test_does_not_treat_backtick_in_info_string_as_fence() -> None:
    body = "```invalid`info\n@copilot"

    assert _neutralize_copilot_mentions(body) == "```invalid`info\n@\u200bcopilot"
