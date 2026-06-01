"""Tests for csrd.context contextvars system."""

import pytest

from csrd.context._contextvars import (
    configure_headers_context_provider,
    get_api_version,
    get_app_id,
    get_headers,
    get_hit_id,
    get_path_params,
    get_query_params,
    reset_api_version_context,
    reset_global_configuration,
    reset_headers_context,
    reset_path_params,
    reset_query_params,
    set_api_version_context,
    set_headers_context,
    set_path_params,
    set_query_params,
)
from csrd.context._models import PathValue


class TestPathParamsContext:
    def test_set_and_get(self):
        token = set_path_params(PathValue({"id": "42"}))
        try:
            params = get_path_params()
            assert params["id"] == "42"
            assert params.id == "42"
        finally:
            reset_path_params(token)

    def test_default_empty(self):
        params = get_path_params()
        assert len(params) == 0

    def test_reset(self):
        token = set_path_params(PathValue({"x": "y"}))
        reset_path_params(token)
        assert len(get_path_params()) == 0


class TestQueryParamsContext:
    def test_set_and_get(self):
        token = set_query_params(PathValue({"page": "2"}))
        try:
            params = get_query_params()
            assert params["page"] == "2"
        finally:
            reset_query_params(token)

    def test_default_empty(self):
        params = get_query_params()
        assert len(params) == 0


class TestApiVersionContext:
    def test_set_and_get(self):
        token = set_api_version_context("2025-06-20")
        try:
            assert get_api_version() == "2025-06-20"
        finally:
            reset_api_version_context(token)

    def test_default_none(self):
        assert get_api_version() is None


class TestHeadersContext:
    def setup_method(self):
        reset_global_configuration()

    def teardown_method(self):
        reset_global_configuration()

    def test_unconfigured_returns_empty_dict(self):
        headers = get_headers()
        assert headers == {}

    def test_configure_and_use(self):
        from contextvars import ContextVar

        cv: ContextVar[dict] = ContextVar("test_headers")
        cv.set({})

        configure_headers_context_provider(
            get_headers=cv.get,
            set_headers=cv.set,
            reset_headers=cv.reset,
        )
        token = set_headers_context({"x-client-app-id": "myapp", "x-client-hit-id": "hit123"})
        try:
            headers = get_headers()
            assert headers["x-client-app-id"] == "myapp"
            assert get_app_id() == "myapp"
            assert get_hit_id() == "hit123"
        finally:
            reset_headers_context(token)

    def test_set_headers_before_configure_raises(self):
        with pytest.raises(RuntimeError, match="not configured"):
            set_headers_context({"key": "val"})

    def test_reset_headers_none_token_is_noop(self):
        # Should not raise
        reset_headers_context(None)

    def test_get_app_id_unconfigured(self):
        assert get_app_id() is None

    def test_get_hit_id_unconfigured(self):
        assert get_hit_id() is None
