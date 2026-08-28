"""End-to-end QUALITY analytics harness for Car Damage Detection.

Single-model pipeline:
  1. Run ``best_car.pt`` (6 damage classes) on each frame.
  2. Shape detections for the analytics engine.
  3. Run ByteTrackWrapper for stable per-damage track IDs
     (needed for window-level unique counting).
  4. Feed into AnalyticsEngine loaded from ``car_damage_detection_new.yaml``.
  5. Emit per-frame + 1-minute aggregation JSON.

Usage (run from repo root or anywhere):
    python src/matrice_analytics/analytics/tests/test_quality_analytics.py
"""
from __future__ import annotations

import csv
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

# ---------------------------------------------------------------------------
# Import bootstrap (analytics + footfall only, no heavy post_processing init)
# ---------------------------------------------------------------------------
_THIS_FILE = Path(__file__).resolve()
_ROOT = _THIS_FILE.parents[4]  # …/py_analytics
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
_register_pkg(
    "matrice_analytics.post_processing.usecases",
    _PKG / "post_processing" / "usecases",
)

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
# Model → analytics entity mapping
# ---------------------------------------------------------------------------
INDEX_TO_CATEGORY_MAP: dict[str, dict[int, str]] = {
    "car_damage_detection": {
        0: "dent",
        1: "scratch",
        2: "crack",
        3: "shattered_glass",
        4: "broken_lamp",
        5: "flat_tire",
    },
    "car_damage_detection_new": {
        0: "dent",
        1: "scratch",
        2: "crack",
        3: "shattered_glass",
        4: "broken_lamp",
        5: "flat_tire",
    },
}


def get_index_to_category(manifest_name: str) -> dict[int, str]:
    """Returns the index→category mapping for a manifest."""
    return INDEX_TO_CATEGORY_MAP.get(manifest_name.lower(), {})


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------
class QualityAnalyticsTestProcessor:
    """End-to-end test harness for the QUALITY processor.

    Runs a YOLO model + ByteTrackWrapper on a video, feeds tracked
    detections into the new ``AnalyticsEngine``, and dumps per-frame +
    aggregation JSONs.
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
        csv_path: str | None = None,
        confidence_threshold: float = 0.4,
        stream_info: dict | None = None,
    ) -> None:
        self.manifest_name = manifest_name
        self.model_path = model_path
        self.video_path = video_path
        self.max_frames = max_frames
        self.loop_count = max(1, loop_count)
        self.json_dir = json_dir
        self.draw_bboxes = draw_bboxes
        self.output_video_path = output_video_path
        self.csv_path = csv_path
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

        default_stream_info: dict[str, Any] = {
            "camera_id": "cam1",
            "app_deployment_id": "test_deployment_001",
        }
        self.engine = AnalyticsEngine(
            manifest_path_or_name=manifest_name,
            stream_info=stream_info or default_stream_info,
        )
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(os.path.join(self.json_dir, "agg"), exist_ok=True)
        self.index_to_category = get_index_to_category(manifest_name)

        # Running cumulative totals across 1-min windows.
        # NOTE: Python processors emit per-window (delta) values by design
        # (see docs/ANALYTICS_FLOW_DESIGN.md §815-817). Cumulative totals
        # are the Go/ClickHouse layer's job (aggregated_analytics_totals).
        # We compute a cumulative view here purely for test inspection.
        self._cum_defect_count: float = 0.0
        self._cum_total_inspected: float = 0.0
        self._agg_rows: list[dict[str, float]] = []

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------
    def _run_inference(self, frame):
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            iou=0.7,
            verbose=False,
        )
        return results[0]

    def _build_raw_detections(self, result) -> list[dict]:
        detections: list[dict] = []
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
    # Drawing
    # ------------------------------------------------------------------
    def _draw_bboxes_on_frame(self, frame, detections):
        color_by_cat = {
            "dent": (255, 200, 0),
            "scratch": (0, 200, 255),
            "crack": (0, 0, 255),
            "shattered_glass": (255, 0, 255),
            "broken_lamp": (0, 128, 255),
            "flat_tire": (128, 0, 128),
        }
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.55
        thickness = 2

        for det in detections:
            bb = det["bounding_box"]
            x1 = int(bb["xmin"])
            y1 = int(bb["ymin"])
            x2 = int(bb["xmax"])
            y2 = int(bb["ymax"])
            color = color_by_cat.get(det["category"], (0, 255, 0))
            label = (
                f"{det['category']} id:{det.get('track_id', '?')} "
                f"{det['confidence']:.2f}"
            )
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
            (tw, th), baseline = cv2.getTextSize(label, font, font_scale, 1)
            cv2.rectangle(
                frame,
                (x1, y1 - th - baseline - 4),
                (x1 + tw + 4, y1),
                color,
                -1,
            )
            cv2.putText(
                frame,
                label,
                (x1 + 2, y1 - baseline - 2),
                font,
                font_scale,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )
        return frame

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------
    @staticmethod
    def _serialize(obj):
        def _to_serializable(o):
            if hasattr(o, "model_dump"):
                return o.model_dump()
            if hasattr(o, "to_dict"):
                return o.to_dict()
            if hasattr(o, "__dict__"):
                return o.__dict__
            return str(o)

        return json.loads(json.dumps(obj, default=_to_serializable))

    @staticmethod
    def _extract_window_metrics(serialized: Any) -> dict[str, float]:
        """Walk a serialized aggregation result and pull out the
        window-level defect_count / total_inspected / defect_rate.

        The Python aggregation output nests metrics under
        ``processors[*].metrics`` (or similar); different SDK revisions
        move keys around, so we do a tolerant recursive search.
        """
        wanted = {"defect_count", "total_inspected", "defect_rate"}
        found: dict[str, float] = {}

        def _walk(node: Any) -> None:
            if isinstance(node, dict):
                # MetricEntry-style: {"key": "defect_count", "data": 23.0, ...}
                k = node.get("key")
                if (
                    isinstance(k, str)
                    and k in wanted
                    and isinstance(node.get("data"), (int, float))
                ):
                    found.setdefault(k, float(node["data"]))
                for key, v in node.items():
                    if key in wanted and isinstance(v, (int, float)):
                        found.setdefault(key, float(v))
                    else:
                        _walk(v)
            elif isinstance(node, list):
                for item in node:
                    _walk(item)

        _walk(serialized)
        return found

    def _record_window_agg(
        self,
        serialized_agg: Any,
        *,
        frame_idx: int,
        loop_idx: int,
        frame_ts: float,
        label: str,
    ) -> dict[str, float]:
        """Update running cumulative totals and stash a row for the
        agg-summary CSV. Returns the row dict."""
        win = self._extract_window_metrics(serialized_agg)
        dc = win.get("defect_count", 0.0)
        ti = win.get("total_inspected", 0.0)
        dr = win.get("defect_rate", 0.0)

        self._cum_defect_count += dc
        self._cum_total_inspected += ti
        cum_rate = (
            self._cum_defect_count / self._cum_total_inspected
            if self._cum_total_inspected > 0
            else 0.0
        )
        row = {
            "label": label,
            "frame_idx": frame_idx,
            "loop_idx": loop_idx,
            "frame_ts": round(frame_ts, 3),
            "window_defect_count": dc,
            "window_total_inspected": ti,
            "window_defect_rate": round(dr, 4),
            "cum_defect_count": self._cum_defect_count,
            "cum_total_inspected": self._cum_total_inspected,
            "cum_defect_rate": round(cum_rate, 4),
        }
        self._agg_rows.append(row)
        return row

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

        video_writer = None
        if self.draw_bboxes:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(
                self.output_video_path, fourcc, fps, (width, height)
            )
            print(f"Video output enabled — {self.output_video_path}")

        csv_file = None
        csv_writer = None
        if self.csv_path:
            os.makedirs(os.path.dirname(self.csv_path) or ".", exist_ok=True)
            csv_file = open(self.csv_path, "w", newline="")
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(
                [
                    "frame_idx",
                    "loop_idx",
                    "frame_ts",
                    "num_detections",
                    "defect_count",
                    "total_inspected",
                    "defect_rate",
                ]
            )
            print(f"CSV output enabled — {self.csv_path}")

        print(f"Starting processing: {self.video_path}")
        print(f"Model: {self.model_path}")
        print(f"Manifest: {self.manifest_name} | categories: {self.engine.categories}")
        print(f"JSON dir: {self.json_dir} | Loop count: {self.loop_count}")
        print("-" * 70)

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

                raw_result = self._run_inference(frame)
                raw_detections = self._build_raw_detections(raw_result)
                detections = self.tracker.update(raw_detections)

                frame_ts = frame_idx / fps if fps > 0 else float(frame_idx)
                frame_result = self.engine.process_frame(
                    detections=detections,
                    frame_ts=frame_ts,
                    frame_id=f"frame_{frame_idx:04d}",
                )

                if self.engine.should_aggregate(frame_ts):
                    agg_result = self.engine.aggregate()
                    serialized = self._serialize(agg_result)
                    row = self._record_window_agg(
                        serialized,
                        frame_idx=frame_idx,
                        loop_idx=loop_idx + 1,
                        frame_ts=frame_ts,
                        label=f"window_{len(self._agg_rows) + 1}",
                    )
                    # Embed cumulative view alongside the processor output
                    # (does not alter the processor's own payload).
                    serialized_with_cum = {
                        "aggregation": serialized,
                        "cumulative_view": {
                            "cum_defect_count": row["cum_defect_count"],
                            "cum_total_inspected": row["cum_total_inspected"],
                            "cum_defect_rate": row["cum_defect_rate"],
                        },
                    }
                    agg_path = os.path.join(
                        self.json_dir, "agg", f"agg_{frame_idx:04d}.json"
                    )
                    with open(agg_path, "w") as f:
                        json.dump(serialized_with_cum, f, indent=2)
                    print(
                        f"  ** Aggregation at frame {frame_idx} → {agg_path} "
                        f"| window dc={row['window_defect_count']:.0f} "
                        f"ti={row['window_total_inspected']:.0f} "
                        f"dr={row['window_defect_rate']:.4f} "
                        f"| cum dc={row['cum_defect_count']:.0f} "
                        f"ti={row['cum_total_inspected']:.0f} "
                        f"dr={row['cum_defect_rate']:.4f}"
                    )

                if video_writer is not None:
                    annotated = self._draw_bboxes_on_frame(frame.copy(), detections)
                    video_writer.write(annotated)

                json_path = os.path.join(self.json_dir, f"frame_{frame_idx:04d}.json")
                with open(json_path, "w") as f:
                    json.dump(self._serialize(frame_result), f, indent=2)

                if csv_writer is not None:
                    # Pull the raw per-frame QUALITY metrics from the
                    # processor's frame buffer (business_analytics is
                    # cumulative, so read the raw MetricEntry list).
                    per_frame: dict[str, float] = {}
                    for _proc in self.engine.processors.values():
                        if not _proc._frame_buffer:
                            continue
                        for _m in _proc._frame_buffer[-1].metrics:
                            per_frame[_m.key] = float(_m.data)
                    csv_writer.writerow(
                        [
                            frame_idx,
                            loop_idx + 1,
                            round(frame_ts, 3),
                            len(detections),
                            per_frame.get("defect_count", 0.0),
                            per_frame.get("total_inspected", 0.0),
                            per_frame.get("defect_rate", 0.0),
                        ]
                    )

                if frame_idx % 30 == 0:
                    print(
                        f"[Loop {loop_idx + 1}/{self.loop_count}] "
                        f"Frame {frame_idx:4d} | dets: {len(detections):3d}"
                    )

                frame_idx += 1
                if self.max_frames and frame_idx >= self.max_frames:
                    print(f"Max frame limit ({self.max_frames}) reached.")
                    done = True
                    break

        final_agg = self.engine.aggregate()
        final_serialized = self._serialize(final_agg)
        final_row = self._record_window_agg(
            final_serialized,
            frame_idx=frame_idx,
            loop_idx=self.loop_count,
            frame_ts=frame_idx / fps if fps > 0 else float(frame_idx),
            label="final_partial",
        )
        final_agg_path = os.path.join(self.json_dir, "agg", "agg_final.json")
        with open(final_agg_path, "w") as f:
            json.dump(
                {
                    "aggregation": final_serialized,
                    "cumulative_view": {
                        "cum_defect_count": final_row["cum_defect_count"],
                        "cum_total_inspected": final_row["cum_total_inspected"],
                        "cum_defect_rate": final_row["cum_defect_rate"],
                    },
                },
                f,
                indent=2,
            )
        print(f"\nFinal aggregation saved: {final_agg_path}")
        print("Final aggregation result:")
        pprint.pprint(final_serialized)

        # Per-window summary CSV (window deltas + running cumulative view).
        summary_csv_path = os.path.join(self.json_dir, "agg", "agg_summary.csv")
        with open(summary_csv_path, "w", newline="") as f:
            sw = csv.writer(f)
            sw.writerow(
                [
                    "label",
                    "frame_idx",
                    "loop_idx",
                    "frame_ts",
                    "window_defect_count",
                    "window_total_inspected",
                    "window_defect_rate",
                    "cum_defect_count",
                    "cum_total_inspected",
                    "cum_defect_rate",
                ]
            )
            for r in self._agg_rows:
                sw.writerow(
                    [
                        r["label"],
                        r["frame_idx"],
                        r["loop_idx"],
                        r["frame_ts"],
                        r["window_defect_count"],
                        r["window_total_inspected"],
                        r["window_defect_rate"],
                        r["cum_defect_count"],
                        r["cum_total_inspected"],
                        r["cum_defect_rate"],
                    ]
                )
        print(f"Aggregation summary CSV: {summary_csv_path}")

        cap.release()
        if video_writer is not None:
            video_writer.release()
            print(f"Output video saved: {self.output_video_path}")
        if csv_file is not None:
            csv_file.close()
            print(f"CSV saved: {self.csv_path}")

        print(f"\nDone. {frame_idx} frames processed.")
        print(f"JSON outputs: {self.json_dir}")


if __name__ == "__main__":
    BASE = Path(r"C:/Users/Sreenivasan/OneDrive/Desktop/matrice/Car Damage detection")
    processor = QualityAnalyticsTestProcessor(
        manifest_name="car_damage_detection",
        model_path=str(BASE / "best_car.pt"),
        video_path=str(BASE / "combined.mp4"),
        max_frames=None,
        loop_count=10,
        json_dir=str(BASE / "output" / "jsons"),
        draw_bboxes=True,
        output_video_path=str(BASE / "output" / "combined_annotated.mp4"),
        csv_path=str(BASE / "output" / "car_damage_per_frame.csv"),
        confidence_threshold=0.4,
    )
    processor.process_video()
