"""
cvc.gateway.security — /api/security/* routes

Exposes the Apple-grade security primitives to the dashboard:
  GET   /api/security/status            — vault + sentinel state
  POST  /api/security/initialize        — create the vault (passphrase)
  POST  /api/security/unlock            — open the vault (passphrase)
  POST  /api/security/lock              — zero the key
  POST  /api/security/rotate            — change passphrase (re-encrypt)
  GET   /api/security/audit             — tail the audit log
  POST  /api/security/audit/verify      — replay the chain, return ok/fail
  POST  /api/security/sentinel/check    — test a URL against the allowlist
  GET   /api/security/sentinel/stats    — allowed/blocked counts

NOTE: passphrases are NEVER logged, echoed back, or stored anywhere
except via the vault's scrypt derivation. Audit log records actions,
not secrets.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

logger = logging.getLogger("cvc.gateway.security")

router = APIRouter()


def _vault_dir() -> Path:
    """Find the active vault dir — defaults to ~/.cvc/vault."""
    candidates = [Path.cwd() / ".cvc" / "vault", Path.home() / ".cvc" / "vault"]
    for p in candidates:
        if p.exists():
            return p
    return candidates[-1]


def _audit_path() -> Path:
    return _vault_dir() / "audit.log"


def _get_vault():
    from cvc.security.vault import SoulVault

    return SoulVault(_vault_dir())


def _get_audit():
    from cvc.security.audit import AuditLog

    return AuditLog(_audit_path())


def _get_sentinel():
    from cvc.security.sentinel import NetworkSentinel

    return NetworkSentinel.from_vault(_vault_dir())


# ── vault ────────────────────────────────────────────────────────────


@router.get("/security/status")
async def security_status() -> dict[str, Any]:
    """Full vault + sentinel state snapshot."""
    try:
        vault = _get_vault()
        sentinel = _get_sentinel()
        audit = _get_audit()
        return {
            "vault": vault.status(),
            "sentinel": sentinel.stats(),
            "audit_entries": audit.count(),
            "ready": True,
        }
    except Exception as exc:
        logger.exception("security/status failed")
        return {"ready": False, "error": str(exc)}


@router.post("/security/initialize")
async def initialize_vault(req: dict[str, Any]) -> dict[str, Any]:
    """Create the vault. Body: { passphrase: str }"""
    passphrase = req.get("passphrase") or ""
    if not passphrase:
        raise HTTPException(400, "passphrase required")
    if len(passphrase) < 8:
        raise HTTPException(400, "passphrase must be ≥8 chars")
    try:
        vault = _get_vault()
        if vault.is_initialized:
            raise HTTPException(409, "vault already initialized — unlock instead")
        vault.initialize(passphrase)
        audit = _get_audit()
        audit.append("vault.initialize", actor="owner")
        return {"ok": True, "status": vault.status()}
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("initialize failed")
        raise HTTPException(500, str(exc))


@router.post("/security/unlock")
async def unlock_vault(req: dict[str, Any]) -> dict[str, Any]:
    """Open the vault. Body: { passphrase: str }"""
    from cvc.security.vault import VaultLocked

    passphrase = req.get("passphrase") or ""
    if not passphrase:
        raise HTTPException(400, "passphrase required")
    try:
        vault = _get_vault()
        vault.unlock(passphrase)
        audit = _get_audit()
        audit.append("vault.unlock", actor="owner")
        return {"ok": True, "status": vault.status()}
    except VaultLocked as exc:
        raise HTTPException(401, str(exc))
    except Exception as exc:
        logger.exception("unlock failed")
        raise HTTPException(500, str(exc))


@router.post("/security/lock")
async def lock_vault() -> dict[str, Any]:
    """Zero the in-memory key."""
    vault = _get_vault()
    vault.lock()
    audit = _get_audit()
    audit.append("vault.lock", actor="owner")
    return {"ok": True, "status": vault.status()}


@router.post("/security/rotate")
async def rotate_passphrase(req: dict[str, Any]) -> dict[str, Any]:
    """
    Change the passphrase. Reads every existing blob with the old key,
    re-encrypts with the new key, atomically replaces.

    Body: { old_passphrase: str, new_passphrase: str }
    """
    old = req.get("old_passphrase") or ""
    new = req.get("new_passphrase") or ""
    if not old or not new:
        raise HTTPException(400, "old_passphrase and new_passphrase required")
    if len(new) < 8:
        raise HTTPException(400, "new passphrase must be ≥8 chars")
    if old == new:
        raise HTTPException(400, "new passphrase must differ from old")

    from cvc.security.vault import SoulVault, VaultLocked

    vault = _get_vault()
    if not vault.is_initialized:
        raise HTTPException(409, "vault not initialized")

    try:
        u_old = vault.unlock(old)
    except VaultLocked as exc:
        raise HTTPException(401, str(exc))

    try:
        # Read + re-encrypt every blob under the new key
        names = vault.list_blobs()
        payloads = [(name, u_old.decrypt(
            (vault.blobs_dir / f"{name}.cvcv").read_bytes(),
            aad=name.encode("utf-8"),
        )) for name in names]

        # Re-init with new passphrase (this swaps the meta + key)
        vault.lock()
        vault.initialize(new)
        u_new = vault.unlock(new)

        import json, time
        # Persist the previous meta so audit chain survives rotation
        prev_meta_path = vault.meta_path.with_suffix(".prev.json")
        prev_meta_path.write_text(vault.meta_path.read_text(encoding="utf-8"), encoding="utf-8")

        for name, pt in payloads:
            vault.write_blob(name, pt)

        audit = _get_audit()
        audit.append(
            "vault.lock",
            actor="owner",
            target="rotate-prep",
            detail={"blobs_reencrypted": len(payloads)},
        )
        audit.append(
            "vault.initialize",
            actor="owner",
            target="rotate",
            detail={"blobs_reencrypted": len(payloads), "ts": time.time()},
        )
        audit.append("vault.unlock", actor="owner", target="rotate")

        return {
            "ok": True,
            "blobs_reencrypted": len(payloads),
            "status": vault.status(),
        }
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("rotate failed")
        raise HTTPException(500, str(exc))


# ── audit ────────────────────────────────────────────────────────────


@router.get("/security/audit")
async def audit_tail(n: int = 50) -> dict[str, Any]:
    """Return the most recent N audit entries (newest last)."""
    try:
        audit = _get_audit()
        return {"entries": audit.tail(n=n), "count": audit.count()}
    except Exception as exc:
        logger.exception("audit/tail failed")
        raise HTTPException(500, str(exc))


@router.post("/security/audit/verify")
async def audit_verify() -> dict[str, Any]:
    """Replay the chain. Returns ok=True/False with the last-verified entry count."""
    try:
        audit = _get_audit()
        ok, msg = audit.verify()
        return {"ok": ok, "message": msg, "entries": audit.count()}
    except Exception as exc:
        logger.exception("audit/verify failed")
        raise HTTPException(500, str(exc))


# ── sentinel ─────────────────────────────────────────────────────────


@router.post("/security/sentinel/check")
async def sentinel_check(req: dict[str, Any]) -> dict[str, Any]:
    """Test a URL against the allowlist. Body: { url: str }"""
    url = req.get("url") or ""
    if not url:
        raise HTTPException(400, "url required")
    sentinel = _get_sentinel()
    allowed = sentinel.check(url)
    return {"url": url, "allowed": allowed, "stats": sentinel.stats()}


@router.get("/security/sentinel/stats")
async def sentinel_stats() -> dict[str, Any]:
    return _get_sentinel().stats()


@router.post("/security/sentinel/configure")
async def sentinel_configure(req: dict[str, Any]) -> dict[str, Any]:
    """
    Update the sentinel config. Body: { allowed_brains?: [...], allowed_hosts?: [...], permissive?: bool }
    """
    sentinel = _get_sentinel()
    allowed = set(req.get("allowed_brains") or [])
    # CRITICAL: never let permissive be set to True via the API. It must
    # be a deliberate local-only decision made by the owner opening a
    # socket — not a JSON payload.
    sentinel.configure(
        allowed_brains=list(allowed),
        allowed_hosts=req.get("allowed_hosts") or [],
        blocked_hosts=req.get("blocked_hosts") or sentinel.config.blocked_hosts,
        allow_loopback=req.get("allow_loopback", sentinel.config.allow_loopback),
        permissive=False,  # hard-disabled from API
    )
    # Persist the config so it survives restarts
    import json

    cfg_path = _vault_dir() / "sentinel.json"
    cfg_path.parent.mkdir(parents=True, exist_ok=True)
    cfg_path.write_text(
        json.dumps(
            {
                "allowed_brains": sentinel.config.allowed_brains,
                "allowed_hosts": sentinel.config.allowed_hosts,
                "blocked_hosts": sentinel.config.blocked_hosts,
                "allow_loopback": sentinel.config.allow_loopback,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return sentinel.stats()