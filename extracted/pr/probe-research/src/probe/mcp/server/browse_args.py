"""refuse an argument the chosen browse mode does not read; turn its `project` / `experiment` scope into the internal `ref`."""

from __future__ import annotations
import json
import re
import uuid
from collections.abc import Callable
from typing import Any
from mcp.server.fastmcp.exceptions import ToolError
from pydantic import WithJsonSchema
from ...sdk.client.ids import _BARE_ID
from ...shared.reads.search_contract import OWNER_MODES, BrowseMode, BrowseOrder


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
# every mode's too, with a mode-specific meaning the schema states. The person
# and time filters (`_PEOPLE_FILTER_ARGS`) join every mode in `OWNER_MODES`
# below, so the two can never disagree.
_MODE_OWN_ARGS: dict[BrowseMode, frozenset[str]] = {
    BrowseMode.PROJECTS: frozenset(
        {
            # The top level's name match: sent only to a server that declares `browse_project_query`.
            "query",
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
    # `query` (runs, files, checkpoints, sessions): the loose name match, sent only to a server that declares
    # `browse_name_query` (`NAME_QUERY_MODES`); datasets and sources send it as their text filter `q` before it.
    BrowseMode.RUNS: frozenset(
        {
            "query",
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
    BrowseMode.FILES: frozenset({"query", "workspace_id", "prefix", "limit"}),
    # The data catalog (C4): each the query parameters of its own route
    # (`service._CATALOG_FILTERS` maps them), and nothing else.
    BrowseMode.DATASETS: frozenset({"query", "project", "registered", "limit"}),
    BrowseMode.CHECKPOINTS: frozenset(
        {"query", "project", "experiment", "run", "best", "stored", "limit"}
    ),
    BrowseMode.SOURCES: frozenset({"query", "provider", "kind", "limit"}),
    # The workspace is the route's address; rows page by the token budget.
    # `branch` opens one of its branches in full, from the same read.
    BrowseMode.BRANCHES: frozenset({"workspace_id", "branch"}),
    # The roster is the team's, whole; `query` finds teammates by name or email (as `owner` does); `limit` pages it.
    BrowseMode.PEOPLE: frozenset({"query", "limit"}),
    # `project` narrows to one project's sessions (resolved into `ref`).
    BrowseMode.SESSIONS: frozenset({"query", "ref", "project", "limit"}),
}

#: The modes whose `query` an older server would ignore (and answer unfiltered): refused there.
NAME_QUERY_MODES = frozenset({BrowseMode.RUNS, BrowseMode.FILES, BrowseMode.CHECKPOINTS, BrowseMode.SESSIONS})

#: The person and time filters (people and time filters B2): passed to the route as given.
_PEOPLE_FILTER_ARGS = frozenset({"owner", "since", "until", "order"})

_BROWSE_MODE_ARGS: dict[BrowseMode, frozenset[str]] = {
    mode: args | _PEOPLE_FILTER_ARGS if mode in OWNER_MODES else args
    for mode, args in _MODE_OWN_ARGS.items()
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


def _browse_args_for_mode(
    mode: BrowseMode, args: dict[str, Any], withheld: frozenset[str] = frozenset()
) -> None:
    """Refuse an argument the chosen browse mode does not read; `withheld` are ones this server cannot take yet.

    Raises ``ToolError`` naming the mode(s) that DO read it, because the usual
    cause is the right filter on the wrong listing."""
    allowed = _BROWSE_MODE_ARGS[mode] - withheld
    supplied = {name for name, value in args.items() if not _browse_arg_is_neutral(name, value)}
    unsupported = sorted(supplied - allowed)
    order = args.get("order")
    if not unsupported and order and mode is not BrowseMode.RUNS and order != BrowseOrder.RECENT:
        # Only mode=runs sorts by a field; every other mode's order is its default or newest first.
        raise ToolError(
            f"browse: mode={mode.value} does not read order={order!r} -- order (read by mode=runs) sorts "
            f'by a field; mode={mode.value} takes order="recent" (newest first) or no order.'
        )
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


#: browse's `filter` schema: an object of run clauses (or null). Text is accepted (`normalize_text_filter`)
#: but not advertised, so the schema keeps teaching the object.
FILTER_JSON_SCHEMA = WithJsonSchema({"anyOf": [{"additionalProperties": True, "type": "object"}, {"type": "null"}]})


def normalize_text_filter(arguments: dict[str, Any]) -> dict[str, Any]:
    """A TEXT `filter` on mode=projects is the name match `query` (readers send it that way); on any
    other mode it is refused in words, not as a pydantic dump. An object `filter` is mode=runs' clauses."""
    text = arguments.get("filter")
    if not isinstance(text, str):
        return arguments
    text = text.strip()
    if not text:
        return {**arguments, "filter": None}
    mode = BrowseMode(arguments.get("mode") or BrowseMode.PROJECTS)
    if mode is BrowseMode.RUNS:
        raise ToolError(
            f'browse: mode=runs takes `filter` as an object of clauses, not text: by name, query={json.dumps(text)} '
            f'(loose) or filter={{"name": {{"$contains": {json.dumps(text)}}}}}.'
        )
    if mode is not BrowseMode.PROJECTS:
        reads_query = "query" in _BROWSE_MODE_ARGS[mode]
        raise ToolError(
            f"browse: mode={mode.value} has no `filter` (an object of run clauses, mode=runs only). "
            + ("Pass the text as `query`." if reads_query else "To find something by name, use search.")
        )
    query = (arguments.get("query") or "").strip()
    if query and query != text:
        raise ToolError("browse: `filter` text and `query` are the same name match on mode=projects; pass one.")
    return {**arguments, "filter": None, "query": text}


# -- browse: the scope, in the words callers use --------------------------------
#
# mode=projects / runs take `project` or `experiment` (a slug or a uuid) and walk
# the internal `ref` (`kind:<uuid>`), which browse delivery plans its pages from
# (`delivery.browse.invoke` reads `ref` before the tool body runs) and the runs
# list needs as a uuid (`listing._uuid_ref`). So the scope is resolved HERE, once
# per call, before delivery: the pages it then fetches carry their own internal
# refs and never pass through this again. `ref` itself still works, undocumented.

#: The modes whose scope `project` / `experiment` name (the catalog modes read them as their own filters).
_SCOPED_MODES = frozenset({BrowseMode.PROJECTS, BrowseMode.RUNS, BrowseMode.SESSIONS})
_SCOPE_KINDS = ("project", "experiment")


#: What may be looked up as a slug: one path segment of the route `entity` reads with, never a `/`, `?`,
#: `#`, `%`, `..` or space that would steer the GET elsewhere.
_SLUG = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def normalize_browse_scope(arguments: dict[str, Any], find_id: Callable[[str, str], str]) -> dict[str, Any]:
    """The caller's browse arguments with `project` / `experiment` (or a slug in `ref`) turned into
    the internal `ref` = `kind:<uuid>`. `find_id(kind, slug)` is the tenant's own lookup (the one
    `entity` reads with); a uuid is used as given. Refuses two scopes at once, naming the one to keep."""
    mode = BrowseMode(arguments.get("mode") or BrowseMode.PROJECTS)
    if mode not in _SCOPED_MODES:
        return arguments
    if mode is BrowseMode.SESSIONS and arguments.get("experiment"):
        raise ToolError("browse: mode=sessions narrows by `project`, not `experiment`.")
    # `order` counts only as "recent": a field order is mode=runs', refused below in its own words.
    people_asked = sorted(
        name for name in _PEOPLE_FILTER_ARGS
        if arguments.get(name) and (name != "order" or arguments[name] == BrowseOrder.RECENT)
    )
    if mode is BrowseMode.PROJECTS and arguments.get("query"):
        people_asked.append("query")
    if mode is BrowseMode.PROJECTS and people_asked and any(arguments.get(k) for k in ("project", "experiment", "ref")):
        # GET /v1/browse filters its TOP level only, and refuses a filter beside a scope.
        raise ToolError(
            f"browse: {', '.join(people_asked)} narrow the top-level project list, not one project's "
            "contents. Drop `project` / `experiment`, or use mode=runs or mode=sessions with `project`."
        )
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
