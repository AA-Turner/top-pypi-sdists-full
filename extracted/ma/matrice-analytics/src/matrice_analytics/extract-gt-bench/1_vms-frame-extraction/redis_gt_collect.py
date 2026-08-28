"""
redis_gt_collect.py — collect inference output aligned to the ORIGINAL video.

The media server streams the GT video as a looping RTSP camera
(`ffmpeg -re -stream_loop -1 ... -c:v copy`).  Inference subsamples source frames
(measured: 30 fps source, ~every 3rd–4th frame processed), so a per-output
counter does NOT equal a source frame index.  Each output instead carries
`rtp_timestamp` (90 kHz media clock); this collector maps every output to its
exact source frame via the source video's PTS table (see rtp_map.py).

No video wrapping, no marker/silence/buffer envelope, no blank↔detection state
machine — those only ever found loop boundaries indirectly.  Here we read the raw
stream and align by media time.

Output: one `frame-{src_idx:06d}.json` per processed source frame (last write
wins), plus a run-level `meta.json` with the mapping parameters and a coverage
report.  In Case A (rtp resets each loop) src_idx is the TRUE source index.  In
Case B (continuous rtp — the common case here) src_idx is correct up to a single
constant rotation, resolved against gt-tracked.json at conversion time.

Env vars
--------
  Required:
    REDIS_PASSWORD, CAM_ID, APP_DEPLOYMENT_ID
    GT_FRAMES_DIR        output directory
    GT_SOURCE_VIDEO      path to the ORIGINAL (unwrapped) GT video — ffprobe'd
  Optional:
    REDIS_HOST (127.0.0.1), REDIS_PORT (6379)
    GT_LOOPS (1)         number of full loops of media time to collect
    GT_LOOP_MODE (auto)  auto | reset | modulo
    GT_MAX_SECONDS       wall-clock safety cap (default: 3 × loop seconds + 120)
    GT_FROM_START (off)  =1 to read from the OLDEST stream entry instead of only new
                         outputs. Start the collector right after (re)starting the file
                         camera and the first output is ~source frame 0 — so src_idx is
                         absolute (no Case B phase offset to resolve later).
"""

import json
import logging
import os
import pathlib
import sys
import time

import redis as redis_lib

from rtp_map import LoopMapper, build_pts_reference

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


def stream_key(camera_id: str, app_deployment_id: str) -> str:
    return f"{camera_id}_{app_deployment_id}_output_topic"


def parse_payload(values: dict) -> dict | None:
    """Extract the fields we align/save from one stream entry."""
    raw = values.get("result") or values.get("data")
    if not raw:
        return None
    try:
        p = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None
    if p.get("rtp_timestamp") is None:
        return None
    fid = p.get("frame_id", "") or ""
    suffix = fid.rsplit("_", 1)[-1] if fid else ""
    try:
        counter = int(suffix)
    except ValueError:
        counter = None
    return {
        "rtp_timestamp": int(p["rtp_timestamp"]) & 0xFFFFFFFF,
        "frame_id": fid,
        "counter": counter,
        "capture_timestamp_ns": p.get("capture_timestamp_ns"),
        "detections": p.get("detections") or [],          # top-level (most apps)
        "agg_summary": p.get("agg_summary") or {},         # tracking-stats apps
    }


def run_collection(
    messages,
    ref,
    out_dir: pathlib.Path,
    loops: int = 1,
    mode: str = "auto",
    max_frames: int | None = None,
    log_every: int = 100,
) -> dict:
    """
    Drive the mapper over an iterable of parsed payloads, saving aligned frames.

    `messages` yields dicts from parse_payload.  Returns a report dict and writes
    `meta.json` into out_dir.  Stops after `loops` full loops of media time (or
    max_frames).  Pure — no Redis dependency, so the replay test reuses it.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    force = None if mode == "auto" else mode
    mapper = LoopMapper(ref, force_mode=force)

    first_cont: int | None = None
    coverage: dict[int, int] = {}
    saved = 0
    span = ref.loop_span_ticks

    for payload in messages:
        res = mapper.feed(payload["rtp_timestamp"])
        if first_cont is None:
            first_cont = res.cont_ticks

        record = {
            "src_idx": res.src_idx,
            "loop_index": res.loop_index,
            "pos_ticks": res.pos_ticks,
            "rtp_timestamp": payload["rtp_timestamp"],
            "frame_id": payload["frame_id"],
            "counter": payload["counter"],
            "detections": payload["detections"],
            "agg_summary": payload["agg_summary"],
        }
        with open(out_dir / f"frame-{res.src_idx:06d}.json", "w") as f:
            json.dump(record, f, indent=2)

        coverage[res.src_idx] = coverage.get(res.src_idx, 0) + 1
        saved += 1
        if saved % log_every == 0:
            log.info(
                "[COLLECT] saved=%d covered=%d/%d loop=%d mode=%s src_idx=%d",
                saved, len(coverage), ref.n_frames, res.loop_index, mapper.mode or "pre", res.src_idx,
            )

        elapsed = res.cont_ticks - first_cont
        if span > 0 and loops and elapsed >= loops * span:
            log.info("[COLLECT] %d loop(s) of media time elapsed -> stop", loops)
            break
        if max_frames and saved >= max_frames:
            log.info("[COLLECT] max_frames=%d reached -> stop", max_frames)
            break

    missing = [i for i in range(ref.n_frames) if i not in coverage]
    report = {
        "source_video": ref.video_path,
        "n_source_frames": ref.n_frames,
        "source_fps": ref.fps,
        "frame_interval_ticks": ref.frame_interval_ticks,
        "loop_span_ticks": span,
        "mode": mapper.mode or "pre",
        "outputs_saved": saved,
        "source_frames_covered": len(coverage),
        "coverage_fraction": round(len(coverage) / ref.n_frames, 4) if ref.n_frames else 0,
        "missing_count": len(missing),
        "duplicate_writes": sum(c - 1 for c in coverage.values() if c > 1),
        "loops_observed": (mapper.loop_index + 1),
    }
    with open(out_dir / "meta.json", "w") as f:
        json.dump({**report, "missing_src_idx": missing}, f, indent=2)

    log.info("=" * 60)
    log.info("COLLECTION REPORT")
    for k, v in report.items():
        log.info("  %-24s %s", k, v)
    if report["mode"] == "modulo":
        log.info("  NOTE: Case B (continuous rtp) — src_idx is rotated by a constant;")
        log.info("        resolve absolute phase against gt-tracked.json at conversion.")
    log.info("=" * 60)
    return report


def redis_messages(r, key: str, max_seconds: float, start_id: str = "$"):
    """Yield parsed payloads from a live Redis stream until max_seconds elapse.

    start_id="$"  -> only NEW outputs (default; src_idx is rotated by an unknown S in Case B).
    start_id="0"  -> from the OLDEST retained entry. If you START the collector within the
                     stream's history window (~MAXLEN entries, ~12s) of (re)starting the file
                     camera, the first output is ~source frame 0, so the resulting src_idx is
                     absolute (S ~= 0) with NO phase guessing needed.
    """
    last_id = start_id
    deadline = time.monotonic() + max_seconds
    while time.monotonic() < deadline:
        try:
            streams = r.xread({key: last_id}, count=50, block=500)
        except redis_lib.exceptions.ConnectionError as exc:
            log.error("Redis connection lost: %s", exc)
            raise
        except Exception as exc:
            if "i/o timeout" in str(exc):
                continue
            raise
        if not streams:
            continue
        for _sn, messages in streams:
            for msg_id, values in messages:
                last_id = msg_id
                payload = parse_payload(values)
                if payload:
                    yield payload
    log.warning("[COLLECT] max_seconds safety cap reached")


if __name__ == "__main__":
    def req(name: str) -> str:
        v = os.environ.get(name)
        if not v:
            log.error("Missing required env var: %s", name)
            sys.exit(1)
        return v

    host = os.environ.get("REDIS_HOST", "127.0.0.1")
    port = int(os.environ.get("REDIS_PORT", "6379"))
    password = req("REDIS_PASSWORD")
    cam = req("CAM_ID")
    dep = req("APP_DEPLOYMENT_ID")
    out_dir = pathlib.Path(req("GT_FRAMES_DIR"))
    source_video = req("GT_SOURCE_VIDEO")
    loops = int(os.environ.get("GT_LOOPS", "1"))
    mode = os.environ.get("GT_LOOP_MODE", "auto")
    # GT_FROM_START=1 -> read from the oldest retained entry so collection begins at the
    # loop boundary (src_idx becomes absolute). Only meaningful if you start the collector
    # right after (re)starting the file camera; otherwise the oldest entry is arbitrary phase.
    from_start = os.environ.get("GT_FROM_START", "") in ("1", "true", "True", "yes")
    start_id = "0" if from_start else "$"

    log.info("Building PTS reference from %s ...", source_video)
    ref = build_pts_reference(source_video)
    log.info(
        "Source: %d frames @ %.3f fps, frame_interval=%d ticks, loop_span=%d ticks (%.2fs)",
        ref.n_frames, ref.fps, ref.frame_interval_ticks, ref.loop_span_ticks,
        ref.loop_span_ticks / 90000,
    )

    default_cap = 3 * (ref.loop_span_ticks / 90000) * max(loops, 1) + 120
    max_seconds = float(os.environ.get("GT_MAX_SECONDS", default_cap))

    key = stream_key(cam, dep)
    r = redis_lib.Redis(host=host, port=port, password=password, decode_responses=True)
    log.info("Connecting to Redis %s:%s — PING %s", host, port, r.ping())
    log.info("Tailing %s (loops=%d mode=%s max_seconds=%.0f start_id=%s)",
             key, loops, mode, max_seconds, start_id)
    if from_start:
        log.info("[COLLECT] GT_FROM_START=1 -> reading from oldest entry; first output "
                 "should be ~source frame 0 (start the camera just before this).")

    run_collection(redis_messages(r, key, max_seconds, start_id), ref, out_dir, loops=loops, mode=mode)
