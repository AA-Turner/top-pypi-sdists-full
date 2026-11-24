"""THE TEST STAMP on the standalone files service (files.matrxserver.com).

Every row a TEST session creates carries ``test_run_id`` + ``test_expires_at``, stamped by the
database trigger ``platform._stamp_test_run`` from the transaction-local GUC ``app.test_run``. A row
body never carries the stamp; the WRITER declares it. Until 2026-10-30 this service declared
nothing, so a ``dev-login`` test run's uploads to files.matrxserver.com (the browser sends
``X-Matrx-Test-Run``) landed unstamped and ``test_run_left_live.py --archive`` never found them.

* IN: ``X-Matrx-Test-Run: <uuid>`` → one ContextVar (:class:`TestRunMiddleware`, pure ASGI).
* OUT: :func:`test_run_gucs` is the matrx-orm session-context provider, so every top-level
  transaction (and every standalone write) opened while it is set begins with ``app.test_run``.
* ACROSS HOPS: only a ``detached_task(..., carry_test_run=True)`` carries it.

No header ⇒ nothing declared ⇒ nothing stamped. Standalone only — the aidream host declares its
own provider (``aidream/services/runtime/test_run.py``) and never calls :func:`install_test_run_stamp`.
Twins: that host module and ``matrx_scraper/test_stamp.py`` (consolidation into one shared
primitive is open work — common-docs file-service STATE.md).
"""

from __future__ import annotations

import re
from contextvars import ContextVar
from typing import Any

from matrx_utils import register_detached_test_run_carrier

HEADER = "x-matrx-test-run"
TEST_RUN_GUC = "app.test_run"

_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I)

_current: ContextVar[str | None] = ContextVar("matrx_files_test_run", default=None)
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


class TestRunMiddleware:
    """Header → ContextVar (pure ASGI, never touches the body). Inert without the header."""

    __test__ = False

    def __init__(self, app: Any) -> None:
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Any, send: Any) -> None:
        run_id = None
        if scope.get("type") in ("http", "websocket"):
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
    """Header middleware + the matrx-orm session-context provider (standalone service only)."""
    from matrx_orm import configure_session_context

    from matrx_files.standalone.request_actor import standalone_session_gucs

    app.add_middleware(TestRunMiddleware)
    # ONE provider for the service: the request's declared actor (request_actor.py) AND the test stamp —
    # a provider that forwarded only the stamp dropped every actor declaration (AD282).
    configure_session_context(standalone_session_gucs)


__all__ = [
    "HEADER",
    "TEST_RUN_GUC",
    "TestRunMiddleware",
    "current_test_run_id",
    "install_test_run_stamp",
    "parse_run_id",
    "test_run_gucs",
]
