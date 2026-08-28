"""
rtp_probe.py — read-only diagnostic for GT_VMS rtp-based alignment.

Tails a live inference output topic for a fixed duration and reports the facts
the rtp-based collector relies on:

  * per-output rtp_timestamp delta histogram  (90 kHz media clock)
  * the tick grid = GCD of positive deltas     (90000 / source_fps)
  * loop behaviour — does rtp RESET each loop (Case A) or run continuously
    across loops (Case B)?  Detected from large backward jumps in rtp.
  * inferred loop period (frames + seconds)
  * dropped-output gaps (jumps in the monotonic frame_id counter)

It changes nothing in Redis.  Optionally also dumps every observed message to a
JSONL fixture (--fixture) for the offline replay test.

The output topic is short (MAXLEN ~100, ~12 s of history), and a full loop is
~30 s, so a loop boundary only exists in the LIVE tail — run this for at least
one full loop period (default 80 s).

Usage
-----
    source redis_export.txt
    python3 rtp_probe.py --seconds 80
    python3 rtp_probe.py --seconds 80 --fixture replay_fixture.jsonl
"""

import argparse
import json
import math
import os
import sys
import time
from collections import Counter

import redis as redis_lib

# RTP video clock rate (Hz). H.264/H.265 RTP timestamps tick at 90 kHz.
RTP_CLOCK_HZ = 90_000
# uint32 RTP timestamp wrap modulus.
RTP_WRAP = 1 << 32
# A backward rtp jump larger than this (in ticks) is treated as a loop reset
# rather than packet reordering.  3 s of media at 90 kHz.
RESET_BACKWARD_TICKS = 3 * RTP_CLOCK_HZ


def stream_key(camera_id: str, app_deployment_id: str) -> str:
    return f"{camera_id}_{app_deployment_id}_output_topic"


def parse_message(values: dict) -> dict | None:
    """Extract the fields we care about from one stream entry's `result` JSON."""
    raw = values.get("result") or values.get("data")
    if not raw:
        return None
    try:
        p = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    fid = p.get("frame_id", "") or ""
    suffix = fid.rsplit("_", 1)[-1] if fid else ""
    try:
        counter = int(suffix)
    except ValueError:
        counter = None
    return {
        "frame_id": fid,
        "counter": counter,
        "rtp_timestamp": p.get("rtp_timestamp"),
        "capture_timestamp_ns": p.get("capture_timestamp_ns"),
        "processed_timestamp": p.get("processed_timestamp"),
        "session_id": p.get("session_id"),
    }


def unwrap_rtp(rtp_values: list[int]) -> list[int]:
    """
    Convert a list of raw uint32 rtp timestamps into a continuous monotone
    sequence, undoing 2**32 wrap.  A genuine loop reset (large backward jump
    that is NOT a near-2**32 wrap) is left in place so it can be detected.
    """
    out = []
    offset = 0
    prev = None
    for r in rtp_values:
        if prev is not None:
            d = (r + offset) - prev
            # Near-full-range backward jump => uint32 wrap, add a period.
            if d < -(RTP_WRAP // 2):
                offset += RTP_WRAP
        out.append(r + offset)
        prev = out[-1]
    return out


def gcd_of(values: list[int], round_to: int = 100) -> int:
    """
    GCD of values, rounding each to the nearest `round_to` first so that ±1-tick
    RTP jitter (e.g. 11999/12000/12001) does not collapse the grid to 1.
    """
    g = 0
    for v in values:
        rv = int(round(v / round_to) * round_to) if round_to else int(v)
        g = math.gcd(g, abs(rv))
    return g


def probe(rows: list[dict]) -> dict:
    """Analyse collected rows; returns a report dict."""
    report: dict = {"messages": len(rows)}
    if len(rows) < 3:
        report["error"] = "not enough messages to analyse"
        return report

    rtp_raw = [r["rtp_timestamp"] for r in rows if r["rtp_timestamp"] is not None]
    report["rtp_present"] = len(rtp_raw)
    if len(rtp_raw) < 3:
        report["error"] = "rtp_timestamp absent/null on this stream — cannot align"
        return report

    rtp_cont = unwrap_rtp(rtp_raw)
    deltas = [b - a for a, b in zip(rtp_cont, rtp_cont[1:])]

    # Loop resets: backward jumps that are not uint32 wraps.
    resets = [i for i, d in enumerate(deltas) if d <= -RESET_BACKWARD_TICKS]
    report["loop_resets_seen"] = len(resets)
    report["case"] = "A (rtp resets each loop)" if resets else "B (continuous rtp, no reset observed)"

    pos_deltas = [d for d in deltas if d > 0]
    report["rtp_delta_hist"] = dict(Counter(pos_deltas).most_common(8))
    grid = gcd_of(pos_deltas)
    report["tick_grid"] = grid
    if grid:
        report["inferred_source_fps"] = round(RTP_CLOCK_HZ / grid, 3)
        report["skip_factors"] = sorted({round(d / grid) for d in pos_deltas})
        report["note"] = (
            "grid is the per-source-frame tick step; skip_factors>1 mean inference "
            "subsamples source frames (a per-output counter would be misaligned)."
        )

    # Loop period.
    if len(resets) >= 1:
        # frames between consecutive resets (counter span)
        counters = [r["counter"] for r in rows]
        if len(resets) >= 2:
            c0 = counters[resets[0]]
            c1 = counters[resets[1]]
            if c0 is not None and c1 is not None:
                report["loop_period_outputs"] = c1 - c0
        # media-time span of one loop = max rtp within the first loop segment
        seg = rtp_cont[resets[0] + 1: (resets[1] + 1 if len(resets) >= 2 else len(rtp_cont))]
        if seg:
            span = seg[-1] - seg[0]
            report["loop_period_seconds"] = round(span / RTP_CLOCK_HZ, 3)
            if grid:
                report["loop_period_source_frames"] = round(span / grid) + 1

    # Dropped outputs: counter gaps (>1).
    counters = [r["counter"] for r in rows if r["counter"] is not None]
    cgaps = [(a, b, b - a) for a, b in zip(counters, counters[1:]) if b - a > 1]
    report["counter_gaps"] = len(cgaps)
    report["counter_dropped_total"] = sum(g[2] - 1 for g in cgaps)

    # rtp <-> capture lock check (do both clocks agree?).
    caps = [r["capture_timestamp_ns"] for r in rows]
    pairs = [
        ((rtp_cont[i + 1] - rtp_cont[i]) / RTP_CLOCK_HZ, (caps[i + 1] - caps[i]) / 1e9)
        for i in range(len(rtp_cont) - 1)
        if caps[i] is not None and caps[i + 1] is not None and deltas[i] > 0
    ]
    if pairs:
        max_skew = max(abs(rt - cp) for rt, cp in pairs)
        report["rtp_capture_max_skew_s"] = round(max_skew, 6)

    report["sessions"] = sorted({r["session_id"] for r in rows if r["session_id"]})
    return report


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seconds", type=float, default=80.0, help="How long to tail the stream (default 80).")
    ap.add_argument("--fixture", default=None, help="Optional path to dump observed messages as JSONL.")
    args = ap.parse_args()

    def req(name: str) -> str:
        v = os.environ.get(name)
        if not v:
            print(f"ERROR: missing env var {name}", file=sys.stderr)
            sys.exit(2)
        return v

    host = os.environ.get("REDIS_HOST", "127.0.0.1")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    password = req("REDIS_PASSWORD")
    cam = req("CAM_ID")
    dep = req("APP_DEPLOYMENT_ID")

    key = stream_key(cam, dep)
    r = redis_lib.Redis(host=host, port=port, password=password, decode_responses=True)
    print(f"[probe] PING {r.ping()}  stream={key}  tailing {args.seconds:.0f}s ...")

    rows: list[dict] = []
    fx = open(args.fixture, "w") if args.fixture else None
    last_id = "$"
    deadline = time.monotonic() + args.seconds
    try:
        while time.monotonic() < deadline:
            streams = r.xread({key: last_id}, count=100, block=500)
            if not streams:
                continue
            for _sn, messages in streams:
                for msg_id, values in messages:
                    last_id = msg_id
                    if fx:
                        fx.write(json.dumps({"id": msg_id, "values": values}) + "\n")
                    row = parse_message(values)
                    if row:
                        rows.append(row)
    except KeyboardInterrupt:
        print("\n[probe] interrupted — analysing what we have")
    finally:
        if fx:
            fx.close()
            print(f"[probe] wrote {len(rows)} messages to fixture {args.fixture}")

    report = probe(rows)
    print("\n" + "=" * 64)
    print("RTP PROBE REPORT")
    print("=" * 64)
    print(json.dumps(report, indent=2))
    print("=" * 64)
    if report.get("case", "").startswith("A"):
        print("Case A: collector anchors loop-start on rtp reset → exact src-frame-0.")
    elif report.get("case", "").startswith("B"):
        print("Case B: no reset seen — collector must segment by loop_span and may")
        print("        need a one-time phase offset to gt-tracked.json. Run longer to")
        print("        confirm no reset exists.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
