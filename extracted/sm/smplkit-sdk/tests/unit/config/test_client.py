"""Tests for the fused ConfigClient and AsyncConfigClient.

The config client exposes one surface: management CRUD + discovery (pure
CRUD) and the live surface (``subscribe`` / ``get_value`` / ``bind`` /
``on_change`` / ``refresh``) which connects lazily on first use — no explicit
install step.
"""

import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from smplkit.errors import (
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
)
from smplkit.clients import AsyncSmplClient, SmplClient
from smplkit.config.clients import AsyncConfigClient, ConfigClient, LiveConfigProxy
from smplkit.config.helpers import _resource_to_config
from smplkit.config.models import AsyncConfig, Config


def _new_config() -> ConfigClient:
    """Build a wired sync config client for management-flavored tests."""
    return SmplClient(api_key="sk_test", base_domain="example.test").config


def _new_async_config() -> AsyncConfigClient:
    """Build a wired async config client for management-flavored tests."""
    return AsyncSmplClient(api_key="sk_test", base_domain="example.test").config


_TEST_UUID = "5a0c6be1-0000-0000-0000-000000000001"
_TEST_UUID_2 = "5a0c6be1-0000-0000-0000-000000000002"


def _mock_attrs(*, name="Test", description=None, parent=None, items=None, environments=None):
    """Create a mock attributes object for a config resource."""
    attrs = MagicMock()
    attrs.name = name
    attrs.description = description
    attrs.parent = parent
    attrs.items = items
    attrs.environments = environments
    attrs.created_at = None
    attrs.updated_at = None
    return attrs


def _mock_response(*, status_code=HTTPStatus.OK, parsed=None, content=b""):
    """Create a mock HTTP response."""
    resp = MagicMock()
    resp.status_code = status_code
    resp.content = content
    resp.parsed = parsed
    return resp


def _mock_list_response(resources):
    """Create a mock list response with the given resources."""
    parsed = MagicMock()
    parsed.data = resources
    return _mock_response(parsed=parsed)


def _mock_single_response(resource, status_code=HTTPStatus.OK):
    """Create a mock single-resource response."""
    parsed = MagicMock()
    parsed.data = resource
    return _mock_response(status_code=status_code, parsed=parsed)


def _mock_resource(id="test", **attr_kwargs):
    """Create a mock resource with attributes."""
    resource = MagicMock()
    resource.id = id
    resource.attributes = _mock_attrs(**attr_kwargs)
    return resource


# ===================================================================
# ConfigClient — new()
# ===================================================================


class TestConfigClientNew:
    def test_new_returns_config_with_no_created_at(self):
        cfg = _new_config().new("my_service")
        assert cfg.id == "my_service"
        assert cfg.created_at is None
        assert cfg.name == "My Service"  # auto-generated from id

    def test_new_with_explicit_name(self):
        cfg = _new_config().new("my_service", name="Custom Name")
        assert cfg.name == "Custom Name"

    def test_new_with_description_and_parent(self):
        cfg = _new_config().new("child_svc", description="A child", parent=_TEST_UUID)
        assert cfg.description == "A child"
        assert cfg.parent == _TEST_UUID

    def test_new_accepts_config_instance_as_parent(self):
        config = _new_config()
        parent = config.new("parent_svc")
        parent.id = "parent_svc"  # simulate persisted (created_at left unset)
        child = config.new("child_svc", parent=parent)
        assert child.parent == "parent_svc"

    def test_new_rejects_unsaved_config_as_parent(self):
        config = _new_config()
        unsaved = config.new("unsaved")
        unsaved.id = ""  # simulate id missing
        with pytest.raises(ValueError, match="must be saved"):
            config.new("child_svc", parent=unsaved)


# ===================================================================
# ConfigClient — get() by id (editable resource fetch)
# ===================================================================


class TestConfigClientGet:
    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_by_id(self, mock_get):
        resource = _mock_resource(id="common", name="Common")
        mock_get.return_value = _mock_single_response(resource)

        cfg = _new_config().get("common")
        assert cfg.id == "common"
        mock_get.assert_called_once()

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_not_found_404(self, mock_get):
        mock_get.return_value = _mock_response(status_code=HTTPStatus.NOT_FOUND, content=b"Not Found")
        with pytest.raises(NotFoundError):
            _new_config().get("nonexistent")

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_not_found_parsed_none(self, mock_get):
        mock_get.return_value = _mock_response(parsed=None)
        with pytest.raises(NotFoundError):
            _new_config().get("missing")

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_not_found_no_data_attr(self, mock_get):
        parsed = MagicMock(spec=[])  # no .data attribute
        mock_get.return_value = _mock_response(parsed=parsed)
        with pytest.raises(NotFoundError):
            _new_config().get("missing")

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_network_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("connection refused")
        with pytest.raises(ConnectionError):
            _new_config().get("common")

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_timeout(self, mock_get):
        mock_get.side_effect = httpx.ReadTimeout("timed out")
        with pytest.raises(TimeoutError):
            _new_config().get("common")

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_get_reraises_non_network_error(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")
        with pytest.raises(RuntimeError, match="unexpected"):
            _new_config().get("common")


# ===================================================================
# ConfigClient — list()
# ===================================================================


class TestConfigClientList:
    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_list(self, mock_list):
        resource = _mock_resource(id="c1", name="Config 1")
        mock_list.return_value = _mock_list_response([resource])

        configs = _new_config().list()
        assert len(configs) == 1
        assert configs[0].id == "c1"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("refused")
        with pytest.raises(ConnectionError):
            _new_config().list()

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_list_parsed_none(self, mock_list):
        mock_list.return_value = _mock_response(parsed=None)
        assert _new_config().list() == []

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_list_no_data_attr(self, mock_list):
        parsed = MagicMock(spec=[])
        mock_list.return_value = _mock_response(parsed=parsed)
        assert _new_config().list() == []

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_list_passes_pagination_kwargs(self, mock_list):
        mock_list.return_value = _mock_list_response([])
        _new_config().list(page_number=2, page_size=10)
        assert mock_list.call_args.kwargs["pagenumber"] == 2
        assert mock_list.call_args.kwargs["pagesize"] == 10

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_list_reraises_non_network_error(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        with pytest.raises(RuntimeError, match="unexpected"):
            _new_config().list()


# ===================================================================
# ConfigClient — delete() by id
# ===================================================================


class TestConfigClientDelete:
    @patch("smplkit.config.clients.delete_config.sync_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _mock_response(status_code=HTTPStatus.NO_CONTENT)
        _new_config().delete("my_config")
        mock_delete.assert_called_once()

    @patch("smplkit.config.clients.delete_config.sync_detailed")
    def test_delete_network_error(self, mock_delete):
        mock_delete.side_effect = httpx.ConnectError("refused")
        with pytest.raises(ConnectionError):
            _new_config().delete("my_config")

    @patch("smplkit.config.clients.delete_config.sync_detailed")
    def test_delete_reraises_non_network_error(self, mock_delete):
        mock_delete.side_effect = RuntimeError("unexpected")
        with pytest.raises(RuntimeError, match="unexpected"):
            _new_config().delete("my_config")


# ===================================================================
# ConfigClient — _create_config / _update_config_from_model (for Config.save)
# ===================================================================


class TestConfigClientCreateUpdate:
    @patch("smplkit.config.clients.create_config.sync_detailed")
    def test_create_config(self, mock_create):
        resource = _mock_resource(id="new_config", name="New Config")
        mock_create.return_value = _mock_single_response(resource, status_code=HTTPStatus.CREATED)

        config = _new_config()
        cfg = config.new("new_config")
        result = config._create_config(cfg)
        assert result.id == "new_config"
        assert result.name == "New Config"

    @patch("smplkit.config.clients.create_config.sync_detailed")
    def test_create_config_network_error(self, mock_create):
        mock_create.side_effect = httpx.ConnectError("refused")
        config = _new_config()
        cfg = config.new("test")
        with pytest.raises(ConnectionError):
            config._create_config(cfg)

    @patch("smplkit.config.clients.create_config.sync_detailed")
    def test_create_config_parsed_none(self, mock_create):
        mock_create.return_value = _mock_response(parsed=None)
        config = _new_config()
        cfg = config.new("test")
        with pytest.raises(ValidationError):
            config._create_config(cfg)

    @patch("smplkit.config.clients.create_config.sync_detailed")
    def test_create_config_reraises_non_network_error(self, mock_create):
        mock_create.side_effect = RuntimeError("unexpected")
        config = _new_config()
        cfg = config.new("test")
        with pytest.raises(RuntimeError, match="unexpected"):
            config._create_config(cfg)

    @patch("smplkit.config.clients.update_config.sync_detailed")
    def test_update_config_from_model(self, mock_update):
        resource = _mock_resource(id="test", name="Updated")
        mock_update.return_value = _mock_single_response(resource)

        config = _new_config()
        from smplkit.config.models import Config

        cfg = Config(config, id="test", name="Old")
        result = config._update_config_from_model(cfg)
        assert result.name == "Updated"

    @patch("smplkit.config.clients.update_config.sync_detailed")
    def test_update_config_from_model_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")
        config = _new_config()
        from smplkit.config.models import Config

        cfg = Config(config, id="test", name="T")
        with pytest.raises(ConnectionError):
            config._update_config_from_model(cfg)

    @patch("smplkit.config.clients.update_config.sync_detailed")
    def test_update_config_from_model_parsed_none(self, mock_update):
        mock_update.return_value = _mock_response(parsed=None)
        config = _new_config()
        from smplkit.config.models import Config

        cfg = Config(config, id="test", name="T")
        with pytest.raises(ValidationError):
            config._update_config_from_model(cfg)

    @patch("smplkit.config.clients.update_config.sync_detailed")
    def test_update_config_from_model_reraises_non_network_error(self, mock_update):
        mock_update.side_effect = RuntimeError("unexpected")
        config = _new_config()
        from smplkit.config.models import Config

        cfg = Config(config, id="test", name="T")
        with pytest.raises(RuntimeError, match="unexpected"):
            config._update_config_from_model(cfg)


# ===================================================================
# ConfigClient — lazy connect (_ensure_connected)
# ===================================================================


class TestConfigClientConnect:
    def _make_mock_config(self, id, items_raw, environments=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg._build_chain.return_value = [{"id": id, "items": items_raw, "environments": environments or {}}]
        return cfg

    def test_ensure_connected_populates_cache(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config._ensure_connected()
        assert client.config._connected is True
        assert "db" in client.config._config_cache

    def test_ensure_connected_is_idempotent(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]) as mock_list:
            client.config._ensure_connected()
            client.config._ensure_connected()
        mock_list.assert_called_once()


# ===================================================================
# ConfigClient — live methods auto-connect (no explicit install)
# ===================================================================


class TestConfigClientLazyConnect:
    def _make_mock_config(self, id, items_raw, environments=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg._build_chain.return_value = [{"id": id, "items": items_raw, "environments": environments or {}}]
        return cfg

    def test_subscribe_lazy_connects(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            proxy = client.config.subscribe("db")
        assert client.config._connected is True
        assert proxy["host"] == "localhost"

    def test_refresh_lazy_connects(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        with patch.object(client.config, "_fetch_all_configs", return_value=[]):
            client.config.refresh()
        assert client.config._connected is True

    def test_on_change_lazy_connects(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        with patch.object(client.config, "_fetch_all_configs", return_value=[]):
            client.config.on_change(lambda e: None)
        assert client.config._connected is True

    def test_get_value_lazy_connects(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            assert client.config.get_value("db", "host") == "localhost"
        assert client.config._connected is True


# ===================================================================
# ConfigClient — subscribe() proxy
# ===================================================================


class TestConfigClientSubscribe:
    def test_subscribe_returns_live_proxy(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost", "port": 5432}}

        result = client.config.subscribe("db")
        assert isinstance(result, LiveConfigProxy)
        assert dict(result) == {"host": "localhost", "port": 5432}

    def test_subscribe_raises_not_found_for_missing_id(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}

        with pytest.raises(NotFoundError, match="Config with id 'missing' not found"):
            client.config.subscribe("missing")

    def test_subscribe_registers_config_declaration(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "h"}}
        with patch.object(client.config, "register_config") as register:
            client.config.subscribe("db")
        register.assert_called_once()
        assert register.call_args.args[0] == "db"

    def test_subscribe_returns_same_cached_proxy(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "h"}}
        a = client.config.subscribe("db")
        b = client.config.subscribe("db")
        assert a is b


# ===================================================================
# LiveConfigProxy — proxy.on_change(...) sugar
# ===================================================================


class TestLiveConfigProxyOnChange:
    def _proxy(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost"}}
        return client, client.config.subscribe("db")

    def test_bare_decorator_registers_config_scoped(self):
        client, proxy = self._proxy()

        @proxy.on_change
        def listener(event):
            pass

        # last listener was added with config_id="db", item_key=None
        fn, config_id, item_key = client.config._listeners[-1]
        assert fn is listener
        assert config_id == "db"
        assert item_key is None

    def test_string_arg_registers_item_scoped(self):
        client, proxy = self._proxy()

        @proxy.on_change("host")
        def listener(event):
            pass

        fn, config_id, item_key = client.config._listeners[-1]
        assert fn is listener
        assert config_id == "db"
        assert item_key == "host"

    def test_no_args_registers_config_scoped(self):
        client, proxy = self._proxy()

        @proxy.on_change()
        def listener(event):
            pass

        fn, config_id, item_key = client.config._listeners[-1]
        assert fn is listener
        assert config_id == "db"
        assert item_key is None


# ===================================================================
# ConfigClient — refresh()
# ===================================================================


class TestConfigClientRefresh:
    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_refresh_updates_cache(self, mock_list):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}

        resource = _mock_resource(id="db", name="DB")
        mock_list.return_value = _mock_list_response([resource])

        with patch(
            "smplkit.config.models.Config._build_chain",
            return_value=[{"id": "cfg-1", "items": {}, "values": {"host": "new-host"}, "environments": {}}],
        ):
            client.config.refresh()

        assert client.config._config_cache["db"]["host"] == "new-host"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_refresh_fires_listeners(self, mock_list):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}

        events = []
        client.config.on_change(lambda e: events.append(e))

        resource = _mock_resource(id="db", name="DB")
        mock_list.return_value = _mock_list_response([resource])

        with patch(
            "smplkit.config.models.Config._build_chain",
            return_value=[{"id": "cfg-1", "values": {"host": "new-host"}, "environments": {}}],
        ):
            client.config.refresh()

        assert len(events) == 1
        assert events[0].config_id == "db"
        assert events[0].item_key == "host"
        assert events[0].old_value == "old"
        assert events[0].new_value == "new-host"
        assert events[0].source == "manual"


# ===================================================================
# ConfigClient — on_change() dual-mode decorator
# ===================================================================


class TestConfigClientOnChange:
    def _installed_client(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        return client

    def test_bare_decorator(self):
        client = self._installed_client()

        @client.config.on_change
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci is None
        assert ik is None

    def test_with_config_id(self):
        client = self._installed_client()

        @client.config.on_change("db")
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci == "db"
        assert ik is None

    def test_with_config_id_and_item_key(self):
        client = self._installed_client()

        @client.config.on_change("db", item_key="host")
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci == "db"
        assert ik == "host"

    def test_empty_parens_decorator(self):
        client = self._installed_client()

        @client.config.on_change()
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci is None
        assert ik is None

    def test_returns_original_function(self):
        client = self._installed_client()

        def handler(event):
            pass

        result = client.config.on_change(handler)
        assert result is handler

    def test_config_id_decorator_returns_original_function(self):
        client = self._installed_client()

        @client.config.on_change("db")
        def handler(event):
            pass

        # The outer call returns a decorator that returns the original fn
        assert callable(handler)


# ===================================================================
# ConfigClient — _fire_change_listeners
# ===================================================================


class TestFireChangeListeners:
    def _installed_client(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        return client

    def test_filters_by_config_id(self):
        client = self._installed_client()
        events = []

        @client.config.on_change("db")
        def handler(event):
            events.append(event)

        client.config._fire_change_listeners(
            {"db": {"host": "old"}, "other": {"x": 1}},
            {"db": {"host": "new"}, "other": {"x": 2}},
            source="manual",
        )
        assert len(events) == 1
        assert events[0].config_id == "db"

    def test_filters_by_item_key(self):
        client = self._installed_client()
        events = []

        @client.config.on_change("db", item_key="host")
        def handler(event):
            events.append(event)

        client.config._fire_change_listeners(
            {"db": {"host": "old", "port": 1}},
            {"db": {"host": "new", "port": 2}},
            source="manual",
        )
        assert len(events) == 1
        assert events[0].item_key == "host"

    def test_no_change_fires_nothing(self):
        client = self._installed_client()
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {"db": {"host": "same"}},
            {"db": {"host": "same"}},
            source="manual",
        )
        assert len(events) == 0

    def test_listener_exception_is_caught(self):
        client = self._installed_client()
        good_events = []

        def bad_listener(event):
            raise ValueError("boom")

        client.config.on_change(bad_listener)
        client.config.on_change(lambda e: good_events.append(e))

        client.config._fire_change_listeners(
            {"db": {"host": "old"}},
            {"db": {"host": "new"}},
            source="manual",
        )
        assert len(good_events) == 1

    def test_new_config_in_new_cache(self):
        client = self._installed_client()
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {},
            {"db": {"host": "new"}},
            source="manual",
        )
        assert len(events) == 1
        assert events[0].old_value is None
        assert events[0].new_value == "new"

    def test_removed_config_in_new_cache(self):
        client = self._installed_client()
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {"db": {"host": "old"}},
            {},
            source="manual",
        )
        assert len(events) == 1
        assert events[0].old_value == "old"
        assert events[0].new_value is None


# ===================================================================
# ConfigClient — _resource_to_config
# ===================================================================


class TestConfigClientModelConversion:
    def test_to_model(self):
        config = _new_config()
        resource = _mock_resource(id="test", name="Test")
        parsed = MagicMock()
        parsed.data = resource
        cfg = _resource_to_config(config, parsed.data)
        assert cfg.id == "test"

    def test_resource_to_model(self):
        config = _new_config()
        resource = _mock_resource(id="test", name="Test", description="desc")
        cfg = _resource_to_config(config, resource)
        assert cfg.id == "test"
        assert cfg.name == "Test"


# ===================================================================
# AsyncConfigClient — new()
# ===================================================================


class TestAsyncConfigClientNew:
    def test_new_returns_async_config_with_no_created_at(self):
        cfg = _new_async_config().new("my_service")
        assert cfg.id == "my_service"
        assert cfg.created_at is None
        assert cfg.name == "My Service"

    def test_new_with_explicit_name(self):
        cfg = _new_async_config().new("my_service", name="Custom Name")
        assert cfg.name == "Custom Name"

    def test_new_with_description_and_parent(self):
        cfg = _new_async_config().new("child_svc", description="A child", parent=_TEST_UUID)
        assert cfg.description == "A child"
        assert cfg.parent == _TEST_UUID

    def test_new_accepts_async_config_instance_as_parent(self):
        config = _new_async_config()
        parent = config.new("parent_svc")
        parent.id = "parent_svc"
        child = config.new("child_svc", parent=parent)
        assert child.parent == "parent_svc"

    def test_new_rejects_unsaved_async_config_as_parent(self):
        config = _new_async_config()
        unsaved = config.new("unsaved")
        unsaved.id = ""
        with pytest.raises(ValueError, match="must be saved"):
            config.new("child_svc", parent=unsaved)


# ===================================================================
# AsyncConfigClient — get() by id
# ===================================================================


class TestAsyncConfigClientGet:
    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_by_id(self, mock_get):
        resource = _mock_resource(id="common", name="Common")
        mock_get.return_value = _mock_single_response(resource)

        async def _run():
            cfg = await _new_async_config().get("common")
            assert cfg.id == "common"

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_not_found_404(self, mock_get):
        mock_get.return_value = _mock_response(status_code=HTTPStatus.NOT_FOUND, content=b"Not Found")

        async def _run():
            with pytest.raises(NotFoundError):
                await _new_async_config().get("nonexistent")

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_not_found_parsed_none(self, mock_get):
        mock_get.return_value = _mock_response(parsed=None)

        async def _run():
            with pytest.raises(NotFoundError):
                await _new_async_config().get("missing")

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_not_found_no_data_attr(self, mock_get):
        parsed = MagicMock(spec=[])
        mock_get.return_value = _mock_response(parsed=parsed)

        async def _run():
            with pytest.raises(NotFoundError):
                await _new_async_config().get("missing")

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_network_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")

        async def _run():
            with pytest.raises(ConnectionError):
                await _new_async_config().get("common")

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_timeout(self, mock_get):
        mock_get.side_effect = httpx.ReadTimeout("timed out")

        async def _run():
            with pytest.raises(TimeoutError):
                await _new_async_config().get("common")

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.asyncio_detailed")
    def test_get_reraises_non_network_error(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")

        async def _run():
            with pytest.raises(RuntimeError, match="unexpected"):
                await _new_async_config().get("common")

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — list()
# ===================================================================


class TestAsyncConfigClientList:
    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_list(self, mock_list):
        resource = _mock_resource(id="c1", name="C1")
        mock_list.return_value = _mock_list_response([resource])

        async def _run():
            configs = await _new_async_config().list()
            assert len(configs) == 1

        asyncio.run(_run())

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("refused")

        async def _run():
            with pytest.raises(ConnectionError):
                await _new_async_config().list()

        asyncio.run(_run())

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_list_parsed_none(self, mock_list):
        mock_list.return_value = _mock_response(parsed=None)

        async def _run():
            result = await _new_async_config().list()
            assert result == []

        asyncio.run(_run())

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_list_no_data_attr(self, mock_list):
        parsed = MagicMock(spec=[])
        mock_list.return_value = _mock_response(parsed=parsed)

        async def _run():
            result = await _new_async_config().list()
            assert result == []

        asyncio.run(_run())

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_list_passes_pagination_kwargs(self, mock_list):
        mock_list.return_value = _mock_list_response([])

        async def _run():
            await _new_async_config().list(page_number=3, page_size=20)

        asyncio.run(_run())
        assert mock_list.call_args.kwargs["pagenumber"] == 3
        assert mock_list.call_args.kwargs["pagesize"] == 20

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_list_reraises_non_network_error(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")

        async def _run():
            with pytest.raises(RuntimeError, match="unexpected"):
                await _new_async_config().list()

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — delete() by id
# ===================================================================


class TestAsyncConfigClientDelete:
    @patch("smplkit.config.clients.delete_config.asyncio_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _mock_response(status_code=HTTPStatus.NO_CONTENT)

        async def _run():
            await _new_async_config().delete("my_config")

        asyncio.run(_run())
        mock_delete.assert_called_once()

    @patch("smplkit.config.clients.delete_config.asyncio_detailed")
    def test_delete_network_error(self, mock_delete):
        mock_delete.side_effect = httpx.ConnectError("refused")

        async def _run():
            with pytest.raises(ConnectionError):
                await _new_async_config().delete("my_config")

        asyncio.run(_run())

    @patch("smplkit.config.clients.delete_config.asyncio_detailed")
    def test_delete_reraises_non_network_error(self, mock_delete):
        mock_delete.side_effect = RuntimeError("unexpected")

        async def _run():
            with pytest.raises(RuntimeError, match="unexpected"):
                await _new_async_config().delete("my_config")

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — _create_config / _update_config_from_model
# ===================================================================


class TestAsyncConfigClientCreateUpdate:
    @patch("smplkit.config.clients.create_config.asyncio_detailed")
    def test_create_config(self, mock_create):
        resource = _mock_resource(id="new_config", name="New Config")
        mock_create.return_value = _mock_single_response(resource, status_code=HTTPStatus.CREATED)

        async def _run():
            config = _new_async_config()
            cfg = config.new("new_config")
            result = await config._create_config(cfg)
            assert result.id == "new_config"

        asyncio.run(_run())

    @patch("smplkit.config.clients.create_config.asyncio_detailed")
    def test_create_config_network_error(self, mock_create):
        mock_create.side_effect = httpx.ConnectError("refused")

        async def _run():
            config = _new_async_config()
            cfg = config.new("test")
            with pytest.raises(ConnectionError):
                await config._create_config(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.clients.create_config.asyncio_detailed")
    def test_create_config_parsed_none(self, mock_create):
        mock_create.return_value = _mock_response(parsed=None)

        async def _run():
            config = _new_async_config()
            cfg = config.new("test")
            with pytest.raises(ValidationError):
                await config._create_config(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.clients.create_config.asyncio_detailed")
    def test_create_config_reraises_non_network_error(self, mock_create):
        mock_create.side_effect = RuntimeError("unexpected")

        async def _run():
            config = _new_async_config()
            cfg = config.new("test")
            with pytest.raises(RuntimeError, match="unexpected"):
                await config._create_config(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.clients.update_config.asyncio_detailed")
    def test_update_config_from_model(self, mock_update):
        resource = _mock_resource(id="test", name="Updated")
        mock_update.return_value = _mock_single_response(resource)

        async def _run():
            config = _new_async_config()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(config, id="test", name="Old")
            result = await config._update_config_from_model(cfg)
            assert result.name == "Updated"

        asyncio.run(_run())

    @patch("smplkit.config.clients.update_config.asyncio_detailed")
    def test_update_config_from_model_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")

        async def _run():
            config = _new_async_config()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(config, id="test", name="T")
            with pytest.raises(ConnectionError):
                await config._update_config_from_model(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.clients.update_config.asyncio_detailed")
    def test_update_config_from_model_parsed_none(self, mock_update):
        mock_update.return_value = _mock_response(parsed=None)

        async def _run():
            config = _new_async_config()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(config, id="test", name="T")
            with pytest.raises(ValidationError):
                await config._update_config_from_model(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.clients.update_config.asyncio_detailed")
    def test_update_config_from_model_reraises_non_network_error(self, mock_update):
        mock_update.side_effect = RuntimeError("unexpected")

        async def _run():
            config = _new_async_config()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(config, id="test", name="T")
            with pytest.raises(RuntimeError, match="unexpected"):
                await config._update_config_from_model(cfg)

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — lazy connect (_ensure_connected)
# ===================================================================


class TestAsyncConfigClientConnect:
    def _make_mock_config(self, id, items_raw, environments=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg._build_chain = AsyncMock(return_value=[{"id": id, "items": items_raw, "environments": environments or {}}])
        return cfg

    def test_ensure_connected_populates_cache(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ):
                await client.config._ensure_connected()
            assert client.config._connected is True
            assert "db" in client.config._config_cache

        asyncio.run(_run())

    def test_ensure_connected_is_idempotent(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ) as mock_list:
                await client.config._ensure_connected()
                await client.config._ensure_connected()
            mock_list.assert_called_once()

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — live methods auto-connect (no explicit install)
# ===================================================================


class TestAsyncConfigClientLazyConnect:
    def _make_mock_config(self, id, items_raw, environments=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg._build_chain = AsyncMock(return_value=[{"id": id, "items": items_raw, "environments": environments or {}}])
        return cfg

    def test_refresh_lazy_connects(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            with patch.object(client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[]):
                await client.config.refresh()
            assert client.config._connected is True

        asyncio.run(_run())

    def test_bind_lazy_connects(self):
        from pydantic import BaseModel

        class Cfg(BaseModel):
            x: int = 1

        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ):
                bound = await client.config.bind("db", Cfg())
            assert client.config._connected is True
            assert bound.x == 1

        asyncio.run(_run())

    def test_get_value_lazy_connects(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ):
                assert await client.config.get_value("db", "host") == "localhost"
            assert client.config._connected is True

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — subscribe()
# ===================================================================


class TestAsyncConfigClientSubscribe:
    def test_subscribe_returns_live_proxy(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost", "port": 5432}}
        result = client.config.subscribe("db")
        assert isinstance(result, LiveConfigProxy)
        assert dict(result) == {"host": "localhost", "port": 5432}

    def test_subscribe_raises_not_found_for_missing_id(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        with pytest.raises(NotFoundError, match="Config with id 'missing' not found"):
            client.config.subscribe("missing")


# ===================================================================
# AsyncConfigClient — refresh()
# ===================================================================


class TestAsyncConfigClientRefresh:
    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_refresh_updates_cache(self, mock_list):
        resource = _mock_resource(id="db", name="DB")

        async def fake_list(*args, **kwargs):
            return _mock_list_response([resource])

        mock_list.side_effect = fake_list

        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            client.config._connected = True
            client.config._config_cache = {"db": {"host": "old"}}
            with patch(
                "smplkit.config.models.AsyncConfig._build_chain",
                return_value=[{"id": "cfg-1", "values": {"host": "new-host"}, "environments": {}}],
            ):
                await client.config.refresh()
            assert client.config._config_cache["db"]["host"] == "new-host"

        asyncio.run(_run())

    @patch("smplkit.config.clients.list_configs.asyncio_detailed")
    def test_refresh_fires_listeners(self, mock_list):
        resource = _mock_resource(id="db", name="DB")

        async def fake_list(*args, **kwargs):
            return _mock_list_response([resource])

        mock_list.side_effect = fake_list

        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            client.config._connected = True
            client.config._config_cache = {"db": {"host": "old"}}
            events = []
            client.config.on_change(lambda e: events.append(e))

            with patch(
                "smplkit.config.models.AsyncConfig._build_chain",
                return_value=[{"id": "cfg-1", "values": {"host": "new-host"}, "environments": {}}],
            ):
                await client.config.refresh()
            assert len(events) == 1
            assert events[0].source == "manual"

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — on_change() dual-mode decorator
# ===================================================================


class TestAsyncConfigClientOnChange:
    def _installed_client(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        return client

    def test_bare_decorator(self):
        client = self._installed_client()

        @client.config.on_change
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci is None

    def test_with_config_id(self):
        client = self._installed_client()

        @client.config.on_change("db")
        def handler(event):
            pass

        fn, ci, ik = client.config._listeners[0]
        assert ci == "db"

    def test_with_config_id_and_item_key(self):
        client = self._installed_client()

        @client.config.on_change("db", item_key="host")
        def handler(event):
            pass

        fn, ci, ik = client.config._listeners[0]
        assert ci == "db"
        assert ik == "host"

    def test_empty_parens_decorator(self):
        client = self._installed_client()

        @client.config.on_change()
        def handler(event):
            pass

        fn, ci, ik = client.config._listeners[0]
        assert ci is None

    def test_fire_change_listeners(self):
        client = self._installed_client()
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {"db": {"host": "old"}},
            {"db": {"host": "new"}},
            source="manual",
        )
        assert len(events) == 1
        assert events[0].config_id == "db"
        assert events[0].item_key == "host"

    def test_fire_change_listeners_filters_work(self):
        client = self._installed_client()
        events = []

        @client.config.on_change("db", item_key="host")
        def handler(event):
            events.append(event)

        client.config._fire_change_listeners(
            {"db": {"host": "old", "port": 1}, "other": {"x": 1}},
            {"db": {"host": "new", "port": 2}, "other": {"x": 2}},
            source="manual",
        )
        assert len(events) == 1
        assert events[0].item_key == "host"

    def test_no_change_fires_nothing(self):
        client = self._installed_client()
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {"db": {"host": "same"}},
            {"db": {"host": "same"}},
            source="manual",
        )
        assert len(events) == 0

    def test_listener_exception_is_caught(self):
        client = self._installed_client()
        good_events = []

        def bad_listener(event):
            raise ValueError("boom")

        client.config.on_change(bad_listener)
        client.config.on_change(lambda e: good_events.append(e))

        client.config._fire_change_listeners(
            {"db": {"host": "old"}},
            {"db": {"host": "new"}},
            source="manual",
        )
        assert len(good_events) == 1


# ===================================================================
# AsyncConfigClient — _resource_to_config
# ===================================================================


class TestAsyncConfigClientModelConversion:
    def test_init(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        assert isinstance(client.config, AsyncConfigClient)

    def test_to_model(self):
        config = _new_async_config()
        resource = _mock_resource(id="test", name="Test")
        parsed = MagicMock()
        parsed.data = resource
        cfg = _resource_to_config(config, parsed.data)
        assert cfg.id == "test"

    def test_resource_to_model(self):
        config = _new_async_config()
        resource = _mock_resource(id="test", name="Test")
        cfg = _resource_to_config(config, resource)
        assert cfg.id == "test"


# ===================================================================
# ConfigClient — WebSocket event handling
# ===================================================================


class TestConfigClientWebSocket:
    def _make_mock_config(self, id, items_raw, environments=None, parent=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg.parent = parent
        cfg._build_chain.return_value = [{"id": id, "items": items_raw, "environments": environments or {}}]
        return cfg

    def test_connect_registers_ws_handlers(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_ws = MagicMock()
        client._ensure_ws = MagicMock(return_value=mock_ws)
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config._ensure_connected()
        client._ensure_ws.assert_called_once()
        mock_ws.on.assert_any_call("config_changed", client.config._handle_config_changed)
        mock_ws.on.assert_any_call("config_deleted", client.config._handle_config_deleted)
        mock_ws.on.assert_any_call("configs_changed", client.config._handle_configs_changed)
        assert mock_ws.on.call_count == 3
        assert client.config._ws_manager is mock_ws

    def test_handle_config_changed_scoped_fetch_updates_cache(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        mock_cfg = self._make_mock_config("db", {"host": {"value": "new"}})
        with patch.object(client.config, "_fetch_config", return_value=mock_cfg):
            client.config._handle_config_changed({"id": "db"})
        assert client.config._config_cache["db"]["host"] == "new"

    def test_handle_config_changed_fires_listener_on_change(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        events = []
        client.config.on_change(lambda e: events.append(e))
        mock_cfg = self._make_mock_config("db", {"host": {"value": "new"}})
        with patch.object(client.config, "_fetch_config", return_value=mock_cfg):
            client.config._handle_config_changed({"id": "db"})
        assert len(events) == 1
        assert events[0].source == "websocket"
        assert events[0].old_value == "old"
        assert events[0].new_value == "new"

    def test_handle_config_changed_no_id_falls_back_to_full_refresh(self):
        # When no "id" in payload, should do full refresh (configs_changed path)
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        mock_cfg = self._make_mock_config("db", {"host": {"value": "new"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config._handle_config_changed({})
        assert client.config._config_cache["db"]["host"] == "new"

    def test_handle_config_changed_logs_error_on_fetch_failure(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        with patch.object(client.config, "_fetch_config", side_effect=RuntimeError("boom")):
            with patch("smplkit.config.clients.ws_logger") as mock_logger:
                client.config._handle_config_changed({"id": "db"})
        mock_logger.error.assert_called_once()

    def test_handle_config_changed_fetches_uncached_parent_chain(self):
        """Regression: a config_changed for a child whose parent (and grandparent)
        are NOT in the raw cache fetches the ancestor chain so the child still
        resolves with its inherited values."""
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        client.config._raw_config_cache = {}
        base = Config(None, id="base", name="Base", parent=None, items={"region": {"value": "us-east"}})
        mid = Config(None, id="mid", name="Mid", parent="base", items={})
        child = Config(None, id="db", name="DB", parent="mid", items={"host": {"value": "local"}})
        fetched = {"db": child, "mid": mid, "base": base}
        with patch.object(client.config, "_fetch_config", side_effect=lambda cid: fetched[cid]):
            client.config._handle_config_changed({"id": "db"})
        # Inherited from the uncached grandparent, plus the child's own value.
        assert client.config._config_cache["db"]["region"] == "us-east"
        assert client.config._config_cache["db"]["host"] == "local"

    def test_handle_config_changed_keeps_already_cached_parent(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        base = Config(None, id="base", name="Base", parent=None, items={"region": {"value": "us-east"}})
        client.config._config_cache = {}
        client.config._raw_config_cache = {"base": base}
        child = Config(None, id="db", name="DB", parent="base", items={})
        with patch.object(client.config, "_fetch_config", side_effect=lambda cid: {"db": child}[cid]) as mock_fetch:
            client.config._handle_config_changed({"id": "db"})
        # Parent already cached → only the changed config is fetched.
        mock_fetch.assert_called_once_with("db")
        assert client.config._config_cache["db"]["region"] == "us-east"

    def test_handle_config_changed_missing_parent_is_logged(self):
        # A parent the server can't return leaves the chain unresolvable; the sync
        # resolver raises and the handler logs rather than crashing the WS thread.
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        client.config._raw_config_cache = {}
        child = Config(None, id="db", name="DB", parent="ghost", items={"host": {"value": "local"}})
        fetched = {"db": child, "ghost": None}
        with patch.object(client.config, "_fetch_config", side_effect=lambda cid: fetched[cid]):
            with patch("smplkit.config.clients.ws_logger") as mock_logger:
                client.config._handle_config_changed({"id": "db"})
        mock_logger.error.assert_called_once()
        assert "db" not in client.config._config_cache

    def test_handle_config_deleted_removes_from_cache(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost"}, "app": {"debug": True}}
        client.config._raw_config_cache = {"db": MagicMock(), "app": MagicMock()}
        client.config._handle_config_deleted({"id": "db"})
        assert "db" not in client.config._config_cache
        assert "app" in client.config._config_cache

    def test_handle_config_deleted_fires_listener(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost"}}
        client.config._raw_config_cache = {"db": MagicMock()}
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._handle_config_deleted({"id": "db"})
        assert any(e.config_id == "db" for e in events)

    def test_handle_config_deleted_no_id_falls_back_to_full_refresh(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        mock_cfg = self._make_mock_config("db", {"host": {"value": "new"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config._handle_config_deleted({})
        assert client.config._config_cache["db"]["host"] == "new"

    def test_handle_config_deleted_unknown_id_is_noop(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        before = {"db": {"host": "localhost"}}
        client.config._config_cache = dict(before)
        client.config._raw_config_cache = {"db": MagicMock()}
        events: list = []
        client.config.on_change(lambda e: events.append(e))
        client.config._handle_config_deleted({"id": "unknown"})
        assert client.config._config_cache == before
        assert events == []

    def test_handle_configs_changed_does_full_refresh(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        mock_cfg = self._make_mock_config("db", {"host": {"value": "new"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config._handle_configs_changed({})
        assert client.config._config_cache["db"]["host"] == "new"

    def test_refresh_uses_manual_source(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        events = []
        client.config.on_change(lambda e: events.append(e))
        mock_cfg = self._make_mock_config("db", {"host": {"value": "new"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config.refresh()
        assert events[0].source == "manual"

    def test_handle_configs_changed_error_is_swallowed(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        with patch.object(client.config, "_fetch_all_configs", side_effect=RuntimeError("boom")):
            client.config._handle_configs_changed({})  # should not raise


# ===================================================================
# AsyncConfigClient — WebSocket event handling
# ===================================================================


class TestAsyncConfigClientWebSocket:
    def test_connect_registers_ws_handlers(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_ws = MagicMock()
            client._ensure_ws = MagicMock(return_value=mock_ws)
            mock_cfg = MagicMock()
            mock_cfg.id = "db"
            mock_cfg._items_raw = {}
            mock_cfg.environments = {}
            mock_cfg._build_chain = AsyncMock(return_value=[{"id": "db", "items": {}, "environments": {}}])
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ):
                await client.config._ensure_connected()
            client._ensure_ws.assert_called_once()
            mock_ws.on.assert_any_call("config_changed", client.config._handle_config_changed)
            mock_ws.on.assert_any_call("config_deleted", client.config._handle_config_deleted)
            mock_ws.on.assert_any_call("configs_changed", client.config._handle_configs_changed)
            assert mock_ws.on.call_count == 3
            assert client.config._ws_manager is mock_ws

        asyncio.run(_run())

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_scoped_fetch_updates_cache(self, mock_get):
        resource = _mock_resource(id="db", name="DB")
        resource.attributes.items = {"host": {"value": "new"}}
        resource.attributes.parent = None
        mock_get.return_value = _mock_single_response(resource)
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        client.config._handle_config_changed({"id": "db"})
        mock_get.assert_called_once()
        assert client.config._config_cache["db"]["host"] == "new"

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_fires_listener_on_change(self, mock_get):
        resource = _mock_resource(id="db", name="DB")
        resource.attributes.items = {"host": {"value": "new"}}
        resource.attributes.parent = None
        mock_get.return_value = _mock_single_response(resource)
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._handle_config_changed({"id": "db"})
        assert len(events) == 1
        assert events[0].source == "websocket"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_config_changed_no_id_falls_back_to_full_refresh(self, mock_list):
        resource = _mock_resource(id="db", name="DB")
        resource.attributes.items = {"host": {"value": "new"}}
        resource.attributes.parent = None
        mock_list.return_value = _mock_list_response([resource])
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        client.config._handle_config_changed({})
        assert client.config._config_cache["db"]["host"] == "new"

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_logs_error_on_fetch_failure(self, mock_get):
        mock_get.side_effect = RuntimeError("boom")
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        with patch("smplkit.config.clients.ws_logger") as mock_logger:
            client.config._handle_config_changed({"id": "db"})
        mock_logger.error.assert_called_once()

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_fetches_uncached_parent_chain(self, mock_get):
        """Regression: a config_changed for a child whose parent (and grandparent)
        are NOT in the raw cache fetches the ancestor chain so the child still
        resolves with its inherited values."""
        base = _mock_resource(id="base", name="Base")
        base.attributes.items = {"region": {"value": "us-east"}}
        base.attributes.parent = None
        mid = _mock_resource(id="mid", name="Mid")
        mid.attributes.items = {}
        mid.attributes.parent = "base"
        child = _mock_resource(id="db", name="DB")
        child.attributes.items = {"host": {"value": "local"}}
        child.attributes.parent = "mid"
        responses = {
            "db": _mock_single_response(child),
            "mid": _mock_single_response(mid),
            "base": _mock_single_response(base),
        }
        mock_get.side_effect = lambda cid, **kw: responses[cid]
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        client.config._raw_config_cache = {}
        client.config._handle_config_changed({"id": "db"})
        assert client.config._config_cache["db"]["region"] == "us-east"
        assert client.config._config_cache["db"]["host"] == "local"

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_keeps_already_cached_parent(self, mock_get):
        child = _mock_resource(id="db", name="DB")
        child.attributes.items = {}
        child.attributes.parent = "base"
        mock_get.return_value = _mock_single_response(child)
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        base = AsyncConfig(None, id="base", name="Base", parent=None, items={"region": {"value": "us-east"}})
        client.config._config_cache = {}
        client.config._raw_config_cache = {"base": base}
        client.config._handle_config_changed({"id": "db"})
        # Parent already cached → only the changed config is fetched.
        mock_get.assert_called_once()
        assert client.config._config_cache["db"]["region"] == "us-east"

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_missing_parent_resolves_without_inheritance(self, mock_get):
        # Parent unavailable → the async resolver breaks the chain and the child
        # still updates with its own value.
        child = _mock_resource(id="db", name="DB")
        child.attributes.items = {"host": {"value": "local"}}
        child.attributes.parent = "ghost"
        responses = {"db": _mock_single_response(child), "ghost": _mock_response(parsed=None)}
        mock_get.side_effect = lambda cid, **kw: responses[cid]
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        client.config._raw_config_cache = {}
        client.config._handle_config_changed({"id": "db"})
        assert client.config._config_cache["db"]["host"] == "local"

    def test_handle_config_deleted_removes_from_cache_and_fires(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost"}, "app": {"debug": True}}
        client.config._raw_config_cache = {"db": MagicMock(), "app": MagicMock()}
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._handle_config_deleted({"id": "db"})
        assert "db" not in client.config._config_cache
        assert "app" in client.config._config_cache
        assert any(e.config_id == "db" for e in events)

    def test_handle_config_deleted_unknown_id_is_noop(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        before = {"db": {"host": "localhost"}}
        client.config._config_cache = dict(before)
        client.config._raw_config_cache = {"db": MagicMock()}
        events: list = []
        client.config.on_change(lambda e: events.append(e))
        client.config._handle_config_deleted({"id": "unknown"})
        assert client.config._config_cache == before
        assert events == []

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_configs_changed_does_full_refresh(self, mock_list):
        resource = _mock_resource(id="db", name="DB")
        resource.attributes.items = {"host": {"value": "new"}}
        resource.attributes.parent = None
        mock_list.return_value = _mock_list_response([resource])
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        client.config._handle_configs_changed({})
        assert client.config._config_cache["db"]["host"] == "new"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_configs_changed_resolves_parent_chain(self, mock_list):
        parent_resource = _mock_resource(id="base", name="Base")
        parent_resource.attributes.items = {"host": {"value": "base-host"}}
        parent_resource.attributes.parent = None
        child_resource = _mock_resource(id="db", name="DB")
        child_resource.attributes.items = {}
        child_resource.attributes.parent = "base"
        mock_list.return_value = _mock_list_response([parent_resource, child_resource])
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        client.config._handle_configs_changed({})
        assert client.config._config_cache["db"]["host"] == "base-host"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_configs_changed_missing_parent_breaks_chain(self, mock_list):
        # Child has parent="missing" but parent not in list → _build_chain_sync break path
        child_resource = _mock_resource(id="db", name="DB")
        child_resource.attributes.items = {"host": {"value": "local"}}
        child_resource.attributes.parent = "missing-parent"
        mock_list.return_value = _mock_list_response([child_resource])
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}
        client.config._handle_configs_changed({})
        assert client.config._config_cache["db"]["host"] == "local"

    @patch("smplkit.config.clients.get_config.sync_detailed")
    def test_handle_config_changed_no_parsed_data_returns_early(self, mock_get):
        # parsed is None → early return, cache unchanged
        mock_get.return_value = _mock_response(parsed=None)
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        original = {"db": {"host": "old"}}
        client.config._config_cache = original
        client.config._handle_config_changed({"id": "db"})

    def test_handle_config_deleted_no_id_falls_back_to_full_refresh(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "old"}}
        from unittest.mock import patch as _patch

        with _patch("smplkit.config.clients.list_configs.sync_detailed") as mock_list:
            resource = _mock_resource(id="db", name="DB")
            resource.attributes.items = {"host": {"value": "new"}}
            resource.attributes.parent = None
            mock_list.return_value = _mock_list_response([resource])
            client.config._handle_config_deleted({})
        assert client.config._config_cache["db"]["host"] == "new"

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_configs_changed_error_is_swallowed(self, mock_list):
        mock_list.side_effect = RuntimeError("boom")
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._handle_configs_changed({})  # should not raise

    @patch("smplkit.config.clients.list_configs.sync_detailed")
    def test_handle_configs_changed_null_parsed_returns_early(self, mock_list):
        mock_list.return_value = _mock_response(parsed=None)
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        original = {"db": {"host": "old"}}
        client.config._config_cache = dict(original)
        client.config._handle_configs_changed({})
        assert client.config._config_cache == original


def test_config_extra_headers_reach_transport() -> None:
    """extra_headers propagate to the config HTTP transport via the management client."""
    client = SmplClient(api_key="sk_api_test", environment="test", service="svc", extra_headers={"X-Test": "v"})
    try:
        assert client._http_client._headers.get("X-Test") == "v"
    finally:
        client.close()


# ===================================================================
# Standalone construction + lifecycle
# ===================================================================


class TestStandaloneConstruction:
    def test_standalone_builds_own_transport(self):
        config = ConfigClient(api_key="sk_test", base_domain="example.test", environment="prod")
        assert config._owns_transport is True
        assert config._parent is None
        assert config._environment == "prod"
        assert config._app_base_url == "https://app.example.test"
        config.close()

    def test_standalone_connect_opens_own_ws(self):
        config = ConfigClient(api_key="sk_test", base_domain="example.test", environment="prod")
        fake_ws = MagicMock()
        with patch("smplkit.config.clients.SharedWebSocket", return_value=fake_ws) as ws_cls:
            with patch.object(config, "_fetch_all_configs", return_value=[]):
                config._ensure_connected()
        ws_cls.assert_called_once()
        assert config._owns_ws is True
        assert config._ws_manager is fake_ws
        fake_ws.start.assert_called_once()
        config.close()
        fake_ws.stop.assert_called_once()

    def test_standalone_close_tears_down_owned_transport(self):
        config = ConfigClient(api_key="sk_test", base_domain="example.test")
        inner = MagicMock()
        config._http._client = inner
        config.close()
        inner.close.assert_called_once()
        assert config._http._client is None

    def test_wired_close_is_noop_on_borrowed_transport(self):
        client = SmplClient(api_key="sk_test", base_domain="example.test")
        sentinel = MagicMock()
        client.config._http._client = sentinel
        client.config.close()  # wired: owns neither transport nor ws
        # Borrowed transport is untouched by the config client's own close().
        assert client.config._http._client is sentinel
        client.close()

    def test_context_manager(self):
        with patch("smplkit.config.clients.SharedWebSocket"):
            with ConfigClient(api_key="sk_test", base_domain="example.test") as config:
                assert isinstance(config, ConfigClient)


class TestStandaloneAsyncConstruction:
    def test_standalone_builds_own_transport(self):
        config = AsyncConfigClient(api_key="sk_test", base_domain="example.test", environment="prod")
        assert config._owns_transport is True
        assert config._parent is None
        assert config._environment == "prod"

    def test_standalone_connect_opens_own_ws(self):
        async def _run():
            config = AsyncConfigClient(api_key="sk_test", base_domain="example.test", environment="prod")
            fake_ws = MagicMock()
            with patch("smplkit.config.clients.SharedWebSocket", return_value=fake_ws) as ws_cls:
                with patch.object(config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[]):
                    await config._ensure_connected()
            ws_cls.assert_called_once()
            assert config._owns_ws is True
            await config.close()
            fake_ws.stop.assert_called_once()

        asyncio.run(_run())

    def test_standalone_close_tears_down_owned_async_transport(self):
        async def _run():
            config = AsyncConfigClient(api_key="sk_test", base_domain="example.test")
            ac = AsyncMock()
            ac.aclose = AsyncMock()
            config._http._async_client = ac
            await config.close()
            ac.aclose.assert_awaited_once()
            assert config._http._async_client is None

        asyncio.run(_run())

    def test_async_context_manager(self):
        async def _run():
            async with AsyncConfigClient(api_key="sk_test", base_domain="example.test") as config:
                assert isinstance(config, AsyncConfigClient)

        asyncio.run(_run())
