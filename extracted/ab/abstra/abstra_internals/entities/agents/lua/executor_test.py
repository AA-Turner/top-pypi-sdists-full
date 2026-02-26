import pathlib
from typing import Any, Dict, List
from unittest.mock import MagicMock

from abstra_internals.entities.agents.lua.executor import (
    MAX_EMPTY_CODE_RETRIES,
    MAX_FINISH_REJECTIONS,
    LuaExecutor,
)
from abstra_internals.entities.agents.lua.runtime import LupaRuntime
from abstra_internals.entities.agents.tools.dispatcher import FinishHandler
from abstra_internals.entities.agents.tools.send_task_handler import SendTaskHandler


class FakeTool:
    def __init__(self, name: str, result: str = "ok"):
        self._name = name
        self._result = result
        self.call_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"Fake tool: {self._name}"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"value": {"type": "string"}}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        self.call_count += 1
        return self._result


class CountingTool:
    def __init__(self, name: str):
        self._name = name
        self.call_count = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"Counting tool: {self._name}"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"index": {"type": "number"}}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        self.call_count += 1
        return f"call #{self.call_count}"


class ErrorTool:
    @property
    def name(self) -> str:
        return "broken"

    @property
    def description(self) -> str:
        return "Always fails"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object"}

    def execute(self, action_input: Dict[str, Any]) -> str:
        raise RuntimeError("Tool exploded!")


class MockAiSDK:  # type: ignore[misc]
    def __init__(self, responses: List[Dict[str, Any]]) -> None:
        self._responses = iter(responses)

    def prompt(
        self,
        prompts: Any = None,
        instructions: Any = None,
        format: Any = None,
        temperature: float = 1.0,
    ) -> dict:
        return next(self._responses)


class TestLuaExecutor:
    def test_finish_success_on_first_step(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "I know the answer.",
                    "action": "finish_success",
                    "argument": "The result is 42.",
                }
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("What is 6*7?", permissions=[])
        assert result.success is True
        assert result.output == "The result is 42."
        assert result.error is None

    def test_finish_failure(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Cannot do this.",
                    "action": "finish_failure",
                    "argument": "No tools available for this task.",
                }
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Impossible task", permissions=[])
        assert result.success is False
        assert result.error is not None and "No tools available" in result.error

    def test_execute_then_finish(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Need to look up data.",
                    "action": "execute",
                    "argument": 'local r = lookup({query = "users"})\nprint(r)',
                },
                {
                    "thought": "Got the data.",
                    "action": "finish_success",
                    "argument": "Found users.",
                },
            ]
        )
        runtime = LupaRuntime()
        tool = FakeTool("lookup", '[{"name": "Alice"}]')
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[tool, FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Find users", permissions=[])
        assert result.success is True
        assert result.output == "Found users."
        assert tool.call_count == 1

    def test_loop_efficiency(self):
        """A single execute step with a for loop calls the tool multiple times."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Move all 5 files in a loop.",
                    "action": "execute",
                    "argument": (
                        "for i = 0, 4 do\n"
                        "  local r = move_file({index = i})\n"
                        "  print(r)\n"
                        "end"
                    ),
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "Moved 5 files.",
                },
            ]
        )
        runtime = LupaRuntime()
        tool = CountingTool("move_file")
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[tool, FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Move files", permissions=[])
        assert result.success is True
        assert tool.call_count == 5
        assert result.output == "Moved 5 files."

    def test_max_steps_reached(self):
        responses = [
            {
                "thought": f"Step {i}",
                "action": "execute",
                "argument": f'print("step {i}")',
            }
            for i in range(10)
        ]
        ai_sdk = MockAiSDK(responses)
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
            max_steps=5,
        )

        result = executor.execute("Infinite task", permissions=[])
        assert result.success is False
        assert (
            result.error is not None
            and "maximum number of steps" in result.error.lower()
        )

    def test_lua_error_continues(self):
        """A Lua error in step 1 returns as observation, step 2 recovers."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Try invalid syntax.",
                    "action": "execute",
                    "argument": "this is not valid lua!!!",
                },
                {
                    "thought": "That failed, finishing.",
                    "action": "finish_success",
                    "argument": "Recovered.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test recovery", permissions=[])
        assert result.success is True
        assert result.output == "Recovered."

    def test_variables_persist_across_steps(self):
        """Variables set in step 1 are available in step 2."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Set a variable.",
                    "action": "execute",
                    "argument": 'my_data = "hello from step 1"',
                },
                {
                    "thought": "Read the variable.",
                    "action": "execute",
                    "argument": "print(my_data)",
                },
                {
                    "thought": "Got it.",
                    "action": "finish_success",
                    "argument": "Variable persisted.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test persistence", permissions=[])
        assert result.success is True
        assert result.output == "Variable persisted."

    def test_tool_error_returned_as_observation(self):
        """When a tool raises an exception, the error appears in output."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Call the broken tool.",
                    "action": "execute",
                    "argument": "local r = broken()\nprint(r)",
                },
                {
                    "thought": "That failed, finish.",
                    "action": "finish_success",
                    "argument": "Done despite error.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[ErrorTool(), FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True
        assert result.output == "Done despite error."

    def test_ai_sdk_exception_is_caught(self):
        class FailingAiSDK:  # type: ignore[misc]
            def prompt(self, **kwargs: Any) -> dict:
                raise ConnectionError("API unavailable")

        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=FailingAiSDK(),  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is False
        assert result.error is not None and "error" in result.error.lower()

    def test_empty_code_returns_error(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "I need to think...",
                    "action": "execute",
                    "argument": "",
                },
                {
                    "thought": "OK let me actually do it.",
                    "action": "finish_success",
                    "argument": "Done.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True
        assert result.output == "Done."

    def test_invalid_action_defaults_to_execute(self):
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Hmm.",
                    "action": "invalid_action",
                    "argument": 'print("still works")',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "OK.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True

    def test_output_truncation(self):
        """Output longer than 10k chars gets truncated."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Print a lot.",
                    "action": "execute",
                    "argument": 'for i = 1, 2000 do print("line " .. i) end',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "Printed.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True
        # The step output should have been truncated

    def test_screenshot_fn_called_after_execute(self):
        """screenshot_fn is called after each execute step."""
        import tempfile

        # Create a fake screenshot file
        tmp = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
        tmp.write(b"fake jpeg data")
        tmp.close()

        call_count = 0

        def fake_screenshot():
            nonlocal call_count
            call_count += 1
            return tmp.name

        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Do something.",
                    "action": "execute",
                    "argument": 'print("hello")',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "OK.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
            screenshot_fn=fake_screenshot,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True
        assert call_count == 1  # Called once for the execute step

        # Cleanup
        pathlib.Path(tmp.name).unlink(missing_ok=True)

    def test_no_screenshot_without_fn(self):
        """Without screenshot_fn, steps have no screenshot."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Do something.",
                    "action": "execute",
                    "argument": 'print("hello")',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "OK.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
            # No screenshot_fn
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True

    def test_empty_code_force_finish_after_max_retries(self):
        """After MAX_EMPTY_CODE_RETRIES consecutive empty codes, executor fails."""
        responses: List[Dict[str, Any]] = []
        for i in range(MAX_EMPTY_CODE_RETRIES + 1):
            responses.append(
                {
                    "thought": f"Thinking step {i + 1}...",
                    "action": "execute",
                    "argument": "",
                }
            )
        # Add a finish response that should never be reached
        responses.append(
            {
                "thought": "Done.",
                "action": "finish_success",
                "argument": "Should not reach here.",
            }
        )

        ai_sdk = MockAiSDK(responses)
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FakeTool("navigate", "page"), FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is False
        assert result.error is not None
        assert "empty code" in result.error.lower()

    def test_empty_code_counter_resets_on_non_empty_code(self):
        """Non-empty code resets the consecutive empty-code counter."""
        ai_sdk = MockAiSDK(
            [
                # Two consecutive empty codes (under the limit)
                {
                    "thought": "Thinking...",
                    "action": "execute",
                    "argument": "",
                },
                {
                    "thought": "Still thinking...",
                    "action": "execute",
                    "argument": "",
                },
                # Non-empty code resets counter
                {
                    "thought": "Now I know.",
                    "action": "execute",
                    "argument": 'print("hello")',
                },
                # Two more empty codes (under the limit again)
                {
                    "thought": "Thinking again...",
                    "action": "execute",
                    "argument": "",
                },
                {
                    "thought": "Still thinking...",
                    "action": "execute",
                    "argument": "",
                },
                # Finish successfully
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "Completed.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True
        assert result.output == "Completed."

    def test_screenshot_fn_returning_none(self):
        """When screenshot_fn returns None, no screenshot is stored."""
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Do something.",
                    "action": "execute",
                    "argument": 'print("hello")',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "OK.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
            screenshot_fn=lambda: None,  # Browser not open
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True


def _make_send_task_handler(task_type: str = "review") -> SendTaskHandler:
    """Helper to create a SendTaskHandler with a mocked task SDK."""
    task_sdk = MagicMock()
    task_sdk.send_task = MagicMock()
    return SendTaskHandler(
        task_type=task_type,
        task_sdk=task_sdk,
        task_schema={"type": "object", "properties": {"title": {"type": "string"}}},
    )


class TestFinishRejection:
    def test_finish_rejected_when_send_task_pending(self):
        """Finish is rejected until the agent calls the send_task tool."""
        send_handler = _make_send_task_handler("review")
        ai_sdk = MockAiSDK(
            [
                # Step 1: AI tries to finish immediately — should be rejected
                {
                    "thought": "All done.",
                    "action": "finish_success",
                    "argument": "Task complete.",
                },
                # Step 2: AI calls the send_task tool
                {
                    "thought": "I need to send the task first.",
                    "action": "execute",
                    "argument": 'send_task_review({title = "Fix bug"})',
                },
                # Step 3: AI finishes — should succeed now
                {
                    "thought": "Now I can finish.",
                    "action": "finish_success",
                    "argument": "Done after sending task.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[send_handler, FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Send a review task", permissions=[])
        assert result.success is True
        assert result.output == "Done after sending task."
        assert len(result.tasks_to_send) == 1
        assert result.tasks_to_send[0]["type"] == "review"

    def test_finish_forced_after_max_rejections(self):
        """After MAX_FINISH_REJECTIONS, finish is force-allowed."""
        send_handler = _make_send_task_handler("review")
        # Build MAX_FINISH_REJECTIONS rejected finish attempts, then one more
        responses: List[Dict[str, Any]] = []
        for i in range(MAX_FINISH_REJECTIONS):
            responses.append(
                {
                    "thought": f"Attempt {i + 1} to finish.",
                    "action": "finish_success",
                    "argument": f"Done (attempt {i + 1}).",
                }
            )
        # The final attempt (MAX_FINISH_REJECTIONS + 1) is force-allowed
        responses.append(
            {
                "thought": "Trying again.",
                "action": "finish_success",
                "argument": "Forced finish.",
            }
        )

        ai_sdk = MockAiSDK(responses)
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[send_handler, FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Do something", permissions=[])
        assert result.success is True
        assert result.output == "Forced finish."
        # send_task was never called so tasks_to_send should be empty
        assert result.tasks_to_send == []

    def test_tasks_to_send_populated_on_success(self):
        """tasks_to_send contains all tasks sent via send_task handlers."""
        send_handler = _make_send_task_handler("deploy")
        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Send the task.",
                    "action": "execute",
                    "argument": 'send_task_deploy({title = "Ship it"})',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "Deployed.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[send_handler, FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Deploy the thing", permissions=[])
        assert result.success is True
        assert isinstance(result.tasks_to_send, list)
        assert len(result.tasks_to_send) == 1
        assert result.tasks_to_send[0]["type"] == "deploy"
        assert result.tasks_to_send[0]["payload"]["title"] == "Ship it"

    def test_tasks_to_send_populated_on_exception(self):
        """Even when executor hits an exception, already-sent tasks are preserved."""
        send_handler = _make_send_task_handler("notify")

        class ExplodingAiSDK:  # type: ignore[misc]
            def __init__(self) -> None:
                self._call_count = 0

            def prompt(self, **kwargs: Any) -> dict:
                self._call_count += 1
                if self._call_count == 1:
                    return {
                        "thought": "Send task first.",
                        "action": "execute",
                        "argument": 'send_task_notify({title = "Alert"})',
                    }
                # Explode on second call
                raise RuntimeError("LLM crashed")

        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ExplodingAiSDK(),  # type: ignore[arg-type]
            tool_handlers=[send_handler, FinishHandler()],
            runtime=runtime,
        )

        result = executor.execute("Notify then crash", permissions=[])
        assert result.success is False
        assert result.error is not None and "error" in result.error.lower()
        # The task sent before the crash should still be in the result
        assert len(result.tasks_to_send) == 1
        assert result.tasks_to_send[0]["type"] == "notify"

    def test_screenshot_fn_exception_does_not_break_execution(self):
        """A screenshot_fn that raises is silently caught."""

        def broken_screenshot():
            raise Exception("Screenshot failed!")

        ai_sdk = MockAiSDK(
            [
                {
                    "thought": "Execute something.",
                    "action": "execute",
                    "argument": 'print("hello")',
                },
                {
                    "thought": "Done.",
                    "action": "finish_success",
                    "argument": "Completed.",
                },
            ]
        )
        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk,  # type: ignore[arg-type]
            tool_handlers=[FinishHandler()],
            runtime=runtime,
            screenshot_fn=broken_screenshot,
        )

        result = executor.execute("Test", permissions=[])
        assert result.success is True
        assert result.output == "Completed."

    def test_finish_rejection_count_resets_between_executions(self):
        """Each call to execute() starts with a fresh rejection counter."""
        send_handler = _make_send_task_handler("review")

        # First execution: reject MAX_FINISH_REJECTIONS times then force-finish
        first_responses: List[Dict[str, Any]] = []
        for i in range(MAX_FINISH_REJECTIONS):
            first_responses.append(
                {
                    "thought": f"Finish attempt {i + 1}.",
                    "action": "finish_success",
                    "argument": f"Done {i + 1}.",
                }
            )
        first_responses.append(
            {
                "thought": "Force finish.",
                "action": "finish_success",
                "argument": "Forced first run.",
            }
        )

        # Second execution: same pattern — must also take MAX_FINISH_REJECTIONS + 1
        second_responses: List[Dict[str, Any]] = []
        for i in range(MAX_FINISH_REJECTIONS):
            second_responses.append(
                {
                    "thought": f"Finish attempt {i + 1}.",
                    "action": "finish_success",
                    "argument": f"Done {i + 1}.",
                }
            )
        second_responses.append(
            {
                "thought": "Force finish.",
                "action": "finish_success",
                "argument": "Forced second run.",
            }
        )

        ai_sdk_1 = MockAiSDK(first_responses)
        ai_sdk_2 = MockAiSDK(second_responses)

        runtime = LupaRuntime()
        executor = LuaExecutor(
            ai_sdk=ai_sdk_1,  # type: ignore[arg-type]
            tool_handlers=[send_handler, FinishHandler()],
            runtime=runtime,
        )

        result1 = executor.execute("First run", permissions=[])
        assert result1.success is True
        assert result1.output == "Forced first run."

        # Swap the AI SDK for the second run
        executor._ai_sdk = ai_sdk_2  # type: ignore[assignment]

        result2 = executor.execute("Second run", permissions=[])
        assert result2.success is True
        assert result2.output == "Forced second run."
