"""Tests for the top-level :class:`SmplManagementClient` / :class:`AsyncSmplManagementClient`.

The contract is:

- Construction has zero side effects (no service registration, no metrics
  thread, no websocket, no HTTP requests).
- All eight management namespaces are wired up.
- close() releases HTTP transport resources.
- Context-manager behavior closes on exit.
"""

from __future__ import annotations

import asyncio
import threading
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from smplkit import AsyncSmplManagementClient, SmplManagementClient
from smplkit._errors import Error
from smplkit.management.client import (
    AccountSettingsClient,
    AsyncAccountSettingsClient,
    AsyncConfigClient,
    AsyncContextsClient,
    AsyncContextTypesClient,
    AsyncEnvironmentsClient,
    AsyncFlagsClient,
    AsyncLogGroupsClient,
    AsyncLoggersClient,
    AsyncServicesClient,
    ConfigClient,
    ContextsClient,
    ContextTypesClient,
    EnvironmentsClient,
    FlagsClient,
    LogGroupsClient,
    LoggersClient,
    ServicesClient,
)


_NS_ATTRS = (
    "contexts",
    "context_types",
    "environments",
    "services",
    "account_settings",
    "configs",
    "flags",
    "loggers",
    "log_groups",
)


# ---------------------------------------------------------------------------
# Sync top-level client
# ---------------------------------------------------------------------------


class TestSmplManagementClientConstruction:
    def test_namespaces_are_wired(self):
        mgmt = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        assert isinstance(mgmt.contexts, ContextsClient)
        assert isinstance(mgmt.context_types, ContextTypesClient)
        assert isinstance(mgmt.environments, EnvironmentsClient)
        assert isinstance(mgmt.services, ServicesClient)
        assert isinstance(mgmt.account_settings, AccountSettingsClient)
        assert isinstance(mgmt.config, ConfigClient)
        assert isinstance(mgmt.flags, FlagsClient)
        assert isinstance(mgmt.loggers, LoggersClient)
        assert isinstance(mgmt.log_groups, LogGroupsClient)
        mgmt.close()

    def test_construction_has_no_side_effects(self):
        """Building the client must not start threads or make HTTP calls.

        We snapshot the live thread set before construction, then assert no
        new daemon threads appear after — proves the runtime side effects
        (auto-registration thread, metrics flusher) of ``SmplClient`` are
        absent here. We also patch ``httpx.Client`` to assert no HTTP
        request is fired.
        """
        before = {t.ident for t in threading.enumerate()}
        with patch("httpx.Client") as mock_sync_client, patch("httpx.AsyncClient") as mock_async_client:
            mgmt = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        after = {t.ident for t in threading.enumerate()}
        # No new threads spawned during construction
        assert before == after
        # No httpx.Client / AsyncClient instantiated for outbound calls
        # (the sub-clients construct their httpx clients lazily on first use)
        mock_sync_client.assert_not_called()
        mock_async_client.assert_not_called()
        mgmt.close()

    def test_resolves_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_env")
        mgmt = SmplManagementClient(base_domain="example.test")
        assert mgmt._api_key == "sk_env"
        mgmt.close()

    def test_constructor_arg_overrides_env(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_env")
        mgmt = SmplManagementClient(api_key="sk_arg", base_domain="example.test")
        assert mgmt._api_key == "sk_arg"
        mgmt.close()

    def test_missing_api_key_raises(self, monkeypatch, tmp_path):
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        # Point HOME at an empty dir so ~/.smplkit doesn't exist
        monkeypatch.setenv("HOME", str(tmp_path))
        with pytest.raises(Error, match="No API key provided"):
            SmplManagementClient()

    def test_debug_flag_enables_debug_logging(self):
        with patch("smplkit.management.client.enable_debug") as mock_enable:
            mgmt = SmplManagementClient(
                api_key="sk_test",
                base_domain="example.test",
                debug=True,
            )
        mock_enable.assert_called_once()
        mgmt.close()

    def test_does_not_require_environment_or_service(self, monkeypatch):
        """Management clients are decoupled from runtime concerns."""
        monkeypatch.delenv("SMPLKIT_ENVIRONMENT", raising=False)
        monkeypatch.delenv("SMPLKIT_SERVICE", raising=False)
        # No Error raised even though env/service are unset
        mgmt = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        mgmt.close()

    def test_close_closes_all_http_clients(self):
        mgmt = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        # Mock out the underlying httpx client to verify close()
        for attr in ("_app_http", "_config_http", "_flags_http", "_logging_http"):
            http = getattr(mgmt, attr)
            http._client = MagicMock()
        mgmt.close()
        for attr in ("_app_http", "_config_http", "_flags_http", "_logging_http"):
            http = getattr(mgmt, attr)
            assert http._client is None

    def test_close_when_no_clients_initialized(self):
        """close() is a no-op when no httpx clients were materialized."""
        mgmt = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        # _client is None on every AuthenticatedClient until first use
        mgmt.close()  # should not raise

    def test_context_manager(self):
        with SmplManagementClient(api_key="sk_test", base_domain="example.test") as mgmt:
            assert isinstance(mgmt, SmplManagementClient)
        # close() called on exit — verify by checking _app_http._client is None
        assert mgmt._app_http._client is None

    def test_instances_have_independent_buffers(self):
        a = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        b = SmplManagementClient(api_key="sk_test", base_domain="example.test")
        assert a._context_buffer is not b._context_buffer
        a.close()
        b.close()


# ---------------------------------------------------------------------------
# Async top-level client
# ---------------------------------------------------------------------------


class TestAsyncSmplManagementClientConstruction:
    def test_namespaces_are_wired(self):
        mgmt = AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")
        assert isinstance(mgmt.contexts, AsyncContextsClient)
        assert isinstance(mgmt.context_types, AsyncContextTypesClient)
        assert isinstance(mgmt.environments, AsyncEnvironmentsClient)
        assert isinstance(mgmt.services, AsyncServicesClient)
        assert isinstance(mgmt.account_settings, AsyncAccountSettingsClient)
        assert isinstance(mgmt.config, AsyncConfigClient)
        assert isinstance(mgmt.flags, AsyncFlagsClient)
        assert isinstance(mgmt.loggers, AsyncLoggersClient)
        assert isinstance(mgmt.log_groups, AsyncLogGroupsClient)

    def test_construction_has_no_side_effects(self):
        before = {t.ident for t in threading.enumerate()}
        with patch("httpx.Client") as mock_sync, patch("httpx.AsyncClient") as mock_async:
            AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")
        after = {t.ident for t in threading.enumerate()}
        assert before == after
        mock_sync.assert_not_called()
        mock_async.assert_not_called()

    def test_debug_flag_enables_debug(self):
        with patch("smplkit.management.client.enable_debug") as mock_enable:
            AsyncSmplManagementClient(
                api_key="sk_test",
                base_domain="example.test",
                debug=True,
            )
        mock_enable.assert_called_once()

    def test_close_closes_all_async_clients(self):
        async def _run():
            mgmt = AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")
            for attr in ("_app_http", "_config_http", "_flags_http", "_logging_http"):
                http = getattr(mgmt, attr)
                ac = AsyncMock()
                ac.aclose = AsyncMock()
                http._async_client = ac
            await mgmt.close()
            for attr in ("_app_http", "_config_http", "_flags_http", "_logging_http"):
                http = getattr(mgmt, attr)
                assert http._async_client is None

        asyncio.run(_run())

    def test_close_when_no_clients_initialized(self):
        async def _run():
            mgmt = AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")
            await mgmt.close()  # no error

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test") as mgmt:
                assert isinstance(mgmt, AsyncSmplManagementClient)
            assert mgmt._app_http._async_client is None

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# resolve_management_config edge cases
# ---------------------------------------------------------------------------


class TestResolveManagementConfig:
    def test_debug_env_var_parsed(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_env")
        monkeypatch.setenv("SMPLKIT_DEBUG", "true")
        from smplkit._config import resolve_management_config

        cfg = resolve_management_config()
        assert cfg.debug is True

    def test_constructor_arg_overrides_env_for_debug(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_env")
        monkeypatch.setenv("SMPLKIT_DEBUG", "false")
        from smplkit._config import resolve_management_config

        cfg = resolve_management_config(debug=True)
        assert cfg.debug is True

    def test_default_base_domain_and_scheme(self, monkeypatch):
        monkeypatch.delenv("SMPLKIT_BASE_DOMAIN", raising=False)
        monkeypatch.delenv("SMPLKIT_SCHEME", raising=False)
        from smplkit._config import resolve_management_config

        cfg = resolve_management_config(api_key="sk_test")
        assert cfg.base_domain == "smplkit.com"
        assert cfg.scheme == "https"

    def test_config_file_provides_api_key_and_debug(self, monkeypatch, tmp_path):
        """Values come from ~/.smplkit when env/args are unset."""
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_BASE_DOMAIN", raising=False)
        monkeypatch.delenv("SMPLKIT_SCHEME", raising=False)
        monkeypatch.delenv("SMPLKIT_DEBUG", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        (tmp_path / ".smplkit").write_text(
            "[default]\napi_key = sk_from_file\nbase_domain = file.smplkit.com\ndebug = true\n"
        )
        from smplkit._config import resolve_management_config

        cfg = resolve_management_config(_home_dir=tmp_path)
        assert cfg.api_key == "sk_from_file"
        assert cfg.base_domain == "file.smplkit.com"
        assert cfg.debug is True


# ---------------------------------------------------------------------------
# Model save() with no client raises (the new RuntimeError guard rail)
# ---------------------------------------------------------------------------


class TestModelsRequireClientForSave:
    def test_config_save_without_client(self):
        from smplkit.config.models import Config

        cfg = Config(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="Config was constructed without a client"):
            cfg.save()

    def test_async_config_save_without_client(self):
        from smplkit.config.models import AsyncConfig

        cfg = AsyncConfig(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="AsyncConfig was constructed without a client"):
                await cfg.save()

        asyncio.run(_run())

    def test_config_build_chain_with_missing_parent_no_client_raises(self):
        from smplkit.config.models import Config

        cfg = Config(None, id="child", name="Child", parent="missing-parent")
        with pytest.raises(RuntimeError, match="cannot resolve parent config"):
            cfg._build_chain([])

    def test_async_config_build_chain_with_missing_parent_no_client_raises(self):
        from smplkit.config.models import AsyncConfig

        cfg = AsyncConfig(None, id="child", name="Child", parent="missing-parent")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot resolve parent config"):
                await cfg._build_chain([])

        asyncio.run(_run())

    def test_flag_save_without_client(self):
        from smplkit.flags.models import Flag

        flag = Flag(None, id="x", name="X", type="BOOLEAN", default=False)
        with pytest.raises(RuntimeError, match="Flag was constructed without a client"):
            flag.save()

    def test_async_flag_save_without_client(self):
        from smplkit.flags.models import AsyncFlag

        flag = AsyncFlag(None, id="x", name="X", type="BOOLEAN", default=False)

        async def _run():
            with pytest.raises(RuntimeError, match="AsyncFlag was constructed without a client"):
                await flag.save()

        asyncio.run(_run())

    def test_logger_save_without_client(self):
        from smplkit.logging.models import SmplLogger

        lg = SmplLogger(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="SmplLogger was constructed without a client"):
            lg.save()

    def test_async_logger_save_without_client(self):
        from smplkit.logging.models import AsyncSmplLogger

        lg = AsyncSmplLogger(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="AsyncSmplLogger was constructed without a client"):
                await lg.save()

        asyncio.run(_run())

    def test_log_group_save_without_client(self):
        from smplkit.logging.models import SmplLogGroup

        grp = SmplLogGroup(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="SmplLogGroup was constructed without a client"):
            grp.save()

    def test_async_log_group_save_without_client(self):
        from smplkit.logging.models import AsyncSmplLogGroup

        grp = AsyncSmplLogGroup(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="AsyncSmplLogGroup was constructed without a client"):
                await grp.save()

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# _maybe_reraise_network_error: SDK exception passthrough
# ---------------------------------------------------------------------------


class TestMaybeReraiseNetworkError:
    def test_passes_through_sdk_exceptions(self):
        from smplkit._errors import NotFoundError
        from smplkit.management.client import _maybe_reraise_network_error

        original = NotFoundError("not found", status_code=404)
        with pytest.raises(NotFoundError, match="not found"):
            _maybe_reraise_network_error(original)


# ---------------------------------------------------------------------------
# Runtime ConfigClient internals — fetch error/empty paths
# ---------------------------------------------------------------------------


class TestRuntimeConfigFetchPaths:
    def _client(self):
        from smplkit import SmplClient

        return SmplClient(api_key="sk_test", environment="test", service="svc")

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_fetch_all_configs_network_error(self, mock_list):
        import httpx

        from smplkit._errors import ConnectionError

        mock_list.side_effect = httpx.ConnectError("refused")
        client = self._client()
        with pytest.raises(ConnectionError):
            client.config._fetch_all_configs()

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_fetch_all_configs_parsed_none(self, mock_list):
        mock = MagicMock()
        mock.status_code = 200
        mock.content = b""
        mock.parsed = None
        mock_list.return_value = mock
        client = self._client()
        assert client.config._fetch_all_configs() == []

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_fetch_config_network_error(self, mock_get):
        import httpx

        from smplkit._errors import ConnectionError

        mock_get.side_effect = httpx.ConnectError("refused")
        client = self._client()
        with pytest.raises(ConnectionError):
            client.config._fetch_config("anything")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_fetch_config_parsed_none_returns_none(self, mock_get):
        mock = MagicMock()
        mock.status_code = 200
        mock.content = b""
        mock.parsed = None
        mock_get.return_value = mock
        client = self._client()
        assert client.config._fetch_config("any") is None

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_handle_config_changed_with_none_fetched_returns_quietly(self, mock_get):
        mock = MagicMock()
        mock.status_code = 200
        mock.content = b""
        mock.parsed = None
        mock_get.return_value = mock
        client = self._client()
        client.config._connected = True
        client.config._config_cache = {"x": {"a": 1}}
        client.config._handle_config_changed({"id": "x"})
        # cache unchanged because fetch returned None
        assert client.config._config_cache == {"x": {"a": 1}}

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_async_fetch_all_configs_network_error(self, mock_list):
        from smplkit import AsyncSmplClient
        from smplkit._errors import ConnectionError
        import httpx

        async def _run():
            mock_list.side_effect = httpx.ConnectError("refused")
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            with pytest.raises(ConnectionError):
                await client.config._fetch_all_configs_async()

        asyncio.run(_run())

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_async_fetch_all_configs_parsed_none(self, mock_list):
        from smplkit import AsyncSmplClient

        async def _run():
            mock = MagicMock()
            mock.status_code = 200
            mock.content = b""
            mock.parsed = None
            mock_list.return_value = mock
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            assert await client.config._fetch_all_configs_async() == []

        asyncio.run(_run())

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_fetch_all_configs_reraises_unknown_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        client = self._client()
        with pytest.raises(RuntimeError, match="unexpected"):
            client.config._fetch_all_configs()

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_fetch_config_reraises_unknown_exception(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")
        client = self._client()
        with pytest.raises(RuntimeError, match="unexpected"):
            client.config._fetch_config("x")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_fetch_config_returns_built_config(self, mock_get):
        attrs = MagicMock()
        attrs.name = "Common"
        attrs.description = "desc"
        attrs.parent = None
        attrs.items = None
        attrs.environments = None
        attrs.created_at = None
        attrs.updated_at = None
        resource = MagicMock()
        resource.id = "common"
        resource.attributes = attrs
        parsed = MagicMock()
        parsed.data = resource
        resp = MagicMock()
        resp.status_code = 200
        resp.content = b""
        resp.parsed = parsed
        mock_get.return_value = resp
        client = self._client()
        cfg = client.config._fetch_config("common")
        assert cfg is not None
        assert cfg.id == "common"
        assert cfg.name == "Common"

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_async_fetch_all_configs_reraises_unknown_exception(self, mock_list):
        from smplkit import AsyncSmplClient

        async def _run():
            mock_list.side_effect = RuntimeError("unexpected")
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            with pytest.raises(RuntimeError, match="unexpected"):
                await client.config._fetch_all_configs_async()

        asyncio.run(_run())
