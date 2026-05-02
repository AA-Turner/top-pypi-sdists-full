"""Tests for SAGE UX orchestration improvements.

Tests verify:
- Clean mode is the default (minimal noise)
- Verbose mode shows all output including thinking
- File discovery provides actual project files
- Thinking blocks are filtered by default
"""

import pytest

from sage.core import renderer
from sage.core.list_generator import extract_list_item_count


class TestOutputModeControl:
    """Test renderer output mode control."""

    def teardown_method(self):
        """Reset output mode after each test."""
        renderer.set_output_mode("clean")

    def test_default_mode_is_clean(self):
        """Default output mode should be 'clean' (minimal noise)."""
        renderer.set_output_mode("clean")  # Reset to default
        assert renderer.get_output_mode() == "clean"
        assert renderer.is_clean() is True
        assert renderer.suppress_thinking() is True
        assert renderer.suppress_phases() is True

    def test_set_verbose_mode(self):
        """Verbose mode should show everything including thinking."""
        renderer.set_output_mode("verbose")
        assert renderer.get_output_mode() == "verbose"
        assert renderer.is_verbose() is True
        assert renderer.suppress_thinking() is False  # Shows thinking in verbose
        assert renderer.suppress_phases() is False

    def test_set_normal_mode(self):
        """Normal mode shows progress but suppresses thinking."""
        renderer.set_output_mode("normal")
        assert renderer.get_output_mode() == "normal"
        assert renderer.is_verbose() is False
        assert renderer.is_clean() is False
        assert renderer.suppress_thinking() is True  # Still suppresses thinking
        assert renderer.suppress_phases() is False

    def test_invalid_mode_raises_error(self):
        """Setting invalid mode should raise ValueError."""
        with pytest.raises(ValueError):
            renderer.set_output_mode("invalid_mode")

    def test_legacy_is_quiet_maps_to_clean(self):
        """Legacy is_quiet() should map to clean mode."""
        renderer.set_output_mode("clean")
        assert renderer.is_quiet() is True
        renderer.set_output_mode("verbose")
        assert renderer.is_quiet() is False

    def test_legacy_is_minimal_maps_to_clean_or_normal(self):
        """Legacy is_minimal() should be True for clean/normal modes."""
        renderer.set_output_mode("clean")
        assert renderer.is_minimal() is True
        renderer.set_output_mode("normal")
        assert renderer.is_minimal() is True
        renderer.set_output_mode("verbose")
        assert renderer.is_minimal() is False


class TestFileDiscovery:
    """Test file discovery for analysis tasks."""

    def test_get_project_file_listing_with_files(self, tmp_path):
        """File listing should return actual project files."""
        # Create some test files
        (tmp_path / "main.py").write_text("print('hello')")
        (tmp_path / "test_main.py").write_text("def test(): pass")
        (tmp_path / "config.json").write_text("{}")
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "utils.py").write_text("def util(): pass")

        # Import the function (it's module-private, so we test via main)
        import sage.main as main_module

        listing = main_module._get_project_file_listing(tmp_path)

        assert "main.py" in listing
        assert "test_main.py" in listing
        assert "src/utils.py" in listing or "src\\utils.py" in listing

    def test_get_project_file_listing_skips_hidden(self, tmp_path):
        """File listing should skip hidden directories."""
        (tmp_path / ".git").mkdir()
        (tmp_path / ".git" / "config").write_text("git config")
        (tmp_path / "visible.py").write_text("code")

        import sage.main as main_module

        listing = main_module._get_project_file_listing(tmp_path)

        assert ".git" not in listing
        assert "visible.py" in listing

    def test_get_project_file_listing_skips_node_modules(self, tmp_path):
        """File listing should skip node_modules."""
        (tmp_path / "node_modules").mkdir()
        (tmp_path / "node_modules" / "package.js").write_text("module")
        (tmp_path / "app.js").write_text("app code")

        import sage.main as main_module

        listing = main_module._get_project_file_listing(tmp_path)

        assert "node_modules" not in listing
        assert "app.js" in listing

    def test_get_project_file_listing_empty_project(self, tmp_path):
        """File listing for empty project should return empty string."""
        import sage.main as main_module

        listing = main_module._get_project_file_listing(tmp_path)
        assert listing == ""


class TestListExtractionIntegration:
    """Test that list extraction is consistent across orchestration."""

    def test_100_item_list_counted_correctly(self):
        """A 100-item list should be counted as 100."""
        items = [f"{i}. Item number {i}" for i in range(1, 101)]
        text = "\n".join(items)
        assert extract_list_item_count(text) == 100

    def test_continuation_prompt_uses_correct_count(self):
        """Continuation prompt should use correct item count."""
        from dataclasses import dataclass

        from sage.core.request_classifier import RequestType

        @dataclass
        class MockClassification:
            request_type: RequestType = RequestType.LIST_GENERATION
            quantity_required: int = 100
            read_only: bool = True

        classification = MockClassification()

        # Response with 50 items
        items = [f"{i}. Item {i}" for i in range(1, 51)]
        response = "\n".join(items)

        import sage.main as main_module

        prompt = main_module._build_readonly_response_retry_prompt(
            response, classification, verified_files=set()
        )

        assert prompt is not None
        assert "50" in prompt  # Should reference 50 items already provided
        assert "51" in prompt  # Should continue from item 51

    def test_continuation_prompt_is_direct(self):
        """Continuation prompt should be direct, no meta-commentary request."""
        from dataclasses import dataclass

        from sage.core.request_classifier import RequestType

        @dataclass
        class MockClassification:
            request_type: RequestType = RequestType.LIST_GENERATION
            quantity_required: int = 100
            read_only: bool = True

        classification = MockClassification()
        items = [f"{i}. Item {i}" for i in range(1, 21)]
        response = "\n".join(items)

        import sage.main as main_module

        prompt = main_module._build_readonly_response_retry_prompt(
            response, classification, verified_files=set()
        )

        # Should be forceful and direct
        assert "CONTINUE" in prompt.upper() or "Start" in prompt
        assert "21." in prompt  # Should tell AI to start with item 21


class TestThinkingBlockFiltering:
    """Test that thinking blocks are properly filtered."""

    def test_thinking_suppressed_by_default(self):
        """Thinking should be suppressed in clean mode (default)."""
        renderer.set_output_mode("clean")
        assert renderer.suppress_thinking() is True

    def test_thinking_shown_in_verbose(self):
        """Thinking should be shown in verbose mode."""
        renderer.set_output_mode("verbose")
        assert renderer.suppress_thinking() is False

    def test_thinking_suppressed_in_normal(self):
        """Thinking should still be suppressed in normal mode."""
        renderer.set_output_mode("normal")
        assert renderer.suppress_thinking() is True

    def test_thinking_block_detected(self):
        """Thinking blocks should be detected in text."""
        text_with_thinking = """
<thinking>
This is internal reasoning that should be hidden.
</thinking>

Here is the actual response.
"""
        # The thinking block pattern should be recognized
        import re

        has_thinking = bool(re.search(r"<thinking>.*?</thinking>", text_with_thinking, re.DOTALL))
        assert has_thinking is True

    def test_thinking_not_in_clean_text(self):
        """Clean text should not have thinking markers."""
        clean_text = """
Here is a response without any thinking blocks.
1. First item
2. Second item
"""
        import re

        has_thinking = bool(re.search(r"<thinking>", clean_text))
        assert has_thinking is False


class TestDirectRendererThinkingSuppression:
    """Test non-stream renderer paths also suppress hidden thinking."""

    def teardown_method(self):
        """Reset output mode after each test."""
        renderer.set_output_mode("clean")

    def test_print_assistant_response_strips_thinking_blocks(self, monkeypatch):
        """Direct assistant output should hide thinking blocks outside verbose mode."""
        captured = []
        monkeypatch.setattr(
            renderer.console,
            "print",
            lambda *args, **kwargs: captured.append((args, kwargs)),
        )

        renderer.set_output_mode("clean")
        renderer.print_assistant_response("<thinking>secret</thinking>Visible reply")

        assert len(captured) == 2
        _, body = captured[0][0]
        assert body.plain == "Visible reply"

    def test_render_markdown_strips_thinking_blocks(self, monkeypatch):
        """Markdown rendering should filter hidden reasoning in non-stream paths too."""
        captured = []
        monkeypatch.setattr(
            renderer.console,
            "print",
            lambda *args, **kwargs: captured.append((args, kwargs)),
        )
        monkeypatch.setattr(renderer, "Markdown", lambda text: ("markdown", text))

        renderer.set_output_mode("clean")
        renderer.render_markdown("<thinking>secret</thinking>\n# Visible heading")

        assert captured == [((("markdown", "# Visible heading"),), {})]

    def test_print_assistant_response_skips_thinking_only_payloads(self, monkeypatch):
        """Thinking-only payloads should not render an empty prompt line."""
        captured = []
        monkeypatch.setattr(
            renderer.console,
            "print",
            lambda *args, **kwargs: captured.append((args, kwargs)),
        )

        renderer.set_output_mode("clean")
        renderer.print_assistant_response("<thinking>secret</thinking>")

        assert captured == []


class TestBottomDockLayout:
    """Test the bottom-anchored Claude Code-style dock layout."""

    def test_bottom_dock_snapshot_renders_active_plan(self):
        """Snapshot should include the active plan, status, and bottom prompt hint."""
        snapshot = renderer.render_bottom_dock_snapshot(
            todos=[
                {"content": "Inspect relevant files", "status": "completed"},
                {"content": "Edit code and tests", "status": "in_progress"},
                {"content": "Run validation", "status": "pending"},
            ],
            status_message="Editing code and tests...",
            prompt_message="Working...",
            width=80,
        )

        assert "Current Plan" in snapshot
        assert "Edit code and tests" in snapshot
        assert "Run validation" in snapshot
        assert "Ctrl+C to interrupt" in snapshot
        assert "Editing code and tests..." in snapshot

    def test_bottom_dock_snapshot_is_empty_when_done(self):
        """No todos and no status should collapse the dock entirely."""
        snapshot = renderer.render_bottom_dock_snapshot(
            todos=[],
            status_message="",
            prompt_message="",
            width=80,
        )

        assert snapshot == ""


class TestCliTaskDockState:
    """Test task-stage helpers that drive the live dock."""

    def test_build_cli_task_todos_for_implementation(self):
        """Implementation requests should get inspect/implement/validate stages."""
        import sage.main as main_module

        todos = main_module._build_cli_task_todos(read_only=False)

        assert [todo["key"] for todo in todos] == ["inspect", "implement", "validate"]
        assert todos[0]["status"] == "in_progress"
        assert todos[1]["status"] == "pending"

    def test_build_cli_task_todos_for_analysis(self):
        """Read-only analysis requests should get evidence-focused stages."""
        import sage.main as main_module

        todos = main_module._build_cli_task_todos(read_only=True)

        assert [todo["key"] for todo in todos] == ["inspect", "verify", "respond"]
        assert todos[0]["content"] == "Inspect repository evidence"

    def test_set_cli_task_stage_advances_statuses(self):
        """Advancing the stage should complete prior items and activate the selected one."""
        import sage.main as main_module

        todos = main_module._build_cli_task_todos(read_only=False)
        updated = main_module._set_cli_task_stage(todos, "validate")

        assert updated[0]["status"] == "completed"
        assert updated[1]["status"] == "completed"
        assert updated[2]["status"] == "in_progress"
