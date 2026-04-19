"""Tests for the memory API router."""

from __future__ import annotations

import sqlite3
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from anteroom.db import _SCHEMA, ThreadSafeConnection
from anteroom.routers.memory import router
from anteroom.services.memory_service import create_memory


@pytest.fixture()
def db() -> ThreadSafeConnection:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(_SCHEMA)
    conn.commit()
    return ThreadSafeConnection(conn)


@pytest.fixture()
def client(db: ThreadSafeConnection) -> TestClient:
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.state.db = db
    return TestClient(app)


class TestListMemoryEndpoint:
    def test_list_empty(self, client: TestClient) -> None:
        resp = client.get("/api/memory")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_returns_memories(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "prefers dark mode", scope="user", category="preference", name="dark")
        create_memory(db, "uses postgres", scope="project", category="project_fact", project_slug="app", name="pg")
        resp = client.get("/api/memory")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_filter_by_scope(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="u")
        create_memory(db, "b", scope="local", category="preference", name="l")
        resp = client.get("/api/memory?scope=user")
        assert resp.status_code == 200
        body = resp.json()
        assert len(body) == 1
        assert body[0]["metadata"]["memory_scope"] == "user"

    def test_filter_by_status(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="u1", status="active")
        create_memory(db, "b", scope="user", category="preference", name="u2", status="candidate")
        resp = client.get("/api/memory?status=candidate")
        assert resp.status_code == 200
        body = resp.json()
        assert len(body) == 1
        assert body[0]["metadata"]["memory_status"] == "candidate"

    def test_filter_by_category(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "a", scope="user", category="preference", name="u1")
        create_memory(db, "b", scope="user", category="decision", name="u2")
        resp = client.get("/api/memory?category=decision")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_invalid_scope_rejected(self, client: TestClient) -> None:
        assert client.get("/api/memory?scope=team").status_code == 400

    def test_invalid_status_rejected(self, client: TestClient) -> None:
        assert client.get("/api/memory?status=deleted").status_code == 400

    def test_invalid_category_rejected(self, client: TestClient) -> None:
        assert client.get("/api/memory?category=random").status_code == 400


class TestGetMemoryEndpoint:
    def test_get_existing(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "content", scope="user", category="preference", name="get1")
        resp = client.get("/api/memory/@user/memory/get1")
        assert resp.status_code == 200
        body = resp.json()
        assert body["fqn"] == "@user/memory/get1"
        assert body["content"] == "content"

    def test_get_missing_returns_404(self, client: TestClient) -> None:
        assert client.get("/api/memory/@user/memory/nope").status_code == 404

    def test_malformed_fqn_rejected(self, client: TestClient) -> None:
        # Traversal and shape violations resolve to 400, not 404.
        assert client.get("/api/memory/@user/memory/..").status_code == 400
        assert client.get("/api/memory/@user/skill/not-a-memory").status_code == 400
        assert client.get("/api/memory/user/memory/no-at").status_code == 400

    def test_get_refuses_non_memory_artifact(self, client: TestClient, db: ThreadSafeConnection) -> None:
        # Even if the FQN passes the regex, a non-memory artifact with the same
        # FQN shape must not be returned.
        from anteroom.services.artifact_storage import create_artifact
        from anteroom.services.artifacts import ArtifactType

        create_artifact(
            db,
            fqn="@user/memory/skill-masquerade",
            artifact_type=ArtifactType.SKILL,
            namespace="user",
            name="skill-masquerade",
            content="a skill",
            metadata={},
        )
        # Regex lets it through (the path shape is valid), but the service
        # refuses to treat it as a memory — expect 404.
        resp = client.get("/api/memory/@user/memory/skill-masquerade")
        assert resp.status_code == 404


class TestCreateMemoryEndpoint:
    def test_create_user_scope(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory",
            json={"content": "hi", "scope": "user", "category": "preference"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["type"] == "memory"
        assert body["namespace"] == "user"
        assert body["content"] == "hi"

    def test_create_project_scope_requires_slug(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory",
            json={"content": "x", "scope": "project", "category": "preference"},
        )
        assert resp.status_code == 400
        assert "project_slug" in resp.json()["detail"]

    def test_create_with_custom_name(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory",
            json={"content": "x", "scope": "user", "category": "preference", "name": "custom"},
        )
        assert resp.status_code == 200
        assert resp.json()["fqn"] == "@user/memory/custom"

    def test_create_invalid_scope(self, client: TestClient) -> None:
        resp = client.post("/api/memory", json={"content": "x", "scope": "team", "category": "preference"})
        assert resp.status_code == 400

    def test_create_invalid_category(self, client: TestClient) -> None:
        resp = client.post("/api/memory", json={"content": "x", "scope": "user", "category": "random"})
        assert resp.status_code == 400

    def test_create_empty_content_rejected(self, client: TestClient) -> None:
        resp = client.post("/api/memory", json={"content": "", "scope": "user", "category": "preference"})
        # Pydantic validation — min_length=1.
        assert resp.status_code == 422

    def test_create_project_slug_reserved_rejected(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory",
            json={
                "content": "x",
                "scope": "project",
                "category": "preference",
                "project_slug": "user",
            },
        )
        assert resp.status_code == 400

    def test_create_invalid_status_rejected(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory",
            json={"content": "x", "scope": "user", "category": "preference", "status": "deleted"},
        )
        assert resp.status_code == 400
        assert "status" in resp.json()["detail"].lower()

    def test_create_invalid_created_by_rejected(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory",
            json={
                "content": "x",
                "scope": "user",
                "category": "preference",
                "created_by": "system",
            },
        )
        assert resp.status_code == 400
        assert "created_by" in resp.json()["detail"]

    def test_create_duplicate_fqn_returns_409(self, client: TestClient) -> None:
        # Duplicates raise sqlite3.IntegrityError at the service layer.
        # The router must catch it and surface 409, not leak a 500.
        first = client.post(
            "/api/memory",
            json={"content": "a", "scope": "user", "category": "preference", "name": "dup"},
        )
        assert first.status_code == 200
        second = client.post(
            "/api/memory",
            json={"content": "b", "scope": "user", "category": "preference", "name": "dup"},
        )
        assert second.status_code == 409
        assert "already exists" in second.json()["detail"].lower()


class TestEditMemoryEndpoint:
    def test_edit_content(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "v1", scope="user", category="preference", name="e1")
        resp = client.patch("/api/memory/@user/memory/e1", json={"content": "v2"})
        assert resp.status_code == 200
        assert resp.json()["content"] == "v2"

    def test_edit_allowed_metadata(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="e2")
        resp = client.patch(
            "/api/memory/@user/memory/e2",
            json={"metadata": {"memory_status": "archived"}},
        )
        assert resp.status_code == 200
        assert resp.json()["metadata"]["memory_status"] == "archived"

    def test_edit_rejects_unknown_metadata_field(self, client: TestClient, db: ThreadSafeConnection) -> None:
        # Truly unknown keys still 400. Review-state fields (reviewed_by,
        # rejected_reason, lineage) moved into the allowlist with #920 so
        # PATCH can still accept them for recovery / admin flows; governed
        # promotion transitions go through the /approve / /reject endpoints.
        create_memory(db, "x", scope="user", category="preference", name="e3")
        resp = client.patch("/api/memory/@user/memory/e3", json={"metadata": {"bogus": "whatever"}})
        assert resp.status_code == 400
        assert "Unknown metadata field" in resp.json()["detail"]

    def test_edit_rejects_memory_scope_change(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="e4")
        resp = client.patch(
            "/api/memory/@user/memory/e4",
            json={"metadata": {"memory_scope": "local"}},
        )
        # memory_scope is in the allowlist check, but update_memory_metadata
        # rejects it with a dedicated error. Router should surface as 400.
        assert resp.status_code == 400

    def test_edit_requires_at_least_one_field(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="e5")
        resp = client.patch("/api/memory/@user/memory/e5", json={})
        assert resp.status_code == 400

    def test_edit_missing_returns_404(self, client: TestClient) -> None:
        resp = client.patch("/api/memory/@user/memory/nope", json={"content": "x"})
        assert resp.status_code == 404


class TestDeleteMemoryEndpoint:
    def test_delete_existing(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "gone", scope="user", category="preference", name="d1")
        resp = client.delete("/api/memory/@user/memory/d1")
        assert resp.status_code == 200
        assert resp.json() == {"status": "deleted"}
        # Confirm idempotent second delete -> 404.
        assert client.delete("/api/memory/@user/memory/d1").status_code == 404

    def test_delete_missing_returns_404(self, client: TestClient) -> None:
        assert client.delete("/api/memory/@user/memory/nope").status_code == 404

    def test_delete_refuses_non_memory(self, client: TestClient, db: ThreadSafeConnection) -> None:
        from anteroom.services.artifact_storage import create_artifact, get_artifact_by_fqn
        from anteroom.services.artifacts import ArtifactType

        create_artifact(
            db,
            fqn="@user/memory/fake-skill",
            artifact_type=ArtifactType.SKILL,
            namespace="user",
            name="fake-skill",
            content="skill",
            metadata={},
        )
        # FQN passes the path regex but the service refuses non-memory types.
        resp = client.delete("/api/memory/@user/memory/fake-skill")
        assert resp.status_code == 404
        # Foreign artifact is still there.
        assert get_artifact_by_fqn(db, "@user/memory/fake-skill") is not None


# ---------------------------------------------------------------------------
# Promotion / review endpoints (#920)
# ---------------------------------------------------------------------------


class TestProposeCandidateEndpoint:
    def _post(self, client: TestClient, **kwargs: object) -> object:
        body = {
            "content": "dark mode preferred",
            "scope": "user",
            "category": "preference",
            "proposer": "user",
            "proposer_id": "u-1",
        }
        body.update(kwargs)
        return client.post("/api/memory/candidates", json=body)

    def test_propose_happy_path(self, client: TestClient) -> None:
        resp = self._post(client)
        assert resp.status_code == 200
        data = resp.json()
        assert data["metadata"]["memory_status"] == "candidate"
        assert data["metadata"]["lineage"][0]["event"] == "proposed"

    def test_propose_invalid_scope(self, client: TestClient) -> None:
        resp = self._post(client, scope="team")
        assert resp.status_code == 400

    def test_propose_invalid_category(self, client: TestClient) -> None:
        resp = self._post(client, category="nope")
        assert resp.status_code == 400

    def test_propose_empty_content_rejected(self, client: TestClient) -> None:
        resp = self._post(client, content="")
        assert resp.status_code == 422  # Pydantic min_length=1

    def test_propose_invalid_proposer(self, client: TestClient) -> None:
        resp = self._post(client, proposer="system")
        assert resp.status_code == 400

    def test_propose_with_provenance(self, client: TestClient) -> None:
        resp = self._post(
            client,
            provenance={
                "conversation_id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
                "message_id": "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["metadata"]["provenance"]["conversation_id"] == "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"

    def test_propose_rate_limit_returns_429(self, client: TestClient) -> None:
        from anteroom.config import AIConfig, AppConfig, MemoryConfig, MemoryPromotionConfig

        cfg = AppConfig(ai=AIConfig(base_url="x", api_key="y", model="m"))
        cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig(max_candidates_per_conversation=1))
        client.app.state.config = cfg  # type: ignore[attr-defined]

        prov = {"conversation_id": "cafecafe-cafe-cafe-cafe-cafecafecafe"}
        first = self._post(client, name="rl-first", provenance=prov)
        assert first.status_code == 200
        second = self._post(client, name="rl-second", provenance=prov)
        assert second.status_code == 429
        body = second.json()["detail"]
        assert body["cap"] == 1
        assert body["current"] == 1
        assert body["retry_hint"]

    def test_propose_agent_blocked_returns_403(self, client: TestClient) -> None:
        from anteroom.config import AIConfig, AppConfig, MemoryConfig, MemoryPromotionConfig

        cfg = AppConfig(ai=AIConfig(base_url="x", api_key="y", model="m"))
        cfg.memory = MemoryConfig(promotion=MemoryPromotionConfig(agent_proposals_enabled=False))
        client.app.state.config = cfg  # type: ignore[attr-defined]

        resp = self._post(client, proposer="agent")
        assert resp.status_code == 403


class TestListCandidatesEndpoint:
    def test_list_defaults_to_candidate(self, client: TestClient) -> None:
        client.post(
            "/api/memory/candidates",
            json={
                "content": "a",
                "scope": "user",
                "category": "preference",
                "proposer": "user",
                "proposer_id": "u-1",
                "name": "list-a",
            },
        )
        resp = client.get("/api/memory/candidates")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_list_invalid_status(self, client: TestClient) -> None:
        resp = client.get("/api/memory/candidates?status=bogus")
        assert resp.status_code == 400

    def test_list_respects_limit(self, client: TestClient) -> None:
        for i in range(3):
            client.post(
                "/api/memory/candidates",
                json={
                    "content": f"a{i}",
                    "scope": "user",
                    "category": "preference",
                    "proposer": "user",
                    "proposer_id": "u-1",
                    "name": f"list-limit-{i}",
                },
            )
        resp = client.get("/api/memory/candidates?limit=2")
        assert resp.status_code == 200
        assert len(resp.json()) == 2


def _propose_one(client: TestClient, name: str = "default") -> str:
    """Propose a candidate through the API and return its FQN."""
    resp = client.post(
        "/api/memory/candidates",
        json={
            "content": "prefer dark mode",
            "scope": "user",
            "category": "preference",
            "proposer": "user",
            "proposer_id": "u-1",
            "name": name,
        },
    )
    assert resp.status_code == 200
    return resp.json()["fqn"]


class TestApproveRejectEndpoints:
    def test_approve_transitions_to_active(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar1")
        resp = client.post(f"/api/memory/{fqn}/approve", json={"reviewer_display": "Alice"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["metadata"]["memory_status"] == "active"
        assert body["metadata"]["lineage"][-1]["event"] == "approved"

    def test_approve_with_edits_transitions_and_edits(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar2")
        resp = client.post(
            f"/api/memory/{fqn}/approve",
            json={"edits": {"content": "edited text", "category": "decision"}},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["content"] == "edited text"
        assert body["metadata"]["memory_category"] == "decision"
        assert body["metadata"]["memory_status"] == "active"

    def test_approve_unknown_fqn_returns_404(self, client: TestClient) -> None:
        resp = client.post("/api/memory/@user/memory/none/approve", json={})
        assert resp.status_code == 404

    def test_approve_active_returns_409(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar3")
        first = client.post(f"/api/memory/{fqn}/approve", json={})
        assert first.status_code == 200
        second = client.post(f"/api/memory/{fqn}/approve", json={})
        assert second.status_code == 409

    def test_edit_and_approve_requires_edits(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar4")
        resp = client.post(f"/api/memory/{fqn}/edit-and-approve", json={})
        assert resp.status_code == 400

    def test_reject_transitions_to_rejected(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar5")
        resp = client.post(f"/api/memory/{fqn}/reject", json={"reason": "stale"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["metadata"]["memory_status"] == "rejected"
        assert body["metadata"]["rejected_reason"] == "stale"

    def test_reject_empty_reason_422(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar6")
        resp = client.post(f"/api/memory/{fqn}/reject", json={"reason": ""})
        assert resp.status_code == 422  # Pydantic min_length=1

    def test_reject_unknown_fqn_returns_404(self, client: TestClient) -> None:
        resp = client.post(
            "/api/memory/@user/memory/none/reject",
            json={"reason": "gone"},
        )
        assert resp.status_code == 404

    def test_reject_already_rejected_returns_409(self, client: TestClient) -> None:
        fqn = _propose_one(client, name="ar7")
        first = client.post(f"/api/memory/{fqn}/reject", json={"reason": "stale"})
        assert first.status_code == 200
        second = client.post(f"/api/memory/{fqn}/reject", json={"reason": "stale again"})
        assert second.status_code == 409


# ---------------------------------------------------------------------------
# Pin / unpin endpoints (#625)
# ---------------------------------------------------------------------------


class TestPinEndpoints:
    def test_pin_sets_pinned_true(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="pin-e1")
        resp = client.post("/api/memory/@user/memory/pin-e1/pin", json={})
        assert resp.status_code == 200
        assert resp.json()["metadata"]["pinned"] is True

    def test_unpin_sets_pinned_false(self, client: TestClient, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="pin-e2")
        client.post("/api/memory/@user/memory/pin-e2/pin", json={})
        resp = client.post("/api/memory/@user/memory/pin-e2/unpin", json={})
        assert resp.status_code == 200
        assert resp.json()["metadata"]["pinned"] is False

    def test_pin_missing_returns_404(self, client: TestClient) -> None:
        resp = client.post("/api/memory/@user/memory/no-such/pin", json={})
        assert resp.status_code == 404

    def test_unpin_missing_returns_404(self, client: TestClient) -> None:
        resp = client.post("/api/memory/@user/memory/no-such/unpin", json={})
        assert resp.status_code == 404

    def test_pin_bad_fqn_returns_400(self, client: TestClient) -> None:
        resp = client.post("/api/memory/@user/memory/../pin", json={})
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Retention endpoints (#625)
# ---------------------------------------------------------------------------


def _retention_client_with_policy(db: ThreadSafeConnection, **kwargs: Any) -> TestClient:
    """Build a TestClient whose ``app.state.config.memory.retention`` is a
    real ``MemoryRetentionConfig`` (not a default). This exercises the
    ``_retention_config(request)`` lookup path, not the fallback."""
    from anteroom.config import AIConfig, AppConfig, MemoryConfig, MemoryRetentionConfig

    cfg = AppConfig(ai=AIConfig(base_url="x", api_key="y", model="m"))
    cfg.memory = MemoryConfig(retention=MemoryRetentionConfig(**kwargs))
    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.state.db = db
    app.state.config = cfg
    return TestClient(app)


class TestRetentionPreviewEndpoint:
    def test_preview_empty_when_policy_disabled(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="prev1", status="rejected")
        client = _retention_client_with_policy(db, enabled=False)
        resp = client.get("/api/memory/retention-preview")
        assert resp.status_code == 200
        body = resp.json()
        assert body["dry_run"] is True
        assert body["purged_count"] == 0
        assert body["items"] == []

    def test_preview_lists_candidates_when_enabled(self, db: ThreadSafeConnection) -> None:
        create_memory(db, "x", scope="user", category="preference", name="prev2", status="rejected")
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])
        resp = client.get("/api/memory/retention-preview")
        assert resp.status_code == 200
        body = resp.json()
        assert body["dry_run"] is True
        assert body["purged_count"] == 1
        assert body["items"][0]["reason"] == "status"

    def test_preview_does_not_delete(self, client: TestClient, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import get_memory

        create_memory(db, "x", scope="user", category="preference", name="prev3")
        client.get("/api/memory/retention-preview")
        assert get_memory(db, "@user/memory/prev3") is not None

    def test_preview_ordering_regression(self, client: TestClient) -> None:
        """Route registration order: the literal ``retention-preview`` path
        must beat the ``{fqn:path}`` catchall. Before the #625 fix this
        request would have returned 400 'Invalid memory FQN' because
        ``retention-preview`` would be parsed as an FQN and fail the regex."""
        resp = client.get("/api/memory/retention-preview")
        assert resp.status_code == 200
        assert "items" in resp.json()


class TestRetentionPurgeEndpoint:
    def test_purge_without_confirm_returns_400(self, db: ThreadSafeConnection) -> None:
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])
        resp = client.post("/api/memory/retention-purge", json={"confirm": False})
        assert resp.status_code == 400

    def test_purge_missing_confirm_is_422(self, db: ThreadSafeConnection) -> None:
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])
        resp = client.post("/api/memory/retention-purge", json={})
        assert resp.status_code == 422  # Pydantic required field

    def test_purge_with_confirm_removes_candidates(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import get_memory

        create_memory(db, "x", scope="user", category="preference", name="pg1", status="rejected")
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])
        resp = client.post("/api/memory/retention-purge", json={"confirm": True})
        assert resp.status_code == 200
        body = resp.json()
        assert body["dry_run"] is False
        assert body["purged_count"] == 1
        assert get_memory(db, "@user/memory/pg1") is None

    def test_purge_with_policy_disabled_is_noop(self, db: ThreadSafeConnection) -> None:
        from anteroom.services.memory_service import get_memory

        create_memory(db, "x", scope="user", category="preference", name="pg2", status="rejected")
        client = _retention_client_with_policy(db, enabled=False)
        resp = client.post("/api/memory/retention-purge", json={"confirm": True})
        assert resp.status_code == 200
        assert resp.json()["purged_count"] == 0
        assert get_memory(db, "@user/memory/pg2") is not None

    def test_purge_stamps_reviewer_identity_from_request(self, db: ThreadSafeConnection) -> None:
        """Reviewer identity flows from the auth layer (request.state.user_id)
        into the PurgeResult.purged_by field in the response body."""
        from starlette.middleware.base import BaseHTTPMiddleware

        create_memory(db, "x", scope="user", category="preference", name="pgr1", status="rejected")
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])

        # Inject the middleware that the production auth layer would — stamp
        # a user_id onto request.state so _reviewer_id_from_request picks it up.
        class _StampUserIdMiddleware(BaseHTTPMiddleware):
            async def dispatch(self, request: Any, call_next: Any) -> Any:
                request.state.user_id = "alice-session-uid"
                return await call_next(request)

        client.app.user_middleware = []
        client.app.middleware_stack = None
        client.app.add_middleware(_StampUserIdMiddleware)
        client.app.build_middleware_stack()

        resp = client.post("/api/memory/retention-purge", json={"confirm": True})
        assert resp.status_code == 200
        body = resp.json()
        assert body["purged_count"] == 1
        assert body["purged_by"] == "alice-session-uid"

    def test_purge_falls_back_to_config_identity_when_state_absent(self, db: ThreadSafeConnection) -> None:
        """When no session user_id is stamped on request.state,
        _reviewer_id_from_request falls back to app.state.config.identity.user_id."""
        create_memory(db, "x", scope="user", category="preference", name="pgr2", status="rejected")
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])
        # Set a real identity on app.state.config.identity.
        from unittest.mock import MagicMock

        identity = MagicMock()
        identity.user_id = "install-owner-uid"
        client.app.state.config.identity = identity

        resp = client.post("/api/memory/retention-purge", json={"confirm": True})
        assert resp.status_code == 200
        assert resp.json()["purged_by"] == "install-owner-uid"

    def test_preview_response_does_not_include_purged_by_when_unset(self, db: ThreadSafeConnection) -> None:
        """The preview path does not supply a reviewer_id, so purged_by
        in the response is null. This also exercises the key being present
        in the payload envelope even when None."""
        client = _retention_client_with_policy(db, enabled=True, purge_statuses=["rejected"])
        resp = client.get("/api/memory/retention-preview")
        assert resp.status_code == 200
        body = resp.json()
        assert "purged_by" in body
        assert body["purged_by"] is None
