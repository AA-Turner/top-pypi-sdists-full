"""Tests for csrd.service — errors, BaseService, and exception handler."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from csrd.service import (
    AuthorizationError,
    BaseService,
    ConflictError,
    DownstreamError,
    NotFoundError,
    ServiceError,
    ValidationError,
    service_exception_handler,
)

# ── Domain Errors ────────────────────────────────────────────────────────


class TestServiceError:
    def test_default_message(self):
        err = ServiceError()
        assert str(err) == "Internal service error"
        assert err.status_code == 500

    def test_custom_message(self):
        err = ServiceError("boom", detail="something broke", code="ERR_001")
        assert err.message == "boom"
        assert err.detail == "something broke"
        assert err.code == "ERR_001"

    def test_status_code_override(self):
        err = ServiceError("custom", status_code=418)
        assert err.status_code == 418

    def test_is_exception(self):
        with pytest.raises(ServiceError):
            raise ServiceError("test")


class TestNotFoundError:
    def test_defaults(self):
        err = NotFoundError()
        assert err.status_code == 404
        assert err.message == "Resource not found"

    def test_custom(self):
        err = NotFoundError("Order not found", detail="order_id=42", code="ORDER_MISSING")
        assert err.status_code == 404
        assert err.message == "Order not found"
        assert err.detail == "order_id=42"
        assert err.code == "ORDER_MISSING"

    def test_is_service_error(self):
        assert isinstance(NotFoundError(), ServiceError)


class TestConflictError:
    def test_defaults(self):
        err = ConflictError()
        assert err.status_code == 409
        assert err.message == "Conflict"


class TestValidationError:
    def test_defaults(self):
        err = ValidationError()
        assert err.status_code == 422
        assert err.message == "Validation failed"


class TestAuthorizationError:
    def test_defaults(self):
        err = AuthorizationError()
        assert err.status_code == 403
        assert err.message == "Forbidden"


class TestDownstreamError:
    def test_defaults(self):
        err = DownstreamError()
        assert err.status_code == 502
        assert err.message == "Downstream service error"

    def test_with_cause(self):
        cause = ValueError("connection refused")
        err = DownstreamError("Payment service down", cause=cause)
        assert err.__cause__ is cause

    def test_subclass_hierarchy(self):
        """All errors should be catchable as ServiceError."""
        for cls in (
            NotFoundError,
            ConflictError,
            ValidationError,
            AuthorizationError,
            DownstreamError,
        ):
            assert issubclass(cls, ServiceError)


# ── BaseService ──────────────────────────────────────────────────────────


class TestBaseService:
    def test_current_user_none_outside_request(self):
        svc = BaseService()
        assert svc.current_user() is None

    def test_current_request_id_none_outside_request(self):
        svc = BaseService()
        assert svc.current_request_id() is None


# ── Exception Handler ────────────────────────────────────────────────────


class TestServiceExceptionHandler:
    def _make_app(self) -> FastAPI:
        app = FastAPI()
        app.add_exception_handler(Exception, service_exception_handler)

        @app.get("/not-found")
        async def _not_found():
            raise NotFoundError("User not found", detail="id=99", code="USER_MISSING")

        @app.get("/conflict")
        async def _conflict():
            raise ConflictError("Duplicate email")

        @app.get("/forbidden")
        async def _forbidden():
            raise AuthorizationError()

        @app.get("/downstream")
        async def _downstream():
            raise DownstreamError("Payments unavailable", status_code=503)

        @app.get("/bare")
        async def _bare():
            raise ServiceError()

        @app.get("/boom")
        async def _boom():
            raise AttributeError("unexpected")

        return app

    def test_not_found_response(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/not-found")
        assert resp.status_code == 404
        body = resp.json()
        assert body["meta"]["status"] == 404
        assert body["meta"]["error"] == "User not found"
        assert body["errors"][0]["detail"] == "id=99"
        assert body["errors"][0]["code"] == "USER_MISSING"

    def test_conflict_response(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/conflict")
        assert resp.status_code == 409
        assert resp.json()["meta"]["error"] == "Duplicate email"

    def test_forbidden_response(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/forbidden")
        assert resp.status_code == 403

    def test_downstream_with_custom_status(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/downstream")
        assert resp.status_code == 503

    def test_bare_service_error(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/bare")
        assert resp.status_code == 500
        body = resp.json()
        assert body["meta"]["error"] == "Internal service error"
        # No detail/code → errors list should be empty
        assert body["errors"] == []

    def test_response_has_camel_case_keys(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/not-found")
        body = resp.json()
        # meta fields should be camelCase
        assert "requestId" in body["meta"]
        assert "apiVersion" in body["meta"]

    def test_response_has_method_and_path(self):
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/not-found")
        meta = resp.json()["meta"]
        assert meta["method"] == "GET"
        assert meta["path"] == "/not-found"

    def test_unhandled_exception_is_json_500(self, caplog: pytest.LogCaptureFixture):
        caplog.set_level("ERROR", logger="csrd.service")
        client = TestClient(self._make_app(), raise_server_exceptions=False)
        resp = client.get("/boom")
        assert resp.status_code == 500
        assert resp.headers["content-type"].startswith("application/json")
        body = resp.json()
        assert body["meta"]["status"] == 500
        assert body["meta"]["error"] == "Internal Server Error"
        assert body["meta"]["method"] == "GET"
        assert body["meta"]["path"] == "/boom"
        assert body["errors"] == []
        assert "AttributeError: unexpected" in caplog.text
