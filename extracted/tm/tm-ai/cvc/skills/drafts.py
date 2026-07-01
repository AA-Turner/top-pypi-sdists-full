"""
cvc.skills.drafts — Storage, audit log, and lifecycle for auto-generated
skill drafts created by ``cvc.agent.auto_skill``.

Draft layout::

    ~/.cvc/skills/.drafts/
    ├── <draft-name>/
    │   └── SKILL.md                  (the draft itself)
    └── .audit.json                   (append-only audit log)

A draft is a SKILL.md with ``state: draft`` in its frontmatter and
audit metadata (``confidence``, ``source.session_id``, ``tool_sequence``)
so the dashboard can sort/filter without re-parsing the body.

Lifecycle:

    draft  →  approved   (moves to ~/.cvc/skills/<cat>/<name>/)
    draft  →  rejected   (deleted + audit marked rejected)

The audit log is append-only — once an entry is written it's never
rewritten. State transitions append a NEW entry referencing the
original draft, so we always have a full history.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

logger = logging.getLogger("cvc.skills.drafts")

# ── Paths ────────────────────────────────────────────────────────────

_CVC_HOME = Path(os.environ.get("CVC_HOME") or Path.home() / ".cvc")
DRAFTS_DIR: Path = _CVC_HOME / "skills" / ".drafts"
AUDIT_PATH: Path = DRAFTS_DIR / ".audit.json"
ACTIVE_SKILLS_DIR: Path = _CVC_HOME / "skills"

# Categories that auto-drafts may be promoted into. Mirrors the
# categories that already exist in cvc/bundled_skills/ so the
# approval path doesn't create unknown top-level dirs.
ALLOWED_CATEGORIES: set[str] = {
    "apple", "autonomous-ai-agents", "blockchain", "communication",
    "creative", "data-science", "devops", "diagramming", "dogfood",
    "domain", "email", "finance", "gaming", "gifs", "github", "health",
    "index-cache", "inference-sh", "mcp", "media", "migration", "mlops",
    "note-taking", "openclaw-imports", "payments", "plugins",
    "productivity", "projects", "red-teaming", "research", "security",
    "smart-home", "social-media", "software-development", "web-development",
    "yuanbao",
}


# ── Audit log ────────────────────────────────────────────────────────


def load_audit() -> list[dict[str, Any]]:
    """Read the audit log. Returns [] if the file doesn't exist yet."""
    if not AUDIT_PATH.exists():
        return []
    try:
        text = AUDIT_PATH.read_text(encoding="utf-8")
        data = json.loads(text)
        return data if isinstance(data, list) else []
    except Exception as e:
        logger.warning("drafts audit log unreadable (%s); returning []", e)
        return []


def append_audit(entry: dict[str, Any]) -> None:
    """Append an entry to the audit log atomically.

    Uses ``tempfile + os.replace`` so a concurrent process can't
    observe a half-written file.
    """
    import tempfile
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)
    existing = load_audit()
    entry = dict(entry)
    entry.setdefault("ts", _now_iso())
    existing.append(entry)
    payload = json.dumps(existing, indent=2, ensure_ascii=False)
    fd, tmp_path = tempfile.mkstemp(
        prefix=".audit-", suffix=".json", dir=str(DRAFTS_DIR.parent)
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(payload)
        os.replace(tmp_path, AUDIT_PATH)
    except Exception:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        raise


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ── Discovery ────────────────────────────────────────────────────────


@dataclass
class DraftRecord:
    """A discovered draft, view-model for the dashboard / CLI."""
    name: str
    path: Path
    confidence: float
    created_at: str
    source_session_id: str
    source_turn_id: str
    tool_sequence: list[str] = field(default_factory=list)
    file_extensions: list[str] = field(default_factory=list)
    skills_loaded: list[str] = field(default_factory=list)
    state: str = "draft"            # draft | approved | rejected
    description: str = ""
    signature_hash: str = ""

    def to_jsonable(self) -> dict[str, Any]:
        d = asdict(self)
        d["path"] = str(self.path)
        return d


def list_drafts(*, state: str | None = "draft") -> list[DraftRecord]:
    """Return all draft records. Default: only pending drafts.

    Pass ``state=None`` to include approved/rejected history.
    """
    audit = load_audit()
    # Latest state per name wins (audit is append-only with state entries).
    by_name: dict[str, dict[str, Any]] = {}
    for entry in audit:
        name = entry.get("name")
        if not name:
            continue
        # Latest entry for a name defines its current state.
        by_name[name] = entry
    out: list[DraftRecord] = []
    for name, entry in by_name.items():
        cur_state = entry.get("state", "draft")
        if state and cur_state != state:
            continue
        path = Path(entry.get("path") or (DRAFTS_DIR / name / "SKILL.md"))
        out.append(DraftRecord(
            name=name,
            path=path,
            confidence=float(entry.get("confidence", 0.0)),
            created_at=entry.get("ts") or entry.get("created_at") or "",
            source_session_id=entry.get("session_id", ""),
            source_turn_id=entry.get("turn_id", ""),
            tool_sequence=list(entry.get("tool_sequence") or []),
            file_extensions=list(entry.get("file_extensions") or []),
            skills_loaded=list(entry.get("skills_loaded") or []),
            state=cur_state,
            signature_hash=entry.get("signature_hash", ""),
            description=_read_description(path),
        ))
    out.sort(key=lambda r: r.created_at, reverse=True)
    return out


def list_pending_drafts() -> list[DraftRecord]:
    """Alias used by the dashboard / CLI for the most common call."""
    return list_drafts(state="draft")


# ── Description extractor (cheap, no PyYAML dependency) ──────────────


_DESC_RE = re.compile(
    r"^description:\s*(.+?)(?=\n[a-zA-Z_]+:|\n---|\Z)",
    re.MULTILINE | re.DOTALL,
)


def _read_description(skill_md: Path) -> str:
    if not skill_md.exists():
        return ""
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""
    m = _DESC_RE.search(text)
    if not m:
        return ""
    raw = m.group(1).strip()
    # Strip surrounding quotes if present
    if (raw.startswith('"') and raw.endswith('"')) or \
       (raw.startswith("'") and raw.endswith("'")):
        raw = raw[1:-1]
    return raw[:240]


# ── Approval / rejection ─────────────────────────────────────────────


def approve_draft(name: str, *, category: str | None = None) -> Path:
    """Move a draft to the active skill tree.

    By default, the category is derived from the skill name's tag
    set; if no category can be inferred, the draft is placed at
    ``~/.cvc/skills/<name>/`` (top-level, no category). Pass an
    explicit ``category=`` to override.

    Returns the destination path. Raises ``FileNotFoundError`` if
    the draft doesn't exist.
    """
    src_dir = DRAFTS_DIR / name
    src_md = src_dir / "SKILL.md"
    if not src_md.exists():
        raise FileNotFoundError(f"No draft named {name!r} at {src_md}")

    cat = category or _infer_category(src_md)
    if cat and cat not in ALLOWED_CATEGORIES:
        # Be conservative — fall back to top-level if the inferred
        # category is unknown.
        logger.warning("drafts: category %r not in ALLOWED_CATEGORIES; promoting top-level", cat)
        cat = None
    dst_dir = (ACTIVE_SKILLS_DIR / cat / name) if cat else (ACTIVE_SKILLS_DIR / name)
    dst_md = dst_dir / "SKILL.md"
    dst_dir.mkdir(parents=True, exist_ok=True)

    # Strip the audit-specific frontmatter fields on promotion so the
    # promoted skill looks like a hand-authored one.
    promoted_text = _strip_audit_frontmatter(src_md.read_text(encoding="utf-8"))
    dst_md.write_text(promoted_text, encoding="utf-8")

    # Move the draft directory to .archive/ rather than deleting, so
    # the user can recover if they made a mistake.
    archive_root = DRAFTS_DIR / ".archive" / name
    archive_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src_dir), str(archive_root))

    append_audit({
        "name": name,
        "state": "approved",
        "promoted_to": str(dst_md),
        "category": cat,
        "session_id": _last_known_session(name),
    })
    logger.info("drafts: approved %s → %s", name, dst_md)
    return dst_md


def reject_draft(name: str, *, reason: str | None = None) -> None:
    """Move a draft to ``.drafts/.archive/<name>/`` and mark rejected."""
    src_dir = DRAFTS_DIR / name
    if not src_dir.exists():
        raise FileNotFoundError(f"No draft named {name!r}")
    archive_root = DRAFTS_DIR / ".archive" / name
    archive_root.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src_dir), str(archive_root))
    append_audit({
        "name": name,
        "state": "rejected",
        "reason": reason,
        "session_id": _last_known_session(name),
    })
    logger.info("drafts: rejected %s", name)


def _last_known_session(name: str) -> str:
    """Return the session_id from the most recent draft entry for name."""
    audit = load_audit()
    for entry in reversed(audit):
        if entry.get("name") == name:
            return entry.get("session_id", "")
    return ""


def _infer_category(skill_md: Path) -> str | None:
    """Pick a category from the skill's `metadata.cvc.tags` if present.

    Falls back to None (top-level) when no category fits. Conservative —
    prefers no category over a wrong one, since the user can re-promote
    later via ``cvc skills drafts approve <name> --category=...``.
    """
    try:
        text = skill_md.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return None
    # Look for tags in frontmatter — cheap tolerant parse.
    tags_m = re.search(r"^tags:\s*\[(.+?)\]", text, re.MULTILINE)
    if not tags_m:
        return None
    tags_raw = tags_m.group(1)
    tags = {t.strip().strip('"').strip("'").lower() for t in tags_raw.split(",")}
    # Map well-known tags to categories.
    tag_to_cat = {
        "github": "github", "ml": "mlops", "mlops": "mlops",
        "research": "research", "creative": "creative",
        "media": "media", "email": "email", "apple": "apple",
        "smart-home": "smart-home", "social-media": "social-media",
        "mcp": "mcp", "productivity": "productivity",
        "data-science": "data-science", "devops": "devops",
        "security": "security", "gaming": "gaming",
        "payments": "payments", "blockchain": "blockchain",
        "web-dev": "web-development", "web": "web-development",
        "code-review": "software-development",
        "refactor": "software-development", "debug": "software-development",
        "test": "software-development", "build": "software-development",
    }
    for t in tags:
        if t in tag_to_cat and tag_to_cat[t] in ALLOWED_CATEGORIES:
            return tag_to_cat[t]
    return None


_AUDIT_KEYS_TO_STRIP = (
    "state", "confidence", "source", "tool_sequence_hash",
)


def _strip_audit_frontmatter(text: str) -> str:
    """Remove auto-skill audit fields from frontmatter on promotion.

    Keeps ``name``, ``description``, ``version``, ``author``, ``license``,
    ``metadata``. Removes ``state``, ``confidence``, ``source``, and the
    tool_sequence_hash from metadata.cvc.
    """
    if not text.startswith("---"):
        return text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return text
    fm_text, body = parts[1], parts[2]
    # Drop top-level audit keys
    for key in _AUDIT_KEYS_TO_STRIP:
        fm_text = re.sub(rf"^{key}:.*\n", "", fm_text, flags=re.MULTILINE)
        # Drop nested source: block (multiline)
        fm_text = re.sub(
            rf"^  {key}:.*(?:\n    .*)*\n", "", fm_text, flags=re.MULTILINE
        )
    return f"---\n{fm_text}---{body}"


# ── Endpoint helpers ────────────────────────────────────────────────


def drafts_summary() -> dict[str, Any]:
    """Return the small summary used by the dashboard's badge."""
    pending = list_pending_drafts()
    if not pending:
        return {"count": 0, "drafts": [], "highest_confidence": 0.0}
    by_conf = sorted(pending, key=lambda r: -r.confidence)
    return {
        "count": len(pending),
        "highest_confidence": by_conf[0].confidence,
        "drafts": [
            {
                "name": r.name,
                "confidence": r.confidence,
                "created_at": r.created_at,
                "description": r.description,
                "source_session_id": r.source_session_id,
                "source_turn_id": r.source_turn_id,
                "tool_count": len(set(r.tool_sequence)),
            }
            for r in by_conf[:10]   # top 10 for the badge popover
        ],
    }
