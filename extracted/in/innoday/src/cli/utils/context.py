"""Resolving which organization and project a command is about.

There are exactly two ways to address a command:

1. **From the workspace** -- the cwd's ``.innoday/project.yml`` (``--dir`` moves
   where that search starts; it is a variant of this mode, not a third one).
2. **Explicitly** -- ``--org <alias|id> --project <alias|id>``, which must work on
   a machine with nothing cloned.

Precedence is flag, then cwd, then an error naming both.

**Why this resolves aliases to UUIDs rather than passing them through.**
Historically it was load-bearing: ``resolve_organization``/``resolve_project``
resolved the entity for *authorization* while the handler went on to query with
the **raw path parameter** -- 105 handlers did -- so an alias against a UUID
column matched nothing and ``GET /organizations/{org}/releases`` answered ``HTTP
200`` with an **empty list**. The server now normalises path refs in
``require_org_role`` (see ``src/middleware/rbac.py``), so that hole is closed.

This stays anyway, for a different reason: the CLI is the only layer that knows
the user *typed* an alias, so it is the only one that can say "No project 'NOPE'
in this organization. Run ``innoday projects list``" rather than relaying a bare
404 about a string the server never saw the user choose.
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from src.cli.utils.formatters import format_error, format_info

#: A UUID needs no lookup. Anything else is treated as an alias (or a name, which
#: the project routes also accept) and resolved. Deliberately permissive about
#: version/variant -- this only decides whether to spend an API call.
_UUID = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)


def looks_like_uuid(value: str) -> bool:
    return bool(value and _UUID.match(value.strip()))


@dataclass
class Context:
    """The resolved identifiers a command should send.

    ``org_id`` and ``project_id`` are always UUIDs. ``*_ref`` is whatever the
    caller actually typed, kept for messages -- telling someone "project PF" is
    useful in a way that telling them a UUID is not.
    """

    org_id: str
    org_ref: str
    project_id: Optional[str] = None
    project_ref: Optional[str] = None


class ContextError(Exception):
    """Raised when org/project cannot be resolved. Carries printable guidance."""

    def __init__(self, message: str, hint: Optional[str] = None):
        super().__init__(message)
        self.message = message
        self.hint = hint

    def print(self, console) -> None:
        console.print(format_error(self.message))
        if self.hint:
            console.print(format_info(self.hint))


_NO_ORG = (
    "Run from a directory with .innoday/project.yml, or pass "
    "--org <alias|id> --project <alias|id>."
)


async def resolve_context(config, client, *, require_project: bool = True) -> Context:
    """Resolve org (and usually project) to UUIDs, from flags or the cwd.

    ``client`` is an ``InnoDayAPIClient``; it is only used when an alias is not
    already cached locally, so the common path costs nothing.
    """
    org_ref = config.get_current_organization()
    if not org_ref:
        raise ContextError("No organization resolved.", _NO_ORG)

    org_id = await _resolve_org_id(config, client, org_ref)

    project_id = None
    project_ref = config.get_current_project_id()
    if project_ref:
        project_id = await _resolve_project_id(client, org_id, project_ref)
    elif require_project:
        raise ContextError("No project resolved.", _NO_ORG)

    return Context(
        org_id=org_id, org_ref=org_ref, project_id=project_id, project_ref=project_ref
    )


async def _resolve_org_id(config, client, org_ref: str) -> str:
    """Alias or id -> id. Local cache first, then the API.

    The local map is only populated by a workspace, ``config init`` or
    ``orgs env-setup`` -- notably **not** by ``innoday login``. Without the API
    fallback, ``--org bp`` on a freshly-authenticated machine yields an alias with
    no id, and ``_build_api_url`` then omits the ``/organizations/{id}/`` prefix
    entirely and requests a path that does not exist. A 404 instead of an answer.
    """
    if looks_like_uuid(org_ref):
        return org_ref.strip()

    cached = config.get_organization_id(org_ref)
    if cached:
        return cached

    orgs = await _get_json(client, "/organizations")
    match = _match_ref(orgs, org_ref, keys=("alias", "name"))
    if not match:
        raise ContextError(
            f"No organization '{org_ref}' is available to you.",
            "Run `innoday orgs list` to see the ones you can reach.",
        )

    org_id = match.get("id")
    # Cache in memory so a second lookup in the same invocation is free. Not
    # saved: ~/.innoday/config.json is shared by every terminal on this machine,
    # and a persisted "current org" is exactly the global mutable state the
    # cwd-resolution model exists to avoid.
    try:
        config._config.setdefault("organizations", {}).setdefault(org_ref, {})["id"] = (
            org_id
        )
    except Exception:  # noqa: BLE001 -- caching is an optimisation, never a failure
        pass
    return org_id


async def _resolve_project_id(client, org_id: str, project_ref: str) -> str:
    """Alias, name or id -> id, within one organization."""
    if looks_like_uuid(project_ref):
        return project_ref.strip()

    projects = await _get_json(client, f"/organizations/{org_id}/projects")
    match = _match_ref(projects, project_ref, keys=("alias", "name"))
    if not match:
        raise ContextError(
            f"No project '{project_ref}' in this organization.",
            "Run `innoday projects list` to see them.",
        )
    return match.get("id")


def _match_ref(
    items: List[Dict[str, Any]], ref: str, keys=("alias",)
) -> Optional[Dict[str, Any]]:
    """Case-insensitive match on id first, then each key in order.

    Order matters and mirrors the server's ``resolve_project``: id, then alias,
    then name. Only ``name`` is non-unique, and it is last, so a collision can
    only ever shadow itself.
    """
    wanted = ref.strip().lower()
    for item in items:
        if str(item.get("id", "")).lower() == wanted:
            return item
    for key in keys:
        for item in items:
            value = item.get(key)
            if value and str(value).lower() == wanted:
                return item
    return None


async def _get_json(client, endpoint: str) -> List[Dict[str, Any]]:
    response = await client.get(endpoint)
    if response.status_code != 200:
        raise ContextError(
            f"Could not reach InnoDay to resolve context "
            f"(HTTP {response.status_code}).",
            "Check `innoday status`.",
        )
    payload = response.json()
    return payload if isinstance(payload, list) else []
