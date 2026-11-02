"""Tests for ``ensure_mdc_frontmatter``."""

from agentic_devtools.cli.speckit.scaffold_update_agent_context import (
    MDC_FRONTMATTER,
    ensure_mdc_frontmatter,
)


class TestEnsureMdcFrontmatter:
    """ensure_mdc_frontmatter prepends alwaysApply frontmatter when absent."""

    def test_prepends_frontmatter_to_empty_string(self) -> None:
        result = ensure_mdc_frontmatter("")
        assert result == MDC_FRONTMATTER

    def test_prepends_frontmatter_to_content_without_frontmatter(self) -> None:
        content = "# Rules\nsome content\n"
        result = ensure_mdc_frontmatter(content)
        assert result == MDC_FRONTMATTER + content

    def test_leaves_content_unchanged_when_frontmatter_present(self) -> None:
        content = "---\nalwaysApply: true\n---\n# Rules\n"
        assert ensure_mdc_frontmatter(content) == content

    def test_preserves_custom_frontmatter_when_always_apply_is_true(self) -> None:
        content = "---\nalwaysApply: true\ndescription: My rules\n---\n# Rules\n"
        assert ensure_mdc_frontmatter(content) == content

    def test_replaces_always_apply_false_with_true(self) -> None:
        content = "---\nalwaysApply: false\ndescription: My rules\n---\n# Rules\n"
        result = ensure_mdc_frontmatter(content)
        assert "alwaysApply: true" in result
        assert "alwaysApply: false" not in result

    def test_replaces_always_apply_false_with_inline_comment(self) -> None:
        content = "---\nalwaysApply: false # temporarily disabled\ndescription: My rules\n---\n# Rules\n"
        result = ensure_mdc_frontmatter(content)
        assert "alwaysApply: true" in result
        assert "alwaysApply: false" not in result
        assert result.count("alwaysApply:") == 1

    def test_replaces_always_apply_true_with_inline_comment(self) -> None:
        content = "---\nalwaysApply: true # enabled\n---\n# Rules\n"
        result = ensure_mdc_frontmatter(content)
        assert "alwaysApply: true" in result
        assert result.count("alwaysApply:") == 1

    def test_adds_always_apply_when_frontmatter_omits_it(self) -> None:
        content = "---\ndescription: My rules\n---\n# Rules\n"
        result = ensure_mdc_frontmatter(content)
        assert result.startswith("---\ndescription: My rules\nalwaysApply: true\n---\n")

    def test_handles_empty_frontmatter_idempotently(self) -> None:
        content = "---\n---\n# Rules\n"
        result = ensure_mdc_frontmatter(content)
        assert result == "---\nalwaysApply: true\n---\n# Rules\n"

    def test_is_idempotent_on_own_output(self) -> None:
        content = "# Rules\n"
        once = ensure_mdc_frontmatter(content)
        twice = ensure_mdc_frontmatter(once)
        assert once == twice

    # CRLF regression cases — Windows-edited .mdc files must be detected and
    # updated rather than receiving a spurious second frontmatter block.

    def test_crlf_frontmatter_is_detected_not_doubled(self) -> None:
        """A CRLF frontmatter that already has alwaysApply: true is left unchanged."""
        content = "---\r\nalwaysApply: true\r\n---\r\n# Rules\r\n"
        result = ensure_mdc_frontmatter(content)
        assert result == content

    def test_crlf_frontmatter_replaces_always_apply_false(self) -> None:
        content = "---\r\nalwaysApply: false\r\n---\r\n# Rules\r\n"
        result = ensure_mdc_frontmatter(content)
        assert "---\r\nalwaysApply: true\r\n---\r\n" in result
        assert "alwaysApply: false" not in result

    def test_crlf_frontmatter_adds_always_apply_when_absent(self) -> None:
        content = "---\r\ndescription: My rules\r\n---\r\n# Rules\r\n"
        result = ensure_mdc_frontmatter(content)
        assert result.startswith("---\r\ndescription: My rules\r\nalwaysApply: true\r\n---\r\n")

    def test_crlf_empty_frontmatter_becomes_always_apply(self) -> None:
        content = "---\r\n---\r\n# Rules\r\n"
        result = ensure_mdc_frontmatter(content)
        assert result == "---\r\nalwaysApply: true\r\n---\r\n# Rules\r\n"

    def test_replaces_quoted_always_apply_false_with_true(self) -> None:
        """alwaysApply: "false" (quoted string) must be replaced, not appended."""
        content = '---\nalwaysApply: "false"\ndescription: My rules\n---\n# Rules\n'
        result = ensure_mdc_frontmatter(content)
        assert "alwaysApply: true" in result
        assert '"false"' not in result
        assert result.count("alwaysApply:") == 1

    def test_replaces_quoted_always_apply_true_leaves_one_key(self) -> None:
        """alwaysApply: 'true' (single-quoted) must not yield duplicate keys."""
        content = "---\nalwaysApply: 'true'\n---\n# Rules\n"
        result = ensure_mdc_frontmatter(content)
        assert "alwaysApply: true" in result
        assert result.count("alwaysApply:") == 1
