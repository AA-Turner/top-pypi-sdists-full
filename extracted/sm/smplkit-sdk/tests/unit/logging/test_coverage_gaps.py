"""Tests targeting specific uncovered lines in logging/client.py."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import httpx
import pytest

from smplkit._errors import ConnectionError
from smplkit.logging.client import (
    AsyncLoggingClient,
    AsyncSmplLogGroup,
    AsyncSmplLogger,
    LoggingClient,
    SmplLogGroup,
    SmplLogger,
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


def _make_group_attrs(*, name="DB", level="WARN", parent_id=None):
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


def _make_sync_client(**kwargs):
    from smplkit.management.client import LoggersClient as _MgmtLoggersClient

    parent = MagicMock()
    parent._api_key = "sk_test"
    parent._environment = "test"
    parent._service = kwargs.get("service", None)
    manage = MagicMock()
    manage.loggers = _MgmtLoggersClient(MagicMock(), base_url="http://logging:8003")
    parent.manage = manage
    with patch("smplkit.logging.client.AuthenticatedClient"):
        return LoggingClient(parent, manage=manage, metrics=parent._metrics)


def _make_async_client(**kwargs):
    from smplkit.management.client import AsyncLoggersClient as _MgmtAsyncLoggersClient

    parent = MagicMock()
    parent._api_key = "sk_test"
    parent._environment = "test"
    parent._service = kwargs.get("service", None)
    manage = MagicMock()
    manage.loggers = _MgmtAsyncLoggersClient(MagicMock(), base_url="http://logging:8003")
    parent.manage = manage
    with patch("smplkit.logging.client.AuthenticatedClient"):
        return AsyncLoggingClient(parent, manage=manage, metrics=parent._metrics)


# ---------------------------------------------------------------------------
# Bare `raise` after _maybe_reraise_network_error (non-httpx exceptions)
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


class TestSyncBareRaise:
    """Cover the `raise` line after _maybe_reraise_network_error for non-httpx errors."""

    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    def test_list_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.loggers.list()

    @patch("smplkit.logging.client.get_logger.sync_detailed")
    def test_get_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.loggers.get("sql")

    @patch("smplkit.logging.client.update_logger.sync_detailed")
    def test_save_logger_unknown_error(self, mock_update):
        mock_update.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        lg = SmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.loggers._save_logger(lg)

    @patch("smplkit.logging.client.update_logger.sync_detailed")
    def test_save_logger_create_upsert_unknown_error(self, mock_update):
        mock_update.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        lg = SmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger")
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.loggers._save_logger(lg)

    @patch("smplkit.logging.client.delete_logger.sync_detailed")
    def test_delete_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.loggers.delete("sql")

    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    def test_list_groups_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.log_groups.list()

    @patch("smplkit.logging.client.get_log_group.sync_detailed")
    def test_get_group_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.log_groups.get("db")

    @patch("smplkit.logging.client.update_log_group.sync_detailed")
    def test_save_group_unknown_error(self, mock_update):
        mock_update.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        grp = SmplLogGroup(mgmt.log_groups, id=_TEST_UUID, name="DB", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.log_groups._save_group(grp)

    @patch("smplkit.logging.client.create_log_group.sync_detailed")
    def test_save_group_create_unknown_error(self, mock_create):
        mock_create.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        grp = SmplLogGroup(mgmt.log_groups, id=None, name="DB")
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.log_groups._save_group(grp)

    @patch("smplkit.logging.client.delete_log_group.sync_detailed")
    def test_delete_group_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            mgmt.log_groups.delete("db")


class TestAsyncBareRaise:
    """Cover the bare `raise` after _maybe_reraise_network_error for async methods."""

    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_list_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.loggers.list())

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_get_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.loggers.get("sql"))

    @patch("smplkit.logging.client.delete_logger.asyncio_detailed")
    def test_delete_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.loggers.delete("sql"))

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    def test_list_groups_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.log_groups.list())

    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_get_group_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.log_groups.get("db"))

    @patch("smplkit.logging.client.delete_log_group.asyncio_detailed")
    def test_delete_group_unknown_error(self, mock):
        mock.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.log_groups.delete("db"))

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_logger_unknown_error(self, mock_update):
        mock_update.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        lg = AsyncSmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.loggers._save_logger(lg))

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_logger_create_upsert_unknown_error(self, mock_update):
        mock_update.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        lg = AsyncSmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger")
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.loggers._save_logger(lg))

    @patch("smplkit.logging.client.update_log_group.asyncio_detailed")
    def test_save_group_unknown_error(self, mock_update):
        mock_update.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        grp = AsyncSmplLogGroup(mgmt.log_groups, id=_TEST_UUID, name="DB", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.log_groups._save_group(grp))

    @patch("smplkit.logging.client.create_log_group.asyncio_detailed")
    def test_save_group_create_unknown_error(self, mock_create):
        mock_create.side_effect = RuntimeError("boom")
        mgmt = _new_async_mgmt()
        grp = AsyncSmplLogGroup(mgmt.log_groups, id=None, name="DB")
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(mgmt.log_groups._save_group(grp))


# ---------------------------------------------------------------------------
# _fetch_and_apply: list_log_groups failure
# ---------------------------------------------------------------------------


class TestFetchAndApplyGroupFailure:
    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    def test_sync_groups_fetch_network_error(self, mock_loggers, mock_groups):
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.side_effect = httpx.ConnectError("refused")
        client = _make_sync_client()
        with pytest.raises(ConnectionError):
            client._fetch_and_apply()

    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    def test_sync_groups_fetch_unknown_error(self, mock_loggers, mock_groups):
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.side_effect = RuntimeError("boom")
        client = _make_sync_client()
        with pytest.raises(RuntimeError, match="boom"):
            client._fetch_and_apply()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_async_groups_fetch_network_error(self, mock_loggers, mock_groups):
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.side_effect = httpx.ConnectError("refused")
        client = _make_async_client()
        with pytest.raises(ConnectionError):
            asyncio.run(client._fetch_and_apply())

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_async_groups_fetch_unknown_error(self, mock_loggers, mock_groups):
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.side_effect = RuntimeError("boom")
        client = _make_async_client()
        with pytest.raises(RuntimeError, match="boom"):
            asyncio.run(client._fetch_and_apply())


# ---------------------------------------------------------------------------
# Async network error paths (httpx exceptions)
# ---------------------------------------------------------------------------


class TestAsyncNetworkErrors:
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    def test_list_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.loggers.list())

    @patch("smplkit.logging.client.get_logger.asyncio_detailed")
    def test_get_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.loggers.get("sql"))

    @patch("smplkit.logging.client.delete_logger.asyncio_detailed")
    def test_delete_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.loggers.delete("sql"))

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_logger_create_upsert_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        lg = AsyncSmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger")
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.loggers._save_logger(lg))

    @patch("smplkit.logging.client.update_logger.asyncio_detailed")
    def test_save_logger_update_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        lg = AsyncSmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.loggers._save_logger(lg))

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    def test_list_groups_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.log_groups.list())

    @patch("smplkit.logging.client.get_log_group.asyncio_detailed")
    def test_get_group_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.log_groups.get("db"))

    @patch("smplkit.logging.client.delete_log_group.asyncio_detailed")
    def test_delete_group_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.log_groups.delete("db"))

    @patch("smplkit.logging.client.create_log_group.asyncio_detailed")
    def test_save_group_create_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        grp = AsyncSmplLogGroup(mgmt.log_groups, id=None, name="DB")
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.log_groups._save_group(grp))

    @patch("smplkit.logging.client.update_log_group.asyncio_detailed")
    def test_save_group_update_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_async_mgmt()
        grp = AsyncSmplLogGroup(mgmt.log_groups, id=_TEST_UUID, name="DB", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(ConnectionError):
            asyncio.run(mgmt.log_groups._save_group(grp))


# ---------------------------------------------------------------------------
# Sync network error paths
# ---------------------------------------------------------------------------


class TestSyncNetworkErrors:
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    def test_list_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.loggers.list()

    @patch("smplkit.logging.client.get_logger.sync_detailed")
    def test_get_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.loggers.get("sql")

    @patch("smplkit.logging.client.delete_logger.sync_detailed")
    def test_delete_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.loggers.delete("sql")

    @patch("smplkit.logging.client.update_logger.sync_detailed")
    def test_save_logger_create_upsert_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        lg = SmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger")
        with pytest.raises(ConnectionError):
            mgmt.loggers._save_logger(lg)

    @patch("smplkit.logging.client.update_logger.sync_detailed")
    def test_save_logger_update_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        lg = SmplLogger(mgmt.loggers, id=_TEST_UUID, name="SQL Logger", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(ConnectionError):
            mgmt.loggers._save_logger(lg)

    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    def test_list_groups_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.log_groups.list()

    @patch("smplkit.logging.client.get_log_group.sync_detailed")
    def test_get_group_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.log_groups.get("db")

    @patch("smplkit.logging.client.delete_log_group.sync_detailed")
    def test_delete_group_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.log_groups.delete("db")

    @patch("smplkit.logging.client.create_log_group.sync_detailed")
    def test_save_group_create_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        grp = SmplLogGroup(mgmt.log_groups, id=None, name="DB")
        with pytest.raises(ConnectionError):
            mgmt.log_groups._save_group(grp)

    @patch("smplkit.logging.client.update_log_group.sync_detailed")
    def test_save_group_update_network_error(self, mock):
        mock.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        grp = SmplLogGroup(mgmt.log_groups, id=_TEST_UUID, name="DB", created_at="2026-01-01T00:00:00Z")
        with pytest.raises(ConnectionError):
            mgmt.log_groups._save_group(grp)


class TestConvertEnvironments:
    def test_passthrough_loggerenvironment_instance(self):
        """LoggerEnvironment instances pass through unchanged."""
        from smplkit import LogLevel
        from smplkit.logging.models import LoggerEnvironment, _convert_environments

        env = LoggerEnvironment(level=LogLevel.ERROR)
        result = _convert_environments({"prod": env})
        assert result["prod"] is env

    def test_invalid_level_string_yields_empty_environment(self):
        """An unrecognized level string falls back to a level-less environment."""
        from smplkit.logging.models import _convert_environments

        result = _convert_environments({"prod": {"level": "NOT_A_LEVEL"}})
        assert result["prod"].level is None

    def test_non_dict_non_environment_value_yields_empty_environment(self):
        """A garbage value (str/int) is treated as an empty override."""
        from smplkit.logging.models import _convert_environments

        result = _convert_environments({"prod": "garbage"})
        assert result["prod"].level is None
