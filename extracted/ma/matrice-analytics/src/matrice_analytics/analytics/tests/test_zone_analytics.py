from __future__ import annotations
import importlib.util
import json
import os
import pprint
import sys
import types
from pathlib import Path
from typing import Any

import cv2
from ultralytics import YOLO
import numpy as np

# --- Import bootstrap (analytics + footfall only) ---
# Avoid ``matrice_analytics/__init__.py`` (pulls all of post_processing) and
# ``usecases/__init__.py`` (pulls color/clip and optional subprocess deps).
_ROOT = Path("C:\\Users\\aswan_3sr40l5\\Matrice\\codespace\\repos\\py_analytics") # add path to the root of the repository
_SRC = _ROOT / "src"
_PKG = _SRC / "matrice_analytics"
sys.path.insert(0, str(_SRC))


def _register_pkg(name: str, path: Path) -> None:
    m = types.ModuleType(name)
    m.__path__ = [str(path)]
    sys.modules[name] = m


_register_pkg("matrice_analytics", _PKG)
_register_pkg("matrice_analytics.analytics", _PKG / "analytics")
_register_pkg("matrice_analytics.post_processing", _PKG / "post_processing")
_register_pkg("matrice_analytics.post_processing.usecases", _PKG / "post_processing" / "usecases")

from matrice_analytics.analytics.engine import AnalyticsEngine  # noqa: E402


_spec_bt = importlib.util.spec_from_file_location(
    "matrice_analytics.post_processing.usecases.footfall",
    _PKG / "post_processing" / "usecases" / "footfall.py",
)
_footfall = importlib.util.module_from_spec(_spec_bt)
assert _spec_bt.loader is not None
sys.modules["matrice_analytics.post_processing.usecases.footfall"] = _footfall
_spec_bt.loader.exec_module(_footfall)
ByteTrackWrapper = _footfall.ByteTrackWrapper


# ---------------------------------------------------------------------------
# Zone definitions (pixel coordinates on 1280x720)
# ---------------------------------------------------------------------------

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

ZONE_POLYGONS_PX: dict[str, list[list[int]]] = {
    "A": [[641, 402], [637, 692], [174, 677], [349, 393]],
    "B": [[639, 684], [1098, 677], [1002, 387], [648, 402]],
}


def _normalize_zones(
    zones_px: dict[str, list[list[int]]],
    width: int,
    height: int,
) -> dict[str, list[list[float]]]:
    """Convert pixel-coordinate zone polygons to normalized 0-1 coordinates."""
    return {
        name: [[pt[0] / width, pt[1] / height] for pt in pts]
        for name, pts in zones_px.items()
    }


# COCO class index to category name for vehicle_type_monitoring
INDEX_TO_CATEGORY: dict[int, str] = {
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}

# Zone overlay colours
ZONE_COLORS: dict[str, tuple[int, int, int]] = {
    "A": (0, 200, 255),   # orange
    "B": (255, 200, 0),   # cyan-blue
}
DEFAULT_ZONE_COLOR = (0, 255, 0)


class ZoneAnalyticsTestProcessor:
    """End-to-end test for per-zone volume analytics.

    Runs YOLO + ByteTrack on a video, feeds detections into the
    AnalyticsEngine with zone polygons configured, draws per-zone
    live counts on the video, and saves aggregation results.
    """

    def __init__(
        self,
        model_path: str,
        video_path: str,
        *,
        max_frames: int | None = None,
        loop_count: int = 1,
        json_dir: str = "jsons_zone",
        output_video_path: str = "output_zone.mp4",
        confidence_threshold: float = 0.45,
    ) -> None:
        self.model_path = model_path
        self.video_path = video_path
        self.max_frames = max_frames
        self.loop_count = max(1, loop_count)
        self.json_dir = json_dir
        self.output_video_path = output_video_path
        self.confidence_threshold = confidence_threshold

        self.model = YOLO(self.model_path)
        self.tracker = ByteTrackWrapper(
            track_high_thresh=0.4,
            track_low_thresh=0.1,
            new_track_thresh=0.4,
            track_buffer=60,
            match_thresh=0.8,
            frame_rate=30,
        )

        # Build stream_info with normalized zone polygons
        zones_normalized = _normalize_zones(ZONE_POLYGONS_PX, VIDEO_WIDTH, VIDEO_HEIGHT)
        stream_info: dict[str, Any] = {
            "camera_id": "cam_highway",
            "app_deployment_id": "zone_test_001",
            "resolution": [VIDEO_WIDTH, VIDEO_HEIGHT],
            "zone_config": {
                "zones": zones_normalized,
            },
        }

        self.engine = AnalyticsEngine(
            manifest_path_or_name="vehicle_type_monitoring_new",
            stream_info=stream_info,
        )

        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(os.path.join(self.json_dir, "agg"), exist_ok=True)

    # ------------------------------------------------------------------
    # Inference + detection building
    # ------------------------------------------------------------------

    def _run_inference(self, frame):
        results = self.model.predict(
            frame, conf=self.confidence_threshold, iou=0.7, verbose=False,
        )
        return results[0]

    def _build_raw_detections(self, result) -> list[dict]:
        detections = []
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            return detections

        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])
            category = INDEX_TO_CATEGORY.get(cls_id)
            if category is None:
                continue

            conf = float(boxes.conf[i])
            x1, y1, x2, y2 = boxes.xyxy[i].tolist()
            detections.append({
                "category": category,
                "category_id": cls_id,
                "confidence": conf,
                "bounding_box": {"xmin": x1, "ymin": y1, "xmax": x2, "ymax": y2},
            })
        return detections

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_zones(self, frame) -> None:
        """Draw semi-transparent zone polygons with labels."""
        overlay = frame.copy()
        for name, pts in ZONE_POLYGONS_PX.items():
            color = ZONE_COLORS.get(name, DEFAULT_ZONE_COLOR)
            poly = np.array(pts, dtype=np.int32)
            cv2.fillPoly(overlay, [poly], color)
            cv2.polylines(frame, [poly], True, color, 2)

            centroid = poly.mean(axis=0).astype(int)
            cv2.putText(
                frame, f"Zone {name}", tuple(centroid),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA,
            )
        cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)

    def _draw_bboxes_from_result(self, frame, frame_result: dict) -> None:
        """Draw bounding boxes only for detections returned by the engine (zone-filtered)."""
        agg_summary = frame_result.get("result", {}).get("value", {}).get("agg_summary", {})

        for zone_name, zone_data in agg_summary.items():
            color = ZONE_COLORS.get(zone_name, DEFAULT_ZONE_COLOR)
            detections = zone_data.get("tracking_stats", {}).get("detections", [])

            for det in detections:
                bb = det.get("bounding_box", {})
                x1, y1 = int(bb.get("xmin", 0)), int(bb.get("ymin", 0))
                x2, y2 = int(bb.get("xmax", 0)), int(bb.get("ymax", 0))
                label = f"{det.get('category', '')} [{zone_name}]"

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame, label, (x1, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA,
                )

    def _draw_zone_counts(self, frame, frame_result: dict) -> None:
        """Draw per-zone live counts from frame result agg_summary."""
        agg_summary = frame_result.get("result", {}).get("value", {}).get("agg_summary", {})

        y_offset = 30
        for zone_name, zone_data in agg_summary.items():
            color = ZONE_COLORS.get(zone_name, DEFAULT_ZONE_COLOR)
            business = zone_data.get("business_analytics", {})
            tracking = zone_data.get("tracking_stats", {})

            # Current detection count from detections list length
            det_count = len(tracking.get("detections", []))

            # Business analytics values
            occupancy = business.get("current_occupancy", det_count)

            text = f"Zone {zone_name}: {int(occupancy)} objects"
            cv2.putText(
                frame, text, (10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2, cv2.LINE_AA,
            )
            y_offset += 35

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize(obj):
        def _to_serializable(o):
            if hasattr(o, "model_dump"):
                return o.model_dump()
            if hasattr(o, "__dict__"):
                return o.__dict__
            return str(o)
        return json.loads(json.dumps(obj, default=_to_serializable))

    # ------------------------------------------------------------------
    # Main processing loop
    # ------------------------------------------------------------------

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {self.video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        video_writer = cv2.VideoWriter(self.output_video_path, fourcc, fps, (width, height))

        print(f"Video: {self.video_path} ({width}x{height} @ {fps:.1f} fps)")
        print(f"Model: {self.model_path}")
        print(f"Manifest: vehicle_type_monitoring")
        print(f"Zones active: {self.engine.zones_active}")
        print(f"Zone processors: {list(self.engine.zone_processors.keys())}")
        print(f"Output video: {self.output_video_path}")
        print(f"JSON dir: {self.json_dir}")
        print(f"Loop count: {self.loop_count}")
        print("-" * 60)

        frame_idx = 0
        done = False
        aggregated_results: list[dict] = []

        for loop_idx in range(self.loop_count):
            if done:
                break

            if loop_idx > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                print(f"\n--- Loop {loop_idx + 1}/{self.loop_count} ---")

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Inference + tracking
                raw_result = self._run_inference(frame)
                raw_detections = self._build_raw_detections(raw_result)
                detections = self.tracker.update(raw_detections)

                # Analytics engine
                frame_ts = frame_idx / fps if fps > 0 else float(frame_idx)
                frame_result = self.engine.process_frame(
                    detections=detections,
                    frame_ts=frame_ts,
                    frame_id=f"frame_{frame_idx:04d}",
                )

                # Aggregation check
                agg_result = None
                if self.engine.should_aggregate(frame_ts):
                    agg_result = self.engine.aggregate()
                    agg_serialized = self._serialize(agg_result)
                    aggregated_results.append(agg_serialized)

                    agg_path = os.path.join(self.json_dir, "agg", f"agg_{frame_idx:04d}.json")
                    with open(agg_path, "w") as f:
                        json.dump(agg_serialized, f, indent=2)
                    print(f"  ** Aggregation at frame {frame_idx} — saved: {agg_path}")

                # Draw on frame
                annotated = frame.copy()
                self._draw_zones(annotated)
                self._draw_bboxes_from_result(annotated, frame_result)
                self._draw_zone_counts(annotated, frame_result)
                video_writer.write(annotated)

                # Save per-frame JSON
                json_path = os.path.join(self.json_dir, f"frame_{frame_idx:04d}.json")
                with open(json_path, "w") as f:
                    json.dump(self._serialize(frame_result), f, indent=2)

                # Print zone summary
                agg_summary = frame_result.get("result", {}).get("value", {}).get("agg_summary", {})
                zone_counts = {
                    zn: len(zd.get("tracking_stats", {}).get("detections", []))
                    for zn, zd in agg_summary.items()
                }
                print(
                    f"[Loop {loop_idx + 1}/{self.loop_count}] Frame {frame_idx:4d} | "
                    f"detections: {len(detections):3d} | zones: {zone_counts}"
                )

                frame_idx += 1
                if self.max_frames and frame_idx >= self.max_frames:
                    print(f"Max frame limit ({self.max_frames}) reached.")
                    done = True
                    break

        # Final aggregation
        final_agg = self.engine.aggregate()
        final_serialized = self._serialize(final_agg)
        aggregated_results.append(final_serialized)

        final_agg_path = os.path.join(self.json_dir, "agg", "agg_final.json")
        with open(final_agg_path, "w") as f:
            json.dump(final_serialized, f, indent=2)

        # Save all aggregated results in one file
        all_agg_path = os.path.join(self.json_dir, "all_aggregated_results.json")
        with open(all_agg_path, "w") as f:
            json.dump(aggregated_results, f, indent=2)

        print(f"\nFinal aggregation saved: {final_agg_path}")
        print(f"All aggregated results saved: {all_agg_path}")
        print("\nFinal aggregation:")
        pprint.pprint(final_serialized)

        cap.release()
        video_writer.release()
        print(f"\nOutput video saved: {self.output_video_path}")
        print(f"Processing complete. {frame_idx} frames processed.")


if __name__ == "__main__":
    processor = ZoneAnalyticsTestProcessor(
        model_path=r"C:\Users\aswan_3sr40l5\Matrice\models\yolov8m.pt",
        video_path=r"C:\Users\aswan_3sr40l5\Matrice\datasets\test_videos\highway.mp4",
        max_frames=None,
        loop_count=10,
        json_dir="jsons_zone_vehicle",
        output_video_path="output_zone_vehicle.mp4",
        confidence_threshold=0.1,
    )
    processor.process_video()
