from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from math import isfinite
from numbers import Integral, Real
from typing import Any, Literal, Protocol

from dreamscale_transport import Observation
from typing_extensions import TypeAliasType

ProviderPreference = TypeAliasType("ProviderPreference", Literal["aws", "modal"])
# "fast" runs a model's dedicated faster route at its fast price.
SpeedPreference = TypeAliasType("SpeedPreference", Literal["standard", "fast"])

TransportPreference = TypeAliasType(
    "TransportPreference",
    Literal["auto", "quic", "relay"],
)
TransportMode = TypeAliasType(
    "TransportMode",
    Literal["quic", "quic_punch", "relay", "wss_tunnel"],
)
RunStopReason = TypeAliasType(
    "RunStopReason",
    Literal["act_callback", "action_limit", "interrupted", "error"],
)
# The AWS-style names earlier releases accepted; the control plane keeps them as aliases of
# its regions (us-west-2 is US West).
SupportedRegion = TypeAliasType(
    "SupportedRegion",
    Literal[
        "ap-southeast-2",
        "us-west-2",
        "us-east-1",
        "eu-central-1",
    ],
)
# "auto" (the default; "nearest" is its older name) measures and picks the nearest region;
# "available" also takes compatible warm compute elsewhere. Any other value is a region id
# such as "us-west" or "japan", which the control plane checks (GET /v1/regions lists them).
RegionPreference = TypeAliasType(
    "RegionPreference",
    Literal[
        "auto",
        "nearest",
        "available",
        "ap-southeast-2",
        "us-west-2",
        "us-east-1",
        "eu-central-1",
    ]
    | str,
)
UnderrunPolicy = TypeAliasType(
    "UnderrunPolicy",
    Literal["hold_position", "repeat_last_action"],
)
BufferHealth = TypeAliasType(
    "BufferHealth",
    Literal["ok", "low", "waiting", "empty"],
)
ActionSmoothingMode = TypeAliasType(
    "ActionSmoothingMode",
    Literal["auto", "output", "motion", "motion_handover", "motion_speed", "continuation"],
)
RunMode = TypeAliasType("RunMode", Literal["async", "sync"])
SamplingMode = TypeAliasType(
    "SamplingMode",
    Literal["upstream_eval", "async_8", "async_latest"],
)

SUPPORTED_REGIONS: tuple[SupportedRegion, ...] = (
    "ap-southeast-2",
    "us-west-2",
    "us-east-1",
    "eu-central-1",
)


class ObservationLike(Protocol):
    def to_wire(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
    ) -> Observation:
        ...


@dataclass(frozen=True)
class ActionTiming:
    obs_to_action_ms: float
    transport_send_ms: float | None = None
    wait_for_chunk_ms: float | None = None
    server_queue_ms: float | None = None
    server_inference_ms: float | None = None
    server_total_ms: float | None = None
    client_overhead_ms: float | None = None
    # The time spent encoding this observation's images before the request (not part of
    # obs_to_action_ms), and the encoded bytes it uploaded, whose transfer is part of
    # client_overhead_ms. Frame content drives both: noisy frames encode slower and larger.
    client_encode_ms: float | None = None
    upload_bytes: int | None = None
    quic_rtt_ms: float | None = None
    data_plane_rtt_ms: float | None = None
    worker_queue_ms: float | None = None
    worker_preprocess_ms: float | None = None
    worker_inference_ms: float | None = None
    worker_postprocess_ms: float | None = None


@dataclass(frozen=True)
class PolicyContract:
    """What a connected model returns and accepts: ``policy.contract``."""

    # The rate the model's actions are spaced at: row i of a chunk follows row 0 by i / action_hz s.
    action_hz: float
    # Actions per chunk.
    chunk_size: int
    action_dim: int | None
    state_dim: int | None
    # A deployment's camera keys, in its order; () where the robot's helper names the cameras.
    camera_keys: tuple[str, ...]
    # Real-time chunking: "train_time" (committed actions are pinned), "inference_time" or "off".
    rtc: str
    # The most committed actions a chunk can start with: train-time RTC's cap (None when the
    # server doesn't report it), a deployment's test-time RTC's (the chunk less its fresh
    # rows), else 0.
    max_prefix_rows: int | None
    # How many entries predict()'s history parameters take: the observations of the control
    # ticks just before this one, and the actions the robot executed on them (0: none).
    past_observations: int = 0
    action_history: int = 0


@dataclass(frozen=True)
class ActionChunkResult:
    observation_id: int
    chunk_id: int | None
    actions: tuple[tuple[float, ...], ...]
    timing: ActionTiming
    transport_mode: TransportMode | None = None
    action_indices: tuple[int, ...] | None = None
    raw_chunk: Any = field(default=None, repr=False)
    # time.time_ns() when the observation was captured: row 0 is the first action after it.
    capture_time_ns: int | None = None
    # How many of the request's committed actions start this chunk (0 when it sent none, or
    # the server held none): train-time RTC pins them exactly as sent; test-time RTC steers
    # the chunk's first rows toward them.
    prefix_rows: int = 0
    # How many ticks of history the SDK filled in (episode-start padding of past observations
    # or executed actions; 0 for a complete history, and for models without one).
    history_padded: int = 0


@dataclass(frozen=True)
class RunStrategy:
    action_hz: float | None = None
    chunk_size: int | None = None
    replan_at_remaining: int | None = None
    underrun: UnderrunPolicy = "hold_position"
    real_time: bool = True
    timeout_s: float = 60.0
    action_smoothing: ActionSmoothingMode = "auto"
    smoothing_new_weight: float | None = None
    smoothing_correction_steps: int | None = None
    smoothing_reference_speed: float | None = None
    dreamzero_sampling: SamplingMode | None = None
    dreamzero_commit_prefix_steps: Literal[1, 2] = 2
    # "async" asks for the next chunk while rows remain and joins it to the plan; "sync" runs
    # each chunk to its end, holding while the next is inferred, and plays its rows as they are
    # (the chunked schedule of upstream's reference, Praxis-1's default).
    mode: RunMode = "async"

    def __post_init__(self) -> None:
        if self.mode not in ("async", "sync"):
            raise ValueError(f"unknown run mode: {self.mode!r}")
        if self.dreamzero_sampling is not None and (
            not isinstance(self.dreamzero_sampling, str)
            or self.dreamzero_sampling
            not in ("upstream_eval", "async_8", "async_latest")
        ):
            raise ValueError(
                f"unknown DreamZero sampling mode: {self.dreamzero_sampling!r}"
            )
        if not isinstance(self.action_smoothing, str) or self.action_smoothing not in {
            "auto",
            "output",
            "motion",
            "motion_handover",
            "motion_speed",
            "continuation",
        }:
            raise ValueError(
                f"unknown action smoothing mode: {self.action_smoothing!r}"
            )
        if self.smoothing_new_weight is not None:
            if isinstance(self.smoothing_new_weight, bool) or not isinstance(
                self.smoothing_new_weight, Real
            ):
                raise ValueError("smoothing_new_weight must be a number")
            try:
                new_weight = float(self.smoothing_new_weight)
            except (TypeError, ValueError, OverflowError) as exc:
                raise ValueError("smoothing_new_weight must be a number") from exc
            if not isfinite(new_weight) or not 0.0 <= new_weight <= 1.0:
                raise ValueError("smoothing_new_weight must be between 0 and 1")
            object.__setattr__(self, "smoothing_new_weight", new_weight)
        if self.smoothing_correction_steps is not None:
            if isinstance(self.smoothing_correction_steps, bool) or not isinstance(
                self.smoothing_correction_steps, Integral
            ):
                raise ValueError("smoothing_correction_steps must be an integer")
            if self.smoothing_correction_steps < 1:
                raise ValueError("smoothing_correction_steps must be positive")
            object.__setattr__(
                self,
                "smoothing_correction_steps",
                int(self.smoothing_correction_steps),
            )
        if self.smoothing_reference_speed is not None:
            value = self.smoothing_reference_speed
            if isinstance(value, bool) or not isinstance(value, Real):
                raise ValueError("smoothing_reference_speed must be finite and positive")
            try:
                value = float(value)
            except (ValueError, OverflowError) as exc:
                raise ValueError("smoothing_reference_speed must be finite and positive") from exc
            if not isfinite(value) or value <= 0:
                raise ValueError("smoothing_reference_speed must be finite and positive")
            object.__setattr__(self, "smoothing_reference_speed", value)

    @classmethod
    def realtime(cls) -> RunStrategy:
        return cls(real_time=True)

    @classmethod
    def as_fast_as_possible(cls) -> RunStrategy:
        return cls(real_time=False)

    @classmethod
    def libero_default(cls) -> RunStrategy:
        return cls(action_hz=10.0, real_time=True)


@dataclass(frozen=True)
class RunContext:
    action_index: int
    observation_id: int
    actions_remaining: int
    stalled: bool
    elapsed_s: float


@dataclass(frozen=True)
class ActResult:
    done: bool = False
    accepted_action: tuple[float, ...] | None = None

    def __post_init__(self) -> None:
        if self.accepted_action is None:
            return
        if isinstance(self.accepted_action, (str, bytes)):
            raise ValueError("accepted_action must be a finite action")
        try:
            raw = tuple(self.accepted_action)
        except TypeError as exc:
            raise ValueError("accepted_action must be a finite action") from exc
        if not raw or any(isinstance(value, bool) for value in raw):
            raise ValueError("accepted_action must be a finite action")
        try:
            accepted = tuple(float(value) for value in raw)
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError("accepted_action must be a finite action") from exc
        if any(not isfinite(value) for value in accepted):
            raise ValueError("accepted_action must be a finite action")
        object.__setattr__(self, "accepted_action", accepted)


@dataclass(frozen=True)
class ActionEvent:
    action_index: int
    stalled: bool
    actions_remaining: int
    action: tuple[float, ...]


@dataclass(frozen=True)
class DispatchEvent:
    action_index: int
    stalled: bool
    requested_action: tuple[float, ...]
    accepted_action: tuple[float, ...]
    started_ns: int
    completed_ns: int


@dataclass(frozen=True)
class ChunkEvent:
    observation_id: int
    chunk_id: int | None
    base_action_index: int
    accepted_action_index: int
    actions: tuple[tuple[float, ...], ...]
    action_indices: tuple[int, ...] | None


@dataclass(frozen=True)
class RequestEvent:
    """Actual prediction submission; observation is borrowed for the callback only."""

    submitted_ns: int
    base_action_index: int
    actions_remaining: int
    observation: Any = field(repr=False)


@dataclass(frozen=True)
class QueueMergeEvent:
    """Aligned queue snapshots at acceptance, before any subsequent dispatch."""

    submitted_ns: int
    accepted_ns: int
    chunk: ChunkEvent
    before: tuple[tuple[int, tuple[float, ...]], ...]
    before_raw: tuple[tuple[int, tuple[float, ...]], ...]
    after: tuple[tuple[int, tuple[float, ...]], ...]


@dataclass(frozen=True)
class MergeEvent:
    observation_id: int
    chunk_id: int | None
    base_action_index: int
    accepted_action_index: int
    requested_mode: str
    resolved_mode: str
    new_action_weight: float | None
    correction_steps: int | None
    stale_steps: int
    overlap_steps: int
    resolved_steps: int
    rebase_offset_steps: int
    first_executable_source_offset: int | None
    max_abs_position_revision: float
    transition_steps: int | None = None
    arm_speed_rad_s: float | None = None
    correction_gain: float | None = None
    correction_rate_ratio: float | None = None


@dataclass(frozen=True)
class PolicyTimingEvent:
    observation_id: int
    chunk_id: int | None
    obs_to_action_ms: float
    server_queue_ms: float | None
    server_inference_ms: float | None
    server_total_ms: float | None
    client_overhead_ms: float | None
    transport_send_ms: float | None
    wait_for_chunk_ms: float | None
    quic_rtt_ms: float | None
    transport_mode: TransportMode | None
    data_plane_rtt_ms: float | None = None
    worker_queue_ms: float | None = None
    worker_preprocess_ms: float | None = None
    worker_inference_ms: float | None = None
    worker_postprocess_ms: float | None = None


@dataclass(frozen=True)
class BufferEvent:
    action_index: int
    remaining: int
    capacity: int
    health: BufferHealth
    in_flight: bool


@dataclass(frozen=True)
class PolicyStepResult:
    action: tuple[float, ...]
    action_index: int
    observation_id: int | None
    stalled: bool
    actions_remaining: int
    source_chunk_id: int | None = None
    source_observation_id: int | None = None
    source_control_tick: int | None = None
    source_capture_to_execution_ms: float | None = None
    replan_epoch: int | None = None
    cache_generation: int | None = None
    timing_events: tuple[PolicyTimingEvent, ...] = ()
    buffer_events: tuple[BufferEvent, ...] = ()
    chunk_events: tuple[ChunkEvent, ...] = ()
    merge_events: tuple[MergeEvent, ...] = ()
    queue_merge_events: tuple[QueueMergeEvent, ...] = ()


@dataclass(frozen=True)
class RunHooks:
    on_action: Callable[[ActionEvent], None] | None = None
    on_timing: Callable[[PolicyTimingEvent], None] | None = None
    on_buffer: Callable[[BufferEvent], None] | None = None
    on_chunk: Callable[[ChunkEvent], None] | None = None
    on_merge: Callable[[MergeEvent], None] | None = None
    on_dispatch: Callable[[DispatchEvent], None] | None = None
    on_summary: Callable[[RunResult], None] | None = None
    on_request: Callable[[RequestEvent], None] | None = None
    on_queue_merge: Callable[[QueueMergeEvent], None] | None = None


@dataclass(frozen=True)
class LatencyStats:
    samples: int = 0
    p50_ms: float | None = None
    p95_ms: float | None = None


@dataclass(frozen=True)
class RunTimingSummary:
    policy_response_ms: LatencyStats = field(default_factory=LatencyStats)
    data_plane_rtt_ms: LatencyStats = field(default_factory=LatencyStats)
    worker_queue_ms: LatencyStats = field(default_factory=LatencyStats)
    worker_preprocess_ms: LatencyStats = field(default_factory=LatencyStats)
    worker_inference_ms: LatencyStats = field(default_factory=LatencyStats)
    worker_postprocess_ms: LatencyStats = field(default_factory=LatencyStats)


@dataclass(frozen=True)
class RunResult:
    """One control-loop invocation.

    ``done`` means the ``act`` callback requested a stop. It does not claim task
    success, and ``actions`` counts completed actuator callbacks rather than
    confirmed physical execution. ``action_attempts`` also counts callbacks
    that raised or were interrupted before their result was confirmed.
    """

    actions: int
    policy_calls: int
    underruns: int
    done: bool
    elapsed_s: float
    max_actions: int | None = None
    stop_reason: RunStopReason = "action_limit"
    timing: RunTimingSummary = field(default_factory=RunTimingSummary)
    model: str | None = None
    region: str | None = None
    transport_mode: TransportMode | None = None
    fallback_reason: str | None = None
    startup_wait_ms: float = 0.0
    startup_holds: int = 0
    execution_underruns: int = 0
    action_attempts: int = 0
    error_type: str | None = None
    loop_cleanup_error_type: str | None = None


@dataclass
class RuntimeStats:
    requests_submitted: int = 0
    chunks_received: int = 0
    underruns: int = 0
    hold_position_count: int = 0
    stale_chunks_dropped: int = 0
    calibration_samples: int = 0
    rtc_requests: int = 0
    rtc_reference_chunks: int = 0
    rtc_reference_actions: int = 0
    rtc_eligible_delay_samples: int = 0
    rtc_merge_delay_steps: int = 0
    rtc_overcoverage_steps: int = 0
    rtc_undercoverage_steps: int = 0
    rtc_hold_or_starvation_gap_steps: int = 0
    # Ticks next_action() held with no session serving (its link was lost and a new
    # session was opening): also counted in underruns and hold_position_count.
    reconnect_holds: int = 0
    # What a server reported of its answers (policy.runtime.server_report; Praxis-1): answers
    # that said whether they continued the episode's context, those that lost it (a restart
    # other than the episode's start), executed steps whose frames never arrived, and target rows
    # its joint solver retried or missed.
    context_reports: int = 0
    context_restarts: int = 0
    history_frames_missing: int = 0
    ik_retries: int = 0
    ik_misses: int = 0
