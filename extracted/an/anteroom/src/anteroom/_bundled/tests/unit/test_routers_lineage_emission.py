"""Router-level emission tests for #925.

Verifies that the memory and workflow routers emit the correct lineage
events on the success path. The emission goes through the lineage layer
which calls ``audit_writer.emit(entry)`` only when audit is enabled.

Tests use a stub ``audit_writer`` rather than a real ``AuditWriter`` so
they can introspect emitted entries directly without spinning up the
HMAC chain or touching disk.
"""

from __future__ import annotations

import sqlite3
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.routers.memory import router as memory_router
from anteroom.routers.workflows import router as workflows_router
from anteroom.services.memory_service import create_memory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


@pytest.fixture()
def stub_writer() -> Any:
    captured: list[Any] = []
    writer = MagicMock()
    writer.enabled = True
    writer.emit.side_effect = captured.append
    writer.captured = captured  # type: ignore[attr-defined]
    return writer


@pytest.fixture()
def memory_client(db: ThreadSafeConnection, stub_writer: Any) -> TestClient:
    app = FastAPI()
    app.include_router(memory_router, prefix="/api")
    app.state.db = db
    app.state.audit_writer = stub_writer
    return TestClient(app)


@pytest.fixture()
def workflow_client(db: ThreadSafeConnection, stub_writer: Any) -> TestClient:
    app = FastAPI()
    app.include_router(workflows_router, prefix="/api")
    app.state.db = db
    app.state.audit_writer = stub_writer
    return TestClient(app)


# ---------------------------------------------------------------------------
# Memory emission
# ---------------------------------------------------------------------------


class TestMemoryRouterEmissions:
    def test_approve_emits_memory_approved(
        self,
        memory_client: TestClient,
        db: ThreadSafeConnection,
        stub_writer: Any,
    ) -> None:
        mem = create_memory(
            db,
            "test content",
            scope="user",
            category="preference",
            name="emit",
            status="candidate",
        )
        resp = memory_client.post(
            f"/api/memory/{mem['fqn']}/approve",
            json={},
        )
        assert resp.status_code == 200
        events = [e.event_type for e in stub_writer.captured]
        assert "memory.approved" in events
        approved = next(e for e in stub_writer.captured if e.event_type == "memory.approved")
        assert approved.details["fqn"] == mem["fqn"]

    def test_reject_emits_memory_rejected(
        self,
        memory_client: TestClient,
        db: ThreadSafeConnection,
        stub_writer: Any,
    ) -> None:
        mem = create_memory(
            db,
            "test content",
            scope="user",
            category="preference",
            name="emit2",
            status="candidate",
        )
        resp = memory_client.post(
            f"/api/memory/{mem['fqn']}/reject",
            json={"reason": "not relevant"},
        )
        assert resp.status_code == 200
        events = [e.event_type for e in stub_writer.captured]
        assert "memory.rejected" in events

    def test_propose_emits_memory_proposed(
        self,
        memory_client: TestClient,
        stub_writer: Any,
    ) -> None:
        """#925 senior review gap 1: propose path must emit memory.proposed."""
        resp = memory_client.post(
            "/api/memory/candidates",
            json={
                "content": "new proposal",
                "scope": "user",
                "category": "preference",
                "proposer": "user",
                "proposer_id": "alice",
                "name": "propcli1",
            },
        )
        assert resp.status_code == 200
        events = [e.event_type for e in stub_writer.captured]
        assert "memory.proposed" in events
        proposed = next(e for e in stub_writer.captured if e.event_type == "memory.proposed")
        # Actor identity must be preserved from the request body
        assert proposed.user_id == "alice"
        assert proposed.details["proposer"] == "user"

    def test_audit_disabled_no_emission(
        self,
        db: ThreadSafeConnection,
    ) -> None:
        # writer.enabled = False → router's _audit_writer returns None
        # → lineage.emit_memory_promotion is a no-op.
        captured: list[Any] = []
        writer = MagicMock()
        writer.enabled = False
        writer.emit.side_effect = captured.append

        app = FastAPI()
        app.include_router(memory_router, prefix="/api")
        app.state.db = db
        app.state.audit_writer = writer
        client = TestClient(app)

        mem = create_memory(db, "x", scope="user", category="preference", name="off", status="candidate")
        resp = client.post(f"/api/memory/{mem['fqn']}/approve", json={})
        assert resp.status_code == 200
        assert captured == []


# ---------------------------------------------------------------------------
# Workflow emission actor-identity preservation (#925 senior review gap 2)
# ---------------------------------------------------------------------------


class TestWorkflowRouterActorIdentity:
    def test_actor_id_helper_uses_body_override_first(self) -> None:
        """Body override beats session and config identity."""
        from unittest.mock import MagicMock

        from anteroom.routers.workflows import _actor_id_from_request

        request = MagicMock()
        request.state.user_id = "session-user"
        request.app.state.config.identity.user_id = "config-user"
        assert _actor_id_from_request(request, override="body-user") == "body-user"

    def test_actor_id_helper_falls_back_to_session(self) -> None:
        from unittest.mock import MagicMock

        from anteroom.routers.workflows import _actor_id_from_request

        request = MagicMock()
        request.state.user_id = "session-user"
        request.app.state.config.identity.user_id = "config-user"
        assert _actor_id_from_request(request, override=None) == "session-user"

    def test_actor_id_helper_falls_back_to_config_identity(self) -> None:
        from unittest.mock import MagicMock

        from anteroom.routers.workflows import _actor_id_from_request

        request = MagicMock()
        request.state.user_id = None
        request.app.state.config.identity.user_id = "config-user"
        assert _actor_id_from_request(request, override=None) == "config-user"

    def test_actor_id_helper_final_fallback_is_operator(self) -> None:
        from unittest.mock import MagicMock

        from anteroom.routers.workflows import _actor_id_from_request

        request = MagicMock()
        request.state.user_id = None
        # app.state.config with no identity
        request.app.state.config.identity = None
        assert _actor_id_from_request(request, override=None) == "operator"

    def test_actor_id_helper_ignores_whitespace_override(self) -> None:
        from unittest.mock import MagicMock

        from anteroom.routers.workflows import _actor_id_from_request

        request = MagicMock()
        request.state.user_id = "session-user"
        request.app.state.config.identity = None
        assert _actor_id_from_request(request, override="   ") == "session-user"


# ---------------------------------------------------------------------------
# Memory lineage endpoint
# ---------------------------------------------------------------------------


class TestMemoryLineageEndpoint:
    def test_existing_memory_returns_view(
        self,
        memory_client: TestClient,
        db: ThreadSafeConnection,
    ) -> None:
        mem = create_memory(
            db,
            "linenage test",
            scope="user",
            category="preference",
            name="lin",
            status="candidate",
            provenance={"conversation_id": "conv-x"},
        )
        resp = memory_client.get(f"/api/memory/{mem['fqn']}/lineage")
        assert resp.status_code == 200
        body = resp.json()
        assert body["fqn"] == mem["fqn"]
        # Provenance includes the conversation_id we set; other keys may
        # be present as None defaults from the storage layer.
        assert body["provenance"] is not None
        assert body["provenance"]["conversation_id"] == "conv-x"
        assert body["related_memories"] == []

    def test_missing_memory_returns_empty_view(
        self,
        memory_client: TestClient,
    ) -> None:
        resp = memory_client.get("/api/memory/@user/memory/nope/lineage")
        assert resp.status_code == 200
        body = resp.json()
        assert body["fqn"].endswith("nope")
        assert body["provenance"] is None
        assert body["lineage"] == []
        assert body["related_memories"] == []
