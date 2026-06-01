"""Tests for docs module: OpenAPI generation, Swagger UI, version labels."""

from enum import Enum

import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from csrd.versioning._docs import (
    _build_version_openapi_schema,
    _build_version_options,
    _deduplicate_operation_ids,
    _extract_path_param_order,
    _normalized_version_labels,
    _sort_openapi_path_params_inplace,
)
from csrd.versioning._swagger_ui_version import SWAGGER_UI_VERSION


class Versions(Enum):
    Unversioned = "Unversioned"
    V1 = "2024-01-01"
    V2 = "2025-06-20"
    Alpha = "alpha"


# ── _build_version_options ───────────────────────────────────────────────


class TestBuildVersionOptions:
    def test_basic_options(self):
        html = _build_version_options(["Unversioned", "2025-06-20"])
        assert "<option" in html
        assert "Unversioned" in html
        assert "2025-06-20" in html

    def test_html_escapes(self):
        html = _build_version_options(['<script>alert("xss")</script>'])
        assert "<script>" not in html
        assert "&lt;script&gt;" in html


# ── _extract_path_param_order ────────────────────────────────────────────


class TestExtractPathParamOrder:
    def test_basic(self):
        order = _extract_path_param_order("/items/{item_id}/sub/{sub_id}")
        assert order == {"item_id": 0, "sub_id": 1}

    def test_no_params(self):
        assert _extract_path_param_order("/items") == {}


# ── _sort_openapi_path_params_inplace ────────────────────────────────────


class TestSortOpenAPIParams:
    def test_path_params_before_query(self):
        schema = {
            "paths": {
                "/items/{item_id}": {
                    "get": {
                        "parameters": [
                            {"name": "q", "in": "query"},
                            {"name": "item_id", "in": "path"},
                        ]
                    }
                }
            }
        }
        _sort_openapi_path_params_inplace(schema)
        params = schema["paths"]["/items/{item_id}"]["get"]["parameters"]
        assert params[0]["name"] == "item_id"
        assert params[1]["name"] == "q"


# ── _deduplicate_operation_ids ───────────────────────────────────────────


class TestDeduplicateOperationIds:
    def test_no_duplicates_unchanged(self):
        app = FastAPI()

        @app.get("/a", operation_id="op_a")
        async def a():
            pass

        @app.get("/b", operation_id="op_b")
        async def b():
            pass

        _deduplicate_operation_ids(app)
        from fastapi.routing import APIRoute

        ops = {r.operation_id for r in app.routes if isinstance(r, APIRoute)}
        assert ops == {"op_a", "op_b"}

    def test_duplicates_get_suffix(self):
        app = FastAPI()

        @app.get("/a")
        async def handler():
            pass

        @app.get("/b")
        async def handler():  # noqa: F811
            pass

        _deduplicate_operation_ids(app)
        from fastapi.routing import APIRoute

        ops = [r.operation_id for r in app.routes if isinstance(r, APIRoute)]
        assert len(set(ops)) == 2  # all unique


# ── _normalized_version_labels ───────────────────────────────────────────


class TestNormalizedVersionLabels:
    def test_unversioned_first(self):
        labels = _normalized_version_labels(
            {Versions.V1: FastAPI(), Versions.Unversioned: FastAPI()}
        )
        assert labels[0] == "Unversioned"

    def test_alpha_before_numeric(self):
        labels = _normalized_version_labels(
            {Versions.Alpha: FastAPI(), Versions.V1: FastAPI(), Versions.V2: FastAPI()}
        )
        alpha_idx = labels.index("alpha")
        v1_idx = labels.index("2024-01-01")
        assert alpha_idx < v1_idx

    def test_numeric_sorted(self):
        labels = _normalized_version_labels({Versions.V2: FastAPI(), Versions.V1: FastAPI()})
        assert labels.index("2024-01-01") < labels.index("2025-06-20")


# ── _build_version_openapi_schema ────────────────────────────────────────


class TestBuildVersionOpenAPISchema:
    def test_schema_has_version_info(self):
        app = FastAPI(title="Test")

        @app.get("/api/items")
        async def items():
            return []

        schema = _build_version_openapi_schema(app, prefix="api", version_key=Versions.V1)
        assert schema["info"]["version"] == "2024-01-01"

    def test_paths_prefixed(self):
        app = FastAPI(title="Test")

        @app.get("/items")
        async def items():
            return []

        schema = _build_version_openapi_schema(app, prefix="api", version_key=Versions.V1)
        assert any(p.startswith("/api") for p in schema["paths"])


# ── Integration: Swagger UI routes ───────────────────────────────────────


class TestSwaggerUIRoutes:
    @pytest.fixture
    def app(self):
        from csrd.versioning import compose_versioned_apps
        from csrd.versioning._config import VersionedApiConfig, VersionedAppComposeConfig

        unv = FastAPI()

        @unv.get("/api/test")
        async def test_endpoint():
            return {"ok": True}

        return compose_versioned_apps(
            {Versions.Unversioned: unv},
            config=VersionedAppComposeConfig(
                api=VersionedApiConfig(prefix="api", include_actuator_endpoints=False)
            ),
        )

    @pytest.fixture
    def client(self, app):
        return TestClient(app, raise_server_exceptions=False)

    def test_swagger_ui_html(self, client):
        r = client.get("/swagger-ui/index.html")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        # Verify the pinned Swagger UI version is embedded — catches broken upgrades
        assert SWAGGER_UI_VERSION in r.text, (
            f"Expected Swagger UI version {SWAGGER_UI_VERSION!r} in rendered HTML. "
            "Run `just swagger-ui <version>` to update the pinned version and SRI hashes."
        )
        # Verify SRI hashes are present — catches incomplete update_swagger_ui.py runs
        assert 'integrity="sha384-' in r.text
        # Standalone preset is required for StandaloneLayout wiring
        assert "swagger-ui-standalone-preset.js" in r.text
        # Ensure all templated SRI placeholders are fully rendered
        assert "__SRI_STANDALONE_JS__" not in r.text

    def test_openapi_json(self, client):
        r = client.get("/openapi/unversioned.json")
        assert r.status_code == 200
        schema = r.json()
        assert "paths" in schema

    def test_info_endpoint(self, client):
        r = client.get("/_info")
        assert r.status_code == 200
        data = r.json()
        assert "versions" in data
        assert "prefix" in data

    def test_favicon(self, client):
        r = client.get("/swagger-ui/favicon.png")
        assert r.status_code == 200
        assert r.headers["content-type"] == "image/png"

    def test_root_favicon_alias(self, client):
        r = client.get("/favicon.ico")
        assert r.status_code == 200

    def test_redoc_default_version(self, client):
        r = client.get("/redoc")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert "redoc" in r.text.lower()
        assert "/openapi/" in r.text

    def test_redoc_with_version_param(self, client):
        r = client.get("/redoc?version=unversioned")
        assert r.status_code == 200
        assert "/openapi/unversioned.json" in r.text
