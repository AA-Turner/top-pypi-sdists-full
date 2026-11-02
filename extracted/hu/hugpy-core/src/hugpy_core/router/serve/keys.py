"""Typed application keys (aiohttp web.AppKey)."""
from __future__ import annotations

import aiohttp
from aiohttp import web

from hugpy_core.router.links.registry import Registry

REGISTRY = web.AppKey("registry", Registry)
CONTRACTS = web.AppKey("contracts", dict)
SESSION = web.AppKey("session", aiohttp.ClientSession)
# central's derived allocation: (box, model_key) -> the model_workers row (resident,
# state, busy, loading, available, fits_any, fit map per quant per option). Absent =
# no derivation here (the pure router of the tests).
ALLOCATION = web.AppKey("allocation", dict)
# central's recorder for a refusal from an allocated box: fn(box, model, options, reason, status, request_id)
REFUSED = web.AppKey("refused", object)
