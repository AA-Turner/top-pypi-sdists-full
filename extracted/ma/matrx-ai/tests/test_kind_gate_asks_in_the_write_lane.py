"""The kind tools' permission PROBE asks in the same lane the WRITE uses (2026-10-17).

Regression: on the admin app ("Edit with agent" on a system kind), a super admin's
kindcomp_patch_code was refused "You do not have edit access to kind ..." because
``kind_rls_allows`` ran ``SELECT ... FOR UPDATE`` in the person's session WITHOUT the
admin lane, while the write (``writing_as_the_person``) would have opened it. And the
admin signal itself was read through ``admin_surface_active`` only — which an agent run
from the admin app (ordinary chat route + the verified ``x-matrx-admin-lane`` header)
never carries.

The fake database below answers like the real UPDATE policy on a Matrx System kind:
the row is changeable only while the admin lane is open AND the caller is a platform
admin. Every case drives the REAL gate (``ensure_can_edit_kind`` -> ``kind_rls_allows``
-> ``person_may_change``) and the REAL write lane (``writing_as_the_person``).
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

from matrx_ai.tools.models import ToolContext

_acting: ContextVar[bool] = ContextVar("gate_test_acting", default=False)
_lane_open: ContextVar[bool] = ContextVar("gate_test_lane_open", default=False)
_caller_is_admin: ContextVar[bool] = ContextVar("gate_test_caller_admin", default=False)


def _db_says_admin_arm_answers() -> bool:
    # platform.is_platform_admin(): admin identity AND admin_lane_open()
    return _acting.get() and _lane_open.get() and _caller_is_admin.get()


class _SystemKinds:
    """A Matrx System kind: no owner, no share — only the admin arm reaches it."""

    _database = "test"
    writes: list[bool] = []

    @staticmethod
    async def get_or_none(use_cache: bool = True, **_pk: Any) -> Any:
        assert _acting.get(), "a probe must never run on the privileged connection"
        # public system kind: anyone signed in may view it
        return SimpleNamespace(id=_pk["id"])

    @staticmethod
    def filter(**_pk: Any) -> Any:
        class _Q:
            def select_for_update(self) -> Any:
                return self

            async def values(self, *_f: str) -> list[dict[str, Any]]:
                assert _acting.get(), "a probe must never run on the privileged connection"
                return [dict(_pk)] if _db_says_admin_arm_answers() else []

        return _Q()


@pytest.fixture
def system_kind_db(monkeypatch: pytest.MonkeyPatch):
    import matrx_orm

    from matrx_ai import _ext
    from matrx_ai.tools.implementations import kind_shared

    @contextlib.asynccontextmanager
    async def acting_as_caller(_ctx: Any = None):
        token = _acting.set(True)
        try:
            yield
        finally:
            _acting.reset(token)

    @contextlib.asynccontextmanager
    async def admin_lane(*, database: str):
        assert _acting.get(), "the lane is opened INSIDE the person's session"
        token = _lane_open.set(True)
        try:
            yield
        finally:
            _lane_open.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", acting_as_caller)
    monkeypatch.setattr(matrx_orm, "admin_lane", admin_lane, raising=False)
    monkeypatch.setattr(kind_shared, "get_db_model", lambda _n: _SystemKinds)
    return kind_shared


@contextlib.contextmanager
def _as(*, is_admin: bool, header_lane: bool = False, admin_surface: bool = False):
    user_id = str(uuid4())
    metadata = {"organization_admitted_by": "admin_lane"} if header_lane else {}
    ctx = AppContext(
        emitter=None,
        user_id=user_id,
        is_authenticated=True,
        is_admin=is_admin,
        admin_level="super_admin" if is_admin else None,
        admin_surface=admin_surface,
        metadata=metadata,
    )
    token = set_app_context(ctx)
    admin_token = _caller_is_admin.set(is_admin)
    try:
        yield ToolContext(call_id=str(uuid4()), tool_name="kindcomp_patch_code")
    finally:
        _caller_is_admin.reset(admin_token)
        clear_app_context(token)


def _system_kind() -> Any:
    return SimpleNamespace(
        id=uuid4(), kind="video_transcript_research", created_by=None,
        organization_id="39c38960-d30c-4840-b0c1-c9960de95582",
    )


@pytest.mark.asyncio
async def test_super_admin_on_the_admin_app_passes_the_gate_and_the_write(system_kind_db) -> None:
    """The admin app's agent run: ordinary chat route, verified admin-lane header."""
    kind_shared = system_kind_db
    with _as(is_admin=True, header_lane=True) as tctx:
        assert kind_shared.ctx_is_admin(tctx) is True
        assert await kind_shared.ensure_can_edit_kind(_system_kind(), tctx) is None
        async with kind_shared.writing_as_the_person(tctx):
            assert _db_says_admin_arm_answers(), "the write rides the same lane"


@pytest.mark.asyncio
async def test_super_admin_on_an_admin_mounted_surface_passes_too(system_kind_db) -> None:
    kind_shared = system_kind_db
    with _as(is_admin=True, admin_surface=True) as tctx:
        assert await kind_shared.ensure_can_edit_kind(_system_kind(), tctx) is None


@pytest.mark.asyncio
async def test_same_admin_on_a_user_page_is_an_ordinary_person(system_kind_db) -> None:
    kind_shared = system_kind_db
    with _as(is_admin=True) as tctx:
        assert kind_shared.ctx_is_admin(tctx) is False
        refusal = await kind_shared.ensure_can_edit_kind(_system_kind(), tctx)
        assert refusal is not None and refusal.error.error_type == "forbidden"
        # viewer still answers from RLS: a public system kind is visible to anyone
        assert await kind_shared.ensure_can_view_kind(_system_kind(), tctx) is None


@pytest.mark.asyncio
async def test_a_non_admin_is_refused_even_carrying_the_lane_marker(system_kind_db) -> None:
    kind_shared = system_kind_db
    with _as(is_admin=False, header_lane=True, admin_surface=True) as tctx:
        assert kind_shared.ctx_is_admin(tctx) is False
        refusal = await kind_shared.ensure_can_edit_kind(_system_kind(), tctx)
        assert refusal is not None and refusal.error.error_type == "forbidden"


@pytest.mark.asyncio
async def test_instance_gate_asks_in_the_same_lane(system_kind_db, monkeypatch) -> None:
    from matrx_ai.tools.implementations import kind_instance as ki

    monkeypatch.setattr(ki, "get_db_model", lambda _n: _SystemKinds)
    row = SimpleNamespace(id=uuid4())
    with _as(is_admin=True, header_lane=True) as tctx:
        assert await ki._can_access_instance(row, tctx, "editor") is True
    with _as(is_admin=True) as tctx:
        assert await ki._can_access_instance(row, tctx, "editor") is False
