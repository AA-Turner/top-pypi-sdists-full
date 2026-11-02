"""Tests for _fence()."""

from agentic_devtools.cli.ci.github_provider import _fence


class TestFence:
    """Tests for the injection-safe code-fencing helper."""

    def test_plain_content_uses_three_backticks(self) -> None:
        assert _fence("hello") == "```\nhello\n```"

    def test_content_with_triple_backtick_run_uses_four(self) -> None:
        result = _fence("a\n```\nb")
        assert result.startswith("````\n")
        assert result.endswith("\n````")
        assert "a\n```\nb" in result

    def test_content_with_quad_backtick_run_uses_five(self) -> None:
        result = _fence("````")
        assert result.startswith("`````\n")
        assert result.endswith("\n`````")

    def test_language_hint_is_applied(self) -> None:
        assert _fence("code", lang="python") == "```python\ncode\n```"
