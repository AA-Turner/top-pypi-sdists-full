"""The drift gate reads a decorated tool through its decorator to the private implementation.

Live 2026-11-06: ``workflow_run`` and ``workflow_catalog`` were the last two "unverified" contracts on every
boot. Both validate their model in a private implementation, and both are decorated. ``functools.wraps`` makes
``getsource`` answer with the wrapped function while ``__globals__`` stays the decorator's module, so the walk
never found the implementation to follow. The second test proves the fix cannot call an unbound tool bound.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

from matrx_ai.tools.validation.runner import find_unverified_tools
from pydantic import BaseModel


class _BoundArgs(BaseModel):
    value: str = ""


class _UnusedArgs(BaseModel):
    value: str = ""


def _wraps_it(func: Any) -> Any:
    from _decorator_elsewhere import passthrough

    return passthrough(func)


async def _impl(args: dict[str, Any]) -> Any:
    return _BoundArgs(**args)


@_wraps_it
async def bound_tool(args: dict[str, Any]) -> Any:
    return await _impl(args)


@_wraps_it
async def unbound_tool(args: dict[str, Any]) -> Any:
    return args.get("value")


def _declared(func: Any, model: Any) -> Any:
    return SimpleNamespace(executor="aidream", args_model=model, func=func, function_path="t")


def test_a_decorated_tool_whose_implementation_binds_its_model_is_verified():
    assert find_unverified_tools({"t": _declared(bound_tool, _BoundArgs)}, {"aidream"}) == []


def test_a_decorated_tool_that_never_uses_its_model_is_still_reported():
    found = find_unverified_tools({"t": _declared(unbound_tool, _UnusedArgs)}, {"aidream"})
    assert [f["tool_name"] for f in found] == ["t"]
