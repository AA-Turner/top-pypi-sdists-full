"""A run's organization is read from the database once per process, not before every write.

2026-10-27: ``_organization_for_run`` ran a full ``SELECT * FROM workflow.run`` before every checkpoint,
every node outcome and every by-reference event value — two to three reads per super-step, part of the
~70 ms each step of a small workflow cost on top of its real work. A run's organization never changes.
A run that is missing or has no organization is still refused every time (a miss is never remembered).
"""

from __future__ import annotations

import types
from typing import Any
from uuid import uuid4

import pytest

from matrx_graph.checkpoint import postgres as module


class _Row:
    def __init__(self, org: str | None) -> None:
        self.organization_id = org


class _FakeWfRun:
    def __init__(self, org_by_run: dict[str, str | None]) -> None:
        self.org_by_run = org_by_run
        self.reads = 0

    async def get_or_none(self, *, id: str) -> Any:
        self.reads += 1
        if id not in self.org_by_run:
            return None
        return _Row(self.org_by_run[id])


def _size(monkeypatch, n: int) -> None:
    async def _knob() -> int:
        return n

    monkeypatch.setattr("matrx_graph.knobs.run_org_cache_size", _knob)


@pytest.fixture
def fake_run(monkeypatch):
    org = str(uuid4())
    good, orgless, missing = str(uuid4()), str(uuid4()), str(uuid4())
    model = _FakeWfRun({good: org, orgless: None})
    monkeypatch.setattr(module, "get_model", lambda name: model)
    monkeypatch.setattr(module, "_RUN_ORGANIZATION", {})
    _size(monkeypatch, 4096)
    return types.SimpleNamespace(model=model, org=org, good=good, orgless=orgless, missing=missing)


@pytest.mark.asyncio
async def test_a_found_organization_is_read_once(fake_run) -> None:
    for _ in range(5):
        assert await module._organization_for_run(fake_run.good) == fake_run.org
    assert fake_run.model.reads == 1


@pytest.mark.asyncio
async def test_a_run_without_an_organization_is_refused_every_time(fake_run) -> None:
    for run_id in (fake_run.orgless, fake_run.missing):
        for _ in range(2):
            with pytest.raises(ValueError):
                await module._organization_for_run(run_id)
    assert fake_run.model.reads == 4  # never remembered


@pytest.mark.asyncio
async def test_the_memory_is_bounded(fake_run, monkeypatch) -> None:
    _size(monkeypatch, 3)  # the workflow.run_org_cache_size knob
    runs = {str(uuid4()): str(uuid4()) for _ in range(5)}
    fake_run.model.org_by_run.update(runs)
    for run_id in runs:
        await module._organization_for_run(run_id)
    assert len(module._RUN_ORGANIZATION) == 3
    assert list(module._RUN_ORGANIZATION) == list(runs)[-3:]  # oldest evicted first



@pytest.mark.asyncio
async def test_an_unreadable_knob_remembers_nothing(fake_run, monkeypatch) -> None:
    _size(monkeypatch, 0)
    for _ in range(3):
        assert await module._organization_for_run(fake_run.good) == fake_run.org
    assert fake_run.model.reads == 3
    assert module._RUN_ORGANIZATION == {}
