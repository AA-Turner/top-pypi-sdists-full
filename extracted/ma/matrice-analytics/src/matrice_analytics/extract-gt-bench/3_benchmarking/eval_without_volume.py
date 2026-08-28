"""Compare ground-truth and prediction detection JSONs **without** going
through the ``VolumeProcessor``.

Reproduces the same metrics as :mod:`eval_with_volume` using only standard
library + :mod:`detection_loader`. Useful as a sanity-check / cross-reference
for the processor-driven version, and as a zero-dependency fallback.

Metrics:
  * Per-frame count accuracy (MAE, RMSE, exact-match fraction).
  * Per-minute unique count accuracy — uniqueness over each 1-minute window of
    frames, counted directly from ``track_id``.
  * Video unique count — distinct ``track_id`` values across the entire video.
  * FP / FN via greedy IoU matching.

Usage::

    python eval_without_volume.py path/to/ground_truth.json path/to/predictions.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from detection_loader import (  # noqa: E402
    iter_frames,
    load_detection_json,
    match_frame_fp_fn,
)


AGG_INTERVAL_SEC = 60.0


def _frame_unique_ids(dets: list[dict[str, Any]]) -> set[Any]:
    """Return the set of non-None ``track_id`` values in this frame's detections."""
    return {d.get("track_id") for d in dets if d.get("track_id") is not None}


def evaluate(
    gt_path: str | Path,
    pred_path: str | Path,
    *,
    target_class: str = "person",
    iou_threshold: float = 0.5,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Run the standalone evaluation and return a results dict."""
    gt_json = load_detection_json(gt_path)
    pred_json = load_detection_json(pred_path)

    fps = float(gt_json.get("fps") or pred_json.get("fps") or 30.0)
    frames_per_window = max(1, int(round(AGG_INTERVAL_SEC * fps)))

    gt_frames = dict(iter_frames(gt_json, target_classes={target_class}))
    pred_frames = dict(
        iter_frames(
            pred_json,
            target_classes={target_class},
            confidence_threshold=confidence_threshold,
        )
    )
    all_frame_ids = sorted(set(gt_frames) | set(pred_frames))

    per_frame_rows: list[dict[str, Any]] = []
    minute_rows: list[dict[str, Any]] = []

    window_gt_ids: set[Any] = set()
    window_pred_ids: set[Any] = set()
    video_gt_ids: set[Any] = set()
    video_pred_ids: set[Any] = set()

    total_tp = total_fp = total_fn = 0
    window_start_frame: int | None = None

    for frame_id in all_frame_ids:
        gt_dets = gt_frames.get(frame_id, [])
        pred_dets = pred_frames.get(frame_id, [])

        gt_count = len(gt_dets)
        pred_count = len(pred_dets)

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

        gt_ids = _frame_unique_ids(gt_dets)
        pred_ids = _frame_unique_ids(pred_dets)
        window_gt_ids |= gt_ids
        window_pred_ids |= pred_ids
        video_gt_ids |= gt_ids
        video_pred_ids |= pred_ids

        if window_start_frame is None:
            window_start_frame = frame_id
        if frame_id - window_start_frame + 1 >= frames_per_window:
            minute_rows.append(
                {
                    "window_end_frame": frame_id,
                    "partial": False,
                    "gt_unique": len(window_gt_ids),
                    "pred_unique": len(window_pred_ids),
                    "abs_err": abs(len(window_pred_ids) - len(window_gt_ids)),
                }
            )
            window_gt_ids = set()
            window_pred_ids = set()
            window_start_frame = None

    # Flush partial window so the last seconds are still scored.
    if window_gt_ids or window_pred_ids:
        minute_rows.append(
            {
                "window_end_frame": all_frame_ids[-1] if all_frame_ids else 0,
                "partial": True,
                "gt_unique": len(window_gt_ids),
                "pred_unique": len(window_pred_ids),
                "abs_err": abs(len(window_pred_ids) - len(window_gt_ids)),
            }
        )

    return _summarise(
        per_frame_rows=per_frame_rows,
        minute_rows=minute_rows,
        gt_video_unique=len(video_gt_ids),
        pred_video_unique=len(video_pred_ids),
        total_tp=total_tp,
        total_fp=total_fp,
        total_fn=total_fn,
    )


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
