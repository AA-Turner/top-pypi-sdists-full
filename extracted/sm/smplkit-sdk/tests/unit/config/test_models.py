"""Tests for Config and AsyncConfig model classes."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from smplkit.config.models import AsyncConfig, Config, ConfigEnvironment, ConfigItem, ItemType


def _make_config(**overrides) -> Config:
    """Create a Config with sensible defaults."""
    defaults = {
        "id": "test_config",
        "name": "Test Config",
        "description": "A test config",
        "parent": None,
        "items": {"retries": {"value": 3, "type": "NUMBER"}},
        "environments": {},
    }
    defaults.update(overrides)
    client = MagicMock()
    return Config(client, **defaults)


def _make_async_config(**overrides) -> AsyncConfig:
    """Create an AsyncConfig with sensible defaults."""
    defaults = {
        "id": "test_config",
        "name": "Test Config",
        "description": "A test config",
        "parent": None,
        "items": {"retries": {"value": 3, "type": "NUMBER"}},
        "environments": {},
    }
    defaults.update(overrides)
    client = MagicMock()
    return AsyncConfig(client, **defaults)


# ===================================================================
# Config — attributes and basics
# ===================================================================


class TestConfigAttributes:
    def test_attributes(self):
        cfg = _make_config()
        assert cfg.id == "test_config"
        assert cfg.name == "Test Config"
        assert cfg.description == "A test config"
        assert cfg.parent is None
        assert cfg.items == {"retries": 3}
        assert cfg.items_raw == {"retries": {"value": 3, "type": "NUMBER"}}
        assert cfg.environments == {}

    def test_repr(self):
        cfg = _make_config()
        r = repr(cfg)
        assert "Config(" in r
        assert "test_config" in r
        assert "Test Config" in r

    def test_items_default_to_empty_dict(self):
        client = MagicMock()
        cfg = Config(client, id="x", name="n")
        assert cfg.items == {}
        assert cfg.environments == {}

    def test_id_can_be_none(self):
        client = MagicMock()
        cfg = Config(client, id=None, name="n")
        assert cfg.id is None


# ===================================================================
# Config — settable items property
# ===================================================================


class TestConfigItemsAccess:
    def test_items_raw_returns_copy(self):
        cfg = _make_config()
        raw = cfg.items_raw
        raw["new_key"] = {"value": "should not leak"}
        assert "new_key" not in cfg.items_raw

    def test_items_returns_copy(self):
        cfg = _make_config()
        view = cfg.items
        view["new_key"] = "should not leak"
        assert "new_key" not in cfg.items

    def test_items_has_no_setter(self):
        cfg = _make_config()
        with pytest.raises(AttributeError):
            cfg.items = {"host": "localhost"}

    def test_environments_returns_copy(self):
        cfg = _make_config()
        cfg.set_number("max_retries", 5, environment="production")
        view = cfg.environments
        del view["production"]
        assert "production" in cfg.environments

    def test_environments_has_no_setter(self):
        cfg = _make_config()
        with pytest.raises(AttributeError):
            cfg.environments = {"prod": {}}


# ===================================================================
# Config — save()
# ===================================================================


class TestConfigSave:
    def test_save_creates_when_created_at_is_none(self):
        mock_client = MagicMock()
        created = _make_config(id="new-id", name="Created Config")
        mock_client._create_config.return_value = created

        cfg = Config(mock_client, id="test", name="Test")
        cfg.save()

        mock_client._create_config.assert_called_once_with(cfg)
        assert cfg.id == "new-id"
        assert cfg.name == "Created Config"

    def test_save_updates_when_created_at_is_set(self):
        import datetime

        mock_client = MagicMock()
        updated = _make_config(id="test_config", name="Updated Config")
        mock_client._update_config_from_model.return_value = updated

        cfg = Config(mock_client, id="test_config", name="Old Name")
        cfg.created_at = datetime.datetime(2025, 1, 1)
        cfg.save()

        mock_client._update_config_from_model.assert_called_once_with(cfg)
        assert cfg.name == "Updated Config"

    def test_delete_calls_client_delete(self):
        mock_client = MagicMock()
        cfg = Config(mock_client, id="test_config", name="X")
        cfg.delete()
        mock_client.delete.assert_called_once_with("test_config")

    def test_delete_without_client_raises(self):
        cfg = Config(None, id="x", name="X")
        with pytest.raises(RuntimeError, match="cannot delete"):
            cfg.delete()


# ===================================================================
# Config — _apply()
# ===================================================================


class TestConfigApply:
    def test_apply_copies_all_fields(self):
        import datetime

        cfg = _make_config(id="old-id", name="Old")
        other = _make_config(
            id="new-id",
            name="New",
            description="New desc",
            parent="parent-id",
            items={"host": {"value": "h"}},
            environments={"prod": {"host": "prod-h"}},
        )
        other.created_at = datetime.datetime(2025, 1, 1)
        other.updated_at = datetime.datetime(2025, 6, 1)

        cfg._apply(other)

        assert cfg.id == "new-id"
        assert cfg.name == "New"
        assert cfg.description == "New desc"
        assert cfg.parent == "parent-id"
        assert cfg.items == {"host": "h"}
        assert list(cfg.environments) == ["prod"]
        assert cfg.environments["prod"].values == {"host": "prod-h"}
        assert cfg.created_at == datetime.datetime(2025, 1, 1)
        assert cfg.updated_at == datetime.datetime(2025, 6, 1)

    def test_apply_copies_items_raw(self):
        cfg = _make_config()
        other = _make_config(items={"x": {"value": 99, "type": "NUMBER"}})
        cfg._apply(other)
        assert cfg._items_raw == {"x": {"value": 99, "type": "NUMBER"}}


# ===================================================================
# Config — _build_chain
# ===================================================================


class TestConfigBuildChain:
    def test_build_chain_no_parent(self):
        cfg = _make_config()
        chain = cfg._build_chain()
        assert len(chain) == 1
        assert chain[0]["id"] == "test_config"

    def test_build_chain_with_parent(self):
        parent_cfg = _make_config(
            id="parent-1",
            name="Parent",
            parent=None,
            items={"inherited": {"value": "yes"}, "shared": {"value": "parent_val"}},
            environments={},
        )
        mock_client = MagicMock()
        mock_client.get.return_value = parent_cfg

        child = Config(
            mock_client,
            id="child-1",
            name="Child",
            parent="parent-1",
            items={"shared": {"value": "child_val"}},
            environments={},
        )

        chain = child._build_chain()
        assert len(chain) == 2
        assert chain[0]["id"] == "child-1"
        assert chain[1]["id"] == "parent-1"
        mock_client.get.assert_called_once_with("parent-1")

    def test_build_chain_with_configs_list(self):
        """When a configs list is provided, parents are looked up by ID without calling get()."""
        parent_cfg = _make_config(
            id="parent-1",
            name="Parent",
            parent=None,
            items={"inherited": {"value": "yes"}},
            environments={},
        )
        mock_client = MagicMock()

        child = Config(
            mock_client,
            id="child-1",
            name="Child",
            parent="parent-1",
            items={"shared": {"value": "child_val"}},
            environments={},
        )

        chain = child._build_chain(configs=[parent_cfg, child])
        assert len(chain) == 2
        assert chain[0]["id"] == "child-1"
        assert chain[1]["id"] == "parent-1"
        mock_client.get.assert_not_called()


# ===================================================================
# AsyncConfig — attributes and basics
# ===================================================================


class TestAsyncConfigAttributes:
    def test_attributes(self):
        cfg = _make_async_config()
        assert cfg.id == "test_config"
        assert cfg.items == {"retries": 3}
        assert cfg.items_raw == {"retries": {"value": 3, "type": "NUMBER"}}

    def test_repr(self):
        cfg = _make_async_config()
        r = repr(cfg)
        assert "AsyncConfig(" in r
        assert "test_config" in r

    def test_id_can_be_none(self):
        client = MagicMock()
        cfg = AsyncConfig(client, id=None, name="n")
        assert cfg.id is None


# ===================================================================
# AsyncConfig — settable items property
# ===================================================================


class TestAsyncConfigItemsAccess:
    def test_items_raw_returns_copy(self):
        cfg = _make_async_config()
        raw = cfg.items_raw
        raw["new_key"] = {"value": "should not leak"}
        assert "new_key" not in cfg.items_raw

    def test_items_returns_copy(self):
        cfg = _make_async_config()
        view = cfg.items
        view["new_key"] = "should not leak"
        assert "new_key" not in cfg.items

    def test_items_has_no_setter(self):
        cfg = _make_async_config()
        with pytest.raises(AttributeError):
            cfg.items = {"host": "localhost"}

    def test_environments_returns_copy(self):
        cfg = _make_async_config()
        cfg.set_number("max_retries", 5, environment="production")
        view = cfg.environments
        del view["production"]
        assert "production" in cfg.environments

    def test_environments_has_no_setter(self):
        cfg = _make_async_config()
        with pytest.raises(AttributeError):
            cfg.environments = {"prod": {}}


# ===================================================================
# AsyncConfig — save()
# ===================================================================


class TestAsyncConfigSave:
    def test_save_creates_when_created_at_is_none(self):
        mock_client = MagicMock()
        created = _make_async_config(id="new-id", name="Created Config")
        mock_client._create_config = AsyncMock(return_value=created)

        cfg = AsyncConfig(mock_client, id="test", name="Test")
        asyncio.run(cfg.save())

        mock_client._create_config.assert_called_once_with(cfg)
        assert cfg.id == "new-id"
        assert cfg.name == "Created Config"

    def test_save_updates_when_created_at_is_set(self):
        import datetime

        mock_client = MagicMock()
        updated = _make_async_config(id="test_config", name="Updated Config")
        mock_client._update_config_from_model = AsyncMock(return_value=updated)

        cfg = AsyncConfig(mock_client, id="test_config", name="Old Name")
        cfg.created_at = datetime.datetime(2025, 1, 1)
        asyncio.run(cfg.save())

        mock_client._update_config_from_model.assert_called_once_with(cfg)
        assert cfg.name == "Updated Config"

    def test_delete_calls_client_delete(self):
        mock_client = MagicMock()
        mock_client.delete = AsyncMock()
        cfg = AsyncConfig(mock_client, id="test_config", name="X")
        asyncio.run(cfg.delete())
        mock_client.delete.assert_called_once_with("test_config")

    def test_delete_without_client_raises(self):
        cfg = AsyncConfig(None, id="x", name="X")

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await cfg.delete()

        asyncio.run(_run())


# ===================================================================
# AsyncConfig — _apply()
# ===================================================================


class TestAsyncConfigApply:
    def test_apply_copies_all_fields(self):
        import datetime

        cfg = _make_async_config(id="old-id", name="Old")
        other = _make_async_config(
            id="new-id",
            name="New",
            description="New desc",
            parent="parent-id",
            items={"host": {"value": "h"}},
            environments={"prod": {"host": "prod-h"}},
        )
        other.created_at = datetime.datetime(2025, 1, 1)
        other.updated_at = datetime.datetime(2025, 6, 1)

        cfg._apply(other)

        assert cfg.id == "new-id"
        assert cfg.name == "New"
        assert cfg.description == "New desc"
        assert cfg.parent == "parent-id"
        assert cfg.items == {"host": "h"}
        assert list(cfg.environments) == ["prod"]
        assert cfg.environments["prod"].values == {"host": "prod-h"}
        assert cfg.created_at == datetime.datetime(2025, 1, 1)
        assert cfg.updated_at == datetime.datetime(2025, 6, 1)

    def test_apply_copies_items_raw(self):
        cfg = _make_async_config()
        other = _make_async_config(items={"x": {"value": 99, "type": "NUMBER"}})
        cfg._apply(other)
        assert cfg._items_raw == {"x": {"value": 99, "type": "NUMBER"}}


# ===================================================================
# AsyncConfig — _build_chain
# ===================================================================


class TestAsyncConfigBuildChain:
    def test_build_chain_with_parent(self):
        parent_cfg = _make_async_config(
            id="parent-1",
            name="Parent",
            parent=None,
            items={"inherited": {"value": "yes"}},
            environments={},
        )
        mock_client = MagicMock()
        mock_client.get = AsyncMock(return_value=parent_cfg)

        child = AsyncConfig(
            mock_client,
            id="child-1",
            name="Child",
            parent="parent-1",
            items={"shared": {"value": "child_val"}},
            environments={},
        )

        async def _run():
            chain = await child._build_chain()
            assert len(chain) == 2
            assert chain[0]["id"] == "child-1"
            assert chain[1]["id"] == "parent-1"

        asyncio.run(_run())
        mock_client.get.assert_called_once_with("parent-1")

    def test_build_chain_with_configs_list(self):
        """When a configs list is provided, parents are looked up by ID without calling get()."""
        parent_cfg = _make_async_config(
            id="parent-1",
            name="Parent",
            parent=None,
            items={"inherited": {"value": "yes"}},
            environments={},
        )
        mock_client = MagicMock()

        child = AsyncConfig(
            mock_client,
            id="child-1",
            name="Child",
            parent="parent-1",
            items={"shared": {"value": "child_val"}},
            environments={},
        )

        async def _run():
            chain = await child._build_chain(configs=[parent_cfg, child])
            assert len(chain) == 2
            assert chain[0]["id"] == "child-1"
            assert chain[1]["id"] == "parent-1"

        asyncio.run(_run())
        mock_client.get.assert_not_called()

    def test_build_chain_no_parent(self):
        cfg = _make_async_config()

        async def _run():
            chain = await cfg._build_chain()
            assert len(chain) == 1
            assert chain[0]["id"] == "test_config"

        asyncio.run(_run())


# ===================================================================
# ConfigItem — typed item helper
# ===================================================================


class TestConfigItem:
    def test_construct_with_enum_type(self):
        item = ConfigItem("host", "localhost", ItemType.STRING)
        assert item.name == "host"
        assert item.value == "localhost"
        assert item.type is ItemType.STRING
        assert item.description is None

    def test_construct_with_string_type(self):
        item = ConfigItem("port", 5432, "NUMBER", description="DB port")
        assert item.type is ItemType.NUMBER
        assert item.description == "DB port"

    def test_repr(self):
        item = ConfigItem("flag", True, ItemType.BOOLEAN)
        r = repr(item)
        assert "ConfigItem(" in r
        assert "flag" in r
        assert "BOOLEAN" in r


class TestConfigSetRemoveItems:
    def test_set_writes_typed_item(self):
        cfg = _make_config()
        cfg.set(ConfigItem("host", "localhost", ItemType.STRING))
        assert cfg.items_raw["host"] == {"value": "localhost", "type": "STRING"}

    def test_set_includes_description(self):
        cfg = _make_config()
        cfg.set(ConfigItem("host", "localhost", ItemType.STRING, description="DB host"))
        assert cfg.items_raw["host"]["description"] == "DB host"

    def test_remove_existing(self):
        cfg = _make_config()
        cfg.set(ConfigItem("host", "localhost", ItemType.STRING))
        cfg.remove("host")
        assert "host" not in cfg.items_raw

    def test_remove_missing_no_error(self):
        cfg = _make_config()
        cfg.remove("never-existed")  # should not raise

    def test_set_string_helper(self):
        cfg = _make_config()
        cfg.set_string("host", "localhost")
        assert cfg.items_raw["host"]["type"] == "STRING"

    def test_set_number_helper(self):
        cfg = _make_config()
        cfg.set_number("port", 5432, description="db")
        assert cfg.items_raw["port"]["type"] == "NUMBER"
        assert cfg.items_raw["port"]["description"] == "db"

    def test_set_boolean_helper(self):
        cfg = _make_config()
        cfg.set_boolean("on", True)
        assert cfg.items_raw["on"]["type"] == "BOOLEAN"

    def test_set_json_helper(self):
        cfg = _make_config()
        cfg.set_json("blob", {"a": 1})
        assert cfg.items_raw["blob"]["type"] == "JSON"


class TestAsyncConfigSetRemoveItems:
    def test_set_writes_typed_item(self):
        cfg = _make_async_config()
        cfg.set(ConfigItem("host", "localhost", ItemType.STRING))
        assert cfg.items_raw["host"] == {"value": "localhost", "type": "STRING"}

    def test_set_includes_description(self):
        cfg = _make_async_config()
        cfg.set(ConfigItem("host", "h", ItemType.STRING, description="hint"))
        assert cfg.items_raw["host"]["description"] == "hint"

    def test_remove_existing(self):
        cfg = _make_async_config()
        cfg.set(ConfigItem("host", "h", ItemType.STRING))
        cfg.remove("host")
        assert "host" not in cfg.items_raw

    def test_remove_missing_no_error(self):
        cfg = _make_async_config()
        cfg.remove("ghost")

    def test_set_string_helper(self):
        cfg = _make_async_config()
        cfg.set_string("host", "h")
        assert cfg.items_raw["host"]["type"] == "STRING"

    def test_set_number_helper(self):
        cfg = _make_async_config()
        cfg.set_number("port", 1)
        assert cfg.items_raw["port"]["type"] == "NUMBER"

    def test_set_boolean_helper(self):
        cfg = _make_async_config()
        cfg.set_boolean("on", False)
        assert cfg.items_raw["on"]["type"] == "BOOLEAN"

    def test_set_json_helper(self):
        cfg = _make_async_config()
        cfg.set_json("blob", [])
        assert cfg.items_raw["blob"]["type"] == "JSON"


class TestConfigEnvironment:
    """Per ADR-024 §2.4 each env entry is a flat ``{key: rawValue}`` map."""

    def test_construct_empty(self):
        env = ConfigEnvironment()
        assert env.values == {}
        assert env.values_raw == {}

    def test_construct_with_flat_values(self):
        env = ConfigEnvironment(values={"host": "h", "port": 5432})
        assert env.values == {"host": "h", "port": 5432}
        assert env.values_raw == {"host": "h", "port": 5432}

    def test_construct_unwraps_legacy_wrapped_value_only(self):
        """Legacy ``{value: ...}`` wrappers are flattened for compat."""
        env = ConfigEnvironment(values={"host": {"value": "h", "type": "STRING"}})
        assert env.values == {"host": "h"}

    def test_construct_preserves_arbitrary_dict_value(self):
        """A dict customer value (e.g. nested JSON) is stored as-is."""
        env = ConfigEnvironment(values={"db": {"host": "h", "port": 5432}})
        assert env.values == {"db": {"host": "h", "port": 5432}}

    def test_values_returns_independent_copy(self):
        env = ConfigEnvironment(values={"host": "h"})
        view = env.values
        view["new"] = "no leak"
        assert "new" not in env.values

    def test_values_raw_returns_independent_copy(self):
        env = ConfigEnvironment(values={"host": "h"})
        view = env.values_raw
        view["new"] = "no leak"
        assert "new" not in env.values_raw

    def test_repr(self):
        env = ConfigEnvironment(values={"host": "h"})
        r = repr(env)
        assert "ConfigEnvironment(" in r
        assert "host" in r


class TestConfigEnvironmentsAccess:
    """Per ADR-024 §2.4 env overrides carry only the raw value, no type/desc."""

    def test_environments_property_starts_empty(self):
        cfg = _make_config()
        assert cfg.environments == {}

    def test_setter_with_environment_kwarg_creates_and_writes(self):
        cfg = _make_config()
        cfg.set_number("max_retries", 5, environment="production")
        assert isinstance(cfg.environments["production"], ConfigEnvironment)
        assert cfg.environments["production"].values == {"max_retries": 5}
        assert cfg.environments["production"].values_raw == {"max_retries": 5}

    def test_setter_with_environment_reuses_existing_env(self):
        cfg = _make_config()
        cfg.set_number("max_retries", 5, environment="production")
        cfg.set_number("request_timeout_ms", 10000, environment="production")
        assert len(cfg.environments) == 1
        prod = cfg.environments["production"]
        assert prod.values == {"max_retries": 5, "request_timeout_ms": 10000}

    def test_set_with_environment_routes_to_override(self):
        cfg = _make_config(items={})
        cfg.set(ConfigItem("host", "prod-h", ItemType.STRING), environment="production")
        assert cfg.items_raw == {}
        assert cfg.environments["production"].values["host"] == "prod-h"

    def test_set_with_environment_ignores_type_and_description(self):
        """Env overrides on the wire are just raw values — type/desc come from the base item."""
        cfg = _make_config(items={})
        cfg.set(
            ConfigItem("host", "prod-h", ItemType.STRING, description="ignored"),
            environment="production",
        )
        assert cfg.environments["production"].values_raw == {"host": "prod-h"}

    def test_remove_with_environment_only_clears_override(self):
        cfg = _make_config()
        cfg.set_number("max_retries", 3)
        cfg.set_number("max_retries", 5, environment="production")
        cfg.remove("max_retries", environment="production")
        assert cfg.items_raw["max_retries"] == {"value": 3, "type": "NUMBER"}
        assert "max_retries" not in cfg.environments["production"].values_raw

    def test_init_converts_flat_wire_dict(self):
        cfg = _make_config(environments={"prod": {"host": "h"}})
        assert isinstance(cfg.environments["prod"], ConfigEnvironment)
        assert cfg.environments["prod"].values == {"host": "h"}

    def test_init_accepts_pre_built_instances(self):
        env = ConfigEnvironment(values={"host": "h"})
        cfg = _make_config(environments={"prod": env})
        assert cfg.environments["prod"] is env

    def test_init_handles_non_dict_values_gracefully(self):
        cfg = _make_config(environments={"prod": "garbage"})
        assert isinstance(cfg.environments["prod"], ConfigEnvironment)
        assert cfg.environments["prod"].values == {}

    def test_async_setter_with_environment_kwarg(self):
        cfg = _make_async_config()
        cfg.set_number("max_retries", 5, environment="production")
        assert cfg.environments["production"].values_raw == {"max_retries": 5}

    def test_async_set_with_environment_routes_to_override(self):
        cfg = _make_async_config(items={})
        cfg.set(ConfigItem("host", "prod-h", ItemType.STRING), environment="production")
        assert cfg.items_raw == {}
        assert cfg.environments["production"].values["host"] == "prod-h"

    def test_async_remove_with_environment_only_clears_override(self):
        cfg = _make_async_config()
        cfg.set_number("max_retries", 5, environment="production")
        cfg.remove("max_retries", environment="production")
        assert "max_retries" not in cfg.environments["production"].values_raw

    def test_async_init_converts_flat_wire_dict(self):
        cfg = _make_async_config(environments={"prod": {"host": "h"}})
        assert isinstance(cfg.environments["prod"], ConfigEnvironment)
        assert cfg.environments["prod"].values == {"host": "h"}
