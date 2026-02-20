import base64
import pathlib
from typing import Any, Dict, List, Optional

from abstra_internals.entities.agents.prompt_builder import (
    AgentPromptBuilder,
    ReActStep,
    process_markdown_images,
)
from abstra_internals.entities.agents.react_executor import ReActExecutor
from abstra_internals.entities.agents.tools.dispatcher import (
    FinishHandler,
    ToolDispatcher,
)

# Minimal 1x1 red pixel PNG
_TINY_PNG_B64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg=="
_TINY_PNG_BYTES = base64.b64decode(_TINY_PNG_B64)


def _md_img(alt="img", ext="png", b64=_TINY_PNG_B64):
    """Build a markdown inline base64 image."""
    return f"![{alt}](data:image/{ext};base64,{b64})"


def _is_image_path(part) -> bool:
    """Check if a prompt part is an image file path (pathlib.Path) that exists."""
    return isinstance(part, pathlib.Path) and part.is_file()


class FakeTool:
    def __init__(self, name: str, result: str = "ok"):
        self._name = name
        self._result = result

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"Fake tool: {self._name}"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"query": {"type": "string"}}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        return self._result


class MockAiSDK:
    """Mock AI SDK that returns a scripted sequence of responses."""

    def __init__(self, responses: List[Dict[str, Any]]) -> None:
        self._responses = iter(responses)

    def prompt(
        self,
        prompts: list,
        instructions: list,
        format: Optional[dict] = None,
        temperature: float = 1.0,
    ) -> dict:
        return next(self._responses)


class TestReActExecutor:
    def test_finish_on_first_step(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "I already know the answer.",
                    "action": "finish",
                    "action_input": {"answer": "The result is 42."},
                }
            ]
        )
        dispatcher = ToolDispatcher([FinishHandler()])
        executor = ReActExecutor(ai_sdk=ai_sdk, tool_dispatcher=dispatcher)

        result = executor.execute("What is 6*7?", permissions=[])

        assert result.success is True
        assert result.output == "The result is 42."
        assert result.error is None

    def test_multi_step_then_finish(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "I need to look up data.",
                    "action": "lookup",
                    "action_input": {"query": "users"},
                },
                {
                    "thought": "Now I need to process it.",
                    "action": "process",
                    "action_input": {"query": "filter active"},
                },
                {
                    "thought": "I have the answer now.",
                    "action": "finish",
                    "action_input": {"answer": "Found 5 active users."},
                },
            ]
        )
        dispatcher = ToolDispatcher(
            [
                FakeTool("lookup", '[{"name": "Alice"}, {"name": "Bob"}]'),
                FakeTool("process", "Processed 2 results"),
                FinishHandler(),
            ]
        )
        executor = ReActExecutor(ai_sdk=ai_sdk, tool_dispatcher=dispatcher)

        result = executor.execute("Find active users", permissions=[])

        assert result.success is True
        assert result.output == "Found 5 active users."

    def test_max_steps_reached(self):
        # LLM always wants to look up more data, never finishes
        responses = [
            {
                "thought": f"Step {i}",
                "action": "lookup",
                "action_input": {"query": f"query_{i}"},
            }
            for i in range(10)
        ]
        ai_sdk = MockAiSDK(responses)
        dispatcher = ToolDispatcher([FakeTool("lookup"), FinishHandler()])
        executor = ReActExecutor(ai_sdk=ai_sdk, tool_dispatcher=dispatcher, max_steps=5)

        result = executor.execute("Infinite task", permissions=[])

        assert result.success is False
        assert "maximum number of steps" in result.error.lower()

    def test_tool_error_continues_loop(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Try the broken tool.",
                    "action": "broken",
                    "action_input": {},
                },
                {
                    "thought": "That failed, let me finish.",
                    "action": "finish",
                    "action_input": {"answer": "Recovered from error."},
                },
            ]
        )

        class BrokenTool:
            @property
            def name(self):
                return "broken"

            @property
            def description(self):
                return "Always fails"

            @property
            def input_schema(self):
                return {"type": "object"}

            def execute(self, action_input):
                raise RuntimeError("Broken!")

        dispatcher = ToolDispatcher([BrokenTool(), FinishHandler()])
        executor = ReActExecutor(ai_sdk=ai_sdk, tool_dispatcher=dispatcher)

        result = executor.execute("Test recovery", permissions=[])

        assert result.success is True
        assert result.output == "Recovered from error."

    def test_unknown_action_produces_error_observation(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Use a tool that doesn't exist.",
                    "action": "nonexistent",
                    "action_input": {},
                },
                {
                    "thought": "OK that didn't work, finish.",
                    "action": "finish",
                    "action_input": {"answer": "Done."},
                },
            ]
        )
        dispatcher = ToolDispatcher([FinishHandler()])
        executor = ReActExecutor(ai_sdk=ai_sdk, tool_dispatcher=dispatcher)

        result = executor.execute("Test", permissions=[])

        assert result.success is True
        assert result.output == "Done."

    def test_ai_sdk_exception_is_caught(self):
        class FailingAiSDK:
            def prompt(self, **kwargs):
                raise ConnectionError("API unavailable")

        dispatcher = ToolDispatcher([FinishHandler()])
        executor = ReActExecutor(ai_sdk=FailingAiSDK(), tool_dispatcher=dispatcher)

        result = executor.execute("Test", permissions=[])

        assert result.success is False
        assert "error" in result.error.lower()

    def test_malformed_action_input_handled(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Test.",
                    "action": "finish",
                    "action_input": "not a dict",  # malformed
                },
            ]
        )
        dispatcher = ToolDispatcher([FinishHandler()])
        executor = ReActExecutor(ai_sdk=ai_sdk, tool_dispatcher=dispatcher)

        result = executor.execute("Test", permissions=[])
        # Should not crash — action_input gets normalized to {}
        assert result.success is True


class TestAgentPromptBuilder:
    def test_build_system_prompt(self):
        builder = AgentPromptBuilder()
        prompt = builder.build_system_prompt("- **greet**: Says hello\n  Input: {}")
        assert "greet" in prompt
        assert "Available Tools" in prompt

    def test_build_step_prompt_no_history(self):
        builder = AgentPromptBuilder()
        parts = builder.build_step_prompt("Process this task.", [])
        prompt = "\n".join(parts)
        assert "Process this task." in prompt
        assert "first action" in prompt.lower()

    def test_build_step_prompt_with_history(self):
        builder = AgentPromptBuilder()
        history = [
            ReActStep(
                step_number=1,
                thought="Need to lookup",
                action="lookup",
                action_input={"q": "test"},
                observation="Found 3 results",
            ),
        ]
        parts = builder.build_step_prompt("Task description.", history)
        prompt = "\n".join(parts)
        assert "Step 1" in prompt
        assert "Need to lookup" in prompt
        assert "Found 3 results" in prompt
        assert "next action" in prompt.lower()


class TestProcessMarkdownImages:
    def test_plain_text_returns_single_element(self):
        result = process_markdown_images("Hello world")
        assert result == ["Hello world"]

    def test_empty_string_returns_single_element(self):
        result = process_markdown_images("")
        assert result == [""]

    def test_single_image_between_text(self):
        md = f"Before {_md_img()} After"
        result = process_markdown_images(md)
        assert len(result) == 3
        assert result[0] == "Before"
        assert result[2] == "After"
        assert _is_image_path(result[1])
        assert result[1].suffix == ".png"

    def test_saved_file_contains_decoded_bytes(self):
        md = _md_img()
        result = process_markdown_images(md)
        assert len(result) == 1
        with open(result[0], "rb") as f:
            assert f.read() == _TINY_PNG_BYTES

    def test_image_only_no_surrounding_text(self):
        md = _md_img()
        result = process_markdown_images(md)
        assert len(result) == 1
        assert _is_image_path(result[0])

    def test_image_at_start(self):
        md = f"{_md_img()} some text after"
        result = process_markdown_images(md)
        assert len(result) == 2
        assert _is_image_path(result[0])
        assert result[1] == "some text after"

    def test_image_at_end(self):
        md = f"some text before {_md_img()}"
        result = process_markdown_images(md)
        assert len(result) == 2
        assert result[0] == "some text before"
        assert _is_image_path(result[1])

    def test_multiple_images(self):
        md = f"Start {_md_img('a')} middle {_md_img('b')} end"
        result = process_markdown_images(md)
        assert len(result) == 5
        assert result[0] == "Start"
        assert _is_image_path(result[1])
        assert result[2] == "middle"
        assert _is_image_path(result[3])
        assert result[4] == "end"

    def test_adjacent_images_no_text_between(self):
        md = f"{_md_img('a')}{_md_img('b')}"
        result = process_markdown_images(md)
        file_parts = [p for p in result if _is_image_path(p)]
        assert len(file_parts) == 2

    def test_temp_file_prefix(self):
        md = _md_img()
        result = process_markdown_images(md)
        assert result[0].name.startswith("agent_img_")

    def test_jpeg_extension(self):
        md = f"![photo](data:image/jpeg;base64,{_TINY_PNG_B64})"
        result = process_markdown_images(md)
        assert len(result) == 1
        assert result[0].suffix == ".jpeg"

    def test_webp_extension(self):
        md = f"![photo](data:image/webp;base64,{_TINY_PNG_B64})"
        result = process_markdown_images(md)
        assert len(result) == 1
        assert result[0].suffix == ".webp"


class TestBuildStepPromptWithImages:
    """Tests that build_step_prompt correctly handles image file paths.

    The prompt SDK (AiSDKController._make_messages) distinguishes text from
    images by checking pathlib.Path(s).exists(). If build_step_prompt corrupts
    a file path (e.g. by prepending '## Task\\n\\n' or appending history text),
    the path won't resolve and the image is silently lost.
    """

    def test_text_image_text(self):
        """Normal case: text before and after image."""
        builder = AgentPromptBuilder()
        md = f"Describe this: {_md_img()} and summarize"
        parts = builder.build_step_prompt(md, [])

        assert parts[0].startswith("## Task")
        assert "Describe this:" in parts[0]

        image_parts = [p for p in parts if _is_image_path(p)]
        assert len(image_parts) == 1

    def test_image_at_start_not_corrupted(self):
        """When template starts with an image, the file path must remain valid."""
        builder = AgentPromptBuilder()
        md = f"{_md_img()} describe this image"
        parts = builder.build_step_prompt(md, [])

        image_parts = [p for p in parts if _is_image_path(p)]
        assert len(image_parts) == 1, (
            f"Image file path was corrupted by build_step_prompt. Parts: {parts}"
        )

    def test_image_at_end_not_corrupted(self):
        """When template ends with an image, the file path must remain valid."""
        builder = AgentPromptBuilder()
        md = f"Analyze this: {_md_img()}"
        parts = builder.build_step_prompt(md, [])

        image_parts = [p for p in parts if _is_image_path(p)]
        assert len(image_parts) == 1, (
            f"Image file path was corrupted by build_step_prompt. Parts: {parts}"
        )

    def test_image_only_template_not_corrupted(self):
        """Template with only an image — path must survive both header and history."""
        builder = AgentPromptBuilder()
        md = _md_img()
        parts = builder.build_step_prompt(md, [])

        image_parts = [p for p in parts if _is_image_path(p)]
        assert len(image_parts) == 1, (
            f"Image file path was corrupted by build_step_prompt. Parts: {parts}"
        )

    def test_image_at_end_with_history_not_corrupted(self):
        """History text appended must not corrupt a trailing image path."""
        builder = AgentPromptBuilder()
        md = f"Look at: {_md_img()}"
        history = [
            ReActStep(
                step_number=1,
                thought="Trying to analyze",
                action="some_tool",
                action_input={},
                observation="Result here",
            ),
        ]
        parts = builder.build_step_prompt(md, history)

        image_parts = [p for p in parts if _is_image_path(p)]
        assert len(image_parts) == 1, (
            f"Image file path was corrupted by history append. Parts: {parts}"
        )

    def test_multiple_images_all_preserved(self):
        """Multiple images in template should all remain valid file paths."""
        builder = AgentPromptBuilder()
        md = f"First: {_md_img('a')} Second: {_md_img('b')}"
        parts = builder.build_step_prompt(md, [])

        image_parts = [p for p in parts if _is_image_path(p)]
        assert len(image_parts) == 2, (
            f"Expected 2 image files, got {len(image_parts)}. Parts: {parts}"
        )

    def test_header_present_when_image_at_start(self):
        """Even with an image first, '## Task' header must appear somewhere."""
        builder = AgentPromptBuilder()
        md = f"{_md_img()} describe this"
        parts = builder.build_step_prompt(md, [])

        full_text = " ".join(p for p in parts if not _is_image_path(p))
        assert "## Task" in full_text

    def test_history_present_when_image_at_end(self):
        """Even with an image last, history/action prompt must appear somewhere."""
        builder = AgentPromptBuilder()
        md = f"Analyze: {_md_img()}"
        parts = builder.build_step_prompt(md, [])

        full_text = " ".join(p for p in parts if not _is_image_path(p))
        assert "first action" in full_text.lower()
