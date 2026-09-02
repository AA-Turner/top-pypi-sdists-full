"""Workloads 1-3 and the storm half of 6. Phase-0 proof harness (NOT shipped code).

PLAN.md's list, verbatim:
  1. idle authenticated tab after stabilization;
  2. ordinary Playwright navigation/form work;
  3. heavy modern web app with multiple tabs;
  6. restore/start storms and TURN-relayed streams.  <- storm half lives here,
                                                       TURN half lives in streaming.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

from .. import config
from .base import STATUS_OK, STATUS_PARTIAL, STATUS_SKIP, Preflight, UnitSpec

WORKER = Path(__file__).resolve().parent.parent / "workers" / "browser_worker.py"


def _browser_preflight(ctx) -> Preflight:
    reasons: list[str] = []
    try:
        import playwright  # noqa: F401
    except Exception as exc:  # noqa: BLE001
        return Preflight(STATUS_SKIP, [f"python playwright not importable: {exc}"])
    root = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    if not any(root.glob("chromium-*/chrome-linux/chrome")):
        return Preflight(
            STATUS_SKIP,
            [
                f"no chromium build under PLAYWRIGHT_BROWSERS_PATH={root} "
                f"(run: playwright install chromium)"
            ],
        )
    if not ctx.headless and not ctx.display:
        return Preflight(
            STATUS_SKIP,
            [
                "headed mode requested but no X display could be started; install Xvfb or "
                "pass --headless (and note the result is then NOT the production shape, "
                "which is headed on Xvfb)"
            ],
        )
    if ctx.headless:
        reasons.append(
            "running HEADLESS: production runs headed on Xvfb, so these numbers "
            "understate per-unit CPU/RAM"
        )
        return Preflight(STATUS_PARTIAL, reasons, ["headed_display_cost"])
    return Preflight(STATUS_OK, reasons)


class _BrowserWorkload:
    steady_state = True
    capacity_class = config.CLASS_BROWSER_UNSTREAMED
    mode = "nav"

    def preflight(self, ctx) -> Preflight:
        return _browser_preflight(ctx)

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec:
        profile = Path(ctx.work_dir) / "profiles" / f"{self.id}_{unit_id}"
        argv = [
            sys.executable,
            str(WORKER),
            "--base-url",
            ctx.base_url,
            "--mode",
            self.mode,
            "--profile-dir",
            str(profile),
            "--duration",
            str(ctx.unit_duration_s),
            "--think-ms",
            str(ctx.think_ms),
        ]
        if ctx.headless:
            argv.append("--headless")
        env = dict(os.environ)
        if ctx.display:
            env["DISPLAY"] = ctx.display
        return UnitSpec(argv=argv, env=env)


class IdleTab(_BrowserWorkload):
    id = "w1_idle_tab"
    plan_workload = 1
    title = "Idle authenticated tab after stabilization"
    mode = "idle"


class NavigationWork(_BrowserWorkload):
    id = "w2_navigation"
    plan_workload = 2
    title = "Ordinary Playwright navigation/form work"
    mode = "nav"


class HeavyApp(_BrowserWorkload):
    id = "w3_heavy_app"
    plan_workload = 3
    title = "Heavy modern web app with multiple tabs"
    mode = "heavy"

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec:
        spec = super().unit_spec(ctx, unit_id, level)
        spec.argv += ["--tabs", str(ctx.heavy_tabs)]
        return spec


class RestoreStartStorm(_BrowserWorkload):
    """Workload 6, storm half: N profiles restored from encrypted-checkpoint-shaped
    archives and started SIMULTANEOUSLY. The measured quantity is start latency under a
    thundering herd, not steady-state throughput -- so this class's admission answer is a
    concurrent-start RATE, not a resident session count."""

    id = "w6_restore_storm"
    plan_workload = 6
    title = "Restore/start storm (TURN-relayed streams: see w6b)"
    capacity_class = config.CLASS_BURST
    steady_state = False
    mode = "storm"

    def preflight(self, ctx) -> Preflight:
        base = _browser_preflight(ctx)
        if not base.runnable:
            return base
        reasons = list(base.reasons)
        reasons.append(
            "restores a PLAIN tar of a real Chromium profile; it does not decrypt an "
            "AES-GCM/KMS envelope, so it measures unpack+start cost, not KMS latency "
            "(P3 owns the envelope; add its decrypt step before quoting restore SLAs)"
        )
        return Preflight(base.status, reasons, base.unmeasurable + ["kms_decrypt_latency"])

    def unit_spec(self, ctx, unit_id: str, level: int) -> UnitSpec:
        spec = super().unit_spec(ctx, unit_id, level)
        archive = ensure_seed_profile(ctx)
        spec.argv += ["--restore-from", str(archive)]
        return spec


def ensure_seed_profile(ctx) -> Path:
    """Build ONE authenticated Chromium profile, tar it, reuse it for every storm unit.

    Every restore in the storm therefore starts from a byte-identical profile, which is
    what makes two hosts comparable.
    """
    archive = Path(ctx.work_dir) / "seed_profile.tar"
    if archive.exists():
        return archive
    seed_dir = Path(ctx.work_dir) / "seed_profile"
    if seed_dir.exists():
        shutil.rmtree(seed_dir, ignore_errors=True)
    seed_dir.mkdir(parents=True, exist_ok=True)
    argv = [
        sys.executable,
        str(WORKER),
        "--base-url",
        ctx.base_url,
        "--mode",
        "nav",
        "--profile-dir",
        str(seed_dir),
        "--duration",
        "6",
    ]
    if ctx.headless:
        argv.append("--headless")
    env = dict(os.environ)
    if ctx.display:
        env["DISPLAY"] = ctx.display
    subprocess.run(argv, env=env, capture_output=True, text=True, timeout=180)
    tmp = Path(tempfile.mkstemp(prefix="p6seed", suffix=".tar")[1])
    with tarfile.open(tmp, "w") as tar:
        for child in seed_dir.iterdir():
            tar.add(child, arcname=child.name)
    tmp.replace(archive)
    return archive
