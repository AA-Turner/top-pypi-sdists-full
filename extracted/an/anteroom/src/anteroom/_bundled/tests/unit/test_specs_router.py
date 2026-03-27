"""Unit tests for the specs API router."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""

UPDATED_SPEC_YAML = """\
requirements: |
  Must support widgets AND gadgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


@pytest.fixture()
def client(db: Any) -> TestClient:
    from anteroom.routers.specs import router

    app = FastAPI()
    app.include_router(router, prefix="/api")
    app.state.db = db
    return TestClient(app)


@pytest.fixture()
def spec_fqn(db: Any) -> str:
    from anteroom.services.spec_service import create_spec

    create_spec(db, "ns", "feat", VALID_SPEC_YAML)
    return "@ns/spec/feat"


# ---------------------------------------------------------------------------
# GET /api/specs
# ---------------------------------------------------------------------------


class TestListSpecs:
    def test_empty(self, client: TestClient) -> None:
        resp = client.get("/api/specs")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_with_specs(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.get("/api/specs")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["fqn"] == spec_fqn
        assert "content" not in data[0]


# ---------------------------------------------------------------------------
# POST /api/specs
# ---------------------------------------------------------------------------


class TestCreateSpec:
    def test_create_valid(self, client: TestClient) -> None:
        resp = client.post(
            "/api/specs",
            json={
                "namespace": "ns",
                "name": "new-spec",
                "content": VALID_SPEC_YAML,
            },
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["fqn"] == "@ns/spec/new-spec"
        assert data["type"] == "spec"

    def test_create_invalid_yaml(self, client: TestClient) -> None:
        resp = client.post(
            "/api/specs",
            json={
                "namespace": "ns",
                "name": "bad",
                "content": "not valid spec yaml",
            },
        )
        assert resp.status_code == 422

    def test_create_missing_fields(self, client: TestClient) -> None:
        resp = client.post("/api/specs", json={"namespace": "ns"})
        assert resp.status_code == 422

    def test_create_duplicate(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(
            "/api/specs",
            json={
                "namespace": "ns",
                "name": "feat",
                "content": VALID_SPEC_YAML,
            },
        )
        assert resp.status_code == 409


# ---------------------------------------------------------------------------
# GET /api/specs/{fqn}
# ---------------------------------------------------------------------------


class TestGetSpec:
    def test_found(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.get(f"/api/specs/{spec_fqn}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["fqn"] == spec_fqn
        assert "phase_info" in data
        assert data["phase_info"]["requirements"]["status"] == "draft"

    def test_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/specs/@ns/spec/nope")
        assert resp.status_code == 404

    def test_invalid_fqn(self, client: TestClient) -> None:
        resp = client.get("/api/specs/bad-fqn")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# POST /api/specs/{fqn}/phases/{phase}/approve
# ---------------------------------------------------------------------------


class TestApprovePhase:
    def test_approve(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(f"/api/specs/{spec_fqn}/phases/design/approve")
        assert resp.status_code == 200
        assert resp.json()["status"] == "approved"

    def test_approve_invalid_phase(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(f"/api/specs/{spec_fqn}/phases/invalid/approve")
        assert resp.status_code == 400

    def test_approve_not_found(self, client: TestClient) -> None:
        resp = client.post("/api/specs/@ns/spec/nope/phases/design/approve")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/specs/{fqn}/phases/{phase}/unapprove
# ---------------------------------------------------------------------------


class TestUnapprovePhase:
    def test_unapprove(self, client: TestClient, spec_fqn: str) -> None:
        client.post(f"/api/specs/{spec_fqn}/phases/design/approve")
        resp = client.post(f"/api/specs/{spec_fqn}/phases/design/unapprove")
        assert resp.status_code == 200
        assert resp.json()["status"] == "draft"

    def test_unapprove_invalid_phase(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(f"/api/specs/{spec_fqn}/phases/bad/unapprove")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/specs/{fqn}/diff
# ---------------------------------------------------------------------------


class TestSpecDiff:
    def test_diff_two_versions(self, client: TestClient, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import update_spec_content

        update_spec_content(db, spec_fqn, UPDATED_SPEC_YAML)
        resp = client.get(f"/api/specs/{spec_fqn}/diff")
        assert resp.status_code == 200
        data = resp.json()
        assert data["version_from"] == 1
        assert data["version_to"] == 2
        req_change = next(pc for pc in data["phase_changes"] if pc["phase"] == "requirements")
        assert req_change["content_changed"] is True

    def test_diff_single_version(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.get(f"/api/specs/{spec_fqn}/diff")
        assert resp.status_code == 422

    def test_diff_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/specs/@ns/spec/nope/diff")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/specs/{fqn}/stale
# ---------------------------------------------------------------------------


class TestSpecStale:
    def test_not_stale(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.get(f"/api/specs/{spec_fqn}/stale")
        assert resp.status_code == 200
        data = resp.json()
        assert data["phases"]["design"]["status"] == "draft"
        assert data["phases"]["design"]["reason"] is None

    def test_stale_after_update(self, client: TestClient, db: Any, spec_fqn: str) -> None:
        from anteroom.services.spec_service import approve_phase, update_spec_content

        approve_phase(db, spec_fqn, "design", "troy")
        update_spec_content(db, spec_fqn, UPDATED_SPEC_YAML)
        resp = client.get(f"/api/specs/{spec_fqn}/stale")
        assert resp.status_code == 200
        data = resp.json()
        assert data["phases"]["design"]["status"] == "stale"
        assert data["phases"]["design"]["reason"] is not None

    def test_stale_not_found(self, client: TestClient) -> None:
        resp = client.get("/api/specs/@ns/spec/nope/stale")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/specs/queue
# ---------------------------------------------------------------------------


class TestGetSpecQueue:
    def test_empty_queue(self, client: TestClient) -> None:
        resp = client.get("/api/specs/queue")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 0
        assert data["needs_review"] == []

    def test_queue_includes_draft_spec(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.get("/api/specs/queue")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] >= 1
        fqns = [item["fqn"] for item in data["needs_review"]]
        assert spec_fqn in fqns


# ---------------------------------------------------------------------------
# PATCH /api/specs/{fqn}
# ---------------------------------------------------------------------------


class TestPatchSpec:
    def test_patch_updates_content(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.patch(
            f"/api/specs/{spec_fqn}",
            json={"content_yaml": UPDATED_SPEC_YAML},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["updated"] is True

    def test_patch_nonexistent_spec(self, client: TestClient) -> None:
        resp = client.patch(
            "/api/specs/@ns/spec/nope",
            json={"content_yaml": VALID_SPEC_YAML},
        )
        assert resp.status_code == 404

    def test_patch_invalid_yaml(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.patch(
            f"/api/specs/{spec_fqn}",
            json={"content_yaml": "not: valid: spec: yaml"},
        )
        assert resp.status_code == 422

    def test_patch_missing_body(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.patch(f"/api/specs/{spec_fqn}", json={})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/specs/{fqn}/conformance
# ---------------------------------------------------------------------------


class TestConformanceEndpoint:
    def test_conformance_check(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(f"/api/specs/{spec_fqn}/conformance")
        assert resp.status_code == 200
        data = resp.json()
        assert data["spec_fqn"] == spec_fqn
        assert "conformant" in data
        assert "findings" in data

    def test_conformance_nonexistent(self, client: TestClient) -> None:
        resp = client.post("/api/specs/@ns/spec/nope/conformance")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET/POST/DELETE /api/specs/{fqn}/links
# ---------------------------------------------------------------------------


class TestLinksEndpoints:
    def test_list_links_empty(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.get(f"/api/specs/{spec_fqn}/links")
        assert resp.status_code == 200
        data = resp.json()
        assert data["links"] == []

    def test_create_branch_link(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(
            f"/api/specs/{spec_fqn}/links",
            json={"type": "branch", "ref": "feature-branch"},
        )
        assert resp.status_code == 201
        assert resp.json()["linked"] is True

    def test_create_pr_link(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(
            f"/api/specs/{spec_fqn}/links",
            json={"type": "pr", "ref": "42", "url": "https://github.com/org/repo/pull/42"},
        )
        assert resp.status_code == 201

    def test_create_link_invalid_type(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(
            f"/api/specs/{spec_fqn}/links",
            json={"type": "tag", "ref": "v1.0"},
        )
        assert resp.status_code == 422

    def test_create_link_missing_fields(self, client: TestClient, spec_fqn: str) -> None:
        resp = client.post(f"/api/specs/{spec_fqn}/links", json={"type": "branch"})
        assert resp.status_code == 422

    def test_delete_link(self, client: TestClient, spec_fqn: str) -> None:
        # Create a link first
        client.post(
            f"/api/specs/{spec_fqn}/links",
            json={"type": "branch", "ref": "feature-branch"},
        )
        # Get the link ID
        links_resp = client.get(f"/api/specs/{spec_fqn}/links")
        links = links_resp.json()["links"]
        assert len(links) >= 1
        link_id = links[0]["id"]
        # Delete it
        resp = client.delete(f"/api/specs/{spec_fqn}/links/{link_id}")
        assert resp.status_code == 200
        assert resp.json()["unlinked"] is True

    def test_list_links_after_create(self, client: TestClient, spec_fqn: str) -> None:
        client.post(
            f"/api/specs/{spec_fqn}/links",
            json={"type": "branch", "ref": "my-branch"},
        )
        resp = client.get(f"/api/specs/{spec_fqn}/links")
        links = resp.json()["links"]
        assert len(links) == 1
        assert links[0]["ref"] == "my-branch"
        assert links[0]["type"] == "branch"


# ---------------------------------------------------------------------------
# POST /api/specs (design-first creation_flow)
# ---------------------------------------------------------------------------


class TestCreateSpecDesignFirst:
    def test_create_with_creation_flow(self, client: TestClient) -> None:
        from anteroom.services.spec_schema import DESIGN_FIRST_TEMPLATE

        resp = client.post(
            "/api/specs",
            json={
                "namespace": "ns",
                "name": "df-test",
                "content": DESIGN_FIRST_TEMPLATE,
                "creation_flow": "design_first",
            },
        )
        assert resp.status_code == 201
