"""Stub file for extract-gt-bench.2_gt-annotations directory."""
from typing import Any, Dict

# Constants
VERIFY_COLORS: Dict[Any, Any] = ...  # From 1-5_align_phase
state: Dict[Any, Any] = ...  # From 1-5_align_phase
VERIFY_COLORS: Dict[Any, Any] = ...  # From 2_verify
state: Dict[Any, Any] = ...  # From 2_verify
DEFAULT_MODEL: Any = ...  # From loitering_common
DEFAULT_YOLO_CONF: float = ...  # From loitering_common
DEFAULT_YOLO_DEVICE: str = ...  # From loitering_common
DEFAULT_YOLO_IMGSZ: int = ...  # From loitering_common
DEFAULT_YOLO_IOU: float = ...  # From loitering_common
LOITERING_CLASS_ID: Any = ...  # From loitering_common
LOITERING_PERSON_CLASS_ID: int = ...  # From loitering_common
PERSON_CLASS_ID: int = ...  # From loitering_common
REPO_ROOT: Any = ...  # From loitering_common
YOLO_PERSON_CLASS_ID: int = ...  # From loitering_common

# Functions
# From 1-5_align_phase
def clamp_di(i: Any) -> Any: ...

# From 1-5_align_phase
def class_label(cid: Any) -> Any: ...

# From 1-5_align_phase
def color_for(cid: Any) -> Any: ...

# From 1-5_align_phase
def draw_box(img: Any, det: Any, w: Any, h: Any) -> Any: ...

# From 1-5_align_phase
def draw_overlay(img: Any) -> Any: ...

# From 1-5_align_phase
def get_dets(src_idx: Any) -> Any: ...

# From 1-5_align_phase
def main() -> Any: ...

# From 1-5_align_phase
def move_detection(delta: Any) -> Any: ...

# From 1-5_align_phase
def move_video(delta: Any) -> Any: ...

# From 1-5_align_phase
def read_video_frame(idx: Any) -> Any: ...

# From 1-5_align_phase
def render() -> Any: ...

# From 1-5_align_phase
def save_aligned(out_path: Any) -> Any: ...

# From 1-5_align_phase
def src_idx_now() -> Any: ...

# From 1-5_align_phase
def toggle_set() -> Any: ...

# From 1-5_align_phase
def wrap_vf(v: Any) -> Any: ...

# From 1_consolidate
def convert(input_folder: Any, output_file: Any, width: Any, height: Any, fps: Any, video: Any, model: Any, usecase: Any, class_names_str: Any, gt_tracked: Any = None, resolve_phase: Any = False, phase_offset: Any = 0, n_frames: Any = None, detections_source: Any = 'tracking_stats') -> Any: ...

# From 1_consolidate
def main() -> Any: ...

# From 2_verify
def adjust_phase(delta: Any) -> Any:
    """
    Nudge the constant Case-B rotation S used to seek the video (wraps mod N).
    """
    ...

# From 2_verify
def class_label(cid: Any) -> Any: ...

# From 2_verify
def color_for(cid: Any) -> Any: ...

# From 2_verify
def draw_box(img: Any, det: Any, w: Any, h: Any) -> Any: ...

# From 2_verify
def draw_overlay(img: Any) -> Any: ...

# From 2_verify
def ensure_opencv_gui() -> Any: ...

# From 2_verify
def export_annotated(video_path: Any, out_path: Any) -> Any:
    """
    Render saved boxes onto ONLY the sampled frames, written in sample order.
    """
    ...

# From 2_verify
def find_box_at(src_idx: Any, x: Any, y: Any) -> Any: ...

# From 2_verify
def get_dets(src_idx: Any) -> Any: ...

# From 2_verify
def main() -> Any: ...

# From 2_verify
def on_mouse(event: Any, x: Any, y: Any, flags: Any, _userdata: Any) -> Any: ...

# From 2_verify
def read_video_frame(video_frame_idx: Any) -> Any: ...

# From 2_verify
def render_frame() -> Any: ...

# From 2_verify
def save_json() -> Any: ...

# From 2_verify
def src_idx_now() -> Any: ...

# From 2_verify
def video_frame_now() -> Any: ...

# From 3_track
def assign_track_ids(data: Any, frame_rate: Any, track_thresh: Any, match_thresh: Any, lost_buffer: Any) -> Any: ...

# From 3_track
def color_for(tid: Any, class_id: Any = 0) -> Any: ...

# From 3_track
def main() -> Any: ...

# From 3_track
def parse_args() -> Any: ...

# From 3_track
def render(video_path: Any, out_path: Any, data: Any, phase_offset: Any) -> Any: ...

# From loitering_common
def add_analytics_src_to_path() -> Any: ...

# From loitering_common
def clamp_class_id(class_id: int) -> int: ...

# From loitering_common
def color_for_class(class_id: int) -> tuple[int, int, int]:
    """
    BGR colors aligned with loitering_detection_test.py drawing.
    """
    ...

# From loitering_common
def ensure_loitering_class_names(class_names: Dict[str, str] | None) -> Dict[str, str]:
    """
    Return a copy of class_names restricted to person + loitering_person.
    """
    ...

# From loitering_common
def json_det_to_matrice(det: Dict[str, Any], width: int, height: int) -> Dict[str, Any]: ...

# From loitering_common
def matrice_det_to_json(det: Dict[str, Any], width: int, height: int) -> Dict[str, Any]: ...

from . import 1-5_align_phase, 1_consolidate, 2_verify, 3_track, loitering_common