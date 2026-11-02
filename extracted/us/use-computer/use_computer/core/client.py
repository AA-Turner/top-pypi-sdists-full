from __future__ import annotations

import os
from dataclasses import dataclass, field
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Literal

import httpx

from use_computer.core.errors import _araise_if_unsupported, _raise_if_unsupported
from use_computer.core.retry import AsyncRetryTransport, RetryTransport
from use_computer.core.sandbox import (
    AsyncMacOSSandbox,
    MacOSSandbox,
    SandboxType,
)

DEFAULT_BASE_URL = "https://api.use.computer"
SDK_VERSION = "0.0.0"
try:
    SDK_VERSION = version("use-computer")
except PackageNotFoundError:
    pass

SandboxTypeInput = SandboxType | Literal["macos"]


def _resolve_api_key(api_key: str | None) -> str | None:
    if api_key is not None:
        return api_key
    return os.getenv("USE_COMPUTER_API_KEY")


def _resolve_base_url(base_url: str | None) -> str:
    return (base_url or os.getenv("USE_COMPUTER_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")


def _resolve_headers(api_key: str | None, host_header: str | None = None) -> dict[str, str]:
    headers: dict[str, str] = {"X-Use-Computer-SDK": f"python/{SDK_VERSION}"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    host = host_header if host_header is not None else os.getenv("USE_COMPUTER_HOST_HEADER")
    if host:
        headers["Host"] = host
    return headers


def _absolute_url(base_url: str, value: str) -> str:
    if not value or value.startswith(("http://", "https://")):
        return value
    return f"{base_url}{'' if value.startswith('/') else '/'}{value}"


def _normalize_sandbox_type(type: SandboxTypeInput) -> SandboxType:
    if isinstance(type, SandboxType):
        return type
    if str(type).lower() != "macos":
        raise ValueError("type must be macos")
    return SandboxType.MACOS


@dataclass
class Reservation:
    """Mac Mini reservation created from account credits."""

    id: str
    reservation_id: str
    user_id: str = ""
    mini_count: int = 0
    hours: int = 0
    start_at: str = ""
    end_at: str = ""
    status: str = ""
    mini_ips: list[str] = field(default_factory=list)
    total_cents: int = 0

    @staticmethod
    def _from_dict(d: dict[str, Any]) -> Reservation:
        rid = d.get("reservation_id") or d.get("id", "")
        return Reservation(
            id=d.get("id", rid),
            reservation_id=rid,
            user_id=d.get("user_id", ""),
            mini_count=d.get("mini_count", 0),
            hours=d.get("hours", 0),
            start_at=d.get("start_at", ""),
            end_at=d.get("end_at", ""),
            status=d.get("status", ""),
            mini_ips=d.get("mini_ips") or [],
            total_cents=d.get("total_cents", 0),
        )


class Computer:
    """use.computer client. Creates and manages macOS sandboxes."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        host_header: str | None = None,
    ):
        self._base_url = _resolve_base_url(base_url)
        self._api_key = _resolve_api_key(api_key)
        self._http = httpx.Client(
            base_url=self._base_url,
            headers=_resolve_headers(self._api_key, host_header),
            timeout=60.0,
            transport=RetryTransport(httpx.HTTPTransport()),
            event_hooks={"response": [_raise_if_unsupported]},
        )

    def platforms(self, reservation_id: str = "") -> dict:
        """Discover available platforms, images, runtimes, and device types."""
        params = {"reservation_id": reservation_id} if reservation_id else None
        resp = self._http.get("/v1/platforms", params=params)
        resp.raise_for_status()
        return resp.json()

    def snapshots(self) -> list[dict[str, Any]]:
        """List macOS snapshots visible to this API key."""
        resp = self._http.get("/v1/snapshots")
        resp.raise_for_status()
        return resp.json().get("snapshots", [])

    def reserve(self, *, hours: int = 24, mini_count: int = 1) -> Reservation:
        """Reserve one Mac Mini using account credits."""
        resp = self._http.post(
            "/v1/reservations",
            json={"hours": hours, "mini_count": mini_count},
            timeout=180.0,
        )
        resp.raise_for_status()
        return Reservation._from_dict(resp.json())

    def create(
        self,
        *,
        type: SandboxTypeInput = SandboxType.MACOS,
        reservation_id: str = "",
        host: str = "",
        snapshot: str = "",
        ephemeral: bool = True,
    ) -> MacOSSandbox:
        """Create a new macOS sandbox.

        Args:
            type: SandboxType.MACOS (default) or "macos".
            reservation_id: Active Mac reservation to use when authenticating
                with a stable account API key.
            host: Pin sandbox to a specific host machine (e.g. "mm001").
            snapshot: Snapshot version returned by sandbox.snapshot().
            ephemeral: If true, delete the sandbox after the idle timeout.
        """
        sandbox_type = _normalize_sandbox_type(type)
        body: dict[str, Any] = {"type": sandbox_type.value, "ephemeral": ephemeral}
        if reservation_id:
            body["reservation_id"] = reservation_id
        if host:
            body["host"] = host
        if snapshot:
            body["snapshot"] = snapshot

        resp = self._http.post("/v1/sandboxes", json=body, timeout=180.0)
        resp.raise_for_status()
        data = resp.json()
        sid = data["sandbox_id"]
        return MacOSSandbox(
            sandbox_id=sid,
            http=self._http,
            vnc_url=_absolute_url(self._base_url, data.get("vnc_url", "")),
            vm_ip=data.get("vm_ip", ""),
            host=data.get("host", ""),
            ssh_url=_absolute_url(self._base_url, data.get("ssh_url", "")),
        )

    def get(self, sandbox_id: str) -> MacOSSandbox:
        """Get an existing sandbox by ID."""
        resp = self._http.get(f"/v1/sandboxes/{sandbox_id}")
        resp.raise_for_status()
        data = resp.json()
        return MacOSSandbox(
            sandbox_id=data["sandbox_id"],
            http=self._http,
            vnc_url=_absolute_url(self._base_url, data.get("vnc_url", "")),
            ssh_url=_absolute_url(self._base_url, data.get("ssh_url", "")),
            vm_ip=data.get("vm_ip", ""),
            host=data.get("host", ""),
        )

    def close(self):
        self._http.close()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


class AsyncComputer:
    """Async use.computer client."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        host_header: str | None = None,
    ):
        self._base_url = _resolve_base_url(base_url)
        self._api_key = _resolve_api_key(api_key)
        self._http = httpx.AsyncClient(
            base_url=self._base_url,
            headers=_resolve_headers(self._api_key, host_header),
            timeout=60.0,
            transport=AsyncRetryTransport(httpx.AsyncHTTPTransport()),
            event_hooks={"response": [_araise_if_unsupported]},
        )

    async def platforms(self, reservation_id: str = "") -> dict:
        """Discover available platforms, images, runtimes, and device types."""
        params = {"reservation_id": reservation_id} if reservation_id else None
        resp = await self._http.get("/v1/platforms", params=params)
        resp.raise_for_status()
        return resp.json()

    async def snapshots(self) -> list[dict[str, Any]]:
        """List macOS snapshots visible to this API key."""
        resp = await self._http.get("/v1/snapshots")
        resp.raise_for_status()
        return resp.json().get("snapshots", [])

    async def reserve(self, *, hours: int = 24, mini_count: int = 1) -> Reservation:
        """Reserve one Mac Mini using account credits."""
        resp = await self._http.post(
            "/v1/reservations",
            json={"hours": hours, "mini_count": mini_count},
            timeout=180.0,
        )
        resp.raise_for_status()
        return Reservation._from_dict(resp.json())

    async def create(
        self,
        *,
        type: SandboxTypeInput = SandboxType.MACOS,
        reservation_id: str = "",
        host: str = "",
        snapshot: str = "",
        ephemeral: bool = True,
    ) -> AsyncMacOSSandbox:
        """Create a new macOS sandbox.

        Args:
            type: SandboxType.MACOS (default) or "macos".
            reservation_id: Active Mac reservation to use when authenticating
                with a stable account API key.
            host: Pin sandbox to a specific host machine (e.g. "mm001").
            snapshot: Snapshot version returned by sandbox.snapshot().
            ephemeral: If true, delete the sandbox after the idle timeout.
        """
        sandbox_type = _normalize_sandbox_type(type)
        body: dict[str, Any] = {"type": sandbox_type.value, "ephemeral": ephemeral}
        if reservation_id:
            body["reservation_id"] = reservation_id
        if host:
            body["host"] = host
        if snapshot:
            body["snapshot"] = snapshot

        resp = await self._http.post("/v1/sandboxes", json=body, timeout=180.0)
        resp.raise_for_status()
        data = resp.json()
        sid = data["sandbox_id"]
        return AsyncMacOSSandbox(
            sandbox_id=sid,
            http=self._http,
            vnc_url=_absolute_url(self._base_url, data.get("vnc_url", "")),
            ssh_url=_absolute_url(self._base_url, data.get("ssh_url", "")),
            vm_ip=data.get("vm_ip", ""),
            host=data.get("host", ""),
        )

    async def get(self, sandbox_id: str) -> AsyncMacOSSandbox:
        """Get an existing sandbox by ID."""
        resp = await self._http.get(f"/v1/sandboxes/{sandbox_id}")
        resp.raise_for_status()
        data = resp.json()
        return AsyncMacOSSandbox(
            sandbox_id=data["sandbox_id"],
            http=self._http,
            vnc_url=_absolute_url(self._base_url, data.get("vnc_url", "")),
            ssh_url=_absolute_url(self._base_url, data.get("ssh_url", "")),
            vm_ip=data.get("vm_ip", ""),
            host=data.get("host", ""),
        )

    async def close(self):
        await self._http.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()
