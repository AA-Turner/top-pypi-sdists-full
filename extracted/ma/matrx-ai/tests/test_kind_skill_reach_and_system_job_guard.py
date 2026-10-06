"""Generated skills mirror their shape's reach; system_job writes are scheduler-only."""

from __future__ import annotations

import asyncio
import contextlib
from types import SimpleNamespace

import pytest

from matrx_ai.tools.implementations.kind_shared import WriteRefused, writing_as_the_person
from matrx_ai.tools.implementations.kind_skill_generation import reach_changes, reach_of

SYS = "39c38960-d30c-4840-b0c1-c9960de95582"


def kd(org, shown=None, web=True):
    return SimpleNamespace(organization_id=org, shown_to=shown, published_to_web=web)


def test_system_org_shape_gives_a_system_published_skill():
    assert reach_of(kd(SYS), SYS) == {
        "shown_to": None, "published_to_web": True, "is_system": True,
    }


def test_other_org_shape_is_not_system_and_mirrors_shown_to():
    r = reach_of(kd("org-2", "everyone", False), SYS)
    assert r["is_system"] is False and r["shown_to"] == "everyone" and set(r) == {"shown_to", "published_to_web", "is_system"}


def test_reach_changes_lists_only_the_drift():
    skill = SimpleNamespace(shown_to=None, published_to_web=False, is_system=False)
    assert set(reach_changes(skill, kd(SYS), SYS)) == {"published_to_web", "is_system"}
    synced = SimpleNamespace(shown_to=None, published_to_web=True, is_system=True)
    assert reach_changes(synced, kd(SYS), SYS) == {}


def test_system_job_is_refused_outside_the_scheduler(monkeypatch):
    opened = []

    @contextlib.asynccontextmanager
    async def session(*a, **k):
        opened.append(1)
        yield

    from matrx_ai import _ext

    monkeypatch.setitem(_ext._registry, "acting_as_caller", session)

    async def go():
        async with writing_as_the_person(None, system_job=True):
            pass

    with pytest.raises(WriteRefused):
        asyncio.run(go())
    assert opened == []  # the admin lane never even got a session


def test_system_job_is_allowed_inside_a_scheduled_run(monkeypatch):
    import matrx_connect.context.app_context as ac

    monkeypatch.setattr(
        ac, "try_get_app_context",
        lambda: SimpleNamespace(origin_class="scheduled", source_app="matrx-scheduler"),
    )
    from matrx_ai.tools.implementations.kind_shared import scheduler_identity_active

    assert scheduler_identity_active() is True
    monkeypatch.setattr(ac, "try_get_app_context", lambda: SimpleNamespace(origin_class="chat", source_app="web"))
    assert scheduler_identity_active() is False
