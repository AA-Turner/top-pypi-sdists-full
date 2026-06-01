"""Tests for adapter auto-loading and register_adapter()."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from unittest.mock import MagicMock, patch

import pytest

from smplkit.logging.adapters.base import LoggingAdapter
from smplkit.logging.adapters.stdlib_logging import StdlibLoggingAdapter
from smplkit.logging.client import AsyncLoggingClient, LoggingClient, _auto_load_adapters


class _MockAdapter(LoggingAdapter):
    """Minimal adapter for testing."""

    def __init__(self, adapter_name: str = "mock") -> None:
        self._name = adapter_name
        self.discover_calls = 0
        self.install_hook_calls = 0
        self.uninstall_hook_calls = 0
        self.apply_level_calls: list[tuple[str, int]] = []

    @property
    def name(self) -> str:
        return self._name

    def discover(self) -> list[tuple[str, int]]:
        self.discover_calls += 1
        return [("mock.logger", 20)]

    def apply_level(self, logger_name: str, level: int) -> None:
        self.apply_level_calls.append((logger_name, level))

    def install_hook(self, on_new_logger):  # type: ignore[override]
        self.install_hook_calls += 1

    def uninstall_hook(self) -> None:
        self.uninstall_hook_calls += 1


def _ok_response(parsed=None, status=HTTPStatus.OK):
    resp = MagicMock()
    resp.status_code = status
    resp.content = b""
    resp.parsed = parsed
    return resp


def _make_list_parsed(resources):
    parsed = MagicMock()
    parsed.data = resources
    return parsed


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


class TestAutoLoadAdapters:
    def test_finds_stdlib(self):
        mock_ep = MagicMock()
        mock_ep.name = "stdlib"
        mock_ep.load.return_value = StdlibLoggingAdapter
        with patch("smplkit.logging.client.entry_points", return_value=[mock_ep]):
            adapters = _auto_load_adapters()
        assert any(a.name == "stdlib-logging" for a in adapters)

    def test_skips_missing_dependency(self):
        stdlib_ep = MagicMock()
        stdlib_ep.name = "stdlib"
        stdlib_ep.load.return_value = StdlibLoggingAdapter

        loguru_ep = MagicMock()
        loguru_ep.name = "loguru"
        loguru_ep.load.side_effect = ImportError("No module named 'loguru'")

        with patch("smplkit.logging.client.entry_points", return_value=[stdlib_ep, loguru_ep]):
            adapters = _auto_load_adapters()

        names = [a.name for a in adapters]
        assert "stdlib-logging" in names
        assert len(adapters) == 1

    def test_no_adapters_warns(self):
        with patch("smplkit.logging.client.entry_points", return_value=[]):
            import logging

            with patch.object(logging.getLogger("smplkit"), "warning") as mock_warning:
                adapters = _auto_load_adapters()
                assert adapters == []
                mock_warning.assert_called()

    def test_non_import_error_warns(self):
        broken_ep = MagicMock()
        broken_ep.name = "broken"
        broken_ep.load.side_effect = RuntimeError("broken")

        with patch("smplkit.logging.client.entry_points", return_value=[broken_ep]):
            import logging

            with patch.object(logging.getLogger("smplkit"), "warning") as mock_warning:
                adapters = _auto_load_adapters()
                assert adapters == []
                assert mock_warning.call_count >= 1


class TestRegisterAdapter:
    def test_register_disables_auto_load(self):
        client = _make_sync_client()
        mock_adapter = _MockAdapter()
        client.register_adapter(mock_adapter)
        assert client._explicit_adapters is True
        assert len(client._adapters) == 1

    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.sync_detailed")
    def test_registered_adapter_used_on_connect(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_sync_client()
        adapter = _MockAdapter()
        client.register_adapter(adapter)
        client._connect_internal()

        assert adapter.discover_calls == 1
        assert adapter.install_hook_calls == 1
        client._close()

    def test_register_after_install_raises(self):
        client = _make_sync_client()
        client._connected = True
        with pytest.raises(RuntimeError, match="Cannot register adapters after install"):
            client.register_adapter(_MockAdapter())

    def test_async_register_after_install_raises(self):
        client = _make_async_client()
        client._connected = True
        with pytest.raises(RuntimeError, match="Cannot register adapters after install"):
            client.register_adapter(_MockAdapter())

    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.sync_detailed")
    def test_multiple_adapters_all_called(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_sync_client()
        adapter1 = _MockAdapter("first")
        adapter2 = _MockAdapter("second")
        client.register_adapter(adapter1)
        client.register_adapter(adapter2)
        client._connect_internal()

        assert adapter1.discover_calls == 1
        assert adapter2.discover_calls == 1
        assert adapter1.install_hook_calls == 1
        assert adapter2.install_hook_calls == 1

        client._close()
        assert adapter1.uninstall_hook_calls == 1
        assert adapter2.uninstall_hook_calls == 1


class TestAsyncRegisterAdapter:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_registered_adapter_used_on_connect(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        client = _make_async_client()
        adapter = _MockAdapter()
        client.register_adapter(adapter)
        asyncio.run(client._connect_internal())

        assert adapter.discover_calls == 1
        assert adapter.install_hook_calls == 1
        client._close()
        assert adapter.uninstall_hook_calls == 1


class TestAdapterErrorResilience:
    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.sync_detailed")
    def test_discover_failure_does_not_block_connect(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        class FailingAdapter(_MockAdapter):
            def discover(self):  # type: ignore[override]
                raise RuntimeError("discover exploded")

        client = _make_sync_client()
        adapter = FailingAdapter()
        client.register_adapter(adapter)
        client._connect_internal()
        assert client._connected is True
        client._close()

    @patch("smplkit.logging.client.list_log_groups.sync_detailed")
    @patch("smplkit.logging.client.list_loggers.sync_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.sync_detailed")
    def test_install_hook_failure_does_not_block_connect(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        class FailingAdapter(_MockAdapter):
            def install_hook(self, on_new_logger):  # type: ignore[override]
                raise RuntimeError("install_hook exploded")

        client = _make_sync_client()
        adapter = FailingAdapter()
        client.register_adapter(adapter)
        client._connect_internal()
        assert client._connected is True
        client._close()

    def test_uninstall_hook_failure_does_not_block_close(self):
        class FailingAdapter(_MockAdapter):
            def uninstall_hook(self) -> None:
                raise RuntimeError("uninstall_hook exploded")

        client = _make_sync_client()
        adapter = FailingAdapter()
        client._adapters = [adapter]
        client._close()  # Should not raise

    def test_apply_level_failure_does_not_block(self):
        class FailingAdapter(_MockAdapter):
            def apply_level(self, logger_name: str, level: int) -> None:
                raise RuntimeError("apply_level exploded")

        client = _make_sync_client()
        adapter = FailingAdapter()
        client._adapters = [adapter]
        client._loggers_cache = {
            "test.key": {"level": "ERROR", "group": None, "managed": True, "environments": {}},
        }
        client._groups_cache = {}
        client._name_map = {"test.key": "test.key"}
        client._apply_levels()  # Should not raise

    def test_on_new_logger_apply_level_failure_sync(self):
        class FailingAdapter(_MockAdapter):
            def apply_level(self, logger_name: str, level: int) -> None:
                raise RuntimeError("apply_level exploded")

        client = _make_sync_client()
        adapter = FailingAdapter()
        client._adapters = [adapter]
        client._connected = True
        test_name = "test.on_new.fail_sync"
        client._loggers_cache = {
            test_name: {"level": "ERROR", "group": None, "managed": True, "environments": {}},
        }
        client._groups_cache = {}
        client._on_new_logger(test_name, 20, 20)  # Should not raise


class TestAsyncAdapterErrorResilience:
    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_async_discover_failure_does_not_block(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        class FailingAdapter(_MockAdapter):
            def discover(self):  # type: ignore[override]
                raise RuntimeError("discover exploded")

        client = _make_async_client()
        adapter = FailingAdapter()
        client.register_adapter(adapter)
        asyncio.run(client._connect_internal())
        assert client._connected is True
        client._close()

    @patch("smplkit.logging.client.list_log_groups.asyncio_detailed")
    @patch("smplkit.logging.client.list_loggers.asyncio_detailed")
    @patch("smplkit.management.client._gen_bulk_register_loggers.asyncio_detailed")
    def test_async_install_hook_failure_does_not_block(self, mock_bulk, mock_loggers, mock_groups):
        mock_bulk.return_value = _ok_response()
        mock_loggers.return_value = _ok_response(_make_list_parsed([]))
        mock_groups.return_value = _ok_response(_make_list_parsed([]))

        class FailingAdapter(_MockAdapter):
            def install_hook(self, on_new_logger):  # type: ignore[override]
                raise RuntimeError("install_hook exploded")

        client = _make_async_client()
        adapter = FailingAdapter()
        client.register_adapter(adapter)
        asyncio.run(client._connect_internal())
        assert client._connected is True
        client._close()

    def test_async_uninstall_hook_failure_does_not_block(self):
        class FailingAdapter(_MockAdapter):
            def uninstall_hook(self) -> None:
                raise RuntimeError("uninstall_hook exploded")

        client = _make_async_client()
        adapter = FailingAdapter()
        client._adapters = [adapter]
        client._close()  # Should not raise

    def test_async_apply_level_failure_does_not_block(self):
        class FailingAdapter(_MockAdapter):
            def apply_level(self, logger_name: str, level: int) -> None:
                raise RuntimeError("apply_level exploded")

        client = _make_async_client()
        adapter = FailingAdapter()
        client._adapters = [adapter]
        client._loggers_cache = {
            "test.key": {"level": "ERROR", "group": None, "managed": True, "environments": {}},
        }
        client._groups_cache = {}
        client._name_map = {"test.key": "test.key"}
        client._apply_levels()  # Should not raise

    def test_async_on_new_logger_apply_level_failure(self):
        class FailingAdapter(_MockAdapter):
            def apply_level(self, logger_name: str, level: int) -> None:
                raise RuntimeError("apply_level exploded")

        client = _make_async_client()
        adapter = FailingAdapter()
        client._adapters = [adapter]
        client._connected = True
        test_name = "test.on_new.fail_async"
        client._loggers_cache = {
            test_name: {"level": "ERROR", "group": None, "managed": True, "environments": {}},
        }
        client._groups_cache = {}
        client._on_new_logger(test_name, 20, 20)  # Should not raise
