"""Tests for commit_node message generation."""

from agentic_devtools.orchestration.nodes.commit import _generate_commit_message


class TestGenerateCommitMessage:
    def test_github_issue_format(self):
        msg = _generate_commit_message("42", "implement feature", {"summary": "Add login"})
        assert "feat(#42):" in msg
        assert "#42" in msg

    def test_jira_issue_format(self):
        msg = _generate_commit_message("PROJECT-1234", "implement feature", {"summary": "Add login"})
        assert "feat(PROJECT-1234):" in msg
        assert "[PROJECT-1234](https://jira.swica.ch/browse/PROJECT-1234)" in msg

    def test_uses_issue_summary(self):
        msg = _generate_commit_message("42", "", {"summary": "Add user authentication"})
        assert "Add user authentication" in msg

    def test_truncates_long_title(self):
        long_summary = "x" * 100
        msg = _generate_commit_message("42", "", {"summary": long_summary})
        first_line = msg.split("\n")[0]
        assert len(first_line) <= 72

    def test_includes_footer_reference(self):
        msg = _generate_commit_message("42", "", {"summary": "test"})
        assert "#42" in msg

    def test_non_dict_issue_data_uses_default_summary(self):
        """When issue_data is not a dict, falls back to plan or default summary."""
        msg = _generate_commit_message("42", "", None)
        assert "implement autonomous workflow" in msg

    def test_plan_first_line_becomes_summary(self):
        """A non-empty plan first line (with no issue summary) becomes the commit summary."""
        msg = _generate_commit_message("42", "Add Webhook Support\nmore detail", {"summary": ""})
        assert "add webhook support" in msg

    def test_plan_with_empty_first_line_uses_default(self):
        """When plan starts with empty line, falls back to default summary."""
        msg = _generate_commit_message("42", "\n\nreal content", {"summary": ""})
        assert "implement autonomous workflow" in msg

    def test_non_string_summary_in_dict_treated_as_empty(self):
        """A non-string summary in issue_data is discarded; falls back to plan/default."""
        for bad_summary in [42, ["Add login"], {"key": "val"}, True]:
            msg = _generate_commit_message("42", "", {"summary": bad_summary})
            assert "implement autonomous workflow" in msg, bad_summary

    def test_non_string_plan_treated_as_empty(self):
        """A non-string plan is normalized to empty; falls back to default summary."""
        for bad_plan in [None, 42, ["step1"], {"k": "v"}]:
            msg = _generate_commit_message("42", bad_plan, {"summary": ""})
            assert "implement autonomous workflow" in msg, bad_plan

    def test_explicit_provider_overrides_inferred_provider(self):
        """Explicit issue_provider drives footer format."""
        msg = _generate_commit_message(
            "PROJECT-1234",
            "implement feature",
            {"summary": "Add login"},
            issue_provider="github",
        )
        assert "feat(PROJECT-1234):" in msg
        assert "\n\nPROJECT-1234" in msg

    def test_unhashable_issue_provider_falls_back_to_inferred(self):
        """A corrupted dict/list issue_provider does not raise TypeError; inferred provider is used."""
        for bad_provider in [{"type": "github"}, ["github"], 42, True]:
            msg = _generate_commit_message(
                "42",
                "implement feature",
                {"summary": "Add login"},
                issue_provider=bad_provider,  # type: ignore[arg-type]
            )
            # Inferred provider for digit key is "github"; footer should be plain scope
            assert "#42" in msg, bad_provider
