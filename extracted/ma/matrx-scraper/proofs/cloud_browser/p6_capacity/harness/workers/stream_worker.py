"""One streamed-browser unit (encoder-proxy form). Phase-0 proof harness (NOT shipped).

This worker is the HONEST SUBSTITUTE used when Selkies is not installed on the host:

    own Xvfb display  ->  headed Chromium doing real work on it  ->  ffmpeg encoding that
    display at 1080p with x264 (or NVENC when asked)

What that measures truthfully: browser cost, encoder cost, encoder utilisation, and
output bitrate for one interactive-quality stream. What it does NOT measure: WebRTC
transport, TURN relay, jitter buffers, and INPUT LATENCY -- there is no human plane here.
The workload therefore reports status "partial" and the input-latency guardrail stays
unmeasured unless the operator supplies --input-latency-cmd at the driver level.

Never present encoder-proxy numbers as an interactive-stream capacity result. They are
an upper bound on how many streams the CPU could encode, not how many humans the system
could serve.

Emits the same JSONL vocabulary as browser_worker, plus:
    {"ev":"encoder","utilisation_pct":..,"bitrate_bps":..,"fps":..,"speed":..}
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
_STOP = threading.Event()


def _emit(**payload) -> None:
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def _on_term(_s, _f) -> None:
    _STOP.set()


def _start_xvfb(display: str, geometry: str) -> subprocess.Popen:
    return subprocess.Popen(
        ["Xvfb", display, "-screen", "0", geometry, "-nolisten", "tcp"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _nvenc_available() -> bool:
    if not shutil.which("ffmpeg"):
        return False
    try:
        out = subprocess.run(
            ["ffmpeg", "-hide_banner", "-encoders"], capture_output=True, text=True, timeout=20
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return False
    return "h264_nvenc" in out


def _gpu_encoder_pct() -> float | None:
    if not shutil.which("nvidia-smi"):
        return None
    try:
        out = (
            subprocess.run(
                ["nvidia-smi", "--query-gpu=utilization.encoder", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=10,
            )
            .stdout.strip()
            .splitlines()
        )
    except (OSError, subprocess.SubprocessError):
        return None
    try:
        return max(float(x) for x in out if x.strip())
    except ValueError:
        return None


def _encoder_loop(proc: subprocess.Popen, target_fps: int, hardware: bool) -> None:
    """Parse ffmpeg -progress output into encoder utilisation + bitrate samples.

    Software utilisation definition (documented in README): a real-time encode runs at
    speed 1.0x when it is exactly keeping up. utilisation_pct = 100 / speed. speed 2.0x
    -> 50% used; 1.0x -> 100% (saturated); below 1.0 -> >100%, i.e. already dropping.
    Hardware utilisation is read directly from nvidia-smi utilization.encoder.
    """
    fps = None
    bitrate = None
    assert proc.stdout is not None
    for raw in proc.stdout:
        if _STOP.is_set():
            break
        line = raw.strip()
        if line.startswith("fps="):
            try:
                fps = float(line.split("=", 1)[1])
            except ValueError:
                fps = None
        elif line.startswith("bitrate="):
            match = re.search(r"([\d.]+)\s*kbits/s", line)
            bitrate = float(match.group(1)) * 1000 if match else None
        elif line.startswith("speed="):
            try:
                speed = float(line.split("=", 1)[1].rstrip("x"))
            except ValueError:
                continue
            gpu = _gpu_encoder_pct() if hardware else None
            util = gpu if gpu is not None else (100.0 / speed if speed > 0 else 999.0)
            _emit(
                ev="encoder",
                utilisation_pct=round(util, 2),
                bitrate_bps=bitrate,
                fps=fps,
                speed=speed,
                source="nvidia-smi" if gpu is not None else "ffmpeg_speed_ratio",
            )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--profile-dir", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--display", required=True)
    ap.add_argument("--geometry", default="1920x1080x24")
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--bitrate", default="4M")
    ap.add_argument("--hardware", action="store_true")
    ap.add_argument("--mode", default="heavy", choices=["idle", "nav", "heavy"])
    args = ap.parse_args()

    signal.signal(signal.SIGTERM, _on_term)
    signal.signal(signal.SIGINT, _on_term)

    if not shutil.which("ffmpeg"):
        _emit(ev="fatal", msg="ffmpeg not on PATH")
        return 2
    if not shutil.which("Xvfb"):
        _emit(ev="fatal", msg="Xvfb not on PATH")
        return 2
    if args.hardware and not _nvenc_available():
        _emit(ev="fatal", msg="hardware encode requested but ffmpeg has no h264_nvenc")
        return 2

    xvfb = _start_xvfb(args.display, args.geometry)
    time.sleep(1.5)
    env = dict(os.environ, DISPLAY=args.display)

    browser = subprocess.Popen(
        [
            sys.executable,
            str(HERE / "browser_worker.py"),
            "--base-url",
            args.base_url,
            "--mode",
            args.mode,
            "--profile-dir",
            args.profile_dir,
            "--duration",
            str(args.duration),
        ],
        env=env,
        stdout=subprocess.PIPE,
        text=True,
    )

    codec = (
        ["-c:v", "h264_nvenc", "-preset", "p4"]
        if args.hardware
        else ["-c:v", "libx264", "-preset", "veryfast", "-tune", "zerolatency"]
    )
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-f",
            "x11grab",
            "-framerate",
            str(args.fps),
            "-video_size",
            args.geometry.rsplit("x", 1)[0],
            "-i",
            f"{args.display}.0",
            *codec,
            "-b:v",
            args.bitrate,
            "-maxrate",
            args.bitrate,
            "-bufsize",
            args.bitrate,
            "-f",
            "null",
            "-",
            "-progress",
            "pipe:1",
            "-nostats",
        ],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )

    enc_thread = threading.Thread(
        target=_encoder_loop, args=(ffmpeg, args.fps, args.hardware), daemon=True
    )
    enc_thread.start()

    # forward the browser's own events (ready/action/error) so the driver sees them
    assert browser.stdout is not None
    for line in browser.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        if _STOP.is_set():
            break

    for proc in (browser, ffmpeg, xvfb):
        try:
            proc.terminate()
        except OSError:
            pass
    for proc in (browser, ffmpeg, xvfb):
        try:
            proc.wait(timeout=10)
        except subprocess.SubprocessError:
            proc.kill()
    _emit(ev="done", actions=None, errors=None)
    return 0


if __name__ == "__main__":
    sys.exit(main())
