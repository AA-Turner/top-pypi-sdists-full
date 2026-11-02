"""The router relays each box's wrapper management API, so core (or a console, or an
operator) talks to ONE address for every box: telemetry out, settings and actions in.

    GET  /v1/boxes                              the boxes: name, url, online, pool, blocked
    *    /v1/boxes/<box>/v1/telemetry[...]      the wrapper's telemetry: cursor tables
                                                (?table=call_log|resource_log|evictions|
                                                operator_actions&since=&limit=) and
                                                /telemetry/state[?wait=&since=] (long-poll)
    *    /v1/boxes/<box>/v1/settings/...        pair settings, quant facts, env profiles
    *    /v1/boxes/<box>/v1/operator/actions... evict / free / restart, and their state
    *    /v1/boxes/<box>/v1/cores               the box's CPU picture
    *    /v1/boxes/<box>/v1/models              the box's models in full: files, quants, predictions
    *    /v1/boxes/<box>/storage                the box's model drive survey

The caller needs the router's admin key (or loopback); the router answers the box with
the box's own key, which never leaves the router. Status, body and content type come
back exactly as the wrapper sent them, plus `X-Hugpy-Box`. A long-poll is held open as
long as the wrapper holds it. The wrapper's /v1/keys is NOT relayed: a box's keys are
managed on the box.
"""
from __future__ import annotations

import aiohttp
from aiohttp import web

from hugpy_core.router.imports.classes import RequestView
from hugpy_core.router.observability import store as S
from hugpy_core.router.serve.keys import REGISTRY, SESSION

RELAYED = ("v1/telemetry", "v1/settings/", "v1/operator/", "v1/cores", "v1/models", "storage")
PASS_HEADERS = ("Content-Type",)


def _admin(request):
    denied = S.KEYS.check(RequestView(request), "admin")
    return None if denied is None else web.json_response(denied[1], status=denied[0])


def _err(status: int, message: str) -> web.Response:
    return web.json_response({"error": {"message": message, "code": status}}, status=status)


async def boxes(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    out = []
    for name, link in request.app[REGISTRY].links.items():
        b = link.box()
        out.append({"name": name, "url": link.url, "online": b.online, "pool": b.pool, "blocked": b.blocked})
    return web.json_response({"boxes": out})


async def relay(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    name, tail = request.match_info["box"], request.match_info["tail"].lstrip("/")
    if not (tail.rstrip("/") == "v1/telemetry" or tail.startswith(RELAYED)):
        return _err(404, f"/{tail} is not relayed (telemetry, settings, operator actions, cores, models, storage)")
    link = request.app[REGISTRY].link(name)
    if link is None:
        return _err(404, f"no box {name!r} behind this router")
    url = f"{link.url}/{tail}" + (f"?{request.query_string}" if request.query_string else "")
    headers = dict(link.headers())
    if request.headers.get("Content-Type"):
        headers["Content-Type"] = request.headers["Content-Type"]
    body = await request.read() if request.can_read_body else None
    try:
        async with request.app[SESSION].request(request.method, url, headers=headers, data=body,
                                                timeout=aiohttp.ClientTimeout(total=None, sock_connect=10)) as r:
            raw = await r.read()
            resp = web.Response(status=r.status, body=raw)
            for h in PASS_HEADERS:
                if h in r.headers:
                    resp.headers[h] = r.headers[h]
            resp.headers["X-Hugpy-Box"] = name
            return resp
    except (aiohttp.ClientError, OSError) as exc:
        return _err(502, f"box {name!r} did not answer: {exc}")
