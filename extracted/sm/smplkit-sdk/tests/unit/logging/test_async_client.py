"""Tests for AsyncLoggingClient — covers all async code paths."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from smplkit import LogLevel
from smplkit._errors import NotFoundError, ValidationError
from smplkit.logging.client import (
    AsyncLoggingClient,
    AsyncSmplLogGroup,
    AsyncSmplLogger,
)


_TEST_UUID = "550e8400-e29b-41d4-a716-446655440000"


def _make_logger_attrs(*, name="SQL Logger", level="DEBUG", group=None, managed=True):
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


def _make_async_logging_client(**kwargs):
    from smplkit.management.client import AsyncLoggersClient as _MgmtAsyncLoggersClient

    parent = MagicMock()
    parent._api_key = "sk_test"
    parent._environment = "test"
    parent._service = kwargs.get("service", None)
    manage = MagicMock()
    manage.loggers = _MgmtAsyncLoggersClient(MagicMock(), base_url="http://logging:8003")
    parent.manage = manage
    with patch("smplkit.logging.client.AuthenticatedClient"):
        client = AsyncLoggingClient(parent, manage=manage, metrics=parent._metrics)
    return client


# ---------------------------------------------------------------------------
# new() — factory for unsaved async loggers
# ---------------------------------------------------------------------------


def _new_mgmt_loggers():
    """Return a LoggersClient bound to a mock http (for management-flavored tests)."""
    from smplkit.management.client import LoggersClient
    from unittest.mock import MagicMock as _MM

    return LoggersClient(_MM(), base_url="http://logging:8003")


def _new_mgmt_log_groups():
    """Return a LogGroupsClient bound to a mock http."""
    from smplkit.management.client import LogGroupsClient
    from unittest.mock import MagicMock as _MM

    return LogGroupsClient(_MM(), base_url="http://logging:8003")


def _new_mgmt():
    """Build a SmplManagementClient for management-flavored tests."""
    from smplkit import SmplManagementClient

    return SmplManagementClient(api_key="sk_test", base_domain="example.test")


def _new_async_mgmt():
    """Build an AsyncSmplManagementClient for management-flavored tests."""
    from smplkit import AsyncSmplManagementClient

    return AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")


class TestAsyncNew:
    def test_new_returns_unsaved_logger(self):
        mgmt = _new_async_mgmt()
        lg = mgmt.loggers.new("sql")
        assert isinstance(lg, AsyncSmplLogger)
        assert lg.id == "sql"
        assert lg.managed is True

    def test_new_name_equals_id(self):
        mgmt = _new_async_mgmt()
        lg = mgmt.loggers.new("sqlalchemy.engine")
        assert lg.name == "sqlalchemy.engine"

    def test_new_with_unmanaged(self):
        mgmt = _new_async_mgmt()
        lg = mgmt.loggers.new("sql", managed=False)
        assert lg.managed is False


# ---------------------------------------------------------------------------
# new_group() — factory for unsaved async log groups
# ---------------------------------------------------------------------------


class TestAsyncNewGroup:
    def test_new_group_returns_unsaved(self):
        mgmt = _new_async_mgmt()
        grp = mgmt.log_groups.new("db-loggers")
        assert isinstance(grp, AsyncSmplLogGroup)
        assert grp.id == "db-loggers"

    def test_new_group_with_name(self):
        mgmt = _new_async_mgmt()
        grp = mgmt.log_groups.new("db-loggers", name="DB Loggers")
        assert grp.name == "DB Loggers"

    def test_new_group_auto_generates_name(self):
        mgmt = _new_async_mgmt()
        grp = mgmt.log_groups.new("db-loggers")
        assert grp.name == "Db Loggers"

    def test_new_group_with_parent_group(self):
        mgmt = _new_async_mgmt()
        grp = mgmt.log_groups.new("child", group="parent-id")
        assert grp.group == "parent-id"


# ---------------------------------------------------------------------------
# list()
# ---------------------------------------------------------------------------


class TestAsyncList:
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_list(self, mock_list):
        attrs = _make_logger_attrs()
        resource = _make_resource(attrs)
        mock_list.return_value = _ok_response(_make_list_parsed([resource]))

        mgmt = _new_async_mgmt()
        result = asyncio.run(mgmt.loggers.list())
        assert len(result) == 1
        assert isinstance(result[0], AsyncSmplLogger)

    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_list_empty_parsed(self, mock_list):
        mock_list.return_value = _ok_response(None)
        mgmt = _new_async_mgmt()
        result = asyncio.run(mgmt.loggers.list())
        assert result == []


# ---------------------------------------------------------------------------
# get(id) — direct lookup via get_logger
# ---------------------------------------------------------------------------


class TestAsyncGet:
    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_get_by_id(self, mock_get):
        attrs = _make_logger_attrs()
        resource = _make_resource(attrs)
        mock_get.return_value = _ok_response(_make_parsed(resource))

        mgmt = _new_async_mgmt()
        result = asyncio.run(mgmt.loggers.get("sql"))
        assert isinstance(result, AsyncSmplLogger)
        assert mock_get.call_args.args[0] == "sql"

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_get_not_found_404(self, mock_get):
        mock_get.return_value = _ok_response(None, HTTPStatus.NOT_FOUND)
        mgmt = _new_async_mgmt()
        with pytest.raises(NotFoundError):
            asyncio.run(mgmt.loggers.get("sql"))

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_get_not_found_null_parsed(self, mock_get):
        mock_get.return_value = _ok_response(None)
        mgmt = _new_async_mgmt()
        with pytest.raises(NotFoundError):
            asyncio.run(mgmt.loggers.get("sql"))


# ---------------------------------------------------------------------------
# save() — create (id=None) and update (id set)
# ---------------------------------------------------------------------------


class TestAsyncSaveLogger:
    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_puts_directly_when_not_created(self, mock_update):
        """PUT is the only call for a new logger — server handles upsert."""
        attrs = _make_logger_attrs(level="DEBUG")
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_async_mgmt()
        lg = mgmt.loggers.new("sql")
        assert lg.created_at is None
        asyncio.run(lg.save())

        mock_update.assert_called_once()
        assert mock_update.call_args.args[0] == "sql"

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_puts_with_null_level_when_not_created(self, mock_update):
        """A new logger with no level is sent as null — server upserts without a level."""
        attrs = _make_logger_attrs(level=None)
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_update.return_value = _ok_response(parsed)

        mgmt = _new_async_mgmt()
        lg = mgmt.loggers.new("app.payments")
        assert lg.level is None
        assert lg.created_at is None
        asyncio.run(lg.save())

        mock_update.assert_called_once()
        body = mock_update.call_args.kwargs["body"]
        assert body.data.attributes.level is None

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_updates_when_id_is_set(self, mock_update):
        updated_attrs = _make_logger_attrs(level="ERROR")
        updated_resource = _make_resource(updated_attrs)
        updated_parsed = _make_parsed(updated_resource)
        mock_update.return_value = _ok_response(updated_parsed)

        mgmt = _new_async_mgmt()
        logger = AsyncSmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=LogLevel.DEBUG,
            managed=True,
            created_at="2026-01-01T00:00:00Z",
        )
        logger.level = LogLevel.ERROR
        asyncio.run(logger.save())

        mock_update.assert_called_once()
        assert logger.level == LogLevel.ERROR

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_null_parsed_raises_validation(self, mock_update):
        mock_update.return_value = _ok_response(None)
        mgmt = _new_async_mgmt()
        logger = AsyncSmplLogger(
            mgmt.loggers,
            id=_TEST_UUID,
            name="SQL Logger",
            level=LogLevel.ERROR,
            managed=True,
            created_at="2026-01-01T00:00:00Z",
        )
        with pytest.raises(ValidationError):
            asyncio.run(logger.save())


# ---------------------------------------------------------------------------
# delete(id) — direct delete via delete_logger
# ---------------------------------------------------------------------------


class TestAsyncDelete:
    @patch("smplkit.logging.client.delete_logger.asyncio_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NO_CONTENT)

        mgmt = _new_async_mgmt()
        asyncio.run(mgmt.loggers.delete("sql"))
        mock_delete.assert_called_once()
        assert mock_delete.call_args.args[0] == "sql"

    @patch("smplkit.logging.client.delete_logger.asyncio_detailed")
    def test_delete_not_found(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NOT_FOUND)
        mgmt = _new_async_mgmt()
        with pytest.raises(NotFoundError):
            asyncio.run(mgmt.loggers.delete("nonexistent"))


# ---------------------------------------------------------------------------
# list_groups()
# ---------------------------------------------------------------------------


class TestAsyncListGroups:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    def test_list_groups(self, mock_list):
        attrs = _make_group_attrs()
        resource = _make_resource(attrs)
        mock_list.return_value = _ok_response(_make_list_parsed([resource]))

        mgmt = _new_async_mgmt()
        result = asyncio.run(mgmt.log_groups.list())
        assert len(result) == 1
        assert isinstance(result[0], AsyncSmplLogGroup)

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    def test_list_groups_empty_parsed(self, mock_list):
        mock_list.return_value = _ok_response(None)
        mgmt = _new_async_mgmt()
        result = asyncio.run(mgmt.log_groups.list())
        assert result == []


# ---------------------------------------------------------------------------
# get_group(id) — direct lookup via get_log_group
# ---------------------------------------------------------------------------


class TestAsyncGetGroup:
    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_get_group_by_id(self, mock_get):
        attrs = _make_group_attrs()
        resource = _make_resource(attrs)
        mock_get.return_value = _ok_response(_make_parsed(resource))

        mgmt = _new_async_mgmt()
        result = asyncio.run(mgmt.log_groups.get("db-loggers"))
        assert isinstance(result, AsyncSmplLogGroup)
        assert mock_get.call_args.args[0] == "db-loggers"

    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_get_group_not_found_404(self, mock_get):
        mock_get.return_value = _ok_response(None, HTTPStatus.NOT_FOUND)

        mgmt = _new_async_mgmt()
        with pytest.raises(NotFoundError):
            asyncio.run(mgmt.log_groups.get("db-loggers"))

    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_get_group_not_found_null_parsed(self, mock_get):
        mock_get.return_value = _ok_response(None)
        mgmt = _new_async_mgmt()
        with pytest.raises(NotFoundError):
            asyncio.run(mgmt.log_groups.get("db-loggers"))


# ---------------------------------------------------------------------------
# Group save() — create and update
# ---------------------------------------------------------------------------


class TestAsyncSaveGroup:
    @patch("smplkit.logging.client.create_log_group.asyncio_detailed")
    def test_save_creates_when_id_is_none(self, mock_create):
        attrs = _make_group_attrs()
        resource = _make_resource(attrs)
        parsed = _make_parsed(resource)
        mock_create.return_value = _ok_response(parsed, HTTPStatus.CREATED)

        mgmt = _new_async_mgmt()
        grp = mgmt.log_groups.new("db-loggers", name="DB Loggers")
        asyncio.run(grp.save())

        mock_create.assert_called_once()
        assert grp.id == _TEST_UUID

    @patch("smplkit.logging.client.update_log_group.asyncio_detailed")
    def test_save_updates_when_id_is_set(self, mock_update):
        updated_attrs = _make_group_attrs(level="ERROR")
        updated_resource = _make_resource(updated_attrs)
        updated_parsed = _make_parsed(updated_resource)
        mock_update.return_value = _ok_response(updated_parsed)

        mgmt = _new_async_mgmt()
        group = AsyncSmplLogGroup(
            mgmt.log_groups,
            id=_TEST_UUID,
            name="DB Loggers",
            level=LogLevel.WARN,
            created_at="2026-01-01T00:00:00Z",
        )
        group.level = LogLevel.ERROR
        asyncio.run(group.save())

        mock_update.assert_called_once()
        assert group.level == LogLevel.ERROR

    @patch("smplkit.logging.client.update_log_group.asyncio_detailed")
    def test_save_null_parsed_raises_validation(self, mock_update):
        mock_update.return_value = _ok_response(None)
        mgmt = _new_async_mgmt()
        group = AsyncSmplLogGroup(
            mgmt.log_groups,
            id=_TEST_UUID,
            name="DB Loggers",
            level=LogLevel.ERROR,
            created_at="2026-01-01T00:00:00Z",
        )
        with pytest.raises(ValidationError):
            asyncio.run(group.save())


# ---------------------------------------------------------------------------
# delete_group(id) — direct delete via delete_log_group
# ---------------------------------------------------------------------------


class TestAsyncDeleteGroup:
    @patch("smplkit.logging.client.delete_log_group.asyncio_detailed")
    def test_delete_group_by_id(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NO_CONTENT)

        mgmt = _new_async_mgmt()
        asyncio.run(mgmt.log_groups.delete("db-loggers"))
        mock_delete.assert_called_once()
        assert mock_delete.call_args.args[0] == "db-loggers"

    @patch("smplkit.logging.client.delete_log_group.asyncio_detailed")
    def test_delete_group_not_found(self, mock_delete):
        mock_delete.return_value = _ok_response(status=HTTPStatus.NOT_FOUND)
        mgmt = _new_async_mgmt()
        with pytest.raises(NotFoundError):
            asyncio.run(mgmt.log_groups.delete("nonexistent"))


# ---------------------------------------------------------------------------
# Async model convenience methods
# ---------------------------------------------------------------------------


class TestAsyncLoggerConvenienceMethods:
    def test_set_level(self):
        lg = AsyncSmplLogger(None, id="sql", name="SQL Logger")
        lg.set_level(LogLevel.ERROR)
        assert lg.level == "ERROR"

    def test_clear_level(self):
        lg = AsyncSmplLogger(None, id="sql", name="SQL Logger", level="DEBUG")
        lg.clear_level()
        assert lg.level is None

    def test_setEnvironmentLevel(self):
        lg = AsyncSmplLogger(None, id="sql", name="SQL Logger")
        lg.set_level(LogLevel.WARN, environment="prod")
        assert lg.environments["prod"].level == LogLevel.WARN

    def test_clearEnvironmentLevel(self):
        lg = AsyncSmplLogger(None, id="sql", name="SQL Logger", environments={"prod": {"level": "WARN"}})
        lg.clear_level(environment="prod")
        assert "prod" not in lg.environments

    def test_clearEnvironmentLevel_missing_key(self):
        lg = AsyncSmplLogger(None, id="sql", name="SQL Logger")
        lg.clear_level(environment="nonexistent")

    def test_clearAllEnvironmentLevels(self):
        lg = AsyncSmplLogger(
            None, id="sql", name="SQL Logger", environments={"prod": {"level": "WARN"}, "dev": {"level": "DEBUG"}}
        )
        lg.clear_all_environment_levels()
        assert lg.environments == {}


class TestAsyncLogGroupConvenienceMethods:
    def test_set_level(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB")
        grp.set_level(LogLevel.ERROR)
        assert grp.level == "ERROR"

    def test_clear_level(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB", level="WARN")
        grp.clear_level()
        assert grp.level is None

    def test_setEnvironmentLevel(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB")
        grp.set_level(LogLevel.DEBUG, environment="staging")
        assert grp.environments["staging"].level == LogLevel.DEBUG

    def test_clearEnvironmentLevel(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB", environments={"staging": {"level": "DEBUG"}})
        grp.clear_level(environment="staging")
        assert "staging" not in grp.environments

    def test_clearEnvironmentLevel_missing_key(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB")
        grp.clear_level(environment="nonexistent")

    def test_clearAllEnvironmentLevels(self):
        grp = AsyncSmplLogGroup(None, id="db", name="DB", environments={"a": {}, "b": {}})
        grp.clear_all_environment_levels()
        assert grp.environments == {}


# ---------------------------------------------------------------------------
# start() — async wrapper for _connect_internal()
# ---------------------------------------------------------------------------


class TestAsyncStart:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_install_connects(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        asyncio.run(client.install())
        assert client._connected is True
        client._close()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_install_is_idempotent(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        asyncio.run(client.install())
        asyncio.run(client.install())
        mock_auto_load.assert_called_once()
        client._close()


# ---------------------------------------------------------------------------
# on_change — dual-mode decorator
# ---------------------------------------------------------------------------


class TestAsyncOnChange:
    def test_bare_decorator_global(self):
        client = _make_async_logging_client()

        @client.on_change
        def handler():
            pass

        assert handler in client._global_listeners

    def test_key_scoped_decorator(self):
        client = _make_async_logging_client()

        @client.on_change("sqlalchemy.engine")
        def handler():
            pass

        assert handler in client._key_listeners["sqlalchemy.engine"]

    def test_parens_no_args_global(self):
        client = _make_async_logging_client()

        @client.on_change()
        def handler():
            pass

        assert handler in client._global_listeners

    def test_returns_original_function(self):
        client = _make_async_logging_client()

        @client.on_change("key")
        def my_fn():
            pass

        assert my_fn.__name__ == "my_fn"


# ---------------------------------------------------------------------------
# Connect flow
# ---------------------------------------------------------------------------


class TestAsyncConnectFlow:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_connect_full_flow(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = [("root", 30, 30), ("myapp.db", 10, 10)]
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        asyncio.run(client._connect_internal())

        assert client._connected is True
        mock_adapter.discover.assert_called_once()
        mock_adapter.install_hook.assert_called_once()
        mock_bulk.assert_called_once()
        client._close()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_connect_with_service(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = [("root", 30, 30)]
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client(service="api-gateway")
        asyncio.run(client._connect_internal())

        assert client._connected is True
        client._close()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_connect_fetch_failure_is_resilient(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.side_effect = Exception("network error")

        client = _make_async_logging_client()
        asyncio.run(client._connect_internal())
        assert client._connected is True
        client._close()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_connect_idempotent(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        asyncio.run(client._connect_internal())
        asyncio.run(client._connect_internal())
        mock_auto_load.assert_called_once()
        client._close()


# ---------------------------------------------------------------------------
# Refresh
# ---------------------------------------------------------------------------


class TestAsyncRefresh:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_refresh_fetches_and_applies(self, mock_loggers, mock_groups):
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        client._connected = True
        asyncio.run(client.refresh())
        mock_loggers.assert_called_once()
        mock_groups.assert_called_once()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_refresh_without_connect_works(self, mock_loggers, mock_groups):
        """refresh() no longer raises SmplNotConnectedError."""
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        assert client._connected is False
        asyncio.run(client.refresh())
        mock_loggers.assert_called_once()


# ---------------------------------------------------------------------------
# Bulk flush
# ---------------------------------------------------------------------------


class TestAsyncBulkFlush:
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_async_flush(self, mock_bulk):
        mock_bulk.return_value = _ok_response()
        client = _make_async_logging_client()
        client._parent.manage.loggers._buffer.add("com.test", "INFO", "INFO", None, None)
        asyncio.run(client._flush_bulk_async())
        mock_bulk.assert_called_once()

    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_async_flush_empty(self, mock_bulk):
        client = _make_async_logging_client()
        asyncio.run(client._flush_bulk_async())
        mock_bulk.assert_not_called()

    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_async_flush_error_swallowed(self, mock_bulk):
        mock_bulk.side_effect = Exception("fail")
        client = _make_async_logging_client()
        client._parent.manage.loggers._buffer.add("com.test", "INFO", "INFO", None, None)
        asyncio.run(client._flush_bulk_async())

    @patch("smplkit.management.client._gen_bulk_register_loggers.sync_detailed")
    def test_mgmt_flush_sync_drains_buffer(self, mock_bulk):
        """``mgmt.loggers.flush_sync()`` drains the buffer the runtime populated."""
        mock_bulk.return_value = _ok_response()
        client = _make_async_logging_client()
        client._parent.manage.loggers._buffer.add("com.test", "INFO", "INFO", None, None)
        client._parent.manage.loggers.flush_sync()
        mock_bulk.assert_called_once()

    @patch("smplkit.management.client._gen_bulk_register_loggers.sync_detailed")
    def test_mgmt_flush_sync_empty(self, mock_bulk):
        client = _make_async_logging_client()
        client._parent.manage.loggers.flush_sync()
        mock_bulk.assert_not_called()

    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_async_flush_logs_warning_on_http_error(self, mock_bulk, caplog):
        import logging as stdlib_logging

        mock_bulk.return_value = _ok_response(status=HTTPStatus.BAD_REQUEST)
        mock_bulk.return_value.content = b'{"errors":[{"detail":"bad"}]}'
        client = _make_async_logging_client()
        client._parent.manage.loggers._buffer.add("com.test", "INFO", "INFO", None, None)
        with caplog.at_level(stdlib_logging.WARNING, logger="smplkit"):
            asyncio.run(client._flush_bulk_async())
        assert len(caplog.records) == 1
        assert "400" in caplog.records[0].message
        assert caplog.records[0].levelno == stdlib_logging.WARNING


# ---------------------------------------------------------------------------
# On new logger callback
# ---------------------------------------------------------------------------


class TestAsyncOnNewLogger:
    def test_callback_adds_to_buffer(self):
        client = _make_async_logging_client()
        client._on_new_logger("my.new.logger", 20, 20)
        assert client._parent.manage.loggers._buffer.pending_count == 1
        assert "my.new.logger" in client._name_map

    def test_callback_applies_level_when_connected(self):
        client = _make_async_logging_client()
        client._connected = True
        test_name = "test.async.on_new.managed_xyz"
        mock_adapter = MagicMock()
        client._adapters = [mock_adapter]
        client._loggers_cache = {
            test_name: {
                "level": "ERROR",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        client._groups_cache = {}
        client._on_new_logger(test_name, 20, 20)
        mock_adapter.apply_level.assert_called_once_with(test_name, 40)


# ---------------------------------------------------------------------------
# Level application
# ---------------------------------------------------------------------------


class TestAsyncLevelApplication:
    def test_apply_levels_managed(self):
        client = _make_async_logging_client()
        test_name = "test.async.apply.managed_111"
        mock_adapter = MagicMock()
        client._adapters = [mock_adapter]
        client._name_map[test_name] = test_name
        client._loggers_cache = {
            test_name: {
                "level": "WARN",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        client._groups_cache = {}
        client._apply_levels()
        mock_adapter.apply_level.assert_called_once_with(test_name, 30)

    def test_apply_levels_unmanaged_skipped(self):
        client = _make_async_logging_client()
        test_name = "test.async.apply.unmanaged_222"
        mock_adapter = MagicMock()
        client._adapters = [mock_adapter]
        client._name_map[test_name] = test_name
        client._loggers_cache = {
            test_name: {
                "level": "ERROR",
                "group": None,
                "managed": False,
                "environments": {},
            }
        }
        client._groups_cache = {}
        client._apply_levels()
        mock_adapter.apply_level.assert_not_called()

    def test_apply_levels_not_in_runtime_skipped(self):
        client = _make_async_logging_client()
        client._loggers_cache = {
            "some.remote": {
                "level": "ERROR",
                "group": None,
                "managed": True,
                "environments": {},
            }
        }
        client._groups_cache = {}
        client._apply_levels()  # Should not raise


# ---------------------------------------------------------------------------
# Close
# ---------------------------------------------------------------------------


class TestAsyncClose:
    def test_close_uninstalls_adapters(self):
        client = _make_async_logging_client()
        adapter = MagicMock()
        client._adapters = [adapter]
        client._close()
        adapter.uninstall_hook.assert_called_once()


# ---------------------------------------------------------------------------
# Fetch and apply
# ---------------------------------------------------------------------------


class TestAsyncFetchAndApply:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_fetches_and_caches(self, mock_loggers, mock_groups):
        logger_attrs = _make_logger_attrs(managed=True)
        logger_resource = _make_resource(logger_attrs, id="com.test")
        mock_loggers.return_value = _ok_response(_make_list_parsed([logger_resource]))

        group_attrs = _make_group_attrs()
        group_resource = _make_resource(group_attrs, id="grp-1")
        mock_groups.return_value = _ok_response(_make_list_parsed([group_resource]))

        client = _make_async_logging_client()
        asyncio.run(client._fetch_and_apply())

        assert "com.test" in client._loggers_cache
        assert "grp-1" in client._groups_cache

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_group_parent_id_stored_as_group_key(self, mock_loggers, mock_groups):
        """groups_cache['group'] must come from parent_id, not a nonexistent 'group' attr."""
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))

        group_attrs = _make_group_attrs(parent_id="parent-grp-id")
        group_resource = _make_resource(group_attrs, id="child-grp")
        mock_groups.return_value = _ok_response(_make_list_parsed([group_resource]))

        client = _make_async_logging_client()
        asyncio.run(client._fetch_and_apply())

        assert client._groups_cache["child-grp"]["group"] == "parent-grp-id"


# ---------------------------------------------------------------------------
# WebSocket event handling
# ---------------------------------------------------------------------------


class TestWebSocketEventHandling:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    @patch("smplkit.logging.client._auto_load_adapters")
    def test_connect_registers_ws_handlers(self, mock_auto_load, mock_bulk, mock_loggers, mock_groups):
        """_connect_internal registers handlers for all five logger events."""
        mock_adapter = MagicMock()
        mock_adapter.discover.return_value = []
        mock_auto_load.return_value = [mock_adapter]
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        mock_ws = MagicMock()
        client._parent._ensure_ws.return_value = mock_ws

        asyncio.run(client._connect_internal())

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

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_handle_loggers_changed_triggers_refetch_in_thread(self, mock_loggers, mock_groups):
        """_handle_loggers_changed spawns a thread that runs _fetch_and_apply."""
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        client._handle_loggers_changed({})

        # Give the daemon thread time to run
        import time

        time.sleep(0.2)

        mock_loggers.assert_called_once()
        mock_groups.assert_called_once()

    def test_close_deregisters_ws_handlers(self):
        """_close calls off() for all five events on the ws manager."""
        client = _make_async_logging_client()
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

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_handle_loggers_changed_swallows_fetch_errors(self, mock_loggers, mock_groups):
        """_handle_loggers_changed catches exceptions from the async _fetch_and_apply thread."""
        mock_loggers.side_effect = RuntimeError("network failure")

        client = _make_async_logging_client()
        # Should not raise; the error is caught inside the daemon thread
        client._handle_loggers_changed({})

        import time

        time.sleep(0.2)  # let thread finish

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_handle_loggers_changed_successive_events_no_event_loop_error(self, mock_loggers, mock_groups):
        """Successive loggers_changed events must not raise 'RuntimeError: Event loop is closed'.

        Regression test: previously _fetch_and_apply reused self._logging_http
        (a shared AuthenticatedClient) across different temporary event loops.
        The httpx AsyncClient caches asyncio transports bound to the first loop;
        when that loop is closed and a second loop reuses the same client,
        cleanup callbacks fire against the now-closed loop.
        """
        import time

        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()

        client._handle_loggers_changed({})
        client._handle_loggers_changed({})

        time.sleep(0.4)  # let both daemon threads finish

        # Both events must have triggered a full refresh cycle.
        assert mock_loggers.call_count == 2
        assert mock_groups.call_count == 2

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.logging.client.AuthenticatedClient")
    def test_handle_loggers_changed_closes_fresh_http_client(self, mock_ac_cls, mock_loggers, mock_groups):
        """The underlying httpx AsyncClient of the fresh client is closed after loggers_changed refresh."""
        import time

        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        # Provide a mock http instance with a non-None _async_client so that the
        # `if ac is not None: await ac.aclose()` branch is exercised.
        mock_async_client = AsyncMock()
        mock_http_instance = MagicMock()
        mock_http_instance._async_client = mock_async_client
        mock_ac_cls.return_value = mock_http_instance

        # _make_async_logging_client() opens its own nested patch for AuthenticatedClient
        # (to set up _logging_http), temporarily overriding mock_ac_cls.  After it
        # exits the constructor, mock_ac_cls is restored and is what _handle_loggers_changed
        # will see when it calls AuthenticatedClient(...).
        client = _make_async_logging_client()
        client._handle_loggers_changed({})

        time.sleep(0.3)  # let the daemon thread finish

        mock_async_client.aclose.assert_called_once()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_handle_loggers_changed_uses_fresh_http_client(self, mock_loggers, mock_groups):
        """loggers_changed refresh must use a fresh AuthenticatedClient, not self._logging_http."""
        import time

        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_logging_client()
        client._handle_loggers_changed({})

        time.sleep(0.2)

        mock_loggers.assert_called_once()
        # The client passed to the API call must NOT be self._logging_http;
        # it must be a fresh AuthenticatedClient scoped to the thread's event loop.
        call_client = mock_loggers.call_args.kwargs.get("client") or mock_loggers.call_args.args[0]
        assert call_client is not client._logging_http

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_handle_logger_changed_spawns_thread_and_fires(self, mock_get):
        """_handle_logger_changed spawns a thread that fetches and fires once per affected logger."""
        import time
        from smplkit.logging.client import LoggerResponse, LoggerResource, GenLogger
        from smplkit._generated.logging.types import UNSET

        attrs = GenLogger(name="sqlalchemy.engine", level="INFO", group=UNSET, managed=True, environments=UNSET)
        resource = LoggerResource(attributes=attrs, id="sqlalchemy.engine", type_="logger")
        parsed = LoggerResponse(data=resource)
        resp = MagicMock()
        resp.status_code = HTTPStatus.OK
        resp.content = b""
        resp.parsed = parsed
        mock_get.return_value = resp

        client = _make_async_logging_client()
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
        time.sleep(0.3)
        mock_get.assert_called_once()
        listener.assert_called_once()
        assert listener.call_args[0][0].level == "INFO"

    def test_handle_logger_deleted_fires_no_event_for_deleted_key(self):
        """_handle_logger_deleted: deleted logger itself fires no listener."""
        import time

        client = _make_async_logging_client()
        client._name_map["sqlalchemy.engine"] = "sqlalchemy.engine"
        client._loggers_cache["sqlalchemy.engine"] = {
            "level": "DEBUG",
            "group": None,
            "managed": True,
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        client._handle_logger_deleted({"id": "sqlalchemy.engine"})
        time.sleep(0.3)
        assert "sqlalchemy.engine" not in client._loggers_cache
        listener.assert_not_called()

    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_handle_group_changed_cascades_to_dependent_logger(self, mock_get):
        """_handle_group_changed cascades to a logger that inherits from the group."""
        import time
        from smplkit.logging.client import LogGroupResponse, LogGroupResource, GenLogGroup
        from smplkit._generated.logging.types import UNSET

        attrs = GenLogGroup(name="db-loggers", level="ERROR", parent_id=UNSET, environments=UNSET)
        resource = LogGroupResource(attributes=attrs, id="db-loggers", type_="log_group")
        parsed = LogGroupResponse(data=resource)
        resp = MagicMock()
        resp.status_code = HTTPStatus.OK
        resp.content = b""
        resp.parsed = parsed
        mock_get.return_value = resp

        client = _make_async_logging_client()
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
        time.sleep(0.3)
        mock_get.assert_called_once()
        global_listener.assert_called_once()
        assert global_listener.call_args[0][0].id == "app.db"
        assert global_listener.call_args[0][0].level == "ERROR"
        key_listener.assert_called_once()

    def test_handle_group_deleted_cascade_no_event_for_group_key(self):
        """_handle_group_deleted cascades to dependent loggers; no event for the group id."""
        import time

        client = _make_async_logging_client()
        client._name_map["app.db"] = "app.db"
        client._groups_cache["db-loggers"] = {"level": "WARN", "group": None, "environments": {}}
        client._loggers_cache["app.db"] = {
            "level": None,
            "group": "db-loggers",
            "managed": True,
            "environments": {},
        }
        group_key_listener = MagicMock()
        client._key_listeners["db-loggers"] = [group_key_listener]
        logger_listener = MagicMock()
        client._key_listeners["app.db"] = [logger_listener]
        client._handle_group_deleted({"id": "db-loggers"})
        time.sleep(0.3)
        assert "db-loggers" not in client._groups_cache
        group_key_listener.assert_not_called()
        logger_listener.assert_called_once()
        assert logger_listener.call_args[0][0].id == "app.db"
        assert logger_listener.call_args[0][0].level == "INFO"

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_async_global_listener_exception_swallowed(self, mock_get):
        """Async fire path swallows exceptions from global listeners."""
        import time
        from smplkit.logging.client import LoggerResponse, LoggerResource, GenLogger
        from smplkit._generated.logging.types import UNSET

        attrs = GenLogger(name="sqlalchemy.engine", level="INFO", group=UNSET, managed=True, environments=UNSET)
        resource = LoggerResource(attributes=attrs, id="sqlalchemy.engine", type_="logger")
        parsed = LoggerResponse(data=resource)
        resp = MagicMock()
        resp.status_code = HTTPStatus.OK
        resp.content = b""
        resp.parsed = parsed
        mock_get.return_value = resp

        client = _make_async_logging_client()
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
        time.sleep(0.3)
        good.assert_called_once()

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_async_key_listener_exception_swallowed(self, mock_get):
        """Async fire path swallows exceptions from per-key listeners."""
        import time
        from smplkit.logging.client import LoggerResponse, LoggerResource, GenLogger
        from smplkit._generated.logging.types import UNSET

        attrs = GenLogger(name="sqlalchemy.engine", level="INFO", group=UNSET, managed=True, environments=UNSET)
        resource = LoggerResource(attributes=attrs, id="sqlalchemy.engine", type_="logger")
        parsed = LoggerResponse(data=resource)
        resp = MagicMock()
        resp.status_code = HTTPStatus.OK
        resp.content = b""
        resp.parsed = parsed
        mock_get.return_value = resp

        client = _make_async_logging_client()
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
        time.sleep(0.3)
        good.assert_called_once()

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_handle_logger_changed_fetch_error_swallowed(self, mock_get):
        """_fetch_logger_and_apply catches exceptions from asyncio_detailed and returns."""
        import time

        mock_get.side_effect = RuntimeError("fetch failed")
        client = _make_async_logging_client()
        client._handle_logger_changed({"id": "sqlalchemy.engine"})
        time.sleep(0.3)  # should not raise

    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_handle_group_changed_fetch_error_swallowed(self, mock_get):
        """_fetch_group_and_apply catches exceptions from asyncio_detailed and returns."""
        import time

        mock_get.side_effect = RuntimeError("fetch failed")
        client = _make_async_logging_client()
        client._handle_group_changed({"id": "db-loggers"})
        time.sleep(0.3)  # should not raise

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    @patch("smplkit.logging.client.AuthenticatedClient")
    def test_handle_logger_changed_closes_fresh_http_client(self, mock_ac_cls, mock_get):
        """_run_ws_handler closes the fresh http client's _async_client after fetch."""
        import time

        resp = MagicMock()
        resp.status_code = HTTPStatus.OK
        resp.content = b""
        resp.parsed = None
        mock_get.return_value = resp

        mock_async_client = AsyncMock()
        mock_http_instance = MagicMock()
        mock_http_instance._async_client = mock_async_client
        mock_ac_cls.return_value = mock_http_instance

        client = _make_async_logging_client()
        client._handle_logger_changed({"id": "sqlalchemy.engine"})
        time.sleep(0.3)
        mock_async_client.aclose.assert_called_once()

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_handle_logger_changed_apply_error_swallowed(self, mock_get):
        """_run_ws_handler swallows exceptions from _apply_deltas_and_fire."""
        import time
        from smplkit.logging.client import LoggerResponse, LoggerResource, GenLogger
        from smplkit._generated.logging.types import UNSET

        attrs = GenLogger(name="sqlalchemy.engine", level="INFO", group=UNSET, managed=True, environments=UNSET)
        resource = LoggerResource(attributes=attrs, id="sqlalchemy.engine", type_="logger")
        parsed = LoggerResponse(data=resource)
        resp = MagicMock()
        resp.status_code = HTTPStatus.OK
        resp.content = b""
        resp.parsed = parsed
        mock_get.return_value = resp

        client = _make_async_logging_client()
        with patch.object(client, "_apply_deltas_and_fire", side_effect=RuntimeError("apply failed")):
            client._handle_logger_changed({"id": "sqlalchemy.engine"})
            time.sleep(0.3)  # should not raise

    def test_handle_logger_deleted_apply_error_swallowed(self):
        """logger_deleted thread swallows exceptions from _apply_deltas_and_fire."""
        import time

        client = _make_async_logging_client()
        client._loggers_cache["sqlalchemy.engine"] = {"level": "DEBUG"}
        with patch.object(client, "_apply_deltas_and_fire", side_effect=RuntimeError("apply failed")):
            client._handle_logger_deleted({"id": "sqlalchemy.engine"})
            time.sleep(0.3)  # should not raise

    def test_handle_group_deleted_apply_error_swallowed(self):
        """group_deleted thread swallows exceptions from _apply_deltas_and_fire."""
        import time

        client = _make_async_logging_client()
        client._groups_cache["db-loggers"] = {"level": "WARN"}
        with patch.object(client, "_apply_deltas_and_fire", side_effect=RuntimeError("apply failed")):
            client._handle_group_deleted({"id": "db-loggers"})
            time.sleep(0.3)  # should not raise

    def test_async_snapshot_skips_loggers_not_in_cache_or_unmanaged(self):
        """Async _snapshot_effective_levels mirrors the sync filter behavior."""
        client = _make_async_logging_client()
        client._name_map["app.unknown"] = "app.unknown"
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

    def test_async_apply_deltas_skips_unchanged_loggers(self):
        """A logger whose effective level matches ``pre`` is skipped (no apply, no fire)."""
        client = _make_async_logging_client()
        client._name_map["app.db"] = "app.db"
        client._loggers_cache["app.db"] = {
            "level": "WARN",
            "group": None,
            "managed": True,
            "environments": {},
        }
        listener = MagicMock()
        client._global_listeners.append(listener)
        # pre matches the current resolved level → continue branch, no fire.
        client._apply_deltas_and_fire({"app.db": "WARN"}, "websocket")
        listener.assert_not_called()

    def test_async_apply_deltas_swallows_adapter_exception(self):
        """A misbehaving adapter is logged and the async fire path continues."""
        client = _make_async_logging_client()
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
        client._apply_deltas_and_fire({}, "websocket")
        bad_adapter.apply_level.assert_called_once()
        listener.assert_called_once()


# ---------------------------------------------------------------------------
# AsyncLoggingManagementClient.register / flush — buffered registration
# ---------------------------------------------------------------------------


class TestAsyncRegisterAndFlush:
    def test_register_then_flush_sends_batch(self):
        from smplkit.logging._sources import LoggerSource

        async def _run():
            mock_coro = AsyncMock(return_value=MagicMock(status_code=200, content=b"{}"))
            with patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed", mock_coro):
                mgmt = _new_async_mgmt()
                mgmt.loggers.register(
                    [
                        LoggerSource(
                            name="sqlalchemy.engine",
                            service="api",
                            environment="production",
                            resolved_level=LogLevel.WARN,
                        ),
                    ]
                )
                await mgmt.loggers.flush()
                mock_coro.assert_called_once()
                _, kwargs = mock_coro.call_args
                assert kwargs["body"].loggers[0].service == "api"

        asyncio.run(_run())

    def test_register_includes_explicit_level(self):
        from smplkit.logging._sources import LoggerSource

        async def _run():
            mock_coro = AsyncMock(return_value=MagicMock(status_code=200, content=b"{}"))
            with patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed", mock_coro):
                mgmt = _new_async_mgmt()
                mgmt.loggers.register(
                    [
                        LoggerSource(
                            name="httpx",
                            service="svc",
                            environment="staging",
                            resolved_level=LogLevel.INFO,
                            level=LogLevel.DEBUG,
                        ),
                    ]
                )
                await mgmt.loggers.flush()
                _, kwargs = mock_coro.call_args
                assert kwargs["body"].loggers[0].level == "DEBUG"

        asyncio.run(_run())

    def test_flush_with_empty_buffer_skips_call(self):
        async def _run():
            mock_coro = AsyncMock(return_value=MagicMock(status_code=200, content=b"{}"))
            with patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed", mock_coro):
                mgmt = _new_async_mgmt()
                await mgmt.loggers.flush()
                mock_coro.assert_not_called()

        asyncio.run(_run())

    def test_flush_propagates_unexpected_errors(self):
        from smplkit.logging._sources import LoggerSource

        async def _run():
            mock_coro = AsyncMock(side_effect=RuntimeError("unexpected"))
            with patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed", mock_coro):
                mgmt = _new_async_mgmt()
                mgmt.loggers.register(
                    [
                        LoggerSource("app", service="svc", environment="prod", resolved_level=LogLevel.INFO),
                    ]
                )
                with pytest.raises(RuntimeError):
                    await mgmt.loggers.flush()

        asyncio.run(_run())
