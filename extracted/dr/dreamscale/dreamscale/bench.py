"""Internal latency benchmark helpers (sandbox phase0 verbs, relocated).

BenchmarkCase/default_benchmark_cases ported verbatim from
sandbox/sdk/python/dropbear/benchmark.py.
"""

from __future__ import annotations

import asyncio
import json
import time
from collections.abc import Callable
from dataclasses import dataclass
from itertools import product
from typing import Any

import numpy as np

from dreamscale import errors, wire
from dreamscale.config import load_config
from dreamscale.constants import (
    MODEL_GROOT_LIBERO,
    MODEL_LIBERO,
    MODEL_SO101,
    OBS_FRAME_HEIGHT,
    OBS_FRAME_WIDTH,
)
from dreamscale.control import ControlPlaneClient
from dreamscale.model_names import public_model
from dreamscale.region_probe import create_session_with_rtt_region_order
from dreamscale.sessions import Heartbeat, stop_session, wait_until_ready


@dataclass(frozen=True)
class BenchmarkCase:
    camera_count: int
    frame_width: int
    frame_height: int
    jpeg_quality: int
    obs_hz: int
    control_hz: int
    chunk_size: int
    fake_inference_ms: int


def default_benchmark_cases() -> list[BenchmarkCase]:
    camera_counts = [1, 2, 3]
    frame_sizes = [(224, 224), (320, 240), (640, 480)]
    jpeg_qualities = [70, 80, 90]
    obs_hz_values = [5, 10, 20, 50]
    chunk_sizes = [5, 10, 20]
    fake_inference_values = [0, 20, 50, 100, 200]
    return [
        BenchmarkCase(
            camera_count=camera_count,
            frame_width=frame_width,
            frame_height=frame_height,
            jpeg_quality=jpeg_quality,
            obs_hz=obs_hz,
            control_hz=obs_hz,
            chunk_size=chunk_size,
            fake_inference_ms=fake_inference_ms,
        )
        for (
            camera_count,
            (frame_width, frame_height),
            jpeg_quality,
            obs_hz,
            chunk_size,
            fake_inference_ms,
        ) in product(
            camera_counts,
            frame_sizes,
            jpeg_qualities,
            obs_hz_values,
            chunk_sizes,
            fake_inference_values,
        )
    ]


def summarize(rtts_ms: list[float]) -> dict[str, float]:
    ordered = sorted(rtts_ms)

    def percentile(p: float) -> float:
        return ordered[min(len(ordered) - 1, round(p / 100 * (len(ordered) - 1)))]

    return {
        "count": len(ordered),
        "min_ms": ordered[0],
        "p50_ms": percentile(50),
        "p95_ms": percentile(95),
        "max_ms": ordered[-1],
    }


async def run_bench_async(*, model: str = MODEL_SO101, iterations: int = 50,
                          client_factory: Callable[..., Any] = ControlPlaneClient,
                          transport_connect: Callable[..., Any] | None = None,
                          preflight_fn: Callable[..., Any] | None = None,
                          allow_fallback: bool = True,
                          relay_connect: Callable[..., Any] | None = None,
                          on_line: Callable[[str], None] = print,
                          sleep: Callable[..., Any] = asyncio.sleep) -> dict[str, float]:
    from dreamscale.arm import _compatible_diagnose_udp, _default_transport_connect, _pin_connect
    from dreamscale.transport_selection import connect_selected_transport

    if model not in {MODEL_SO101, MODEL_LIBERO, MODEL_GROOT_LIBERO}:
        raise errors.catalog(
            "unknown_model",
            model=model,
            hint=errors.SEE_MODELS,
        )
    if transport_connect is None:
        transport_connect = _default_transport_connect
    if preflight_fn is None:
        from dreamscale_transport import diagnose_udp as preflight_fn
    preflight_fn = _compatible_diagnose_udp(preflight_fn)
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")
    client = client_factory(config.control_plane_url, config.api_key)
    session_to_delete: Any | None = None
    transport: Any | None = None
    heartbeat: Heartbeat | None = None
    completed = False
    try:
        created = await create_session_with_rtt_region_order(
            client, model, region=config.preferred_region or "nearest"
        )
        session_to_delete = created
        session = await wait_until_ready(client, created, on_progress=on_line, sleep=sleep)
        session_to_delete = session

        async def quic_connect(ready_session):
            return await _pin_connect(transport_connect, ready_session)

        async def relay_connect_for_session(ready_session):
            connect = relay_connect or getattr(client, "connect_relay", None)
            if connect is None:
                raise errors.catalog("relay_unavailable")
            return await connect(ready_session)

        transport = await connect_selected_transport(
            session,
            diagnose_udp_fn=preflight_fn,
            quic_connect=quic_connect,
            relay_connect=relay_connect_for_session,
            allow_fallback=allow_fallback,
            on_line=on_line,
            report_transport_fn=getattr(client, "report_transport", None),
        )
        heartbeat = Heartbeat(client, session.session_id)
        heartbeat.start()
        frame = np.zeros((OBS_FRAME_HEIGHT, OBS_FRAME_WIDTH, 3), dtype=np.uint8)
        chunks = transport.action_chunks().__aiter__()
        rtts: list[float] = []
        for observation_id in range(iterations):
            observation = _bench_observation(model, session.session_id,
                                             observation_id, frame)
            start = time.monotonic()
            await transport.send_observation(observation)
            await asyncio.wait_for(chunks.__anext__(), timeout=30.0)
            rtts.append((time.monotonic() - start) * 1000.0)
        summary = summarize(rtts)
        completed = True
        return summary
    finally:
        await _cleanup_bench_resources(
            client=client,
            session=session_to_delete,
            transport=transport,
            heartbeat=heartbeat,
            raise_errors=completed,
        )


async def _cleanup_bench_resources(*, client, session, transport,
                                   heartbeat: Heartbeat | None,
                                   raise_errors: bool) -> None:
    first_error: Exception | None = None

    async def run_cleanup(cleanup):
        nonlocal first_error
        try:
            await cleanup()
        except Exception as exc:  # noqa: BLE001 - finish all cleanup attempts first
            if first_error is None:
                first_error = exc

    if heartbeat is not None:
        await run_cleanup(heartbeat.stop)
    if transport is not None:
        await run_cleanup(transport.close)
    if session is not None:
        await run_cleanup(lambda: stop_session(client, session.session_id))
    await run_cleanup(client.close)
    if first_error is not None and raise_errors:
        raise first_error


def _bench_observation(model: str, session_id: str, observation_id: int, frame):
    if model in {MODEL_LIBERO, MODEL_GROOT_LIBERO}:
        return wire.build_libero_observation(
            session_id=session_id, observation_id=observation_id,
            agent_frame=frame, wrist_frame=frame, libero_state=[0.0] * 8,
            instruction="benchmark")
    return wire.build_so101_observation(
        session_id=session_id, observation_id=observation_id,
        joint_positions=[0.0] * 6, side_frame=frame, wrist_frame=frame,
        instruction="benchmark",
        actions_remaining=0)


def run_bench(model: str = MODEL_SO101, iterations: int = 50,
              json_output: bool = False, allow_fallback: bool = True) -> dict[str, float]:
    summary = asyncio.run(run_bench_async(
        model=model,
        iterations=iterations,
        allow_fallback=allow_fallback,
    ))
    if json_output:
        print(json.dumps(summary, sort_keys=True))
    else:
        print("Dreamscale bench")
        print(f"model: {public_model(model)}")
        print(f"iterations: {iterations}")
        for key, value in summary.items():
            print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")
    return summary
