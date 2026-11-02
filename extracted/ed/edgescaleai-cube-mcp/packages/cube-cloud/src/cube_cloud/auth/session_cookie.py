"""Browser session cookie helpers for the cube-cloud app proxy (Phase 1).

The app proxy lets an account-less browser reach an in-cube web app over the
apex's wildcard subdomains. Auth is carried by a parent-domain cookie holding
the existing ``cmcp_`` API key, so it is valid across every ``<app>-<env>``
subdomain *and* the apex login host.

Everything is derived from ``settings.domain`` (the apex, e.g.
``cube.edgescaleai-cube.com`` in prod, ``cube-dev.edgescaleai-cube.com`` in
dev) rather than hardcoded, so the gate is environment-correct.

Two security primitives live here and are reused verbatim by the middleware:
  * :func:`is_app_subdomain_host` — the host gate that decides where
    cookie-auth is honored (cookie-auth on app subdomains only; the apex and
    its ``/mcp`` + ``/tunnel`` surface stay Bearer-only — spec §4.2 CSRF rule).
  * :func:`validate_next` — the open-redirect guard on the post-login ``next``
    target (spec §4.4).
"""

from __future__ import annotations

from urllib.parse import unquote, urlsplit

from starlette.responses import Response

from cube_cloud.config import settings

# Cookie carrying the cmcp_ key. HttpOnly + Secure + SameSite=Lax, parent-domain
# scoped, 12h fixed max-age (spec §4.2).
SESSION_COOKIE_NAME = "cmcp_session"
SESSION_MAX_AGE = 43200  # 12 hours

# The console's single reserved apex prefix (docs/console-spec.md §4.1). Everything
# the browser UI serves — HTML shell and its JSON API — lives under this one path,
# so the middleware allowlist, the host gate, and the post-login redirect target
# are each a single thing to reason about.
CONSOLE_PREFIX = "/console"

# Percent-decoding passes applied before the traversal check in is_console_path.
# More than one so a double-encoded payload cannot survive a single unquote; kept
# small so a crafted value cannot spin the loop.
_MAX_DECODE_PASSES = 3


def strip_session_cookie(cookie_header: str) -> str:
    """Remove the ``cmcp_session`` cookie from a raw ``Cookie`` header value.

    Shared by both proxy legs — HTTP ``build_request_headers`` and the WS
    ``build_upstream_handshake_headers`` — so the ``cmcp_`` API key the session
    cookie carries is never forwarded to the in-cube app, while the app's own
    cookies are preserved. Returns the filtered header (may be empty).
    """
    kept = []
    for part in cookie_header.split(";"):
        crumb = part.strip()
        if not crumb:
            continue
        cname = crumb.split("=", 1)[0].strip().lower()
        if cname == SESSION_COOKIE_NAME.lower():
            continue
        kept.append(crumb)
    return "; ".join(kept)


def apex_host() -> str:
    """The apex login host, lower-cased. Empty string if unconfigured."""
    return (settings.domain or "").lower()


def cookie_domain() -> str | None:
    """Parent-domain scope for the session cookie (``.<apex>``).

    Returns ``None`` when no apex is configured so the cookie is host-only
    rather than scoped to a bogus domain.
    """
    apex = apex_host()
    return f".{apex}" if apex else None


def is_app_subdomain_host(host: str) -> bool:
    """True iff ``host`` is a strict subdomain of the configured apex.

    The apex itself is **not** an app subdomain — this is the load-bearing
    distinction that keeps the apex's MCP surface Bearer-only even though the
    parent-domain cookie is attached to apex requests too. A leading-label
    requirement (``host.endswith("." + apex)``) defeats suffix-spoofs like
    ``evilcube.edgescaleai-cube.com``.
    """
    apex = apex_host()
    if not apex or not host:
        return False
    h = host.split(":")[0].lower()  # strip any :port
    return h != apex and h.endswith("." + apex)


def set_session_cookie(response: Response, api_key: str) -> None:
    """Attach the session cookie carrying ``api_key`` to ``response``.

    Flags per spec §4.2: HttpOnly, Secure, SameSite=Lax (so the post-login
    top-level navigation back to the app subdomain still sends it),
    parent-domain scoped, 12h max-age.
    """
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=api_key,
        max_age=SESSION_MAX_AGE,
        path="/",
        domain=cookie_domain(),
        secure=True,
        httponly=True,
        samesite="lax",
    )


def clear_session_cookie(response: Response) -> None:
    """Expire the session cookie (logout). Must match name/domain/path."""
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        path="/",
        domain=cookie_domain(),
    )


def is_console_path(next_url: str) -> bool:
    """True iff ``next_url`` is a **relative** path inside the console prefix.

    Requires a leading ``/`` and either exactly ``/console`` or a ``/console/``
    descendant — so ``/consolefoo`` (a prefix-spoof onto some other route) is
    rejected. Any ``..`` segment is rejected too: it stays same-origin, so it is
    not an open redirect, but it would let a crafted ``next`` bounce the browser
    to an arbitrary *other* apex path, and the console never needs it.

    **Both the raw and the percent-decoded forms must pass.** Checking only the
    raw string is not enough: per WHATWG a *double-dot path segment* includes
    ``%2e%2e`` (and ``.%2e`` / ``%2e.``), which browsers collapse during
    normalization — so ``/console/%2e%2e/auth/logout`` would sail through a raw
    ``..`` check and then land the browser on ``/auth/logout``, killing the
    session it had just created. Decoding is looped (bounded) so a
    double-encoded ``%252e%252e`` cannot slip past one pass either.
    """
    path = next_url.split("?", 1)[0].split("#", 1)[0]

    decoded = path
    for _ in range(_MAX_DECODE_PASSES):
        once = unquote(decoded)
        if once == decoded:
            break
        decoded = once

    for candidate in (path, decoded):
        if candidate != CONSOLE_PREFIX and not candidate.startswith(CONSOLE_PREFIX + "/"):
            return False
        if ".." in candidate.split("/"):
            return False
    return True


def validate_next(next_url: str | None) -> str | None:
    """Open-redirect guard for the post-login ``next`` target.

    Two shapes are accepted, and nothing else:

    * an ``https`` URL whose host is a strict subdomain of the configured apex
      (an ``<app>-<env>`` app host) — the browser app-proxy flow; and
    * a **relative** path under :data:`CONSOLE_PREFIX` — the console flow
      (docs/console-spec.md §4.7). Relative on purpose: with no scheme and no
      authority there is no host to spoof, which makes this strictly tighter
      than allowing an absolute apex URL. The apex itself remains an invalid
      *absolute* target.

    Anything else — foreign host, suffix spoof, an absolute apex URL, a
    non-https or ``javascript:``/``data:`` scheme, protocol-relative ``//evil``
    — returns ``None`` so the caller falls back to the default flow rather than
    bouncing the browser somewhere attacker-controlled.
    """
    if not next_url:
        return None
    # Reject backslashes (WHATWG treats `\` in the authority as `/`, so urlsplit's
    # host can disagree with the browser's) and any control char (CR/LF/NUL header
    # or attribute smuggling) before parsing — these never belong in a real next.
    if "\\" in next_url or any(ord(c) < 0x20 for c in next_url):
        return None
    # Relative form. `//host` is protocol-relative — a browser reads it as an
    # authority, so it must never reach the console-path check.
    if next_url.startswith("/"):
        if next_url.startswith("//"):
            return None
        return next_url if is_console_path(next_url) else None
    parts = urlsplit(next_url)
    if parts.scheme != "https":
        return None
    host = (parts.hostname or "").lower()
    if not is_app_subdomain_host(host):
        return None
    return next_url
