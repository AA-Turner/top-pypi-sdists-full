"""Tests for SmplClient/AsyncSmplClient construction and the platform/account
clients they wire up.

After the management-namespace split there is no ``client.manage`` — the
cross-cutting CRUD lives on ``client.platform`` (environments / services /
contexts / context_types) and ``client.account`` (settings). The contract:

- All sub-clients are wired; audit/jobs/config/flags/logging are top-level.
- The per-service transports are built side-effect-free (no threads, no HTTP).
- ``client.close()`` releases every per-service HTTP transport.
- ``PlatformClient`` / ``AccountClient`` are constructible standalone.
"""

from __future__ import annotations

import asyncio
import threading
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from smplkit import (
    AccountClient,
    AsyncAccountClient,
    AsyncPlatformClient,
    AsyncSmplClient,
    Error,
    PlatformClient,
    SmplClient,
)
from smplkit._config import resolve_client_config
from smplkit._transport import _to_transport_config, build_service_transports
from smplkit.account._client import AsyncSettingsClient, SettingsClient
from smplkit.config._client import AsyncConfigClient, ConfigClient
from smplkit.flags._client import AsyncFlagsClient, FlagsClient
from smplkit.logging._client import (
    AsyncLoggingClient,
    LoggingClient,
    AsyncLogGroupsClient,
    AsyncLoggersClient,
    LogGroupsClient,
    LoggersClient,
)
from smplkit.platform._client import (
    AsyncContextsClient,
    AsyncContextTypesClient,
    AsyncEnvironmentsClient,
    AsyncServicesClient,
    ContextsClient,
    ContextTypesClient,
    EnvironmentsClient,
    ServicesClient,
)


# ---------------------------------------------------------------------------
# Sync construction
# ---------------------------------------------------------------------------


class TestSmplClientConstruction:
    def test_platform_and_account_are_wired(self):
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        platform = client.platform
        assert isinstance(platform, PlatformClient)
        assert isinstance(platform.contexts, ContextsClient)
        assert isinstance(platform.context_types, ContextTypesClient)
        assert isinstance(platform.environments, EnvironmentsClient)
        assert isinstance(platform.services, ServicesClient)
        assert isinstance(client.account, AccountClient)
        assert isinstance(client.account.settings, SettingsClient)
        # config/flags/logging/audit/jobs are top-level (client.config /
        # client.flags / client.logging / client.audit / client.jobs). Logger /
        # log-group CRUD lives on client.logging.loggers / log_groups.
        assert isinstance(client.config, ConfigClient)
        assert isinstance(client.flags, FlagsClient)
        assert isinstance(client.logging, LoggingClient)
        assert isinstance(client.logging.loggers, LoggersClient)
        assert isinstance(client.logging.log_groups, LogGroupsClient)
        # The management namespace is gone entirely.
        assert not hasattr(client, "manage")
        client.close()

    def test_flags_contexts_seam_points_at_platform_contexts(self):
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        assert client.flags._contexts is client.platform.contexts
        client.close()

    def test_platform_borrows_parent_app_transport(self):
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        assert client.platform._app_http is client._app_http
        assert client.platform._owns_transport is False
        client.close()

    def test_transport_construction_has_no_side_effects(self):
        """Building the per-service transports must not start threads or HTTP."""
        cfg = _to_transport_config(resolve_client_config(api_key="sk_test", base_domain="example.test"))
        before = {t.ident for t in threading.enumerate()}
        with patch("httpx.Client") as mock_sync_client, patch("httpx.AsyncClient") as mock_async_client:
            build_service_transports(cfg)
        after = {t.ident for t in threading.enumerate()}
        assert before == after
        mock_sync_client.assert_not_called()
        mock_async_client.assert_not_called()

    def test_close_closes_all_http_clients(self):
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        transports = client._transports
        for attr in ("app_http", "config_http", "flags_http", "logging_http", "jobs_http"):
            getattr(transports, attr)._client = MagicMock()
        client.close()
        for attr in ("app_http", "config_http", "flags_http", "logging_http", "jobs_http"):
            assert getattr(transports, attr)._client is None

    def test_close_when_no_clients_initialized(self):
        """close() is a no-op for transports when no httpx clients materialized."""
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        client.close()  # should not raise

    def test_instances_have_independent_context_buffers(self):
        a = SmplClient(api_key="sk_test", base_domain="example.test")
        b = SmplClient(api_key="sk_test", base_domain="example.test")
        assert a.platform._context_buffer is not b.platform._context_buffer
        a.close()
        b.close()


# ---------------------------------------------------------------------------
# Async construction
# ---------------------------------------------------------------------------


class TestAsyncSmplClientConstruction:
    def test_platform_and_account_are_wired(self):
        client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
        platform = client.platform
        assert isinstance(platform, AsyncPlatformClient)
        assert isinstance(platform.contexts, AsyncContextsClient)
        assert isinstance(platform.context_types, AsyncContextTypesClient)
        assert isinstance(platform.environments, AsyncEnvironmentsClient)
        assert isinstance(platform.services, AsyncServicesClient)
        assert isinstance(client.account, AsyncAccountClient)
        assert isinstance(client.account.settings, AsyncSettingsClient)
        assert isinstance(client.config, AsyncConfigClient)
        assert isinstance(client.flags, AsyncFlagsClient)
        assert isinstance(client.logging, AsyncLoggingClient)
        assert isinstance(client.logging.loggers, AsyncLoggersClient)
        assert isinstance(client.logging.log_groups, AsyncLogGroupsClient)
        assert not hasattr(client, "manage")
        asyncio.run(client.close())

    def test_flags_contexts_seam_points_at_platform_contexts(self):
        client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
        assert client.flags._contexts is client.platform.contexts
        asyncio.run(client.close())

    def test_close_closes_all_async_clients(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
            transports = client._transports
            for attr in ("app_http", "config_http", "flags_http", "logging_http", "jobs_http"):
                ac = AsyncMock()
                ac.aclose = AsyncMock()
                getattr(transports, attr)._async_client = ac
            await client.close()
            for attr in ("app_http", "config_http", "flags_http", "logging_http", "jobs_http"):
                assert getattr(transports, attr)._async_client is None

        asyncio.run(_run())

    def test_close_when_no_clients_initialized(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
            await client.close()  # no error

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Standalone PlatformClient / AccountClient construction + close
# ---------------------------------------------------------------------------


class TestStandalonePlatformClient:
    def test_standalone_builds_own_transport(self):
        platform = PlatformClient(api_key="sk_test", base_domain="example.test")
        assert platform._owns_transport is True
        assert platform._app_http._base_url == "https://app.example.test"
        assert isinstance(platform.environments, EnvironmentsClient)
        assert isinstance(platform.contexts, ContextsClient)
        platform.close()

    def test_standalone_close_tears_down_owned_transport(self):
        platform = PlatformClient(api_key="sk_test", base_domain="example.test")
        inner = MagicMock()
        platform._app_http._client = inner
        platform.close()
        inner.close.assert_called_once()
        assert platform._app_http._client is None

    def test_standalone_close_noop_without_materialized_client(self):
        platform = PlatformClient(api_key="sk_test", base_domain="example.test")
        platform._app_http._client = None
        platform.close()  # no error

    def test_context_manager(self):
        with PlatformClient(api_key="sk_test", base_domain="example.test") as platform:
            assert isinstance(platform, PlatformClient)

    def test_wired_close_is_noop_on_borrowed_transport(self):
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        sentinel = MagicMock()
        client.platform._app_http._client = sentinel
        client.platform.close()  # wired: borrows parent transport
        assert client.platform._app_http._client is sentinel
        client.close()

    def test_base_url_used_directly_when_supplied(self):
        platform = PlatformClient(api_key="sk_test", base_url="http://app.localhost")
        assert platform._app_http._base_url == "http://app.localhost"
        platform.close()


class TestStandaloneAsyncPlatformClient:
    def test_standalone_builds_own_transport(self):
        platform = AsyncPlatformClient(api_key="sk_test", base_domain="example.test")
        assert platform._owns_transport is True
        assert isinstance(platform.environments, AsyncEnvironmentsClient)
        assert isinstance(platform.contexts, AsyncContextsClient)

    def test_standalone_aclose_tears_down_owned_transport(self):
        async def _run():
            platform = AsyncPlatformClient(api_key="sk_test", base_domain="example.test")
            ac = AsyncMock()
            ac.aclose = AsyncMock()
            platform._app_http._async_client = ac
            await platform.aclose()
            ac.aclose.assert_awaited_once()
            assert platform._app_http._async_client is None

        asyncio.run(_run())

    def test_aclose_noop_without_materialized_client(self):
        async def _run():
            platform = AsyncPlatformClient(api_key="sk_test", base_domain="example.test")
            platform._app_http._async_client = None
            await platform.aclose()  # no error

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncPlatformClient(api_key="sk_test", base_domain="example.test") as platform:
                assert isinstance(platform, AsyncPlatformClient)

        asyncio.run(_run())

    def test_wired_aclose_is_noop_on_borrowed_transport(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", base_domain="example.test")
            sentinel = AsyncMock()
            client.platform._app_http._async_client = sentinel
            await client.platform.aclose()  # wired: borrows parent transport
            assert client.platform._app_http._async_client is sentinel
            await client.close()

        asyncio.run(_run())


class TestStandaloneAccountClient:
    def test_standalone_builds_settings_client(self):
        account = AccountClient(api_key="sk_test", base_domain="example.test")
        assert isinstance(account.settings, SettingsClient)
        assert account.settings._base_url == "https://app.example.test"
        account.close()  # no-op

    def test_base_url_used_directly_when_supplied(self):
        account = AccountClient(api_key="sk_test", base_url="http://app.localhost")
        assert account.settings._base_url == "http://app.localhost"

    def test_context_manager(self):
        with AccountClient(api_key="sk_test", base_domain="example.test") as account:
            assert isinstance(account, AccountClient)

    def test_extra_headers_forwarded(self):
        account = AccountClient(api_key="sk_test", base_domain="example.test", extra_headers={"X-Trace": "1"})
        assert account.settings._headers["X-Trace"] == "1"


class TestStandaloneAsyncAccountClient:
    def test_standalone_builds_settings_client(self):
        account = AsyncAccountClient(api_key="sk_test", base_domain="example.test")
        assert isinstance(account.settings, AsyncSettingsClient)
        assert account.settings._base_url == "https://app.example.test"

    def test_aclose_is_noop(self):
        async def _run():
            account = AsyncAccountClient(api_key="sk_test", base_domain="example.test")
            await account.aclose()  # no-op

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncAccountClient(api_key="sk_test", base_domain="example.test") as account:
                assert isinstance(account, AsyncAccountClient)

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# resolve_client_config edge cases
# ---------------------------------------------------------------------------


class TestResolveManagementConfig:
    def test_missing_api_key_raises(self, monkeypatch, tmp_path):
        # api_key is required even for the management resolver (backs the
        # standalone AuditClient/JobsClient transports).
        monkeypatch.delenv("SMPLKIT_API_KEY", raising=False)
        monkeypatch.delenv("SMPLKIT_PROFILE", raising=False)
        with pytest.raises(Error, match="No API key provided"):
            resolve_client_config(_home_dir=tmp_path)

    def test_debug_env_var_parsed(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_env")
        monkeypatch.setenv("SMPLKIT_DEBUG", "true")
        from smplkit._config import resolve_client_config

        cfg = resolve_client_config()
        assert cfg.debug is True

    def test_constructor_arg_overrides_env_for_debug(self, monkeypatch):
        monkeypatch.setenv("SMPLKIT_API_KEY", "sk_env")
        monkeypatch.setenv("SMPLKIT_DEBUG", "false")
        from smplkit._config import resolve_client_config

        cfg = resolve_client_config(debug=True)
        assert cfg.debug is True

    def test_default_base_domain_and_scheme(self, monkeypatch):
        monkeypatch.delenv("SMPLKIT_BASE_DOMAIN", raising=False)
        monkeypatch.delenv("SMPLKIT_SCHEME", raising=False)
        from smplkit._config import resolve_client_config

        cfg = resolve_client_config(api_key="sk_test")
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
        from smplkit._config import resolve_client_config

        cfg = resolve_client_config(_home_dir=tmp_path)
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
# Runtime ConfigClient internals — fetch error/empty paths
# ---------------------------------------------------------------------------


class TestRuntimeConfigFetchPaths:
    def _client(self):
        from smplkit import SmplClient

        return SmplClient(api_key="sk_test", environment="test", service="svc")

    @patch("smplkit.config._client.list_configs.sync_detailed")
    def test_fetch_all_configs_network_error(self, mock_list):
        import httpx

        from smplkit._errors import ConnectionError

        mock_list.side_effect = httpx.ConnectError("refused")
        client = self._client()
        with pytest.raises(ConnectionError):
            client.config._fetch_all_configs()

    @patch("smplkit.config._client.list_configs.sync_detailed")
    def test_fetch_all_configs_parsed_none(self, mock_list):
        mock = MagicMock()
        mock.status_code = 200
        mock.content = b""
        mock.parsed = None
        mock_list.return_value = mock
        client = self._client()
        assert client.config._fetch_all_configs() == []

    @patch("smplkit.config._client.get_config.sync_detailed")
    def test_fetch_config_network_error(self, mock_get):
        import httpx

        from smplkit._errors import ConnectionError

        mock_get.side_effect = httpx.ConnectError("refused")
        client = self._client()
        with pytest.raises(ConnectionError):
            client.config._fetch_config("anything")

    @patch("smplkit.config._client.get_config.sync_detailed")
    def test_fetch_config_parsed_none_returns_none(self, mock_get):
        mock = MagicMock()
        mock.status_code = 200
        mock.content = b""
        mock.parsed = None
        mock_get.return_value = mock
        client = self._client()
        assert client.config._fetch_config("any") is None

    @patch("smplkit.config._client.get_config.sync_detailed")
    def test_handle_config_changed_with_none_fetched_returns_quietly(self, mock_get):
        mock = MagicMock()
        mock.status_code = 200
        mock.content = b""
        mock.parsed = None
        mock_get.return_value = mock
        client = self._client()
        client.config._installed = True
        client.config._config_cache = {"x": {"a": 1}}
        client.config._handle_config_changed({"id": "x"})
        # cache unchanged because fetch returned None
        assert client.config._config_cache == {"x": {"a": 1}}

    @patch("smplkit.config._client.list_configs.asyncio_detailed")
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

    @patch("smplkit.config._client.list_configs.asyncio_detailed")
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

    @patch("smplkit.config._client.list_configs.sync_detailed")
    def test_fetch_all_configs_reraises_unknown_exception(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        client = self._client()
        with pytest.raises(RuntimeError, match="unexpected"):
            client.config._fetch_all_configs()

    @patch("smplkit.config._client.get_config.sync_detailed")
    def test_fetch_config_reraises_unknown_exception(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")
        client = self._client()
        with pytest.raises(RuntimeError, match="unexpected"):
            client.config._fetch_config("x")

    @patch("smplkit.config._client.get_config.sync_detailed")
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

    @patch("smplkit.config._client.list_configs.asyncio_detailed")
    def test_async_fetch_all_configs_reraises_unknown_exception(self, mock_list):
        from smplkit import AsyncSmplClient

        async def _run():
            mock_list.side_effect = RuntimeError("unexpected")
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            with pytest.raises(RuntimeError, match="unexpected"):
                await client.config._fetch_all_configs_async()

        asyncio.run(_run())
