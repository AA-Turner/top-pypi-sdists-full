"""Tests for smplkit.platform.models — environment/service/context-type models."""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock

import pytest

from smplkit.flags.types import Context
from smplkit.platform.models import (
    AsyncContextType,
    AsyncEnvironment,
    AsyncService,
    ContextType,
    Environment,
    Service,
    _ContextTypeBase,
    _EnvironmentBase,
    _ServiceBase,
)
from smplkit.platform.types import Color, EnvironmentClassification


# ---------------------------------------------------------------------------
# _EnvironmentBase / Environment / AsyncEnvironment
# ---------------------------------------------------------------------------


class TestEnvironmentBase:
    def test_default_init(self):
        env = _EnvironmentBase.__new__(_EnvironmentBase)
        _EnvironmentBase.__init__(env, name="production")
        assert env.id is None
        assert env.name == "production"
        assert env.color is None
        assert env.classification == EnvironmentClassification.STANDARD
        assert env.created_at is None
        assert env.updated_at is None

    def test_full_init(self):
        env = _EnvironmentBase.__new__(_EnvironmentBase)
        _EnvironmentBase.__init__(
            env,
            id="env-1",
            name="staging",
            color="#00ff00",
            classification=EnvironmentClassification.AD_HOC,
            created_at="2026-01-01",
            updated_at="2026-01-02",
        )
        assert env.id == "env-1"
        assert env.color == Color("#00ff00")
        assert env.classification == EnvironmentClassification.AD_HOC

    def test_repr(self):
        env = Environment(name="production", classification=EnvironmentClassification.STANDARD)
        r = repr(env)
        assert "Environment" in r
        assert "production" in r
        assert "STANDARD" in r

    def test_apply(self):
        env1 = Environment(name="production", id="e-1", created_at="2026-01-01")
        env2 = Environment(name="staging", id="e-2", color="#ff0000", updated_at="2026-02-01")
        env1._apply(env2)
        assert env1.name == "staging"
        assert env1.id == "e-2"
        assert env1.color == Color("#ff0000")
        assert env1.updated_at == "2026-02-01"

    def test_color_setter_accepts_hex_string(self):
        env = Environment(name="production")
        env.color = "#ef4444"
        assert env.color == Color("#ef4444")

    def test_color_setter_accepts_color_instance(self):
        env = Environment(name="production")
        env.color = Color("#ef4444")
        assert env.color == Color("#ef4444")

    def test_color_setter_accepts_none(self):
        env = Environment(name="production", color="#ef4444")
        env.color = None
        assert env.color is None

    def test_color_setter_rejects_other_types(self):
        env = Environment(name="production")
        with pytest.raises(TypeError, match="color must be a Color, hex string, or None"):
            env.color = 0xEF4444  # type: ignore[assignment]

    def test_color_setter_rejects_invalid_hex(self):
        env = Environment(name="production")
        with pytest.raises(ValueError, match="must be a CSS hex string"):
            env.color = "red"


class TestEnvironmentSave:
    def test_save_no_client_raises(self):
        env = Environment(name="production")
        with pytest.raises(RuntimeError, match="without a client"):
            env.save()

    def test_save_creates_when_no_created_at(self):
        mock_client = MagicMock()
        created = Environment(mock_client, id="env-1", name="production", created_at="2026-01-01")
        mock_client._create.return_value = created
        env = Environment(mock_client, name="production")
        env.save()
        mock_client._create.assert_called_once_with(env)
        assert env.id == "env-1"

    def test_save_updates_when_created_at_is_set(self):
        mock_client = MagicMock()
        updated = Environment(mock_client, id="env-1", name="updated-name", created_at="2026-01-01")
        mock_client._update.return_value = updated
        env = Environment(mock_client, id="env-1", name="production", created_at="2026-01-01")
        env.save()
        mock_client._update.assert_called_once_with(env)
        assert env.name == "updated-name"


class TestAsyncEnvironmentSave:
    def test_save_no_client_raises(self):
        env = AsyncEnvironment(name="production")
        with pytest.raises(RuntimeError, match="without a client"):
            asyncio.run(env.save())

    def test_save_creates(self):
        async def _run():
            mock_client = MagicMock()
            created = AsyncEnvironment(mock_client, id="env-1", name="production", created_at="2026-01-01")
            mock_client._create = AsyncMockReturning(created)
            env = AsyncEnvironment(mock_client, name="production")
            await env.save()
            assert env.id == "env-1"

        asyncio.run(_run())

    def test_save_updates(self):
        async def _run():
            mock_client = MagicMock()
            updated = AsyncEnvironment(mock_client, id="e-1", name="new-name", created_at="2026-01-01")

            async def fake_create(arg):
                return updated

            async def fake_update(arg):
                return updated

            mock_client._create = fake_create
            mock_client._update = fake_update

            env = AsyncEnvironment(mock_client, id="e-1", name="production", created_at="2026-01-01")
            await env.save()
            assert env.name == "new-name"

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# _ContextTypeBase / ContextType / AsyncContextType
# ---------------------------------------------------------------------------


class TestContextTypeBase:
    def test_default_init(self):
        ct = _ContextTypeBase.__new__(_ContextTypeBase)
        _ContextTypeBase.__init__(ct, name="user")
        assert ct.id is None
        assert ct.name == "user"
        assert ct.attributes == {}
        assert ct.created_at is None

    def test_init_with_attributes(self):
        ct = _ContextTypeBase.__new__(_ContextTypeBase)
        _ContextTypeBase.__init__(ct, name="user", attributes={"plan": {"type": "string"}})
        assert ct.attributes == {"plan": {"type": "string"}}

    def test_add_attribute(self):
        ct = ContextType(name="user")
        ct.add_attribute("plan", type="string", required=True)
        assert ct.attributes["plan"] == {"type": "string", "required": True}

    def test_remove_attribute(self):
        ct = ContextType(name="user", attributes={"plan": {}, "region": {}})
        ct.remove_attribute("plan")
        assert "plan" not in ct.attributes
        assert "region" in ct.attributes

    def test_remove_attribute_missing_key_no_error(self):
        ct = ContextType(name="user")
        ct.remove_attribute("nonexistent")  # should not raise

    def test_update_attribute(self):
        ct = ContextType(name="user", attributes={"plan": {"type": "string"}})
        ct.update_attribute("plan", type="integer", required=False)
        assert ct.attributes["plan"] == {"type": "integer", "required": False}

    def test_repr(self):
        ct = ContextType(id="ct-1", name="user")
        r = repr(ct)
        assert "ContextType" in r
        assert "ct-1" in r
        assert "user" in r

    def test_apply(self):
        ct1 = ContextType(id="ct-1", name="user", attributes={"a": {}})
        ct2 = ContextType(id="ct-2", name="account", attributes={"b": {}}, created_at="2026-01-01")
        ct1._apply(ct2)
        assert ct1.id == "ct-2"
        assert ct1.name == "account"
        assert ct1.attributes == {"b": {}}
        assert ct1.created_at == "2026-01-01"


class TestContextTypeSave:
    def test_save_no_client_raises(self):
        ct = ContextType(name="user")
        with pytest.raises(RuntimeError, match="without a client"):
            ct.save()

    def test_save_creates_when_no_created_at(self):
        mock_client = MagicMock()
        result = ContextType(mock_client, id="ct-1", name="user", created_at="2026-01-01")
        mock_client._create.return_value = result
        ct = ContextType(mock_client, name="user")
        ct.save()
        mock_client._create.assert_called_once_with(ct)
        assert ct.id == "ct-1"

    def test_save_updates_when_created_at_set(self):
        mock_client = MagicMock()
        result = ContextType(mock_client, id="ct-1", name="updated", created_at="2026-01-01")
        mock_client._update.return_value = result
        ct = ContextType(mock_client, id="ct-1", name="user", created_at="2026-01-01")
        ct.save()
        mock_client._update.assert_called_once_with(ct)
        assert ct.name == "updated"


class TestAsyncContextTypeSave:
    def test_save_no_client_raises(self):
        ct = AsyncContextType(name="user")
        with pytest.raises(RuntimeError, match="without a client"):
            asyncio.run(ct.save())

    def test_save_creates(self):
        async def _run():
            mock_client = MagicMock()
            result = AsyncContextType(mock_client, id="ct-1", name="user", created_at="2026-01-01")

            async def fake_create(arg):
                return result

            mock_client._create = fake_create
            ct = AsyncContextType(mock_client, name="user")
            await ct.save()
            assert ct.id == "ct-1"

        asyncio.run(_run())

    def test_save_updates(self):
        async def _run():
            mock_client = MagicMock()
            result = AsyncContextType(mock_client, id="ct-1", name="updated", created_at="2026-01-01")

            async def fake_update(arg):
                return result

            mock_client._update = fake_update
            ct = AsyncContextType(mock_client, id="ct-1", name="user", created_at="2026-01-01")
            await ct.save()
            assert ct.name == "updated"

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Context (server-returned)
# ---------------------------------------------------------------------------


class TestContextServerSide:
    def test_init(self):
        ctx = Context("user", "u-1", {"plan": "pro"}, name="Alice")
        assert ctx.type == "user"
        assert ctx.key == "u-1"
        assert ctx.name == "Alice"
        assert ctx.attributes == {"plan": "pro"}

    def test_default_metadata(self):
        ctx = Context("user", "u-1")
        assert ctx.name is None
        assert ctx.attributes == {}
        assert ctx.created_at is None
        assert ctx.updated_at is None

    def test_id_property(self):
        ctx = Context("user", "u-42")
        assert ctx.id == "user:u-42"

    def test_with_timestamps(self):
        ctx = Context("user", "u-1", created_at="2026-01-01", updated_at="2026-01-02")
        assert ctx.id == "user:u-1"
        assert ctx.created_at == "2026-01-01"
        assert ctx.updated_at == "2026-01-02"


# ---------------------------------------------------------------------------
# _ServiceBase / Service / AsyncService
# ---------------------------------------------------------------------------


class TestServiceBase:
    def test_default_init(self):
        svc = _ServiceBase.__new__(_ServiceBase)
        _ServiceBase.__init__(svc, name="User Service")
        assert svc.id is None
        assert svc.name == "User Service"
        assert svc.created_at is None
        assert svc.updated_at is None

    def test_full_init(self):
        svc = _ServiceBase.__new__(_ServiceBase)
        _ServiceBase.__init__(
            svc,
            id="user_service",
            name="User Service",
            created_at="2026-01-01",
            updated_at="2026-01-02",
        )
        assert svc.id == "user_service"
        assert svc.name == "User Service"
        assert svc.created_at == "2026-01-01"
        assert svc.updated_at == "2026-01-02"

    def test_repr(self):
        svc = Service(id="user_service", name="User Service")
        r = repr(svc)
        assert "Service" in r
        assert "user_service" in r
        assert "User Service" in r

    def test_apply(self):
        svc1 = Service(id="s-1", name="One", created_at="2026-01-01")
        svc2 = Service(id="s-2", name="Two", created_at="2026-02-01", updated_at="2026-02-02")
        svc1._apply(svc2)
        assert svc1.id == "s-2"
        assert svc1.name == "Two"
        assert svc1.created_at == "2026-02-01"
        assert svc1.updated_at == "2026-02-02"


class TestServiceSave:
    def test_save_no_client_raises(self):
        svc = Service(name="User Service")
        with pytest.raises(RuntimeError, match="without a client"):
            svc.save()

    def test_save_creates_when_no_created_at(self):
        mock_client = MagicMock()
        created = Service(mock_client, id="user_service", name="User Service", created_at="2026-01-01")
        mock_client._create.return_value = created
        svc = Service(mock_client, id="user_service", name="User Service")
        svc.save()
        mock_client._create.assert_called_once_with(svc)
        assert svc.created_at == "2026-01-01"

    def test_save_updates_when_created_at_is_set(self):
        mock_client = MagicMock()
        updated = Service(mock_client, id="user_service", name="Renamed", created_at="2026-01-01")
        mock_client._update.return_value = updated
        svc = Service(mock_client, id="user_service", name="User Service", created_at="2026-01-01")
        svc.save()
        mock_client._update.assert_called_once_with(svc)
        assert svc.name == "Renamed"


class TestAsyncServiceSave:
    def test_save_no_client_raises(self):
        svc = AsyncService(name="User Service")
        with pytest.raises(RuntimeError, match="without a client"):
            asyncio.run(svc.save())

    def test_save_creates(self):
        async def _run():
            mock_client = MagicMock()
            created = AsyncService(mock_client, id="user_service", name="User Service", created_at="2026-01-01")
            mock_client._create = AsyncMockReturning(created)
            svc = AsyncService(mock_client, id="user_service", name="User Service")
            await svc.save()
            assert svc.created_at == "2026-01-01"

        asyncio.run(_run())

    def test_save_updates(self):
        async def _run():
            mock_client = MagicMock()
            updated = AsyncService(mock_client, id="user_service", name="Renamed", created_at="2026-01-01")

            async def fake_update(arg):
                return updated

            mock_client._update = fake_update

            svc = AsyncService(mock_client, id="user_service", name="User Service", created_at="2026-01-01")
            await svc.save()
            assert svc.name == "Renamed"

        asyncio.run(_run())


# ---------------------------------------------------------------------------
# Helper for async tests
# ---------------------------------------------------------------------------


class AsyncMockReturning:
    """Minimal async callable returning a fixed value."""

    def __init__(self, value):
        self._value = value

    async def __call__(self, *args, **kwargs):
        return self._value
