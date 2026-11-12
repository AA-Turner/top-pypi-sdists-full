"""refuse an argument the chosen browse mode does not read; turn its `project` / `experiment` scope into the internal `ref`."""

from __future__ import annotations
import re
import uuid
from collections.abc import Callable
from typing import Any
from mcp.server.fastmcp.exceptions import ToolError
from ...sdk.client.ids import _BARE_ID
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
    BrowseMode.PROJECTS: frozenset(
        {
            "ref",
            "project",
            "experiment",
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
    BrowseMode.RUNS: frozenset(
        {
            "ref",
            "project",
            "experiment",
            "status",
            "tags",
            "active",
            "filter",
            "order",
            "latest_metrics",
            "limit",
        }
    ),
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


# -- browse: the scope, in the words callers use --------------------------------
#
# mode=projects / runs take `project` or `experiment` (a slug or a uuid) and walk
# the internal `ref` (`kind:<uuid>`), which browse delivery plans its pages from
# (`delivery.browse.invoke` reads `ref` before the tool body runs) and the runs
# list needs as a uuid (`listing._uuid_ref`). So the scope is resolved HERE, once
# per call, before delivery: the pages it then fetches carry their own internal
# refs and never pass through this again. `ref` itself still works, undocumented.

#: The modes whose scope `project` / `experiment` name (the catalog modes read them as their own filters).
_SCOPED_MODES = frozenset({BrowseMode.PROJECTS, BrowseMode.RUNS})
_SCOPE_KINDS = ("project", "experiment")


#: What may be looked up as a slug: one path segment of the route `entity` reads with, never a `/`, `?`,
#: `#`, `%`, `..` or space that would steer the GET elsewhere.
_SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def normalize_browse_scope(arguments: dict[str, Any], find_id: Callable[[str, str], str]) -> dict[str, Any]:
    """The caller's browse arguments with `project` / `experiment` (or a slug in `ref`) turned into
    the internal `ref` = `kind:<uuid>`. `find_id(kind, slug)` is the tenant's own lookup (the one
    `entity` reads with); a uuid is used as given. Refuses two scopes at once, naming the one to keep."""
    if BrowseMode(arguments.get("mode") or BrowseMode.PROJECTS) not in _SCOPED_MODES:
        return arguments
    given = {kind: arguments.get(kind) for kind in _SCOPE_KINDS if arguments.get(kind)}
    ref = arguments.get("ref")
    if len(given) == 2:
        raise ToolError(
            "browse: pass `experiment` alone -- it already names its project; `project` and "
            "`experiment` together are two scopes."
        )
    if given and ref:
        (kind,) = given
        raise ToolError(f"browse: pass `{kind}` alone -- `ref` is an older spelling of the same scope.")
    if given:
        ((kind, value),) = given.items()
    elif isinstance(ref, str) and ref.partition(":")[0] in _SCOPE_KINDS and ref.partition(":")[2]:
        kind, _, value = ref.partition(":")
    else:
        return arguments
    value = str(value).strip()
    prefix = f"{kind}:"
    if value.startswith(prefix):
        value = value[len(prefix):]
    if _BARE_ID.fullmatch(value):
        ident = value
    elif _SLUG.fullmatch(value) and ".." not in value:
        ident = find_id(kind, value)
    else:
        raise ToolError(f"browse: {kind} {value!r} is neither a slug nor a uuid")
    try:
        ident = str(uuid.UUID(str(ident)))
    except ValueError:
        raise ToolError(f"browse: the {kind} {value!r} resolved to no usable id") from None
    return {**arguments, "ref": f"{kind}:{ident}", "project": None, "experiment": None}
