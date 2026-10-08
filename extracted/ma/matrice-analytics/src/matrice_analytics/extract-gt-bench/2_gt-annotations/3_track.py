"""
3_track.py — assign ByteTrack track_ids to the verified boxes -> final GT.

Step 3 of section 2:  consolidate -> verify -> [track].

Input is the verified JSON from `2_verify.py`.  Its `frames` map is SPARSE — keyed
by the subsampled source-frame indices, not 0..N — because the VMS only processed
every 3rd-4th frame.  ByteTrack runs over those keys in ascending order (it sees
them as consecutive updates).  Because real time between two samples is 3-4 source
frames, keep `--lost-buffer` generous so a track survives the gaps.

Output is the ground-truth JSON consumed by section 3 (benchmarking) as `--gt`.

Usage
-----
    python 3_track.py --video path/to/test-vms-gt.mp4 \
        --json verified.json --out-json gt-tracked.json
    # also write an overlay video of the sampled frames:
    python 3_track.py --video gt.mp4 --json verified.json \
        --out-json gt-tracked.json --out-video gt-tracked.mp4
"""

import argparse
import json
import logging
import sys
from pathlib import Path

import cv2
import numpy as np
import supervision as sv
from loitering_common import color_for_class, ensure_loitering_class_names

_logger = logging.getLogger(__name__)


def _configure_cli_logging() -> None:
    """Send INFO to stdout and ERROR to stderr, with no level/name decoration.

    This script is an operator CLI: its stdout IS its output, and the previous
    print() calls wrote the bare message with no prefix. A plain logger would
    change both the stream and the text, so the handlers below reproduce the
    original split exactly -- progress lines on stdout, errors on stderr, format
    "%(message)s". Writes are flushed per record, matching the former
    print(..., flush=True).
    """
    if _logger.handlers:
        return
    out = logging.StreamHandler(sys.stdout)
    out.setLevel(logging.INFO)
    out.addFilter(lambda record: record.levelno < logging.ERROR)
    out.setFormatter(logging.Formatter("%(message)s"))
    err = logging.StreamHandler(sys.stderr)
    err.setLevel(logging.ERROR)
    err.setFormatter(logging.Formatter("%(message)s"))
    _logger.addHandler(out)
    _logger.addHandler(err)
    _logger.setLevel(logging.INFO)
    _logger.propagate = False


def color_for(tid, class_id=0):
    if int(class_id) == 1:
        return color_for_class(1)
    if tid >= 0:
        palette = [
            (56, 64, 238),
            (140, 237, 224),
            (255, 184, 16),
            (98, 228, 134),
            (38, 72, 224),
            (227, 142, 255),
            (255, 219, 79),
            (122, 179, 255),
        ]
        return palette[int(tid) % len(palette)]
    return color_for_class(int(class_id))


def parse_args():
    p = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    p.add_argument("--video", required=True, help="Original source video (for the overlay render).")
    p.add_argument(
        "--json", required=True, help="Verified detections JSON (output of 2_verify.py)."
    )
    p.add_argument(
        "--out-json", required=True, help="Final ground-truth JSON with track_id per box."
    )
    p.add_argument(
        "--out-video", default=None, help="Optional overlay video of the sampled frames."
    )
    p.add_argument(
        "--phase-offset",
        type=int,
        default=0,
        help="Add to each src_idx before seeking the video (must match 2_verify.py).",
    )
    p.add_argument(
        "--frame-rate",
        type=int,
        default=None,
        help="ByteTrack frame_rate; default = JSON fps. Lower it toward the effective "
        "sampled fps (~8) if tracks fragment across the subsample gaps.",
    )
    p.add_argument("--track-thresh", type=float, default=0.25)
    p.add_argument("--match-thresh", type=float, default=0.8)
    p.add_argument("--lost-buffer", type=int, default=30)
    return p.parse_args()


def assign_track_ids(data, frame_rate, track_thresh, match_thresh, lost_buffer):
    frames = data["frames"]
    width, height = int(data["width"]), int(data["height"])
    keys = sorted(frames.keys(), key=int)

    tracker = sv.ByteTrack(
        track_activation_threshold=track_thresh,
        lost_track_buffer=lost_buffer,
        minimum_matching_threshold=match_thresh,
        frame_rate=int(frame_rate) if frame_rate else 30,
        minimum_consecutive_frames=1,
    )
    seen = set()
    n = len(keys)
    for fi, k in enumerate(keys):
        if fi % 100 == 0 or fi == n - 1:
            _logger.info("  tracking %s/%s ...", fi + 1, n)
        dets = frames[k]
        for d in dets:
            d["track_id"] = -1
        if not dets:
            tracker.update_with_detections(sv.Detections.empty())
            continue
        xyxy = np.array(
            [
                [
                    d["bbox"][0] * width,
                    d["bbox"][1] * height,
                    d["bbox"][2] * width,
                    d["bbox"][3] * height,
                ]
                for d in dets
            ],
            dtype=np.float32,
        )
        conf = np.array([float(d.get("confidence", 1.0)) for d in dets], dtype=np.float32)
        cls = np.array([int(d["class_id"]) for d in dets], dtype=int)
        tracked = tracker.update_with_detections(
            sv.Detections(xyxy=xyxy, confidence=conf, class_id=cls)
        )
        if tracked.tracker_id is None or len(tracked) == 0:
            continue
        for i in range(len(tracked)):
            tid = int(tracked.tracker_id[i])
            tx = tracked.xyxy[i]
            for j, d in enumerate(dets):
                if d["track_id"] != -1:
                    continue
                if (
                    abs(xyxy[j, 0] - tx[0]) < 0.5
                    and abs(xyxy[j, 1] - tx[1]) < 0.5
                    and abs(xyxy[j, 2] - tx[2]) < 0.5
                    and abs(xyxy[j, 3] - tx[3]) < 0.5
                ):
                    d["track_id"] = tid
                    seen.add(tid)
                    break
    return len(seen)


def render(video_path, out_path, data, phase_offset):
    frames = data["frames"]
    class_names = data.get("class_names", {})
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        _logger.error("ERROR: cannot open %s", video_path)
        sys.exit(1)
    fps = float(data.get("fps") or cap.get(cv2.CAP_PROP_FPS) or 30.0)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
    if not writer.isOpened():
        _logger.error("ERROR: cannot open writer for %s", out_path)
        sys.exit(1)
    samples = sorted(frames.keys(), key=int)
    for n, k in enumerate(samples):
        if n % 100 == 0:
            _logger.info("  rendering %s/%s ...", n + 1, len(samples))
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(k) + phase_offset)
        ok, frame = cap.read()
        if not ok:
            continue
        for d in frames[k]:
            cid = int(d["class_id"])
            tid = int(d.get("track_id", -1))
            x1, y1 = int(d["bbox"][0] * w), int(d["bbox"][1] * h)
            x2, y2 = int(d["bbox"][2] * w), int(d["bbox"][3] * h)
            c = color_for(tid if tid >= 0 else cid, cid)
            cv2.rectangle(frame, (x1, y1), (x2, y2), c, 2)
            name = class_names.get(str(cid), str(cid))
            label = f"#{tid} {name}" if tid >= 0 else name
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(frame, (x1, max(0, y1 - th - 6)), (x1 + tw + 6, y1), c, -1)
            cv2.putText(
                frame,
                label,
                (x1 + 3, max(th + 1, y1 - 4)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
        writer.write(frame)
    cap.release()
    writer.release()


def main():
    _configure_cli_logging()
    args = parse_args()
    _logger.info("Loading verified JSON (%s) ...", args.json)
    data = json.loads(Path(args.json).read_text())
    if "frames" not in data:
        sys.exit("ERROR: input JSON has no 'frames' key")
    data["class_names"] = ensure_loitering_class_names(data.get("class_names"))
    frame_rate = args.frame_rate or float(data.get("fps") or 30.0)

    _logger.info(
        "Running ByteTrack over %s sampled frames (frame_rate=%s, lost_buffer=%s) ...",
        len(data["frames"]),
        int(frame_rate),
        args.lost_buffer,
    )
    n = assign_track_ids(data, frame_rate, args.track_thresh, args.match_thresh, args.lost_buffer)
    Path(args.out_json).write_text(json.dumps(data, indent=2))
    _logger.info("tracking done. unique track ids: %s -> %s", n, args.out_json)

    if args.out_video:
        _logger.info("Rendering overlay -> %s ...", args.out_video)
        render(args.video, args.out_video, data, args.phase_offset)
        _logger.info("wrote %s", args.out_video)


if __name__ == "__main__":
    main()
