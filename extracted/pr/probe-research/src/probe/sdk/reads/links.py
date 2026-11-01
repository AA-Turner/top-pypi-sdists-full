"""Dashboard URLs for the entities an agent creates and closes.

CLI, SDK and MCP identify entities by uuid, unclickable for a human. This is the one
place that turns a uuid into a link, so no caller (or model) needs the dashboard's routes.

The hard part is the dashboard origin: the API base URL is NOT reliably its sibling
(hosted MCP pods point ``PROBE_BASE_URL`` at an in-cluster Service,
``deploy/mcp/k8s.yaml``, naming no public host). So: an explicit override, one
certain derivation, else ``None`` (:func:`dashboard_base_url`).
"""

from __future__ import annotations

import os
from functools import lru_cache
from urllib.parse import urlsplit

# Route segment per kind, mirroring dashboard/src/app. Only these three have a page;
# artifact, group and document render INSIDE one of them, so they get no link.
#
# A SESSION lost its page when the digest cutover deleted `/sessions/[id]`: a link
# to a 404 is worse than none. Content: `GET /v1/sessions/{id}/transcript`.
_ROUTES = {
    "run": "runs",
    "experiment": "experiments",
    "project": "projects",
}

#: Kinds whose page is NESTED under another entity's: (parent segment, own segment).
#: A trial's page is the canonical shareable rollout link but needs the RUN id too,
#: so it cannot be a row in `_ROUTES`.
_NESTED_ROUTES = {
    "trial": ("runs", "trials"),
}

#: Set when the API host does not name the dashboard (self-hosted, hosted MCP). Never guessed.
DASHBOARD_URL_ENV = "PROBE_DASHBOARD_URL"


@lru_cache(maxsize=8)
def _derive(api_base_url: str) -> str | None:
    """Dashboard origin implied by an API base URL, or None if it implies none.

    Only an ``api.`` label on an https host is read (``api.research.prbe.ai`` ->
    ``research.prbe.ai``). A plain host, bare IP, in-cluster Service or localhost
    API may have its dashboard elsewhere or nowhere, so nothing else is inferred.

    Cached: the MCP annotates every node of every browse response.
    """
    parts = urlsplit(api_base_url)
    # http:// is in-cluster/localhost, never a public dashboard.
    if parts.scheme != "https" or not parts.hostname:
        return None
    host = parts.hostname
    if not host.startswith("api."):
        return None
    remainder = host[len("api.") :]
    # `api.` alone or `api.localhost` leaves nothing addressable.
    if "." not in remainder:
        return None
    return f"https://{remainder}"


def dashboard_base_url(api_base_url: str | None = None) -> str | None:
    """Public dashboard origin, or ``None`` when it cannot be known.

    ``PROBE_DASHBOARD_URL`` wins outright.

    ``None`` is a real answer: no link costs one navigation, a WRONG one a trusted
    404. Never guess the public host; a self-hosted install would get links into
    somebody else's tenant.
    """
    explicit = (os.environ.get(DASHBOARD_URL_ENV) or "").strip()
    if explicit:
        return explicit.rstrip("/")
    if api_base_url is None:
        # Lazy: resolving config reads the context file; some paths already hold a base URL.
        from ..settings.settings import resolve

        api_base_url = resolve().base_url
    return _derive(api_base_url.rstrip("/"))


def entity_url(
    kind: str,
    entity_id: str | None,
    *,
    parent_id: str | None = None,
    api_base_url: str | None = None,
) -> str | None:
    """Link to one entity's dashboard page, or ``None`` if it has no page.

    ``None`` for: unroutable kind, missing id, nested kind without ``parent_id``, or
    unknown dashboard origin; callers say nothing. A half-built `/runs//trials/<id>`
    looks real and 404s, which a reader blames on the record.
    """
    if not entity_id:
        return None
    base = dashboard_base_url(api_base_url)
    if not base:
        return None
    nested = _NESTED_ROUTES.get(str(kind))
    if nested:
        parent_route, own_route = nested
        if not parent_id:
            return None
        return f"{base}/{parent_route}/{parent_id}/{own_route}/{entity_id}"
    route = _ROUTES.get(str(kind))
    if not route:
        return None
    return f"{base}/{route}/{entity_id}"
