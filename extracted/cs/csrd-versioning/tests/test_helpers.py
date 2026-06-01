"""Tests for csrd.versioning helpers: find_bearer, find_token."""

from contextvars import ContextVar

import pytest
from fastapi import HTTPException

from csrd.context._contextvars import (
    configure_headers_context_provider,
    reset_global_configuration,
    reset_headers_context,
    set_headers_context,
)
from csrd.versioning._helpers import find_bearer, find_token


@pytest.fixture(autouse=True)
def _setup_headers_provider():
    reset_global_configuration()
    cv: ContextVar[dict] = ContextVar("test_headers")
    cv.set({})
    configure_headers_context_provider(
        get_headers=cv.get,
        set_headers=cv.set,
        reset_headers=cv.reset,
    )
    yield
    reset_global_configuration()


class TestFindBearer:
    def test_authorization_header(self):
        token = set_headers_context({"authorization": "Bearer abc123"})
        try:
            assert find_bearer() == "Bearer abc123"
        finally:
            reset_headers_context(token)

    def test_missing_header_raises(self):
        token = set_headers_context({})
        try:
            with pytest.raises(HTTPException) as exc_info:
                find_bearer()
            assert exc_info.value.status_code == 401
        finally:
            reset_headers_context(token)

    def test_missing_header_optional(self):
        token = set_headers_context({})
        try:
            result = find_bearer(fail_on_missing=False)
            assert result is None
        finally:
            reset_headers_context(token)

    def test_explicit_headers_dict(self):
        result = find_bearer({"authorization": "Token xyz"})
        assert result == "Token xyz"

    def test_explicit_headers_callable(self):
        result = find_bearer(lambda: {"authorization": "Bearer func"})
        assert result == "Bearer func"


class TestFindToken:
    def test_bearer_prefix_stripped(self):
        token = set_headers_context({"authorization": "Bearer mytoken123"})
        try:
            assert find_token() == "mytoken123"
        finally:
            reset_headers_context(token)

    def test_raw_token_without_prefix(self):
        token = set_headers_context({"authorization": "raw-api-key"})
        try:
            assert find_token() == "raw-api-key"
        finally:
            reset_headers_context(token)

    def test_empty_bearer_raises(self):
        token = set_headers_context({"authorization": "Bearer "})
        try:
            with pytest.raises(HTTPException) as exc_info:
                find_token()
            assert exc_info.value.status_code == 401
        finally:
            reset_headers_context(token)

    def test_only_bearer_keyword_raises(self):
        token = set_headers_context({"authorization": "Bearer"})
        try:
            with pytest.raises(HTTPException) as exc_info:
                find_token()
            assert exc_info.value.status_code == 401
        finally:
            reset_headers_context(token)

    def test_no_auth_header_raises(self):
        token = set_headers_context({})
        try:
            with pytest.raises(HTTPException) as exc_info:
                find_token()
            assert exc_info.value.status_code == 401
        finally:
            reset_headers_context(token)
