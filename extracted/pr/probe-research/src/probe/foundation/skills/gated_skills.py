"""Which gated skills this person may see (`GET /v1/me/gated-skills`, A24), kept on disk for the session-start
skill sync (`root_skills_core.load_allowed_gated`): at sign-in, and on the daemon's message poll at most hourly."""

from __future__ import annotations

import json
import time

from probe.foundation.skills import root_skills_core as core

GATED_SKILLS_PATH = "/v1/me/gated-skills"
#: One try, this long at most: a sign-in or a poll never waits longer on it.
FETCH_TIMEOUT_S = 5.0
#: A kept answer younger than this is not asked again (well inside `core.GATED_FRESH_S`).
REFRESH_S = 3600.0
#: After a failed ask, this process waits this long before the next (`refresh_if_due`).
RETRY_AFTER_FAILURE_S = 600.0
#: Answers that mean "no gated skill" for sure: a refused key, or a server without the route.
_DENIED_STATUSES = (401, 403, 404)

_next_try_at = 0.0


def fetch_allowed_gated(base_url: str, token: str, timeout: float = FETCH_TIMEOUT_S) -> "tuple[str, ...] | None":
    """The server's list; () for a sure no (`_DENIED_STATUSES`); None when unknown (offline, a 5xx, a
    redirect, a body that is not the list). Never raises."""
    import urllib.error
    import urllib.request

    class _NoRedirect(urllib.request.HTTPRedirectHandler):
        """Never followed: urllib would carry the bearer wherever a redirect points."""

        def redirect_request(self, request, response, status, message, headers, new_url):  # noqa: ANN001, ARG002
            return None

    try:
        from probe.foundation.tls.tls import ssl_context

        opener = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=ssl_context()))
        request = urllib.request.Request(base_url.rstrip("/") + GATED_SKILLS_PATH,
                                         headers={"Authorization": f"Bearer {token}", "User-Agent": "probe-cli"})
        with opener.open(request, timeout=timeout) as response:
            body = json.loads(response.read(64 * 1024) or b"{}")
    except urllib.error.HTTPError as exc:
        return () if exc.code in _DENIED_STATUSES else None
    except Exception:  # noqa: BLE001 -- offline, a timeout, a bad body: no answer
        return None
    skills = body.get("skills") if isinstance(body, dict) else None
    if not isinstance(skills, list):
        return None
    return tuple(s for s in skills if isinstance(s, str))


def keep_gated_skills(base_url: str, token: str, *, is_sign_in: bool = False) -> bool:
    """Ask, and keep the answer for the hook. No answer keeps the last one, except at a sign-in, which may be
    another person's: then the kept answer goes (fail closed). True when an answer was kept. Never raises."""
    try:
        allowed = fetch_allowed_gated(base_url, token)
        if allowed is None:
            if is_sign_in:
                core.clear_allowed_gated()
            return False
        core.save_allowed_gated(allowed)
        return True
    except Exception:  # noqa: BLE001 -- the hook then reads no answer: no gated skill
        return False


def is_refresh_due(now: "float | None" = None) -> bool:
    """No kept answer, an unreadable one, or one older than REFRESH_S."""
    try:
        at = json.loads(core.get_gated_cache_path().read_text(encoding="utf-8"))["at"]
        age = (time.time() if now is None else now) - float(at)
    except Exception:  # noqa: BLE001
        return True
    return not 0 <= age < REFRESH_S


def refresh_if_due(base_url: str, token: str) -> None:
    """The daemon poll's refresh: ask only when the kept answer is due and this process has not just failed."""
    global _next_try_at
    if not token or time.monotonic() < _next_try_at or not is_refresh_due():
        return
    if not keep_gated_skills(base_url, token):
        _next_try_at = time.monotonic() + RETRY_AFTER_FAILURE_S
