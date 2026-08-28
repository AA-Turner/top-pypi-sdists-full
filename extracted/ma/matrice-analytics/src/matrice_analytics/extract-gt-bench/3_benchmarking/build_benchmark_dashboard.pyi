"""Auto-generated stub for module: build_benchmark_dashboard."""
from typing import Any

# Constants
MAX_SERIES_POINTS: int

# Functions
def aggregate_all_classes(gt_path: Any, pred_path: Any) -> dict[str, Any]:
    """
    Single-pass multi-class aggregation for dashboard series + summaries.
    """
    ...
def build_dashboard_data(gt_path: Any, pred_path: Any, bench_path: Any | None) -> dict[str, Any]: ...
def load_or_build_summaries(gt_path: Any, pred_path: Any, bench_path: Any | None) -> dict[str, dict[str, Any]]:
    """
    Prefer freshly computed summaries; merge extended fields from bench.json when present.
    """
    ...
def main() -> None: ...
def parse_args() -> Any.Any: ...
def render_html(data: dict[str, Any]) -> str: ...
