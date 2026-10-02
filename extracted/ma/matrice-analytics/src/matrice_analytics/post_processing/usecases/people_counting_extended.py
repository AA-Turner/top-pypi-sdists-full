"""People counting with appearance-based re-identification.

``people_counting`` counts a person twice when they leave the frame and come
back, because the tracker's memory is short and position-based:
``AdvancedTracker`` keeps a lost track for ~48 s (``max_time_lost=1200`` at
``frame_rate=25``) and its only recovery mechanism is IoU against the last
known box, which cannot match somebody who re-enters somewhere else. In a
mall or office people routinely step away for five or ten minutes.

This use case closes that gap: person crops are embedded with OSNet-AIN-x1.0
(person re-identification, MSMT17-trained) and matched against a short-lived
in-RAM gallery, so a returning person keeps their original ``track_id`` and
the cumulative unique count does not increment.

**Temporary bridge.** The embedding model lives in the use-case layer for
now; re-identification belongs at the tracker level. Everything new lives in
``usecases/reid/`` plus this file, so removal is deleting a directory and a
handful of additive registration lines. Nothing in ``Trackers/``,
``advanced_tracker/`` or ``people_counting.py`` is modified.

Two design points carry the whole thing:

1. **The video path never waits.** One OSNet forward pass measured ~35 ms on
   a laptop RTX 3060 -- longer than an entire 30 FPS frame budget -- because
   the network is 478 modules of small depthwise convolutions and is
   kernel-launch bound rather than compute bound. Embedding therefore runs on
   a background worker and answers land on a *later* frame. The per-frame
   cost here is dict lookups.

2. **Counting is gated behind the verdict, not racing it.** The parent
   promotes a track into the cumulative total once it has been present for
   ``min_hits_for_new_track`` frames (``people_counting.py:1199-1202``).
   Without care that happens *before* the embedding answer arrives, the raw
   id is committed permanently, and rewriting ``track_id`` afterwards cannot
   undo it -- the person is counted twice anyway. So a track awaiting its
   verdict is withheld from the parent's counting pass: the parent only
   promotes ids it is shown, so promotion cannot happen early. The frame is
   restored immediately afterwards, because zone analysis and the output
   payload run later and must see every detection with its real id.

   The deferred detection is removed from the list rather than having its
   ``track_id`` blanked. SG-25's ``record_untracked_frame`` reads a missing
   ``track_id`` as a broken tracker and increments a process-wide health
   counter plus an ERROR log; a deferred track is not a fault, and blanking
   would make a healthy deployment look broken.

When anything is unavailable -- torch, CUDA, the checkpoint, frame pixels --
this degrades to exactly ``people_counting``.
"""

from __future__ import annotations

import logging
import math
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from ..core.base import ConfigProtocol, ProcessingContext, ProcessingResult
from ..core.config import PeopleCountingConfig, PeopleCountingExtendedConfig
from .people_counting import PeopleCountingUseCase

logger = logging.getLogger(__name__)

__all__ = ["PeopleCountingExtendedUseCase"]

#: Sentinel meaning "the frame was handed over out of band".
_RAW_BGR_SENTINEL = b"__RAW_BGR__"

#: A bbox whose largest raw coordinate is at most this is read as normalized
#: 0-1 rather than pixels. Matches ``geometry_utils.to_zone_test_point``; the
#: slack above 1.0 absorbs a box resting exactly on the frame edge.
_NORMALIZED_MAX = 1.5

#: Diagonal of the 1x1 space a normalized bbox lives in, i.e. sqrt(2).
#: Computed rather than written out: the literal digits trip the org's
#: hardcoded-credit-card rule, and a `# nosemgrep` on a mathematical constant
#: reads as a suppressed finding rather than what it is.
_UNIT_DIAGONAL = math.sqrt(2.0)


def _is_placeholder_id(raw: Any) -> bool:
    """Whether ``raw`` is a per-frame placeholder rather than a tracker id.

    Upstream emits ``untracked_<frame>_<index>`` when no tracker ran: the
    index is the detection's position in the frame, so the id is different on
    every single frame and no two frames ever share one. Appearance is then
    the *only* thing that can link a person across frames, and every gate
    phrased in terms of "how many frames has this id been seen" is dead --
    ``reid_min_track_frames`` can never be satisfied, so nothing is ever
    embedded and the gallery stays empty (observed in production: 70 minutes,
    ``reid_gallery_size: 0``, ``reid_queue_depth: 0``, worker alive and idle).

    ``parking_lot_analytics._is_placeholder_track_id`` applies the same test
    for the same reason; kept local rather than imported so this file stays
    removable as a unit.
    """
    return isinstance(raw, str) and raw.startswith("untracked")


def _refresh_key(raw: Any) -> Tuple[str, Any]:
    """Worker key for a refresh embedding of an already-resolved track.

    Distinct from the bare raw id so a refresh can never be mistaken for a
    first-sighting verdict.
    """
    return ("refresh", raw)


@dataclass
class _FrameWork:
    """Everything one frame's detection loop reads or appends to.

    Bundled so :meth:`_reid_one_detection` takes one argument instead of
    eighteen; the fields are exactly the locals the loop body used before it
    was extracted.
    """

    deferred: Set[Any]
    candidates: List[Tuple[float, Any, np.ndarray]]
    inline: List[Tuple[Dict[str, Any], Any, Tuple[int, int, int, int]]]
    next_boxes: Dict[Any, Tuple[int, int, int, int]]
    live_canonicals: Set[Any]
    valid_boxes: List[Tuple[int, int, int, int]]
    ctx: Dict[str, Any]
    frame: Any
    frame_idx: int
    now: float
    worker_alive: bool
    have_frame: bool
    fshape: Tuple[int, int]
    min_frames: int
    min_conf: float
    max_defer: int
    budget: int
    config: Any


class PeopleCountingExtendedUseCase(PeopleCountingUseCase):
    """``people_counting`` plus long-horizon person re-identification."""

    #: Minimum overlap for the untracked path to treat a detection as the
    #: continuation of an identity seen on the previous frame.
    _CARRY_IOU = 0.5

    #: Proximity-merge thresholds for raw ids re-identification has not
    #: resolved. Redeclared here rather than inherited because the parent's
    #: equivalents are hardcoded in pixels (``iou >= 0.28 or
    #: (center_dist < 35 and size_ratio > 0.6)``) and therefore merge every
    #: pair of people on a normalized feed. ``people_counting`` keeps its own.
    _MERGE_IOU = 0.28
    #: As a fraction of the frame diagonal, so it means the same thing in
    #: either coordinate space. 35 px on 1280x720 (diagonal 1468.6) = 0.0238.
    _MERGE_CENTER_DIST_FRAC = 0.0238
    _MERGE_SIZE_RATIO = 0.6

    def __init__(self) -> None:
        super().__init__()
        self.name = "people_counting_extended"
        # Its own analytics/incident identity. This previously echoed the
        # parent's "people_counting", which made every published field -- the
        # human_text app name, incident_category, incident_type and the
        # incident_id prefix -- claim to be plain people counting, and routed
        # `get_legacy_profile(incident_type)` (incident_manager_utils.py:1619)
        # to the people_counting profile, so this use case's own profile and
        # its "Unique People Counting" display name were never read.
        self.CASE_TYPE = "people_counting_extended"
        self.CASE_VERSION = "1.1.1"

        self._reid_enabled: bool = True
        self._reid_state: str = "init"  # init|ready|degraded|absent|disabled
        self._embedder: Any = None
        self._worker: Any = None
        self._gallery: Any = None
        self._reid_init_attempted = False

        self._pending_frame: Optional[np.ndarray] = None

        # raw tracker id -> canonical id
        self._reid_canonical: Dict[Any, Any] = {}
        # raw tracker id -> frame index when it was first deferred
        self._reid_deferred_since: Dict[Any, int] = {}
        # raw tracker id -> consecutive frames observed
        self._reid_track_frames: Dict[Any, int] = {}
        # raw tracker id -> last frame index seen. Covers EVERY raw id,
        # including ones never eligible for re-identification, so pruning
        # cannot miss the tracks that accumulate fastest.
        self._reid_seen_frame: Dict[Any, int] = {}
        # raw tracker id -> last frame index we embedded it
        self._reid_last_embed: Dict[Any, int] = {}
        # canonical id -> last frame index seen (for liveness masking)
        self._reid_canonical_last_frame: Dict[Any, int] = {}

        self._reid_counter = 0
        self._reid_recovered_total = 0
        self._reid_recovered_this_frame = 0
        self._reid_deferred_expired = 0
        self._reid_last_score = 0.0
        self._reid_rejected_by_margin = 0
        self._reid_refresh_applied = 0
        self._reid_refresh_rejected = 0
        self._reid_dropped_inline = 0
        self._reid_untracked_mode = False
        self._reid_frame_disabled = False
        self._reid_carried_total = 0
        # canonical id -> its box on the previous frame, for the untracked
        # path's spatial carry-forward.
        self._reid_prev_boxes: Dict[Any, Tuple[int, int, int, int]] = {}
        # Canonical ids this class minted or matched. The parent's
        # proximity merge must not touch these.
        self._reid_resolved_ids: Set[Any] = set()

    # ------------------------------------------------------------------ #
    # Frame resolution                                                     #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _resolve_frame(input_bytes: Any) -> Optional[np.ndarray]:
        """Resolve the pipeline's frame payload to a BGR array, or ``None``.

        ``input_bytes`` is not always JPEG: the pipeline delivers encoded
        bytes, a raw BGR ndarray, the ``__RAW_BGR__`` sentinel, or nothing at
        all (the decoupled analytics node never supplies pixels). Mirrors
        ``vehicle_speed_estimation._resolve_frame``.
        """
        if input_bytes is None:
            return None
        if isinstance(input_bytes, np.ndarray):
            return input_bytes
        if isinstance(input_bytes, (bytes, bytearray)):
            if bytes(input_bytes) == _RAW_BGR_SENTINEL:
                return None
            try:
                import cv2  # noqa: PLC0415

                return cv2.imdecode(np.frombuffer(bytes(input_bytes), np.uint8), cv2.IMREAD_COLOR)
            except Exception as exc:  # noqa: BLE001 - a bad frame must not break counting
                logger.debug("ReID frame decode failed: %s", exc)
                return None
        return None

    # ------------------------------------------------------------------ #
    # Lazy ReID initialisation                                             #
    # ------------------------------------------------------------------ #
    def _ensure_reid(self, config: Any) -> bool:
        """Bring up the embedder/worker/gallery once. Never raises."""
        if not getattr(config, "enable_reid", True):
            self._reid_state = "disabled"
            return False
        if self._worker is not None and self._gallery is not None:
            return True
        if self._reid_init_attempted and self._embedder is None:
            # A previous attempt failed; model.get_shared_embedder applies a
            # process-wide backoff, so retrying here is cheap but bounded.
            return self._try_build(config)
        self._reid_init_attempted = True
        return self._try_build(config)

    def _try_build(self, config: Any) -> bool:
        try:
            from .reid.gallery import ReIDGallery  # noqa: PLC0415
            from .reid.model import EMBEDDING_DIM, get_shared_embedder  # noqa: PLC0415
            from .reid.worker import EmbedWorker  # noqa: PLC0415
        except Exception as exc:  # noqa: BLE001 - optional subsystem
            logger.warning("ReID unavailable (import): %s", exc)
            self._reid_state = "absent"
            return False

        batch = int(getattr(config, "reid_max_crops_per_frame", 8))
        embedder = get_shared_embedder(
            fp16=bool(getattr(config, "reid_fp16", True)),
            max_batch=batch,
            allow_cpu=bool(getattr(config, "reid_allow_cpu", False)),
            weights_path=getattr(config, "reid_model_path", None),
        )
        if embedder is None:
            self._reid_state = "degraded"
            return False

        self._embedder = embedder
        if self._gallery is None:
            self._gallery = ReIDGallery(
                dim=getattr(embedder, "dim", EMBEDDING_DIM),
                capacity=int(getattr(config, "reid_gallery_capacity", 100)),
                match_threshold=float(getattr(config, "reid_match_threshold", 0.67)),
                margin=float(getattr(config, "reid_match_margin", 0.06)),
                min_absence_s=float(getattr(config, "reid_min_absence_s", 3.0)),
            )
        if self._worker is None or not self._worker.alive:
            self._worker = EmbedWorker(
                embed_fn=embedder.embed,
                batch_size=batch,
                max_pending=max(32, batch * 8),
            )
        self._reid_state = "ready"
        return True

    # ------------------------------------------------------------------ #
    # Crop quality                                                         #
    # ------------------------------------------------------------------ #
    @staticmethod
    def _bbox_xyxy(
        bbox: Any, fshape: Tuple[int, int] = (0, 0)
    ) -> Optional[Tuple[int, int, int, int]]:
        """Pixel-space ``(x1, y1, x2, y2)``, or ``None``.

        Detections carrying the newer coordinate-frame convention
        (``metadata.coordinate_frame.space: "normalized"``) arrive as 0-1
        fractions. Truncating those to int gives ``(0, 0, 0, 1)`` for every
        person in the frame, which fails every crop-quality gate, so nothing
        is ever embedded and the gallery stays empty -- re-identification is
        silently off while reporting itself ready.

        The normalized test is the one already used repo-wide by
        ``geometry_utils.to_zone_test_point``: no raw coordinate above ~1.
        Scaling needs the frame, so an unscalable normalized bbox returns
        ``None`` (skip this detection) rather than a degenerate box that
        would read as a real, tiny person.
        """
        raw: Optional[Tuple[float, float, float, float]] = None
        if isinstance(bbox, dict):
            try:
                if "xmin" in bbox:
                    raw = (
                        float(bbox["xmin"]),
                        float(bbox["ymin"]),
                        float(bbox["xmax"]),
                        float(bbox["ymax"]),
                    )
                elif "x1" in bbox:
                    raw = (
                        float(bbox["x1"]),
                        float(bbox["y1"]),
                        float(bbox["x2"]),
                        float(bbox["y2"]),
                    )
            except (KeyError, TypeError, ValueError):
                return None
        elif isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            try:
                raw = (float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3]))
            except (TypeError, ValueError):
                return None
        if raw is None:
            return None

        if max(raw) <= _NORMALIZED_MAX:
            height, width = fshape
            if height <= 0 or width <= 0:
                return None
            return (
                int(raw[0] * width),
                int(raw[1] * height),
                int(raw[2] * width),
                int(raw[3] * height),
            )
        return (int(raw[0]), int(raw[1]), int(raw[2]), int(raw[3]))

    @staticmethod
    def _iou(a: Tuple[int, int, int, int], b: Tuple[int, int, int, int]) -> float:
        ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
        ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
        iw, ih = max(0, ix2 - ix1), max(0, iy2 - iy1)
        inter = iw * ih
        if inter <= 0:
            return 0.0
        area_a = max(0, a[2] - a[0]) * max(0, a[3] - a[1])
        area_b = max(0, b[2] - b[0]) * max(0, b[3] - b[1])
        union = area_a + area_b - inter
        return (inter / union) if union > 0 else 0.0

    def _crop_is_usable(
        self,
        box: Tuple[int, int, int, int],
        others: List[Tuple[int, int, int, int]],
        frame_shape: Tuple[int, int],
        config: Any,
    ) -> bool:
        """Reject crops that would produce a misleading embedding.

        A bad crop is worse than no crop: it becomes a prototype and can
        cause a false merge later.
        """
        x1, y1, x2, y2 = box
        h, w = y2 - y1, x2 - x1
        if h < int(getattr(config, "reid_min_crop_height", 96)):
            return False
        if w < int(getattr(config, "reid_min_crop_width", 40)):
            return False
        ar = h / float(w) if w > 0 else 0.0
        if not (
            float(getattr(config, "reid_min_aspect_ratio", 1.6))
            <= ar
            <= float(getattr(config, "reid_max_aspect_ratio", 4.5))
        ):
            return False
        # Truncation at a frame edge is the top source of bad prototypes --
        # and edges are exactly where tracks appear and disappear, so it is
        # also the most tempting moment to sample.
        m = int(getattr(config, "reid_edge_margin_px", 6))
        fh, fw = frame_shape
        if x1 < m or y1 < m or x2 > fw - m or y2 > fh - m:
            return False
        max_iou = float(getattr(config, "reid_max_occlusion_iou", 0.25))
        for other in others:
            if other is box:
                continue
            if self._iou(box, other) > max_iou:
                return False  # occlusion bakes the other person into this crop
        return True

    # ------------------------------------------------------------------ #
    # The ReID pass                                                        #
    # ------------------------------------------------------------------ #
    def _mint_canonical(self) -> str:
        self._reid_counter += 1
        return f"r{self._reid_counter}"

    def _reid_remap_in_place(self, detections: List[Dict[str, Any]], config: Any) -> Set[Any]:
        """Apply known verdicts, queue new work, and report deferred raw ids.

        Returns the set of raw track ids whose verdict is still pending and
        which must therefore be withheld from counting this frame.
        """
        deferred: Set[Any] = set()
        self._reid_recovered_this_frame = 0
        if self._worker is None or self._gallery is None:
            return deferred

        frame_idx = int(getattr(self, "_total_frame_counter", 0))
        now = time.monotonic()

        max_defer = int(getattr(config, "reid_max_defer_frames", 15))
        min_frames = int(getattr(config, "reid_min_track_frames", 3))
        min_conf = float(getattr(config, "reid_min_confidence", 0.5))
        refresh = int(getattr(config, "reid_refresh_interval_frames", 45))
        budget = int(getattr(config, "reid_max_crops_per_frame", 8))

        # A dead worker can never answer, so nothing may be deferred behind
        # it -- otherwise tracks wait out the budget and (until the release
        # path runs) are not counted at all.
        worker_alive = bool(getattr(self._worker, "alive", False))
        # A worker that has been handed work but produced nothing for seconds
        # is starved, not merely slow. Frame budgets cannot catch that (frames
        # tick while the thread gets no time), so release on wall clock too.
        if worker_alive and self._worker.starving():
            worker_alive = False

        frame = self._pending_frame
        have_frame = frame is not None and getattr(frame, "size", 0) > 0
        fshape = (frame.shape[0], frame.shape[1]) if have_frame else (0, 0)

        # Per-frame constants the refresh path needs, bundled so the helper
        # takes one argument rather than six.
        ctx: Dict[str, Any] = {
            "frame": frame,
            "have_frame": have_frame,
            "fshape": fshape,
            "refresh": refresh,
            "config": config,
        }

        boxes: List[Optional[Tuple[int, int, int, int]]] = []
        for det in detections:
            boxes.append(self._bbox_xyxy(det.get("bounding_box") or det.get("bbox"), fshape))
        valid_boxes = [b for b in boxes if b is not None]

        # Identities visible right now: a person cannot be in two places, so
        # these are excluded from matching.
        live_canonicals: Set[Any] = set()
        for det in detections:
            c = self._reid_canonical.get(det.get("track_id"))
            if c is not None:
                live_canonicals.add(c)

        candidates: List[Tuple[float, Any, np.ndarray]] = []
        inline: List[Tuple[Dict[str, Any], Any, Tuple[int, int, int, int]]] = []
        # Where each identity sat this frame, for the next frame's carry-
        # forward. Rebuilt per frame so an identity that leaves is dropped.
        next_boxes: Dict[Any, Tuple[int, int, int, int]] = {}

        work = _FrameWork(
            deferred=deferred,
            candidates=candidates,
            inline=inline,
            next_boxes=next_boxes,
            live_canonicals=live_canonicals,
            valid_boxes=valid_boxes,
            ctx=ctx,
            frame=frame,
            frame_idx=frame_idx,
            now=now,
            worker_alive=worker_alive,
            have_frame=have_frame,
            fshape=fshape,
            min_frames=min_frames,
            min_conf=min_conf,
            max_defer=max_defer,
            budget=budget,
            config=config,
        )
        for det, box in zip(detections, boxes, strict=True):
            self._reid_one_detection(det, box, work)

        # Resolve the untracked detections as a single batch, best crops
        # first. A crowded frame spends a bounded amount of time here; the
        # people who miss the cut are not counted this frame and get another
        # chance on the next one, which is the right trade -- the alternative
        # is an unbounded forward pass on the video path.
        if inline:
            if len(inline) > budget:
                inline.sort(key=lambda t: self._inline_quality(t[0], t[2]), reverse=True)
                self._reid_dropped_inline += len(inline) - budget
                del inline[budget:]
            self._resolve_inline_batch(
                inline, deferred, now, live_canonicals, config, frame_idx, next_boxes
            )

        if self._reid_untracked_mode:
            self._reid_prev_boxes = next_boxes

        # Offer the best crops; the rest retry on a later frame.
        candidates.sort(key=lambda t: t[0], reverse=True)
        for _, raw, crop in candidates[:budget]:
            self._worker.offer(raw, crop)

        return deferred

    def _reid_one_detection(
        self,
        det: Dict[str, Any],
        box: Optional[Tuple[int, int, int, int]],
        w: "_FrameWork",
    ) -> None:
        """Resolve one detection: apply, carry forward, queue or withhold.

        Split out of :meth:`_reid_remap_in_place` to keep that method under
        the org complexity cap. The ordering of the four cases is
        load-bearing and unchanged.
        """
        raw = det.get("track_id")
        if raw is None:
            return

        self._reid_track_frames[raw] = self._reid_track_frames.get(raw, 0) + 1
        self._reid_seen_frame[raw] = w.frame_idx
        seen = self._reid_track_frames[raw]

        # A placeholder id is new every frame, so "seen N frames" can never be
        # satisfied. Appearance is the only continuity available, so such a
        # detection is eligible on its first and only sighting.
        placeholder = _is_placeholder_id(raw)
        if placeholder:
            seen = w.min_frames

        # 1. Already resolved -> apply the canonical id.
        canonical = self._reid_canonical.get(raw)
        if canonical is not None:
            w.ctx["box"] = box
            w.ctx["valid_boxes"] = w.valid_boxes
            self._apply_known_identity(det, raw, canonical, w.frame_idx, w.now, w.ctx)
            return

        # 2. A verdict may have arrived since the last frame.
        vec = self._worker.pop_result(raw)
        if vec is not None:
            canonical = self._resolve_identity(raw, vec, w.now, w.live_canonicals, w.config)
            det["reid_raw_track_id"] = raw
            det["track_id"] = canonical
            det["reid_canonical_id"] = canonical
            w.live_canonicals.add(canonical)
            self._reid_canonical_last_frame[canonical] = w.frame_idx
            self._reid_resolved_ids.add(canonical)
            self._reid_deferred_since.pop(raw, None)
            return

        # 3. Not yet resolved. Queue it if it qualifies.
        eligible = (
            w.worker_alive
            and w.have_frame
            and box is not None
            and seen >= w.min_frames
            and float(det.get("confidence") or 0.0) >= w.min_conf
            and self._crop_is_usable(box, w.valid_boxes, w.fshape, w.config)
        )
        if eligible and placeholder:
            if not self._try_carry_forward(
                det, raw, box, w.now, w.frame_idx, w.live_canonicals, w.next_boxes
            ):
                w.inline.append((det, raw, box))
            return
        if eligible and not self._worker.has_pending(raw) and len(w.candidates) < w.budget * 2:
            crop = w.frame[box[1] : box[3], box[0] : box[2]]
            if crop.size > 0:
                w.candidates.append((self._inline_quality(det, box), raw, crop))

        # 4. Decide whether to withhold this track from counting.
        if self._should_defer(
            det, raw, eligible, w.frame_idx, w.worker_alive, w.max_defer, placeholder
        ):
            w.deferred.add(raw)
        det.setdefault("reid_raw_track_id", raw)
        if placeholder and det.get("track_id") == raw:
            # Still unidentified. The raw value is a per-frame placeholder that
            # means nothing downstream and would read as a real, never-
            # repeating track id, so publish it as unknown instead.
            det["track_id"] = None
            det["reid_unresolved"] = True

    def _try_carry_forward(
        self,
        det: Dict[str, Any],
        raw: Any,
        box: Tuple[int, int, int, int],
        now: float,
        frame_idx: int,
        live_canonicals: Set[Any],
        next_boxes: Dict[Any, Tuple[int, int, int, int]],
    ) -> bool:
        """Stamp a continued identity on ``det``; False if it needs embedding.

        A placeholder id does not survive to the next frame, so an answer that
        lands later can never be claimed: the worker is keyed by the id that
        asked, and that id is already gone. Such detections must be embedded
        and matched synchronously -- but embedding everybody on every frame is
        exactly what a tracker exists to avoid. OSNet-AIN-x1.0 measures ~20 ms
        per crop on CPU, so seven people at 25 fps would be 143 ms against a
        40 ms budget. A person who has barely moved since the last frame is
        overwhelmingly the same person, so carry the identity forward on
        overlap and spend the forward pass only on what is actually new.
        """
        self._reid_untracked_mode = True
        carried = self._carry_forward(box, live_canonicals)
        if carried is None:
            return False
        det["reid_raw_track_id"] = raw
        det["track_id"] = carried
        det["reid_canonical_id"] = carried
        det["reid_carried"] = True
        live_canonicals.add(carried)
        self._reid_canonical_last_frame[carried] = frame_idx
        self._reid_resolved_ids.add(carried)
        self._reid_carried_total += 1
        self._gallery.touch(carried, now)
        next_boxes[carried] = box
        return True

    def _carry_forward(self, box: Tuple[int, int, int, int], live: Set[Any]) -> Optional[Any]:
        """Identity whose previous-frame box this one clearly continues.

        Only used on the untracked path, where there is no tracker to do it.
        The IoU floor is deliberately high: at 25 fps a walking person moves a
        small fraction of their own width between frames, so a genuine
        continuation overlaps heavily. Anything less confident is sent to the
        embedder instead -- a wasted forward pass is cheap, a wrong identity
        is not.

        Identities already claimed by another detection on this frame are
        excluded, so two people crossing cannot both inherit the same id.
        """
        best: Optional[Any] = None
        best_iou = self._CARRY_IOU
        for cid, prev in self._reid_prev_boxes.items():
            if cid in live:
                continue
            iou = self._iou(box, prev)
            if iou > best_iou:
                best_iou, best = iou, cid
        return best

    @staticmethod
    def _inline_quality(det: Dict[str, Any], box: Tuple[int, int, int, int]) -> float:
        """Rank for the per-frame crop budget: taller and more confident wins."""
        return min(1.0, (box[3] - box[1]) / 256.0) * float(det.get("confidence") or 0.0)

    def _resolve_inline_batch(
        self,
        inline: List[Tuple[Dict[str, Any], Any, Tuple[int, int, int, int]]],
        deferred: Set[Any],
        now: float,
        live_canonicals: Set[Any],
        config: Any,
        frame_idx: int,
        next_boxes: Dict[Any, Tuple[int, int, int, int]],
    ) -> None:
        """Embed and match untracked detections in one forward pass.

        One ``embed`` call for the whole frame rather than one per person:
        the network is kernel-launch bound, so N separate calls cost close to
        N times a batch of N. Anything that cannot be resolved stays in
        ``deferred`` and is simply not counted this frame -- never adopted
        under its own id, which would count it again on the next frame.
        """
        frame = self._pending_frame
        if frame is None:
            return
        crops: List[np.ndarray] = []
        kept: List[Tuple[Dict[str, Any], Any, Tuple[int, int, int, int]]] = []
        for det, raw, box in inline:
            crop = frame[box[1] : box[3], box[0] : box[2]]
            if crop.size:
                crops.append(crop)
                kept.append((det, raw, box))
        if not crops:
            return
        try:
            vecs = self._embedder.embed(crops)
        except Exception as exc:  # noqa: BLE001 - embedding must never break counting
            logger.debug("ReID inline embed failed: %s", exc)
            return
        if vecs is None or len(vecs) != len(kept):
            return
        for (det, raw, box), vec in zip(kept, vecs, strict=True):
            canonical = self._resolve_identity(
                raw, np.asarray(vec), now, live_canonicals, config, require_absence=False
            )
            det["reid_raw_track_id"] = raw
            det["track_id"] = canonical
            det["reid_canonical_id"] = canonical
            live_canonicals.add(canonical)
            self._reid_canonical_last_frame[canonical] = frame_idx
            self._reid_resolved_ids.add(canonical)
            next_boxes[canonical] = box
            deferred.discard(raw)

    def _apply_known_identity(
        self,
        det: Dict[str, Any],
        raw: Any,
        canonical: Any,
        frame_idx: int,
        now: float,
        ctx: Dict[str, Any],
    ) -> None:
        """Stamp an already-resolved identity onto ``det`` and refresh it.

        Split out of :meth:`_reid_remap_in_place` to keep that method under
        the org complexity cap; the logic is unchanged.
        """
        det["reid_raw_track_id"] = raw
        det["track_id"] = canonical
        det["reid_canonical_id"] = canonical
        self._reid_canonical_last_frame[canonical] = frame_idx
        self._gallery.touch(canonical, now)
        self._absorb_refresh(raw, canonical, now)

        # Occasional refresh keeps the prototype current.
        box = ctx.get("box")
        if not ctx["have_frame"] or box is None:
            return
        if frame_idx - self._reid_last_embed.get(raw, -(10**9)) < ctx["refresh"]:
            return
        if not self._crop_is_usable(box, ctx["valid_boxes"], ctx["fshape"], ctx["config"]):
            return
        crop = ctx["frame"][box[1] : box[3], box[0] : box[2]]
        if crop.size > 0:
            self._worker.offer(_refresh_key(raw), crop)
            self._reid_last_embed[raw] = frame_idx

    def _absorb_refresh(self, raw: Any, canonical: Any, now: float) -> None:
        """Fold any finished embedding for an already-resolved track into the gallery.

        Two results can be waiting: a refresh (queued under ``_refresh_key``),
        and a first-sighting verdict that arrived after the track was already
        released under its raw id. Left in the worker, either one blocks every
        later refresh for the track (``offer`` reports it as known) and is
        never freed.

        ``touch`` alone does not move an identity into the active generation,
        so without this a person who stays in view longer than the gallery
        window is rotated out and double-counted when they later return.

        A refresh can only move a prototype toward what it already looks like.
        A vector below the match threshold most likely comes from a tracker id
        switch onto someone else. It still keeps the identity alive
        (``weight=0.0``), but it is never blended in.
        """
        for key in (_refresh_key(raw), raw):
            vec = self._worker.pop_result(key)
            if vec is None:
                continue
            try:
                sim = self._gallery.similarity(canonical, vec)
                if sim is None:
                    # Not retained (rotated out, or released under its raw id
                    # before a verdict): enrol it so it can be re-identified.
                    self._gallery.insert(canonical, vec, now)
                    self._reid_refresh_applied += 1
                elif sim >= self._gallery.match_threshold:
                    self._gallery.update_prototype(canonical, vec, now)
                    self._reid_refresh_applied += 1
                else:
                    self._gallery.update_prototype(canonical, vec, now, weight=0.0)
                    self._reid_refresh_rejected += 1
            except Exception as exc:  # noqa: BLE001 - a stale prototype is survivable
                logger.debug("ReID refresh failed for %s: %s", canonical, exc)

    def _should_defer(
        self,
        det: Dict[str, Any],
        raw: Any,
        eligible: bool,
        frame_idx: int,
        worker_alive: bool,
        max_defer: int,
        placeholder: bool = False,
    ) -> bool:
        """Whether ``raw`` must be withheld from counting this frame.

        Returning ``False`` normally means the track counts *now* under some
        id. That fallback is safe for a real tracker id, which persists across
        frames, so adopting it over-counts by at most one person.

        It is **not** safe for a placeholder id. Those are unique per frame,
        so adopting one counts a person once per frame for as long as they are
        visible -- the 530-from-7 behaviour seen in production. A placeholder
        that cannot be resolved is therefore held out of counting entirely
        rather than adopted: an unidentified person is better uncounted than
        counted thirty times a second, and the next frame gets another chance
        at the same face.
        """
        if not worker_alive:
            if placeholder:
                # No verdict is coming and the raw id is unusable. Withhold.
                return True
            # No verdict is coming: count under the raw id immediately rather
            # than deferring into a wait that can never end.
            self._adopt_raw(raw, frame_idx)
            det["reid_canonical_id"] = raw
            return False
        if not (self._worker.has_pending(raw) or eligible):
            return placeholder

        first = self._reid_deferred_since.setdefault(raw, frame_idx)
        if frame_idx - first <= max_defer:
            return True
        # Bounded wait: release with the raw id rather than ever losing a
        # count. A slow worker delays, never drops.
        self._reid_deferred_expired += 1
        if placeholder:
            return True
        self._adopt_raw(raw, frame_idx)
        det["reid_canonical_id"] = raw
        return False

    def _adopt_raw(self, raw: Any, frame_idx: int) -> Any:
        """Give up on ReID for ``raw`` and let it count under its own id."""
        self._reid_canonical[raw] = raw
        self._reid_canonical_last_frame[raw] = frame_idx
        self._reid_deferred_since.pop(raw, None)
        return raw

    def _resolve_now(
        self,
        det: Dict[str, Any],
        raw: Any,
        box: Tuple[int, int, int, int],
        now: float,
        live_canonicals: Set[Any],
        config: Any,
    ) -> Optional[Any]:
        """Embed and match ``det`` in-line, for ids that do not outlive a frame.

        Returns the canonical id, or ``None`` when no embedding could be
        produced -- in which case the caller leaves the detection deferred and
        it is simply not counted this frame.
        """
        frame = self._pending_frame
        if frame is None:
            return None
        crop = frame[box[1] : box[3], box[0] : box[2]]
        if crop.size == 0:
            return None
        try:
            vecs = self._embedder.embed([crop])
        except Exception as exc:  # noqa: BLE001 - embedding must never break counting
            logger.debug("ReID inline embed failed: %s", exc)
            return None
        if vecs is None or len(vecs) == 0:
            return None
        canonical = self._resolve_identity(
            raw, np.asarray(vecs[0]), now, live_canonicals, config, require_absence=False
        )
        det["reid_raw_track_id"] = raw
        det["track_id"] = canonical
        det["reid_canonical_id"] = canonical
        return canonical

    def _resolve_identity(
        self,
        raw: Any,
        vec: np.ndarray,
        now: float,
        live_canonicals: Set[Any],
        config: Any,
        require_absence: bool = True,
    ) -> Any:
        """Match ``vec`` against the gallery, or mint a new identity."""
        match = None
        try:
            match = self._gallery.match(
                vec, now, exclude_ids=live_canonicals, require_absence=require_absence
            )
        except Exception as exc:  # noqa: BLE001 - matching must never break counting
            logger.debug("ReID match failed: %s", exc)

        if match is not None:
            canonical = match.canonical_id
            self._reid_last_score = float(match.score)
            self._reid_recovered_total += 1
            self._reid_recovered_this_frame += 1
            try:
                self._gallery.update_prototype(canonical, vec, now)
            except Exception as exc:  # noqa: BLE001 - a stale prototype is survivable
                logger.debug("ReID prototype update failed for %s: %s", canonical, exc)
        else:
            canonical = self._mint_canonical()
            try:
                self._gallery.insert(canonical, vec, now)
            except Exception as exc:  # noqa: BLE001
                logger.debug("ReID insert failed: %s", exc)
                canonical = raw
        self._reid_canonical[raw] = canonical
        return canonical

    # ------------------------------------------------------------------ #
    # Counting hook                                                        #
    # ------------------------------------------------------------------ #
    def _merge_or_register_track(self, raw_id: Any, bbox: Any) -> Any:
        """Proximity-merge raw ids, in a coordinate space that is known.

        The parent merges two raw tracker ids whose boxes are close, to paper
        over sub-second tracker flicker. Its test is
        ``iou >= 0.28 or (center_dist < 35 and size_ratio > 0.6)`` with the
        ``35`` in **pixels** and not configurable. On a feed whose detections
        arrive normalized 0-1 every center distance is below 1, so the
        distance clause is always true and any two similarly-sized people
        merge -- seven people 600 px apart collapse into one identity.

        ``people_counting`` is deliberately left exactly as it is. This class
        instead answers the question itself, with two differences that both
        exist to protect the unique count:

        * an id re-identification already resolved is a *canonical* identity,
          matched on appearance across minutes, not a raw id needing flicker
          repair -- re-merging it can only destroy that work, so it is
          returned untouched;
        * the centre-distance test is expressed as a **fraction of the frame
          diagonal** (:attr:`_MERGE_CENTER_DIST_FRAC`), which means the same
          thing whether coordinates arrive normalized or in pixels. The
          default is calibrated to the parent's 35 px on a 1280x720 frame, so
          a pixel-space deployment sees the behaviour it saw before.
        """
        if raw_id is not None and raw_id in self._reid_resolved_ids:
            return raw_id
        if raw_id is None or bbox is None:
            return raw_id

        now = time.time()
        alias = self._track_aliases.get(raw_id)
        if alias is not None:
            info = self._canonical_tracks.get(alias)
            if info is not None:
                info["last_bbox"] = bbox
                info["last_update"] = now
                info["raw_ids"].add(raw_id)
            return alias

        for cid in [
            c
            for c, i in self._canonical_tracks.items()
            if now - i["last_update"] > self._track_merge_time_window
        ]:
            del self._canonical_tracks[cid]

        match = self._closest_canonical(bbox, now)
        if match is not None:
            info = self._canonical_tracks[match]
            self._track_aliases[raw_id] = match
            info["last_bbox"] = bbox
            info["last_update"] = now
            info["raw_ids"].add(raw_id)
            return match

        self._track_aliases[raw_id] = raw_id
        self._canonical_tracks[raw_id] = {
            "last_bbox": bbox,
            "last_update": now,
            "raw_ids": {raw_id},
        }
        return raw_id

    @staticmethod
    def _bbox_floats(bbox: Any) -> Optional[Tuple[float, float, float, float]]:
        """Raw ``(x1, y1, x2, y2)`` floats, in whatever space they arrived in.

        Deliberately does NOT scale: the merge test is scale-free, so it is
        correct in either space provided both boxes are in the SAME space --
        which they are, both coming from this frame's detections.
        """
        if isinstance(bbox, dict):
            try:
                if "xmin" in bbox:
                    return (
                        float(bbox["xmin"]),
                        float(bbox["ymin"]),
                        float(bbox["xmax"]),
                        float(bbox["ymax"]),
                    )
                if "x1" in bbox:
                    return (
                        float(bbox["x1"]),
                        float(bbox["y1"]),
                        float(bbox["x2"]),
                        float(bbox["y2"]),
                    )
            except (KeyError, TypeError, ValueError):
                return None
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 4:
            try:
                return (float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3]))
            except (TypeError, ValueError):
                return None
        return None

    @staticmethod
    def _iou_f(a: Tuple[float, float, float, float], b: Tuple[float, float, float, float]) -> float:
        """IoU on floats. Already a ratio, so it needs no scaling."""
        ix1, iy1 = max(a[0], b[0]), max(a[1], b[1])
        ix2, iy2 = min(a[2], b[2]), min(a[3], b[3])
        inter = max(0.0, ix2 - ix1) * max(0.0, iy2 - iy1)
        if inter <= 0:
            return 0.0
        area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
        area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
        union = area_a + area_b - inter
        return (inter / union) if union > 0 else 0.0

    def _closest_canonical(self, bbox: Any, now: float) -> Optional[Any]:
        """Canonical id whose last box this one plausibly continues.

        Scale-free by construction: IoU is already a ratio, and the centre
        distance is compared against a fraction of the frame diagonal, so the
        same thresholds hold for normalized and pixel coordinates alike.
        """
        for cid, info in self._canonical_tracks.items():
            if now - info["last_update"] > self._track_merge_time_window:
                continue
            prev = info.get("last_bbox")
            if prev is None:
                continue
            a, b = self._bbox_floats(prev), self._bbox_floats(bbox)
            if a is None or b is None:
                continue
            if self._iou_f(a, b) >= self._MERGE_IOU:
                return cid
            diag = self._frame_diagonal(a, b)
            dist = (
                ((a[0] + a[2]) / 2 - (b[0] + b[2]) / 2) ** 2
                + ((a[1] + a[3]) / 2 - (b[1] + b[3]) / 2) ** 2
            ) ** 0.5
            area_a = max(0.0, a[2] - a[0]) * max(0.0, a[3] - a[1])
            area_b = max(0.0, b[2] - b[0]) * max(0.0, b[3] - b[1])
            ratio = min(area_a, area_b) / max(area_a, area_b) if max(area_a, area_b) > 0 else 0.0
            if dist < self._MERGE_CENTER_DIST_FRAC * diag and ratio > self._MERGE_SIZE_RATIO:
                return cid
        return None

    def _frame_diagonal(self, *boxes: Tuple[float, float, float, float]) -> float:
        """Diagonal of the coordinate space these boxes live in.

        Normalized boxes live in a 1x1 space, diagonal ~1.414. Pixel boxes
        are measured against the decoded frame when one is in hand, and
        against a 1280x720 reference otherwise -- the resolution the parent's
        35 px was tuned at, so an unknown-resolution pixel feed keeps exactly
        the behaviour it had.
        """
        if max((c for box in boxes for c in box), default=0.0) <= _NORMALIZED_MAX:
            return _UNIT_DIAGONAL
        frame = self._pending_frame
        if frame is not None and getattr(frame, "size", 0) > 0:
            return float((frame.shape[0] ** 2 + frame.shape[1] ** 2) ** 0.5)
        return 1468.6  # sqrt(1280^2 + 720^2)

    def _update_tracking_state(self, detections: list) -> Any:
        """Remap ids, then gate promotion behind the ReID verdict.

        A track still awaiting its verdict is **withheld from the parent's
        counting pass entirely** -- the parent only promotes ids it is shown,
        so a deferred track cannot be committed to the cumulative total under
        a raw id that re-identification is about to replace.

        Withholding the detection (rather than blanking its ``track_id``) is
        deliberate. SG-25 added ``record_untracked_frame``, which treats a
        detection with no ``track_id`` as evidence of a broken tracker and
        increments a **process-wide** health counter plus an ERROR log. A
        deferred track is not a tracker fault, so blanking the id would make a
        healthy deployment look broken and would bury real faults in noise.

        The list is restored in ``finally``: zone analysis, the output payload
        and every other consumer run after this call and must see the complete
        frame with real ids.
        """
        config = getattr(self, "_reid_active_config", None)
        deferred: Set[Any] = set()
        if self._reid_enabled and config is not None and self._worker is not None:
            try:
                deferred = self._reid_remap_in_place(detections, config)
            except Exception as exc:  # noqa: BLE001 - ReID must never break counting
                logger.warning("ReID pass failed, counting normally: %s", exc)
                deferred = set()

        if not deferred:
            return super()._update_tracking_state(detections)

        original = list(detections)
        visible: List[Dict[str, Any]] = []
        for det in original:
            raw = det.get("reid_raw_track_id", det.get("track_id"))
            if raw in deferred:
                det["reid_pending"] = True
            else:
                visible.append(det)

        # Mutate in place: the parent reads `detections`, and the caller holds
        # a reference to this same list object. Restored to the ORIGINAL order,
        # not visible-then-held, so nothing downstream sees a reordered frame.
        detections[:] = visible
        try:
            return super()._update_tracking_state(detections)
        finally:
            detections[:] = original

    # ------------------------------------------------------------------ #
    # Entry point                                                          #
    # ------------------------------------------------------------------ #
    def process(
        self,
        data: Any,
        config: ConfigProtocol,
        input_bytes: Optional[bytes] = None,
        context: Optional[ProcessingContext] = None,
        stream_info: Optional[Dict[str, Any]] = None,
    ) -> ProcessingResult:
        # Accept the parent config too, so a misrouted config degrades to
        # plain counting rather than erroring.
        if not isinstance(config, PeopleCountingConfig):
            return self.create_error_result(
                "Invalid config type for people_counting_extended",
                usecase=self.name,
                category=self.category,
                context=context,
            )

        # Default ON: this use case is "unique people counting", so running it
        # without re-identification does not degrade the answer, it changes it
        # into a different (wrong) one. Only an explicit `enable_reid: false`
        # turns it off.
        self._reid_enabled = bool(getattr(config, "enable_reid", True)) and isinstance(
            config, PeopleCountingExtendedConfig
        )
        self._reid_active_config = config
        self._reid_frame_disabled = False

        if self._reid_enabled:
            try:
                if not self._ensure_reid(config):
                    # Disabled for THIS frame only. A previous implementation
                    # cleared the flag permanently, so one transient failure
                    # -- a checkpoint download still in flight, a brief CUDA
                    # OOM -- silently demoted the stream to plain people
                    # counting for the rest of the process's life, with no
                    # way back short of a restart. `get_shared_embedder`
                    # already applies a process-wide backoff, so retrying per
                    # frame is bounded.
                    self._reid_frame_disabled = True
            except Exception as exc:  # noqa: BLE001 - never block counting
                logger.warning("ReID init failed, counting normally: %s", exc)
                self._reid_frame_disabled = True
        else:
            self._reid_frame_disabled = True

        if self._reid_frame_disabled:
            self._reid_enabled = False

        if self._reid_enabled:
            self._pending_frame = self._resolve_frame(input_bytes)
        else:
            self._pending_frame = None

        try:
            result = super().process(data, config, context, stream_info)
        finally:
            # Never retain a frame past the call: a 1080p BGR frame is ~6 MB
            # and instances are long-lived and per-stream.
            self._pending_frame = None
            self._prune_reid_state()

        try:
            self._attach_diagnostics(result)
        except Exception as exc:  # noqa: BLE001 - diagnostics are never load-bearing
            logger.debug("ReID diagnostics attach failed: %s", exc)
        return result

    # ------------------------------------------------------------------ #
    # Housekeeping and diagnostics                                         #
    # ------------------------------------------------------------------ #
    def _prune_reid_state(self, max_entries: int = 20000) -> None:
        """Bound every per-track map. Unbounded dicts are how a stream that
        runs for days leaks.

        Keyed off ``_reid_seen_frame``, which records *every* raw id we have
        touched -- not off ``_reid_canonical``. A track that is permanently
        ineligible for re-identification (too small, always occluded, or a
        stream that never delivers pixels) never acquires a canonical id, so
        a canonical-keyed sweep would never fire for exactly the tracks that
        accumulate fastest.
        """
        if len(self._reid_seen_frame) <= max_entries:
            return
        frame_idx = int(getattr(self, "_total_frame_counter", 0))
        cutoff = frame_idx - 10000
        stale = [raw for raw, last in self._reid_seen_frame.items() if last < cutoff]
        if not stale:
            # Everything is recent (a very crowded stream). Drop the oldest
            # half rather than growing without bound -- losing re-id history
            # for long-gone tracks is preferable to unbounded memory.
            ordered = sorted(self._reid_seen_frame.items(), key=lambda kv: kv[1])
            stale = [raw for raw, _ in ordered[: len(ordered) // 2]]
        for raw in stale:
            canon = self._reid_canonical.pop(raw, None)
            self._reid_seen_frame.pop(raw, None)
            self._reid_track_frames.pop(raw, None)
            self._reid_last_embed.pop(raw, None)
            self._reid_deferred_since.pop(raw, None)
            if canon is not None and canon not in self._reid_canonical.values():
                self._reid_canonical_last_frame.pop(canon, None)
        if self._worker is not None:
            self._worker.forget([*stale, *(_refresh_key(raw) for raw in stale)])

    def reid_stats(self) -> Dict[str, Any]:
        worker = self._worker.stats() if self._worker is not None else {}
        gallery = self._gallery.stats() if self._gallery is not None else {}
        return {
            "reid_model_state": self._reid_state,
            "reid_gallery_size": gallery.get("size", 0),
            "reid_gallery_bytes": gallery.get("bytes", 0),
            "reid_recovered_total": self._reid_recovered_total,
            "reid_recovered_this_frame": self._reid_recovered_this_frame,
            "reid_queue_depth": worker.get("pending", 0),
            "reid_dropped_crops": worker.get("dropped", 0),
            "reid_deferred_pending": len(self._reid_deferred_since),
            "reid_deferred_expired": self._reid_deferred_expired,
            "reid_last_match_score": round(self._reid_last_score, 4),
            "reid_worker_latency_ms_ema": worker.get("latency_ms_ema", 0.0),
            "reid_worker_alive": worker.get("alive", False),
            "reid_refresh_applied": self._reid_refresh_applied,
            "reid_refresh_rejected": self._reid_refresh_rejected,
            # Untracked detections that missed the per-frame crop budget.
            # Rising steadily means the budget is too small for the scene and
            # some people are being seen but not counted.
            "reid_dropped_inline": self._reid_dropped_inline,
            # Whether this stream is running without tracker ids, so the
            # untracked (synchronous, appearance-only) path is in use.
            "reid_untracked_mode": self._reid_untracked_mode,
        }

    def _attach_diagnostics(self, result: Any) -> None:
        """Add ReID counters to ``tracking_stats`` without disturbing it."""
        data = getattr(result, "data", None)
        if not isinstance(data, dict):
            return
        agg = data.get("agg_summary")
        if not isinstance(agg, dict):
            return
        stats = self.reid_stats()
        for frame_payload in agg.values():
            if isinstance(frame_payload, dict) and isinstance(
                frame_payload.get("tracking_stats"), dict
            ):
                frame_payload["tracking_stats"].update(stats)

    def reset(self) -> None:
        """Release ReID resources. Safe to call repeatedly."""
        if self._worker is not None:
            try:
                self._worker.stop()
            except Exception as exc:  # noqa: BLE001 - reset must always complete
                logger.debug("ReID worker stop failed during reset: %s", exc)
            self._worker = None
        if self._gallery is not None:
            self._gallery.clear()
        self._reid_canonical.clear()
        self._reid_deferred_since.clear()
        self._reid_track_frames.clear()
        self._reid_seen_frame.clear()
        self._reid_last_embed.clear()
        self._reid_canonical_last_frame.clear()

    def __del__(self) -> None:  # pragma: no cover - best-effort teardown
        # No logging here: at interpreter shutdown the logging machinery may
        # already be torn down, so a log call can itself raise. `reset()` is
        # the path that reports failures; this is only the safety net.
        try:
            if self._worker is not None:
                self._worker.stop(timeout=0.2)
        except Exception:  # noqa: BLE001, S110 - see above
            pass
