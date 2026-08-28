"""Compare ground-truth and model-prediction detection JSONs using the
``VolumeProcessor`` from ``analytics.processors.volume``.

Computes:
  * **Per-frame count accuracy** — for every frame, how close pred-count is to
    GT-count (MAE, RMSE, exact-match fraction).
  * **Per-minute unique count accuracy** — using ``VolumeProcessor.aggregate_1min``
    on both streams, compare ``tracking_stats.total_current_counts`` per
    1-minute window.
  * **Video unique count accuracy** — final cumulative unique IDs across the
    whole video (``tracking_stats.total_counts`` after the last aggregate).
  * **FP / FN per frame** — IoU-based greedy matching (independent of the
    volume processor).

Usage::

    python eval_with_volume.py path/to/ground_truth.json path/to/predictions.json

Both JSONs must follow the schema described in :mod:`detection_loader`.
Track IDs are required on each detection for unique counting to be meaningful.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Make sibling "analytics" package importable when this script is run directly.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from analytics.processors.volume import VolumeProcessor  # noqa: E402

from detection_loader import (  # noqa: E402
    iter_frames,
    load_detection_json,
    match_frame_fp_fn,
)


AGG_INTERVAL_SEC = 60.0


def _build_manifest_config(target_class: str) -> dict[str, Any]:
    """Build a minimal manifest dict for a VolumeProcessor doing counting only."""
    return {
        "entity_mapping": {target_class: target_class},
        # Confirm a track on its first sighting; mirrors GT-style direct counting.
        "min_consecutive_frames": 1,
        "volume": {
            "metrics": [
                {"key": "current_occupancy", "agg_type": "max", "category": "VOLUME"},
            ]
        },
        "alerts": {},
    }


def _unique_count(stats: dict[str, Any], key: str, category: str) -> int:
    """Sum ``count`` values in ``stats[key]`` for the given category."""
    entries = stats.get(key, []) or []
    return sum(int(e.get("count", 0)) for e in entries if e.get("category") == category)


def evaluate(
    gt_path: str | Path,
    pred_path: str | Path,
    *,
    target_class: str = "person",
    iou_threshold: float = 0.5,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Run the evaluation and return a results dict ready to print or serialise."""
    gt_json = load_detection_json(gt_path)
    pred_json = load_detection_json(pred_path)

    fps = float(gt_json.get("fps") or pred_json.get("fps") or 30.0)

    manifest_config = _build_manifest_config(target_class)
    proc_gt = VolumeProcessor(category="VOLUME", manifest_config=manifest_config)
    proc_pred = VolumeProcessor(category="VOLUME", manifest_config=manifest_config)

    gt_iter = iter_frames(gt_json, target_classes={target_class})
    pred_iter = iter_frames(
        pred_json,
        target_classes={target_class},
        confidence_threshold=confidence_threshold,
    )

    gt_frames: dict[int, list[dict[str, Any]]] = dict(gt_iter)
    pred_frames: dict[int, list[dict[str, Any]]] = dict(pred_iter)
    all_frame_ids = sorted(set(gt_frames) | set(pred_frames))

    per_frame_rows: list[dict[str, Any]] = []
    minute_rows: list[dict[str, Any]] = []
    last_agg_ts: float | None = None
    total_tp = total_fp = total_fn = 0

    for frame_id in all_frame_ids:
        frame_ts = frame_id / fps if fps > 0 else float(frame_id)

        gt_dets = gt_frames.get(frame_id, [])
        pred_dets = pred_frames.get(frame_id, [])

        out_gt = proc_gt.process_frame(gt_dets, frame_ts, str(frame_id))
        out_pred = proc_pred.process_frame(pred_dets, frame_ts, str(frame_id))

        gt_count = int(out_gt.business_analytics.get("current_occupancy", len(gt_dets)))
        pred_count = int(out_pred.business_analytics.get("current_occupancy", len(pred_dets)))

        tp, fp, fn = match_frame_fp_fn(gt_dets, pred_dets, iou_threshold=iou_threshold)
        total_tp += tp
        total_fp += fp
        total_fn += fn

        per_frame_rows.append(
            {
                "frame": frame_id,
                "gt_count": gt_count,
                "pred_count": pred_count,
                "count_abs_err": abs(pred_count - gt_count),
                "tp": tp,
                "fp": fp,
                "fn": fn,
            }
        )

        if last_agg_ts is None:
            last_agg_ts = frame_ts
        if frame_ts - last_agg_ts >= AGG_INTERVAL_SEC:
            agg_gt = proc_gt.aggregate_1min()
            agg_pred = proc_pred.aggregate_1min()
            minute_rows.append(
                _record_minute(
                    window_end_frame=frame_id,
                    target_class=target_class,
                    agg_gt=agg_gt,
                    agg_pred=agg_pred,
                )
            )
            last_agg_ts = frame_ts

    # Final (partial) window — always emit so the last minute is comparable too.
    agg_gt_final = proc_gt.aggregate_1min()
    agg_pred_final = proc_pred.aggregate_1min()
    minute_rows.append(
        _record_minute(
            window_end_frame=all_frame_ids[-1] if all_frame_ids else 0,
            target_class=target_class,
            agg_gt=agg_gt_final,
            agg_pred=agg_pred_final,
            partial=True,
        )
    )

    # Video totals (cumulative unique across the whole run).
    gt_video_unique = _unique_count(agg_gt_final.tracking_stats, "total_counts", target_class)
    pred_video_unique = _unique_count(agg_pred_final.tracking_stats, "total_counts", target_class)

    return _summarise(
        per_frame_rows=per_frame_rows,
        minute_rows=minute_rows,
        gt_video_unique=gt_video_unique,
        pred_video_unique=pred_video_unique,
        total_tp=total_tp,
        total_fp=total_fp,
        total_fn=total_fn,
    )


def _record_minute(
    *,
    window_end_frame: int,
    target_class: str,
    agg_gt,
    agg_pred,
    partial: bool = False,
) -> dict[str, Any]:
    """Pull the per-minute unique counts out of a pair of aggregate outputs."""
    gt_unique = _unique_count(agg_gt.tracking_stats, "total_current_counts", target_class)
    pred_unique = _unique_count(agg_pred.tracking_stats, "total_current_counts", target_class)
    return {
        "window_end_frame": window_end_frame,
        "partial": partial,
        "gt_unique": gt_unique,
        "pred_unique": pred_unique,
        "abs_err": abs(pred_unique - gt_unique),
    }


def _summarise(
    *,
    per_frame_rows: list[dict[str, Any]],
    minute_rows: list[dict[str, Any]],
    gt_video_unique: int,
    pred_video_unique: int,
    total_tp: int,
    total_fp: int,
    total_fn: int,
) -> dict[str, Any]:
    per_frame_acc = _avg_accuracy(
        [(r["gt_count"], r["pred_count"]) for r in per_frame_rows]
    )
    minute_acc = _avg_accuracy(
        [(r["gt_unique"], r["pred_unique"]) for r in minute_rows]
    )
    video_acc = _pair_accuracy(gt_video_unique, pred_video_unique)

    return {
        "per_frame_count_accuracy": per_frame_acc,
        "minute_unique_count_accuracy": minute_acc,
        "video_unique_count_accuracy": video_acc,
        "fp": total_fp,
        "fn": total_fn,
    }


def _pair_accuracy(gt: int, pred: int) -> float:
    """Single-pair accuracy: ``1 - abs_err / max(gt, 1)``, clamped to [0, 1]."""
    if gt == 0:
        return 1.0 if pred == 0 else 0.0
    return max(0.0, 1.0 - abs(pred - gt) / gt)


def _avg_accuracy(pairs: list[tuple[int, int]]) -> float:
    """Mean of ``_pair_accuracy`` over a list of ``(gt, pred)`` pairs."""
    if not pairs:
        return 0.0
    return sum(_pair_accuracy(g, p) for g, p in pairs) / len(pairs)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    parser.add_argument("gt_json", help="Ground-truth detection JSON path")
    parser.add_argument("pred_json", help="Model-predictions detection JSON path")
    parser.add_argument("--class", dest="target_class", default="person")
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--conf-threshold", type=float, default=None)
    parser.add_argument("--out", help="Optional path to write the report as JSON")
    args = parser.parse_args()

    report = evaluate(
        args.gt_json,
        args.pred_json,
        target_class=args.target_class,
        iou_threshold=args.iou,
        confidence_threshold=args.conf_threshold,
    )

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
