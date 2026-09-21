"""Regression: ingest_filesystem() must carry organization_id on skill.definition writes.

``skill.definition.organization_id`` is NOT NULL. Before this fix,
``ingest_filesystem`` upserted rows with no organization_id at all. Every
current caller ingests with ``is_system=True`` (builtin/admin/dev skills),
so those rows belong to the platform tenant (``SYSTEM_ORGANIZATION_ID``) —
this test asserts the row handed to ``create_item`` carries it, and that an
``is_system=False`` call (which has no legitimate org source yet) is refused
rather than defaulted.
"""
from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

from matrx_ai.skills.ingest import ingest_filesystem

SKILL_MD = """---
name: org-write-regression-skill
description: A flat-layout skill used to prove the org-write guard.
---

# org-write-regression-skill

Body.
"""


class _FakeQuery(list):
    async def all(self):
        return list(self)


class _FakeCategoriesManager:
    async def filter_items(self, **_kw):
        return []


class _FakeCreatedRow:
    def __init__(self, kwargs):
        self.id = uuid4()
        self._kwargs = kwargs


class _FakeDefinitionsManager:
    def __init__(self):
        self.create_calls: list[dict] = []

    async def filter_items(self, **_kw):
        return []

    async def create_item(self, **kwargs):
        self.create_calls.append(kwargs)
        return _FakeCreatedRow(kwargs)

    async def update_item(self, *_a, **_kw):
        raise AssertionError("no existing row in this test")


def _patch_managers(monkeypatch, defs_mgr, cat_mgr):
    import matrx_ai.db._registry as registry

    def fake_get_instance(name):
        if name == "skl_definitions_manager":
            return defs_mgr
        if name == "skl_categories_manager":
            return cat_mgr
        raise AssertionError(f"unexpected get_instance({name!r})")

    monkeypatch.setattr(registry, "get_instance", fake_get_instance)


@pytest.mark.asyncio
async def test_ingest_filesystem_carries_system_organization_id(tmp_path: Path, monkeypatch):
    from matrx_orm.session.fallback import SYSTEM_ORGANIZATION_ID

    root = tmp_path / "skills"
    root.mkdir()
    (root / "org-write-regression-skill.md").write_text(SKILL_MD)

    defs_mgr = _FakeDefinitionsManager()
    _patch_managers(monkeypatch, defs_mgr, _FakeCategoriesManager())

    report = await ingest_filesystem(
        [root], admin_user_id=str(uuid4()), dry_run=False, is_system=True
    )

    assert not report["errors"], report["errors"]
    assert report["created"] == 1
    assert len(defs_mgr.create_calls) == 1
    assert defs_mgr.create_calls[0].get("organization_id") == SYSTEM_ORGANIZATION_ID


@pytest.mark.asyncio
async def test_ingest_filesystem_refuses_is_system_false(tmp_path: Path, monkeypatch):
    root = tmp_path / "skills"
    root.mkdir()
    (root / "org-write-regression-skill.md").write_text(SKILL_MD)

    defs_mgr = _FakeDefinitionsManager()
    _patch_managers(monkeypatch, defs_mgr, _FakeCategoriesManager())

    report = await ingest_filesystem(
        [root], admin_user_id=str(uuid4()), dry_run=False, is_system=False
    )

    assert report["errors"], "expected a refusal error"
    assert not defs_mgr.create_calls
