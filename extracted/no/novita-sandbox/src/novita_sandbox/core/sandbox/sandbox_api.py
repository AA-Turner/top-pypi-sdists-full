import math

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union, cast

from typing_extensions import NotRequired, Unpack

from novita_sandbox.core import ConnectionConfig
from novita_sandbox.core.api.client.models import (
    ListedSandbox,
    SandboxDetail,
    SandboxLifecycle as ClientSandboxLifecycle,
    SandboxNetworkConfig as ClientSandboxNetworkConfig,
    SandboxState,
)
from novita_sandbox.core.api.client.types import Unset
from novita_sandbox.core.connection_config import ApiParams
from novita_sandbox.core.sandbox.mcp import McpServer as BaseMcpServer


class GitHubMcpServerConfig(TypedDict):
    """
    Configuration for a GitHub-based MCP server.
    """

    run_cmd: str
    """
    Command to run the MCP server. Must start a stdio-compatible server.
    """
    install_cmd: NotRequired[str]
    """
    Command to install dependencies for the MCP server. Working directory is the root of the github repository.
    """
    envs: NotRequired[Dict[str, str]]
    """
    Environment variables to set in the MCP process.
    """


# Extended MCP server configuration that includes base servers
# and allows dynamic GitHub-based MCP servers with custom run and install commands.
# For GitHub servers, use keys in the format "github/owner/repo"
GitHubMcpServer = Dict[str, Union[GitHubMcpServerConfig, Any]]

# Union type that combines base MCP servers with GitHub-based servers
McpServer = Union[BaseMcpServer, GitHubMcpServer]


class SandboxResourceTargets(TypedDict, total=False):
    """Absolute resource totals for a sandbox, not increments.

    Memory and disk values are user-facing GiB and converted to the MiB values
    the API expects. A changed memory or disk total must be a whole number of
    GiB on the server, but fractional GiB values that are exact MiB multiples
    can be used to match a template's non-integral size.
    """

    cpu: int
    """Total virtual CPUs. Must be 1 or an even number."""
    memory_gib: float
    """Total memory in GiB."""
    disk_gib: float
    """Total disk size in GiB."""


class SandboxResizeItem(TypedDict, total=False):
    """Outcome of one resource in a resize request."""

    status: str
    """One of ``applied``, ``skipped``, ``failed`` or ``unknown``."""
    requested: float
    """Requested total: cores for cpu, GiB for memory and disk."""
    previous: float
    """Total before the call: cores for cpu, GiB for memory and disk."""
    current: float
    """Total after the call: cores for cpu, GiB for memory and disk."""
    unit: Literal["cores", "GiB"]
    """Unit of requested, previous and current."""
    code: int
    """HTTP status this resource would have returned on its own."""
    reason: str
    """Reason code when the resource was not applied."""
    message: str
    """Human-readable reason when the resource was not applied."""


class SandboxResizeResult(TypedDict, total=False):
    """Per-resource resize outcome; only requested resources are present."""

    cpu: SandboxResizeItem
    memory: SandboxResizeItem
    disk: SandboxResizeItem


_MIB_PER_GIB = 1024

_RESOURCE_FIELDS = {
    "cpu": "vcpu",
    "memory_gib": "memory_mb",
    "disk_gib": "disk_size_mb",
}


def _gib_to_mib(value: Union[int, float], name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"resource target {name} must be a positive number")
    if not math.isfinite(value) or value <= 0:
        raise ValueError(f"resource target {name} must be a positive number")
    mib = value * _MIB_PER_GIB
    if isinstance(mib, float):
        if not mib.is_integer():
            raise ValueError(
                f"resource target {name} must be an exact number of MiB; "
                f"use a multiple of 1/{_MIB_PER_GIB} GiB"
            )
    return int(mib)


def reject_unknown_resize_kwargs(opts: Mapping[str, Any]) -> None:
    """Reject keyword arguments that ``get_api_params`` would silently drop."""
    unexpected = sorted(set(opts) - set(ApiParams.__annotations__))
    if unexpected:
        raise TypeError(
            "Sandbox.resize() got unexpected keyword argument(s): "
            + ", ".join(unexpected)
            + ". Resource totals are set with cpu, memory_gib and disk_gib."
        )


def resource_targets_to_api(resources: SandboxResourceTargets) -> Dict[str, int]:
    """Validate public GiB resource totals and return the MiB request body."""
    if not isinstance(resources, Mapping):
        raise ValueError(
            "resources must be a mapping of cpu, memory_gib and disk_gib "
            "to absolute totals"
        )
    unknown = set(resources) - set(_RESOURCE_FIELDS)
    if unknown:
        raise ValueError(f"unsupported resource fields: {', '.join(sorted(unknown))}")

    body: Dict[str, int] = {}
    for key, value in resources.items():
        if key == "cpu":
            if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
                raise ValueError("resource target cpu must be a positive whole number")
            body["vcpu"] = value
        else:
            body[_RESOURCE_FIELDS[key]] = _gib_to_mib(value, key)
    if not body:
        raise ValueError("at least one of cpu, memory_gib or disk_gib is required")
    return body


def resize_result_from_api(data: Dict[str, Any]) -> SandboxResizeResult:
    """Map the MiB values returned by the API to the GiB values users see."""
    result: Dict[str, Any] = {}
    if data.get("cpu") is not None:
        result["cpu"] = {**data["cpu"], "unit": "cores"}
    for key in ("memory", "disk"):
        item = data.get(key)
        if item is None:
            continue
        result[key] = {
            **item,
            "requested": item.get("requested", 0) / _MIB_PER_GIB,
            "previous": item.get("previous", 0) / _MIB_PER_GIB,
            "current": item.get("current", 0) / _MIB_PER_GIB,
            "unit": "GiB",
        }
    return cast(SandboxResizeResult, result)


class SandboxNetworkOpts(TypedDict):
    """
    Sandbox network configuration options.
    """

    allow_out: NotRequired[List[str]]
    """
    Allow outbound traffic from the sandbox to the specified addresses.
    If `allow_out` is not specified, all outbound traffic is allowed.

    Examples:
    - To allow traffic to specific addresses: `["1.1.1.1", "8.8.8.0/24"]`
    """

    deny_out: NotRequired[List[str]]
    """
    Deny outbound traffic from the sandbox to the specified addresses.

    Examples:
    - To deny traffic to specific addresses: `["1.1.1.1", "8.8.8.0/24"]`
    """

    allow_public_traffic: NotRequired[bool]
    """
    Controls whether sandbox URLs should be publicly accessible or require authentication.
    Defaults to True.
    """

    mask_request_host: NotRequired[str]
    """
    Allows specifying a custom host mask for all sandbox requests.
    Supports ${PORT} variable. Defaults to "${PORT}-sandboxid.us-phx-1.sandbox.novita.ai".

    Examples:
    - Custom subdomain: `"${PORT}-myapp.example.com"`
    """


class SandboxLifecycle(TypedDict):
    """
    Sandbox lifecycle configuration; defines post-timeout behavior and auto-resume settings.
    Defaults to `on_timeout="kill"` and `auto_resume=False`.
    """

    on_timeout: Literal["pause", "kill"]
    """
    What should happen to the sandbox when timeout is reached. `"kill"` means the sandbox will be terminated, while `"pause"` means the sandbox will be paused and can be resumed later. Defaults to `"kill"`.
    """

    auto_resume: NotRequired[bool]
    """
    Whether activity should cause the sandbox to resume when paused. Defaults to `False`.
    Can be `True` only when `on_timeout` is `pause`.
    """


def legacy_create_network_config(
    network: Optional[SandboxNetworkOpts],
) -> Optional[Dict[str, bool]]:
    """Serialize the network option accepted by legacy create."""
    if network is None:
        return None
    unsupported = sorted(set(network) - {"allow_public_traffic"})
    if unsupported:
        from novita_sandbox.core.exceptions import SandboxException

        raise SandboxException(
            "Sandbox.create network only supports allow_public_traffic on legacy "
            f"domains; unsupported options: {', '.join(unsupported)}"
        )
    if "allow_public_traffic" not in network:
        return {}
    return {"allowPublicTraffic": bool(network["allow_public_traffic"])}


class SandboxInfoLifecycle(TypedDict):
    """
    Sandbox lifecycle configuration returned by sandbox info.
    """

    on_timeout: Literal["pause", "kill"]
    """
    What should happen to the sandbox when timeout is reached.
    """

    auto_resume: bool
    """
    Whether activity should cause the sandbox to resume when paused.
    """


def get_auto_resume_enabled(lifecycle: Optional[SandboxLifecycle]) -> Optional[bool]:
    if lifecycle is None or lifecycle.get("on_timeout") != "pause":
        return None

    return lifecycle.get("auto_resume", False)


def from_client_network_config(
    network: Union[Unset, ClientSandboxNetworkConfig],
) -> Optional[SandboxNetworkOpts]:
    if isinstance(network, Unset):
        return None

    result: SandboxNetworkOpts = {}

    if not isinstance(network.allow_out, Unset):
        result["allow_out"] = list(network.allow_out)
    if not isinstance(network.deny_out, Unset):
        result["deny_out"] = list(network.deny_out)
    if not isinstance(network.allow_public_traffic, Unset):
        result["allow_public_traffic"] = network.allow_public_traffic
    if not isinstance(network.mask_request_host, Unset):
        result["mask_request_host"] = network.mask_request_host

    return result


def from_client_lifecycle(
    lifecycle: Union[Unset, ClientSandboxLifecycle],
) -> Optional[SandboxInfoLifecycle]:
    if isinstance(lifecycle, Unset):
        return None

    result: SandboxInfoLifecycle = {
        "on_timeout": cast(Literal["pause", "kill"], lifecycle.on_timeout),
        "auto_resume": lifecycle.auto_resume,
    }

    return result


@dataclass
class SandboxInfo:
    """Information about a sandbox."""

    sandbox_id: str
    """Sandbox ID."""
    sandbox_domain: Optional[str]
    """Domain where the sandbox is hosted."""
    template_id: str
    """Template ID."""
    name: Optional[str]
    """Template name."""
    metadata: Dict[str, str]
    """Saved sandbox metadata."""
    started_at: datetime
    """Sandbox start time."""
    end_at: datetime
    """Sandbox expiration date."""
    state: SandboxState
    """Sandbox state."""
    cpu_count: int
    """Sandbox CPU count."""
    memory_mb: int
    """Sandbox Memory size in MiB."""
    envd_version: str
    """Envd version."""
    _envd_access_token: Optional[str]
    """Envd access token."""
    disk_size_mb: Optional[int] = None
    """Sandbox disk size in MiB, when the server returns it."""
    allow_internet_access: Optional[bool] = None
    """Whether internet access was explicitly enabled or disabled for the sandbox."""
    network: Optional[SandboxNetworkOpts] = None
    """Sandbox network configuration."""
    lifecycle: Optional[SandboxInfoLifecycle] = None
    """Sandbox lifecycle configuration."""
    volume_mounts: List[Dict[str, str]] = field(default_factory=list)
    """Volume mounts for the sandbox."""

    @classmethod
    def _from_sandbox_data(
        cls,
        sandbox: Union[ListedSandbox, SandboxDetail],
        envd_access_token: Optional[str] = None,
        sandbox_domain: Optional[str] = None,
        allow_internet_access: Optional[bool] = None,
        network: Optional[SandboxNetworkOpts] = None,
        lifecycle: Optional[SandboxInfoLifecycle] = None,
    ):
        return cls(
            sandbox_domain=sandbox_domain,
            sandbox_id=sandbox.sandbox_id,
            template_id=sandbox.template_id,
            name=(sandbox.alias if isinstance(sandbox.alias, str) else None),
            metadata=cast(
                Dict[str, str],
                sandbox.metadata if isinstance(sandbox.metadata, dict) else {},
            ),
            started_at=sandbox.started_at,
            end_at=sandbox.end_at,
            state=sandbox.state,
            cpu_count=sandbox.cpu_count,
            memory_mb=sandbox.memory_mb,
            disk_size_mb=(
                sandbox.disk_size_mb if isinstance(sandbox.disk_size_mb, int) else None
            ),
            envd_version=sandbox.envd_version,
            volume_mounts=[
                {"name": vm.name, "path": vm.path} for vm in sandbox.volume_mounts
            ]
            if not isinstance(sandbox.volume_mounts, Unset)
            else [],
            _envd_access_token=envd_access_token,
            allow_internet_access=allow_internet_access,
            network=network,
            lifecycle=lifecycle,
        )

    @classmethod
    def _from_listed_sandbox(cls, listed_sandbox: ListedSandbox):
        return cls._from_sandbox_data(listed_sandbox)

    @classmethod
    def _from_sandbox_detail(cls, sandbox_detail: SandboxDetail):
        return cls._from_sandbox_data(
            sandbox_detail,
            (
                sandbox_detail.envd_access_token
                if isinstance(sandbox_detail.envd_access_token, str)
                else None
            ),
            sandbox_domain=(
                sandbox_detail.domain
                if isinstance(sandbox_detail.domain, str)
                else None
            ),
            allow_internet_access=(
                sandbox_detail.allow_internet_access
                if isinstance(sandbox_detail.allow_internet_access, bool)
                else None
            ),
            network=from_client_network_config(sandbox_detail.network),
            lifecycle=from_client_lifecycle(sandbox_detail.lifecycle),
        )


@dataclass
class SandboxQuery:
    """Query parameters for listing sandboxes."""

    metadata: Optional[dict[str, str]] = None
    """Filter sandboxes by metadata."""

    state: Optional[list[SandboxState]] = None
    """Filter sandboxes by state."""


@dataclass
class SandboxMetrics:
    """Sandbox metrics."""

    cpu_count: int
    """Number of CPUs."""
    cpu_used_pct: float
    """CPU usage percentage."""
    disk_total: int
    """Total disk space in bytes."""
    disk_used: int
    """Disk used in bytes."""
    mem_total: int
    """Total memory in bytes."""
    mem_used: int
    """Memory used in bytes."""
    timestamp: datetime
    """Timestamp of the metric entry."""

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SandboxMetrics":
        timestamp = data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return cls(
            cpu_count=data.get("cpuCount", 0),
            cpu_used_pct=data.get("cpuUsedPct", 0),
            disk_total=data.get("diskTotal", -1),
            disk_used=data.get("diskUsed", -1),
            mem_total=data.get("memTotal", 0),
            mem_used=data.get("memUsed", 0),
            timestamp=timestamp or datetime.fromtimestamp(0),
        )


@dataclass
class SnapshotInfo:
    """Information about a snapshot."""

    snapshot_id: str
    """Snapshot identifier — template ID with tag, or namespaced name with tag (e.g. my-snapshot:latest). Can be used with Sandbox.create() to create a new sandbox from this snapshot."""


@dataclass
class SandboxQuotaLimit:
    """Sandbox quota limits."""

    concurrent_instances: int
    """Maximum number of concurrently running sandbox instances."""
    concurrent_vcpu: int
    """Maximum total VCPU cores in use."""
    concurrent_ram_mb: int
    """Maximum total memory in MB."""
    max_length_hours: int
    """Maximum sandbox lifetime in hours."""
    disk_mb: int
    """Per-sandbox disk space in MB."""
    max_vcpu: int
    """Per-sandbox VCPU core limit (effective after template build)."""
    max_ram_mb: int
    """Per-sandbox memory limit in MB (effective after template build)."""


@dataclass
class SandboxQuotaUsage:
    """Current sandbox quota usage."""

    concurrent_instances: int
    """Currently running sandbox instances."""
    concurrent_vcpu: int
    """Currently used VCPU cores."""
    concurrent_ram_mb: int
    """Currently used memory in MB."""


@dataclass
class SandboxQuota:
    """Sandbox quota information."""

    limit: SandboxQuotaLimit
    """Quota upper limits."""
    usage: SandboxQuotaUsage
    """Current resource usage."""


@dataclass
class SandboxEventItem:
    """A single sandbox event."""

    event_id: str
    """Event unique ID."""
    record_at: int
    """Event record time, Unix seconds."""
    template_id: str
    """Template ID used by the sandbox."""
    template_name: str
    """Template name used by the sandbox."""
    sandbox_id: str
    """Sandbox ID (short suffix stripped)."""
    event_name: str
    """Event type, e.g. create, pause, resume, connect, timeout, delete."""
    state: str
    """Operation status."""
    error_msg: str
    """Error message if any."""
    status_code: int
    """HTTP status code of the operation."""


@dataclass
class SandboxEventsResult:
    """Sandbox events query result."""

    items: List[SandboxEventItem]
    """List of events."""
    total: int
    """Total matching events (unaffected by pagination)."""
    has_more: bool
    """Whether more pages are available."""


class PaginatorBase:
    def __init__(
        self,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        self._config = ConnectionConfig(**opts)
        self.limit = limit
        self._has_next = True
        self._next_token = next_token

    @property
    def has_next(self) -> bool:
        """
        Returns True if there are more items to fetch.
        """
        return self._has_next

    @property
    def next_token(self) -> Optional[str]:
        """
        Returns the next token to use for pagination.
        """
        return self._next_token


class SnapshotPaginatorBase(PaginatorBase):
    def __init__(
        self,
        sandbox_id: Optional[str] = None,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        super().__init__(limit=limit, next_token=next_token, **opts)
        self.sandbox_id = sandbox_id


class SandboxPaginatorBase(PaginatorBase):
    def __init__(
        self,
        query: Optional[SandboxQuery] = None,
        limit: Optional[int] = None,
        next_token: Optional[str] = None,
        **opts: Unpack[ApiParams],
    ):
        super().__init__(limit=limit, next_token=next_token, **opts)
        self.query = query
