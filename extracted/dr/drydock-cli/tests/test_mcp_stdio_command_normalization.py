"""Regression: stdio MCP server command must not be passed as a string.

The 2026-05-18 bug: ``read_mcp_resource`` failed with
``Input should be a valid list, input_value='ython3'`` because
``mcp_resources.py`` passed ``srv.command`` (which can be a string)
directly to functions that did ``command[0], command[1:]``. For
``command="python3"`` that yields ``("p", "ython3")`` and pydantic
rejects ``args="ython3"``.
"""

import pytest

from drydock.core.tools.mcp.tools import _split_command
from drydock.core.tools.base import ToolError


def test_split_command_handles_list() -> None:
    exe, args = _split_command(["python3", "-m", "srv"])
    assert exe == "python3"
    assert args == ["-m", "srv"]


def test_split_command_handles_bare_string() -> None:
    """The historical failure mode — string instead of list."""
    exe, args = _split_command("python3")
    assert exe == "python3"
    assert args == []
    # Critically: args is NOT the string "ython3"
    assert args != "ython3"


def test_split_command_handles_string_with_args() -> None:
    exe, args = _split_command("python3 -m my_server --port 1234")
    assert exe == "python3"
    assert args == ["-m", "my_server", "--port", "1234"]


def test_split_command_empty_raises() -> None:
    with pytest.raises(ToolError):
        _split_command([])
    with pytest.raises(ToolError):
        _split_command("")


def test_mcpstdio_argv_returns_list_for_both_forms() -> None:
    """MCPStdio.argv() is the right way for callers to get a list."""
    from drydock.core.config import MCPStdio

    s1 = MCPStdio(name="a", transport="stdio", command="python3 -m srv")
    assert s1.argv() == ["python3", "-m", "srv"]

    s2 = MCPStdio(name="b", transport="stdio", command=["python3", "-m", "srv"])
    assert s2.argv() == ["python3", "-m", "srv"]
