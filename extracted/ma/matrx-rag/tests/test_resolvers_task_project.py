"""Phase C — task + project resolvers (closing the Phase B no-op).

Verifies matrx_rag.sources._resolve_task / _resolve_project:

* an OWNED row returns a ResolvedSource with text composed from the meaningful
  text columns (title/name + description), the right owner_id, and a hash.
* a NON-owned row (different user) returns None — fail-closed, no leak.
* project ownership keys off ``created_by`` (the table has no user_id column).
* task ownership also keys off ``created_by`` (vestigial user_id dropped).

Fakes ``get_db_model("Tasks"|"Projects")`` to mimic the resolver's ORM
filter/values chain; no live DB.
"""

from __future__ import annotations

import pytest
from matrx_rag import sources

OWNER = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
OTHER = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"
ORG = "cccccccc-cccc-cccc-cccc-cccccccccccc"


class _FakeQuery:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def filter(self, *args, **kwargs):
        return self

    async def values(self, *fields):
        return self._rows


class _FakeTasksModel:
    def __init__(self, tasks: dict) -> None:
        self._tasks = tasks

    def filter(self, *, id=None, created_by=None, deleted_at__isnull=None, **kwargs):
        row = self._tasks.get(id)
        rows = []
        if row is not None and row["owner_id"] == created_by:
            rows.append(
                {
                    "id": row["id"],
                    "created_by": row["owner_id"],
                    "organization_id": row["organization_id"],
                    "project_id": row["project_id"],
                    "title": row["title"],
                    "description": row["description"],
                    "status": row["status"],
                    "priority": row["priority"],
                    "due_date": row["due_date"],
                }
            )
        return _FakeQuery(rows)


class _FakeProjectsModel:
    def __init__(self, projects: dict) -> None:
        self._projects = projects

    def filter(self, *, id=None, created_by=None, **kwargs):
        row = self._projects.get(id)
        rows = []
        if row is not None and row["owner_id"] == created_by:
            rows.append(
                {
                    "id": row["id"],
                    "created_by": row["owner_id"],
                    "organization_id": row["organization_id"],
                    "name": row["name"],
                    "description": row["description"],
                    "slug": row["slug"],
                }
            )
        return _FakeQuery(rows)


@pytest.fixture
def patched_pool(monkeypatch):
    tasks = {
        "task-1": {
            "id": "task-1",
            "owner_id": OWNER,
            "organization_id": ORG,
            "project_id": "proj-1",
            "title": "Ship the KG pipeline",
            "description": "Wire NER into ingest and verify end to end.",
            "status": "in_progress",
            "priority": "high",
            "due_date": None,
        },
        "task-empty": {
            "id": "task-empty",
            "owner_id": OWNER,
            "organization_id": None,
            "project_id": None,
            "title": "",
            "description": "",
            "status": "todo",
            "priority": None,
            "due_date": None,
        },
    }
    projects = {
        "proj-1": {
            "id": "proj-1",
            "owner_id": OWNER,  # created_by mapped to owner_id in SQL
            "organization_id": ORG,
            "name": "Knowledge Graph",
            "description": "Auto-association across the platform.",
            "slug": "kg",
        },
    }
    tasks_model = _FakeTasksModel(tasks)
    projects_model = _FakeProjectsModel(projects)

    def _fake_get_db_model(name: str, schema: str | None = None):
        if name == "Tasks":
            return tasks_model
        if name == "Projects":
            return projects_model
        raise AssertionError(f"unexpected get_db_model({name!r}) call in this test")

    monkeypatch.setattr(sources, "get_db_model", _fake_get_db_model)
    yield


@pytest.mark.asyncio
async def test_resolve_task_owned(patched_pool):
    res = await sources.resolve("task", "task-1", user_id=OWNER)
    assert res is not None
    assert res.source_kind == "task"
    assert res.owner_id == OWNER
    assert res.organization_id == ORG
    assert "Ship the KG pipeline" in res.text
    assert "Wire NER into ingest" in res.text
    assert res.source_hash
    assert res.metadata["status"] == "in_progress"
    assert res.metadata["priority"] == "high"


@pytest.mark.asyncio
async def test_resolve_task_not_owned_returns_none(patched_pool):
    res = await sources.resolve("task", "task-1", user_id=OTHER)
    assert res is None


@pytest.mark.asyncio
async def test_resolve_task_missing_user_id_returns_none(patched_pool):
    # The dispatch fails closed when user_id is absent (fail-closed contract).
    res = await sources.resolve("task", "task-1", user_id=None)
    assert res is None


@pytest.mark.asyncio
async def test_resolve_task_empty_text_returns_none(patched_pool):
    res = await sources.resolve("task", "task-empty", user_id=OWNER)
    assert res is None


@pytest.mark.asyncio
async def test_resolve_project_owned(patched_pool):
    res = await sources.resolve("project", "proj-1", user_id=OWNER)
    assert res is not None
    assert res.source_kind == "project"
    assert res.owner_id == OWNER  # from created_by
    assert res.organization_id == ORG
    assert "Knowledge Graph" in res.text
    assert "Auto-association" in res.text
    assert res.metadata["slug"] == "kg"


@pytest.mark.asyncio
async def test_resolve_project_not_owned_returns_none(patched_pool):
    res = await sources.resolve("project", "proj-1", user_id=OTHER)
    assert res is None
