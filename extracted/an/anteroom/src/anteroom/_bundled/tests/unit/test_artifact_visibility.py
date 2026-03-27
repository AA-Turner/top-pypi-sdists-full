"""Tests for artifact visibility and delete guards (#1010)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from anteroom.routers.artifacts import router
from anteroom.services.artifact_storage import create_artifact
from anteroom.services.artifacts import ArtifactSource


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture()
def app(db: Any) -> FastAPI:
    application = FastAPI()
    application.include_router(router, prefix="/api")
    application.state.db = db
    application.state.artifact_registry = None
    return application


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)


def _create_test_artifact(db: Any, name: str = "greet", art_type: str = "skill") -> dict[str, Any]:
    fqn = f"@testns/{art_type}/{name}"
    return create_artifact(
        db,
        fqn=fqn,
        artifact_type=art_type,
        namespace="testns",
        name=name,
        content="Hello!",
        source=ArtifactSource.PROJECT,
    )


def _make_pack_owned(db: Any, artifact_id: str) -> str:
    pack_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO packs (id, name, namespace, version, description, source_path, installed_at, updated_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (pack_id, "test-pack", "testns", "1.0.0", "", "/tmp/pack", now, now),
    )
    db.execute(
        "INSERT INTO pack_artifacts (pack_id, artifact_id) VALUES (?, ?)",
        (pack_id, artifact_id),
    )
    db.commit()
    return pack_id


def _attach_pack(db: Any, pack_id: str, scope: str = "global") -> None:
    att_id = uuid.uuid4().hex
    now = datetime.now(timezone.utc).isoformat()
    db.execute(
        "INSERT INTO pack_attachments (id, pack_id, project_path, space_id, scope, priority, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (att_id, pack_id, None, None, scope, 50, now),
    )
    db.commit()


class TestListArtifactsAttachedOnly:
    def test_attached_only_filters(self, client: TestClient, db: Any) -> None:
        art = _create_test_artifact(db)
        _make_pack_owned(db, art["id"])
        # No attachment — should be filtered out
        resp = client.get("/api/artifacts?attached_only=true")
        assert resp.status_code == 200
        fqns = [a["fqn"] for a in resp.json()]
        assert "@testns/skill/greet" not in fqns

    def test_attached_only_includes_attached(self, client: TestClient, db: Any) -> None:
        art = _create_test_artifact(db)
        pack_id = _make_pack_owned(db, art["id"])
        _attach_pack(db, pack_id)
        resp = client.get("/api/artifacts?attached_only=true")
        assert resp.status_code == 200
        fqns = [a["fqn"] for a in resp.json()]
        assert "@testns/skill/greet" in fqns

    def test_attached_only_includes_standalone(self, client: TestClient, db: Any) -> None:
        _create_test_artifact(db)
        resp = client.get("/api/artifacts?attached_only=true")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_pack_owned_field_in_response(self, client: TestClient, db: Any) -> None:
        art = _create_test_artifact(db)
        pack_id = _make_pack_owned(db, art["id"])
        _attach_pack(db, pack_id)
        resp = client.get("/api/artifacts")
        assert resp.status_code == 200
        items = resp.json()
        assert len(items) == 1
        assert items[0]["pack_owned"] is True


class TestGetArtifactAttachedOnly:
    def test_attached_only_returns_404_for_detached(self, client: TestClient, db: Any) -> None:
        art = _create_test_artifact(db)
        _make_pack_owned(db, art["id"])
        resp = client.get("/api/artifacts/@testns/skill/greet?attached_only=true")
        assert resp.status_code == 404

    def test_attached_only_returns_ok_for_attached(self, client: TestClient, db: Any) -> None:
        art = _create_test_artifact(db)
        pack_id = _make_pack_owned(db, art["id"])
        _attach_pack(db, pack_id)
        resp = client.get("/api/artifacts/@testns/skill/greet?attached_only=true")
        assert resp.status_code == 200
        assert resp.json()["pack_owned"] is True


class TestDeleteArtifactGuard:
    def test_delete_returns_403_for_pack_owned(self, client: TestClient, db: Any) -> None:
        art = _create_test_artifact(db)
        _make_pack_owned(db, art["id"])
        resp = client.delete("/api/artifacts/@testns/skill/greet")
        assert resp.status_code == 403
        assert "pack-owned" in resp.json()["detail"]

    def test_delete_succeeds_for_non_pack(self, client: TestClient, db: Any) -> None:
        _create_test_artifact(db)
        resp = client.delete("/api/artifacts/@testns/skill/greet")
        assert resp.status_code == 200
        assert resp.json()["status"] == "deleted"
