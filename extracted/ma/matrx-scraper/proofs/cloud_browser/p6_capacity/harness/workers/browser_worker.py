"""One browser unit. Phase-0 proof harness (NOT shipped code).

A "unit" is one isolated persistent-context Chromium with its own user_data_dir -- the
same shape PLAN.md describes for a browser worker ("one isolated worker/sidecar per
active profile"). One OS process per unit, so the sampler can attribute a whole process
tree to it and so a crash is a real process exit rather than a swallowed exception.

Emits JSONL on stdout; the driver reads it:
    {"ev":"ready","start_ms":1234.5}          browser start latency (process -> first paint)
    {"ev":"action","name":"nav","ms":88.2}    automation action latency
    {"ev":"error","name":"...","msg":"..."}   a failed action (counted, not fatal)
    {"ev":"done","actions":N,"errors":M}      clean exit

Exits 0 on clean stop (SIGTERM or duration reached), non-zero on failure to start. The
driver treats any non-zero exit or signal death as a crash for the crash/OOM guardrail.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import signal
import sys
import tarfile
import tempfile
import time
from pathlib import Path

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")

_STOP = False


def _emit(**payload) -> None:
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


def _on_term(_signum, _frame) -> None:
    global _STOP
    _STOP = True


CHROMIUM_ARGS = [
    "--no-first-run",
    "--no-default-browser-check",
    "--disable-background-networking",
    "--disable-features=Translate,MediaRouter",
    # NOT --disable-dev-shm-usage: on the real hosts /dev/shm sizing is part of what we
    # are measuring, and masking it here would hide a real capacity failure mode.
]


def _restore_profile(target: Path, archive: Path) -> float:
    """Restore-storm half of workload 6: unpack a profile before launch, timed."""
    t0 = time.perf_counter()
    if target.exists():
        shutil.rmtree(target, ignore_errors=True)
    target.mkdir(parents=True, exist_ok=True)
    with tarfile.open(archive, "r:*") as tar:
        try:
            tar.extractall(target, filter="data")  # py>=3.12 default, explicit here
        except TypeError:
            tar.extractall(target)
    return (time.perf_counter() - t0) * 1000.0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--mode", required=True, choices=["idle", "nav", "heavy", "storm"])
    ap.add_argument("--profile-dir", required=True)
    ap.add_argument("--duration", type=float, required=True)
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--restore-from", default=None)
    ap.add_argument("--tabs", type=int, default=3)
    ap.add_argument("--think-ms", type=int, default=250)
    args = ap.parse_args()

    signal.signal(signal.SIGTERM, _on_term)
    signal.signal(signal.SIGINT, _on_term)

    profile_dir = Path(args.profile_dir)
    restore_ms = None
    if args.restore_from:
        restore_ms = _restore_profile(profile_dir, Path(args.restore_from))
        _emit(ev="restore", ms=round(restore_ms, 2))
    profile_dir.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # noqa: BLE001
        _emit(ev="fatal", msg=f"playwright import failed: {exc}")
        return 2

    deadline = time.time() + args.duration
    actions = 0
    errors = 0
    t_start = time.perf_counter()

    with sync_playwright() as pw:
        try:
            ctx = pw.chromium.launch_persistent_context(
                str(profile_dir),
                headless=args.headless,
                args=CHROMIUM_ARGS,
                viewport={"width": 1280, "height": 900},
            )
        except Exception as exc:  # noqa: BLE001
            _emit(ev="fatal", msg=f"launch failed: {exc}")
            return 3

        try:
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            # authenticate once: every workload runs on an AUTHENTICATED profile,
            # which is what PLAN.md's workload 1 explicitly names.
            page.goto(f"{args.base_url}/login", wait_until="load")
            page.fill("#u", "synthetic-user")
            page.fill("#p", "synthetic-secret")
            page.click("#submit")
            page.wait_for_selector("#state", timeout=15000)
            start_ms = (time.perf_counter() - t_start) * 1000.0
            _emit(
                ev="ready",
                start_ms=round(start_ms, 2),
                restore_ms=None if restore_ms is None else round(restore_ms, 2),
            )

            pages = [page]
            if args.mode == "heavy":
                for _ in range(max(0, args.tabs - 1)):
                    pages.append(ctx.new_page())
                for p in pages:
                    p.goto(f"{args.base_url}/heavy", wait_until="load")
            elif args.mode == "idle":
                page.goto(f"{args.base_url}/idle", wait_until="load")

            while not _STOP and time.time() < deadline:
                t0 = time.perf_counter()
                try:
                    if args.mode == "idle":
                        # An idle tab is not a dead tab: a cheap liveness read every few
                        # seconds is what tells us the renderer is still responsive.
                        page.title()
                        page.evaluate("() => document.getElementById('stamp').textContent")
                        name = "idle_probe"
                        sleep_s = 5.0
                    elif args.mode in ("nav", "storm"):
                        page.goto(f"{args.base_url}/form", wait_until="load")
                        page.fill("#name", f"u{random.randint(1000, 9999)}")
                        page.fill("#qty", str(random.randint(1, 9)))
                        page.click("#go")
                        page.wait_for_selector("#result", timeout=20000)
                        name = "nav_form_cycle"
                        sleep_s = args.think_ms / 1000.0
                    else:  # heavy
                        target = pages[actions % len(pages)]
                        target.bring_to_front()
                        target.click("#churn")
                        target.wait_for_function(
                            "() => Number(document.getElementById('count').textContent) > 0",
                            timeout=30000,
                        )
                        target.mouse.wheel(0, 4000)
                        name = "heavy_churn_cycle"
                        sleep_s = args.think_ms / 1000.0
                    _emit(ev="action", name=name, ms=round((time.perf_counter() - t0) * 1000.0, 2))
                    actions += 1
                except Exception as exc:  # noqa: BLE001
                    errors += 1
                    _emit(ev="error", name=args.mode, msg=str(exc)[:300])
                    sleep_s = 1.0
                slept = 0.0
                while slept < sleep_s and not _STOP and time.time() < deadline:
                    time.sleep(min(0.2, sleep_s - slept))
                    slept += 0.2
        finally:
            try:
                ctx.close()
            except Exception:  # noqa: BLE001
                pass

    _emit(ev="done", actions=actions, errors=errors)
    return 0


if __name__ == "__main__":
    tmp = tempfile.gettempdir()
    os.environ.setdefault("TMPDIR", tmp)
    sys.exit(main())
