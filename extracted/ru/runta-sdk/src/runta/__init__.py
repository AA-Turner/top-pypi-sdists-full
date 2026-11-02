"""Runta Python SDK public API."""

from __future__ import annotations

import asyncio
import time
import tarfile
import uuid
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class RuntaError(Exception):
    """Base class for SDK errors."""


class ConfigError(RuntaError):
    """Configuration is missing or invalid."""


class ApiError(RuntaError):
    """Control-plane RPC failed."""

    status_code: int | None
    """HTTP status code, when available."""
    code: str | None
    """Runta API error code, when available."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        code: str | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code

    def __str__(self) -> str:
        parts = []
        if self.status_code is not None:
            parts.append(f"HTTP {self.status_code}")
        if self.code:
            parts.append(str(self.code))
        message = super().__str__()
        if message:
            parts.append(message)
        return ": ".join(parts) if parts else self.__class__.__name__


_RUNTIME_READINESS_MAX_POLL_INTERVAL = 10.0


class CommandError(RuntaError):
    """A runtime command failed."""

    exit_code: int | None
    """Command exit code, when available."""

    def __init__(self, message: str, *, exit_code: int | None = None) -> None:
        super().__init__(message)
        self.exit_code = exit_code


class RuntimeStatus(str, Enum):
    """Lifecycle state reported for a runtime."""

    RUNNING = "running"
    """The runtime is running and accepts work."""
    PAUSED = "paused"
    """The runtime is paused and can be resumed."""
    SHUTDOWN = "shutdown"
    """The runtime is shut down."""
    CREATING = "creating"
    """The runtime is being created."""
    DELETING = "deleting"
    """The runtime is being deleted."""
    ERROR = "error"
    """The runtime entered an error state."""
    CRASHED = "crashed"
    """The runtime process crashed."""
    SUSPENDED = "suspended"
    """The runtime is suspended and can wake on demand."""
    UNAVAILABLE = "unavailable"
    """The runtime is temporarily unavailable."""

    @classmethod
    def from_user(cls, value: str) -> "RuntimeStatus":
        """Parse a user-provided runtime status name."""
        try:
            return cls(value.lower())
        except ValueError as exc:
            raise ValueError(f"unknown runtime status: {value}") from exc


class CheckpointState(str, Enum):
    """Creation state reported for a checkpoint."""

    CREATING = "creating"
    """The checkpoint is still being created."""
    READY = "ready"
    """The checkpoint is ready to restore."""
    FAILED = "failed"
    """Checkpoint creation failed."""


class EgressMode(str, Enum):
    """Supported runtime egress policy modes."""

    DENYLIST = "denylist"
    """Allow outbound hosts except those explicitly denied."""
    ALLOWLIST = "allowlist"
    """Deny outbound hosts except those explicitly allowed."""

    @classmethod
    def from_user(cls, value: "EgressMode | str") -> "EgressMode":
        """Normalize a user-provided egress mode."""
        if isinstance(value, cls):
            return value
        return cls(str(value))


@dataclass(slots=True)
class IngressSpec:
    """Ingress protocol and runtime port mapping."""

    protocol: str
    """Ingress protocol, such as `tcp` or `http`."""
    runtime_port: int
    """Port exposed by the runtime."""

    def to_json(self) -> dict[str, Any]:
        """Serialize this ingress spec for an API request."""
        return {"protocol": self.protocol, "runtime_port": self.runtime_port}

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "IngressSpec":
        """Create an ingress spec from an API response payload."""
        return cls(
            protocol=str(data["protocol"]), runtime_port=int(data["runtime_port"])
        )


@dataclass(slots=True)
class EgressPolicy:
    """Network egress policy attached to a runtime."""

    mode: EgressMode | str = EgressMode.DENYLIST
    """Whether the policy uses an allowlist or denylist."""
    allowed_hosts: list[str] = field(default_factory=list)
    """Hosts explicitly allowed by the policy."""
    denied_hosts: list[str] = field(default_factory=list)
    """Hosts explicitly denied by the policy."""

    def __post_init__(self) -> None:
        self.mode = EgressMode.from_user(self.mode)

    def to_json(self) -> dict[str, Any]:
        """Serialize this egress policy for an API request."""
        return {
            "mode": self.mode.value,
            "allowed_hosts": list(self.allowed_hosts),
            "denied_hosts": list(self.denied_hosts),
        }

    @classmethod
    def from_json(cls, data: dict[str, Any] | None) -> "EgressPolicy":
        """Create an egress policy from an API response payload."""
        if not data:
            return cls()
        return cls(
            mode=EgressMode.from_user(data.get("mode", EgressMode.DENYLIST.value)),
            allowed_hosts=list(data.get("allowed_hosts", [])),
            denied_hosts=list(data.get("denied_hosts", [])),
        )


@dataclass(slots=True)
class RuntimeResourceRequests:
    """Requested runtime memory and CPU allocation."""

    memory_mib: int
    """Requested runtime memory in MiB."""
    vcpus: int
    """Requested virtual CPU count."""

    def to_json(self) -> dict[str, Any]:
        """Serialize these runtime resource requests for an API request."""
        return {"memory_mib": self.memory_mib, "vcpus": self.vcpus}

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "RuntimeResourceRequests":
        """Create runtime resource requests from an API response payload."""
        return cls(memory_mib=int(data["memory_mib"]), vcpus=int(data["vcpus"]))


@dataclass(slots=True)
class RuntimeResourceLimits:
    """Maximum runtime memory allocation."""

    memory_mib: int
    """Maximum runtime memory in MiB."""

    def to_json(self) -> dict[str, Any]:
        """Serialize these runtime resource limits for an API request."""
        return {"memory_mib": self.memory_mib}

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "RuntimeResourceLimits":
        """Create runtime resource limits from an API response payload."""
        return cls(memory_mib=int(data["memory_mib"]))


@dataclass(slots=True)
class RuntimeResources:
    """Effective runtime resource requests and limits."""

    requests: RuntimeResourceRequests
    """Requested runtime memory and CPU."""
    limits: RuntimeResourceLimits
    """Maximum runtime resources."""

    def to_json(self) -> dict[str, Any]:
        """Serialize this runtime resource configuration for an API request."""
        return {
            "requests": self.requests.to_json(),
            "limits": self.limits.to_json(),
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "RuntimeResources":
        """Create a runtime resource configuration from an API response payload."""
        return cls(
            requests=RuntimeResourceRequests.from_json(data["requests"]),
            limits=RuntimeResourceLimits.from_json(data["limits"]),
        )


@dataclass(slots=True)
class CreateRuntimeResourceRequests:
    """Resource requests accepted while creating a runtime."""

    memory_mib: int = 1024
    """Initial requested memory in MiB."""
    vcpus: int = 1
    """Initial requested virtual CPU count."""

    def to_json(self) -> dict[str, Any]:
        """Serialize resource requests used when creating a runtime."""
        return {"memory_mib": self.memory_mib, "vcpus": self.vcpus}

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "CreateRuntimeResourceRequests":
        """Create runtime-creation resource requests from an API payload."""
        return cls(
            memory_mib=int(data.get("memory_mib", 1024)),
            vcpus=int(data.get("vcpus", 1)),
        )


@dataclass(slots=True)
class CreateRuntimeResources:
    """Structured resource configuration used while creating a runtime."""

    requests: CreateRuntimeResourceRequests = field(
        default_factory=CreateRuntimeResourceRequests
    )
    """Resource requests for the new runtime."""
    limits: RuntimeResourceLimits | None = None
    """Resource limits for the new runtime."""

    def to_json(self) -> dict[str, Any]:
        """Serialize the resource configuration used to create a runtime."""
        data: dict[str, Any] = {"requests": self.requests.to_json()}
        if self.limits is not None:
            data["limits"] = self.limits.to_json()
        return data

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "CreateRuntimeResources":
        """Create a runtime-creation resource configuration from an API payload."""
        return cls(
            requests=CreateRuntimeResourceRequests.from_json(data.get("requests", {})),
            limits=RuntimeResourceLimits.from_json(data["limits"])
            if data.get("limits") is not None
            else None,
        )


@dataclass(slots=True)
class PatchRuntimeResourceRequests:
    """Resource requests accepted while updating a runtime."""

    memory_mib: int | None = None
    """Replacement requested memory in MiB."""

    def to_json(self) -> dict[str, Any]:
        """Serialize resource request changes for an API request."""
        data: dict[str, Any] = {}
        if self.memory_mib is not None:
            data["memory_mib"] = self.memory_mib
        return data

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "PatchRuntimeResourceRequests":
        """Create resource request changes from an API payload."""
        return cls(
            memory_mib=int(data["memory_mib"])
            if data.get("memory_mib") is not None
            else None
        )


@dataclass(slots=True)
class PatchRuntimeResources:
    """Structured resource configuration used while updating a runtime."""

    requests: PatchRuntimeResourceRequests | None = None
    """Updated runtime resource requests."""
    limits: RuntimeResourceLimits | None = None
    """Updated runtime resource limits."""

    def to_json(self) -> dict[str, Any]:
        """Serialize runtime resource changes for an API request."""
        data: dict[str, Any] = {}
        if self.requests is not None:
            data["requests"] = self.requests.to_json()
        if self.limits is not None:
            data["limits"] = self.limits.to_json()
        return data

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "PatchRuntimeResources":
        """Create runtime resource changes from an API payload."""
        return cls(
            requests=PatchRuntimeResourceRequests.from_json(data["requests"])
            if data.get("requests") is not None
            else None,
            limits=RuntimeResourceLimits.from_json(data["limits"])
            if data.get("limits") is not None
            else None,
        )


def _timeout_seconds(policy: Mapping[str, Any] | None) -> int:
    if not policy or policy["mode"] == "disabled":
        return 0
    return int(policy["after_seconds"])


def _deadline_from_json(value: str | None) -> datetime | None:
    if value is None:
        return None
    # Python 3.10 does not accept the RFC 3339 Z suffix in fromisoformat.
    deadline = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if deadline.tzinfo is None:
        deadline = deadline.replace(tzinfo=timezone.utc)
    return deadline


@dataclass(slots=True)
class RuntimeInfo:
    """Runtime metadata returned by the Runta API."""

    id: str
    """Runtime UUID."""
    display_name: str
    """Human-readable runtime name."""
    resources: RuntimeResources
    """Effective resource requests and limits."""
    ingress_specs: list[IngressSpec]
    """Ingress ports exposed by the runtime."""
    status: RuntimeStatus
    """Current runtime lifecycle state."""
    egress_policy: EgressPolicy = field(default_factory=EgressPolicy)
    """Current outbound network policy."""

    auto_shutdown_after_secs: int = 0
    """Running-session limit in seconds; zero means disabled."""
    auto_delete_after_secs: int = 0
    """Retention after confirmed shutdown in seconds; zero means disabled."""
    auto_shutdown_at: datetime | None = None
    """Current session deadline, with a timezone, when supplied by the server."""
    auto_delete_at: datetime | None = None
    """Deletion deadline, with a timezone, when supplied by the server."""
    tcp_allowlist: list[str] = field(default_factory=list)
    """Exact FQDN:port destinations allowed to receive raw TCP."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "RuntimeInfo":
        """Create runtime metadata from an API response payload."""
        return cls(
            id=str(data["id"]),
            display_name=str(data["display_name"]),
            resources=RuntimeResources.from_json(data["resources"]),
            ingress_specs=[
                IngressSpec.from_json(item) for item in data.get("ingress_specs", [])
            ],
            status=RuntimeStatus(str(data["status"])),
            egress_policy=EgressPolicy.from_json(data.get("egress_policy")),
            auto_shutdown_after_secs=_timeout_seconds(data.get("auto_shutdown_policy")),
            auto_delete_after_secs=_timeout_seconds(data.get("auto_delete_policy")),
            auto_shutdown_at=_deadline_from_json(data.get("auto_shutdown_at")),
            auto_delete_at=_deadline_from_json(data.get("auto_delete_at")),
            tcp_allowlist=list(data.get("tcp_allowlist", [])),
        )


@dataclass(slots=True)
class CheckpointInfo:
    """Checkpoint metadata returned by the Runta API."""

    id: str
    """Checkpoint UUID."""
    display_name: str
    """Human-readable checkpoint name."""
    resources: RuntimeResources
    """Resources captured by the checkpoint."""
    state: CheckpointState
    """Current checkpoint creation state."""
    kind: str | None = None
    """Checkpoint kind, such as full or cold; absent on older servers."""
    safe_error_code: str | None = None
    """Non-sensitive failure code, when supplied by the server."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "CheckpointInfo":
        """Create checkpoint metadata from an API response payload."""
        return cls(
            id=str(data["id"]),
            display_name=str(data["display_name"]),
            resources=RuntimeResources.from_json(data["resources"]),
            state=CheckpointState(str(data["state"])),
            kind=data.get("kind"),
            safe_error_code=data.get("safe_error_code"),
        )


@dataclass(slots=True)
class SecretInfo:
    """Stored tenant secret metadata."""

    id: str
    """Secret UUID."""
    display_name: str
    """Human-readable secret name."""
    cache_ttl_secs: int
    """How long injected values may be cached, in seconds."""
    value_preview: str | None = None
    """Redacted preview of the stored value, when available."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "SecretInfo":
        """Create tenant secret metadata from an API response payload."""
        return cls(
            id=str(data["id"]),
            display_name=str(data["display_name"]),
            cache_ttl_secs=int(data.get("cache_ttl_secs", 0)),
            value_preview=str(data["value_preview"])
            if data.get("value_preview") is not None
            else None,
        )


@dataclass(slots=True)
class CommandResult:
    """Buffered command result returned by runtime execution methods."""

    exit_code: int
    """Process exit code."""
    stdout: bytes
    """Captured standard output bytes."""
    stderr: bytes
    """Captured standard error bytes."""
    duration: float
    """Command duration in seconds."""
    stdout_truncated: bool = False
    """Whether standard output exceeded the configured limit."""
    stderr_truncated: bool = False
    """Whether standard error exceeded the configured limit."""

    @property
    def stdout_text(self) -> str:
        """Decode captured standard output as text."""
        return self.stdout.decode(errors="replace")

    @property
    def stderr_text(self) -> str:
        """Decode captured standard error as text."""
        return self.stderr.decode(errors="replace")


def _copy_egress_policy(policy: EgressPolicy) -> EgressPolicy:
    return EgressPolicy(
        mode=policy.mode,
        allowed_hosts=list(policy.allowed_hosts),
        denied_hosts=list(policy.denied_hosts),
    )


def _normalize_egress_policy(policy: EgressPolicy) -> EgressPolicy:
    def normalize_hosts(hosts: list[str]) -> list[str]:
        return sorted({host.strip().rstrip(".").lower() for host in hosts})

    return EgressPolicy(
        mode=policy.mode,
        allowed_hosts=normalize_hosts(policy.allowed_hosts),
        denied_hosts=normalize_hosts(policy.denied_hosts),
    )


from ._internal.async_http import _AsyncHttpClient  # noqa: E402
from ._internal.config import resolve_config  # noqa: E402
from ._internal.helpers import (  # noqa: E402
    ingress_json,
    status_query,
)
from ._internal.retry import (  # noqa: E402
    _full_jitter_delay,
    read_deadline as _read_deadline,
)
from ._internal.sync_http import _SyncHttpClient  # noqa: E402


class _SdkOwnedHandle:
    __slots__ = ()

    _owner_description = "SDK accessors"

    def __new__(cls, *_args: object, **_kwargs: object) -> Any:
        raise TypeError(
            f"{cls.__name__} handles are returned by {cls._owner_description}; "
            f"do not call {cls.__name__}(...) directly."
        )

    @classmethod
    def _from_owner(cls, owner: Any) -> Any:
        handle = object.__new__(cls)
        handle._init(owner)
        return handle


class RuntimeManager(_SdkOwnedHandle):
    """Creates, lists, and resolves runtimes for a synchronous client."""

    __slots__ = ("_client",)

    _owner_description = "Runta.runtimes"

    def _init(self, client: Runta) -> None:
        self._client = client

    def list(self, status: str | Sequence[str] | None = None) -> list[Runtime]:
        """List runtimes, optionally filtered by lifecycle state."""
        infos = self._client._http.list_runtimes(status_query(status))
        return [Runtime._from_info(self._client, info) for info in infos]

    def create(
        self,
        name: str | None = None,
        *,
        checkpoint_id: str | None = None,
        vcpus: int = 1,
        memory_mib: int = 1024,
        memory_max_mib: int | None = None,
        resources: CreateRuntimeResources | Mapping[str, object] | None = None,
        ingress_specs: Sequence[IngressSpec | Mapping[str, object]] | None = None,
        egress_policy: EgressPolicy | None = None,
        idle_suspend_after_secs: int | None = None,
        auto_shutdown_after_secs: int | None = None,
        auto_delete_after_secs: int | None = None,
        tcp_allowlist: Sequence[str] | None = None,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> Runtime:
        """Create a runtime and optionally wait until it is ready.

        Args:
            name: Optional display name for the runtime.
            checkpoint_id: Checkpoint UUID to restore into the new runtime.
            vcpus: Requested virtual CPU count for fresh creation when
                `resources` is not supplied.
            memory_mib: Requested memory in MiB for fresh creation when
                `resources` is not supplied.
            memory_max_mib: Optional maximum memory allocation for fresh creation.
            resources: Structured resource requests and limits. For cold checkpoint
                restores, supply this to override CPU and memory; omit it to retain
                the checkpoint's resources. Live checkpoints reject overrides.
            ingress_specs: Ports and protocols to expose from the runtime.
            egress_policy: Initial outbound network policy.
            idle_suspend_after_secs: Idle time before automatic suspension.
            auto_shutdown_after_secs: Running-session limit. None omits the policy;
                zero disables it; a positive integer enables it.
            auto_delete_after_secs: Retention after confirmed shutdown. None omits
                the policy; zero disables it; starting cancels pending deletion.
            tcp_allowlist: Exact FQDN:port destinations for raw TCP, at most 16.
                Empty denies raw TCP on fresh creation. When restoring a checkpoint,
                omission or an empty list inherits its snapshot configuration.
            wait: Wait until the runtime is ready before returning.
            timeout: Maximum number of seconds to wait for readiness.
            poll_interval: Initial full-jitter delay bound; doubles up to 10 seconds.

        Returns:
            The newly created runtime handle.

        Raises:
            ApiError: If the control plane rejects the create request.
            TimeoutError: If `wait` is true and the runtime is not ready in time.

        Examples:
            >>> runtime = client.runtimes.create(name="worker", memory_mib=2048)
            >>> runtime.status()
            <RuntimeStatus.RUNNING: 'running'>
        """
        info = self._client._http.create_runtime(
            name,
            checkpoint_id=checkpoint_id,
            vcpus=vcpus,
            memory_mib=memory_mib,
            memory_max_mib=memory_max_mib,
            resources=resources,
            ingress_specs=[ingress_json(item) for item in ingress_specs or []],
            egress_policy=egress_policy,
            idle_suspend_after_secs=idle_suspend_after_secs,
            auto_shutdown_after_secs=auto_shutdown_after_secs,
            auto_delete_after_secs=auto_delete_after_secs,
            tcp_allowlist=tcp_allowlist,
        )
        runtime = Runtime._from_info(self._client, info)
        if wait:
            runtime.wait_until_ready(timeout=timeout, poll_interval=poll_interval)
        return runtime

    def get(self, id: str) -> Runtime:
        """Resolve a runtime by UUID or display name."""
        try:
            return Runtime._from_info(self._client, self._client._http.get_runtime(id))
        except ApiError:
            for info in self._client._http.list_runtimes():
                if info.id == id or info.display_name == id:
                    return Runtime._from_info(self._client, info)
            raise


class AsyncRuntimeManager(_SdkOwnedHandle):
    """Creates, lists, and resolves runtimes asynchronously."""

    __slots__ = ("_client",)

    _owner_description = "AsyncRunta.runtimes"

    def _init(self, client: AsyncRunta) -> None:
        self._client = client

    async def list(
        self, status: str | Sequence[str] | None = None
    ) -> list[AsyncRuntime]:
        """List runtimes, optionally filtered by lifecycle state."""
        infos = await self._client._http.list_runtimes(status_query(status))
        return [AsyncRuntime._from_info(self._client, info) for info in infos]

    async def create(
        self,
        name: str | None = None,
        *,
        checkpoint_id: str | None = None,
        vcpus: int = 1,
        memory_mib: int = 1024,
        memory_max_mib: int | None = None,
        resources: CreateRuntimeResources | Mapping[str, object] | None = None,
        ingress_specs: Sequence[IngressSpec | Mapping[str, object]] | None = None,
        egress_policy: EgressPolicy | None = None,
        idle_suspend_after_secs: int | None = None,
        auto_shutdown_after_secs: int | None = None,
        auto_delete_after_secs: int | None = None,
        tcp_allowlist: Sequence[str] | None = None,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> AsyncRuntime:
        """Create a runtime and optionally wait until it is ready.

        Args:
            name: Optional display name for the runtime.
            checkpoint_id: Checkpoint UUID to restore into the new runtime.
            vcpus: Requested virtual CPU count for fresh creation when
                `resources` is not supplied.
            memory_mib: Requested memory in MiB for fresh creation when
                `resources` is not supplied.
            memory_max_mib: Optional maximum memory allocation for fresh creation.
            resources: Structured resource requests and limits. For cold checkpoint
                restores, supply this to override CPU and memory; omit it to retain
                the checkpoint's resources. Live checkpoints reject overrides.
            ingress_specs: Ports and protocols to expose from the runtime.
            egress_policy: Initial outbound network policy.
            idle_suspend_after_secs: Idle time before automatic suspension.
            auto_shutdown_after_secs: Running-session limit. None omits the policy;
                zero disables it; a positive integer enables it.
            auto_delete_after_secs: Retention after confirmed shutdown. None omits
                the policy; zero disables it; starting cancels pending deletion.
            tcp_allowlist: Exact FQDN:port destinations for raw TCP, at most 16.
                Empty denies raw TCP on fresh creation. When restoring a checkpoint,
                omission or an empty list inherits its snapshot configuration.
            wait: Wait until the runtime is ready before returning.
            timeout: Maximum number of seconds to wait for readiness.
            poll_interval: Initial full-jitter delay bound; doubles up to 10 seconds.

        Returns:
            The newly created asynchronous runtime handle.

        Raises:
            ApiError: If the control plane rejects the create request.
            TimeoutError: If `wait` is true and the runtime is not ready in time.

        Examples:
            >>> runtime = await client.runtimes.create(name="worker", memory_mib=2048)
            >>> await runtime.status()
            <RuntimeStatus.RUNNING: 'running'>
        """
        info = await self._client._http.create_runtime(
            name,
            checkpoint_id=checkpoint_id,
            vcpus=vcpus,
            memory_mib=memory_mib,
            memory_max_mib=memory_max_mib,
            resources=resources,
            ingress_specs=[ingress_json(item) for item in ingress_specs or []],
            egress_policy=egress_policy,
            idle_suspend_after_secs=idle_suspend_after_secs,
            auto_shutdown_after_secs=auto_shutdown_after_secs,
            auto_delete_after_secs=auto_delete_after_secs,
            tcp_allowlist=tcp_allowlist,
        )
        runtime = AsyncRuntime._from_info(self._client, info)
        if wait:
            await runtime.wait_until_ready(timeout=timeout, poll_interval=poll_interval)
        return runtime

    async def get(self, id: str) -> AsyncRuntime:
        """Resolve a runtime by UUID or display name."""
        try:
            return AsyncRuntime._from_info(
                self._client, await self._client._http.get_runtime(id)
            )
        except ApiError:
            for info in await self._client._http.list_runtimes():
                if info.id == id or info.display_name == id:
                    return AsyncRuntime._from_info(self._client, info)
            raise


class SecretManager(_SdkOwnedHandle):
    """Manages stored tenant secrets."""

    __slots__ = ("_client",)

    _owner_description = "Runta.secrets"

    def _init(self, client: Runta) -> None:
        self._client = client

    def set(self, name: str, val: str, *, cache_ttl_secs: int = 0) -> SecretInfo:
        """Create or replace a tenant secret.

        Args:
            name: Display name used to resolve the secret later.
            val: Secret value to store.
            cache_ttl_secs: Number of seconds runtime agents may cache the value.

        Returns:
            Metadata for the stored secret. The secret value is never returned.

        Examples:
            >>> secret = client.secrets.set("github-token", os.environ["GITHUB_TOKEN"])
            >>> secret.display_name
            'github-token'
        """
        return self._client._http.set_secret(name, val, cache_ttl_secs)

    def get(self, name: str) -> SecretInfo:
        """Resolve a tenant secret by UUID or display name."""
        try:
            return self._client._http.get_secret(name)
        except ApiError:
            for item in self.list():
                if item.id == name or item.display_name == name:
                    return item
            raise

    def list(self) -> list[SecretInfo]:
        """List tenant secrets."""
        return self._client._http.list_secrets()

    def delete(self, name: str) -> None:
        """Delete a tenant secret by UUID or display name."""
        secret = self.get(name)
        self._client._http.delete_secret(secret.id)


class AsyncSecretManager(_SdkOwnedHandle):
    """Manages stored tenant secrets asynchronously."""

    __slots__ = ("_client",)

    _owner_description = "AsyncRunta.secrets"

    def _init(self, client: AsyncRunta) -> None:
        self._client = client

    async def set(self, name: str, val: str, *, cache_ttl_secs: int = 0) -> SecretInfo:
        """Create or replace a tenant secret.

        Args:
            name: Display name used to resolve the secret later.
            val: Secret value to store.
            cache_ttl_secs: Number of seconds runtime agents may cache the value.

        Returns:
            Metadata for the stored secret. The secret value is never returned.

        Examples:
            >>> secret = await client.secrets.set(
            ...     "github-token", os.environ["GITHUB_TOKEN"]
            ... )
            >>> secret.display_name
            'github-token'
        """
        return await self._client._http.set_secret(name, val, cache_ttl_secs)

    async def get(self, name: str) -> SecretInfo:
        """Resolve a tenant secret by UUID or display name."""
        try:
            return await self._client._http.get_secret(name)
        except ApiError:
            for item in await self.list():
                if item.id == name or item.display_name == name:
                    return item
            raise

    async def list(self) -> list[SecretInfo]:
        """List tenant secrets."""
        return await self._client._http.list_secrets()

    async def delete(self, name: str) -> None:
        """Delete a tenant secret by UUID or display name."""
        secret = await self.get(name)
        await self._client._http.delete_secret(secret.id)


class CheckpointManager(_SdkOwnedHandle):
    """Lists, resolves, waits for, and deletes tenant checkpoints."""

    __slots__ = ("_client",)

    _owner_description = "Runta.checkpoints"

    def _init(self, client: Runta) -> None:
        self._client = client

    def list(self) -> list[CheckpointInfo]:
        """List user-created tenant checkpoints."""
        return self._client._http.list_checkpoints()

    def get(self, id: str) -> CheckpointInfo:
        """Resolve a checkpoint by UUID or display name."""
        try:
            return self._client._http.get_checkpoint(id)
        except ApiError:
            for item in self.list():
                if item.id == id or item.display_name == id:
                    return item
            raise

    def wait_until_ready(
        self,
        id: str,
        *,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> CheckpointInfo:
        """Wait until a checkpoint is ready or has failed."""
        deadline = time.monotonic() + timeout
        last_state: CheckpointState | None = None
        while time.monotonic() < deadline:
            try:
                with _read_deadline(deadline):
                    checkpoint = self.get(id)
            except (ApiError, TimeoutError):
                if time.monotonic() < deadline:
                    raise
                break
            if time.monotonic() >= deadline:
                break
            last_state = checkpoint.state
            if last_state == CheckpointState.READY:
                return checkpoint
            if last_state == CheckpointState.FAILED:
                raise RuntimeError(f"checkpoint {checkpoint.id} entered failed state")
            time.sleep(min(poll_interval, max(0.0, deadline - time.monotonic())))
        raise TimeoutError(
            f"checkpoint {id} did not become ready within {timeout}s"
            f" (last state: {last_state.value if last_state else 'unknown'})"
        )

    def delete(self, id: str) -> None:
        """Delete a checkpoint by UUID or display name."""
        checkpoint = self.get(id)
        self._client._http.delete_checkpoint(checkpoint.id)


class AsyncCheckpointManager(_SdkOwnedHandle):
    """Lists, resolves, waits for, and deletes checkpoints asynchronously."""

    __slots__ = ("_client",)

    _owner_description = "AsyncRunta.checkpoints"

    def _init(self, client: AsyncRunta) -> None:
        self._client = client

    async def list(self) -> list[CheckpointInfo]:
        """List user-created tenant checkpoints."""
        return await self._client._http.list_checkpoints()

    async def get(self, id: str) -> CheckpointInfo:
        """Resolve a checkpoint by UUID or display name."""
        try:
            return await self._client._http.get_checkpoint(id)
        except ApiError:
            for item in await self.list():
                if item.id == id or item.display_name == id:
                    return item
            raise

    async def wait_until_ready(
        self,
        id: str,
        *,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> CheckpointInfo:
        """Wait until a checkpoint is ready or has failed."""
        deadline = time.monotonic() + timeout
        last_state: CheckpointState | None = None
        while time.monotonic() < deadline:
            try:
                with _read_deadline(deadline):
                    checkpoint = await self.get(id)
            except (ApiError, TimeoutError):
                if time.monotonic() < deadline:
                    raise
                break
            if time.monotonic() >= deadline:
                break
            last_state = checkpoint.state
            if last_state == CheckpointState.READY:
                return checkpoint
            if last_state == CheckpointState.FAILED:
                raise RuntimeError(f"checkpoint {checkpoint.id} entered failed state")
            await asyncio.sleep(
                min(poll_interval, max(0.0, deadline - time.monotonic()))
            )
        raise TimeoutError(
            f"checkpoint {id} did not become ready within {timeout}s"
            f" (last state: {last_state.value if last_state else 'unknown'})"
        )

    async def delete(self, id: str) -> None:
        """Delete a checkpoint by UUID or display name."""
        checkpoint = await self.get(id)
        await self._client._http.delete_checkpoint(checkpoint.id)


class Runtime:
    """Controls lifecycle, commands, files, and networking for one runtime."""

    __slots__ = (
        "_cached_info",
        "_checkpoints",
        "_client",
        "_egress",
        "_files",
        "_id",
    )

    def __new__(cls, *_args: object, **_kwargs: object) -> Runtime:
        raise TypeError(
            "Runtime handles are returned by Runta.runtimes.create(), "
            "Runta.runtimes.get(), or Runta.runtimes.list(); do not call "
            "Runtime(...) directly."
        )

    @classmethod
    def _from_info(cls, client: Runta, info: RuntimeInfo) -> Runtime:
        runtime = object.__new__(cls)
        runtime._init(client, info)
        return runtime

    def _init(self, client: Runta, info: RuntimeInfo) -> None:
        self._client = client
        self._id = info.id
        self._cached_info = info
        self._egress: EgressManager = EgressManager._from_owner(self)
        self._files: FileManager = FileManager._from_owner(self)
        self._checkpoints: RuntimeCheckpointManager = (
            RuntimeCheckpointManager._from_owner(self)
        )

    @property
    def cached_info(self) -> RuntimeInfo:
        """Return the most recently fetched runtime metadata."""
        return self._cached_info

    @property
    def egress(self) -> EgressManager:
        """Return the egress policy manager for this runtime."""
        return self._egress

    @property
    def files(self) -> FileManager:
        """Return the file manager for this runtime."""
        return self._files

    @property
    def checkpoints(self) -> RuntimeCheckpointManager:
        """Return the checkpoint manager for this runtime."""
        return self._checkpoints

    @property
    def id(self) -> str:
        """Return the runtime UUID."""
        return self._id

    @property
    def name(self) -> str:
        """Return the runtime display name."""
        return self.cached_info.display_name

    def refresh_info(self) -> RuntimeInfo:
        """Refresh and return runtime metadata from the API."""
        self._cached_info = self._client._http.get_runtime(self.id)
        return self.cached_info

    def boot(
        self,
        *,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> None:
        """Boot the runtime and optionally wait until it is ready."""
        self._cached_info = self._client._http.update_runtime_status(self.id, "boot")
        if wait:
            self.wait_until_ready(timeout=timeout, poll_interval=poll_interval)

    def wait_until_ready(
        self,
        *,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> RuntimeInfo:
        """Wait until running with full jitter; double the delay bound up to 10s."""
        deadline = time.monotonic() + timeout
        delay = min(poll_interval, _RUNTIME_READINESS_MAX_POLL_INTERVAL)
        last_status: RuntimeStatus | None = None
        while time.monotonic() < deadline:
            try:
                with _read_deadline(deadline):
                    last_status = self.status()
            except (ApiError, TimeoutError):
                if time.monotonic() < deadline:
                    raise
                break
            if time.monotonic() >= deadline:
                break
            if last_status == RuntimeStatus.RUNNING:
                return self.cached_info
            if last_status in {
                RuntimeStatus.ERROR,
                RuntimeStatus.CRASHED,
                RuntimeStatus.DELETING,
            }:
                raise RuntimeError(
                    f"runtime {self.id} entered {last_status.value} state"
                )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            time.sleep(_full_jitter_delay(delay, remaining))
            delay = min(delay * 2, _RUNTIME_READINESS_MAX_POLL_INTERVAL)
        raise TimeoutError(
            f"runtime {self.id} did not become ready within {timeout}s"
            f" (last status: {last_status.value if last_status else 'unknown'})"
        )

    def pause(self) -> None:
        """Pause the runtime."""
        self._cached_info = self._client._http.update_runtime_status(self.id, "pause")

    def resume(
        self,
        *,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> None:
        """Resume the runtime and optionally wait until it is ready."""
        self._cached_info = self._client._http.update_runtime_status(self.id, "resume")
        if wait:
            self.wait_until_ready(timeout=timeout, poll_interval=poll_interval)

    def shutdown(self) -> None:
        """Shut down the runtime."""
        self._cached_info = self._client._http.update_runtime_status(
            self.id, "shutdown"
        )

    def delete(self) -> None:
        """Delete the runtime with idempotent retries in the HTTP client."""
        try:
            self._client._http.delete_runtime(self.id)
        except ApiError as error:
            if error.status_code != 404:
                raise

    def update_resources(
        self,
        resources: PatchRuntimeResources | Mapping[str, object],
    ) -> RuntimeInfo:
        """Update the runtime resource configuration."""
        self._cached_info = self._client._http.patch_runtime(
            self.id,
            resources=resources,
        )
        return self.cached_info

    def update_timeout_policies(
        self,
        *,
        auto_shutdown_after_secs: int | None = None,
        auto_delete_after_secs: int | None = None,
    ) -> RuntimeInfo:
        """Update automatic shutdown and deletion policies and refresh cached metadata.

        Args:
            auto_shutdown_after_secs: Running-session limit in seconds. None leaves
                unchanged; zero disables; 1 through 2147483647 enables.
            auto_delete_after_secs: Retention after confirmed shutdown in seconds.
                None leaves unchanged; zero disables; 1 through 2147483647 enables.

        Explicitly saving a policy resets only that policy's clock, even when its
        value is unchanged. Starting the runtime cancels pending deletion.
        """
        self._cached_info = self._client._http.patch_runtime(
            self.id,
            auto_shutdown_after_secs=auto_shutdown_after_secs,
            auto_delete_after_secs=auto_delete_after_secs,
        )
        return self.cached_info

    def resize_memory(self, new_memory_mib: int) -> RuntimeInfo:
        """Change the runtime memory limit in MiB."""
        return self.update_resources(
            PatchRuntimeResources(
                requests=PatchRuntimeResourceRequests(memory_mib=new_memory_mib),
                limits=RuntimeResourceLimits(memory_mib=new_memory_mib),
            )
        )

    def status(self) -> RuntimeStatus:
        """Fetch the current runtime lifecycle status."""
        self.refresh_info()
        return self.cached_info.status

    heartbeat = status
    """Alias for `status()`."""

    def exec(
        self,
        command: str | Sequence[str],
        timeout: float | None = None,
        env: Mapping[str, str] | None = None,
        stdin: bytes | str | None = None,
        cwd: str | None = None,
        max_output_bytes: int | None = None,
    ) -> CommandResult:
        """Run a command and return its buffered output.

        Args:
            command: Shell command or argument sequence to execute.
            timeout: Optional execution timeout in seconds.
            env: Environment variables added to the command.
            stdin: Bytes or text written to standard input.
            cwd: Working directory used for the command.
            max_output_bytes: Maximum buffered output size.

        Returns:
            The command exit code and buffered standard output and error.

        Raises:
            ApiError: If command execution cannot be started or completed.

        Examples:
            >>> result = runtime.exec("python --version")
            >>> print(result.stdout_text)
            Python 3.12.0
        """
        return self._exec(command, timeout, env, stdin, cwd, max_output_bytes)

    def exec_detached(self, command: str | Sequence[str], **kwargs: Any) -> Future:
        """Run a command in a background worker and return a future."""
        return self._client._executor.submit(self.exec, command, **kwargs)

    def restore(
        self, checkpoint_id: str, *, name: str | None = None, **options: Any
    ) -> Runtime:
        """Create a runtime from one of this runtime’s checkpoints."""
        return self._client.runtimes.create(
            name or self.name, checkpoint_id=checkpoint_id, **options
        )

    def _exec(
        self,
        command: str | Sequence[str],
        timeout: float | None,
        env: Mapping[str, str] | None,
        stdin: bytes | str | None,
        cwd: str | None,
        max_output_bytes: int | None,
    ) -> CommandResult:
        return _Execution._new(
            self,
            command,
            timeout=timeout,
            env=env,
            stdin=stdin,
            cwd=cwd,
            max_output_bytes=max_output_bytes,
        ).wait()

    def _exec_route_miss_can_retry(self) -> bool:
        try:
            self._cached_info = self._client._http.get_runtime(self.id)
        except ApiError:
            return False
        return self.cached_info.status in {
            RuntimeStatus.CREATING,
            RuntimeStatus.RUNNING,
        }


class AsyncRuntime:
    """Controls one runtime through asynchronous lifecycle and I/O operations."""

    __slots__ = (
        "_cached_info",
        "_checkpoints",
        "_client",
        "_egress",
        "_files",
        "_id",
    )

    def __new__(cls, *_args: object, **_kwargs: object) -> AsyncRuntime:
        raise TypeError(
            "AsyncRuntime handles are returned by AsyncRunta.runtimes.create(), "
            "AsyncRunta.runtimes.get(), or AsyncRunta.runtimes.list(); do not call "
            "AsyncRuntime(...) directly."
        )

    @classmethod
    def _from_info(cls, client: AsyncRunta, info: RuntimeInfo) -> AsyncRuntime:
        runtime = object.__new__(cls)
        runtime._init(client, info)
        return runtime

    def _init(self, client: AsyncRunta, info: RuntimeInfo) -> None:
        self._client = client
        self._id = info.id
        self._cached_info = info
        self._egress: AsyncEgressManager = AsyncEgressManager._from_owner(self)
        self._files: AsyncFileManager = AsyncFileManager._from_owner(self)
        self._checkpoints: AsyncRuntimeCheckpointManager = (
            AsyncRuntimeCheckpointManager._from_owner(self)
        )

    @property
    def cached_info(self) -> RuntimeInfo:
        """Return the most recently fetched runtime metadata."""
        return self._cached_info

    @property
    def egress(self) -> AsyncEgressManager:
        """Return the egress policy manager for this runtime."""
        return self._egress

    @property
    def files(self) -> AsyncFileManager:
        """Return the file manager for this runtime."""
        return self._files

    @property
    def checkpoints(self) -> AsyncRuntimeCheckpointManager:
        """Return the checkpoint manager for this runtime."""
        return self._checkpoints

    @property
    def id(self) -> str:
        """Return the runtime UUID."""
        return self._id

    @property
    def name(self) -> str:
        """Return the runtime display name."""
        return self.cached_info.display_name

    async def refresh_info(self) -> RuntimeInfo:
        """Refresh and return runtime metadata from the API."""
        self._cached_info = await self._client._http.get_runtime(self.id)
        return self.cached_info

    async def boot(
        self,
        *,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> None:
        """Boot the runtime and optionally wait until it is ready."""
        self._cached_info = await self._client._http.update_runtime_status(
            self.id, "boot"
        )
        if wait:
            await self.wait_until_ready(timeout=timeout, poll_interval=poll_interval)

    async def pause(self) -> None:
        """Pause the runtime."""
        self._cached_info = await self._client._http.update_runtime_status(
            self.id, "pause"
        )

    async def resume(
        self,
        *,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> None:
        """Resume the runtime and optionally wait until it is ready."""
        self._cached_info = await self._client._http.update_runtime_status(
            self.id, "resume"
        )
        if wait:
            await self.wait_until_ready(timeout=timeout, poll_interval=poll_interval)

    async def shutdown(self) -> None:
        """Shut down the runtime."""
        self._cached_info = await self._client._http.update_runtime_status(
            self.id, "shutdown"
        )

    async def delete(self) -> None:
        """Delete the runtime with idempotent retries in the HTTP client."""
        try:
            await self._client._http.delete_runtime(self.id)
        except ApiError as error:
            if error.status_code != 404:
                raise

    async def update_resources(
        self,
        resources: PatchRuntimeResources | Mapping[str, object],
    ) -> RuntimeInfo:
        """Update the runtime resource configuration."""
        self._cached_info = await self._client._http.patch_runtime(
            self.id,
            resources=resources,
        )
        return self.cached_info

    async def update_timeout_policies(
        self,
        *,
        auto_shutdown_after_secs: int | None = None,
        auto_delete_after_secs: int | None = None,
    ) -> RuntimeInfo:
        """Update automatic shutdown and deletion policies and refresh cached metadata.

        Args:
            auto_shutdown_after_secs: Running-session limit in seconds. None leaves
                unchanged; zero disables; 1 through 2147483647 enables.
            auto_delete_after_secs: Retention after confirmed shutdown in seconds.
                None leaves unchanged; zero disables; 1 through 2147483647 enables.

        Explicitly saving a policy resets only that policy's clock, even when its
        value is unchanged. Starting the runtime cancels pending deletion.
        """
        self._cached_info = await self._client._http.patch_runtime(
            self.id,
            auto_shutdown_after_secs=auto_shutdown_after_secs,
            auto_delete_after_secs=auto_delete_after_secs,
        )
        return self.cached_info

    async def resize_memory(self, new_memory_mib: int) -> RuntimeInfo:
        """Change the runtime memory limit in MiB."""
        return await self.update_resources(
            PatchRuntimeResources(
                requests=PatchRuntimeResourceRequests(memory_mib=new_memory_mib),
                limits=RuntimeResourceLimits(memory_mib=new_memory_mib),
            )
        )

    async def status(self) -> RuntimeStatus:
        """Fetch the current runtime lifecycle status."""
        await self.refresh_info()
        return self.cached_info.status

    heartbeat = status
    """Alias for `status()`."""

    async def wait_until_ready(
        self,
        *,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> RuntimeInfo:
        """Wait until running with full jitter; double the delay bound up to 10s."""
        deadline = time.monotonic() + timeout
        delay = min(poll_interval, _RUNTIME_READINESS_MAX_POLL_INTERVAL)
        last_status: RuntimeStatus | None = None
        while time.monotonic() < deadline:
            try:
                with _read_deadline(deadline):
                    last_status = await self.status()
            except (ApiError, TimeoutError):
                if time.monotonic() < deadline:
                    raise
                break
            if time.monotonic() >= deadline:
                break
            if last_status == RuntimeStatus.RUNNING:
                return self.cached_info
            if last_status in {
                RuntimeStatus.ERROR,
                RuntimeStatus.CRASHED,
                RuntimeStatus.DELETING,
            }:
                raise RuntimeError(
                    f"runtime {self.id} entered {last_status.value} state"
                )
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                break
            await asyncio.sleep(_full_jitter_delay(delay, remaining))
            delay = min(delay * 2, _RUNTIME_READINESS_MAX_POLL_INTERVAL)
        raise TimeoutError(
            f"runtime {self.id} did not become ready within {timeout}s"
            f" (last status: {last_status.value if last_status else 'unknown'})"
        )

    async def exec(
        self,
        command: str | Sequence[str],
        timeout: float | None = None,
        env: Mapping[str, str] | None = None,
        stdin: bytes | str | None = None,
        cwd: str | None = None,
        max_output_bytes: int | None = None,
    ) -> CommandResult:
        """Run a command and return its buffered output.

        Args:
            command: Shell command or argument sequence to execute.
            timeout: Optional execution timeout in seconds.
            env: Environment variables added to the command.
            stdin: Bytes or text written to standard input.
            cwd: Working directory used for the command.
            max_output_bytes: Maximum buffered output size.

        Returns:
            The command exit code and buffered standard output and error.

        Raises:
            ApiError: If command execution cannot be started or completed.

        Examples:
            >>> result = await runtime.exec("python --version")
            >>> print(result.stdout_text)
            Python 3.12.0
        """
        return await self._exec(command, timeout, env, stdin, cwd, max_output_bytes)

    def exec_detached(
        self,
        command: str | Sequence[str],
        timeout: float | None = None,
        env: Mapping[str, str] | None = None,
        stdin: bytes | str | None = None,
        cwd: str | None = None,
        max_output_bytes: int | None = None,
    ) -> asyncio.Task[CommandResult]:
        """Run a command in a background worker and return a future."""
        return asyncio.create_task(
            self._exec(command, timeout, env, stdin, cwd, max_output_bytes)
        )

    async def restore(
        self, checkpoint_id: str, *, name: str | None = None, **options: Any
    ) -> AsyncRuntime:
        """Create a runtime from one of this runtime’s checkpoints."""
        return await self._client.runtimes.create(
            name or self.name, checkpoint_id=checkpoint_id, **options
        )

    async def _exec(
        self,
        command: str | Sequence[str],
        timeout: float | None,
        env: Mapping[str, str] | None,
        stdin: bytes | str | None,
        cwd: str | None,
        max_output_bytes: int | None,
    ) -> CommandResult:
        return await _AsyncExecution._new(
            self,
            command,
            timeout=timeout,
            env=env,
            stdin=stdin,
            cwd=cwd,
            max_output_bytes=max_output_bytes,
        ).wait()

    async def _exec_route_miss_can_retry(self) -> bool:
        try:
            self._cached_info = await self._client._http.get_runtime(self.id)
        except ApiError:
            return False
        return self.cached_info.status in {
            RuntimeStatus.CREATING,
            RuntimeStatus.RUNNING,
        }


class EgressManager(_SdkOwnedHandle):
    """Reads and updates the network egress policy for a runtime."""

    __slots__ = ("_runtime",)

    _owner_description = "Runtime.egress"

    def _init(self, runtime: Runtime) -> None:
        self._runtime = runtime

    def set_policy(self, policy: EgressPolicy) -> RuntimeInfo:
        """Replace the complete egress policy and return refreshed metadata.

        Examples:
            >>> runtime.egress.set_policy(
            ...     EgressPolicy(
            ...         mode=EgressMode.ALLOWLIST,
            ...         allowed_hosts=["api.github.com"],
            ...     )
            ... )
            RuntimeInfo(...)
        """
        policy = _normalize_egress_policy(policy)
        self._runtime._cached_info = self._runtime._client._http.patch_runtime(
            self._runtime.id, egress_policy=policy
        )
        return self._runtime.cached_info

    def set_tcp_allowlist(self, hosts: Sequence[str]) -> RuntimeInfo:
        """Replace the complete raw TCP allowlist and refresh cached metadata.

        Args:
            hosts: At most 16 nonempty exact FQDN:port destinations. An empty list
                denies raw TCP. The server validates destinations and resolves
                each hostname to the permitted public IPv4 address and port.
        """
        self._runtime._cached_info = self._runtime._client._http.patch_runtime(
            self._runtime.id, tcp_allowlist=hosts
        )
        return self._runtime.cached_info

    def get_tcp_allowlist(self) -> list[str]:
        """Fetch the runtime's raw TCP allowlist and return an independent list."""
        self._runtime.refresh_info()
        return list(self._runtime.cached_info.tcp_allowlist)

    def get(self) -> EgressPolicy:
        """Return the cached egress policy."""
        self._runtime.refresh_info()
        return _copy_egress_policy(self._runtime.cached_info.egress_policy)


class AsyncEgressManager(_SdkOwnedHandle):
    """Reads and updates a runtime egress policy asynchronously."""

    __slots__ = ("_runtime",)

    _owner_description = "AsyncRuntime.egress"

    def _init(self, runtime: AsyncRuntime) -> None:
        self._runtime = runtime

    async def set_policy(self, policy: EgressPolicy) -> RuntimeInfo:
        """Replace the complete egress policy and return refreshed metadata.

        Examples:
            >>> await runtime.egress.set_policy(
            ...     EgressPolicy(
            ...         mode=EgressMode.ALLOWLIST,
            ...         allowed_hosts=["api.github.com"],
            ...     )
            ... )
            RuntimeInfo(...)
        """
        policy = _normalize_egress_policy(policy)
        self._runtime._cached_info = await self._runtime._client._http.patch_runtime(
            self._runtime.id, egress_policy=policy
        )
        return self._runtime.cached_info

    async def set_tcp_allowlist(self, hosts: Sequence[str]) -> RuntimeInfo:
        """Replace the complete raw TCP allowlist and refresh cached metadata.

        Args:
            hosts: At most 16 nonempty exact FQDN:port destinations. An empty list
                denies raw TCP. The server validates destinations and resolves
                each hostname to the permitted public IPv4 address and port.
        """
        self._runtime._cached_info = await self._runtime._client._http.patch_runtime(
            self._runtime.id, tcp_allowlist=hosts
        )
        return self._runtime.cached_info

    async def get_tcp_allowlist(self) -> list[str]:
        """Fetch the runtime's raw TCP allowlist and return an independent list."""
        await self._runtime.refresh_info()
        return list(self._runtime.cached_info.tcp_allowlist)

    async def get(self) -> EgressPolicy:
        """Return the cached egress policy."""
        await self._runtime.refresh_info()
        return _copy_egress_policy(self._runtime.cached_info.egress_policy)


class FileManager(_SdkOwnedHandle):
    """Reads, writes, uploads, and downloads files for a runtime."""

    __slots__ = ("_runtime",)

    _owner_description = "Runtime.files"

    def _init(self, runtime: Runtime) -> None:
        self._runtime = runtime

    def read(self, path: str, max_bytes: int | None = None) -> bytes:
        """Read a file from the runtime as bytes."""
        content = self._runtime._client._http.read_file(self._runtime.id, path)
        if max_bytes is not None:
            return content[:max_bytes]
        return content

    def write(self, path: str, content: bytes | str, executable: bool = False) -> None:
        """Write bytes or text to a runtime file.

        Args:
            path: Absolute destination path inside the runtime.
            content: Text or binary content to write.
            executable: Mark the resulting file executable.

        Examples:
            >>> runtime.files.write(
            ...     "/workspace/hello.sh", "#!/bin/sh\\necho hello\\n", executable=True
            ... )
            >>> runtime.exec(["/workspace/hello.sh"]).stdout_text
            'hello\\n'
        """
        self._runtime._client._http.write_file(self._runtime.id, path, content)
        if executable:
            result = self._runtime.exec(["chmod", "755", "--", path])
            if result.exit_code != 0:
                raise CommandError(result.stderr_text, exit_code=result.exit_code)

    def upload(self, src: str, dst: str) -> None:
        """Stream a local file or directory to the runtime.

        The transfer isn't limited by the REST request-body size. Files are
        written through a temporary sibling and atomically renamed. Directory
        uploads are extracted into a staging directory and committed only after
        the complete archive is received.

        Args:
            src: Local file or directory path.
            dst: Destination path inside the runtime. A trailing slash places a
                file beneath that directory using its local basename.

        Examples:
            >>> runtime.files.upload("./project", "/workspace/project")
            >>> runtime.files.upload("./model.bin", "/workspace/models/")
        """
        src_path = Path(src)
        self._runtime._client._http.upload_path(self._runtime.id, src_path, dst)

    def download(self, src: str, dst: str) -> None:
        """Stream a runtime file or directory to a staged local path.

        Args:
            src: Source file or directory inside the runtime.
            dst: Local destination. A trailing slash or existing directory
                places the source beneath it using the remote basename.

        Examples:
            >>> runtime.files.download("/workspace/dist", "./artifacts/")
        """
        dst_path = Path(dst)
        destination_is_directory = dst.endswith("/") or dst_path.is_dir()
        self._runtime._client._http.download_path(
            self._runtime.id,
            src,
            dst_path,
            destination_is_directory=destination_is_directory,
        )

    def download_dir_contents(
        self,
        src: str,
        dst: str,
        *,
        paths: Sequence[str] | None = None,
        filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    ) -> None:
        """Merge a runtime directory's contents into a local directory.

        Existing unrelated files are preserved and matching files overwritten.
        Source directory links are followed; nested links are preserved when
        supported. Safe data filtering is always enforced, including after a
        custom tarfile-style filter. Special files are rejected unless skipped
        by that callback. Permissions follow tarfile.data_filter semantics.

        This operation is not transactional: failures or cancellation can leave
        partially merged contents. A file/directory type conflict raises instead
        of deleting a directory. An empty source preserves existing contents.

        Args:
            src: Source directory inside the runtime.
            dst: Local directory, created if absent; no source name is appended.
            paths: Relative paths to transfer without directory recursion. None
                downloads everything; an empty sequence performs no operation.
                Selected symlinks are skipped; intermediate symlinks are rejected.
                Missing paths fail before merging.
            filter: Optional synchronous (TarInfo, destination) callback. Return
                None to skip a member. Async callbacks are not supported.

        Examples:
            >>> runtime.files.download_dir_contents("/workspace/dist", "./artifacts")
        """
        self._runtime._client._http.download_dir_contents(
            self._runtime.id,
            src,
            Path(dst),
            paths=paths,
            filter=filter,
        )


class AsyncFileManager(_SdkOwnedHandle):
    """Reads, writes, uploads, and downloads runtime files asynchronously."""

    __slots__ = ("_runtime",)

    _owner_description = "AsyncRuntime.files"

    def _init(self, runtime: AsyncRuntime) -> None:
        self._runtime = runtime

    async def read(self, path: str, max_bytes: int | None = None) -> bytes:
        """Read a file from the runtime as bytes."""
        content = await self._runtime._client._http.read_file(self._runtime.id, path)
        if max_bytes is not None:
            return content[:max_bytes]
        return content

    async def write(
        self, path: str, content: bytes | str, executable: bool = False
    ) -> None:
        """Write bytes or text to a runtime file.

        Args:
            path: Absolute destination path inside the runtime.
            content: Text or binary content to write.
            executable: Mark the resulting file executable.

        Examples:
            >>> await runtime.files.write(
            ...     "/workspace/hello.sh", "#!/bin/sh\\necho hello\\n", executable=True
            ... )
            >>> result = await runtime.exec(["/workspace/hello.sh"])
            >>> result.stdout_text
            'hello\\n'
        """
        await self._runtime._client._http.write_file(self._runtime.id, path, content)
        if executable:
            result = await self._runtime.exec(["chmod", "755", "--", path])
            if result.exit_code != 0:
                raise CommandError(result.stderr_text, exit_code=result.exit_code)

    async def upload(self, src: str, dst: str) -> None:
        """Asynchronously stream a local file or directory to the runtime.

        Args:
            src: Local file or directory path.
            dst: Destination path inside the runtime.

        Examples:
            >>> await runtime.files.upload("./project", "/workspace/project")
        """
        src_path = Path(src)
        await self._runtime._client._http.upload_path(self._runtime.id, src_path, dst)

    async def download(self, src: str, dst: str) -> None:
        """Asynchronously stream a runtime file or directory locally.

        Args:
            src: Source file or directory inside the runtime.
            dst: Local destination path.

        Examples:
            >>> await runtime.files.download("/workspace/dist", "./artifacts/")
        """
        dst_path = Path(dst)
        destination_is_directory = dst.endswith("/") or dst_path.is_dir()
        await self._runtime._client._http.download_path(
            self._runtime.id,
            src,
            dst_path,
            destination_is_directory=destination_is_directory,
        )

    async def download_dir_contents(
        self,
        src: str,
        dst: str,
        *,
        paths: Sequence[str] | None = None,
        filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    ) -> None:
        """Merge a runtime directory's contents into a local directory.

        Existing unrelated files are preserved and matching files overwritten.
        Source directory links are followed; nested links are preserved when
        supported. Safe data filtering is always enforced, including after a
        custom tarfile-style filter. Special files are rejected unless skipped
        by that callback. Permissions follow tarfile.data_filter semantics.

        This operation is not transactional: failures or cancellation can leave
        partially merged contents. A file/directory type conflict raises instead
        of deleting a directory. An empty source preserves existing contents.

        Args:
            src: Source directory inside the runtime.
            dst: Local directory, created if absent; no source name is appended.
            paths: Relative paths to transfer without directory recursion. None
                downloads everything; an empty sequence performs no operation.
                Selected symlinks are skipped; intermediate symlinks are rejected.
                Missing paths fail before merging.
            filter: Optional synchronous (TarInfo, destination) callback. Return
                None to skip a member. Async callbacks are not supported.

        Examples:
            >>> await runtime.files.download_dir_contents("/workspace/dist", "./artifacts")
        """
        await self._runtime._client._http.download_dir_contents(
            self._runtime.id,
            src,
            Path(dst),
            paths=paths,
            filter=filter,
        )


class RuntimeCheckpointManager(_SdkOwnedHandle):
    """Creates, lists, and deletes checkpoints for a runtime."""

    __slots__ = ("_runtime",)

    _owner_description = "Runtime.checkpoints"

    def _init(self, runtime: Runtime) -> None:
        self._runtime = runtime

    def create(
        self,
        kind: str = "full",
        name: str | None = None,
        *,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> CheckpointInfo:
        """Create a checkpoint from this runtime and optionally wait until ready.

        Args:
            kind: Checkpoint kind. The public API currently accepts ``"full"``.
            name: Optional display name for the checkpoint.
            wait: Wait for the checkpoint to become ready before returning.
            timeout: Maximum number of seconds to wait for readiness.
            poll_interval: Seconds between readiness checks.

        Returns:
            Metadata for the created checkpoint.

        Examples:
            >>> checkpoint = runtime.checkpoints.create(name="worker-ready")
            >>> restored = client.runtimes.create(checkpoint_id=checkpoint.id)
        """
        if kind != "full":
            raise ValueError("runta-api currently supports only full checkpoints")
        checkpoint_name = name or f"{self._runtime.name}-{uuid.uuid4().hex[:8]}"
        checkpoint = self._runtime._client._http.create_checkpoint(
            self._runtime.id, checkpoint_name, kind
        )
        if wait:
            checkpoint = self._runtime._client.checkpoints.wait_until_ready(
                checkpoint.id, timeout=timeout, poll_interval=poll_interval
            )
        return checkpoint

    def list(self) -> list[CheckpointInfo]:
        """List checkpoints created from this runtime."""
        checkpoints = self._runtime._client.checkpoints.list()
        return [
            item
            for item in checkpoints
            if item.display_name.startswith(f"{self._runtime.name}-")
        ]

    def delete(self, id: str) -> None:
        """Delete one of this runtime’s checkpoints."""
        self._runtime._client.checkpoints.delete(id)


class AsyncRuntimeCheckpointManager(_SdkOwnedHandle):
    """Creates, lists, and deletes runtime checkpoints asynchronously."""

    __slots__ = ("_runtime",)

    _owner_description = "AsyncRuntime.checkpoints"

    def _init(self, runtime: AsyncRuntime) -> None:
        self._runtime = runtime

    async def create(
        self,
        kind: str = "full",
        name: str | None = None,
        *,
        wait: bool = True,
        timeout: float = 240.0,
        poll_interval: float = 0.5,
    ) -> CheckpointInfo:
        """Create a checkpoint from this runtime and optionally wait until ready.

        Args:
            kind: Checkpoint kind. The public API currently accepts ``"full"``.
            name: Optional display name for the checkpoint.
            wait: Wait for the checkpoint to become ready before returning.
            timeout: Maximum number of seconds to wait for readiness.
            poll_interval: Seconds between readiness checks.

        Returns:
            Metadata for the created checkpoint.

        Examples:
            >>> checkpoint = await runtime.checkpoints.create(name="worker-ready")
            >>> restored = await client.runtimes.create(checkpoint_id=checkpoint.id)
        """
        if kind != "full":
            raise ValueError("runta-api currently supports only full checkpoints")
        checkpoint_name = name or f"{self._runtime.name}-{uuid.uuid4().hex[:8]}"
        checkpoint = await self._runtime._client._http.create_checkpoint(
            self._runtime.id, checkpoint_name, kind
        )
        if wait:
            checkpoint = await self._runtime._client.checkpoints.wait_until_ready(
                checkpoint.id, timeout=timeout, poll_interval=poll_interval
            )
        return checkpoint

    async def list(self) -> list[CheckpointInfo]:
        """List checkpoints created from this runtime."""
        checkpoints = await self._runtime._client.checkpoints.list()
        return [
            item
            for item in checkpoints
            if item.display_name.startswith(f"{self._runtime.name}-")
        ]

    async def delete(self, id: str) -> None:
        """Delete one of this runtime’s checkpoints."""
        await self._runtime._client.checkpoints.delete(id)


class Runta:
    """Main synchronous client for runtimes, secrets, and checkpoints.

    ``connection_pool_maxsize`` limits concurrent HTTP connections (default 250).
    Pass ``None`` for unlimited connections. This does not limit WebSockets.
    """

    __slots__ = (
        "_checkpoints",
        "_closed",
        "_executor",
        "_http",
        "_runtimes",
        "_secrets",
    )

    def __init__(
        self,
        *,
        token: str | None = None,
        endpoint: str | None = None,
        config_path: str | Path | None = None,
        timeout: float = 30.0,
        retry_max_attempts: int = 16,
        connection_pool_maxsize: int | None = 250,
    ) -> None:
        if type(retry_max_attempts) is not int or not 1 <= retry_max_attempts <= 16:
            raise ValueError("retry_max_attempts must be between 1 and 16")
        endpoint, token = resolve_config(
            endpoint=endpoint, token=token, config_path=config_path
        )
        self._http = _SyncHttpClient(
            endpoint,
            token,
            timeout=timeout,
            retry_max_attempts=retry_max_attempts,
            connection_pool_maxsize=connection_pool_maxsize,
        )
        self._executor = ThreadPoolExecutor(thread_name_prefix="runta-sdk")
        self._closed = False
        self._runtimes: RuntimeManager = RuntimeManager._from_owner(self)
        self._secrets: SecretManager = SecretManager._from_owner(self)
        self._checkpoints: CheckpointManager = CheckpointManager._from_owner(self)

    @property
    def runtimes(self) -> RuntimeManager:
        """Return the runtime manager."""
        return self._runtimes

    @property
    def secrets(self) -> SecretManager:
        """Return the tenant secret manager."""
        return self._secrets

    @property
    def checkpoints(self) -> CheckpointManager:
        """Return the tenant checkpoint manager."""
        return self._checkpoints

    def __enter__(self) -> Runta:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Release client resources."""
        if self._closed:
            return
        self._closed = True
        self._executor.shutdown(wait=True)
        self._http.close()

    def health(self) -> bool:
        """Return whether the Runta API is reachable."""
        return self._http.health()


class AsyncRunta:
    """Main asynchronous client for runtimes, secrets, and checkpoints.

    ``connection_pool_maxsize`` limits concurrent HTTP connections (default 250).
    Pass ``None`` for unlimited connections. This does not limit WebSockets.
    ``timeout`` bounds each complete REST request, including pool waiting and
    response reading. Use and close the client in the same event loop.
    ``file_io_workers`` bounds the dedicated download file pool; ``None`` uses
    min(32, available CPUs + 4). Downloads already started retain the pool until
    their file operations and cleanup finish, even after client close.
    """

    __slots__ = (
        "_checkpoints",
        "_http",
        "_runtimes",
        "_secrets",
    )

    def __init__(
        self,
        *,
        token: str | None = None,
        endpoint: str | None = None,
        config_path: str | Path | None = None,
        timeout: float = 30.0,
        retry_max_attempts: int = 16,
        connection_pool_maxsize: int | None = 250,
        file_io_workers: int | None = None,
    ) -> None:
        if type(retry_max_attempts) is not int or not 1 <= retry_max_attempts <= 16:
            raise ValueError("retry_max_attempts must be between 1 and 16")
        endpoint, token = resolve_config(
            endpoint=endpoint, token=token, config_path=config_path
        )
        self._http = _AsyncHttpClient(
            endpoint,
            token,
            timeout=timeout,
            retry_max_attempts=retry_max_attempts,
            connection_pool_maxsize=connection_pool_maxsize,
            file_io_workers=file_io_workers,
        )
        self._runtimes: AsyncRuntimeManager = AsyncRuntimeManager._from_owner(self)
        self._secrets: AsyncSecretManager = AsyncSecretManager._from_owner(self)
        self._checkpoints: AsyncCheckpointManager = AsyncCheckpointManager._from_owner(
            self
        )

    @property
    def runtimes(self) -> AsyncRuntimeManager:
        """Return the runtime manager."""
        return self._runtimes

    @property
    def secrets(self) -> AsyncSecretManager:
        """Return the tenant secret manager."""
        return self._secrets

    @property
    def checkpoints(self) -> AsyncCheckpointManager:
        """Return the tenant checkpoint manager."""
        return self._checkpoints

    async def __aenter__(self) -> AsyncRunta:
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.close()

    async def close(self) -> None:
        """Release client resources."""
        await self._http.close()

    async def health(self) -> bool:
        """Return whether the Runta API is reachable."""
        return await self._http.health()


from ._internal.execution import (  # noqa: E402
    AsyncExecution as _AsyncExecution,
    Execution as _Execution,
    ExecutionError,
)

ExecutionError.__module__ = __name__


__all__ = [
    "ApiError",
    "AsyncCheckpointManager",
    "AsyncEgressManager",
    "AsyncFileManager",
    "AsyncRuntime",
    "AsyncRuntimeCheckpointManager",
    "AsyncRuntimeManager",
    "AsyncRunta",
    "AsyncSecretManager",
    "CheckpointInfo",
    "CheckpointManager",
    "CheckpointState",
    "CommandError",
    "CommandResult",
    "ConfigError",
    "CreateRuntimeResourceRequests",
    "CreateRuntimeResources",
    "EgressManager",
    "EgressMode",
    "EgressPolicy",
    "ExecutionError",
    "FileManager",
    "IngressSpec",
    "PatchRuntimeResourceRequests",
    "PatchRuntimeResources",
    "Runta",
    "RuntaError",
    "Runtime",
    "RuntimeCheckpointManager",
    "RuntimeInfo",
    "RuntimeManager",
    "RuntimeResourceLimits",
    "RuntimeResourceRequests",
    "RuntimeResources",
    "RuntimeStatus",
    "SecretInfo",
    "SecretManager",
]
