"""Tests for pull-request-review consolidate-and-submit prompt template rendering."""

from agentic_devtools.prompts import loader


class TestPrReviewConsolidateAndSubmitPromptRendering:
    """Tests for default-consolidate-and-submit-prompt.md in the pull-request-review workflow."""

    def _render(self, **kwargs):
        """Render the actual PR review consolidate-and-submit template."""
        template = loader.load_prompt_template("pull-request-review", "consolidate-and-submit")
        return loader.substitute_variables(template, kwargs)

    def _base_variables(self):
        return {"pull_request_id": "42"}

    def test_renders_without_error(self):
        """Template renders without exceptions with the base variable."""
        result = self._render(**self._base_variables())
        assert result is not None
        assert len(result) > 0

    def test_pull_request_id_rendered(self):
        """Pull request ID appears in the prompt."""
        result = self._render(**self._base_variables())
        assert "#42" in result

    def test_refresh_command_present(self):
        """The live refresh command is referenced."""
        result = self._render(**self._base_variables())
        assert "agdt-pr-review-refresh-comment --pr 42" in result
        assert "--pull-request-id" not in result

    def test_submit_command_present(self):
        """The terminal submit command is referenced."""
        result = self._render(**self._base_variables())
        assert "agdt-pr-review-submit --pr 42" in result

    def test_next_action_points_to_decision(self):
        """Next Action advances to the decision step."""
        result = self._render(**self._base_variables())
        assert "agdt-advance-workflow decision" in result

    def test_instructions_file_reference_present(self):
        """Instructions file reference appears at the end of the rendered output."""
        result = self._render(**self._base_variables())
        assert "temp-pull-request-review-consolidate-and-submit-prompt.md" in result
