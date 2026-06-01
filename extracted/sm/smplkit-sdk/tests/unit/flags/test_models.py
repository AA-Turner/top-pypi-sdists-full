"""Tests for the unified Flag model hierarchy (sync and async variants)."""

import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest

from smplkit.flags.models import (
    AsyncBooleanFlag,
    AsyncFlag,
    AsyncJsonFlag,
    AsyncNumberFlag,
    AsyncStringFlag,
    BooleanFlag,
    Flag,
    FlagEnvironment,
    FlagRule,
    FlagValue,
    JsonFlag,
    NumberFlag,
    StringFlag,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _env(enabled=True, default=None, rules=None):
    """Shorthand for FlagEnvironment in test fixtures."""
    return FlagEnvironment(enabled=enabled, default=default, rules=tuple(rules or ()))


def _rule(logic=None, value=None, description=None):
    """Shorthand for FlagRule in test fixtures."""
    return FlagRule(logic=dict(logic or {}), value=value, description=description)


def _val(name, value):
    """Shorthand for FlagValue."""
    return FlagValue(name=name, value=value)


def _make_flag(cls=Flag, client=None, **overrides):
    defaults = {
        "id": "test-flag",
        "name": "Test Flag",
        "type": "BOOLEAN",
        "default": False,
        "values": [_val("True", True)],
        "description": "A test flag",
        "environments": {"staging": _env()},
    }
    defaults.update(overrides)
    client = client or MagicMock()
    return cls(client, **defaults)


# ===========================================================================
# Flag (sync base)
# ===========================================================================


class TestFlag:
    def test_properties(self):
        flag = _make_flag()
        assert flag.id == "test-flag"
        assert flag.name == "Test Flag"
        assert flag.type == "BOOLEAN"
        assert flag.default is False
        assert flag.description == "A test flag"
        assert flag.values == [_val("True", True)]
        assert flag.environments == {"staging": FlagEnvironment(enabled=True, default=None, rules=())}

    def test_defaults(self):
        client = MagicMock()
        flag = Flag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.values is None
        assert flag.description is None
        assert flag.environments == {}
        assert flag.created_at is None
        assert flag.updated_at is None

    def test_unconstrained_values_none(self):
        client = MagicMock()
        flag = Flag(client, id="k", name="n", type="STRING", default="hello", values=None)
        assert flag.values is None
        assert flag.default == "hello"

    def test_repr(self):
        flag = _make_flag()
        r = repr(flag)
        assert "test-flag" in r
        assert "BOOLEAN" in r

    # ------------------------------------------------------------------
    # save() — create path (created_at is None)
    # ------------------------------------------------------------------

    def test_save_creates_when_created_at_is_none(self):
        client = MagicMock()
        flag = Flag(client, id="new-flag", name="New", type="BOOLEAN", default=False)
        created = Flag(client, id="new-flag", name="New", type="BOOLEAN", default=False, created_at="2024-01-01")
        client._create_flag.return_value = created

        flag.save()

        client._create_flag.assert_called_once_with(flag)
        assert flag.created_at == "2024-01-01"

    # ------------------------------------------------------------------
    # save() — update path (created_at is set)
    # ------------------------------------------------------------------

    def test_save_updates_when_created_at_is_set(self):
        client = MagicMock()
        flag = Flag(client, id="existing-id", name="Old", type="BOOLEAN", default=False, created_at="2024-01-01")
        updated = Flag(client, id="existing-id", name="Updated", type="BOOLEAN", default=True, created_at="2024-01-01")
        client._update_flag.return_value = updated

        flag.save()

        client._update_flag.assert_called_once_with(flag=flag)
        assert flag.name == "Updated"
        assert flag.default is True

    # ------------------------------------------------------------------
    # delete()
    # ------------------------------------------------------------------

    def test_delete_calls_client_delete(self):
        client = MagicMock()
        flag = Flag(client, id="to-delete", name="x", type="BOOLEAN", default=False)
        flag.delete()
        client.delete.assert_called_once_with("to-delete")

    def test_delete_without_client_raises(self):
        flag = Flag(None, id="x", name="x", type="BOOLEAN", default=False)
        with pytest.raises(RuntimeError, match="cannot delete"):
            flag.delete()

    # ------------------------------------------------------------------
    # _apply
    # ------------------------------------------------------------------

    def test_apply_copies_all_fields(self):
        client = MagicMock()
        flag = Flag(client, id="k", name="n", type="BOOLEAN", default=False)
        other = Flag(
            client,
            id="new-id",
            name="new-name",
            type="STRING",
            default="hello",
            values=[_val("v", "v")],
            description="desc",
            environments={"prod": _env()},
            created_at="2024-01-01",
            updated_at="2024-06-01",
        )
        flag._apply(other)
        assert flag.id == "new-id"
        assert flag.name == "new-name"
        assert flag.type == "STRING"
        assert flag.default == "hello"
        assert flag.values == [_val("v", "v")]
        assert flag.description == "desc"
        assert flag.environments == {"prod": FlagEnvironment(enabled=True)}
        assert flag.created_at == "2024-01-01"
        assert flag.updated_at == "2024-06-01"

    # ------------------------------------------------------------------
    # add_rule — local mutation
    # ------------------------------------------------------------------

    def test_addRule_appends_to_environment(self):
        flag = _make_flag(environments={"staging": _env()})
        rule = {"environment": "staging", "logic": {"==": [1, 1]}, "value": True, "description": "always on"}
        result = flag.add_rule(rule)

        # Returns self for chaining
        assert result is flag
        # Rule added as a typed FlagRule (no leftover "environment" field)
        assert len(flag.environments["staging"].rules) == 1
        added = flag.environments["staging"].rules[0]
        assert added.logic == {"==": [1, 1]}
        assert added.value is True
        assert added.description == "always on"

    def test_addRule_creates_environment_if_missing(self):
        flag = _make_flag(environments={})
        flag.add_rule({"environment": "production", "logic": {}, "value": "v"})
        assert "production" in flag.environments
        assert len(flag.environments["production"].rules) == 1

    def test_addRule_requires_environment_key(self):
        flag = _make_flag()
        with pytest.raises(ValueError, match="environment"):
            flag.add_rule({"logic": {}, "value": True})

    def test_addRule_chaining(self):
        flag = _make_flag(environments={})
        flag.add_rule({"environment": "staging", "logic": {}, "value": 1}).add_rule(
            {"environment": "staging", "logic": {}, "value": 2}
        )
        assert len(flag.environments["staging"].rules) == 2

    # ------------------------------------------------------------------
    # enable_rules / disable_rules
    # ------------------------------------------------------------------

    def test_disable_rules_existing(self):
        flag = _make_flag(environments={"staging": _env()})
        flag.disable_rules(environment="staging")
        assert flag.environments["staging"].enabled is False

    def test_enable_rules_new_environment(self):
        flag = _make_flag(environments={})
        flag.enable_rules(environment="production")
        assert flag.environments["production"].enabled is True

    def test_disable_rules_new_environment(self):
        flag = _make_flag(environments={})
        flag.disable_rules(environment="production")
        assert flag.environments["production"].enabled is False

    def test_enable_rules_no_env_applies_to_all(self):
        flag = _make_flag(environments={"staging": _env(enabled=False), "production": _env(enabled=False)})
        flag.enable_rules()
        assert flag.environments["staging"].enabled is True
        assert flag.environments["production"].enabled is True

    def test_disable_rules_no_env_applies_to_all(self):
        flag = _make_flag(environments={"staging": _env(enabled=True), "production": _env(enabled=True)})
        flag.disable_rules()
        assert flag.environments["staging"].enabled is False
        assert flag.environments["production"].enabled is False

    # ------------------------------------------------------------------
    # set_default / clear_default
    # ------------------------------------------------------------------

    def test_set_default_base(self):
        flag = _make_flag(default=False)
        flag.set_default(True)
        assert flag.default is True

    def test_set_default_environment_existing(self):
        flag = _make_flag(environments={"staging": _env()})
        flag.set_default("new-default", environment="staging")
        assert flag.environments["staging"].default == "new-default"

    def test_set_default_environment_new(self):
        flag = _make_flag(environments={})
        flag.set_default(42, environment="production")
        assert flag.environments["production"].default == 42

    def test_clear_default_existing(self):
        flag = _make_flag(environments={"staging": _env(default="overridden")})
        flag.clear_default(environment="staging")
        assert flag.environments["staging"].default is None

    def test_clear_default_missing_env_is_noop(self):
        flag = _make_flag(environments={})
        flag.clear_default(environment="production")  # should not raise
        assert "production" not in flag.environments

    # ------------------------------------------------------------------
    # clear_rules
    # ------------------------------------------------------------------

    def test_clearRules_existing(self):
        flag = _make_flag(environments={"staging": _env(rules=[_rule(value=True)])})
        flag.clear_rules(environment="staging")
        assert flag.environments["staging"].rules == ()

    def test_clearRules_new_environment(self):
        flag = _make_flag(environments={})
        flag.clear_rules(environment="production")
        assert flag.environments["production"].rules == ()

    def test_clearRules_no_env_applies_to_all(self):
        flag = _make_flag(
            environments={
                "staging": _env(rules=[_rule(value=True)]),
                "production": _env(rules=[_rule(value=False)]),
            }
        )
        flag.clear_rules()
        assert flag.environments["staging"].rules == ()
        assert flag.environments["production"].rules == ()

    # ------------------------------------------------------------------
    # add_value / remove_value / clear_values
    # ------------------------------------------------------------------

    def test_addValue_appends_dict(self):
        flag = _make_flag(values=[_val("Red", "red")])
        result = flag.add_value("Blue", "blue")
        assert flag.values == [_val("Red", "red"), _val("Blue", "blue")]
        assert result is flag  # chainable

    def test_addValue_initializes_when_none(self):
        flag = _make_flag(values=None)
        flag.add_value("Red", "red")
        assert flag.values == [_val("Red", "red")]

    def test_removeValue_drops_matching_entry(self):
        flag = _make_flag(
            values=[_val("Red", "red"), _val("Blue", "blue")],
        )
        result = flag.remove_value("red")
        assert flag.values == [_val("Blue", "blue")]
        assert result is flag

    def test_removeValue_no_op_when_values_none(self):
        flag = _make_flag(values=None)
        flag.remove_value("red")
        assert flag.values is None

    def test_clearValues_sets_to_none(self):
        flag = _make_flag(values=[_val("Red", "red")])
        flag.clear_values()
        assert flag.values is None

    # ------------------------------------------------------------------
    # get (runtime evaluation)
    # ------------------------------------------------------------------

    def test_get_delegates_to_client(self):
        client = MagicMock()
        client._evaluate_handle.return_value = True
        flag = Flag(client, id="k", name="n", type="BOOLEAN", default=False)
        result = flag.get()
        client._evaluate_handle.assert_called_once_with("k", False, None)
        assert result is True

    def test_get_with_context(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "matched"
        flag = Flag(client, id="k", name="n", type="STRING", default="off")
        ctx = [MagicMock()]
        result = flag.get(context=ctx)
        client._evaluate_handle.assert_called_once_with("k", "off", ctx)
        assert result == "matched"


# ===========================================================================
# Typed sync flags
# ===========================================================================


class TestBooleanFlag:
    def test_returns_bool(self):
        client = MagicMock()
        client._evaluate_handle.return_value = True
        flag = BooleanFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.get() is True

    def test_returns_default_on_non_bool(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "not a bool"
        flag = BooleanFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.get() is False


class TestStringFlag:
    def test_returns_string(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "blue"
        flag = StringFlag(client, id="color", name="Color", type="STRING", default="red")
        assert flag.get() == "blue"

    def test_returns_default_on_non_string(self):
        client = MagicMock()
        client._evaluate_handle.return_value = 42
        flag = StringFlag(client, id="color", name="Color", type="STRING", default="red")
        assert flag.get() == "red"


class TestNumberFlag:
    def test_returns_int(self):
        client = MagicMock()
        client._evaluate_handle.return_value = 5
        flag = NumberFlag(client, id="retries", name="Retries", type="NUMERIC", default=3)
        assert flag.get() == 5

    def test_returns_float(self):
        client = MagicMock()
        client._evaluate_handle.return_value = 3.14
        flag = NumberFlag(client, id="rate", name="Rate", type="NUMERIC", default=1.0)
        assert flag.get() == 3.14

    def test_rejects_bool(self):
        client = MagicMock()
        client._evaluate_handle.return_value = True
        flag = NumberFlag(client, id="retries", name="Retries", type="NUMERIC", default=3)
        assert flag.get() == 3

    def test_returns_default_on_string(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "not a number"
        flag = NumberFlag(client, id="retries", name="Retries", type="NUMERIC", default=3)
        assert flag.get() == 3


class TestJsonFlag:
    def test_returns_dict(self):
        client = MagicMock()
        client._evaluate_handle.return_value = {"mode": "dark"}
        flag = JsonFlag(client, id="theme", name="Theme", type="JSON", default={"mode": "light"})
        assert flag.get() == {"mode": "dark"}

    def test_returns_default_on_non_dict(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "not a dict"
        flag = JsonFlag(client, id="theme", name="Theme", type="JSON", default={"mode": "light"})
        assert flag.get() == {"mode": "light"}


# ===========================================================================
# AsyncFlag
# ===========================================================================


class TestAsyncFlag:
    def test_properties(self):
        client = MagicMock()
        flag = AsyncFlag(
            client,
            id="async-flag",
            name="Async Flag",
            type="BOOLEAN",
            default=True,
            values=[],
            description="async desc",
            environments={"prod": _env()},
        )
        assert flag.id == "async-flag"
        assert flag.name == "Async Flag"
        assert flag.description == "async desc"

    def test_defaults(self):
        client = MagicMock()
        flag = AsyncFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.values is None
        assert flag.environments == {}

    def test_repr(self):
        flag = _make_flag(cls=AsyncFlag)
        r = repr(flag)
        assert "AsyncFlag" in r
        assert "test-flag" in r

    # ------------------------------------------------------------------
    # save() — create path (created_at is None, async)
    # ------------------------------------------------------------------

    def test_save_creates_when_created_at_is_none(self):
        client = AsyncMock()
        flag = AsyncFlag(client, id="new-flag", name="New", type="BOOLEAN", default=False)
        created = AsyncFlag(client, id="new-flag", name="New", type="BOOLEAN", default=False, created_at="2024-01-01")
        client._create_flag.return_value = created

        async def _run():
            await flag.save()
            assert flag.created_at == "2024-01-01"

        asyncio.run(_run())

    # ------------------------------------------------------------------
    # save() — update path (created_at is set, async)
    # ------------------------------------------------------------------

    def test_save_updates_when_created_at_is_set(self):
        client = AsyncMock()
        flag = AsyncFlag(client, id="existing-id", name="Old", type="BOOLEAN", default=False, created_at="2024-01-01")
        updated = AsyncFlag(
            client, id="existing-id", name="Updated", type="BOOLEAN", default=True, created_at="2024-01-01"
        )
        client._update_flag.return_value = updated

        async def _run():
            await flag.save()
            assert flag.name == "Updated"
            assert flag.default is True

        asyncio.run(_run())

    # ------------------------------------------------------------------
    # delete()
    # ------------------------------------------------------------------

    def test_delete_calls_client_delete(self):
        client = AsyncMock()
        flag = AsyncFlag(client, id="to-delete", name="x", type="BOOLEAN", default=False)

        async def _run():
            await flag.delete()
            client.delete.assert_called_once_with("to-delete")

        asyncio.run(_run())

    def test_delete_without_client_raises(self):
        flag = AsyncFlag(None, id="x", name="x", type="BOOLEAN", default=False)

        async def _run():
            with pytest.raises(RuntimeError, match="cannot delete"):
                await flag.delete()

        asyncio.run(_run())

    # ------------------------------------------------------------------
    # _apply
    # ------------------------------------------------------------------

    def test_apply_copies_all_fields(self):
        client = MagicMock()
        flag = AsyncFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        other = AsyncFlag(
            client,
            id="new-id",
            name="new-name",
            type="STRING",
            default="hello",
            values=[_val("v", "v")],
            description="desc",
            environments={"prod": _env()},
            created_at="2024-01-01",
            updated_at="2024-06-01",
        )
        flag._apply(other)
        assert flag.id == "new-id"
        assert flag.type == "STRING"
        assert flag.default == "hello"

    # ------------------------------------------------------------------
    # add_rule — local mutation (sync)
    # ------------------------------------------------------------------

    def test_addRule_appends_to_environment(self):
        flag = _make_flag(cls=AsyncFlag, environments={"staging": _env()})
        result = flag.add_rule({"environment": "staging", "logic": {"==": [1, 1]}, "value": True})
        assert result is flag
        assert len(flag.environments["staging"].rules) == 1
        assert flag.environments["staging"].rules[0].logic == {"==": [1, 1]}

    def test_addRule_creates_environment_if_missing(self):
        flag = _make_flag(cls=AsyncFlag, environments={})
        flag.add_rule({"environment": "production", "logic": {}, "value": "v"})
        assert "production" in flag.environments

    def test_addRule_requires_environment_key(self):
        flag = _make_flag(cls=AsyncFlag)
        with pytest.raises(ValueError, match="environment"):
            flag.add_rule({"logic": {}, "value": True})

    # ------------------------------------------------------------------
    # enable_rules / disable_rules / set_default / clear_rules
    # ------------------------------------------------------------------

    def test_enable_rules(self):
        flag = _make_flag(cls=AsyncFlag, environments={})
        flag.enable_rules(environment="staging")
        assert flag.environments["staging"].enabled is True

    def test_disable_rules(self):
        flag = _make_flag(cls=AsyncFlag, environments={})
        flag.disable_rules(environment="staging")
        assert flag.environments["staging"].enabled is False

    def test_set_default_base(self):
        flag = _make_flag(cls=AsyncFlag, default="old")
        flag.set_default("new")
        assert flag.default == "new"

    def test_set_default_environment(self):
        flag = _make_flag(cls=AsyncFlag, environments={})
        flag.set_default("default-val", environment="staging")
        assert flag.environments["staging"].default == "default-val"

    def test_clearRules(self):
        flag = _make_flag(
            cls=AsyncFlag,
            environments={"staging": _env(rules=[_rule(value=True)])},
        )
        flag.clear_rules(environment="staging")
        assert flag.environments["staging"].rules == ()

    def test_enable_rules_no_env_applies_to_all(self):
        flag = _make_flag(
            cls=AsyncFlag,
            environments={"staging": _env(enabled=False), "production": _env(enabled=False)},
        )
        flag.enable_rules()
        assert flag.environments["staging"].enabled is True
        assert flag.environments["production"].enabled is True

    def test_disable_rules_no_env_applies_to_all(self):
        flag = _make_flag(
            cls=AsyncFlag,
            environments={"staging": _env(enabled=True), "production": _env(enabled=True)},
        )
        flag.disable_rules()
        assert flag.environments["staging"].enabled is False
        assert flag.environments["production"].enabled is False

    def test_clearRules_no_env_applies_to_all(self):
        flag = _make_flag(
            cls=AsyncFlag,
            environments={
                "staging": _env(rules=[_rule(value=True)]),
                "production": _env(rules=[_rule(value=False)]),
            },
        )
        flag.clear_rules()
        assert flag.environments["staging"].rules == ()
        assert flag.environments["production"].rules == ()

    def test_clear_default_existing(self):
        flag = _make_flag(cls=AsyncFlag, environments={"staging": _env(default="overridden")})
        flag.clear_default(environment="staging")
        assert flag.environments["staging"].default is None

    def test_clear_default_missing_env_is_noop(self):
        flag = _make_flag(cls=AsyncFlag, environments={})
        flag.clear_default(environment="production")
        assert "production" not in flag.environments

    # ------------------------------------------------------------------
    # add_value / remove_value / clear_values (async)
    # ------------------------------------------------------------------

    def test_addValue_appends_dict(self):
        flag = _make_flag(cls=AsyncFlag, values=[_val("Red", "red")])
        result = flag.add_value("Blue", "blue")
        assert flag.values == [_val("Red", "red"), _val("Blue", "blue")]
        assert result is flag

    def test_addValue_initializes_when_none(self):
        flag = _make_flag(cls=AsyncFlag, values=None)
        flag.add_value("Red", "red")
        assert flag.values == [_val("Red", "red")]

    def test_removeValue_drops_matching_entry(self):
        flag = _make_flag(
            cls=AsyncFlag,
            values=[_val("Red", "red"), _val("Blue", "blue")],
        )
        result = flag.remove_value("red")
        assert flag.values == [_val("Blue", "blue")]
        assert result is flag

    def test_removeValue_no_op_when_values_none(self):
        flag = _make_flag(cls=AsyncFlag, values=None)
        flag.remove_value("red")
        assert flag.values is None

    def test_clearValues_sets_to_none(self):
        flag = _make_flag(cls=AsyncFlag, values=[_val("Red", "red")])
        flag.clear_values()
        assert flag.values is None

    # ------------------------------------------------------------------
    # get (runtime evaluation — sync)
    # ------------------------------------------------------------------

    def test_get_delegates_to_client(self):
        client = MagicMock()
        client._evaluate_handle.return_value = True
        flag = AsyncFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.get() is True
        client._evaluate_handle.assert_called_once_with("k", False, None)

    def test_get_with_context(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "val"
        flag = AsyncFlag(client, id="k", name="n", type="STRING", default="off")
        ctx = [MagicMock()]
        assert flag.get(context=ctx) == "val"


# ===========================================================================
# Typed async flags
# ===========================================================================


class TestAsyncBooleanFlag:
    def test_returns_bool(self):
        client = MagicMock()
        client._evaluate_handle.return_value = True
        flag = AsyncBooleanFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.get() is True

    def test_returns_default_on_non_bool(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "not a bool"
        flag = AsyncBooleanFlag(client, id="k", name="n", type="BOOLEAN", default=False)
        assert flag.get() is False


class TestAsyncStringFlag:
    def test_returns_string(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "blue"
        flag = AsyncStringFlag(client, id="color", name="Color", type="STRING", default="red")
        assert flag.get() == "blue"

    def test_returns_default_on_non_string(self):
        client = MagicMock()
        client._evaluate_handle.return_value = 42
        flag = AsyncStringFlag(client, id="color", name="Color", type="STRING", default="red")
        assert flag.get() == "red"


class TestAsyncNumberFlag:
    def test_returns_int(self):
        client = MagicMock()
        client._evaluate_handle.return_value = 5
        flag = AsyncNumberFlag(client, id="retries", name="Retries", type="NUMERIC", default=3)
        assert flag.get() == 5

    def test_returns_float(self):
        client = MagicMock()
        client._evaluate_handle.return_value = 3.14
        flag = AsyncNumberFlag(client, id="rate", name="Rate", type="NUMERIC", default=1.0)
        assert flag.get() == 3.14

    def test_rejects_bool(self):
        client = MagicMock()
        client._evaluate_handle.return_value = True
        flag = AsyncNumberFlag(client, id="retries", name="Retries", type="NUMERIC", default=3)
        assert flag.get() == 3

    def test_returns_default_on_string(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "nope"
        flag = AsyncNumberFlag(client, id="retries", name="Retries", type="NUMERIC", default=3)
        assert flag.get() == 3


class TestAsyncJsonFlag:
    def test_returns_dict(self):
        client = MagicMock()
        client._evaluate_handle.return_value = {"mode": "dark"}
        flag = AsyncJsonFlag(client, id="theme", name="Theme", type="JSON", default={"mode": "light"})
        assert flag.get() == {"mode": "dark"}

    def test_returns_default_on_non_dict(self):
        client = MagicMock()
        client._evaluate_handle.return_value = "not a dict"
        flag = AsyncJsonFlag(client, id="theme", name="Theme", type="JSON", default={"mode": "light"})
        assert flag.get() == {"mode": "light"}
