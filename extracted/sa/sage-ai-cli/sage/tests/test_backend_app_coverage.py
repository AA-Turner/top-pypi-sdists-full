"""Coverage tests for backend.app — pure helpers + open endpoints.

We exercise:
  - bearer token extraction
  - path parameter validators
  - the open endpoints (/health, /models, /models/names, /hardware)
  - error paths for invalid IDs

Auth-gated endpoints (/chat, /models/download, /billing/*) need a real Firebase
identity, which mocking-to-test is mock-of-mock work — they're covered by
test_critical_integrity_fixes already.
"""

from __future__ import annotations

import os
import pytest


# Set required env BEFORE importing backend.app
os.environ.setdefault("SAGE_FIREBASE_API_KEY", "test-dummy")
os.environ.setdefault("FIREBASE_PROJECT_ID", "test-project")


from backend.app import (
    _extract_bearer_token,
    validate_model_id_path,
    validate_conversation_id_path,
    validate_model_name_path,
    app,
    ValidationError,  # defined inside app.py
)


# ── _extract_bearer_token ────────────────────────────────────────────────────


class TestExtractBearerToken:

    def test_missing_header_returns_none(self):
        assert _extract_bearer_token(None) is None

    def test_empty_string_returns_none(self):
        assert _extract_bearer_token("") is None

    def test_valid_bearer_token(self):
        assert _extract_bearer_token("Bearer abc123") == "abc123"

    def test_case_insensitive_scheme(self):
        assert _extract_bearer_token("bearer abc123") == "abc123"
        assert _extract_bearer_token("BEARER abc123") == "abc123"

    def test_non_bearer_scheme_returns_none(self):
        assert _extract_bearer_token("Basic abc123") is None

    def test_bearer_without_token_returns_none(self):
        assert _extract_bearer_token("Bearer") is None
        assert _extract_bearer_token("Bearer ") is None


# ── path validators ──────────────────────────────────────────────────────────


class TestValidateModelIdPath:

    def test_valid_id_passes(self):
        assert validate_model_id_path("qwen2.5-coder-7b") == "qwen2.5-coder-7b"

    def test_path_traversal_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_id_path("../etc/passwd")

    def test_empty_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_id_path("")

    def test_special_chars_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_id_path("foo;rm -rf /")


class TestValidateConversationIdPath:

    def test_uuid_like_passes(self):
        assert validate_conversation_id_path("conv-abc123") == "conv-abc123"

    def test_path_traversal_rejected(self):
        with pytest.raises(ValidationError):
            validate_conversation_id_path("../../secret")

    def test_empty_rejected(self):
        with pytest.raises(ValidationError):
            validate_conversation_id_path("")


class TestValidateModelNamePath:

    def test_simple_name_passes(self):
        assert validate_model_name_path("llama3.2") == "llama3.2"

    def test_empty_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_name_path("")

    def test_whitespace_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_name_path("   ")

    def test_path_traversal_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_name_path("../foo")

    def test_forward_slash_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_name_path("a/b")

    def test_backslash_rejected(self):
        with pytest.raises(ValidationError):
            validate_model_name_path("a\\b")


# ── Open (no-auth) endpoints via TestClient ──────────────────────────────────


@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)


class TestOpenEndpoints:

    def test_health_returns_ok(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is True
        assert "version" in body
        # loaded_model_id is None when nothing's loaded yet — that's still OK
        assert "loaded_model_id" in body

    def test_hardware_returns_summary(self, client):
        r = client.get("/hardware")
        assert r.status_code == 200
        body = r.json()
        # detect_hardware_summary returns os, cpu, ram, gpu info
        assert isinstance(body, dict)

    def test_models_list_returns_array(self, client):
        r = client.get("/models")
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is True
        assert isinstance(body["models"], list)

    def test_models_names_returns_sorted(self, client):
        r = client.get("/models/names")
        assert r.status_code == 200
        body = r.json()
        assert body["ok"] is True
        assert isinstance(body["names"], list)
        assert body["names"] == sorted(body["names"])

    def test_get_model_with_invalid_id_returns_422(self, client):
        r = client.get("/models/..%2F..%2Fetc")  # path-traversal attempt
        # FastAPI rejects the encoded form OR the validator catches it
        assert r.status_code in (400, 404, 422)

    def test_get_unknown_model_returns_404(self, client):
        r = client.get("/models/totally-not-a-real-model-xyz")
        assert r.status_code == 404


class TestAppShape:
    """Sanity checks on the FastAPI app — middleware + routes registered."""

    def test_app_has_health_route(self):
        paths = {r.path for r in app.routes if hasattr(r, "path")}
        assert "/health" in paths
        assert "/models" in paths
        assert "/chat" in paths

    def test_app_has_request_id_middleware(self, client):
        """The add_request_id middleware must attach X-Request-ID to every response."""
        r = client.get("/health")
        # Header should exist (its value is a UUID-ish string)
        assert r.headers.get("x-request-id") or r.headers.get("X-Request-ID")
