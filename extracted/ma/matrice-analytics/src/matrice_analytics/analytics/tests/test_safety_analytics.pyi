"""Auto-generated stub for module: test_safety_analytics."""
from typing import Any, Dict, Tuple

# Constants
ALLOWED_GEAR_LABELS: Any
CAPPED_GEAR_CATEGORIES: Tuple[Any, ...]
DEDUP_IOU_MERGE_THRESHOLD: float
DEFAULT_BASE: Any
DEFAULT_MANIFEST: Any
DEFAULT_OUT_DIR: Any
DEFAULT_PEOPLE_MODEL: Any
DEFAULT_PPE_MODEL: Any
DEFAULT_VIDEO: Any
GEAR_COLORS_BGR: Dict[Any, Any]
PERSON_BOX_BGR: Tuple[Any, ...]
PPE_ROI_EXPAND_FACTOR: float
VIOLATION_LABELS: Any

# Functions
def main() -> None: ...
def run(video_path: Any, people_model_path: str, ppe_model_path: Any, manifest_path: Any, out_dir: Any) -> None: ...
