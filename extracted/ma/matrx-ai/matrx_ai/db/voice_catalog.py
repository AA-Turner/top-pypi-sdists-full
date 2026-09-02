"""Voice catalog reader — the DB-backed source of truth for TTS voices.

Reads ``ai.voices`` (the provider-agnostic catalog populated by the host's
``scripts/sync_voices.py``) through the host-injected ``Voices`` model. Lives in
matrx-ai because the agent_runners that pick voices (podcast, ...) live here and
must not import ``aidream/db`` — the model is injected via
``matrx_ai.configure(db_models={"Voices": Voices})`` and read back through the
registry, exactly like ``arm_managers``.

Standalone-safe: when no DB is configured (or the table is empty / errors), the
loader returns ``[]`` so callers fall back to their built-in constants. It never
raises.
"""

from __future__ import annotations

from typing import Any

from matrx_utils import vcprint

from matrx_ai.db._registry import get_model


async def load_enabled_voices(provider: str) -> list[dict[str, Any]]:
    """Return enabled, non-deleted catalog voices for ``provider`` as plain dicts.

    Each dict carries at least ``provider_voice_id``, ``name``, ``gender``,
    ``quality_score``, ``tags``. Returns ``[]`` on any failure (no DB configured,
    empty table, query error) so the caller keeps its built-in fallback.
    """
    try:
        Voices = get_model("Voices")
    except Exception:
        return []

    try:
        rows = await Voices.filter(
            provider=provider, enabled=True, deleted_at=None
        ).order_by("sort_order").all()
    except Exception as exc:  # noqa: BLE001 — degrade to fallback, never block
        vcprint(
            f"[voice-catalog] could not load '{provider}' voices from DB "
            f"({exc!r}); using built-in fallback.",
            color="yellow",
        )
        return []

    out: list[dict[str, Any]] = []
    for r in rows:
        vid = (getattr(r, "provider_voice_id", "") or "").strip()
        if not vid:
            continue
        out.append(
            {
                "provider_voice_id": vid,
                "name": getattr(r, "name", "") or vid,
                "gender": (getattr(r, "gender", "") or "unknown").strip().lower(),
                "quality_score": getattr(r, "quality_score", None),
                "tags": list(getattr(r, "tags", []) or []),
            }
        )
    return out
