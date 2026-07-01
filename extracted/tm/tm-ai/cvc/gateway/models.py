"""
Models router — /api/models/* (CVC's resolved model + provider info)
"""

from __future__ import annotations

import logging

from fastapi import APIRouter

logger = logging.getLogger("cvc.gateway.models")

router = APIRouter()


@router.get("/models")
async def list_models():
    """Return the currently-configured model as the catalog entry.
    The vendored api_server only advertises the active model — we mirror that.
    """
    from cvc.gateway.agent import get_config
    import time
    cfg = get_config()
    model = cfg.get("model") or "unknown"
    provider = cfg.get("provider") or "unknown"
    return {
        "object": "list",
        "data": [
            {
                "id": model,
                "object": "model",
                "created": int(time.time()),
                "owned_by": provider,
                "permission": [],
                "root": model,
                "parent": None,
            }
        ],
    }


@router.get("/models/current")
async def current_model():
    """Return the currently-configured provider + model + key-set status.

    v3.3.42 — Surface a clear `model_warning` field when the resolved
    model looks suspicious (e.g. matches a semver shape like "4.0.0"
    rather than a real LLM model name). The dashboard can render this
    as a yellow banner so the user knows to fix their config.
    """
    import re
    from cvc.gateway.agent import get_config

    cfg = get_config()
    raw = cfg.get("raw_cvc_config") or {}
    api_keys = raw.get("api_keys") or {}
    provider = cfg.get("provider") or ""
    api_key = cfg.get("api_key") or ""
    env_key_set = bool(api_key)
    model = cfg.get("model") or ""

    warning = None
    if model and re.fullmatch(r"\d+\.\d+\.\d+", model):
        warning = (
            f"Configured model {model!r} looks like a version number, not a "
            f"model name. The gateway fell back to the provider default — "
            f"please update default_model in ~/.cvc/config.yaml."
        )

    return {
        "provider": provider,
        "model": model,
        "base_url": cfg.get("base_url"),
        "api_key_set": env_key_set,
        "api_key_prefix": api_key[:8] + "..." if api_key else None,
        "api_keys_stored": {k: bool(v) for k, v in api_keys.items()},
        "workspace_path": raw.get("current_workspace"),
        "model_warning": warning,
    }
