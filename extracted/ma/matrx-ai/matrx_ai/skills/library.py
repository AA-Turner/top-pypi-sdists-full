"""Platform library skills → ``skill.definition`` (AI Matrx's own skills).

A *platform library set* is a folder of SKILL.md files AI Matrx itself wrote for
the in-app skills library — public, end-user-facing skills an agent inside the
app loads and follows with our tools. The first set is our own version of each
imported outside SEO skill (Arman, 2026-09-27: *"for any actual skill that they
have ... we also need to take the text of the skill and create our own skill as
well for our skills library"*).

It is the third declared source beside the repo mirror (``ingest.py``, coding
agents' ``.claude/skills``, always ``internal``) and outside packs
(``packs.py``, faithful imports of someone else's text). Rules:

* **Declared, not discovered.** ``library/<set>/library.yaml`` names the set,
  its web lane (``published_to_web``), category and every skill in it; each declared skill must be a
  ``<skill_id>/SKILL.md`` folder whose frontmatter ``name`` equals its id, and
  every folder in the set must be declared (complete or loud). The set lives
  under the ``matrx_ai.skills`` package, which repo-mirror discovery never
  walks, so a repo ingest can never pick these up as ``internal`` mirrors.
* **Linked to what it derives from.** A skill may declare ``parent`` (a skill
  id) and the set may declare ``parent_pack`` (the outside pack that owns the
  parents); the write resolves it to ``parent_skill_id`` and refuses the skill
  when it does not match exactly one active row.
* **Paired both ways.** After the write, each of our rows carries
  ``config.derived_from`` (the original's id, skill id, pack, source repo and
  authors) and the original carries ``config.our_version`` (our id, skill id,
  set) — merged beside the pack's own stamps, never replacing them, so the pack
  ingest's re-run stays ``unchanged`` and the library UI can show each row's
  counterpart. Written only when it differs; a rerun writes nothing.
* **Owned by the set.** Rows carry ``config.ingested_from = "platform_library"``
  and ``config.library_set``; every other source sees them as foreign.
* **Re-runnable.** A second run over unchanged files is all ``unchanged``.

Run: ``uv run python scripts/ingest_skills.py --library <set dir> [--dry-run] [--prune]``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID

from matrx_ai.skills.ingest import (
    _VALID_SKILL_TYPES,
    ParsedSkill,
    _parse_content,
    _parse_frontmatter,
    _row_config,
    declared_published_to_web,
    ensure_skill_category,
    upsert_parsed_skills,
)

LIBRARY_DIR = Path(__file__).parent / "library"
PLATFORM_LIBRARY_SOURCE = "platform_library"
# Where the sets live, relative to the aidream repo root — stamped as
# ``config.source_path`` so a row's provenance is the same on every machine.
LIBRARY_REPO_PATH = "packages/matrx-ai/matrx_ai/skills/library"
MANIFEST_NAME = "library.yaml"


class LibraryError(ValueError):
    """The set's manifest or folder cannot be ingested completely."""


@dataclass
class LibrarySet:
    set_id: str
    title: str
    published_to_web: bool
    skill_type: str
    category: dict[str, Any]
    root: Path
    parent_pack: str | None = None
    # skill_id -> {"parent": <skill id> | None}
    skills: dict[str, dict[str, Any]] = field(default_factory=dict)


def load_library_set(set_dir: Path | str) -> LibrarySet:
    """Read and validate ``<set_dir>/library.yaml``. Raises :class:`LibraryError`."""
    import yaml  # type: ignore[import-not-found]

    root = Path(set_dir).expanduser().resolve()
    manifest = root / MANIFEST_NAME
    if not manifest.is_file():
        raise LibraryError(f"{root} has no {MANIFEST_NAME}")
    raw = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    try:
        ls = LibrarySet(
            set_id=str(raw["set_id"]),
            title=str(raw["title"]),
            published_to_web=declared_published_to_web(raw, f"skill library {manifest}"),
            skill_type=str(raw.get("skill_type", "reference")),
            category=dict(raw["category"]),
            root=root,
            parent_pack=(str(raw["parent_pack"]) if raw.get("parent_pack") else None),
            skills={
                str(k): {"parent": (str((v or {}).get("parent")) if (v or {}).get("parent") else None)}
                for k, v in (raw.get("skills") or {}).items()
            },
        )
    except KeyError as exc:
        raise LibraryError(f"{manifest} is missing required key {exc}") from exc
    except ValueError as exc:
        raise LibraryError(str(exc)) from exc
    if ls.skill_type not in _VALID_SKILL_TYPES:
        raise LibraryError(f"skill_type {ls.skill_type!r} is not a skl_skill_type value")
    if not ls.category.get("slug") or not ls.category.get("name"):
        raise LibraryError("category needs both slug and name")
    if not ls.skills:
        raise LibraryError(f"{manifest} declares no skills")
    for sid, spec in ls.skills.items():
        if spec["parent"] and spec["parent"] == sid:
            raise LibraryError(
                f"{sid!r} names itself as its parent; a derived skill needs its own id"
            )
    return ls


def walk_library_set(ls: LibrarySet) -> tuple[list[ParsedSkill], list[str]]:
    """Parse every declared skill. Returns ``(skills, errors)``; any error
    means the run must write nothing."""
    errors: list[str] = []
    skills: list[ParsedSkill] = []
    declared = set(ls.skills)
    for child in sorted(ls.root.iterdir()):
        if child.name == MANIFEST_NAME or child.name.startswith("."):
            continue
        if not child.is_dir() or child.name not in declared:
            errors.append(f"{child.name}: not a declared skill of set {ls.set_id!r}")
    for sid, spec in sorted(ls.skills.items()):
        path = ls.root / sid / "SKILL.md"
        if not path.is_file():
            errors.append(f"{sid}: declared but {path} does not exist")
            continue
        content = path.read_text(encoding="utf-8")
        fm, _body = _parse_frontmatter(content)
        if str(fm.get("name") or "") != sid:
            errors.append(f"{sid}: frontmatter name {fm.get('name')!r} must equal the folder name")
            continue
        if not str(fm.get("description") or "").strip():
            errors.append(f"{sid}: frontmatter needs a description")
            continue
        parsed = _parse_content(
            content,
            skill_id=sid,
            source_path=f"{LIBRARY_REPO_PATH}/{ls.root.name}/{sid}/SKILL.md",
        )
        if parsed is None:
            errors.append(f"{sid}: could not be parsed")
            continue
        parsed.skill_type = ls.skill_type
        parsed.declared_skill_type = True
        parsed.category = str(ls.category["slug"])
        parsed.published_to_web = ls.published_to_web
        parsed.ingested_from = PLATFORM_LIBRARY_SOURCE
        parsed.extra_config = {"library_set": ls.set_id, "source_repo": "aidream"}
        if spec["parent"]:
            ref = {"skill_id": spec["parent"]}
            if ls.parent_pack:
                ref["pack_id"] = ls.parent_pack
            parsed.parent_ref = ref
        skills.append(parsed)
    return skills, errors


def library_owns(set_id: str):
    """Ownership predicate: a row belongs to THIS library set and nothing else."""

    def _owns(row: Any) -> bool:
        cfg = _row_config(row)
        return cfg.get("ingested_from") == PLATFORM_LIBRARY_SOURCE and cfg.get("library_set") == set_id

    return _owns


async def ingest_library_set(
    set_dir: Path | str,
    *,
    admin_user_id: UUID | str,
    dry_run: bool = False,
    prune: bool = False,
) -> dict[str, Any]:
    """Ingest (or re-sync) one platform library set. Idempotent; writes only its
    own rows. Refuses to write anything when the walk found an error."""
    import asyncio

    def _read() -> tuple[LibrarySet, list[ParsedSkill], list[str]]:
        ls = load_library_set(set_dir)
        parsed, errs = walk_library_set(ls)
        return ls, parsed, errs

    ls, parsed, errors = await asyncio.to_thread(_read)
    if errors:
        return {
            "set_id": ls.set_id,
            "parsed": len(parsed),
            "created": 0,
            "updated": 0,
            "unchanged": 0,
            "skipped_foreign": 0,
            "deactivated": 0,
            "errors": errors,
            "skills": [],
            "roots": [str(ls.root)],
            "collisions": [],
            "prune_plan": [],
            "category": None,
            "counterparts_linked": 0,
        }
    category = await ensure_skill_category(
        ls.category,
        published_to_web=ls.published_to_web,
        extra_metadata={"library_set": ls.set_id, "source_repo": "aidream"},
        admin_user_id=str(admin_user_id),
        dry_run=dry_run,
    )
    report = await upsert_parsed_skills(
        parsed,
        admin_user_id=admin_user_id,
        dry_run=dry_run,
        is_system=True,
        adopt=False,
        owns=library_owns(ls.set_id),
        prune_candidate=(lambda _row: True) if prune else None,
        roots=[str(ls.root)],
    )
    report["counterparts_linked"] = 0 if dry_run else await link_counterparts(ls.set_id)
    report["set_id"] = ls.set_id
    report["category"] = category
    return report


async def link_counterparts(set_id: str) -> int:
    """Stamp the pairing both ways for every row of this set that has a parent.

    ``parent_skill_id`` already points ours → original; this adds the readable
    half on each side (``derived_from`` / ``our_version``) so every surface shows
    the counterpart without a second query. ``config`` is merged, never
    replaced (the one-write-path contract in ``ingest.py``). Returns the number
    of rows written; 0 when everything already agrees.
    """
    from matrx_ai.db._registry import get_instance

    defs_mgr = get_instance("skl_definitions_manager")
    rows = await defs_mgr.filter_items()
    by_id = {str(r.id): r for r in rows}
    owns = library_owns(set_id)
    written = 0
    for ours in rows:
        if not owns(ours) or not getattr(ours, "is_active", False):
            continue
        parent = by_id.get(str(getattr(ours, "parent_skill_id", None) or ""))
        if parent is None:
            continue
        parent_cfg = _row_config(parent)
        derived_from: dict[str, Any] = {
            "id": str(parent.id),
            "skill_id": str(parent.skill_id),
        }
        for key in ("pack_id", "source_repo", "source_authors"):
            if parent_cfg.get(key):
                derived_from[key] = parent_cfg[key]
        our_version = {"id": str(ours.id), "skill_id": str(ours.skill_id), "library_set": set_id}
        for row, key, value in ((ours, "derived_from", derived_from), (parent, "our_version", our_version)):
            cfg = _row_config(row)
            if cfg.get(key) == value:
                continue
            await defs_mgr.update_item(str(row.id), config={**cfg, key: value})
            written += 1
    return written
