from __future__ import annotations

import asyncio
import math
from collections.abc import Mapping
from contextlib import suppress
from typing import Any

from dreamscale import wire
from dreamscale.policy.runtime.server_report import answer_engine, real_rows
from dreamscale.policy.types import ActionChunkResult, ActionTiming


def result_from_chunk(
    *,
    observation_id: int,
    chunk: Any,
    start_ns: int,
    send_start_ns: int,
    send_end_ns: int,
    end_ns: int,
    transport: Any,
    data_plane_rtt_ms: float | None = None,
    capture_time_ns: int | None = None,
    frame: Any = None,
) -> ActionChunkResult:
    server_queue_ms, server_inference_ms, server_total_ms = _server_timings(chunk)
    # The compatibility name predates the GPU executor. This interval begins
    # only after the GPU lock is acquired, so it is worker preprocessing.
    worker_preprocess_ms = server_queue_ms
    if data_plane_rtt_ms is None:
        data_plane_rtt_ms = _data_plane_rtt_sample(transport, None)
    else:
        data_plane_rtt_ms = _finite_ms(data_plane_rtt_ms)
    worker_queue_ms = _runtime_server_ms(chunk, "gpu_queue_ms")
    worker_postprocess_ms = None
    if (
        server_total_ms is not None
        and worker_preprocess_ms is not None
        and server_inference_ms is not None
    ):
        worker_postprocess_ms = max(
            0.0,
            server_total_ms - worker_preprocess_ms - server_inference_ms,
        )
    obs_to_action_ms = (end_ns - start_ns) / 1_000_000.0
    client_overhead_ms = (
        obs_to_action_ms - server_total_ms if server_total_ms is not None else None
    )
    actions = tuple(tuple(action) for action in wire.chunk_actions(chunk))
    indices = tuple(wire.chunk_action_indices(chunk))
    rows = real_rows(chunk)
    if rows is not None and rows < len(actions):
        # An older worker padded its answer past the model's real rows: never run them.
        actions, indices = actions[:rows], indices[:rows]
    engine, engine_reason = answer_engine(chunk)
    return ActionChunkResult(
        observation_id=observation_id,
        chunk_id=getattr(chunk, "chunk_id", None),
        actions=actions,
        action_indices=indices,
        timing=ActionTiming(
            obs_to_action_ms=obs_to_action_ms,
            transport_send_ms=(send_end_ns - send_start_ns) / 1_000_000.0,
            wait_for_chunk_ms=(end_ns - send_end_ns) / 1_000_000.0,
            server_queue_ms=server_queue_ms,
            server_inference_ms=server_inference_ms,
            server_total_ms=server_total_ms,
            client_overhead_ms=client_overhead_ms,
            client_encode_ms=_encode_ms(frame),
            upload_bytes=_upload_bytes(frame),
            quic_rtt_ms=(
                data_plane_rtt_ms
                if getattr(transport, "mode", None) == "quic"
                else None
            ),
            data_plane_rtt_ms=data_plane_rtt_ms,
            worker_queue_ms=worker_queue_ms,
            worker_preprocess_ms=worker_preprocess_ms,
            worker_inference_ms=server_inference_ms,
            worker_postprocess_ms=worker_postprocess_ms,
        ),
        transport_mode=getattr(transport, "mode", None),
        raw_chunk=chunk,
        capture_time_ns=capture_time_ns,
        prefix_rows=_prefix_rows(chunk),
        engine=engine,
        engine_reason=engine_reason,
    )


def _prefix_rows(chunk: Any) -> int:
    """The committed actions the server pinned at the start of this chunk (trained RTC's
    ``runtime_metadata.rtc.prefix_rows``; test-time RTC's guided ``inference_delay_steps``, at
    most its horizon over the rows sent); 0 when it reports none."""
    runtime_metadata = getattr(chunk, "runtime_metadata", None)
    if runtime_metadata is None:
        return 0
    if isinstance(runtime_metadata, Mapping):
        rtc = runtime_metadata.get("rtc")
    else:
        rtc = getattr(runtime_metadata, "rtc", None)
    if not isinstance(rtc, Mapping):
        return 0
    value = rtc.get("prefix_rows")
    if rtc.get("mode") == "test_time":
        # held to the committed rows for its inference delay, when it guided at all, and never
        # past the rows it was sent (the server clips its horizon to them)
        delay, horizon = rtc.get("inference_delay_steps"), rtc.get("execution_horizon_steps")
        value = (
            min(delay, horizon)
            if rtc.get("guided") and isinstance(delay, int) and isinstance(horizon, int)
            else 0
        )
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return 0
    return value


def _server_timings(chunk: Any) -> tuple[float | None, float | None, float | None]:
    receive = _int_attr(chunk, "server_receive_time_ns")
    inference_start = _int_attr(chunk, "inference_start_time_ns")
    inference_end = _int_attr(chunk, "inference_end_time_ns")
    send = _int_attr(chunk, "server_send_time_ns")
    return (
        _duration_ms(receive, inference_start),
        _duration_ms(inference_start, inference_end),
        _duration_ms(receive, send),
    )


def _int_attr(obj: Any, name: str) -> int | None:
    value = getattr(obj, name, None)
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError, OverflowError):
        return None


def _duration_ms(start_ns: int | None, end_ns: int | None) -> float | None:
    if start_ns is None or end_ns is None or end_ns < start_ns:
        return None
    return (end_ns - start_ns) / 1_000_000.0


def _runtime_server_ms(chunk: Any, name: str) -> float | None:
    runtime_metadata = getattr(chunk, "runtime_metadata", None)
    if runtime_metadata is None:
        return None
    if isinstance(runtime_metadata, Mapping):
        server = runtime_metadata.get("server")
    else:
        server = getattr(runtime_metadata, "server", None)
    if not isinstance(server, Mapping):
        return None
    value = server.get(name)
    try:
        parsed = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    if not math.isfinite(parsed) or parsed < 0.0:
        return None
    return parsed


def _data_plane_rtt_sample(
    transport: Any,
    probe: asyncio.Task[float | None] | None,
) -> float | None:
    if probe is not None and probe.done() and not probe.cancelled():
        with suppress(Exception):
            value = probe.result()
            if value is not None:
                return _finite_ms(value)
    data_plane_rtt_ms = getattr(transport, "data_plane_rtt_ms", None)
    if callable(data_plane_rtt_ms):
        with suppress(Exception):
            value = data_plane_rtt_ms()
            if value is not None:
                return _finite_ms(value)
    return _transport_rtt_ms(transport)


def _transport_rtt_ms(transport: Any) -> float | None:
    network_rtt_ms = getattr(transport, "network_rtt_ms", None)
    if callable(network_rtt_ms):
        value = network_rtt_ms()
        if value is not None:
            return _finite_ms(value)
    value = getattr(transport, "rtt_ms", None)
    return _finite_ms(value)


def _finite_ms(value: object) -> float | None:
    try:
        parsed = float(value)
    except (TypeError, ValueError, OverflowError):
        return None
    return parsed if math.isfinite(parsed) and parsed >= 0.0 else None


def _encode_ms(frame: Any) -> float | None:
    """How long the client spent encoding the observation's images, when it recorded it."""
    start = getattr(frame, "encode_start_time_ns", None)
    end = getattr(frame, "encode_end_time_ns", None)
    if start is None or end is None or end < start:
        return None
    return (end - start) / 1_000_000.0


def _upload_bytes(frame: Any) -> int | None:
    """The encoded image bytes the observation carried."""
    cameras = getattr(frame, "cameras", None)
    if not cameras:
        return None
    return sum(int(getattr(camera, "payload_bytes", 0) or 0) for camera in cameras)
