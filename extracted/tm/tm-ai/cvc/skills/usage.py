"""
cvc.skills.usage — CVC-native skill state tracking (Phase 1A native port).

Tracks per-skill lifecycle state, pinned flag, and lightweight usage
counters in a sidecar JSON file at ``$CVC_HOME/skills/.usage.json``,
keyed by skill name.

Scope (Phase 1A):
    The minimum surface required by ``cvc.cli_skills``:

        STATE_ACTIVE, STATE_STALE, STATE_ARCHIVED     (constants)
        load_usage()         -> Dict[str, Dict[str, Any]]
        get_record(name)     -> Dict[str, Any]
        archive_skill(name)  -> Tuple[bool, str]
        restore_skill(name)  -> Tuple[bool, str]
        set_pinned(name, b)  -> None
        set_state(name, s)   -> None
        list_archived_skill_names() -> List[str]

The CVC-native port keeps the same function names and return shapes as
the vendored module so callers (notably ``cvc.cli_skills``) do not need
behavioral changes — only the import path moves.

Design notes
------------
* Sidecar, not frontmatter. Keeps operational telemetry out of
  user-authored SKILL.md content and avoids conflict pressure for
  bundled/hub skills.
* Atomic writes via tempfile + ``os.replace``.
* All counter bumps are best-effort: failures log at DEBUG and return
  silently. A broken sidecar never breaks the underlying tool call.
* Bundled and hub-installed skills are NEVER recorded as agent-created
  in the sidecar; they are filtered out at mutation time.
* File-level locking (``fcntl`` on POSIX, ``msvcrt`` on Windows)
  serialises read-modify-write across processes.
* Pydantic models (``SkillUsageRecord``, ``SkillUsageMap``) describe
  the on-disk schema for type-safety; runtime I/O uses plain dicts
  (the schema is permissive — old files may lack fields).

Lifecycle states:
    active    — default
    stale     — unused for > stale_after_days (config)
    archived  — unused for > archive_after_days (config); moved to .archive/
    pinned    — opt-out from auto transitions (boolean flag, orthogonal to state)
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from pydantic import BaseModel, Field

from cvc.core.logging import get_cvc_home

__all__ = [
    "STATE_ACTIVE",
    "STATE_STALE",
    "STATE_ARCHIVED",
    "SkillUsageRecord",
    "SkillUsageMap",
    "load_usage",
    "get_record",
    "archive_skill",
    "restore_skill",
    "set_pinned",
    "set_state",
    "list_archived_skill_names",
    "is_agent_created",
    "save_usage",
    "forget",
    "bump_use",
    "bump_view",
]

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Pydantic models — describe the on-disk schema (per record)
# ---------------------------------------------------------------------------

class SkillUsageRecord(BaseModel):
    """Schema for a single skill's usage record.

    All fields default to permissive values so old sidecar files (which
    may be missing fields) round-trip cleanly through validation.
    """

    model_config = {"extra": "allow"}

    created_by: Optional[str] = None
    use_count: int = 0
    view_count: int = 0
    last_used_at: Optional[str] = None
    last_viewed_at: Optional[str] = None
    patch_count: int = 0
    last_patched_at: Optional[str] = None
    created_at: Optional[str] = None
    state: str = "active"
    pinned: bool = False
    archived_at: Optional[str] = None
    agent_created: Optional[bool] = None


class SkillUsageMap(BaseModel):
    """Schema for the entire ``.usage.json`` sidecar."""

    model_config = {"extra": "allow"}

    # Map is open-ended — keys are skill names, values are records.
    records: Dict[str, Dict[str, Any]] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# State constants
# ---------------------------------------------------------------------------

STATE_ACTIVE = "active"
STATE_STALE = "stale"
STATE_ARCHIVED = "archived"
_VALID_STATES = {STATE_ACTIVE, STATE_STALE, STATE_ARCHIVED}


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

def _skills_dir() -> Path:
    """Return ``$CVC_HOME/skills`` (or ``HERMES_HOME/skills`` for compat)."""
    return get_cvc_home() / "skills"


def _usage_file() -> Path:
    """Return the sidecar ``.usage.json`` path."""
    return _skills_dir() / ".usage.json"


def _archive_dir() -> Path:
    """Return the archive directory path."""
    return _skills_dir() / ".archive"


# ---------------------------------------------------------------------------
# File locking
# ---------------------------------------------------------------------------

msvcrt = None
try:
    import fcntl
except ImportError:  # pragma: no cover - platform-specific fallback
    fcntl = None
    try:
        import msvcrt
    except ImportError:
        pass


@contextmanager
def _usage_file_lock():
    """Serialize ``.usage.json`` read-modify-write cycles across processes."""
    lock_path = _usage_file().with_suffix(".json.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    if fcntl is None and msvcrt is None:
        yield
        return

    if msvcrt and (not lock_path.exists() or lock_path.stat().st_size == 0):
        lock_path.write_text(" ", encoding="utf-8")

    fd = open(lock_path, "r+" if msvcrt else "a+", encoding="utf-8")
    try:
        if fcntl:
            fcntl.flock(fd, fcntl.LOCK_EX)
        else:
            fd.seek(0)
            msvcrt.locking(fd.fileno(), msvcrt.LK_LOCK, 1)  # type: ignore[union-attr]
        yield
    finally:
        if fcntl:
            fcntl.flock(fd, fcntl.LOCK_UN)
        elif msvcrt:
            try:
                fd.seek(0)
                msvcrt.locking(fd.fileno(), msvcrt.LK_UNLCK, 1)  # type: ignore[union-attr]
            except (OSError, IOError):
                pass
        fd.close()


# ---------------------------------------------------------------------------
# Time helpers
# ---------------------------------------------------------------------------

def _now_iso() -> str:
    """Return the current UTC time as an ISO-8601 string."""
    return datetime.now(timezone.utc).isoformat()


def _empty_record() -> Dict[str, Any]:
    """Return a fresh empty usage record (matches the vendored shape)."""
    return {
        "created_by": None,
        "use_count": 0,
        "view_count": 0,
        "last_used_at": None,
        "last_viewed_at": None,
        "patch_count": 0,
        "last_patched_at": None,
        "created_at": _now_iso(),
        "state": STATE_ACTIVE,
        "pinned": False,
        "archived_at": None,
    }


# ---------------------------------------------------------------------------
# Provenance (bundled / hub manifests)
# ---------------------------------------------------------------------------

def _read_bundled_manifest_names() -> Set[str]:
    """Return the set of skill names seeded from the bundled repo.

    Reads ``$CVC_HOME/skills/.bundled_manifest`` (format: ``name:hash``
    per line). Returns an empty set if the file is missing/unreadable.
    """
    manifest = _skills_dir() / ".bundled_manifest"
    if not manifest.exists():
        return set()
    names: Set[str] = set()
    try:
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            name = line.split(":", 1)[0].strip()
            if name:
                names.add(name)
    except OSError as e:
        logger.debug("Failed to read bundled manifest: %s", e)
    return names


def _read_hub_installed_names() -> Set[str]:
    """Return the set of skill names installed via the Skills Hub.

    Reads ``$CVC_HOME/skills/.hub/lock.json``.
    """
    lock_path = _skills_dir() / ".hub" / "lock.json"
    if not lock_path.exists():
        return set()
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            installed = data.get("installed") or {}
            if isinstance(installed, dict):
                names = {str(k) for k in installed.keys()}
                skills_dir = _skills_dir()
                for entry in installed.values():
                    if not isinstance(entry, dict):
                        continue
                    install_path = entry.get("install_path")
                    if not isinstance(install_path, str) or not install_path.strip():
                        continue
                    skill_dir = Path(install_path)
                    if not skill_dir.is_absolute():
                        skill_dir = skills_dir / install_path
                    try:
                        resolved = skill_dir.resolve()
                        resolved.relative_to(skills_dir.resolve())
                    except (OSError, ValueError):
                        continue
                    skill_md = resolved / "SKILL.md"
                    if skill_md.exists():
                        names.add(_read_skill_name(skill_md, fallback=resolved.name))
                return names
    except (OSError, json.JSONDecodeError) as e:
        logger.debug("Failed to read hub lock file: %s", e)
    return set()


def is_agent_created(skill_name: str) -> bool:
    """Return ``True`` when *skill_name* is neither bundled nor hub-installed."""
    off_limits = _read_bundled_manifest_names() | _read_hub_installed_names()
    return skill_name not in off_limits


# ---------------------------------------------------------------------------
# SKILL.md frontmatter parsing
# ---------------------------------------------------------------------------

_FRONTMATTER_NAME = re.compile(r"^\s*name\s*:\s*[\"']?([^\"'\n]+)[\"']?", re.IGNORECASE)


def _read_skill_name(skill_md: Path, fallback: str) -> str:
    """Parse the ``name:`` field from a SKILL.md YAML frontmatter.

    Falls back to *fallback* (typically the directory name) if the
    frontmatter is missing/invalid.
    """
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return fallback
    in_frontmatter = False
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped == "---":
            if in_frontmatter:
                break
            in_frontmatter = True
            continue
        if in_frontmatter and stripped.lower().startswith("name:"):
            value = stripped.split(":", 1)[1].strip().strip("\"'")
            if value:
                return value
    return fallback


# ---------------------------------------------------------------------------
# Sidecar I/O
# ---------------------------------------------------------------------------

def load_usage() -> Dict[str, Dict[str, Any]]:
    """Read the entire ``.usage.json`` map.

    Returns an empty dict on missing/corrupt file.  Non-dict values are
    silently dropped to keep callers safe against partial writes.
    """
    path = _usage_file()
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        logger.debug("Failed to read %s: %s", path, e)
        return {}
    if not isinstance(data, dict):
        return {}
    clean: Dict[str, Dict[str, Any]] = {}
    for k, v in data.items():
        if isinstance(v, dict):
            clean[str(k)] = v
    return clean


def save_usage(data: Dict[str, Dict[str, Any]]) -> None:
    """Write the usage map atomically.

    Best-effort — errors are logged at DEBUG, not raised.  Uses
    ``tempfile`` + ``os.replace`` for atomicity.
    """
    path = _usage_file()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(
            dir=str(path.parent), prefix=".usage_", suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, path)
        except BaseException:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise
    except Exception as e:
        logger.debug("Failed to write %s: %s", path, e, exc_info=True)


def get_record(skill_name: str) -> Dict[str, Any]:
    """Return the record for *skill_name*, creating a fresh one if missing.

    Any missing keys are backfilled from :func:`_empty_record` so callers
    can index any field without ``KeyError``.
    """
    data = load_usage()
    rec = data.get(skill_name)
    if not isinstance(rec, dict):
        return _empty_record()
    base = _empty_record()
    for k, v in base.items():
        rec.setdefault(k, v)
    return rec


def _mutate(skill_name: str, mutator) -> None:
    """Load → apply *mutator(record)* in place → save. Best-effort.

    Bundled and hub-installed skills are NEVER recorded in the sidecar.
    """
    if not skill_name:
        return
    try:
        if not is_agent_created(skill_name):
            return
        with _usage_file_lock():
            data = load_usage()
            rec = data.get(skill_name)
            if not isinstance(rec, dict):
                rec = _empty_record()
            mutator(rec)
            data[skill_name] = rec
            save_usage(data)
    except Exception as e:
        logger.debug("skill_usage._mutate(%s) failed: %s", skill_name, e, exc_info=True)


# ---------------------------------------------------------------------------
# Lifecycle setters
# ---------------------------------------------------------------------------

def set_state(skill_name: str, state: str) -> None:
    """Set the lifecycle *state* of *skill_name*. No-op if *state* is invalid."""
    if state not in _VALID_STATES:
        logger.debug("set_state: invalid state %r for %s", state, skill_name)
        return

    def _apply(rec: Dict[str, Any]) -> None:
        rec["state"] = state
        if state == STATE_ARCHIVED:
            rec["archived_at"] = _now_iso()
        elif state == STATE_ACTIVE:
            rec["archived_at"] = None

    _mutate(skill_name, _apply)


def set_pinned(skill_name: str, pinned: bool) -> None:
    """Set the *pinned* flag of *skill_name* (boolean)."""
    def _apply(rec: Dict[str, Any]) -> None:
        rec["pinned"] = bool(pinned)
    _mutate(skill_name, _apply)


# ---------------------------------------------------------------------------
# Usage counters (Phase 1B)
# ---------------------------------------------------------------------------


def bump_use(skill_name: str) -> None:
    """Increment the *use_count* of *skill_name* and stamp *last_used_at*.

    Idempotent against the file-lock layer; safe to call from any thread.
    No-op (with a debug log) if the skill does not exist in usage yet.
    """
    def _apply(rec: Dict[str, Any]) -> None:
        rec["use_count"] = int(rec.get("use_count", 0)) + 1
        rec["last_used_at"] = _now_iso()
    _mutate(skill_name, _apply)


def bump_view(skill_name: str) -> None:
    """Increment the *view_count* of *skill_name* and stamp *last_viewed_at*.

    Idempotent against the file-lock layer; safe to call from any thread.
    No-op (with a debug log) if the skill does not exist in usage yet.
    """
    def _apply(rec: Dict[str, Any]) -> None:
        rec["view_count"] = int(rec.get("view_count", 0)) + 1
        rec["last_viewed_at"] = _now_iso()
    _mutate(skill_name, _apply)


def forget(skill_name: str) -> None:
    """Drop a skill's usage entry entirely. Called when a skill is deleted."""
    if not skill_name:
        return
    try:
        with _usage_file_lock():
            data = load_usage()
            if skill_name in data:
                del data[skill_name]
                save_usage(data)
    except Exception as e:
        logger.debug("skill_usage.forget(%s) failed: %s", skill_name, e, exc_info=True)


# ---------------------------------------------------------------------------
# Archive / restore
# ---------------------------------------------------------------------------

def list_archived_skill_names() -> List[str]:
    """Enumerate skills in ``$CVC_HOME/skills/.archive/``.

    Archive layout is flat (``.archive/<skill>/``) as set by
    :func:`archive_skill`, so the directory name is the skill name.
    """
    archive_root = _archive_dir()
    if not archive_root.exists():
        return []
    return sorted({p.name for p in archive_root.iterdir() if p.is_dir()})


def _find_skill_dir(skill_name: str) -> Optional[Path]:
    """Locate the directory for *skill_name* by its frontmatter ``name:`` field.

    Handles both flat (``$CVC_HOME/skills/<skill>/SKILL.md``) and
    category-nested (``$CVC_HOME/skills/<category>/<skill>/SKILL.md``)
    layouts.
    """
    base = _skills_dir()
    if not base.exists():
        return None
    for skill_md in base.rglob("SKILL.md"):
        try:
            rel = skill_md.relative_to(base)
        except ValueError:
            continue
        if rel.parts and rel.parts[0].startswith("."):
            continue
        if _read_skill_name(skill_md, fallback=skill_md.parent.name) == skill_name:
            return skill_md.parent
    return None


def archive_skill(skill_name: str) -> Tuple[bool, str]:
    """Move an agent-created skill directory to ``.archive/``.

    Returns ``(ok, message)``. Refuses to archive bundled or hub skills
    as a safety net (callers should also check provenance).

    Archive layout is flattened to ``.archive/<skill>/``; on name
    collision a timestamp suffix is appended.
    """
    if not is_agent_created(skill_name):
        return False, f"skill '{skill_name}' is bundled or hub-installed; never archive"

    skill_dir = _find_skill_dir(skill_name)
    if skill_dir is None:
        return False, f"skill '{skill_name}' not found"

    archive_root = _archive_dir()
    try:
        archive_root.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        return False, f"failed to create archive dir: {e}"

    dest = archive_root / skill_dir.name
    if dest.exists():
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        dest = archive_root / f"{skill_dir.name}-{ts}"

    try:
        skill_dir.rename(dest)
    except OSError:
        # Cross-device — fall back to shutil.move
        try:
            shutil.move(str(skill_dir), str(dest))
        except Exception as e2:
            return False, f"failed to archive: {e2}"

    set_state(skill_name, STATE_ARCHIVED)
    return True, f"archived to {dest}"


def restore_skill(skill_name: str) -> Tuple[bool, str]:
    """Move an archived skill back to ``$CVC_HOME/skills/``.

    Restores to the flat top-level layout; original category nesting is
    NOT reconstructed. Refuses to restore under a name that would shadow
    a bundled or hub-installed skill.
    """
    if not is_agent_created(skill_name):
        return False, (
            f"skill '{skill_name}' is now bundled or hub-installed; "
            "restore would shadow the upstream version"
        )
    archive_root = _archive_dir()
    if not archive_root.exists():
        return False, "no archive directory"

    # Exact name match first, then prefix match (for timestamped dupes).
    candidates = [
        p for p in archive_root.rglob("*")
        if p.is_dir() and p.name == skill_name
    ]
    if not candidates:
        candidates = sorted(
            [
                p for p in archive_root.rglob("*")
                if p.is_dir() and p.name.startswith(f"{skill_name}-")
            ],
            reverse=True,
        )
    if not candidates:
        return False, f"skill '{skill_name}' not found in archive"

    src = candidates[0]
    dest = _skills_dir() / skill_name
    if dest.exists():
        return False, f"destination already exists: {dest}"

    try:
        src.rename(dest)
    except OSError:
        try:
            shutil.move(str(src), str(dest))
        except Exception as e:
            return False, f"failed to restore: {e}"

    set_state(skill_name, STATE_ACTIVE)
    return True, f"restored to {dest}"
