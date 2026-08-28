from __future__ import annotations
import argparse
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
_ROOT = Path(__file__).resolve().parents[4]
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


INDEX_TO_CATEGORY_MAP: dict[str, dict[int, str]] = {
    "fire_detection_new": {0: "fire", 1: "smoke"},
    "weapon_detection_new": {0: "weapon", 1: "person"},
}


def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """Returns the index-to-category mapping according to the analytics manifest.

    Args:
        manifest_name: The YAML manifest name (e.g. "fire_detection").
    """
    key = manifest_name.lower()
    if key in INDEX_TO_CATEGORY_MAP:
        return INDEX_TO_CATEGORY_MAP[key]
    return {0: "fire"}


class IncidentAnalyticsTestProcessor:
    """End-to-end test harness for incident-type analytics (fire detection).

    Runs YOLO inference on a video, converts detections into the format
    expected by the AnalyticsEngine with an INCIDENT category processor,
    and stores per-frame results, aggregation results, and incident events
    as JSON files.
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
        output_video_path: str = "output.mp4",
        confidence_threshold: float = 0.45,
        stream_info: dict | None = None,
    ) -> None:
        """Initialize the incident test processor.

        Args:
            manifest_name: Name of the YAML manifest under analytics/config/
                (e.g. "fire_detection").
            model_path: Path to the YOLO model weights (.pt).
            video_path: Path to the input video file.
            max_frames: Stop after this many frames (None = all, across all loops).
            loop_count: Number of times to loop the video (default 1 = no loop).
            json_dir: Directory for per-frame JSON outputs.
            draw_bboxes: If True, annotate frames and write an output video.
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
        self.output_video_path = output_video_path
        self.confidence_threshold = confidence_threshold

        self.model = YOLO(self.model_path)
        self.tracker = ByteTrackWrapper(
            track_high_thresh=0.4,
            track_low_thresh=0.1,
            new_track_thresh=0.4,
            track_buffer=90,
            match_thresh=0.8,
            frame_rate=30,
        )

        default_stream_info: dict[str, Any] = {
            "camera_id": "cam1",
            "app_deployment_id": f"test_deployment_{manifest_name}_001",
        }
        resolved_stream = stream_info or default_stream_info
        self._camera_id = str(resolved_stream.get("camera_id", "default_camera"))
        self.engine = AnalyticsEngine(
            manifest_path_or_name=manifest_name,
            stream_info=resolved_stream,
        )
        os.makedirs(self.json_dir, exist_ok=True)
        self.index_to_category = get_index_to_category(manifest_name)
        self._manifest_name = manifest_name

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def _run_inference(self, frame):
        """Run YOLO inference and return raw results."""
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
            - category: mapped entity name (e.g. "fire", "smoke")
            - category_id: class id from model
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

    def _tag_detections_camera(self, detections: list[dict]) -> list[dict]:
        """Attach ``_camera_id`` so :class:`IncidentProcessor` resolves the same camera as ``StreamInfo``."""
        for det in detections:
            det["_camera_id"] = self._camera_id
        return detections

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_bboxes_on_frame(self, frame, detections):
        """Draw bounding boxes with category label and confidence."""
        color_map = {
            "fire": (0, 0, 255),
            "smoke": (128, 128, 128),
            "weapon": (0, 140, 255),
            "person": (0, 200, 0),
        }
        text_color = (255, 255, 255)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2

        for det in detections:
            bb = det["bounding_box"]
            x1, y1, x2, y2 = int(bb["xmin"]), int(bb["ymin"]), int(bb["xmax"]), int(bb["ymax"])
            cat = det["category"]
            label = f"{cat} id:{det.get('track_id', '?')} {det['confidence']:.2f}"
            bbox_color = color_map.get(cat, (0, 255, 0))

            cv2.rectangle(frame, (x1, y1), (x2, y2), bbox_color, thickness)

            (tw, th), baseline = cv2.getTextSize(label, font, font_scale, 1)
            cv2.rectangle(frame, (x1, y1 - th - baseline - 4), (x1 + tw + 4, y1), bbox_color, -1)
            cv2.putText(frame, label, (x1 + 2, y1 - baseline - 2), font, font_scale, text_color, 1, cv2.LINE_AA)

        return frame

    def _draw_incident_status(self, frame, severity: str, quant: float):
        """Draw an incident severity banner at the top of the frame."""
        severity_colors = {
            "none": (0, 128, 0),
            "low": (0, 200, 200),
            "medium": (0, 165, 255),
            "significant": (0, 69, 255),
            "high": (0, 69, 255),  # backend alias for significant
            "critical": (0, 0, 255),
            "info": (200, 200, 200),
        }
        color = severity_colors.get(severity, (128, 128, 128))
        width = frame.shape[1]

        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (width, 40), color, -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)

        label = f"Severity: {severity.upper()} | Quant: {quant:.1f}%"
        cv2.putText(frame, label, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

        return frame

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
        """Run inference + incident analytics engine on every frame."""
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {self.video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        video_writer = None
        if self.draw_bboxes:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(self.output_video_path, fourcc, fps, (width, height))
            print(f"Video output enabled — output video: {self.output_video_path}")

        print(f"Starting incident analytics test: {self.video_path}")
        print(f"Model: {self.model_path}")
        print(f"Manifest: {self._manifest_name} | Engine categories: {self.engine.categories}")
        print(f"Output directory: {self.json_dir}")
        print(f"Loop count: {self.loop_count}")
        print("-" * 60)

        frame_idx = 0
        done = False
        total_events: list[dict[str, Any]] = []

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

                raw_result = self._run_inference(frame)
                raw_detections = self._build_raw_detections(raw_result)
                detections = self.tracker.update(raw_detections)
                detections = self._tag_detections_camera(detections)

                frame_ts = frame_idx / fps if fps > 0 else float(frame_idx)
                frame_result = self.engine.process_frame(
                    detections=detections,
                    frame_ts=frame_ts,
                    frame_id=f"frame_{frame_idx:04d}",
                )

                # Drain incident events (Pydantic ``IncidentEvent`` models)
                events = self.engine.drain_incident_events()
                if events:
                    for ev in events:
                        ev_dict = ev.model_dump() if hasattr(ev, "model_dump") else ev
                        total_events.append(ev_dict)
                    events_dir = os.path.join(self.json_dir, "events")
                    os.makedirs(events_dir, exist_ok=True)
                    for ev in events:
                        ev_dict = ev.model_dump() if hasattr(ev, "model_dump") else ev
                        ev_path = os.path.join(events_dir, f"event_{frame_idx:04d}.json")
                        with open(ev_path, "w") as f:
                            json.dump(ev_dict, f, indent=2)
                        sev = ev_dict.get("severity_level", "?")
                        etype = "END" if ev_dict.get("is_end_signal") else "ALERT"
                        print(f"  ** [{etype}] Incident event at frame {frame_idx}: severity={sev}")

                os.makedirs(os.path.join(self.json_dir, "agg"), exist_ok=True)

                agg_result = None
                if self.engine.should_aggregate(frame_ts):
                    agg_result = self.engine.aggregate()
                    agg_path = os.path.join(self.json_dir, "agg", f"agg_{frame_idx:04d}.json")
                    with open(agg_path, "w") as f:
                        json.dump(self._serialize(agg_result), f, indent=2)
                    print(f"  ** Aggregation triggered at frame {frame_idx} — saved: {agg_path}")

                # Extract severity / quant from ``IncidentFrameResult`` (no metrics[] for INCIDENT)
                incident_fr = frame_result.get("INCIDENT") or {}
                sr = incident_fr.get("severity_level", "none")
                if hasattr(sr, "value"):
                    severity_name = str(sr.value)
                else:
                    severity_name = str(sr) if sr is not None else "none"
                quant_val = float(incident_fr.get("incident_quant", 0.0))

                if self.draw_bboxes and video_writer is not None:
                    annotated = frame.copy()
                    annotated = self._draw_bboxes_on_frame(annotated, detections)
                    annotated = self._draw_incident_status(annotated, severity_name, quant_val)
                    video_writer.write(annotated)

                json_path = os.path.join(self.json_dir, f"frame_{frame_idx:04d}.json")
                with open(json_path, "w") as f:
                    json.dump(self._serialize(frame_result), f, indent=2)

                print(
                    f"[Loop {loop_idx + 1}/{self.loop_count}] Frame {frame_idx:4d} | "
                    f"detections: {len(detections):3d} | severity: {severity_name:12s} | "
                    f"quant: {quant_val:6.2f}% | saved: {json_path}"
                )

                frame_idx += 1
                if self.max_frames and frame_idx >= self.max_frames:
                    print(f"Max frame limit ({self.max_frames}) reached.")
                    done = True
                    break

        # Final aggregation
        final_agg = self.engine.aggregate()
        final_agg_path = os.path.join(self.json_dir, "agg", "agg_final.json")
        with open(final_agg_path, "w") as f:
            json.dump(self._serialize(final_agg), f, indent=2)
        print(f"\nFinal aggregation saved: {final_agg_path}")
        print("Final aggregation result:")
        pprint.pprint(self._serialize(final_agg))

        # Save all incident events summary
        if total_events:
            all_events_path = os.path.join(self.json_dir, "events", "all_events.json")
            with open(all_events_path, "w") as f:
                json.dump(self._serialize(total_events), f, indent=2)
            print(f"\n{len(total_events)} incident event(s) saved: {all_events_path}")
        else:
            print("\nNo incident events emitted during processing.")

        # Print lifecycle state for debugging (``IncidentLifecycleState`` Pydantic model).
        # With no detections yet, the processor may still use ``default_camera``.
        for cid in (self._camera_id, "default_camera"):
            state = self.engine.get_incident_state(cid)
            if state:
                print(f"\nFinal incident lifecycle state ({cid}):")
                pprint.pprint(state.model_dump() if hasattr(state, "model_dump") else state)
                break

        cap.release()
        if video_writer is not None:
            video_writer.release()
            print(f"Output video saved to: {self.output_video_path}")

        print(f"\nProcessing complete. {frame_idx} frames processed.")
        print(f"JSON outputs saved in: {self.json_dir}")


MANIFEST_DEFAULTS: dict[str, dict[str, Any]] = {
    "fire_detection_new": {
        "model_path": r"C:\Users\aswan_3sr40l5\Matrice\models\yolov8n_fire.pt",
        "video_path": r"C:\Users\aswan_3sr40l5\Matrice\datasets\test_videos\fire_gap.mp4",
        "json_dir": "jsons_fire_detection",
        "output_video_path": "output_fire_detection.mp4",
        "confidence_threshold": 0.25,
    },
    "weapon_detection_new": {
        "model_path": r"C:\Users\aswan_3sr40l5\Matrice\models\weapon_human_best.pt",
        "video_path": r"C:\Users\aswan_3sr40l5\Matrice\datasets\test_videos\weapon_test.mp4",
        "json_dir": "jsons_weapon_detection",
        "output_video_path": "output_weapon_detection.mp4",
        "confidence_threshold": 0.28,
    },
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run incident analytics test harness.")
    parser.add_argument(
        "--manifest",
        default="fire_detection_new",
        choices=sorted(INDEX_TO_CATEGORY_MAP.keys()),
        help="Analytics manifest under analytics/config/ (default: fire_detection_new).",
    )
    parser.add_argument("--model-path", default=None, help="YOLO weights (.pt).")
    parser.add_argument("--video-path", default=None, help="Input video file.")
    parser.add_argument("--json-dir", default=None, help="Output directory for JSON artifacts.")
    parser.add_argument("--output-video", default=None, help="Annotated output video path.")
    parser.add_argument("--max-frames", type=int, default=None)
    parser.add_argument("--loop-count", type=int, default=1)
    parser.add_argument("--confidence", type=float, default=None)
    parser.add_argument("--no-video", action="store_true", help="Skip annotated video output.")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    defaults = MANIFEST_DEFAULTS.get(args.manifest, {})
    processor = IncidentAnalyticsTestProcessor(
        manifest_name=args.manifest,
        model_path=args.model_path or defaults.get("model_path", ""),
        video_path=args.video_path or defaults.get("video_path", ""),
        max_frames=args.max_frames,
        loop_count=args.loop_count,
        json_dir=args.json_dir or defaults.get("json_dir", "jsons"),
        draw_bboxes=not args.no_video,
        output_video_path=args.output_video or defaults.get("output_video_path", "output.mp4"),
        confidence_threshold=args.confidence if args.confidence is not None else defaults.get(
            "confidence_threshold", 0.45
        ),
    )
    processor.process_video()
