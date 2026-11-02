"""Tests for GitHubActionsProvider._render_squash_message_from_sdk."""

from pathlib import Path
from unittest.mock import patch

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider

_render = GitHubActionsProvider._render_squash_message_from_sdk
_TMPL = "agentic_devtools.cli.ci.github_provider.resolve_commit_message_from_template"


class TestRenderSquashMessageFromSdk:
    """Tests for turning raw SDK output into a template-rendered commit message."""

    def test_title_and_body_passed_to_template(self):
        with patch(_TMPL, return_value="fix(#42): add x\n\n- a\n\n#42") as mock_tmpl:
            result = _render("add x\n\n- a\n- b", issue_key="42", issue_type="fix")
        assert result == "fix(#42): add x\n\n- a\n\n#42"
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx == {
            "issueType": "fix",
            "commitMessageTitle": "add x",
            "issueKey": "42",
            "commitMessageBody": "- a\n- b",
        }

    def test_no_body_omits_body(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("add x", issue_key="42", issue_type="fix")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert "commitMessageBody" not in ctx
        assert ctx["commitMessageTitle"] == "add x"

    def test_no_issue_key_omits_issue_key(self):
        with patch(_TMPL, return_value=None) as mock_tmpl:
            _render("add x", issue_key=None, issue_type="chore")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert "issueKey" not in ctx
        assert ctx["issueType"] == "chore"

    def test_strips_fences_before_split(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("```\nadd x\n\n- a\n```", issue_key="42", issue_type="fix")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "add x"
        assert ctx["commitMessageBody"] == "- a"

    def test_incomplete_opening_fence_is_not_stripped(self):
        """A leading ``` that is not a complete fence block is left intact (no strip)."""
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("```add x\n\nbody", issue_key="42", issue_type="fix")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "```add x"
        assert ctx["commitMessageBody"] == "body"

    def test_clips_long_title(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("x" * 130, issue_key="42", issue_type="fix")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert len(ctx["commitMessageTitle"]) <= 100

    def test_conversational_title_returns_none_without_rendering(self):
        with patch(_TMPL) as mock_tmpl:
            result = _render("Here is the message: add x", issue_key="42", issue_type="fix")
        assert result is None
        mock_tmpl.assert_not_called()

    def test_empty_raw_returns_none(self):
        with patch(_TMPL) as mock_tmpl:
            result = _render("   ", issue_key="42", issue_type="fix")
        assert result is None
        mock_tmpl.assert_not_called()

    def test_empty_after_fence_strip_returns_none(self):
        with patch(_TMPL) as mock_tmpl:
            result = _render("```\n\n```", issue_key="42", issue_type="fix")
        assert result is None
        mock_tmpl.assert_not_called()

    def test_returns_none_when_template_returns_none(self):
        with patch(_TMPL, return_value=None):
            result = _render("add x", issue_key="42", issue_type="fix")
        assert result is None

    def test_forwards_git_root(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("add x", issue_key="42", issue_type="fix", git_root=Path("/repo"))
        assert mock_tmpl.call_args.args[0] == Path("/repo")

    def test_strips_commit_message_prefix_before_render(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            result = _render("commit message: add x\n\n- a", issue_key="42", issue_type="fix")
        assert result == "rendered"
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "add x"
        assert ctx["commitMessageBody"] == "- a"

    def test_strips_duplicate_conventional_prefix_and_footer_from_sdk_output(self):
        def render_from_context(_git_root: Path | None, *, context: dict[str, str]) -> str:
            body = context.get("commitMessageBody")
            header = f"{context['issueType']}(#{context['issueKey']}): {context['commitMessageTitle']}"
            if not body:
                return f"{header}\n\n#{context['issueKey']}"
            return f"{header}\n\n{body}\n\n#{context['issueKey']}"

        raw = (
            "feat(#2202): make v2 orchestrator PR review the default workflow\n\n"
            "- Replace monolithic file-review + pull-request-overview steps\n\n"
            "#2202"
        )
        with patch(_TMPL, side_effect=render_from_context) as mock_tmpl:
            result = _render(raw, issue_key="2202", issue_type="feat")
        assert result is not None
        assert result.startswith("feat(#2202): make v2 orchestrator PR review the default workflow")
        assert result.count("feat(#2202):") == 1
        assert result.splitlines().count("#2202") == 1
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "make v2 orchestrator PR review the default workflow"
        assert ctx["commitMessageBody"] == "- Replace monolithic file-review + pull-request-overview steps"

    def test_no_prefix_title_is_preserved(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("add webhook support\n\n- detail", issue_key="42", issue_type="fix")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "add webhook support"
        assert ctx["commitMessageBody"] == "- detail"

    def test_subject_colon_is_preserved(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render("add support for foo: bar", issue_key="42", issue_type="fix")
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "add support for foo: bar"

    def test_strips_breaking_prefix_and_breaking_change_footer(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render(
                "fix!: drop legacy behavior\n\n- update docs\n\nBREAKING CHANGE: #2202",
                issue_key="2202",
                issue_type="fix",
            )
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "drop legacy behavior"
        assert ctx["commitMessageBody"] == "- update docs"

    def test_mid_body_issue_reference_is_not_stripped(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render(
                "add update\n\n- Mention #2202 inside prose\n\n- keep this line\n\n#2202",
                issue_key="2202",
                issue_type="feat",
            )
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageBody"] == "- Mention #2202 inside prose\n\n- keep this line"

    def test_render_is_idempotent_for_already_sanitized_output(self):
        def render_from_context(_git_root: Path | None, *, context: dict[str, str]) -> str:
            body = context.get("commitMessageBody")
            header = f"{context['issueType']}(#{context['issueKey']}): {context['commitMessageTitle']}"
            if not body:
                return f"{header}\n\n#{context['issueKey']}"
            return f"{header}\n\n{body}\n\n#{context['issueKey']}"

        raw = "feat(#2202): make flow stable\n\n- keep behavior\n\n#2202"
        with patch(_TMPL, side_effect=render_from_context):
            once = _render(raw, issue_key="2202", issue_type="feat")
            twice = _render(once or "", issue_key="2202", issue_type="feat")
        assert once == twice

    def test_strips_trailing_jira_bare_footer_from_body(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render(
                "feat(PROJECT-1234): improve jira flow\n\n- detail\n\nPROJECT-1234",
                issue_key="PROJECT-1234",
                issue_type="feat",
            )
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "improve jira flow"
        assert ctx["commitMessageBody"] == "- detail"

    def test_strips_trailing_jira_markdown_link_footer_from_body(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render(
                "feat(PROJECT-1234): improve jira flow\n\n- detail\n\n"
                "[PROJECT-1234](https://jira.example.com/browse/PROJECT-1234)",
                issue_key="PROJECT-1234",
                issue_type="feat",
            )
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "improve jira flow"
        assert ctx["commitMessageBody"] == "- detail"

    def test_strips_trailing_multi_issue_footer_line(self):
        with patch(_TMPL, return_value="rendered") as mock_tmpl:
            _render(
                "feat(#2202): batch change\n\n- detail\n\n#2202, #2203",
                issue_key="2202",
                issue_type="feat",
            )
        ctx = mock_tmpl.call_args.kwargs["context"]
        assert ctx["commitMessageTitle"] == "batch change"
        assert ctx["commitMessageBody"] == "- detail"
