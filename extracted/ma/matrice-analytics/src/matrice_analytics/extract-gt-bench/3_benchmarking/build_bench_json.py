"""Build consolidated bench.json from GT + prediction JSONs (all vehicle classes).

Uses eval_without_volume.evaluate() per class so the three accuracy metrics match
the benchmarking harness exactly. Adds underlying unique-ID counts so 0.0 scores
are auditable in bench.json and the dashboard.

Usage::

    python build_bench_json.py
    python build_bench_json.py --gt ../apps/vehicle-counting/gt-tracked.json \\
        --pred ../apps/vehicle-counting/pred-tracked.json --out ../apps/vehicle-counting/bench.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
_APPS_VC = _HERE.parent / "apps" / "vehicle-counting"
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from build_benchmark_dashboard import (  # noqa: E402
    _class_names_ordered,
    _f1_score,
    aggregate_all_classes,
)
from detection_loader import load_detection_json  # noqa: E402
from eval_without_volume import evaluate  # noqa: E402


def build_bench_report(
    gt_path: Path,
    pred_path: Path,
    *,
    iou_threshold: float = 0.5,
    confidence_threshold: float | None = None,
) -> dict[str, Any]:
    """Return consolidated bench dict with canonical metrics + unique-count breakdown."""
    gt_json = load_detection_json(gt_path)
    class_names = _class_names_ordered(gt_json)
    if not class_names:
        raise ValueError("No class_names found in GT JSON")

    agg = aggregate_all_classes(
        gt_path,
        pred_path,
        class_names=class_names,
        iou_threshold=iou_threshold,
        confidence_threshold=confidence_threshold,
    )

    classes_out: dict[str, dict[str, Any]] = {}
    for cls in class_names:
        ev = evaluate(
            gt_path,
            pred_path,
            target_class=cls,
            iou_threshold=iou_threshold,
            confidence_threshold=confidence_threshold,
        )
        extra = agg["summaries"][cls]

        # Canonical harness metrics (from evaluate — must match aggregate)
        row: dict[str, Any] = {
            "per_frame_count_accuracy": float(ev["per_frame_count_accuracy"]),
            "minute_unique_count_accuracy": float(ev["minute_unique_count_accuracy"]),
            "video_unique_count_accuracy": float(ev["video_unique_count_accuracy"]),
            "fp": int(ev["fp"]),
            "fn": int(ev["fn"]),
            "tp": int(extra["tp"]),
            "precision": extra["precision"],
            "recall": extra["recall"],
            "f1": extra.get("f1", _f1_score(extra["precision"], extra["recall"])),
            "gt_total_detections": int(extra["gt_total_detections"]),
            "pred_total_detections": int(extra["pred_total_detections"]),
            "exact_match_fraction": float(extra["exact_match_fraction"]),
            "gt_video_unique": int(extra["gt_video_unique"]),
            "pred_video_unique": int(extra["pred_video_unique"]),
        }

        # Explicit breakdown behind video / minute unique accuracy
        row["video_unique"] = {
            "gt": row["gt_video_unique"],
            "pred": row["pred_video_unique"],
            "accuracy": row["video_unique_count_accuracy"],
        }

        series = agg["series"][cls]
        mg = series.get("minute_gt_unique") or []
        mp = series.get("minute_pred_unique") or []
        if mg and mp:
            row["minute_unique_windows"] = {
                "window_count": len(mg),
                "avg_gt_unique": sum(mg) / len(mg),
                "avg_pred_unique": sum(mp) / len(mp),
                "accuracy": row["minute_unique_count_accuracy"],
            }
        else:
            row["minute_unique_windows"] = {
                "window_count": 0,
                "avg_gt_unique": 0.0,
                "avg_pred_unique": 0.0,
                "accuracy": row["minute_unique_count_accuracy"],
            }

        classes_out[cls] = row

    return {
        "evaluator": "eval_without_volume",
        "gt_json": str(gt_path.as_posix()),
        "pred_json": str(pred_path.as_posix()),
        "iou_threshold": iou_threshold,
        "confidence_threshold": confidence_threshold,
        "fps": agg["fps"],
        "frame_count": agg["frame_count"],
        "classes": classes_out,
    }


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    p.add_argument("--gt", type=Path, default=_APPS_VC / "gt-tracked.json")
    p.add_argument("--pred", type=Path, default=_APPS_VC / "pred-tracked.json")
    p.add_argument("--out", type=Path, default=_APPS_VC / "bench.json")
    p.add_argument("--iou", type=float, default=0.5)
    p.add_argument("--conf-threshold", type=float, default=None)
    return p.parse_args()


def main() -> None:
    args = parse_args()
    if not args.gt.is_file():
        sys.exit(f"GT JSON not found: {args.gt}")
    if not args.pred.is_file():
        sys.exit(f"Pred JSON not found: {args.pred}")

    report = build_bench_report(
        args.gt,
        args.pred,
        iou_threshold=args.iou,
        confidence_threshold=args.conf_threshold,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Wrote {args.out.resolve()} ({len(report['classes'])} classes)")


if __name__ == "__main__":
    main()
