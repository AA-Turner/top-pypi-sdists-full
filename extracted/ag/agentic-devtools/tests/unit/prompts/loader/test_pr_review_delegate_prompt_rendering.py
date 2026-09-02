"""Tests for pull-request-review delegate prompt template rendering."""

from agentic_devtools.prompts import loader


class TestPrReviewDelegatePromptRendering:
    """Tests for the default-delegate-prompt.md template in pull-request-review workflow."""

    def _render(self, **kwargs):
        """Render the actual PR review delegate template with the given variables."""
        template = loader.load_prompt_template("pull-request-review", "delegate")
        return loader.substitute_variables(template, kwargs)

    def _base_variables(self):
        return {
            "pull_request_id": "42",
            "completed_count": "3",
            "pending_count": "2",
            "total_count": "5",
        }

    def test_renders_without_error(self):
        """Template renders without exceptions with all base variables."""
        result = self._render(**self._base_variables())
        assert result is not None
        assert len(result) > 0

    def test_pull_request_id_rendered(self):
        """Pull request ID appears in the PR header."""
        result = self._render(**self._base_variables())
        assert "Pull Request **#42**" in result

    def test_queue_progress_rendered(self):
        """Completed and pending counts appear in queue progress section."""
        result = self._render(**self._base_variables())
        assert "**Completed**: 3" in result
        assert "**Remaining**: 2" in result

    def test_single_path_no_strategy_menu(self):
        """The delegate step has a single path: no Strategy A/B menu remains."""
        result = self._render(**self._base_variables())
        assert "Strategy A" not in result
        assert "Strategy B" not in result

    def test_spawn_file_reviewer_referenced(self):
        """One file-reviewer per file is the only path."""
        result = self._render(**self._base_variables())
        assert "file-reviewer" in result

    def test_single_agent_cli_fallback_guidance_present(self):
        """Headless CLI sessions have direct file-review guidance."""
        result = self._render(**self._base_variables())
        mode_b_section = result.split("### Mode B:", 1)[1].split("## Cross-file synthesis", 1)[0]
        assert "Single-Agent" in result
        assert "headless" in result
        assert 'agdt-file-review-write --file-key <fileKey> --answer-file "<printed draft path>"' in mode_b_section
        assert (
            'agdt-pr-review-accept-answer --file-key <fileKey> --answer-file "<printed draft path>"' in mode_b_section
        )

    def test_single_agent_mode_scaffold_copy_instructed(self):
        """Mode B instructs the agent to copy the scaffold before filling it."""
        result = self._render(**self._base_variables())
        mode_b_section = result.split("### Mode B:", 1)[1].split("## Cross-file synthesis", 1)[0]
        assert "python -c" in mode_b_section
        assert "resolve_answers_dir" in mode_b_section
        assert "shutil.copy2" in mode_b_section
        assert "printed draft path" in mode_b_section
        assert "artifact_dir=$(" not in mode_b_section
        assert 'cp "$artifact_dir' not in mode_b_section
        assert "promptHash" in mode_b_section
        assert "attemptId" in mode_b_section

    def test_multi_agent_mode_accept_answer_required(self):
        """Mode A includes an agdt-pr-review-accept-answer step so VS Code reviews advance."""
        result = self._render(**self._base_variables())
        mode_a_section = result.split("### Mode A:", 1)[1].split("### Mode B:", 1)[0]
        assert (
            'agdt-pr-review-accept-answer --file-key <fileKey> --answer-file "<path-to-answer.json>"' in mode_a_section
        )

    def test_rubber_duck_resolution_referenced(self):
        """Deep files run rubber ducks via the resolve-ducks command."""
        result = self._render(**self._base_variables())
        assert "agdt-pr-review-resolve-ducks" in result

    def test_next_action_points_to_consolidate(self):
        """Next Action advances to consolidate-and-submit."""
        result = self._render(**self._base_variables())
        assert "agdt-advance-workflow consolidate-and-submit" in result

    def test_instructions_file_reference_present(self):
        """Instructions file reference appears at the end of the rendered output."""
        result = self._render(**self._base_variables())
        assert "temp-pull-request-review-delegate-prompt.md" in result
