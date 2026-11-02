"""Forward the Fleet arm API to its local, separately installed service."""
from __future__ import annotations

import json

import requests
from flask import Response, request, stream_with_context
from abstract_flask import get_bp, register_categories, spec

agent_proxy_bp, logger = get_bp("agent_proxy_bp", __name__)
_DESCRIPTOR = "/usr/share/hugpy/arms.d/agent.json"
_HOP_HEADERS = {"connection", "content-length", "host", "transfer-encoding",
                "keep-alive", "proxy-authenticate", "proxy-authorization",
                "te", "trailer", "upgrade"}


def proxy_agent(rest):
    try:
        with open(_DESCRIPTOR, encoding="utf-8") as fh:
            upstream = json.load(fh)["upstream"].rstrip("/")
        # The Agent systemd unit is a loopback-only service.
        if not upstream.startswith(("http://127.0.0.1:", "http://localhost:")):
            raise ValueError("Agent upstream must be local")
        url = upstream + "/api/agent/" + rest
        if request.query_string:
            url += "?" + request.query_string.decode("ascii")
        headers = {k: v for k, v in request.headers if k.lower() not in _HOP_HEADERS}
        upstream_response = requests.request(
            request.method, url, headers=headers, data=request.get_data(),
            stream=True, timeout=(5, 120), allow_redirects=False)
    except (OSError, KeyError, ValueError, requests.RequestException) as exc:
        return {"error": f"Agent service unavailable: {exc}"}, 503

    response_headers = [(k, v) for k, v in upstream_response.headers.items()
                        if k.lower() not in _HOP_HEADERS]

    def body():
        try:
            yield from upstream_response.raw.stream(65536, decode_content=False)
        finally:
            upstream_response.close()

    return Response(stream_with_context(body()), status=upstream_response.status_code,
                    headers=response_headers, direct_passthrough=True)


# The ``agent`` category is a single raw-request passthrough: every method
# streams to the local service. ``/agent/`` (the index, with an empty ``rest``
# default) and ``/agent/<path:rest>`` are stated as explicit rules on the leaf
# because a trailing-slash index that still feeds the ``rest`` kwarg cannot be
# spelled by dict nesting alone — the raw-proxy adapter the convention allows.
ALL_CATEGORIES = {
    "agent": spec(
        proxy_agent, ["GET", "HEAD", "POST", "PUT", "PATCH", "DELETE"],
        response="native", inputs="path", strict_slashes=True,
        rules=[{"rule": "/agent/", "defaults": {"rest": ""}}, "/agent/<path:rest>"],
    ),
}
register_categories(agent_proxy_bp, ALL_CATEGORIES)
