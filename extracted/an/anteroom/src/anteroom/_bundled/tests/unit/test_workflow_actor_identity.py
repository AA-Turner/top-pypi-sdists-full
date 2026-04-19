"""End-to-end actor-identity preservation for workflow emissions (#925).

The senior re-review flagged that earlier tests only exercised the
``_actor_id_from_request`` helper with a manually-set
``request.state.user_id``, but no middleware in production was stamping
that attribute. These tests drive a real authenticated request through
the full ``BearerTokenMiddleware`` stack (which now stamps
``request.state.user_id = config.identity.user_id`` on successful auth)
and verify the stamped identity actually flows into the workflow router
emission.
"""

from __future__ import annotations

import hashlib
import sqlite3
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from anteroom.app import BearerTokenMiddleware, _derive_auth_token
from anteroom.config import SessionConfig, UserIdentity
from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.routers.workflows import router as workflows_router


class _StubConfig:
    """Minimal config stub carrying only the fields the middleware reads."""

    def __init__(self, identity: UserIdentity) -> None:
        self.identity = identity
        self.trusted_proxy = None


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


@pytest.fixture()
def test_config() -> _StubConfig:
    identity = UserIdentity(
        user_id="real-actor-42",
        display_name="",
        public_key="",
        private_key=(
            "-----BEGIN PRIVATE KEY-----\n"
            "MC4CAQAwBQYDK2VwBCIEIKm3jiGLj2ROYfJFzxVxV0iJq0J3XOqT5PnJPBG7vLZE\n"
            "-----END PRIVATE KEY-----"
        ),
    )
    return _StubConfig(identity=identity)


@pytest.fixture()
def stub_writer() -> Any:
    captured: list[Any] = []
    writer = MagicMock()
    writer.enabled = True
    writer.emit.side_effect = captured.append
    writer.captured = captured  # type: ignore[attr-defined]
    return writer


@pytest.fixture()
def authed_client(
    db: ThreadSafeConnection,
    test_config: _StubConfig,
    stub_writer: Any,
) -> tuple[TestClient, str]:
    """TestClient plumbed through real BearerTokenMiddleware + workflows router."""
    app = FastAPI()
    token = _derive_auth_token(test_config)
    token_hash = hashlib.sha256(token.encode()).hexdigest()
    app.add_middleware(
        BearerTokenMiddleware,
        token_hash=token_hash,
        auth_token=token,
        session_config=SessionConfig(allowed_ips=[]),
    )
    app.include_router(workflows_router, prefix="/api")
    app.state.db = db
    app.state.audit_writer = stub_writer
    app.state.config = test_config
    app.state.event_bus = None
    return TestClient(app), token


def _seed_running_run(db: ThreadSafeConnection) -> str:
    """Insert a workflow run in 'running' status so /cancel has something to cancel."""
    from anteroom.services import workflow_storage as ws

    run = ws.create_workflow_run(
        db,
        workflow_id="wf-identity-test",
        workflow_version="0.1",
        target_kind="none",
        target_ref="",
    )
    run_id: str = run["id"]
    ws.update_workflow_run(db, run_id, status="running")
    return run_id


class TestBearerMiddlewareStampsIdentity:
    def test_unauthenticated_request_is_401(
        self,
        authed_client: tuple[TestClient, str],
    ) -> None:
        """Auth failure keeps the middleware from ever reaching the handler.

        Defence in depth — a handler that relied on the stamp would
        never even be invoked on an unauthenticated call.
        """
        client, _ = authed_client
        resp = client.get("/api/workflow-runs")
        assert resp.status_code == 401


class TestWorkflowRouterEmitsRealActor:
    """These tests drive the REAL middleware path end-to-end so we know
    the single-user identity claim holds without any manual stamping."""

    def test_cancel_emission_uses_stamped_identity_without_body(
        self,
        authed_client: tuple[TestClient, str],
        stub_writer: Any,
        db: ThreadSafeConnection,
        test_config: _StubConfig,
    ) -> None:
        """With no body override, the emission user_id is the stamped identity."""
        run_id = _seed_running_run(db)
        client, token = authed_client
        resp = client.post(
            f"/api/workflow-runs/{run_id}/cancel",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200, resp.text
        cancel_events = [e for e in stub_writer.captured if e.event_type == "workflow.cancel_requested"]
        assert len(cancel_events) == 1
        assert cancel_events[0].user_id == test_config.identity.user_id == "real-actor-42"
        # Crucially, NOT the legacy "operator" fallback:
        assert cancel_events[0].user_id != "operator"

    def test_cancel_emission_body_override_beats_stamped_identity(
        self,
        authed_client: tuple[TestClient, str],
        stub_writer: Any,
        db: ThreadSafeConnection,
    ) -> None:
        """Body `resolved_by` wins; CLI identity flows through server-mode."""
        run_id = _seed_running_run(db)
        client, token = authed_client
        resp = client.post(
            f"/api/workflow-runs/{run_id}/cancel",
            headers={"Authorization": f"Bearer {token}"},
            json={"resolved_by": "explicit-cli-actor"},
        )
        assert resp.status_code == 200, resp.text
        cancel_events = [e for e in stub_writer.captured if e.event_type == "workflow.cancel_requested"]
        assert len(cancel_events) == 1
        assert cancel_events[0].user_id == "explicit-cli-actor"
