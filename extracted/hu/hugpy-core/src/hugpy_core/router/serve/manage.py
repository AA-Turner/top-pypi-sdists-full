"""The router's management API (admin key, except from loopback):

    GET  /v1/router/state                  every box: link mode, online, residents, catalog size,
                                           room; the contracts the router has sent
    GET  /v1/queue                         central's queue above the boxes: the waiting tickets in order
    GET  /v1/telemetry?since=<id>&limit=<n> the router's own call rows (route_log), cursor
    GET  /v1/keys[?all=1], POST /v1/keys, POST /v1/keys/<id>/revoke
    GET  /v1/boxes, * /v1/boxes/<box>/v1/...  each box's wrapper API, relayed (serve/relay.py)
"""
from __future__ import annotations

import json

from aiohttp import web

from hugpy_core.router.imports.classes import RequestView
from hugpy_core.router.observability import store as S
from hugpy_core.router.serve.keys import CONTRACTS, REGISTRY
from hugpy_core.router.serve.queue import QUEUE

MAX_LIMIT = 5000


def _admin(request):
    denied = S.KEYS.check(RequestView(request), "admin")
    return None if denied is None else web.json_response(denied[1], status=denied[0])


async def state(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    reg = request.app[REGISTRY]
    boxes = []
    for name, link in reg.links.items():
        b = link.box()
        boxes.append({"name": name, "url": link.url, "link": link.mode, "online": b.online, "pool": b.pool,
                      "blocked": b.blocked, "room_gpu": b.room_gpu, "models": len(b.models),
                      'observation_identity': b.observation_identity,
                      'observation_generation': b.observation_generation,
                      "residents": [r.__dict__ for r in b.residents]})
    from hugpy_core.router.core.types import CallSpec
    contracts = [{"box": k[0], **CallSpec(model=k[1],
                  options=v[0] if isinstance(v, tuple) else v,
                  knobs_json=v[1] if isinstance(v, tuple) else '{}').execution_request(),
                  'worker_identity': v[2] if isinstance(v, tuple) and len(v) == 3 else None}
                 for k, v in request.app[CONTRACTS].items()]
    return web.json_response({"boxes": boxes, "contracts": contracts})


async def queue(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    q = request.app.get(QUEUE)
    return web.json_response(q.snapshot() if q is not None else {"policy": None, "tickets": []})


async def telemetry(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    try:
        since = int(request.query.get("since", "0"))
        limit = max(1, min(int(request.query.get("limit", "500")), MAX_LIMIT))
    except ValueError:
        return web.json_response({"error": {"message": "since and limit must be integers"}}, status=400)
    rows = []
    for r in S.STORE.read("SELECT * FROM route_log WHERE id > ? ORDER BY id LIMIT ?", (since, limit)):
        row = dict(r)
        for k in ("decision", "attempts"):
            if isinstance(row.get(k), str):
                row[k] = json.loads(row[k])
        rows.append(row)
    return web.json_response({"table": "route_log", "rows": rows, "next": rows[-1]["id"] if rows else since,
                              "more": len(rows) == limit})


async def keys(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    if request.method == "GET":
        return web.json_response({"keys": S.KEYS.list_keys(include_revoked=request.query.get("all") == "1")})
    try:
        body = await request.json()
        k = S.KEYS.create(body.get("name"), body.get("scope") or "use", body.get("expires_days"),
                          created_by=body.get("created_by") or request.remote)
    except ValueError as exc:
        return web.json_response({"error": {"message": str(exc)}}, status=400)
    return web.json_response({**k, "note": "store this key now; it is not shown again"}, status=201)


async def revoke(request: web.Request) -> web.Response:
    if (d := _admin(request)) is not None:
        return d
    kid = request.match_info["kid"]
    if not S.KEYS.revoke(kid):
        return web.json_response({"error": {"message": "no such active key"}}, status=404)
    return web.json_response({"id": kid, "revoked": True})
