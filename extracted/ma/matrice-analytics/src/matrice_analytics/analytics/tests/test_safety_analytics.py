"""End-to-end PPE Safety analytics harness.

Two-stage detection:

  1. People YOLO (YOLO11m COCO) → person bboxes.
  2. Expand each person box by 25% → crop → run PPE YOLO on crop.
  3. Per-person dedupe: at most one Hardhat / Safety Vest / Gloves /
     Goggles (IoU≥0.5 merge for helmet/vest).
  4. AdvancedTracker (BYTETracker-like) on the person boxes → stable
     ``track_id`` per person. Every PPE detection inherits its person's
     ``track_id``.
  5. Feed shaped detections into AnalyticsEngine loaded from
     ``ppe_detection.yaml`` (SAFETY + VOLUME processors).
  6. Emit JSON (per-frame + 1-min agg), CSV (per-frame metrics),
     annotated MP4 (person + PPE boxes + legend).

Usage (from anywhere):
    python test_safety_ppe.py --video "C:/.../ppe-compliance.mp4"
"""

from __future__ import annotations

import argparse
import csv
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import cv2
import numpy as np

# ---------------------------------------------------------------------------
# Make local py_analytics source importable (take precedence over site-packages)
# ---------------------------------------------------------------------------
_PY_ANALYTICS_SRC = Path(
    r"C:/Users/Sreenivasan/OneDrive/Desktop/matrice/py_analytics/src"
)
if _PY_ANALYTICS_SRC.is_dir():
    sys.path.insert(0, str(_PY_ANALYTICS_SRC))

# Stub out internal 'matrice_common' so post_processing's optional use-case
# imports don't crash when that package isn't installed locally. We only
# touch the analytics engine, not those use-cases, so a no-op stub is safe.
import types as _types  # noqa: E402

for _stub_name in ("matrice_common", "matrice_common.session"):
    if _stub_name not in sys.modules:
        _mod = _types.ModuleType(_stub_name)
        if _stub_name.endswith(".session"):

            class _StubSession:  # noqa: D401
                """No-op Session stub (only used during imports we don't hit)."""

                def __init__(self, *a, **kw) -> None: ...

            _mod.Session = _StubSession
        sys.modules[_stub_name] = _mod

from matrice_analytics.analytics.engine import AnalyticsEngine  # noqa: E402
from matrice_analytics.analytics.schemas import StreamInfo  # noqa: E402
from matrice_analytics.post_processing.advanced_tracker.config import (  # noqa: E402
    TrackerConfig,
)
from matrice_analytics.post_processing.advanced_tracker.tracker import (  # noqa: E402
    AdvancedTracker,
)

from ultralytics import YOLO  # noqa: E402

# ---------------------------------------------------------------------------
# Config / constants (copied from ppe_test.py to preserve accuracy)
# ---------------------------------------------------------------------------

PPE_INDEX_TO_CATEGORY: Dict[int, str] = {
    0: "Hardhat",
    1: "Gloves",
    2: "Safety Vest",
    3: "Boots",
    4: "Goggles",
    5: "none",
    6: "Person",
    7: "NO-Hardhat",
    8: "NO-Goggles",
    9: "NO-Gloves",
    10: "NO-Boots",
}

ALLOWED_GEAR_LABELS = frozenset({"Hardhat", "Mask", "Safety Vest", "Gloves", "Goggles"})
CAPPED_GEAR_CATEGORIES = ("Hardhat", "Safety Vest", "Gloves", "Goggles")
VIOLATION_LABELS = frozenset({"NO-Hardhat", "NO-Goggles", "NO-Gloves", "NO-Boots"})
DEDUP_IOU_MERGE_THRESHOLD = 0.5
PPE_ROI_EXPAND_FACTOR = 1.25

PERSON_BOX_BGR = (255, 128, 0)
GEAR_COLORS_BGR = {
    "Hardhat": (0, 255, 255),
    "Mask": (255, 0, 255),
    "Safety Vest": (0, 200, 100),
    "Gloves": (0, 140, 255),
    "Goggles": (255, 180, 100),
    "NO-Hardhat": (0, 0, 255),
    "NO-Goggles": (0, 0, 255),
    "NO-Gloves": (0, 0, 255),
    "NO-Boots": (0, 0, 255),
}

DEFAULT_BASE = Path(r"C:/Users/Sreenivasan/OneDrive/Desktop/matrice/PPE detection")
DEFAULT_VIDEO = DEFAULT_BASE / "ppe-compliance.mp4"
DEFAULT_PPE_MODEL = DEFAULT_BASE / "ppe-monitoring-2.pt"
DEFAULT_PEOPLE_MODEL = str(DEFAULT_BASE / "people_counting_coco_kaggle_0.91_Y11m.pt")
DEFAULT_MANIFEST = (
    _PY_ANALYTICS_SRC
    / "matrice_analytics"
    / "analytics"
    / "config"
    / "ppe_detection.yaml"
)
DEFAULT_OUT_DIR = DEFAULT_BASE / "output"


# ---------------------------------------------------------------------------
# Geometry helpers (from ppe_test.py)
# ---------------------------------------------------------------------------


def _clip_xyxy(x1, y1, x2, y2, w, h) -> Tuple[int, int, int, int]:
    xi1 = max(0, min(w - 1, int(round(x1))))
    yi1 = max(0, min(h - 1, int(round(y1))))
    xi2 = max(xi1 + 1, min(w, int(round(x2))))
    yi2 = max(yi1 + 1, min(h, int(round(y2))))
    return xi1, yi1, xi2, yi2


def _expand_bbox(x1, y1, x2, y2, w, h, scale=PPE_ROI_EXPAND_FACTOR):
    bw = max(1, x2 - x1)
    bh = max(1, y2 - y1)
    cx = (x1 + x2) * 0.5
    cy = (y1 + y2) * 0.5
    nbw = bw * scale
    nbh = bh * scale
    return _clip_xyxy(cx - nbw / 2, cy - nbh / 2, cx + nbw / 2, cy + nbh / 2, w, h)


def _iou(a, b) -> float:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    ix1, iy1 = max(ax1, bx1), max(ay1, by1)
    ix2, iy2 = min(ax2, bx2), min(ay2, by2)
    iw, ih = max(0.0, ix2 - ix1), max(0.0, iy2 - iy1)
    inter = iw * ih
    if inter <= 0:
        return 0.0
    aa = max(0.0, ax2 - ax1) * max(0.0, ay2 - ay1)
    ba = max(0.0, bx2 - bx1) * max(0.0, by2 - by1)
    union = aa + ba - inter
    return inter / union if union > 0 else 0.0


def _merge_same_class_high_iou(items, iou_thresh):
    n = len(items)
    if n <= 1:
        return list(items)
    parent = list(range(n))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(n):
        for j in range(i + 1, n):
            if _iou(items[i][:4], items[j][:4]) >= iou_thresh:
                ri, rj = find(i), find(j)
                if ri != rj:
                    parent[rj] = ri

    groups: Dict[int, List[int]] = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)

    merged = []
    for idxs in groups.values():
        xs = [items[k] for k in idxs]
        x1 = min(t[0] for t in xs)
        y1 = min(t[1] for t in xs)
        x2 = max(t[2] for t in xs)
        y2 = max(t[3] for t in xs)
        best = max(xs, key=lambda t: t[4])
        merged.append((x1, y1, x2, y2, best[4], best[5]))
    return merged


def _dedupe_gear_for_person(raw_boxes, person_top_y):
    """Same dedupe rules as ppe_test.py."""
    by_cat: Dict[str, List[Tuple[float, float, float, float, float, int]]] = {}
    for cat, conf, ppe_cid, gx1, gy1, gx2, gy2 in raw_boxes:
        if cat not in CAPPED_GEAR_CATEGORIES:
            continue
        by_cat.setdefault(cat, []).append(
            (float(gx1), float(gy1), float(gx2), float(gy2), float(conf), int(ppe_cid))
        )

    out = []
    for cat in CAPPED_GEAR_CATEGORIES:
        items = by_cat.get(cat, [])
        if not items:
            continue
        if cat in ("Hardhat", "Safety Vest"):
            items = _merge_same_class_high_iou(items, DEDUP_IOU_MERGE_THRESHOLD)
            if len(items) > 1:
                if cat == "Safety Vest":
                    best = max(items, key=lambda t: t[4])
                else:
                    best = min(
                        items,
                        key=lambda t: (abs(t[1] - float(person_top_y)), -t[4]),
                    )
                items = [best]
        else:
            items = [max(items, key=lambda t: t[4])]

        x1, y1, x2, y2, conf, ppe_cid = items[0]
        out.append(
            {
                "category": cat,
                "confidence": float(conf),
                "ppe_cls_id": int(ppe_cid),
                "bounding_box": {
                    "xmin": int(round(x1)),
                    "ymin": int(round(y1)),
                    "xmax": int(round(x2)),
                    "ymax": int(round(y2)),
                },
            }
        )
    return out


def _person_class_id(model) -> int:
    names = getattr(model, "names", None) or getattr(
        getattr(model, "model", None), "names", {}
    )
    if not names:
        return 0
    for k, v in names.items():
        if str(v).strip().lower() == "person":
            try:
                return int(k)
            except (TypeError, ValueError):
                return 0
    return 0


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------


def _draw_frame(frame_bgr, people, gear, stats, frame_idx, agg_hint=""):
    out = frame_bgr.copy()
    font = cv2.FONT_HERSHEY_SIMPLEX

    def _bbi(bb):
        return (
            int(bb["xmin"]),
            int(bb["ymin"]),
            int(bb["xmax"]),
            int(bb["ymax"]),
        )

    for p in people:
        x1, y1, x2, y2 = _bbi(p["bounding_box"])
        cv2.rectangle(out, (x1, y1), (x2, y2), PERSON_BOX_BGR, 2)
        tid = p.get("track_id")
        label = f"person id={tid}" if tid is not None else "person"
        (tw, th), bl = cv2.getTextSize(label, font, 0.5, 1)
        cv2.rectangle(
            out, (x1, y1 - th - bl - 4), (x1 + tw + 4, y1), PERSON_BOX_BGR, -1
        )
        cv2.putText(
            out,
            label,
            (x1 + 2, y1 - bl - 2),
            font,
            0.5,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    for g in gear:
        x1, y1, x2, y2 = _bbi(g["bounding_box"])
        cat = g["category"]
        color = GEAR_COLORS_BGR.get(cat, (200, 200, 200))
        cv2.rectangle(out, (x1, y1), (x2, y2), color, 2)
        label = f"{cat} {g.get('confidence', 0):.2f}"
        (tw, th), bl = cv2.getTextSize(label, font, 0.45, 1)
        cv2.rectangle(out, (x1, y1 - th - bl - 4), (x1 + tw + 4, y1), color, -1)
        cv2.putText(
            out,
            label,
            (x1 + 2, y1 - bl - 2),
            font,
            0.45,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    # Legend (bottom-right)
    lines = [
        "PPE Safety Summary",
        f"Frame: {frame_idx}",
        f"Persons: {stats['total_persons']}",
        f"Compliant: {stats['compliant_count']}",
        f"Violations: {stats['violation_count']}",
        f"Compliance: {stats['compliance_pct']:.1f}%",
        f"Hardhat: {stats['hardhat_count']}  Vest: {stats['safety_vest_count']}",
    ]
    if agg_hint:
        lines.append(f"[{agg_hint}]")

    scale, thick, gap, pad = 0.52, 1, 22, 10
    max_tw = max(cv2.getTextSize(ln, font, scale, thick)[0][0] for ln in lines)
    panel_w = max_tw + pad * 2
    panel_h = pad * 2 + gap * len(lines)
    fh, fw = out.shape[:2]
    x0 = max(0, fw - panel_w - 12)
    y0 = max(0, fh - panel_h - 12)
    x1, y1 = x0 + panel_w, y0 + panel_h
    roi = out[y0:y1, x0:x1]
    if roi.size:
        blended = cv2.addWeighted(np.full_like(roi, (40, 40, 40)), 0.62, roi, 0.38, 0)
        out[y0:y1, x0:x1] = blended
    y = y0 + pad + 16
    for i, ln in enumerate(lines):
        col = (0, 220, 255) if i == 0 else (235, 235, 235)
        cv2.putText(out, ln, (x0 + pad, y), font, scale, col, thick, cv2.LINE_AA)
        y += gap
    return out


# ---------------------------------------------------------------------------
# Detection shaping for the SDK
# ---------------------------------------------------------------------------


def _shape_detections_for_sdk(
    tracked_persons: List[Dict[str, Any]],
    gear_per_person: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Build the flat detection list fed to AnalyticsEngine.process_frame.

    - Person detections keep their ``track_id`` from AdvancedTracker.
    - Each gear detection inherits its owning person's ``track_id``.
    """
    shaped: List[Dict[str, Any]] = []
    for p in tracked_persons:
        shaped.append(
            {
                "category": "person",
                "confidence": p.get("confidence", 0.0),
                "bounding_box": p["bounding_box"],
                "track_id": p.get("track_id"),
            }
        )
    index_to_tid = {i: p.get("track_id") for i, p in enumerate(tracked_persons)}
    for g in gear_per_person:
        pid = g.get("person_index")
        tid = index_to_tid.get(pid) if pid is not None else None
        shaped.append(
            {
                "category": g["category"],  # raw label; entity_mapping normalises
                "confidence": g.get("confidence", 0.0),
                "bounding_box": g["bounding_box"],
                "track_id": tid,
            }
        )
    return shaped


# ---------------------------------------------------------------------------
# Main run loop
# ---------------------------------------------------------------------------


def run(
    video_path: Path,
    people_model_path: str,
    ppe_model_path: Path,
    manifest_path: Path,
    out_dir: Path,
    *,
    people_conf: float = 0.35,
    ppe_conf: float = 0.25,
    max_frames: Optional[int] = None,
    display: bool = False,
    agg_interval_sec: float = 60.0,
    num_loops: int = 1,
) -> None:
    log = logging.getLogger("test_safety_ppe")
    out_dir.mkdir(parents=True, exist_ok=True)

    if not video_path.is_file():
        raise FileNotFoundError(video_path)
    if not ppe_model_path.is_file():
        raise FileNotFoundError(ppe_model_path)
    if not manifest_path.is_file():
        raise FileNotFoundError(manifest_path)

    log.info("Loading people model: %s", people_model_path)
    people_model = YOLO(str(people_model_path))
    log.info("Loading PPE model: %s", ppe_model_path)
    ppe_model = YOLO(str(ppe_model_path))

    person_cls = _person_class_id(people_model)
    log.info("People model person class id = %d", person_cls)

    # Tracker on persons
    tracker = AdvancedTracker(
        TrackerConfig(track_high_thresh=0.4, track_low_thresh=0.1, frame_rate=30),
        namespace="ppe_safety_persons",
    )

    # Engine
    stream_info = StreamInfo(
        camera_id="ppe_test_cam",
        camera_name="PPE Test Camera",
        app_deployment_id="dep_ppe_local",
        app_id="ppe_detection",
        application_name="PPE Detection",
        application_key_name="ppe_detection",
        application_version="1.0",
        location="Local Test",
    )
    engine = AnalyticsEngine(str(manifest_path), stream_info=stream_info)
    engine._agg_interval = float(agg_interval_sec)  # allow short windows for demo

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {video_path}")
    fps = float(cap.get(cv2.CAP_PROP_FPS) or 30.0)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    annotated_path = out_dir / "ppe_safety_annotated.mp4"
    csv_path = out_dir / "ppe_safety_per_frame.csv"
    frame_json_path = out_dir / "ppe_safety_frames.json"
    agg_json_path = out_dir / "ppe_safety_aggregations.json"

    writer = cv2.VideoWriter(
        str(annotated_path),
        cv2.VideoWriter_fourcc(*"mp4v"),
        fps,
        (width, height),
    )

    csv_file = csv_path.open("w", newline="", encoding="utf-8")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        [
            "frame_idx",
            "frame_ts",
            "total_persons",
            "compliant_count",
            "violation_count",
            "compliance_pct",
            "hardhat_count",
            "safety_vest_count",
            "gloves_count",
            "goggles_count",
            "mask_count",
            "entry_count",
            "current_occupancy",
        ]
    )

    frame_summaries: List[Dict[str, Any]] = []
    aggregations: List[Dict[str, Any]] = []

    frame_idx = 0
    latest_agg_hint = ""
    n_loops = max(1, int(num_loops))
    if n_loops > 1:
        log.info("Looping input video %d times for longer aggregation windows", n_loops)
    try:
        loop_done = False
        for loop_i in range(n_loops):
            if loop_done:
                break
            if loop_i > 0:
                # Rewind to start. frame_idx and frame_ts keep accumulating
                # so engine sees a continuously-growing timeline that
                # naturally rolls over the agg window.
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                log.info(
                    "Loop %d/%d  starting at frame_idx=%d  ts=%.2fs",
                    loop_i + 1,
                    n_loops,
                    frame_idx,
                    frame_idx / fps,
                )
            while cap.isOpened():
                ret, frame_bgr = cap.read()
                if not ret:
                    break
                h, w = frame_bgr.shape[:2]
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                frame_ts = frame_idx / fps

                # ── Stage 1: persons ────────────────────────────────────
                pres = people_model(frame_rgb, verbose=False, conf=people_conf)
                persons: List[Dict[str, Any]] = []
                if pres and pres[0].boxes is not None and len(pres[0].boxes):
                    for xyxy, conf, cls in zip(
                        pres[0].boxes.xyxy, pres[0].boxes.conf, pres[0].boxes.cls
                    ):
                        if int(cls.item()) != person_cls:
                            continue
                        x1, y1, x2, y2 = xyxy.tolist()
                        xi1, yi1, xi2, yi2 = _clip_xyxy(x1, y1, x2, y2, w, h)
                        persons.append(
                            {
                                "category": "person",
                                "confidence": float(conf.item()),
                                "bounding_box": {
                                    "xmin": xi1,
                                    "ymin": yi1,
                                    "xmax": xi2,
                                    "ymax": yi2,
                                },
                            }
                        )

                # ── Attach tracker IDs ─────────────────────────────────
                tracked_persons = tracker.update(persons) if persons else []

                # ── Stage 2: PPE per person (uses tracked boxes) ───────
                gear_all: List[Dict[str, Any]] = []
                for pi, person in enumerate(tracked_persons):
                    bb = person["bounding_box"]
                    xi1, yi1, xi2, yi2 = (
                        int(bb["xmin"]),
                        int(bb["ymin"]),
                        int(bb["xmax"]),
                        int(bb["ymax"]),
                    )
                    exi1, eyi1, exi2, eyi2 = _expand_bbox(xi1, yi1, xi2, yi2, w, h)
                    crop_bgr = frame_bgr[eyi1:eyi2, exi1:exi2]
                    if (
                        crop_bgr.size == 0
                        or crop_bgr.shape[0] < 8
                        or crop_bgr.shape[1] < 8
                    ):
                        continue
                    crop_rgb = cv2.cvtColor(crop_bgr, cv2.COLOR_BGR2RGB)
                    gres = ppe_model(crop_rgb, verbose=False, conf=ppe_conf)
                    if not gres or gres[0].boxes is None or len(gres[0].boxes) == 0:
                        continue
                    pb = gres[0].boxes
                    raw = []
                    violations_here: List[Dict[str, Any]] = []
                    for xyxy, cf, cl in zip(pb.xyxy, pb.conf, pb.cls):
                        cid = int(cl.item())
                        label = PPE_INDEX_TO_CATEGORY.get(cid, f"id_{cid}")
                        cx1, cy1, cx2, cy2 = xyxy.tolist()
                        gx1, gy1 = int(round(cx1)) + exi1, int(round(cy1)) + eyi1
                        gx2, gy2 = int(round(cx2)) + exi1, int(round(cy2)) + eyi1
                        gx1, gy1, gx2, gy2 = _clip_xyxy(gx1, gy1, gx2, gy2, w, h)
                        if label in ALLOWED_GEAR_LABELS:
                            raw.append(
                                (label, float(cf.item()), cid, gx1, gy1, gx2, gy2)
                            )
                        elif label in VIOLATION_LABELS:
                            violations_here.append(
                                {
                                    "category": label,
                                    "confidence": float(cf.item()),
                                    "ppe_cls_id": cid,
                                    "bounding_box": {
                                        "xmin": gx1,
                                        "ymin": gy1,
                                        "xmax": gx2,
                                        "ymax": gy2,
                                    },
                                    "person_index": pi,
                                }
                            )
                    deduped = _dedupe_gear_for_person(raw, yi1)
                    # optional Mask
                    mask_raw = [t for t in raw if t[0] == "Mask"]
                    if mask_raw:
                        _c, mconf, mid_, mx1, my1, mx2, my2 = max(
                            mask_raw, key=lambda t: t[1]
                        )
                        deduped.append(
                            {
                                "category": "Mask",
                                "confidence": float(mconf),
                                "ppe_cls_id": int(mid_),
                                "bounding_box": {
                                    "xmin": int(mx1),
                                    "ymin": int(my1),
                                    "xmax": int(mx2),
                                    "ymax": int(my2),
                                },
                            }
                        )
                    for g in deduped:
                        g = dict(g)
                        g["person_index"] = pi
                        gear_all.append(g)
                    gear_all.extend(violations_here)

                # ── Feed engine ────────────────────────────────────────
                detections = _shape_detections_for_sdk(tracked_persons, gear_all)
                engine.process_frame(detections, frame_ts, str(frame_idx))

                # Pull RAW per-frame metrics from each processor's frame buffer.
                # We deliberately bypass `business_analytics` here because the
                # base processor cumulates any agg_type=sum metric into running
                # totals (entry_count-style behavior).  For a per-frame snapshot
                # CSV/JSON we want the unsummed values straight from
                # _compute_frame_metrics.
                per_frame_metrics: Dict[str, float] = {}
                for _cat, _proc in engine.processors.items():
                    if not _proc._frame_buffer:
                        continue
                    for _m in _proc._frame_buffer[-1].metrics:
                        per_frame_metrics[_m.key] = float(_m.data)

                stats = {
                    "total_persons": int(per_frame_metrics.get("total_persons", 0)),
                    "compliant_count": int(per_frame_metrics.get("compliant_count", 0)),
                    "violation_count": int(per_frame_metrics.get("violation_count", 0)),
                    "compliance_pct": float(
                        per_frame_metrics.get("compliance_pct", 0.0)
                    ),
                    "hardhat_count": int(per_frame_metrics.get("hardhat_count", 0)),
                    "safety_vest_count": int(
                        per_frame_metrics.get("safety_vest_count", 0)
                    ),
                    "gloves_count": int(per_frame_metrics.get("gloves_count", 0)),
                    "goggles_count": int(per_frame_metrics.get("goggles_count", 0)),
                    "mask_count": int(per_frame_metrics.get("mask_count", 0)),
                    "entry_count": int(per_frame_metrics.get("entry_count", 0)),
                    "current_occupancy": int(
                        per_frame_metrics.get("current_occupancy", 0)
                    ),
                }

                # ── Aggregate when the window rolls over ───────────────
                if engine.should_aggregate(frame_ts):
                    agg = engine.aggregate().model_dump(by_alias=True)
                    aggregations.append({"frame_idx_at_agg": frame_idx, **agg})
                    latest_agg_hint = (
                        f"agg@f{frame_idx}: "
                        f"cpl={_get_metric(agg, 'compliance_pct'):.1f}% "
                        f"vio={_get_metric(agg, 'violation_count'):.0f}"
                    )

                # ── Output ─────────────────────────────────────────────
                csv_writer.writerow(
                    [
                        frame_idx,
                        f"{frame_ts:.3f}",
                        *[
                            stats[k]
                            for k in [
                                "total_persons",
                                "compliant_count",
                                "violation_count",
                                "compliance_pct",
                                "hardhat_count",
                                "safety_vest_count",
                                "gloves_count",
                                "goggles_count",
                                "mask_count",
                                "entry_count",
                                "current_occupancy",
                            ]
                        ],
                    ]
                )
                frame_summaries.append(
                    {
                        "frame_idx": frame_idx,
                        "frame_ts": frame_ts,
                        "stats": stats,
                        "person_track_ids": [
                            p.get("track_id") for p in tracked_persons
                        ],
                        "n_gear": len(gear_all),
                    }
                )

                vis = _draw_frame(
                    frame_bgr,
                    tracked_persons,
                    gear_all,
                    stats,
                    frame_idx,
                    latest_agg_hint,
                )
                writer.write(vis)
                if display:
                    cv2.imshow("ppe_safety", vis)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        loop_done = True
                        break

                frame_idx += 1
                if frame_idx % 30 == 0:
                    log.info(
                        "frame %d  persons=%d  cpl=%d  vio=%d  cpl_pct=%.1f",
                        frame_idx,
                        stats["total_persons"],
                        stats["compliant_count"],
                        stats["violation_count"],
                        stats["compliance_pct"],
                    )
                if max_frames is not None and frame_idx >= max_frames:
                    loop_done = True
                    break

        # Final aggregation at end of video
        final_agg = engine.aggregate().model_dump(by_alias=True)
        aggregations.append({"frame_idx_at_agg": frame_idx, "final": True, **final_agg})
        log.info(
            "FINAL agg: cpl=%.1f%% vio=%.0f persons=%.0f",
            _get_metric(final_agg, "compliance_pct"),
            _get_metric(final_agg, "violation_count"),
            _get_metric(final_agg, "total_persons"),
        )
    finally:
        cap.release()
        writer.release()
        csv_file.close()
        if display:
            cv2.destroyAllWindows()

    frame_json_path.write_text(
        json.dumps({"frames": frame_summaries}, indent=2), encoding="utf-8"
    )
    agg_json_path.write_text(
        json.dumps({"aggregations": aggregations}, indent=2), encoding="utf-8"
    )
    logging.getLogger("test_safety_ppe").info(
        "Done. Outputs:\n  video: %s\n  csv  : %s\n  frames: %s\n  aggs : %s",
        annotated_path,
        csv_path,
        frame_json_path,
        agg_json_path,
    )


def _get_metric(agg: Dict[str, Any], key: str) -> float:
    for m in agg.get("metrics", []):
        if m.get("key") == key:
            try:
                return float(m.get("data", 0))
            except (TypeError, ValueError):
                return 0.0
    return 0.0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", type=Path, default=DEFAULT_VIDEO)
    ap.add_argument("--people-model", type=str, default=DEFAULT_PEOPLE_MODEL)
    ap.add_argument("--ppe-model", type=Path, default=DEFAULT_PPE_MODEL)
    ap.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--people-conf", type=float, default=0.35)
    ap.add_argument("--ppe-conf", type=float, default=0.25)
    ap.add_argument("--max-frames", type=int, default=None)
    ap.add_argument("--display", action="store_true")
    ap.add_argument(
        "--agg-interval-sec",
        type=float,
        default=60.0,
        help="Seconds between 1-min aggregation triggers (shorten for demos).",
    )
    ap.add_argument(
        "--num-loops",
        type=int,
        default=1,
        help="Loop the input video N times (useful when video is shorter than agg window).",
    )
    ap.add_argument("--log-level", default="INFO")
    args = ap.parse_args()

    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(levelname)s:%(name)s:%(message)s",
        force=True,
    )

    # Quiet ultralytics noise
    os.environ.setdefault("YOLO_VERBOSE", "False")

    run(
        args.video,
        args.people_model,
        args.ppe_model,
        args.manifest,
        args.out_dir,
        people_conf=args.people_conf,
        ppe_conf=args.ppe_conf,
        max_frames=args.max_frames,
        display=args.display,
        agg_interval_sec=args.agg_interval_sec,
        num_loops=args.num_loops,
    )


if __name__ == "__main__":
    main()
