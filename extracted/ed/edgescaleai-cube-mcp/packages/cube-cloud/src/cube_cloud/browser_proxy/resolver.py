"""Host <-> Teleport app name mapping for the browser app proxy (Phase 2a).

POC convention (spec §5 Phase 2a): the app-subdomain host label IS already
the qualified Teleport app name `expose` produces (``<app>-<env>``, see
``tools/expose.py::_qualified_app_name``) -- e.g. host
``f1-points-tracker-cube-66odzn95.cube-dev.edgescaleai-cube.com`` resolves to
Teleport app ``f1-points-tracker-cube-66odzn95``. Generalizing this to a real
per-app registry (arbitrary developer apps, not a hardcoded label match) is
Phase 4.

BOTH directions live here on purpose. ``resolve_app_name`` parses an inbound
Host; ``browser_app_url`` builds the URL we publish for an app. They share one
label rule (``_APP_LABEL_RE``), which is what makes "we published this URL" and
"the proxy will route it" the same predicate rather than two notions that drift
-- see the round-trip invariant on ``browser_app_url``. Every surface that tells
a human how to reach an exposed app -- the console card (``console/reads.py``)
and the ``expose``/``list_exposed``/``app_list`` tools -- goes through the
builder here, so there is exactly one answer to "what is this app's URL".

**This module must never import from ``cube_cloud.tools`` or
``cube_cloud.teleport``.** ``browser_proxy/authz.py`` imports ``tools.expose``
and ``tools.expose`` imports this module; that is only safe because the import
graph stays acyclic at module level (this file imports ``re`` +
``auth.session_cookie``, and ``browser_proxy/__init__.py`` imports nothing).
Adding a ``tools``/``teleport`` import here closes the cycle for real.
"""

from __future__ import annotations

import re

from cube_cloud.auth import session_cookie

# A single DNS label -- the exact charset `_qualified_app_name` sanitizes to
# at expose time. Rejecting anything else here (rather than forwarding a
# crafted/spoofed Host-derived string further down the dial path) keeps a
# malicious Host header from reaching tbot's cert generation, which embeds
# app_name directly into a YAML config file
# (tunnel/relay.py::AppCertManager._generate_cert).
_APP_LABEL_RE = re.compile(r"^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$")


def is_app_label(label: str) -> bool:
    """True iff ``label`` is a single DNS label this proxy would accept back.

    The same rule `resolve_app_name` applies to a Host-derived label, exported so
    a WRITE path can refuse a name up front instead of storing one no published
    URL could ever reach. `tools/expose.py` uses it on the `public_addr`-override
    path, which takes `app_name` verbatim instead of sanitizing it.
    """
    return bool(_APP_LABEL_RE.fullmatch(label or ""))


def is_http_app(app_uri: str) -> bool:
    """True iff an exposed app is one the browser proxy can serve at all.

    The proxy speaks HTTP and WebSocket only (`http_proxy.py`, `ws_proxy.py`), so
    a ``tcp://`` app (mosquitto, postgres) has NO browser URL and is reachable
    only through `app_proxy`'s local tunnel. Anything not explicitly ``tcp://``
    counts as HTTP -- the same default `tbot_manager._fetch_app_types` falls back
    to, so the two can never disagree about one app.
    """
    return not (app_uri or "").strip().lower().startswith("tcp://")


def browser_app_url(app_name: str) -> str:
    """The browser-app-proxy URL for an exposed app: ``https://<app_name>.<apex>``.

    THE url to publish anywhere a human is told how to reach an exposed app: it
    authenticates with the same login cube-mcp already issues. The ``public_addr``
    stored on the Teleport app is deliberately NOT this -- reaching it needs a
    Teleport account nobody outside the platform team has, so it stays in Apollo
    for Teleport's own routing and is never rendered.

    ``app_name`` must be the QUALIFIED name (``<app>-<env>``) that
    `tools/expose.py::_qualified_app_name` produces, because `resolve_app_name`
    strips the apex and uses the remaining label AS the Teleport app name to dial;
    a bare app name looks right and fails at dial time.

    Returns "" -- never a half-built URL -- when no apex is configured or when
    ``app_name`` is not a label the parser above would accept. That is the
    round-trip invariant this pair guarantees: for any non-empty result,
    ``resolve_app_name(<host of result>) == app_name``. A caller that gets ""
    must publish no URL at all rather than one that cannot route.
    """
    apex = session_cookie.apex_host().strip().strip("/")
    if not apex or not is_app_label(app_name):
        return ""
    return f"https://{app_name}.{apex}"


# Why an app has no browser URL, in words safe to publish. Each names no host and
# no other tenant's app, so they are safe in output that crosses a company
# boundary. `app_proxy` is named here and ONLY here: these are the cases where it
# is the sole way in, not an alternative to a URL that exists.
NO_APEX_REASON = "this stack has no public apex configured -- use app_proxy"
TCP_APP_REASON = "TCP app; the browser proxy serves HTTP/WebSocket only -- use app_proxy"
BAD_LABEL_REASON = "the app name is not a routable DNS label -- use app_proxy"


def browser_app_url_or_reason(app_name: str, app_uri: str = "") -> tuple[str, str]:
    """``(url, reason)`` -- the browser URL, or a publishable reason there is none.

    Exactly one side is non-empty. Tool text renders ``url or f"none -- {reason}"``
    so every response ANSWERS "what URL do I hand a human?": an agent given a
    silently missing URL invents one, or falls back to the account-gated Teleport
    address this exists to stop advertising.
    """
    if not is_http_app(app_uri):
        return "", TCP_APP_REASON
    url = browser_app_url(app_name)
    if url:
        return url, ""
    if not session_cookie.apex_host().strip().strip("/"):
        return "", NO_APEX_REASON
    return "", BAD_LABEL_REASON


def resolve_app_name(host: str) -> str | None:
    """Return the Teleport app name a proxied request's Host resolves to.

    Returns ``None`` when ``host`` is not a valid app-subdomain request --
    callers must treat that as "no such route" (404) and never attempt a
    dial. This function does no I/O and makes no trust decision beyond
    hostname shape; authentication and authorization happen elsewhere.
    """
    if not session_cookie.is_app_subdomain_host(host):
        return None
    h = host.split(":")[0].lower()
    apex = session_cookie.apex_host()
    label = h[: -(len(apex) + 1)]  # strip the trailing "."+apex
    if not _APP_LABEL_RE.fullmatch(label):
        return None
    return label
