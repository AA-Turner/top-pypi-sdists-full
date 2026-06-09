"""Verify that a tool with a broken annotation can't crash the whole session.

Before 2026-06-08: a single tool whose `run()` annotation made
`get_parameters()` raise TypeError would take down both:
  - the LLM call (`format.get_available_tools` listed all tools)
  - the session save (`session_logger.save_interaction` listed all tools)

Both call sites now isolate per-tool failures with a logged warning
and continue with the rest. A bad tool is invisible to the model for
that turn; the session keeps going.
"""
from __future__ import annotations
from unittest.mock import MagicMock


def test_get_available_tools_isolates_broken_tools(caplog):
    """A tool whose get_parameters() raises does not abort the list."""
    from drydock.core.llm.format import APIToolFormatHandler

    class GoodTool:
        @classmethod
        def get_name(cls) -> str:
            return "good"

        @classmethod
        def get_parameters(cls) -> dict:
            return {"type": "object", "properties": {}}

        description = "a working tool"

    class BrokenTool:
        @classmethod
        def get_name(cls) -> str:
            return "broken"

        @classmethod
        def get_parameters(cls) -> dict:
            raise TypeError("simulated annotation bug")

        description = "a broken tool"

    tm = MagicMock()
    tm.available_tools = {"good": GoodTool, "broken": BrokenTool}

    handler = APIToolFormatHandler()
    tools = handler.get_available_tools(tm)

    # Good tool survives, broken tool is filtered out.
    names = [t.function.name for t in tools]
    assert "good" in names, names
    assert "broken" not in names, names


def test_get_available_tools_returns_empty_if_all_broken():
    """All tools broken → empty list, not exception."""
    from drydock.core.llm.format import APIToolFormatHandler

    class BrokenTool:
        @classmethod
        def get_name(cls) -> str:
            return "broken"

        @classmethod
        def get_parameters(cls) -> dict:
            raise TypeError("simulated")

        description = "broken"

    tm = MagicMock()
    tm.available_tools = {"broken": BrokenTool}

    handler = APIToolFormatHandler()
    tools = handler.get_available_tools(tm)
    assert tools == []
