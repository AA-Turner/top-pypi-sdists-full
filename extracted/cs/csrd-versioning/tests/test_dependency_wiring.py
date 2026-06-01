"""Tests for dependency wiring."""

import contextlib

import pytest
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
from fastapi.security import HTTPBearer

from csrd.versioning._dependency_wiring import (
    PathParamParser,
    _build_normalized_dependency_specs,
    _documented_error_statuses_from_handlers,
    _get_route_param_names,
    _has_dependency,
    _remove_bearer_dependencies,
    _route_bearer_guard_opt_out,
    _status_description,
    _strip_prefix_from_versioned_routes,
)

# ── _status_description ─────────────────────────────────────────────────


class TestStatusDescription:
    def test_known_status(self):
        assert _status_description(200) == "OK"
        assert _status_description(404) == "Not Found"
        assert _status_description(500) == "Internal Server Error"

    def test_unknown_status(self):
        assert _status_description(999) == "HTTP 999"


# ── _get_route_param_names ───────────────────────────────────────────────


class TestGetRouteParamNames:
    def test_simple_params(self):
        route = APIRoute("/items/{item_id}", endpoint=lambda: None)
        assert _get_route_param_names(route) == {"item_id"}

    def test_typed_params(self):
        route = APIRoute("/items/{item_id:int}/sub/{sub_id:str}", endpoint=lambda: None)
        assert _get_route_param_names(route) == {"item_id", "sub_id"}

    def test_no_params(self):
        route = APIRoute("/items", endpoint=lambda: None)
        assert _get_route_param_names(route) == set()


# ── _documented_error_statuses_from_handlers ─────────────────────────────


class TestDocumentedErrorStatuses:
    def test_extracts_int_keys(self):
        handlers = {400: None, 404: None, ValueError: None}
        result = _documented_error_statuses_from_handlers(handlers)
        assert 400 in result
        assert 404 in result
        assert 401 in result  # always included
        assert 403 in result  # always included

    def test_empty_still_includes_auth(self):
        result = _documented_error_statuses_from_handlers({})
        assert result == {401, 403}


# ── _route_bearer_guard_opt_out ──────────────────────────────────────────


class TestBearerGuardOptOut:
    def test_no_extra(self):
        route = APIRoute("/test", endpoint=lambda: None)
        assert _route_bearer_guard_opt_out(route) is False

    def test_opt_out_true(self):
        route = APIRoute("/test", endpoint=lambda: None, openapi_extra={"x-bearer-guard": False})
        assert _route_bearer_guard_opt_out(route) is True

    def test_opt_in_explicitly(self):
        route = APIRoute("/test", endpoint=lambda: None, openapi_extra={"x-bearer-guard": True})
        assert _route_bearer_guard_opt_out(route) is False


# ── _remove_bearer_dependencies ──────────────────────────────────────────


class TestRemoveBearerDependencies:
    def test_removes_http_bearer(self):
        bearer_dep = Depends(HTTPBearer())
        other_dep = Depends(lambda: None)
        filtered, removed = _remove_bearer_dependencies([bearer_dep, other_dep])
        assert len(filtered) == 1
        assert removed is True

    def test_no_bearer_present(self):
        dep = Depends(lambda: None)
        filtered, removed = _remove_bearer_dependencies([dep])
        assert len(filtered) == 1
        assert removed is False


# ── _has_dependency ──────────────────────────────────────────────────────


class TestHasDependency:
    def test_found(self):
        fn = lambda: None  # noqa: E731
        deps = [Depends(fn)]
        assert _has_dependency(deps, fn) is True

    def test_not_found(self):
        deps = [Depends(lambda: None)]
        assert _has_dependency(deps, lambda: None) is False


# ── _strip_prefix_from_versioned_routes ──────────────────────────────────


class TestStripPrefix:
    def test_strips_prefix(self):
        app = FastAPI()

        @app.get("/api/items")
        async def items():
            pass

        _strip_prefix_from_versioned_routes(app, "api")
        api_route = next(r for r in app.routes if isinstance(r, APIRoute))
        assert api_route.path == "/items"

    def test_root_prefix_noop(self):
        app = FastAPI()

        @app.get("/items")
        async def items():
            pass

        _strip_prefix_from_versioned_routes(app, "/")
        api_route = next(r for r in app.routes if isinstance(r, APIRoute))
        assert api_route.path == "/items"

    def test_exact_prefix_becomes_root(self):
        app = FastAPI()

        @app.get("/api")
        async def root():
            pass

        _strip_prefix_from_versioned_routes(app, "api")
        api_route = next(r for r in app.routes if isinstance(r, APIRoute))
        assert api_route.path == "/"


# ── _build_normalized_dependency_specs ───────────────────────────────────


class TestBuildNormalizedDependencySpecs:
    def test_none_returns_empty(self):
        assert _build_normalized_dependency_specs(None) == []


# ── PathParamParser ──────────────────────────────────────────────────────


class TestPathParamParser:
    @pytest.mark.asyncio
    async def test_sets_and_resets_context(self):
        from unittest.mock import MagicMock

        from csrd.context import get_path_params

        parser = PathParamParser()
        mock_request = MagicMock()
        mock_request.path_params = {"id": "123"}
        mock_request.query_params = {"q": "search"}

        gen = parser(mock_request)
        await gen.__anext__()

        path_params = get_path_params()
        assert path_params is not None

        with contextlib.suppress(StopAsyncIteration):
            await gen.__anext__()
