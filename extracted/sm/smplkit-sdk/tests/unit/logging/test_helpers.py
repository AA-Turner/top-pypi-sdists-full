"""Tests for logging client helper functions."""

from __future__ import annotations

import datetime
from http import HTTPStatus
from unittest.mock import MagicMock

import httpx
import pytest

from smplkit._errors import (
    ConflictError,
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
)
from smplkit._generated.logging.models.log_group_environments_type_0 import LogGroupEnvironmentsType0
from smplkit._generated.logging.models.logger_environments_type_0 import LoggerEnvironmentsType0
from smplkit._generated.logging.types import UNSET
from smplkit.logging.client import (
    AsyncSmplLogGroup,
    AsyncSmplLogger,
    SmplLogGroup,
    SmplLogger,
    _build_group_body,
    _build_logger_body,
    _check_response_status,
    _extract_datetime,
    _extract_environments,
    _extract_sources,
    _make_environments,
    _make_group_environments,
    _maybe_reraise_network_error,
    _unset_to_none,
)


class TestUnsetToNone:
    def test_none_stays_none(self):
        assert _unset_to_none(None) is None

    def test_unset_becomes_none(self):
        assert _unset_to_none(UNSET) is None

    def test_value_passes_through(self):
        assert _unset_to_none("hello") == "hello"


class TestExtractDatetime:
    def test_none(self):
        assert _extract_datetime(None) is None

    def test_unset(self):
        assert _extract_datetime(UNSET) is None

    def test_datetime(self):
        dt = datetime.datetime(2026, 1, 1)
        assert _extract_datetime(dt) is dt


class TestExtractEnvironments:
    def test_none(self):
        assert _extract_environments(None) == {}

    def test_unset(self):
        assert _extract_environments(UNSET) == {}

    def test_logger_environments_type(self):
        obj = LoggerEnvironmentsType0()
        obj.additional_properties = {"prod": {"level": "ERROR"}}
        assert _extract_environments(obj) == {"prod": {"level": "ERROR"}}

    def test_log_group_environments_type(self):
        obj = LogGroupEnvironmentsType0()
        obj.additional_properties = {"staging": {"level": "DEBUG"}}
        assert _extract_environments(obj) == {"staging": {"level": "DEBUG"}}

    def test_dict(self):
        assert _extract_environments({"prod": {"level": "WARN"}}) == {"prod": {"level": "WARN"}}

    def test_unknown_type(self):
        assert _extract_environments(42) == {}


class TestMakeEnvironments:
    def test_none(self):
        assert _make_environments(None) is None

    def test_dict(self):
        result = _make_environments({"prod": {"level": "ERROR"}})
        assert isinstance(result, LoggerEnvironmentsType0)
        assert result.additional_properties == {"prod": {"level": "ERROR"}}


class TestMakeGroupEnvironments:
    def test_none(self):
        assert _make_group_environments(None) is None

    def test_dict(self):
        result = _make_group_environments({"prod": {"level": "WARN"}})
        assert isinstance(result, LogGroupEnvironmentsType0)
        assert result.additional_properties == {"prod": {"level": "WARN"}}


class TestExtractSources:
    def test_none(self):
        assert _extract_sources(None) == []

    def test_unset(self):
        assert _extract_sources(UNSET) == []

    def test_list_with_additional_properties(self):
        item = MagicMock()
        item.additional_properties = {"service": "api", "first_observed": "2026-01-01"}
        result = _extract_sources([item])
        assert result == [{"service": "api", "first_observed": "2026-01-01"}]

    def test_list_with_dict(self):
        result = _extract_sources([{"service": "api"}])
        assert result == [{"service": "api"}]

    def test_not_list(self):
        assert _extract_sources(42) == []


class TestCheckResponseStatus:
    def test_404(self):
        with pytest.raises(NotFoundError):
            _check_response_status(HTTPStatus.NOT_FOUND, b"not found")

    def test_409(self):
        with pytest.raises(ConflictError):
            _check_response_status(HTTPStatus.CONFLICT, b"conflict")

    def test_422(self):
        with pytest.raises(ValidationError):
            _check_response_status(HTTPStatus.UNPROCESSABLE_ENTITY, b"bad data")

    def test_200_ok(self):
        _check_response_status(HTTPStatus.OK, b"")

    def test_201_created(self):
        _check_response_status(HTTPStatus.CREATED, b"")


class TestMaybeReraiseNetworkError:
    def test_timeout(self):
        with pytest.raises(TimeoutError):
            _maybe_reraise_network_error(httpx.ReadTimeout("timed out"))

    def test_timeout_includes_url_when_available(self):
        exc = httpx.ReadTimeout("timed out")
        exc.request = httpx.Request("GET", "http://logging.localhost/api/v1/loggers")
        with pytest.raises(TimeoutError, match="http://logging.localhost/api/v1/loggers"):
            _maybe_reraise_network_error(exc)

    def test_http_error(self):
        with pytest.raises(ConnectionError):
            _maybe_reraise_network_error(httpx.ConnectError("refused"))

    def test_http_error_includes_url_when_available(self):
        exc = httpx.ConnectError("nodename nor servname provided, or not known")
        exc.request = httpx.Request("GET", "http://logging.localhost/api/v1/loggers")
        with pytest.raises(ConnectionError, match="http://logging.localhost/api/v1/loggers"):
            _maybe_reraise_network_error(exc)

    def test_http_error_fallback_message_without_url(self):
        exc = httpx.ConnectError("nodename nor servname provided, or not known")
        with pytest.raises(ConnectionError, match="Connection error"):
            _maybe_reraise_network_error(exc)

    def test_connection_error_uses_base_url_when_request_not_attached(self):
        exc = httpx.ConnectError("nodename nor servname provided, or not known")
        with pytest.raises(ConnectionError, match="http://logging.localhost"):
            _maybe_reraise_network_error(exc, "http://logging.localhost")

    def test_timeout_uses_base_url_when_request_not_attached(self):
        exc = httpx.ReadTimeout("timed out")
        with pytest.raises(TimeoutError, match="http://logging.localhost"):
            _maybe_reraise_network_error(exc, "http://logging.localhost")

    def test_exc_url_takes_precedence_over_base_url(self):
        exc = httpx.ConnectError("refused")
        exc.request = httpx.Request("GET", "http://logging.localhost/api/v1/loggers")
        with pytest.raises(ConnectionError, match="http://logging.localhost/api/v1/loggers"):
            _maybe_reraise_network_error(exc, "http://other.host")

    def test_not_found_error(self):
        with pytest.raises(NotFoundError):
            _maybe_reraise_network_error(NotFoundError("nope"))

    def test_conflict_error(self):
        with pytest.raises(ConflictError):
            _maybe_reraise_network_error(ConflictError("conflict"))

    def test_validation_error(self):
        with pytest.raises(ValidationError):
            _maybe_reraise_network_error(ValidationError("bad"))

    def test_other_error_passes_through(self):
        # Should not raise; caller raises separately
        _maybe_reraise_network_error(ValueError("unrelated"))


class TestBuildLoggerBody:
    def test_basic(self):
        body = _build_logger_body(name="SQL Logger")
        assert body.data.attributes.name == "SQL Logger"

    def test_with_environments(self):
        body = _build_logger_body(name="Test", environments={"prod": {"level": "ERROR"}})
        assert body.data.attributes.environments is not None

    def test_with_logger_id(self):
        body = _build_logger_body(logger_id="abc-123", name="Test")
        assert body.data.id == "abc-123"

    def test_without_logger_id(self):
        body = _build_logger_body(name="Test")
        assert body.data.id is None


class TestBuildGroupBody:
    def test_basic(self):
        body = _build_group_body(name="DB Loggers")
        assert body.data.attributes.name == "DB Loggers"

    def test_with_group_id(self):
        body = _build_group_body(group_id="grp-1", name="DB")
        assert body.data.id == "grp-1"

    def test_without_group_id(self):
        body = _build_group_body(name="DB")
        assert body.data.id is None


class TestSmplLoggerRepr:
    def test_repr(self):
        lg = SmplLogger(None, id="sql", name="SQL Logger")
        assert "sql" in repr(lg)

    def test_repr_none_id(self):
        lg = SmplLogger(None, id=None, name="SQL Logger")
        assert "None" in repr(lg)


class TestSmplLogGroupRepr:
    def test_repr(self):
        grp = SmplLogGroup(None, id="db", name="DB Loggers")
        assert "db" in repr(grp)

    def test_repr_none_id(self):
        grp = SmplLogGroup(None, id=None, name="DB Loggers")
        assert "None" in repr(grp)


class TestAsyncSmplLoggerRepr:
    def test_repr(self):
        lg = AsyncSmplLogger(None, id="sql", name="SQL Logger")
        assert "sql" in repr(lg)


class TestAsyncSmplLogGroupRepr:
    def test_repr(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB Loggers")
        assert "db" in repr(grp)


# ===================================================================
# delete() — active-record style for logger / log group
# ===================================================================


class TestSmplLoggerDelete:
    def test_calls_client_delete(self):
        client = MagicMock()
        lg = SmplLogger(client, id="sql", name="SQL")
        lg.delete()
        client.delete.assert_called_once_with("sql")

    def test_without_client_raises(self):
        lg = SmplLogger(None, id="sql", name="SQL")
        with pytest.raises(RuntimeError, match="cannot delete"):
            lg.delete()


class TestSmplLogGroupDelete:
    def test_calls_client_delete(self):
        client = MagicMock()
        grp = SmplLogGroup(client, id="db", name="DB")
        grp.delete()
        client.delete.assert_called_once_with("db")

    def test_without_client_raises(self):
        grp = SmplLogGroup(None, id="db", name="DB")
        with pytest.raises(RuntimeError, match="cannot delete"):
            grp.delete()


class TestAsyncSmplLoggerDelete:
    def test_calls_client_delete(self):
        import asyncio
        from unittest.mock import AsyncMock

        client = MagicMock()
        client.delete = AsyncMock()
        lg = AsyncSmplLogger(client, id="sql", name="SQL")
        asyncio.run(lg.delete())
        client.delete.assert_called_once_with("sql")

    def test_without_client_raises(self):
        import asyncio

        lg = AsyncSmplLogger(None, id="sql", name="SQL")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await lg.delete()

        asyncio.run(_run())


class TestAsyncSmplLogGroupDelete:
    def test_calls_client_delete(self):
        import asyncio
        from unittest.mock import AsyncMock

        client = MagicMock()
        client.delete = AsyncMock()
        grp = AsyncSmplLogGroup(client, id="db", name="DB")
        asyncio.run(grp.delete())
        client.delete.assert_called_once_with("db")

    def test_without_client_raises(self):
        import asyncio

        grp = AsyncSmplLogGroup(None, id="db", name="DB")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await grp.delete()

        asyncio.run(_run())
