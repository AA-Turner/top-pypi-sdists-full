from typing import Any, Dict

from abstra_internals.entities.agents.tools.dispatcher import (
    FinishHandler,
    ToolDispatcher,
)


class FakeHandler:
    def __init__(self, name: str, result: str = "ok"):
        self._name = name
        self._result = result

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return f"Fake handler: {self._name}"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object", "properties": {"value": {"type": "string"}}}

    def execute(self, action_input: Dict[str, Any]) -> str:
        return self._result


class ErrorHandler:
    @property
    def name(self) -> str:
        return "error_tool"

    @property
    def description(self) -> str:
        return "A tool that always fails"

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {"type": "object"}

    def execute(self, action_input: Dict[str, Any]) -> str:
        raise RuntimeError("Tool exploded")


class TestToolDispatcher:
    def test_dispatch_known_action(self):
        dispatcher = ToolDispatcher([FakeHandler("greet", "Hello!")])
        result = dispatcher.dispatch("greet", {})
        assert result == "Hello!"

    def test_dispatch_unknown_action(self):
        dispatcher = ToolDispatcher([FakeHandler("greet")])
        result = dispatcher.dispatch("unknown", {})
        assert "Error: Unknown action 'unknown'" in result
        assert "greet" in result

    def test_dispatch_error_is_caught(self):
        dispatcher = ToolDispatcher([ErrorHandler()])
        result = dispatcher.dispatch("error_tool", {})
        assert "Error executing 'error_tool'" in result
        assert "Tool exploded" in result

    def test_get_action_names(self):
        dispatcher = ToolDispatcher(
            [
                FakeHandler("a"),
                FakeHandler("b"),
                FinishHandler(),
            ]
        )
        names = dispatcher.get_action_names()
        assert set(names) == {"a", "b", "finish"}

    def test_get_tool_descriptions(self):
        dispatcher = ToolDispatcher([FakeHandler("greet"), FinishHandler()])
        desc = dispatcher.get_tool_descriptions()
        assert "greet" in desc
        assert "finish" in desc
        assert "Fake handler: greet" in desc

    def test_empty_dispatcher(self):
        dispatcher = ToolDispatcher([])
        result = dispatcher.dispatch("anything", {})
        assert "Error: Unknown action" in result
        assert dispatcher.get_action_names() == []


class TestFinishHandler:
    def test_finish_returns_answer(self):
        handler = FinishHandler()
        result = handler.execute({"answer": "Done!"})
        assert result == "Done!"

    def test_finish_default_answer(self):
        handler = FinishHandler()
        result = handler.execute({})
        assert result == "Task completed."

    def test_finish_properties(self):
        handler = FinishHandler()
        assert handler.name == "finish"
        assert (
            "complete" in handler.description.lower()
            or "finish" in handler.description.lower()
        )
        assert handler.input_schema["type"] == "object"
