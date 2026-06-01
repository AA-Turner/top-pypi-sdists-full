"""Tests for ConfigClient and AsyncConfigClient."""

import asyncio
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from smplkit._errors import (
    ConnectionError,
    NotFoundError,
    TimeoutError,
    ValidationError,
)
from smplkit.client import AsyncSmplClient, SmplClient
from smplkit.config.client import AsyncConfigClient, LiveConfigProxy
from smplkit.config.helpers import _resource_to_config


def _new_mgmt():
    """Build a SmplManagementClient for management-flavored tests."""
    from smplkit import SmplManagementClient

    return SmplManagementClient(api_key="sk_test", base_domain="example.test")


def _new_async_mgmt():
    """Build an AsyncSmplManagementClient for management-flavored tests."""
    from smplkit import AsyncSmplManagementClient

    return AsyncSmplManagementClient(api_key="sk_test", base_domain="example.test")


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
        mgmt = _new_mgmt()
        cfg = mgmt.config.new("my_service")
        assert cfg.id == "my_service"
        assert cfg.created_at is None
        assert cfg.name == "My Service"  # auto-generated from id

    def test_new_with_explicit_name(self):
        mgmt = _new_mgmt()
        cfg = mgmt.config.new("my_service", name="Custom Name")
        assert cfg.name == "Custom Name"

    def test_new_with_description_and_parent(self):
        mgmt = _new_mgmt()
        cfg = mgmt.config.new("child_svc", description="A child", parent=_TEST_UUID)
        assert cfg.description == "A child"
        assert cfg.parent == _TEST_UUID

    def test_new_accepts_config_instance_as_parent(self):
        mgmt = _new_mgmt()
        parent = mgmt.config.new("parent_svc")
        parent.id = "parent_svc"  # simulate persisted (created_at left unset)
        child = mgmt.config.new("child_svc", parent=parent)
        assert child.parent == "parent_svc"

    def test_new_rejects_unsaved_config_as_parent(self):
        mgmt = _new_mgmt()
        unsaved = mgmt.config.new("unsaved")
        unsaved.id = ""  # simulate id missing
        with pytest.raises(ValueError, match="must be saved"):
            mgmt.config.new("child_svc", parent=unsaved)


# ===================================================================
# ConfigClient — get() by id
# ===================================================================


class TestConfigClientGet:
    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_by_id(self, mock_get):
        resource = _mock_resource(id="common", name="Common")
        mock_get.return_value = _mock_single_response(resource)

        mgmt = _new_mgmt()
        cfg = mgmt.config.get("common")
        assert cfg.id == "common"
        mock_get.assert_called_once()

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_not_found_404(self, mock_get):
        mock_get.return_value = _mock_response(status_code=HTTPStatus.NOT_FOUND, content=b"Not Found")
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.config.get("nonexistent")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_not_found_parsed_none(self, mock_get):
        mock_get.return_value = _mock_response(parsed=None)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.config.get("missing")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_not_found_no_data_attr(self, mock_get):
        parsed = MagicMock(spec=[])  # no .data attribute
        mock_get.return_value = _mock_response(parsed=parsed)
        mgmt = _new_mgmt()
        with pytest.raises(NotFoundError):
            mgmt.config.get("missing")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_network_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("connection refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.config.get("common")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_timeout(self, mock_get):
        mock_get.side_effect = httpx.ReadTimeout("timed out")
        mgmt = _new_mgmt()
        with pytest.raises(TimeoutError):
            mgmt.config.get("common")

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_get_reraises_non_network_error(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="unexpected"):
            mgmt.config.get("common")


# ===================================================================
# ConfigClient — list()
# ===================================================================


class TestConfigClientList:
    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_list(self, mock_list):
        resource = _mock_resource(id="c1", name="Config 1")
        mock_list.return_value = _mock_list_response([resource])

        mgmt = _new_mgmt()
        configs = mgmt.config.list()
        assert len(configs) == 1
        assert configs[0].id == "c1"

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.config.list()

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_list_parsed_none(self, mock_list):
        mock_list.return_value = _mock_response(parsed=None)
        mgmt = _new_mgmt()
        assert mgmt.config.list() == []

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_list_no_data_attr(self, mock_list):
        parsed = MagicMock(spec=[])
        mock_list.return_value = _mock_response(parsed=parsed)
        mgmt = _new_mgmt()
        assert mgmt.config.list() == []

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_list_reraises_non_network_error(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="unexpected"):
            mgmt.config.list()


# ===================================================================
# ConfigClient — delete() by id
# ===================================================================


class TestConfigClientDelete:
    @patch("smplkit.config.client.delete_config.sync_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _mock_response(status_code=HTTPStatus.NO_CONTENT)

        mgmt = _new_mgmt()
        mgmt.config.delete("my_config")

        mock_delete.assert_called_once()

    @patch("smplkit.config.client.delete_config.sync_detailed")
    def test_delete_network_error(self, mock_delete):
        mock_delete.side_effect = httpx.ConnectError("refused")

        mgmt = _new_mgmt()
        with pytest.raises(ConnectionError):
            mgmt.config.delete("my_config")

    @patch("smplkit.config.client.delete_config.sync_detailed")
    def test_delete_reraises_non_network_error(self, mock_delete):
        mock_delete.side_effect = RuntimeError("unexpected")

        mgmt = _new_mgmt()
        with pytest.raises(RuntimeError, match="unexpected"):
            mgmt.config.delete("my_config")


# ===================================================================
# ConfigClient — _create_config / _update_config_from_model (for Config.save)
# ===================================================================


class TestConfigClientCreateUpdate:
    @patch("smplkit.config.client.create_config.sync_detailed")
    def test_create_config(self, mock_create):
        resource = _mock_resource(id="new_config", name="New Config")
        mock_create.return_value = _mock_single_response(resource, status_code=HTTPStatus.CREATED)

        mgmt = _new_mgmt()
        cfg = mgmt.config.new("new_config")
        result = mgmt.config._create_config(cfg)
        assert result.id == "new_config"
        assert result.name == "New Config"

    @patch("smplkit.config.client.create_config.sync_detailed")
    def test_create_config_network_error(self, mock_create):
        mock_create.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        cfg = mgmt.config.new("test")
        with pytest.raises(ConnectionError):
            mgmt.config._create_config(cfg)

    @patch("smplkit.config.client.create_config.sync_detailed")
    def test_create_config_parsed_none(self, mock_create):
        mock_create.return_value = _mock_response(parsed=None)
        mgmt = _new_mgmt()
        cfg = mgmt.config.new("test")
        with pytest.raises(ValidationError):
            mgmt.config._create_config(cfg)

    @patch("smplkit.config.client.create_config.sync_detailed")
    def test_create_config_reraises_non_network_error(self, mock_create):
        mock_create.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        cfg = mgmt.config.new("test")
        with pytest.raises(RuntimeError, match="unexpected"):
            mgmt.config._create_config(cfg)

    @patch("smplkit.config.client.update_config.sync_detailed")
    def test_update_config_from_model(self, mock_update):
        resource = _mock_resource(id="test", name="Updated")
        mock_update.return_value = _mock_single_response(resource)

        mgmt = _new_mgmt()
        from smplkit.config.models import Config

        cfg = Config(mgmt.config, id="test", name="Old")
        result = mgmt.config._update_config_from_model(cfg)
        assert result.name == "Updated"

    @patch("smplkit.config.client.update_config.sync_detailed")
    def test_update_config_from_model_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")
        mgmt = _new_mgmt()
        from smplkit.config.models import Config

        cfg = Config(mgmt.config, id="test", name="T")
        with pytest.raises(ConnectionError):
            mgmt.config._update_config_from_model(cfg)

    @patch("smplkit.config.client.update_config.sync_detailed")
    def test_update_config_from_model_parsed_none(self, mock_update):
        mock_update.return_value = _mock_response(parsed=None)
        mgmt = _new_mgmt()
        from smplkit.config.models import Config

        cfg = Config(mgmt.config, id="test", name="T")
        with pytest.raises(ValidationError):
            mgmt.config._update_config_from_model(cfg)

    @patch("smplkit.config.client.update_config.sync_detailed")
    def test_update_config_from_model_reraises_non_network_error(self, mock_update):
        mock_update.side_effect = RuntimeError("unexpected")
        mgmt = _new_mgmt()
        from smplkit.config.models import Config

        cfg = Config(mgmt.config, id="test", name="T")
        with pytest.raises(RuntimeError, match="unexpected"):
            mgmt.config._update_config_from_model(cfg)


# ===================================================================
# ConfigClient — start
# ===================================================================


class TestConfigClientConnectInternal:
    def _make_mock_config(self, id, items_raw, environments=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg._build_chain.return_value = [{"id": id, "items": items_raw, "environments": environments or {}}]
        return cfg

    def test_connect_internal_populates_cache(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config.start()
        assert client.config._connected is True
        assert "db" in client.config._config_cache

    def test_connect_internal_is_idempotent(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]) as mock_list:
            client.config.start()
            client.config.start()
        mock_list.assert_called_once()


# ===================================================================
# ConfigClient — resolve()
# ===================================================================


class TestConfigClientResolve:
    def test_resolve_returns_flat_dict(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost", "port": 5432}}

        result = client.config.get("db")
        assert isinstance(result, LiveConfigProxy)
        assert dict(result) == {"host": "localhost", "port": 5432}

    def test_resolve_raises_not_found_for_missing_id(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {}

        with pytest.raises(NotFoundError, match="Config with id 'missing' not found"):
            client.config.get("missing")

    def test_resolve_triggers_connect(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        with patch.object(client.config, "start") as mock_connect:
            with patch.object(client.config, "_config_cache", {"db": {"host": "h"}}):
                client.config.get("db")
        mock_connect.assert_called_once()


# ===================================================================
# LiveConfigProxy — proxy.on_change(...) sugar
# ===================================================================


class TestLiveConfigProxyOnChange:
    def _proxy(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._connected = True
        client.config._config_cache = {"db": {"host": "localhost"}}
        return client, client.config.get("db")

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
    @patch("smplkit.config.client.list_configs.sync_detailed")
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

    @patch("smplkit.config.client.list_configs.sync_detailed")
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
    def test_bare_decorator(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci is None
        assert ik is None

    def test_with_config_id(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change("db")
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci == "db"
        assert ik is None

    def test_with_config_id_and_item_key(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change("db", item_key="host")
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci == "db"
        assert ik == "host"

    def test_empty_parens_decorator(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change()
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci is None
        assert ik is None

    def test_returns_original_function(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")

        def handler(event):
            pass

        result = client.config.on_change(handler)
        assert result is handler

    def test_config_id_decorator_returns_original_function(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change("db")
        def handler(event):
            pass

        # The outer call returns a decorator that returns the original fn
        assert callable(handler)


# ===================================================================
# ConfigClient — _fire_change_listeners
# ===================================================================


class TestFireChangeListeners:
    def test_filters_by_config_id(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
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
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
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
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {"db": {"host": "same"}},
            {"db": {"host": "same"}},
            source="manual",
        )
        assert len(events) == 0

    def test_listener_exception_is_caught(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
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
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
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
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
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
# ConfigClient — _to_model / _resource_to_model
# ===================================================================


class TestConfigClientModelConversion:
    def test_to_model(self):
        mgmt = _new_mgmt()
        resource = _mock_resource(id="test", name="Test")
        parsed = MagicMock()
        parsed.data = resource
        cfg = _resource_to_config(mgmt.config, parsed.data)
        assert cfg.id == "test"

    def test_resource_to_model(self):
        mgmt = _new_mgmt()
        resource = _mock_resource(id="test", name="Test", description="desc")
        cfg = _resource_to_config(mgmt.config, resource)
        assert cfg.id == "test"
        assert cfg.name == "Test"


# ===================================================================
# AsyncConfigClient — new()
# ===================================================================


class TestAsyncConfigClientNew:
    def test_new_returns_async_config_with_no_created_at(self):
        mgmt = _new_async_mgmt()
        cfg = mgmt.config.new("my_service")
        assert cfg.id == "my_service"
        assert cfg.created_at is None
        assert cfg.name == "My Service"

    def test_new_with_explicit_name(self):
        mgmt = _new_async_mgmt()
        cfg = mgmt.config.new("my_service", name="Custom Name")
        assert cfg.name == "Custom Name"

    def test_new_with_description_and_parent(self):
        mgmt = _new_async_mgmt()
        cfg = mgmt.config.new("child_svc", description="A child", parent=_TEST_UUID)
        assert cfg.description == "A child"
        assert cfg.parent == _TEST_UUID

    def test_new_accepts_async_config_instance_as_parent(self):
        mgmt = _new_async_mgmt()
        parent = mgmt.config.new("parent_svc")
        parent.id = "parent_svc"
        child = mgmt.config.new("child_svc", parent=parent)
        assert child.parent == "parent_svc"

    def test_new_rejects_unsaved_async_config_as_parent(self):
        mgmt = _new_async_mgmt()
        unsaved = mgmt.config.new("unsaved")
        unsaved.id = ""
        with pytest.raises(ValueError, match="must be saved"):
            mgmt.config.new("child_svc", parent=unsaved)


# ===================================================================
# AsyncConfigClient — get() by id
# ===================================================================


class TestAsyncConfigClientGet:
    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_by_id(self, mock_get):
        resource = _mock_resource(id="common", name="Common")
        mock_get.return_value = _mock_single_response(resource)

        async def _run():
            mgmt = _new_async_mgmt()
            cfg = await mgmt.config.get("common")
            assert cfg.id == "common"

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_not_found_404(self, mock_get):
        mock_get.return_value = _mock_response(status_code=HTTPStatus.NOT_FOUND, content=b"Not Found")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(NotFoundError):
                await mgmt.config.get("nonexistent")

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_not_found_parsed_none(self, mock_get):
        mock_get.return_value = _mock_response(parsed=None)

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(NotFoundError):
                await mgmt.config.get("missing")

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_not_found_no_data_attr(self, mock_get):
        parsed = MagicMock(spec=[])
        mock_get.return_value = _mock_response(parsed=parsed)

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(NotFoundError):
                await mgmt.config.get("missing")

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_network_error(self, mock_get):
        mock_get.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(ConnectionError):
                await mgmt.config.get("common")

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_timeout(self, mock_get):
        mock_get.side_effect = httpx.ReadTimeout("timed out")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(TimeoutError):
                await mgmt.config.get("common")

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.asyncio_detailed")
    def test_get_reraises_non_network_error(self, mock_get):
        mock_get.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(RuntimeError, match="unexpected"):
                await mgmt.config.get("common")

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — list()
# ===================================================================


class TestAsyncConfigClientList:
    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_list(self, mock_list):
        resource = _mock_resource(id="c1", name="C1")
        mock_list.return_value = _mock_list_response([resource])

        async def _run():
            mgmt = _new_async_mgmt()
            configs = await mgmt.config.list()
            assert len(configs) == 1

        asyncio.run(_run())

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_list_network_error(self, mock_list):
        mock_list.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(ConnectionError):
                await mgmt.config.list()

        asyncio.run(_run())

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_list_parsed_none(self, mock_list):
        mock_list.return_value = _mock_response(parsed=None)

        async def _run():
            mgmt = _new_async_mgmt()
            result = await mgmt.config.list()
            assert result == []

        asyncio.run(_run())

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_list_no_data_attr(self, mock_list):
        parsed = MagicMock(spec=[])
        mock_list.return_value = _mock_response(parsed=parsed)

        async def _run():
            mgmt = _new_async_mgmt()
            result = await mgmt.config.list()
            assert result == []

        asyncio.run(_run())

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
    def test_list_reraises_non_network_error(self, mock_list):
        mock_list.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(RuntimeError, match="unexpected"):
                await mgmt.config.list()

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — delete() by id
# ===================================================================


class TestAsyncConfigClientDelete:
    @patch("smplkit.config.client.delete_config.asyncio_detailed")
    def test_delete_by_id(self, mock_delete):
        mock_delete.return_value = _mock_response(status_code=HTTPStatus.NO_CONTENT)

        async def _run():
            mgmt = _new_async_mgmt()
            await mgmt.config.delete("my_config")

        asyncio.run(_run())
        mock_delete.assert_called_once()

    @patch("smplkit.config.client.delete_config.asyncio_detailed")
    def test_delete_network_error(self, mock_delete):
        mock_delete.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(ConnectionError):
                await mgmt.config.delete("my_config")

        asyncio.run(_run())

    @patch("smplkit.config.client.delete_config.asyncio_detailed")
    def test_delete_reraises_non_network_error(self, mock_delete):
        mock_delete.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            with pytest.raises(RuntimeError, match="unexpected"):
                await mgmt.config.delete("my_config")

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — _create_config / _update_config_from_model
# ===================================================================


class TestAsyncConfigClientCreateUpdate:
    @patch("smplkit.config.client.create_config.asyncio_detailed")
    def test_create_config(self, mock_create):
        resource = _mock_resource(id="new_config", name="New Config")
        mock_create.return_value = _mock_single_response(resource, status_code=HTTPStatus.CREATED)

        async def _run():
            mgmt = _new_async_mgmt()
            cfg = mgmt.config.new("new_config")
            result = await mgmt.config._create_config(cfg)
            assert result.id == "new_config"

        asyncio.run(_run())

    @patch("smplkit.config.client.create_config.asyncio_detailed")
    def test_create_config_network_error(self, mock_create):
        mock_create.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            cfg = mgmt.config.new("test")
            with pytest.raises(ConnectionError):
                await mgmt.config._create_config(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.client.create_config.asyncio_detailed")
    def test_create_config_parsed_none(self, mock_create):
        mock_create.return_value = _mock_response(parsed=None)

        async def _run():
            mgmt = _new_async_mgmt()
            cfg = mgmt.config.new("test")
            with pytest.raises(ValidationError):
                await mgmt.config._create_config(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.client.create_config.asyncio_detailed")
    def test_create_config_reraises_non_network_error(self, mock_create):
        mock_create.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            cfg = mgmt.config.new("test")
            with pytest.raises(RuntimeError, match="unexpected"):
                await mgmt.config._create_config(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.client.update_config.asyncio_detailed")
    def test_update_config_from_model(self, mock_update):
        resource = _mock_resource(id="test", name="Updated")
        mock_update.return_value = _mock_single_response(resource)

        async def _run():
            mgmt = _new_async_mgmt()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(mgmt.config, id="test", name="Old")
            result = await mgmt.config._update_config_from_model(cfg)
            assert result.name == "Updated"

        asyncio.run(_run())

    @patch("smplkit.config.client.update_config.asyncio_detailed")
    def test_update_config_from_model_network_error(self, mock_update):
        mock_update.side_effect = httpx.ConnectError("refused")

        async def _run():
            mgmt = _new_async_mgmt()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(mgmt.config, id="test", name="T")
            with pytest.raises(ConnectionError):
                await mgmt.config._update_config_from_model(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.client.update_config.asyncio_detailed")
    def test_update_config_from_model_parsed_none(self, mock_update):
        mock_update.return_value = _mock_response(parsed=None)

        async def _run():
            mgmt = _new_async_mgmt()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(mgmt.config, id="test", name="T")
            with pytest.raises(ValidationError):
                await mgmt.config._update_config_from_model(cfg)

        asyncio.run(_run())

    @patch("smplkit.config.client.update_config.asyncio_detailed")
    def test_update_config_from_model_reraises_non_network_error(self, mock_update):
        mock_update.side_effect = RuntimeError("unexpected")

        async def _run():
            mgmt = _new_async_mgmt()
            from smplkit.config.models import AsyncConfig

            cfg = AsyncConfig(mgmt.config, id="test", name="T")
            with pytest.raises(RuntimeError, match="unexpected"):
                await mgmt.config._update_config_from_model(cfg)

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — start
# ===================================================================


class TestAsyncConfigClientConnectInternal:
    def _make_mock_config(self, id, items_raw, environments=None):
        cfg = MagicMock()
        cfg.id = id
        cfg._items_raw = items_raw
        cfg.environments = environments or {}
        cfg._build_chain = AsyncMock(return_value=[{"id": id, "items": items_raw, "environments": environments or {}}])
        return cfg

    def test_connect_internal_populates_cache(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ):
                await client.config.start()
            assert client.config._connected is True
            assert "db" in client.config._config_cache

        asyncio.run(_run())

    def test_connect_internal_is_idempotent(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
            with patch.object(
                client.config, "_fetch_all_configs_async", new_callable=AsyncMock, return_value=[mock_cfg]
            ) as mock_list:
                await client.config.start()
                await client.config.start()
            mock_list.assert_called_once()

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — resolve()
# ===================================================================


class TestAsyncConfigClientResolve:
    def test_resolve_returns_flat_dict(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            client.config._connected = True
            client.config._config_cache = {"db": {"host": "localhost", "port": 5432}}
            result = await client.config.get("db")
            assert isinstance(result, LiveConfigProxy)
            assert dict(result) == {"host": "localhost", "port": 5432}

        asyncio.run(_run())

    def test_resolve_raises_not_found_for_missing_id(self):
        async def _run():
            client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
            client.config._connected = True
            client.config._config_cache = {}
            with pytest.raises(NotFoundError, match="Config with id 'missing' not found"):
                await client.config.get("missing")

        asyncio.run(_run())


# ===================================================================
# AsyncConfigClient — refresh()
# ===================================================================


class TestAsyncConfigClientRefresh:
    @patch("smplkit.config.client.list_configs.asyncio_detailed")
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

    @patch("smplkit.config.client.list_configs.asyncio_detailed")
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
    def test_bare_decorator(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change
        def handler(event):
            pass

        assert len(client.config._listeners) == 1
        fn, ci, ik = client.config._listeners[0]
        assert fn is handler
        assert ci is None

    def test_with_config_id(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change("db")
        def handler(event):
            pass

        fn, ci, ik = client.config._listeners[0]
        assert ci == "db"

    def test_with_config_id_and_item_key(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change("db", item_key="host")
        def handler(event):
            pass

        fn, ci, ik = client.config._listeners[0]
        assert ci == "db"
        assert ik == "host"

    def test_empty_parens_decorator(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")

        @client.config.on_change()
        def handler(event):
            pass

        fn, ci, ik = client.config._listeners[0]
        assert ci is None

    def test_fire_change_listeners(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
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
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
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
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        events = []
        client.config.on_change(lambda e: events.append(e))
        client.config._fire_change_listeners(
            {"db": {"host": "same"}},
            {"db": {"host": "same"}},
            source="manual",
        )
        assert len(events) == 0

    def test_listener_exception_is_caught(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
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
# AsyncConfigClient — _to_model / _resource_to_model
# ===================================================================


class TestAsyncConfigClientModelConversion:
    def test_init(self):
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        assert isinstance(client.config, AsyncConfigClient)

    def test_to_model(self):
        mgmt = _new_async_mgmt()
        resource = _mock_resource(id="test", name="Test")
        parsed = MagicMock()
        parsed.data = resource
        cfg = _resource_to_config(mgmt.config, parsed.data)
        assert cfg.id == "test"

    def test_resource_to_model(self):
        mgmt = _new_async_mgmt()
        resource = _mock_resource(id="test", name="Test")
        cfg = _resource_to_config(mgmt.config, resource)
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

    def test_connect_internal_registers_ws_handlers(self):
        client = SmplClient(api_key="sk_test", environment="test", service="svc")
        mock_ws = MagicMock()
        client._ensure_ws = MagicMock(return_value=mock_ws)
        mock_cfg = self._make_mock_config("db", {"host": {"value": "localhost"}})
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            client.config.start()
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
            with patch("smplkit.config.client.ws_logger") as mock_logger:
                client.config._handle_config_changed({"id": "db"})
        mock_logger.error.assert_called_once()

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
    def test_connect_internal_registers_ws_handlers(self):
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
                await client.config.start()
            client._ensure_ws.assert_called_once()
            mock_ws.on.assert_any_call("config_changed", client.config._handle_config_changed)
            mock_ws.on.assert_any_call("config_deleted", client.config._handle_config_deleted)
            mock_ws.on.assert_any_call("configs_changed", client.config._handle_configs_changed)
            assert mock_ws.on.call_count == 3
            assert client.config._ws_manager is mock_ws

        asyncio.run(_run())

    @patch("smplkit.config.client.get_config.sync_detailed")
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

    @patch("smplkit.config.client.get_config.sync_detailed")
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

    @patch("smplkit.config.client.list_configs.sync_detailed")
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

    @patch("smplkit.config.client.get_config.sync_detailed")
    def test_handle_config_changed_logs_error_on_fetch_failure(self, mock_get):
        mock_get.side_effect = RuntimeError("boom")
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        with patch("smplkit.config.client.ws_logger") as mock_logger:
            client.config._handle_config_changed({"id": "db"})
        mock_logger.error.assert_called_once()

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

    @patch("smplkit.config.client.list_configs.sync_detailed")
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

    @patch("smplkit.config.client.list_configs.sync_detailed")
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

    @patch("smplkit.config.client.list_configs.sync_detailed")
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

    @patch("smplkit.config.client.get_config.sync_detailed")
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

        mock_cfg = MagicMock()
        mock_cfg.id = "db"
        mock_cfg._items_raw = {"host": {"value": "new"}}
        mock_cfg.environments = {}
        mock_cfg.parent = None
        with _patch("smplkit.config.client.list_configs.sync_detailed") as mock_list:
            resource = _mock_resource(id="db", name="DB")
            resource.attributes.items = {"host": {"value": "new"}}
            resource.attributes.parent = None
            mock_list.return_value = _mock_list_response([resource])
            client.config._handle_config_deleted({})
        assert client.config._config_cache["db"]["host"] == "new"

    @patch("smplkit.config.client.list_configs.sync_detailed")
    def test_handle_configs_changed_error_is_swallowed(self, mock_list):
        mock_list.side_effect = RuntimeError("boom")
        client = AsyncSmplClient(api_key="sk_test", environment="test", service="svc")
        client.config._handle_configs_changed({})  # should not raise

    @patch("smplkit.config.client.list_configs.sync_detailed")
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
