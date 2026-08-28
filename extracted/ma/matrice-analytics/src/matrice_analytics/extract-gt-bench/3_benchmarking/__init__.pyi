"""Stub file for extract-gt-bench.3_benchmarking directory."""
from typing import Any, List, Optional

# Constants
MAX_SERIES_POINTS: int = ...  # From build_benchmark_dashboard
AGG_INTERVAL_SEC: float = ...  # From eval_with_volume
AGG_INTERVAL_SEC: float = ...  # From eval_without_volume

# Functions
# From build_bench_json
def build_bench_report(gt_path: Any, pred_path: Any) -> dict[str, Any]:
    """
    Return consolidated bench dict with canonical metrics + unique-count breakdown.
    """
    ...

# From build_bench_json
def main() -> None: ...

# From build_bench_json
def parse_args() -> Any.Any: ...

# From build_benchmark_dashboard
def aggregate_all_classes(gt_path: Any, pred_path: Any) -> dict[str, Any]:
    """
    Single-pass multi-class aggregation for dashboard series + summaries.
    """
    ...

# From build_benchmark_dashboard
def build_dashboard_data(gt_path: Any, pred_path: Any, bench_path: Any | None) -> dict[str, Any]: ...

# From build_benchmark_dashboard
def load_or_build_summaries(gt_path: Any, pred_path: Any, bench_path: Any | None) -> dict[str, dict[str, Any]]:
    """
    Prefer freshly computed summaries; merge extended fields from bench.json when present.
    """
    ...

# From build_benchmark_dashboard
def main() -> None: ...

# From build_benchmark_dashboard
def parse_args() -> Any.Any: ...

# From build_benchmark_dashboard
def render_html(data: dict[str, Any]) -> str: ...

# From detection_loader
def iou_xyxy(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> float:
    """
    Standard IoU of two ``[x1, y1, x2, y2]`` boxes.
    """
    ...

# From detection_loader
def iter_frames(detection_json: dict[str, Any]) -> Any:
    """
    Yield ``(frame_idx, processor_detections)`` in numeric frame order.
    """
    ...

# From detection_loader
def load_detection_json(path: str | Any) -> dict[str, Any]:
    """
    Load a detection JSON file and return the parsed dict unchanged.
    """
    ...

# From detection_loader
def match_frame_fp_fn(gt_dets: list[dict[str, Any]], pred_dets: list[dict[str, Any]], iou_threshold: float = 0.5) -> tuple[int, int, int]:
    """
    Greedy IoU matching for one frame.
    
        Returns:
            ``(true_positives, false_positives, false_negatives)``.
    """
    ...

# From detection_loader
def to_processor_detections(raw_frame_dets: list[dict[str, Any]], class_names: dict[str, str], width: int, height: int) -> list[dict[str, Any]]:
    """
    Convert one frame's raw detections to the processor input shape.
    
        Args:
            raw_frame_dets: List of detections from ``frames[<idx>]``.
            class_names: Mapping ``{"0": "person", ...}`` from the JSON header.
            width: Frame width in pixels (for denormalizing bbox).
            height: Frame height in pixels.
            target_classes: Optional whitelist of class names to keep (e.g. {"person"}).
                ``None`` keeps everything.
            confidence_threshold: Optional minimum confidence. ``None`` keeps everything.
    
        Returns:
            List of processor-shaped detection dicts.
    """
    ...

# From eval_with_volume
def evaluate(gt_path: str | Any, pred_path: str | Any) -> dict[str, Any]:
    """
    Run the evaluation and return a results dict ready to print or serialise.
    """
    ...

# From eval_with_volume
def main() -> None: ...

# From eval_without_volume
def evaluate(gt_path: str | Any, pred_path: str | Any) -> dict[str, Any]:
    """
    Run the standalone evaluation and return a results dict.
    """
    ...

# From eval_without_volume
def main() -> None: ...

from . import build_bench_json, build_benchmark_dashboard, detection_loader, eval_with_volume, eval_without_volume