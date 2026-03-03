import unittest

from abstra_internals.agents.tools.base import AgentTools
from abstra_internals.interface.sdk.ai_agent import (
    _callable_to_tool_item,
    _collect_tools,
)


class TestAiAgentInternalTools(unittest.TestCase):
    def test_callable_to_tool_item_with_docstring(self):
        def my_tool(param1: str, param2: int):
            """This is a test tool description."""
            return f"{param1} {param2}"

        item = _callable_to_tool_item(my_tool)

        self.assertEqual(item.function_name, "my_tool")
        self.assertEqual(item.description, "This is a test tool description.")
        self.assertIn("properties", item.parameters)
        self.assertIn("param1", item.parameters["properties"])
        self.assertIn("param2", item.parameters["properties"])

    def test_callable_to_tool_item_without_docstring(self):
        def no_doc_tool(x: float):
            return x

        item = _callable_to_tool_item(no_doc_tool)
        self.assertEqual(item.function_name, "no_doc_tool")
        self.assertEqual(item.description, "Tool: no_doc_tool")

    def test_collect_tools_with_callables(self):
        def tool_a():
            """Doc A"""
            pass

        def tool_b(x: int):
            """Doc B"""
            pass

        tools = [tool_a, tool_b]
        items, callables = _collect_tools(tools)

        self.assertEqual(len(items), 2)
        self.assertEqual(items[0].function_name, "tool_a")
        self.assertEqual(items[1].function_name, "tool_b")
        self.assertIs(callables["tool_a"], tool_a)
        self.assertIs(callables["tool_b"], tool_b)

    def test_collect_tools_with_agent_tools_class(self):
        class MyTools(AgentTools):
            def __tools__(self):
                return ["method_one", "method_two"]

            def method_one(self, val: str):
                """Method One Doc"""
                pass

            def method_two(self):
                """Method Two Doc"""
                pass

        instance = MyTools()
        items, callables = _collect_tools([instance])

        self.assertEqual(len(items), 2)
        names = [item.function_name for item in items]
        self.assertIn("method_one", names)
        self.assertIn("method_two", names)

    def test_collect_tools_mixed_types(self):
        def simple_tool():
            """Simple"""
            pass

        class ExtraTools(AgentTools):
            def __tools__(self):
                return ["extra_method"]

            def extra_method(self):
                """Extra"""
                pass

        items, callables = _collect_tools([simple_tool, ExtraTools()])
        self.assertEqual(len(items), 2)
        names = [item.function_name for item in items]
        self.assertIn("simple_tool", names)
        self.assertIn("extra_method", names)

    def test_collect_tools_raises_on_duplicate_name(self):
        def duplicate():
            pass

        def other_duplicate():
            pass

        other_duplicate.__name__ = "duplicate"

        with self.assertRaises(ValueError) as cm:
            _collect_tools([duplicate, other_duplicate])
        self.assertEqual(str(cm.exception), "Duplicate tool name: 'duplicate'.")

    def test_collect_tools_raises_on_invalid_type(self):
        with self.assertRaises(TypeError) as cm:
            _collect_tools(["not_a_tool"])
        self.assertIn("Invalid tool: str", str(cm.exception))
