"""THE TEST STAMP on the scraper service — a test session's run id reaches Postgres as ``app.test_run``.

Every row a TEST session creates carries ``test_run_id`` + ``test_expires_at``, stamped by the database
trigger ``platform._stamp_test_run`` from the transaction-local GUC ``app.test_run``. A row body never
carries the stamp (the trigger ignores one); the WRITER declares it. This module is how the standalone
scraper service declares it, the same way every other platform server does:

* IN: a request carrying ``X-Matrx-Test-Run: <uuid>`` (aidream's scraper client forwards its own test
  run; a ``dev-login`` browser sends it directly) — :class:`TestRunMiddleware` puts it in one ContextVar.
* OUT: :func:`test_run_gucs` is the matrx-orm session-context provider (:func:`install_test_run_stamp`),
  so every top-level transaction opened while it is set begins with ``set_config('app.test_run', …, true)``.
* ACROSS HOPS: the stamp crosses a ``detached_task`` hop ONLY where the spawner opts in
  (``carry_test_run=True``: the hop writes this crawl's own rows) — a sweep or tail a test request
  happens to trigger starts unstamped. A crawl never needs the hop: its stamp is PERSISTED on its
  session (``scope["test_run_id"]``, :func:`stamp_scope`) and every run — started, resumed, or
  crash-resumed with no request at all — re-declares exactly that (:func:`declared_test_run`) before it writes.

No header ⇒ nothing is declared ⇒ nothing is stamped. Never imports the host (package boundary): the
host-side twin is aidream ``services/runtime/test_run.py``.
"""

from __future__ import annotations

import re
from collections.abc import Iterator, MutableMapping
from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any

from matrx_utils import register_detached_test_run_carrier

HEADER = "x-matrx-test-run"
TEST_RUN_GUC = "app.test_run"
#: Key under a crawl session's ``scope`` carrying the run's stamp across the request boundary.
SCOPE_KEY = "test_run_id"

_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)

_current: ContextVar[str | None] = ContextVar("matrx_scraper_test_run", default=None)
# A detached task starts with an empty context, and the stamp crosses only when the spawner declares the
# task writes this request's own rows (``detached_task(..., carry_test_run=True)``). Never an always-carried
# identity carrier: a sweep a test request triggers would stamp — and later archive — other people's rows.
register_detached_test_run_carrier(_current)


def parse_run_id(raw: Any) -> str | None:
    value = str(raw or "").strip().lower()
    return value if _UUID.match(value) else None


def current_test_run_id() -> str | None:
    return _current.get()


def test_run_gucs() -> dict[str, str]:
    """The GUCs the current test run implies; empty outside a test session."""
    run_id = _current.get()
    return {TEST_RUN_GUC: run_id} if run_id else {}


@contextmanager
def test_run_scope(run_id: Any) -> Iterator[str | None]:
    """Stamp every row written inside this block with ``run_id``; a no-op when it is not a uuid."""
    parsed = parse_run_id(run_id)
    if parsed is None:
        yield _current.get()
        return
    token = _current.set(parsed)
    try:
        yield parsed
    finally:
        _current.reset(token)


@contextmanager
def declared_test_run(run_id: Any) -> Iterator[str | None]:
    """The block runs as EXACTLY ``run_id``'s test run — or, when it is not a uuid, as NO test run.

    Unlike :func:`test_run_scope` this never inherits: a durable record that persisted no stamp (a person's
    crawl) clears an ambient one, so a resume reached through a test request never stamps its new rows."""
    token = _current.set(parse_run_id(run_id))
    try:
        yield _current.get()
    finally:
        _current.reset(token)


def stamp_scope(scope: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    """Persist the ambient test run on a durable record's ``scope`` (no-op outside a test session)."""
    run_id = _current.get()
    if run_id:
        scope[SCOPE_KEY] = run_id
    return scope


def scope_test_run_id(scope: Any) -> str | None:
    """The test run a durable record's ``scope`` was started under."""
    return parse_run_id(scope.get(SCOPE_KEY)) if isinstance(scope, dict) else None


class TestRunMiddleware:
    """Header → ContextVar (pure ASGI, never touches the body). Inert without the header."""

    __test__ = False  # not a pytest class

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        if scope.get("type") not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return
        run_id = None
        for name, value in scope.get("headers") or ():
            if name == HEADER.encode():
                run_id = parse_run_id(value.decode("latin-1"))
                break
        if run_id is None:
            await self.app(scope, receive, send)
            return
        token = _current.set(run_id)
        try:
            await self.app(scope, receive, send)
        finally:
            _current.reset(token)


def install_test_run_stamp(app: Any) -> None:
    """Wire the stamp into a standalone server: the header middleware + the matrx-orm provider.

    Only for a process where this package owns the ORM session context (the scraper service). A host
    that mounts these routes itself (aidream) declares its own provider and must not call this.
    """
    from matrx_orm import configure_session_context

    app.add_middleware(TestRunMiddleware)
    configure_session_context(test_run_gucs)


__all__ = [
    "HEADER", "SCOPE_KEY", "TEST_RUN_GUC", "TestRunMiddleware", "current_test_run_id", "declared_test_run",
    "install_test_run_stamp", "parse_run_id", "scope_test_run_id", "stamp_scope",
    "test_run_gucs", "test_run_scope",
]
