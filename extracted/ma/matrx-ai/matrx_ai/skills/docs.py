"""Plain markdown documents → ``skill.definition`` (reference skills).

Fourth declared source beside the repo mirror, outside packs and library sets. A manifest
(``doc_manifests/<set>.yaml``) maps ``skill_id -> {path, description?, label?}`` for documents
that live in a docs checkout (common-docs) and carry OKF frontmatter (type/title/description),
not SKILL.md frontmatter. The document stays the single source of truth; the row is a mirror.

* Declared, not discovered; every declared path must exist or the run writes nothing.
* Body = the document minus its frontmatter. Label = OKF ``title`` (or manifest ``label``).
  Description = manifest ``description``, else the OKF ``description``.
* ``source_hash`` covers body + label + description, so a changed description also re-syncs.
* Set-owned: ``config.ingested_from = "doc_manifest"`` + ``config.doc_set``; system org, internal
  (``published_to_web`` from the manifest). Same write path (``upsert_parsed_skills``) as every
  other source, so idempotency, provenance stamps and prune semantics are identical.

Run: ``uv run python scripts/ingest_skills.py --docs <manifest> <docs root> [--dry-run] [--prune]``.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import UUID

from matrx_ai.skills.ingest import (
    _VALID_SKILL_TYPES,
    ParsedSkill,
    _parse_frontmatter,
    _row_config,
    declared_published_to_web,
    ensure_skill_category,
    upsert_parsed_skills,
)

DOC_MANIFEST_SOURCE = "doc_manifest"


class DocManifestError(ValueError):
    """The manifest or a declared document cannot be ingested completely."""


@dataclass
class DocSet:
    set_id: str
    title: str
    published_to_web: bool
    skill_type: str
    category: dict[str, Any]
    docs: dict[str, dict[str, Any]] = field(default_factory=dict)


def load_doc_set(manifest_path: Path | str) -> DocSet:
    import yaml  # type: ignore[import-not-found]

    manifest = Path(manifest_path).expanduser().resolve()
    if not manifest.is_file():
        raise DocManifestError(f"{manifest} not found")
    raw = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    try:
        ds = DocSet(
            set_id=str(raw["set_id"]),
            title=str(raw["title"]),
            published_to_web=declared_published_to_web(raw, f"doc manifest {manifest}"),
            skill_type=str(raw.get("skill_type", "reference")),
            category=dict(raw["category"]),
            docs={str(k): dict(v or {}) for k, v in (raw.get("docs") or {}).items()},
        )
    except KeyError as exc:
        raise DocManifestError(f"{manifest} is missing required key {exc}") from exc
    except ValueError as exc:
        raise DocManifestError(str(exc)) from exc
    if ds.skill_type not in _VALID_SKILL_TYPES:
        raise DocManifestError(f"skill_type {ds.skill_type!r} is not a skl_skill_type value")
    if not ds.category.get("slug") or not ds.category.get("name"):
        raise DocManifestError("category needs both slug and name")
    if not ds.docs:
        raise DocManifestError(f"{manifest} declares no docs")
    for sid, spec in ds.docs.items():
        if not spec.get("path"):
            raise DocManifestError(f"{sid}: needs a path")
    return ds


def walk_doc_set(ds: DocSet, docs_root: Path) -> tuple[list[ParsedSkill], list[str]]:
    errors: list[str] = []
    out: list[ParsedSkill] = []
    for sid, spec in sorted(ds.docs.items()):
        rel = str(spec["path"])
        path = docs_root / rel
        if not path.is_file():
            errors.append(f"{sid}: declared but {path} does not exist")
            continue
        fm, body = _parse_frontmatter(path.read_text(encoding="utf-8"))
        body = body.strip()
        description = str(spec.get("description") or fm.get("description") or "").strip()
        label = str(spec.get("label") or fm.get("title") or "").strip()
        if not description or not label or not body:
            errors.append(f"{sid}: needs a label (title), a description and a body")
            continue
        digest = hashlib.sha256("\0".join([body, label, description]).encode("utf-8")).hexdigest()
        out.append(
            ParsedSkill(
                skill_id=sid,
                label=label[:300],
                description=description[:2000],
                skill_type=ds.skill_type,
                declared_skill_type=True,
                body=body,
                category=str(ds.category["slug"]),
                allowed_tools=[],
                trigger_patterns=[],
                disable_auto_invocation=False,
                version=None,
                source_hash=digest,
                source_path=rel,
                published_to_web=ds.published_to_web,
                ingested_from=DOC_MANIFEST_SOURCE,
                extra_config={"doc_set": ds.set_id, "source_repo": docs_root.name},
            )
        )
    return out, errors


def doc_set_owns(set_id: str):
    def _owns(row: Any) -> bool:
        cfg = _row_config(row)
        return cfg.get("ingested_from") == DOC_MANIFEST_SOURCE and cfg.get("doc_set") == set_id

    return _owns


async def ingest_doc_set(
    manifest_path: Path | str,
    docs_root: Path | str,
    *,
    admin_user_id: UUID | str,
    dry_run: bool = False,
    prune: bool = False,
) -> dict[str, Any]:
    import asyncio

    root = Path(docs_root).expanduser().resolve()

    def _read() -> tuple[DocSet, list[ParsedSkill], list[str]]:
        ds = load_doc_set(manifest_path)
        parsed, errs = walk_doc_set(ds, root)
        return ds, parsed, errs

    ds, parsed, errors = await asyncio.to_thread(_read)
    if errors:
        return {
            "set_id": ds.set_id, "parsed": len(parsed), "created": 0, "updated": 0,
            "unchanged": 0, "skipped_foreign": 0, "deactivated": 0, "errors": errors,
            "skills": [], "roots": [str(root)], "collisions": [], "prune_plan": [],
            "category": None,
        }
    category = await ensure_skill_category(
        ds.category,
        published_to_web=ds.published_to_web,
        extra_metadata={"doc_set": ds.set_id, "source_repo": root.name},
        admin_user_id=str(admin_user_id),
        dry_run=dry_run,
    )
    report = await upsert_parsed_skills(
        parsed,
        admin_user_id=admin_user_id,
        dry_run=dry_run,
        is_system=True,
        adopt=False,
        owns=doc_set_owns(ds.set_id),
        prune_candidate=(lambda _row: True) if prune else None,
        roots=[str(root)],
    )
    report["set_id"] = ds.set_id
    report["category"] = category
    return report
