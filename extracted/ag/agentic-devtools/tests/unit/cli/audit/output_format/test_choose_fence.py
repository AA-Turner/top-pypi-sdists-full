"""Tests for _choose_fence() helper in output_format."""

from agentic_devtools.cli.audit.output_format import _choose_fence


class TestChooseFence:
    """Tests for _choose_fence() — dynamic code-fence selection."""

    def test_plain_content_returns_triple_backtick(self) -> None:
        """Content without any backticks gets the minimum 3-backtick fence."""
        assert _choose_fence("Hello world") == "```"

    def test_empty_content_returns_triple_backtick(self) -> None:
        """Empty content gets the minimum 3-backtick fence."""
        assert _choose_fence("") == "```"

    def test_content_with_triple_backtick_returns_four(self) -> None:
        """Content containing ``` gets a 4-backtick fence."""
        content = "example:\n```python\nprint('hi')\n```"
        fence = _choose_fence(content)
        assert fence == "````"
        assert fence not in content

    def test_content_with_four_backticks_returns_five(self) -> None:
        """Content containing ```` gets a 5-backtick fence."""
        content = "````python\ncode\n````"
        fence = _choose_fence(content)
        assert fence == "`````"
        assert fence not in content

    def test_fence_never_appears_in_content(self) -> None:
        """The returned fence string does not appear literally in the content."""
        content = "``` triple\n```` quad\n````` quint"
        fence = _choose_fence(content)
        assert fence not in content
        assert len(fence) >= 3

    def test_single_backtick_in_content_returns_triple(self) -> None:
        """A single backtick in content still yields the minimum 3-backtick fence."""
        content = "use `variable` here"
        assert _choose_fence(content) == "```"

    def test_double_backtick_in_content_returns_triple(self) -> None:
        """Two consecutive backticks still yield the minimum 3-backtick fence."""
        content = "``double``"
        assert _choose_fence(content) == "```"
