"""River API client implementation."""

from __future__ import annotations

import concurrent.futures
import datetime
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass
import json as _json
import logging
import os
import threading
import time
import uuid
import warnings
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request as _UrlRequest
from urllib.request import urlopen as _urlopen

import grpc
import numpy as np

from river_client import __version__
from river_client._nested_codec import from_bytes as _nested_from_bytes
from river_client._nested_codec import to_bytes as _nested_to_bytes
from river_client._proto import pb2, pb2_grpc
from river_client.tokenizers import load_tokenizer
from river_client.types import (
    AuthenticationError,
    ChatCompleteResult,
    Checkpoint,
    ExpertRouting,
    ForwardResult,
    LoraConfig,
    ModelNotFoundError,
    OptimStepResult,
    PendingOp,
    PendingSample,
    PromotedStreamingReplica,
    RiverConnectionError,
    RiverError,
    RiverTimeoutError,
    Sample,
    SessionHeartbeatError,
    TrainingDataArtifact,
    TrainingDataAttestation,
    AttestedTrainingDataArtifact,
    TopLogprob,
)

_SERVICE_CONFIG = _json.dumps(
    {
        "methodConfig": [
            {
                "name": [{"service": "river.api.v1.RiverService"}],
                "retryPolicy": {
                    "maxAttempts": 5,
                    "initialBackoff": "0.5s",
                    "maxBackoff": "8s",
                    "backoffMultiplier": 2,
                    "retryableStatusCodes": ["UNAVAILABLE"],
                },
            }
        ],
    }
)

# Identifier this SDK sends on every request — as `x-river-client` gRPC
# metadata and HTTP header, as the channel's user-agent prefix, and as
# `CreateSessionRequest.sdk_version` — so the server can attribute traffic
# to an exact client version for deprecation tracking. The server matches
# it against an allowlist of released versions (`KNOWN_RIVER_CLIENTS` in
# river-api-server's client_info.rs); keep the format
# `river-client-python/<version>`.
_CLIENT_IDENTIFIER = f"river-client-python/{__version__}"

# gRPC Core represents finite message limits as signed 32-bit integers. This
# is the largest finite client-side value; the River server enforces 2 GiB.
_GRPC_MAX_MESSAGE_SIZE_BYTES = 2 * 1024 * 1024 * 1024 - 1

# A request that cannot fit in one gRPC message is submitted as sequential
# gradient-accumulation sub-batches. The upload API accepts an assembled body
# up to and including 1 GiB, so use that full capacity to avoid unnecessary
# accumulation calls for large datums.
_FORWARD_BACKWARD_SUB_BATCH_BYTES = 1024 * 1024 * 1024

_FORWARD_BACKWARD_SUM_METRIC_KEYS = frozenset(
    {
        "loss_sum",
        "opsd_objective_sum",
        "num_tokens",
        "weight_sum",
        "policy_loss_sum",
        "ratio_sum",
        "log_ratio_sum",
        "entropy_sum",
        "num_response",
        "clip_count",
        "trunc_count",
        "quad_penalty_sum",
        "ref_kl_k3_sum",
        "ref_kl_penalty_sum",
        "kl_weight_sum",
        "echo_loss_sum",
        "echo_penalty_sum",
        "echo_weight_sum",
        "num_echo_tokens",
        "echo_policy_overlap_count",
        "ce_loss_sum",
        "kl_loss_sum",
        "num_ce_tokens",
        "num_kl_tokens",
        "moe/expert_capping_ratio_sum",
        "moe/expert_capping_layer_count",
        "moe/expert_capping_dropped_pairs_sum",
        "moe/expert_capping_token_pairs_sum",
        "moe/routing_contributor_count",
        "moe/dropless_routing_contributor_count",
        "moe/routing_expected_contributor_count",
    }
)

_FORWARD_BACKWARD_MAX_METRIC_KEYS = frozenset({"moe/expert_capping_ratio_max"})


@dataclass(frozen=True)
class _ForwardBackwardRequestPlan:
    """Exact and conservative request sizes plus per-datum wire sizes."""

    static_input_size: int
    datum_field_sizes: tuple[int, ...]
    total_size: int
    maximum_total_size: int


def _protobuf_varint_size(value: int) -> int:
    """Return the encoded size of a non-negative protobuf varint."""
    size = 1
    while value >= 1 << 7:
        value >>= 7
        size += 1
    return size


def _length_delimited_field_size(payload_size: int) -> int:
    """Return the wire size of a one-byte-tag length-delimited field."""
    return 1 + _protobuf_varint_size(payload_size) + payload_size


def _forward_backward_input_without_data(
    source_input: pb2.ForwardBackwardInput,
) -> pb2.ForwardBackwardInput:
    """Copy every configured input field except datum payloads.

    Use the descriptor rather than a hand-maintained list so a newly added
    ForwardBackwardInput option is carried into every sub-batch automatically.
    """
    copied_input = pb2.ForwardBackwardInput()
    for field, value in source_input.ListFields():
        if field.name == "data":
            continue
        copied_value = getattr(copied_input, field.name)
        if field.is_repeated:
            if (
                field.message_type is not None
                and field.message_type.GetOptions().map_entry
            ):
                copied_value.update(value)
            else:
                copied_value.extend(value)
        elif field.message_type is not None:
            copied_value.CopyFrom(value)
        else:
            setattr(copied_input, field.name, value)
    return copied_input


def _forward_backward_request_size(
    request: pb2.ForwardBackwardRequest,
    *,
    static_input_size: int,
    datum_field_size: int,
    maximum_sequence_id_size: bool = False,
) -> int:
    """Calculate request bytes without serializing its datum list.

    Both message fields that wrap the input and each datum field have one-byte
    tags in the River protocol. ``static_input_size`` is the encoded size of
    the input without ``data``; ``datum_field_size`` includes the data field's
    tag and length prefix for every included datum.
    """
    envelope = pb2.ForwardBackwardRequest(model_id=request.model_id)
    if maximum_sequence_id_size:
        envelope.seq_id = (1 << 63) - 1
    elif request.HasField("seq_id"):
        envelope.seq_id = request.seq_id
    input_size = static_input_size + datum_field_size
    return envelope.ByteSize() + _length_delimited_field_size(input_size)


def _forward_backward_request_plan(
    request: pb2.ForwardBackwardRequest,
    datums: Iterable[pb2.Datum],
) -> _ForwardBackwardRequestPlan:
    """Measure a datum stream without building one message containing all of it."""
    source_input = request.forward_backward_input
    if source_input.data:
        raise ValueError("forward/backward request plan requires an input without data")
    static_input_size = source_input.ByteSize()
    datum_field_sizes = tuple(
        _length_delimited_field_size(datum.ByteSize()) for datum in datums
    )
    total_size = _forward_backward_request_size(
        request,
        static_input_size=static_input_size,
        datum_field_size=sum(datum_field_sizes),
    )
    maximum_total_size = _forward_backward_request_size(
        request,
        static_input_size=static_input_size,
        datum_field_size=sum(datum_field_sizes),
        maximum_sequence_id_size=True,
    )
    return _ForwardBackwardRequestPlan(
        static_input_size=static_input_size,
        datum_field_sizes=datum_field_sizes,
        total_size=total_size,
        maximum_total_size=maximum_total_size,
    )


def _merge_forward_backward_sub_batch_results(
    results: list[ForwardResult], chunk_sizes: list[int]
) -> ForwardResult:
    """Restore the logical batch's result from sequential sub-batches."""
    if not results:
        raise RiverError("forward_backward sub-batch plan was empty")
    if len(results) == 1:
        return results[0]

    # A sub-batch result has server-finalized derived metrics and model-specific
    # state. Keep only values this client can combine exactly; reporting the
    # last chunk's value as a logical-batch metric is silently incorrect.
    metrics: dict[str, float] = {}
    for key in _FORWARD_BACKWARD_SUM_METRIC_KEYS:
        values = [result.metrics[key] for result in results if key in result.metrics]
        if values:
            metrics[key] = sum(values)
    for key in _FORWARD_BACKWARD_MAX_METRIC_KEYS:
        values = [result.metrics[key] for result in results if key in result.metrics]
        if values:
            metrics[key] = max(values)

    # The server reports loss as its sum-loss divided by the number of valid
    # datums. A failing datum fails the whole sub-request, so the submitted
    # datum count is the correct denominator for every successful result.
    if all("loss" in result.metrics for result in results):
        total_items = sum(chunk_sizes)
        metrics["loss"] = (
            sum(
                result.metrics["loss"] * size
                for result, size in zip(results, chunk_sizes)
            )
            / total_items
        )
    if any("micro_batches" in result.metrics for result in results):
        metrics["micro_batches"] = sum(
            result.metrics.get("micro_batches", 0.0) for result in results
        )

    # Re-derive the public loss statistics from their raw numerator and
    # denominator fields, matching the server's cross-crew aggregation.
    _derive_metric_ratio(metrics, "loss_mean", "loss_sum", "weight_sum")
    for key in (
        "mean_ratio",
        "kl",
        "entropy",
        "clip_frac",
        "truncation_frac",
        "quad_penalty",
    ):
        numerator = {
            "mean_ratio": "ratio_sum",
            "kl": "log_ratio_sum",
            "entropy": "entropy_sum",
            "clip_frac": "clip_count",
            "truncation_frac": "trunc_count",
            "quad_penalty": "quad_penalty_sum",
        }[key]
        _derive_metric_ratio(metrics, key, numerator, "num_response")
    _derive_metric_ratio(metrics, "ref_kl_k3", "ref_kl_k3_sum", "kl_weight_sum")
    _derive_metric_ratio(
        metrics, "ref_kl_penalty", "ref_kl_penalty_sum", "kl_weight_sum"
    )
    _derive_metric_ratio(metrics, "echo_loss", "echo_loss_sum", "echo_weight_sum")
    _derive_metric_ratio(metrics, "echo_penalty", "echo_penalty_sum", "echo_weight_sum")
    _derive_metric_ratio(metrics, "ce_loss", "ce_loss_sum", "num_ce_tokens")
    _derive_metric_ratio(metrics, "opsd_kl", "kl_loss_sum", "num_kl_tokens")
    _derive_metric_ratio(
        metrics,
        "moe/expert_capping_ratio_avg",
        "moe/expert_capping_ratio_sum",
        "moe/expert_capping_layer_count",
    )
    _derive_metric_ratio(
        metrics,
        "moe/expert_capping_drop_fraction",
        "moe/expert_capping_dropped_pairs_sum",
        "moe/expert_capping_token_pairs_sum",
    )
    if (
        "moe/expert_capping_dropped_pairs_sum" not in metrics
        and metrics.get("moe/routing_expected_contributor_count", 0.0) > 0.0
        and metrics.get("moe/routing_contributor_count")
        == metrics.get("moe/routing_expected_contributor_count")
        and metrics.get("moe/dropless_routing_contributor_count")
        == metrics.get("moe/routing_expected_contributor_count")
    ):
        metrics["moe/dropless_routing"] = 1.0
        metrics["moe/expert_capping_drop_fraction"] = 0.0

    logprobs = None
    if all(result.logprobs is not None for result in results):
        logprobs = [item for result in results for item in result.logprobs or []]
    return ForwardResult(metrics=metrics, logprobs=logprobs)


def _derive_metric_ratio(
    metrics: dict[str, float], output: str, numerator: str, denominator: str
) -> None:
    if numerator in metrics and metrics.get(denominator, 0.0) > 0.0:
        metrics[output] = metrics[numerator] / metrics[denominator]
    else:
        metrics.pop(output, None)


_GRPC_CHANNEL_BASE_OPTIONS: list[tuple[str, object]] = [
    # Prefixes the wire user-agent (`river-client-python/x.y.z
    # grpc-python/...`), identifying the SDK even on paths that bypass
    # `_get_metadata`.
    ("grpc.primary_user_agent", _CLIENT_IDENTIFIER),
    ("grpc.keepalive_time_ms", 10_000),
    ("grpc.keepalive_timeout_ms", 5_000),
    ("grpc.keepalive_permit_without_calls", 1),
    ("grpc.http2.max_pings_without_data", 0),
    # Message-size limits so large training responses (per-token logprobs for
    # long sequences / big batches) don't hit gRPC's default 4 MiB cap.
    ("grpc.max_receive_message_length", _GRPC_MAX_MESSAGE_SIZE_BYTES),
    ("grpc.max_send_message_length", _GRPC_MAX_MESSAGE_SIZE_BYTES),
]


def _grpc_channel_options(*, enable_retries: bool) -> list[tuple[str, object]]:
    options = list(_GRPC_CHANNEL_BASE_OPTIONS)
    if enable_retries:
        options.extend(
            (
                ("grpc.service_config", _SERVICE_CONFIG),
                ("grpc.enable_retries", 1),
            )
        )
    else:
        options.append(("grpc.enable_retries", 0))
    return options


_GRPC_CHANNEL_OPTIONS = _grpc_channel_options(enable_retries=True)

_HEARTBEAT_INTERVAL_SECS = 2.0
_HEARTBEAT_POLL_INTERVAL_SECS = 5.0
# Per-call deadline for a single heartbeat RPC. Generous so that on a slow or
# congested network a heartbeat that *would* succeed (just with high latency)
# still completes and counts as a success, instead of being cut short and
# recorded as a DEADLINE_EXCEEDED failure. A healthy heartbeat returns in <100ms,
# so this only bounds the worst case and does not affect the 2s send cadence;
# it just lets an occasional good beat land and reset the liveness window even
# when the network is badly degraded.
_HEARTBEAT_RPC_TIMEOUT_SECS = 30.0
_HEARTBEAT_MAX_ATTEMPTS = 3
_HEARTBEAT_RETRY_BACKOFF_SECS = 0.5
# How long to tolerate heartbeat failures before deciding the session is dead.
# The background thread keeps beating (every _HEARTBEAT_INTERVAL_SECS) the whole
# time; these only govern when a *sustained* failure run makes us give up.
# Two separate thresholds:
#   - transport  : gRPC couldn't reach/serve the server in time (pod rolling,
#                  network blip, or the server briefly overloaded so heartbeats
#                  time out with DEADLINE_EXCEEDED). The request is still alive
#                  server-side, so keep trying for a long time — aligned with the
#                  server's session-active window (30 min), past which the server
#                  reaps the session anyway and retrying can't recover it.
#   - rejection  : server explicitly rejected the heartbeat (session truly gone
#                  from its DB / owner mismatch). Not recoverable by retrying, but
#                  we still grant a grace window to ride out a transient blip
#                  (e.g. failover / row replication lag) before erroring out.
_HEARTBEAT_UNHEALTHY_AFTER_SECS = 120.0
_HEARTBEAT_UNHEALTHY_AFTER_TRANSPORT_SECS = 1800.0

# Status codes that indicate a transient transport-layer failure where the
# request is likely still alive on the server and will succeed if we retry.
_TRANSIENT_GRPC_STATUS_CODES = frozenset({"UNAVAILABLE", "DEADLINE_EXCEEDED"})

# Backoff schedule for polling retries when we hit a transient gRPC error.
# Capped so we don't wait too long between polls, but backs off enough not
# to hammer a recovering server.
_POLL_RETRY_INITIAL_SLEEP_SECS = 0.5
_POLL_RETRY_MAX_SLEEP_SECS = 5.0

# Backoff schedule for Submit-RPC retries (the first call of every user-facing
# operation). Sits on top of gRPC's built-in retry policy so short transient
# transport outages don't fail the user's call before the operation even gets
# a ``request_id``. Bounded by the same window as the heartbeat transport
# tolerance (_HEARTBEAT_UNHEALTHY_AFTER_TRANSPORT_SECS) — past that point the
# server has reaped the session anyway, so retrying can't recover it.
_SUBMIT_RETRY_INITIAL_SLEEP_SECS = 1.0
_SUBMIT_RETRY_MAX_SLEEP_SECS = 8.0


# Parallel-chunk upload of large request bodies. A single gRPC message rides
# one TCP connection, so upload throughput is capped by the sender's kernel
# send buffer over one round trip (~3.3MB in flight on stock Linux — ~19MB/s
# at 170ms to the API edge). Bodies at or above the threshold are split into
# chunks and shipped over separate connections (CreateUpload / UploadChunk),
# then submitted as a thin request referencing the upload. The server
# assembles and processes the identical bytes, so semantics are unchanged.
_UPLOAD_THRESHOLD_BYTES = int(
    os.environ.get("RIVER_UPLOAD_THRESHOLD_BYTES", 64 * 1024 * 1024)
)
_REQUIRE_CHUNKED_UPLOAD = os.environ.get("RIVER_REQUIRE_CHUNKED_UPLOAD") == "1"
_UPLOAD_CHUNK_BYTES = int(os.environ.get("RIVER_UPLOAD_CHUNK_BYTES", 32 * 1024 * 1024))
_UPLOAD_PARALLELISM = int(os.environ.get("RIVER_UPLOAD_PARALLELISM", "6"))
# Server-side cap on chunks per upload session; chunk size grows past
# _UPLOAD_CHUNK_BYTES rather than exceeding this.
_UPLOAD_MAX_CHUNKS = 16
_UPLOAD_CHUNK_RETRIES = 3
_UPLOAD_CHUNK_TIMEOUT_SECS = 120.0

_logger = logging.getLogger(__name__)

# Default timeout for client operations. Set to 1 day so jobs keep running
# while the backend recovers from transient issues rather than failing fast.
_DEFAULT_TIMEOUT_SECS = 86_400.0
_SAMPLE_POLL_INTERVAL_SECS = 1.0
_STREAM_READ_TIMEOUT_SECS = 60.0
_STREAMING_REPLICA_READY = "ready"
_STREAMING_REPLICA_DEGRADED = "degraded"
_STREAMING_REPLICA_ROUTEABLE = {
    _STREAMING_REPLICA_READY,
    _STREAMING_REPLICA_DEGRADED,
}


def _warn_return_logprobs_ignored(return_logprobs: bool) -> None:
    if return_logprobs:
        # Attribute to the first frame outside this package: a fixed
        # stacklevel can't cover both the direct submit call and the
        # sync wrapper's delegation, and the default filters only show
        # DeprecationWarning attributed to user code.
        warnings.warn(
            "return_logprobs is ignored for forward_backward; training "
            "logprobs are returned when the worker includes them in the result",
            DeprecationWarning,
            stacklevel=2,
            skip_file_prefixes=(os.path.dirname(os.path.abspath(__file__)),),
        )


def _require_ids_only_routing_replay(force_routing_replay: object) -> None:
    """Reject internal wire modes at the public client boundary."""
    if not isinstance(force_routing_replay, bool):
        raise TypeError("force_routing_replay must be a bool")


def _is_transient_connection_error(error: Exception) -> bool:
    """Return True when `error` is a transport-level gRPC failure that's safe
    to retry (the request is still in flight or queued server-side)."""
    return (
        isinstance(error, RiverConnectionError)
        and error.status_code in _TRANSIENT_GRPC_STATUS_CODES
    )


# gRPC status codes that are TERMINAL on the idempotent RetrieveFuture poll:
# retrying can't clear them (auth / identity / argument / state problems), so we
# surface them immediately rather than masking the real, actionable error.
#
# Everything NOT in this set is retried by default on the poll — including
# INTERNAL/UNKNOWN/ABORTED/RESOURCE_EXHAUSTED and the HTTP/2 stream resets
# (RST_STREAM / GOAWAY / connection reset) that an external L7 LB throws on
# long-lived / large-response streams. The poll is an idempotent read, so
# re-polling is side-effect-free; we only need to fail fast on the unrecoverable
# codes, not enumerate every transient one.
_POLL_TERMINAL_STATUS_CODES = frozenset(
    {
        "UNAUTHENTICATED",
        "PERMISSION_DENIED",
        "NOT_FOUND",
        "INVALID_ARGUMENT",
        "FAILED_PRECONDITION",
        "ALREADY_EXISTS",
        "UNIMPLEMENTED",
        "CANCELLED",
    }
)
# Max default (non-in-flight) retries per poll before giving up, counted since
# the last successful poll — NOT strictly back-to-back. An interleaved
# UNAVAILABLE/DEADLINE_EXCEEDED takes the in-flight retry path and does NOT reset
# the counter, so a run like INTERNAL, UNAVAILABLE, INTERNAL, … still trips the
# cap. That's deliberate: it bounds a deterministically-failing response (e.g.
# one too large for the LB, which resets every attempt) so it surfaces instead
# of hanging until the operation timeout, even when the server is also
# intermittently UNAVAILABLE. UNAVAILABLE/DEADLINE_EXCEEDED are exempt from the
# count — the request is still in flight server-side — and retried until the
# timeout. The counter resets only on a successful poll (including
# ``try_again``).
_POLL_MAX_RETRIES = 6


def _proto_top_logprobs_to_dicts(positions) -> list[list[TopLogprob]]:
    """Convert a repeated ``TopLogprobsPosition`` proto field into nested
    ``TopLogprob`` dataclass lists for ergonomic access.

    Empty input (server didn't populate top-K) maps to an empty outer list.
    """
    return [
        [
            TopLogprob(logprob=c.logprob, token_id=c.token_id, token=c.token)
            for c in pos.candidates
        ]
        for pos in positions
    ]


def _optional_proto_list(message, field_name: str) -> list:
    """Return a proto repeated field as a list when this client/server pair has it.

    River services may roll independently from the Python client. Keep additive
    response fields optional so mixed-version deployments can still serve basic
    generation.
    """
    return list(getattr(message, field_name, []) or [])


def _expert_routing_proto_to_dict(er) -> dict | None:
    """Convert an ``ExpertRouting`` proto submessage into a plain dict
    for downstream consumers, or ``None`` when the message is unset or
    empty.

    Output shape mirrors the ``ExpertRouting`` dataclass:

      * ``num_tokens`` (int) — informational; equals ``seqlen - 1``.
      * ``num_decoder_layers`` (int) — informational.
      * ``top_k`` (int) — informational.
      * ``layer_indices`` (list[int]) — informational.
      * ``topk_ids`` (bytes, int16 LE) — authoritative.

    Routing replay is ids-only. Any captured weights are ignored because the
    trainer recomputes weights with its live gate at the captured experts.
    """
    if er is None:
        return None
    ids = getattr(er, "topk_ids", b"") or b""
    handle = getattr(er, "routing_handle", "") or ""
    if not ids and not handle:
        return None
    return {
        "num_tokens": int(getattr(er, "num_tokens", 0)),
        "num_decoder_layers": int(getattr(er, "num_decoder_layers", 0)),
        "top_k": int(getattr(er, "top_k", 0)),
        "layer_indices": list(getattr(er, "layer_indices", []) or []),
        "topk_ids": bytes(ids),
        "handle": handle,
    }


def _tokens_and_logprobs_from_raw(
    r: dict,
    tokenizer,
    max_tokens: int,
) -> tuple[list[int], list[float], str]:
    """Resolve generated token IDs, logprobs, and stop reason from a raw result.

    Prefers server-side ``token_ids`` when populated (native /generate path).
    Falls back to ``tokenizer.encode(text)`` when they are absent (legacy
    worker or OpenAI fallback). Aligns ``token_logprobs`` with the resolved
    tokens, padding with 0.0 if needed.
    """
    text = r["text"]
    server_token_ids: list[int] = r.get("token_ids") or []
    token_logprobs: list[float] = r.get("token_logprobs", [])
    if server_token_ids:
        tokens = list(server_token_ids)
    else:
        tokens = tokenizer.encode(text, add_special_tokens=False)

    if token_logprobs and len(token_logprobs) == len(tokens):
        logprobs = list(token_logprobs)
    elif token_logprobs:
        logprobs = list(token_logprobs[: len(tokens)])
        while len(logprobs) < len(tokens):
            logprobs.append(0.0)
    else:
        logprobs = [0.0] * len(tokens)

    stop_reason = "length" if len(tokens) >= max_tokens else "stop"
    return tokens, logprobs, stop_reason


def _optional_prompt_logprobs(
    r: dict, return_prompt_logprobs: bool
) -> list[float] | None:
    if not return_prompt_logprobs:
        return None
    return list(r.get("prompt_token_logprobs", []) or [])


def _optional_prompt_token_ids(
    r: dict, return_prompt_token_ids: bool
) -> list[int] | None:
    """Return server-provided prompt token IDs when they were requested."""
    if not return_prompt_token_ids:
        return None
    ids = r.get("prompt_token_ids") or []
    return list(ids) if ids else None


def _optional_top_logprobs(
    r: dict,
    key: str,
) -> list[list[TopLogprob]] | None:
    """Pass through a top-K block from the raw dict, or ``None`` if absent.

    Whether top-K was actually requested is encoded by the server — if the
    caller didn't set ``prompts[i]["logprobs"] > 0`` then the server returns
    an empty list here and we surface that as ``None``.
    """
    value = r.get(key) or []
    return list(value) if value else None


def _normalize_per_prompt_images(
    prompts: list[str],
    images: list[bytes] | list[list[bytes]] | None,
) -> list[list[bytes]]:
    """Coerce ``images`` to per-prompt list-of-lists shape.

    Three accepted forms:

    * ``None`` → empty image list per prompt (text-only).
    * ``list[bytes]`` (flat) → applies to every prompt (i.e. broadcast
      the same image set to all prompts in the batch). Useful when
      sending a single prompt with a single image.
    * ``list[list[bytes]]`` (nested) → per-prompt explicit; outer
      length must match ``len(prompts)``.

    Raises ``ValueError`` on mismatched lengths or wrong types.
    """
    if images is None:
        return [[] for _ in prompts]
    if not isinstance(images, list):
        raise ValueError(f"images must be a list, got {type(images).__name__}")
    if len(images) == 0:
        return [[] for _ in prompts]
    first = images[0]
    if isinstance(first, (bytes, bytearray)):
        # Flat form: same image set for every prompt.
        flat = [bytes(b) for b in images]  # type: ignore[arg-type]
        return [list(flat) for _ in prompts]
    if isinstance(first, list):
        if len(images) != len(prompts):
            raise ValueError(
                f"images length ({len(images)}) does not match prompts length "
                f"({len(prompts)}); pass a flat list[bytes] to broadcast a "
                "single image set to every prompt."
            )
        return [
            [bytes(b) for b in per_prompt]  # type: ignore[union-attr]
            for per_prompt in images
        ]
    raise ValueError(
        f"images entries must be bytes or list[bytes], got {type(first).__name__}"
    )


def _normalize_prompt_token_ids(
    prompt_token_ids: list[int] | list[list[int]],
) -> list[list[int]]:
    """Normalize ``prompt_token_ids`` to per-prompt form (``list[list[int]]``).

    A flat ``list[int]`` means a single token prompt. Rejects empty
    prompts and non-int ids early — an empty or malformed id list on the
    wire is at best a confusing server error and at worst (on older
    servers) a crashed sampler.
    """
    if not prompt_token_ids:
        raise ValueError("prompt_token_ids must not be empty")
    per_prompt: list[list[int]]
    if isinstance(prompt_token_ids[0], (list, tuple)):
        per_prompt = [list(ids) for ids in prompt_token_ids]  # type: ignore[arg-type]
    else:
        per_prompt = [list(prompt_token_ids)]  # type: ignore[arg-type]
    for idx, ids in enumerate(per_prompt):
        if not ids:
            raise ValueError(f"prompt_token_ids[{idx}] must not be empty")
        for token_id in ids:
            if not isinstance(token_id, int) or isinstance(token_id, bool):
                raise ValueError(
                    f"prompt_token_ids[{idx}] must contain only ints, got "
                    f"{type(token_id).__name__}"
                )
            if token_id < 0:
                raise ValueError(
                    f"prompt_token_ids[{idx}] contains negative token id {token_id}"
                )
    return per_prompt


# Placeholder token strings per multimodal family (mirrors
# ``renderers.qwen3_vl.IMAGE_PAD`` / ``renderers.kimi.MEDIA_PAD``;
# duplicated here to keep client.py free of renderer imports).
# ``_lower_model_input_chunks`` resolves them through the caller's
# tokenizer — a given vocabulary exposes exactly one of these.
_IMAGE_PAD_TOKEN_CANDIDATES = ("<|image_pad|>", "<|media_pad|>")


def _image_placeholder_token_id(tokenizer: Any) -> int:
    """Resolve the model's image placeholder token id via its tokenizer."""
    unk_id = getattr(tokenizer, "unk_token_id", None)
    for token in _IMAGE_PAD_TOKEN_CANDIDATES:
        try:
            token_id = tokenizer.convert_tokens_to_ids(token)
        except (KeyError, ValueError):
            # TikToken-backed tokenizers (Kimi) raise on unknown tokens
            # instead of returning the unk id.
            continue
        if (
            token_id is None
            or token_id < 0
            or (unk_id is not None and token_id == unk_id)
        ):
            continue
        return int(token_id)
    raise ValueError(
        f"tokenizer has none of {_IMAGE_PAD_TOKEN_CANDIDATES!r}; "
        "`model_input` image chunks require a multimodal base model"
    )


def _lower_model_input_chunks(
    model_input: list[dict] | list[list[dict]],
    *,
    image_placeholder_token_id: int,
) -> tuple[list[list[int]], list[list[bytes]]]:
    """Lower training-style ``model_input`` chunk lists to the token-form
    sampling representation.

    Accepts one prompt (``list[chunk]``) or a batch (``list[list[chunk]]``),
    where chunks follow the training-datum convention
    (:meth:`Session._encode_chunked_datum`): ``{"type": "text", "tokens":
    [...]}`` and ``{"type": "image", "data": bytes, ...}``, with any
    vision start/end marker tokens living in the neighboring text chunks.

    Per prompt, text chunks concatenate verbatim and each image chunk
    becomes exactly ONE un-expanded placeholder token — the inference
    backend re-expands it server-side from the image bytes — with the
    bytes collected in chunk order. This means the placeholder count
    always matches the image count by construction, and the identical
    ``model_input`` list works for both ``sample()`` and
    ``forward_backward()``.

    ``expected_tokens`` and ``format`` on image chunks are accepted and
    ignored (the backend derives the true expansion from the bytes;
    format is sniffed from the magic header). To validate that the
    backend's expansion matches a training-side ``expected_tokens``,
    sample with ``return_prompt_logprobs=True``: the echoed
    ``Sample.prompt_token_ids`` has the expanded length, so the total
    image expansion is ``len(prompt_token_ids) - sum(text chunk
    lengths)``. (Expanded image positions echo as internal pad ids —
    typically 0 — not as the placeholder token id.)
    """
    if not isinstance(model_input, list) or not model_input:
        raise ValueError("model_input must be a non-empty list")
    per_prompt_chunks: list[list[dict]]
    if isinstance(model_input[0], dict):
        per_prompt_chunks = [model_input]  # type: ignore[list-item]
    else:
        per_prompt_chunks = [list(chunks) for chunks in model_input]  # type: ignore[arg-type]

    prompt_token_ids: list[list[int]] = []
    per_prompt_images: list[list[bytes]] = []
    for pidx, chunks in enumerate(per_prompt_chunks):
        ids: list[int] = []
        images: list[bytes] = []
        for cidx, chunk in enumerate(chunks):
            if not isinstance(chunk, dict) or "type" not in chunk:
                raise ValueError(
                    f"model_input[{pidx}][{cidx}] must be a dict with a 'type' "
                    f"field; got {chunk!r}"
                )
            ctype = chunk["type"]
            if ctype == "text":
                tokens = chunk.get("tokens")
                if tokens is None:
                    raise ValueError(
                        f"model_input[{pidx}][{cidx}]: text chunk missing 'tokens'"
                    )
                ids.extend(int(t) for t in tokens)
            elif ctype == "image":
                data = chunk.get("data")
                if isinstance(data, (bytes, bytearray, memoryview)):
                    data_bytes = bytes(data)
                elif isinstance(data, np.ndarray) and data.dtype == np.uint8:
                    data_bytes = data.tobytes()
                else:
                    raise ValueError(
                        f"model_input[{pidx}][{cidx}]: image chunk 'data' must "
                        f"be bytes or uint8 ndarray; got {type(data)!r}"
                    )
                ids.append(image_placeholder_token_id)
                images.append(data_bytes)
            else:
                raise ValueError(
                    f"model_input[{pidx}][{cidx}] has unsupported type {ctype!r} "
                    "(expected 'text' or 'image')"
                )
        # The lowering emits exactly one placeholder per image chunk, so any
        # surplus means a placeholder id was hand-written into a text chunk.
        # The backend cannot recover from that (placeholders > images fails
        # deep in the engine and gets retried as if transient; images >
        # placeholders silently drops images), so reject it here where the
        # placeholder id is known.
        n_placeholders = sum(1 for t in ids if t == image_placeholder_token_id)
        if n_placeholders != len(images):
            raise ValueError(
                f"model_input[{pidx}]: found {n_placeholders} image placeholder "
                f"token(s) (id {image_placeholder_token_id}) for {len(images)} "
                "image chunk(s). Do not put placeholder ids inside text chunks; "
                "each image chunk supplies its own placeholder."
            )
        prompt_token_ids.append(ids)
        per_prompt_images.append(images)
    return prompt_token_ids, per_prompt_images


def _resolve_model_input(
    model_input: list[dict] | list[list[dict]] | None,
    *,
    prompts: str | list[str] | None,
    prompt_token_ids: list[int] | list[list[int]] | None,
    images: list[bytes] | list[list[bytes]] | None,
    tokenizer: Any,
) -> tuple[
    str | list[str] | None,
    list[int] | list[list[int]] | None,
    list[bytes] | list[list[bytes]] | None,
]:
    """Fold an optional ``model_input`` into ``(prompts, prompt_token_ids,
    images)``. No-op when ``model_input`` is None."""
    if model_input is None:
        return prompts, prompt_token_ids, images
    if prompts is not None or prompt_token_ids is not None or images is not None:
        raise ValueError(
            "model_input is mutually exclusive with prompts, prompt_token_ids, "
            "and images"
        )
    lowered_ids, lowered_images = _lower_model_input_chunks(
        model_input,
        image_placeholder_token_id=_image_placeholder_token_id(tokenizer),
    )
    has_images = any(imgs for imgs in lowered_images)
    return None, lowered_ids, (lowered_images if has_images else None)


def _build_sample_prompt_dicts(
    prompts: str | list[str] | None,
    *,
    num_samples: int,
    max_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
    stop: list[str] | None,
    seed: int | None,
    return_prompt_logprobs: bool,
    logprobs: int | None,
    seeds: list[int] | None = None,
    images: list[bytes] | list[list[bytes]] | None = None,
    return_expert_routing: bool = False,
    prompt_token_ids: list[int] | list[list[int]] | None = None,
) -> tuple[list[str] | list[list[int]], list[dict]]:
    if (prompts is None) == (prompt_token_ids is None):
        raise ValueError("exactly one of `prompts` and `prompt_token_ids` is required")

    token_prompts: list[list[int]] | None = None
    if prompt_token_ids is not None:
        token_prompts = _normalize_prompt_token_ids(prompt_token_ids)
        prompts = [""] * len(token_prompts)
    elif isinstance(prompts, str):
        prompts = [prompts]
    assert prompts is not None

    per_prompt_images = _normalize_per_prompt_images(prompts, images)
    sample_count = len(prompts) * num_samples
    if seed is not None and seeds is not None:
        raise ValueError("`seed` and `seeds` are mutually exclusive")
    if seeds is not None:
        if len(seeds) != sample_count:
            raise ValueError(
                "`seeds` must provide exactly one seed per prompt/sample "
                f"({sample_count} expected, got {len(seeds)})"
            )
        if any(
            not isinstance(value, int) or isinstance(value, bool) for value in seeds
        ):
            raise TypeError("`seeds` must contain integers")

    prompt_dicts: list[dict] = []
    for prompt_idx, prompt in enumerate(prompts):
        for sample_idx in range(num_samples):
            d: dict = {
                "prompt": prompt,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
            }
            if token_prompts is not None:
                d["input_ids"] = token_prompts[prompt_idx]
            if stop:
                d["stop"] = stop
            seed_index = prompt_idx * num_samples + sample_idx
            if seeds is not None:
                d["seed"] = seeds[seed_index]
            elif seed is not None:
                d["seed"] = seed + seed_index
            if return_prompt_logprobs:
                d["return_prompt_logprobs"] = True
            if logprobs is not None and logprobs > 0:
                d["logprobs"] = logprobs
            if return_expert_routing:
                d["return_expert_routing"] = True
            # All ``num_samples`` repeats of a prompt see the same
            # images — image processing is deterministic per image, no
            # per-sample variation.
            if per_prompt_images[prompt_idx]:
                d["images"] = list(per_prompt_images[prompt_idx])
            prompt_dicts.append(d)

    return (token_prompts if token_prompts is not None else prompts), prompt_dicts


def _group_sample_dicts(
    raw_results: list[dict],
    *,
    num_prompts: int,
    num_samples: int,
    tokenizer,
    max_tokens: int,
    model_step: int,
    request_id: str,
    return_prompt_logprobs: bool,
    return_prompt_token_ids: bool,
) -> list[list[Sample]]:
    expected = num_prompts * num_samples
    if len(raw_results) != expected:
        raise RiverError(
            f"Inference returned {len(raw_results)} results, "
            f"expected {expected} ({num_prompts} prompts x {num_samples} samples). "
            "This is a server-side bug."
        )

    grouped: list[list[Sample]] = []
    idx = 0
    for _prompt_idx in range(num_prompts):
        samples: list[Sample] = []
        for _sample_idx in range(num_samples):
            r = raw_results[idx]
            idx += 1

            tokens, token_lps, stop_reason = _tokens_and_logprobs_from_raw(
                r, tokenizer, max_tokens
            )
            samples.append(
                Sample(
                    tokens=tokens,
                    text=r["text"],
                    logprobs=token_lps,
                    stop_reason=stop_reason,
                    model_step=model_step,
                    prompt_logprobs=_optional_prompt_logprobs(
                        r, return_prompt_logprobs
                    ),
                    request_id=request_id,
                    prompt_token_ids=_optional_prompt_token_ids(
                        r, return_prompt_token_ids
                    ),
                    top_logprobs=_optional_top_logprobs(r, "top_logprobs"),
                    prompt_top_logprobs=_optional_top_logprobs(
                        r, "prompt_top_logprobs"
                    ),
                    expert_routing=_dict_to_expert_routing(r.get("expert_routing")),
                    metrics=dict(r.get("metrics") or {}),
                )
            )
        grouped.append(samples)
    return grouped


def _dict_to_expert_routing(d: dict | None) -> ExpertRouting | None:
    """Materialize an ``ExpertRouting`` dataclass from the raw parsed dict
    produced by :meth:`Session._inference_to_dicts`. Returns ``None`` when
    the field was empty or absent on the wire."""
    if d is None:
        return None
    return ExpertRouting(
        topk_ids=bytes(d.get("topk_ids", b"") or b""),
        num_tokens=int(d.get("num_tokens", 0)),
        num_decoder_layers=int(d.get("num_decoder_layers", 0)),
        top_k=int(d.get("top_k", 0)),
        layer_indices=list(d.get("layer_indices", []) or []),
        handle=str(d.get("handle", "") or ""),
    )


def _json_error_message(body: bytes) -> str | None:
    try:
        parsed = _json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, _json.JSONDecodeError):
        return None
    if not isinstance(parsed, dict):
        return None
    details = parsed.get("error", parsed)
    if isinstance(details, dict):
        message = details.get("message")
        code = details.get("code")
        if message and code:
            return f"{code}: {message}"
        if message:
            return str(message)
        if code:
            return str(code)
    return None


def _http_error(
    status_code: int,
    body: bytes,
    context: str,
) -> RiverError:
    message = _json_error_message(body) or f"{context} failed with HTTP {status_code}"
    if status_code in (401, 403):
        return AuthenticationError(message)
    if status_code == 404:
        return ModelNotFoundError(message)
    if status_code >= 500:
        return RiverConnectionError(
            message,
            status_code=str(status_code),
            details=message,
        )
    return RiverError(message)


def _http_base_url(endpoint: str, port: int, use_ssl: bool) -> str:
    scheme = "https" if use_ssl else "http"
    default_port = 443 if use_ssl else 80
    if port == default_port:
        return f"{scheme}://{endpoint}"
    return f"{scheme}://{endpoint}:{port}"


def _required_str_field(raw: dict[str, Any], field: str) -> str:
    value = raw.get(field)
    if not isinstance(value, str) or not value:
        raise RiverConnectionError(
            f"Streaming replica discovery response missing string field {field!r}"
        )
    return value


def _optional_str_field(raw: dict[str, Any], field: str) -> str | None:
    value = raw.get(field)
    if value is None:
        return None
    if not isinstance(value, str):
        raise RiverConnectionError(
            f"Streaming replica discovery response has non-string field {field!r}"
        )
    return value


def _promoted_streaming_replica_from_raw(
    raw: dict[str, Any],
) -> PromotedStreamingReplica:
    return PromotedStreamingReplica(
        checkpoint=_required_str_field(raw, "checkpoint"),
        status=_required_str_field(raw, "status"),
        base_url=_optional_str_field(raw, "base_url"),
        replica_id=_optional_str_field(raw, "replica_id"),
        model=_required_str_field(raw, "model"),
        base_model=_required_str_field(raw, "base_model"),
        updated_at=_required_str_field(raw, "updated_at"),
        status_reason=_optional_str_field(raw, "status_reason"),
    )


def _stream_chunk_from_blocking_response(response: dict[str, Any]) -> dict[str, Any]:
    """Convert a non-streaming OpenAI chat response into one stream-shaped chunk."""
    choices = []
    for index, choice in enumerate(response.get("choices") or []):
        if not isinstance(choice, dict):
            continue
        message = choice.get("message")
        delta = dict(message) if isinstance(message, dict) else {}
        stream_choice = {
            "index": choice.get("index", index),
            "delta": delta,
            "finish_reason": choice.get("finish_reason"),
        }
        if "logprobs" in choice:
            stream_choice["logprobs"] = choice.get("logprobs")
        choices.append(stream_choice)

    chunk: dict[str, Any] = {
        "id": response.get("id", ""),
        "object": "chat.completion.chunk",
        "created": response.get("created"),
        "model": response.get("model", ""),
        "choices": choices,
    }
    if response.get("usage") is not None:
        chunk["usage"] = response["usage"]
    if response.get("system_fingerprint") is not None:
        chunk["system_fingerprint"] = response["system_fingerprint"]
    return chunk


def _next_sse_frame(buffer: bytearray) -> tuple[int, int] | None:
    lf = buffer.find(b"\n\n")
    crlf = buffer.find(b"\r\n\r\n")
    if lf == -1 and crlf == -1:
        return None
    if lf == -1:
        return crlf, 4
    if crlf == -1:
        return lf, 2
    return (crlf, 4) if crlf < lf else (lf, 2)


def _parse_sse_payload(frame: bytes) -> str | None:
    try:
        text = frame.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RiverError(f"stream emitted non-UTF-8 SSE data: {error}") from error

    lines: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip("\r")
        if line.startswith("data:"):
            data = line[5:]
            if data.startswith(" "):
                data = data[1:]
            lines.append(data)

    if not lines:
        return None
    return "\n".join(lines)


def _iter_sse_payloads(response) -> Iterator[str]:
    """Yield SSE data payloads from a file-like HTTP response."""
    buffer = bytearray()
    while True:
        chunk = response.read(4096)
        if not chunk:
            break
        buffer.extend(chunk)
        while frame := _next_sse_frame(buffer):
            frame_end, delimiter_len = frame
            raw_frame = bytes(buffer[:frame_end])
            del buffer[: frame_end + delimiter_len]
            payload = _parse_sse_payload(raw_frame)
            if payload is not None:
                yield payload

    if any(not chr(byte).isspace() for byte in buffer):
        raise RiverError(f"stream ended with a partial SSE frame ({len(buffer)} bytes)")


def _iter_openai_stream_events(response) -> Iterator[dict[str, Any]]:
    """Decode OpenAI-compatible SSE events.

    The caller should either exhaust this iterator or call ``close()`` on it
    after breaking early so the underlying HTTP connection is released.
    """
    with response:
        for event_payload in _iter_sse_payloads(response):
            if event_payload == "[DONE]":
                return
            try:
                raw = _json.loads(event_payload)
            except _json.JSONDecodeError as error:
                raise RiverError(f"stream emitted invalid JSON: {error}") from error
            if not isinstance(raw, dict):
                raise RiverError("stream emitted a non-object JSON payload")
            yield raw
            if "error" in raw:
                return


class Model:
    """A training model with mutable in-memory weights."""

    def __init__(
        self,
        session: Session,
        model_id: str,
        training_run_id: str,
        base_model: str,
        tokenizer: Any,
    ):
        self._session = session
        self._model_id = model_id
        self._training_run_id = training_run_id
        self._base_model = base_model
        self._tokenizer = tokenizer
        self._step = 0
        self._seq_id = 0

    def __repr__(self) -> str:
        return (
            f"Model(training_run_id={self._training_run_id!r}, "
            f"base_model={self._base_model!r}, step={self._step})"
        )

    @property
    def model_id(self) -> str:
        return self._model_id

    @property
    def training_run_id(self) -> str:
        return self._training_run_id

    @property
    def step(self) -> int:
        """Current training step.

        Advances when an optimizer step is submitted (so pipelined
        submissions observe a consistent value), not when it resolves —
        a failed or timed-out optimizer step leaves it advanced.
        """
        return self._step

    def _next_seq_id(self) -> int:
        self._seq_id += 1
        return self._seq_id

    # --- Training operations ---

    def forward(
        self,
        data: list[dict],
        loss_fn: str = "cross_entropy",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        **loss_config: float,
    ) -> ForwardResult:
        """Forward pass only (compute loss, no gradients).

        Args:
            data: List of training samples, each with "input_ids" and "labels"
            loss_fn: Loss function name
            timeout: Timeout in seconds
            **loss_config: Loss function configuration

        Returns:
            ForwardResult with metrics
        """
        return self._session._forward(
            model_id=self._model_id,
            seq_id=self._next_seq_id(),
            data=data,
            loss_fn=loss_fn,
            loss_config=loss_config,
            timeout=timeout,
        )

    def forward_backward(
        self,
        data: list[dict],
        loss_fn: str = "cross_entropy",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        return_logprobs: bool = False,
        zero_out: bool = True,
        compute_expert_flip_metric: bool = False,
        force_routing_replay: bool = False,
        **loss_config: float,
    ) -> ForwardResult:
        """Forward + backward pass (compute gradients).

        Args:
            data: List of training samples, each with "input_ids" and "labels"
            loss_fn: Loss function name
            timeout: Timeout in seconds
            return_logprobs: Deprecated no-op. Training losses return per-token
                logprobs when the worker includes them in the result; this
                argument is accepted for older callers but is not sent to the
                server as a loss configuration key.
            zero_out: When ``gradient_accumulation`` is enabled, clear existing
                gradients before this call. Use ``True`` for the first
                micro-batch and ``False`` for subsequent micro-batches.
            compute_expert_flip_metric: When True, compares sampled expert
                routing against the training-time routing per token and MoE
                layer, then emits one scalar into
                ``ForwardResult.metrics``:
                  * ``expert_flip/per_token_expert_rate`` ∈ [0, 1] — the
                    fraction of individual top-k expert slots that differ,
                    (top_k − |intersection|) / top_k over (token, layer).
                Independent of ``force_routing_replay``. Requires per-datum
                routing keys from ``Sample.routing_datum_keys(required=True)``.
            force_routing_replay: When true, replay the sampled expert
                selection while recomputing routing weights at those experts
                with the trainer's live gate. Every datum in ``data`` must
                include the keys returned by
                ``Sample.routing_datum_keys(required=True)``.
            **loss_config: Loss function configuration

        Returns:
            ForwardResult with metrics and logprobs when returned by the worker.

        Requests larger than the 1 GiB upload limit are split at datum
        boundaries into sequential gradient-accumulation sub-batches. The
        first sub-batch honors ``zero_out``; later sub-batches retain its
        gradients. A failed sub-batch stops the sequence and this method does
        not submit an optimizer step. ``timeout`` applies to each submitted
        sub-batch, so the total operation can take up to the number of chunks
        times ``timeout``. Split requests return only metrics the client can
        combine exactly across sub-batches; per-sub-batch-only metrics are
        omitted.
        """
        _require_ids_only_routing_replay(force_routing_replay)
        _warn_return_logprobs_ignored(return_logprobs)
        request, plan = self._new_forward_backward_request(
            data=data,
            loss_fn=loss_fn,
            loss_config=dict(loss_config),
            gradient_accumulation=True,
            init_gradients=zero_out,
            compute_expert_flip_metric=compute_expert_flip_metric,
            force_routing_replay=force_routing_replay,
        )
        if plan.maximum_total_size <= _FORWARD_BACKWARD_SUB_BATCH_BYTES:
            request.seq_id = self._next_seq_id()
            chunk = self._session._single_forward_backward_chunk(request, data, plan)
            result = self._submit_forward_backward_request(
                chunk,
                request_size=chunk.ByteSize(),
                timeout=timeout,
            ).result()
            # PendingOp.result() is typed as the union of op results; this
            # PendingOp was built with the forward-backward parser.
            return cast("ForwardResult", result)

        self._validate_forward_backward_sub_batch_plan(request, plan)
        return self._run_forward_backward_sub_batches(
            request, data=data, plan=plan, timeout=timeout
        )

    def optim_step(
        self,
        lr: float,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
        weight_decay: float = 0.0,
        grad_clip_norm: float | None = None,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> OptimStepResult:
        """Apply gradients with Adam optimizer.

        Args:
            lr: Learning rate
            beta1: Adam beta1
            beta2: Adam beta2
            eps: Adam epsilon
            weight_decay: Weight decay
            grad_clip_norm: Gradient clipping norm (None to disable)
            timeout: Timeout in seconds

        Returns:
            OptimStepResult with metrics (step, lr, grad_norm, grad_norm_finite)
        """
        result = self.submit_optim_step(
            lr,
            beta1=beta1,
            beta2=beta2,
            eps=eps,
            weight_decay=weight_decay,
            grad_clip_norm=grad_clip_norm,
            timeout=timeout,
        ).result()
        # PendingOp.result() is typed as the union of op results; this
        # PendingOp was built with the optim-step parser.
        return cast("OptimStepResult", result)

    def train_step(
        self,
        data: list[dict],
        lr: float,
        *,
        loss_fn: str = "cross_entropy",
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
        weight_decay: float = 0.0,
        grad_clip_norm: float | None = None,
        compute_expert_flip_metric: bool = False,
        force_routing_replay: bool = False,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        **loss_config: float,
    ) -> tuple[ForwardResult, OptimStepResult]:
        """Complete training step: forward+backward plus optimizer update.

        Submits forward+backward and the optimizer step back-to-back —
        the server runs them in order as one pipelined unit, without a
        client round trip in between — then waits for both results. See
        :meth:`forward_backward` and :meth:`optim_step` for the full
        parameter reference.

        The error path differs from calling ``forward_backward()`` then
        ``optim_step()``: the optimizer step is already submitted when
        forward-backward resolves, so if forward-backward fails, this
        call raises its error while the optimizer step still runs
        server-side and ``Model.step`` has already advanced. Callers
        that need to inspect both outcomes should use
        :meth:`submit_train_step`.

        A train step is a complete step: gradients are always cleared
        first. For micro-batch gradient accumulation, use
        ``submit_forward_backward(zero_out=...)`` and
        ``submit_optim_step`` directly.

        For a request larger than the 1 GiB upload limit, the client waits for
        each accumulated forward/backward sub-batch before submitting the
        optimizer step. Smaller requests retain the normal pipelined path.
        The forward/backward result from a split request includes only metrics
        the client can combine exactly across its sub-batches.

        Args:
            data: List of training samples, each with "input_ids" and "labels"
            lr: Learning rate
            **loss_config: Loss function configuration

        Returns:
            Tuple of (ForwardResult, OptimStepResult).
        """
        self._reject_train_step_forward_backward_kwargs(loss_config)
        _require_ids_only_routing_replay(force_routing_replay)
        request, plan = self._new_forward_backward_request(
            data=data,
            loss_fn=loss_fn,
            loss_config=dict(loss_config),
            gradient_accumulation=True,
            init_gradients=True,
            compute_expert_flip_metric=compute_expert_flip_metric,
            force_routing_replay=force_routing_replay,
        )
        if plan.maximum_total_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
            self._validate_forward_backward_sub_batch_plan(request, plan)
            fb_result = self._run_forward_backward_sub_batches(
                request, data=data, plan=plan, timeout=timeout
            )
            optim_result = self.optim_step(
                lr,
                beta1=beta1,
                beta2=beta2,
                eps=eps,
                weight_decay=weight_decay,
                grad_clip_norm=grad_clip_norm,
                timeout=timeout,
            )
            return fb_result, optim_result

        request.seq_id = self._next_seq_id()
        chunk = self._session._single_forward_backward_chunk(request, data, plan)
        fb, optim = self._submit_train_step_from_forward_backward_request(
            chunk,
            request_size=chunk.ByteSize(),
            lr=lr,
            beta1=beta1,
            beta2=beta2,
            eps=eps,
            weight_decay=weight_decay,
            grad_clip_norm=grad_clip_norm,
            timeout=timeout,
        )
        # PendingOp.result() is typed as the union of op results; the pair
        # was built with the forward-backward and optim-step parsers.
        return cast("ForwardResult", fb.result()), cast(
            "OptimStepResult", optim.result()
        )

    # --- Async / pipelined operations ---

    def submit_forward_backward(
        self,
        data: list[dict],
        loss_fn: str = "cross_entropy",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        return_logprobs: bool = False,
        zero_out: bool = True,
        compute_expert_flip_metric: bool = False,
        force_routing_replay: bool = False,
        **loss_config: float,
    ) -> PendingOp:
        """Submit forward+backward without blocking. Returns a PendingOp.

        Call ``pending.result()`` later to get the ForwardResult.
        This enables pipelining: submit step N+1 while step N is still running.
        See :meth:`Model.forward_backward` for the full kwarg reference.

        When submitting multiple micro-batches before ``submit_optim_step``, use
        ``zero_out=True`` for the first one and ``False`` for later submissions.

        ``timeout`` bounds the submit RPC and, separately, the wait inside
        ``pending.result()``.

        Requests larger than the 1 GiB upload limit must use the synchronous
        :meth:`forward_backward` method so the client can keep later
        sub-batches and any optimizer step behind successful earlier ones.
        """
        _require_ids_only_routing_replay(force_routing_replay)
        _warn_return_logprobs_ignored(return_logprobs)
        request, plan = self._new_forward_backward_request(
            data=data,
            loss_fn=loss_fn,
            loss_config=dict(loss_config),
            gradient_accumulation=True,
            init_gradients=zero_out,
            compute_expert_flip_metric=compute_expert_flip_metric,
            force_routing_replay=force_routing_replay,
        )
        if plan.maximum_total_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
            raise RiverError(
                "forward_backward batch exceeds the 1 GiB upload limit; use "
                "forward_backward() so the client can submit accumulated "
                "sub-batches sequentially"
            )
        request.seq_id = self._next_seq_id()
        chunk = self._session._single_forward_backward_chunk(request, data, plan)
        return self._submit_forward_backward_request(
            chunk,
            request_size=chunk.ByteSize(),
            timeout=timeout,
        )

    def _new_forward_backward_request(
        self,
        *,
        data: list[dict],
        loss_fn: str,
        loss_config: dict[str, float],
        gradient_accumulation: bool,
        init_gradients: bool,
        compute_expert_flip_metric: bool,
        force_routing_replay: bool,
    ) -> tuple[pb2.ForwardBackwardRequest, _ForwardBackwardRequestPlan]:
        request = self._session._build_forward_backward_request(
            model_id=self._model_id,
            # Do not consume the model sequence until the request is accepted:
            # submit_* rejects oversized requests synchronously.
            seq_id=self._seq_id + 1,
            loss_fn=loss_fn,
            loss_config=loss_config,
            gradient_accumulation=gradient_accumulation,
            init_gradients=init_gradients,
            compute_expert_flip_metric=compute_expert_flip_metric,
            force_routing_replay=force_routing_replay,
        )
        return request, self._session._plan_forward_backward_request(request, data)

    def _submit_forward_backward_request(
        self,
        request: pb2.ForwardBackwardRequest,
        *,
        request_size: int,
        timeout: float,
    ) -> PendingOp:
        request_id = self._session._submit_forward_backward_request(
            request, request_size=request_size, timeout=timeout
        )
        return PendingOp(
            request_id=request_id,
            _session=self._session,
            _model_id=self._model_id,
            _parse_result=self._session._forward_backward_result,
            _timeout=timeout,
        )

    @staticmethod
    def _validate_forward_backward_sub_batch_plan(
        request: pb2.ForwardBackwardRequest,
        plan: _ForwardBackwardRequestPlan,
    ) -> None:
        """Reject an unsendable datum before consuming a model sequence id."""
        for datum_field_size in plan.datum_field_sizes:
            maximum_size = _forward_backward_request_size(
                request,
                static_input_size=plan.static_input_size,
                datum_field_size=datum_field_size,
                maximum_sequence_id_size=True,
            )
            if maximum_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
                raise RiverError(
                    "A single forward_backward datum exceeds the client "
                    f"sub-batch limit of {_FORWARD_BACKWARD_SUB_BATCH_BYTES} bytes"
                )

    def _run_forward_backward_sub_batches(
        self,
        request: pb2.ForwardBackwardRequest,
        *,
        data: list[dict],
        plan: _ForwardBackwardRequestPlan,
        timeout: float,
    ) -> ForwardResult:
        results: list[ForwardResult] = []
        chunk_sizes: list[int] = []
        request.seq_id = self._next_seq_id()
        for chunk_index, (chunk, chunk_size) in enumerate(
            self._session._iter_forward_backward_sub_batches(request, data, plan)
        ):
            if chunk_index:
                chunk.seq_id = self._next_seq_id()
                chunk.forward_backward_input.init_gradients = False
            result = self._submit_forward_backward_request(
                chunk, request_size=chunk.ByteSize(), timeout=timeout
            ).result()
            results.append(cast("ForwardResult", result))
            chunk_sizes.append(chunk_size)
        return _merge_forward_backward_sub_batch_results(results, chunk_sizes)

    def submit_optim_step(
        self,
        lr: float,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
        weight_decay: float = 0.0,
        grad_clip_norm: float | None = None,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> PendingOp:
        """Submit optimizer step without blocking. Returns a PendingOp.

        Call ``pending.result()`` later to get the OptimStepResult.
        ``Model.step`` advances at submit time, even if the operation
        later fails.
        """
        request_id = self._session._submit_optim_step(
            model_id=self._model_id,
            seq_id=self._next_seq_id(),
            lr=lr,
            beta1=beta1,
            beta2=beta2,
            eps=eps,
            weight_decay=weight_decay,
            grad_clip_norm=grad_clip_norm,
        )
        self._step += 1
        return PendingOp(
            request_id=request_id,
            _session=self._session,
            _model_id=self._model_id,
            _parse_result=self._session._optim_step_result,
            _timeout=timeout,
        )

    def submit_train_step(
        self,
        data: list[dict],
        lr: float,
        *,
        loss_fn: str = "cross_entropy",
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8,
        weight_decay: float = 0.0,
        grad_clip_norm: float | None = None,
        compute_expert_flip_metric: bool = False,
        force_routing_replay: bool = False,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        **loss_config: float,
    ) -> tuple[PendingOp, PendingOp]:
        """Submit a complete training step without blocking.

        Fires forward+backward and the optimizer step back-to-back; the
        server runs them in submission order per model. Returns the two
        PendingOps as ``(forward_backward, optim_step)``.

        Because both are submitted up front, a failed forward-backward
        does not cancel the already-submitted optimizer step.
        ``Model.step`` advances at submit time. See
        :meth:`Model.train_step` for the full kwarg reference.

        Requests larger than the 1 GiB upload limit must use
        :meth:`train_step`, which waits for all accumulated sub-batches before
        submitting the optimizer step.
        """
        self._reject_train_step_forward_backward_kwargs(loss_config)
        _require_ids_only_routing_replay(force_routing_replay)
        request, plan = self._new_forward_backward_request(
            data=data,
            loss_fn=loss_fn,
            loss_config=dict(loss_config),
            gradient_accumulation=True,
            init_gradients=True,
            compute_expert_flip_metric=compute_expert_flip_metric,
            force_routing_replay=force_routing_replay,
        )
        if plan.maximum_total_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
            raise RiverError(
                "forward_backward batch exceeds the 1 GiB upload limit; use "
                "train_step() so the client can submit accumulated sub-batches "
                "before the optimizer step"
            )
        request.seq_id = self._next_seq_id()
        chunk = self._session._single_forward_backward_chunk(request, data, plan)
        return self._submit_train_step_from_forward_backward_request(
            chunk,
            request_size=chunk.ByteSize(),
            lr=lr,
            beta1=beta1,
            beta2=beta2,
            eps=eps,
            weight_decay=weight_decay,
            grad_clip_norm=grad_clip_norm,
            timeout=timeout,
        )

    @staticmethod
    def _reject_train_step_forward_backward_kwargs(
        loss_config: dict[str, float],
    ) -> None:
        # These read as forward_backward kwargs but would otherwise ship
        # silently as loss-config floats while gradients are still cleared.
        for reserved in ("zero_out", "return_logprobs"):
            if reserved in loss_config:
                raise TypeError(
                    f"train_step does not accept {reserved!r}; a train step "
                    "always clears gradients first — for micro-batch "
                    "accumulation use submit_forward_backward(zero_out=...) "
                    "and submit_optim_step directly"
                )

    def _submit_train_step_from_forward_backward_request(
        self,
        request: pb2.ForwardBackwardRequest,
        *,
        request_size: int,
        lr: float,
        beta1: float,
        beta2: float,
        eps: float,
        weight_decay: float,
        grad_clip_norm: float | None,
        timeout: float,
    ) -> tuple[PendingOp, PendingOp]:
        fb = self._submit_forward_backward_request(
            request, request_size=request_size, timeout=timeout
        )
        optim = self.submit_optim_step(
            lr,
            beta1=beta1,
            beta2=beta2,
            eps=eps,
            weight_decay=weight_decay,
            grad_clip_norm=grad_clip_norm,
            timeout=timeout,
        )
        return fb, optim

    # --- Sampling ---

    def sample(
        self,
        prompts: str | list[str] | None = None,
        *,
        num_samples: int = 1,
        max_tokens: int = 256,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: list[str] | None = None,
        seed: int | None = None,
        seeds: list[int] | None = None,
        return_prompt_logprobs: bool = False,
        logprobs: int | None = None,
        images: list[bytes] | list[list[bytes]] | None = None,
        return_expert_routing: bool = False,
        prompt_token_ids: list[int] | list[list[int]] | None = None,
        model_input: list[dict] | list[list[dict]] | None = None,
        metrics_type: str = "",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        poll_interval: float = _SAMPLE_POLL_INTERVAL_SECS,
    ) -> list[list[Sample]]:
        """Sample from the current in-memory training weights.

        Generates text using the model's current weights, without
        needing to save a checkpoint first. Per-token logprobs are
        always returned.

        Args:
            prompts: Single prompt string or list of prompts.
                Mutually exclusive with ``prompt_token_ids``.
            num_samples: Number of independent samples per prompt.
            max_tokens: Maximum tokens to generate per sample.
            temperature: Sampling temperature.
            top_p: Nucleus sampling threshold.
            top_k: Top-k sampling (-1 = disabled).
            stop: Stop sequences.
            seed: Random seed (varied per sample automatically).
            seeds: Exact per-prompt/sample seeds. Mutually exclusive with
                ``seed`` and ordered by prompt then sample.
            return_prompt_logprobs: Whether to return prompt token logprobs.
            logprobs: If set to ``K > 0``, request the top-K alternative
                logprobs at each output position (and, when
                ``return_prompt_logprobs=True``, at each prompt position).
                Off by default — enabling it roughly halves server
                throughput for small serialization gain, so it's opt-in.
            images: Optional raw image bytes (PNG / JPEG) for
                multimodal sampling. Accepts ``list[bytes]`` (broadcast
                the same image set to every prompt) or
                ``list[list[bytes]]`` (per-prompt explicit). Bytes
                are sent to the inference backend as image data.
                Most ergonomic source: ``**Qwen35VLRenderer.build_sample_prompt(messages).to_kwargs()``,
                which emits ``{"prompt", "images"}``. The image format is
                inferred from the bytes' magic header, so no separate format
                hint is sent over the wire.
            return_expert_routing: Capture per-token MoE expert routing
                during this sampling call. When available, each
                :class:`Sample` exposes an ``.expert_routing`` object that can
                be round-tripped into training data with
                ``sample.routing_datum_keys(required=True)`` before calling
                ``forward_backward(force_routing_replay=...)`` or
                ``forward_backward(compute_expert_flip_metric=True)``.
            prompt_token_ids: Pre-tokenized prompt(s) — a flat
                ``list[int]`` (one prompt) or ``list[list[int]]`` (one
                entry per prompt). Mutually exclusive with ``prompts``.
                Ids are forwarded verbatim for sampling, bypassing
                server-side tokenization, so the sampled continuation is
                conditioned on exactly these ids (no training/sampling
                tokenization skew). Ids must be valid for this model's
                vocabulary. May be combined with ``images`` using the
                same single-placeholder convention as text prompts: one
                un-expanded ``<|image_pad|>``-style token id per image,
                in ``images`` order — the placeholder count must match
                the image count exactly (a surplus of images is silently
                dropped by the backend otherwise).
            model_input: Training-style chunk list(s) — the same
                ``[{"type": "text", "tokens": [...]}, {"type": "image",
                "data": bytes, ...}, ...]`` shape ``forward_backward``
                accepts, for one prompt (``list[dict]``) or a batch
                (``list[list[dict]]``). Lowered client-side to
                ``prompt_token_ids`` + ``images`` (each image chunk
                becomes one un-expanded placeholder token). Mutually
                exclusive with ``prompts`` / ``prompt_token_ids`` /
                ``images``. ``expected_tokens`` and ``format`` on image
                chunks are accepted and ignored; to validate the
                backend's image expansion against ``expected_tokens``,
                pass ``return_prompt_logprobs=True`` and count
                placeholder ids in the echoed ``Sample.prompt_token_ids``.
            metrics_type: Opaque server-interpreted token enabling extra
                scalar metrics on the response. Unrecognized values are
                silently ignored; when recognized, per-result metrics
                appear on ``Sample.metrics``.
            timeout: Timeout in seconds for the entire operation
                (includes server-side wait for LoRA slot availability).
            poll_interval: Seconds between completion polls once the
                request is in flight. The default (1s) suits ad-hoc
                sampling; tight RL loops that immediately consume the
                results can lower it to shave the post-completion
                notice lag off every step.

        Returns:
            ``list[list[Sample]]`` — outer list is per-prompt,
            inner list is per-sample. Each :class:`Sample` has
            ``.tokens``, ``.text``, ``.logprobs``, and ``.stop_reason``.
        """
        return self.submit_sample(
            prompts,
            num_samples=num_samples,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            seed=seed,
            seeds=seeds,
            return_prompt_logprobs=return_prompt_logprobs,
            logprobs=logprobs,
            images=images,
            return_expert_routing=return_expert_routing,
            prompt_token_ids=prompt_token_ids,
            model_input=model_input,
            metrics_type=metrics_type,
            timeout=timeout,
            poll_interval=poll_interval,
        ).result()

    def submit_sample(
        self,
        prompts: str | list[str] | None = None,
        *,
        num_samples: int = 1,
        max_tokens: int = 256,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: list[str] | None = None,
        seed: int | None = None,
        seeds: list[int] | None = None,
        return_prompt_logprobs: bool = False,
        logprobs: int | None = None,
        images: list[bytes] | list[list[bytes]] | None = None,
        return_expert_routing: bool = False,
        prompt_token_ids: list[int] | list[list[int]] | None = None,
        model_input: list[dict] | list[list[dict]] | None = None,
        metrics_type: str = "",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        poll_interval: float = _SAMPLE_POLL_INTERVAL_SECS,
    ) -> PendingSample:
        """Submit sampling from current training weights without waiting.

        See :meth:`Model.sample` for the full kwarg reference.
        """
        operation_started_at = time.monotonic()
        prompts, prompt_token_ids, images = _resolve_model_input(
            model_input,
            prompts=prompts,
            prompt_token_ids=prompt_token_ids,
            images=images,
            tokenizer=self._tokenizer,
        )
        prompt_list, prompt_dicts = _build_sample_prompt_dicts(
            prompts,
            num_samples=num_samples,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            seed=seed,
            seeds=seeds,
            return_prompt_logprobs=return_prompt_logprobs,
            logprobs=logprobs,
            images=images,
            return_expert_routing=return_expert_routing,
            prompt_token_ids=prompt_token_ids,
        )
        submit_timeout = timeout - (time.monotonic() - operation_started_at)
        if submit_timeout <= 0:
            raise RiverTimeoutError(
                f"Sampling timed out after {timeout}s before submission"
            )
        request_id = self._session._submit_sample_batched_from_training(
            model_id=self._model_id,
            prompts=prompt_dicts,
            metrics_type=metrics_type,
            timeout=submit_timeout,
        )
        remaining_timeout = timeout - (time.monotonic() - operation_started_at)
        if remaining_timeout <= 0:
            raise RiverTimeoutError(
                f"Operation {request_id} timed out after {timeout}s",
                request_id=request_id,
            )
        model_step = self._step

        def parse_result(response: pb2.InferenceResponse) -> list[list[Sample]]:
            return _group_sample_dicts(
                self._session._inference_to_dicts(response),
                num_prompts=len(prompt_list),
                num_samples=num_samples,
                tokenizer=self._tokenizer,
                max_tokens=max_tokens,
                model_step=model_step,
                request_id=request_id,
                return_prompt_logprobs=return_prompt_logprobs,
                return_prompt_token_ids=(
                    return_prompt_logprobs or return_expert_routing
                ),
            )

        return PendingSample(
            request_id=request_id,
            _session=self._session,
            _model_id=self._model_id,
            _timeout=remaining_timeout,
            _poll_interval=poll_interval,
            _parse_result=parse_result,
        )

    def chat_complete(
        self,
        messages: list[dict],
        *,
        timeout: float | None = None,
        **kwargs,
    ) -> ChatCompleteResult:
        """OpenAI-compatible chat completion from current training weights.

        Like ``model.sample()`` but using the OpenAI chat-completions format
        instead of raw prompts.

        Args:
            messages: OpenAI-format messages list
                (e.g. ``[{"role": "user", "content": "Hello"}]``).
            timeout: Timeout in seconds.
            **kwargs: Extra fields for the OpenAI request body
                (e.g. ``max_tokens``, ``temperature``, ``tools``).

        Returns:
            ChatCompleteResult with ``response_json`` (full OpenAI-format
            JSON string) and ``status_code``.
        """
        return self._session._client.chat_complete_from_training(
            messages,
            model_id=self._model_id,
            timeout=timeout,
            **kwargs,
        )

    # --- Weights management ---

    def save_weights(
        self,
        name: str,
        mode: str = "training",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        ttl: datetime.timedelta | None = None,
    ) -> Checkpoint:
        """Save a checkpoint of the current model weights.

        Args:
            name: Checkpoint name (e.g. ``"final"`` or ``"step_000100"``).
            mode: ``"training"`` saves optimizer state (for training
                continuation), ``"inference"`` saves PEFT format only (for
                sampling/inference).
            timeout: Timeout in seconds.
            ttl: Lifetime before the checkpoint is reaped. Applies to explicit
                user-saved checkpoints in both modes; when omitted, the server
                default is 1 year. 1 year is also the maximum — the server
                rejects a longer ``ttl``.

        Returns:
            Checkpoint object with ``river://`` path.
        """
        if mode not in ("training", "inference"):
            raise ValueError(
                f"Invalid mode {mode!r}. Must be 'training' or 'inference'."
            )

        ttl_seconds: int | None = None
        if ttl is not None:
            ttl_seconds = int(ttl.total_seconds())
            if ttl_seconds <= 0:
                raise ValueError("ttl must be positive")

        scoped_name = f"{self._training_run_id}/{name}"
        return self._session._save_weights(
            model_id=self._model_id,
            seq_id=self._next_seq_id(),
            name=scoped_name,
            mode=mode,
            timeout=timeout,
            step=self._step,
            ttl_seconds=ttl_seconds,
        )

    def promote_to_streaming(
        self,
        model: str,
        checkpoint: str | Checkpoint | None = None,
        checkpoint_name: str | None = None,
        timeout: float | None = _DEFAULT_TIMEOUT_SECS,
    ) -> PromotedStreamingReplica:
        """Promote this model's current or saved checkpoint to a stream alias.

        When ``checkpoint`` is omitted, this saves the current weights with
        ``mode="inference"`` using ``checkpoint_name`` or a generated name,
        then asks the control plane to promote that checkpoint asynchronously.
        The ``timeout`` is applied separately to the save and promotion calls,
        not as one end-to-end deadline. Omitted ``checkpoint_name`` values
        create a new server-side inference checkpoint for each call.
        """
        if checkpoint is not None and checkpoint_name is not None:
            raise ValueError("checkpoint_name is only valid when checkpoint is omitted")

        if checkpoint is None:
            save_timeout = _DEFAULT_TIMEOUT_SECS if timeout is None else timeout
            name = checkpoint_name or f"streaming-{uuid.uuid4().hex}"
            checkpoint = self.save_weights(
                name,
                mode="inference",
                timeout=save_timeout,
            )

        return self._session._client.promote_streaming_replica(
            checkpoint,
            model,
            timeout=timeout,
        )

    def load_weights(
        self,
        checkpoint: str | Checkpoint,
        load_optimizer: bool = True,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> None:
        """Load weights from a checkpoint.

        Args:
            checkpoint: A ``river://`` path string or a :class:`Checkpoint` object.
                If a ``Checkpoint`` is passed, its step is restored on the model.
            load_optimizer: Whether to load optimizer state.
            timeout: Timeout in seconds.
        """
        if isinstance(checkpoint, Checkpoint):
            path = checkpoint.path
            self._step = checkpoint.step
        else:
            path = checkpoint

        self._session._load_weights(
            model_id=self._model_id,
            seq_id=self._next_seq_id(),
            path=path,
            load_optimizer=load_optimizer,
            timeout=timeout,
        )


class Session:
    """A training session with GPU allocation."""

    def __init__(
        self,
        client: Client,
        session_id: str,
        stub: pb2_grpc.RiverServiceStub,
        metadata: list[tuple[str, str]],
        before_poll: Callable[[], None] | None = None,
    ):
        self._client = client
        self._session_id = session_id
        self._stub = stub
        self._metadata = metadata
        self._before_poll = before_poll
        self._heartbeat_thread: threading.Thread | None = None
        self._heartbeat_stop = threading.Event()
        self._heartbeat_state_lock = threading.Lock()
        self._heartbeat_last_success = time.monotonic()
        self._heartbeat_last_error: SessionHeartbeatError | None = None
        self._models: list[Model] = []
        self._model_seq_id = 0

    @property
    def _live_stub(self) -> pb2_grpc.RiverServiceStub:
        """Always returns the current stub (follows channel recreation)."""
        return self._client._get_stub()

    @property
    def _live_metadata(self) -> list[tuple[str, str]]:
        """Always returns current metadata."""
        return self._client._get_metadata()

    @property
    def session_id(self) -> str:
        return self._session_id

    def _build_heartbeat_error(
        self,
        error: RiverConnectionError | SessionHeartbeatError,
        *,
        message: str,
    ) -> SessionHeartbeatError:
        if isinstance(error, SessionHeartbeatError):
            return error
        return SessionHeartbeatError(
            message,
            status_code=error.status_code,
            details=error.details,
            original_error=error.original_error,
        )

    def _record_heartbeat_success(self) -> None:
        with self._heartbeat_state_lock:
            self._heartbeat_last_success = time.monotonic()
            self._heartbeat_last_error = None

    def _record_heartbeat_failure(self, error: SessionHeartbeatError) -> None:
        with self._heartbeat_state_lock:
            self._heartbeat_last_error = error

    def _heartbeat_rpc(self, *, timeout: float) -> None:
        req = pb2.SessionHeartbeatRequest(session_id=self._session_id)
        response = self._client._rpc(
            lambda: self._client._get_heartbeat_stub().SessionHeartbeat(
                req,
                metadata=self._client._get_metadata(),
                timeout=timeout,
            ),
            context="Session heartbeat",
        )
        if not response.success:
            raise SessionHeartbeatError("Session heartbeat rejected by server")

    def _attempt_heartbeat(
        self,
        *,
        timeout: float = _HEARTBEAT_RPC_TIMEOUT_SECS,
        max_attempts: int = _HEARTBEAT_MAX_ATTEMPTS,
    ) -> bool:
        last_error: SessionHeartbeatError | None = None
        backoff = _HEARTBEAT_RETRY_BACKOFF_SECS

        for attempt in range(max_attempts):
            try:
                self._heartbeat_rpc(timeout=timeout)
                self._record_heartbeat_success()
                return True
            except (RiverConnectionError, SessionHeartbeatError) as error:
                last_error = self._build_heartbeat_error(
                    error,
                    message="Session heartbeat failed",
                )
                if last_error.status_code in _TRANSIENT_GRPC_STATUS_CODES:
                    self._client._reset_heartbeat_channel()

            if attempt + 1 == max_attempts:
                break
            if self._heartbeat_stop.wait(backoff):
                return False
            backoff = min(backoff * 2, timeout)

        if last_error is not None:
            self._record_heartbeat_failure(last_error)
        return False

    def _check_heartbeat_health(self, *, request_id: str | None = None) -> None:
        with self._heartbeat_state_lock:
            last_success = self._heartbeat_last_success
            last_error = self._heartbeat_last_error

        if last_error is None:
            return

        silence_secs = time.monotonic() - last_success

        # Transport-level heartbeat failures (the service is briefly unreachable,
        # e.g. during a rollout) get a much longer tolerance window than true
        # session rejections — a rejected heartbeat means the server is up and
        # it has explicitly lost our session, which cannot be recovered.
        tolerance = (
            _HEARTBEAT_UNHEALTHY_AFTER_TRANSPORT_SECS
            if last_error.status_code in _TRANSIENT_GRPC_STATUS_CODES
            else _HEARTBEAT_UNHEALTHY_AFTER_SECS
        )
        if silence_secs < tolerance:
            return

        request_context = f" while waiting for {request_id}" if request_id else ""
        raise SessionHeartbeatError(
            f"Session heartbeat lost{request_context} after {silence_secs:.1f}s",
            status_code=last_error.status_code,
            details=last_error.details or str(last_error),
            original_error=last_error.original_error or last_error,
        )

    def _start_heartbeat(self, interval: float = _HEARTBEAT_INTERVAL_SECS) -> None:
        """Start background heartbeat thread."""

        def heartbeat_loop() -> None:
            next_heartbeat = time.monotonic() + interval

            while True:
                now = time.monotonic()
                wait_time = max(0, next_heartbeat - now)

                if self._heartbeat_stop.wait(wait_time):
                    break

                next_heartbeat = time.monotonic() + interval

                self._attempt_heartbeat()

        self._heartbeat_thread = threading.Thread(target=heartbeat_loop, daemon=True)
        self._heartbeat_thread.start()

    def _stop_heartbeat(self) -> None:
        """Stop background heartbeat thread."""
        self._heartbeat_stop.set()
        heartbeat = self._heartbeat_thread
        if heartbeat is None or heartbeat.ident is None:
            return
        heartbeat.join(timeout=_HEARTBEAT_RPC_TIMEOUT_SECS + 1.0)
        if heartbeat.is_alive():
            raise SessionHeartbeatError(
                "Session heartbeat did not stop before cleanup completed"
            )

    def _unload_all_models(self) -> None:
        """Unload all models created in this session."""
        cleanup_errors: list[BaseException] = []
        for model in self._models:
            try:
                req = pb2.UnloadModelRequest(model_id=model.model_id)
                response = self._client._rpc(
                    lambda: self._live_stub.UnloadModel(
                        req, metadata=self._live_metadata
                    ),
                    context="Unloading model",
                )
                self._wait_for_future(
                    response.request_id,
                    timeout=_DEFAULT_TIMEOUT_SECS,
                    model_id=model.model_id,
                )
            except BaseException as error:
                cleanup_errors.append(error)
        self._models.clear()
        if cleanup_errors:
            first = cleanup_errors[0]
            for error in cleanup_errors[1:]:
                first.add_note(
                    f"River model unload also failed: {type(error).__name__}: {error}"
                )
            raise first

    def attest_training_data(
        self,
        artifacts: list[TrainingDataArtifact],
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> TrainingDataAttestation:
        """Ask the API to hash source artifacts and retain their manifest.

        The source bytes are discarded by the API after hashing. Pass the
        result to :meth:`create_model` to make the server fail closed before
        every forward/backward request if that manifest disappears or no longer
        belongs to the model's session.
        """
        proto_artifacts: list[pb2.TrainingDataArtifact] = []
        for artifact in artifacts:
            if not isinstance(artifact, TrainingDataArtifact):
                raise TypeError("artifacts must contain TrainingDataArtifact values")
            if not isinstance(artifact.content, bytes):
                raise TypeError("TrainingDataArtifact.content must be bytes")
            proto_artifacts.append(
                pb2.TrainingDataArtifact(
                    name=artifact.name,
                    expected_sha256=artifact.expected_sha256,
                    content=artifact.content,
                )
            )

        response = self._client._rpc_with_retry(
            lambda: self._live_stub.CreateTrainingDataAttestation(
                pb2.CreateTrainingDataAttestationRequest(
                    session_id=self._session_id,
                    artifacts=proto_artifacts,
                ),
                metadata=self._live_metadata,
                timeout=timeout,
            ),
            context="Creating training-data attestation",
            heartbeat_check=self._check_heartbeat_health,
        )
        return TrainingDataAttestation(
            training_data_attestation_id=response.training_data_attestation_id,
            artifacts=[
                AttestedTrainingDataArtifact(
                    name=artifact.name,
                    sha256=artifact.sha256,
                    size_bytes=artifact.size_bytes,
                )
                for artifact in response.artifacts
            ],
        )

    def create_model(
        self,
        base_model: str,
        lora: LoraConfig,
        tokenizer: str | Any | None = None,
        checkpoint: str | Checkpoint | None = None,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        training_data_attestation: TrainingDataAttestation | str | None = None,
    ) -> Model:
        """Create a new model for training.

        Args:
            base_model: Base model name (e.g., "Qwen/Qwen3.6-35B-A3B-FP8")
            lora: LoRA configuration for the run (required). River training
                is LoRA-only — no base model supports full fine-tuning — so
                the server rejects ``create_model`` without one.
            tokenizer: Tokenizer name (defaults to base_model) or an already-loaded
                tokenizer object
            checkpoint: Optional checkpoint to load after creation. Can be a
                ``river://`` path string or a :class:`Checkpoint` object.
                If a ``Checkpoint`` is passed, its step is restored and
                ``load_optimizer`` is set automatically based on checkpoint type.
            timeout: Timeout in seconds
            training_data_attestation: Optional server-verified source-artifact
                manifest. When supplied, the API rejects forward/backward
                requests if its manifest is missing or no longer belongs to
                this session.

        Returns:
            Model object for training
        """
        if lora is None:
            raise ValueError(
                "lora is required: River training is LoRA-only (no base "
                "model supports full fine-tuning) — pass e.g. "
                "river.LoraConfig(rank=16)"
            )

        self._model_seq_id += 1

        # Build request
        req = pb2.CreateModelRequest(
            session_id=self._session_id,
            model_seq_id=self._model_seq_id,
            base_model=base_model,
        )

        if isinstance(training_data_attestation, TrainingDataAttestation):
            req.training_data_attestation_id = (
                training_data_attestation.training_data_attestation_id
            )
        elif isinstance(training_data_attestation, str):
            req.training_data_attestation_id = training_data_attestation
        elif training_data_attestation is not None:
            raise TypeError(
                "training_data_attestation must be a TrainingDataAttestation, str, or None"
            )

        req.lora_config.CopyFrom(
            pb2.LoraConfig(
                rank=lora.rank,
                train_attn=lora.train_attn,
                train_mlp=lora.train_mlp,
                train_unembed=lora.train_unembed,
            )
        )
        if lora.seed is not None:
            req.lora_config.seed = lora.seed

        # Send request and wait for result
        response = self._client._rpc_with_retry(
            lambda: self._live_stub.CreateModel(req, metadata=self._live_metadata),
            context="Creating model",
            heartbeat_check=self._check_heartbeat_health,
        )
        result = self._wait_for_future(response.request_id, timeout=timeout)

        if result.WhichOneof("response") != "create_model":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        create_model_result = result.create_model

        tok = load_tokenizer(tokenizer, base_model=base_model)

        model = Model(
            session=self,
            model_id=create_model_result.model_id,
            training_run_id=create_model_result.training_run_id,
            base_model=base_model,
            tokenizer=tok,
        )
        self._models.append(model)

        # Load checkpoint if provided
        if checkpoint is not None:
            if isinstance(checkpoint, Checkpoint):
                load_optimizer = checkpoint.checkpoint_type == "training"
                model.load_weights(
                    checkpoint, load_optimizer=load_optimizer, timeout=timeout
                )
            else:
                # String path: default to loading optimizer
                model.load_weights(checkpoint, load_optimizer=True, timeout=timeout)

        return model

    def sample(
        self,
        prompts: str | list[str] | None = None,
        *,
        base_model: str,
        checkpoint: str | Checkpoint | None = None,
        num_samples: int = 1,
        max_tokens: int = 256,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: list[str] | None = None,
        seed: int | None = None,
        return_prompt_logprobs: bool = False,
        logprobs: int | None = None,
        return_expert_routing: bool = False,
        images: list[bytes] | list[list[bytes]] | None = None,
        prompt_token_ids: list[int] | list[list[int]] | None = None,
        model_input: list[dict] | list[list[dict]] | None = None,
        tokenizer: Any | None = None,
        metrics_type: str = "",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> list[list[Sample]]:
        """Sample from a base model or checkpoint.

        When ``checkpoint`` is provided, the server loads the LoRA from the
        saved checkpoint, generates text, then unloads.

        Args:
            prompts: Single prompt string or list of prompts.
                Mutually exclusive with ``prompt_token_ids``.
            base_model: Base model name
                (e.g. ``"Qwen/Qwen3.6-35B-A3B-FP8"``).
            checkpoint: Optional ``river://`` path or :class:`Checkpoint` object.
                If provided, samples from that checkpoint's LoRA weights.
            num_samples: Number of independent samples per prompt.
            max_tokens: Maximum tokens to generate per sample.
            temperature: Sampling temperature.
            top_p: Nucleus sampling threshold.
            top_k: Top-k sampling (-1 = disabled).
            stop: Stop sequences.
            seed: Random seed (varied per sample automatically).
            return_prompt_logprobs: Whether to return prompt token logprobs.
            logprobs: If set to ``K > 0``, request the top-K alternative
                logprobs at each position. Off by default — enabling it
                roughly halves server throughput.
            images: Optional raw image bytes for multimodal sampling.
                See :meth:`Model.sample` for the per-prompt vs.
                broadcast semantics.
            prompt_token_ids: Pre-tokenized prompt(s); mutually exclusive
                with ``prompts``. See :meth:`Model.sample` for details.
            model_input: Training-style chunk list(s); mutually exclusive
                with ``prompts`` / ``prompt_token_ids`` / ``images``.
                See :meth:`Model.sample` for details.
            tokenizer: Optional already-loaded tokenizer. Passing this avoids
                repeated Hugging Face cache/network resolution in tight loops.
            metrics_type: Opaque server-interpreted token enabling extra
                scalar metrics on the response. Unrecognized values are
                silently ignored; when recognized, per-result metrics
                appear on ``Sample.metrics``.
            timeout: Timeout in seconds.

        Returns:
            ``list[list[Sample]]`` — outer list is per-prompt,
            inner list is per-sample.
        """
        return self.submit_sample(
            prompts,
            base_model=base_model,
            checkpoint=checkpoint,
            num_samples=num_samples,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            seed=seed,
            return_prompt_logprobs=return_prompt_logprobs,
            logprobs=logprobs,
            return_expert_routing=return_expert_routing,
            images=images,
            prompt_token_ids=prompt_token_ids,
            model_input=model_input,
            tokenizer=tokenizer,
            metrics_type=metrics_type,
            timeout=timeout,
        ).result()

    def submit_sample(
        self,
        prompts: str | list[str] | None = None,
        *,
        base_model: str,
        checkpoint: str | Checkpoint | None = None,
        num_samples: int = 1,
        max_tokens: int = 256,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: list[str] | None = None,
        seed: int | None = None,
        return_prompt_logprobs: bool = False,
        logprobs: int | None = None,
        return_expert_routing: bool = False,
        images: list[bytes] | list[list[bytes]] | None = None,
        prompt_token_ids: list[int] | list[list[int]] | None = None,
        model_input: list[dict] | list[list[dict]] | None = None,
        tokenizer: Any | None = None,
        metrics_type: str = "",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> PendingSample:
        """Submit sampling from a base model or checkpoint without waiting.

        See :meth:`Session.sample` for the full kwarg reference.
        """
        operation_started_at = time.monotonic()
        tokenizer = load_tokenizer(tokenizer, base_model=base_model)
        prompts, prompt_token_ids, images = _resolve_model_input(
            model_input,
            prompts=prompts,
            prompt_token_ids=prompt_token_ids,
            images=images,
            tokenizer=tokenizer,
        )
        checkpoint_path: str | None = None
        checkpoint_step: int = 0
        if checkpoint is not None:
            if isinstance(checkpoint, Checkpoint):
                checkpoint_path = checkpoint.path
                checkpoint_step = checkpoint.step
            else:
                checkpoint_path = checkpoint

        prompt_list, prompt_dicts = _build_sample_prompt_dicts(
            prompts,
            num_samples=num_samples,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            seed=seed,
            return_prompt_logprobs=return_prompt_logprobs,
            logprobs=logprobs,
            return_expert_routing=return_expert_routing,
            images=images,
            prompt_token_ids=prompt_token_ids,
        )

        submit_timeout = timeout - (time.monotonic() - operation_started_at)
        if submit_timeout <= 0:
            raise RiverTimeoutError(
                f"Sampling timed out after {timeout}s before submission"
            )
        if checkpoint_path is not None:
            request_id = self._submit_sample_from_checkpoint(
                checkpoint_path=checkpoint_path,
                base_model=base_model,
                prompts=prompt_dicts,
                metrics_type=metrics_type,
                timeout=submit_timeout,
            )
        else:
            request_id = self._submit_generate_from_base_model(
                base_model=base_model,
                prompts=prompt_dicts,
                metrics_type=metrics_type,
                timeout=submit_timeout,
            )

        def parse_result(response: pb2.InferenceResponse) -> list[list[Sample]]:
            return _group_sample_dicts(
                self._inference_to_dicts(response),
                num_prompts=len(prompt_list),
                num_samples=num_samples,
                tokenizer=tokenizer,
                max_tokens=max_tokens,
                model_step=checkpoint_step,
                request_id=request_id,
                return_prompt_logprobs=return_prompt_logprobs,
                return_prompt_token_ids=(
                    return_prompt_logprobs or return_expert_routing
                ),
            )

        remaining_timeout = timeout - (time.monotonic() - operation_started_at)
        if remaining_timeout <= 0:
            raise RiverTimeoutError(
                f"Operation {request_id} timed out after {timeout}s",
                request_id=request_id,
            )
        return PendingSample(
            request_id=request_id,
            _session=self,
            _timeout=remaining_timeout,
            _poll_interval=_SAMPLE_POLL_INTERVAL_SECS,
            _parse_result=parse_result,
        )

    # --- Internal methods ---

    def _wait_for_future(
        self,
        request_id: str,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        poll_interval: float = 0.01,
        *,
        model_id: str | None = None,
        retry_connection_errors: bool = True,
        before_poll: Callable[[], None] | None = None,
    ) -> pb2.RetrieveFutureResponse:
        """Poll for async operation result."""
        deadline = time.monotonic() + timeout
        next_heartbeat_poll = time.monotonic() + _HEARTBEAT_POLL_INTERVAL_SECS
        poll_retry_sleep = _POLL_RETRY_INITIAL_SLEEP_SECS
        poll_retries = 0

        while True:
            self._check_heartbeat_health(request_id=request_id)

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RiverTimeoutError(
                    f"Operation {request_id} timed out after {timeout}s",
                    request_id=request_id,
                )

            if time.monotonic() >= next_heartbeat_poll:
                self._attempt_heartbeat()
                next_heartbeat_poll = time.monotonic() + _HEARTBEAT_POLL_INTERVAL_SECS

            req = pb2.RetrieveFutureRequest(request_id=request_id)
            if model_id is not None:
                req.model_id = model_id
            poll_guard = before_poll or self._before_poll
            if poll_guard is not None:
                poll_guard()
            try:
                response = self._client._rpc(
                    lambda: self._live_stub.RetrieveFuture(
                        req,
                        metadata=self._live_metadata,
                        timeout=remaining,
                    ),
                    context="Retrieving operation result",
                )
            except RiverConnectionError as error:
                if not retry_connection_errors:
                    raise
                # Terminal errors never clear by retrying (auth / identity /
                # argument / state) — surface them immediately.
                if error.status_code in _POLL_TERMINAL_STATUS_CODES:
                    raise
                # UNAVAILABLE / DEADLINE_EXCEEDED: the request is still in flight
                # server-side (server rolling / overloaded), so wait it out with
                # no consecutive cap. Everything else (INTERNAL/UNKNOWN/ABORTED/
                # RESOURCE_EXHAUSTED, incl. HTTP/2 stream resets) is also retried —
                # the poll is idempotent — but bounded, so a deterministically
                # failing response surfaces instead of hanging until the timeout.
                if not _is_transient_connection_error(error):
                    poll_retries += 1
                    if poll_retries > _POLL_MAX_RETRIES:
                        raise
                time.sleep(min(poll_retry_sleep, max(0.0, deadline - time.monotonic())))
                poll_retry_sleep = min(poll_retry_sleep * 2, _POLL_RETRY_MAX_SLEEP_SECS)
                continue
            poll_retry_sleep = _POLL_RETRY_INITIAL_SLEEP_SECS
            poll_retries = 0

            response_type = response.WhichOneof("response")

            if response_type == "try_again":
                time.sleep(min(poll_interval, max(0.0, deadline - time.monotonic())))
                continue
            if response_type == "failed":
                error = response.failed
                raise RiverError(f"{error.error_category}: {error.message}")

            return response

    @staticmethod
    def _parse_logprobs(fb_result) -> list | None:
        """Parse per-sample logprobs from a ForwardBackwardOutput proto.

        The logprobs are stored as Nested-encoded bytes in loss_fn_outputs["logprobs"].
        Returns a list of numpy arrays (one per sample in the batch), or None
        if logprobs are not present.
        """
        if "logprobs" not in fb_result.loss_fn_outputs:
            return None

        logprobs_tensor = fb_result.loss_fn_outputs["logprobs"]
        if not logprobs_tensor.data:
            return None

        try:
            decoded = _nested_from_bytes(logprobs_tensor.data)

            # Normalize to list of 1D arrays for consistent interface
            if isinstance(decoded, np.ndarray):
                if decoded.ndim == 2:
                    return [decoded[i] for i in range(decoded.shape[0])]
                return [decoded]

            if isinstance(decoded, list):
                return decoded

            return None
        except Exception:
            return None

    @staticmethod
    def _forward_backward_result(raw: pb2.RetrieveFutureResponse) -> ForwardResult:
        """Parse a resolved forward / forward-backward future."""
        if raw.WhichOneof("response") != "forward_backward":
            raise RiverError(f"Unexpected response type: {raw.WhichOneof('response')}")
        fb_result = raw.forward_backward
        return ForwardResult(
            metrics=dict(fb_result.metrics),
            logprobs=Session._parse_logprobs(fb_result),
        )

    @staticmethod
    def _optim_step_result(raw: pb2.RetrieveFutureResponse) -> OptimStepResult:
        """Parse a resolved optimizer-step future."""
        if raw.WhichOneof("response") != "optim_step":
            raise RiverError(f"Unexpected response type: {raw.WhichOneof('response')}")
        return OptimStepResult(metrics=dict(raw.optim_step.metrics))

    def _encode_datum(self, sample: dict) -> pb2.Datum:
        """Encode a training sample to Datum protobuf.

        Two wire forms are supported:

        * **Flat / text-only** — sample has ``input_ids`` (and usually
          ``weights``/``attention_mask``); every value is numpy-ified
          before Nested encoding. This is the historical contract used
          by ``forward_backward(loss_fn=...)`` for text samples.

        * **Chunked / multimodal** — sample has ``model_input``
          (a list of chunk dicts with ``{"type": "text"|"image", ...}``)
          plus ``weights``. Image bytes ride through as ``uint8``
          arrays since the Nested codec lacks a native ``bytes`` type;
          the worker materializes chunks back into ``input_ids`` +
          ``pixel_values`` server-side.

        Additional fields (``target_tokens``, ``old_logprobs``,
        ``advantages`` for RL losses) are passed through in both
        forms.
        """
        if "model_input" in sample:
            return self._encode_chunked_datum(sample)
        return self._encode_flat_datum(sample)

    def _encode_flat_datum(self, sample: dict) -> pb2.Datum:
        """Encode the legacy flat (text-only) training datum.

        Each value is converted to a numpy array (with dtype inference
        on Python lists) so Nested produces compact array payloads.
        """
        input_ids = sample.get("input_ids")
        if input_ids is None:
            raise ValueError(
                "Sample must have 'input_ids' (or 'model_input' for multimodal samples)"
            )

        datum_dict: dict = {}
        for key, value in sample.items():
            if value is None:
                continue
            if isinstance(value, (bytes, bytearray, memoryview)):
                # Nested has no native ``bytes`` type and ``np.array(b)``
                # produces a ``|S<N>`` dtype the codec rejects. Convert
                # to a 1-D ``uint8`` array (mirroring the image-chunks
                # workaround); the worker side calls ``.tobytes()`` to
                # recover the original bytes.
                value = np.frombuffer(bytes(value), dtype=np.uint8)
            elif not isinstance(value, np.ndarray):
                if isinstance(value, list):
                    # Infer dtype from the first scalar leaf: float →
                    # float32, else int64.  Descend through nesting so a
                    # 2-D list (e.g. top-K cross_entropy ``weights`` of
                    # shape [T, K]) is typed by its elements, not
                    # mis-bucketed to int64 (which would silently
                    # truncate fractional weights to zero).
                    leaf = value[0] if value else None
                    while isinstance(leaf, list):
                        leaf = leaf[0] if leaf else None
                    if isinstance(leaf, float):
                        value = np.array(value, dtype=np.float32)
                    else:
                        value = np.array(value, dtype=np.int64)
                else:
                    value = np.array(value)
            datum_dict[key] = value

        if not isinstance(datum_dict["input_ids"], np.ndarray):
            datum_dict["input_ids"] = np.array(datum_dict["input_ids"], dtype=np.int64)

        if "attention_mask" not in datum_dict:
            datum_dict["attention_mask"] = np.ones_like(datum_dict["input_ids"])

        encoded = _nested_to_bytes(datum_dict)
        return pb2.Datum(data=encoded)

    def _encode_chunked_datum(self, sample: dict) -> pb2.Datum:
        """Encode a multimodal (chunked) training datum.

        ``model_input`` is a list of dicts that the Nested codec walks
        natively (``_TAG_LIST`` of ``_TAG_DICT``). ``ImageChunk.data``
        is converted from ``bytes`` to a 1-D ``uint8`` array since
        Nested has no native ``bytes`` type; the worker reconstitutes
        the bytes via ``.tobytes()`` before handing them to PIL.
        """
        chunks = sample["model_input"]
        if not isinstance(chunks, list):
            raise ValueError(
                f"'model_input' must be a list of chunk dicts; got {type(chunks)!r}"
            )

        wire_chunks: list[dict] = []
        for idx, chunk in enumerate(chunks):
            if not isinstance(chunk, dict) or "type" not in chunk:
                raise ValueError(
                    f"chunk[{idx}] must be a dict with a 'type' field; got {chunk!r}"
                )
            ctype = chunk["type"]
            if ctype == "text":
                tokens = chunk.get("tokens")
                if tokens is None:
                    raise ValueError(f"text chunk[{idx}] missing 'tokens'")
                wire_chunks.append(
                    {
                        "type": "text",
                        "tokens": np.asarray(tokens, dtype=np.int64),
                    }
                )
            elif ctype == "image":
                data = chunk.get("data")
                if isinstance(data, (bytes, bytearray)):
                    data_arr = np.frombuffer(bytes(data), dtype=np.uint8)
                elif isinstance(data, np.ndarray) and data.dtype == np.uint8:
                    data_arr = data
                else:
                    raise ValueError(
                        f"image chunk[{idx}] 'data' must be bytes or "
                        f"uint8 ndarray; got {type(data)!r}"
                    )
                fmt = chunk.get("format", "png")
                expected = int(chunk.get("expected_tokens", 0))
                wire_chunks.append(
                    {
                        "type": "image",
                        "data": data_arr,
                        "format": str(fmt),
                        "expected_tokens": np.asarray(expected, dtype=np.int64),
                    }
                )
            else:
                raise ValueError(
                    f"chunk[{idx}] has unsupported type {ctype!r} "
                    "(expected 'text' or 'image')"
                )

        datum_dict: dict = {"model_input": wire_chunks}
        for key, value in sample.items():
            if key == "model_input" or value is None:
                continue
            if isinstance(value, (bytes, bytearray, memoryview)):
                value = np.frombuffer(bytes(value), dtype=np.uint8)
            elif not isinstance(value, np.ndarray):
                if isinstance(value, list):
                    if value and isinstance(value[0], float):
                        value = np.array(value, dtype=np.float32)
                    else:
                        value = np.array(value, dtype=np.int64)
                else:
                    value = np.array(value)
            datum_dict[key] = value

        encoded = _nested_to_bytes(datum_dict)
        return pb2.Datum(data=encoded)

    def _forward(
        self,
        model_id: str,
        seq_id: int,
        data: list[dict],
        loss_fn: str,
        loss_config: dict[str, float],
        timeout: float,
    ) -> ForwardResult:
        """Execute forward pass."""
        if not self._models:
            raise RiverError("No models created in session")

        req = pb2.ForwardRequest(
            model_id=model_id,
            seq_id=seq_id,
            forward_input=pb2.ForwardBackwardInput(
                data=[self._encode_datum(d) for d in data],
                loss_fn=loss_fn,
                loss_fn_config=loss_config,
            ),
        )

        response = self._client._rpc_with_retry(
            lambda: self._live_stub.Forward(req, metadata=self._live_metadata),
            context="Forward pass",
            heartbeat_check=self._check_heartbeat_health,
        )
        result = self._wait_for_future(
            response.request_id,
            timeout=timeout,
            model_id=model_id,
        )
        return self._forward_backward_result(result)

    def _submit_forward_backward(
        self,
        model_id: str,
        seq_id: int,
        data: list[dict],
        loss_fn: str,
        loss_config: dict[str, float],
        *,
        timeout: float | None = None,
        gradient_accumulation: bool = False,
        init_gradients: bool = True,
        compute_expert_flip_metric: bool = False,
        force_routing_replay: bool = False,
    ) -> str:
        """Fire forward+backward RPC without waiting. Returns request_id."""
        request = self._build_forward_backward_request(
            model_id=model_id,
            seq_id=seq_id,
            loss_fn=loss_fn,
            loss_config=loss_config,
            gradient_accumulation=gradient_accumulation,
            init_gradients=init_gradients,
            compute_expert_flip_metric=compute_expert_flip_metric,
            force_routing_replay=force_routing_replay,
        )
        plan = self._plan_forward_backward_request(request, data)
        if plan.maximum_total_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
            raise RiverError(
                "forward_backward batch exceeds the 1 GiB upload limit; use "
                "Model.forward_backward() so the client can submit accumulated "
                "sub-batches sequentially"
            )
        request = self._single_forward_backward_chunk(request, data, plan)
        return self._submit_forward_backward_request(
            request,
            request_size=request.ByteSize(),
            timeout=timeout,
        )

    def _build_forward_backward_request(
        self,
        *,
        model_id: str,
        seq_id: int,
        loss_fn: str,
        loss_config: dict[str, float],
        gradient_accumulation: bool,
        init_gradients: bool,
        compute_expert_flip_metric: bool,
        force_routing_replay: bool,
    ) -> pb2.ForwardBackwardRequest:
        """Build a forward/backward request header without datum payloads."""
        _require_ids_only_routing_replay(force_routing_replay)
        if not self._models:
            raise RiverError("No models created in session")

        fb_kwargs: dict = dict(
            loss_fn=loss_fn,
            loss_fn_config=loss_config,
            gradient_accumulation=gradient_accumulation,
            init_gradients=init_gradients,
        )
        # Routing-override / flip-metric flags ride on ForwardBackwardInput
        # (proto fields 8 & 7). Only include when set so a default request
        # stays clean. The wire field remains a string for protocol stability;
        # this client exposes a boolean and sends the only supported replay
        # mode, ``"ids"``, when enabled.
        if force_routing_replay:
            fb_kwargs["force_routing_replay"] = "ids"
        if compute_expert_flip_metric:
            fb_kwargs["compute_expert_flip_metric"] = True

        return pb2.ForwardBackwardRequest(
            model_id=model_id,
            seq_id=seq_id,
            forward_backward_input=pb2.ForwardBackwardInput(**fb_kwargs),
        )

    def _plan_forward_backward_request(
        self,
        request: pb2.ForwardBackwardRequest,
        data: list[dict],
    ) -> _ForwardBackwardRequestPlan:
        """Measure raw samples without constructing one batch-sized protobuf.

        Planning and chunk construction both encode each datum. That intentional
        two-pass trade-off keeps peak memory bounded by the raw batch plus one
        sub-batch instead of retaining a second, fully encoded multi-GiB batch.
        """
        return _forward_backward_request_plan(
            request, (self._encode_datum(datum) for datum in data)
        )

    def _single_forward_backward_chunk(
        self,
        request: pb2.ForwardBackwardRequest,
        data: list[dict],
        plan: _ForwardBackwardRequestPlan,
    ) -> pb2.ForwardBackwardRequest:
        """Build the one expected chunk and verify planning did not split it."""
        chunks = self._iter_forward_backward_sub_batches(request, data, plan)
        chunk, _ = next(chunks)
        if next(chunks, None) is not None:
            raise RiverError(
                "forward_backward request unexpectedly split into sub-batches"
            )
        return chunk

    def _submit_forward_backward_request(
        self,
        request: pb2.ForwardBackwardRequest,
        *,
        request_size: int | None = None,
        timeout: float | None,
    ) -> str:
        """Send an already encoded forward/backward request."""
        req = self._maybe_upload_request(request, request_size=request_size)
        response = self._client._rpc_with_retry(
            lambda: self._live_stub.ForwardBackward(
                req, metadata=self._live_metadata, timeout=timeout
            ),
            context="Forward-backward pass",
            heartbeat_check=self._check_heartbeat_health,
        )
        return response.request_id

    def _iter_forward_backward_sub_batches(
        self,
        request: pb2.ForwardBackwardRequest,
        data: list[dict],
        plan: _ForwardBackwardRequestPlan,
    ) -> Iterator[tuple[pb2.ForwardBackwardRequest, int]]:
        """Encode raw samples into request-sized chunks one at a time."""
        source_input = request.forward_backward_input

        def new_chunk() -> pb2.ForwardBackwardRequest:
            chunk = pb2.ForwardBackwardRequest(
                model_id=request.model_id,
                forward_backward_input=_forward_backward_input_without_data(
                    source_input
                ),
            )
            if request.HasField("seq_id"):
                chunk.seq_id = request.seq_id
            return chunk

        data_iterator = iter(data)
        chunk = new_chunk()
        chunk_datum_field_size = 0
        chunk_datum_count = 0
        if not plan.datum_field_sizes:
            yield chunk, 0
            return
        for planned_datum_field_size in plan.datum_field_sizes:
            try:
                raw_datum = next(data_iterator)
            except StopIteration as error:
                raise RiverError(
                    "forward_backward data changed while the request was being prepared"
                ) from error
            datum = self._encode_datum(raw_datum)
            datum_field_size = _length_delimited_field_size(datum.ByteSize())
            if datum_field_size != planned_datum_field_size:
                raise RiverError(
                    "forward_backward data changed while the request was being prepared"
                )
            candidate_size = _forward_backward_request_size(
                chunk,
                static_input_size=plan.static_input_size,
                datum_field_size=chunk_datum_field_size + datum_field_size,
                maximum_sequence_id_size=True,
            )
            if candidate_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
                if chunk_datum_count == 0:
                    raise RiverError(
                        "A single forward_backward datum exceeds the client "
                        f"sub-batch limit of {_FORWARD_BACKWARD_SUB_BATCH_BYTES} bytes"
                    )
                yield chunk, chunk_datum_count
                chunk = new_chunk()
                chunk_datum_field_size = 0
                chunk_datum_count = 0
                candidate_size = _forward_backward_request_size(
                    chunk,
                    static_input_size=plan.static_input_size,
                    datum_field_size=datum_field_size,
                    maximum_sequence_id_size=True,
                )
                if candidate_size > _FORWARD_BACKWARD_SUB_BATCH_BYTES:
                    raise RiverError(
                        "A single forward_backward datum exceeds the client "
                        f"sub-batch limit of {_FORWARD_BACKWARD_SUB_BATCH_BYTES} bytes"
                    )
            chunk.forward_backward_input.data.append(datum)
            chunk_datum_field_size += datum_field_size
            chunk_datum_count += 1

        if chunk_datum_count:
            yield chunk, chunk_datum_count

        try:
            next(data_iterator)
        except StopIteration:
            return
        raise RiverError(
            "forward_backward data changed while the request was being prepared"
        )

    def _maybe_upload_request(
        self,
        req: pb2.ForwardBackwardRequest,
        *,
        request_size: int | None = None,
    ) -> pb2.ForwardBackwardRequest:
        """Ship a large request body over parallel connections.

        A single gRPC message is bound to one TCP connection, whose kernel
        send buffer caps throughput at roughly one bufferful per round trip.
        Bodies at or above ``RIVER_UPLOAD_THRESHOLD_BYTES`` are serialized
        once, split into chunks, uploaded concurrently over the client's
        upload connection pool, and replaced with a thin request referencing
        the upload; the server assembles the identical bytes and processes
        them exactly as an inline request. Small bodies, and servers that
        predate the upload API (UNIMPLEMENTED), use the inline path. Set
        ``RIVER_REQUIRE_CHUNKED_UPLOAD=1`` to fail instead of falling back
        inline when a request crosses the threshold.
        """
        if self._client._chunked_upload_unsupported:
            if _REQUIRE_CHUNKED_UPLOAD:
                raise RiverConnectionError(
                    "Chunked upload is required but this API server does not support it",
                    status_code="UNIMPLEMENTED",
                )
            return req
        size = req.ByteSize() if request_size is None else request_size
        if size < _UPLOAD_THRESHOLD_BYTES:
            return req
        chunk_bytes = max(_UPLOAD_CHUNK_BYTES, -(-size // _UPLOAD_MAX_CHUNKS))
        chunk_count = -(-size // chunk_bytes)
        try:
            created = self._client._rpc(
                lambda: self._live_stub.CreateUpload(
                    pb2.CreateUploadRequest(
                        model_id=req.model_id,
                        total_size=size,
                        chunk_count=chunk_count,
                    ),
                    metadata=self._live_metadata,
                ),
                context="Creating upload session",
            )
        except RiverConnectionError as error:
            if error.status_code == "UNIMPLEMENTED":
                self._client._chunked_upload_unsupported = True
                if _REQUIRE_CHUNKED_UPLOAD:
                    raise
                return req
            if _REQUIRE_CHUNKED_UPLOAD:
                raise
            # Chunking is an optimization: a failed session bootstrap (e.g.
            # RESOURCE_EXHAUSTED from leaked sessions, or a transient
            # transport error) must never fail a request the inline path can
            # still carry.
            _logger.warning(
                "Chunked upload unavailable (%s); sending request inline", error
            )
            return req
        body = req.SerializeToString()
        parallelism = max(
            1,
            min(
                chunk_count,
                _UPLOAD_PARALLELISM,
                created.max_parallelism or _UPLOAD_PARALLELISM,
            ),
        )
        stubs = self._client._get_upload_stubs(parallelism)

        def send(index: int) -> None:
            chunk = pb2.UploadChunkRequest(
                upload_id=created.upload_id,
                chunk_index=index,
                data=body[index * chunk_bytes : (index + 1) * chunk_bytes],
            )
            for attempt in range(_UPLOAD_CHUNK_RETRIES):
                try:
                    stubs[index % parallelism].UploadChunk(
                        chunk,
                        metadata=self._live_metadata,
                        timeout=_UPLOAD_CHUNK_TIMEOUT_SECS,
                    )
                    return
                except grpc.RpcError as error:
                    if attempt + 1 == _UPLOAD_CHUNK_RETRIES:
                        raise RiverConnectionError.from_grpc_error(
                            error, f"Uploading chunk {index}"
                        ) from None
                    time.sleep(min(2.0 * (attempt + 1), 8.0))

        # More workers than connections: chunks assigned to the same
        # connection run as concurrent HTTP/2 streams, so one chunk's wire
        # transfer overlaps the previous chunk's server-side storage write.
        # With one stream per connection the pipe would sit idle for the
        # duration of every storage write.
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=chunk_count) as pool:
                list(pool.map(send, range(chunk_count)))
        except RiverConnectionError as error:
            if _REQUIRE_CHUNKED_UPLOAD:
                raise
            # Same principle as above; the abandoned session expires on TTL.
            _logger.warning("Chunked upload failed (%s); sending request inline", error)
            return req
        thin = pb2.ForwardBackwardRequest(
            model_id=req.model_id, upload_id=created.upload_id
        )
        if req.HasField("seq_id"):
            thin.seq_id = req.seq_id
        return thin

    def _submit_optim_step(
        self,
        model_id: str,
        seq_id: int,
        lr: float,
        beta1: float,
        beta2: float,
        eps: float,
        weight_decay: float,
        grad_clip_norm: float | None,
    ) -> str:
        """Fire optim step RPC without waiting. Returns request_id."""
        adam_params = pb2.AdamParams(
            learning_rate=lr,
            beta1=beta1,
            beta2=beta2,
            eps=eps,
            weight_decay=weight_decay,
        )
        if grad_clip_norm is not None:
            adam_params.grad_clip_norm = grad_clip_norm
        req = pb2.OptimStepRequest(
            model_id=model_id,
            seq_id=seq_id,
            adam_params=adam_params,
        )
        response = self._client._rpc_with_retry(
            lambda: self._live_stub.OptimStep(req, metadata=self._live_metadata),
            context="Optimizer step",
            heartbeat_check=self._check_heartbeat_health,
        )
        return response.request_id

    def _save_weights(
        self,
        model_id: str,
        seq_id: int,
        name: str,
        mode: str,
        timeout: float,
        step: int,
        ttl_seconds: int | None = None,
    ) -> Checkpoint:
        """Save checkpoint (training or inference mode)."""
        req = pb2.SaveWeightsRequest(
            model_id=model_id,
            seq_id=seq_id,
            path=name,
            mode=mode,
        )
        if ttl_seconds is not None:
            req.ttl_seconds = ttl_seconds

        response = self._client._rpc_with_retry(
            lambda: self._live_stub.SaveWeights(req, metadata=self._live_metadata),
            context="Saving weights",
            heartbeat_check=self._check_heartbeat_health,
        )
        result = self._wait_for_future(
            response.request_id,
            timeout=timeout,
            model_id=model_id,
        )

        if result.WhichOneof("response") != "save_weights":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return Checkpoint(
            path=result.save_weights.path,
            step=step,
            checkpoint_type=mode,
        )

    def _load_weights(
        self,
        model_id: str,
        seq_id: int,
        path: str,
        load_optimizer: bool,
        timeout: float,
    ) -> None:
        """Load weights from checkpoint."""
        req = pb2.LoadWeightsRequest(
            model_id=model_id,
            seq_id=seq_id,
            path=path,
            optimizer=load_optimizer,
        )

        response = self._client._rpc_with_retry(
            lambda: self._live_stub.LoadWeights(req, metadata=self._live_metadata),
            context="Loading weights",
            heartbeat_check=self._check_heartbeat_health,
        )
        self._wait_for_future(
            response.request_id,
            timeout=timeout,
            model_id=model_id,
        )

    @staticmethod
    def _prompts_to_proto(prompts: list[dict]) -> list[pb2.InferencePrompt]:
        """Convert prompt dicts to InferencePrompt protos."""
        result = []
        for p in prompts:
            proto = pb2.InferencePrompt(
                prompt=p["prompt"],
                max_tokens=p.get("max_tokens", 256),
                temperature=p.get("temperature", 1.0),
                top_p=p.get("top_p", 1.0),
                top_k=p.get("top_k", 0),
                stop=p.get("stop", []),
            )
            if "seed" in p and p["seed"] is not None:
                proto.seed = p["seed"]
            if "logprobs" in p and p["logprobs"] is not None:
                proto.logprobs = p["logprobs"]
            if (
                "return_prompt_logprobs" in p
                and p["return_prompt_logprobs"] is not None
            ):
                proto.return_prompt_logprobs = p["return_prompt_logprobs"]
            if p.get("return_expert_routing"):
                proto.return_expert_routing = True
            # Pre-tokenized prompt: `prompt` stays empty and the ids are sent
            # as-is, bypassing server-side tokenization.
            if p.get("input_ids"):
                proto.input_ids.extend(p["input_ids"])
            # Vision images ride through as raw bytes; preprocessing happens
            # server-side.
            if "images" in p and p["images"]:
                for image in p["images"]:
                    proto.images.append(bytes(image))
            result.append(proto)
        return result

    @staticmethod
    def _inference_to_dicts(
        response: pb2.InferenceResponse,
    ) -> list[dict]:
        """Convert InferenceResponse proto to list of result dicts.

        Dict shape (all lists present; empty when the server didn't populate them):
          * ``text`` (str)
          * ``token_logprobs`` (list[float]) — output tokens
          * ``tokens`` (list[str]) — output token strings; legacy field, may be
            empty when the server is on the native /generate path
          * ``prompt_token_logprobs`` (list[float])
          * ``token_ids`` (list[int]) — output token IDs; populated on native
            /generate, empty on the legacy /v1/completions path
          * ``prompt_token_ids`` (list[int])
          * ``top_logprobs`` (list[list[TopLogprob]]) — output side top-K
          * ``prompt_top_logprobs`` (list[list[TopLogprob]]) — prompt side top-K
          * ``metrics`` (dict[str, float]) — per-result scalar metrics; empty
            unless the request carried a recognized ``metrics_type`` token
        """
        return [
            {
                "text": r.text,
                "token_logprobs": _optional_proto_list(r, "token_logprobs"),
                "tokens": _optional_proto_list(r, "tokens"),
                "prompt_token_logprobs": _optional_proto_list(
                    r, "prompt_token_logprobs"
                ),
                "token_ids": _optional_proto_list(r, "token_ids"),
                "prompt_token_ids": _optional_proto_list(r, "prompt_token_ids"),
                "top_logprobs": _proto_top_logprobs_to_dicts(
                    getattr(r, "top_logprobs", [])
                ),
                "prompt_top_logprobs": _proto_top_logprobs_to_dicts(
                    getattr(r, "prompt_top_logprobs", [])
                ),
                "expert_routing": _expert_routing_proto_to_dict(
                    getattr(r, "expert_routing", None)
                ),
                "metrics": dict(getattr(r, "metrics", {})),
            }
            for r in response.results
        ]

    def _sample_batched_from_training(
        self,
        model_id: str,
        prompts: list[dict],
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> list[dict]:
        """Sample from training model's current weights.

        Args:
            model_id: Training model ID.
            prompts: List of prompt dicts.
            timeout: Timeout in seconds.

        Returns:
            List of result dicts with 'text', 'token_logprobs', etc.
        """
        request_id = self._submit_sample_batched_from_training(
            model_id=model_id,
            prompts=prompts,
        )
        result = self._wait_for_future(
            request_id,
            timeout=timeout,
            model_id=model_id,
        )

        if result.WhichOneof("response") != "inference":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return self._inference_to_dicts(result.inference)

    def _submit_sample_batched_from_training(
        self,
        model_id: str,
        prompts: list[dict],
        metrics_type: str = "",
        timeout: float | None = None,
    ) -> str:
        """Submit sampling from training model's current weights."""
        req = pb2.SampleFromTrainingRequest(
            model_id=model_id,
            prompts=self._prompts_to_proto(prompts),
            metrics_type=metrics_type,
        )
        response = self._client._rpc_with_retry(
            lambda: self._live_stub.SampleFromTraining(
                req, metadata=self._live_metadata, timeout=timeout
            ),
            context="Pool sample from training",
            max_wait_secs=(
                timeout
                if timeout is not None
                else _HEARTBEAT_UNHEALTHY_AFTER_TRANSPORT_SECS
            ),
            heartbeat_check=self._check_heartbeat_health,
        )
        return response.request_id

    def _generate_from_base_model(
        self,
        base_model: str,
        prompts: list[dict],
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> list[dict]:
        """Generate from a base model (no LoRA).

        Args:
            base_model: Base model name.
            prompts: List of prompt dicts.
            timeout: Timeout in seconds.

        Returns:
            List of result dicts with 'text', 'token_logprobs', etc.
        """
        operation_started_at = time.monotonic()
        request_id = self._submit_generate_from_base_model(
            base_model=base_model,
            prompts=prompts,
            timeout=timeout,
        )
        remaining_timeout = timeout - (time.monotonic() - operation_started_at)
        if remaining_timeout <= 0:
            raise RiverTimeoutError(
                f"Operation {request_id} timed out after {timeout}s",
                request_id=request_id,
            )
        result = self._wait_for_future(request_id, timeout=remaining_timeout)

        if result.WhichOneof("response") != "inference":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return self._inference_to_dicts(result.inference)

    def _submit_generate_from_base_model(
        self,
        base_model: str,
        prompts: list[dict],
        metrics_type: str = "",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> str:
        """Submit generation from a base model."""
        deadline = time.monotonic() + timeout
        req = pb2.InferenceGenerateRequest(
            base_model=base_model,
            prompts=self._prompts_to_proto(prompts),
            metrics_type=metrics_type,
        )

        def submit():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RiverTimeoutError(
                    f"Pool generate timed out after {timeout}s before submission"
                )
            return self._live_stub.InferenceGenerate(
                req,
                metadata=self._live_metadata,
                timeout=remaining,
            )

        response = self._client._rpc_with_retry(
            submit,
            context="Pool generate",
            max_wait_secs=timeout,
            heartbeat_check=self._check_heartbeat_health,
        )
        return response.request_id

    def _sample_from_checkpoint(
        self,
        checkpoint_path: str,
        base_model: str,
        prompts: list[dict],
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> tuple[list[dict], str]:
        """Sample from a saved checkpoint.

        Args:
            checkpoint_path: ``river://`` checkpoint path.
            base_model: Base model name.
            prompts: List of prompt dicts.
            timeout: Timeout in seconds.

        Returns:
            Tuple of (result dicts, request_id).
        """
        operation_started_at = time.monotonic()
        request_id = self._submit_sample_from_checkpoint(
            checkpoint_path=checkpoint_path,
            base_model=base_model,
            prompts=prompts,
            timeout=timeout,
        )
        remaining_timeout = timeout - (time.monotonic() - operation_started_at)
        if remaining_timeout <= 0:
            raise RiverTimeoutError(
                f"Operation {request_id} timed out after {timeout}s",
                request_id=request_id,
            )
        result = self._wait_for_future(request_id, timeout=remaining_timeout)

        if result.WhichOneof("response") != "inference":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return self._inference_to_dicts(result.inference), request_id

    def _submit_sample_from_checkpoint(
        self,
        checkpoint_path: str,
        base_model: str,
        prompts: list[dict],
        metrics_type: str = "",
        timeout: float = _DEFAULT_TIMEOUT_SECS,
    ) -> str:
        """Submit sampling from a saved checkpoint."""
        deadline = time.monotonic() + timeout
        req = pb2.SampleFromCheckpointRequest(
            checkpoint_path=checkpoint_path,
            base_model=base_model,
            prompts=self._prompts_to_proto(prompts),
            metrics_type=metrics_type,
        )

        def submit():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RiverTimeoutError(
                    f"Pool sample from checkpoint timed out after {timeout}s "
                    "before submission"
                )
            return self._live_stub.SampleFromCheckpoint(
                req,
                metadata=self._live_metadata,
                timeout=remaining,
            )

        response = self._client._rpc_with_retry(
            submit,
            context="Pool sample from checkpoint",
            max_wait_secs=timeout,
            heartbeat_check=self._check_heartbeat_health,
        )
        return response.request_id


class SessionContext:
    """Context manager for Session with auto-heartbeat."""

    def __init__(
        self,
        client: Client,
        tags: dict[str, str],
        timeout: float,
        *,
        before_poll: Callable[[], None] | None = None,
        on_session_creation_attempted: Callable[[], None] | None = None,
        on_session_created: Callable[[], None] | None = None,
        on_session_closed: Callable[[], None] | None = None,
    ):
        self._client = client
        self._tags = tags
        self._timeout = timeout
        self._before_poll = before_poll
        self._on_session_creation_attempted = on_session_creation_attempted
        self._on_session_created = on_session_created
        self._on_session_closed = on_session_closed
        self._session: Session | None = None
        self._session_creation_attempted_reported = False
        self._session_created_reported = False
        self._enter_attempted = False
        self._closed = False

    def _report_session_creation_attempted(self) -> None:
        if self._session_creation_attempted_reported:
            return
        self._session_creation_attempted_reported = True
        if self._on_session_creation_attempted is not None:
            self._on_session_creation_attempted()

    def _report_session_created(self) -> None:
        if self._session_created_reported:
            return
        self._session_created_reported = True
        if self._on_session_created is not None:
            self._on_session_created()

    def _close_session(self, primary_error: BaseException | None = None) -> None:
        if self._session is None or self._closed:
            return
        self._closed = True
        cleanup_errors: list[BaseException] = []
        try:
            self._session._unload_all_models()
        except BaseException as error:
            cleanup_errors.append(error)
        try:
            self._session._stop_heartbeat()
        except BaseException as error:
            cleanup_errors.append(error)
        if not cleanup_errors and self._on_session_closed is not None:
            try:
                self._on_session_closed()
            except BaseException as error:
                cleanup_errors.append(error)
        if primary_error is not None:
            for error in cleanup_errors:
                primary_error.add_note(
                    "River session cleanup also failed: "
                    f"{type(error).__name__}: {error}"
                )
            return
        if cleanup_errors:
            first = cleanup_errors[0]
            for error in cleanup_errors[1:]:
                first.add_note(
                    "River session cleanup also failed: "
                    f"{type(error).__name__}: {error}"
                )
            raise first

    def __enter__(self) -> Session:
        if self._enter_attempted:
            raise RuntimeError("River SessionContext cannot be entered more than once")
        self._enter_attempted = True
        self._session = self._client._create_session(
            self._tags,
            timeout=self._timeout,
            before_poll=self._before_poll,
            on_session_creation_attempted=self._report_session_creation_attempted,
            on_session_created=self._report_session_created,
        )
        try:
            # Preserve compatibility with test doubles and older internal
            # clients that return without invoking the response-bound callback.
            self._report_session_created()
            self._session._start_heartbeat()
        except BaseException as error:
            self._close_session(error)
            raise
        return self._session

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._close_session(exc_val)


class Client:
    """River API client.

    Connects to the River API server over gRPC with automatic retry on
    transient failures and connection keepalive.
    """

    def __init__(
        self,
        api_key: str,
        endpoint: str = "api.river.ai",
        port: int = 443,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        use_ssl: bool = True,
        enable_retries: bool = True,
    ):
        """Create a River client.

        Args:
            api_key: API key for authentication
            endpoint: API endpoint hostname
            port: API port
            timeout: Default timeout for operations
            use_ssl: Whether to use SSL
            enable_retries: Whether submit RPCs and gRPC transport may retry
                transient failures. Disable this for fail-closed evaluation
                protocols that require one server submission per model turn.
        """
        self._api_key = api_key
        self._endpoint = endpoint
        self._port = port
        self._timeout = timeout
        self._use_ssl = use_ssl
        self._enable_retries = bool(enable_retries)
        self._channel_options = _grpc_channel_options(
            enable_retries=self._enable_retries
        )
        self._channel: grpc.Channel | None = None
        self._stub: pb2_grpc.RiverServiceStub | None = None
        self._session_channel: grpc.Channel | None = None
        self._session_stub: pb2_grpc.RiverServiceStub | None = None
        self._heartbeat_channel: grpc.Channel | None = None
        self._heartbeat_stub: pb2_grpc.RiverServiceStub | None = None
        self._upload_channels: list[grpc.Channel] = []
        self._upload_stubs: list[pb2_grpc.RiverServiceStub] = []
        self._chunked_upload_unsupported = False

    def _get_channel(self) -> grpc.Channel:
        """Get or create gRPC channel."""
        if self._channel is None:
            target = f"{self._endpoint}:{self._port}"
            if self._use_ssl:
                credentials = grpc.ssl_channel_credentials()
                self._channel = grpc.secure_channel(
                    target, credentials, options=self._channel_options
                )
            else:
                self._channel = grpc.insecure_channel(
                    target, options=self._channel_options
                )
        return self._channel

    def _get_stub(self) -> pb2_grpc.RiverServiceStub:
        """Get or create gRPC stub."""
        if self._stub is None:
            self._stub = pb2_grpc.RiverServiceStub(self._get_channel())
        return self._stub

    def _get_session_stub(self) -> pb2_grpc.RiverServiceStub:
        """Return a stub whose transport cannot retry ambiguous session creation."""
        if self._session_stub is None:
            target = f"{self._endpoint}:{self._port}"
            options = _grpc_channel_options(enable_retries=False)
            if self._use_ssl:
                self._session_channel = grpc.secure_channel(
                    target, grpc.ssl_channel_credentials(), options=options
                )
            else:
                self._session_channel = grpc.insecure_channel(target, options=options)
            self._session_stub = pb2_grpc.RiverServiceStub(self._session_channel)
        return self._session_stub

    def _get_upload_stubs(self, n: int) -> list[pb2_grpc.RiverServiceStub]:
        """Grow the parallel-upload pool to ``n`` connections and return it.

        Each pool channel sets ``grpc.use_local_subchannel_pool`` so it owns a
        genuinely separate TCP connection: without it, channels to the same
        target share one subchannel from the process-global pool and parallel
        uploads silently collapse onto a single connection (whose kernel send
        buffer is exactly the bottleneck this pool exists to multiply).
        Channels persist across steps so later uploads skip connection
        establishment and TCP slow-start.
        """
        target = f"{self._endpoint}:{self._port}"
        while len(self._upload_stubs) < n:
            options = [
                *self._channel_options,
                ("grpc.use_local_subchannel_pool", 1),
            ]
            if self._use_ssl:
                channel = grpc.secure_channel(
                    target, grpc.ssl_channel_credentials(), options=options
                )
            else:
                channel = grpc.insecure_channel(target, options=options)
            self._upload_channels.append(channel)
            self._upload_stubs.append(pb2_grpc.RiverServiceStub(channel))
        return self._upload_stubs[:n]

    def _get_heartbeat_channel(self) -> grpc.Channel:
        """Get or create dedicated heartbeat gRPC channel."""
        if self._heartbeat_channel is None:
            target = f"{self._endpoint}:{self._port}"
            if self._use_ssl:
                credentials = grpc.ssl_channel_credentials()
                self._heartbeat_channel = grpc.secure_channel(
                    target, credentials, options=self._channel_options
                )
            else:
                self._heartbeat_channel = grpc.insecure_channel(
                    target, options=self._channel_options
                )
        return self._heartbeat_channel

    def _get_heartbeat_stub(self) -> pb2_grpc.RiverServiceStub:
        """Get or create dedicated heartbeat stub."""
        if self._heartbeat_stub is None:
            self._heartbeat_stub = pb2_grpc.RiverServiceStub(
                self._get_heartbeat_channel()
            )
        return self._heartbeat_stub

    def _reset_heartbeat_channel(self) -> None:
        """Force the next heartbeat onto a fresh gRPC connection."""
        channel = self._heartbeat_channel
        self._heartbeat_channel = None
        self._heartbeat_stub = None
        if channel is not None:
            channel.close()

    def _get_metadata(self) -> list[tuple[str, str]]:
        """Get gRPC metadata with authentication and client attribution."""
        return [
            ("x-api-key", self._api_key),
            ("x-river-client", _CLIENT_IDENTIFIER),
        ]

    def _http_base_url(self) -> str:
        return _http_base_url(self._endpoint, self._port, self._use_ssl)

    def _http_authorization_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._api_key}",
            "x-river-client": _CLIENT_IDENTIFIER,
        }

    def _rpc(self, fn, context: str = "API call"):
        """Execute a gRPC call, converting errors to RiverConnectionError."""
        try:
            return fn()
        except grpc.RpcError as e:
            raise RiverConnectionError.from_grpc_error(e, context) from None

    def _rpc_with_retry(
        self,
        fn,
        context: str = "API call",
        max_wait_secs: float = _HEARTBEAT_UNHEALTHY_AFTER_TRANSPORT_SECS,
        heartbeat_check=None,
    ):
        """Like ``_rpc``, but retries ``UNAVAILABLE`` up to ``max_wait_secs``.

        Intended for Submit RPCs (the first call of each user-facing
        operation). gRPC's built-in retry policy already absorbs short
        UNAVAILABLE bursts (~15s budget); this wrapper extends that window
        to the same span the heartbeat thread tolerates transport failures
        (``_HEARTBEAT_UNHEALTHY_AFTER_TRANSPORT_SECS``), so an extended
        transport or service outage doesn't kill the training run before
        it even gets a ``request_id``.

        Trade-off: UNAVAILABLE does not guarantee the server hasn't already
        seen the request. Transport resets can happen after the request has
        been forwarded and partially processed, so a retry can queue a
        duplicate operation server-side with a fresh ``request_id``. This is
        the same exposure gRPC's built-in retry already has today — the wrapper
        scales the window, not the risk.
        ``DEADLINE_EXCEEDED`` is explicitly not retried because it's a
        stronger signal that the server has started work.

        If ``heartbeat_check`` is provided, it's invoked between retries and
        may raise ``SessionHeartbeatError`` to abort early when the session
        has been silent past its own tolerance window.
        """
        if not self._enable_retries:
            return self._rpc(fn, context)
        start = time.monotonic()
        sleep = _SUBMIT_RETRY_INITIAL_SLEEP_SECS
        while True:
            try:
                return self._rpc(fn, context)
            except RiverConnectionError as error:
                if error.status_code != "UNAVAILABLE":
                    raise
                elapsed = time.monotonic() - start
                if elapsed >= max_wait_secs:
                    raise
                if heartbeat_check is not None:
                    heartbeat_check()
                wait = min(sleep, max_wait_secs - elapsed)
                if wait <= 0:
                    raise
                time.sleep(wait)
                sleep = min(sleep * 2, _SUBMIT_RETRY_MAX_SLEEP_SECS)

    def _create_session(
        self,
        tags: dict[str, str],
        *,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        before_poll: Callable[[], None] | None = None,
        on_session_creation_attempted: Callable[[], None] | None = None,
        on_session_created: Callable[[], None] | None = None,
    ) -> Session:
        """Create a new session."""
        deadline = time.monotonic() + timeout
        req = pb2.CreateSessionRequest(tags=tags, sdk_version=_CLIENT_IDENTIFIER)

        def create():
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RiverTimeoutError(f"Creating session timed out after {timeout}s")
            return self._get_session_stub().CreateSession(
                req,
                metadata=self._get_metadata(),
                timeout=remaining,
            )

        # A transport error may arrive after the server committed the session.
        # Publish ownership before the only RPC attempt and never replay it.
        if on_session_creation_attempted is not None:
            on_session_creation_attempted()
        response = self._rpc(create, "Creating session")

        if response.error_message:
            raise RiverError(response.error_message)
        if on_session_created is not None:
            on_session_created()
        # Server-to-client notice channel: the server uses warning_message
        # for things the user should act on (e.g. "this SDK version is
        # deprecated, please upgrade") and info_message for FYI notices.
        if response.warning_message:
            warnings.warn(response.warning_message, stacklevel=3)
        if response.info_message:
            _logger.info("%s", response.info_message)

        return Session(
            client=self,
            session_id=response.session_id,
            stub=self._get_stub(),
            metadata=self._get_metadata(),
            before_poll=before_poll,
        )

    def session(
        self,
        *,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        before_poll: Callable[[], None] | None = None,
        on_session_creation_attempted: Callable[[], None] | None = None,
        on_session_created: Callable[[], None] | None = None,
        on_session_closed: Callable[[], None] | None = None,
        **tags: str,
    ) -> SessionContext:
        """Create a session context manager.

        Args:
            timeout: End-to-end session-creation timeout in seconds.
            **tags: Optional tags for the session

        Returns:
            Context manager that yields a Session
        """
        return SessionContext(
            self,
            tags,
            timeout,
            before_poll=before_poll,
            on_session_creation_attempted=on_session_creation_attempted,
            on_session_created=on_session_created,
            on_session_closed=on_session_closed,
        )

    def _wait_for_future(
        self,
        request_id: str,
        timeout: float = _DEFAULT_TIMEOUT_SECS,
        poll_interval: float = 0.01,
        *,
        model_id: str | None = None,
        retry_connection_errors: bool = True,
        before_poll: Callable[[], None] | None = None,
    ) -> pb2.RetrieveFutureResponse:
        """Poll for async operation result (stateless, no session)."""
        deadline = time.monotonic() + timeout
        poll_retry_sleep = _POLL_RETRY_INITIAL_SLEEP_SECS
        poll_retries = 0

        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RiverTimeoutError(
                    f"Operation {request_id} timed out after {timeout}s",
                    request_id=request_id,
                )

            req = pb2.RetrieveFutureRequest(request_id=request_id)
            if model_id is not None:
                req.model_id = model_id
            if before_poll is not None:
                before_poll()
            try:
                response = self._rpc(
                    lambda: self._get_stub().RetrieveFuture(
                        req,
                        metadata=self._get_metadata(),
                        timeout=remaining,
                    ),
                    context="Retrieving operation result",
                )
            except RiverConnectionError as error:
                if not retry_connection_errors:
                    raise
                # Terminal errors never clear by retrying (auth / identity /
                # argument / state) — surface them immediately.
                if error.status_code in _POLL_TERMINAL_STATUS_CODES:
                    raise
                # UNAVAILABLE / DEADLINE_EXCEEDED: the request is still in flight
                # server-side (server rolling / overloaded), so wait it out with
                # no consecutive cap. Everything else (INTERNAL/UNKNOWN/ABORTED/
                # RESOURCE_EXHAUSTED, incl. HTTP/2 stream resets) is also retried —
                # the poll is idempotent — but bounded, so a deterministically
                # failing response surfaces instead of hanging until the timeout.
                if not _is_transient_connection_error(error):
                    poll_retries += 1
                    if poll_retries > _POLL_MAX_RETRIES:
                        raise
                time.sleep(min(poll_retry_sleep, max(0.0, deadline - time.monotonic())))
                poll_retry_sleep = min(poll_retry_sleep * 2, _POLL_RETRY_MAX_SLEEP_SECS)
                continue
            poll_retry_sleep = _POLL_RETRY_INITIAL_SLEEP_SECS
            poll_retries = 0

            response_type = response.WhichOneof("response")

            if response_type == "try_again":
                time.sleep(min(poll_interval, max(0.0, deadline - time.monotonic())))
                continue
            if response_type == "failed":
                error = response.failed
                raise RiverError(f"{error.error_category}: {error.message}")

            return response

    def sample(
        self,
        prompts: str | list[str] | None = None,
        *,
        base_model: str,
        num_samples: int = 1,
        max_tokens: int = 256,
        temperature: float = 1.0,
        top_p: float = 1.0,
        top_k: int = -1,
        stop: list[str] | None = None,
        seed: int | None = None,
        return_prompt_logprobs: bool = False,
        logprobs: int | None = None,
        images: list[bytes] | list[list[bytes]] | None = None,
        prompt_token_ids: list[int] | list[list[int]] | None = None,
        model_input: list[dict] | list[list[dict]] | None = None,
        tokenizer: Any | None = None,
        metrics_type: str = "",
        timeout: float | None = None,
    ) -> list[Sample]:
        """Sample from a base model (no session required).

        Args:
            prompts: Single prompt string or list of prompts.
                Mutually exclusive with ``prompt_token_ids``.
            base_model: Base model name
                (e.g. ``"Qwen/Qwen3.6-35B-A3B-FP8"``).
            num_samples: Number of independent samples per prompt.
            max_tokens: Maximum tokens to generate per sample.
            temperature: Sampling temperature.
            top_p: Nucleus sampling threshold.
            top_k: Top-k sampling (-1 = disabled).
            stop: Stop sequences.
            seed: Random seed (varied per sample automatically).
            return_prompt_logprobs: Whether to return prompt token logprobs.
            logprobs: If set to ``K > 0``, request the top-K alternative
                logprobs at each position. Off by default — enabling it
                roughly halves server throughput.
            images: Optional raw image bytes for multimodal sampling.
                See :meth:`Model.sample` for the per-prompt vs.
                broadcast semantics.
            prompt_token_ids: Pre-tokenized prompt(s); mutually exclusive
                with ``prompts``. See :meth:`Model.sample` for details.
            model_input: Training-style chunk list(s); mutually exclusive
                with ``prompts`` / ``prompt_token_ids`` / ``images``.
                See :meth:`Model.sample` for details.
            tokenizer: Optional tokenizer name or already-loaded tokenizer.
                Defaults to ``base_model`` after applying River model-alias
                resolution.
            metrics_type: Opaque server-interpreted token enabling extra
                scalar metrics on the response. Unrecognized values are
                silently ignored; when recognized, per-result metrics
                appear on ``Sample.metrics``.
            timeout: Timeout in seconds.

        Returns:
            Flat ``list[Sample]`` — all samples across all prompts.
            For a single prompt with ``num_samples=1`` (the default),
            this is a list with one element: ``result[0].text``.
        """
        timeout = timeout if timeout is not None else self._timeout

        if isinstance(prompts, str):
            prompts = [prompts]

        tokenizer = load_tokenizer(tokenizer, base_model=base_model)
        prompts, prompt_token_ids, images = _resolve_model_input(
            model_input,
            prompts=prompts,
            prompt_token_ids=prompt_token_ids,
            images=images,
            tokenizer=tokenizer,
        )

        # Use the shared ``_build_sample_prompt_dicts`` helper so the
        # images normalization (None / list[bytes] / list[list[bytes]])
        # is consistent across Client.sample / Session.sample / Model.sample.
        _, prompt_dicts = _build_sample_prompt_dicts(
            prompts,
            num_samples=num_samples,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
            seed=seed,
            return_prompt_logprobs=return_prompt_logprobs,
            logprobs=logprobs,
            images=images,
            prompt_token_ids=prompt_token_ids,
        )

        grpc_req = pb2.InferenceGenerateRequest(
            base_model=base_model,
            prompts=Session._prompts_to_proto(prompt_dicts),
            metrics_type=metrics_type,
        )
        response = self._rpc_with_retry(
            lambda: self._get_stub().InferenceGenerate(
                grpc_req, metadata=self._get_metadata()
            ),
            context="Pool generate",
        )
        future_result = self._wait_for_future(response.request_id, timeout=timeout)

        if future_result.WhichOneof("response") != "inference":
            raise RiverError(
                f"Unexpected response type: {future_result.WhichOneof('response')}"
            )

        raw_results = Session._inference_to_dicts(future_result.inference)

        # Build flat list of Sample objects
        samples: list[Sample] = []
        for r in raw_results:
            tokens, token_lps, stop_reason = _tokens_and_logprobs_from_raw(
                r, tokenizer, max_tokens
            )
            samples.append(
                Sample(
                    tokens=tokens,
                    text=r["text"],
                    logprobs=token_lps,
                    stop_reason=stop_reason,
                    model_step=0,
                    prompt_logprobs=_optional_prompt_logprobs(
                        r, return_prompt_logprobs
                    ),
                    prompt_token_ids=_optional_prompt_token_ids(
                        r, return_prompt_logprobs
                    ),
                    top_logprobs=_optional_top_logprobs(r, "top_logprobs"),
                    prompt_top_logprobs=_optional_top_logprobs(
                        r, "prompt_top_logprobs"
                    ),
                    metrics=dict(r.get("metrics") or {}),
                )
            )

        return samples

    def health_check(self) -> bool:
        """Check API health.

        Returns:
            True if healthy
        """
        try:
            req = pb2.HealthCheckRequest()
            response = self._rpc(
                lambda: self._get_stub().HealthCheck(
                    req, metadata=self._get_metadata()
                ),
                context="Health check",
            )
            return response.status == "ok"
        except Exception:
            return False

    def get_capabilities(self) -> list[str]:
        """Get supported models.

        Returns:
            List of supported model names
        """
        req = pb2.GetServerCapabilitiesRequest()
        response = self._rpc(
            lambda: self._get_stub().GetServerCapabilities(
                req, metadata=self._get_metadata()
            ),
            context="Get capabilities",
        )

        return [m.model_name for m in response.supported_models]

    def get_streaming_replica(
        self,
        model: str,
        *,
        timeout: float | None = None,
    ) -> PromotedStreamingReplica | None:
        """Return promoted streaming metadata for ``model`` when available.

        This reads server-owned routing metadata from the control plane.
        Missing metadata returns ``None``; other HTTP/auth failures raise a
        River client exception.
        """
        timeout = timeout if timeout is not None else _STREAM_READ_TIMEOUT_SECS
        query = urlencode({"model": model})
        request = _UrlRequest(
            f"{self._http_base_url()}/api/v1/streaming/replicas?{query}",
            headers={
                **self._http_authorization_headers(),
                "Accept": "application/json",
            },
            method="GET",
        )

        try:
            with _urlopen(request, timeout=timeout) as response:
                body = response.read()
        except HTTPError as error:
            body = error.read()
            if error.code == 404:
                return None
            raise _http_error(error.code, body, "Streaming replica discovery") from None
        except URLError as error:
            raise RiverConnectionError(
                f"Streaming replica discovery failed: {error}",
                details=str(error),
                original_error=error,
            ) from None

        try:
            raw = _json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, _json.JSONDecodeError) as error:
            raise RiverConnectionError(
                f"Streaming replica discovery returned invalid JSON: {error}",
                original_error=error,
            ) from error
        if not isinstance(raw, dict):
            raise RiverConnectionError(
                "Streaming replica discovery returned non-object JSON"
            )

        return _promoted_streaming_replica_from_raw(raw)

    def promote_streaming_replica(
        self,
        checkpoint: str | Checkpoint,
        model: str,
        *,
        timeout: float | None = None,
    ) -> PromotedStreamingReplica:
        """Request beta promotion of a checkpoint to a streaming model alias.

        The request is asynchronous: the returned metadata is usually
        ``status="provisioning"``. Poll :meth:`get_streaming_replica` until the
        status is ``"ready"`` or ``"degraded"`` before using
        :meth:`chat_complete_stream`.
        """
        read_timeout = timeout if timeout is not None else _STREAM_READ_TIMEOUT_SECS
        checkpoint_path = (
            checkpoint.path if isinstance(checkpoint, Checkpoint) else checkpoint
        )
        request_body = {"checkpoint": checkpoint_path, "model": model}
        request = _UrlRequest(
            f"{self._http_base_url()}/api/v1/streaming/promotions",
            data=_json.dumps(request_body).encode("utf-8"),
            headers={
                **self._http_authorization_headers(),
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with _urlopen(request, timeout=read_timeout) as response:
                body = response.read()
        except HTTPError as error:
            body = error.read()
            raise _http_error(error.code, body, "Streaming replica promotion") from None
        except URLError as error:
            raise RiverConnectionError(
                f"Streaming replica promotion failed: {error}",
                details=str(error),
                original_error=error,
            ) from None

        try:
            raw = _json.loads(body.decode("utf-8"))
        except (UnicodeDecodeError, _json.JSONDecodeError) as error:
            raise RiverConnectionError(
                f"Streaming replica promotion returned invalid JSON: {error}",
                original_error=error,
            ) from error
        if not isinstance(raw, dict):
            raise RiverConnectionError(
                "Streaming replica promotion returned non-object JSON"
            )
        return _promoted_streaming_replica_from_raw(raw)

    def chat_complete_stream(
        self,
        messages: list[dict],
        *,
        model: str,
        timeout: float | None = None,
        on_not_ready: str = "raise",
        **kwargs,
    ) -> Iterator[dict[str, Any]]:
        """Stream OpenAI-compatible chat chunks from a promoted replica.

        ``timeout`` is the socket read timeout for each blocking read, not an
        end-to-end generation deadline. Let the iterator finish, or call
        ``close()`` on it when breaking early, so the HTTP connection is closed.

        Args:
            messages: OpenAI-format messages list.
            model: Product-facing promoted model alias.
            timeout: Per-read HTTP timeout. Defaults to 60 seconds.
            on_not_ready: ``"raise"`` (default) or ``"blocking"``. The blocking
                fallback returns one stream-shaped chunk converted from the
                existing blocking control-plane chat path when promoted metadata
                is missing, unreachable, or not ready.
            **kwargs: Extra OpenAI chat-completions request fields, such as
                ``max_tokens``, ``temperature``, ``logprobs=True``, and
                ``top_logprobs=N``.

        Returns:
            Iterator of decoded OpenAI streaming chunk dictionaries.
        """
        read_timeout = timeout if timeout is not None else _STREAM_READ_TIMEOUT_SECS
        fallback = on_not_ready.lower()
        if fallback not in {"raise", "blocking"}:
            raise ValueError("on_not_ready must be 'raise' or 'blocking'")

        try:
            replica = self.get_streaming_replica(model, timeout=read_timeout)
        except RiverConnectionError:
            if fallback == "blocking":
                return self._blocking_chat_fallback(
                    messages, model, None, read_timeout, kwargs
                )
            raise
        if (
            replica is None
            or replica.status not in _STREAMING_REPLICA_ROUTEABLE
            or not replica.base_url
        ):
            if fallback == "blocking":
                return self._blocking_chat_fallback(
                    messages, model, replica, read_timeout, kwargs
                )
            status = "missing" if replica is None else replica.status
            raise RiverError(
                f"promoted streaming replica for model {model!r} is not ready ({status})"
            )

        request_body = {"model": model, "messages": messages, **kwargs, "stream": True}
        url = f"{replica.base_url.rstrip('/')}/v1/chat/completions"
        request = _UrlRequest(
            url,
            data=_json.dumps(request_body).encode("utf-8"),
            headers={
                **self._http_authorization_headers(),
                "Accept": "text/event-stream",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            response = _urlopen(request, timeout=read_timeout)
        except HTTPError as error:
            body = error.read()
            raise _http_error(error.code, body, "Streaming chat completion") from None
        except URLError as error:
            raise RiverConnectionError(
                f"Streaming chat completion failed: {error}",
                details=str(error),
                original_error=error,
            ) from None

        return _iter_openai_stream_events(response)

    def _blocking_chat_fallback(
        self,
        messages: list[dict],
        model: str,
        replica: PromotedStreamingReplica | None,
        timeout: float,
        kwargs: dict[str, Any],
    ) -> Iterator[dict[str, Any]]:
        request_kwargs = dict(kwargs)
        request_kwargs.pop("stream", None)
        request_kwargs.pop("stream_options", None)
        if replica is not None:
            result = self.chat_complete_from_checkpoint(
                messages,
                checkpoint_path=replica.checkpoint,
                base_model=replica.base_model,
                timeout=timeout,
                **request_kwargs,
            )
        else:
            result = self.chat_complete(
                messages,
                base_model=model,
                timeout=timeout,
                **request_kwargs,
            )
        result = cast(ChatCompleteResult, result)
        response = _json.loads(result.response_json)
        if not isinstance(response, dict):
            raise RiverError("blocking chat fallback returned non-object JSON")
        yield _stream_chunk_from_blocking_response(response)

    def chat_complete(
        self,
        messages: list[dict],
        *,
        base_model: str,
        timeout: float | None = None,
        **kwargs,
    ) -> ChatCompleteResult | Iterator[dict[str, Any]]:
        """Chat completion from a base model (no LoRA).

        Builds an OpenAI-format request body and sends it through the
        gRPC ``ChatCompleteFromBase`` RPC.

        Args:
            messages: OpenAI-format messages list.
            base_model: Base model name for routing.
            timeout: Timeout in seconds.
            **kwargs: Extra fields for the OpenAI request body
                (e.g. ``max_tokens``, ``temperature``).

        Returns:
            ChatCompleteResult with response_json and status_code.
        """
        import json

        if kwargs.get("stream") is True:
            stream_kwargs = dict(kwargs)
            stream_kwargs.pop("stream", None)
            return self.chat_complete_stream(
                messages,
                model=base_model,
                timeout=timeout,
                **stream_kwargs,
            )

        timeout = timeout if timeout is not None else self._timeout
        request_body = {"model": base_model, "messages": messages, **kwargs}

        req = pb2.ChatCompleteFromBaseRequest(
            base_model=base_model,
            request_json=json.dumps(request_body),
        )
        response = self._rpc_with_retry(
            lambda: self._get_stub().ChatCompleteFromBase(
                req, metadata=self._get_metadata()
            ),
            context="Chat completion (base)",
        )
        result = self._wait_for_future(response.request_id, timeout=timeout)

        if result.WhichOneof("response") != "chat_complete":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return ChatCompleteResult(
            response_json=result.chat_complete.response_json,
            status_code=result.chat_complete.status_code,
        )

    def chat_complete_from_checkpoint(
        self,
        messages: list[dict],
        *,
        checkpoint_path: str,
        base_model: str = "",
        timeout: float | None = None,
        **kwargs,
    ) -> ChatCompleteResult:
        """Chat completion from a saved checkpoint.

        Args:
            messages: OpenAI-format messages list.
            checkpoint_path: ``river://`` checkpoint path.
            base_model: Base model name (optional; resolved from DB if empty).
            timeout: Timeout in seconds.
            **kwargs: Extra fields for the OpenAI request body.

        Returns:
            ChatCompleteResult with response_json and status_code.
        """
        import json

        timeout = timeout if timeout is not None else self._timeout
        model = base_model or checkpoint_path
        request_body = {"model": model, "messages": messages, **kwargs}

        req = pb2.ChatCompleteFromCheckpointRequest(
            checkpoint_path=checkpoint_path,
            base_model=base_model,
            request_json=json.dumps(request_body),
        )
        response = self._rpc_with_retry(
            lambda: self._get_stub().ChatCompleteFromCheckpoint(
                req, metadata=self._get_metadata()
            ),
            context="Chat completion (checkpoint)",
        )
        result = self._wait_for_future(response.request_id, timeout=timeout)

        if result.WhichOneof("response") != "chat_complete":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return ChatCompleteResult(
            response_json=result.chat_complete.response_json,
            status_code=result.chat_complete.status_code,
        )

    def chat_complete_from_training(
        self,
        messages: list[dict],
        *,
        model_id: str,
        timeout: float | None = None,
        **kwargs,
    ) -> ChatCompleteResult:
        """Chat completion from in-memory training weights.

        Args:
            messages: OpenAI-format messages list.
            model_id: Training model ID (e.g. ``session_id:model:seq``).
            timeout: Timeout in seconds.
            **kwargs: Extra fields for the OpenAI request body.

        Returns:
            ChatCompleteResult with response_json and status_code.
        """
        import json

        timeout = timeout if timeout is not None else self._timeout
        request_body = {"model": model_id, "messages": messages, **kwargs}

        req = pb2.ChatCompleteFromTrainingRequest(
            model_id=model_id,
            request_json=json.dumps(request_body),
        )
        response = self._rpc_with_retry(
            lambda: self._get_stub().ChatCompleteFromTraining(
                req, metadata=self._get_metadata()
            ),
            context="Chat completion (training)",
        )
        result = self._wait_for_future(
            response.request_id,
            timeout=timeout,
            model_id=model_id,
        )

        if result.WhichOneof("response") != "chat_complete":
            raise RiverError(
                f"Unexpected response type: {result.WhichOneof('response')}"
            )

        return ChatCompleteResult(
            response_json=result.chat_complete.response_json,
            status_code=result.chat_complete.status_code,
        )

    def close(self) -> None:
        """Close the client connection."""
        if self._session_channel is not None:
            self._session_channel.close()
            self._session_channel = None
            self._session_stub = None
        if self._channel is not None:
            self._channel.close()
            self._channel = None
            self._stub = None
        for channel in self._upload_channels:
            channel.close()
        self._upload_channels = []
        self._upload_stubs = []
        self._reset_heartbeat_channel()
