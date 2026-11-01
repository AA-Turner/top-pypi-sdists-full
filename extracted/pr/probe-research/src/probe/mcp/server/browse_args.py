"""refuse an argument the chosen browse mode does not read."""

from __future__ import annotations
from typing import Any
from mcp.server.fastmcp.exceptions import ToolError
from ...shared.reads.search_contract import BrowseMode


# -- browse: one tool, five listings ------------------------------------------
#
# The flat modes were added beside the tree rather than as tools of their own,
# for the reason `metrics` holds its grains: "list what exists" is the concept
# and WHICH list is an argument. That makes browse's schema a UNION of every
# mode's arguments, and a union validated as a union accepts `query` on the tree
# -- which no route reads, so the agent would get the whole tree back as an
# answer to a search. (Not hypothetical: a lazy-loading agent once believed
# browse took `query`, which is why `_RetiringMCP` refuses undeclared names.)
# So, as for metrics: REFUSE, NEVER DROP, checked against what the chosen mode
# RETURNS, in the caller's own argument names.
#
# The cursor is every mode's (delivery owns it) and is not listed. `limit` is
# every mode's too, with a mode-specific meaning the schema states.
_BROWSE_MODE_ARGS: dict[BrowseMode, frozenset[str]] = {
    BrowseMode.TREE: frozenset(
        {
            "ref",
            "depth",
            "status",
            "tags",
            "workspace_id",
            "limit",
            "runs_cursor",
            "subprojects_cursor",
        }
    ),
    # `status` and `tags` are the runs list's own server filters, so they mean
    # the same here as on the tree's run level. `workspace_id` is NOT: GET
    # /v1/runs has no workspace filter, and accepting it would list every run.
    BrowseMode.RUNS: frozenset({"ref", "status", "tags", "active", "limit"}),
    # GET /v1/workspaces takes no parameters; `limit` pages the delivered list.
    BrowseMode.WORKSPACES: frozenset({"limit"}),
    # No `ref`: the catalog's parent branch is the dashboard explorer's lazy tree
    # (the NOTED CHILDREN of an entity, not its note), and the route refuses a
    # parent beside a query. An entity's own note is `entity(view="notes")`.
    BrowseMode.NOTES: frozenset({"query", "limit"}),
    # `workspace_id` names whose files; absent is the Shared folder. A run's,
    # experiment's or project's files are `entity(view="artifacts")`.
    BrowseMode.FILES: frozenset({"workspace_id", "prefix", "limit"}),
    # The data catalog (C4): each the query parameters of its own route
    # (`service._CATALOG_FILTERS` maps them), and nothing else.
    BrowseMode.DATASETS: frozenset({"query", "project", "registered", "limit"}),
    BrowseMode.CHECKPOINTS: frozenset(
        {"project", "experiment", "run", "best", "stored", "limit"}
    ),
    BrowseMode.SOURCES: frozenset({"query", "provider", "kind", "limit"}),
    # The workspace is the route's address; rows page by the token budget.
    # `branch` opens one of its branches in full, from the same read.
    BrowseMode.BRANCHES: frozenset({"workspace_id", "branch"}),
}

#: Browse arguments whose DEFAULT is not None. Supplied means "differs from the
#: default", since the wire cannot tell an explicit default from an absent one,
#: and an explicit default is a no-op in every mode.
_BROWSE_DEFAULTS: dict[str, Any] = {"depth": 1, "limit": 10}


def _browse_arg_is_neutral(name: str, value: Any) -> bool:
    """Whether an argument asks for nothing: absent, its default, or the empty
    form of its type -- `active=false`, `tags=[]`, `query=""`. Each is the same
    request as leaving it out, so refusing one would refuse a correct call.
    Spelled out with `is`, because `0 == False` would make `depth=0` vanish."""
    if value is None or value is False or value == "" or value == []:
        return True
    return name in _BROWSE_DEFAULTS and value == _BROWSE_DEFAULTS[name]


def _browse_args_for_mode(mode: BrowseMode, args: dict[str, Any]) -> None:
    """Refuse an argument the chosen browse mode does not read.

    Raises ``ToolError`` naming the mode(s) that DO read it, because the usual
    cause is the right filter on the wrong listing."""
    allowed = _BROWSE_MODE_ARGS[mode]
    supplied = {name for name, value in args.items() if not _browse_arg_is_neutral(name, value)}
    unsupported = sorted(supplied - allowed)
    if not unsupported:
        return
    detail = "; ".join(
        f"{name} (read by mode={' or '.join(modes)})" if modes else f"{name} (read by no mode)"
        for name, modes in (
            (
                name,
                sorted(m.value for m, ok in _BROWSE_MODE_ARGS.items() if name in ok and m != mode),
            )
            for name in unsupported
        )
    )
    hints = []
    if "query" in unsupported:
        hints.append("To search across everything, use search.")
    if mode == BrowseMode.FILES and "ref" in unsupported:
        hints.append(
            'A run\'s, experiment\'s or project\'s own files are entity(view="artifacts").'
        )
    if mode in (BrowseMode.DATASETS, BrowseMode.CHECKPOINTS) and "ref" in unsupported:
        hints.append(f"mode={mode.value} narrows by `project` (checkpoints: `experiment`, `run`).")
    raise ToolError(
        f"browse: mode={mode.value} does not read {', '.join(unsupported)} -- {detail}. "
        + " ".join(hints)
        + (" " if hints else "")
        + "Re-issue the call in the mode that reads it; passing it here would return a "
        "listing that ignored it."
    )
