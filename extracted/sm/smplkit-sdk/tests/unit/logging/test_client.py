"""Tests for LoggingClient (sync) management API, runtime, and integration."""

from __future__ import annotations

import logging as stdlib_logging
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest

from smplkit import LogLevel
from smplkit._errors import NotFoundError, ValidationError
from smplkit._buffer import _LoggerRegistrationBuffer
from smplkit.logging._client import (
    LoggingClient,
    SmplLogGroup,
    SmplLogger,
    _check_response_status,
)

_TEST_UUID = "550e8400-e29b-41d4-a716-446655440000"


def _new_mgmt():
    """Build the logging client for management-flavored tests.

    The logger / log-group CRUD sub-clients now live on ``client.logging``
    (``client.logging.loggers`` / ``client.logging.log_groups``), so this
    returns the logging client; ``.loggers`` / ``.log_groups`` resolve there.
    """
    from smplkit import SmplClient

    return SmplClient(api_key="sk_test", base_domain="example.test").logging


def _new_async_mgmt():
    """Build the async logging client for management-flavored tests."""
    from smplkit import AsyncSmplClient

    return AsyncSmplClient(api_key="sk_test", base_domain="example.test").logging


def _make_logger_attrs(*, name="SQL Logger", level="DEBUG", group=None, managed=True):
    """Build mock logger attributes."""
    from smplkit._generated.logging.types import UNSET

    attrs = MagicMock()
    attrs.name = name
    attrs.level = level
    attrs.group = group if group is not None else UNSET
    attrs.managed = managed
    attrs.sources = UNSET
    attrs.environments = UNSET
    attrs.created_at = UNSET
    attrs.updated_at = UNSET
    return attrs


def _make_group_attrs(*, name="DB Loggers", level="WARN", parent_id=None):
    """Build mock log group attributes."""
    from smplkit._generated.logging.types import UNSET

    attrs = MagicMock()
    attrs.name = name
    attrs.level = level
    attrs.parent_id = parent_id if parent_id is not None else UNSET
    attrs.environments = UNSET
    attrs.created_at = UNSET
    attrs.updated_at = UNSET
    return attrs


def _make_resource(attrs, id=_TEST_UUID):
    resource = MagicMock()
    resource.id = id
    resource.attributes = attrs
    return resource


def _make_parsed(resource):
    parsed = MagicMock()
    parsed.data = resource
    return parsed


def _make_list_parsed(resources):
    parsed = MagicMock()
    parsed.data = resources
    return parsed


def _ok_response(parsed=None, status=HTTPStatus.OK):
    resp = MagicMock()
    resp.status_code = status
    resp.content = b""
    resp.parsed = parsed
    return resp


def _make_logging_client(**kwargs):
    """Create a wired LoggingClient with a mocked parent + injected transport.

    The fused client owns its own ``loggers`` / ``log_groups`` sub-clients
    (sharing one discovery buffer); no management delegation.
    """
    parent = MagicMock()
    parent._api_key = "sk_test"
    parent._environment = "test"
    parent._service = kwargs.get("service", None)
    transport = MagicMock()
    transport._base_url = "http://logging:8003"
    client = LoggingClient(parent=parent, transport=transport, metrics=parent._metrics)
    return client


# ---------------------------------------------------------------------------
# new() — factory for unsaved loggers
# ---------------------------------------------------------------------------


class TestNew:
    def test_new_returns_unsaved_logger(self):
        mgmt = _new_mgmt()
        lg = mgmt.loggers.new("sql")
        assert isinstance(lg, SmplLogger)
        assert lg.id == "sql"
        assert lg.managed is True

    def test_new_name_equals_id(self):
        mgmt = _new_mgmt()
        lg = mgmt.loggers.new("sqlalchemy.engine")
        assert lg.name == "sqlalchemy.engine"

    def test_new_with_unmanaged(self):
        mgmt = _new_mgmt()
        lg = mgmt.loggers.new("sql", managed=False)
        assert lg.managed is False


# ---------------------------------------------------------------------------
# new_group() — factory for unsaved log groups
# ---------------------------------------------------------------------------


class TestNewGroup:
    def test_new_group_returns_unsaved(self):
        mgmt = _new_mgmt()
        grp = mgmt.log_groups.new("db-loggers")
        assert isinstance(grp, SmplLogGroup)
        assert grp.id == "db-loggers"

    def test_new_group_with_name(self):
        mgmt = _new_mgmt()
        grp = mgmt.log_groups.new("db-loggers", name="DB Loggers")
        assert grp.name == "DB Loggers"

    def test_new_group_auto_generates_name(self):
        mgmt = _new_mgmt()
        grp = mgmt.log_groups.new("db-loggers")
        assert grp.name == "Db Loggers"

    def test_new_group_with_parent_group(self):
        mgmt = _new_mgmt()
        grp = mgmt.log_groups.new("child", group="parent-id")
        assert grp.group == "parent-id"


# ---------------------------------------------------------------------------
# list()
# ---------------------------------------------------------------------------


class TestList:
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_list(self, mock_list):
        attrs = _make_logger_attrs()
        resource = _make_resource(attrs)
        mock_list.return_value = _ok_response(_make_list_parsed([resource]))

        mgmt = _new_mgmt()
        result = mgmt.loggers.list()
        assert len(result) == 1
        assert isinstance(result[0], SmplLogger)

    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_list_empty_parsed(self, mock_list):
        mock_list.return_value = _ok_response(None)
        mgmt = _new_mgmt()
        result = mgmt.loggers.list()
        assert result == []


# ---------------------------------------------------------------------------
# get(id) — direct lookup via get_logger
# ---------------------------------------------------------------------------


class TestGet:
    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_get_by_id(self, mock_get):
        attrs = _make_logger_attrs()
        resource = _make_resource(attrs)
        mock_get.return_value = _ok_response(_make_parsed(resource))

        mgmt = _new_mgmt()
        result = mgmt.loggers.get("sql")
        assert isinstance(result, SmplLogger)
        mock_get.assert_called_once()
        assert mock_get.call_args.args[0] == "sql"

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_get_not_found_404(self, mock_get):
        mock_get.return_value = _ok_response(None, HTTPStatus.NOT_FOUND)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.loggers.get("sql")

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_get_not_found_null_parsed(self, mock_get):
        mock_get.return_value = _ok_response(None)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.loggers.get("sql")


# ---------------------------------------------------------------------------
# save() — create (id=None) and update (id set)
# ---------------------------------------------------------------------------


class TestSaveLogger:
    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_puts_directly_when_not_created(self, mock_update):
        """PUT is the only call for a new logger — server handles upsert."""
        attrs = _make_logger_attrs(level="INFO")
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        lg = mgmt.loggers.new("sql")
        assert lg.created_at is None
        lg.save()

        mock_update.assert_called_once()
        assert mock_update.call_args.args[0] == "sql"

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_puts_with_null_level_when_not_created(self, mock_update):
        """A new logger with no level is sent as null — server upserts without a level."""
        attrs = _make_logger_attrs(level=None)
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        lg = mgmt.loggers.new("app.payments")
        assert lg.level is None
        assert lg.created_at is None
        lg.save()

        mock_update.assert_called_once()
        body = mock_update.call_args.kwargs["body"]
        assert body.data.attributes.level is None

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_updates_when_id_is_set(self, mock_update):
        attrs = _make_logger_attrs(level="ERROR")
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        lg = SmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=LogLevel.DEBUG,
            managed=True,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        lg.level = LogLevel.ERROR
        lg.save()

        mock_update.assert_called_once()
        body = mock_update.call_args.kwargs["body"]
        body_attrs = body.data.attributes
        assert body_attrs.level == "ERROR"

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_sends_all_fields(self, mock_update):
        attrs = _make_logger_attrs(name="SQL Logger", level="DEBUG", managed=True)
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        lg = SmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=LogLevel.DEBUG,
            managed=True,
            group=None,
            environments={"prod": {"level": "WARN"}},
            created_at="2026-01-01T00:00:00Z",
        )
        lg.save()

        body = mock_update.call_args.kwargs["body"]
        body_attrs = body.data.attributes
        assert body_attrs.name == "SQL Logger"
        assert body_attrs.level == "DEBUG"
        assert body_attrs.managed is True
        assert body_attrs.group is None

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_with_level_none(self, mock_update):
        attrs = _make_logger_attrs(level=None)
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        lg = SmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=None,
            managed=True,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        lg.save()

        body = mock_update.call_args.kwargs["body"]
        assert body.data.attributes.level is None

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_with_managed_false(self, mock_update):
        attrs = _make_logger_attrs(managed=False)
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        lg = SmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=LogLevel.DEBUG,
            managed=False,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        lg.save()

        body = mock_update.call_args.kwargs["body"]
        assert body.data.attributes.managed is False

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_updates_self_in_place(self, mock_update):
        response_attrs = _make_logger_attrs(name="SQL Logger v2", level="ERROR", managed=True)
        response_resource = _make_resource(response_attrs)
        response_parsed = _make_parsed(response_resource)
        mock_update.return_value = _ok_response(response_parsed)

        mgmt = _new_mgmt()
        lg = SmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=LogLevel.DEBUG,
            managed=True,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        lg.level = LogLevel.ERROR
        lg.save()

        assert lg.name == "SQL Logger v2"
        assert lg.level == LogLevel.ERROR
        assert lg.id == _TEST_UUID

    @patch("smplkit.logging._client.update_logger.sync_detailed")
    def test_save_null_parsed_raises_validation(self, mock_update):
        mock_update.return_value = _ok_response(None)
        mgmt = _new_mgmt()
        lg = SmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(ValidationError):
            lg.save()


# ---------------------------------------------------------------------------
# delete(id) — direct delete via delete_logger
# ---------------------------------------------------------------------------


class TestDelete:
    @patch("smplkit.logging._client.delete_logger.sync_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NO_CONTENT)

        mgmt = _new_mgmt()
        mgmt.loggers.delete("sql")
        mock_delete.assert_called_once()
        assert mock_delete.call_args.args[0] == "sql"

    @patch("smplkit.logging._client.delete_logger.sync_detailed")
    def test_delete_not_found(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NOT_FOUND)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.loggers.delete("nonexistent")


# ---------------------------------------------------------------------------
# list_groups()
# ---------------------------------------------------------------------------


class TestListGroups:
    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    def test_list_groups(self, mock_list):
        attrs = _make_group_attrs()
        resource = _make_resource(attrs)
        mock_list.return_value = _ok_response(_make_list_parsed([resource]))

        mgmt = _new_mgmt()
        result = mgmt.log_groups.list()
        assert len(result) == 1
        assert isinstance(result[0], SmplLogGroup)

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    def test_list_groups_empty_parsed(self, mock_list):
        mock_list.return_value = _ok_response(None)
        mgmt = _new_mgmt()
        result = mgmt.log_groups.list()
        assert result == []


# ---------------------------------------------------------------------------
# get_group(id) — direct lookup via get_log_group
# ---------------------------------------------------------------------------


class TestGetGroup:
    @patch("smplkit.logging._client.get_log_group.sync_detailed")
    def test_get_group_by_id(self, mock_get):
        attrs = _make_group_attrs()
        resource = _make_resource(attrs)
        mock_get.return_value = _ok_response(_make_parsed(resource))

        mgmt = _new_mgmt()
        result = mgmt.log_groups.get("db-loggers")
        assert isinstance(result, SmplLogGroup)
        mock_get.assert_called_once()
        assert mock_get.call_args.args[0] == "db-loggers"

    @patch("smplkit.logging._client.get_log_group.sync_detailed")
    def test_get_group_not_found_404(self, mock_get):
        mock_get.return_value = _ok_response(None, HTTPStatus.NOT_FOUND)

        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.log_groups.get("db-loggers")

    @patch("smplkit.logging._client.get_log_group.sync_detailed")
    def test_get_group_not_found_null_parsed(self, mock_get):
        mock_get.return_value = _ok_response(None)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.log_groups.get("db-loggers")


# ---------------------------------------------------------------------------
# Group save() — create and update
# ---------------------------------------------------------------------------


class TestSaveGroup:
    @patch("smplkit.logging._client.create_log_group.sync_detailed")
    def test_save_creates_when_id_is_none(self, mock_create):
        attrs = _make_group_attrs()
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_create.return_value = _ok_response(parsed, HTTPStatus.CREATED)

        mgmt = _new_mgmt()
        grp = mgmt.log_groups.new("db-loggers", name="DB Loggers")
        grp.save()

        mock_create.assert_called_once()
        assert grp.id == _TEST_UUID

    @patch("smplkit.logging._client.update_log_group.sync_detailed")
    def test_save_updates_when_id_is_set(self, mock_update):
        attrs = _make_group_attrs(level="ERROR")
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        grp = SmplLogGroup(
            mgmt.log_groups,
            id=_TEST_UUID,
            name="DB Loggers",
            level=LogLevel.WARN,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        grp.level = LogLevel.ERROR
        grp.save()

        mock_update.assert_called_once()
        body = mock_update.call_args.kwargs["body"]
        assert body.data.attributes.level == "ERROR"

    @patch("smplkit.logging._client.update_log_group.sync_detailed")
    def test_save_sends_all_fields(self, mock_update):
        attrs = _make_group_attrs(name="DB Loggers", level="WARN")
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        grp = SmplLogGroup(
            mgmt.log_groups,
            id=_TEST_UUID,
            name="DB Loggers",
            level=LogLevel.WARN,
            group=None,
            environments={"prod": {"level": "ERROR"}},
            created_at="2026-01-01T00:00:00Z",
        )
        grp.save()

        body = mock_update.call_args.kwargs["body"]
        body_attrs = body.data.attributes
        assert body_attrs.name == "DB Loggers"
        assert body_attrs.level == "WARN"
        assert body_attrs.parent_id is None

    @patch("smplkit.logging._client.update_log_group.sync_detailed")
    def test_save_with_level_none(self, mock_update):
        attrs = _make_group_attrs(level=None)
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_mgmt()
        grp = SmplLogGroup(
            mgmt.log_groups,
            id=_TEST_UUID,
            name="DB Loggers",
            level=None,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        grp.save()

        body = mock_update.call_args.kwargs["body"]
        assert body.data.attributes.level is None

    @patch("smplkit.logging._client.update_log_group.sync_detailed")
    def test_save_updates_self_in_place(self, mock_update):
        response_attrs = _make_group_attrs(name="DB Loggers v2", level="ERROR")
        response_resource = _make_resource(response_attrs)
        response_parsed = _make_parsed(response_resource)
        mock_update.return_value = _ok_response(response_parsed)

        mgmt = _new_mgmt()
        grp = SmplLogGroup(
            mgmt.log_groups,
            id=_TEST_UUID,
            name="DB Loggers",
            level=LogLevel.WARN,
            group=None,
            environments={},
            created_at="2026-01-01T00:00:00Z",
        )
        grp.level = LogLevel.ERROR
        grp.save()

        assert grp.name == "DB Loggers v2"
        assert grp.level == LogLevel.ERROR
        assert grp.id == _TEST_UUID

    @patch("smplkit.logging._client.update_log_group.sync_detailed")
    def test_save_null_parsed_raises_validation(self, mock_update):
        mock_update.return_value = _ok_response(None)
        mgmt = _new_mgmt()
        grp = SmplLogGroup(mgmt.log_groups, id=_TEST_UUID, name="DB Loggers", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(ValidationError):
            grp.save()


# ---------------------------------------------------------------------------
# delete_group(id) — direct delete via delete_log_group
# ---------------------------------------------------------------------------


class TestDeleteGroup:
    @patch("smplkit.logging._client.delete_log_group.sync_detailed")
    def test_delete_group_by_id(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NO_CONTENT)

        mgmt = _new_mgmt()
        mgmt.log_groups.delete("db-loggers")
        mock_delete.assert_called_once()
        assert mock_delete.call_args.args[0] == "db-loggers"

    @patch("smplkit.logging._client.delete_log_group.sync_detailed")
    def test_delete_group_not_found(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NOT_FOUND)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.log_groups.delete("nonexistent")


# ---------------------------------------------------------------------------
# Model convenience methods: setLevel, clearLevel, environment methods
# ---------------------------------------------------------------------------


class TestLoggerConvenienceMethods:
    def test_set_level(self):
        lg = SmplLogger(None, id="sql", name="SQL Logger")
        lg.set_level(LogLevel.ERROR)
        assert lg.level == "ERROR"

    def test_clear_level(self):
        lg = SmplLogger(None, id="sql", name="SQL Logger", level="DEBUG")
        lg.clear_level()
        assert lg.level is None

    def test_setEnvironmentLevel(self):
        lg = SmplLogger(None, id="sql", name="SQL Logger")
        lg.set_level(LogLevel.WARN, environment="prod")
        assert lg.environments["prod"].level == LogLevel.WARN

    def test_clearEnvironmentLevel(self):
        lg = SmplLogger(None, id="sql", name="SQL Logger", environments={"prod": {"level": "WARN"}})
        lg.clear_level(environment="prod")
        assert "prod" not in lg.environments

    def test_clearEnvironmentLevel_missing_key(self):
        lg = SmplLogger(None, id="sql", name="SQL Logger")
        lg.clear_level(environment="nonexistent")  # should not raise

    def test_clearAllEnvironmentLevels(self):
        lg = SmplLogger(
            None, id="sql", name="SQL Logger", environments={"prod": {"level": "WARN"}, "dev": {"level": "DEBUG"}}
        )
        lg.clear_all_environment_levels()
        assert lg.environments == {}


class TestLogGroupConvenienceMethods:
    def test_set_level(self):
        grp = SmplLogGroup(None, id="db", name="DB")
        grp.set_level(LogLevel.ERROR)
        assert grp.level == "ERROR"

    def test_clear_level(self):
        grp = SmplLogGroup(None, id="db", name="DB", level="WARN")
        grp.clear_level()
        assert grp.level is None

    def test_setEnvironmentLevel(self):
        grp = SmplLogGroup(None, id="db", name="DB")
        grp.set_level(LogLevel.DEBUG, environment="staging")
        assert grp.environments["staging"].level == LogLevel.DEBUG

    def test_clearEnvironmentLevel(self):
        grp = SmplLogGroup(None, id="db", name="DB", environments={"staging": {"level": "DEBUG"}})
        grp.clear_level(environment="staging")
        assert "staging" not in grp.environments

    def test_clearEnvironmentLevel_missing_key(self):
        grp = SmplLogGroup(None, id="db", name="DB")
        grp.clear_level(environment="nonexistent")

    def test_clearAllEnvironmentLevels(self):
        grp = SmplLogGroup(None, id="db", name="DB", environments={"a": {"level": "DEBUG"}, "b": {"level": "ERROR"}})
        grp.clear_all_environment_levels()
        assert grp.environments == {}


# ---------------------------------------------------------------------------
# start() — public wrapper for _connect_internal()
# ---------------------------------------------------------------------------


class TestStart:
    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging._client._auto_load_adapters")
    def test_install_connects(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        client.install()
        assert client._connected is True
        client._close()

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging._client._auto_load_adapters")
    def test_install_is_idempotent(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        client.install()
        client.install()  # second call should be no-op
        mock_auto_load.assert_called_once()
        client._close()


# ---------------------------------------------------------------------------
# on_change — dual-mode decorator
# ---------------------------------------------------------------------------


class TestOnChange:
    def test_bare_decorator_global(self):
        client = _make_logging_client()
        client._connected = True
        calls = []

        @client.on_change
        def handler():
            calls.append(True)

        assert handler in client._global_listeners

    def test_key_scoped_decorator(self):
        client = _make_logging_client()
        client._connected = True
        calls = []

        @client.on_change("sqlalchemy.engine")
        def handler():
            calls.append(True)

        assert handler in client._key_listeners["sqlalchemy.engine"]

    def test_parens_no_args_global(self):
        client = _make_logging_client()
        client._connected = True
        calls = []

        @client.on_change()
        def handler():
            calls.append(True)

        assert handler in client._global_listeners

    def test_returns_original_function(self):
        client = _make_logging_client()
        client._connected = True

        @client.on_change("key")
        def my_fn():
            pass

        assert my_fn.__name__ == "my_fn"

    def test_on_change_before_install_raises(self):
        from smplkit import NotInstalledError

        client = _make_logging_client()
        with pytest.raises(NotInstalledError, match="install"):
            client.on_change(lambda event: None)


# ---------------------------------------------------------------------------
# Management works without connect
# ---------------------------------------------------------------------------


class TestManagementWithoutConnect:
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_list_without_connect(self, mock_list):
        mock_list.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        mgmt = _new_mgmt()
        assert client._connected is False
        result = mgmt.loggers.list()
        assert result == []


# ---------------------------------------------------------------------------
# Registration buffer
# ---------------------------------------------------------------------------


class TestLoggerRegistrationBuffer:
    def test_add_and_drain(self):
        buf = _LoggerRegistrationBuffer()
        buf.add("com.example", "INFO", "INFO", "my-service", "production")
        batch = buf.drain()
        assert len(batch) == 1
        assert batch[0] == {
            "id": "com.example",
            "level": "INFO",
            "resolved_level": "INFO",
            "service": "my-service",
            "environment": "production",
        }

    def test_null_explicit_level_omitted(self):
        """When explicit level is None, 'level' key is absent from item dict."""
        buf = _LoggerRegistrationBuffer()
        buf.add("com.example", None, "INFO", "svc", "staging")
        batch = buf.drain()
        assert "level" not in batch[0]
        assert batch[0]["resolved_level"] == "INFO"
        assert batch[0]["environment"] == "staging"

    def test_dedup(self):
        buf = _LoggerRegistrationBuffer()
        buf.add("com.example", "INFO", "INFO", "svc", "prod")
        buf.add("com.example", "DEBUG", "DEBUG", "svc", "prod")
        batch = buf.drain()
        assert len(batch) == 1

    def test_service_omitted_when_none(self):
        buf = _LoggerRegistrationBuffer()
        buf.add("com.example", "INFO", "INFO", None, "prod")
        batch = buf.drain()
        assert "service" not in batch[0]

    def test_environment_omitted_when_none(self):
        buf = _LoggerRegistrationBuffer()
        buf.add("com.example", "INFO", "INFO", "svc", None)
        batch = buf.drain()
        assert "environment" not in batch[0]
        assert batch[0]["service"] == "svc"

    def test_drain_clears_pending(self):
        buf = _LoggerRegistrationBuffer()
        buf.add("a", "INFO", "INFO", None, None)
        buf.drain()
        assert buf.drain() == []

    def test_pending_count(self):
        buf = _LoggerRegistrationBuffer()
        assert buf.pending_count == 0
        buf.add("a", "INFO", "INFO", None, None)
        assert buf.pending_count == 1
        buf.add("b", "DEBUG", "DEBUG", None, None)
        assert buf.pending_count == 2

    def test_includes_service_when_provided(self):
        buf = _LoggerRegistrationBuffer()
        buf.add("x", "WARN", "WARN", "api-gateway", "production")
        batch = buf.drain()
        assert batch[0]["service"] == "api-gateway"
        assert batch[0]["environment"] == "production"


# ---------------------------------------------------------------------------
# Bulk flush (fire-and-forget)
# ---------------------------------------------------------------------------


class TestBulkFlush:
    """Coverage of ``mgmt.loggers.flush()`` driven from the runtime buffer."""

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_flush_sends_batch(self, mock_bulk):
        mock_bulk.return_value = _ok_response()
        client = _make_logging_client()
        client.loggers._buffer.add("com.test", "INFO", "INFO", None, None)
        client.loggers.flush()
        mock_bulk.assert_called_once()

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_flush_includes_service_and_environment(self, mock_bulk):
        """Flush payload includes service and environment when provided."""
        mock_bulk.return_value = _ok_response()
        client = _make_logging_client()
        client.loggers._buffer.add("com.test", "INFO", "INFO", "my-svc", "production")
        client.loggers.flush()

        call_kwargs = mock_bulk.call_args
        body = call_kwargs[1]["body"] if "body" in call_kwargs[1] else call_kwargs[0][1]
        item = body.loggers[0]
        assert item.service == "my-svc"
        assert item.environment == "production"

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_flush_noop_when_empty(self, mock_bulk):
        client = _make_logging_client()
        client.loggers.flush()
        mock_bulk.assert_not_called()


# ---------------------------------------------------------------------------
# Payload assembly — resolved_level and level
# ---------------------------------------------------------------------------


class TestPayloadAssembly:
    """Verify correct level/resolved_level values in the bulk registration payload."""

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_logger_with_explicit_level_sends_both(self, mock_bulk):
        """Logger with explicit level: both level and resolved_level are non-null."""
        mock_bulk.return_value = _ok_response()
        import logging as _log

        lg = _log.getLogger("test.payload.explicit")
        lg.setLevel(_log.ERROR)  # explicitly set

        from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter

        client = _make_logging_client()
        adapter = StdlibLoggingAdapter(prefix="test.payload.explicit")
        discovered = adapter.discover()
        assert len(discovered) >= 1
        name, explicit, effective = next(t for t in discovered if t[0] == "test.payload.explicit")
        assert explicit == _log.ERROR
        assert effective == _log.ERROR

        # Buffer and flush
        from smplkit.logging._levels import python_level_to_smpl

        smpl_explicit = python_level_to_smpl(explicit) if explicit else None
        smpl_effective = python_level_to_smpl(effective)
        client.loggers._buffer.add("test.payload.explicit", smpl_explicit, smpl_effective, None, None)
        client.loggers.flush()

        call_kwargs = mock_bulk.call_args
        body = call_kwargs[1]["body"] if "body" in call_kwargs[1] else call_kwargs[0][1]
        item = body.loggers[0]
        assert item.level == "ERROR"
        assert item.resolved_level == "ERROR"

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_logger_without_explicit_level_sends_null_level(self, mock_bulk):
        """Logger with no explicit level: level is null, resolved_level is parent's level."""
        mock_bulk.return_value = _ok_response()
        import logging as _log

        parent_lg = _log.getLogger("test.payload.inherit_parent")
        parent_lg.setLevel(_log.WARNING)
        child_lg = _log.getLogger("test.payload.inherit_parent.child")
        child_lg.setLevel(0)  # NOTSET

        from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter

        client = _make_logging_client()
        adapter = StdlibLoggingAdapter(prefix="test.payload.inherit_parent.child")
        discovered = adapter.discover()
        match = next((t for t in discovered if t[0] == "test.payload.inherit_parent.child"), None)
        assert match is not None
        _name, explicit, effective = match
        assert explicit is None
        assert effective == _log.WARNING

        from smplkit.logging._levels import python_level_to_smpl

        smpl_explicit = python_level_to_smpl(explicit) if explicit is not None else None
        smpl_effective = python_level_to_smpl(effective)
        client.loggers._buffer.add("test.payload.inherit_parent.child", smpl_explicit, smpl_effective, None, None)
        client.loggers.flush()

        call_kwargs = mock_bulk.call_args
        body = call_kwargs[1]["body"] if "body" in call_kwargs[1] else call_kwargs[0][1]
        item = body.loggers[0]
        # level must be absent/None (not explicitly set)
        from smplkit._generated.logging.types import UNSET

        assert item.level is None or item.level is UNSET
        assert item.resolved_level == "WARN"

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_root_logger_has_non_null_level(self, mock_bulk):
        """Root logger always has an explicit level."""
        mock_bulk.return_value = _ok_response()

        from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter

        client = _make_logging_client()
        adapter = StdlibLoggingAdapter()
        discovered = adapter.discover()
        root_entry = next((t for t in discovered if t[0] == "root"), None)
        assert root_entry is not None
        _name, explicit, effective = root_entry
        assert explicit is not None  # root always has explicit level

        from smplkit.logging._levels import python_level_to_smpl

        smpl_explicit = python_level_to_smpl(explicit)
        smpl_effective = python_level_to_smpl(effective)
        client.loggers._buffer.add("root", smpl_explicit, smpl_effective, None, None)
        client.loggers.flush()

        call_kwargs = mock_bulk.call_args
        body = call_kwargs[1]["body"] if "body" in call_kwargs[1] else call_kwargs[0][1]
        item = body.loggers[0]
        assert item.level is not None
        assert item.resolved_level is not None


# ---------------------------------------------------------------------------
# Level application
# ---------------------------------------------------------------------------


class TestLevelApplication:
    def test_managed_logger_gets_level_applied(self):
        client = _make_logging_client()
        test_name = "test.apply.managed_001"
        mock_adapter = MagicMock()
        client._adapters = [mock_adapter]
        client._name_map[test_name] = "test.apply.managed_001"
        client._loggers_cache = {
            "test.apply.managed_001": {
                "level": "ERROR",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        client._groups_cache = {}

        client._apply_levels()
        mock_adapter.apply_level.assert_called_once_with(test_name, 40)

    def test_unmanaged_logger_not_touched(self):
        client = _make_logging_client()
        test_name = "test.apply.unmanaged_002"
        mock_adapter = MagicMock()
        client._adapters = [mock_adapter]
        client._name_map[test_name] = "test.apply.unmanaged_002"
        client._loggers_cache = {
            "test.apply.unmanaged_002": {
                "level": "ERROR",
                "group": None,
                "managed": False,
                "environments": {},
            }
        }
        client._groups_cache = {}

        client._apply_levels()
        mock_adapter.apply_level.assert_not_called()

    def test_logger_in_server_not_in_runtime(self):
        client = _make_logging_client()
        client._loggers_cache = {
            "some.remote.logger": {
                "level": "ERROR",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        client._groups_cache = {}
        client._apply_levels()


# ---------------------------------------------------------------------------
# Refresh
# ---------------------------------------------------------------------------


class TestRefresh:
    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_refresh_fetches_and_applies(self, mock_loggers, mock_groups):
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        client._connected = True
        client.refresh()
        mock_loggers.assert_called_once()
        mock_groups.assert_called_once()

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_refresh_before_install_raises(self, mock_loggers, mock_groups):
        """refresh() before install() raises NotInstalledError (live surface gate)."""
        from smplkit import NotInstalledError

        client = _make_logging_client()
        assert client._connected is False
        with pytest.raises(NotInstalledError, match="install"):
            client.refresh()
        mock_loggers.assert_not_called()


# ---------------------------------------------------------------------------
# Integration: connect flow
# ---------------------------------------------------------------------------


class TestConnectFlow:
    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging._client._auto_load_adapters")
    def test_connect_runs_full_flow(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = [("root", 30, 30), ("myapp.db", 10, 10)]
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        client.install()

        assert client._connected is True
        mock_adapter.discover.assert_called_once()
        mock_adapter.install_hook.assert_called_once()
        mock_bulk.assert_called_once()
        mock_loggers.assert_called_once()
        mock_groups.assert_called_once()
        client._close()

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging._client._auto_load_adapters")
    def test_connect_applies_managed_levels(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        test_name = "test.connect.managed_apply_flow"
        stdlib_logging.getLogger(test_name).setLevel(stdlib_logging.DEBUG)

        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = [(test_name, stdlib_logging.DEBUG, stdlib_logging.DEBUG)]
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()

        logger_attrs = _make_logger_attrs(level="ERROR", managed=True)
        logger_resource = _make_resource(logger_attrs, id=test_name)
        mock_loggers.return_value = _ok_response(_make_list_parsed([logger_resource]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        client.install()

        # Level is applied via the adapter
        mock_adapter.apply_level.assert_called()
        client._close()

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging._client._auto_load_adapters")
    def test_connect_idempotent(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        client.install()
        client.install()  # second call is no-op
        mock_auto_load.assert_called_once()
        client._close()


# ---------------------------------------------------------------------------
# Close
# ---------------------------------------------------------------------------


class TestClose:
    def test_close_uninstalls_adapters(self):
        client = _make_logging_client()
        adapter = MagicMock()
        client._adapters = [adapter]
        client._close()
        adapter.uninstall_hook.assert_called_once()


# ---------------------------------------------------------------------------
# Error mapping
# ---------------------------------------------------------------------------


class TestCheckResponseStatus:
    def test_404_raises_not_found(self):
        with pytest.raises(NotFoundError):
            _check_response_status(HTTPStatus.NOT_FOUND, b"not found")

    def test_422_raises_validation(self):
        with pytest.raises(ValidationError):
            _check_response_status(HTTPStatus.UNPROCESSABLE_ENTITY, b"validation error")

    def test_200_no_raise(self):
        _check_response_status(HTTPStatus.OK, b"")


# ---------------------------------------------------------------------------
# WebSocket event handling
# ---------------------------------------------------------------------------


def _make_logger_response(key="sqlalchemy.engine", level="DEBUG", group=None):
    """Build a mock HTTP response whose .parsed is a LoggerResponse instance."""
    from smplkit.logging._client import LoggerResponse, LoggerResource, GenLogger
    from smplkit._generated.logging.types import UNSET

    attrs = GenLogger(name=key, level=level, group=group or UNSET, managed=True, environments=UNSET)
    resource = LoggerResource(attributes=attrs, id=key, type_="logger")
    parsed = LoggerResponse(data=resource)
    resp = MagicMock()
    resp.status_code = HTTPStatus.OK
    resp.content = b""
    resp.parsed = parsed
    return resp


def _make_group_response(key="db-loggers", level="WARN", parent_id=None):
    """Build a mock HTTP response whose .parsed is a LogGroupResponse instance."""
    from smplkit.logging._client import LogGroupResponse, LogGroupResource, GenLogGroup
    from smplkit._generated.logging.types import UNSET

    attrs = GenLogGroup(name=key, level=level, parent_id=parent_id or UNSET, environments=UNSET)
    resource = LogGroupResource(attributes=attrs, id=key, type_="log_group")
    parsed = LogGroupResponse(data=resource)
    resp = MagicMock()
    resp.status_code = HTTPStatus.OK
    resp.content = b""
    resp.parsed = parsed
    return resp


class TestWebSocketEventHandling:
    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    @patch("smplkit.logging._client._auto_load_adapters")
    def test_connect_registers_ws_handlers(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        """_connect_internal registers handlers for all five logger events."""
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_logging_client()
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        client.install()

        assert mock_ws.on.call_count == 5
        registered_events = {call[0][0] for call in mock_ws.on.call_args_list}
        assert registered_events == {
            "logger_changed",
            "logger_deleted",
            "group_changed",
            "group_deleted",
            "loggers_changed",
        }
        client._close()

    def test_close_deregisters_ws_handlers(self):
        """_close calls off() for all five events on the ws manager."""
        client = _make_logging_client()
        mock_ws = MagicMock()
        client._ws_manager = mock_ws

        client._close()

        assert mock_ws.off.call_count == 5
        deregistered_events = {call[0][0] for call in mock_ws.off.call_args_list}
        assert deregistered_events == {
            "logger_changed",
            "logger_deleted",
            "group_changed",
            "group_deleted",
            "loggers_changed",
        }
        assert client._ws_manager is None

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_handle_logger_changed_scoped_fetch_and_fires(self, mock_get):
        """logger_changed fires once per logger whose effective level moved."""
        mock_get.return_value = _make_logger_response("sqlalchemy.engine", level="INFO")
        client = _make_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_logger_changed({"id": "sqlalchemy.engine"})
        mock_get.assert_called_once()
        listener.assert_called_once()
        event = listener.call_args[0][0]
        assert event.id == "sqlalchemy.engine"
        assert event.source == "websocket"
        assert event.level == "INFO"

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_handle_logger_changed_no_fire_when_effective_unchanged(self, mock_get):
        """logger_changed fires no listener when effective level is unchanged."""
        mock_get.return_value = _make_logger_response("sqlalchemy.engine", level="DEBUG")
        client = _make_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_logger_changed({"id": "sqlalchemy.engine"})
        listener.assert_not_called()

    def test_handle_logger_deleted_removes_cache_and_fires_no_event_for_deleted_key(self):
        """logger_deleted removes the cache entry. The deleted logger itself
        fires no listener (deletion is not a level change). Loggers whose
        effective level changes due to the deletion fire normally."""
        client = _make_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        global_listener = MagicMock()
        key_listener_on_deleted = MagicMock()
        client._global_listeners.append(global_listener)
        client._key_listeners["sqlalchemy.engine"] = [key_listener_on_deleted]
        client._handle_logger_deleted({"id": "sqlalchemy.engine"})
        assert "sqlalchemy.engine" not in client._loggers_cache
        # The deleted entity's own listener never fires for a deletion.
        global_listener.assert_not_called()
        key_listener_on_deleted.assert_not_called()

    def test_handle_logger_deleted_missing_key_no_fire(self):
        """logger_deleted does not fire when the key was not in cache."""
        client = _make_logging_client()
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_logger_deleted({"id": "ghost"})
        listener.assert_not_called()

    @patch("smplkit.logging._client.get_log_group.sync_detailed")
    def test_handle_group_changed_cascades_to_dependent_logger(self, mock_get):
        """group_changed fires once per dependent logger whose effective level moved."""
        mock_get.return_value = _make_group_response("db-loggers", level="ERROR")
        client = _make_logging_client()
        client._name_map["app.db"] = "app.db"
        client._groups_cache["db-loggers"] = {"level": "WARN", "group": None, "environments": {}}
        client._loggers_cache["app.db"] = {
            "level": None,
            "group": "db-loggers",
            "managed": True,
            "environments": {},
        }
        global_listener = MagicMock()
        client._global_listeners.append(global_listener)
        key_listener = MagicMock()
        client._key_listeners["app.db"] = [key_listener]
        client._handle_group_changed({"id": "db-loggers"})
        mock_get.assert_called_once()
        global_listener.assert_called_once()
        event = global_listener.call_args[0][0]
        assert event.id == "app.db"
        assert event.level == "ERROR"
        key_listener.assert_called_once()
        assert key_listener.call_args[0][0].id == "app.db"

    def test_handle_group_deleted_cascade_no_event_for_group_key(self):
        """group_deleted cascades to dependent loggers; no event for the group id."""
        client = _make_logging_client()
        client._name_map["app.db"] = "app.db"
        client._groups_cache["db-loggers"] = {"level": "WARN", "group": None, "environments": {}}
        client._loggers_cache["app.db"] = {
            "level": None,
            "group": "db-loggers",
            "managed": True,
            "environments": {},
        }
        # A listener on the group key — must NOT fire (groups aren't loggers).
        group_key_listener = MagicMock()
        client._key_listeners["db-loggers"] = [group_key_listener]
        logger_listener = MagicMock()
        client._key_listeners["app.db"] = [logger_listener]
        client._handle_group_deleted({"id": "db-loggers"})
        assert "db-loggers" not in client._groups_cache
        group_key_listener.assert_not_called()
        logger_listener.assert_called_once()
        event = logger_listener.call_args[0][0]
        assert event.id == "app.db"
        assert event.level == "INFO"  # system fallback

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_handle_loggers_changed_full_refetch_and_diff_fire(self, mock_loggers, mock_groups):
        """loggers_changed re-fetches and fires once per logger whose effective level moved."""
        logger_attrs = _make_logger_attrs(name="SQL Logger", level="INFO")
        resource = _make_resource(logger_attrs, id="sqlalchemy.engine")
        mock_loggers.return_value = _ok_response(_make_list_parsed([resource]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))
        client = _make_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_loggers_changed({})
        mock_loggers.assert_called_once()
        listener.assert_called_once()
        assert listener.call_args[0][0].level == "INFO"

    @patch("smplkit.logging._client.list_log_groups.sync_detailed")
    @patch("smplkit.logging._client.list_loggers.sync_detailed")
    def test_handle_loggers_changed_swallows_fetch_errors(self, mock_loggers, mock_groups):
        """loggers_changed does not raise on fetch failure."""
        mock_loggers.side_effect = RuntimeError("network failure")
        client = _make_logging_client()
        client._handle_loggers_changed({})  # should not raise

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_handle_logger_changed_fetch_error_swallowed(self, mock_get):
        """_handle_logger_changed logs warning on fetch failure."""
        mock_get.side_effect = RuntimeError("network down")
        client = _make_logging_client()
        client._handle_logger_changed({"id": "sqlalchemy.engine"})  # should not raise

    @patch("smplkit.logging._client.get_log_group.sync_detailed")
    def test_handle_group_changed_fetch_error_swallowed(self, mock_get):
        """_handle_group_changed logs warning on fetch failure."""
        mock_get.side_effect = RuntimeError("network down")
        client = _make_logging_client()
        client._handle_group_changed({"id": "db-loggers"})  # should not raise

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_global_listener_exception_swallowed(self, mock_get):
        """_fire_for_logger swallows exceptions from global listeners."""
        mock_get.return_value = _make_logger_response("sqlalchemy.engine", level="INFO")
        client = _make_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._global_listeners.extend([bad, good])
        client._handle_logger_changed({"id": "sqlalchemy.engine"})
        good.assert_called_once()

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_key_listener_exception_swallowed(self, mock_get):
        """_fire_for_logger swallows exceptions from per-key listeners."""
        mock_get.return_value = _make_logger_response("sqlalchemy.engine", level="INFO")
        client = _make_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        bad = MagicMock(side_effect=RuntimeError("boom"))
        good = MagicMock()
        client._key_listeners["sqlalchemy.engine"] = [bad, good]
        client._handle_logger_changed({"id": "sqlalchemy.engine"})
        good.assert_called_once()

    def test_logger_change_event_repr(self):
        from smplkit.logging._client import LoggerChangeEvent

        event = LoggerChangeEvent(id="sqlalchemy.engine", level="DEBUG", source="websocket")
        r = repr(event)
        assert "sqlalchemy.engine" in r
        assert "websocket" in r
        assert "DEBUG" in r


# ---------------------------------------------------------------------------
# Listener fanout diagnostics
#
# One invocation per effective-level apply. Global listeners are
# semantically a key-scoped subscription on every logger — so an N-way
# cascade fires N invocations of every global, not one summary event.
# Deletion is not a level change: the deleted entity itself never fires;
# only dependent loggers whose effective level moves fire (through the
# normal apply path).
# ---------------------------------------------------------------------------


class TestListenerFanoutDiagnostics:
    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_diagnostic_1_dot_ancestor_cascade_fires_per_logger(self, mock_get):
        """logger_changed on com.acme cascades to 5 descendants → global fires 6x."""
        mock_get.return_value = _make_logger_response("com.acme", level="ERROR")
        client = _make_logging_client()
        for name in ["com.acme", "com.acme.a", "com.acme.b", "com.acme.c", "com.acme.d", "com.acme.e"]:
            client._name_map[name] = name
            client._loggers_cache[name] = {
                "level": "WARN" if name == "com.acme" else None,
                "group": None,
                "managed": True,
                "environments": {},
            }
        global_listener = MagicMock()
        client._global_listeners.append(global_listener)
        client._handle_logger_changed({"id": "com.acme"})
        assert global_listener.call_count == 6
        # Each invocation carries one logger's id and the new level.
        ids = {c.args[0].id for c in global_listener.call_args_list}
        levels = {c.args[0].level for c in global_listener.call_args_list}
        assert ids == {"com.acme", "com.acme.a", "com.acme.b", "com.acme.c", "com.acme.d", "com.acme.e"}
        assert levels == {"ERROR"}

    @patch("smplkit.logging._client.get_log_group.sync_detailed")
    def test_diagnostic_2_group_cascade_fires_per_logger(self, mock_get):
        """group_changed on app cascades to 3 dependent loggers → global fires 3x."""
        mock_get.return_value = _make_group_response("app", level="ERROR")
        client = _make_logging_client()
        client._groups_cache["app"] = {"level": "WARN", "group": None, "environments": {}}
        for name in ["app.db", "app.queue", "app.api"]:
            client._name_map[name] = name
            client._loggers_cache[name] = {
                "level": None,
                "group": "app",
                "managed": True,
                "environments": {},
            }
        global_listener = MagicMock()
        client._global_listeners.append(global_listener)
        client._handle_group_changed({"id": "app"})
        assert global_listener.call_count == 3
        ids = {c.args[0].id for c in global_listener.call_args_list}
        assert ids == {"app.db", "app.queue", "app.api"}
        assert all(c.args[0].level == "ERROR" for c in global_listener.call_args_list)

    def test_diagnostic_3_group_deleted_cascade_fires_per_dependent_no_deleted_event(self):
        """group_deleted on app fires 3 cascade events for dependents. NO event
        for the deleted group id; NO deleted-flavored event anywhere."""
        client = _make_logging_client()
        client._groups_cache["app"] = {"level": "ERROR", "group": None, "environments": {}}
        for name in ["app.db", "app.queue", "app.api"]:
            client._name_map[name] = name
            client._loggers_cache[name] = {
                "level": None,
                "group": "app",
                "managed": True,
                "environments": {},
            }
        global_listener = MagicMock()
        client._global_listeners.append(global_listener)
        # Listener on the deleted group key — must not fire (groups aren't loggers).
        group_key_listener = MagicMock()
        client._key_listeners["app"] = [group_key_listener]
        client._handle_group_deleted({"id": "app"})
        assert global_listener.call_count == 3
        ids = [c.args[0].id for c in global_listener.call_args_list]
        assert set(ids) == {"app.db", "app.queue", "app.api"}
        # No event carries id="app", no event has a `deleted` field at all.
        assert "app" not in ids
        for c in global_listener.call_args_list:
            assert not hasattr(c.args[0], "deleted")
            assert c.args[0].level == "INFO"  # system fallback
        group_key_listener.assert_not_called()

    @patch("smplkit.logging._client.get_logger.sync_detailed")
    def test_diagnostic_4_name_only_edit_fires_nothing(self, mock_get):
        """logger_changed whose payload differs only on a non-resolving field
        (here: an off-environment override) fires zero listener invocations."""
        # Active env is "test". The fetched logger keeps its own level WARN and
        # only adds a staging override → effective level for "test" is unchanged.
        new_logger = _make_logger_response("app.db", level="WARN")
        new_logger.parsed.data.attributes.environments = MagicMock(
            additional_properties={"staging": MagicMock(level="DEBUG")},
        )
        mock_get.return_value = new_logger

        client = _make_logging_client()
        client._name_map["app.db"] = "app.db"
        client._loggers_cache["app.db"] = {
            "level": "WARN",
            "group": None,
            "managed": True,
            "environments": {},
        }
        global_listener = MagicMock()
        key_listener = MagicMock()
        client._global_listeners.append(global_listener)
        client._key_listeners["app.db"] = [key_listener]
        client._handle_logger_changed({"id": "app.db"})
        global_listener.assert_not_called()
        key_listener.assert_not_called()

    def test_snapshot_skips_loggers_not_in_cache_or_unmanaged(self):
        """_snapshot_effective_levels skips a name_map entry that has no cache
        row or whose cache row is unmanaged."""
        client = _make_logging_client()
        client._name_map["app.unknown"] = "app.unknown"  # no cache entry
        client._name_map["app.unmanaged"] = "app.unmanaged"
        client._loggers_cache["app.unmanaged"] = {
            "level": "DEBUG",
            "group": None,
            "managed": False,
            "environments": {},
        }
        client._name_map["app.tracked"] = "app.tracked"
        client._loggers_cache["app.tracked"] = {
            "level": "WARN",
            "group": None,
            "managed": True,
            "environments": {},
        }
        snap = client._snapshot_effective_levels()
        assert snap == {"app.tracked": "WARN"}

    def test_apply_deltas_swallows_adapter_exception(self):
        """A misbehaving adapter is logged and the fire path continues."""
        client = _make_logging_client()
        client._name_map["app.db"] = "app.db"
        client._loggers_cache["app.db"] = {
            "level": "WARN",
            "group": None,
            "managed": True,
            "environments": {},
        }
        bad_adapter = MagicMock()
        bad_adapter.name = "bad"
        bad_adapter.apply_level.side_effect = RuntimeError("adapter exploded")
        client._adapters = [bad_adapter]
        listener = MagicMock()
        client._global_listeners.append(listener)
        # Pre is empty, so any current level counts as a delta — apply and fire.
        client._apply_deltas_and_fire({}, "websocket")
        # Adapter's apply_level was called and raised; fire still happened.
        bad_adapter.apply_level.assert_called_once()
        listener.assert_called_once()

    def test_refresh_fires_with_source_manual(self):
        """refresh() runs the delta path with source='manual' (not 'websocket')."""
        client = _make_logging_client()
        client._connected = True
        client._name_map["app.db"] = "app.db"
        # Cache starts at WARN; mock the refresh to return ERROR.
        client._loggers_cache["app.db"] = {
            "level": "WARN",
            "group": None,
            "managed": True,
            "environments": {},
        }
        with (
            patch("smplkit.logging._client.list_loggers.sync_detailed") as mock_loggers,
            patch("smplkit.logging._client.list_log_groups.sync_detailed") as mock_groups,
        ):
            attrs = _make_logger_attrs(name="app.db", level="ERROR")
            mock_loggers.return_value = _ok_response(_make_list_parsed([_make_resource(attrs, id="app.db")]))
            mock_groups.return_value = _ok_response(_make_list_parsed([]))
            listener = MagicMock()
            client._global_listeners.append(listener)
            client.refresh()
        listener.assert_called_once()
        assert listener.call_args[0][0].source == "manual"
        assert listener.call_args[0][0].level == "ERROR"


# ---------------------------------------------------------------------------
# _str_to_log_level helper
# ---------------------------------------------------------------------------


class TestStrToLogLevel:
    def test_valid_level(self):
        from smplkit.logging._client import _str_to_log_level

        assert _str_to_log_level("WARN") == LogLevel.WARN

    def test_invalid_level_returns_none(self):
        from smplkit.logging._client import _str_to_log_level

        assert _str_to_log_level("NOTAVALID") is None

    def test_none_input(self):
        from smplkit.logging._client import _str_to_log_level

        assert _str_to_log_level(None) is None


class TestLogLevelValue:
    """``_loglevel_value`` is the boundary helper used by every save_*
    method: enum in → wire string out, ``None`` passes through, anything
    else raises a TypeError that names the call site."""

    def test_enum_passes_through(self):
        from smplkit.logging._client import _loglevel_value

        assert _loglevel_value(LogLevel.WARN, where="t") == "WARN"

    def test_none_returns_none(self):
        from smplkit.logging._client import _loglevel_value

        assert _loglevel_value(None, where="t") is None

    def test_valid_loglevel_string_is_accepted(self):
        """A valid LogLevel-string is accepted and normalized to its wire value."""
        from smplkit.logging._client import _loglevel_value

        assert _loglevel_value("WARN", where="caller") == "WARN"

    def test_invalid_string_raises_pointing_at_caller(self):
        """An unrecognized string should raise a TypeError that names the caller."""
        import pytest

        from smplkit.logging._client import _loglevel_value

        with pytest.raises(TypeError, match="SmplLogGroup.save"):
            _loglevel_value("NOT_A_LEVEL", where="SmplLogGroup.save")

    def test_other_garbage_raises(self):
        import pytest

        from smplkit.logging._client import _loglevel_value

        with pytest.raises(TypeError, match=r"got int"):
            _loglevel_value(42, where="anywhere")


# ---------------------------------------------------------------------------
# register / flush (sync) — buffered and eager-flush registration
# ---------------------------------------------------------------------------


class TestRegisterAndFlush:
    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_register_with_flush_sends_immediately(self, mock_bulk):
        from smplkit.logging._sources import LoggerSource

        mock_bulk.return_value = MagicMock(status_code=200, content=b"{}")
        mgmt = _new_mgmt()
        mgmt.loggers.register(
            [
                LoggerSource(
                    name="sqlalchemy.engine",
                    service="api",
                    environment="production",
                    resolved_level=LogLevel.WARN,
                ),
            ],
            flush=True,
        )
        mock_bulk.assert_called_once()
        _, kwargs = mock_bulk.call_args
        assert kwargs["body"].loggers[0].service == "api"

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_register_includes_explicit_level(self, mock_bulk):
        from smplkit.logging._sources import LoggerSource

        mock_bulk.return_value = MagicMock(status_code=200, content=b"{}")
        mgmt = _new_mgmt()
        mgmt.loggers.register(
            [
                LoggerSource(
                    name="httpx",
                    service="svc",
                    environment="staging",
                    resolved_level=LogLevel.INFO,
                    level=LogLevel.DEBUG,
                ),
            ],
            flush=True,
        )
        _, kwargs = mock_bulk.call_args
        assert kwargs["body"].loggers[0].level == "DEBUG"

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_flush_with_empty_buffer_skips_call(self, mock_bulk):
        mgmt = _new_mgmt()
        mgmt.loggers.flush()
        mock_bulk.assert_not_called()

    @patch("smplkit.logging._client.bulk_register_loggers.sync_detailed")
    def test_register_with_flush_propagates_unexpected_errors(self, mock_bulk):
        from smplkit.logging._sources import LoggerSource

        mock_bulk.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError):
            mgmt.loggers.register(
                [
                    LoggerSource("app", service="svc", environment="prod", resolved_level=LogLevel.INFO),
                ],
                flush=True,
            )


def test_logging_client_extra_headers_reach_transport() -> None:
    """extra_headers are stored on LoggingClient._logging_http and applied to every request."""
    from smplkit._client import SmplClient

    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client.logging._logging_http._headers.get("X-Test") == "v"
    finally:
        client.close()
