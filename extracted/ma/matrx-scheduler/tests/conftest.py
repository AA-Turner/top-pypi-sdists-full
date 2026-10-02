"""
Shared pytest fixtures: a fake matrx-orm-shaped backend + a FastAPI test
harness with matrx_connect AppContext injection.

Both ``api.user_queries`` (the HTTP routes, RLS-scoped) and ``queries.py``
(the scanner, unscoped/privileged) speak matrx-orm exclusively now -- no
PostgREST ``.table()``/``.rpc()`` calls anywhere in this package (see
``packages/matrx-scheduler/CLAUDE.md``). These fixtures fake the SAME
injection seam the host wires in production:

* ``matrx_scheduler.configure_db(models=...)`` -- fake Model classes
  (``SchTask``/``SchAgentTask``/``SchTrigger``/``SchRun``) implementing
  exactly the surface this package's queries use (``filter``/``values``/
  ``count``/``create``/``update_where``/``delete_where``/``upsert``).
* ``matrx_scheduler.configure(rls_session=..., call_function=..., database=...)``
  -- a no-op RLS-session context manager and a fake ``sch_enqueue_manual_run``
  RPC, matching ``matrx_orm.rls_session`` / ``matrx_orm.call_function``'s
  real signatures.

This mirrors the fake-ORM-model pattern used elsewhere in the raw-SQL-
elimination campaign (e.g. ``packages/matrx-rag/tests/test_ner.py``,
``aidream/api/tests/test_rag_admin_data_store_access.py``).

The fake does NOT simulate Postgres RLS (same as the pre-conversion fake
it replaces) -- these tests verify route plumbing, AppContext-layer
authorization gating (``ctx.is_authenticated``/``ctx.is_admin``), and
Pydantic wire shapes. RLS enforcement itself is the live database's job,
covered by matrx-orm's own ``rls_session`` tests.
"""

from __future__ import annotations

import uuid
from copy import deepcopy
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any
from collections.abc import AsyncIterator

import pytest


async def _retry_read_once(factory, *, attempts: int = 2, **_kwargs):
    """Test host equivalent of matrx-orm's read-only transient retry."""
    from matrx_orm import QueryTimeoutError

    for attempt in range(attempts):
        try:
            return await factory()
        except QueryTimeoutError:
            if attempt + 1 == attempts:
                raise
    raise AssertionError("unreachable")

# ── Fake matrx-orm Model layer ──────────────────────────────────────────────


def _match(row: dict[str, Any], filters: dict[str, Any]) -> bool:
    """Minimal lookup-operator support -- exactly what this package's own
    matrx-orm call sites use (``eq``, ``__isnull``, ``__in``, and the
    ``__lt``/``__lte``/``__gt``/``__gte`` comparisons the lease-expiry sweep
    and the due-task scan use). Anything beyond that is a sign a query grew a
    new shape and this fake needs a matching update, so it raises loudly
    rather than silently no-op'ing."""
    for key, value in filters.items():
        if "__" in key:
            field, op = key.rsplit("__", 1)
        else:
            field, op = key, "eq"
        rv = row.get(field)
        if op == "eq":
            if rv != value:
                return False
        elif op == "isnull":
            if (rv is None) != bool(value):
                return False
        elif op == "in":
            if rv not in (value or []):
                return False
        elif op == "overlap":
            # Postgres ``&&`` — the due-task scan's surface filter.
            if not set(rv or []) & set(value or []):
                return False
        elif op in ("lt", "lte", "gt", "gte"):
            if rv is None:
                return False
            if op == "lt" and not rv < value:
                return False
            if op == "lte" and not rv <= value:
                return False
            if op == "gt" and not rv > value:
                return False
            if op == "gte" and not rv >= value:
                return False
        else:
            raise NotImplementedError(f"fake ORM filter operator not implemented: {op!r}")
    return True


class _FakeQuery:
    """Fakes the chain ``Model.filter(...).order_by(...).limit(...).offset(...).values()/.count()``."""

    def __init__(
        self,
        table_rows: list[dict[str, Any]],
        filters: dict[str, Any],
        lock_events: list[str] | None = None,
        table_name: str | None = None,
    ) -> None:
        self._table_rows = table_rows
        self._filters = dict(filters)
        self._lock_events = lock_events
        self._table_name = table_name
        self._order: str | None = None
        self._limit: int | None = None
        self._offset = 0

    def filter(self, **kw: Any) -> _FakeQuery:
        self._filters.update(kw)
        return self

    def order_by(self, col: str) -> _FakeQuery:
        self._order = col
        return self

    def limit(self, n: int) -> _FakeQuery:
        self._limit = n
        return self

    def offset(self, n: int) -> _FakeQuery:
        self._offset = n
        return self

    def select_for_update(self, **_kwargs: Any) -> _FakeQuery:
        """The fake is single-threaded; transaction snapshots prove rollback."""
        if self._lock_events is not None and self._table_name is not None:
            self._lock_events.append(self._table_name)
        return self

    def _matched(self) -> list[dict[str, Any]]:
        rows = [r for r in self._table_rows if _match(r, self._filters)]
        if self._order:
            desc = self._order.startswith("-")
            key = self._order[1:] if desc else self._order
            rows.sort(key=lambda r: (r.get(key) is None, r.get(key)), reverse=desc)
        if self._offset:
            rows = rows[self._offset :]
        if self._limit is not None:
            rows = rows[: self._limit]
        return rows

    async def values(self, *fields: str) -> list[dict[str, Any]]:
        matched = self._matched()
        if fields:
            return [{f: r.get(f) for f in fields} for r in matched]
        return [dict(r) for r in matched]

    async def count(self) -> int:
        return len([r for r in self._table_rows if _match(r, self._filters)])


class _FakeInstance:
    def __init__(self, row: dict[str, Any]) -> None:
        self._row = row

    def to_dict(self) -> dict[str, Any]:
        return dict(self._row)


#: Tables whose live ``organization_id`` is NOT NULL with no default and no
#: stamping trigger. The fake refuses a row without it exactly as Postgres does
#: (23502) — a fake that accepts it hid the create-schedule outage.
ORG_NOT_NULL_TABLES = frozenset({"sch_task", "sch_trigger", "sch_run"})

#: The organization every authenticated test request carries.
TEST_ORGANIZATION_ID = "0f0f0f0f-0000-4000-8000-00000000000a"


def _make_fake_model(table: str, backend: FakeSchedulerBackend) -> type:
    """Build a fake matrx-orm Model class bound to ``backend.rows[table]``."""

    class _FakeModel:
        _table = table
        _backend = backend

        @classmethod
        def filter(cls, **kw: Any) -> _FakeQuery:
            return _FakeQuery(
                cls._backend.rows[cls._table], kw, cls._backend.lock_events, cls._table
            )

        @classmethod
        async def create(cls, **data: Any) -> _FakeInstance:
            if cls._table in ORG_NOT_NULL_TABLES and not data.get("organization_id"):
                raise RuntimeError(
                    f'null value in column "organization_id" of relation "{cls._table}" '
                    "violates not-null constraint"
                )
            row = dict(data)
            if cls._table == "sch_run" and cls._backend.fail_next_run_create:
                cls._backend.fail_next_run_create = False
                raise RuntimeError("simulated successor insert failure")
            if cls._table == "sch_run" and row.get("status") in {"queued", "claimed", "running"}:
                if any(
                    existing.get("task_id") == row.get("task_id")
                    and existing.get("status") in {"queued", "claimed", "running"}
                    for existing in cls._backend.rows[cls._table]
                ):
                    raise RuntimeError("23505 duplicate key sch_run_unique_active_per_task")
            now = datetime.now(UTC)
            row.setdefault("created_at", now)
            row.setdefault("updated_at", now)
            cls._backend.rows[cls._table].append(row)
            return _FakeInstance(row)

        @classmethod
        async def update_where(cls, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
            matched = [r for r in cls._backend.rows[cls._table] if _match(r, filters)]
            for r in matched:
                r.update(updates)
                r["updated_at"] = datetime.now(UTC)
            return SimpleNamespace(
                rows_affected=len(matched), updated_rows=[dict(r) for r in matched]
            )

        @classmethod
        async def delete_where(cls, **filters: Any) -> int:
            rows = cls._backend.rows[cls._table]
            matched = [r for r in rows if _match(r, filters)]
            cls._backend.rows[cls._table] = [r for r in rows if r not in matched]
            return len(matched)

        @classmethod
        async def upsert(
            cls, payload: dict[str, Any], conflict_fields: list[str]
        ) -> _FakeInstance:
            rows = cls._backend.rows[cls._table]
            key = {f: payload.get(f) for f in conflict_fields}
            existing = next(
                (r for r in rows if all(r.get(f) == v for f, v in key.items())), None
            )
            now = datetime.now(UTC)
            if existing is not None:
                existing.update(payload)
                existing["updated_at"] = now
                return _FakeInstance(existing)
            row = dict(payload)
            row.setdefault("created_at", now)
            row.setdefault("updated_at", now)
            rows.append(row)
            return _FakeInstance(row)

    _FakeModel.__name__ = f"Fake{table}"
    return _FakeModel


@asynccontextmanager
async def _fake_rls_session(
    claims: dict[str, Any], *, role: str, database: str | None = None
) -> AsyncIterator[None]:
    """No-op stand-in for ``matrx_orm.rls_session`` -- RLS itself is the
    live database's job (see module docstring); this only has to satisfy
    the async-context-manager shape ``api.user_queries`` calls it with."""
    yield


class FakeSchedulerBackend:
    """
    Stands in for BOTH:

    (1) the per-request Supabase client ``user_client_dep`` returns --
        now used ONLY to carry the caller's bearer JWT (see
        ``api.per_request.user_client_dep``'s docstring; the JWT is read
        back out via ``sb.options.headers["Authorization"]`` by
        ``api.user_queries._claims_from_client``);
    (2) the in-memory store backing the fake matrx-orm Model classes
        injected via ``configure_db``, plus the fake ``call_function`` RPC.

    ``.rows`` / ``.rpc_calls`` are kept as public attributes with the same
    shape/names the pre-conversion ``FakeSupabase`` used, so existing test
    assertions that inspect DB state directly didn't need to change.
    """

    def __init__(self, user_id: str) -> None:
        self.rows: dict[str, list[dict[str, Any]]] = {
            "sch_task": [],
            "sch_agent_task": [],
            "sch_trigger": [],
            "sch_run": [],
        }
        self.rpc_calls: list[tuple[str, dict[str, Any]]] = []
        self.fail_next_run_create = False
        self.lock_events: list[str] = []
        jwt_lib = pytest.importorskip("jwt")
        token = jwt_lib.encode(
            {"sub": user_id, "role": "authenticated"},
            "test-secret-at-least-32-bytes-long!!",
            algorithm="HS256",
        )
        self.options = SimpleNamespace(headers={"Authorization": f"Bearer {token}"})

    def db_models(self) -> dict[str, Any]:
        return {
            "SchTask": _make_fake_model("sch_task", self),
            "SchAgentTask": _make_fake_model("sch_agent_task", self),
            "SchTrigger": _make_fake_model("sch_trigger", self),
            "SchRun": _make_fake_model("sch_run", self),
        }

    @asynccontextmanager
    async def transaction(self) -> AsyncIterator[None]:
        """Rollback-capable host transaction seam used by atomic package tests."""
        snapshot = deepcopy(self.rows)
        try:
            yield
        except BaseException:
            self.rows = snapshot
            raise

    async def call_function(
        self,
        database: str,
        schema: str,
        function: str,
        *args: Any,
        mode: str = "scalar",
        field: str | None = None,
    ) -> Any:
        """Fakes the one RPC this package calls:
        ``sch_enqueue_manual_run`` (``api.user_queries.enqueue_manual_run``).
        Matches ``matrx_orm.call_function``'s real positional signature."""
        if function == "sch_enqueue_manual_run":
            task_id = args[0]
            self.rpc_calls.append((function, {"p_task_id": task_id}))
            owner = next((t for t in self.rows["sch_task"] if t.get("id") == task_id), None)
            if owner is None:
                raise RuntimeError("task not found")
            new_run_id = str(uuid.uuid4())
            now = datetime.now(UTC)
            self.rows["sch_run"].append(
                {
                    "id": new_run_id,
                    "task_id": task_id,
                    "trigger_id": None,
                    "user_id": owner.get("user_id"),
                    "status": "queued",
                    "surface": None,
                    "queue": owner.get("queue"),
                    "output_ref": None,
                    "due_at": now,
                    "claimed_at": None,
                    "started_at": None,
                    "finished_at": None,
                    "claim_token": None,
                    "claim_expires_at": None,
                    "result_summary": None,
                    "error_message": None,
                    "result_metadata": None,
                    "created_at": now,
                }
            )
            return new_run_id
        raise RuntimeError(f"fake RPC '{function}' not implemented")


# ── Fixtures ────────────────────────────────────────────────────────────


@pytest.fixture
def authed_user_id() -> str:
    return "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def other_user_id() -> str:
    return "22222222-2222-2222-2222-222222222222"


@pytest.fixture
def fake_supabase(authed_user_id) -> FakeSchedulerBackend:
    return FakeSchedulerBackend(authed_user_id)


def _build_app(
    fake_supabase: FakeSchedulerBackend,
    *,
    user_id: str,
    email: str | None,
    is_authenticated: bool,
    is_admin: bool,
    organization_id: str | None = TEST_ORGANIZATION_ID,
):
    fastapi = pytest.importorskip("fastapi")
    pytest.importorskip("matrx_connect")
    import matrx_scheduler
    from matrx_connect.context.app_context import AppContext, set_app_context
    from matrx_connect.emitters import ConsoleEmitter
    from matrx_scheduler.api import include_routers
    from matrx_scheduler.api.per_request import user_client_dep

    app = fastapi.FastAPI()

    @app.middleware("http")
    async def _inject_context(request, call_next):
        ctx = AppContext(
            emitter=ConsoleEmitter(),
            user_id=user_id,
            email=email,
            auth_type="token" if is_authenticated else "anonymous",
            is_authenticated=is_authenticated,
            is_admin=is_admin,
            request_id="test-req",
            organization_id=organization_id if is_authenticated else None,
        )
        token = set_app_context(ctx)
        try:
            request.state.context = ctx
            return await call_next(request)
        finally:
            from matrx_connect.context.app_context import clear_app_context

            clear_app_context(token)

    # Override the per-request client dep so every request uses the fake
    # (which carries the bearer JWT api.user_queries decodes).
    app.dependency_overrides[user_client_dep] = lambda: fake_supabase

    matrx_scheduler.configure_db(models=fake_supabase.db_models())
    matrx_scheduler.configure(
        supabase_client=fake_supabase,
        surface="test",
        database="test",
        rls_session=_fake_rls_session,
        call_function=fake_supabase.call_function,
        retry_on_transient=_retry_read_once,
    )

    include_routers(app, prefix="/scheduler")
    return app


@pytest.fixture
def fastapi_app(fake_supabase, authed_user_id):
    """FastAPI app with matrx_connect AppContext injected as the authed user."""
    return _build_app(
        fake_supabase,
        user_id=authed_user_id,
        email="test@example.com",
        is_authenticated=True,
        is_admin=False,
    )


@pytest.fixture
def admin_app(fake_supabase, authed_user_id):
    """Variant of fastapi_app that marks the caller as admin."""
    return _build_app(
        fake_supabase,
        user_id=authed_user_id,
        email="admin@example.com",
        is_authenticated=True,
        is_admin=True,
    )


@pytest.fixture
def no_org_app(fake_supabase, authed_user_id):
    """An authenticated caller whose request names no organization."""
    return _build_app(
        fake_supabase,
        user_id=authed_user_id,
        email="test@example.com",
        is_authenticated=True,
        is_admin=False,
        organization_id=None,
    )


@pytest.fixture
def anon_app(fake_supabase):
    """Variant with an unauthenticated AppContext."""
    return _build_app(
        fake_supabase,
        user_id="",
        email=None,
        is_authenticated=False,
        is_admin=False,
    )


@pytest.fixture
def client(fastapi_app):
    httpx = pytest.importorskip("httpx")
    transport = httpx.ASGITransport(app=fastapi_app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def admin_client(admin_app):
    httpx = pytest.importorskip("httpx")
    transport = httpx.ASGITransport(app=admin_app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def no_org_client(no_org_app):
    httpx = pytest.importorskip("httpx")
    transport = httpx.ASGITransport(app=no_org_app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")


@pytest.fixture
def anon_client(anon_app):
    httpx = pytest.importorskip("httpx")
    transport = httpx.ASGITransport(app=anon_app)
    return httpx.AsyncClient(transport=transport, base_url="http://test")
