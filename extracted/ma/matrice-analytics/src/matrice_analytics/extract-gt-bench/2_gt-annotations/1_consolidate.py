"""
1_consolidate.py — fold a folder of VMS frame-*.json into ONE predictions JSON.

Input  : the unzipped collection from section 1 (`1_vms-frame-extraction`):
            frame-{src_idx:06d}.json  (one per processed/subsampled source frame)
            meta.json                 (run summary: n_source_frames, fps, coverage)

Output : a single JSON keyed by the TRUE source frame index, carrying per-frame
         detections (+category), and — pulled out of the VMS agg_summary — the
         per-frame alerts and tracking counts.  This file is the "VMS predictions"
         (what the deployed model said) and is the `--pred` input to section 3.

    {
      "video": "", "width": 1920, "height": 1080, "fps": 30.0,
      "class_names": {"0": "person", "1": "loitering_person"},
      "usecase": "loitering_detection", "n_frames": 2150, "phase_offset": 0,
      "source": "vms",
      "frames": { "0": [ {class_id, confidence, bbox, category, track_id}, ... ] },
      "alerts": { "0": [ ... ] },                  # only frames that carried alerts
      "counts": { "0": {total_counts, current_counts} }   # only frames that carried them
    }

`frames` stays a flat {idx: [detections]} map so it feeds the benchmark harness
directly.  `alerts` / `counts` are sibling maps so the detection schema is
untouched.  Keys are sparse — only subsampled (processed) source frames appear,
which is correct: only those frames have a prediction to score.

Detections come from `agg_summary[*].tracking_stats.detections` (the post-processed
boxes the analytics actually tracked/counted) by default; pass
`--detections_source model` to use the raw top-level model `detections` instead.
The tracking_stats boxes carry only `category` + `bounding_box`, so class_id is
looked up from category and confidence/track_id get defaults.  Boxes are
auto-detected as pixel vs normalised.

Phase (Case B): when the live RTP clock runs continuously across loops (the usual
case — see section 1), src_idx is correct up to a constant rotation S.  Pass
`--gt_tracked gt.json --resolve_phase` to recover S by cross-correlating per-frame
detection counts, or `--phase_offset N` to apply a known shift.  Case A (rtp
resets each loop) needs neither.

Usage
-----
    python 1_consolidate.py --input_folder loitering-test \
        --output_file vms-pred.json \
        --class_names "person=0,loitering_person=1" \
        --usecase loitering_detection
"""

import argparse
import json
import os
import re
import sys


def _parse_class_names(raw: str) -> dict:
    mapping = {}
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "=" not in part:
            raise ValueError(f"Expected 'name=id', got: {part!r}")
        name, idx = part.rsplit("=", 1)
        mapping[name.strip()] = int(idx.strip())
    return mapping


def _src_idx_from_name(path: str) -> int:
    nums = re.findall(r"\d+", os.path.basename(path))
    return int(nums[0]) if nums else 0


def _normalise_bbox(bb: dict, width: int, height: int) -> list:
    """Pixel->[0,1] unless values are already normalised (max<=1)."""
    vals = [bb["xmin"], bb["ymin"], bb["xmax"], bb["ymax"]]
    if max(vals) <= 1.0:
        return [round(v, 6) for v in vals]
    return [bb["xmin"] / width, bb["ymin"] / height, bb["xmax"] / width, bb["ymax"] / height]


def _agg_blocks(data: dict):
    """Yield each per-frame agg_summary block (the values under agg_summary)."""
    agg = data.get("agg_summary")
    if isinstance(agg, dict):
        for v in agg.values():
            if isinstance(v, dict):
                yield v


def _model_detections(data: dict) -> list:
    """Raw top-level model detections (class_id, confidence, track_id, box)."""
    top = data.get("detections")
    return top if isinstance(top, list) else []


def _tracking_stats_detections(data: dict) -> list:
    """Post-processed detections the analytics actually tracked/counted
    (agg_summary[*].tracking_stats.detections — category + bounding_box only)."""
    dets: list = []
    for block in _agg_blocks(data):
        dets.extend(block.get("tracking_stats", {}).get("detections", []) or [])
    return dets


def _raw_detections(data: dict, source: str = "tracking_stats") -> list:
    """
    Pull the detection list out of a VMS record, from the requested source, with
    the other as a fallback when the preferred one is empty.

      source="tracking_stats" (default): agg_summary tracking_stats.detections
      source="model"                  : top-level model `detections`
    """
    return (
        _tracking_stats_detections(data)
        if source == "tracking_stats"
        else _model_detections(data)
    )


def _frame_alerts(data: dict) -> list:
    """Collect any alerts/incidents the VMS emitted for this frame."""
    out: list = []
    top = data.get("alerts")
    if isinstance(top, list) and top:
        out.extend(top)
    for block in _agg_blocks(data):
        ts = block.get("tracking_stats", {})
        for a in ts.get("alerts", []) or []:
            out.append(a)
        for a in block.get("alerts", []) or []:
            out.append(a)
        inc = ts.get("incidents") or block.get("incidents")
        if isinstance(inc, dict) and inc:
            out.append({"incidents": inc})
    return out


def _frame_counts(data: dict) -> dict:
    """Collect tracking counts (total/current) the VMS emitted for this frame."""
    for block in _agg_blocks(data):
        ts = block.get("tracking_stats", {})
        counts = {}
        for key in ("total_counts", "current_counts", "total_current_counts"):
            if ts.get(key):
                counts[key] = ts[key]
        if counts:
            return counts
    return {}


def _convert_detections(raw: list, category_to_id: dict, width: int, height: int, src_idx: int) -> list:
    out = []
    for det in raw:
        category = det.get("category", "")
        class_id = det.get("class_id")
        if class_id is None:
            if category not in category_to_id:
                print(f"  [WARN] unknown category {category!r} @src_idx {src_idx}, skipping")
                continue
            class_id = category_to_id[category]
        bb = det.get("bounding_box") or det.get("bbox")
        if not bb:
            continue
        if isinstance(bb, dict):
            bbox = _normalise_bbox(bb, width, height)
        else:  # already a [xmin,ymin,xmax,ymax] list
            bbox = [round(float(v), 6) for v in bb]
        rec = {
            "class_id": int(class_id),
            "confidence": float(det.get("confidence", 1.0)),
            "bbox": bbox,
            "track_id": str(det.get("track_id", -1)),
        }
        if category:
            rec["category"] = category
        out.append(rec)
    return out


def _resolve_phase(pred_counts: dict, gt_path: str, n_frames: int) -> int:
    """Circular cross-correlation of per-frame detection counts -> rotation S."""
    gt = json.load(open(gt_path))
    gt_frames = gt.get("frames", gt)
    gt_counts = [0.0] * n_frames
    for k, v in gt_frames.items():
        try:
            idx = int(k)
        except ValueError:
            continue
        if 0 <= idx < n_frames:
            gt_counts[idx] = float(len(v))
    gt_mean = sum(gt_counts) / n_frames if n_frames else 0.0
    gt_c = [x - gt_mean for x in gt_counts]

    covered = sorted(pred_counts)
    if not covered:
        return 0
    pmean = sum(pred_counts.values()) / len(pred_counts)
    pc = {i: pred_counts[i] - pmean for i in covered}

    best_s, best_score = 0, float("-inf")
    for s in range(n_frames):
        score = sum(pc[i] * gt_c[(i + s) % n_frames] for i in covered)
        if score > best_score:
            best_score, best_s = score, s
    return best_s


def convert(input_folder, output_file, width, height, fps, video, model, usecase,
            class_names_str, gt_tracked=None, resolve_phase=False,
            phase_offset=0, n_frames=None, detections_source="tracking_stats"):
    category_to_id = _parse_class_names(class_names_str)
    id_to_name = {str(v): k for k, v in category_to_id.items()}

    files = sorted(
        [os.path.join(input_folder, f) for f in os.listdir(input_folder)
         if f.endswith(".json") and f != "meta.json"],
        key=_src_idx_from_name,
    )
    if not files:
        sys.exit(f"No frame-*.json files found in: {input_folder}")

    # Pull n_frames / fps from the collector's meta.json when present.
    meta_path = os.path.join(input_folder, "meta.json")
    meta = {}
    if os.path.exists(meta_path):
        meta = json.load(open(meta_path))
        n_frames = n_frames or meta.get("n_source_frames")
        if meta.get("source_fps"):
            fps = meta["source_fps"]

    by_idx: dict[int, list] = {}
    alerts_by_idx: dict[int, list] = {}
    counts_by_idx: dict[int, dict] = {}
    pred_counts: dict[int, int] = {}
    for fp in files:
        with open(fp) as fh:
            data = json.load(fh)
        src_idx = data.get("src_idx")
        if src_idx is None:
            src_idx = _src_idx_from_name(fp)
        src_idx = int(src_idx)
        dets = _convert_detections(_raw_detections(data, detections_source),
                                   category_to_id, width, height, src_idx)
        by_idx[src_idx] = dets
        pred_counts[src_idx] = len(dets)
        fa = _frame_alerts(data)
        if fa:
            alerts_by_idx[src_idx] = fa
        fc = _frame_counts(data)
        if fc:
            counts_by_idx[src_idx] = fc

    if n_frames is None:
        n_frames = max(by_idx) + 1

    # Phase alignment.
    shift = phase_offset % n_frames if n_frames else 0
    if resolve_phase:
        if not gt_tracked:
            sys.exit("--resolve_phase requires --gt_tracked")
        shift = _resolve_phase(pred_counts, gt_tracked, n_frames)
        print(f"[phase] resolved rotation S = {shift} frames (against {gt_tracked})")

    def rot(idx):
        return (idx + shift) % n_frames if n_frames else idx

    frames = {str(rot(idx)): dets for idx, dets in by_idx.items()}
    alerts = {str(rot(idx)): a for idx, a in alerts_by_idx.items()}
    counts = {str(rot(idx)): c for idx, c in counts_by_idx.items()}

    output = {
        "video": video, "width": width, "height": height, "fps": fps,
        "class_names": id_to_name, "model": model, "usecase": usecase,
        "n_frames": n_frames, "phase_offset": shift, "source": "vms",
        "detections_source": detections_source,
        "frames": frames,
    }
    if alerts:
        output["alerts"] = alerts
    if counts:
        output["counts"] = counts

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, "w") as fh:
        json.dump(output, fh, indent=2)
    n_alert_frames = len(alerts)
    total_dets = sum(len(v) for v in frames.values())
    print(f"Done. {len(frames)} source frames written -> {output_file}")
    print(f"      detections_source={detections_source}, total detections={total_dets}, "
          f"coverage {len(frames)}/{n_frames}, phase_offset={shift}, "
          f"alert frames={n_alert_frames}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--input_folder", required=True, help="Unzipped frame-*.json + meta.json folder.")
    p.add_argument("--output_file", required=True, help="Consolidated predictions JSON to write.")
    p.add_argument("--width", type=int, default=1920)
    p.add_argument("--height", type=int, default=1080)
    p.add_argument("--fps", type=float, default=30.0)
    p.add_argument("--video", default="")
    p.add_argument("--model", default="")
    p.add_argument("--usecase", default="loitering_detection")
    p.add_argument("--class_names", default="person=0,loitering_person=1")
    p.add_argument("--gt_tracked", default=None, help="gt JSON for phase resolution (Case B)")
    p.add_argument("--resolve_phase", action="store_true",
                   help="recover the constant rotation S vs gt_tracked (Case B)")
    p.add_argument("--phase_offset", type=int, default=0, help="apply a known rotation S")
    p.add_argument("--n_frames", type=int, default=None,
                   help="source frame count (else from meta.json or max index)")
    p.add_argument("--detections_source", choices=["tracking_stats", "model"],
                   default="tracking_stats",
                   help="which boxes to consolidate: post-processed "
                        "agg_summary tracking_stats.detections (default) or the raw "
                        "top-level model detections")
    args = p.parse_args()

    convert(
        input_folder=args.input_folder, output_file=args.output_file,
        width=args.width, height=args.height, fps=args.fps, video=args.video,
        model=args.model, usecase=args.usecase, class_names_str=args.class_names,
        gt_tracked=args.gt_tracked, resolve_phase=args.resolve_phase,
        phase_offset=args.phase_offset, n_frames=args.n_frames,
        detections_source=args.detections_source,
    )


if __name__ == "__main__":
    main()
