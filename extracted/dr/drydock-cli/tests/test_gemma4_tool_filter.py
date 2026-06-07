"""Tool-list narrowing regression tests for Gemma-derived models.

User-observed loops 2026-06-06:
  - task -> blocked -> task -> blocked x 6     (v2.9.93-.97 saga)
  - exit_plan_mode -> "Already in implementation mode" x 4
  - notebook_edit on a .py file
  - count tool on "."

Root cause: with 72 tools exposed, the model gravitates to whichever
tool has the trivialest arg shape. Grammar union (v2.9.86-.97) made it
strict iteration. Even with union OFF (v2.9.98), Gemma 4 still wanders
through too many low-value branches.

These tests pin which tools must NOT be exposed for Gemma-derived
models so the regression can't come back.
"""
from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from drydock.core.tools.manager import ToolManager


def _gemma4_available_names() -> set[str]:
    """Build a ToolManager configured for a Gemma 4 model and return the
    set of tool names the model would see in `available_tools`."""
    cfg = MagicMock()
    cfg.enabled_tools = None
    cfg.disabled_tools = None
    cfg.mcp_servers = []
    cfg.tool_paths = []

    class FakeModel:
        name = "gemma-4-26b"
        alias = "gemma4"

    cfg.get_active_model = lambda: FakeModel()

    mgr = ToolManager(config_getter=lambda: cfg)
    return set(mgr.available_tools.keys())


# ---------------------------------------------------------------------------
# Tools that MUST be filtered out for Gemma 4
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("forbidden", [
    "task",            # v2.9.97: re-disabled after looping pattern
    "task_create",
    "task_update",
    "task_list",
    "ask_user_question",
    "invoke_skill",
    "tool_search",
    "todo",
    "search_replace",  # v2.9.84+: disabled due to arg-copying loops
    "notebook_edit",   # v2.9.95: confusion bait, write_file handles .ipynb
    "exit_plan_mode",  # v2.9.98: 0-arg "Already in implementation mode" loop
    "cron_create",     # v2.9.100: zero relevance to coding, escape hatch
    "cron_delete",
    "cron_list",       # v2.9.100: 3-in-a-row in reshard-c4-data trial
    "memory",          # v2.9.102: 7-in-a-row identical recall in extract-elf
])
def test_gemma4_does_not_expose_loop_prone_tool(forbidden):
    names = _gemma4_available_names()
    assert forbidden not in names, (
        f"{forbidden!r} is exposed for Gemma 4 - known loop driver. "
        f"Add it to _GEMMA4_AUTO_DISABLE in drydock/core/tools/manager.py."
    )


# ---------------------------------------------------------------------------
# Sanity: the core write/edit set IS still exposed for Gemma 4
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("required", [
    "write_file",
    "read_file",
    "bash",
    "grep",
    "glob",
])
def test_gemma4_keeps_core_tools(required):
    names = _gemma4_available_names()
    assert required in names, (
        f"{required!r} is the core action set - must stay exposed for Gemma 4"
    )
