"""CVC Dashboard — Providers & Credentials REST API.

Surfaces Phase-1 Category-1 plumbing (provider registry + CredentialPool +
FallbackChain) over HTTP so the Vite/React dashboard and CLI stay in sync.

Mounted onto the FastAPI app via ``register_providers_routes(app)`` from
``cvc/gateway.py``.

Endpoints
─────────
GET    /api/providers                       → list all profiles + capability flags
GET    /api/providers/{name}                → single provider profile detail
GET    /api/credentials                     → all credentials, grouped by provider (masked)
POST   /api/credentials                     → add a credential
DELETE /api/credentials/{provider}/{cid}    → remove credential
POST   /api/credentials/{provider}/{cid}/reset → manually clear exhausted state
GET    /api/credentials/stats               → pool stats (totals, exhausted counts)
GET    /api/fallback/preview                → resolve a (provider, model) into an ordered chain

All write paths are guarded — secrets are never echoed back; only the last
6 characters of the access_token are returned for display.
"""
from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, HTTPException, Request

logger = logging.getLogger(__name__)


# ─── Helpers ───────────────────────────────────────────────────────────────


def _profile_to_dict(profile: Any) -> dict[str, Any]:
    return {
        "name": profile.name,
        "aliases": list(profile.aliases or []),
        "env_vars": list(profile.env_vars or []),
        "base_url": profile.base_url,
        "auth_type": profile.auth_type,
        "api_mode": profile.api_mode,
        "fallback_models": list(profile.fallback_models or []),
        "fixed_temperature": profile.fixed_temperature,
        "default_max_tokens": profile.default_max_tokens,
        "supports_streaming": profile.supports_streaming,
        "supports_tools": profile.supports_tools,
        "supports_reasoning": profile.supports_reasoning,
        "supports_prompt_cache": profile.supports_prompt_cache,
    }


def _mask_token(token: str) -> str:
    if not token:
        return ""
    if len(token) <= 10:
        return "•" * len(token)
    return f"{'•' * 6}{token[-6:]}"


def _credential_to_dict(cred: Any) -> dict[str, Any]:
    return {
        "id": cred.id,
        "provider": cred.provider,
        "label": cred.label,
        "auth_type": cred.auth_type,
        "source": cred.source,
        "priority": cred.priority,
        "access_token_masked": _mask_token(cred.access_token or ""),
        "base_url": cred.base_url,
        "expires_at": cred.expires_at,
        "last_status": cred.last_status,
        "last_status_at": cred.last_status_at,
        "last_error_code": cred.last_error_code,
        "last_error_message": cred.last_error_message,
        "last_error_reset_at": cred.last_error_reset_at,
        "request_count": cred.request_count,
    }


# ─── Route registration ─────────────────────────────────────────────────────


def register_providers_routes(app: FastAPI) -> None:
    """Attach Providers & Credentials endpoints to the FastAPI app."""

    @app.get("/api/providers")
    async def _list_providers() -> dict[str, Any]:
        from cvc.providers import all_profiles

        profiles = all_profiles()
        return {
            "providers": [_profile_to_dict(p) for p in profiles],
            "count": len(profiles),
        }

    @app.get("/api/providers/{name}")
    async def _get_provider(name: str) -> dict[str, Any]:
        from cvc.providers import get_provider

        profile = get_provider(name)
        if not profile:
            raise HTTPException(status_code=404, detail=f"unknown provider: {name}")
        return _profile_to_dict(profile)

    # ─── Credentials ────────────────────────────────────────────────────────

    @app.get("/api/credentials")
    async def _list_credentials(provider: str | None = None) -> dict[str, Any]:
        from cvc.agent.credential_pool import CredentialPool

        pool = CredentialPool.get_instance()
        creds = pool.list(provider)
        grouped: dict[str, list[dict[str, Any]]] = {}
        for c in creds:
            grouped.setdefault(c.provider, []).append(_credential_to_dict(c))
        return {"credentials": grouped, "total": len(creds)}

    @app.post("/api/credentials")
    async def _add_credential(request: Request) -> dict[str, Any]:
        from cvc.agent.credential_pool import (
            AUTH_TYPE_API_KEY,
            SOURCE_USER,
            CredentialPool,
            PooledCredential,
        )

        body = await request.json()
        required = {"provider", "label", "access_token"}
        missing = required - set(body)
        if missing:
            raise HTTPException(status_code=400, detail=f"missing fields: {sorted(missing)}")

        cred = PooledCredential(
            provider=str(body["provider"]),
            id=str(body.get("id") or _gen_id()),
            label=str(body["label"]),
            auth_type=str(body.get("auth_type") or AUTH_TYPE_API_KEY),
            source=str(body.get("source") or SOURCE_USER),
            access_token=str(body["access_token"]),
            base_url=body.get("base_url"),
        )
        pool = CredentialPool.get_instance()
        pool.add(cred)
        return {"ok": True, "credential": _credential_to_dict(cred)}

    @app.delete("/api/credentials/{provider}/{credential_id}")
    async def _remove_credential(provider: str, credential_id: str) -> dict[str, Any]:
        from cvc.agent.credential_pool import CredentialPool

        pool = CredentialPool.get_instance()
        ok = pool.remove(provider, credential_id)
        if not ok:
            raise HTTPException(status_code=404, detail="credential not found")
        return {"ok": True}

    @app.post("/api/credentials/{provider}/{credential_id}/reset")
    async def _reset_credential(provider: str, credential_id: str) -> dict[str, Any]:
        from cvc.agent.credential_pool import CredentialPool

        pool = CredentialPool.get_instance()
        cred = pool.get(provider, credential_id)
        if not cred:
            raise HTTPException(status_code=404, detail="credential not found")
        pool.reset(cred)
        return {"ok": True, "credential": _credential_to_dict(cred)}

    @app.get("/api/credentials/stats")
    async def _credential_stats() -> dict[str, Any]:
        from cvc.agent.credential_pool import CredentialPool

        return CredentialPool.get_instance().stats()

    # ─── Fallback chain preview ─────────────────────────────────────────────

    @app.get("/api/fallback/preview")
    async def _fallback_preview(provider: str, model: str) -> dict[str, Any]:
        """Show the ordered fallback chain a (provider, model) request would
        produce, so the dashboard can render exactly what would be tried."""
        from cvc.providers import get_provider

        profile = get_provider(provider)
        if not profile:
            raise HTTPException(status_code=404, detail=f"unknown provider: {provider}")

        chain: list[dict[str, str]] = [{"provider": profile.name, "model": model}]
        for fb in profile.fallback_models:
            chain.append({"provider": profile.name, "model": fb})
        return {"requested": {"provider": provider, "model": model}, "chain": chain}


def _gen_id() -> str:
    import uuid

    return uuid.uuid4().hex[:12]
