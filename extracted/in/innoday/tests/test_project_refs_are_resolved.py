"""Every inbound project reference is resolved, or exempt **by name**.

`normalize_path_refs` makes a project **path** parameter arrive resolved, so a
handler cannot get that wrong. A `project_id` that arrives as a **query
parameter** or a **body field** is not a path param, and the only thing standing
between it and a UUID column is an author remembering to call
`resolve_project_ref` -- which is the same "the next author will forget" trap the
normaliser exists to remove, and it had already been forgotten **ten times** when
#635 was reviewed: `get_release_by_version` answered 200 with an invented release,
`update_release` put the alias into a validated FK, and
`POST /organizations/{org}/tickets` 404'd on a project the caller owns.

So the rule is enforced structurally rather than remembered:

* The routes are read from **the app**, not from a list kept by hand. A site that
  is added and forgotten is exactly the case a hand-kept list misses.
* An exemption is a **named entry** with a reason, and the assertion is an
  equality, so a stale exemption fails too. A pattern-matched filter would let
  new cases opt out silently -- how `test_auth_tiers.py` came to certify 13 admin
  routes it was not checking.
* Resolution is detected by **parsing the handler for a call**, not by searching
  its text. The same test file records why: prose counts as source to a substring
  search, and the one handler exempted below *mentions* `resolve_project_ref` in a
  comment explaining why it does not call it.
"""

import ast
import inspect
import textwrap

from fastapi.routing import APIRoute
from pydantic import BaseModel

from src.api.app import app

#: Inbound refs that deliberately go unresolved, keyed by
#: `handler` -> `site`, with the reason. Add to this only with one.
EXEMPT = {
    ("tickets.create_ticket", "body:TicketCreate.project_id"): (
        "The board-scoped create reads `board.project_id`, never the body's -- a "
        "board cannot exist without a project, so the body field is inert on this "
        "route. Resolving it would add a 404 for a value that changes nothing."
    ),
}

#: The traversal below walks FastAPI's route tree, which changed shape in 0.140
#: (`include_router` now nests an `_IncludedRouter` instead of flattening). A
#: version that nests it differently again would find **no routes at all** and
#: this file would pass while checking nothing -- the failure mode
#: `test_auth_tiers.py` hit with a non-recursive glob. These two pin it: the count
#: is a floor, and the canary is a site that must always be found.
#:
#: A *floor*, deliberately below the 12 sites there are today: it exists to catch a
#: traversal that half works -- body-model introspection breaking leaves the four
#: query sites and would otherwise pass -- not to make deleting a route fail.
MINIMUM_SITES = 8
CANARY = ("releases.list_releases", "query:project_id")


def _api_routes(routes):
    """Every `APIRoute`, flattened or nested behind an `_IncludedRouter`."""
    for route in routes:
        if isinstance(route, APIRoute):
            yield route
            continue
        inner = getattr(route, "original_router", None) or getattr(
            route, "router", None
        )
        if inner is not None:
            yield from _api_routes(inner.routes)


def _org_guarded(route) -> bool:
    """True when `require_org_role` is somewhere in this route's dependency tree.

    Transitively, for the reason `test_every_auth_dep_resolves_a_real_user` gives:
    the guard is a factory, so the dependency FastAPI records is its inner
    closure.
    """
    stack = list(route.dependant.dependencies)
    while stack:
        dep = stack.pop()
        call = getattr(dep, "call", None)
        if call is not None and "require_org_role" in getattr(call, "__qualname__", ""):
            return True
        stack.extend(dep.dependencies)
    return False


def _body_models(route):
    """Pydantic models reachable from this route's body, outermost first.

    Nested because FastAPI wraps multiple body params (and `Form` fields) in a
    synthetic model, so the declared one is a *field* of what `body_field` names.
    """
    field = getattr(route, "body_field", None)
    if field is None:
        return []
    found, seen, stack = [], set(), [field.field_info.annotation]
    while stack:
        annotation = stack.pop()
        if not (inspect.isclass(annotation) and issubclass(annotation, BaseModel)):
            continue
        if annotation in seen:
            continue
        seen.add(annotation)
        found.append(annotation)
        stack.extend(f.annotation for f in annotation.model_fields.values())
    return found


def _calls_the_resolver(route) -> bool:
    """Does the handler *call* `resolve_project_ref`?

    Parsed, not grepped. A comment naming the function is not a call, and this
    file's one exemption is a handler whose comment says precisely that.
    """
    try:
        source = textwrap.dedent(inspect.getsource(route.endpoint))
    except OSError:  # pragma: no cover -- source is always available here
        return False
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "id", None) or getattr(func, "attr", None)
            if name == "resolve_project_ref":
                return True
    return False


def _inbound_sites():
    """`{(handler, site): resolved}` for every org-guarded inbound project ref.

    A *site* is where the reference arrives: `query:project_id`, or
    `body:<Model>.project_id`. Keyed by handler rather than by path so an
    exemption survives a route being renamed or re-prefixed -- and so it names
    something a reader can open.
    """
    sites = {}
    for route in _api_routes(app.routes):
        if not _org_guarded(route):
            # Not this rule's subject. The `/ui` pages and `PUT /auth/me/identities`
            # carry their own resolution (`_resolve_org`, `_project_for_caller`)
            # and have no org path param for the guard to read.
            continue
        resolved = _calls_the_resolver(route)
        handler = (
            f"{route.endpoint.__module__.split('.')[-1]}.{route.endpoint.__name__}"
        )

        for param in route.dependant.query_params:
            if "project_id" in (param.name, getattr(param, "alias", None)):
                sites[(handler, "query:project_id")] = resolved

        for model in _body_models(route):
            if "project_id" in model.model_fields:
                sites[(handler, f"body:{model.__name__}.project_id")] = resolved

    return sites


def test_the_enumeration_still_finds_the_routes():
    """Guards the guard: a traversal that finds nothing must fail, not pass."""
    sites = _inbound_sites()
    assert len(sites) >= MINIMUM_SITES, (
        f"only {len(sites)} inbound project refs found -- the route walk or the "
        "body-model introspection has stopped seeing them (FastAPI route-tree "
        f"shape?), not the API that shrank. Found: {sorted(sites)}"
    )
    assert CANARY in sites, sorted(sites)


def test_every_inbound_project_ref_is_resolved():
    """A query param or body `project_id` must pass through `resolve_project_ref`.

    Unresolved, it is compared against a UUID column: as a filter that is
    `200 []`, as a lookup a spurious 404, and as a write a validated
    non-deferrable FK refusing the row (`releases_project_id_fkey`) -- measured on
    Postgres, invisible on SQLite. See "An alias in a URL" in CLAUDE.md.
    """
    unresolved = {site for site, resolved in _inbound_sites().items() if not resolved}
    exempt = set(EXEMPT)

    assert unresolved == exempt, (
        "inbound project refs that never reach resolve_project_ref:\n  "
        + "\n  ".join(f"{h} -- {s}" for h, s in sorted(unresolved - exempt))
        + "\nexemptions that no longer apply (delete them):\n  "
        + "\n  ".join(f"{h} -- {s}" for h, s in sorted(exempt - unresolved))
    )
