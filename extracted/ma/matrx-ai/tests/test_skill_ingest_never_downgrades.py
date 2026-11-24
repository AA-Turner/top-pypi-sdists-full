"""A source built from an OLDER commit never replaces (or deactivates) a skill row built from a newer one.

2026-11-03 04:09 UTC: a server booting from an image built before 03:24 re-published its bundled
``spaces-and-pages`` over the row a lane had just published from main, silently dropping a rule. Every
row now records the commit it was built from; the one write path refuses the downgrade, by name.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills import ingest as ingest_mod

PATH = "/app/common-docs/skills/spaces-and-pages/SKILL.md"
NEW = {"sha": "b" * 40, "time": "2026-11-03T03:24:00+00:00"}
OLD = {"sha": "a" * 40, "time": "2026-11-03T02:50:00+00:00"}


def _parsed(source_hash: str = "old-image-hash") -> ingest_mod.ParsedSkill:
    return ingest_mod.ParsedSkill(
        skill_id="spaces-and-pages", label="Spaces and pages", description="Use when building pages.",
        skill_type="reference", declared_skill_type=False, body="# old\n", category=None, allowed_tools=[],
        trigger_patterns=[], disable_auto_invocation=False, version=None, source_hash=source_hash,
        source_path=PATH,
    )


def _row(commit: dict[str, str] | None, *, source_hash: str = "fresh-main-hash"):
    cfg = {"ingested_from": "filesystem", "source_hash": source_hash, "source_path": PATH,
           "source_repo": "aidream", "ingested_at": "2026-11-03T03:24:05+00:00"}
    if commit:
        cfg |= {"source_commit": commit["sha"], "source_commit_time": commit["time"]}
    return SimpleNamespace(
        id=uuid4(), skill_id="spaces-and-pages", is_active=True, is_system=True, skill_type="reference",
        config=cfg, published_to_web=False, organization_id=uuid4(), parent_skill_id=None,
        allowed_tools=[], trigger_patterns=[], disable_auto_invocation=False,
    )


class _Defs:
    def __init__(self, row):
        self.row, self.updates, self.creates = row, [], []

    async def filter_items(self, **_kw):
        return [self.row]

    async def update_item(self, *a, **kw):
        self.updates.append((a, kw))
        return self.row

    async def create_item(self, **kw):
        self.creates.append(kw)
        return SimpleNamespace(id=uuid4())


class _Cats:
    async def filter_items(self, **_kw):
        return []


def _setup(monkeypatch, parsed: list, row):
    import matrx_ai.db._registry as registry

    defs = _Defs(row)
    monkeypatch.setattr(registry, "get_instance", lambda n: defs if n == "skl_definitions_manager" else _Cats())
    monkeypatch.setattr(ingest_mod, "walk_paths", lambda paths: (parsed, [], []))
    return defs


async def _ingest(tmp_path, commit, **kw):
    return await ingest_mod.ingest_filesystem(
        [tmp_path], admin_user_id=str(uuid4()), dry_run=False, source_commit=commit, **kw
    )


@pytest.mark.asyncio
async def test_an_older_image_never_replaces_a_row_built_from_a_newer_commit(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, [_parsed()], _row(NEW))
    report = await _ingest(tmp_path, OLD)
    assert defs.updates == [], "the older copy overwrote the newer row"
    assert report["skipped_older_source"] == 1
    entry = report["skills"][0]
    assert entry["status"] == "skipped_older_source" and NEW["sha"][:12] in entry["reason"]


@pytest.mark.asyncio
async def test_a_source_that_names_no_commit_time_cannot_replace_a_stamped_row(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, [_parsed()], _row(NEW))
    report = await _ingest(tmp_path, {"sha": "c" * 40})
    assert defs.updates == [] and report["skipped_older_source"] == 1


@pytest.mark.asyncio
async def test_a_newer_commit_updates_and_stamps_the_row(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, [_parsed("newest-hash")], _row(OLD))
    report = await _ingest(tmp_path, NEW)
    assert report["updated"] == 1 and report["skipped_older_source"] == 0
    cfg = defs.updates[0][1]["config"]
    assert cfg["source_commit"] == NEW["sha"] and cfg["source_commit_time"] == NEW["time"]


@pytest.mark.asyncio
async def test_an_unstamped_row_is_written_and_stamped(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, [_parsed()], _row(None))
    await _ingest(tmp_path, OLD)
    assert defs.updates and defs.updates[0][1]["config"]["source_commit"] == OLD["sha"]


@pytest.mark.asyncio
async def test_same_bytes_from_an_older_image_are_quietly_unchanged(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, [_parsed("fresh-main-hash")], _row(NEW))
    report = await _ingest(tmp_path, OLD)
    assert defs.updates == [] and report["skipped_older_source"] == 0 and report["unchanged"] == 1


@pytest.mark.asyncio
async def test_an_older_image_never_deactivates_a_skill_a_newer_commit_added(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, [], _row(NEW))
    report = await _ingest(tmp_path, OLD, prune_scopes=["/app/common-docs/skills"])
    assert defs.updates == [] and report["deactivated"] == 0 and report["skipped_older_source"] == 1
