"""Opt-in P6 capacity driver for the production browser-worker image.

This is deliberately not a second worker implementation. It boots the real
``BrowserWorker`` against the image's real Xvfb display, starts the same
``SelkiesSupervisor`` used by the HTTP transport, and drives actions through the
real ordered command path. The ordinary image entrypoint selects this module only
when ``P6_BENCHMARK_MODE=1`` is explicitly present.
"""

from __future__ import annotations

import asyncio
import html
import json
import os
import signal
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from matrx_scraper.cloud_browser.streaming.supervisor import SelkiesSupervisor
from matrx_scraper.cloud_browser.worker import commands as C
from matrx_scraper.cloud_browser.worker import models as M
from matrx_scraper.cloud_browser.worker.runtime import BrowserWorker
from matrx_scraper.cloud_browser.worker.stub_control_plane import StubControlPlane


def _emit(**payload: Any) -> None:
    sys.stdout.write(json.dumps(payload, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _positive_float(name: str, default: str) -> float:
    raw = os.environ.get(name, default)
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


@dataclass(frozen=True)
class BenchmarkConfig:
    base_url: str
    duration_s: float
    action_interval_s: float
    display: str
    width: int
    height: int
    profile_dir: Path
    requested_fps: int
    requested_bitrate: str

    @classmethod
    def from_env(cls) -> BenchmarkConfig:
        if os.environ.get("P6_BENCHMARK_MODE") != "1":
            raise ValueError("P6_BENCHMARK_MODE=1 is required")
        return cls(
            base_url=os.environ.get("P6_BASE_URL", "about:blank"),
            duration_s=_positive_float("P6_DURATION", "120"),
            action_interval_s=_positive_float("P6_ACTION_INTERVAL", "0.25"),
            display=os.environ.get("DISPLAY", ":99"),
            width=int(os.environ.get("BROWSER_WORKER_WIDTH", "1920")),
            height=int(os.environ.get("BROWSER_WORKER_HEIGHT", "1080")),
            profile_dir=Path(
                os.environ.get(
                    "P6_PROFILE_DIR", f"{tempfile.gettempdir()}/matrx-p6-browser-profile"
                )
            ),
            requested_fps=int(os.environ.get("P6_STREAM_FPS", "30")),
            requested_bitrate=os.environ.get("P6_STREAM_BITRATE", "4M"),
        )


def _bitrate_kbps(value: str) -> str:
    normalized = value.strip().upper()
    if normalized.endswith("M"):
        return str(int(float(normalized[:-1]) * 1000))
    if normalized.endswith("K"):
        return str(int(float(normalized[:-1])))
    return str(int(float(normalized)))


class _ContainerCpuMeter:
    """Container CPU use as the x264 encoder-capacity signal.

    The production stream uses the software x264 encoder, so there is no hardware
    encoder counter. In this one-purpose container, cgroup CPU usage is the honest
    capacity metric for Chromium plus the software encoder together. Host CPU is
    still independently enforced by the outer P6 sampler.
    """

    def __init__(self) -> None:
        self._last_wall = time.monotonic()
        self._last_cpu = self._cpu_seconds()

    @staticmethod
    def _cpu_seconds() -> float:
        cpu_stat = Path("/sys/fs/cgroup/cpu.stat")
        if cpu_stat.exists():
            fields = dict(line.split(maxsplit=1) for line in cpu_stat.read_text().splitlines())
            if "usage_usec" in fields:
                return float(fields["usage_usec"]) / 1_000_000.0
        return time.process_time()

    @staticmethod
    def _available_cpus() -> float:
        cpu_max = Path("/sys/fs/cgroup/cpu.max")
        if cpu_max.exists():
            quota, period = cpu_max.read_text().strip().split(maxsplit=1)
            if quota != "max":
                return max(float(quota) / float(period), 0.01)
        return float(max(os.cpu_count() or 1, 1))

    def sample(self) -> float:
        wall = time.monotonic()
        cpu = self._cpu_seconds()
        elapsed = max(wall - self._last_wall, 1e-9)
        used = max(cpu - self._last_cpu, 0.0)
        self._last_wall = wall
        self._last_cpu = cpu
        cpus = self._available_cpus()
        return min(100.0, (used / elapsed / cpus) * 100.0)


async def run_benchmark(
    config: BenchmarkConfig,
    *,
    worker: BrowserWorker | None = None,
    control: StubControlPlane | None = None,
    supervisor: SelkiesSupervisor | None = None,
    cpu_meter: _ContainerCpuMeter | None = None,
    emit: Callable[..., None] = _emit,
    stop: asyncio.Event | None = None,
) -> int:
    started = time.perf_counter()
    stop = stop or asyncio.Event()
    worker = worker or BrowserWorker(worker_id="p6-browser-worker", xvfb_display=config.display)
    control = control or StubControlPlane(worker)
    supervisor = supervisor or SelkiesSupervisor()
    cpu_meter = cpu_meter or _ContainerCpuMeter()
    actions = 0
    errors = 0
    booted = False
    stream_started = False

    config.profile_dir.mkdir(parents=True, exist_ok=True)
    try:
        boot = await control.bootstrap(
            user_data_dir=str(config.profile_dir),
            run_mode="handoff_capable",
            display=M.DisplayConfig(kind="xvfb", width=config.width, height=config.height),
            allow_eval_js=True,
        )
        if not boot.ok:
            emit(ev="fatal", msg=f"real worker bootstrap refused: {boot.error}")
            return 2
        booted = True
        page = worker.page_object(worker.active_page_id or "")
        if page is None:
            emit(ev="fatal", msg="real worker booted without an active page")
            return 3
        await page.set_content(
            "<main style='font:48px sans-serif;padding:48px'>"
            "<h1>Matrx browser capacity proof</h1>"
            f"<p>{html.escape(config.base_url)}</p><p id='tick'>0</p></main>"
        )

        # The supervisor inherits these official Selkies settings. The normal
        # production path remains unchanged because only benchmark containers set them.
        os.environ["SELKIES_FRAMERATE"] = str(config.requested_fps)
        os.environ["SELKIES_VIDEO_BITRATE"] = _bitrate_kbps(config.requested_bitrate)
        supervisor.start()
        stream_started = True
        emit(
            ev="ready",
            start_ms=round((time.perf_counter() - started) * 1000, 2),
            runtime="production_browser_worker",
            stream="production_selkies_supervisor",
            width=config.width,
            height=config.height,
            fps=config.requested_fps,
            bitrate_kbps=int(os.environ["SELKIES_VIDEO_BITRATE"]),
        )

        deadline = time.monotonic() + config.duration_s
        next_heartbeat = time.monotonic() + 30.0
        while not stop.is_set() and time.monotonic() < deadline:
            if time.monotonic() >= next_heartbeat:
                await control.heartbeat(lease_seconds=60)
                next_heartbeat = time.monotonic() + 30.0
            action_started = time.perf_counter()
            expression = (
                "() => { const el = document.getElementById('tick'); "
                "el.textContent = String(Number(el.textContent) + 1); return el.textContent; }"
            )
            response = await control.command(C.EvalJsCommand(expression=expression))
            if response.ok:
                actions += 1
                emit(
                    ev="action",
                    name="real_worker_eval_js",
                    ms=round((time.perf_counter() - action_started) * 1000, 2),
                )
            else:
                errors += 1
                emit(ev="error", name="real_worker_eval_js", msg=str(response.error)[:300])
            emit(
                ev="encoder",
                utilisation_pct=round(cpu_meter.sample(), 2),
                source="container_cpu_x264",
            )
            try:
                await asyncio.wait_for(stop.wait(), timeout=config.action_interval_s)
            except TimeoutError:
                pass
    finally:
        if stream_started:
            supervisor.stop()
        if booted:
            await control.shutdown(reason="operator")

    emit(ev="done", actions=actions, errors=errors)
    return 0


def main() -> int:
    try:
        config = BenchmarkConfig.from_env()
    except (TypeError, ValueError) as exc:
        _emit(ev="fatal", msg=str(exc))
        return 2

    async def execute() -> int:
        stop = asyncio.Event()
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGTERM, signal.SIGINT):
            try:
                loop.add_signal_handler(sig, stop.set)
            except NotImplementedError:
                pass
        return await run_benchmark(config, stop=stop)

    try:
        return asyncio.run(execute())
    except Exception as exc:  # noqa: BLE001 - JSONL fatal is the container contract
        _emit(ev="fatal", msg=f"benchmark failed: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
