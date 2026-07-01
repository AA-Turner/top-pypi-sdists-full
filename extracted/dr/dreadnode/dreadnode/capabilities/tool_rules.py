"""Tool filtering rules with glob-pattern matching.

Agents declare tool access via a dict of {pattern: bool} rules.
Rules are evaluated in insertion order; last matching rule wins.
Patterns use fnmatch glob syntax (*, ?, [seq]).

Examples:
    {}                                           -> all tools allowed (default)
    {"*": True, "bash": False}                   -> everything except bash
    {"*": False, "read": True, "grep": True}     -> only read and grep
    {"web_pd__*": False}                         -> block all web_pd capability tools
    {"*": True, "web_pd__*": False,
     "web_pd__pd_start_scan": True}              -> allow one, deny other web_pd tools
"""

import fnmatch
import typing as t
from collections import defaultdict

ToolRules = dict[str, bool]


def validate_wire_names(tools: t.Iterable[t.Any]) -> None:
    """Raise if two tools in *tools* compute the same wire name (CAP-IDENT-013).

    Different `namespace` tuples produce different wire names by
    construction, so cross-capability bare-name overlap is not a collision.
    Intra-capability wire collisions (e.g. Python tool named
    ``{server}__{name}`` clashing with MCP tool ``{name}`` under server
    ``{server}``) are vanishingly rare but structurally possible — this
    validator surfaces them with an actionable error naming both
    offending components.
    """
    seen: dict[str, list[t.Any]] = defaultdict(list)
    for tool in tools:
        wire = getattr(tool, "wire_name", None)
        if wire is None:
            continue
        seen[wire].append(tool)

    collisions = {wire: bucket for wire, bucket in seen.items() if len(bucket) > 1}
    if not collisions:
        return

    lines: list[str] = []
    for wire, bucket in collisions.items():
        parts = []
        for tool in bucket:
            source = getattr(tool, "source", "unknown")
            bare = getattr(tool, "name", "?")
            namespace = getattr(tool, "namespace", ())
            ns_repr = "/".join(namespace) if namespace else "()"
            parts.append(f"{source}:{ns_repr}:{bare}")
        lines.append(f"  {wire!r}: {', '.join(parts)}")
    raise ValueError(
        "Multiple components compute the same wire name. "
        "Rename one of the colliding components or change the capability/server "
        "segment so projections diverge:\n" + "\n".join(lines)
    )


def match_pattern(name: str, pattern: str) -> bool:
    """Match a tool name against a glob pattern (*, ?, [seq]).

    Matching is case-insensitive so authors don't need to worry about
    the exact casing of tool names.
    """
    return fnmatch.fnmatchcase(name.lower(), pattern.lower())


def is_tool_allowed(tool_or_name: t.Any, rules: ToolRules) -> bool:
    """Check if a tool is allowed by evaluating rules in order.

    Under CAP-IDENT-014, a pattern matches if it matches either the tool's
    ``wire_name`` (the LLM-facing projection, e.g. ``bloodhound__connect``)
    or its bare ``name`` (e.g. ``connect``). Existing bare-name rules in
    capability YAMLs continue to work without modification.

    Accepts either a tool-like object (with ``wire_name`` and ``name``) or
    a plain string for legacy call sites that don't have a Tool handy.
    Last matching rule wins. If no rule matches, the tool is allowed.
    """
    if isinstance(tool_or_name, str):
        names: tuple[str, ...] = (tool_or_name,)
    else:
        wire = getattr(tool_or_name, "wire_name", None)
        bare = getattr(tool_or_name, "name", None)
        if wire is not None and bare is not None and wire != bare:
            names = (wire, bare)
        else:
            names = tuple(n for n in (wire, bare) if n is not None)
    result = True
    for pattern, allowed in rules.items():
        if any(match_pattern(name, pattern) for name in names):
            result = allowed
    return result


def filter_tools(
    tools: list[t.Any],
    rules: ToolRules,
    *,
    name_fn: t.Callable[[t.Any], str] | None = None,
) -> list[t.Any]:
    """Filter tool objects through rules. Empty rules = all tools pass.

    By default passes the full tool object to ``is_tool_allowed`` so dual-match
    against wire and bare names runs. Pass ``name_fn`` for fixtures that only
    expose a name string.
    """
    if not rules:
        return list(tools)
    if name_fn is not None:
        return [tool for tool in tools if is_tool_allowed(name_fn(tool), rules)]
    return [tool for tool in tools if is_tool_allowed(tool, rules)]
