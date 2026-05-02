from __future__ import annotations

import asyncio

import pytest

from capsule_sdk import AsyncCapsuleClient
from capsule_sdk.resources.async_workloads import AsyncWorkloads


class TestAsyncClientSurface:
    def test_workloads_is_primary_high_level_surface(self) -> None:
        client = AsyncCapsuleClient(
            control_plane_addr="http://testserver:8080",
            tenant_id="test-tenant",
        )
        try:
            assert isinstance(client.workloads, AsyncWorkloads)
        finally:
            asyncio.run(client.close())

    def test_layered_configs_is_not_public_surface(self) -> None:
        client = AsyncCapsuleClient(
            control_plane_addr="http://testserver:8080",
            tenant_id="test-tenant",
        )
        try:
            assert not hasattr(client, "layered_configs")
            with pytest.raises(AttributeError):
                _ = client.layered_configs
        finally:
            asyncio.run(client.close())
