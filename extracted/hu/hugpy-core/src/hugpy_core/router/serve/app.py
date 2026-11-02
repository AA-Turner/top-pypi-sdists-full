"""The router's aiohttp application: routes, box links, one shared HTTP client."""
from __future__ import annotations

from typing import List, Optional

import aiohttp
from aiohttp import web
from abstract_flask import get_aiohttp_app

from hugpy_core.router.imports import constants as C
from hugpy_core.router.links.registry import Registry
from hugpy_core.router.serve import manage, proxy, relay
from hugpy_core.router.serve.keys import CONTRACTS, REGISTRY, SESSION
from hugpy_core.router.serve.queue import QUEUE, CentralQueue, free_by_registry


async def health(request: web.Request) -> web.Response:   # raw handler: first param named `request`
    return web.json_response({"status": "ok"})


def _merge_categories(left: dict, right: dict) -> dict:
    """Merge route trees, retaining a callable parent as its ``""`` leaf."""
    merged = dict(left)
    for name, value in right.items():
        if name not in merged:
            merged[name] = value
        elif isinstance(merged[name], dict) or isinstance(value, dict):
            first = merged[name] if isinstance(merged[name], dict) else {"": merged[name]}
            second = value if isinstance(value, dict) else {"": value}
            merged[name] = _merge_categories(first, second)
        elif merged[name] is not value:
            raise ValueError(f"duplicate aiohttp category route: {name}")
    return merged


def create_app(boxes: List[dict], session: Optional[aiohttp.ClientSession] = None, *,
               models_handler=None, categories=None, middlewares=None) -> web.Application:
    # abstract_flask aiohttp convention: FLAT {category: {route_name: handler}} ->
    # GET+POST on /{category}/{route_name} (+ trailing slash). Every handler here is
    # RAW (first param named `request`): the request is passed straight through and
    # its web.Response/web.StreamResponse returned unchanged. Categories are chosen
    # so the URLs match the originals exactly (C.PROXY_ROUTES fans out to proxy.handle).
    models = models_handler or proxy.models
    ALL_CATEGORIES = {
        "v1": {
            "health": health,            # /v1/health
            "models": models,            # /v1/models
            "completions": proxy.handle, # /v1/completions
            "embeddings": proxy.handle,  # /v1/embeddings
            "summarize": proxy.handle,   # /v1/summarize
            "keywords": proxy.handle,    # /v1/keywords
            "queue": manage.queue,       # /v1/queue
            "telemetry": manage.telemetry,  # /v1/telemetry
            "boxes": relay.boxes,        # /v1/boxes — core's view of every box
            "chat": {"completions": proxy.handle},  # /v1/chat/completions
            "audio": {
                "transcriptions": proxy.handle,     # /v1/audio/transcriptions
                "translations": proxy.handle,       # /v1/audio/translations
                "speech": proxy.handle,             # /v1/audio/speech
            },
            "images": {
                "generations": proxy.handle,        # /v1/images/generations
                "edits": proxy.handle,              # /v1/images/edits
                "variations": proxy.handle,         # /v1/images/variations
            },
            "videos": {"generations": proxy.handle},  # /v1/videos/generations
            "router": {"state": manage.state},         # /v1/router/state
        },
        "health": health,                           # /health (single-segment, callable leaf)
    }
    # The abstract_flask aiohttp factory owns the complete convention route
    # map. Basic Core passes its own categories here as well.
    if categories:
        ALL_CATEGORIES = _merge_categories(ALL_CATEGORIES, categories)
    async def _start(app):
        app[SESSION] = session or aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=None, sock_connect=C.CONNECT_TIMEOUT_S))
        app[REGISTRY].start(app[SESSION])

    async def _stop(app):
        await app[REGISTRY].stop()
        if session is None:
            await app[SESSION].close()

    app = get_aiohttp_app(categories=ALL_CATEGORIES, middlewares=middlewares,
                          on_startup=[_start])
    # The adapter has no client_max_size option yet. Preserve the original 1 GiB
    # upload bound for audio/image requests forwarded through the router.
    app._client_max_size = 1024 ** 3
    app[REGISTRY] = Registry(boxes)
    app[CONTRACTS] = {}
    app[QUEUE] = CentralQueue()
    app[QUEUE].attach(app[REGISTRY], free_by_registry(app[REGISTRY]))
    app.on_cleanup.append(_stop)

    # Kept NATIVE — not expressible as a plain GET/POST /{category}/{route_name}:
    app.router.add_route("*", "/v1/keys", manage.keys)                   # any-method (GET list / POST create)
    app.router.add_post("/v1/keys/{kid}/revoke", manage.revoke)          # {kid} mid-path param (match_info)
    app.router.add_route("*", "/v1/boxes/{box}/{tail:.*}", relay.relay)  # wildcard catch-all, any-method
    return app
