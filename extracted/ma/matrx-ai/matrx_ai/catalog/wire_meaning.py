"""What a wire payload MEANS, key by key (PB-03 U3, 2026-10-17).

A setting a model's rules mark unsupported must not reach the provider in ANY shape —
not as a top-level key, and not folded into a nested one (Gemini ``thinking_config``,
Anthropic ``thinking``, OpenAI ``reasoning``, ``generation_config`` ...). "Translated"
never excuses sending a value the model cannot take. This module names, per canonical
setting, the wire leaf names that carry its MEANING, and finds them anywhere in a payload.
"""

from __future__ import annotations

from typing import Any

# canonical setting -> leaf names (any nesting depth, any casing style) that carry it.
MEANING_LEAVES: dict[str, frozenset[str]] = {
    "thinking_budget": frozenset({"thinking_budget", "thinkingbudget", "budget_tokens", "budgettokens"}),
    "include_thoughts": frozenset({"include_thoughts", "includethoughts"}),
    "thinking_level": frozenset({"thinking_level", "thinkinglevel"}),
    "reasoning_effort": frozenset({"reasoning_effort", "reasoningeffort", "effort"}),
    "reasoning_summary": frozenset({"reasoning_summary", "summary"}),
    "clear_thinking": frozenset({"clear_thinking"}),
    "temperature": frozenset({"temperature"}),
    "top_p": frozenset({"top_p", "topp"}),
    "top_k": frozenset({"top_k", "topk"}),
    "seed": frozenset({"seed"}),
    "frequency_penalty": frozenset({"frequency_penalty", "frequencypenalty"}),
    "presence_penalty": frozenset({"presence_penalty", "presencepenalty"}),
    "stop_sequences": frozenset({"stop", "stop_sequences", "stopsequences"}),
    "parallel_tool_calls": frozenset({"parallel_tool_calls", "disable_parallel_tool_use"}),
    "verbosity": frozenset({"verbosity"}),
    "store": frozenset({"store"}),
}


def _walk(node: Any, path: str):
    if isinstance(node, dict):
        for k, v in node.items():
            yield from _walk(v, f"{path}.{k}" if path else str(k))
    elif isinstance(node, (list, tuple)):
        for i, v in enumerate(node):
            yield from _walk(v, f"{path}[{i}]")
    else:
        yield path, node


def leaves(payload: Any) -> list[tuple[str, Any]]:
    """Every (dotted path, scalar) in a payload, however deep."""
    return list(_walk(payload, ""))


# Hosted (provider-run) tools. A setting like ``internal_web_search`` has no scalar wire
# leaf: its meaning is a TOOL ENTRY in a ``tools`` array (L16, defect 45). canonical
# setting -> normalized stems (lowercased, ``_``/``-`` removed) of the tool ``type`` or
# wrapper key that carries it, for every provider:
#   Anthropic  {"type": "web_search_20250305"}, web_fetch_*, code_execution_*
#   OpenAI     {"type": "web_search"} / {"type": "web_search_preview"}, {"type": "code_interpreter"}
#   Google     {"google_search": {}} / {"googleSearch": {}}, {"url_context": {}}, {"code_execution": {}}
#   xAI        {"type": "web_search"}, {"type": "x_search"}
HOSTED_TOOL_MEANING: dict[str, tuple[str, ...]] = {
    "internal_web_search": ("websearch", "googlesearch"),
    "internal_url_context": ("urlcontext", "webfetch"),
    "internal_x_search": ("xsearch",),
    "code_execution": ("codeexecution", "codeinterpreter"),
}


def _norm(name: Any) -> str:
    return str(name).lower().replace("_", "").replace("-", "")


def _tool_means(tool: Any, stems: tuple[str, ...]) -> bool:
    if not isinstance(tool, dict):
        return False
    # ``type`` only: a local function tool is identified by ``name``, and a function the
    # caller named "web_search" is not the provider's hosted tool. Google wraps the hosted
    # tool in a key of its own name.
    kind = tool.get("type")
    if isinstance(kind, str) and _norm(kind).startswith(stems):
        return True
    return any(
        _norm(k).startswith(stems) and v is not None
        for k, v in tool.items()
        if k not in ("type", "name")
    )


def hosted_tool_paths(payload: Any, key: str) -> list[str]:
    """Paths of every hosted-tool entry meaning ``key`` in any ``tools`` array of ``payload``
    (top level or nested: ``config.tools``, ``generation_config.tools`` ...)."""
    stems = HOSTED_TOOL_MEANING.get(key)
    if not stems:
        return []
    out: list[str] = []

    def visit(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for k, v in node.items():
                here = f"{path}.{k}" if path else str(k)
                if str(k).lower() == "tools" and isinstance(v, (list, tuple)):
                    for i, tool in enumerate(v):
                        if _tool_means(tool, stems):
                            out.append(f"{here}[{i}]")
                        else:
                            visit(tool, f"{here}[{i}]")
                else:
                    visit(v, here)
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                visit(v, f"{path}[{i}]")

    visit(payload, "")
    return out


def meaning_paths(payload: Any, key: str) -> list[str]:
    """Wire paths in ``payload`` whose leaf name carries canonical setting ``key`` — scalar
    leaves at any depth, plus hosted-tool entries in ``tools`` arrays (every provider)."""
    names = MEANING_LEAVES.get(key, frozenset({key.lower()}))
    out: list[str] = list(hosted_tool_paths(payload, key))
    for path, _ in leaves(payload):
        leaf = path.rsplit(".", 1)[-1].split("[", 1)[0]
        if leaf.lower() in names:
            out.append(path)
    return out
