"""Tests for prescriptive config access: resolve, subscribe, LiveConfigProxy, change listeners."""

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from smplkit.errors import NotFoundError
from smplkit.clients import AsyncSmplClient, SmplClient
from smplkit.config.clients import ConfigChangeEvent, LiveConfigProxy


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_connected_client(cache=None):
    """Create a SmplClient with a pre-populated config cache."""
    client = SmplClient(api_key="sk_test", environment="production", service="svc")
    if cache is None:
        cache = {
            "db": {
                "host": "localhost",
                "port": 5432,
                "retries": 3,
                "enabled": True,
                "name": "test",
                "ratio": 0.75,
            },
        }
    client.config._config_cache = cache
    client.config._connected = True
    return client


def _make_connected_async_client(cache=None):
    """Create an AsyncSmplClient with a pre-populated config cache."""
    client = AsyncSmplClient(api_key="sk_test", environment="production", service="svc")
    if cache is None:
        cache = {
            "db": {
                "host": "localhost",
                "port": 5432,
                "retries": 3,
                "enabled": True,
                "name": "test",
                "ratio": 0.75,
            },
        }
    client.config._config_cache = cache
    client.config._connected = True
    return client


# ===================================================================
# 1. resolve() — sync
# ===================================================================


class TestResolveSyncPrescriptive:
    def test_resolve_returns_flat_dict(self):
        client = _make_connected_client()
        result = client.config.subscribe("db")
        assert isinstance(result, LiveConfigProxy)
        assert dict(result) == {
            "host": "localhost",
            "port": 5432,
            "retries": 3,
            "enabled": True,
            "name": "test",
            "ratio": 0.75,
        }

    def test_resolve_raises_not_found_for_missing_config(self):
        client = _make_connected_client()
        with pytest.raises(NotFoundError, match="Config with id 'nonexistent' not found"):
            client.config.subscribe("nonexistent")

    def test_subscribe_lazy_connects_without_explicit_install(self):
        client = SmplClient(api_key="sk_test", environment="production", service="svc")
        # No explicit install — subscribe connects lazily on first use.
        mock_cfg = MagicMock()
        mock_cfg.id = "db"
        mock_cfg._items_raw = {"host": {"value": "h"}}
        mock_cfg.environments = {}
        mock_cfg._build_chain.return_value = [{"id": "db", "items": {"host": {"value": "h"}}, "environments": {}}]
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            proxy = client.config.subscribe("db")
        assert client.config._connected is True
        assert proxy["host"] == "h"


# ===================================================================
# 2. resolve() — async
# ===================================================================


class TestResolveAsyncPrescriptive:
    def test_resolve_returns_flat_dict(self):
        client = _make_connected_async_client()

        async def _run():
            result = client.config.subscribe("db")
            assert isinstance(result, LiveConfigProxy)
            assert result["host"] == "localhost"
            assert result["port"] == 5432

        asyncio.run(_run())

    def test_resolve_raises_not_found_for_missing_config(self):
        client = _make_connected_async_client()

        async def _run():
            with pytest.raises(NotFoundError, match="Config with id 'nonexistent' not found"):
                client.config.subscribe("nonexistent")

        asyncio.run(_run())


# ===================================================================
# 3. LiveConfigProxy returned by get() — sync
# ===================================================================


class TestGetProxyBehaviorSync:
    def test_proxy_attribute_access(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        assert proxy.host == "localhost"
        assert proxy.port == 5432

    def test_proxy_getitem_access(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        assert proxy["host"] == "localhost"
        assert proxy["port"] == 5432

    def test_proxy_reflects_cache_updates(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        assert proxy.host == "localhost"

        # Simulate cache update (as refresh() would do)
        client.config._config_cache["db"]["host"] = "new-host"
        assert proxy.host == "new-host"

    def test_proxy_missing_attribute_raises(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        with pytest.raises(AttributeError, match="No config item"):
            _ = proxy.nonexistent

    def test_proxy_missing_getitem_raises(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        with pytest.raises(KeyError):
            _ = proxy["nonexistent"]

    def test_proxy_repr_without_model(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        r = repr(proxy)
        assert "LiveConfigProxy" in r
        assert "db" in r

    def test_get_for_missing_config_raises_not_found(self):
        client = _make_connected_client()
        with pytest.raises(NotFoundError, match="Config with id 'nonexistent' not found"):
            client.config.subscribe("nonexistent")

    def test_proxy_contains(self):
        client = _make_connected_client()
        proxy = client.config.subscribe("db")
        assert "host" in proxy
        assert "nope" not in proxy

    def test_proxy_len(self):
        client = _make_connected_client({"db": {"host": "localhost", "port": 5432}})
        proxy = client.config.subscribe("db")
        assert len(proxy) == 2

    def test_proxy_iter(self):
        client = _make_connected_client({"db": {"host": "localhost", "port": 5432}})
        proxy = client.config.subscribe("db")
        assert sorted(iter(proxy)) == ["host", "port"]

    def test_proxy_keys_values_items(self):
        client = _make_connected_client({"db": {"host": "localhost", "port": 5432}})
        proxy = client.config.subscribe("db")
        assert sorted(proxy.keys()) == ["host", "port"]
        assert set(proxy.values()) == {"localhost", 5432}
        assert dict(proxy.items()) == {"host": "localhost", "port": 5432}

    def test_proxy_get_method(self):
        client = _make_connected_client({"db": {"host": "localhost"}})
        proxy = client.config.subscribe("db")
        assert proxy.get("host") == "localhost"
        assert proxy.get("missing") is None
        assert proxy.get("missing", "fallback") == "fallback"


# ===================================================================
# 4. LiveConfigProxy returned by get() — async
# ===================================================================


class TestGetProxyBehaviorAsync:
    def test_proxy_attribute_access(self):
        client = _make_connected_async_client()

        async def _run():
            proxy = client.config.subscribe("db")
            assert proxy.host == "localhost"

        asyncio.run(_run())

    def test_proxy_getitem_access(self):
        client = _make_connected_async_client()

        async def _run():
            proxy = client.config.subscribe("db")
            assert proxy["host"] == "localhost"

        asyncio.run(_run())

    def test_proxy_reflects_cache_updates(self):
        client = _make_connected_async_client()

        async def _run():
            proxy = client.config.subscribe("db")
            assert proxy.host == "localhost"
            client.config._config_cache["db"]["host"] = "updated"
            assert proxy.host == "updated"

        asyncio.run(_run())


# ===================================================================
# 5. Refresh — sync
# ===================================================================


class TestRefreshSync:
    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_refresh_updates_cache(self, mock_list):
        client = _make_connected_client({"db": {"host": "old"}})

        mock_attrs = MagicMock()
        mock_attrs.name = "DB"
        mock_attrs.description = None
        mock_attrs.parent = None
        mock_attrs.items = None
        mock_attrs.environments = None
        mock_attrs.created_at = None
        mock_attrs.updated_at = None

        mock_resource = MagicMock()
        mock_resource.id = "db"
        mock_resource.attributes = mock_attrs

        mock_parsed = MagicMock()
        mock_parsed.data = [mock_resource]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_response.parsed = mock_parsed
        mock_list.return_value = mock_response

        with patch(
            "smplkit.config.models.Config._build_chain",
            return_value=[{"id": "db", "items": {}, "values": {"host": "new-host"}, "environments": {}}],
        ):
            client.config.refresh()

        assert client.config._config_cache["db"]["host"] == "new-host"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_refresh_fires_listeners(self, mock_list):
        client = _make_connected_client({"db": {"host": "old"}})

        events = []
        client.config.on_change(lambda e: events.append(e))

        mock_attrs = MagicMock()
        mock_attrs.name = "DB"
        mock_attrs.description = None
        mock_attrs.parent = None
        mock_attrs.items = None
        mock_attrs.environments = None
        mock_attrs.created_at = None
        mock_attrs.updated_at = None

        mock_resource = MagicMock()
        mock_resource.id = "db"
        mock_resource.attributes = mock_attrs

        mock_parsed = MagicMock()
        mock_parsed.data = [mock_resource]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_response.parsed = mock_parsed
        mock_list.return_value = mock_response

        with patch(
            "smplkit.config.models.Config._build_chain",
            return_value=[{"id": "db", "values": {"host": "new-host"}, "environments": {}}],
        ):
            client.config.refresh()

        assert len(events) == 1
        assert events[0].config_id == "db"
        assert events[0].item_key == "host"
        assert events[0].old_value == "old"
        assert events[0].new_value == "new-host"
        assert events[0].source == "manual"


# ===================================================================
# 6. Refresh — async
# ===================================================================


class TestRefreshAsync:
    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_refresh_updates_cache(self, mock_list):
        client = _make_connected_async_client({"db": {"host": "old"}})

        mock_attrs = MagicMock()
        mock_attrs.name = "DB"
        mock_attrs.description = None
        mock_attrs.parent = None
        mock_attrs.items = None
        mock_attrs.environments = None
        mock_attrs.created_at = None
        mock_attrs.updated_at = None

        mock_resource = MagicMock()
        mock_resource.id = "db"
        mock_resource.attributes = mock_attrs

        mock_parsed = MagicMock()
        mock_parsed.data = [mock_resource]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_response.parsed = mock_parsed

        async def fake_list(*args, **kwargs):
            return mock_response

        mock_list.side_effect = fake_list

        async def run():
            with patch(
                "smplkit.config.models.AsyncConfig._build_chain",
                return_value=[{"id": "db", "values": {"host": "new-host"}, "environments": {}}],
            ):
                await client.config.refresh()

        asyncio.run(run())
        assert client.config._config_cache["db"]["host"] == "new-host"

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_refresh_fires_listeners(self, mock_list):
        client = _make_connected_async_client({"db": {"host": "old"}})

        events = []
        client.config.on_change(lambda e: events.append(e))

        mock_attrs = MagicMock()
        mock_attrs.name = "DB"
        mock_attrs.description = None
        mock_attrs.parent = None
        mock_attrs.items = None
        mock_attrs.environments = None
        mock_attrs.created_at = None
        mock_attrs.updated_at = None

        mock_resource = MagicMock()
        mock_resource.id = "db"
        mock_resource.attributes = mock_attrs

        mock_parsed = MagicMock()
        mock_parsed.data = [mock_resource]

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b""
        mock_response.parsed = mock_parsed

        async def fake_list(*args, **kwargs):
            return mock_response

        mock_list.side_effect = fake_list

        async def run():
            with patch(
                "smplkit.config.models.AsyncConfig._build_chain",
                return_value=[{"id": "db", "values": {"host": "new-host"}, "environments": {}}],
            ):
                await client.config.refresh()

        asyncio.run(run())
        assert len(events) == 1
        assert events[0].source == "manual"


# ===================================================================
# 7. ConfigChangeEvent
# ===================================================================


class TestConfigChangeEvent:
    def test_attributes(self):
        event = ConfigChangeEvent(
            config_id="db",
            item_key="host",
            old_value="old",
            new_value="new",
            source="manual",
        )
        assert event.config_id == "db"
        assert event.item_key == "host"
        assert event.old_value == "old"
        assert event.new_value == "new"
        assert event.source == "manual"

    def test_repr(self):
        event = ConfigChangeEvent(
            config_id="db",
            item_key="host",
            old_value="old",
            new_value="new",
            source="websocket",
        )
        r = repr(event)
        assert "ConfigChangeEvent" in r
        assert "db" in r
        assert "host" in r


# ===================================================================
# 8. LiveConfigProxy — direct unit tests
# ===================================================================


class TestLiveConfigProxyDirect:
    def test_current_values_reads_from_cache(self):
        client = _make_connected_client({"db": {"host": "h", "port": 5432}})
        proxy = LiveConfigProxy(client.config, "db")
        assert proxy._current_values() == {"host": "h", "port": 5432}

    def test_current_values_missing_key(self):
        client = _make_connected_client({})
        proxy = LiveConfigProxy(client.config, "missing")
        assert proxy._current_values() == {}

    def test_setattr_raises(self):
        client = _make_connected_client({"db": {"host": "h"}})
        proxy = LiveConfigProxy(client.config, "db")
        with pytest.raises(AttributeError, match="read-only"):
            proxy.host = "spoofed"

    def test_setitem_raises(self):
        client = _make_connected_client({"db": {"host": "h"}})
        proxy = LiveConfigProxy(client.config, "db")
        with pytest.raises(TypeError, match="read-only"):
            proxy["host"] = "spoofed"

    def test_delattr_raises(self):
        client = _make_connected_client({"db": {"host": "h"}})
        proxy = LiveConfigProxy(client.config, "db")
        with pytest.raises(AttributeError, match="read-only"):
            del proxy.host

    def test_delitem_raises(self):
        client = _make_connected_client({"db": {"host": "h"}})
        proxy = LiveConfigProxy(client.config, "db")
        with pytest.raises(TypeError, match="read-only"):
            del proxy["host"]
