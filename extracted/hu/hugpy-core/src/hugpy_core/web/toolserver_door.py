"""Core's door to its toolserver: everything under ``/toolserver/`` is the toolserver's own API.

``<core>/toolserver/<path>`` goes to ``<HUGPY_CORE_TOOLSERVER_URL>/<path>`` with the caller's
method, query, body and credentials as sent, and the toolserver's answer (event streams included)
comes back as it is. Core adds no credential of its own, so the toolserver's gate decides exactly
as if the caller had reached it directly: a Station that stores ``<core>/toolserver`` as its
toolserver address and holds a toolserver token works unchanged.

This is not the ``/ts/{categories,list,call}`` relay in ``agent_tools.py``: that one takes a Core
admin key and calls the toolserver with Core's operator token.
"""
from __future__ import annotations

from urllib.parse import quote

from hugpy_core.config import settings
from hugpy_core.web import arm_proxy

PREFIX = "/toolserver"
# Hop-by-hop names only: Authorization, X-Operator-Token and Cookie are the caller's own
# toolserver credentials and must arrive.
DROP_REQUEST = {"connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
                "te", "trailer", "transfer-encoding", "upgrade", "host"}


class ToolserverDoor:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        path = environ.get("PATH_INFO") or "/"
        if path != PREFIX and not path.startswith(PREFIX + "/"):
            return self.app(environ, start_response)
        upstream = (settings.TOOLSERVER_URL or "").rstrip("/")
        # PATH_INFO is the decoded path carried as latin-1; send the same bytes on, re-encoded.
        rest = path[len(PREFIX):] or "/"
        target = upstream + quote(rest.encode("latin-1"), safe="/:@!$&'()*+,;=-._~")
        query = environ.get("QUERY_STRING")
        if query:
            target += "?" + query
        headers = arm_proxy.request_headers(environ, DROP_REQUEST)
        # The toolserver lets a direct loopback caller read its tool catalog without a token, and
        # Core itself connects from loopback. Always mark the request as forwarded, so every
        # relayed caller has to present a credential.
        hops = [hop for hop in (environ.get("HTTP_X_FORWARDED_FOR"), environ.get("REMOTE_ADDR")) if hop]
        headers["X-Forwarded-For"] = ", ".join(hops) or "unknown"
        return arm_proxy.forward(
            environ, start_response, target, headers, chunk_size=None,
            unreachable=lambda exc: {
                "message": f"Core's toolserver is unreachable at {upstream}: {type(exc).__name__}",
                "upstream": upstream})


def wrap(app):
    return ToolserverDoor(app)
