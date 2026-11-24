"""A skill copy found on someone's own machine (a sandbox walk) never overwrites the row the repo published.

2026-11-03: the deployed boot published the fresh ``handoff``; minutes later a sandbox's
``~/.agents/skills/handoff`` (an older copy) replaced the platform's row, because the sandbox auto-discovery
ingests as a system write and the loader updated whatever row matched the name.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills import ingest as ingest_mod

BODY = "# handoff\n\nOld local copy.\n"


def _parsed(source_path: str) -> ingest_mod.ParsedSkill:
    return ingest_mod.ParsedSkill(
        skill_id="handoff", label="Handoff", description="Use when handing off.", skill_type="reference",
        declared_skill_type=False, body=BODY, category=None, allowed_tools=[], trigger_patterns=[],
        disable_auto_invocation=False, version=None, source_hash="old-local-hash", source_path=source_path,
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


def _setup(monkeypatch, parsed, row):
    import matrx_ai.db._registry as registry

    defs = _Defs(row)
    monkeypatch.setattr(registry, "get_instance", lambda n: defs if n == "skl_definitions_manager" else _Cats())
    monkeypatch.setattr(ingest_mod, "walk_paths", lambda paths: ([parsed], [], []))
    return defs


def _repo_row():
    return SimpleNamespace(
        id=uuid4(), skill_id="handoff", is_active=True, is_system=True, skill_type="reference",
        config={"ingested_from": "filesystem", "source_hash": "fresh-repo-hash",
                "source_path": "/app/common-docs/skills/handoff/SKILL.md"},
        published_to_web=False, organization_id=uuid4(), parent_skill_id=None,
    )


@pytest.mark.asyncio
async def test_a_sandbox_copy_never_replaces_the_repo_row(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, _parsed("sandbox://inst_x/Users/someone/.agents/skills/handoff/SKILL.md"), _repo_row())
    report = await ingest_mod.ingest_filesystem([tmp_path], admin_user_id=str(uuid4()), dry_run=False)
    assert defs.updates == [] and defs.creates == []
    assert report.get("skipped_repo_owned") == 1
    assert report["skills"][0]["status"] == "skipped_repo_owned"


@pytest.mark.asyncio
async def test_the_repo_still_updates_its_own_row(tmp_path, monkeypatch):
    defs = _setup(monkeypatch, _parsed("/app/common-docs/skills/handoff/SKILL.md"), _repo_row())
    report = await ingest_mod.ingest_filesystem([tmp_path], admin_user_id=str(uuid4()), dry_run=False)
    assert not report.get("skipped_repo_owned")
    assert defs.updates, report
