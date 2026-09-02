"""
Tests for prompt template loader.
"""

import pytest

from agentic_devtools.prompts import loader


class TestLoadAndRenderPrompt:
    """Tests for load_and_render_prompt function."""

    def test_load_and_render_full_workflow(self, temp_prompts_dir, temp_output_dir):
        """Test full load and render workflow."""
        template_content = "Hello {{name}}, working on {{task}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        template_file = workflow_dir / "default-initiate-prompt.md"
        template_file.write_text(template_content, encoding="utf-8")

        context = {"name": "Alice", "task": "PROJECT-1234"}
        result = loader.load_and_render_prompt("test", "initiate", context)

        assert result == "Hello Alice, working on PROJECT-1234"

    def test_load_and_render_with_override(self, temp_prompts_dir, temp_output_dir):
        """Test load and render with override template."""
        default_content = "Default {{name}}"
        override_content = "Custom: {{name}}"

        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()

        default_file = workflow_dir / "default-initiate-prompt.md"
        default_file.write_text(default_content, encoding="utf-8")

        # Override filename has no prefix (no 'default-')
        override_file = workflow_dir / "initiate-prompt.md"
        override_file.write_text(override_content, encoding="utf-8")

        context = {"name": "Bob"}
        result = loader.load_and_render_prompt("test", "initiate", context)

        assert result == "Custom: Bob"

    def test_load_and_render_validates_override(self, temp_prompts_dir, temp_output_dir):
        """Test that override is validated against default."""
        default_content = "{{name}}"
        override_content = "{{name}} {{extra}}"

        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()

        default_file = workflow_dir / "default-initiate-prompt.md"
        default_file.write_text(default_content, encoding="utf-8")

        # Override filename has no prefix (no 'default-')
        override_file = workflow_dir / "initiate-prompt.md"
        override_file.write_text(override_content, encoding="utf-8")

        with pytest.raises(loader.TemplateValidationError):
            loader.load_and_render_prompt("test", "initiate", {"name": "Test"})

    def test_warns_on_missing_template_variables(self, temp_prompts_dir, temp_output_dir, capsys):
        """Missing template variables produce a warning on stderr."""
        template_content = "Hello {{name}}, working on {{task}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        (workflow_dir / "default-initiate-prompt.md").write_text(template_content, encoding="utf-8")

        # Provide only one of the two declared variables
        loader.load_and_render_prompt("test", "initiate", {"name": "Alice"})

        captured = capsys.readouterr()
        assert "WARNING" in captured.err
        assert "task" in captured.err
        assert "test/initiate" in captured.err

    def test_no_warning_when_all_variables_provided(self, temp_prompts_dir, temp_output_dir, capsys):
        """No warning is printed when all template variables are provided."""
        template_content = "Hello {{name}}, working on {{task}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        (workflow_dir / "default-initiate-prompt.md").write_text(template_content, encoding="utf-8")

        loader.load_and_render_prompt("test", "initiate", {"name": "Alice", "task": "T1"})

        captured = capsys.readouterr()
        assert "WARNING" not in captured.err

    def test_no_warning_when_warn_on_missing_false(self, temp_prompts_dir, temp_output_dir, capsys):
        """No warning is printed when warn_on_missing=False even with missing variables."""
        template_content = "Hello {{name}}, working on {{task}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        (workflow_dir / "default-initiate-prompt.md").write_text(template_content, encoding="utf-8")

        loader.load_and_render_prompt("test", "initiate", {"name": "Alice"}, warn_on_missing=False)

        captured = capsys.readouterr()
        assert "WARNING" not in captured.err

    def test_save_to_temp_false_skips_file_creation(self, temp_prompts_dir, temp_output_dir):
        """No file is created when save_to_temp=False."""
        template_content = "Hello {{name}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        (workflow_dir / "default-initiate-prompt.md").write_text(template_content, encoding="utf-8")

        result = loader.load_and_render_prompt(
            "test", "initiate", {"name": "Alice"}, save_to_temp=False, log_output=False
        )

        assert result == "Hello Alice"
        # No file should be created in temp dir
        expected_file = temp_output_dir / "temp-test-initiate-prompt.md"
        assert not expected_file.exists()

    def test_log_output_false_suppresses_console(self, temp_prompts_dir, temp_output_dir, capsys):
        """Console output is suppressed when log_output=False."""
        template_content = "Hello {{name}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        (workflow_dir / "default-initiate-prompt.md").write_text(template_content, encoding="utf-8")

        result = loader.load_and_render_prompt("test", "initiate", {"name": "Alice"}, log_output=False)

        assert result == "Hello Alice"
        captured = capsys.readouterr()
        # Should not contain the workflow header that log_prompt_with_save_notice produces
        assert "WORKFLOW:" not in captured.out

    def test_save_to_temp_false_log_output_true_no_save_notice(self, temp_prompts_dir, temp_output_dir, capsys):
        """When save_to_temp=False and log_output=True, header prints but no 'saved to' notice."""
        template_content = "Hello {{name}}"
        workflow_dir = temp_prompts_dir / "test"
        workflow_dir.mkdir()
        (workflow_dir / "default-initiate-prompt.md").write_text(template_content, encoding="utf-8")

        result = loader.load_and_render_prompt(
            "test", "initiate", {"name": "Alice"}, save_to_temp=False, log_output=True
        )

        assert result == "Hello Alice"
        captured = capsys.readouterr()
        # Workflow header should still be present
        assert "WORKFLOW:" in captured.out
        # No file was saved, so the save notice must not appear
        assert "also saved to" not in captured.out
