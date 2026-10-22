"""context_breakdown reads a tool declaration that is not a dict, and a failing send step is loud.

Live 2026-10-20: ``(d or {}).get`` on a string declaration raised AttributeError in the
``context_breakdown`` send step 344 times in 172 conversations, ignored without a trace.
"""

from __future__ import annotations

import logging
from types import SimpleNamespace

from matrx_ai.config.context_breakdown import measure
from matrx_ai.config.send_boundary import SendPrep, _run_step


def _config(decls: object) -> SimpleNamespace:
    return SimpleNamespace(
        system_instruction="be brief", tool_declarations={"anthropic": decls}, messages=[], model="m"
    )


def test_a_declaration_given_as_a_string_does_not_raise() -> None:
    out = measure(_config(["web_search", {"name": "mcp.x.y"}, {"function": {"name": "custom_tool_1"}}]))
    by_key = {c["key"]: c for c in out["categories"]}
    assert by_key["system_tools"]["items"] == 1
    assert by_key["mcp_tools"]["items"] == 1
    assert by_key["agent_tools"]["items"] == 1


def test_a_single_string_declaration_does_not_raise() -> None:
    assert measure(_config("web_search"))["total_chars"] > 0


def test_a_failing_step_is_logged_as_an_error_with_its_traceback(caplog) -> None:
    prep = SendPrep(stage="loop")

    def boom() -> None:
        raise AttributeError("'str' object has no attribute 'get'")

    with caplog.at_level(logging.ERROR):
        _run_step(prep, "context_breakdown", boom)
    records = [r for r in caplog.records if r.levelno >= logging.ERROR]
    assert records and "context_breakdown" in records[0].getMessage()
    assert records[0].exc_info is not None
