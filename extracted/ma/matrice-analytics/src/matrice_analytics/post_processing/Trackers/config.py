"""Configuration for Matrice tracker factory and adapters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional

SUPPORTED_TRACKING_METHODS = frozenset(
    {
        "advanced",
        "kalman",  # alias for advanced
        "sort",
        "bytetrack",
        "oc_sort",
        "deep_oc_sort",
        "deepsort",
        "botsort",
        "none",
    }
)


@dataclass
class MatriceTrackerConfig:
    """Unified config passed from use cases into tracker adapters."""

    # AdvancedTracker thresholds
    track_high_thresh: float = 0.4
    track_low_thresh: float = 0.05
    new_track_thresh: float = 0.3
    match_thresh: float = 0.8
    track_buffer: int = 600
    max_time_lost: int = 1200
    frame_rate: int = 25

    # SORT
    sort_iou_threshold: float = 0.25
    sort_max_age: int = 30
    sort_min_hits: int = 2

    # ByteTrack (YOLOX wrapper defaults)
    bytetrack_fps: float = 30.0
    bytetrack_track_thresh: float = 0.25
    bytetrack_match_thresh: float = 0.80
    bytetrack_track_buffer: int = 30

    # OC-SORT
    oc_sort_det_thresh: float = 0.3
    oc_sort_max_age: int = 30
    oc_sort_min_hits: int = 3
    oc_sort_iou_threshold: float = 0.3
    oc_sort_delta_t: int = 3
    oc_sort_asso_func: str = "iou"
    oc_sort_inertia: float = 0.2
    oc_sort_use_byte: bool = True

    # DeepSORT
    deepsort_max_iou_distance: float = 0.7
    deepsort_max_age: int = 30
    deepsort_n_init: int = 3
    deepsort_matching_threshold: float = 0.2
    deepsort_budget: int = 100
    # ``deep-sort-realtime`` backend (pip install deep-sort-realtime)
    deepsort_embedder: Optional[str] = None  # None = IoU-only via dummy embeds; "mobilenet" = auto-download ReID
    deepsort_embedder_half: bool = True
    deepsort_embedder_gpu: bool = False
    # ``None`` / ``"auto"`` prefers ``deep-sort-realtime`` when installed, else vendor clone
    deepsort_backend: Optional[str] = None

    # DeepOCSORT. The ``boxmot.DeepOcSort`` ReID backend was removed (AGPL-3.0
    # licensing -- see Trackers/deep_oc_sort/adapter.py's module docstring); this
    # adapter is now always the in-repo pure-python ``advanced`` motion tracker.
    # The ReID/embedding/appearance fields below are accepted-and-unused (kept so
    # an existing deployment config setting them doesn't hard-fail).
    deep_oc_sort_det_thresh: float = 0.3
    deep_oc_sort_max_age: int = 30
    deep_oc_sort_min_hits: int = 3
    deep_oc_sort_iou_threshold: float = 0.3
    deep_oc_sort_delta_t: int = 3
    deep_oc_sort_asso_func: str = "iou"
    deep_oc_sort_inertia: float = 0.2
    deep_oc_sort_w_association_emb: float = 0.75  # unused (boxmot ReID removed)
    deep_oc_sort_alpha_fixed_emb: float = 0.95  # unused (boxmot ReID removed)
    deep_oc_sort_aw_param: float = 0.5  # unused (boxmot ReID removed)
    deep_oc_sort_embedding_off: bool = False  # unused (boxmot ReID removed)
    deep_oc_sort_cmc_off: bool = False  # unused (boxmot ReID removed)
    deep_oc_sort_reid_weights: Optional[str] = None  # unused (boxmot ReID removed)
    deep_oc_sort_device: str = "cpu"  # unused (boxmot ReID removed)
    deep_oc_sort_half: bool = False  # unused (boxmot ReID removed)
    # ``"boxmot"`` is still accepted (never a hard failure for an existing
    # deployment config) but always resolves to the fallback -- see adapter.py.
    deep_oc_sort_backend: Optional[str] = None

    # BoT-SORT
    botsort_with_reid: bool = False
    botsort_track_high_thresh: float = 0.6
    botsort_track_low_thresh: float = 0.1
    botsort_new_track_thresh: float = 0.7
    botsort_track_buffer: int = 30
    botsort_match_thresh: float = 0.8
    botsort_proximity_thresh: float = 0.5
    botsort_appearance_thresh: float = 0.25
    botsort_cmc_method: str = "none"

    confidence_threshold: Optional[float] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_config(cls, config: Any, stream_info: Optional[Dict[str, Any]] = None) -> MatriceTrackerConfig:
        """Build tracker config from a use-case config object."""
        _ = stream_info
        conf = getattr(config, "confidence_threshold", None)
        fps = 30.0
        try:
            if stream_info:
                fps_val = stream_info.get("input_settings", {}).get("original_fps")
                if fps_val and float(fps_val) > 1e-6:
                    fps = float(fps_val)
        except Exception:
            fps = 30.0

        return cls(
            track_high_thresh=float(getattr(config, "track_high_thresh", 0.4)),
            track_low_thresh=float(getattr(config, "track_low_thresh", 0.05)),
            new_track_thresh=float(getattr(config, "new_track_thresh", 0.3)),
            match_thresh=float(getattr(config, "match_thresh", 0.8)),
            track_buffer=int(getattr(config, "track_buffer", 600)),
            max_time_lost=int(getattr(config, "max_time_lost", 1200)),
            frame_rate=int(getattr(config, "frame_rate", 25)),
            sort_iou_threshold=float(getattr(config, "tracking_iou_threshold", 0.25)),
            sort_max_age=int(getattr(config, "tracking_max_age", 30)),
            sort_min_hits=int(getattr(config, "tracking_min_hits", 2)),
            bytetrack_fps=fps,
            bytetrack_track_thresh=float(getattr(config, "bytetrack_track_thresh", 0.25)),
            bytetrack_match_thresh=float(getattr(config, "bytetrack_match_thresh", 0.80)),
            bytetrack_track_buffer=int(getattr(config, "tracking_max_age", 30)),
            confidence_threshold=float(conf) if conf is not None else None,
            # DeepOCSORT passthrough (use-case config may override any of these).
            deep_oc_sort_det_thresh=float(getattr(config, "deep_oc_sort_det_thresh", 0.3)),
            deep_oc_sort_max_age=int(getattr(config, "deep_oc_sort_max_age", 30)),
            deep_oc_sort_min_hits=int(getattr(config, "deep_oc_sort_min_hits", 3)),
            deep_oc_sort_iou_threshold=float(getattr(config, "deep_oc_sort_iou_threshold", 0.3)),
            deep_oc_sort_delta_t=int(getattr(config, "deep_oc_sort_delta_t", 3)),
            deep_oc_sort_asso_func=str(getattr(config, "deep_oc_sort_asso_func", "iou")),
            deep_oc_sort_inertia=float(getattr(config, "deep_oc_sort_inertia", 0.2)),
            deep_oc_sort_embedding_off=bool(getattr(config, "deep_oc_sort_embedding_off", False)),
            deep_oc_sort_cmc_off=bool(getattr(config, "deep_oc_sort_cmc_off", False)),
            deep_oc_sort_reid_weights=getattr(config, "deep_oc_sort_reid_weights", None),
            deep_oc_sort_device=str(getattr(config, "deep_oc_sort_device", "cpu")),
            deep_oc_sort_half=bool(getattr(config, "deep_oc_sort_half", False)),
            deep_oc_sort_backend=getattr(config, "deep_oc_sort_backend", None),
        )
