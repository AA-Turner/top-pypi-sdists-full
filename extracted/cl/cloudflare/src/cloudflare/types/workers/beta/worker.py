# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = [
    "Worker",
    "Observability",
    "ObservabilityIssues",
    "ObservabilityLogs",
    "ObservabilityTraces",
    "References",
    "ReferencesDispatchNamespaceOutbound",
    "ReferencesDomain",
    "ReferencesDurableObject",
    "ReferencesQueue",
    "ReferencesWorker",
    "Subdomain",
    "TailConsumer",
    "PreviewsBaseConfig",
    "PreviewsBaseConfigCacheOptions",
    "PreviewsBaseConfigEnv",
    "PreviewsBaseConfigLimits",
    "PreviewsBaseConfigObservability",
    "PreviewsBaseConfigObservabilityIssues",
    "PreviewsBaseConfigObservabilityLogs",
    "PreviewsBaseConfigObservabilityTraces",
    "PreviewsBaseConfigPlacement",
    "PreviewsBaseConfigPlacementMode",
    "PreviewsBaseConfigPlacementRegion",
    "PreviewsBaseConfigPlacementHostname",
    "PreviewsBaseConfigPlacementHost",
    "PreviewsBaseConfigPlacementUnionMember4",
    "PreviewsBaseConfigPlacementUnionMember5",
    "PreviewsBaseConfigPlacementUnionMember6",
    "PreviewsBaseConfigPlacementUnionMember7",
    "PreviewsBaseConfigPlacementUnionMember7Target",
    "PreviewsBaseConfigPlacementUnionMember7TargetRegion",
    "PreviewsBaseConfigPlacementUnionMember7TargetHostname",
    "PreviewsBaseConfigPlacementUnionMember7TargetHost",
    "PreviewsBaseConfigTailConsumer",
]


class ObservabilityIssues(BaseModel):
    """Real-time Issues settings for the Worker."""

    enabled: Optional[bool] = None
    """Whether real-time Issues are enabled for the Worker."""


class ObservabilityLogs(BaseModel):
    """Log settings for the Worker."""

    destinations: Optional[List[str]] = None
    """A list of destinations where logs will be exported to."""

    enabled: Optional[bool] = None
    """Whether logs are enabled for the Worker."""

    head_sampling_rate: Optional[float] = None
    """The sampling rate for logs. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    invocation_logs: Optional[bool] = None
    """
    Whether
    [invocation logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/#invocation-logs)
    are enabled for the Worker.
    """

    persist: Optional[bool] = None
    """Whether log persistence is enabled for the Worker."""


class ObservabilityTraces(BaseModel):
    """Trace settings for the Worker."""

    destinations: Optional[List[str]] = None
    """A list of destinations where traces will be exported to."""

    enabled: Optional[bool] = None
    """Whether traces are enabled for the Worker."""

    head_sampling_rate: Optional[float] = None
    """The sampling rate for traces. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    persist: Optional[bool] = None
    """Whether trace persistence is enabled for the Worker."""

    propagation_policy: Optional[Literal["authenticated", "accept"]] = None
    """
    Controls how inbound trace context (traceparent/tracestate) headers on incoming
    requests are handled. "authenticated" honors inbound trace context only when
    accompanied by a valid trace auth token. "accept" unconditionally accepts
    inbound trace context. Requires the trace propagation feature to be enabled.
    Returns null when the trace propagation feature is not enabled for the account.
    """


class Observability(BaseModel):
    """Observability settings for the Worker."""

    enabled: Optional[bool] = None
    """Whether observability is enabled for the Worker."""

    head_sampling_rate: Optional[float] = None
    """The sampling rate for observability. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    issues: Optional[ObservabilityIssues] = None
    """Real-time Issues settings for the Worker."""

    logs: Optional[ObservabilityLogs] = None
    """Log settings for the Worker."""

    redact_query_string: Optional[bool] = None
    """Whether query strings are removed from request URLs in logs and traces."""

    traces: Optional[ObservabilityTraces] = None
    """Trace settings for the Worker."""


class ReferencesDispatchNamespaceOutbound(BaseModel):
    namespace_id: str
    """ID of the dispatch namespace."""

    namespace_name: str
    """Name of the dispatch namespace."""

    worker_id: str
    """ID of the Worker using the dispatch namespace."""

    worker_name: str
    """Name of the Worker using the dispatch namespace."""


class ReferencesDomain(BaseModel):
    id: str
    """ID of the custom domain."""

    certificate_id: str
    """ID of the TLS certificate issued for the custom domain."""

    hostname: str
    """Full hostname of the custom domain, including the zone name."""

    zone_id: str
    """ID of the zone."""

    zone_name: str
    """Name of the zone."""


class ReferencesDurableObject(BaseModel):
    namespace_id: str
    """ID of the Durable Object namespace being used."""

    namespace_name: str
    """Name of the Durable Object namespace being used."""

    worker_id: str
    """ID of the Worker using the Durable Object implementation."""

    worker_name: str
    """Name of the Worker using the Durable Object implementation."""


class ReferencesQueue(BaseModel):
    queue_consumer_id: str
    """ID of the queue consumer configuration."""

    queue_id: str
    """ID of the queue."""

    queue_name: str
    """Name of the queue."""


class ReferencesWorker(BaseModel):
    id: str
    """ID of the referencing Worker."""

    name: str
    """Name of the referencing Worker."""


class References(BaseModel):
    """Other resources that reference the Worker and depend on it existing."""

    dispatch_namespace_outbounds: List[ReferencesDispatchNamespaceOutbound]
    """
    Other Workers that reference the Worker as an outbound for a dispatch namespace.
    """

    domains: List[ReferencesDomain]
    """Custom domains connected to the Worker."""

    durable_objects: List[ReferencesDurableObject]
    """Other Workers that reference Durable Object classes implemented by the Worker."""

    queues: List[ReferencesQueue]
    """Queues that send messages to the Worker."""

    workers: List[ReferencesWorker]
    """
    Other Workers that reference the Worker using
    [service bindings](https://developers.cloudflare.com/workers/runtime-apis/bindings/service-bindings/).
    """


class Subdomain(BaseModel):
    """Subdomain settings for the Worker."""

    enabled: Optional[bool] = None
    """Whether the \\**.workers.dev subdomain is enabled for the Worker."""

    preview_url_suffix: Optional[str] = None
    """
    Prepend a version or preview prefix to this host suffix to form the
    \\**.workers.dev
    [preview URL](https://developers.cloudflare.com/workers/configuration/previews/)
    the Worker would serve on once previews are enabled, e.g.
    `https://<prefix>-my-worker.my-subdomain.workers.dev`. Present whenever the
    account owns a workers.dev subdomain, regardless of whether `previews_enabled`
    is true, so presence does not imply preview URLs are currently live. Absent only
    when the account owns no workers.dev subdomain.
    """

    previews_enabled: Optional[bool] = None
    """
    Whether
    [preview URLs](https://developers.cloudflare.com/workers/configuration/previews/)
    are enabled for the Worker.
    """

    url: Optional[str] = None
    """
    The address the Worker would serve on once its \\**.workers.dev subdomain is
    enabled. Present whenever the account owns a workers.dev subdomain, regardless
    of whether `enabled` is true, so presence does not imply the Worker is currently
    live at this URL. Absent only when the account owns no workers.dev subdomain.
    """


class TailConsumer(BaseModel):
    name: str
    """Name of the consumer Worker."""


class PreviewsBaseConfigCacheOptions(BaseModel):
    """Cache options used when creating new Previews."""

    enabled: bool
    """Whether caching is enabled for this Worker."""

    cross_version_cache: Optional[bool] = None
    """Whether cached responses are shared across Worker version uploads.

    This is independent of `enabled`. It can stay true while caching is off, so the
    preference survives turning caching off and back on.
    """


class PreviewsBaseConfigEnv(BaseModel):
    """A single entry in the `env` map.

    An entry holds the same payload
    as an entry of `bindings` without the `name` property, because
    the map key supplies the name. See `binding_item` for the payload
    of each binding kind.
    """

    type: str
    """The kind of resource that the binding provides."""

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]


class PreviewsBaseConfigLimits(BaseModel):
    """Resource limits enforced at runtime for newly created Previews."""

    cpu_ms: Optional[int] = None
    """The amount of CPU time this Worker can use in milliseconds."""

    subrequests: Optional[int] = None
    """The number of subrequests this Worker can make per request."""


class PreviewsBaseConfigObservabilityIssues(BaseModel):
    """Real-time Issues settings for the Worker."""

    enabled: Optional[bool] = None
    """Whether real-time Issues are enabled for the Worker."""


class PreviewsBaseConfigObservabilityLogs(BaseModel):
    """Log settings for the Worker."""

    destinations: Optional[List[str]] = None
    """A list of destinations where logs will be exported to."""

    enabled: Optional[bool] = None
    """Whether logs are enabled for the Worker."""

    head_sampling_rate: Optional[float] = None
    """The sampling rate for logs. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    invocation_logs: Optional[bool] = None
    """
    Whether
    [invocation logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/#invocation-logs)
    are enabled for the Worker.
    """

    persist: Optional[bool] = None
    """Whether log persistence is enabled for the Worker."""


class PreviewsBaseConfigObservabilityTraces(BaseModel):
    """Trace settings for the Worker."""

    destinations: Optional[List[str]] = None
    """A list of destinations where traces will be exported to."""

    enabled: Optional[bool] = None
    """Whether traces are enabled for the Worker."""

    head_sampling_rate: Optional[float] = None
    """The sampling rate for traces. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    persist: Optional[bool] = None
    """Whether trace persistence is enabled for the Worker."""

    propagation_policy: Optional[Literal["authenticated", "accept"]] = None
    """
    Controls how inbound trace context (traceparent/tracestate) headers on incoming
    requests are handled. "authenticated" honors inbound trace context only when
    accompanied by a valid trace auth token. "accept" unconditionally accepts
    inbound trace context. Requires the trace propagation feature to be enabled.
    Returns null when the trace propagation feature is not enabled for the account.
    """


class PreviewsBaseConfigObservability(BaseModel):
    """Observability settings used when creating new Previews."""

    enabled: Optional[bool] = None
    """Whether observability is enabled for the Worker."""

    head_sampling_rate: Optional[float] = None
    """The sampling rate for observability. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    issues: Optional[PreviewsBaseConfigObservabilityIssues] = None
    """Real-time Issues settings for the Worker."""

    logs: Optional[PreviewsBaseConfigObservabilityLogs] = None
    """Log settings for the Worker."""

    redact_query_string: Optional[bool] = None
    """Whether query strings are removed from request URLs in logs and traces."""

    traces: Optional[PreviewsBaseConfigObservabilityTraces] = None
    """Trace settings for the Worker."""


class PreviewsBaseConfigPlacementMode(BaseModel):
    mode: Literal["smart"]
    """
    Enables
    [Smart Placement](https://developers.cloudflare.com/workers/configuration/smart-placement).
    """


class PreviewsBaseConfigPlacementRegion(BaseModel):
    region: str
    """Cloud region for targeted placement in format 'provider:region'."""


class PreviewsBaseConfigPlacementHostname(BaseModel):
    hostname: str
    """HTTP hostname for targeted placement."""


class PreviewsBaseConfigPlacementHost(BaseModel):
    host: str
    """TCP host and port for targeted placement."""


class PreviewsBaseConfigPlacementUnionMember4(BaseModel):
    mode: Literal["targeted"]
    """Targeted placement mode."""

    region: str
    """Cloud region for targeted placement in format 'provider:region'."""


class PreviewsBaseConfigPlacementUnionMember5(BaseModel):
    hostname: str
    """HTTP hostname for targeted placement."""

    mode: Literal["targeted"]
    """Targeted placement mode."""


class PreviewsBaseConfigPlacementUnionMember6(BaseModel):
    host: str
    """TCP host and port for targeted placement."""

    mode: Literal["targeted"]
    """Targeted placement mode."""


class PreviewsBaseConfigPlacementUnionMember7TargetRegion(BaseModel):
    region: str
    """Cloud region in format 'provider:region'."""


class PreviewsBaseConfigPlacementUnionMember7TargetHostname(BaseModel):
    hostname: str
    """HTTP hostname for targeted placement."""


class PreviewsBaseConfigPlacementUnionMember7TargetHost(BaseModel):
    host: str
    """TCP host:port for targeted placement."""


PreviewsBaseConfigPlacementUnionMember7Target: TypeAlias = Union[
    PreviewsBaseConfigPlacementUnionMember7TargetRegion,
    PreviewsBaseConfigPlacementUnionMember7TargetHostname,
    PreviewsBaseConfigPlacementUnionMember7TargetHost,
]


class PreviewsBaseConfigPlacementUnionMember7(BaseModel):
    mode: Literal["targeted"]
    """Targeted placement mode."""

    target: List[PreviewsBaseConfigPlacementUnionMember7Target]
    """Array of placement targets (currently limited to single target)."""


PreviewsBaseConfigPlacement: TypeAlias = Union[
    PreviewsBaseConfigPlacementMode,
    PreviewsBaseConfigPlacementRegion,
    PreviewsBaseConfigPlacementHostname,
    PreviewsBaseConfigPlacementHost,
    PreviewsBaseConfigPlacementUnionMember4,
    PreviewsBaseConfigPlacementUnionMember5,
    PreviewsBaseConfigPlacementUnionMember6,
    PreviewsBaseConfigPlacementUnionMember7,
]


class PreviewsBaseConfigTailConsumer(BaseModel):
    name: str
    """Name of the consumer Worker."""


class PreviewsBaseConfig(BaseModel):
    """Template configuration used when creating new Previews for this Worker."""

    cache_options: Optional[PreviewsBaseConfigCacheOptions] = None
    """Cache options used when creating new Previews."""

    env: Optional[Dict[str, PreviewsBaseConfigEnv]] = None
    """Bindings used when creating new Previews, keyed by binding name."""

    limits: Optional[PreviewsBaseConfigLimits] = None
    """Resource limits enforced at runtime for newly created Previews."""

    logpush: Optional[bool] = None
    """Whether logpush is enabled when creating new Previews."""

    observability: Optional[PreviewsBaseConfigObservability] = None
    """Observability settings used when creating new Previews."""

    placement: Optional[PreviewsBaseConfigPlacement] = None
    """Placement configuration used when creating new Previews."""

    tail_consumers: Optional[List[PreviewsBaseConfigTailConsumer]] = None
    """Other Workers that should consume logs from newly created Previews."""


class Worker(BaseModel):
    id: str
    """Immutable ID of the Worker."""

    created_on: datetime
    """When the Worker was created."""

    logpush: bool
    """Whether logpush is enabled for the Worker."""

    name: str
    """Name of the Worker."""

    observability: Observability
    """Observability settings for the Worker."""

    references: References
    """Other resources that reference the Worker and depend on it existing."""

    subdomain: Subdomain
    """Subdomain settings for the Worker."""

    tags: List[str]
    """Tags associated with the Worker."""

    tail_consumers: List[TailConsumer]
    """Other Workers that should consume logs from the Worker."""

    updated_on: datetime
    """When the Worker was most recently updated."""

    deployed_on: Optional[datetime] = None
    """When the Worker's most recent deployment was created.

    `null` if the Worker has never been deployed.
    """

    previews_base_config: Optional[PreviewsBaseConfig] = None
    """Template configuration used when creating new Previews for this Worker."""
