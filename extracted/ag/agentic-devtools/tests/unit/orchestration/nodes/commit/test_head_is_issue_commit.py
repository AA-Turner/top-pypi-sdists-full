"""Tests for agentic_devtools.orchestration.nodes.commit._head_is_issue_commit."""

from __future__ import annotations

import pytest

from agentic_devtools.orchestration.nodes.commit import _head_is_issue_commit


class TestHeadIsIssueCommit:
    # ---- GitHub numeric key (issue_key="42") ---------------------------------

    def test_github_scope_matches(self):
        """Conventional-commit scope (#42) is recognised."""
        assert _head_is_issue_commit("feat(#42): implement feature\n", "42") is True

    def test_github_footer_matches(self):
        """Bare footer token #42 on its own line is recognised."""
        assert _head_is_issue_commit("fix: resolve crash\n\n#42\n", "42") is True

    def test_github_scope_and_footer_both_match(self):
        """A full conventional commit with both scope and footer passes."""
        assert _head_is_issue_commit("feat(#42): add endpoint\n\n- point 1\n\n#42\n", "42") is True

    def test_github_no_false_positive_version_number(self):
        """Bare '42' embedded in a version string must NOT match."""
        assert _head_is_issue_commit("chore: bump version to v42.0.1", "42") is False

    def test_github_no_false_positive_embedded_larger_number(self):
        """'42' inside '142' or '420' must NOT match."""
        assert _head_is_issue_commit("fix: processed 142 records", "42") is False
        assert _head_is_issue_commit("fix: processed 420 records", "42") is False

    def test_github_no_false_positive_prefixed_hash(self):
        """#142 must NOT match #42."""
        assert _head_is_issue_commit("see #142 for context", "42") is False

    def test_github_no_false_positive_suffixed_word_char(self):
        """#42x must NOT match #42 (trailing word char)."""
        assert _head_is_issue_commit("see #42x for context", "42") is False

    def test_github_no_false_positive_unrelated_number(self):
        """A commit with no reference to the issue at all must NOT match."""
        assert _head_is_issue_commit("docs: update README", "42") is False

    def test_github_footer_inline_in_sentence_matches(self):
        """#42 surrounded by spaces (inline footer) is recognised."""
        assert _head_is_issue_commit("closes #42", "42") is True

    # ---- Jira key (issue_key="PROJECT-42") ----------------------------------

    def test_jira_scope_matches(self):
        """Conventional-commit scope (PROJECT-42) is recognised."""
        assert _head_is_issue_commit("feat(PROJECT-42): implement\n", "PROJECT-42") is True

    def test_jira_footer_matches(self):
        """Jira key on its own footer line is recognised."""
        assert _head_is_issue_commit("fix: something\n\nPROJECT-42\n", "PROJECT-42") is True

    def test_jira_case_insensitive_scope(self):
        """Scope and footer matching is case-insensitive for Jira keys."""
        assert _head_is_issue_commit("feat(project-42): x", "PROJECT-42") is True

    def test_jira_no_false_positive_superset_key(self):
        """PROJECT-420 must NOT match PROJECT-42."""
        assert _head_is_issue_commit("fix: see PROJECT-420 for context", "PROJECT-42") is False

    def test_jira_no_false_positive_embedded_key(self):
        """XPROJECT-42 must NOT match PROJECT-42."""
        assert _head_is_issue_commit("fix: see XPROJECT-42", "PROJECT-42") is False

    def test_jira_no_false_positive_hyphen_prefixed_key(self):
        """SOME-PROJECT-42 must NOT match PROJECT-42 (hyphen in lookbehind)."""
        assert _head_is_issue_commit("fix: see SOME-PROJECT-42", "PROJECT-42") is False

    def test_jira_no_false_positive_unrelated(self):
        """An unrelated commit message must NOT match."""
        assert _head_is_issue_commit("chore: tidy up", "PROJECT-42") is False

    # ---- Edge cases ----------------------------------------------------------

    def test_empty_message_returns_false(self):
        """An empty commit message never matches."""
        assert _head_is_issue_commit("", "42") is False

    def test_whitespace_only_message_returns_false(self):
        """A whitespace-only message never matches."""
        assert _head_is_issue_commit("   \n  ", "42") is False

    @pytest.mark.parametrize("key", ["1", "100", "9999"])
    def test_various_github_numeric_keys(self, key: str):
        """Any valid GitHub numeric key matches its own scope and footer."""
        assert _head_is_issue_commit(f"feat(#{key}): x\n\n#{key}\n", key) is True
        # Adjacent key must not match
        bigger = str(int(key) + 1000)
        assert _head_is_issue_commit(f"feat(#{bigger}): x\n\n#{bigger}\n", key) is False
