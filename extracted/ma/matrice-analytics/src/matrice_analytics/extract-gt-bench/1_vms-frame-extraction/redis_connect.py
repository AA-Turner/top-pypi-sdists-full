"""
redis_connect.py

Python port of PredictionWebSocketService.consumeOutputStream (Go).
Reads live predictions from a Redis stream and fans them out via a
callback (write_pred), mirroring the Go logic exactly:
  - Starts from "$" (latest only)
  - Skips stale messages (>5 s old)
  - Emits idle warnings while the stream stays silent
  - Emits a "predictions_resumed" status when the stream comes back
  - Logs periodic stats every 60 s
"""

import json
import logging
import time
from datetime import datetime, timezone
from typing import Any, Callable

import redis as redis_lib

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants (mirror Go)
# ---------------------------------------------------------------------------
BLOCK_MS            = 100          # XRead block window (milliseconds)
READ_COUNT          = 100          # messages per XRead call
STALE_THRESHOLD_S   = 5.0          # skip predictions older than this
IDLE_WARN_THRESHOLD = 5.0          # seconds of silence before idle warning
IDLE_NOTIFY_INTERVAL = 2.0         # seconds between repeated idle notifications
STATS_INTERVAL      = 60.0         # seconds between debug stats logs


def prediction_output_stream_key(camera_id: str, app_deployment_id: str) -> str:
    return f"{camera_id}_{app_deployment_id}_output_topic"


# ---------------------------------------------------------------------------
# Idle notifier (mirrors notifyIdleIfNeeded in Go)
# ---------------------------------------------------------------------------
def _notify_idle_if_needed(
    write_pred: Callable[[dict], None],
    camera_id: str,
    app_deployment_id: str,
    stream_name: str,
    last_msg_time: float,
    idle_warn_threshold: float,
    idle_notify_interval: float,
    last_idle_notify: list,   # mutable box: [float]
    was_idle: list,           # mutable box: [bool]
) -> None:
    silence = time.monotonic() - last_msg_time
    if silence < idle_warn_threshold:
        return
    now = time.monotonic()
    if now - last_idle_notify[0] < idle_notify_interval:
        return
    last_idle_notify[0] = now
    was_idle[0] = True
    log.warning(
        "No predictions received for %.1fs — stream may be idle. "
        "camera_id=%s stream=%s",
        silence, camera_id, stream_name,
    )
    try:
        write_pred({
            "type":              "status",
            "status":            "predictions_idle",
            "message":           f"No predictions received for {silence:.1f}s",
            "camera_id":         camera_id,
            "app_deployment_id": app_deployment_id,
        })
    except Exception as exc:
        log.debug("idle status broadcast failed: %s", exc)


# ---------------------------------------------------------------------------
# Main consumer (mirrors consumeOutputStream in Go)
# ---------------------------------------------------------------------------
def consume_output_stream(
    r: redis_lib.Redis,
    camera_id: str,
    app_deployment_id: str,
    write_pred: Callable[[dict], None],
    stop_event=None,   # threading.Event or similar; None = run forever
) -> None:
    """
    Blocking loop that reads from the Redis prediction stream and calls
    write_pred(msg) for every live, non-stale message.

    Parameters
    ----------
    r               : connected redis.Redis client
    camera_id       : camera identifier
    app_deployment_id: deployment identifier
    write_pred      : callback(dict) — called for every outgoing message
    stop_event      : optional threading.Event; loop exits when set
    """
    log.info(
        "Starting output stream consumer... camera_id=%s app_deployment_id=%s",
        camera_id, app_deployment_id,
    )

    stream_name = prediction_output_stream_key(camera_id, app_deployment_id)
    log.debug("Redis prediction consumer starting topic=%s", stream_name)

    # Always start from latest — client wants live predictions, not history.
    last_id = "$"
    log.info("Output consumer ready stream=%s start_id=%s", stream_name, last_id)

    # Stats
    sent_count    = 0
    stale_skipped = 0
    last_stats_log = time.monotonic()

    # Idle tracking
    last_msg_time    = time.monotonic()
    last_idle_notify = [0.0]   # mutable box
    was_idle         = [False] # mutable box

    def _stopped() -> bool:
        return stop_event is not None and stop_event.is_set()

    while not _stopped():

        # ── Periodic stats ──────────────────────────────────────────────
        if time.monotonic() - last_stats_log > STATS_INTERVAL:
            log.debug(
                "Prediction WS consumer stats camera_id=%s sent=%d stale_skipped=%d period=60s",
                camera_id, sent_count, stale_skipped,
            )
            sent_count    = 0
            stale_skipped = 0
            last_stats_log = time.monotonic()

        # ── XRead ───────────────────────────────────────────────────────
        try:
            streams = r.xread(
                {stream_name: last_id},
                count=READ_COUNT,
                block=BLOCK_MS,
            )
        except redis_lib.exceptions.ConnectionError as exc:
            log.error("Redis connection error: %s", exc)
            raise
        except Exception as exc:
            if "i/o timeout" in str(exc):
                continue
            log.error("Failed to read from Redis: %s", exc)
            raise

        # No new messages (block window expired)
        if not streams:
            _notify_idle_if_needed(
                write_pred, camera_id, app_deployment_id, stream_name,
                last_msg_time, IDLE_WARN_THRESHOLD, IDLE_NOTIFY_INTERVAL,
                last_idle_notify, was_idle,
            )
            continue

        # ── Process messages ─────────────────────────────────────────────
        jump_to_latest = False

        for _stream_name, messages in streams:
            if jump_to_latest:
                break

            for msg_id, values in messages:
                if _stopped():
                    log.debug("Stop event set, exiting consumer camera_id=%s", camera_id)
                    return

                # ── Parse prediction data ────────────────────────────────
                prediction_data: dict[str, Any] | None = None

                # 1. Try "data" field (nested JSON)
                if "data" in values:
                    data_val = values["data"]
                    if isinstance(data_val, str):
                        try:
                            prediction_data = json.loads(data_val)
                        except json.JSONDecodeError:
                            log.warning("Failed to parse data field as JSON string")
                    elif isinstance(data_val, dict):
                        prediction_data = data_val

                # 2. Fall back: scan all fields for a valid JSON map
                if prediction_data is None:
                    for _k, v in values.items():
                        if isinstance(v, str) and v:
                            try:
                                parsed = json.loads(v)
                                if isinstance(parsed, dict):
                                    prediction_data = parsed
                                    break
                            except json.JSONDecodeError:
                                pass

                if prediction_data is None:
                    log.warning("Could not parse prediction data from any field msg_id=%s", msg_id)
                    continue

                # ── Stale check ──────────────────────────────────────────
                processed_ts_raw = prediction_data.get("processed_timestamp", "")
                if processed_ts_raw:
                    try:
                        parsed_ts = datetime.fromisoformat(processed_ts_raw)
                        age = (datetime.now(timezone.utc) - parsed_ts).total_seconds()
                        if age > STALE_THRESHOLD_S:
                            stale_skipped += 1
                            log.debug(
                                "Skipping stale prediction, jumping to latest "
                                "camera_id=%s age=%.2fs",
                                camera_id, age,
                            )
                            last_id = "$"
                            jump_to_latest = True
                            break   # continue readLoop equivalent
                    except ValueError:
                        pass

                # ── Build outgoing message ───────────────────────────────
                frame_id           = prediction_data.get("frame_id", "")
                capture_ts_ns      = int(prediction_data.get("capture_timestamp_ns") or 0)
                rtp_timestamp      = int(prediction_data.get("rtp_timestamp") or 0)

                prediction_msg: dict[str, Any] = {
                    "type":                 "prediction",
                    "frame_id":             frame_id,
                    "capture_timestamp_ns": capture_ts_ns,
                    "camera_id":            camera_id,
                    "app_deployment_id":    app_deployment_id,
                    "rtp_timestamp":        rtp_timestamp,
                }

                if "detections" in prediction_data:
                    prediction_msg["detections"] = prediction_data["detections"]
                if "agg_summary" in prediction_data:
                    prediction_msg["agg_summary"] = prediction_data["agg_summary"]
                if "metadata" in prediction_data:
                    prediction_msg["metadata"] = prediction_data["metadata"]
                if "processed_timestamp" in prediction_data:
                    prediction_msg["processed_timestamp"] = prediction_data["processed_timestamp"]

                # ── Fan out ──────────────────────────────────────────────
                if _stopped():
                    log.debug("Context cancelled, stopping consumer camera_id=%s", camera_id)
                    return

                try:
                    write_pred(prediction_msg)
                except Exception as exc:
                    log.error("Failed to send prediction: %s", exc)
                    raise

                # Advance cursor
                last_id    = msg_id
                sent_count += 1
                last_msg_time = time.monotonic()

                # Resumed after idle
                if was_idle[0]:
                    log.info(
                        "Predictions resumed from ML side camera_id=%s "
                        "app_deployment_id=%s stream=%s",
                        camera_id, app_deployment_id, stream_name,
                    )
                    try:
                        write_pred({
                            "type":              "status",
                            "status":            "predictions_resumed",
                            "message":           "Predictions resumed from ML side",
                            "camera_id":         camera_id,
                            "app_deployment_id": app_deployment_id,
                        })
                    except Exception as exc:
                        log.debug(
                            "prediction resume status broadcast failed camera_id=%s error=%s",
                            camera_id, exc,
                        )
                    was_idle[0]         = False
                    last_idle_notify[0] = 0.0


# ---------------------------------------------------------------------------
# Entrypoint — export these env vars before running:
#
#   Required:
#     export REDIS_PASSWORD="..."
#     export APP_DEPLOYMENT_ID="..."
#     export CAM_ID="..."
#     export GT_FRAMES_DIR="/home/mleng1/frames/vehicle-counting/gt-frames"
#     export GT_FRAME_COUNT="500"          # number of frames to collect then stop
#
#   Optional (have defaults):
#     export REDIS_HOST="127.0.0.1"
#     export REDIS_PORT="6379"
#
#   Run:
#     python3 redis_connect.py
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    import sys
    import threading
    import pathlib

    def _require(name: str) -> str:
        val = os.environ.get(name)
        if not val:
            log.error("Missing required env var: %s", name)
            sys.exit(1)
        return val

    REDIS_HOST        = os.environ.get("REDIS_HOST", "127.0.0.1")
    REDIS_PORT        = int(os.environ.get("REDIS_PORT", "6379"))
    REDIS_PASSWORD    = _require("REDIS_PASSWORD")
    APP_DEPLOYMENT_ID = _require("APP_DEPLOYMENT_ID")
    CAM_ID            = _require("CAM_ID")
    GT_FRAMES_DIR     = _require("GT_FRAMES_DIR")
    GT_FRAME_COUNT    = int(_require("GT_FRAME_COUNT"))

    # Ensure output directory exists
    out_dir = pathlib.Path(GT_FRAMES_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)

    log.info(
        "Config: host=%s port=%d cam_id=%s app_deployment_id=%s",
        REDIS_HOST, REDIS_PORT, CAM_ID, APP_DEPLOYMENT_ID,
    )
    log.info(
        "GT collection: dir=%s target_frames=%d",
        GT_FRAMES_DIR, GT_FRAME_COUNT,
    )

    r = redis_lib.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        password=REDIS_PASSWORD,
        decode_responses=True,
    )
    log.info("PING: %s", r.ping())

    # Stop signal — set when GT_FRAME_COUNT frames have been saved
    stop_event = threading.Event()
    saved_count = [0]  # mutable box

    def write_pred(msg: dict) -> None:
        # Only process prediction frames (skip status messages)
        if msg.get("type") != "prediction":
            return

        agg_summary = msg.get("agg_summary")
        if not agg_summary:
            return

        raw_frame_id = msg.get("frame_id", "unknown")
        # frame_id is e.g. "shm_cam_9824_265293" — extract the numeric suffix
        frame_id = raw_frame_id.rsplit("_", 1)[-1]

        # Write agg_summary only to frames/[app-name]/gt-frames/frame-[frame_id].json
        out_file = out_dir / f"frame-{frame_id}.json"
        with open(out_file, "w") as f:
            json.dump(agg_summary, f, indent=2)

        saved_count[0] += 1
        log.info(
            "[%d/%d] saved frame-%s.json",
            saved_count[0], GT_FRAME_COUNT, frame_id,
        )

        # Stop once we've collected enough frames
        if saved_count[0] >= GT_FRAME_COUNT:
            log.info(
                "Collected %d frames — done. Output: %s",
                GT_FRAME_COUNT, GT_FRAMES_DIR,
            )
            stop_event.set()

    consume_output_stream(r, CAM_ID, APP_DEPLOYMENT_ID, write_pred, stop_event=stop_event)
