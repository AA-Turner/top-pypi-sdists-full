"""Tests for the SDK-side discovery pipeline:

- ``_ConfigRegistrationBuffer`` (mgmt buffer)
- ``ConfigClient.bind`` (declarative Pydantic-instance binding)
- Pydantic introspection helpers (instance walk, ``model_fields_set``)
- In-place mutation of bound instances via WebSocket dispatch
- Pre-connect flush hook
"""

from __future__ import annotations

import asyncio
import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from pydantic import BaseModel, Field

from smplkit._errors import NotFoundError
from smplkit._client import AsyncSmplClient, SmplClient
from smplkit.config._client import (
    ConfigChangeEvent,
    _apply_change_to_target,
    _build_config_bulk_request,
    _is_pydantic_model,
    _iter_dict_items,
    _iter_pydantic_items_from_instance,
    _pydantic_field_type,
    _value_to_item_type,
)
from smplkit._buffer import _ConfigRegistrationBuffer


# ===========================================================================
# _ConfigRegistrationBuffer
# ===========================================================================


class TestConfigRegistrationBuffer:
    def test_declare_then_drain(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="svc", environment="prod")
        batch = buf.drain()
        assert len(batch) == 1
        assert batch[0]["id"] == "billing"
        assert batch[0]["items"] == {}
        assert batch[0]["service"] == "svc"
        assert batch[0]["environment"] == "prod"

    def test_declare_includes_optional_metadata(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare(
            "billing",
            service="s",
            environment="e",
            parent="common",
            name="Billing",
            description="Plan limits.",
        )
        entry = buf.drain()[0]
        assert entry["parent"] == "common"
        assert entry["name"] == "Billing"
        assert entry["description"] == "Plan limits."

    def test_declare_omits_none_metadata(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service=None, environment=None)
        entry = buf.drain()[0]
        assert "service" not in entry
        assert "environment" not in entry
        assert "parent" not in entry
        assert "name" not in entry
        assert "description" not in entry

    def test_declare_is_idempotent(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="s1", environment="e1")
        buf.declare("billing", service="s2", environment="e2")  # ignored
        entries = buf.drain()
        assert len(entries) == 1
        assert entries[0]["service"] == "s1"  # first writer wins

    def test_add_item_attaches_to_existing_entry(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="s", environment="e")
        buf.add_item("billing", "max_seats", "NUMBER", 5, "Max seats.")
        entry = buf.drain()[0]
        assert entry["items"] == {
            "max_seats": {
                "value": 5,
                "type": "NUMBER",
                "description": "Max seats.",
            }
        }

    def test_add_item_without_description_omits_field(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="s", environment="e")
        buf.add_item("billing", "k", "STRING", "foo")
        entry = buf.drain()[0]
        assert entry["items"]["k"] == {"value": "foo", "type": "STRING"}

    def test_add_item_without_declare_is_dropped(self):
        buf = _ConfigRegistrationBuffer()
        buf.add_item("unknown", "k", "NUMBER", 1)
        assert buf.drain() == []

    def test_add_item_dedups_within_session(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="s", environment="e")
        buf.add_item("billing", "max_seats", "NUMBER", 5)
        buf.add_item("billing", "max_seats", "NUMBER", 99)  # ignored — already pending
        entry = buf.drain()[0]
        assert entry["items"]["max_seats"]["value"] == 5

    def test_add_item_dedups_across_drains(self):
        """After a successful flush (drain), the same item must not re-send."""
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="s", environment="e")
        buf.add_item("billing", "max_seats", "NUMBER", 5)
        first = buf.drain()
        assert first[0]["items"]
        buf.add_item("billing", "max_seats", "NUMBER", 5)  # already sent
        assert buf.drain() == []

    def test_delta_after_drain_includes_metadata(self):
        """A new item declared after drain creates a fresh pending entry."""
        buf = _ConfigRegistrationBuffer()
        buf.declare(
            "billing",
            service="svc",
            environment="prod",
            parent="common",
        )
        buf.add_item("billing", "k1", "NUMBER", 1)
        buf.drain()

        buf.add_item("billing", "k2", "NUMBER", 2)
        delta = buf.drain()
        assert len(delta) == 1
        assert delta[0]["service"] == "svc"
        assert delta[0]["environment"] == "prod"
        assert delta[0]["parent"] == "common"
        assert delta[0]["items"] == {"k2": {"value": 2, "type": "NUMBER"}}

    def test_drain_clears_pending(self):
        buf = _ConfigRegistrationBuffer()
        buf.declare("billing", service="s", environment="e")
        assert buf.drain() != []
        assert buf.drain() == []

    def test_pending_count(self):
        buf = _ConfigRegistrationBuffer()
        assert buf.pending_count == 0
        buf.declare("billing", service="s", environment="e")
        assert buf.pending_count == 1
        buf.declare("user-service", service="s", environment="e")
        assert buf.pending_count == 2
        buf.drain()
        assert buf.pending_count == 0


# ===========================================================================
# _build_config_bulk_request helper
# ===========================================================================


class TestBuildConfigBulkRequest:
    def test_empty_returns_none(self):
        assert _build_config_bulk_request([]) is None

    def test_translates_entry(self):
        body = _build_config_bulk_request(
            [
                {
                    "id": "billing",
                    "items": {
                        "max_seats": {"value": 5, "type": "NUMBER", "description": "Max."},
                    },
                    "service": "svc",
                    "environment": "prod",
                    "parent": "common",
                    "name": "Billing",
                    "description": "Plan limits.",
                }
            ]
        )
        assert body is not None
        assert len(body.configs) == 1
        item = body.configs[0]
        assert item.id == "billing"
        assert item.name == "Billing"
        assert item.parent == "common"
        assert "max_seats" in item.items.additional_properties

    def test_omits_unset_fields(self):
        body = _build_config_bulk_request([{"id": "minimal", "items": {}}])
        item = body.configs[0]
        # No items, no metadata — generator UNSET sentinels remain.
        assert item.id == "minimal"

    def test_translates_multiple_entries(self):
        body = _build_config_bulk_request(
            [
                {"id": "a", "items": {}},
                {"id": "b", "items": {}},
            ]
        )
        assert [c.id for c in body.configs] == ["a", "b"]


# ===========================================================================
# Pydantic introspection helpers
# ===========================================================================


class TestPydanticHelpers:
    def test_field_type_mapping(self):
        assert _pydantic_field_type(bool) == "BOOLEAN"
        assert _pydantic_field_type(int) == "NUMBER"
        assert _pydantic_field_type(float) == "NUMBER"
        assert _pydantic_field_type(str) == "STRING"
        # Anything else → STRING (universal fallback; admin can retype).
        assert _pydantic_field_type(dict) == "STRING"
        assert _pydantic_field_type(list) == "STRING"
        assert _pydantic_field_type(object) == "STRING"

    def test_is_pydantic_model_negative(self):
        assert not _is_pydantic_model(int)
        assert not _is_pydantic_model("not a class")
        assert not _is_pydantic_model(None)

    def test_iter_instance_uses_instance_values_not_class_defaults(self):
        class Billing(BaseModel):
            max_seats: int = 5
            tier: str = "free"

        # Construct with overrides → instance values land in the payload.
        instance = Billing(max_seats=50, tier="pro")
        items = _iter_pydantic_items_from_instance(instance, explicit_only=False)
        by_key = {k: (t, v, d) for (k, t, v, d) in items}
        assert by_key["max_seats"] == ("NUMBER", 50, None)
        assert by_key["tier"] == ("STRING", "pro", None)

    def test_iter_instance_propagates_field_description(self):
        class Billing(BaseModel):
            trial_days: int = Field(default=14, description="Trial.")
            max_seats: int = 5

        items = _iter_pydantic_items_from_instance(Billing(), explicit_only=False)
        by_key = {k: d for (k, _t, _v, d) in items}
        assert by_key["trial_days"] == "Trial."
        assert by_key["max_seats"] is None

    def test_iter_instance_flattens_nested_models(self):
        class Database(BaseModel):
            host: str = "localhost"
            port: int = 5432

        class App(BaseModel):
            database: Database = Database()
            debug: bool = False

        items = _iter_pydantic_items_from_instance(App(), explicit_only=False)
        keys = [k for (k, _, _, _) in items]
        assert "database.host" in keys
        assert "database.port" in keys
        assert "debug" in keys

    def test_iter_instance_returns_empty_for_non_pydantic(self):
        class Plain:
            pass

        # ``_iter_pydantic_items_from_instance`` defends against non-model
        # inputs by checking ``_is_pydantic_model(type(instance))``.
        assert _iter_pydantic_items_from_instance(Plain(), explicit_only=False) == []  # type: ignore[arg-type]

    def test_explicit_only_skips_unset_top_level_fields(self):
        class Plan(BaseModel):
            name: str = "Free"
            price: float = 0.0
            seats: int = 5

        # Only ``name`` and ``seats`` were passed; ``price`` took the default.
        instance = Plan(name="Pro", seats=50)
        keys = [k for (k, _, _, _) in _iter_pydantic_items_from_instance(instance, explicit_only=True)]
        assert "name" in keys
        assert "seats" in keys
        assert "price" not in keys

    def test_explicit_only_recurses_into_nested_model_fields_set(self):
        class Audit(BaseModel):
            streams: int = 0
            siem: bool = False

        class Plan(BaseModel):
            name: str = "Base"
            audit: Audit = Audit()

        # Top-level ``audit`` is explicitly set (it's in the constructor),
        # but inside, only ``streams`` is explicit — ``siem`` took its
        # class default and must be skipped so it can inherit.
        instance = Plan(audit=Audit(streams=10))
        keys = [k for (k, _, _, _) in _iter_pydantic_items_from_instance(instance, explicit_only=True)]
        assert "audit.streams" in keys
        assert "audit.siem" not in keys
        # ``name`` wasn't passed at the top level either.
        assert "name" not in keys

    def test_explicit_only_skips_everything_when_nothing_was_passed(self):
        class Plan(BaseModel):
            name: str = "Free"
            seats: int = 5

        # Empty constructor → no fields explicitly set → every field
        # inherits from the parent.
        instance = Plan()
        assert _iter_pydantic_items_from_instance(instance, explicit_only=True) == []

    def test_required_field_must_be_explicit_in_every_instance(self):
        class Plan(BaseModel):
            name: str  # required, no default
            seats: int = 5

        # Pydantic forces the caller to pass ``name``; ``model_fields_set``
        # therefore always includes it. This is the documented rule:
        # commonly-inheritable fields need class defaults.
        instance = Plan(name="Pro")
        keys = [k for (k, _, _, _) in _iter_pydantic_items_from_instance(instance, explicit_only=True)]
        assert keys == ["name"]


# ===========================================================================
# _value_to_item_type
# ===========================================================================


class TestValueToItemType:
    def test_bool(self):
        assert _value_to_item_type(True) == "BOOLEAN"
        assert _value_to_item_type(False) == "BOOLEAN"

    def test_int(self):
        assert _value_to_item_type(5) == "NUMBER"

    def test_float(self):
        assert _value_to_item_type(0.5) == "NUMBER"

    def test_str(self):
        assert _value_to_item_type("hello") == "STRING"

    def test_other_falls_back_to_string(self):
        assert _value_to_item_type([1, 2, 3]) == "STRING"
        assert _value_to_item_type({"k": "v"}) == "STRING"
        assert _value_to_item_type(None) == "STRING"


# ===========================================================================
# _iter_dict_items
# ===========================================================================


class TestIterDictItems:
    def test_flat_dict(self):
        items = _iter_dict_items({"max_seats": 5, "tier": "free", "enabled": True})
        by_key = {k: (t, v, d) for (k, t, v, d) in items}
        assert by_key["max_seats"] == ("NUMBER", 5, None)
        assert by_key["tier"] == ("STRING", "free", None)
        assert by_key["enabled"] == ("BOOLEAN", True, None)

    def test_nested_dict_flattens(self):
        items = _iter_dict_items(
            {
                "connection": {"host": "localhost", "port": 5432},
                "timeout": 30,
            }
        )
        keys = [k for (k, _, _, _) in items]
        assert "connection.host" in keys
        assert "connection.port" in keys
        assert "timeout" in keys

    def test_deeply_nested_dict(self):
        items = _iter_dict_items({"a": {"b": {"c": 1}}})
        keys = [k for (k, _, _, _) in items]
        assert keys == ["a.b.c"]
        assert items[0] == ("a.b.c", "NUMBER", 1, None)

    def test_empty_dict(self):
        assert _iter_dict_items({}) == []

    def test_non_string_keys_are_stringified(self):
        items = _iter_dict_items({1: "first", 2: "second"})
        keys = sorted(k for (k, _, _, _) in items)
        assert keys == ["1", "2"]


# ===========================================================================
# _apply_change_to_target
# ===========================================================================


class TestApplyChangeToTargetPydantic:
    def test_applies_top_level_field(self):
        class Plan(BaseModel):
            seats: int = 5

        instance = Plan()
        _apply_change_to_target(instance, "seats", 50)
        assert instance.seats == 50

    def test_applies_nested_field(self):
        class Audit(BaseModel):
            streams: int = 0

        class Plan(BaseModel):
            audit: Audit = Audit()

        instance = Plan()
        _apply_change_to_target(instance, "audit.streams", 99)
        assert instance.audit.streams == 99

    def test_mutates_in_place_so_held_nested_reference_sees_update(self):
        """Local references to nested submodels stay live."""

        class Audit(BaseModel):
            streams: int = 0

        class Plan(BaseModel):
            audit: Audit = Audit()

        instance = Plan()
        audit_ref = instance.audit
        _apply_change_to_target(instance, "audit.streams", 99)
        assert audit_ref.streams == 99

    def test_bypasses_frozen_models(self):
        """object.__setattr__ writes through the freeze."""
        from pydantic import ConfigDict

        class Plan(BaseModel):
            model_config = ConfigDict(frozen=True)
            seats: int = 5

        instance = Plan()
        _apply_change_to_target(instance, "seats", 100)
        assert instance.seats == 100

    def test_unknown_intermediate_is_swallowed(self):
        class Plan(BaseModel):
            seats: int = 5

        instance = Plan()
        _apply_change_to_target(instance, "missing.path.deep", 1)
        assert instance.seats == 5

    def test_non_pydantic_intermediate_is_swallowed(self):
        """If the walk lands on a non-BaseModel intermediate, do nothing."""

        class Plan(BaseModel):
            note: str = "x"

        instance = Plan()
        # ``note.length`` walks into a str, which isn't a BaseModel/dict.
        _apply_change_to_target(instance, "note.length", 42)
        assert instance.note == "x"


class TestApplyChangeToTargetDict:
    def test_applies_top_level_key(self):
        target = {"seats": 5}
        _apply_change_to_target(target, "seats", 50)
        assert target["seats"] == 50

    def test_creates_new_top_level_key(self):
        target = {"seats": 5}
        _apply_change_to_target(target, "new_key", "added")
        assert target["new_key"] == "added"

    def test_applies_nested_key(self):
        target = {"connection": {"host": "localhost", "port": 5432}}
        _apply_change_to_target(target, "connection.host", "remote")
        assert target["connection"]["host"] == "remote"

    def test_mutates_in_place_held_nested_reference_sees_update(self):
        target = {"connection": {"host": "localhost"}}
        conn_ref = target["connection"]
        _apply_change_to_target(target, "connection.host", "remote")
        assert conn_ref["host"] == "remote"

    def test_unknown_intermediate_is_swallowed(self):
        target = {"a": 1}
        _apply_change_to_target(target, "missing.path.deep", 1)
        assert target == {"a": 1}

    def test_non_dict_intermediate_is_swallowed(self):
        target = {"note": "x"}
        # walks into a str via dict path, not a dict/BaseModel
        _apply_change_to_target(target, "note.length", 42)
        assert target == {"note": "x"}

    def test_non_dict_non_basemodel_intermediate_during_walk(self):
        """Walk halts when an intermediate node is neither dict nor BaseModel."""
        target = {"a": "scalar"}
        # parts = ["a", "b", "c"] — after stepping into "a" we get "scalar",
        # which falls through the else-branch in the walk loop.
        _apply_change_to_target(target, "a.b.c", "value")
        assert target == {"a": "scalar"}

    def test_non_basemodel_non_dict_target_is_no_op(self):
        # Should not raise.
        _apply_change_to_target("not a target", "k", 1)  # type: ignore[arg-type]


# ===========================================================================
# ConfigClient.bind (sync)
# ===========================================================================


def _new_sync_client() -> SmplClient:
    return SmplClient(api_key="sk_test", environment="prod", service="svc")


class _Billing(BaseModel):
    """Billing plan."""

    max_seats: int = 5
    tier: str = "free"


class _Plan(BaseModel):
    """A plan."""

    name: str = "Free"
    price: float = 0.0


class TestBindSync:
    def test_bind_returns_the_same_instance(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        instance = _Billing(max_seats=10, tier="pro")
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    result = client.config.bind("billing", instance)
        assert result is instance

    def test_bind_is_idempotent_returns_original_instance(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        first = _Billing(max_seats=10)
        second = _Billing(max_seats=999)
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    a = client.config.bind("billing", first)
                    b = client.config.bind("billing", second)
        assert a is first
        assert b is first  # second instance is silently discarded

    def test_bind_rejects_non_basemodel_non_dict(self):
        client = _new_sync_client()
        client.config._connected = True
        with pytest.raises(TypeError, match="BaseModel instance or dict"):
            client.config.bind("billing", "just a string")  # type: ignore[arg-type]

    def test_bind_registers_class_name_and_docstring(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        with patch.object(client.config, "register_config") as register:
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("billing", _Billing(max_seats=10))
        register.assert_called_once_with(
            "billing",
            service="svc",
            environment="prod",
            parent=None,
            name="_Billing",
            description="Billing plan.",
        )

    def test_bind_omits_description_when_class_has_no_docstring(self):
        class NoDoc(BaseModel):
            x: int = 1

        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"nodoc": {}}
        with patch.object(client.config, "register_config") as register:
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("nodoc", NoDoc())
        assert register.call_args.kwargs["description"] is None

    def test_bind_without_parent_registers_every_field(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item") as reg_item:
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("billing", _Billing(max_seats=10))
        keys = [c.args[1] for c in reg_item.call_args_list]
        assert "max_seats" in keys
        assert "tier" in keys  # took the class default — still registered

    def test_bind_with_parent_only_registers_explicit_overrides(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "pro": {}}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item") as reg_item:
                with patch.object(client.config, "_ensure_connected"):
                    base = client.config.bind("base", _Billing(max_seats=0, tier="base"))
                    reg_item.reset_mock()
                    # Only ``max_seats`` is passed; ``tier`` should inherit from base.
                    client.config.bind("pro", _Billing(max_seats=50), parent=base)
        keys = [c.args[1] for c in reg_item.call_args_list]
        assert keys == ["max_seats"]
        assert reg_item.call_args.args == ("pro", "max_seats", "NUMBER", 50, None)

    def test_bind_with_parent_resolves_parent_id_from_instance(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "pro": {}}
        with patch.object(client.config, "register_config") as register:
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    base = client.config.bind("base", _Billing())
                    register.reset_mock()
                    client.config.bind("pro", _Billing(max_seats=99), parent=base)
        register.assert_called_once()
        assert register.call_args.kwargs["parent"] == "base"

    def test_bind_rejects_unbound_parent(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {}
        stray = _Billing()  # not bound
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    with pytest.raises(ValueError, match="previously returned from client.config.bind"):
                        client.config.bind("pro", _Billing(), parent=stray)

    def test_bind_syncs_instance_from_cache(self):
        """Pre-existing server values override the in-code defaults."""
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {"max_seats": 999, "tier": "enterprise"}}
        instance = _Billing(max_seats=5)  # in-code default
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    result = client.config.bind("billing", instance)
        assert result.max_seats == 999  # from cache, not from in-code value
        assert result.tier == "enterprise"

    def test_bind_records_binding_in_registry(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        instance = _Billing()
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("billing", instance)
        assert client.config._bindings["billing"] is instance


# ===========================================================================
# ConfigClient.bind — dict form
# ===========================================================================


class TestBindDictSync:
    def test_bind_returns_the_same_dict(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        payload = {"connection_string": "postgres://localhost", "timeout": 30}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    result = client.config.bind("db", payload)
        assert result is payload

    def test_bind_rejects_non_basemodel_non_dict(self):
        client = _new_sync_client()
        client.config._connected = True
        with pytest.raises(TypeError, match="BaseModel instance or dict"):
            client.config.bind("billing", ["not", "a", "dict"])  # type: ignore[arg-type]

    def test_bind_dict_does_not_set_name_or_description(self):
        """Dicts carry no class metadata — the SDK omits both fields."""
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        with patch.object(client.config, "register_config") as register:
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("db", {"k": "v"})
        register.assert_called_once_with(
            "db",
            service="svc",
            environment="prod",
            parent=None,
            name=None,
            description=None,
        )

    def test_bind_dict_registers_every_key(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item") as reg_item:
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("db", {"connection_string": "x", "timeout": 30, "tls": True})
        registered = {c.args[1]: (c.args[2], c.args[3]) for c in reg_item.call_args_list}
        assert registered["connection_string"] == ("STRING", "x")
        assert registered["timeout"] == ("NUMBER", 30)
        assert registered["tls"] == ("BOOLEAN", True)

    def test_bind_dict_flattens_nested_keys(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item") as reg_item:
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("db", {"connection": {"host": "h", "port": 5432}})
        keys = [c.args[1] for c in reg_item.call_args_list]
        assert "connection.host" in keys
        assert "connection.port" in keys

    def test_bind_dict_with_dict_parent_resolves_parent_id(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "child": {}}
        with patch.object(client.config, "register_config") as register:
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    base = client.config.bind("base", {"k": "v"})
                    register.reset_mock()
                    client.config.bind("child", {"other": "x"}, parent=base)
        register.assert_called_once()
        assert register.call_args.kwargs["parent"] == "base"

    def test_bind_dict_with_pydantic_parent(self):
        """Cross-type parent chaining: dict child, Pydantic parent."""
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "child": {}}
        with patch.object(client.config, "register_config") as register:
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    base = client.config.bind("base", _Billing(max_seats=5))
                    register.reset_mock()
                    client.config.bind("child", {"override_key": 1}, parent=base)
        assert register.call_args.kwargs["parent"] == "base"

    def test_bind_dict_is_idempotent(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        first = {"k": "v1"}
        second = {"k": "v2"}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    a = client.config.bind("db", first)
                    b = client.config.bind("db", second)
        assert a is first
        assert b is first

    def test_bind_dict_syncs_from_cache(self):
        """Pre-existing server values land on the bound dict in place."""
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"connection_string": "remote", "timeout": 99}}
        payload = {"connection_string": "local", "timeout": 30}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    result = client.config.bind("db", payload)
        assert result["connection_string"] == "remote"
        assert result["timeout"] == 99


# ===========================================================================
# ConfigClient.get — full config + single value
# ===========================================================================


class TestSubscribeValueReadSync:
    """Value reads now happen through the ``subscribe(id)`` proxy.

    The old client-level ``get(id, key)`` / ``get(id, key, default=X)``
    value-read forms were dropped when ``get`` became the management
    resource-fetch; ``subscribe`` registers the config declaration and
    returns a live proxy whose ``[]`` / ``.get(key, default)`` cover the
    same read paths.
    """

    def test_proxy_value_read(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"connection_string": "postgres://x"}}
        proxy = client.config.subscribe("db")
        assert proxy["connection_string"] == "postgres://x"

    def test_proxy_missing_key_raises_key_error(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        proxy = client.config.subscribe("db")
        with pytest.raises(KeyError, match="connection_string"):
            proxy["connection_string"]

    def test_proxy_get_with_default_returns_value_when_present(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"connection_string": "real"}}
        proxy = client.config.subscribe("db")
        assert proxy.get("connection_string", "fallback") == "real"

    def test_proxy_get_with_default_returns_default_when_key_missing(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        proxy = client.config.subscribe("db")
        assert proxy.get("missing", "fallback") == "fallback"

    def test_subscribe_registers_config(self):
        """subscribe() registers the config declaration for observability."""
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"k": "v"}}
        with patch.object(client.config, "register_config") as register:
            client.config.subscribe("db")
        register.assert_called_once_with(
            "db",
            service="svc",
            environment="prod",
            parent=None,
            name=None,
            description=None,
        )


# ===========================================================================
# get_value() — ad-hoc resolved single-value read
# ===========================================================================


class TestGetValueSync:
    def _connected_client(self, cache):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = cache
        return client

    def test_no_default_returns_resolved_value(self):
        client = self._connected_client({"db": {"host": "localhost"}})
        assert client.config.get_value("db", "host") == "localhost"

    def test_no_default_missing_config_raises_not_found(self):
        client = self._connected_client({})
        with pytest.raises(NotFoundError, match="Config with id 'db' not found"):
            client.config.get_value("db", "host")

    def test_no_default_missing_key_raises_key_error(self):
        client = self._connected_client({"db": {}})
        with pytest.raises(KeyError, match="connection_string"):
            client.config.get_value("db", "connection_string")

    def test_default_returns_value_when_present(self):
        client = self._connected_client({"db": {"host": "real"}})
        assert client.config.get_value("db", "host", "fallback") == "real"

    def test_default_returns_fallback_when_config_missing(self):
        client = self._connected_client({})
        assert client.config.get_value("db", "host", "fallback") == "fallback"

    def test_default_returns_fallback_when_key_missing(self):
        client = self._connected_client({"db": {}})
        assert client.config.get_value("db", "host", "fallback") == "fallback"

    def test_default_registers_config_and_item(self):
        client = self._connected_client({})
        with patch.object(client.config, "register_config") as reg_cfg:
            with patch.object(client.config, "register_config_item") as reg_item:
                client.config.get_value("max-seats-cfg", "max_seats", 42)
        reg_cfg.assert_called_once()
        assert reg_cfg.call_args.args[0] == "max-seats-cfg"
        reg_item.assert_called_once()
        # (config_id, item_key, inferred_type, default, description)
        assert reg_item.call_args.args == ("max-seats-cfg", "max_seats", "NUMBER", 42, None)

    def test_no_default_does_not_register(self):
        client = self._connected_client({"db": {"host": "h"}})
        with patch.object(client.config, "register_config") as reg_cfg:
            with patch.object(client.config, "register_config_item") as reg_item:
                client.config.get_value("db", "host")
        reg_cfg.assert_not_called()
        reg_item.assert_not_called()

    def test_resolves_inherited_value(self):
        # Cache holds the resolved chain, so inheritance is already folded in.
        client = self._connected_client({"pro": {"max_seats": 5, "tier": "base"}})
        assert client.config.get_value("pro", "tier") == "base"

    def test_lazy_connects_on_first_use(self):
        client = _new_sync_client()
        mock_cfg = MagicMock()
        mock_cfg.id = "db"
        mock_cfg._items_raw = {"host": {"value": "localhost"}}
        mock_cfg.environments = {}
        mock_cfg._build_chain.return_value = [
            {"id": "db", "items": {"host": {"value": "localhost"}}, "environments": {}}
        ]
        with patch.object(client.config, "_fetch_all_configs", return_value=[mock_cfg]):
            assert client.config.get_value("db", "host") == "localhost"
        assert client.config._connected is True


class TestGetValueAsync:
    def _connected_client(self, cache):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = cache
        return client

    def test_no_default_returns_resolved_value(self):
        async def _run():
            client = self._connected_client({"db": {"host": "localhost"}})
            assert await client.config.get_value("db", "host") == "localhost"

        asyncio.run(_run())

    def test_no_default_missing_config_raises_not_found(self):
        async def _run():
            client = self._connected_client({})
            with pytest.raises(NotFoundError, match="Config with id 'db' not found"):
                await client.config.get_value("db", "host")

        asyncio.run(_run())

    def test_no_default_missing_key_raises_key_error(self):
        async def _run():
            client = self._connected_client({"db": {}})
            with pytest.raises(KeyError, match="connection_string"):
                await client.config.get_value("db", "connection_string")

        asyncio.run(_run())

    def test_default_returns_fallback_when_config_missing(self):
        async def _run():
            client = self._connected_client({})
            assert await client.config.get_value("db", "host", "fallback") == "fallback"

        asyncio.run(_run())

    def test_default_returns_fallback_when_key_missing(self):
        async def _run():
            client = self._connected_client({"db": {}})
            assert await client.config.get_value("db", "host", "fallback") == "fallback"

        asyncio.run(_run())

    def test_default_registers_config_and_item(self):
        async def _run():
            client = self._connected_client({})
            with patch.object(client.config, "register_config") as reg_cfg:
                with patch.object(client.config, "register_config_item") as reg_item:
                    await client.config.get_value("max-seats-cfg", "max_seats", 42)
            reg_cfg.assert_called_once()
            assert reg_item.call_args.args == ("max-seats-cfg", "max_seats", "NUMBER", 42, None)

        asyncio.run(_run())


# ===========================================================================
# bind() seeds the local cache so reads work immediately (no flush/refresh)
# ===========================================================================


class TestBindSeedsCacheSync:
    def _connected_client(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {}  # nothing fetched server-side
        return client

    def test_subscribe_works_immediately_after_bind(self):
        client = self._connected_client()
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                client.config.bind("billing", _Billing(max_seats=10, tier="pro"))
        # No flush/refresh — subscribe reads the seeded cache.
        proxy = client.config.subscribe("billing")
        assert proxy["max_seats"] == 10
        assert proxy["tier"] == "pro"

    def test_get_value_works_immediately_after_bind(self):
        client = self._connected_client()
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                client.config.bind("billing", _Billing(max_seats=10))
        assert client.config.get_value("billing", "max_seats") == 10

    def test_dict_bind_seeds_cache(self):
        client = self._connected_client()
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                client.config.bind("db", {"timeout": 30, "host": "local"})
        assert client.config.get_value("db", "timeout") == 30
        assert client.config.subscribe("db")["host"] == "local"

    def test_existing_server_config_not_overwritten_by_seed(self):
        # id already in cache → server values authoritative (sync, not seed).
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {"max_seats": 999}}
        instance = _Billing(max_seats=10)
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                client.config.bind("billing", instance)
        assert client.config.get_value("billing", "max_seats") == 999
        assert instance.max_seats == 999  # synced from server

    def test_seed_resolves_through_bound_parent_chain(self):
        client = self._connected_client()
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                base = client.config.bind("base", _Billing(max_seats=1, tier="base"))
                # Pro overrides only max_seats; tier inherits from base.
                client.config.bind("pro", _Billing(max_seats=50), parent=base)
        # tier resolves from the bound parent (base), max_seats from the child.
        assert client.config.get_value("pro", "max_seats") == 50
        assert client.config.get_value("pro", "tier") == "base"

    def test_merge_pending_seeds_survives_cache_rebuild(self):
        # A bound-but-unflushed config must survive a cache rebuild (e.g. a
        # WebSocket event for another config) that omits it.
        client = self._connected_client()
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                client.config.bind("billing", _Billing(max_seats=10))
        rebuilt: dict = {}
        client.config._merge_pending_seeds(rebuilt)  # true branch: re-seeds
        assert rebuilt["billing"]["max_seats"] == 10
        rebuilt = {"billing": {"max_seats": 999}}
        client.config._merge_pending_seeds(rebuilt)  # false branch: left as-is
        assert rebuilt["billing"]["max_seats"] == 999


class TestBindSeedsCacheAsync:
    def test_subscribe_and_get_value_work_immediately_after_bind(self):
        async def _run():
            client = _new_async_client()
            client.config._connected = True
            client.config._config_cache = {}
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    await client.config.bind("billing", _Billing(max_seats=7, tier="team"))
            assert client.config.subscribe("billing")["max_seats"] == 7
            assert await client.config.get_value("billing", "tier") == "team"

        asyncio.run(_run())

    def test_seed_resolves_through_bound_parent_chain(self):
        async def _run():
            client = _new_async_client()
            client.config._connected = True
            client.config._config_cache = {}
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    base = await client.config.bind("base", _Billing(max_seats=1, tier="base"))
                    await client.config.bind("pro", _Billing(max_seats=50), parent=base)
            assert await client.config.get_value("pro", "max_seats") == 50
            assert await client.config.get_value("pro", "tier") == "base"

        asyncio.run(_run())

    def test_merge_pending_seeds_survives_cache_rebuild(self):
        async def _run():
            client = _new_async_client()
            client.config._connected = True
            client.config._config_cache = {}
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    await client.config.bind("billing", _Billing(max_seats=10))
            rebuilt: dict = {}
            client.config._merge_pending_seeds(rebuilt)  # true branch: re-seeds
            assert rebuilt["billing"]["max_seats"] == 10
            rebuilt = {"billing": {"max_seats": 999}}
            client.config._merge_pending_seeds(rebuilt)  # false branch: left as-is
            assert rebuilt["billing"]["max_seats"] == 999

        asyncio.run(_run())


# ===========================================================================
# In-place mutation via change-listener pipeline
# ===========================================================================


class TestBoundInstanceMutation:
    def test_fire_change_listeners_mutates_bound_instance(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {"max_seats": 5}}
        instance = _Billing(max_seats=5)
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("billing", instance)
        # Simulate a server-side value bump.
        old_cache = {"billing": {"max_seats": 5}}
        new_cache = {"billing": {"max_seats": 50}}
        client.config._fire_change_listeners(old_cache, new_cache, source="websocket")
        assert instance.max_seats == 50

    def test_fire_change_listeners_fires_user_callback_after_mutation(self):
        """Listeners see the new value when they re-read the bound instance."""
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {"max_seats": 5}}
        instance = _Billing(max_seats=5)
        observed: list[int] = []
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("billing", instance)

        @client.config.on_change("billing", item_key="max_seats")
        def _capture(_event: ConfigChangeEvent) -> None:
            observed.append(instance.max_seats)

        old_cache = {"billing": {"max_seats": 5}}
        new_cache = {"billing": {"max_seats": 50}}
        client.config._fire_change_listeners(old_cache, new_cache, source="websocket")
        assert observed == [50]


class TestBoundDictMutation:
    """WebSocket dispatch path for dict-bound configs."""

    def test_fire_change_listeners_mutates_bound_dict(self):
        client = _new_sync_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"timeout": 30}}
        payload = {"timeout": 30}
        with patch.object(client.config, "register_config"):
            with patch.object(client.config, "register_config_item"):
                with patch.object(client.config, "_ensure_connected"):
                    client.config.bind("db", payload)
        old_cache = {"db": {"timeout": 30}}
        new_cache = {"db": {"timeout": 120}}
        client.config._fire_change_listeners(old_cache, new_cache, source="websocket")
        assert payload["timeout"] == 120


# ===========================================================================
# Pre-start flush hook
# ===========================================================================


class TestPreConnectFlush:
    def test_sync_connect_flushes_buffer_before_fetch(self):
        client = _new_sync_client()
        with patch.object(client.config, "flush") as flush:
            with patch.object(client.config, "_do_refresh"):
                with patch.object(client.config, "_parent") as parent:
                    parent._ensure_ws.return_value = MagicMock()
                    client.config._ensure_connected()
        assert flush.called

    def test_sync_connect_swallows_flush_errors(self, caplog):
        client = _new_sync_client()
        with patch.object(client.config, "flush", side_effect=RuntimeError("boom")):
            with patch.object(client.config, "_do_refresh"):
                with patch.object(client.config, "_parent") as parent:
                    parent._ensure_ws.return_value = MagicMock()
                    with caplog.at_level(logging.WARNING, logger="smplkit"):
                        client.config._ensure_connected()
        assert any("Config discovery flush before connect" in r.message for r in caplog.records)


# ===========================================================================
# Async equivalents
# ===========================================================================


def _new_async_client() -> AsyncSmplClient:
    return AsyncSmplClient(api_key="sk_test", environment="prod", service="svc")


class TestBindAsync:
    def test_bind_returns_the_same_instance(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        instance = _Billing(max_seats=10)

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        return await client.config.bind("billing", instance)

        result = asyncio.run(_run())
        assert result is instance

    def test_bind_is_idempotent(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {}}
        first = _Billing(max_seats=10)
        second = _Billing(max_seats=999)

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        a = await client.config.bind("billing", first)
                        b = await client.config.bind("billing", second)
                        return a, b

        a, b = asyncio.run(_run())
        assert a is first and b is first

    def test_bind_rejects_non_basemodel_non_dict(self):
        client = _new_async_client()
        client.config._connected = True

        async def _run():
            with pytest.raises(TypeError, match="BaseModel instance or dict"):
                await client.config.bind("billing", 42)  # type: ignore[arg-type]

        asyncio.run(_run())

    def test_bind_with_parent_resolves_parent_id(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "pro": {}}

        async def _run():
            with patch.object(client.config, "register_config") as register:
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        base = await client.config.bind("base", _Billing())
                        register.reset_mock()
                        await client.config.bind("pro", _Billing(max_seats=50), parent=base)
            return register

        register = asyncio.run(_run())
        register.assert_called_once()
        assert register.call_args.kwargs["parent"] == "base"

    def test_bind_with_parent_skips_unset_fields(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "pro": {}}

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item") as reg_item:
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        base = await client.config.bind("base", _Billing(max_seats=0, tier="base"))
                        reg_item.reset_mock()
                        await client.config.bind("pro", _Billing(max_seats=50), parent=base)
            return reg_item

        reg_item = asyncio.run(_run())
        keys = [c.args[1] for c in reg_item.call_args_list]
        assert keys == ["max_seats"]

    def test_bind_rejects_unbound_parent(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {}
        stray = _Billing()

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        with pytest.raises(ValueError, match="previously returned from client.config.bind"):
                            await client.config.bind("pro", _Billing(), parent=stray)

        asyncio.run(_run())

    def test_bind_syncs_instance_from_cache(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {"max_seats": 999, "tier": "enterprise"}}
        instance = _Billing(max_seats=5)

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        return await client.config.bind("billing", instance)

        result = asyncio.run(_run())
        assert result.max_seats == 999
        assert result.tier == "enterprise"

    def test_fire_change_listeners_mutates_bound_instance(self):
        """The async client's listener path also applies updates to bound instances."""
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"billing": {"max_seats": 5}}
        instance = _Billing(max_seats=5)

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        await client.config.bind("billing", instance)

        asyncio.run(_run())
        old_cache = {"billing": {"max_seats": 5}}
        new_cache = {"billing": {"max_seats": 50}}
        client.config._fire_change_listeners(old_cache, new_cache, source="websocket")
        assert instance.max_seats == 50

    def test_subscribe_raises_not_found(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {}

        with pytest.raises(NotFoundError):
            client.config.subscribe("missing")

    def test_async_connect_flushes_buffer_before_fetch(self):
        client = _new_async_client()

        async def _run():
            async def noop_flush():
                return None

            with patch.object(client.config, "flush", side_effect=noop_flush) as flush:
                with patch.object(client.config, "_do_refresh") as refresh:

                    async def noop_refresh(source):
                        return None

                    refresh.side_effect = noop_refresh
                    with patch.object(client.config, "_parent") as parent:
                        parent._ensure_ws.return_value = MagicMock()
                        await client.config._ensure_connected()
            assert flush.called

        asyncio.run(_run())

    def test_async_connect_swallows_flush_errors(self, caplog):
        client = _new_async_client()

        async def _run():
            async def boom_flush():
                raise RuntimeError("boom")

            with patch.object(client.config, "flush", side_effect=boom_flush):
                with patch.object(client.config, "_do_refresh") as refresh:

                    async def noop_refresh(source):
                        return None

                    refresh.side_effect = noop_refresh
                    with patch.object(client.config, "_parent") as parent:
                        parent._ensure_ws.return_value = MagicMock()
                        with caplog.at_level(logging.WARNING, logger="smplkit"):
                            await client.config._ensure_connected()
            assert any("Config discovery flush before connect" in r.message for r in caplog.records)

        asyncio.run(_run())


# ===========================================================================
# Async dict-bind + single-value get
# ===========================================================================


class TestBindDictAsync:
    def test_bind_returns_the_same_dict(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        payload = {"connection_string": "x", "timeout": 30}

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        return await client.config.bind("db", payload)

        result = asyncio.run(_run())
        assert result is payload

    def test_bind_rejects_non_basemodel_non_dict(self):
        client = _new_async_client()
        client.config._connected = True

        async def _run():
            with pytest.raises(TypeError, match="BaseModel instance or dict"):
                await client.config.bind("db", ["nope"])  # type: ignore[arg-type]

        asyncio.run(_run())

    def test_bind_dict_registers_every_key(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item") as reg_item:
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        await client.config.bind("db", {"k": "v", "n": 5, "b": True})
            return reg_item

        reg_item = asyncio.run(_run())
        types = {c.args[1]: c.args[2] for c in reg_item.call_args_list}
        assert types == {"k": "STRING", "n": "NUMBER", "b": "BOOLEAN"}

    def test_bind_dict_with_parent(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"base": {}, "child": {}}

        async def _run():
            with patch.object(client.config, "register_config") as register:
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        base = await client.config.bind("base", {"k": "v"})
                        register.reset_mock()
                        await client.config.bind("child", {"other": 1}, parent=base)
            return register

        register = asyncio.run(_run())
        register.assert_called_once()
        assert register.call_args.kwargs["parent"] == "base"

    def test_bind_dict_rejects_unbound_parent(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {}
        stray = {"k": "v"}

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        with pytest.raises(ValueError, match="previously returned from client.config.bind"):
                            await client.config.bind("child", {"k": "v"}, parent=stray)

        asyncio.run(_run())

    def test_bind_dict_syncs_from_cache(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"timeout": 999}}
        payload = {"timeout": 30}

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        return await client.config.bind("db", payload)

        result = asyncio.run(_run())
        assert result["timeout"] == 999

    def test_fire_change_listeners_mutates_bound_dict(self):
        """The async client's listener pipeline also handles dict targets."""
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"timeout": 30}}
        payload = {"timeout": 30}

        async def _run():
            with patch.object(client.config, "register_config"):
                with patch.object(client.config, "register_config_item"):
                    with patch.object(client.config, "_ensure_connected", new_callable=AsyncMock):
                        await client.config.bind("db", payload)

        asyncio.run(_run())
        old_cache = {"db": {"timeout": 30}}
        new_cache = {"db": {"timeout": 120}}
        client.config._fire_change_listeners(old_cache, new_cache, source="websocket")
        assert payload["timeout"] == 120


class TestSubscribeValueReadAsync:
    """Async value reads go through the ``subscribe(id)`` proxy."""

    def test_proxy_value_read(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"connection_string": "x"}}
        proxy = client.config.subscribe("db")
        assert proxy["connection_string"] == "x"

    def test_proxy_missing_key_raises_key_error(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        proxy = client.config.subscribe("db")
        with pytest.raises(KeyError, match="connection_string"):
            proxy["connection_string"]

    def test_proxy_get_with_default_returns_value_when_present(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"k": "real"}}
        proxy = client.config.subscribe("db")
        assert proxy.get("k", "fallback") == "real"

    def test_proxy_get_with_default_returns_default_when_key_missing(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {}}
        proxy = client.config.subscribe("db")
        assert proxy.get("missing", "fallback") == "fallback"

    def test_subscribe_registers_config(self):
        client = _new_async_client()
        client.config._connected = True
        client.config._config_cache = {"db": {"k": "v"}}
        with patch.object(client.config, "register_config") as register:
            client.config.subscribe("db")
        register.assert_called_once_with(
            "db",
            service="svc",
            environment="prod",
            parent=None,
            name=None,
            description=None,
        )
