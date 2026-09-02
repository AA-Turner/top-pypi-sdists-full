"""Tests for PR review pr-synthesis prompt rendering with repo_review_focus_areas."""

from agentic_devtools.prompts import loader


class TestPrReviewPrSynthesisPromptRendering:
    """Tests for the default-pr-synthesis-prompt.md template in pull-request-review workflow."""

    def _render(self, **kwargs):
        """Render the actual PR review pr-synthesis template with the given variables."""
        template = loader.load_prompt_template("pull-request-review", "pr-synthesis")
        return loader.substitute_variables(template, kwargs)

    def _base_variables(self):
        return {
            "pull_request_id": "42",
            "pr_title": "feat: add feature",
            "pr_author": "Alice",
            "source_branch": "feature/test",
            "target_branch": "main",
            "jira_issue_key": "",
            "file_count": "3",
            "repo_review_focus_areas": "",
            "pr_url": "https://dev.azure.com/example-org/ExampleProject/_git/example-repo-name/pullrequest/42",
            "source_code_platform": "AzureDevOps",
        }

    def test_renders_without_focus_areas(self):
        """Focus areas section is absent when repo_review_focus_areas is empty."""
        result = self._render(**self._base_variables())

        assert "Repo-Specific Review Focus Areas" not in result

    def test_renders_with_focus_areas(self):
        """Focus areas section appears when repo_review_focus_areas has content."""
        variables = self._base_variables()
        variables["repo_review_focus_areas"] = "## .NET DI\n- Use constructor injection"
        result = self._render(**variables)

        assert "Repo-Specific Review Focus Areas" in result
        assert ".NET DI" in result
        assert "constructor injection" in result

    def test_focus_areas_section_omitted_when_none(self):
        """Focus areas section is omitted when variable is not provided (treated as falsy)."""
        variables = self._base_variables()
        del variables["repo_review_focus_areas"]
        result = self._render(**variables)

        assert "Repo-Specific Review Focus Areas" not in result

    def test_build_manifest_command_present(self):
        """The deterministic manifest + triage commands are referenced."""
        result = self._render(**self._base_variables())

        assert "agdt-pr-review-build-manifest --pr 42" in result
        assert "agdt-pr-review-triage --pr 42" in result
        assert "--pull-request-id" not in result

    def test_pr_context_authoring_referenced(self):
        """The orchestrator is told to author pr-context.md."""
        result = self._render(**self._base_variables())

        assert "pr-context.md" in result

    def test_review_criteria_present(self):
        """Review criteria are listed."""
        result = self._render(**self._base_variables())

        assert "Review Criteria" in result
        assert "security" in result

    def test_pr_details_rendered(self):
        """Core PR details are rendered in the output."""
        result = self._render(**self._base_variables())

        assert "42" in result
        assert "feat: add feature" in result
        assert "Alice" in result

    def test_jira_link_absent_when_no_issue_key(self):
        """Jira link is absent when jira_issue_key is empty."""
        result = self._render(**self._base_variables())

        assert "Jira Issue" not in result

    def test_jira_link_present_when_issue_key_provided(self):
        """Jira link appears when jira_issue_key is provided."""
        variables = self._base_variables()
        variables["jira_issue_key"] = "PROJECT-1234"
        result = self._render(**variables)

        assert "PROJECT-1234" in result

    def test_next_action_points_to_delegate(self):
        """Next Action instructs the agent to advance to the delegate step."""
        result = self._render(**self._base_variables())

        assert "agdt-advance-workflow delegate" in result

    def test_pr_url_rendered(self):
        """PR URL value appears in the rendered output."""
        result = self._render(**self._base_variables())

        assert "https://dev.azure.com/example-org/ExampleProject/_git/example-repo-name/pullrequest/42" in result

    def test_source_code_platform_rendered(self):
        """Source Code Hosting Platform field and value appear in the rendered output."""
        result = self._render(**self._base_variables())

        assert "Source Code Hosting Platform" in result
        assert "AzureDevOps" in result

    def test_instructions_file_reference_present(self):
        """Instructions file reference appears at the end of the rendered output."""
        result = self._render(**self._base_variables())

        assert "temp-pull-request-review-pr-synthesis-prompt.md" in result
