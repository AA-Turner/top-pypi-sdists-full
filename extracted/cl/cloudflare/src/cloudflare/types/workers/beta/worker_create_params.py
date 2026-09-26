# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from ...._types import SequenceNotStr

__all__ = [
    "WorkerCreateParams",
    "Observability",
    "ObservabilityIssues",
    "ObservabilityLogs",
    "ObservabilityTraces",
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
    "Subdomain",
    "TailConsumer",
]


class WorkerCreateParams(TypedDict, total=False):
    account_id: Required[str]
    """Identifier."""

    name: Required[str]
    """Name of the Worker."""

    logpush: bool
    """Whether logpush is enabled for the Worker."""

    observability: Observability
    """Observability settings for the Worker."""

    previews_base_config: PreviewsBaseConfig
    """Template configuration used when creating new Previews for this Worker."""

    subdomain: Subdomain
    """Subdomain settings for the Worker."""

    tags: SequenceNotStr[str]
    """Tags associated with the Worker."""

    tail_consumers: Iterable[TailConsumer]
    """Other Workers that should consume logs from the Worker."""


class ObservabilityIssues(TypedDict, total=False):
    """Real-time Issues settings for the Worker."""

    enabled: bool
    """Whether real-time Issues are enabled for the Worker."""


class ObservabilityLogs(TypedDict, total=False):
    """Log settings for the Worker."""

    destinations: SequenceNotStr[str]
    """A list of destinations where logs will be exported to."""

    enabled: bool
    """Whether logs are enabled for the Worker."""

    head_sampling_rate: float
    """The sampling rate for logs. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    invocation_logs: bool
    """
    Whether
    [invocation logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/#invocation-logs)
    are enabled for the Worker.
    """

    persist: bool
    """Whether log persistence is enabled for the Worker."""


class ObservabilityTraces(TypedDict, total=False):
    """Trace settings for the Worker."""

    destinations: SequenceNotStr[str]
    """A list of destinations where traces will be exported to."""

    enabled: bool
    """Whether traces are enabled for the Worker."""

    head_sampling_rate: float
    """The sampling rate for traces. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    persist: bool
    """Whether trace persistence is enabled for the Worker."""

    propagation_policy: Optional[Literal["authenticated", "accept"]]
    """
    Controls how inbound trace context (traceparent/tracestate) headers on incoming
    requests are handled. "authenticated" honors inbound trace context only when
    accompanied by a valid trace auth token. "accept" unconditionally accepts
    inbound trace context. Requires the trace propagation feature to be enabled.
    Returns null when the trace propagation feature is not enabled for the account.
    """


class Observability(TypedDict, total=False):
    """Observability settings for the Worker."""

    enabled: bool
    """Whether observability is enabled for the Worker."""

    head_sampling_rate: float
    """The sampling rate for observability. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    issues: Optional[ObservabilityIssues]
    """Real-time Issues settings for the Worker."""

    logs: ObservabilityLogs
    """Log settings for the Worker."""

    redact_query_string: bool
    """Whether query strings are removed from request URLs in logs and traces."""

    traces: ObservabilityTraces
    """Trace settings for the Worker."""


class PreviewsBaseConfigCacheOptions(TypedDict, total=False):
    """Cache options used when creating new Previews."""

    enabled: Required[bool]
    """Whether caching is enabled for this Worker."""

    cross_version_cache: bool
    """Whether cached responses are shared across Worker version uploads.

    This is independent of `enabled`. It can stay true while caching is off, so the
    preference survives turning caching off and back on.
    """


class PreviewsBaseConfigEnv(  # type: ignore[call-arg]
    TypedDict,
    total=False,
    extra_items=object,  # pyright: ignore[reportGeneralTypeIssues]
):
    """A single entry in the `env` map.

    An entry holds the same payload
    as an entry of `bindings` without the `name` property, because
    the map key supplies the name. See `binding_item` for the payload
    of each binding kind.
    """

    type: Required[str]
    """The kind of resource that the binding provides."""


class PreviewsBaseConfigLimits(TypedDict, total=False):
    """Resource limits enforced at runtime for newly created Previews."""

    cpu_ms: int
    """The amount of CPU time this Worker can use in milliseconds."""

    subrequests: int
    """The number of subrequests this Worker can make per request."""


class PreviewsBaseConfigObservabilityIssues(TypedDict, total=False):
    """Real-time Issues settings for the Worker."""

    enabled: bool
    """Whether real-time Issues are enabled for the Worker."""


class PreviewsBaseConfigObservabilityLogs(TypedDict, total=False):
    """Log settings for the Worker."""

    destinations: SequenceNotStr[str]
    """A list of destinations where logs will be exported to."""

    enabled: bool
    """Whether logs are enabled for the Worker."""

    head_sampling_rate: float
    """The sampling rate for logs. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    invocation_logs: bool
    """
    Whether
    [invocation logs](https://developers.cloudflare.com/workers/observability/logs/workers-logs/#invocation-logs)
    are enabled for the Worker.
    """

    persist: bool
    """Whether log persistence is enabled for the Worker."""


class PreviewsBaseConfigObservabilityTraces(TypedDict, total=False):
    """Trace settings for the Worker."""

    destinations: SequenceNotStr[str]
    """A list of destinations where traces will be exported to."""

    enabled: bool
    """Whether traces are enabled for the Worker."""

    head_sampling_rate: float
    """The sampling rate for traces. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    persist: bool
    """Whether trace persistence is enabled for the Worker."""

    propagation_policy: Optional[Literal["authenticated", "accept"]]
    """
    Controls how inbound trace context (traceparent/tracestate) headers on incoming
    requests are handled. "authenticated" honors inbound trace context only when
    accompanied by a valid trace auth token. "accept" unconditionally accepts
    inbound trace context. Requires the trace propagation feature to be enabled.
    Returns null when the trace propagation feature is not enabled for the account.
    """


class PreviewsBaseConfigObservability(TypedDict, total=False):
    """Observability settings used when creating new Previews."""

    enabled: bool
    """Whether observability is enabled for the Worker."""

    head_sampling_rate: float
    """The sampling rate for observability. From 0 to 1 (1 = 100%, 0.1 = 10%)."""

    issues: Optional[PreviewsBaseConfigObservabilityIssues]
    """Real-time Issues settings for the Worker."""

    logs: PreviewsBaseConfigObservabilityLogs
    """Log settings for the Worker."""

    redact_query_string: bool
    """Whether query strings are removed from request URLs in logs and traces."""

    traces: PreviewsBaseConfigObservabilityTraces
    """Trace settings for the Worker."""


class PreviewsBaseConfigPlacementMode(TypedDict, total=False):
    mode: Required[Literal["smart"]]
    """
    Enables
    [Smart Placement](https://developers.cloudflare.com/workers/configuration/smart-placement).
    """


class PreviewsBaseConfigPlacementRegion(TypedDict, total=False):
    region: Required[str]
    """Cloud region for targeted placement in format 'provider:region'."""


class PreviewsBaseConfigPlacementHostname(TypedDict, total=False):
    hostname: Required[str]
    """HTTP hostname for targeted placement."""


class PreviewsBaseConfigPlacementHost(TypedDict, total=False):
    host: Required[str]
    """TCP host and port for targeted placement."""


class PreviewsBaseConfigPlacementUnionMember4(TypedDict, total=False):
    mode: Required[Literal["targeted"]]
    """Targeted placement mode."""

    region: Required[str]
    """Cloud region for targeted placement in format 'provider:region'."""


class PreviewsBaseConfigPlacementUnionMember5(TypedDict, total=False):
    hostname: Required[str]
    """HTTP hostname for targeted placement."""

    mode: Required[Literal["targeted"]]
    """Targeted placement mode."""


class PreviewsBaseConfigPlacementUnionMember6(TypedDict, total=False):
    host: Required[str]
    """TCP host and port for targeted placement."""

    mode: Required[Literal["targeted"]]
    """Targeted placement mode."""


class PreviewsBaseConfigPlacementUnionMember7TargetRegion(TypedDict, total=False):
    region: Required[str]
    """Cloud region in format 'provider:region'."""


class PreviewsBaseConfigPlacementUnionMember7TargetHostname(TypedDict, total=False):
    hostname: Required[str]
    """HTTP hostname for targeted placement."""


class PreviewsBaseConfigPlacementUnionMember7TargetHost(TypedDict, total=False):
    host: Required[str]
    """TCP host:port for targeted placement."""


PreviewsBaseConfigPlacementUnionMember7Target: TypeAlias = Union[
    PreviewsBaseConfigPlacementUnionMember7TargetRegion,
    PreviewsBaseConfigPlacementUnionMember7TargetHostname,
    PreviewsBaseConfigPlacementUnionMember7TargetHost,
]


class PreviewsBaseConfigPlacementUnionMember7(TypedDict, total=False):
    mode: Required[Literal["targeted"]]
    """Targeted placement mode."""

    target: Required[Iterable[PreviewsBaseConfigPlacementUnionMember7Target]]
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


class PreviewsBaseConfigTailConsumer(TypedDict, total=False):
    name: Required[str]
    """Name of the consumer Worker."""


class PreviewsBaseConfig(TypedDict, total=False):
    """Template configuration used when creating new Previews for this Worker."""

    cache_options: PreviewsBaseConfigCacheOptions
    """Cache options used when creating new Previews."""

    env: Dict[str, PreviewsBaseConfigEnv]
    """Bindings used when creating new Previews, keyed by binding name."""

    limits: PreviewsBaseConfigLimits
    """Resource limits enforced at runtime for newly created Previews."""

    logpush: bool
    """Whether logpush is enabled when creating new Previews."""

    observability: PreviewsBaseConfigObservability
    """Observability settings used when creating new Previews."""

    placement: PreviewsBaseConfigPlacement
    """Placement configuration used when creating new Previews."""

    tail_consumers: Iterable[PreviewsBaseConfigTailConsumer]
    """Other Workers that should consume logs from newly created Previews."""


class Subdomain(TypedDict, total=False):
    """Subdomain settings for the Worker."""

    enabled: bool
    """Whether the \\**.workers.dev subdomain is enabled for the Worker."""

    previews_enabled: bool
    """
    Whether
    [preview URLs](https://developers.cloudflare.com/workers/configuration/previews/)
    are enabled for the Worker.
    """


class TailConsumer(TypedDict, total=False):
    name: Required[str]
    """Name of the consumer Worker."""
