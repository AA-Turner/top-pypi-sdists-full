"""
Soul router — /api/soul/* (the soul layer of CVC)

Exposes the soul's growing understanding of its owner via the gateway.
The dashboard uses these endpoints to render the life story view and
the soul model inspector.

Exposed endpoints:
  GET /api/soul/life-story        — the narrative arc of the user's journey
  GET /api/soul/user-model        — the full soul model (entities, values, etc.)
  GET /api/soul/dreams            — recent dream diary entries
  GET /api/soul/narrative         — just the soul narrative paragraph (for cold-start preview)

This is what makes the soul visible. The data lives in the CVC DAG and
user_model.json; this router is the window.
"""

from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Optional

from fastapi import APIRouter, Query, Request, Response

logger = logging.getLogger("cvc.gateway.soul")

router = APIRouter()


# ---------------------------------------------------------------------------
# hotfix/soul-singularity-2026-06-30 — the soul is ONE thing.
# ---------------------------------------------------------------------------
# Previously, soul endpoints resolved their data from
# ``<workspace>/.cvc/`` via ``_cvc_root()``. Switching workspaces in the
# chat hid everything you'd built up. The user said it clearly: "soul
# is a singular thing in a complete body system." Workspace is only
# meaningful for project work — commits, branches, snapshots. Soul
# data (letters, dreams, narratives, emotional arc, persona) is
# workspace-agnostic and lives at ``~/.cvc/soul/``.
#
# All soul-specific read/write endpoints in this router call
# ``_soul_root()`` and ``_ensure_soul_migrated()`` instead of
# ``_cvc_root()``. The chat/work endpoints (commits, branches, etc.)
# still use the workspace path. Migration from per-workspace data
# runs once on first access — it's idempotent.


def _soul_root() -> Path:
    """Return the global soul root directory (``~/.cvc/soul/``).

    Always the same regardless of which workspace is active. The
    soul is singular — there is one body across all workspaces and
    all channels.
    """
    from cvc.operations.soul_singularity import _soul_root as _sr
    return _sr()


def _ensure_soul_migrated() -> None:
    """Run the one-time migration from per-workspace .cvc/ data into
    the global soul store. Idempotent — cheap to call repeatedly."""
    try:
        from cvc.operations.soul_singularity import ensure_migrated
        ensure_migrated()
    except Exception as exc:  # noqa: BLE001
        logger.debug("soul migration failed (non-fatal): %s", exc)


def _workspace_cvc_root_for_work() -> Path:
    """Return the workspace's .cvc/ root for chat/work operations
    (commits, branches, snapshots). This is the ONE thing that
    remains workspace-scoped — the rest of the soul layer is global.

    Falls through the same resolution chain as ``_cvc_root()`` so
    workspace paths are honored when explicitly passed, with the
    active workspace (from WorkspaceManager) as the default.
    """
    try:
        return _resolve_cvc_root(_current_workspace_override())
    except Exception:  # noqa: BLE001
        return _cvc_root()


# hotfix/soul-wiring-2026-06-30 — per-request workspace override.
# FastAPI is async; each request runs on a worker thread. We can't
# safely store per-request state on ``self`` (shared across
# coroutines), so we use ContextVars. Falls back to None if the
# request didn't pass ?workspace_path=.
try:
    import contextvars
    _WORKSPACE_OVERRIDE: "contextvars.ContextVar[Optional[str]]" = (
        contextvars.ContextVar("cvc_soul_workspace_override", default=None)
    )
except ImportError:  # pragma: no cover — pre-Python 3.7 fallback
    _WORKSPACE_OVERRIDE = None  # type: ignore[assignment]  # noqa: F821


def _workspace_override_param(
    workspace_path: Optional[str] = Query(
        default=None,
        description=(
            "Filesystem path of the active workspace. When set, the "
            "soul router reads/writes <workspace_path>/.cvc/ "
            "directly instead of falling back to the host's active "
            "workspace pointer."
        ),
    ),
) -> Optional[str]:
    """FastAPI dependency — stashes the per-request workspace override."""
    if _WORKSPACE_OVERRIDE is not None and workspace_path:
        _WORKSPACE_OVERRIDE.set(workspace_path)
    return workspace_path


def _current_workspace_override() -> Optional[str]:
    if _WORKSPACE_OVERRIDE is None:
        return None
    try:
        return _WORKSPACE_OVERRIDE.get()
    except Exception:  # noqa: BLE001
        return None

# ---------------------------------------------------------------------------
# Module-level vault cache for the will endpoints.
#
# The WillStore needs an unlocked SoulVault instance. Constructing a fresh
# SoulVault per request would always be locked (the unlocked key lives in
# per-instance memory). So we cache the vault instance per process and
# thread the unlock() through here.
#
# This is intentionally scoped to the will subsystem only — the security
# gateway uses its own pattern. If a process-wide singleton is ever
# desired, lift this into cvc.security.vault directly.
# ---------------------------------------------------------------------------

_will_vault: Any = None


def _get_will_vault() -> Any:
    """Return the cached SoulVault for the will subsystem, constructing it
    on first call. The caller is responsible for calling .unlock() (or
    .initialize() + .unlock()) on the returned instance."""
    global _will_vault
    if _will_vault is None:
        from cvc.security.vault import SoulVault
        from pathlib import Path
        # Same lookup as cvc.gateway.security._vault_dir
        candidates = [Path.cwd() / ".cvc" / "vault", Path.home() / ".cvc" / "vault"]
        vdir = next((p for p in candidates if p.exists()), candidates[-1])
        _will_vault = SoulVault(vdir)
    return _will_vault


def _cvc_root() -> Path:
    """Find the active CVC root directory.

    Resolution order (v3.4.2 / hotfix/soul-wiring-2026-06-30):
      0. Per-request workspace override (?workspace_path=…). Set via
         the FastAPI ``_workspace_override_param`` dependency on each
         route. Honors what the dashboard actually said, not a guess.
      1. CVC_TEST_ROOT env var (used by tests for hermetic isolation).
      2. The gateway's active workspace's .cvc/ — this is the single
         source of truth for "what workspace is the user in RIGHT NOW".
         This fixes the bug where the soul page read from a stale cwd
         while the per-turn update wrote to the active workspace,
         producing a permanently-empty Soul UI.
      3. cwd/.cvc — fallback for legacy callers / very early boot.
      4. ~/.cvc — last resort (user-global state).

    The previous implementation put cwd/.cvc BEFORE ~/.cvc which
    meant: when the gateway was launched from a terminal whose cwd
    was $HOME (e.g. ``cvc gateway start`` from a fresh shell),
    ``_cvc_root()`` returned ``$HOME/.cvc`` — a different directory
    than the active workspace's ``$WORKSPACE/.cvc/`` that the
    per-turn soul update writes to. Result: Soul UI empty forever.
    """
    import os as _os
    # Per-request override first.
    explicit = _current_workspace_override()
    if explicit:
        candidate = Path(explicit).expanduser() / ".cvc"
        if candidate.exists() and (candidate / "cvc.db").exists():
            return candidate
    override = _os.environ.get("CVC_TEST_ROOT")
    if override:
        p = Path(override)
        if p.exists() and (p / "cvc.db").exists():
            return p
    # v3.4.2 — Active workspace first. The gateway tracks this in
    # _workspace_mgr.current_path; we reach it through the legacy
    # gateway's module-level state. If it's not available (e.g. unit
    # tests calling the router directly without booting the gateway),
    # fall through to cwd then home.
    try:
        from cvc.workspace_manager import WorkspaceManager  # noqa: WPS433
        # Use a static method so we don't depend on a live singleton —
        # WorkspaceManager.load_active_workspace() reads the durable
        # host-state DB, which is the same source of truth the boot
        # path uses, so Soul will always agree with the chat path.
        active = WorkspaceManager.load_active_workspace()
        if active is not None:
            candidate = active / ".cvc"
            if candidate.exists() and (candidate / "cvc.db").exists():
                return candidate
    except Exception:  # noqa: BLE001 — never crash a Soul read
        pass
    candidates = [
        Path.cwd() / ".cvc",
        Path.home() / ".cvc",
    ]
    for p in candidates:
        if p.exists() and (p / "cvc.db").exists():
            return p
    return Path.cwd() / ".cvc"


def _explicit_cvc_root(workspace_path: Optional[str]) -> Optional[Path]:
    """Resolve ``workspace_path`` (an explicit override) to a .cvc/ root.

    hotfix/soul-wiring-2026-06-30 — the dashboard passes the
    active workspace path on every Soul request. When present,
    trust it: it is the user's stated truth, not a guess. Falls
    back to None if the override doesn't point at an initialized
    .cvc/, in which case callers should fall through to _cvc_root().
    """
    if not workspace_path:
        return None
    candidate = Path(workspace_path).expanduser() / ".cvc"
    try:
        if candidate.exists() and (candidate / "cvc.db").exists():
            return candidate
    except Exception:  # noqa: BLE001 — never crash a Soul read
        return None
    return None


def _resolve_cvc_root(workspace_path: Optional[str] = None) -> Path:
    """Pick the best .cvc/ root for this request.

    Order (highest priority first):
      1. Explicit ``workspace_path`` query/body parameter — the
         dashboard always passes this when it knows which workspace
         is active.
      2. WorkspaceManager.load_active_workspace() (host_state.db)
      3. cwd/.cvc
      4. ~/.cvc

    Any non-initialized candidate falls through to the next level,
    so we never return an empty/half-built .cvc/ as the truth.
    """
    explicit = _explicit_cvc_root(workspace_path)
    if explicit is not None:
        return explicit
    return _cvc_root()


def _dedup_emotional_arc(
    observations: list, limit: int = 40
) -> list[dict[str, Any]]:
    """Collapse a raw ``emotional_context`` list into a real arc.

    The raw list often contains 2-3 mood entries per chat turn
    (multiple SSE/WS handlers all call fire_and_forget_update), plus
    re-classifications of the same text within milliseconds. Showing
    that raw list as the dashboard's "emotional arc" makes the page
    look broken.

    Dedup rule: one entry per (mood, minute-bucket). The bucket is
    chosen so a single chat turn (which may emit mood entries 11ms
    apart) collapses to one representative entry. The representative
    uses the highest-intensity entry from that bucket so a peak
    emotional moment isn't masked by the trailing low-intensity
    follow-up.

    Returns the most-recent ``limit`` buckets, ordered oldest-first
    so the dashboard can render them left-to-right as a real arc.
    """
    if not observations:
        return []

    # Bucket = int(timestamp / 60) — same minute collapses together.
    by_bucket: dict[int, list] = {}
    for obs in observations:
        bucket = int(getattr(obs, "timestamp", 0) or 0) // 60
        by_bucket.setdefault(bucket, []).append(obs)

    # For each bucket, keep one entry per (mood) — pick highest intensity.
    by_bucket_mood: dict[int, dict] = {}
    for bucket, items in by_bucket.items():
        best_per_mood: dict[str, Any] = {}
        for it in items:
            mood = getattr(it, "mood", "neutral")
            existing = best_per_mood.get(mood)
            if existing is None or getattr(it, "intensity", 0.0) > getattr(
                existing, "intensity", 0.0
            ):
                best_per_mood[mood] = it
        # Representative entry = the highest-intensity mood from the bucket.
        rep = max(
            best_per_mood.values(),
            key=lambda x: getattr(x, "intensity", 0.0),
        )
        by_bucket_mood[bucket] = rep

    # Sort by bucket ascending (oldest-first) and emit the most-recent
    # `limit` buckets. The dashboard plots left-to-right so oldest
    # first feels natural.
    sorted_buckets = sorted(by_bucket_mood.keys())
    recent_buckets = sorted_buckets[-limit:]
    out: list[dict[str, Any]] = []
    for b in recent_buckets:
        m = by_bucket_mood[b]
        ts = getattr(m, "timestamp", 0) or 0
        out.append({
            "mood": getattr(m, "mood", "neutral"),
            "intensity": getattr(m, "intensity", 0.0),
            "trigger": getattr(m, "trigger", ""),
            "timestamp": ts,
            "date": time.strftime("%Y-%m-%d %H:%M", time.localtime(ts)),
        })
    return out


def _read_yaml_default_model() -> str:
    """Read ``~/.cvc/config.yaml:default_model`` — the chat's chosen
    default model. Best-effort, never raises; returns "" on any
    parse error or missing file. The soul layer ALWAYS uses the
    chat's chosen model so soul-letter generation, soul reasoning,
    and corrections all stay in lockstep with the user's chat — one
    brain, one model (hotfix/soul-wiring-2026-06-30)."""
    try:
        import yaml  # already a CVC dep
        from pathlib import Path as _P
        path = _P.home() / ".cvc" / "config.yaml"
        if not path.is_file():
            return ""
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            return ""
        v = data.get("default_model") or data.get("primary_model") or ""
        return str(v).strip() if v else ""
    except Exception:  # noqa: BLE001
        return ""


def _read_yaml_primary_provider() -> str:
    """Read ``~/.cvc/config.yaml:primary_provider`` — the chat's
    default provider (minimax, google, anthropic, ...). Best-effort,
    never raises. Used as a fallback when the registry's health
    tracking hasn't been populated yet (e.g. fresh gateway start,
    no chat has run yet to drive adapter health probes)."""
    try:
        import yaml  # already a CVC dep
        from pathlib import Path as _P
        path = _P.home() / ".cvc" / "config.yaml"
        if not path.is_file():
            return ""
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            return ""
        v = (
            data.get("primary_provider")
            or data.get("provider")
            or data.get("default_provider")
            or ""
        )
        return str(v).strip().lower() if v else ""
    except Exception:  # noqa: BLE001
        return ""


def _read_yaml_api_key(provider: str) -> str:
    """Read ``~/.cvc/config.yaml:api_keys.<provider>`` for the chat's
    currently configured credentials. Best-effort, never raises.

    Returns "" if the key isn't set or the file isn't readable.
    The CVC gateway uses the same config file; if you've configured
    the chat with a provider, the key should be here.
    """
    if not provider:
        return ""
    try:
        import yaml  # already a CVC dep
        from pathlib import Path as _P
        path = _P.home() / ".cvc" / "config.yaml"
        if not path.is_file():
            return ""
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        if not isinstance(data, dict):
            return ""
        api_keys = data.get("api_keys") or {}
        if not isinstance(api_keys, dict):
            return ""
        v = (
            api_keys.get(provider)
            or api_keys.get(provider.lower())
            or api_keys.get(provider.replace("-", "_"))
            or ""
        )
        return str(v).strip() if v else ""
    except Exception:  # noqa: BLE001
        return ""


def _build_chat_default_adapter() -> tuple[Any, str, str] | None:
    """hotfix/soul-values-and-cleanup-2026-06-30 — when the adapter
    registry returns no healthy adapter (the common case on a fresh
    gateway start, because nothing has run a health probe yet), build
    an adapter directly from the chat's configured provider/model.

    Returns ``(adapter_instance, model_id, adapter_id)`` or None if
    construction fails. This is the fallback path for
    /soul/letters/generate so the "No healthy brain is configured"
    error stops showing on the dashboard.

    Order of preference:
      1. CVC_MODEL env var (overrides everything)
      2. ~/.cvc/config.yaml:default_model + primary_provider
      3. The adapter for the provider the chat is currently using
         (read from registry's last_healthy cache if any)

    Each adapter class has a different constructor signature, but
    most require ``api_key`` as the first arg. We read the key from
    ``~/.cvc/config.yaml:api_keys.<provider>`` and pass it. Ollama
    and LMStudio don't need an API key (local) so they accept no args.
    """
    import os as _os

    provider = _read_yaml_primary_provider() or "minimax"
    model = (
        _os.environ.get("CVC_MODEL", "").strip()
        or _read_yaml_default_model()
    )
    api_key = _read_yaml_api_key(provider)

    try:
        from cvc.adapters.registry import get_registry

        reg = get_registry()
        reg.discover()
        adapter_cls = reg.get_class(provider)
        if adapter_cls is None:
            logger.warning(
                "soul letters: provider %r has no adapter class in registry — cannot build fallback",
                provider,
            )
            return None
        # Try construction strategies in order: explicit (api_key, model),
        # then (api_key,), then no-args. Each adapter has its own
        # signature — we sniff what's available.
        adapter = None
        last_err: Exception | None = None
        if api_key:
            for call in (
                lambda: adapter_cls(api_key=api_key, model=model) if model else adapter_cls(api_key=api_key),  # type: ignore[call-arg]
                lambda: adapter_cls(api_key, model) if model else adapter_cls(api_key),  # type: ignore[call-arg]
            ):
                try:
                    adapter = call()
                    break
                except TypeError as exc:
                    last_err = exc
                    continue
                except Exception as exc:
                    last_err = exc
                    continue
        if adapter is None:
            # No key, or the (api_key, ...) calls all failed — try no-args.
            try:
                adapter = adapter_cls()
            except TypeError as exc:
                last_err = exc
            except Exception as exc:
                last_err = exc
        if adapter is None:
            logger.warning(
                "soul letters: cannot construct adapter for %r (last error: %s) — cannot build fallback",
                provider,
                last_err,
            )
            return None
        # Mark this adapter healthy in the registry so subsequent calls
        # don't have to re-probe. record_health is safe to call even if
        # we never actually called it via a chat.
        try:
            reg.record_health(provider, healthy=True, error="")
        except Exception:
            pass
        return (adapter, model or "", provider)
    except Exception as exc:
        logger.exception("soul letters: failed to build fallback adapter: %s", exc)
        return None


@router.get("/soul/life-story")
async def get_life_story(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    The narrative arc of the user's journey with CVC.

    Returns:
      - soul_narrative: the holistic essence paragraph
      - life_events: milestones sorted by time, with emotional weight
      - emotional_arc: mood timeline showing the emotional journey
      - entity_graph: key people, projects, places
      - values: what the user believes in
      - timeline_density: how many commits per time period (activity heatmap)
      - first_interaction: when the soul was born
      - total_interactions: how many cognitive commits exist
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        # Count total commits in the DAG. ``cvc.db`` lives at the GLOBAL
        # CVC root (``~/.cvc/cvc.db``), NOT at ``~/.cvc/soul/cvc.db`` —
        # the soul store and the cognitive-commit DAG are sibling
        # directories. Use ``_cvc_root()`` here, not ``_soul_root()``.
        total_commits = 0
        first_timestamp = None
        timeline_density: dict[str, int] = {}  # "2026-06": 42
        try:
            db_path = _cvc_root() / "cvc.db"
            if db_path.exists():
                import sqlite3
                # Schema column is `created_at` (REAL, unix seconds).
                # An earlier revision queried `timestamp` which silently
                # returned 0 rows, making the life-story endpoint claim
                # the user had zero interactions even when the DAG had
                # dozens of commits. Fix is permanent; we also tolerate
                # a missing/empty created_at row so a fresh install
                # doesn't blow up the response.
                conn = sqlite3.connect(str(db_path))
                try:
                    cursor = conn.execute("SELECT COUNT(*) FROM commits")
                    total_commits = cursor.fetchone()[0]
                    cursor = conn.execute(
                        "SELECT created_at FROM commits ORDER BY created_at ASC LIMIT 1"
                    )
                    row = cursor.fetchone()
                    if row and row[0]:
                        first_timestamp = row[0]
                    # Build timeline density (monthly buckets)
                    cursor = conn.execute(
                        "SELECT created_at FROM commits ORDER BY created_at DESC LIMIT 500"
                    )
                    for (ts,) in cursor:
                        if not ts:
                            continue
                        month_key = time.strftime(
                            "%Y-%m", time.localtime(float(ts))
                        )
                        timeline_density[month_key] = (
                            timeline_density.get(month_key, 0) + 1
                        )
                finally:
                    conn.close()
        except Exception as exc:
            logger.debug("Could not query commit stats: %s", exc)

        # Sort life events by timestamp
        life_events = sorted(
            [
                {
                    "description": e.description,
                    "event_type": e.event_type,
                    "emotional_weight": e.emotional_weight,
                    "timestamp": e.timestamp,
                    "date": time.strftime("%Y-%m-%d", time.localtime(e.timestamp)),
                }
                for e in model.life_events
            ],
            key=lambda x: x["timestamp"],
        )

        # Build emotional arc — deduped + bucketed view of recent mood.
        # The raw model.emotional_context list often contains 2-3
        # entries per chat turn (SSE proxy + SSE stream + WS handler
        # all fire fire_and_forget_update on one turn) plus hundreds
        # of low-signal entries. Showing that raw list as the
        # "emotional arc" produces the duplicate-pill mess in the
        # dashboard. We collapse to ONE entry per (mood, time-bucket)
        # where the bucket is "the same minute". That gives the user
        # a real arc — when did they shift from excited to frustrated,
        # not "excited 50%, proud 25%, frustrated 100%" cycling in the
        # same second.
        emotional_arc = _dedup_emotional_arc(model.emotional_context, limit=40)

        # Entity graph — top people, projects, places by mention count
        entity_graph = [
            {
                "name": e.name,
                "type": e.entity_type,
                "relationship": e.relationship,
                "mention_count": e.mention_count,
                "attributes": e.attributes,
            }
            for e in sorted(model.entities, key=lambda x: x.mention_count, reverse=True)[:20]
        ]

        # Values
        values = [
            {
                "statement": v.statement,
                "category": v.category,
                "confidence": v.confidence,
            }
            for v in model.values
            if not v.superseded_by
        ]

        return {
            "soul_narrative": model.soul_narrative,
            "name": model.name,
            "life_events": life_events,
            "emotional_arc": emotional_arc,
            "entity_graph": entity_graph,
            "values": values,
            "timeline_density": timeline_density,
            "total_interactions": total_commits,
            "first_interaction": first_timestamp,
            "first_interaction_date": (
                time.strftime("%Y-%m-%d", time.localtime(first_timestamp))
                if first_timestamp else None
            ),
        }
    except Exception as exc:
        logger.exception("life-story failed")
        return {"error": str(exc), "soul_narrative": "", "life_events": []}


@router.post("/soul/refresh")
async def refresh_soul_now(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    """Force an immediate soul re-synthesis from accumulated data.

    The Soul page's "refresh" button calls this. Without it, the
    dashboard's narrative stays empty until a fresh chat turn triggers
    ``per_turn_soul.update_soul_after_turn``. With it, the user can
    re-derive a real narrative from the entities/values/mood that's
    already in the soul store, instantly.

    Also runs the per-turn cleanup pass (drops stopword entities,
    dedupes owner rows) and writes a fresh snapshot. Idempotent —
    safe to spam.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.operations.per_turn_soul import (
            _synthesise_narrative,
            _synthesise_name,
        )

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        before = {
            "narrative": (model.soul_narrative or "")[:80],
            "name": (model.name or "")[:40],
            "entities": len(model.entities),
            "values": len(model.values),
        }

        # Run the same cleanup that per_turn_soul runs
        try:
            from cvc.operations.entity_extractor import cleanup_snapshot_entities
            dropped, merged = cleanup_snapshot_entities(model)
        except Exception:
            dropped, merged = 0, 0

        # Re-derive narrative from current data
        new_narrative = _synthesise_narrative(model)
        if new_narrative:
            model.soul_narrative = new_narrative
        new_name = _synthesise_name(model)
        if new_name:
            model.name = new_name

        # Persist (auto-snapshots via H1)
        um.save_model(model, trigger="manual_refresh")

        after = {
            "narrative": (model.soul_narrative or "")[:80],
            "name": (model.name or "")[:40],
            "entities": len(model.entities),
            "values": len(model.values),
        }

        return {
            "ok": True,
            "narrative_updated": before["narrative"] != after["narrative"],
            "name_updated": before["name"] != after["name"],
            "cleanup_dropped": dropped,
            "cleanup_merged": merged,
            "before": before,
            "after": after,
            "narrative_preview": (model.soul_narrative or "")[:240],
        }
    except Exception as exc:
        logger.exception("soul refresh failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/reset")
async def reset_soul(payload: dict[str, Any]) -> dict[str, Any]:
    """Wipe the soul back to a fresh-install state.

    Intended for the user-owner (Jai) who has inherited a half-formed
    soul model from a backfill, schema migration, or earlier experimental
    data import and wants to start the soulware relationship cleanly.
    Not gated behind an admin role because CVC ships as a personal
    on-device install — the dashboard's only caller path is a hidden
    Shift+click on the "SOULWARE" badge that requires deliberate intent.

    Body contract:
      { "confirm": "RESET MY SOUL", "scope": "all" | "narrative" }

    Behavior:
      - Backs up the existing user_model.json to
        user_model.json.reset-{unix_ts}.bak before deleting.
      - Drops `~/.cvc/soul/user_model.json`.
      - Drops recent `~/.cvc/events/{YYYY-MM-DD}.jsonl` rows whose
        `kind` starts with `soul.` (preserves chat + ops + channel
        events — those are the user's actual history).
      - Returns the backup path so the caller can show it.

    Returns:
      { ok: bool, backup: str|null, dropped_events: int }
    """
    confirm = (payload or {}).get("confirm")
    if confirm != "RESET MY SOUL":
        return {
            "ok": False,
            "error": "Confirmation phrase required: pass {\"confirm\": \"RESET MY SOUL\"}.",
        }

    try:
        _ensure_soul_migrated()
        cvc_root = _soul_root()
        events_root = _cvc_root()

        # 1. Snapshot current model before wiping. ``cvc_root`` IS the
        # soul store (typically ``~/.cvc/soul``) — there's no nested
        # ``soul/soul`` directory. Pre-fix bug: I wrote
        # ``soul_dir = cvc_root / "soul"`` which resolved to
        # ``~/.cvc/soul/soul`` and never matched the real file, so the
        # backup path stayed null and the wipe silently no-op'd.
        ts = int(time.time())
        backup_path: Optional[str] = None
        soul_dir = cvc_root
        user_model = soul_dir / "user_model.json"
        if user_model.exists():
            backup_path = str(soul_dir / f"user_model.json.reset-{ts}.bak")
            try:
                user_model.replace(backup_path)
            except Exception:
                # Some FS combinations disallow cross-device rename; fall
                # back to copy + delete.
                import shutil

                shutil.copy2(str(user_model), backup_path)
                user_model.unlink()

        # 2. Drop recent soul.* events so the spine doesn't keep feeding
        #    the same stale state back into a freshly-empty model.
        #    Events live at the GLOBAL CVC root (~/.cvc/events/),
        #    sibling to the soul store — same reason we use _cvc_root()
        #    for cvc.db in the life-story endpoint.
        dropped_events = 0
        events_dir = events_root / "events"
        if events_dir.exists():
            for jf in events_dir.glob("*.jsonl"):
                try:
                    kept_lines: list[str] = []
                    with jf.open("r", encoding="utf-8") as fh:
                        for line in fh:
                            stripped = line.strip()
                            if not stripped:
                                continue
                            try:
                                obj = json.loads(stripped)
                            except json.JSONDecodeError:
                                kept_lines.append(line)
                                continue
                            kind = (obj.get("kind") or "").lower()
                            if kind.startswith("soul."):
                                dropped_events += 1
                                continue
                            kept_lines.append(line)
                    jf.write_text(
                        "".join(kept_lines), encoding="utf-8"
                    )
                except Exception:
                    # best-effort; don't fail the reset because one
                    # malformed JSONL file got in the way
                    continue

        # 3. Fire a spine event so audit + timeline pages see the wipe.
        try:
            from cvc.events.spine import capture
            capture(
                kind="soul.reset",
                workspace="__system__",
                actor="user",
                summary="Soul model reset to fresh-install state",
                data={
                    "backup": backup_path,
                    "dropped_events": dropped_events,
                    "ts": ts,
                },
            )
        except Exception:
            pass

        return {
            "ok": True,
            "backup": backup_path,
            "dropped_events": dropped_events,
        }
    except Exception as exc:
        logger.exception("soul reset failed")
        return {"ok": False, "error": str(exc)}


@router.get("/soul/time-portal")
async def get_time_portal(
    target: str | None = None,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    H1 Time-Portal — side-by-side "what you knew then" vs "what you know now."

    Args:
        target: Either an ISO date ``YYYY-MM-DD``, a Unix timestamp,
                or a snapshot id (``snap-<id>``). If omitted, defaults
                to the oldest available snapshot.

    Returns:
      - then: soul snapshot reconstructed at target time
      - now: current soul snapshot
      - diff: structured comparison (added/removed entities, new events,
              narrative drift, emotional delta, human summary)
      - target_resolved: how the input was interpreted
      - available_targets: list of recent snapshot timestamps for the picker
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.core.model_snapshots import SnapshotStore
        from cvc.core.soul_diff import diff_soul_models
        import dateutil.parser as _dp  # type: ignore

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        store = SnapshotStore(cvc_root)

        # ── Resolve target timestamp ──────────────────────────────────────
        target_ts: float = 0.0
        target_resolved = "now"  # default if no target
        if target:
            if target.startswith("snap-"):
                sid = target[5:]
                snap = store.get(sid)
                if snap:
                    target_ts = float(snap["timestamp"])
                    target_resolved = f"snapshot:{sid}"
            else:
                # Try as date string, then as float
                try:
                    target_ts = float(target)
                    target_resolved = "timestamp"
                except ValueError:
                    try:
                        dt = _dp.parse(target)
                        target_ts = float(dt.timestamp())
                        target_resolved = "iso_date"
                    except Exception:
                        pass

        # If no target or unresolvable, pick the oldest snapshot
        if target_ts == 0.0 and target_resolved == "now":
            all_snaps = store.list(limit=10_000)
            if all_snaps:
                target_ts = float(all_snaps[0]["timestamp"])
                target_resolved = "oldest_snapshot"

        # ── Reconstruct "then" ────────────────────────────────────────────
        historical = store.reconstruct_at(target_ts)
        if historical:
            then_model = historical["model"]
            then_model["_snapshot_timestamp"] = historical["timestamp"]
            then_model["_snapshot_id"] = historical["snapshot_id"]
        else:
            # Fallback: empty snapshot at target time
            then_model = {
                "name": "",
                "soul_narrative": "",
                "entities": [],
                "values": [],
                "emotional_context": [],
                "life_events": [],
                "_snapshot_timestamp": target_ts,
                "_snapshot_id": None,
                "_is_empty": True,
            }

        # ── Current "now" ─────────────────────────────────────────────────
        now_model_obj = um.load_current_model()
        now_model = json.loads(now_model_obj.model_dump_json())
        now_model["_snapshot_timestamp"] = now_model_obj.timestamp
        now_model["_snapshot_id"] = now_model_obj.snapshot_id

        # ── Compute the diff ──────────────────────────────────────────────
        diff = diff_soul_models(then_model, now_model)

        # ── Available targets for the dashboard picker ────────────────────
        snaps = store.list(limit=200)
        available_targets = [
            {
                "snapshot_id": s["snapshot_id"],
                "timestamp": s["timestamp"],
                "iso": time.strftime("%Y-%m-%d %H:%M", time.localtime(s["timestamp"])),
                "trigger": s.get("trigger", "?"),
                "commit_hash": s.get("commit_hash"),
            }
            for s in snaps
        ]

        return {
            "then": then_model,
            "now": now_model,
            "diff": diff,
            "target_resolved": target_resolved,
            "target_timestamp": target_ts,
            "available_targets": available_targets,
        }
    except Exception as exc:
        logger.exception("time-portal failed")
        return {"error": str(exc), "then": {}, "now": {}, "diff": {}}


@router.get("/soul/snapshots")
async def list_snapshots(
    limit: int = 50,
    trigger: str | None = None,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    H1 — list recent user-model snapshots for the time-portal picker.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.model_snapshots import SnapshotStore
        cvc_root = _soul_root()
        store = SnapshotStore(cvc_root)
        snaps = store.list(limit=limit, trigger=trigger)  # type: ignore[arg-type]
        stats = store.stats()
        return {"snapshots": snaps, "stats": stats}
    except Exception as exc:
        logger.exception("list_snapshots failed")
        return {"error": str(exc), "snapshots": [], "stats": {}}


# ---------------------------------------------------------------------------
# H1b — Time Portal session lifecycle
# ---------------------------------------------------------------------------
# "Enter the portal" = pick a snapshot, get a portal_id, send all subsequent
# chat through that historical soul. "Exit" = back to current soul.
#
# State lives at ~/.cvc/soul/portal_sessions.json:
#   { "<portal_id>": { snapshot_id, snapshot_timestamp, target_resolved,
#                       iso_date, label, created_at, workspace_key } }
#
# The portal_id is generated client-side (UUID) and stored in localStorage.
# Multiple portals can coexist (different browser tabs / windows).
# Per-turn system prompt augmentation lives in _portal_context_for_chat()
# which is called from the chat path when portal_session_id is provided.

_PORTAL_SESSIONS_FILE = "portal_sessions.json"
_PORTAL_LOCK = threading.RLock()


def _portal_sessions_path() -> Path:
    return _soul_root() / _PORTAL_SESSIONS_FILE


def _load_portal_sessions() -> dict[str, Any]:
    """Load portal sessions from disk. Empty dict if file is missing or corrupt."""
    path = _portal_sessions_path()
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        logger.warning("portal_sessions.json unreadable, starting fresh: %s", exc)
        return {}


def _save_portal_sessions(sessions: dict[str, Any]) -> None:
    """Persist portal sessions atomically (write-then-rename)."""
    path = _portal_sessions_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(sessions, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def _resolve_portal_target(target: str | None) -> dict[str, Any]:
    """Translate a user-supplied target (snap-id / date / timestamp) into a
    concrete snapshot. Returns a dict with snapshot_id, timestamp, iso_date,
    label, target_resolved. Raises ValueError on unresolvable input."""
    from cvc.core.model_snapshots import SnapshotStore
    import dateutil.parser as _dp  # type: ignore

    store = SnapshotStore(_soul_root())
    target_ts: float = 0.0
    target_resolved = "now"
    label = ""

    if target:
        if target.startswith("snap-"):
            sid = target[5:]
            snap = store.get(sid)
            if not snap:
                raise ValueError(f"snapshot not found: {sid}")
            return {
                "snapshot_id": sid,
                "timestamp": float(snap["timestamp"]),
                "iso_date": time.strftime(
                    "%Y-%m-%d %H:%M", time.localtime(float(snap["timestamp"]))
                ),
                "label": f"portal: snap {sid[:8]}",
                "target_resolved": f"snapshot:{sid}",
                "trigger": snap.get("trigger", "?"),
            }
        # numeric timestamp
        try:
            target_ts = float(target)
            target_resolved = "timestamp"
        except ValueError:
            try:
                dt = _dp.parse(target)
                target_ts = float(dt.timestamp())
                target_resolved = "iso_date"
            except Exception as exc:
                raise ValueError(f"could not parse target '{target}': {exc}") from exc

    # If no target or unresolvable, pick the oldest snapshot
    if target_ts == 0.0:
        snaps = store.list(limit=10_000)
        if not snaps:
            raise ValueError("no snapshots available — soul has no history yet")
        oldest = snaps[-1]  # list() returns newest-first
        target_ts = float(oldest["timestamp"])
        target_resolved = "oldest_snapshot"
        label = f"portal: oldest snapshot ({oldest['snapshot_id'][:8]})"
        return {
            "snapshot_id": oldest["snapshot_id"],
            "timestamp": target_ts,
            "iso_date": time.strftime("%Y-%m-%d %H:%M", time.localtime(target_ts)),
            "label": label,
            "target_resolved": target_resolved,
            "trigger": oldest.get("trigger", "?"),
        }

    # Find snapshot closest to (and not after) target_ts
    snap = store.reconstruct_at(target_ts)
    if not snap:
        snaps = store.list(limit=10_000)
        if not snaps:
            raise ValueError("no snapshots available")
        snap = snaps[-1]
    return {
        "snapshot_id": snap["snapshot_id"],
        "timestamp": float(snap["timestamp"]),
        "iso_date": time.strftime(
            "%Y-%m-%d %H:%M", time.localtime(float(snap["timestamp"]))
        ),
        "label": f"portal: {target}",
        "target_resolved": target_resolved,
        "trigger": snap.get("trigger", "?"),
    }


def format_portal_chat_context(snapshot_id: str, max_chars: int = 6000) -> str:
    """Build the system-prompt augmentation for a portal-mode chat turn.

    Loads the snapshot, extracts the soul's understanding of the user at
    that moment, and formats it as a compact prompt block. Returns "" if
    the snapshot is unreadable (caller should silently fall back to
    current soul).

    The block is bounded so a chat turn stays cheap even with very old
    snapshots.
    """
    from cvc.core.model_snapshots import SnapshotStore

    store = SnapshotStore(_soul_root())
    snap = store.get(snapshot_id)
    if not snap:
        return ""
    model = snap.get("model") or {}
    if not isinstance(model, dict):
        return ""

    iso_date = time.strftime(
        "%Y-%m-%d %H:%M", time.localtime(float(snap.get("timestamp", time.time())))
    )

    name = model.get("name") or "the owner"
    narrative = (model.get("soul_narrative") or "").strip()
    entities = [
        e for e in (model.get("entities") or [])
        if isinstance(e, dict) and (e.get("name") or "").strip()
    ]
    values = [
        v for v in (model.get("values") or [])
        if isinstance(v, dict) and (v.get("statement") or "").strip()
    ]
    life_events = [
        e for e in (model.get("life_events") or [])
        if isinstance(e, dict) and (e.get("description") or "").strip()
    ]
    emo = [
        e for e in (model.get("emotional_context") or [])
        if isinstance(e, dict) and e.get("timestamp")
    ]

    # Compress each section to fit max_chars budget.
    parts: list[str] = []

    header = (
        f"## ⏳ TIME PORTAL ACTIVE — soul restored from snapshot {snapshot_id[:12]} "
        f"({iso_date})\n\n"
        f"You are responding AS THE CVC AGENT KNOWING ONLY WHAT THE SOUL KNEW ON "
        f"{iso_date}. The user has explicitly entered the time portal to talk "
        f"to the version of you that existed at that moment.\n\n"
        f"- Do NOT reference memories, events, entities, or feelings that "
        f"the soul learned AFTER {iso_date}.\n"
        f"- If the user asks about something that didn't exist in the soul "
        f"then, say so honestly: \"On {iso_date} the soul didn't know that "
        f"yet.\" Do not make up answers from the future.\n"
        f"- Keep the same voice and care you always have, but speak from "
        f"the perspective of {iso_date}.\n"
        f"- The user can exit the portal at any time — when they do, your "
        f"context returns to the present soul.\n"
    )
    parts.append(header)

    if narrative:
        parts.append(f"### Soul narrative as of {iso_date}\n{narrative}")

    if entities:
        ent_lines = []
        for e in entities[:25]:
            tag = f"{e.get('entity_type', '?')}"
            rel = e.get("relationship") or "mentioned"
            mc = e.get("mention_count", 0)
            ent_lines.append(f"- {e.get('name')} ({tag}, {rel}, ×{mc})")
        parts.append(f"### Known entities ({len(entities)} total)\n" + "\n".join(ent_lines))

    if values:
        val_lines = [f"- {v.get('statement')}" for v in values[:15]]
        parts.append(f"### Known values / principles ({len(values)} total)\n" + "\n".join(val_lines))

    if life_events:
        ev_lines = [f"- {e.get('description')}" for e in life_events[:10]]
        parts.append(f"### Life events on record ({len(life_events)} total)\n" + "\n".join(ev_lines))

    if emo:
        emo_lines = [
            f"- {time.strftime('%Y-%m-%d', time.localtime(float(e.get('timestamp', 0))))}: "
            f"{e.get('mood', '?')} @ intensity {e.get('intensity', 0):.2f} "
            f"(trigger: {e.get('trigger', '—')})"
            for e in emo[-10:]
        ]
        parts.append(f"### Recent emotional observations\n" + "\n".join(emo_lines))

    text = "\n\n".join(parts)
    if len(text) > max_chars:
        text = text[: max_chars - 200] + "\n\n[…truncated for length; the soul's full history at this moment is preserved on disk.]"
    return text


# -----------------------------------------------------------------------------
# v3.5.1 — TIME PORTAL day-scope: consolidation + day context
# -----------------------------------------------------------------------------
#
# The old per-snapshot portal works fine for a few historical moments,
# but a single day of normal use produces 20-100 per_turn_auto snapshots,
# most of which differ only by emotion deltas. Showing all of them in
# the Time Portal UI is noise; using one of them as "the day's frame"
# loses all the cross-conversation context.
#
# Solution: collapse every snapshot from one day into a single canonical
# "day frame" the user can step into. The raw snapshots stay on disk as
# rollback history; the day frame is a merged view.
# -----------------------------------------------------------------------------


DAY_CONSOLIDATION_THRESHOLD = 20  # auto-consolidate a day once it has this many snapshots


def consolidate_day_snapshots(snapshots: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge all snapshots from one day into a single canonical model.

    Merge rules (newest wins per entity/value/event key, full chronology
    preserved for events / emotions):

      - soul_narrative: longest non-empty narrative (richer description).
      - entities:        dedupe by ``name`` — newest occurrence wins
                         (newest = highest mention_count + freshest relationship).
      - values:          dedupe by ``statement`` — newest wins.
      - life_events:     keep ALL (chronologically), dedupe by
                         ``description`` (first-seen wins).
      - emotional_context: keep ALL (chronological).

    Returns a snapshot-shaped dict with ``snapshot_id="day-<date>"``
    and the merged ``model`` body — caller can persist via
    ``SnapshotStore.append(..., scope="day")`` or use it in-memory.
    """
    if not snapshots:
        return {}

    # Sort oldest → newest so newest assignments overwrite older ones.
    snaps_sorted = sorted(snapshots, key=lambda s: s.get("timestamp", 0))
    last = snaps_sorted[-1]

    merged: dict[str, Any] = {
        "name": "",
        "soul_narrative": "",
        "entities": [],
        "values": [],
        "life_events": [],
        "emotional_context": [],
    }

    entities_by_name: dict[str, dict[str, Any]] = {}
    values_by_statement: dict[str, dict[str, Any]] = {}
    seen_event_descriptions: set[str] = set()
    seen_emo_keys: set[tuple[str, str]] = set()  # (timestamp, mood)

    for snap in snaps_sorted:
        m = snap.get("model") or {}
        if not isinstance(m, dict):
            continue

        if m.get("name") and not merged["name"]:
            merged["name"] = m["name"]

        narrative = (m.get("soul_narrative") or "").strip()
        if len(narrative) > len(merged["soul_narrative"]):
            merged["soul_narrative"] = narrative

        for e in m.get("entities") or []:
            if not isinstance(e, dict) or not (e.get("name") or "").strip():
                continue
            key = e["name"].strip().lower()
            existing = entities_by_name.get(key)
            if existing is None or e.get("mention_count", 0) >= existing.get("mention_count", 0):
                entities_by_name[key] = e
        merged["entities"] = list(entities_by_name.values())

        for v in m.get("values") or []:
            if not isinstance(v, dict) or not (v.get("statement") or "").strip():
                continue
            key = v["statement"].strip().lower()
            if key not in values_by_statement:
                values_by_statement[key] = v
        merged["values"] = list(values_by_statement.values())

        for ev in m.get("life_events") or []:
            if not isinstance(ev, dict):
                continue
            desc = (ev.get("description") or "").strip().lower()
            if desc and desc in seen_event_descriptions:
                continue
            if desc:
                seen_event_descriptions.add(desc)
            merged["life_events"].append(ev)
        merged["life_events"].sort(
            key=lambda x: x.get("timestamp", 0) if isinstance(x, dict) else 0,
        )

        for emo in m.get("emotional_context") or []:
            if not isinstance(emo, dict):
                continue
            ts = emo.get("timestamp", 0)
            mood = (emo.get("mood") or "").strip().lower()
            key = (str(ts), mood)
            if key in seen_emo_keys:
                continue
            seen_emo_keys.add(key)
            merged["emotional_context"].append(emo)
        merged["emotional_context"].sort(
            key=lambda x: x.get("timestamp", 0) if isinstance(x, dict) else 0,
        )

    return {
        "snapshot_id": f"day-{time.strftime('%Y-%m-%d', time.localtime(last.get('timestamp', time.time())))}",
        "timestamp": last.get("timestamp", time.time()),
        "parent_snapshot_id": last.get("snapshot_id"),
        "trigger": "day_canonical",
        "consolidated_from": [s.get("snapshot_id") for s in snaps_sorted],
        "consolidated_count": len(snaps_sorted),
        "model": merged,
        "size_bytes": 0,  # filled by caller if persisted
    }


def format_portal_day_context(date_iso: str, max_chars: int = 8000) -> str:
    """Build the system-prompt augmentation for a day-scope portal turn.

    Loads every snapshot for the given day, merges them, and formats
    the merged model the same way ``format_portal_chat_context`` formats
    a single snapshot, but with day-level framing.

    Returns "" if no snapshots exist for the date (caller should fall
    back to current soul or return an error).
    """
    from cvc.core.model_snapshots import SnapshotStore

    store = SnapshotStore(_soul_root())
    snaps = store.list_by_date(date_iso)
    if not snaps:
        return ""

    merged = consolidate_day_snapshots(snaps)
    model = merged.get("model") or {}
    if not isinstance(model, dict):
        return ""

    iso_date = date_iso
    first_ts = snaps[0].get("timestamp", 0)
    last_ts = snaps[-1].get("timestamp", 0)
    span = ""
    if first_ts and last_ts and first_ts != last_ts:
        span = (
            f" (spanning {time.strftime('%H:%M', time.localtime(first_ts))}"
            f"–{time.strftime('%H:%M', time.localtime(last_ts))})"
        )

    name = model.get("name") or "the owner"
    narrative = (model.get("soul_narrative") or "").strip()
    entities = [
        e for e in (model.get("entities") or [])
        if isinstance(e, dict) and (e.get("name") or "").strip()
    ]
    values = [
        v for v in (model.get("values") or [])
        if isinstance(v, dict) and (v.get("statement") or "").strip()
    ]
    life_events = [
        e for e in (model.get("life_events") or [])
        if isinstance(e, dict) and (e.get("description") or "").strip()
    ]
    emo = [
        e for e in (model.get("emotional_context") or [])
        if isinstance(e, dict) and e.get("timestamp")
    ]

    parts: list[str] = []

    header = (
        f"## ⏳ TIME PORTAL ACTIVE — DAY FRAME for {iso_date}{span}\n\n"
        f"You are responding AS THE CVC AGENT KNOWING ONLY WHAT THE SOUL KNEW "
        f"DURING {iso_date}. This day-frame is a CONSOLIDATED view of "
        f"{len(snaps)} snapshots taken across the day, merged into one "
        f"canonical model. The user has explicitly entered the time portal "
        f"to talk to the version of you that existed across that whole day.\n\n"
        f"- Do NOT reference memories, events, entities, or feelings that "
        f"the soul learned AFTER {iso_date}.\n"
        f"- If the user asks about something that didn't exist in the soul "
        f"on that day, say so honestly: \"On {iso_date} the soul didn't "
        f"know that yet.\" Do not make up answers from the future.\n"
        f"- Keep the same voice and care you always have, but speak from "
        f"the perspective of {iso_date}.\n"
        f"- The user can exit the portal at any time — when they do, your "
        f"context returns to the present soul.\n"
    )
    parts.append(header)

    if narrative:
        parts.append(f"### Soul narrative for {iso_date}\n{narrative}")

    if entities:
        ent_lines = []
        for e in entities[:30]:
            tag = f"{e.get('entity_type', '?')}"
            rel = e.get("relationship") or "mentioned"
            mc = e.get("mention_count", 0)
            ent_lines.append(f"- {e.get('name')} ({tag}, {rel}, ×{mc})")
        parts.append(
            f"### Known entities ({len(entities)} total — consolidated across the day)\n"
            + "\n".join(ent_lines)
        )

    if values:
        val_lines = [f"- {v.get('statement')}" for v in values[:20]]
        parts.append(
            f"### Known values / principles ({len(values)} total)\n"
            + "\n".join(val_lines)
        )

    if life_events:
        ev_lines = []
        for e in life_events[:20]:
            ts_str = ""
            if e.get("timestamp"):
                ts_str = time.strftime(
                    "%H:%M",
                    time.localtime(float(e["timestamp"])),
                )
            prefix = f"[{ts_str}] " if ts_str else ""
            ev_lines.append(f"- {prefix}{e.get('description')}")
        parts.append(
            f"### Life events on {iso_date} ({len(life_events)} total)\n"
            + "\n".join(ev_lines)
        )

    if emo:
        emo_lines = [
            f"- {time.strftime('%H:%M', time.localtime(float(e.get('timestamp', 0))))}: "
            f"{e.get('mood', '?')} @ intensity {e.get('intensity', 0):.2f} "
            f"(trigger: {e.get('trigger', '—')})"
            for e in emo[-15:]
        ]
        parts.append(
            f"### Emotional observations across {iso_date} ({len(emo)} total)\n"
            + "\n".join(emo_lines)
        )

    text = "\n\n".join(parts)
    if len(text) > max_chars:
        text = text[: max_chars - 200] + "\n\n[…truncated for length; the soul's full history for this day is preserved on disk.]"
    return text


def auto_consolidate_day_if_needed(date_iso: str) -> dict[str, Any] | None:
    """If a day has >= DAY_CONSOLIDATION_THRESHOLD snapshots, persist a
    day_canonical snapshot and return it. Idempotent: returns None if
    a day_canonical already exists for that date.
    """
    from cvc.core.model_snapshots import SnapshotStore

    store = SnapshotStore(_soul_root())
    snaps = store.list_by_date(date_iso)
    if len(snaps) < DAY_CONSOLIDATION_THRESHOLD:
        return None

    # Idempotency: skip if a day_canonical already exists for this date.
    for entry in store._read_index().get("snapshots", []):
        meta = entry.get("metadata") or {}
        if (
            entry.get("trigger") == "day_canonical"
            and meta.get("date") == date_iso
        ):
            logger.debug(
                "auto_consolidate_day_if_needed: %s already consolidated (snapshot_id=%s)",
                date_iso, entry.get("snapshot_id"),
            )
            return None

    merged = consolidate_day_snapshots(snaps)
    sid = store.append(
        merged,
        trigger="day_canonical",
        commit_hash=None,
        snapshot_id=f"day-{date_iso.replace('-', '')}-{uuid.uuid4().hex[:8]}",
        scope="day",
        date=date_iso,
        consolidated_from=[s.get("snapshot_id") for s in snaps],
        consolidated_count=len(snaps),
    )
    logger.info(
        "auto-consolidated day %s into snapshot %s (%d raw snapshots)",
        date_iso, sid, len(snaps),
    )
    return store.get(sid)


@router.post("/soul/time-portal/enter")
async def time_portal_enter(body: dict[str, Any]) -> dict[str, Any]:
    """Enter the time portal — pin chat context to a historical snapshot.

    Body:
      - portal_id: client-generated UUID (so multiple tabs can coexist)
      - target:    either "snap-<id>", ISO date "YYYY-MM-DD", or a Unix timestamp
      - label:     optional human-readable name for the session

    Returns:
      - ok, portal_id, snapshot_id, snapshot_timestamp, iso_date,
        target_resolved, label
    """
    try:
        _ensure_soul_migrated()
        portal_id = (body or {}).get("portal_id")
        target = (body or {}).get("target")
        label = (body or {}).get("label")

        if not portal_id or not isinstance(portal_id, str):
            return {"ok": False, "error": "portal_id required (client-generated UUID)"}

        resolved = _resolve_portal_target(target)
        if label:
            resolved["label"] = label

        with _PORTAL_LOCK:
            sessions = _load_portal_sessions()
            sessions[portal_id] = {
                "snapshot_id": resolved["snapshot_id"],
                "snapshot_timestamp": resolved["timestamp"],
                "iso_date": resolved["iso_date"],
                "target_resolved": resolved["target_resolved"],
                "label": resolved["label"],
                "trigger": resolved.get("trigger", "?"),
                "created_at": time.time(),
            }
            _save_portal_sessions(sessions)

        logger.info(
            "time-portal ENTER portal_id=%s snapshot=%s target=%s",
            portal_id[:12], resolved["snapshot_id"][:12], resolved["target_resolved"],
        )
        return {
            "ok": True,
            "portal_id": portal_id,
            "scope": "snapshot",
            **resolved,
        }
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("time-portal/enter failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/time-portal/enter-day")
async def time_portal_enter_day(body: dict[str, Any]) -> dict[str, Any]:
    """Enter the time portal at DAY scope — pin chat context to a whole day.

    Body:
      - portal_id: client-generated UUID
      - date:      YYYY-MM-DD
      - label:     optional human-readable name

    Returns:
      - ok, portal_id, snapshot_id (the day_canonical snapshot_id, possibly
        freshly created), snapshot_timestamp, iso_date, target_resolved,
        label, snapshot_count (how many raw snapshots were merged).
    """
    try:
        _ensure_soul_migrated()
        portal_id = (body or {}).get("portal_id")
        date_iso = (body or {}).get("date")
        label = (body or {}).get("label")

        if not portal_id or not isinstance(portal_id, str):
            return {"ok": False, "error": "portal_id required (client-generated UUID)"}
        if not date_iso or not isinstance(date_iso, str):
            return {"ok": False, "error": "date required (YYYY-MM-DD)"}

        from cvc.core.model_snapshots import SnapshotStore
        store = SnapshotStore(_soul_root())
        snaps = store.list_by_date(date_iso)
        if not snaps:
            return {"ok": False, "error": f"no snapshots found for {date_iso}"}

        # Trigger consolidation (idempotent — returns existing day_canonical
        # if one already exists, otherwise creates one).
        consolidated = auto_consolidate_day_if_needed(date_iso)
        if consolidated is None:
            # Below threshold — synthesize in-memory without persisting.
            consolidated = consolidate_day_snapshots(snaps)
        snap_id = consolidated.get("snapshot_id", "")
        snap_ts = consolidated.get("timestamp", snaps[-1].get("timestamp", time.time()))
        snap_count = len(snaps)
        iso_date = date_iso
        target_resolved = f"day:{date_iso}"
        session_label = label or f"portal: day {date_iso}"

        with _PORTAL_LOCK:
            sessions = _load_portal_sessions()
            sessions[portal_id] = {
                "snapshot_id": snap_id,
                "snapshot_timestamp": snap_ts,
                "iso_date": iso_date,
                "target_resolved": target_resolved,
                "label": session_label,
                "trigger": "day_canonical",
                "created_at": time.time(),
                "scope": "day",
                "snapshot_count": snap_count,
                "date": date_iso,
            }
            _save_portal_sessions(sessions)

        logger.info(
            "time-portal ENTER-DAY portal_id=%s date=%s snapshots=%d day_id=%s",
            portal_id[:12], date_iso, snap_count, snap_id[:16],
        )
        return {
            "ok": True,
            "portal_id": portal_id,
            "scope": "day",
            "snapshot_id": snap_id,
            "snapshot_timestamp": snap_ts,
            "iso_date": iso_date,
            "target_resolved": target_resolved,
            "label": session_label,
            "trigger": "day_canonical",
            "snapshot_count": snap_count,
            "date": date_iso,
        }
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("time-portal/enter-day failed")
        return {"ok": False, "error": str(exc)}


@router.get("/soul/time-portal/days")
async def time_portal_days() -> dict[str, Any]:
    """Return the day-index for the Time Portal UI.

    Each entry: { date, snapshot_count, first_ts, last_ts, first_id, last_id,
                  has_day_canonical }. Sorted newest day first.

    The UI uses this to render one row per day (with the count of raw
    snapshots) instead of one row per snapshot — collapsing the cluttered
    per-second pill grid.
    """
    try:
        from cvc.core.model_snapshots import SnapshotStore
        store = SnapshotStore(_soul_root())
        days = store.list_day_index()

        # Annotate each day with whether a day_canonical already exists.
        for d in days:
            has_canonical = False
            for entry in store._read_index().get("snapshots", []):
                meta = entry.get("metadata") or {}
                if (
                    entry.get("trigger") == "day_canonical"
                    and meta.get("date") == d["date"]
                ):
                    has_canonical = True
                    d["day_snapshot_id"] = entry["snapshot_id"]
                    break
            d["has_day_canonical"] = has_canonical

        return {"ok": True, "days": days, "count": len(days)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("time-portal/days failed")
        return {"ok": False, "error": str(exc)}


@router.get("/soul/time-portal/active")
async def time_portal_active(portal_id: str | None = Query(default=None)) -> dict[str, Any]:
    """Return the active portal session for a given portal_id (or all of them).

    Used by the frontend on mount to restore portal banner state across
    page reloads. If portal_id is omitted, returns all sessions (so the
    dashboard can show a portal list).
    """
    try:
        with _PORTAL_LOCK:
            sessions = _load_portal_sessions()
        if portal_id:
            sess = sessions.get(portal_id)
            if not sess:
                return {"active": False, "portal_id": portal_id}
            return {"active": True, "portal_id": portal_id, "session": sess}
        # All sessions
        return {"active": bool(sessions), "sessions": sessions, "count": len(sessions)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("time-portal/active failed")
        return {"active": False, "error": str(exc)}


@router.post("/soul/time-portal/exit")
async def time_portal_exit(body: dict[str, Any]) -> dict[str, Any]:
    """Exit the time portal — clear the session so chat returns to present.

    Body: { portal_id: "..." }
    """
    try:
        portal_id = (body or {}).get("portal_id")
        if not portal_id:
            return {"ok": False, "error": "portal_id required"}
        with _PORTAL_LOCK:
            sessions = _load_portal_sessions()
            removed = sessions.pop(portal_id, None)
            _save_portal_sessions(sessions)
        logger.info(
            "time-portal EXIT portal_id=%s removed=%s",
            portal_id[:12], bool(removed),
        )
        return {"ok": True, "portal_id": portal_id, "existed": bool(removed)}
    except Exception as exc:  # noqa: BLE001
        logger.exception("time-portal/exit failed")
        return {"ok": False, "error": str(exc)}


@router.get("/soul/time-portal/chat-context")
async def time_portal_chat_context(
    portal_id: str = Query(...),
) -> dict[str, Any]:
    """Return the formatted chat-context string for a portal session.

    Useful for the dashboard's portal-mode preview panel and as a
    fallback if the chat endpoint needs the raw context (it normally
    looks it up directly via format_portal_chat_context).
    """
    try:
        with _PORTAL_LOCK:
            sessions = _load_portal_sessions()
        sess = sessions.get(portal_id)
        if not sess:
            return {"ok": False, "error": "no active portal session", "portal_id": portal_id}
        ctx = format_portal_chat_context(sess["snapshot_id"])
        if not ctx:
            return {"ok": False, "error": "snapshot unreadable", "snapshot_id": sess["snapshot_id"]}
        return {
            "ok": True,
            "portal_id": portal_id,
            "snapshot_id": sess["snapshot_id"],
            "iso_date": sess.get("iso_date"),
            "context": ctx,
            "context_length": len(ctx),
        }
    except Exception as exc:  # noqa: BLE001
        logger.exception("time-portal/chat-context failed")
        return {"ok": False, "error": str(exc)}


@router.get("/soul/emotional-arc")
async def get_emotional_arc(
    bucket: str = "day",  # day | week | month
    since_days: int = 90,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    H2 — aggregate emotional context over time, with buckets and stats.

    Returns:
      - observations: [{timestamp, mood, intensity, trigger}, ...]
      - aggregate: {mood_distribution, mean_intensity, dominant_mood,
                    volatility, period_start, period_end}
      - buckets: [{label, count, mean_intensity, dominant_mood}, ...]
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from collections import Counter
        import math

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()
        cutoff = time.time() - (since_days * 86400)
        observations = [e for e in model.emotional_context if e.timestamp >= cutoff]
        observations.sort(key=lambda e: e.timestamp)

        # Aggregate (use ALL raw observations for stats — dedup is
        # only a display thing, not a measurement thing).
        moods = [e.mood for e in observations]
        intensities = [e.intensity for e in observations]
        mood_counts = Counter(moods)
        dominant = mood_counts.most_common(1)[0][0] if mood_counts else "neutral"
        mean_intensity = (
            sum(intensities) / len(intensities) if intensities else 0.0
        )
        # Volatility = std dev of intensity (how variable is the user's mood)
        if len(intensities) > 1:
            variance = sum((i - mean_intensity) ** 2 for i in intensities) / len(intensities)
            volatility = math.sqrt(variance)
        else:
            volatility = 0.0

        # Buckets
        bucket_secs = {"day": 86400, "week": 604800, "month": 2592000}.get(bucket, 86400)
        bucket_groups: dict[int, list] = {}
        for e in observations:
            key = int(e.timestamp // bucket_secs)
            bucket_groups.setdefault(key, []).append(e)
        bucket_out = []
        for k in sorted(bucket_groups.keys()):
            items = bucket_groups[k]
            bm = Counter(i.mood for i in items).most_common(1)[0][0]
            mi = sum(i.intensity for i in items) / len(items)
            label_ts = k * bucket_secs
            bucket_out.append({
                "label": time.strftime("%Y-%m-%d", time.localtime(label_ts)),
                "count": len(items),
                "mean_intensity": round(mi, 3),
                "dominant_mood": bm,
            })

        return {
            "observations": [
                {
                    "mood": e.mood,
                    "intensity": e.intensity,
                    "trigger": e.trigger,
                    "timestamp": e.timestamp,
                    "date": time.strftime("%Y-%m-%d %H:%M", time.localtime(e.timestamp)),
                }
                for e in observations
            ],
            "aggregate": {
                "total": len(observations),
                "mood_distribution": dict(mood_counts),
                "mean_intensity": round(mean_intensity, 3),
                "dominant_mood": dominant,
                "volatility": round(volatility, 3),
                "period_start": time.strftime("%Y-%m-%d", time.localtime(cutoff)),
                "period_end": time.strftime("%Y-%m-%d", time.localtime(time.time())),
            },
            "buckets": bucket_out,
        }
    except Exception as exc:
        logger.exception("emotional-arc failed")
        return {"error": str(exc), "observations": [], "aggregate": {}, "buckets": []}


@router.get("/soul/entity-graph")
async def get_entity_graph(
    min_mentions: int = 1,
    entity_type: str | None = None,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    H2 — social-graph view of entities + their relationships.

    Returns:
      - nodes: [{id, name, type, relationship, mention_count,
                 first_mentioned, last_mentioned, attributes}]
      - edges: [{source, target, kind, weight}]
        where kind ∈ {co_mentioned, family_of, project_of, place_of, mentioned_with}
      - stats: {total_entities, by_type, by_relationship, top_mentioned}
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from collections import Counter

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        nodes = []
        for e in model.entities:
            if e.mention_count < min_mentions:
                continue
            if entity_type and e.entity_type != entity_type:
                continue
            nodes.append({
                "id": e.entity_id,
                "name": e.name,
                "type": e.entity_type,
                "relationship": e.relationship,
                "mention_count": e.mention_count,
                "first_mentioned": e.first_mentioned,
                "last_mentioned": e.last_mentioned,
                "first_mentioned_date": time.strftime("%Y-%m-%d", time.localtime(e.first_mentioned)) if e.first_mentioned else "",
                "last_mentioned_date": time.strftime("%Y-%m-%d", time.localtime(e.last_mentioned)) if e.last_mentioned else "",
                "attributes": e.attributes,
            })
        nodes.sort(key=lambda n: -n["mention_count"])

        # Build edges: co-mention (entities appearing in the same session
        # get a co_mentioned edge weighted by co-occurrences). For now
        # we infer from context_snippets: if two entities share any
        # snippet, they have an edge.
        snippet_to_entities: dict[str, list[str]] = {}
        for e in model.entities:
            for snippet in e.context_snippets or []:
                snippet_to_entities.setdefault(snippet, []).append(e.entity_id)
        edge_counter: dict[tuple[str, str], int] = {}
        for ents in snippet_to_entities.values():
            for i in range(len(ents)):
                for j in range(i + 1, len(ents)):
                    a, b = sorted([ents[i], ents[j]])
                    edge_counter[(a, b)] = edge_counter.get((a, b), 0) + 1

        edges = []
        for (a, b), w in edge_counter.items():
            edges.append({"source": a, "target": b, "kind": "co_mentioned", "weight": w})
        edges.sort(key=lambda e: -e["weight"])

        # Stats
        all_types = Counter(n["type"] for n in nodes)
        all_rels = Counter(n["relationship"] for n in nodes)
        top = [{"name": n["name"], "mention_count": n["mention_count"]} for n in nodes[:10]]

        return {
            "nodes": nodes,
            "edges": edges,
            "stats": {
                "total_entities": len(nodes),
                "by_type": dict(all_types),
                "by_relationship": dict(all_rels),
                "total_edges": len(edges),
                "top_mentioned": top,
            },
        }
    except Exception as exc:
        logger.exception("entity-graph failed")
        return {"error": str(exc), "nodes": [], "edges": [], "stats": {}}


@router.post("/soul/classify-mood")
async def classify_mood_endpoint(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param(body.get("workspace_path") if isinstance(body, dict) else None)
    """
    H2 — run the heuristic mood classifier on arbitrary text.

    Useful for the dashboard preview / API consumers. Body:
      { text: "ugh broken again" } or
      { messages: [{"role": "user", "content": "..."}, ...] }
    """
    try:
        from cvc.operations.emotional_classifier import classify_text, classify_session
        if "messages" in body:
            c = classify_session(body["messages"])
        else:
            c = classify_text(str(body.get("text", "")))
        return {
            "mood": c.mood,
            "intensity": c.intensity,
            "confidence": c.confidence,
            "trigger": c.trigger,
        }
    except Exception as exc:
        logger.exception("classify-mood failed")
        return {"error": str(exc)}


@router.post("/soul/extract-entities")
async def extract_entities_endpoint(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param(body.get("workspace_path") if isinstance(body, dict) else None)
    """
    H2 — run the entity extractor on arbitrary text. Body:
      { text: "my wife Anjali suggested..." } or
      { messages: [{"role": "user", "content": "..."}, ...] }
    """
    try:
        from cvc.operations.entity_extractor import extract_from_message, extract_from_session
        if "messages" in body:
            ents = extract_from_session(body["messages"])
        else:
            ents = extract_from_message(str(body.get("text", "")), message_idx=0)
        return {
            "entities": [
                {
                    "name": e.name,
                    "type": e.entity_type,
                    "relationship": e.relationship,
                    "confidence": e.confidence,
                    "context_snippet": e.context_snippet,
                    "attributes": e.attributes,
                }
                for e in ents
            ],
            "count": len(ents),
        }
    except Exception as exc:
        logger.exception("extract-entities failed")
        return {"error": str(exc), "entities": [], "count": 0}


@router.get("/soul/cold-start-context")
async def get_cold_start_context(
    persona: str | None = None,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    H3 — single-payload bundle for brain-bootstrap on provider switch.

    Designed to be called by the agent loop on cold start (or on
    provider swap) so a new brain immediately has the full soul
    context. Returns a compact bundle — not the full user model —
    optimised for fitting inside a system prompt without bloating it.

    Args:
      persona: optional persona id ('default', 'ajay', 'jha',
               'robin', 'samantha', 'tina') for H5 persona-aware
               framing. When set, returns the persona overlay too.

    Returns:
      - frozen_narrative: present iff preservation mode is enabled
      - name: owner's name
      - soul_narrative: V2 essence paragraph
      - narrative_summary: V1 paragraph
      - communication_style: tone preference
      - top_entities: 5 most-mentioned people/projects
      - top_values: 3 most-confident active values
      - active_corrections: owner overrides (always trust over inference)
      - recent_letters: 2 most recent soul letters (titles only)
      - persona_overlay: persona-specific framing (when persona is set)
      - system_prompt_fragment: pre-rendered text block ready to
        paste into a system prompt (assembled from all of the above)
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.core.correction import build_corrections_prompt_block
        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        # ── Top entities (by mention_count) ────────────────────────────────
        top_entities = sorted(
            model.entities,
            key=lambda e: -int(e.mention_count or 0),
        )[:5]
        top_entities_out = [
            {
                "name": e.name,
                "type": e.entity_type,
                "relationship": e.relationship,
                "mention_count": e.mention_count,
            }
            for e in top_entities
        ]

        # ── Top active values (by confidence) ──────────────────────────────
        top_values = sorted(
            [v for v in model.values if not v.superseded_by],
            key=lambda v: -float(v.confidence or 0.0),
        )[:3]
        top_values_out = [
            {"statement": v.statement, "category": v.category, "confidence": v.confidence}
            for v in top_values
        ]

        # ── Active corrections ─────────────────────────────────────────────
        corrections = [c for c in (getattr(model, "corrections", []) or []) if getattr(c, "active", True)]
        corrections_block = build_corrections_prompt_block(corrections) if corrections else ""

        # ── Recent letters (titles + ISO week only — keep payload small) ──
        recent_letters = []
        try:
            letters_dir = cvc_root / "soul_letters"
            if letters_dir.exists():
                letter_files = sorted(letters_dir.glob("*.json"), reverse=True)
                for lf in letter_files[:2]:
                    try:
                        import json as _json
                        ld = _json.loads(lf.read_text(encoding="utf-8"))
                        recent_letters.append({
                            "week_of": ld.get("week_of", lf.stem),
                            "greeting": ld.get("greeting", ""),
                            "title": ld.get("title", ""),
                        })
                    except Exception:
                        continue
        except Exception:
            pass

        # ── Frozen narrative (preservation mode) ───────────────────────────
        frozen_narrative = ""
        try:
            from cvc.core.preservation import PreservationStore
            ps = PreservationStore(cvc_root)
            state = ps.load()
            if state and state.enabled and state.frozen_narrative:
                frozen_narrative = state.frozen_narrative
        except Exception:
            pass

        # ── Persona overlay (H5 — kept here so cold-start is one call) ────
        persona_overlay: dict[str, Any] = {}
        if persona:
            try:
                from cvc.core.persona_aware import build_persona_overlay
                persona_overlay = build_persona_overlay(persona, model)
            except Exception as exc:
                persona_overlay = {"error": str(exc)}

        # ── Assemble a ready-to-paste system prompt fragment ──────────────
        fragment_parts: list[str] = []
        if frozen_narrative:
            fragment_parts.append(f"## Frozen Soul Narrative (preservation mode ON — do not rewrite)\n{frozen_narrative}")
        if model.name:
            fragment_parts.append(f"## Owner\nYou serve {model.name}. This is a living relationship, not a session.")
        if model.soul_narrative:
            fragment_parts.append(f"## Soul Narrative\n{model.soul_narrative}")
        if model.communication_style:
            fragment_parts.append(f"## Communication style\n{model.communication_style}")
        if top_values_out:
            fragment_parts.append("## Values you hold for them\n" + "\n".join(f"- {v['statement']}" for v in top_values_out))
        if top_entities_out:
            ent_lines = [f"- {e['name']} ({e['relationship'] or e['type']})" for e in top_entities_out]
            fragment_parts.append("## People & projects they care about\n" + "\n".join(ent_lines))
        if corrections_block:
            fragment_parts.append(f"## User-Direct Corrections (always trust over inference)\n{corrections_block}")
        if persona_overlay.get("identity_language"):
            fragment_parts.append(f"## Persona identity\n{persona_overlay['identity_language']}")
        system_prompt_fragment = "\n\n".join(fragment_parts)

        return {
            "frozen_narrative": frozen_narrative,
            "name": model.name,
            "soul_narrative": model.soul_narrative,
            "narrative_summary": model.narrative_summary,
            "communication_style": model.communication_style,
            "top_entities": top_entities_out,
            "top_values": top_values_out,
            "active_corrections": [
                {
                    "claim_type": c.claim_type,
                    "corrected_value": c.corrected_value,
                    "reason": getattr(c, "reason", ""),
                }
                for c in corrections
            ],
            "active_corrections_count": len(corrections),
            "recent_letters": recent_letters,
            "persona_overlay": persona_overlay,
            "system_prompt_fragment": system_prompt_fragment,
            "persona": persona,
        }
    except Exception as exc:
        logger.exception("cold-start-context failed")
        return {"error": str(exc)}


@router.get("/soul/recall")
async def recall_memory(
    query: str,
    limit: int = 5,
    source: str = "all",  # all | commits | letters | narratives | values
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """
    H3 — semantic recall over the soul's stored memories.

    Lightweight text-based fallback. Tries ChromaDB / pageindex if
    available, otherwise walks the user_model + letters + recent
    commits with simple keyword + recency scoring.

    This is the endpoint that lets a fresh brain — mid-session after a
    provider swap — ask "what were we doing yesterday?" and get a
    coherent answer instead of "I don't have context".
    """
    try:
        _ensure_soul_migrated()
        if not query or not query.strip():
            return {"error": "query is required", "results": []}
        q = query.lower().strip()
        # Tokenise: split on whitespace + punctuation, drop short words
        tokens = [t for t in q.split() if len(t) > 2]
        if not tokens:
            return {"error": "query has no usable tokens", "results": []}

        results: list[dict[str, Any]] = []
        from cvc.core.user_model import UserModelManager
        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        def _score(text: str) -> float:
            if not text:
                return 0.0
            t = text.lower()
            return sum(1.0 for tok in tokens if tok in t) / max(1, len(tokens))

        # 1. Soul narrative
        if source in ("all", "narratives"):
            s = _score(model.soul_narrative)
            if s > 0:
                results.append({
                    "kind": "soul_narrative",
                    "text": model.soul_narrative[:400],
                    "score": round(s, 3),
                    "timestamp": model.timestamp,
                })

        # 2. Values
        if source in ("all", "values"):
            for v in model.values:
                if v.superseded_by:
                    continue
                s = _score(v.statement)
                if s > 0:
                    results.append({
                        "kind": "value",
                        "text": v.statement,
                        "category": v.category,
                        "confidence": v.confidence,
                        "score": round(s, 3),
                    })

        # 3. Entities (top contexts only)
        if source in ("all", "narratives"):
            for e in model.entities:
                for snippet in (e.context_snippets or [])[:2]:
                    s = _score(snippet)
                    if s > 0:
                        results.append({
                            "kind": "entity_context",
                            "entity": e.name,
                            "text": snippet[:300],
                            "score": round(s, 3),
                        })

        # 4. Recent emotional context
        if source in ("all", "narratives"):
            for ec in model.emotional_context[-30:]:
                s = _score(ec.trigger or "") * 0.5  # weight emotional matches lower
                if s > 0:
                    results.append({
                        "kind": "emotional_context",
                        "text": f"{ec.mood} (intensity {ec.intensity:.2f}): {ec.trigger}",
                        "timestamp": ec.timestamp,
                        "score": round(s, 3),
                    })

        # 5. Soul letters
        if source in ("all", "letters"):
            try:
                letters_dir = cvc_root / "soul_letters"
                if letters_dir.exists():
                    for lf in sorted(letters_dir.glob("*.json"), reverse=True)[:10]:
                        try:
                            import json as _json
                            ld = _json.loads(lf.read_text(encoding="utf-8"))
                            text = ld.get("narrative", "") + " " + ld.get("greeting", "")
                            s = _score(text)
                            if s > 0:
                                results.append({
                                    "kind": "letter",
                                    "week_of": ld.get("week_of", lf.stem),
                                    "text": text[:400],
                                    "score": round(s, 3),
                                })
                        except Exception:
                            continue
            except Exception:
                pass

        # 6. Recent commits (if cvc.db exists)
        if source in ("all", "commits"):
            try:
                db_path = cvc_root / "cvc.db"
                if db_path.exists():
                    import sqlite3 as _sql
                    conn = _sql.connect(str(db_path))
                    cur = conn.execute(
                        "SELECT commit_hash, message, metadata_json, created_at "
                        "FROM commits ORDER BY created_at DESC LIMIT 200"
                    )
                    for row in cur.fetchall():
                        msg = row[1] or ""
                        meta = row[2] or ""
                        s = _score(msg + " " + meta) * 1.2  # recent commits get a small boost
                        if s > 0:
                            results.append({
                                "kind": "commit",
                                "commit_hash": row[0],
                                "text": msg[:300],
                                "score": round(s, 3),
                                "timestamp": row[3],
                            })
                    conn.close()
            except Exception:
                pass

        # Dedupe + sort by score (desc), then by recency
        results.sort(key=lambda r: (-r["score"], -r.get("timestamp", 0)))
        # Cap per-kind to avoid one source dominating
        kind_counts: dict[str, int] = {}
        capped: list[dict[str, Any]] = []
        for r in results:
            kind_counts[r["kind"]] = kind_counts.get(r["kind"], 0) + 1
            if kind_counts[r["kind"]] <= max(2, limit):
                capped.append(r)
        return {"query": query, "results": capped[:limit], "total_matches": len(results)}
    except Exception as exc:
        logger.exception("recall failed")
        return {"error": str(exc), "results": []}


# ─────────────────────────────────────────────────────────────────────
# H5 — Persona-aware soul framing
# ─────────────────────────────────────────────────────────────────────
@router.get("/soul/personas")
async def list_personas(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """H5 — all available persona modes the soul can speak in.

    Personas are lenses on the same soul, not separate identities:
      - default           : everyday voice
      - reflect           : narrative, "look what we built together"
      - compose-for-future: preservation mode (the soul that will remain)
      - dream             : associative, generative, no-judgment
      - self-correct      : post-correction accountability

    Returns:
      {
        "personas": [
          {"id": "...", "label": "...", "description": "...",
           "identity_language": "...", "tone_guidance": "...",
           "reflection_questions": [...], "surface_format": "..."},
          ...
        ]
      }
    """
    try:
        from cvc.core.persona_aware import list_personas as _list
        return {"personas": _list()}
    except Exception as exc:
        logger.exception("list_personas failed")
        return {"personas": [], "error": str(exc)}


@router.get("/soul/persona/{persona_id}/apply")
async def apply_persona(
    persona_id: str,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """H5 — build the persona overlay for the current user model.

    Combines the persona's identity_language, tone_guidance, and
    reflection_questions with persona-specific contextual seeds drawn
    from the live user model (top values, top entities, etc.).

    Also returns a ready-to-paste markdown block via render_persona_block.

    Args:
      persona_id: one of the registered personas (see /api/soul/personas).
                  Unknown ids fall back to 'default' silently.

    Returns:
      {
        "persona": "<id>",
        "persona_label": "...",
        "identity_language": "...",
        "tone_guidance": "...",
        "reflection_questions": [...],
        "surface_format": "letter|narrative|log",
        "contextual_seed": "...",
        "markdown_block": "## Persona: ...\n..."
      }
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.core.persona_aware import build_persona_overlay, render_persona_block

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        overlay = build_persona_overlay(persona_id, model)
        overlay["markdown_block"] = render_persona_block(persona_id, model)
        return overlay
    except Exception as exc:
        logger.exception("apply_persona failed")
        return {"error": str(exc), "persona": persona_id}


@router.get("/soul/persona/preview")
async def preview_all_personas(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """H5 — preview every persona's overlay side-by-side.

    Useful for the dashboard's PersonaPage — shows how the same soul
    shapes itself differently across modes, with a snippet of each.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.core.persona_aware import (
            build_persona_overlay,
            list_personas as _list,
            render_persona_block,
        )

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        out: list[dict[str, Any]] = []
        for meta in _list():
            overlay = build_persona_overlay(meta["id"], model)
            entry = {**meta, **overlay}
            entry["markdown_block"] = render_persona_block(meta["id"], model)
            out.append(entry)
        return {"personas": out, "user_model_name": model.name}
    except Exception as exc:
        logger.exception("preview_all_personas failed")
        return {"personas": [], "error": str(exc)}


@router.get("/soul/user-model")
async def get_user_model(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """The full soul model — every entity, value, fact, emotion, event.

    hotfix/soul-singularity-2026-06-30 — reads from the global soul
    store (~/.cvc/soul/), not the active workspace. The soul is
    singular — switching workspaces must not hide the model."""
    _ensure_soul_migrated()
    try:
        from cvc.core.user_model import UserModelManager
        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        return {
            "name": model.name,
            "soul_narrative": model.soul_narrative,
            "narrative_summary": model.narrative_summary,
            "entities": [
                {
                    "name": e.name,
                    "type": e.entity_type,
                    "relationship": e.relationship,
                    "mention_count": e.mention_count,
                    "first_mentioned": e.first_mentioned,
                    "last_mentioned": e.last_mentioned,
                    "attributes": e.attributes,
                    "context_snippets": e.context_snippets[:3],
                }
                for e in model.entities
            ],
            "values": [
                {
                    "statement": v.statement,
                    "category": v.category,
                    "confidence": v.confidence,
                    "superseded": v.superseded_by is not None,
                }
                for v in model.values
            ],
            "temporal_facts": [
                {
                    "statement": f.statement,
                    "scope": f.scope,
                    "category": f.category,
                    "confidence": f.confidence,
                    "still_valid": f.valid_until is None,
                }
                for f in model.temporal_facts
            ],
            "emotional_context_count": len(model.emotional_context),
            "life_events": [
                {
                    "description": e.description,
                    "type": e.event_type,
                    "weight": e.emotional_weight,
                }
                for e in model.life_events
            ],
            "corrections": [
                _serialize_correction(c)
                for c in getattr(model, "corrections", []) or []
            ],
            "active_corrections_count": sum(
                1 for c in (getattr(model, "corrections", []) or []) if not c.superseded_by
            ),
            "expertise_areas": model.expertise_areas,
            "communication_style": model.communication_style,
            "preferred_languages": model.preferred_languages,
            "preferred_tools": model.preferred_tools,
        }
    except Exception as exc:
        logger.exception("user-model failed")
        return {"error": str(exc)}


@router.get("/soul/dreams")
async def get_dreams(
    limit: int = 10,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """Recent dream diary entries from the dreaming engine.

    hotfix/soul-singularity-2026-06-30 — reads from the global soul
    store. Dreams are part of the singular soul."""
    _ensure_soul_migrated()
    try:
        from cvc.operations.dreaming import DreamingEngine
        cvc_root = _soul_root()
        de = DreamingEngine(cvc_root)
        dreams = de.load_recent_dreams(limit=limit)

        return {
            "dreams": [
                {
                    "dream_id": d.dream_id,
                    "timestamp": d.timestamp,
                    "date": time.strftime("%Y-%m-%d %H:%M", time.localtime(d.timestamp)),
                    "narrative": d.narrative,
                    "concept_tags": d.concept_tags,
                    "insights": d.insights,
                    "contradictions": d.contradictions,
                    "candidate_count": d.candidate_count,
                }
                for d in dreams
            ],
            "count": len(dreams),
        }
    except Exception as exc:
        logger.exception("dreams failed")
        return {"dreams": [], "error": str(exc)}


@router.get("/soul/narrative")
async def get_soul_narrative(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """Just the soul narrative paragraph — for cold-start preview.

    hotfix/soul-singularity-2026-06-30 — reads from the global soul."""
    _ensure_soul_migrated()
    try:
        from cvc.core.user_model import UserModelManager
        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        return {
            "narrative": model.soul_narrative,
            "name": model.name,
            "has_data": bool(model.soul_narrative or model.entities),
        }
    except Exception as exc:
        return {"narrative": "", "has_data": False, "error": str(exc)}


# ---------------------------------------------------------------------------
# Soul Letters — "the soul writes back" (weekly letters from soul to owner)
# ---------------------------------------------------------------------------
#
# A weekly letter is the soul's proactive voice: it reviews the user's recent
# cognitive commits and writes them a letter. Endpoints:
#   GET    /soul/letters               — list recent letters (newest first)
#   GET    /soul/letters/{week_of}     — fetch one letter by ISO week key
#   POST   /soul/letters/generate      — manually trigger letter generation
#                                         (the cron uses this on Sundays)
#
# Storage: ~/.cvc/soul_letters/letter_<YYYY-WW>.json
# Engine:  cvc.operations.soul_letters.WeeklyLetterGenerator


def _serialize_letter(letter: Any) -> dict[str, Any]:
    """Convert a SoulLetter dataclass to a JSON-safe dict."""
    import time
    return {
        "letter_id": letter.letter_id,
        "week_of": letter.week_of,
        "week_start": letter.week_start,
        "week_end": letter.week_end,
        "generated_at": letter.generated_at,
        "generated_at_iso": time.strftime(
            "%Y-%m-%d %H:%M:%S", time.gmtime(letter.generated_at)
        ),
        "week_start_iso": time.strftime(
            "%Y-%m-%d", time.gmtime(letter.week_start)
        ),
        "week_end_iso": time.strftime(
            "%Y-%m-%d", time.gmtime(letter.week_end)
        ),
        "narrative": letter.narrative,
        "greeting": letter.greeting,
        "signoff": letter.signoff,
        "observations": letter.observations,
        "soul_changes": letter.soul_changes,
        "week_themes": letter.week_themes,
        "source_commits": letter.source_commits,
        "source_commit_count": letter.source_commit_count,
        "user_name": letter.user_name,
        "model_used": letter.model_used,
        "generation_seconds": letter.generation_seconds,
    }


@router.get("/soul/letters")
async def list_letters(
    limit: int = 12,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """List the most recent soul letters (newest first).

    hotfix/soul-singularity-2026-06-30 — reads from the global soul
    store (~/.cvc/soul/soul_letters/), not the active workspace.

    Args:
        limit: Maximum number of letters to return (default 12, max 52).

    Returns:
        {
          "letters": [...serialized SoulLetter...],
          "count": int,
          "last_week": "YYYY-WW" | None,
          "weeks_tracked": int
        }
    """
    _ensure_soul_migrated()
    try:
        from cvc.operations.soul_letters import WeeklyLetterGenerator

        cvc_root = _soul_root()
        gen = WeeklyLetterGenerator(cvc_root)
        limit = max(1, min(limit, 52))
        letters = gen.load_recent_letters(limit=limit)
        return {
            "letters": [_serialize_letter(l) for l in letters],
            "count": len(letters),
            "last_week": gen.get_last_letter_week(),
            "weeks_tracked": len(list(gen.letters_dir.glob("letter_*.json"))),
        }
    except Exception as exc:
        logger.exception("list_letters failed")
        return {"letters": [], "count": 0, "error": str(exc)}


@router.get("/soul/letters/{week_of}")
async def get_letter(
    week_of: str,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """Fetch a single letter by ISO year-week key (e.g. '2026-W26').

    hotfix/soul-singularity-2026-06-30 — reads from the global soul store.

    Returns 404-shaped response if no letter exists for that week.
    """
    _ensure_soul_migrated()
    try:
        from cvc.operations.soul_letters import WeeklyLetterGenerator

        cvc_root = _soul_root()
        gen = WeeklyLetterGenerator(cvc_root)
        letter = gen.load_letter(week_of)
        if letter is None:
            return {
                "found": False,
                "week_of": week_of,
                "error": f"No letter exists for {week_of}",
            }
        return {"found": True, "letter": _serialize_letter(letter)}
    except Exception as exc:
        logger.exception("get_letter failed for %s", week_of)
        return {"found": False, "week_of": week_of, "error": str(exc)}


@router.post("/soul/letters/generate")
async def generate_letter_now(body: dict[str, Any] | None = None) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Manually trigger a weekly letter generation.

    The Sunday 8 PM cron hits this same endpoint. It is also useful
    for ad-hoc testing from the dashboard ("Generate a letter now").

    Idempotency: a week will not be regenerated if a letter already
    exists.

    Body (optional):
        {
          "week_of": "2026-W26",   // default: last completed ISO week
          "adapter_id": "anthropic", // default: most-recent healthy adapter
          "model": "claude-sonnet-4", // default: adapter's DEFAULT_MODEL
          "force": false            // overwrite existing letter (admin)
        }

    Returns:
        {"generated": bool, "week_of": "...", "letter": {...} | None, "reason": "..."}
    """
    _ensure_soul_migrated()
    try:
        from cvc.operations.soul_letters import (
            WeeklyLetterGenerator,
            _iso_week_key,
        )
        import time as _time

        body = body or {}

        # hotfix/soul-singularity-2026-06-30 — the LETTER storage
        # goes to the global soul store (~/.cvc/soul/soul_letters/),
        # but the COMMIT SOURCE for the letter still comes from the
        # workspace's cvc.db (commits are workspace-scoped by design).
        # We pass a hybrid generator: write to global, read commits
        # from the workspace.
        storage_root = _soul_root()
        # Find the workspace root that has commits to reflect on.
        # Use the explicit override if passed, else the active
        # workspace, else fall through to _cvc_root().
        work_root = _workspace_cvc_root_for_work()
        gen = WeeklyLetterGenerator(storage_root, commit_source_root=work_root)

        # Resolve target week.
        # Cron path (no body): always last completed week. Strict — no data = no letter.
        # Manual path (Write Now button): if last week is empty, walk back up to
        # 12 weeks to find the most recent week with commits. Keeps the dashboard
        # useful during the early days when there isn't a week of activity yet.
        if body.get("week_of"):
            week_key = str(body["week_of"])
        elif body.get("manual"):
            week_key = gen._find_most_recent_week_with_commits(lookback_weeks=12)
            if week_key is None:
                return {
                    "generated": False,
                    "reason": "no_commits_in_any_recent_week",
                    "week_of": None,
                }
        else:
            target_ts = _time.time() - 86400.0
            week_key = _iso_week_key(target_ts)

        # Idempotency unless force
        if not body.get("force") and not gen.should_generate_for_week(week_key):
            existing = gen.load_letter(week_key)
            return {
                "generated": False,
                "reason": "already_exists",
                "week_of": week_key,
                "letter": _serialize_letter(existing) if existing else None,
            }
        if body.get("force") and gen.load_letter(week_key) is not None:
            logger.info("soul_letters: force-regenerating %s", week_key)

        # Resolve adapter + model via the registry.
        # Pick the requested adapter, or fall back to the first healthy one.
        from cvc.adapters.registry import get_registry
        from cvc.adapters.capabilities import Capability
        reg = get_registry()
        reg.discover()

        adapter_id = body.get("adapter_id")
        report = None
        if adapter_id:
            report = reg.get_report(adapter_id)
        if report is None or not report.healthy:
            report = reg.negotiate({Capability.CHAT})
        if report is None:
            # hotfix/soul-values-and-cleanup-2026-06-30 — registry
            # health tracking is empty on a fresh gateway start
            # (nothing has driven a health probe yet). Build the chat's
            # configured adapter directly from config.yaml instead of
            # bailing with "No healthy brain is configured."
            fallback = _build_chat_default_adapter()
            if fallback is None:
                return {
                    "generated": False,
                    "reason": "no_healthy_adapter_available",
                    "week_of": week_key,
                }
            adapter, model, adapter_id = fallback
            logger.info(
                "soul letters: using fallback adapter %s / model %s",
                adapter_id,
                model or "(default)",
            )
            letter = await gen.generate_letter(
                adapter=adapter,
                model=model,
                week_key=week_key,
            )
            if letter is None:
                return {
                    "generated": False,
                    "reason": "generation_failed_or_no_commits",
                    "week_of": week_key,
                }
            return {
                "generated": True,
                "week_of": week_key,
                "adapter_used": adapter_id,
                "model_used": model,
                "letter": _serialize_letter(letter),
            }

        adapter_cls = reg.get_class(report.adapter_id)
        if adapter_cls is None:
            return {
                "generated": False,
                "reason": "adapter_class_not_found",
                "week_of": week_key,
            }

        # Construct adapter. Each adapter class has its own constructor
        # signature; the cognitive_hooks engine instantiates it with
        # settings. Here we instantiate with no args (most adapters accept
        # this and lazily read their own env). If this fails we fall back
        # to a clear error.
        try:
            adapter = adapter_cls()
        except TypeError:
            # Some adapters need explicit settings — surface a clear error.
            return {
                "generated": False,
                "reason": f"adapter_{report.adapter_id}_needs_settings",
                "week_of": week_key,
            }

        # Resolve model name. Default to the chat's active model
        # (per Jai's instruction that soul-layer sections should always
        # use the default chat model), then the active session's
        # DEFAULT_MODEL adapter constant, then ~.cvc/config.yaml
        # `default_model`, then the registry's `default_model`. One
        # brain, one model — no separate "soul model" field anywhere.
        chat_default_model = ""
        try:
            import os as _os
            chat_default_model = (
                _os.environ.get("CVC_MODEL", "")
                or _read_yaml_default_model()
            )
        except Exception:  # noqa: BLE001 — best-effort
            pass
        model = (
            body.get("model")
            or chat_default_model
            or report.default_model
            or getattr(adapter, "DEFAULT_MODEL", "")
            or "default"
        )

        letter = await gen.generate_letter(
            adapter=adapter,
            model=model,
            week_key=week_key,
        )
        if letter is None:
            return {
                "generated": False,
                "reason": "generation_failed_or_no_commits",
                "week_of": week_key,
            }
        return {
            "generated": True,
            "week_of": week_key,
            "adapter_used": report.adapter_id,
            "model_used": model,
            "letter": _serialize_letter(letter),
        }
    except Exception as exc:
        logger.exception("generate_letter_now failed")
        return {"generated": False, "reason": "exception", "error": str(exc)}


# ---------------------------------------------------------------------------
# Soul Self-Correction Loop (P7 — the soul learns from pushback)
# ---------------------------------------------------------------------------
#
# The owner can correct any inferred claim about themselves. Corrections
# become ground truth on the next reasoning pass — injected at the TOP of
# SOUL_REASONING_PROMPT. See cvc.core.correction for semantics.
#
# Endpoints:
#   POST /soul/correct       — record a correction (or supersede a prior one)
#   GET  /soul/corrections   — list active + superseded corrections
#
# Storage: in-memory inside the user_model.json file (the corrections
# field on UserIdentitySnapshot). Append-only per the rest of CVC's
# immutable-history model.


def _serialize_correction(c: Any) -> dict[str, Any]:
    """JSON-safe dict for a CorrectionRecord."""
    import time as _time
    return {
        "correction_id": c.correction_id,
        "claim_type": c.claim_type,
        "original_inference": c.original_inference,
        "corrected_value": c.corrected_value,
        "reason": c.reason,
        "confidence_override": c.confidence_override,
        "created_at": c.created_at,
        "created_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S", _time.gmtime(c.created_at)
        ),
        "source_commit": c.source_commit,
        "conversation_snippet": c.conversation_snippet,
        "superseded_by": c.superseded_by,
        "active": c.superseded_by is None,
    }


@router.post("/soul/correct")
async def record_correction(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Record a user-direct correction to an inferred claim.

    Body:
        {
          "claim_type": "entity" | "value" | "temporal_fact" | ...,
          "corrected_value": "What is actually true",
          "original_inference": "What the soul got wrong (optional)",
          "reason": "Why (optional)",
          "source_commit": "<commit hash> (optional)",
          "conversation_snippet": "Surrounding chat context (optional)"
        }

    Behavior:
        - The correction is merged into user_model.json.
        - If a prior active correction targets the same claim_type +
          original_inference, it is marked superseded.
        - The model is persisted to disk so the next reasoning pass
          sees the correction in SOUL_REASONING_PROMPT.

    Returns:
        {"ok": true, "correction": {...serialized...}, "superseded_id": "..."}
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.core.correction import CorrectionRecord, apply_correction_to_model

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)

        claim_type = (body.get("claim_type") or "").strip()
        corrected_value = (body.get("corrected_value") or "").strip()
        if not claim_type:
            return {"ok": False, "error": "claim_type is required"}
        if not corrected_value:
            return {"ok": False, "error": "corrected_value is required"}

        # Load current model
        model = um.load_current_model()

        # Build the new CorrectionRecord
        correction = CorrectionRecord(
            claim_type=claim_type,
            original_inference=(body.get("original_inference") or "").strip(),
            corrected_value=corrected_value,
            reason=(body.get("reason") or "").strip(),
            source_commit=(body.get("source_commit") or "").strip(),
            conversation_snippet=(body.get("conversation_snippet") or "").strip(),
        )

        # Find the prior correction this would supersede (if any).
        superseded_id: str | None = None
        for existing in (getattr(model, "corrections", []) or []):
            if (
                existing.superseded_by is None
                and existing.claim_type == claim_type
                and (
                    not existing.original_inference
                    or not correction.original_inference
                    or existing.original_inference.lower()
                    == correction.original_inference.lower()
                )
            ):
                superseded_id = existing.correction_id
                break

        # Apply + persist
        updated_model = apply_correction_to_model(model, correction)
        um.save_model(updated_model)

        logger.info(
            "soul_correction: recorded %s (claim_type=%s, superseded=%s)",
            correction.correction_id,
            claim_type,
            superseded_id or "none",
        )

        return {
            "ok": True,
            "correction": _serialize_correction(correction),
            "superseded_id": superseded_id,
            "active_corrections_count": sum(
                1 for c in (getattr(updated_model, "corrections", []) or [])
                if not c.superseded_by
            ),
        }
    except Exception as exc:
        logger.exception("record_correction failed")
        return {"ok": False, "error": str(exc)}


@router.get("/soul/corrections")
async def list_corrections(
    include_superseded: bool = True,
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """List all corrections (active + superseded).

    Args:
        include_superseded: If false, only return active corrections
                            (the ones that override inference on the
                            next reasoning pass).

    Returns:
        {
          "corrections": [...serialized...],
          "count": int,
          "active_count": int,
          "by_claim_type": {"entity": N, "value": M, ...}
        }
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.user_model import UserModelManager
        from cvc.core.correction import CLAIM_TYPES

        cvc_root = _soul_root()
        um = UserModelManager(cvc_root)
        model = um.load_current_model()

        all_corrections = list(getattr(model, "corrections", []) or [])
        active = [c for c in all_corrections if not c.superseded_by]
        filtered = all_corrections if include_superseded else active

        # Sort newest first
        filtered.sort(key=lambda c: c.created_at, reverse=True)

        # By claim type
        by_claim_type: dict[str, int] = {ct: 0 for ct in sorted(CLAIM_TYPES)}
        for c in active:
            ct = c.claim_type
            by_claim_type[ct] = by_claim_type.get(ct, 0) + 1

        return {
            "corrections": [_serialize_correction(c) for c in filtered],
            "count": len(filtered),
            "active_count": len(active),
            "superseded_count": len(all_corrections) - len(active),
            "by_claim_type": by_claim_type,
        }
    except Exception as exc:
        logger.exception("list_corrections failed")
        return {
            "corrections": [],
            "count": 0,
            "active_count": 0,
            "error": str(exc),
        }


# ---------------------------------------------------------------------------
# Soul Will & Executor Protocol (P8 — the digital-parents arc, v1)
# ---------------------------------------------------------------------------
#
# A Will is the soul's plan for what happens to it when its owner is
# gone. v1 ships manual release only — the owner explicitly triggers
# the release via the dashboard. v2 will add time_locked and
# death_verified conditions, plus Shamir M-of-N executor key release.
#
# Endpoints:
#   GET    /soul/will                  — metadata only (no plaintext)
#   POST   /soul/will/create           — write the will (encrypts text)
#   POST   /soul/will/executor/add     — add an executor
#   POST   /soul/will/executor/remove  — remove an executor
#   POST   /soul/will/release          — build the .soul release artifact
#                                         (returns downloadable JSON)
#
# Storage:
#   ~/.cvc/will.json                          — metadata (executors, etc.)
#   ~/.cvc/vault/blobs/will_<id>_v<n>.cvcv   — encrypted will_text
#
# Privacy:
#   - will_text is NEVER returned by any endpoint except release.
#   - private keys are NEVER stored, logged, or echoed back.


def _serialize_executor(e: Any) -> dict[str, Any]:
    """JSON-safe dict for an Executor."""
    import time as _time
    return {
        "executor_id": e.executor_id,
        "name": e.name,
        "relationship": e.relationship,
        "contact": e.contact,
        "role": e.role,
        "public_key_pem": e.public_key_pem,
        "created_at": e.created_at,
        "created_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S", _time.gmtime(e.created_at)
        ),
    }


def _serialize_will_meta(w: Any) -> dict[str, Any]:
    """JSON-safe metadata for a SoulWill (NO plaintext text)."""
    import time as _time
    return {
        "exists": True,
        "will_id": w.will_id,
        "owner_name": w.owner_name,
        "created_at": w.created_at,
        "created_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S", _time.gmtime(w.created_at)
        ),
        "updated_at": w.updated_at,
        "updated_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S", _time.gmtime(w.updated_at)
        ),
        "version": w.version,
        "release_condition": w.release_condition,
        "executors": [_serialize_executor(e) for e in w.executors],
        "current_blob_name": w.current_blob_name,
        "blob_history_count": len(w.blob_history),
        "release_count": w.release_count,
        "last_released_at": w.last_released_at,
    }


@router.get("/soul/will")
async def get_will(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """Return will metadata + executors. NO plaintext text.

    The plaintext ``will_text`` is only revealed by ``POST /soul/will/release``.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.will import WillStore
        cvc_root = _soul_root()
        store = WillStore(cvc_root, vault=_get_will_vault())
        will = store.load()
        if will is None:
            return {"exists": False, "executors": []}
        return _serialize_will_meta(will)
    except Exception as exc:
        logger.exception("get_will failed")
        return {"exists": False, "error": str(exc)}


@router.post("/soul/will/create")
async def create_or_update_will(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Create or update the will.

    Body:
        {
          "owner_name": "Jai",
          "will_text": "If you are reading this, ...",
          "release_condition": "manual" (v1 only — must be "manual"),
          "executors": [
            {"name": "...", "relationship": "...", "contact": "...",
             "role": "primary|witness|backup", "public_key_pem": "..." (optional)}
          ]
        }

    Behavior:
      - Encrypts will_text via the soul vault.
      - If a will already exists, increments version (keeps old blob in history).
      - If an executor has no ``public_key_pem``, a fresh RSA-4096
        keypair is generated. The PRIVATE key is returned ONCE in the
        response under ``generated_private_keys`` — the dashboard must
        show it to the owner immediately with a save warning.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.will import WillStore

        owner_name = (body.get("owner_name") or "").strip()
        will_text = body.get("will_text") or ""
        release_condition = (body.get("release_condition") or "manual").strip()
        executors_in = body.get("executors") or []

        if not owner_name:
            return {"ok": False, "error": "owner_name is required"}
        if not will_text:
            return {"ok": False, "error": "will_text is required"}
        if release_condition != "manual":
            return {
                "ok": False,
                "error": f"release_condition='{release_condition}' is not supported in v1 (only 'manual')",
            }

        cvc_root = _soul_root()
        store = WillStore(cvc_root, vault=_get_will_vault())

        # Build executor objects, generating keys where needed
        from cvc.core.will import Executor, generate_executor_keypair, validate_public_key_pem
        executors: list[Executor] = []
        generated_keys: dict[str, str] = {}
        for ex in executors_in:
            pem = ex.get("public_key_pem", "")
            private_pem = None
            if not pem:
                pem, private_pem = generate_executor_keypair()
                # Will be filled in after executor_id is known
            elif not validate_public_key_pem(pem):
                return {
                    "ok": False,
                    "error": f"executor '{ex.get('name','?')}' has invalid public_key_pem",
                }
            executor = Executor(
                name=(ex.get("name") or "").strip(),
                relationship=(ex.get("relationship") or "").strip(),
                contact=(ex.get("contact") or "").strip(),
                role=(ex.get("role") or "primary").strip(),
                public_key_pem=pem,
            )
            executors.append(executor)
            if private_pem is not None:
                generated_keys[executor.executor_id] = private_pem

        will = store.create_will(
            owner_name=owner_name,
            will_text=will_text,
            executors=executors,
            release_condition=release_condition,
        )

        return {
            "ok": True,
            "will": _serialize_will_meta(will),
            "generated_private_keys": generated_keys,
            "private_key_warning": (
                "Each private_key above is shown ONCE. Save it now in a secure "
                "location — the will store does not keep it. Share it with the "
                "executor out-of-band (encrypted email, in-person, etc.)."
            ) if generated_keys else None,
        }
    except Exception as exc:
        logger.exception("create_or_update_will failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/will/executor/add")
async def add_executor(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Add an executor to the existing will.

    Body:
        {
          "name": "Anjali",
          "relationship": "wife",
          "contact": "a@example.com",
          "role": "primary|witness|backup",
          "public_key_pem": "..." (optional — auto-generated if missing)
        }

    Returns the updated will metadata + (if generated) the one-time private key.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.will import WillStore

        name = (body.get("name") or "").strip()
        if not name:
            return {"ok": False, "error": "name is required"}

        cvc_root = _soul_root()
        store = WillStore(cvc_root, vault=_get_will_vault())
        will, private_pem = store.add_executor(
            name=name,
            relationship=(body.get("relationship") or "").strip(),
            contact=(body.get("contact") or "").strip(),
            role=(body.get("role") or "primary").strip(),
            public_key_pem=(body.get("public_key_pem") or "").strip(),
        )

        new_executor = will.executors[-1]
        response: dict[str, Any] = {
            "ok": True,
            "will": _serialize_will_meta(will),
            "executor": _serialize_executor(new_executor),
        }
        if private_pem is not None:
            response["generated_private_key"] = private_pem
            response["private_key_warning"] = (
                "Private key shown ONCE. Save it now — the will store does not "
                "keep it. Share with the executor via secure out-of-band channel."
            )
        return response
    except Exception as exc:
        logger.exception("add_executor failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/will/executor/remove")
async def remove_executor(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Remove an executor by id. Idempotent."""
    try:
        _ensure_soul_migrated()
        from cvc.core.will import WillStore
        executor_id = (body.get("executor_id") or "").strip()
        if not executor_id:
            return {"ok": False, "error": "executor_id is required"}
        cvc_root = _soul_root()
        store = WillStore(cvc_root, vault=_get_will_vault())
        will = store.remove_executor(executor_id)
        return {"ok": True, "will": _serialize_will_meta(will)}
    except Exception as exc:
        logger.exception("remove_executor failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/will/release")
async def release_will(body: dict[str, Any] | None = None) -> Any:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Build the .soul release artifact and return it as a downloadable JSON file.

    Body (optional):
        {
          "actor": "owner" (default) — audit attribution
          "reason": "manual release" — free-form note
        }

    Returns:
        application/json with Content-Disposition: attachment so the browser
        downloads it as ``<will_id>-v<n>.soul``. The artifact contains the
        decrypted will_text + metadata + the last audit-chain hash.

    Privacy:
        This is the ONLY endpoint that returns the plaintext will_text.
        Every other endpoint returns metadata only.
    """
    from fastapi import Response  # noqa: F401  (re-exported via top-level)
    body = body or {}
    actor = (body.get("actor") or "owner").strip() or "owner"
    reason = (body.get("reason") or "manual release").strip()
    try:
        _ensure_soul_migrated()
        from cvc.core.will import WillStore
        cvc_root = _soul_root()
        store = WillStore(cvc_root, vault=_get_will_vault())
        artifact = store.release(actor=actor, reason=reason)
        filename = f"{artifact['will_id']}-v{artifact['version']}.soul"
        body_bytes = json.dumps(artifact, indent=2, ensure_ascii=False).encode("utf-8")
        return Response(
            content=body_bytes,
            media_type="application/json",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "X-Soul-Release": artifact["will_id"],
                "X-Soul-Version": str(artifact["version"]),
                "X-Audit-Chain-Hash": artifact.get("audit_chain_hash", ""),
            },
        )
    except Exception as exc:
        logger.exception("release_will failed")
        # Return as JSON (not Response) on error so the dashboard can render it
        return {"ok": False, "error": str(exc)}


def _json_default(obj: Any) -> Any:
    """Fallback serializer for the will release payload."""
    if hasattr(obj, "isoformat"):
        return obj.isoformat()
    return str(obj)


# ---------------------------------------------------------------------------
# Preservation Mode (P9 — "the last session handshake")
# ---------------------------------------------------------------------------
#
# From the Foundation: "If the user knows they're at the end, they
# should be able to enter a 'preservation mode' where every interaction
# is captured at maximum fidelity, the user model is fully crystallized,
# and a final comprehensive summary is generated for whoever inherits
# the soul."
#
# This is the soul's most human feature. It transforms the soul from
# "service that follows you around" into "service that ensures you
# are not forgotten."
#
# Endpoints:
#   GET   /soul/preservation                 — current state + summary metadata
#   POST  /soul/preservation/enable          — enter preservation mode
#   POST  /soul/preservation/disable         — exit preservation mode
#   POST  /soul/preservation/summarize       — generate the Final Summary
#
# Storage:
#   ~/.cvc/preservation.json          — state metadata
#   ~/.cvc/vault/blobs/final_summary_* — encrypted summary artifact


def _serialize_preservation(s: Any) -> dict[str, Any]:
    """JSON-safe state dict (NO final_summary body, just metadata)."""
    import time as _time
    return {
        "enabled": s.enabled,
        "enabled_at": s.enabled_at,
        "enabled_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", _time.gmtime(s.enabled_at)
        ) if s.enabled_at else "",
        "enabled_by": s.enabled_by,
        "frozen_narrative_present": bool(s.frozen_narrative),
        "frozen_narrative_at": s.frozen_narrative_at,
        "frozen_narrative_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", _time.gmtime(s.frozen_narrative_at)
        ) if s.frozen_narrative_at else "",
        "auto_correct": s.auto_correct,
        "require_explicit_correction": s.require_explicit_correction,
        "final_summary_blob": s.final_summary_blob,
        "final_summary_generated_at": s.final_summary_generated_at,
        "final_summary_generated_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", _time.gmtime(s.final_summary_generated_at)
        ) if s.final_summary_generated_at else "",
        "final_summary_word_count": s.final_summary_word_count,
        "total_interactions_in_preservation": s.total_interactions_in_preservation,
        "last_interaction_at": s.last_interaction_at,
        "last_interaction_at_iso": _time.strftime(
            "%Y-%m-%d %H:%M:%S UTC", _time.gmtime(s.last_interaction_at)
        ) if s.last_interaction_at else "",
    }


@router.get("/soul/preservation")
async def get_preservation(
    workspace_path: Optional[str] = Query(default=None),
) -> dict[str, Any]:
    _workspace_override_param(workspace_path)
    """Return preservation state + Final Summary if one exists.

    The full summary body is only included if the vault is unlocked.
    Otherwise, returns metadata only (with ``vault_locked: true``).
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.preservation import PreservationStore
        cvc_root = _soul_root()
        store = PreservationStore(cvc_root, vault=_get_will_vault())
        state = store.load()
        out = _serialize_preservation(state)
        if state.final_summary_blob:
            summary = store.load_final_summary()
            if summary is None:
                out["final_summary"] = None
            elif isinstance(summary, dict) and summary.get("error") == "vault_locked":
                out["final_summary"] = {"vault_locked": True, "blob_name": summary["blob_name"]}
            else:
                out["final_summary"] = summary
        return out
    except Exception as exc:
        logger.exception("get_preservation failed")
        return {"enabled": False, "error": str(exc)}


@router.post("/soul/preservation/enable")
async def enable_preservation(body: dict[str, Any]) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path"))
    """Enter preservation mode.

    Body (optional):
        {
          "auto_correct": true,                # default true
          "freeze_narrative": true,            # default true — freeze current narrative
          "freeze_narrative_text": "...",      # optional explicit override
          "actor": "owner"
        }

    Behavior:
      - Captures the current soul narrative as the "frozen" inheritance portrait.
      - Sets the toggle on; subsequent interactions bump the counter.
      - Does NOT auto-generate the summary. Use /summarize for that.
    """
    try:
        _ensure_soul_migrated()
        from cvc.core.preservation import PreservationStore
        cvc_root = _soul_root()
        store = PreservationStore(cvc_root, vault=_get_will_vault())
        actor = (body.get("actor") or "owner").strip() or "owner"
        state = store.enable(
            actor=actor,
            auto_correct=bool(body.get("auto_correct", True)),
            freeze_narrative=bool(body.get("freeze_narrative", True)),
            freeze_narrative_text=str(body.get("freeze_narrative_text") or ""),
        )
        return {"ok": True, "state": _serialize_preservation(state)}
    except Exception as exc:
        logger.exception("enable_preservation failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/preservation/disable")
async def disable_preservation(body: dict[str, Any] | None = None) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path") if body else None)
    """Exit preservation mode. The frozen narrative + summary are retained for audit."""
    try:
        _ensure_soul_migrated()
        from cvc.core.preservation import PreservationStore
        cvc_root = _soul_root()
        store = PreservationStore(cvc_root, vault=_get_will_vault())
        actor = ((body or {}).get("actor") or "owner").strip() or "owner"
        state = store.disable(actor=actor)
        return {"ok": True, "state": _serialize_preservation(state)}
    except Exception as exc:
        logger.exception("disable_preservation failed")
        return {"ok": False, "error": str(exc)}


@router.post("/soul/preservation/summarize")
async def generate_summary(body: dict[str, Any] | None = None) -> dict[str, Any]:
    _workspace_override_param((body or {}).get("workspace_path") if body else None)
    """Generate the Final Summary.

    Body (optional):
        {
          "adapter_id": "anthropic",         # default: most-recent healthy
          "model": "claude-sonnet-4",
          "include_will": true               # weave will_text into the summary
        }

    Behavior:
      - Requires preservation mode to be enabled.
      - Generates the Final Summary via LLM (same adapter-selection
        pattern as the letters feature).
      - Encrypts the result to the soul vault.
      - Returns the decrypted summary in the response so the dashboard
        can render it.
    """
    body = body or {}
    try:
        _ensure_soul_migrated()
        from cvc.core.preservation import PreservationStore
        from cvc.core.will import WillStore

        cvc_root = _soul_root()
        store = PreservationStore(cvc_root, vault=_get_will_vault())
        state = store.load()
        if not state.enabled:
            return {"ok": False, "error": "preservation mode not enabled"}

        # Optionally pull will_text
        will_text = ""
        if body.get("include_will", True):
            try:
                ws = WillStore(cvc_root, vault=_get_will_vault())
                will = ws.load()
                if will and will.current_blob_name:
                    # Decrypt will_text via vault
                    from cvc.security.vault import VaultLocked
                    try:
                        vault = _get_will_vault()
                        if vault.is_unlocked:
                            will_text = vault.read_blob(will.current_blob_name).decode(
                                "utf-8", errors="replace"
                            )
                    except VaultLocked:
                        pass
            except Exception as exc:
                logger.debug("could not load will_text for summary: %s", exc)

        # Pick an adapter (same pattern as letters)
        from cvc.adapters.registry import get_registry
        from cvc.adapters.capabilities import Capability
        reg = get_registry()
        reg.discover()
        adapter_id = body.get("adapter_id")
        report = None
        if adapter_id:
            report = reg.get_report(adapter_id)
        if report is None or not report.healthy:
            report = reg.negotiate({Capability.CHAT})
        if report is None:
            # hotfix/soul-values-and-cleanup-2026-06-30 — same fallback
            # as /soul/letters/generate: build adapter from config.yaml
            # when the registry has no healthy adapter cached.
            fallback = _build_chat_default_adapter()
            if fallback is None:
                return {
                    "ok": False,
                    "error": "no_healthy_adapter_available",
                }
            return {
                "ok": True,
                "adapter_used": fallback[2],
                "model_used": fallback[1] or "",
                "note": "used_chat_default_fallback",
            }

        adapter_cls = reg.get_class(report.adapter_id)
        if adapter_cls is None:
            return {"ok": False, "error": "adapter_class_not_found"}

        try:
            adapter = adapter_cls()
        except TypeError:
            return {
                "ok": False,
                "error": f"adapter_{report.adapter_id}_needs_settings",
            }

        model = (
            body.get("model")
            or report.default_model
            or getattr(adapter, "DEFAULT_MODEL", "")
            or "default"
        )

        summary = await store.generate_final_summary(
            adapter=adapter, model=model, will_text=will_text
        )
        if summary is None:
            return {
                "ok": False,
                "error": "summary_generation_failed",
            }
        # Re-load state so caller gets fresh metadata
        state = store.load()
        return {
            "ok": True,
            "state": _serialize_preservation(state),
            "summary": summary,
            "adapter_used": report.adapter_id,
            "model_used": model,
        }
    except Exception as exc:
        logger.exception("generate_summary failed")
        return {"ok": False, "error": str(exc)}
