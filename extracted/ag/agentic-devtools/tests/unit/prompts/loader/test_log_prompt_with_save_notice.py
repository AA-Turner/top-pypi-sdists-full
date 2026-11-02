"""
Tests for prompt template loader.
"""

from agentic_devtools.prompts import loader


class TestLogPromptWithSaveNotice:
    """Tests for log_prompt_with_save_notice function."""

    def test_log_outputs_prompt_content(self, capsys, temp_output_dir):
        """Test that log outputs the prompt content."""
        prompt_content = "# Prompt\n\nContent here"
        loader.log_prompt_with_save_notice("test", "step", prompt_content)

        captured = capsys.readouterr()
        assert "# Prompt" in captured.out
        assert "Content here" in captured.out

    def test_log_includes_save_path(self, capsys, temp_output_dir):
        """Test that log includes where prompt was saved when a path is provided."""
        saved = temp_output_dir / "temp-test-step-prompt.md"
        loader.log_prompt_with_save_notice("test", "step", "content", saved_path=saved)

        captured = capsys.readouterr()
        assert "temp-test-step-prompt.md" in captured.out

    def test_log_no_save_notice_when_path_omitted(self, capsys, temp_output_dir):
        """Test that no save notice is printed when saved_path is None."""
        loader.log_prompt_with_save_notice("test", "step", "content")

        captured = capsys.readouterr()
        assert "WORKFLOW: test" in captured.out
        assert "also saved to" not in captured.out
