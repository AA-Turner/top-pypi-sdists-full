from __future__ import annotations

from unittest.mock import patch

import pytest

from anteroom.services.mission_adapters import (
    AdapterStatus,
    MissionAdapterRegistry,
    NoopAdapter,
    create_default_adapter_registry,
)


class TestAdapterStatus:
    def test_construction_defaults(self) -> None:
        status = AdapterStatus(state="pending")
        assert status.state == "pending"
        assert status.summary == ""
        assert status.artifacts == {}
        assert status.adapter_ref is None

    def test_construction_full(self) -> None:
        status = AdapterStatus(
            state="completed",
            summary="done",
            artifacts={"key": "val"},
            adapter_ref="ref-123",
        )
        assert status.state == "completed"
        assert status.summary == "done"
        assert status.artifacts == {"key": "val"}
        assert status.adapter_ref == "ref-123"

    def test_frozen_immutability(self) -> None:
        status = AdapterStatus(state="pending")
        with pytest.raises(AttributeError):
            status.state = "running"  # type: ignore[misc]


class TestMissionAdapterRegistry:
    def test_register_and_get(self) -> None:
        registry = MissionAdapterRegistry()
        adapter = NoopAdapter()
        registry.register("test", adapter)
        assert registry.get("test") is adapter

    def test_get_miss_returns_none(self) -> None:
        registry = MissionAdapterRegistry()
        assert registry.get("nonexistent") is None

    def test_list_types_sorted(self) -> None:
        registry = MissionAdapterRegistry()
        registry.register("beta", NoopAdapter())
        registry.register("alpha", NoopAdapter())
        assert registry.list_types() == ["alpha", "beta"]

    def test_duplicate_registration_overwrites(self) -> None:
        registry = MissionAdapterRegistry()
        first = NoopAdapter()
        second = NoopAdapter()
        registry.register("noop", first)
        registry.register("noop", second)
        assert registry.get("noop") is second


class TestNoopAdapter:
    @pytest.mark.asyncio
    async def test_create_returns_completed(self) -> None:
        adapter = NoopAdapter()
        result = await adapter.create(item={"name": "task1"}, context={})
        assert result.state == "completed"
        assert result.summary == "No-op execution"
        assert result.adapter_ref is not None
        assert len(result.adapter_ref) == 36  # UUID format

    @pytest.mark.asyncio
    async def test_status_returns_completed(self) -> None:
        adapter = NoopAdapter()
        result = await adapter.status(adapter_ref="ref-123")
        assert result.state == "completed"

    @pytest.mark.asyncio
    async def test_cancel_returns_cancelled(self) -> None:
        adapter = NoopAdapter()
        result = await adapter.cancel(adapter_ref="ref-123")
        assert result.state == "cancelled"

    @pytest.mark.asyncio
    async def test_create_error_handling(self) -> None:
        adapter = NoopAdapter()
        with patch("anteroom.services.mission_adapters.uuid4", side_effect=RuntimeError("boom")):
            result = await adapter.create(item={}, context={})
        assert result.state == "failed"
        assert "boom" in result.summary


class TestCreateDefaultAdapterRegistry:
    def test_has_noop_registered(self) -> None:
        registry = create_default_adapter_registry()
        adapter = registry.get("noop")
        assert adapter is not None
        assert isinstance(adapter, NoopAdapter)

    def test_list_types(self) -> None:
        registry = create_default_adapter_registry()
        assert "noop" in registry.list_types()
