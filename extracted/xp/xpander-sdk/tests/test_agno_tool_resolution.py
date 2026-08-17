"""Unknown tool calls repair into xp_execute_tool instead of dead-ending."""

import json
from types import SimpleNamespace
from typing import Any, Dict, List, Optional

import pytest
from agno.tools.function import Function

from xpander_sdk.utils import agno_tool_resolution
from xpander_sdk.utils.agno_tool_resolution import (
    UNKNOWN_TOOL_PREFIX,
    install_agno_tool_resolution_patch,
    register_dynamic_tools_repo,
)

HIDDEN_ID = "XpanderWebSearchSearchWebUsingTavilyAPI"
MCP_HIDDEN_ID = "mcp_tool_notion-fetch"


class _FakeRepo:
    def __init__(self, catalog: List[Any]) -> None:
        self.dynamic_catalog = catalog


def _make_repo() -> _FakeRepo:
    catalog = [
        SimpleNamespace(id=HIDDEN_ID, name="Search Web", description="web search"),
        SimpleNamespace(
            id=MCP_HIDDEN_ID,
            name=MCP_HIDDEN_ID,
            description="fetch a notion page",
            is_mcp_proxy=True,
        ),
        SimpleNamespace(id="xp_get_tool", name="xp_get_tool", description="meta"),
    ]
    return _FakeRepo(catalog)


def _functions(with_meta_tools: bool = True) -> Dict[str, Function]:
    names = ["known_tool"]
    if with_meta_tools:
        names += ["xp_execute_tool", "xp_search_tools"]
    return {name: Function(name=name) for name in names}


@pytest.fixture(autouse=True)
def _patched_with_repo():
    install_agno_tool_resolution_patch()
    repo = _make_repo()
    register_dynamic_tools_repo(repo)
    yield repo
    agno_tool_resolution._DYNAMIC_REPOS.pop(id(repo), None)


def _resolve(
    name: str,
    arguments: Optional[str] = None,
    call_id: Optional[str] = None,
    functions: Optional[Dict[str, Function]] = None,
) -> Any:
    import agno.utils.functions as agno_functions

    return agno_functions.get_function_call(
        name=name, arguments=arguments, call_id=call_id, functions=functions
    )


def test_hidden_id_rewritten_into_execute_tool():
    args = {"body_params": {"query": "xpander"}}
    fc = _resolve(HIDDEN_ID, json.dumps(args), "call_1", _functions())
    assert fc is not None and fc.error is None
    assert fc.function.name == "xp_execute_tool"
    assert fc.call_id == "call_1"
    assert fc.arguments == {"payload": {"name": HIDDEN_ID, "arguments": args}}


def test_mcp_hidden_id_rewritten_with_flat_args():
    args = {"page_id": "abc123"}
    fc = _resolve(MCP_HIDDEN_ID, json.dumps(args), None, _functions())
    assert fc.function.name == "xp_execute_tool"
    assert fc.arguments == {"payload": {"name": MCP_HIDDEN_ID, "arguments": args}}


def test_payload_wrapped_args_are_not_double_wrapped():
    args = {"payload": {"body_params": {"query": "xpander"}}}
    fc = _resolve(HIDDEN_ID, json.dumps(args), None, _functions())
    assert fc.arguments == {
        "payload": {"name": HIDDEN_ID, "arguments": args["payload"]}
    }


def test_hidden_name_resolves_to_canonical_id():
    fc = _resolve("Search Web", "{}", None, _functions())
    assert fc.function.name == "xp_execute_tool"
    assert fc.arguments["payload"]["name"] == HIDDEN_ID


def test_unknown_id_gets_repair_path_error():
    fc = _resolve("ghost_tool", "{}", "call_2", _functions())
    assert fc is not None
    assert fc.call_id == "call_2"
    assert fc.error == (
        UNKNOWN_TOOL_PREFIX + " 'ghost_tool' is not directly callable. Find it "
        'with xp_search_tools(query="...") and run the match with '
        "xp_execute_tool(name, arguments). If the work is already complete, "
        "answer now with your final result."
    )


def test_unknown_id_without_meta_tools_gets_static_guidance():
    fc = _resolve("ghost_tool", "{}", None, _functions(with_meta_tools=False))
    assert fc.error.startswith(UNKNOWN_TOOL_PREFIX)
    assert "xp_search_tools" not in fc.error
    assert "answer now" in fc.error


def test_hidden_id_with_unparseable_args_falls_to_repair_path():
    fc = _resolve(HIDDEN_ID, "not json at all {{", None, _functions())
    assert fc.error is not None
    assert fc.error.startswith(UNKNOWN_TOOL_PREFIX)


def test_known_function_calls_untouched():
    functions = _functions()
    fc = _resolve("known_tool", '{"payload": {"x": 1}}', "call_3", functions)
    assert fc.function is functions["known_tool"]
    assert fc.error is None
    assert fc.arguments == {"payload": {"x": 1}}


def test_patch_is_idempotent():
    import agno.utils.functions as agno_functions
    import agno.utils.tools as agno_tools

    before = agno_functions.get_function_call
    assert install_agno_tool_resolution_patch() is True
    assert agno_functions.get_function_call is before
    assert getattr(agno_functions.get_function_call, "_xpander_tool_repair", False)
    assert getattr(agno_tools.get_function_call, "_xpander_tool_repair", False)


def test_consumer_path_through_tool_call_dict():
    """The production path: agno.models.base resolves via get_function_call_for_tool_call."""
    from agno.utils.tools import get_function_call_for_tool_call

    tool_call = {
        "type": "function",
        "id": "call_4",
        "function": {"name": HIDDEN_ID, "arguments": json.dumps({"q": "hi"})},
    }
    fc = get_function_call_for_tool_call(tool_call, _functions())
    assert fc is not None
    assert fc.function.name == "xp_execute_tool"
    assert fc.arguments == {"payload": {"name": HIDDEN_ID, "arguments": {"q": "hi"}}}
