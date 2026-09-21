"""Regression: TasksManager.create_task() must carry organization_id.

``workspace.tasks.organization_id`` is NOT NULL. Before this fix,
``create_task()`` built its insert payload from user_id/title/etc. with no
organization_id parameter at all — the tool caller (``tasks.py``'s
``task_create``) had no way to supply one even if it wanted to. This asserts
the row handed to ``create_item`` carries organization_id, and that a missing
one is refused rather than silently omitted.
"""
from __future__ import annotations

from uuid import uuid4

import pytest

from matrx_ai.db.content_types import tasks as tasks_module


@pytest.mark.asyncio
async def test_create_task_carries_organization_id(monkeypatch):
    org_id = str(uuid4())
    captured: dict = {}

    class _FakeRow:
        def __init__(self, kwargs):
            self._kwargs = kwargs

        def to_dict(self):
            return dict(self._kwargs)

    async def fake_create_item(self, **kwargs):
        captured.update(kwargs)
        return _FakeRow(kwargs)

    monkeypatch.setattr(
        type(tasks_module.tasks_manager_instance), "create_item", fake_create_item, raising=True
    )

    result = await tasks_module.tasks_manager_instance.create_task(
        user_id="user-1",
        organization_id=org_id,
        title="Do the thing",
    )

    assert result.get("success"), result
    assert captured.get("organization_id") == org_id


@pytest.mark.asyncio
async def test_create_task_refuses_without_organization_id(monkeypatch):
    async def fake_create_item(self, **kwargs):
        raise AssertionError("create_item must not be reached without an organization_id")

    monkeypatch.setattr(
        type(tasks_module.tasks_manager_instance), "create_item", fake_create_item, raising=True
    )

    result = await tasks_module.tasks_manager_instance.create_task(
        user_id="user-1",
        organization_id="",
        title="Do the thing",
    )

    assert not result.get("success")
