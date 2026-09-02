"""Workloads 4, 5 and the TURN half of 6. Phase-0 proof harness (NOT shipped code).

PLAN.md, verbatim:
  4. one 1080p interactive stream using x264, then supported hardware encoding;
  5. full sandbox plus streamed browser; and
  6. restore/start storms and TURN-relayed streams.

These are the workloads most likely to SKIP, because they need a stream plane (Selkies),
sometimes a GPU, a sandbox image, and a TURN server. That is expected and is not a
harness failure -- but it is also not a result. Every skip is labelled with what is
missing and what to install, and the run summary refuses the word "complete".

Selkies mode vs encoder-proxy mode
----------------------------------
  P6_SELKIES_IMAGE set + docker present -> each unit is one container of the operator's
      own Selkies image. This is the real shape. The harness measures host CPU/memory/
      disk, container process trees, and GPU encoder utilisation; input latency still
      requires --input-latency-cmd, because only the operator's stream client can
      measure a round trip.
  ffmpeg present, no Selkies -> ENCODER PROXY (see workers/stream_worker.py). Encoder
      utilisation and bitrate are real; WebRTC/TURN/input latency are absent. status =
      partial, and the numbers are an upper bound, never an interactive-session count.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from .. import config
from .base import STATUS_OK, STATUS_PARTIAL, STATUS_SKIP, Preflight, UnitSpec

WORKER = Path(__file__).resolve().parent.parent / "workers" / "stream_worker.py"


def _ffmpeg_has(encoder: str) -> bool:
    if not shutil.which("ffmpeg"):
        return False
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, timeout=20
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return encoder in out


def _stream_plane(ctx) -> tuple[str, list[str]]:
    """-> (mode, reasons). mode in {"selkies", "encoder_proxy", "none"}"""
    if ctx.selkies_image:
        if not shutil.which("docker"):
            return "none", [
                f"P6_SELKIES_IMAGE={ctx.selkies_image} is set but docker is not on PATH"
            ]
        if os.environ.get("P6_IMAGE_BENCHMARK_CONTRACT") != "1":
            return "none", [
                "P6_SELKIES_IMAGE is set, but P6_IMAGE_BENCHMARK_CONTRACT=1 is not. "
                "The image must consume P6_BASE_URL/P6_DURATION and emit the harness "
                "JSONL ready/action/encoder events; the production browser-worker image "
                "does not currently implement that benchmark entrypoint. Refusing a "
                "misleading capacity run."
            ]
        return "selkies", []
    reasons = ["P6_SELKIES_IMAGE not set: no real stream plane available"]
    if not shutil.which("ffmpeg"):
        reasons.append("ffmpeg not on PATH either, so not even the encoder proxy can run")
        return "none", reasons
    if not shutil.which("Xvfb"):
        reasons.append("Xvfb not on PATH, so the encoder proxy has no display to capture")
        return "none", reasons
    return "encoder_proxy", reasons


class InteractiveStream:
    id = "w4_stream_1080p"
    plan_workload = 4
    title = "1080p interactive stream (x264, then hardware encoding)"
    capacity_class = config.CLASS_STREAMED_BROWSER
    steady_state = True

    def __init__(self, hardware: bool = False) -> None:
        self.hardware = hardware
        if hardware:
            self.id = "w4_stream_1080p_hw"
            self.title = "1080p interactive stream (hardware encoding)"

    def preflight(self, ctx) -> Preflight:
        mode, reasons = _stream_plane(ctx)
        if mode == "none":
            return Preflight(STATUS_SKIP, reasons)
        if self.hardware and not _ffmpeg_has("h264_nvenc"):
            return Preflight(
                STATUS_SKIP,
                reasons
                + [
                    "no h264_nvenc in ffmpeg (no NVIDIA GPU / driver / SDK build); "
                    "PLAN.md's 'then supported hardware encoding' cannot be run here"
                ],
            )
        unmeasurable: list[str] = []
        status = STATUS_OK
        if mode == "encoder_proxy":
            status = STATUS_PARTIAL
            reasons.append(
                "ENCODER PROXY: browser + ffmpeg 1080p encode of a real display. No WebRTC, "
                "no TURN, no human plane -- an upper bound on encodable streams, NOT an "
                "interactive-session capacity result"
            )
        if not ctx.input_latency_cmd:
            unmeasurable.append("input_latency")
            reasons.append(
                "no --input-latency-cmd supplied: PLAN.md's 250 ms p95 input-latency "
                "guardrail cannot be evaluated for this workload"
            )
            status = STATUS_PARTIAL
        return Preflight(status, reasons, unmeasurable)

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec:
        mode, _ = _stream_plane(ctx)
        profile = Path(ctx.work_dir) / "profiles" / f"{self.id}_{unit_id}"
        if mode == "selkies":
            return _selkies_unit(ctx, self.id, unit_id, ctx.selkies_image)
        index = int(unit_id.rsplit("-", 1)[-1]) if "-" in unit_id else 0
        display = f":{ctx.display_base + 1 + index}"
        argv = [
            sys.executable,
            str(WORKER),
            "--base-url",
            ctx.base_url,
            "--profile-dir",
            str(profile),
            "--duration",
            str(ctx.unit_duration_s),
            "--display",
            display,
            "--fps",
            str(ctx.stream_fps),
            "--bitrate",
            ctx.stream_bitrate,
        ]
        if self.hardware:
            argv.append("--hardware")
        return UnitSpec(argv=argv, env=dict(os.environ))


class SandboxPlusStream:
    id = "w5_sandbox_plus_stream"
    plan_workload = 5
    title = "Full sandbox plus streamed browser"
    capacity_class = config.CLASS_FULL_UI_SANDBOX
    steady_state = True

    def preflight(self, ctx) -> Preflight:
        reasons: list[str] = []
        if not shutil.which("docker"):
            reasons.append("docker not on PATH")
        if not ctx.sandbox_image:
            reasons.append(
                "P6_SANDBOX_IMAGE not set: this workload runs the REAL sandbox image "
                "(the one Phase 4 ships), not a stand-in -- a substitute would measure "
                "the wrong thing"
            )
        mode, stream_reasons = _stream_plane(ctx)
        if mode == "none":
            reasons.extend(stream_reasons)
        if reasons:
            return Preflight(STATUS_SKIP, reasons)
        unmeasurable = [] if ctx.input_latency_cmd else ["input_latency"]
        status = STATUS_OK if (mode == "selkies" and ctx.input_latency_cmd) else STATUS_PARTIAL
        if mode != "selkies":
            stream_reasons.append("sandbox present but stream plane is the encoder proxy")
        return Preflight(status, stream_reasons, unmeasurable)

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec:
        return _selkies_unit(ctx, self.id, unit_id, ctx.sandbox_image)


class TurnRelayedStream:
    id = "w6b_turn_relayed_stream"
    plan_workload = 6
    title = "TURN-relayed streams (storm half is w6_restore_storm)"
    capacity_class = config.CLASS_STREAMED_BROWSER
    steady_state = True

    def preflight(self, ctx) -> Preflight:
        reasons: list[str] = []
        mode, stream_reasons = _stream_plane(ctx)
        if mode != "selkies":
            reasons.extend(stream_reasons)
            reasons.append(
                "a TURN-relayed stream cannot be simulated by a local encoder: the "
                "quantity under test IS the relay path"
            )
        if not ctx.turn_url:
            reasons.append("P6_TURN_URL not set (coTURN endpoint to force relay through)")
        if not ctx.input_latency_cmd:
            reasons.append(
                "--input-latency-cmd required: relayed input latency is the whole point "
                "of this workload"
            )
        if reasons:
            return Preflight(STATUS_SKIP, reasons)
        return Preflight(STATUS_OK, ["forcing ICE relay-only through the supplied TURN URL"])

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec:
        spec = _selkies_unit(ctx, self.id, unit_id, ctx.selkies_image)
        spec.env["P6_FORCE_TURN"] = "1"
        spec.env["P6_TURN_URL"] = ctx.turn_url or ""
        return spec


def _selkies_unit(ctx, workload_id: str, unit_id: str, image: str | None) -> UnitSpec:
    """One container of the operator's own image.

    The harness cannot know an arbitrary image's entrypoint contract, so it passes the
    benchmark parameters as environment variables and expects the image to start a
    browser session. Any image-specific flags go in P6_DOCKER_EXTRA_ARGS.
    """
    name = f"p6-{workload_id}-{unit_id}"
    extra = (os.environ.get("P6_DOCKER_EXTRA_ARGS") or "").split()
    argv = [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
        "--env",
        "P6_BENCHMARK_MODE=1",
        "--env",
        f"P6_BASE_URL={ctx.base_url}",
        "--env",
        f"P6_DURATION={ctx.unit_duration_s}",
        "--env",
        f"P6_STREAM_FPS={ctx.stream_fps}",
        "--env",
        f"P6_STREAM_BITRATE={ctx.stream_bitrate}",
        "--env",
        "BROWSER_WORKER_WIDTH=1920",
        "--env",
        "BROWSER_WORKER_HEIGHT=1080",
        *extra,
        str(image),
    ]
    return UnitSpec(argv=argv, env=dict(os.environ))
