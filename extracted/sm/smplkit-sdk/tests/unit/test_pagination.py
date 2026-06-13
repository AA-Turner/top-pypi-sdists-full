"""Tests that the runtime fetch-all sites loop until short page, and that
management list methods forward ``page_number`` / ``page_size`` through to
the generated client.
"""

from __future__ import annotations

import asyncio
import json
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

from smplkit._generated.flags.types import UNSET as _FLAGS_UNSET
from smplkit._helpers import PAGE_SIZE
from smplkit.clients import AsyncSmplClient, SmplClient


# ---------------------------------------------------------------------------
# Helpers — shared response/resource builders
# ---------------------------------------------------------------------------


def _resp(parsed=None, *, status: int = HTTPStatus.OK, content: bytes = b"") -> MagicMock:
    r = MagicMock()
    r.status_code = status
    r.content = content
    r.parsed = parsed
    return r


def _list_resp(items):
    parsed = MagicMock()
    parsed.data = items
    return _resp(parsed=parsed)


def _config_resource(id_: str) -> MagicMock:
    attrs = MagicMock()
    attrs.name = id_
    attrs.description = None
    attrs.parent = None
    attrs.items = None
    attrs.environments = None
    attrs.created_at = None
    attrs.updated_at = None
    r = MagicMock()
    r.id = id_
    r.attributes = attrs
    return r


def _flag_json_dict(id_: str) -> dict:
    return {
        "id": id_,
        "type": "flag",
        "attributes": {
            "name": id_,
            "type": "BOOLEAN",
            "default": False,
            "values": [{"name": "True", "value": True}, {"name": "False", "value": False}],
            "environments": {},
            "description": "",
            "created_at": None,
            "updated_at": None,
        },
    }


def _json_resp(data: dict) -> MagicMock:
    return _resp(content=json.dumps(data).encode())


def _logger_resource(id_: str) -> MagicMock:
    attrs = MagicMock()
    attrs.level = _FLAGS_UNSET
    attrs.group = _FLAGS_UNSET
    attrs.managed = True
    attrs.environments = _FLAGS_UNSET
    r = MagicMock()
    r.id = id_
    r.attributes = attrs
    return r


def _log_group_resource(id_: str) -> MagicMock:
    attrs = MagicMock()
    attrs.level = _FLAGS_UNSET
    attrs.parent_id = _FLAGS_UNSET
    attrs.environments = _FLAGS_UNSET
    r = MagicMock()
    r.id = id_
    r.attributes = attrs
    return r


# ---------------------------------------------------------------------------
# Config runtime
# ---------------------------------------------------------------------------


class TestConfigRuntimePagination:
    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_fetch_all_configs_single_short_page(self, mock_list):
        mock_list.return_value = _list_resp([_config_resource("c1")])
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        try:
            configs = client.config._fetch_all_configs()
            assert len(configs) == 1
            assert mock_list.call_count == 1
            assert mock_list.call_args.kwargs["pagenumber"] == 1
            assert mock_list.call_args.kwargs["pagesize"] == PAGE_SIZE
        finally:
            client.close()

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_fetch_all_configs_multi_page_exit(self, mock_list):
        full_page = [_config_resource(f"c{i}") for i in range(PAGE_SIZE)]
        short_page = [_config_resource("c_last")]
        mock_list.side_effect = [_list_resp(full_page), _list_resp(short_page)]

        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        try:
            configs = client.config._fetch_all_configs()
            assert len(configs) == PAGE_SIZE + 1
            assert mock_list.call_count == 2
            page_numbers = [c.kwargs["pagenumber"] for c in mock_list.call_args_list]
            assert page_numbers == [1, 2]
            assert all(c.kwargs["pagesize"] == PAGE_SIZE for c in mock_list.call_args_list)
        finally:
            client.close()

    @patch("smplkit.config.clients.list_configs.asyncio_detailed", new_callable=AsyncMock)
    def test_fetch_all_configs_async_multi_page_exit(self, mock_list):
        full_page = [_config_resource(f"c{i}") for i in range(PAGE_SIZE)]
        short_page = [_config_resource("c_last")]
        mock_list.side_effect = [_list_resp(full_page), _list_resp(short_page)]

        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        configs = asyncio.run(client.config._fetch_all_configs_async())
        assert len(configs) == PAGE_SIZE + 1
        assert mock_list.await_count == 2
        page_numbers = [c.kwargs["pagenumber"] for c in mock_list.call_args_list]
        assert page_numbers == [1, 2]

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_configs_changed_multi_page_exit(self, mock_list):
        full_page = [_config_resource(f"c{i}") for i in range(PAGE_SIZE)]
        short_page = [_config_resource("c_last")]
        mock_list.side_effect = [_list_resp(full_page), _list_resp(short_page)]

        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._installed = True
        client.config._handle_configs_changed({})
        # ``raw_cache`` now contains every resource across both pages.
        assert len(client.config._raw_config_cache) == PAGE_SIZE + 1
        page_numbers = [c.kwargs["pagenumber"] for c in mock_list.call_args_list]
        assert page_numbers == [1, 2]


# ---------------------------------------------------------------------------
# Flags runtime
# ---------------------------------------------------------------------------


class TestFlagsRuntimePagination:
    def _flags_client(self):
        from smplkit._buffer import _ContextRegistrationBuffer
        from smplkit.flags.clients import FlagsClient
        from smplkit.platform.clients import ContextsClient as ContextsClient

        parent = MagicMock()
        parent._environment = "test"
        parent._service = None
        contexts = ContextsClient(MagicMock(), _ContextRegistrationBuffer())
        with patch("smplkit.flags.clients.AuthenticatedClient"):
            return FlagsClient(parent=parent, transport=MagicMock(), contexts=contexts, metrics=parent._metrics)

    def _async_flags_client(self):
        from smplkit._buffer import _ContextRegistrationBuffer
        from smplkit.flags.clients import AsyncFlagsClient
        from smplkit.platform.clients import AsyncContextsClient

        parent = MagicMock()
        parent._environment = "test"
        parent._service = None
        contexts = AsyncContextsClient(MagicMock(), _ContextRegistrationBuffer())
        with patch("smplkit.flags.clients.AuthenticatedClient"):
            return AsyncFlagsClient(parent=parent, transport=MagicMock(), contexts=contexts, metrics=parent._metrics)

    @patch("smplkit.flags.clients.list_flags.sync_detailed")
    def test_fetch_flags_list_multi_page_exit(self, mock_list):
        full_page = [_flag_json_dict(f"f{i}") for i in range(PAGE_SIZE)]
        short_page = [_flag_json_dict("f_last")]
        mock_list.side_effect = [
            _json_resp({"data": full_page}),
            _json_resp({"data": short_page}),
        ]

        client = self._flags_client()
        flags = client._fetch_flags_list()
        assert len(flags) == PAGE_SIZE + 1
        assert mock_list.call_count == 2
        page_numbers = [c.kwargs["pagenumber"] for c in mock_list.call_args_list]
        assert page_numbers == [1, 2]

    @patch("smplkit.flags.clients.list_flags.sync_detailed")
    def test_fetch_all_flags_sync_multi_page_exit(self, mock_list):
        full_page = [_flag_json_dict(f"f{i}") for i in range(PAGE_SIZE)]
        short_page = [_flag_json_dict("f_last")]
        mock_list.side_effect = [
            _json_resp({"data": full_page}),
            _json_resp({"data": short_page}),
        ]

        client = self._async_flags_client()
        client._fetch_all_flags_sync()
        assert len(client._flag_store) == PAGE_SIZE + 1
        assert mock_list.call_count == 2

    @patch("smplkit.flags.clients.list_flags.asyncio_detailed", new_callable=AsyncMock)
    def test_fetch_flags_list_async_multi_page_exit(self, mock_list):
        full_page = [_flag_json_dict(f"f{i}") for i in range(PAGE_SIZE)]
        short_page = [_flag_json_dict("f_last")]
        mock_list.side_effect = [
            _json_resp({"data": full_page}),
            _json_resp({"data": short_page}),
        ]

        client = self._async_flags_client()
        flags = asyncio.run(client._fetch_flags_list())
        assert len(flags) == PAGE_SIZE + 1
        assert mock_list.await_count == 2


# ---------------------------------------------------------------------------
# Logging runtime
# ---------------------------------------------------------------------------


class TestLoggingRuntimePagination:
    @patch("smplkit.logging.clients.list_log_groups.sync_detailed")
    @patch("smplkit.logging.clients.list_loggers.sync_detailed")
    def test_fetch_and_apply_loggers_multi_page_exit(self, mock_loggers, mock_groups):
        full_loggers = [_logger_resource(f"lg{i}") for i in range(PAGE_SIZE)]
        short_loggers = [_logger_resource("lg_last")]
        mock_loggers.side_effect = [_list_resp(full_loggers), _list_resp(short_loggers)]
        mock_groups.return_value = _list_resp([])

        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        try:
            client.logging._fetch_and_apply("test")
            assert len(client.logging._loggers_cache) == PAGE_SIZE + 1
            assert mock_loggers.call_count == 2
            logger_pages = [c.kwargs["pagenumber"] for c in mock_loggers.call_args_list]
            assert logger_pages == [1, 2]
        finally:
            client.close()

    @patch("smplkit.logging.clients.list_log_groups.sync_detailed")
    @patch("smplkit.logging.clients.list_loggers.sync_detailed")
    def test_fetch_and_apply_log_groups_multi_page_exit(self, mock_loggers, mock_groups):
        full_groups = [_log_group_resource(f"g{i}") for i in range(PAGE_SIZE)]
        short_groups = [_log_group_resource("g_last")]
        mock_loggers.return_value = _list_resp([])
        mock_groups.side_effect = [_list_resp(full_groups), _list_resp(short_groups)]

        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        try:
            client.logging._fetch_and_apply("test")
            assert len(client.logging._groups_cache) == PAGE_SIZE + 1
            assert mock_groups.call_count == 2
            group_pages = [c.kwargs["pagenumber"] for c in mock_groups.call_args_list]
            assert group_pages == [1, 2]
        finally:
            client.close()

    @patch("smplkit.logging.clients.list_log_groups.asyncio_detailed", new_callable=AsyncMock)
    @patch("smplkit.logging.clients.list_loggers.asyncio_detailed", new_callable=AsyncMock)
    def test_fetch_and_apply_async_loggers_multi_page_exit(self, mock_loggers, mock_groups):
        full_loggers = [_logger_resource(f"lg{i}") for i in range(PAGE_SIZE)]
        short_loggers = [_logger_resource("lg_last")]
        mock_loggers.side_effect = [_list_resp(full_loggers), _list_resp(short_loggers)]
        mock_groups.return_value = _list_resp([])

        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        asyncio.run(client.logging._fetch_and_apply("test"))
        assert len(client.logging._loggers_cache) == PAGE_SIZE + 1
        assert mock_loggers.await_count == 2

    @patch("smplkit.logging.clients.list_log_groups.asyncio_detailed", new_callable=AsyncMock)
    @patch("smplkit.logging.clients.list_loggers.asyncio_detailed", new_callable=AsyncMock)
    def test_fetch_and_apply_async_log_groups_multi_page_exit(self, mock_loggers, mock_groups):
        full_groups = [_log_group_resource(f"g{i}") for i in range(PAGE_SIZE)]
        short_groups = [_log_group_resource("g_last")]
        mock_loggers.return_value = _list_resp([])
        mock_groups.side_effect = [_list_resp(full_groups), _list_resp(short_groups)]

        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        asyncio.run(client.logging._fetch_and_apply("test"))
        assert len(client.logging._groups_cache) == PAGE_SIZE + 1
        assert mock_groups.await_count == 2


# ---------------------------------------------------------------------------
# Management list — pagination kwarg forwarding
# ---------------------------------------------------------------------------


def _mgmt_sync_pair_assert(call, *, page_number, page_size):
    if page_number is None:
        assert "pagenumber" not in call.kwargs
    else:
        assert call.kwargs["pagenumber"] == page_number
    if page_size is None:
        assert "pagesize" not in call.kwargs
    else:
        assert call.kwargs["pagesize"] == page_size


class TestManagementListPaginationForwarding:
    def _mgmt(self):
        from smplkit import SmplClient

        return SmplClient(api_key="sk_test", base_domain="example.test").platform

    def _async_mgmt(self):
        from smplkit import AsyncSmplClient

        return AsyncSmplClient(api_key="sk_test", base_domain="example.test").platform

    def _logging(self):
        """Logger / log-group CRUD lives on client.logging (loggers / log_groups)."""
        from smplkit import SmplClient

        return SmplClient(api_key="sk_test", base_domain="example.test").logging

    def _async_logging(self):
        from smplkit import AsyncSmplClient

        return AsyncSmplClient(api_key="sk_test", base_domain="example.test").logging

    # ------------------------------------------------------------------
    # Environments
    # ------------------------------------------------------------------

    @patch("smplkit.platform.clients._gen_list_environments.sync_detailed")
    def test_environments_list_defaults(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        self._mgmt().environments.list()
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=None, page_size=None)

    @patch("smplkit.platform.clients._gen_list_environments.sync_detailed")
    def test_environments_list_forwards(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        self._mgmt().environments.list(page_number=3, page_size=50)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=3, page_size=50)

    @patch("smplkit.platform.clients._gen_list_environments.asyncio_detailed", new_callable=AsyncMock)
    def test_environments_async_list_forwards(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        asyncio.run(self._async_mgmt().environments.list(page_number=2, page_size=25))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=2, page_size=25)

    # ------------------------------------------------------------------
    # Context types
    # ------------------------------------------------------------------

    @patch("smplkit.platform.clients._gen_list_context_types.sync_detailed")
    def test_context_types_list_forwards(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        self._mgmt().context_types.list(page_number=4, page_size=10)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=4, page_size=10)

    @patch("smplkit.platform.clients._gen_list_context_types.asyncio_detailed", new_callable=AsyncMock)
    def test_context_types_async_list_forwards(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        asyncio.run(self._async_mgmt().context_types.list(page_number=4, page_size=10))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=4, page_size=10)

    # ------------------------------------------------------------------
    # Contexts
    # ------------------------------------------------------------------

    @patch("smplkit.platform.clients._gen_list_contexts.sync_detailed")
    def test_contexts_list_forwards(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        self._mgmt().contexts.list("user", page_number=5, page_size=20)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=5, page_size=20)
        assert mock_list.call_args.kwargs["filtercontext_type"] == "user"

    @patch("smplkit.platform.clients._gen_list_contexts.asyncio_detailed", new_callable=AsyncMock)
    def test_contexts_async_list_forwards(self, mock_list):
        mock_list.return_value = _resp(content=b'{"data": []}')
        asyncio.run(self._async_mgmt().contexts.list("user", page_number=5, page_size=20))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=5, page_size=20)

    # ------------------------------------------------------------------
    # Config
    # ------------------------------------------------------------------

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_config_list_forwards(self, mock_list):
        from smplkit import SmplClient

        mock_list.return_value = _list_resp([])
        SmplClient(api_key="sk_test", base_domain="example.test").config.list(page_number=2, page_size=100)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=2, page_size=100)

    @patch("smplkit.config.clients.list_configs.asyncio_detailed", new_callable=AsyncMock)
    def test_config_async_list_forwards(self, mock_list):
        from smplkit import AsyncSmplClient

        mock_list.return_value = _list_resp([])
        client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
        asyncio.run(client.config.list(page_number=2, page_size=100))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=2, page_size=100)

    # ------------------------------------------------------------------
    # Flags
    # ------------------------------------------------------------------

    @patch("smplkit.flags.clients.list_flags.sync_detailed")
    def test_flags_list_forwards(self, mock_list):
        from smplkit import SmplClient

        mock_list.return_value = _resp(content=b'{"data": []}')
        SmplClient(api_key="sk_test", base_domain="example.test").flags.list(page_number=7, page_size=42)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=7, page_size=42)

    @patch("smplkit.flags.clients.list_flags.asyncio_detailed", new_callable=AsyncMock)
    def test_flags_async_list_forwards(self, mock_list):
        from smplkit import AsyncSmplClient

        mock_list.return_value = _resp(content=b'{"data": []}')
        client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
        asyncio.run(client.flags.list(page_number=7, page_size=42))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=7, page_size=42)

    # ------------------------------------------------------------------
    # Loggers
    # ------------------------------------------------------------------

    @patch("smplkit.logging.clients.list_loggers.sync_detailed")
    def test_loggers_list_forwards(self, mock_list):
        mock_list.return_value = _list_resp([])
        self._logging().loggers.list(page_number=9, page_size=11)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=9, page_size=11)

    @patch("smplkit.logging.clients.list_loggers.asyncio_detailed", new_callable=AsyncMock)
    def test_loggers_async_list_forwards(self, mock_list):
        mock_list.return_value = _list_resp([])
        asyncio.run(self._async_logging().loggers.list(page_number=9, page_size=11))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=9, page_size=11)

    # ------------------------------------------------------------------
    # Log groups
    # ------------------------------------------------------------------

    @patch("smplkit.logging.clients.list_log_groups.sync_detailed")
    def test_log_groups_list_forwards(self, mock_list):
        mock_list.return_value = _list_resp([])
        self._logging().log_groups.list(page_number=6, page_size=8)
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=6, page_size=8)

    @patch("smplkit.logging.clients.list_log_groups.asyncio_detailed", new_callable=AsyncMock)
    def test_log_groups_async_list_forwards(self, mock_list):
        mock_list.return_value = _list_resp([])
        asyncio.run(self._async_logging().log_groups.list(page_number=6, page_size=8))
        _mgmt_sync_pair_assert(mock_list.call_args, page_number=6, page_size=8)


class TestPaginationKwargsHelper:
    def test_empty_when_both_none(self):
        from smplkit.platform.clients import _pagination_kwargs

        assert _pagination_kwargs(None, None) == {}

    def test_includes_only_set_values(self):
        from smplkit.platform.clients import _pagination_kwargs

        assert _pagination_kwargs(2, None) == {"pagenumber": 2}
        assert _pagination_kwargs(None, 50) == {"pagesize": 50}
        assert _pagination_kwargs(2, 50) == {"pagenumber": 2, "pagesize": 50}
