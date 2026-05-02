"""
ghostlogic-demo — 20-minute forensic pipeline replay.

Replays 642K real events with timed Inspector + Arbitrator triggers:
  min 0-20:  Event replay (65 batches, sealed continuously)
  min 4:     Inspector run #1 (early warning)
  min 12:    Inspector run #2 + Arbitrator preliminary
  min 20:    Inspector run #3 + Arbitrator final settlement

Usage:
    pip install ghostlogic-demo
    ghostlogic-demo              # just runs. auto-registers. zero config.
    ghostlogic-demo --dry-run    # test locally without sending
    ghostlogic-demo --fast       # no wait between batches
"""

import argparse
import gzip
import io
import json
import os
import sys
import time
import threading

if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from .sender import API_URL

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".ghostlogic")
CONFIG_FILE = os.path.join(CONFIG_DIR, "demo.json")
DATASET = os.path.join(os.path.dirname(__file__), "dataset.json.gz")

BATCH_SIZE = 10_000

# Timed triggers (minutes from start)
INSPECTOR_TIMES = [4, 12, 20]       # Inspector runs at min 4, 12, 20
ARBITRATOR_TIMES = [12, 20]          # Arbitrator runs at min 12, 20


def _load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def _save_config(cfg: dict):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def _get_key(url: str) -> str:
    cfg = _load_config()
    if cfg.get("key") and cfg.get("url") == url:
        return cfg["key"]
    from .sender import register
    print("  Registering with Blackbox...", end=" ", flush=True)
    key = register(url)
    print(f"\033[1;32m✓\033[0m")
    _save_config({"url": url, "key": key})

    print(f"""
\033[1;33m╔══════════════════════════════════════════════════════════╗
║  OPEN THIS IN YOUR BROWSER:                              ║
║                                                          ║
║  \033[1;37mhttps://blackbox.ghostlogic.tech\033[1;33m                        ║
║                                                          ║
║  When it asks for an API key, paste this:                ║
║                                                          ║
║  \033[1;37m{key}\033[1;33m
║                                                          ║
║  Then watch the Vault, Inspector, and Arbitrator tabs.   ║
╚══════════════════════════════════════════════════════════╝\033[0m
""")
    return key


def _bar(pct: float, width: int = 30) -> str:
    filled = int(width * pct)
    return f"[{'=' * filled}{' ' * (width - filled)}]"


def _load_dataset() -> list[dict]:
    print("  Loading real forensic dataset...", end=" ", flush=True)
    t0 = time.time()
    with gzip.open(DATASET, "rt", encoding="utf-8") as f:
        events = json.load(f)
    print(f"\033[1;32m✓\033[0m  {len(events):,} events ({time.time()-t0:.1f}s)")
    return events


def _run_inspector(url: str, key: str, label: str, capsule_id: str = ""):
    """Trigger Inspector on a specific capsule and poll for completion."""
    from .sender import investigate, get_investigation, force_seal, get_capsules

    # Seal first to capture latest events
    seal_resp = force_seal(url, key)

    # If no capsule_id provided, get the most recent one from the vault
    if not capsule_id:
        capsule_id = seal_resp.get("capsule_id", seal_resp.get("id", ""))

    if not capsule_id:
        # List capsules and grab the most recent
        caps_resp = get_capsules(url, key)
        capsules = caps_resp.get("capsules", [])
        if capsules:
            capsule_id = capsules[-1].get("capsule_id", capsules[-1].get("id", ""))

    if not capsule_id:
        print(f"\n\033[1;36m  ── INSPECTOR ({label}) ──\033[0m")
        print(f"  \033[1;31m✗\033[0m  No capsule ID available to investigate")
        return None

    print(f"\n\033[1;36m  ── INSPECTOR ({label}) ──\033[0m")
    print(f"  Investigating capsule {capsule_id[:12]}...", end=" ", flush=True)

    inv_resp = investigate(url, key, capsule_id)

    if "error" in str(inv_resp.get("status", "")):
        detail = str(inv_resp.get("detail", ""))[:200]
        print(f"\033[1;31m✗\033[0m  {detail}")
        return None

    job_id = inv_resp.get("job_id", "")
    print(f"\033[1;32m✓\033[0m  job={job_id[:12] if job_id else 'queued'}...")

    # Poll (max 5 min)
    poll_start = time.time()
    while time.time() - poll_start < 300:
        time.sleep(5)
        status_resp = get_investigation(url, key, capsule_id)
        status = status_resp.get("status", "unknown")
        elapsed = int(time.time() - poll_start)

        if status == "completed":
            print(f"  Inspector ({label}) complete in {elapsed}s \033[1;32m✓\033[0m")
            return capsule_id
        elif status == "error":
            print(f"  Inspector ({label}) failed: {status_resp.get('error', '')[:100]}")
            return capsule_id
        else:
            print(f"\r  Inspector ({label}) running... {elapsed}s    ", end="", flush=True)

    print(f"\n  Inspector ({label}) still running after 5min — continuing")
    return cid


def _run_arbitrator(url: str, key: str, label: str, capsule_id: str, event_count: int = 0):
    """Run Arbitrator settlement with proper payload format."""
    from .sender import run_arbitrator, get_investigation

    print(f"\n\033[1;33m  ── ARBITRATOR ({label}) ──\033[0m")
    print(f"  Running 6-layer settlement engine...", end=" ", flush=True)

    # Get investigation report to feed into arbitrator
    inv_data = get_investigation(url, key, capsule_id)
    report = inv_data.get("report", {}) or {}

    ev_count = report.get("event_count", event_count) or event_count
    tics = report.get("tics_score")
    trust = report.get("tics_trust_state", "")
    summary = report.get("executive_summary", "")

    # Derive claimed_loss from evidence (same logic as the console)
    trust_upper = (trust or "").upper()
    if trust_upper in ("BROKEN", "COMPROMISED"):
        claimed = 75000 + (ev_count * 0.5)
    elif trust_upper == "DEGRADED":
        claimed = 45000 + (ev_count * 0.3)
    else:
        claimed = 25000 + (ev_count * 0.15)
    if tics:
        claimed *= (1 + tics)
    claimed = max(claimed, 50000)  # floor

    mode = "final" if "final" in label else "preliminary"

    arb_resp = run_arbitrator(url, key, {
        "mode": mode,
        "policy": {
            "policy_limit": 3000000,
            "deductible": 25000,
            "coverage": ["IR", "BI", "FORENSIC"],
        },
        "claim": {
            "incident_type": "compromise",
            "claimed_loss": round(claimed, 2),
        },
        "evidence": {
            "event_count": ev_count,
            "tics_score": tics,
            "trust_state": trust,
            "executive_summary": summary[:500] if summary else None,
        },
    })

    if "payout" not in arb_resp:
        detail = str(arb_resp.get("detail", arb_resp.get("error", "")))[:200]
        print(f"\033[1;31m✗\033[0m  {detail}")
        return

    payout = arb_resp["payout"]
    confidence = arb_resp.get("confidence", "N/A")
    trace = arb_resp.get("trace", {})

    print(f"\033[1;32m✓\033[0m")
    print(f"\033[1;33m  ┌─────────────────────────────────────────┐")
    print(f"  │  {label.upper():^39s}  │")
    print(f"  │                                         │")
    print(f"  │  Payout:     ${payout:>12,.2f}              │")
    print(f"  │  Confidence: {confidence:>6.1%}                      │")
    print(f"  │  Claimed:    ${claimed:>12,.2f}              │")
    print(f"  │  Events:     {ev_count:>8,}                    │")
    print(f"  │                                         │")

    # Show trace layers
    for layer_name in ["causality", "coverage", "loss", "uncertainty", "economics", "dispute"]:
        layer = trace.get(layer_name, {})
        decision = layer.get("decision", "—")
        lconf = layer.get("confidence", 0)
        print(f"  │  {layer_name:12s}  {decision:20s} {lconf:.0%}  │")

    print(f"  └─────────────────────────────────────────┘\033[0m")


def main():
    parser = argparse.ArgumentParser(
        prog="ghostlogic-demo",
        description="20-minute forensic pipeline replay with timed Inspector + Arbitrator",
    )
    parser.add_argument("--url", default=API_URL, help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true", help="Load dataset but don't send")
    parser.add_argument("--fast", action="store_true", help="No wait between batches")
    parser.add_argument("--accept-waiver", action="store_true", help="Skip the waiver prompt")
    parser.add_argument("--interval", type=float, default=None, help=argparse.SUPPRESS)
    args = parser.parse_args()

    # Waiver
    if not args.accept_waiver:
        print(f"""
\033[1;33m╔════════════════════════════════════════════════════════════╗
║                        DEMO WAIVER                         ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  This software replays REAL forensic telemetry from a      ║
║  previously investigated security incident through the     ║
║  GhostLogic Blackbox API for demonstration purposes.       ║
║                                                            ║
║  By continuing, you acknowledge:                           ║
║                                                            ║
║  1. This is a DEMO. No active breach is occurring.         ║
║  2. The events are historical — not live threats.           ║
║  3. Data is sent to api.ghostlogic.tech (GhostLogic        ║
║     production server) and stored as sealed capsules.       ║
║  4. No malware is installed. No system changes are made.   ║
║  5. You may uninstall at any time (see below).             ║
║                                                            ║
║  TO UNINSTALL:                                             ║
║    pip uninstall ghostlogic-demo                           ║
║    rm -rf ~/.ghostlogic       (Linux/Mac)                  ║
║    del %USERPROFILE%\\.ghostlogic  (Windows)                ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝\033[0m
""")
        answer = input("  Type 'yes' to accept and continue: ").strip().lower()
        if answer != "yes":
            print("\n  Demo cancelled. Nothing was sent.\n")
            sys.exit(0)
        print()

    # Load real events
    events = _load_dataset()

    # Chunk into batches of 10K
    batches = []
    for i in range(0, len(events), BATCH_SIZE):
        batches.append(events[i:i + BATCH_SIZE])

    num_batches = len(batches)
    interval = args.interval or (0 if args.fast else (20 * 60) / num_batches)
    duration_min = (num_batches * interval) / 60

    # Get key
    if not args.dry_run:
        from .sender import send_batch, force_seal
        key = _get_key(args.url)

    evt_line = f"  {num_batches} batches x {BATCH_SIZE:,} events = {len(events):,} total"
    dur_line = f"  Interval: {interval:.1f}s  |  Duration: ~{duration_min:.0f} minutes"

    print(f"""
\033[1;36m╔════════════════════════════════════════════════════════════╗
║            GHOSTLOGIC FORENSIC REPLAY                      ║
║                                                            ║
║  Real events from HP_Envy + MacBook HEXBOI breach          ║
║{evt_line:<60s}║
║{dur_line:<60s}║
║                                                            ║
║  min  4:  Inspector #1 (early warning)                     ║
║  min 12:  Inspector #2 + Arbitrator (preliminary)          ║
║  min 20:  Inspector #3 + Arbitrator (final settlement)     ║
║                                                            ║
║  This is not a simulation. These are real forensic         ║
║  events from a real APT compromise.                        ║
╚════════════════════════════════════════════════════════════╝\033[0m
""")

    if args.dry_run:
        print("\033[1;33m[DRY RUN — dataset loaded, not sending]\033[0m\n")

    total_sent = 0
    start = time.time()
    inspector_triggered = set()
    arbitrator_triggered = set()
    last_capsule_id = None

    for batch_num, batch in enumerate(batches, 1):
        elapsed_min = (time.time() - start) / 60
        pct = batch_num / num_batches
        bar = _bar(pct)

        if args.dry_run:
            print(f"  Batch {batch_num:2d}/{num_batches}  {bar}  {len(batch):,} events  [{elapsed_min:.1f}m]")
            total_sent += len(batch)

            # Show when triggers would fire
            for t in INSPECTOR_TIMES:
                if t not in inspector_triggered and elapsed_min >= t:
                    inspector_triggered.add(t)
                    print(f"\n\033[1;36m  ── INSPECTOR (min {t}) would trigger here ──\033[0m\n")
            for t in ARBITRATOR_TIMES:
                if t not in arbitrator_triggered and elapsed_min >= t:
                    arbitrator_triggered.add(t)
                    print(f"\033[1;33m  ── ARBITRATOR (min {t}) would trigger here ──\033[0m\n")
        else:
            # Check Inspector triggers BEFORE sending batch
            for t in INSPECTOR_TIMES:
                if t not in inspector_triggered and elapsed_min >= t:
                    inspector_triggered.add(t)
                    inv_cid = _run_inspector(args.url, key, f"min {t}", last_capsule_id or "")
                    if inv_cid:
                        last_capsule_id = inv_cid
                    if t in ARBITRATOR_TIMES and t not in arbitrator_triggered:
                        arbitrator_triggered.add(t)
                        if last_capsule_id:
                            label = "preliminary" if t == 12 else "final settlement"
                            _run_arbitrator(args.url, key, label, last_capsule_id)
                    print()

            # Send in 2K chunks so the dashboard buffer fills visibly, seal at the end
            CHUNK = 2000
            t1 = time.time()
            batch_accepted = 0
            batch_ok = True

            for ci in range(0, len(batch), CHUNK):
                chunk = batch[ci:ci + CHUNK]
                resp = send_batch(args.url, key, chunk)
                accepted = resp.get("accepted", 0)
                batch_accepted += accepted
                if resp.get("status") != "ingested":
                    batch_ok = False
                # 3s gap between chunks — dashboard polls every 5s, so buffer climbs visibly
                if ci + CHUNK < len(batch):
                    time.sleep(3)

            # Now seal — dashboard sees buffer drop to 0, capsule count jump
            seal_resp = force_seal(args.url, key)
            seal_status = seal_resp.get("status", "error")
            cid = seal_resp.get("capsule_id", seal_resp.get("id", ""))
            if cid:
                last_capsule_id = cid

            total_sent += batch_accepted
            send_time = time.time() - t1

            marker = "\033[1;32m✓\033[0m" if batch_ok else "\033[1;31m✗\033[0m"
            seal_marker = "\033[1;36mSEALED\033[0m" if seal_status != "error" else "\033[1;31mSEAL FAIL\033[0m"

            print(f"  Batch {batch_num:2d}/{num_batches}  {bar}  {batch_accepted:,} accepted  {marker}  {send_time:.1f}s  {seal_marker}  [{elapsed_min:.1f}m]")

            if not batch_ok:
                detail = resp.get("detail", "")[:100]
                print(f"           \033[1;31m└─ {detail}\033[0m")

        if batch_num < num_batches and not args.dry_run and interval > 0:
            wait = max(0, interval - (time.time() - t1))
            if wait > 1:
                for sec in range(int(wait), 0, -1):
                    print(f"\r  Next batch in {sec}s...  ", end="", flush=True)
                    time.sleep(1)
                print("\r" + " " * 40 + "\r", end="")

    # Final triggers if not yet fired (e.g. --fast mode finished before min 20)
    if not args.dry_run:
        for t in INSPECTOR_TIMES:
            if t not in inspector_triggered:
                inspector_triggered.add(t)
                inv_cid = _run_inspector(args.url, key, f"min {t}", last_capsule_id or "")
                if inv_cid:
                    last_capsule_id = inv_cid
                if t in ARBITRATOR_TIMES and t not in arbitrator_triggered:
                    arbitrator_triggered.add(t)
                    if last_capsule_id:
                        label = "preliminary" if t == 12 else "final settlement"
                        _run_arbitrator(args.url, key, label, last_capsule_id)

    total_time = time.time() - start

    print(f"""
\033[1;36m{'=' * 60}
  Full pipeline complete.

  Events replayed:  {total_sent:,}
  Capsules sealed:  {num_batches}
  Inspector runs:   {len(inspector_triggered)}
  Arbitrator runs:  {len(arbitrator_triggered)}
  Total time:       {total_time / 60:.1f} minutes

  View everything at https://blackbox.ghostlogic.tech
{'=' * 60}\033[0m

\033[2m  To uninstall:
    pip uninstall ghostlogic-demo
    rm -rf ~/.ghostlogic          (Linux/Mac)
    del %USERPROFILE%\\.ghostlogic   (Windows)

  GhostLogic Tech Company — ghostlogic.tech\033[0m
""")


if __name__ == "__main__":
    main()
