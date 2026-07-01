"""cvc.operations.soul_singularity — The soul is ONE thing.

hotfix/soul-singularity-2026-06-30 — the soul used to live in
``<workspace>/.cvc/user_model.json``, which meant switching workspaces
hid everything you'd built up. Letters, dreams, emotional context,
narratives — all of it disappeared when you changed the workspace picker
in the chat, because the read went to a different .cvc/.

That's wrong. The soul is singular — one body across all the user's
workspaces, all the channels, all the years. Workspace is only meaningful
for the project work itself (commits, branches, snapshots). The soul
captures from everywhere and shows the same thing everywhere.

This module provides the global soul store at ``~/.cvc/soul/`` and the
migration path that brings existing per-workspace soul data into the
global store on first access. Migration is idempotent — re-running it
is a no-op.

Storage layout
--------------
::

    ~/.cvc/soul/
    ├── user_model.json           # The merged identity snapshot
    ├── user_model_snapshots/     # Time-machine history of the global model
    ├── soul_letters/             # Weekly letters (letter_YYYY-Www.json)
    ├── dreams/                   # Dream diary entries (dream_*.json)
    ├── emotional_arc.jsonl       # One-line-per-event timeline
    ├── preservation.json         # Final-summary / preservation state
    └── .migrated                 # Per-workspace migration ledger (JSONL)

The legacy per-workspace files (``<ws>/.cvc/user_model.json``,
``<ws>/.cvc/soul_letters/``, ``<ws>/.cvc/dreams/``) are NOT deleted on
migration — they remain valid source data for the per-workspace
SnapshotStore (the time-machine UX still needs them). They are simply
no longer the canonical store for the soul.
"""
from __future__ import annotations

import json
import logging
import os
import time
from pathlib import Path
from typing import Any, Iterable

logger = logging.getLogger("cvc.soul_singularity")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SOUL_DIRNAME = "soul"
USER_MODEL_FILE = "user_model.json"
LETTERS_DIRNAME = "soul_letters"
DREAMS_DIRNAME = "dreams"
EMOTIONAL_ARC_FILE = "emotional_arc.jsonl"
PRESERVATION_FILE = "preservation.json"
SNAPSHOTS_DIRNAME = "user_model_snapshots"
MIGRATION_LEDGER = ".migrated"


def _soul_root() -> Path:
    """The single, workspace-agnostic soul store.

    Lives at ``~/.cvc/soul/`` regardless of which project the user is
    currently working in. This is the only place soul data should be
    read from or written to going forward. Per-workspace .cvc/ stays
    the home for commit history, branches, and snapshots.

    Override via ``CVC_SOUL_ROOT`` env var (used by tests).
    """
    override = os.environ.get("CVC_SOUL_ROOT")
    if override:
        p = Path(override).expanduser()
        p.mkdir(parents=True, exist_ok=True)
        return p
    p = Path.home() / ".cvc" / SOUL_DIRNAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def soul_user_model_path() -> Path:
    return _soul_root() / USER_MODEL_FILE


def soul_letters_dir() -> Path:
    p = _soul_root() / LETTERS_DIRNAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def soul_dreams_dir() -> Path:
    p = _soul_root() / DREAMS_DIRNAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def soul_emotional_arc_path() -> Path:
    return _soul_root() / EMOTIONAL_ARC_FILE


def soul_preservation_path() -> Path:
    return _soul_root() / PRESERVATION_FILE


def soul_snapshots_dir() -> Path:
    p = _soul_root() / SNAPSHOTS_DIRNAME
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------


def _workspace_cvc_candidates() -> list[Path]:
    """Best-effort: list every .cvc/ directory on the local machine.

    We walk $HOME one level deep — covers the common case (user has
    ``~/Projects/<name>/.cvc/`` directories). For deeper nesting we
    also scan $HOME/Projects (the macOS default for the user's setup).

    This list is used ONLY for migration: once we've copied data from
    each workspace's .cvc/ into ~/.cvc/soul/, we never look here again.
    """
    out: list[Path] = []
    home = Path.home()
    seen: set[str] = set()

    def _add(p: Path) -> None:
        try:
            p = p.resolve()
        except Exception:
            return
        s = str(p)
        if s in seen:
            return
        if p.is_dir() and (p / "cvc.db").exists():
            seen.add(s)
            out.append(p)

    # Direct: ~/.cvc/
    _add(home / ".cvc")

    # Common patterns: ~/Projects/*/, ~/Documents/*/, ~/*/.
    for parent in (home / "Projects", home / "Documents", home / "repos", home / "code", home / "work", home / "src"):
        if not parent.is_dir():
            continue
        try:
            for child in parent.iterdir():
                _add(child / ".cvc")
        except (PermissionError, OSError):
            continue

    # Also $HOME itself: ~/<name>/.cvc/ one level deep.
    try:
        for child in home.iterdir():
            if child.is_dir():
                _add(child / ".cvc")
    except (PermissionError, OSError):
        pass

    return out


def _migrated_workspaces() -> set[str]:
    """Read the migration ledger and return the set of workspace paths
    that have already been migrated."""
    ledger = _soul_root() / MIGRATION_LEDGER
    if not ledger.exists():
        return set()
    out: set[str] = set()
    try:
        for line in ledger.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                ws = rec.get("workspace")
                if ws:
                    out.add(str(ws))
            except Exception:
                continue
    except Exception:
        return set()
    return out


def _record_migration(workspace_root: Path, *, merged_entities: int, merged_values: int, merged_emotional: int, merged_letters: int, merged_dreams: int) -> None:
    ledger = _soul_root() / MIGRATION_LEDGER
    rec = {
        "workspace": str(workspace_root.resolve()),
        "timestamp": time.time(),
        "merged_entities": merged_entities,
        "merged_values": merged_values,
        "merged_emotional": merged_emotional,
        "merged_letters": merged_letters,
        "merged_dreams": merged_dreams,
    }
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec) + "\n")


def _merge_snapshot_into_global(src_path: Path) -> tuple[int, int, int]:
    """Merge one workspace's user_model.json into the global store.

    Returns (entities_added, values_added, emotional_added) — counts of
    new items that didn't already exist in the global model.
    """
    from cvc.core.user_model import UserModelManager

    src_manager = UserModelManager(src_path)
    src_model = src_manager.load_current_model()
    if not src_model.entities and not src_model.values and not src_model.emotional_context:
        return (0, 0, 0)

    dst_manager = UserModelManager(_soul_root())
    dst_model = dst_manager.load_current_model()

    ents_added = 0
    vals_added = 0
    emo_added = 0
    dedup_bumps = 0

    # Entities — dedup by lowercased name; merge mention_count.
    existing_keys = {e.name.lower(): e for e in dst_model.entities}
    for src_ent in src_model.entities:
        key = src_ent.name.lower()
        if key in existing_keys:
            dst_ent = existing_keys[key]
            dst_ent.mention_count = int(dst_ent.mention_count or 1) + int(src_ent.mention_count or 1)
            dst_ent.last_mentioned = max(float(dst_ent.last_mentioned or 0), float(src_ent.last_mentioned or 0))
            dedup_bumps += 1
        else:
            dst_model.entities.append(src_ent.model_copy(deep=True))
            existing_keys[key] = dst_model.entities[-1]
            ents_added += 1

    # Values — dedup by statement (lowercased); higher confidence wins.
    existing_val_keys = {v.statement.lower(): v for v in dst_model.values}
    for src_val in src_model.values:
        key = src_val.statement.lower()
        if key in existing_val_keys:
            dst_val = existing_val_keys[key]
            if src_val.confidence > dst_val.confidence:
                dst_val.confidence = src_val.confidence
                dst_val.category = src_val.category
            dst_val.last_reinforced = max(
                float(dst_val.last_reinforced or 0),
                float(src_val.last_reinforced or 0),
            )
            dedup_bumps += 1
        else:
            dst_model.values.append(src_val.model_copy(deep=True))
            existing_val_keys[key] = dst_model.values[-1]
            vals_added += 1

    # Emotional context — dedup by (mood, trigger); keep earliest seen.
    existing_emo_keys = {(e.mood, e.trigger): e for e in dst_model.emotional_context}
    for src_emo in src_model.emotional_context:
        key = (src_emo.mood, src_emo.trigger)
        if key in existing_emo_keys:
            continue
        dst_model.emotional_context.append(src_emo.model_copy(deep=True))
        existing_emo_keys[key] = dst_model.emotional_context[-1]
        emo_added += 1

    if ents_added or vals_added or emo_added or dedup_bumps:
        dst_manager.save_model(dst_model, trigger=f"migration_from_{src_path.parent}")

    return (ents_added, vals_added, emo_added)


def _merge_letters_into_global(src_cvc_root: Path) -> int:
    """Copy any letters from a workspace's soul_letters/ into the global store.

    Returns the count of new letters added. Existing letters (matched by
    week_of) are not overwritten — the first letter for a given week is
    the canonical one.
    """
    src_letters = src_cvc_root / LETTERS_DIRNAME
    if not src_letters.is_dir():
        return 0
    dst_letters = soul_letters_dir()
    added = 0
    for src_file in sorted(src_letters.glob("letter_*.json")):
        try:
            data = json.loads(src_file.read_text(encoding="utf-8"))
            week_of = data.get("week_of") or src_file.stem.replace("letter_", "")
            if not week_of:
                continue
            dst_file = dst_letters / src_file.name
            if dst_file.exists():
                # Already migrated — keep the existing one (first-wins)
                continue
            dst_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            added += 1
        except Exception as exc:
            logger.debug("migration: failed to migrate letter %s: %s", src_file, exc)
    return added


def _merge_dreams_into_global(src_cvc_root: Path) -> int:
    """Copy any dreams from a workspace's dreams/ into the global store."""
    src_dreams = src_cvc_root / DREAMS_DIRNAME
    if not src_dreams.is_dir():
        return 0
    dst_dreams = soul_dreams_dir()
    added = 0
    for src_file in sorted(src_dreams.glob("dream_*.json")):
        try:
            data = json.loads(src_file.read_text(encoding="utf-8"))
            dream_id = data.get("dream_id") or src_file.stem.replace("dream_", "")
            if not dream_id:
                continue
            dst_file = dst_dreams / src_file.name
            if dst_file.exists():
                continue
            dst_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            added += 1
        except Exception as exc:
            logger.debug("migration: failed to migrate dream %s: %s", src_file, exc)
    return added


def run_migration_once() -> dict[str, Any]:
    """Run the migration from every workspace's .cvc/ into ~/.cvc/soul/.

    Idempotent — re-running is a no-op. Returns a summary dict for logging.
    """
    migrated = _migrated_workspaces()
    candidates = [p for p in _workspace_cvc_candidates() if str(p.resolve()) not in migrated]

    # Filter out the global soul root itself if it appears in candidates.
    candidates = [p for p in candidates if p.resolve() != _soul_root().resolve()]

    totals = {
        "workspaces_scanned": 0,
        "workspaces_with_data": 0,
        "entities_added": 0,
        "values_added": 0,
        "emotional_added": 0,
        "letters_added": 0,
        "dreams_added": 0,
        "already_migrated": len(migrated),
    }

    for src in candidates:
        ents, vals, emo = _merge_snapshot_into_global(src)
        lets = _merge_letters_into_global(src)
        dreams = _merge_dreams_into_global(src)
        if ents or vals or emo or lets or dreams:
            _record_migration(
                src,
                merged_entities=ents,
                merged_values=vals,
                merged_emotional=emo,
                merged_letters=lets,
                merged_dreams=dreams,
            )
            totals["workspaces_with_data"] += 1
        totals["workspaces_scanned"] += 1
        totals["entities_added"] += ents
        totals["values_added"] += vals
        totals["emotional_added"] += emo
        totals["letters_added"] += lets
        totals["dreams_added"] += dreams

    if totals["workspaces_scanned"]:
        logger.info(
            "soul_singularity: scanned %d workspaces, %d had data "
            "(entities=%d, values=%d, emotional=%d, letters=%d, dreams=%d, "
            "already_migrated=%d)",
            totals["workspaces_scanned"],
            totals["workspaces_with_data"],
            totals["entities_added"],
            totals["values_added"],
            totals["emotional_added"],
            totals["letters_added"],
            totals["dreams_added"],
            totals["already_migrated"],
        )
    return totals


def ensure_migrated() -> None:
    """Run migration on first access. Cheap to call repeatedly — checks
    the ledger first."""
    run_migration_once()


# ---------------------------------------------------------------------------
# Convenience accessors used by the gateway
# ---------------------------------------------------------------------------


def get_global_user_model():
    """Return the global user model (migrated + current).

    Always returns a model — empty if no data anywhere yet.
    """
    ensure_migrated()
    from cvc.core.user_model import UserModelManager

    return UserModelManager(_soul_root()).load_current_model()


def save_global_user_model(model, *, trigger: str = "manual") -> Path:
    """Persist the global user model."""
    ensure_migrated()
    from cvc.core.user_model import UserModelManager

    return UserModelManager(_soul_root()).save_model(model, trigger=trigger)


def get_global_narrative() -> str:
    """Return the soul narrative paragraph from the global model."""
    ensure_migrated()
    from cvc.core.user_model import UserModelManager

    return UserModelManager(_soul_root()).get_soul_narrative()


def get_global_user_name() -> str:
    """Return the user's display name from the global model."""
    ensure_migrated()
    from cvc.core.user_model import UserModelManager

    model = UserModelManager(_soul_root()).load_current_model()
    return model.name or ""