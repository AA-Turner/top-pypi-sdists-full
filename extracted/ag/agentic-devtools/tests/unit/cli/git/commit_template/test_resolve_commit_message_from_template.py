"""Tests for resolve_commit_message_from_template."""

from unittest.mock import Mock, patch

from agentic_devtools.cli.git.commit_template import (
    TEMPLATE_PATH,
    resolve_commit_message_from_template,
)

_MOD = "agentic_devtools.cli.git.commit_template"


class TestResolveCommitMessageFromTemplate:
    """Tests for resolve_commit_message_from_template."""

    def test_returns_rendered_message(self, tmp_path):
        """Returns rendered commit message on success."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("feat({{ issueKey }}): {{ commitMessageTitle }}", encoding="utf-8")
        ctx = {"issueKey": "42", "commitMessageTitle": "add feature"}
        with patch(f"{_MOD}._build_render_context", return_value=ctx):
            result = resolve_commit_message_from_template(tmp_path)
        assert result == "feat(42): add feature"

    def test_explicit_context_bypasses_state(self, tmp_path):
        """An explicit context is used verbatim; _build_render_context is not called."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("feat(#{{ issueKey }}): {{ commitMessageTitle }}", encoding="utf-8")
        ctx = {"issueKey": "2249", "commitMessageTitle": "fix squash"}
        with patch(f"{_MOD}._build_render_context", side_effect=AssertionError("should not be called")):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "feat(#2249): fix squash"

    def test_explicit_context_missing_hard_required_returns_none(self, tmp_path, capsys):
        """Explicit context missing a referenced hard-required var returns None."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("{{ issueType }}(#{{ issueKey }}): {{ commitMessageTitle }}", encoding="utf-8")
        # Missing issueKey (hard-required + referenced).
        ctx = {"issueType": "feat", "commitMessageTitle": "x"}
        result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result is None
        assert "issueKey" in capsys.readouterr().err

    def test_returns_none_when_no_template(self, tmp_path):
        """Returns None when template file does not exist (FR-005 fallback)."""
        result = resolve_commit_message_from_template(tmp_path)
        assert result is None

    def test_returns_none_for_syntax_error(self, tmp_path, capsys):
        """Returns None when template has syntax error (FR-007 fallback)."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("{% if x %}", encoding="utf-8")
        result = resolve_commit_message_from_template(tmp_path)
        assert result is None

    def test_returns_none_when_rendered_empty(self, tmp_path, capsys):
        """Returns None when template renders to empty string."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("{{ missing }}", encoding="utf-8")
        with patch(f"{_MOD}._build_render_context", return_value={}):
            # Missing variables render as empty string with jinja2.Undefined
            result = resolve_commit_message_from_template(tmp_path)
        assert result is None

    @patch(f"{_MOD}._discover_git_root", return_value=None)
    def test_returns_none_when_not_in_git_repo(self, mock_discover):
        """Returns None when git_root is None and cannot be discovered."""
        result = resolve_commit_message_from_template(None)
        assert result is None

    @patch(f"{_MOD}._discover_git_root")
    def test_discovers_git_root_when_none(self, mock_discover, tmp_path):
        """Discovers git root when not provided."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("{{ issueType }}: msg", encoding="utf-8")
        mock_discover.return_value = tmp_path
        with patch(f"{_MOD}._build_render_context", return_value={"issueType": "feat"}):
            result = resolve_commit_message_from_template(None)
        assert result == "feat: msg"

    def test_strips_trailing_whitespace(self, tmp_path):
        """Strips trailing whitespace from rendered message."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("feat: title   \n\n\n", encoding="utf-8")
        with patch(f"{_MOD}._build_render_context", return_value={}):
            result = resolve_commit_message_from_template(tmp_path)
        assert result == "feat: title"

    def test_undefined_variables_render_empty(self, tmp_path, capsys):
        """Template with undefined variables renders them as empty strings when not hard-required."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        # Use only commitMessageBody (soft-required) as the undefined var so we
        # don't hit the hard-required guard and can verify jinja2.Undefined behaviour.
        template_file.write_text("feat: {{ commitMessageTitle }}\n\n{{ commitMessageBody }}", encoding="utf-8")
        ctx = {"commitMessageTitle": "add feature"}
        with patch(f"{_MOD}._build_render_context", return_value=ctx):
            result = resolve_commit_message_from_template(tmp_path)
        # commitMessageBody is soft-required; rendering proceeds with it empty
        assert result == "feat: add feature"
        # A warning should still be emitted for the unresolved soft-required var
        err = capsys.readouterr().err
        assert "commitMessageBody" in err
        assert "unresolved" in err.lower()

    def test_returns_none_when_hard_required_vars_missing(self, tmp_path, capsys):
        """Returns None when hard-required variables are referenced but unresolved."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text(
            "{{ issueType }}([#{{ issueKey }}]({{ issueLink }})): {{ commitMessageTitle }}",
            encoding="utf-8",
        )
        with patch(f"{_MOD}._build_render_context", return_value={}):
            result = resolve_commit_message_from_template(tmp_path)
        assert result is None
        err = capsys.readouterr().err
        assert "falling back" in err.lower()
        # All four hard-required vars should be mentioned
        for var in ("issueType", "issueKey", "issueLink", "commitMessageTitle"):
            assert var in err

    def test_returns_none_on_render_syntax_error(self, tmp_path, capsys):
        """Returns None when env.from_string raises TemplateSyntaxError."""
        import jinja2

        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("valid content", encoding="utf-8")
        _sandboxed = "jinja2.sandbox.SandboxedEnvironment.from_string"
        with patch(f"{_MOD}._build_render_context", return_value={}):
            with patch(_sandboxed, side_effect=jinja2.TemplateSyntaxError("bad", 1)):
                result = resolve_commit_message_from_template(tmp_path)
        assert result is None
        assert "syntax error" in capsys.readouterr().err

    def test_returns_none_on_undefined_error(self, tmp_path, capsys):
        """Returns None when template render raises UndefinedError."""
        import jinja2

        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("valid content", encoding="utf-8")
        mock_tmpl = type("MockTemplate", (), {"render": staticmethod(lambda **_kw: None)})()
        mock_tmpl.render = lambda _ctx=None, **_kw: (_ for _ in ()).throw(jinja2.UndefinedError("x is undefined"))
        with patch(f"{_MOD}._build_render_context", return_value={}):
            with patch("jinja2.sandbox.SandboxedEnvironment.from_string", return_value=mock_tmpl):
                result = resolve_commit_message_from_template(tmp_path)
        assert result is None
        assert "undefined variable" in capsys.readouterr().err

    def test_returns_none_on_template_runtime_error(self, tmp_path, capsys):
        """Returns None when template render raises TemplateRuntimeError."""
        import jinja2

        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("valid content", encoding="utf-8")
        mock_tmpl = Mock()
        mock_tmpl.render.side_effect = jinja2.TemplateRuntimeError("runtime boom")
        with patch(f"{_MOD}._build_render_context", return_value={}):
            with patch("jinja2.sandbox.SandboxedEnvironment.from_string", return_value=mock_tmpl):
                result = resolve_commit_message_from_template(tmp_path)
        assert result is None
        assert "runtime error" in capsys.readouterr().err

    def test_returns_none_on_unexpected_render_error(self, tmp_path, capsys):
        """Returns None when template rendering raises an unexpected error."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("valid content", encoding="utf-8")
        mock_tmpl = Mock()
        mock_tmpl.render.side_effect = RuntimeError("boom")
        with patch(f"{_MOD}._build_render_context", return_value={}):
            with patch("jinja2.sandbox.SandboxedEnvironment.from_string", return_value=mock_tmpl):
                result = resolve_commit_message_from_template(tmp_path)
        assert result is None
        assert "unexpected commit template rendering error" in capsys.readouterr().err.lower()

    def test_explicit_context_augmented_with_derived_issue_link(self, tmp_path):
        """Explicit context missing issueLink gets it derived from issueKey."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text(
            "{{ issueType }}(#{{ issueKey }}): {{ commitMessageTitle }}\n\n[#{{ issueKey }}]({{ issueLink }})",
            encoding="utf-8",
        )
        ctx = {"issueType": "fix", "issueKey": "42", "commitMessageTitle": "fix squash"}
        with patch(f"{_MOD}._derive_issue_link_from_key", return_value="https://github.com/o/r/issues/42"):
            with patch(f"{_MOD}._build_render_context", side_effect=AssertionError("should not be called")):
                result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "fix(#42): fix squash\n\n[#42](https://github.com/o/r/issues/42)"

    def test_explicit_context_augmented_with_jira_issue_link(self, tmp_path):
        """Explicit context with a Jira key gets issueLink derived for a Jira template."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text(
            "{{ issueType }}({{ issueKey }}): {{ commitMessageTitle }}\n\n[{{ issueKey }}]({{ issueLink }})",
            encoding="utf-8",
        )
        ctx = {"issueType": "feat", "issueKey": "PROJECT-1234", "commitMessageTitle": "add thing"}
        derived = "https://jira.example.com/browse/PROJECT-1234"
        with patch(f"{_MOD}._derive_issue_link_from_key", return_value=derived):
            with patch(f"{_MOD}._build_render_context", side_effect=AssertionError("should not be called")):
                result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "feat(PROJECT-1234): add thing\n\n[PROJECT-1234](https://jira.example.com/browse/PROJECT-1234)"

    def test_explicit_context_does_not_overwrite_provided_issue_link(self, tmp_path):
        """Explicit context that already contains issueLink is left unchanged."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("{{ issueType }}: {{ commitMessageTitle }} {{ issueLink }}", encoding="utf-8")
        ctx = {
            "issueType": "fix",
            "issueKey": "42",
            "commitMessageTitle": "title",
            "issueLink": "https://custom.example.com/42",
        }
        with patch(f"{_MOD}._derive_issue_link_from_key", side_effect=AssertionError("should not be called")):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "fix: title https://custom.example.com/42"

    def test_explicit_context_augmentation_skipped_when_no_issue_key(self, tmp_path):
        """No augmentation attempt when issueKey is absent from the explicit context."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text("{{ issueType }}: {{ commitMessageTitle }}", encoding="utf-8")
        ctx = {"issueType": "chore", "commitMessageTitle": "minor update"}
        with patch(f"{_MOD}._derive_issue_link_from_key", side_effect=AssertionError("should not be called")):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "chore: minor update"

    def test_explicit_context_augmentation_when_derivation_returns_none(self, tmp_path):
        """When derive returns None, issueLink stays absent; hard-required guard may then fail."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        # Template that references issueLink (hard-required when referenced).
        template_file.write_text(
            "{{ issueType }}([#{{ issueKey }}]({{ issueLink }})): {{ commitMessageTitle }}",
            encoding="utf-8",
        )
        ctx = {"issueType": "fix", "issueKey": "42", "commitMessageTitle": "t"}
        with patch(f"{_MOD}._derive_issue_link_from_key", return_value=None):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        # issueLink unreachable → hard-required guard fires → None returned
        assert result is None

    def test_empty_issue_link_triggers_derivation(self, tmp_path):
        """Empty issueLink in explicit context is treated as absent; derivation runs."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text(
            "{{ issueType }}({{ issueKey }}): {{ commitMessageTitle }}\n\n[{{ issueKey }}]({{ issueLink }})",
            encoding="utf-8",
        )
        ctx = {
            "issueType": "feat",
            "issueKey": "PROJECT-1234",
            "commitMessageTitle": "add thing",
            "issueLink": "",  # blank — should be treated as missing
        }
        derived = "https://jira.example.com/browse/PROJECT-1234"
        with patch(f"{_MOD}._derive_issue_link_from_key", return_value=derived):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "feat(PROJECT-1234): add thing\n\n[PROJECT-1234](https://jira.example.com/browse/PROJECT-1234)"

    def test_whitespace_issue_link_triggers_derivation(self, tmp_path):
        """Whitespace-only issueLink in explicit context is treated as absent; derivation runs."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text(
            "{{ issueType }}({{ issueKey }}): {{ commitMessageTitle }}\n\n[{{ issueKey }}]({{ issueLink }})",
            encoding="utf-8",
        )
        ctx = {
            "issueType": "feat",
            "issueKey": "PROJECT-1234",
            "commitMessageTitle": "add thing",
            "issueLink": "   ",  # whitespace-only — should be treated as missing
        }
        derived = "https://jira.example.com/browse/PROJECT-1234"
        with patch(f"{_MOD}._derive_issue_link_from_key", return_value=derived):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        assert result == "feat(PROJECT-1234): add thing\n\n[PROJECT-1234](https://jira.example.com/browse/PROJECT-1234)"

    def test_empty_issue_link_derivation_fails_hard_required_guard_fires(self, tmp_path):
        """Empty issueLink with failed derivation triggers hard-required guard → None returned."""
        template_file = tmp_path / TEMPLATE_PATH
        template_file.parent.mkdir(parents=True)
        template_file.write_text(
            "{{ issueType }}([{{ issueKey }}]({{ issueLink }})): {{ commitMessageTitle }}",
            encoding="utf-8",
        )
        ctx = {
            "issueType": "fix",
            "issueKey": "PROJECT-99",
            "commitMessageTitle": "fix thing",
            "issueLink": "",  # blank — derivation runs but returns None
        }
        with patch(f"{_MOD}._derive_issue_link_from_key", return_value=None):
            result = resolve_commit_message_from_template(tmp_path, context=ctx)
        # issueLink stripped, derivation returns None → hard-required guard fires → None
        assert result is None
