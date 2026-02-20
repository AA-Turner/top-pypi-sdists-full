import pathlib
import tempfile

from abstra_internals.entities.agents.lua.prompt_builder import (
    LuaPromptBuilder,
    LuaStep,
)


class TestLuaPromptBuilder:
    def test_build_system_prompt(self):
        builder = LuaPromptBuilder()
        prompt = builder.build_system_prompt("- **greet**: Says hello\n  Input: {}")
        assert "greet" in prompt
        assert "Available Functions" in prompt
        assert "execute" in prompt
        assert "finish_success" in prompt

    def test_build_step_prompt_no_history(self):
        builder = LuaPromptBuilder()
        parts = builder.build_step_prompt("Process this task.", [])
        prompt = "\n".join(str(p) for p in parts)
        assert "Process this task." in prompt
        assert "first" in prompt.lower()

    def test_build_step_prompt_with_history(self):
        builder = LuaPromptBuilder()
        history = [
            LuaStep(
                step_number=1,
                thought="Need to lookup",
                action="execute",
                code="local r = lookup()\nprint(r)",
                output="Found 3 results",
            ),
        ]
        parts = builder.build_step_prompt("Task description.", history)
        prompt = "\n".join(str(p) for p in parts)
        assert "Step 1" in prompt
        assert "Need to lookup" in prompt
        assert "Found 3 results" in prompt
        assert "lua" in prompt.lower()

    def test_build_step_prompt_with_finish(self):
        builder = LuaPromptBuilder()
        history = [
            LuaStep(
                step_number=1,
                thought="Done.",
                action="finish_success",
                code="Task completed.",
            ),
        ]
        parts = builder.build_step_prompt("Task description.", history)
        prompt = "\n".join(str(p) for p in parts)
        assert "finish_success" in prompt
        assert "Task completed." in prompt

    def test_build_step_prompt_with_screenshot(self):
        """Screenshot Paths are interleaved in the output list."""
        # Create a real temp file to act as screenshot
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.write(b"fake jpeg")
        tmp.close()
        screenshot_path = pathlib.Path(tmp.name)

        builder = LuaPromptBuilder()
        history = [
            LuaStep(
                step_number=1,
                thought="Navigated.",
                action="execute",
                code='navigate({url = "https://example.com"})',
                output="Page loaded.",
                screenshot=screenshot_path,
            ),
        ]
        parts = builder.build_step_prompt("Do the task.", history)

        # Should contain at least one Path element
        path_parts = [p for p in parts if isinstance(p, pathlib.Path)]
        assert len(path_parts) == 1
        assert path_parts[0] == screenshot_path

        # Text parts should still contain step info
        text = "\n".join(str(p) for p in parts if isinstance(p, str))
        assert "Step 1" in text
        assert "Page loaded." in text

        # Cleanup
        screenshot_path.unlink(missing_ok=True)

    def test_build_step_prompt_no_screenshot_when_none(self):
        """Steps without screenshots don't include Paths."""
        builder = LuaPromptBuilder()
        history = [
            LuaStep(
                step_number=1,
                thought="Did stuff.",
                action="execute",
                code='print("hi")',
                output="hi",
                screenshot=None,
            ),
        ]
        parts = builder.build_step_prompt("Task.", history)
        path_parts = [p for p in parts if isinstance(p, pathlib.Path)]
        assert len(path_parts) == 0
