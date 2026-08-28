"""End-to-end IDENTITY analytics harness for License Plate Recognition.

Two-stage pipeline:
  1. Run ``license_plate_detector_v1.pt`` on each frame → plate bboxes.
  2. Shape detections for the analytics engine.
  3. Run ByteTrackWrapper for stable per-plate track IDs
     (needed for window-level unique counting).
  4. Crop each plate bbox + run ``fast_plate_ocr`` → ``plate_text``
     with a per-track cache so OCR isn't re-run every frame for the
     same plate.
  5. Feed tracked + OCR'd detections into AnalyticsEngine loaded from
     ``license_plate_recognition.yaml``.
  6. Emit per-frame + 1-minute aggregation JSON, running a cumulative
     view across windows (for test inspection only — the Python layer
     emits per-window values by design; cumulative totals are the
     Go/ClickHouse job).

Usage (run from repo root or anywhere):
    python src/matrice_analytics/analytics/tests/test_identity_analytics.py
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
import numpy as np
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
# license_plate_detector_v1.pt class map: {0: 'license_plate', 1: 'mask'}
# Only class 0 is surfaced to the analytics engine.
INDEX_TO_CATEGORY_MAP: dict[str, dict[int, str]] = {
    "license_plate_recognition": {
        0: "license_plate",
    },
}


def get_index_to_category(manifest_name: str) -> dict[int, str]:
    return INDEX_TO_CATEGORY_MAP.get(manifest_name.lower(), {})


# ---------------------------------------------------------------------------
# OCR wrapper -- per-track cache to amortise OCR cost
# ---------------------------------------------------------------------------
class PlateOCR:
    """Wrap ``fast_plate_ocr.LicensePlateRecognizer`` with a per-track cache.

    The OCR model runs only when:
      - we have not yet produced any text for this track_id, OR
      - the cached confidence is below ``refresh_conf`` AND the track
        has been re-seen since the last OCR attempt more than
        ``refresh_every`` frames ago.
    """

    def __init__(
        self,
        hub_model: str = "cct-xs-v1-global-model",
        min_box_px: int = 24,
        refresh_conf: float = 0.75,
        refresh_every: int = 30,
    ) -> None:
        from fast_plate_ocr import LicensePlateRecognizer

        self._reader = LicensePlateRecognizer(hub_model)
        self._min_box_px = min_box_px
        self._refresh_conf = refresh_conf
        self._refresh_every = refresh_every

        # track_id -> {"text": str, "conf": float, "last_frame": int}
        self._cache: dict[Any, dict[str, Any]] = {}

    def _crop(self, frame: np.ndarray, bb: dict[str, float]) -> np.ndarray | None:
        h, w = frame.shape[:2]
        x1 = max(0, int(bb["xmin"]))
        y1 = max(0, int(bb["ymin"]))
        x2 = min(w, int(bb["xmax"]))
        y2 = min(h, int(bb["ymax"]))
        if x2 - x1 < self._min_box_px or y2 - y1 < self._min_box_px:
            return None
        return frame[y1:y2, x1:x2]

    def _run_ocr(self, crop: np.ndarray) -> tuple[str, float]:
        try:
            preds = self._reader.run(crop, return_confidence=True)
        except Exception:  # pragma: no cover - defensive
            return "", 0.0
        if not preds:
            return "", 0.0
        p = preds[0]
        text = (p.plate or "").strip()
        probs = getattr(p, "char_probs", None)
        if probs is not None and len(probs) > 0:
            conf = float(np.mean(probs))
        else:
            conf = 0.0
        return text, conf

    def enrich(
        self,
        detections: list[dict[str, Any]],
        frame: np.ndarray,
        frame_idx: int,
    ) -> None:
        """Attach ``plate_text`` + ``identity_confidence`` in place."""
        for det in detections:
            tid = det.get("track_id")
            bb = det.get("bounding_box") or {}
            cached = self._cache.get(tid) if tid is not None else None

            need_ocr = True
            if cached is not None:
                if cached["conf"] >= self._refresh_conf:
                    need_ocr = False
                elif frame_idx - cached["last_frame"] < self._refresh_every:
                    need_ocr = False

            if need_ocr:
                crop = self._crop(frame, bb)
                if crop is not None and crop.size > 0:
                    text, conf = self._run_ocr(crop)
                    if cached is None or conf >= cached["conf"]:
                        cached = {
                            "text": text,
                            "conf": conf,
                            "last_frame": frame_idx,
                        }
                        if tid is not None:
                            self._cache[tid] = cached
                    else:
                        cached["last_frame"] = frame_idx

            if cached is not None:
                det["plate_text"] = cached["text"]
                det["identity_confidence"] = cached["conf"]
            else:
                det["plate_text"] = ""
                det["identity_confidence"] = 0.0


# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------
class IdentityAnalyticsTestProcessor:
    """End-to-end test harness for the IDENTITY processor (LPR)."""

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
        confidence_threshold: float = 0.35,
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
            track_high_thresh=0.35,
            track_low_thresh=0.1,
            new_track_thresh=0.35,
            track_buffer=60,
            match_thresh=0.8,
            frame_rate=30,
        )
        self.ocr = PlateOCR()

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

        # Cumulative view across 1-min windows (test-only).
        self._cum_total: float = 0.0
        self._cum_matched: float = 0.0
        self._cum_unknown: float = 0.0
        self._cum_blacklist: float = 0.0
        self._agg_rows: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------
    def _run_inference(self, frame):
        results = self.model.predict(
            frame,
            conf=self.confidence_threshold,
            iou=0.6,
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
                continue  # skip "mask" class
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
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.55
        thickness = 2
        for det in detections:
            bb = det["bounding_box"]
            x1 = int(bb["xmin"])
            y1 = int(bb["ymin"])
            x2 = int(bb["xmax"])
            y2 = int(bb["ymax"])
            plate_text = det.get("plate_text") or ""
            ocr_conf = det.get("identity_confidence", 0.0)
            color = (0, 200, 0) if plate_text else (0, 165, 255)
            label = (
                f"id:{det.get('track_id', '?')} {plate_text or '...'} "
                f"det:{det['confidence']:.2f} ocr:{ocr_conf:.2f}"
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
        """Pull IDENTITY metrics out of a serialized aggregation result."""
        wanted = {
            "total_identifications",
            "matched_count",
            "unknown_count",
            "blacklist_matches",
            "match_confidence_avg",
        }
        found: dict[str, float] = {}

        def _walk(node: Any) -> None:
            if isinstance(node, dict):
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
    ) -> dict[str, Any]:
        win = self._extract_window_metrics(serialized_agg)
        total = win.get("total_identifications", 0.0)
        matched = win.get("matched_count", 0.0)
        unknown = win.get("unknown_count", 0.0)
        blacklist = win.get("blacklist_matches", 0.0)
        avg_conf = win.get("match_confidence_avg", 0.0)

        self._cum_total += total
        self._cum_matched += matched
        self._cum_unknown += unknown
        self._cum_blacklist += blacklist
        cum_match_rate = (
            self._cum_matched / self._cum_total if self._cum_total > 0 else 0.0
        )
        row = {
            "label": label,
            "frame_idx": frame_idx,
            "loop_idx": loop_idx,
            "frame_ts": round(frame_ts, 3),
            "window_total": total,
            "window_matched": matched,
            "window_unknown": unknown,
            "window_blacklist": blacklist,
            "window_match_conf_avg": round(avg_conf, 4),
            "cum_total": self._cum_total,
            "cum_matched": self._cum_matched,
            "cum_unknown": self._cum_unknown,
            "cum_blacklist": self._cum_blacklist,
            "cum_match_rate": round(cum_match_rate, 4),
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
                    "total_identifications",
                    "matched_count",
                    "unknown_count",
                    "blacklist_matches",
                    "match_confidence_avg",
                    "plate_texts",
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
                # OCR enrichment (populates plate_text + identity_confidence)
                self.ocr.enrich(detections, frame, frame_idx)

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
                    serialized_with_cum = {
                        "aggregation": serialized,
                        "cumulative_view": {
                            "cum_total": row["cum_total"],
                            "cum_matched": row["cum_matched"],
                            "cum_unknown": row["cum_unknown"],
                            "cum_blacklist": row["cum_blacklist"],
                            "cum_match_rate": row["cum_match_rate"],
                        },
                    }
                    agg_path = os.path.join(
                        self.json_dir, "agg", f"agg_{frame_idx:04d}.json"
                    )
                    with open(agg_path, "w") as f:
                        json.dump(serialized_with_cum, f, indent=2)
                    print(
                        f"  ** Aggregation at frame {frame_idx} → {agg_path} "
                        f"| win total={row['window_total']:.0f} "
                        f"matched={row['window_matched']:.0f} "
                        f"unknown={row['window_unknown']:.0f} "
                        f"blk={row['window_blacklist']:.0f} "
                        f"conf={row['window_match_conf_avg']:.2f} "
                        f"| cum total={row['cum_total']:.0f} "
                        f"matched={row['cum_matched']:.0f}"
                    )

                if video_writer is not None:
                    annotated = self._draw_bboxes_on_frame(frame.copy(), detections)
                    video_writer.write(annotated)

                json_path = os.path.join(self.json_dir, f"frame_{frame_idx:04d}.json")
                with open(json_path, "w") as f:
                    json.dump(self._serialize(frame_result), f, indent=2)

                if csv_writer is not None:
                    per_frame: dict[str, float] = {}
                    for _proc in self.engine.processors.values():
                        if not _proc._frame_buffer:
                            continue
                        for _m in _proc._frame_buffer[-1].metrics:
                            per_frame[_m.key] = float(_m.data)
                    plate_texts = [
                        d.get("plate_text") or ""
                        for d in detections
                        if d.get("plate_text")
                    ]
                    csv_writer.writerow(
                        [
                            frame_idx,
                            loop_idx + 1,
                            round(frame_ts, 3),
                            len(detections),
                            per_frame.get("total_identifications", 0.0),
                            per_frame.get("matched_count", 0.0),
                            per_frame.get("unknown_count", 0.0),
                            per_frame.get("blacklist_matches", 0.0),
                            round(per_frame.get("match_confidence_avg", 0.0), 4),
                            "|".join(plate_texts),
                        ]
                    )

                if frame_idx % 30 == 0:
                    print(
                        f"[Loop {loop_idx + 1}/{self.loop_count}] "
                        f"Frame {frame_idx:4d} | dets: {len(detections):3d} "
                        f"| plates seen: {len(self.ocr._cache)}"
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
                        "cum_total": final_row["cum_total"],
                        "cum_matched": final_row["cum_matched"],
                        "cum_unknown": final_row["cum_unknown"],
                        "cum_blacklist": final_row["cum_blacklist"],
                        "cum_match_rate": final_row["cum_match_rate"],
                    },
                },
                f,
                indent=2,
            )
        print(f"\nFinal aggregation saved: {final_agg_path}")
        print("Final aggregation result:")
        pprint.pprint(final_serialized)

        # Per-window summary CSV
        summary_csv_path = os.path.join(self.json_dir, "agg", "agg_summary.csv")
        with open(summary_csv_path, "w", newline="") as f:
            sw = csv.writer(f)
            sw.writerow(
                [
                    "label",
                    "frame_idx",
                    "loop_idx",
                    "frame_ts",
                    "window_total",
                    "window_matched",
                    "window_unknown",
                    "window_blacklist",
                    "window_match_conf_avg",
                    "cum_total",
                    "cum_matched",
                    "cum_unknown",
                    "cum_blacklist",
                    "cum_match_rate",
                ]
            )
            for r in self._agg_rows:
                sw.writerow(
                    [
                        r["label"],
                        r["frame_idx"],
                        r["loop_idx"],
                        r["frame_ts"],
                        r["window_total"],
                        r["window_matched"],
                        r["window_unknown"],
                        r["window_blacklist"],
                        r["window_match_conf_avg"],
                        r["cum_total"],
                        r["cum_matched"],
                        r["cum_unknown"],
                        r["cum_blacklist"],
                        r["cum_match_rate"],
                    ]
                )
        print(f"Aggregation summary CSV: {summary_csv_path}")

        # Dump the final plate-text cache (all unique plates the OCR saw)
        plates_dump_path = os.path.join(self.json_dir, "agg", "plates_seen.json")
        plates_out = {
            str(tid): {
                "text": v["text"],
                "conf": round(v["conf"], 4),
                "last_frame": v["last_frame"],
            }
            for tid, v in self.ocr._cache.items()
        }
        with open(plates_dump_path, "w") as f:
            json.dump(plates_out, f, indent=2)
        print(f"Plates-seen dump: {plates_dump_path}  ({len(plates_out)} unique tracks)")

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
    BASE = Path(r"C:/Users/Sreenivasan/OneDrive/Desktop/matrice/LPR")
    processor = IdentityAnalyticsTestProcessor(
        manifest_name="license_plate_recognition",
        model_path=str(BASE / "license_plate_detector_v1.pt"),
        video_path=str(BASE / "combined.mp4"),
        max_frames=None,
        loop_count=1,
        json_dir=str(BASE / "output" / "jsons"),
        draw_bboxes=True,
        output_video_path=str(BASE / "output" / "combined_annotated.mp4"),
        csv_path=str(BASE / "output" / "lpr_per_frame.csv"),
        confidence_threshold=0.35,
    )
    processor.process_video()
