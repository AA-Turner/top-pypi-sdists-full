import re
from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, field_validator

from arraylake.types import RedactedReprModel


class ServiceType(StrEnum):
    dap = "dap2"
    edr = "edr"
    wms = "wms"
    tiles = "tiles"
    zarr = "zarr"
    openeo = "openeo"
    sql = "sql"


class ServiceStatus(StrEnum):
    """Where a compute service actually is, as the API reports it.

    Read off the ComputeService CR's status.phase, which the controller owns. The first five
    describe a service that is meant to be running. The last four describe one that is deliberately
    not: two because someone asked for that, and two because the controller took it down.
    """

    available = "available"
    progressing = "progressing"
    unknown = "unknown"
    error = "error"
    # Scaled to zero at its own floor. Still reachable, but the next request pays a cold start.
    sleeping = "sleeping"
    stopped = "stopped"
    suspended = "suspended"
    quota_exceeded = "quota_exceeded"
    # Taken down because the org's account standing is suspended, not because of anything the
    # service or its owner asked for. Distinct from `suspended`, which is the customer's own stop.
    org_suspended = "org_suspended"


class LogLevel(StrEnum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


# Identity of the per-protocol ComputeService CRDs. Shared source of truth so the
# server (which writes the CRs) and the compute-controller (which watches them)
# can never drift on the kind names.
COMPUTE_CRD_GROUP = "compute.earthmover.io"
COMPUTE_CRD_VERSION = "v1alpha1"

CRD_KIND: dict[ServiceType, str] = {
    ServiceType.dap: "Dap2Service",
    ServiceType.edr: "EdrService",
    ServiceType.wms: "WmsService",
    ServiceType.tiles: "TilesService",
    ServiceType.zarr: "ZarrService",
    ServiceType.openeo: "OpeneoService",
    ServiceType.sql: "SqlService",
}


def crd_plural(service_type: ServiceType) -> str:
    return f"{CRD_KIND[service_type].lower()}s"


class ServiceConfig(BaseModel):
    service_type: ServiceType
    org: str

    # NOTE: This is necessary to have our unauthenticated, public-facing demos.
    is_public: bool

    # Optional deployment name (defaults to protocol name if not provided)
    # Used for uniqueness validation and K8s resource naming
    deployment_name: str | None = None

    # Optional Booth image tag
    service_version: str | None = None

    # Optional scaling parameters
    min_replicas: int | None = 1
    max_replicas: int | None = 24

    # Optional Booth store cache duration (in seconds). If unset, the server picks the value.
    store_cache_ttl: int | None = None

    # Optional Booth store cache max number of datasets. If unset, the server picks the value.
    store_cache_size: int | None = None

    # Optional cache max-age for cache control headers of the service responses (in seconds)
    # If not set, the default is 0, which means functionally no caching, but requests are revalidated.
    cache_max_age: int | None = 0

    # Optional control over icechunk chunk cache size in bytes. Override for services whose
    # single-request working set (e.g. all shards touched by an EDR query) exceeds the default,
    # otherwise chunks are evicted and re-fetched from object storage on every request.
    # If unset, the server sizes it from the pod's memory limit.
    icechunk_cache_chunk_bytes: int | None = None

    # Optional control over the number of chunk refs icechunk cache
    # If unset, the server sizes it from the pod's memory limit.
    icechunk_cache_chunk_ref_count: int | None = None

    # Optional zarr concurrency configuration, the number of concurrent reads zarr will use fulfilling requests
    # If unset, the server picks the value.
    zarr_concurrency: int | None = None

    # Optional zarr codec pipeline batch size, the number of chunks zarr encodes/decodes per
    # asyncio task. Zarr's own default of 1 spawns a task per inner chunk when decoding
    # sharded arrays, which is significantly slower. If unset, the server picks the value.
    zarr_codec_pipeline_batch_size: int | None = None

    # Optional zarr threading configuration, the max number of worker threads zarr uses for codec
    # encode/decode. If unset, the server derives it from the pod's CPU limit (rounded, minimum 1),
    # since zarr's own default counts the node's cores rather than the container's.
    zarr_max_workers: int | None = None

    # Optional log level for the service
    log_level: LogLevel | None = LogLevel.info

    # Optionally force-enable Dask (threaded scheduler, 2GB cache) for protocols
    # other than DAP2. DAP2 always uses Dask regardless of this setting.
    use_dask: bool = False

    tiles_num_threads: int | None = None
    tiles_num_concurrent_data_loads: int | None = None
    tiles_max_renderable_size: int | None = None

    sku_code: str | None = None

    # Unset means the per-protocol default, which default_spot() decides.
    spot: bool | None = None

    cpu_request: str | None = None
    cpu_limit: str | None = None
    memory_request: str | None = None
    memory_limit: str | None = None

    @field_validator("deployment_name")
    @classmethod
    def validate_deployment_name(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if len(v) > 16:
            raise ValueError("deployment_name must be at most 16 characters")
        if not re.match(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$|^[a-z0-9]$", v):
            raise ValueError("deployment_name must be lowercase alphanumeric with dashes, cannot start or end with dash")
        return v

    def __str__(self) -> str:
        as_str = f"{self.service_type.value}://{self.org}"
        if self.deployment_name:
            as_str += f"/{self.deployment_name}"
        return as_str


class DeploymentInfo(BaseModel):
    """Compute deployment information."""

    name: str
    url: str
    created: datetime
    config: ServiceConfig
    status: ServiceStatus
    # Pods serving right now. A service that scales to zero sits at 0 while still being available,
    # so this is what separates "ready to answer" from "the next request has to start it".
    ready_replicas: int = 0


class LoadResults(BaseModel):
    succeeded: list[str]
    failed: list[str]


class ComputeConfig(RedactedReprModel):
    service_uri: str
    domain: str
    env: str
    container_repository: str
    kube_config: dict
    legacy_domain: str | None = None
    openmeter_api_key: str | None = None

    __redacted_repr_fields__ = frozenset({"kube_config", "openmeter_api_key"})


class LogMessage(BaseModel):
    time: str
    message: str

    def __str__(self) -> str:
        return f"{self.time} | {self.message}\n"

    @classmethod
    def from_log_line(cls, log: str) -> "LogMessage":
        """Parse a log line into a LogMessage object.

        Example log line:
        # "2025-03-29T19:30:15.505397124Z stderr F INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)"

        The log line is split into a timestamp, stream, completeness, and message. For now we ignore the stream
        and completeness.
        """
        time, _stream, _completeness, *message = log.split(" ")
        return cls(time=time, message=" ".join(message))
