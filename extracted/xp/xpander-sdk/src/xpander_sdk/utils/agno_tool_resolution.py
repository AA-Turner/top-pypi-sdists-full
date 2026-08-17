"""Unknown tool-call repair for agno runs.

With dynamic tools active, the catalog hint and xp_search_tools results show
the model hidden tool ids that are reachable only through xp_execute_tool.
Models regularly call those ids directly; agno resolves the name to None and
feeds back "the requested tool does not exist" with no next step. Wrapping
agno's resolver turns a hidden-catalog id into a transparent xp_execute_tool
call, and gives every other unknown name a repair path instead of a dead end.
"""

import json
import weakref
from typing import Any, Callable, Dict, Optional

from loguru import logger

EXECUTE_META_TOOL = "xp_execute_tool"
SEARCH_META_TOOL = "xp_search_tools"

# Stable prefix: joins the no-progress markers and keys the log trend.
UNKNOWN_TOOL_PREFIX = "Tool not loaded this turn:"

UNKNOWN_TOOL_DYNAMIC_GUIDANCE = (
    UNKNOWN_TOOL_PREFIX + " '{name}' is not directly callable. Find it with "
    'xp_search_tools(query="...") and run the match with '
    "xp_execute_tool(name, arguments). If the work is already complete, "
    "answer now with your final result."
)
UNKNOWN_TOOL_STATIC_GUIDANCE = (
    UNKNOWN_TOOL_PREFIX + " '{name}' is not directly callable. Use one of the "
    "tools available in this conversation, or if the work is already "
    "complete, answer now with your final result."
)

_DYNAMIC_REPOS: Dict[int, "weakref.ref"] = {}

_INSTALLED = False


def register_dynamic_tools_repo(repo: Any) -> None:
    """Make `repo`'s hidden catalog visible to the resolver, weakly held."""
    _DYNAMIC_REPOS.pop(id(repo), None)
    for key, ref in list(_DYNAMIC_REPOS.items()):
        if ref() is None:
            _DYNAMIC_REPOS.pop(key, None)
    try:
        _DYNAMIC_REPOS[id(repo)] = weakref.ref(repo)
    except TypeError:
        pass


def resolve_hidden_tool_id(name: str) -> Optional[str]:
    """Canonical id when `name` names a hidden dynamic-catalog tool, else None."""
    if not name:
        return None
    from xpander_sdk.modules.tools_repository.sub_modules.dynamic_tools import (
        hidden_tools,
    )

    for ref in list(_DYNAMIC_REPOS.values()):
        repo = ref()
        if repo is None:
            continue
        try:
            for tool in hidden_tools(repo.dynamic_catalog):
                if name in (tool.id, tool.name):
                    return tool.id
        except Exception:
            continue
    return None


def _parse_arguments(arguments: Optional[str]) -> Optional[Dict[str, Any]]:
    """Arguments string as a dict; {} when empty, None when unrecoverable."""
    if arguments is None or arguments == "":
        return {}
    try:
        try:
            parsed = json.loads(arguments)
        except Exception:
            import ast

            parsed = ast.literal_eval(arguments)
    except Exception:
        return None
    if not isinstance(parsed, dict):
        return None
    # a model imitating the loaded-tool convention wraps the args once already
    if set(parsed) == {"payload"} and isinstance(parsed["payload"], dict):
        parsed = parsed["payload"]
    return parsed


def _repair_function_call(
    name: str, call_id: Optional[str], functions: Optional[Dict[str, Any]]
) -> Any:
    """FunctionCall whose .error carries the repair path agno feeds back."""
    from agno.tools.function import Function, FunctionCall

    template = (
        UNKNOWN_TOOL_DYNAMIC_GUIDANCE
        if functions and SEARCH_META_TOOL in functions
        else UNKNOWN_TOOL_STATIC_GUIDANCE
    )
    function_call = FunctionCall(
        function=Function(name=name), error=template.format(name=name)
    )
    if call_id is not None:
        function_call.call_id = call_id
    return function_call


def _patch_get_function_call(original: Callable) -> Callable:
    """Wrap agno's resolver: known names untouched, unknown names repaired."""

    def get_function_call(
        name: str,
        arguments: Optional[str] = None,
        call_id: Optional[str] = None,
        functions: Optional[Dict[str, Any]] = None,
    ) -> Optional[Any]:
        if functions is None or name in functions:
            return original(
                name=name, arguments=arguments, call_id=call_id, functions=functions
            )
        hidden_id = resolve_hidden_tool_id(name)
        if hidden_id is not None and EXECUTE_META_TOOL in functions:
            parsed = _parse_arguments(arguments)
            if parsed is not None:
                logger.warning(
                    f"[tool-repair] unknown function '{name}' rewritten into "
                    f"{EXECUTE_META_TOOL}"
                )
                wrapped = json.dumps(
                    {"payload": {"name": hidden_id, "arguments": parsed}}
                )
                return original(
                    name=EXECUTE_META_TOOL,
                    arguments=wrapped,
                    call_id=call_id,
                    functions=functions,
                )
        logger.warning(
            f"[tool-repair] unknown function '{name}' answered with the repair path"
        )
        return _repair_function_call(name, call_id, functions)

    return get_function_call


# agno.utils.tools binds the resolver at import time, so both bindings need the patch
_TARGET_MODULES = (
    "agno.utils.functions",
    "agno.utils.tools",
)


def install_agno_tool_resolution_patch() -> bool:
    """Repair unknown tool calls instead of dead-ending; safe to call repeatedly."""
    global _INSTALLED
    if _INSTALLED:
        return True
    import importlib

    reached_agno = False
    for module_name in _TARGET_MODULES:
        try:
            module = importlib.import_module(module_name)
        except Exception:
            continue
        original = getattr(module, "get_function_call", None)
        if original is None:
            continue
        reached_agno = True
        if getattr(original, "_xpander_tool_repair", False):
            continue
        replacement = _patch_get_function_call(original)
        replacement._xpander_tool_repair = True  # type: ignore[attr-defined]
        setattr(module, "get_function_call", replacement)
    # only latch once the patch is really in effect, so a failed import can retry later
    _INSTALLED = reached_agno
    if not reached_agno:
        logger.debug("[tool-repair] patch not installed - agno resolver unreachable")
    return reached_agno
