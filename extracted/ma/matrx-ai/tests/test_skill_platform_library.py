"""Platform library skills: declared, complete, parent-linked, set-owned, idempotent.

Witnesses for ``matrx_ai.skills.library`` and the ``parent_ref`` leg of the one
write path (``upsert_parsed_skills``). Arman, 2026-09-27: every imported outside
skill also gets our own version in the library, linked to the original.
"""

from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills.ingest import ParsedSkill, _hash, discover_skill_roots, upsert_parsed_skills
from matrx_ai.skills.library import (
    LIBRARY_DIR,
    LibraryError,
    ingest_library_set,
    load_library_set,
    walk_library_set,
)


class _Row(SimpleNamespace):
    pass


class _Defs:
    def __init__(self, rows=None):
        self.rows: list[_Row] = list(rows or [])
        self.creates = 0
        self.updates = 0

    async def filter_items(self, **_kw):
        return list(self.rows)

    async def create_item(self, **kw):
        self.creates += 1
        row = _Row(id=uuid4(), **kw)
        self.rows.append(row)
        return row

    async def update_item(self, row_id, **kw):
        self.updates += 1
        for r in self.rows:
            if str(r.id) == str(row_id):
                for k, v in kw.items():
                    setattr(r, k, v)
                return r
        raise AssertionError("update of unknown row")


class _Cats:
    def __init__(self):
        self.rows: list[_Row] = []

    async def filter_items(self, **_kw):
        return list(self.rows)

    async def create_item(self, **kw):
        row = _Row(id=uuid4(), **kw)
        self.rows.append(row)
        return row

    async def update_item(self, row_id, **kw):
        for r in self.rows:
            if str(r.id) == str(row_id):
                for k, v in kw.items():
                    setattr(r, k, v)
                return r
        raise AssertionError("update of unknown category")


def _patch(monkeypatch, defs, cats):
    import matrx_ai.db._registry as registry

    monkeypatch.setattr(
        registry,
        "get_instance",
        lambda name: {"skl_definitions_manager": defs, "skl_categories_manager": cats}[name],
    )


def _imported(skill_id: str, pack_id: str = "outside-pack") -> _Row:
    return _Row(
        id=uuid4(),
        skill_id=skill_id,
        body="their text",
        is_active=True,
        visibility="public",
        config={"ingested_from": "outside_pack", "pack_id": pack_id},
    )


def _parsed(skill_id: str, parent_ref: dict | None) -> ParsedSkill:
    body = f"# {skill_id}\n\nOur method."
    return ParsedSkill(
        skill_id=skill_id,
        label=skill_id,
        description="d",
        skill_type="reference",
        declared_skill_type=True,
        body=body,
        category=None,
        allowed_tools=[],
        trigger_patterns=[],
        disable_auto_invocation=False,
        version=None,
        source_hash=_hash(body),
        source_path=f"lib/{skill_id}/SKILL.md",
        visibility="public",
        ingested_from="platform_library",
        extra_config={"library_set": "t", "source_repo": "aidream"},
        parent_ref=parent_ref,
    )


def _owns(row):
    return (getattr(row, "config", None) or {}).get("ingested_from") == "platform_library"


# ---------------------------------------------------------------------------
# The generic leg: upsert_parsed_skills writes parent_skill_id from parent_ref
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_parent_ref_writes_parent_skill_id_and_reruns_unchanged(monkeypatch):
    parent = _imported("seo-audit")
    defs, cats = _Defs([parent]), _Cats()
    _patch(monkeypatch, defs, cats)
    parsed = [_parsed("matrx-seo-audit", {"skill_id": "seo-audit", "pack_id": "outside-pack"})]

    first = await upsert_parsed_skills(
        parsed, admin_user_id=str(uuid4()), dry_run=False, is_system=True, adopt=False, owns=_owns
    )
    assert first["errors"] == [] and first["created"] == 1
    ours = next(r for r in defs.rows if r.skill_id == "matrx-seo-audit")
    assert str(ours.parent_skill_id) == str(parent.id)

    second = await upsert_parsed_skills(
        parsed, admin_user_id=str(uuid4()), dry_run=False, is_system=True, adopt=False, owns=_owns
    )
    assert (second["created"], second["updated"], second["unchanged"]) == (0, 0, 1)


@pytest.mark.asyncio
async def test_a_wrong_parent_link_is_repaired_on_the_next_run(monkeypatch):
    parent = _imported("seo-audit")
    ours = _Row(
        id=uuid4(),
        skill_id="matrx-seo-audit",
        is_active=True,
        visibility="public",
        parent_skill_id=None,
        config={
            "ingested_from": "platform_library",
            "source_hash": _hash("# matrx-seo-audit\n\nOur method."),
            "source_path": "lib/matrx-seo-audit/SKILL.md",
            "source_repo": "aidream",
            "ingested_at": "2026-09-27T00:00:00Z",
            "library_set": "t",
        },
    )
    defs, cats = _Defs([parent, ours]), _Cats()
    _patch(monkeypatch, defs, cats)
    report = await upsert_parsed_skills(
        [_parsed("matrx-seo-audit", {"skill_id": "seo-audit"})],
        admin_user_id=str(uuid4()),
        dry_run=False,
        is_system=True,
        adopt=False,
        owns=_owns,
    )
    assert report["updated"] == 1
    assert str(ours.parent_skill_id) == str(parent.id)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("rows", "ref"),
    [
        ([], {"skill_id": "seo-audit"}),  # parent not imported
        ([_imported("seo-audit", "a"), _imported("seo-audit", "b")], {"skill_id": "seo-audit"}),
        ([_imported("seo-audit", "a")], {"skill_id": "seo-audit", "pack_id": "b"}),
    ],
    ids=["missing", "ambiguous", "wrong-pack"],
)
async def test_a_parent_that_is_not_exactly_one_row_refuses_the_skill(monkeypatch, rows, ref):
    defs, cats = _Defs(rows), _Cats()
    _patch(monkeypatch, defs, cats)
    report = await upsert_parsed_skills(
        [_parsed("matrx-seo-audit", ref)],
        admin_user_id=str(uuid4()),
        dry_run=False,
        is_system=True,
        adopt=False,
        owns=_owns,
    )
    assert report["created"] == 0 and defs.creates == 0
    assert len(report["errors"]) == 1 and "expected exactly one" in report["errors"][0]


@pytest.mark.asyncio
async def test_no_parent_ref_never_clears_a_hand_set_link(monkeypatch):
    hand = uuid4()
    row = _Row(
        id=uuid4(),
        skill_id="x",
        is_active=True,
        visibility="public",
        parent_skill_id=hand,
        config={"ingested_from": "platform_library"},
    )
    defs, cats = _Defs([row]), _Cats()
    _patch(monkeypatch, defs, cats)
    await upsert_parsed_skills(
        [_parsed("x", None)], admin_user_id=str(uuid4()), dry_run=False, is_system=True,
        adopt=False, owns=_owns,
    )
    assert row.parent_skill_id == hand


# ---------------------------------------------------------------------------
# The library source
# ---------------------------------------------------------------------------


def _set(tmp_path: Path, *, extra_folder: str | None = None, bad_name: bool = False) -> Path:
    root = tmp_path / "demo"
    (root / "matrx-alpha").mkdir(parents=True)
    (root / "library.yaml").write_text(
        "set_id: demo-set\ntitle: Demo\nvisibility: public\nskill_type: workflow\n"
        "category: {slug: demo, name: Demo}\nparent_pack: outside-pack\n"
        "skills:\n  matrx-alpha: {parent: alpha}\n"
    )
    name = "wrong" if bad_name else "matrx-alpha"
    (root / "matrx-alpha" / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Our alpha.\n---\n\n# Alpha\n\nSteps.\n"
    )
    if extra_folder:
        (root / extra_folder).mkdir()
    return root


@pytest.mark.asyncio
async def test_library_set_is_public_categorised_parented_and_idempotent(tmp_path, monkeypatch):
    parent = _imported("alpha")
    defs, cats = _Defs([parent, _imported("alpha", "someone-else")]), _Cats()
    _patch(monkeypatch, defs, cats)
    root = _set(tmp_path)

    first = await ingest_library_set(root, admin_user_id=str(uuid4()))
    assert first["errors"] == [] and first["created"] == 1
    assert first["category"]["status"] == "created"
    row = next(r for r in defs.rows if r.skill_id == "matrx-alpha")
    assert row.visibility == "public" and row.is_system is True and row.skill_type == "workflow"
    assert str(row.parent_skill_id) == str(parent.id)  # narrowed by parent_pack
    assert str(row.category_id) == str(cats.rows[0].id)
    assert row.config["ingested_from"] == "platform_library"
    assert row.config["library_set"] == "demo-set"

    second = await ingest_library_set(root, admin_user_id=str(uuid4()))
    assert (second["created"], second["updated"], second["unchanged"]) == (0, 0, 1)


@pytest.mark.asyncio
async def test_library_never_writes_an_imported_row_of_the_same_name(tmp_path, monkeypatch):
    clash = _imported("matrx-alpha")
    defs, cats = _Defs([_imported("alpha", "outside-pack"), clash]), _Cats()
    _patch(monkeypatch, defs, cats)
    report = await ingest_library_set(_set(tmp_path), admin_user_id=str(uuid4()))
    assert report["skipped_foreign"] == 1 and clash.body == "their text"


def test_undeclared_folder_and_name_mismatch_are_errors(tmp_path):
    ls = load_library_set(_set(tmp_path, extra_folder="stray"))
    _skills, errors = walk_library_set(ls)
    assert any("stray" in e for e in errors)

    ls2 = load_library_set(_set(tmp_path / "b", bad_name=True))
    _skills, errors = walk_library_set(ls2)
    assert any("frontmatter name" in e for e in errors)


def test_self_parent_is_refused(tmp_path):
    root = _set(tmp_path)
    (root / "library.yaml").write_text(
        "set_id: s\ntitle: t\ncategory: {slug: c, name: C}\nskills:\n  matrx-alpha: {parent: matrx-alpha}\n"
    )
    with pytest.raises(LibraryError):
        load_library_set(root)


def test_repo_mirror_discovery_never_reaches_the_library():
    package_root = LIBRARY_DIR.parent.parent  # matrx_ai/
    for found in discover_skill_roots(package_root, max_depth=6):
        assert LIBRARY_DIR not in Path(found).resolve().parents


# ---------------------------------------------------------------------------
# The shipped SEO set: our own version of every imported SEO skill
# ---------------------------------------------------------------------------

SEO_PARENTS = {
    "seo-audit",
    "keyword-research",
    "keyword-clustering",
    "competitor-analysis",
    "competitive-landscape",
    "link-prospecting",
    "local-seo",
    "seo-coach",
    "seo-project-setup",
    "seo-report",
}

# Our users work inside AI Matrx: a native skill never sends them to another
# product, a plugin, a slash command, a coding tool, or "credits".
_FORBIDDEN = re.compile(
    r"openseo|\bMCP\b|plugin|Claude Code|Cursor|Codex|\bcredits?\b|slash command|`/[a-z]",
    re.IGNORECASE,
)


def test_shipped_seo_set_covers_every_imported_skill_and_speaks_ai_matrx():
    ls = load_library_set(LIBRARY_DIR / "seo")
    assert ls.parent_pack == "every-app-seo-skills" and ls.visibility == "public"
    skills, errors = walk_library_set(ls)
    assert errors == []
    assert {s.parent_ref["skill_id"] for s in skills} == SEO_PARENTS
    for s in skills:
        assert s.skill_id not in SEO_PARENTS
        assert s.parent_ref["pack_id"] == "every-app-seo-skills"
        hit = _FORBIDDEN.search(s.body) or _FORBIDDEN.search(s.description)
        assert hit is None, f"{s.skill_id}: {hit.group(0)!r} does not belong in an AI Matrx skill"


@pytest.mark.asyncio
async def test_category_visibility_column_follows_the_declared_visibility(tmp_path, monkeypatch):
    from matrx_ai.skills.ingest import ensure_skill_category

    defs, cats = _Defs(), _Cats()
    _patch(monkeypatch, defs, cats)
    cat = {"slug": "demo", "name": "Demo"}
    admin = str(uuid4())

    created = await ensure_skill_category(
        cat, visibility="public", extra_metadata={}, admin_user_id=admin, dry_run=False
    )
    assert created["status"] == "created" and cats.rows[0].visibility == "public"

    # A category left at the column default (internal) is reconciled, once.
    cats.rows[0].visibility = "internal"
    fixed = await ensure_skill_category(
        cat, visibility="public", extra_metadata={}, admin_user_id=admin, dry_run=False
    )
    assert fixed["status"] == "visibility_fixed" and cats.rows[0].visibility == "public"
    again = await ensure_skill_category(
        cat, visibility="public", extra_metadata={}, admin_user_id=admin, dry_run=False
    )
    assert again["status"] == "exists"
