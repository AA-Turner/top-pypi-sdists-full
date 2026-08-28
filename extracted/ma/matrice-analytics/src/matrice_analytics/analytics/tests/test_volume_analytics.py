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



# YOLO COCO class-id → analytics entity name
# people_counting.yaml maps detection_class "person" with role "tracked_entity"
# INDEX_TO_CATEGORY = {0: "person"}


# COCO class index to category name mapping (for YOLO and analytics purposes)
# COCO index-to-category mapping by use case.
# For 'vehicle_type_monitoring': bicycle, car, motorcycle, bus, truck only.
# For 'people_counting' and 'footfall': person only.

INDEX_TO_CATEGORY_MAP = {
    "vehicle_type_monitoring_new": {
        1: "bicycle",
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck",
    },
    "people_counting_new": {0: "person"},
    "footfall": {0: "person"},
}

# StreamInfo defaults for footfall tests: geometry that used to live under
# ``volume.zone_config`` in legacy footfall.yaml (resolution + normalized lines).
# Counting method / in_direction / use_foot_center now come from manifest
# ``volume.counter``; keep this aligned with engine StreamInfo + manifest split.
FOOTFALL_DEFAULT_STREAM_INFO: dict[str, Any] = {
    "camera_id": "cam1",
    "app_deployment_id": "test_deployment_001",
    # Legacy zone_config.resolution — frame size in pixels (878×478).
    "resolution": [878, 478],
    "zone_config": {
        "lines": {
            # Normalized 0–1; pixel originals on 878×478:
            #   Line A: [[100, 292], [628, 340]]
            #   Line B: [[94, 339], [642, 389]]
            "Line A": [[0.1139, 0.6109], [0.7153, 0.7113]],
            "Line B": [[0.1071, 0.7092], [0.7312, 0.8138]],
        },
    },
}


def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """
    Returns the index-to-category mapping according to the analytics manifest.
    Args:
        manifest_name: The YAML manifest name or usecase (e.g., "vehicle_type_monitoring", "people_counting", "footfall").
    """
    key = manifest_name.lower()
    if key in INDEX_TO_CATEGORY_MAP:
        return INDEX_TO_CATEGORY_MAP[key]
    # Default: fallback to person-only
    return {0: "person"}


class AnalyticsEngineTestProcessor:
    """End-to-end test harness for the new AnalyticsEngine.

    Runs YOLO inference + ByteTrackWrapper (same config as footfall use case)
    on a video, converts tracked detections into the format expected by the
    engine, and stores per-frame + aggregation results as JSON files.
    """

    def __init__(
        self,
        manifest_name: str,
        model_path: str,
        video_path: str,
        *,
        max_frames: int | None = None,
        loop_count: int = 1,
        json_dir: str = "jsons",
        draw_bboxes: bool = False,
        draw_lines: bool = False,
        output_video_path: str = "output.mp4",
        confidence_threshold: float = 0.45,
        stream_info: dict | None = None,
    ) -> None:
        """Initialize the test processor.

        Args:
            manifest_name: Name of the YAML manifest under analytics/config/
                (e.g. "people_counting").
            model_path: Path to the YOLO model weights (.pt).
            video_path: Path to the input video file.
            max_frames: Stop after this many frames (None = all, across all loops).
            loop_count: Number of times to loop the video (default 1 = no loop).
            json_dir: Directory for per-frame JSON outputs.
            draw_bboxes: If True, annotate frames and write an output video.
            draw_lines: If True, draw zone lines/zones from the engine's
                ``stream_info.zone_config`` (and method from ``volume.counter``)
                on the output video. Implies video output.
            output_video_path: Path for the annotated output video.
            confidence_threshold: Minimum confidence for detections.
            stream_info: Optional stream metadata passed to the engine.
        """
        self.model_path = model_path
        self.video_path = video_path
        self.max_frames = max_frames
        self.loop_count = max(1, loop_count)
        self.json_dir = json_dir
        self.draw_bboxes = draw_bboxes
        self.draw_lines = draw_lines
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
        default_stream_info: dict[str, Any] = (
            dict(FOOTFALL_DEFAULT_STREAM_INFO)
            if manifest_name.lower() == "footfall"
            else {
                "camera_id": "cam1",
                "app_deployment_id": "test_deployment_001",
            }
        )
        self.engine = AnalyticsEngine(
            manifest_path_or_name=manifest_name,
            stream_info=stream_info or default_stream_info,
        )
        os.makedirs(self.json_dir, exist_ok=True)
        self.index_to_category = get_index_to_category(manifest_name)

    # ------------------------------------------------------------------
    # Tracker helpers
    # ------------------------------------------------------------------

    def _run_inference(self, frame):
        """Run YOLO inference only (no tracking) and return raw results."""
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            iou=0.7,
            verbose=False,
        )
        return results[0]

    def _build_raw_detections(self, result) -> list[dict]:
        """Convert ultralytics predict result into detection dicts (no track_id).

        Each detection dict contains:
            - category: mapped entity name (e.g. "person")
            - category_id: COCO class id
            - confidence: float
            - bounding_box: {xmin, ymin, xmax, ymax}
        """
        detections = []
        boxes = result.boxes
        if boxes is None or len(boxes) == 0:
            return detections

        for i in range(len(boxes)):
            cls_id = int(boxes.cls[i])

            category = self.index_to_category.get(cls_id)
            if category is None:
                continue

            conf = float(boxes.conf[i])
            x1, y1, x2, y2 = boxes.xyxy[i].tolist()

            detections.append(
                {
                    "category": category,
                    "category_id": cls_id,
                    "confidence": conf,
                    "bounding_box": {
                        "xmin": x1,
                        "ymin": y1,
                        "xmax": x2,
                        "ymax": y2,
                    },
                }
            )

        return detections

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_bboxes_on_frame(self, frame, detections):
        """Draw bounding boxes with track_id and category label."""
        bbox_color = (0, 255, 0)
        label_bg = (0, 255, 0)
        text_color = (0, 0, 0)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2

        for det in detections:
            bb = det["bounding_box"]
            x1, y1, x2, y2 = int(bb["xmin"]), int(bb["ymin"]), int(bb["xmax"]), int(bb["ymax"])
            label = f"{det['category']} id:{det.get('track_id', '?')} {det['confidence']:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), bbox_color, thickness)

            (tw, th), baseline = cv2.getTextSize(label, font, font_scale, 1)
            cv2.rectangle(frame, (x1, y1 - th - baseline - 4), (x1 + tw + 4, y1), label_bg, -1)
            cv2.putText(frame, label, (x1 + 2, y1 - baseline - 2), font, font_scale, text_color, 1, cv2.LINE_AA)

        return frame

    # ------------------------------------------------------------------
    # Zone / line drawing helpers
    # ------------------------------------------------------------------

    def _parse_zone_geometry(self, width: int, height: int) -> dict[str, Any] | None:
        """Denormalize ``engine.stream_info.zone_config`` to pixel coords for overlays.

        ``method`` and ``in_direction`` come from manifest ``volume.counter``.
        Returns a dict with keys ``method``, ``in_direction``, and either
        ``lines`` (dict of name → (2,2) ndarray) or ``zones`` (dict of
        name → (N,2) ndarray), or None if no zone geometry is present.
        """
        zc = self.engine.stream_info.zone_config
        if zc is None:
            return None

        volume_cfg = self.engine._manifest_config.get("volume", {})
        counter = volume_cfg.get("counter")
        counter = counter if isinstance(counter, dict) else {}

        method = counter.get("method", "abline")
        in_direction = counter.get("in_direction", "A_to_B")

        parsed: dict[str, Any] = {"method": method, "in_direction": in_direction}

        raw_lines = zc.lines
        if raw_lines:
            pixel_lines: dict[str, np.ndarray] = {}
            for name, pts in raw_lines.items():
                arr = np.array(pts, dtype=np.float64)
                arr[:, 0] *= width
                arr[:, 1] *= height
                pixel_lines[name] = arr.astype(np.int32)
            parsed["lines"] = pixel_lines

        raw_zones = zc.zones
        if raw_zones:
            pixel_zones: dict[str, np.ndarray] = {}
            for name, pts in raw_zones.items():
                arr = np.array(pts, dtype=np.float64)
                arr[:, 0] *= width
                arr[:, 1] *= height
                pixel_zones[name] = arr.astype(np.int32)
            parsed["zones"] = pixel_zones

        if "lines" not in parsed and "zones" not in parsed:
            return None

        return parsed

    def _draw_zone_overlay(self, frame, geometry: dict[str, Any]) -> None:
        """Draw lines and/or zones from the parsed zone geometry onto the frame.

        For ``abline`` method: draws two lines with a semi-transparent trap
        zone fill and endpoint circles, coloured by entry/exit direction.
        For ``polygon`` method: draws filled semi-transparent polygons.
        """
        color_entry = (0, 255, 0)  # green
        color_exit = (0, 0, 255)  # red
        trap_fill = (128, 128, 128)

        method = geometry["method"]
        in_direction = geometry.get("in_direction", "A_to_B")

        if method == "abline" and "lines" in geometry:
            line_names = list(geometry["lines"].keys())
            if len(line_names) < 2:
                return
            line_a = geometry["lines"][line_names[0]]
            line_b = geometry["lines"][line_names[1]]

            if in_direction == "A_to_B":
                color_a, color_b = color_exit, color_entry
            else:
                color_a, color_b = color_entry, color_exit

            a1 = tuple(line_a[0])
            a2 = tuple(line_a[1])
            b1 = tuple(line_b[0])
            b2 = tuple(line_b[1])

            quad = np.array([a1, a2, b2, b1], dtype=np.int32)
            overlay = frame.copy()
            cv2.fillPoly(overlay, [quad], trap_fill)
            cv2.addWeighted(overlay, 0.25, frame, 0.75, 0, frame)

            cv2.line(frame, a1, a2, color_a, 3)
            cv2.line(frame, b1, b2, color_b, 3)
            for pt in (a1, a2):
                cv2.circle(frame, pt, 6, color_a, -1)
            for pt in (b1, b2):
                cv2.circle(frame, pt, 6, color_b, -1)

            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, line_names[0], (a1[0] + 10, a1[1] - 10), font, 0.6, color_a, 2, cv2.LINE_AA)
            cv2.putText(frame, line_names[1], (b1[0] + 10, b1[1] - 10), font, 0.6, color_b, 2, cv2.LINE_AA)

        elif method == "polygon" and "zones" in geometry:
            colors = [color_entry, color_exit]
            for idx, (name, poly) in enumerate(geometry["zones"].items()):
                color = colors[idx % len(colors)]
                overlay = frame.copy()
                cv2.fillPoly(overlay, [poly], color)
                cv2.addWeighted(overlay, 0.2, frame, 0.8, 0, frame)
                cv2.polylines(frame, [poly], True, color, 2)

                centroid = poly.mean(axis=0).astype(int)
                cv2.putText(frame, name, tuple(centroid), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2, cv2.LINE_AA)

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    @staticmethod
    def _serialize(obj):
        """Make an object JSON-serializable."""

        def _to_serializable(o):
            if hasattr(o, "model_dump"):
                return o.model_dump()
            if hasattr(o, "to_dict"):
                return o.to_dict()
            if hasattr(o, "__dict__"):
                return o.__dict__
            return str(o)

        return json.loads(json.dumps(obj, default=_to_serializable))

    # ------------------------------------------------------------------
    # Main processing loop
    # ------------------------------------------------------------------

    def process_video(self):
        """Run inference + tracking + analytics engine on every frame."""
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {self.video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        write_video = self.draw_bboxes or self.draw_lines
        video_writer = None
        zone_geometry = None

        if write_video:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(self.output_video_path, fourcc, fps, (width, height))
            print(f"Video output enabled — output video: {self.output_video_path}")

        if self.draw_lines:
            zone_geometry = self._parse_zone_geometry(width, height)
            if zone_geometry:
                print(f"Zone drawing enabled — method: {zone_geometry['method']}")
            else:
                print("draw_lines enabled but no zone_config found in manifest")

        print(f"Starting video processing: {self.video_path}")
        print(f"Model: {self.model_path}")
        print(f"Manifest: people_counting | Engine categories: {self.engine.categories}")
        print(f"Output directory: {self.json_dir}")
        print(f"Loop count: {self.loop_count}")
        print("-" * 60)

        frame_idx = 0
        done = False

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

                # Step 1: Run YOLO inference (no tracking)
                raw_result = self._run_inference(frame)

                # Step 2: Convert to detection dicts, then run ByteTrackWrapper
                raw_detections = self._build_raw_detections(raw_result)
                detections = self.tracker.update(raw_detections)

                # Step 3: Feed into the AnalyticsEngine
                frame_ts = frame_idx / fps if fps > 0 else float(frame_idx)
                frame_result = self.engine.process_frame(
                    detections=detections,
                    frame_ts=frame_ts,
                    frame_id=f"frame_{frame_idx:04d}",
                )
                os.makedirs(os.path.join(self.json_dir, "agg"), exist_ok=True)
                # Step 4: Check for 1-minute aggregation
                agg_result = None
                if self.engine.should_aggregate(frame_ts):
                    agg_result = self.engine.aggregate()
                    agg_path = os.path.join(self.json_dir, "agg", f"agg_{frame_idx:04d}.json")
                    with open(agg_path, "w") as f:
                        json.dump(self._serialize(agg_result), f, indent=2)
                    print(f"  ** Aggregation triggered at frame {frame_idx} — saved: {agg_path}")

                # Step 5: Draw overlays and write video frame
                if write_video and video_writer is not None:
                    annotated = frame.copy()
                    if zone_geometry:
                        self._draw_zone_overlay(annotated, zone_geometry)
                    if self.draw_bboxes:
                        annotated = self._draw_bboxes_on_frame(annotated, detections)
                    video_writer.write(annotated)

                # Step 6: Save per-frame result
                json_path = os.path.join(self.json_dir, f"frame_{frame_idx:04d}.json")
                with open(json_path, "w") as f:
                    json.dump(self._serialize(frame_result), f, indent=2)

                print(
                    f"[Loop {loop_idx + 1}/{self.loop_count}] Frame {frame_idx:4d} | "
                    f"detections: {len(detections):3d} | metrics: {frame_result} | saved: {json_path}"
                )

                frame_idx += 1
                if self.max_frames and frame_idx >= self.max_frames:
                    print(f"Max frame limit ({self.max_frames}) reached.")
                    done = True
                    break

        # Final aggregation for remaining frames
        final_agg = self.engine.aggregate()
        final_agg_path = os.path.join(self.json_dir, "agg", "agg_final.json")
        with open(final_agg_path, "w") as f:
            json.dump(self._serialize(final_agg), f, indent=2)
        print(f"\nFinal aggregation saved: {final_agg_path}")
        print("Final aggregation result:")
        pprint.pprint(self._serialize(final_agg))

        cap.release()
        if video_writer is not None:
            video_writer.release()
            print(f"Output video saved to: {self.output_video_path}")

        print(f"\nProcessing complete. {frame_idx} frames processed.")
        print(f"JSON outputs saved in: {self.json_dir}")


if __name__ == "__main__":
    processor = AnalyticsEngineTestProcessor(
        manifest_name="footfall",
        model_path=r"C:\Users\aswan_3sr40l5\Matrice\models\best_Finetune_enterprise_11m.pt",
        video_path=r"C:\Users\aswan_3sr40l5\Matrice\datasets\test_videos\ayala4.mp4",
        max_frames=None,
        loop_count=10,
        json_dir="jsons_footfall_new6",
        draw_bboxes=True,
        draw_lines=True,
        output_video_path="output_footfall_new6.mp4",
        confidence_threshold=0.1,
    )
    processor.process_video()
