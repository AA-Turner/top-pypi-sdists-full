from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .rpc import AsyncRpcClient
    from .bridge import AsyncBridge


class AsyncSandboxEnv:
    def __init__(self, rpc: AsyncRpcClient):
        self._rpc = rpc

    async def get(self, key: str) -> str:
        """Get the value of an environment variable."""

        params = {"key": key}
        result = await self._rpc.call("envGet", params)

        return result

    async def set(self, key: str, value: str) -> None:
        """Set the value of an environment variable."""

        params = {"key": key, "value": value}
        await self._rpc.call("envSet", params)

    async def as_dict(self) -> dict[str, str]:
        """Get all environment variables."""

        params = {}
        result = await self._rpc.call("envToObject", params)

        return result

    async def delete(self, key: str) -> None:
        """Delete an environment variable."""

        params = {"key": key}
        await self._rpc.call("envDelete", params)


class SandboxEnv:
    def __init__(self, rpc: AsyncRpcClient, bridge: AsyncBridge):
        self._rpc = rpc
        self._bridge = bridge
        self._async = AsyncSandboxEnv(rpc)

    def get(self, key: str) -> str:
        """Get the value of an environment variable."""
        return self._bridge.run(self._async.get(key))

    def set(self, key: str, value: str) -> None:
        """Set the value of an environment variable."""
        self._bridge.run(self._async.set(key, value))

    def as_dict(self) -> dict[str, str]:
        """Get all environment variables."""
        return self._bridge.run(self._async.as_dict())

    def delete(self, key: str) -> None:
        """Delete an environment variable."""
        self._bridge.run(self._async.delete(key))
