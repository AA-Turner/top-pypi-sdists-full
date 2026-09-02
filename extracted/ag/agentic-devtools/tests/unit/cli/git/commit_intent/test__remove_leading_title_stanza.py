"""Tests for agentic_devtools.cli.git.commit_intent._remove_leading_title_stanza.

These lock in that the stale-title regex detects the canonical ``(#NNN)`` scope
form (and the legacy markdown-link form) so a duplicated leading title stanza is
stripped from the commit body regardless of which convention produced it.
"""

from agentic_devtools.cli.git.commit_intent import _remove_leading_title_stanza


class TestRemoveLeadingTitleStanza:
    """Tests for stripping a duplicated leading conventional-commit title stanza."""

    def test_detects_new_hash_scope_form(self):
        """A leading ``fix(#2249): ...`` stanza (new GitHub form) is stripped."""
        body = "fix(#2249): old title\n\nactual body line"
        result = _remove_leading_title_stanza(body, "feat: new title")
        assert result == "actual body line"

    def test_detects_new_parent_child_scope_form(self):
        """A leading ``feat(#10/#42): ...`` parent/child stanza is stripped."""
        body = "feat(#10/#42): sub-feature\n\nreal body"
        result = _remove_leading_title_stanza(body, "feat: new title")
        assert result == "real body"

    def test_detects_legacy_markdown_link_scope_form(self):
        """The legacy markdown-link scope form is still detected (backward compat)."""
        body = "fix([#42](https://github.com/org/repo/issues/42)): old\n\nbody here"
        result = _remove_leading_title_stanza(body, "feat: new title")
        assert result == "body here"

    def test_non_conventional_first_line_preserved(self):
        """A body that does not start with a conventional title is left intact."""
        body = "just some prose\n\nmore prose"
        result = _remove_leading_title_stanza(body, "feat: new title")
        assert result == "just some prose\n\nmore prose"

    def test_matching_create_title_stripped_without_scope(self):
        """A first line equal to the create title (no scope) is also stripped."""
        body = "feat: new title\n\nthe body"
        result = _remove_leading_title_stanza(body, "feat: new title")
        assert result == "the body"

    def test_new_form_without_blank_separator(self):
        """The stanza is stripped even without a blank separator line."""
        body = "fix(#7): title\nbody immediately after"
        result = _remove_leading_title_stanza(body, "feat: x")
        assert result == "body immediately after"
