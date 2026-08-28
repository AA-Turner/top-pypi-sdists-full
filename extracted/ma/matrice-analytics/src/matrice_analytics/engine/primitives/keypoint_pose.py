"""``keypoint_pose`` -- per-frame pose classification from a COCO-17 skeleton.

Normative sources: ``_contracts/08-tobe-primitive-catalogue.md`` §2 and
``_migration/wave-d1/group4-missing/PRIMITIVE_SPECS.md`` §2, which was written against the
legacy code.  It replaces the skeleton geometry triplicated in ``fall_detection.py:54-118``,
``fence_climbing_detection_pose.py:35-110`` and ``face_covering_detection_pose.py:53-114``.

**This primitive is stateless and per-frame, which is half the size the config schema
implies.**  Three files hand-rolled three hold timers for it --
``pose_stay_down_seconds: 3.0`` (``fall_detection.py:144``), ``min_climbing_frames: 3`` and
``exit_grace_frames: 3`` (``fence_climbing_detection.py:56-57``), ``min_covering_frames: 3``
(``face_covering_detection_pose.py:197``) -- and every one of them is already
``dwell.threshold_seconds`` or ``state_machine.confirm_frames``/``recovery_frames``.
``dwell.gate`` exists for exactly this composition, so ``fall_detection`` becomes::

    detect -> track -> keypoint_pose -> dwell(gate: {keypoint_pose: down}, threshold_seconds: 3.0)

which is why **the load-bearing output here is the per-track state**, not the counts.  Legacy
computes precisely these quantities (``fall_detection.py:1767-1770``) and then never reads them
again -- they are excluded from ``_count_categories`` and never reach ``agg_summary``; the same
in fence, where ``pose_head_reference_y`` is written at ``:316`` and popped unread at
``fence_climbing_detection.py:745``.

**Only 9 of the 17 COCO joints are ever read** across the three files: the five facial
landmarks (fence's head reference), the shoulders, the wrists and the hips.  There is no
hip/ankle y-drop, no head height and no body-height normalisation anywhere in the tree -- the
plan assumed those; the code does not have them.  Elbows, knees and ankles are never touched.

Every geometric quantity the legacy tree derives from keypoints, exhaustively -- there are
**three**, and this module has all three and nothing else: a confidence-gated pair midpoint
(``fall_detection.py:1652-1655``), the torso angle from vertical (``:1663-1665``), and
"joint above the highest visible facial landmark" (``fence_climbing_detection_pose.py:133-144``).

Two things that are *not* ported, deliberately:

**fall_detection's documented three-step algorithm is not the algorithm that runs.**  The drop
step is ``sudden_drop = False`` at ``fall_detection.py:1729`` with the implementation commented
out at ``:1730-1736``, because the tracker loses the id mid-fall (the in-code rationale at
``:1723-1728``).  ``pose_drop_window_seconds``, ``pose_drop_ratio_thresh``,
``pose_drop_to_down_grace`` and the whole ``frame_h`` plumbing are live in the legacy schema and
dead in the legacy code.  They are not built here.

**The relabel is not ported.**  ``det["category"] = "fall"`` (``:1773``) exists only to get a
detection past ``target_categories = ["fall"]`` (``:399-400``).  In this engine the pose label
*is* the output, so nothing needs renaming and no primitive mutates a detection.

Pure ``math``: no numpy on either real path (neither ``fall_detection.py`` nor
``fence_climbing_detection_pose.py`` imports it), no clock (**PY-13** -- there is no duration
here at all), and no frame resolution except for the one rule that genuinely needs the frame's
*shape* (see :attr:`PoseRule.ratio`).
"""

from __future__ import annotations

import logging
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any, ClassVar, Final

from matrice_analytics.engine.contract.schemas import GLOBAL_ZONE
from matrice_analytics.engine.manifest.models import KeypointPoseConfig
from matrice_analytics.engine.primitives.base import (
    FrameContext,
    Keypoint,
    PipelineDetection,
    PrimitiveOutput,
    PrimitiveValueError,
    Scalar,
    TrackState,
    WindowOutput,
    register,
)
from matrice_analytics.engine.primitives.velocity_state import require_track_ids
from matrice_analytics.engine.state import Lifetime, StateStore

__all__ = [
    "COCO17_JOINTS",
    "POSE_TESTS",
    "UNKNOWN_POSE",
    "KeypointPose",
    "PoseRule",
    "joint_midpoint",
    "torso_angle_degrees",
]

logger = logging.getLogger(__name__)


COCO17_JOINTS: Final[Mapping[str, int]] = {
    "nose": 0,
    "left_eye": 1,
    "right_eye": 2,
    "left_ear": 3,
    "right_ear": 4,
    "left_shoulder": 5,
    "right_shoulder": 6,
    "left_elbow": 7,
    "right_elbow": 8,
    "left_wrist": 9,
    "right_wrist": 10,
    "left_hip": 11,
    "right_hip": 12,
    "left_knee": 13,
    "right_knee": 14,
    "left_ankle": 15,
    "right_ankle": 16,
}
"""Joint name -> index, in the Ultralytics/OpenPose COCO-17 order.

The legacy tree has these as bare integers in three files
(``fall_detection.py:28-29``, ``fence_climbing_detection_pose.py:25-32``,
``face_covering_detection_pose.py``) and a manifest cannot write an integer it can be sure of.
Naming them once is the point: ``joint: [left_wrist, right_wrist]`` is reviewable and
``joint: [9, 10]`` is not.
"""

_SHOULDERS: Final[tuple[int, int]] = (COCO17_JOINTS["left_shoulder"], COCO17_JOINTS["right_shoulder"])
_HIPS: Final[tuple[int, int]] = (COCO17_JOINTS["left_hip"], COCO17_JOINTS["right_hip"])

UNKNOWN_POSE: Final[str] = ""
"""No rule matched, or the track had nothing to classify.

Empty rather than ``"unknown"``, for the same reason as
:data:`~matrice_analytics.engine.primitives.velocity_state.UNKNOWN_STATE`: it is the default of
:attr:`~.base.TrackState.state`, so "we did not decide" has one representation and
``dwell.gate: {keypoint_pose: down}`` cannot accidentally match it.
"""

POSE_TESTS: Final[frozenset[str]] = frozenset(
    {"torso_angle_gt", "joint_above_joint", "bbox_aspect_gt", "any_of"}
)
"""The closed predicate set.  A new predicate is a code change, deliberately.

``rules: list[dict[str, Any]]`` on the config model validates nothing, generates no JSON
Schema for editor completion, and moves every authoring error from manifest load to the first
frame -- which is the failure mode this engine exists to remove.  Until the model carries a
typed ``PoseRule``, :meth:`PoseRule.parse` does that validation in this stage's **constructor**,
so a bad rule is still a startup refusal rather than a mid-stream ``KeyError``.
"""

#: WINDOW keys.  ``match_count`` is a level, so its last and peak readings get separate names
#: (**PY-1**) -- a ``WindowOutput`` goes out verbatim and ``agg_type`` cannot split one name.
_LAST_MATCHES = "last_match_count"
_PEAK_MATCHES = "peak_match_count"
_LAST_MEASURED = "last_measured_count"
_WINDOW_FRAMES = "frames_in_window"

#: Defaults for the fields ``PRIMITIVE_SPECS.md`` §2.2 adds to ``KeypointPoseConfig`` and which
#: are not on the model yet.  Read with ``getattr`` **once, in the constructor**, so this
#: primitive picks each field up the moment it lands and behaves per the spec until then.  See
#: the port report: every one of them is a schema correction, not a permanent private constant.
_DEFAULT_MIN_KEYPOINT_CONFIDENCE: Final[float] = 0.3
_DEFAULT_ON_MISSING_KEYPOINTS: Final[str] = "unknown"


def joint_midpoint(
    keypoints: Sequence[Keypoint], first: int, second: int, min_confidence: float
) -> tuple[float, float] | None:
    """Midpoint of two joints, or ``None`` when either is not confidently visible.

    ``fall_detection.py:1652-1655``: **both** joints must clear the threshold or the result is
    ``None``.  That is the right rule and it is kept -- averaging a confident shoulder with a
    hallucinated one produces a torso vector that is neither.

    Args:
        keypoints: This detection's joints, normalized 0-1.
        first: Index of the first joint, e.g. ``COCO17_JOINTS["left_shoulder"]``.
        second: Index of the second.
        min_confidence: Per-joint visibility floor.

    Returns:
        ``(x, y)`` normalized 0-1, or ``None``.
    """
    if max(first, second) >= len(keypoints):
        return None
    left = keypoints[first]
    right = keypoints[second]
    if left.confidence < min_confidence or right.confidence < min_confidence:
        return None
    return ((left.x + right.x) * 0.5, (left.y + right.y) * 0.5)


def torso_angle_degrees(
    keypoints: Sequence[Keypoint], min_confidence: float
) -> float | None:
    """Angle of the torso away from upright, in degrees, or ``None`` when unmeasurable.

    ``0`` is upright, ``90`` is horizontal, ``180`` is inverted.  The torso vector is
    shoulder-centre minus hip-centre, both confidence-gated pair midpoints, and the angle is
    scale-invariant -- which is the reason to prefer this rule over a pixel one, and the reason
    this primitive needs no frame resolution for it.

    **One deliberate divergence from ``fall_detection.py:1663-1665``.**  Legacy computes
    ``degrees(atan2(abs(dx), abs(dy)))``, which confines the result to ``[0, 90]`` and makes an
    **inverted person indistinguishable from an upright one** -- both read ``0``.  This
    function keeps the sign of the vertical component, so the range is ``[0, 180]``.  For every
    pose where the shoulders are above the hips the two agree *exactly* (with ``dy < 0``,
    ``atan2(|dx|, -dy) == atan2(|dx|, |dy|)``), so a legacy ``pose_angle_thresh_deg: 45``
    carries over unchanged; they differ only where legacy was blind, and there the difference is
    that a person on their head now reads ``~180`` and matches ``torso_angle_gt: 45`` instead of
    reading ``0`` and matching nothing.

    Args:
        keypoints: This detection's joints, normalized 0-1.
        min_confidence: Per-joint visibility floor; all four of shoulders and hips must clear it.

    Returns:
        Degrees in ``[0, 180]``, or ``None`` when either midpoint is unavailable.  ``None`` is
        **not** ``0.0``: an unmeasured torso is not an upright one, and conflating them is how
        ``fall_detection`` confirms a fall from a bounding box alone (``:1719-1721``).
    """
    shoulder = joint_midpoint(keypoints, _SHOULDERS[0], _SHOULDERS[1], min_confidence)
    hip = joint_midpoint(keypoints, _HIPS[0], _HIPS[1], min_confidence)
    if shoulder is None or hip is None:
        return None
    dx = shoulder[0] - hip[0]
    dy = shoulder[1] - hip[1]
    # Image coordinates grow downwards, so an upright torso has dy < 0. Negating it makes
    # "upright" the zero of the angle without folding the inverted case onto it.
    return float(math.degrees(math.atan2(abs(dx), -dy)))


@dataclass(frozen=True, slots=True)
class PoseRule:
    """One named pose predicate, parsed and validated from a manifest ``rules[]`` entry.

    A frozen dataclass in this module rather than a Pydantic model in ``manifest/models.py``
    only because the config model still declares ``rules: list[dict[str, Any]]``; the field set
    below is what that model should carry (see the port report).  :meth:`parse` accepts either
    the raw mapping or an already-typed object, so nothing here changes when it does.
    """

    name: str
    """The label published in ``pose_state`` and on each matching track, e.g. ``"down"``.

    This is the string ``dwell.gate: {keypoint_pose: down}`` joins on, by exact match.
    """

    test: str
    """One of :data:`POSE_TESTS`."""

    degrees: float | None = None
    """``torso_angle_gt``: match when the torso angle exceeds this.  ``45`` is
    ``fall_detection.py``'s ``pose_angle_thresh_deg``."""

    joint: tuple[str, ...] = ()
    """``joint_above_joint``: the joints being tested, e.g. ``("left_wrist", "right_wrist")``."""

    above: tuple[str, ...] = ()
    """``joint_above_joint``: the reference joints.  The reference is the **highest visible**
    one of them (``head_ref_y = min(y)``, ``fence_climbing_detection_pose.py:137``)."""

    margin: float = 0.0
    """``joint_above_joint``: extra clearance required, as a **fraction of frame height**.

    Legacy's ``hands_above_head_margin_px`` (``fence_climbing_detection_pose.py:171``) is
    pixels, compared directly against a pixel keypoint ``y``.  Keypoints are normalized at
    intake here (**PY-7**), so the margin is normalized too -- and since the legacy default is
    ``0.0``, which is unit-free, that costs nothing today.  ``0.02`` on a 1080-line stream is
    the old ``margin_px: 21.6``.
    """

    require_all: bool = False
    """``joint_above_joint``: require **every** joint in :attr:`joint`, not just one.  Legacy's
    ``require_both_wrists_above_head`` (``fence_climbing_detection_pose.py:175``)."""

    ratio: float | None = None
    """``bbox_aspect_gt``: match when ``width / height`` of the box, **in pixels**, exceeds
    this.  ``1.0`` is ``fall_detection.py``'s ``pose_aspect_ratio_thresh``.

    It is a bbox test rather than a keypoint one, and it lives here only because legacy ORs it
    with the torso angle (``fall_detection.py:1721``); keeping it means ``fall_detection`` needs
    no ``custom`` stage.  **This is the one rule that needs the frame resolution**: boxes are
    normalized 0-1, so ``w/h`` in normalized units is the pixel aspect ratio multiplied by the
    frame's own aspect ratio -- on 1920x1080 a pixel aspect of ``1.0`` is a normalized ``0.5625``,
    and comparing the normalized value against the legacy threshold would silently mis-fire by
    that factor.  A pipeline with no such rule never touches
    :meth:`~.base.FrameContext.require_resolution`.
    """

    of: tuple[str, ...] = ()
    """``any_of``: names of **earlier** rules, matched when any of them matches.  This is the
    OR at ``fall_detection.py:1721``; without a combinator that app is not expressible in
    config at all."""

    @classmethod
    def parse(cls, raw: Any, index: int, known: Sequence[str]) -> "PoseRule":
        """Validate one manifest rule entry.

        Args:
            raw: The mapping from ``rules[]``, or any object carrying the same attributes.
            index: Its position in ``rules``, for the error message -- an unnamed rule cannot
                be pointed at any other way.
            known: Names of the rules already parsed, which is what an ``any_of`` may reference.

        Returns:
            The validated rule.

        Raises:
            ValueError: The entry is not a mapping, names no ``test``, names an unknown one, is
                missing the field its test needs, references an unknown joint, or forward-
                references a rule.  Every one of these is a manifest error and every one of
                them is silent in the legacy tree, where ``rules`` is untyped.
        """
        data: Mapping[str, Any]
        if isinstance(raw, Mapping):
            data = raw
        else:
            data = {
                key: getattr(raw, key)
                for key in ("name", "test", "degrees", "joint", "above", "margin", "require_all", "ratio", "of")
                if getattr(raw, key, None) is not None
            }

        where = f"keypoint_pose.rules[{index}]"
        test = data.get("test")
        if test not in POSE_TESTS:
            raise ValueError(
                f"{where} has test={test!r}; it must be one of "
                f"{', '.join(sorted(POSE_TESTS))}. The predicate set is closed on purpose: a "
                "free-form rule dict validates nothing and fails on the first frame instead of "
                "at load."
            )
        name = str(data.get("name") or "").strip()
        if not name:
            raise ValueError(
                f"{where} has no name. The name is what is published in pose_state and what "
                "`dwell.gate: {keypoint_pose: <name>}` joins on by exact string match, so an "
                "unnamed rule can never be composed with anything."
            )

        joints = _as_names(data.get("joint"), f"{where}.joint")
        above = _as_names(data.get("above"), f"{where}.above")
        for role, names in (("joint", joints), ("above", above)):
            unknown = [j for j in names if j not in COCO17_JOINTS]
            if unknown:
                raise ValueError(
                    f"{where}.{role} names {unknown!r}, which are not COCO-17 joints. Legal "
                    f"names: {', '.join(COCO17_JOINTS)}."
                )
        of = _as_names(data.get("of"), f"{where}.of")

        rule = cls(
            name=name,
            test=str(test),
            degrees=None if data.get("degrees") is None else float(data["degrees"]),
            joint=joints,
            above=above,
            margin=float(data.get("margin") or 0.0),
            require_all=bool(data.get("require_all") or False),
            ratio=None if data.get("ratio") is None else float(data["ratio"]),
            of=of,
        )
        rule._check_required(where, known)
        return rule

    def _check_required(self, where: str, known: Sequence[str]) -> None:
        """Reject a rule missing the field its own test needs."""
        if self.test == "torso_angle_gt":
            if self.degrees is None or not 0.0 <= self.degrees <= 180.0:
                raise ValueError(
                    f"{where} is torso_angle_gt and needs degrees in 0-180 (0 = upright, "
                    "90 = horizontal, 180 = inverted); fall_detection's threshold is 45."
                )
        elif self.test == "joint_above_joint":
            if not self.joint or not self.above:
                raise ValueError(
                    f"{where} is joint_above_joint and needs both 'joint' and 'above', e.g. "
                    "joint: [left_wrist, right_wrist], above: [nose, left_eye, right_eye, "
                    "left_ear, right_ear]."
                )
            if self.margin < 0.0:
                raise ValueError(
                    f"{where}.margin is {self.margin}; it is a fraction of frame height and a "
                    "negative clearance would mean 'below', which is what swapping joint and "
                    "above says explicitly."
                )
        elif self.test == "bbox_aspect_gt":
            if self.ratio is None or self.ratio <= 0.0:
                raise ValueError(
                    f"{where} is bbox_aspect_gt and needs ratio > 0 (width/height in pixels); "
                    "fall_detection's threshold is 1.0."
                )
        elif self.test == "any_of":
            if not self.of:
                raise ValueError(f"{where} is any_of and needs 'of': a list of earlier rule names.")
            missing = [name for name in self.of if name not in known]
            if missing:
                raise ValueError(
                    f"{where}.of references {missing!r}, which name no earlier rule. Rules "
                    f"resolve in order and a forward reference cannot be evaluated; rules so "
                    f"far: {', '.join(known) or '(none)'}."
                )


def _as_names(value: Any, where: str) -> tuple[str, ...]:
    """Read a joint/rule name list, accepting a bare string for one name."""
    if value is None:
        return ()
    if isinstance(value, str):
        return (value,)
    if isinstance(value, Sequence):
        return tuple(str(item) for item in value)
    raise ValueError(f"{where} must be a name or a list of names, got {type(value).__name__}")


@dataclass(frozen=True, slots=True)
class _Pose:
    """What one detection's skeleton says, before the rules are applied."""

    torso_angle: float | None
    aspect_ratio: float | None
    joints_seen: int
    has_keypoints: bool
    keypoints: tuple[Keypoint, ...] = field(default=())


@register(name="keypoint_pose")
class KeypointPose:
    """Per-frame pose classification for one zone, published per track.

    Outputs (:attr:`~.base.PrimitiveOutput.values`):

    ``pose_state``
        The modal rule name across this frame's tracks, ``""`` when none matched -- the
        ``velocity_state.state`` convention.
    ``match_count``
        Tracks matching any published rule this frame.
    ``measured_count``
        Tracks that had usable keypoints.  **The pose-model outage signal**: a detector-only
        stream makes this ``0`` while ``detect`` reports a busy scene, and legacy has no
        equivalent -- ``fence_climbing_detection_pose`` publishes zero climbing alerts forever
        in that situation (``:130-131``) while its zone counting continues normally, so the app
        looks healthy.

    Plus :attr:`~.base.PrimitiveOutput.tracks`, where each matching track carries
    ``state = <rule name>`` and ``attributes = {"torso_angle_deg": ..., "keypoints_seen": ...}``.
    **That per-track state is the load-bearing output**, because it is what ``dwell.gate``
    reads; the scalars above are for dashboards.

    Rule resolution, stated because it is not inferable:

    * Rules are evaluated in manifest order and the **first matching** one names the track.
    * A rule referenced by some ``any_of``'s ``of`` list is an **ingredient**: it is evaluated,
      but it never names a track and never counts towards ``match_count``.  That is what lets
      ``fall_detection`` publish one label ``down`` over the ``angle OR aspect`` pair instead of
      leaking the two helper names into ``pose_state`` and breaking ``dwell.gate``.
    """

    name: ClassVar[str] = "keypoint_pose"
    Config: ClassVar[type[KeypointPoseConfig]] = KeypointPoseConfig

    __slots__ = (
        "_classes",
        "_config",
        "_min_confidence",
        "_needs_resolution",
        "_on_missing",
        "_published",
        "_rules",
        "_state",
    )

    def __init__(self, config: KeypointPoseConfig, state: StateStore) -> None:
        """Parse and validate the rule set once, at startup.

        Args:
            config: The validated ``keypoint_pose:`` block.
            state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.  Only the
                window's last/peak readings live here; there is no per-track state, because
                duration is ``dwell``'s and hysteresis is ``state_machine``'s.

        Raises:
            ValueError: ``skeleton_type`` is not ``coco17``, or a rule is malformed.  Both are
                startup refusals (``09`` §5): a pose rule that cannot be evaluated must not
                become a stage that matches nothing.
        """
        # Either spelling: the model declares ``skeleton_type`` today and ``PRIMITIVE_SPECS.md``
        # §2.2 renames it ``skeleton`` while narrowing it to ``coco17``.
        skeleton = str(
            getattr(config, "skeleton", None) or getattr(config, "skeleton_type", "coco17")
        )
        if skeleton != "coco17":
            raise ValueError(
                f"keypoint_pose supports skeleton 'coco17' only, got {skeleton!r}. The joint "
                "indices this primitive reads (shoulders 5/6, wrists 9/10, hips 11/12, face "
                "0-4) are COCO-17 positions; coco18 and 'custom' renumber them, so evaluating "
                "a rule against one would silently read the wrong joints. No consumer in the "
                "tree sends either -- narrow the manifest until one does."
            )
        self._config = config
        self._state = state
        # Read once, here: see _DEFAULT_* above, and the port report for the schema fix.
        self._min_confidence = float(
            getattr(config, "min_keypoint_confidence", _DEFAULT_MIN_KEYPOINT_CONFIDENCE)
        )
        self._on_missing = str(
            getattr(config, "on_missing_keypoints", _DEFAULT_ON_MISSING_KEYPOINTS)
        )
        # No `classes` on the model yet; an empty tuple means "every entity in this zone",
        # which is what the legacy apps do -- they filter by target_categories upstream.
        self._classes: tuple[str, ...] = tuple(getattr(config, "classes", ()) or ())

        rules: list[PoseRule] = []
        for index, raw in enumerate(config.rules):
            rules.append(PoseRule.parse(raw, index, [rule.name for rule in rules]))
        self._rules: tuple[PoseRule, ...] = tuple(rules)
        ingredients = {name for rule in self._rules for name in rule.of}
        self._published: frozenset[str] = frozenset(
            rule.name for rule in self._rules if rule.name not in ingredients
        )
        if not self._published:
            raise ValueError(
                "keypoint_pose has no publishable rule: every rule is referenced by an "
                "any_of, so no rule name can ever reach pose_state or a track's state. The "
                "combinator rule itself is the label -- give it a name nothing else "
                "references, e.g. name: down, test: any_of, of: [down_angle, down_flat]."
            )
        self._needs_resolution = any(rule.test == "bbox_aspect_gt" for rule in self._rules)

    # -- per frame ----------------------------------------------------------

    def process(self, ctx: FrameContext) -> PrimitiveOutput:
        """Classify every tracked object in this zone, for this frame.

        Args:
            ctx: The frame.  ``det.keypoints`` are normalized 0-1 (the runtime does that at
                intake) and ``det.track_id`` is stamped by the tracker stage.

        Returns:
            The three values plus one :class:`~.base.TrackState` per evaluated track.  Never
            any events: a pose is a state, and turning a state into an incident is
            ``state_machine`` plus the manifest (**O1**).

        Raises:
            TrackingRequiredError: No tracker ran, or its ids never reached the detections.
                Per-track state is this primitive's output, so an untracked pipeline would
                publish an empty ``tracks`` map forever.
            PrimitiveValueError: ``on_missing_keypoints: error`` and a detection carries none;
                or a ``bbox_aspect_gt`` rule is configured on a stream with no resolution.
        """
        tracked = require_track_ids(ctx, self.name, state=self._state)
        aspect_scale = 1.0
        if self._needs_resolution:
            width, height = ctx.require_resolution(
                f"keypoint_pose stage {self._config.stage_name!r} (a bbox_aspect_gt rule "
                "compares width/height in pixels)"
            )
            # Normalized w/h times W/H is the pixel aspect ratio.
            aspect_scale = float(width) / float(height)

        tracks: dict[int, TrackState] = {}
        label_counts: dict[str, int] = {}
        matches = 0
        measured = 0
        seen: set[int] = set()

        for track_id, det in tracked:
            if track_id in seen:
                # Two boxes, one id: the tracker is confused. Keep the first, deterministically.
                continue
            if self._classes and det.entity not in self._classes:
                continue
            seen.add(track_id)
            pose = self._read_pose(det, ctx, aspect_scale)
            if pose is None:
                continue
            if pose.has_keypoints:
                measured += 1
            label = self._classify(pose)
            if label:
                matches += 1
                label_counts[label] = label_counts.get(label, 0) + 1
            attributes: dict[str, Scalar] = {"keypoints_seen": pose.joints_seen}
            if pose.torso_angle is not None:
                attributes["torso_angle_deg"] = pose.torso_angle
            if pose.aspect_ratio is not None:
                attributes["bbox_aspect_ratio"] = pose.aspect_ratio
            tracks[track_id] = TrackState(
                track_id=track_id,
                entity=det.entity,
                zone=ctx.zone or GLOBAL_ZONE,
                first_seen=ctx.frame_ts,
                last_seen=ctx.frame_ts,
                state=label,
                attributes=attributes,
            )

        self._accumulate(matches, measured)
        return PrimitiveOutput(
            values={
                "pose_state": _modal(label_counts),
                "match_count": matches,
                "measured_count": measured,
            },
            tracks=tracks,
        )

    def _read_pose(
        self, det: PipelineDetection, ctx: FrameContext, aspect_scale: float
    ) -> _Pose | None:
        """Derive this detection's three geometric quantities, applying the missing policy.

        Returns:
            The pose, or ``None`` when the detection has no keypoints and the policy is
            ``unknown`` -- in which case the track is not classified at all and does not appear
            in ``tracks``.  That is the deliberate opposite of ``fall_detection``, which lets
            ``angle = None`` degrade ``is_horizontal`` to ``aspect_ratio > 1.0`` (``:1719-1721``)
            and **confirms a fall with zero keypoints**, with no log.

        Raises:
            PrimitiveValueError: The policy is ``error``.  That is
                ``fence_climbing_detection_pose``'s silent hard-fail (``:130-131``), made loud:
                there, a detection-only stream yields zero climbing alerts forever while zone
                counting continues and the app looks healthy.
        """
        box = det.bounding_box
        width = box.xmax - box.xmin
        height = box.ymax - box.ymin
        aspect = (width / height) * aspect_scale if height > 0.0 else None
        keypoints = det.keypoints
        joints_seen = sum(1 for kp in keypoints if kp.confidence >= self._min_confidence)

        if joints_seen:
            return _Pose(
                torso_angle=torso_angle_degrees(keypoints, self._min_confidence),
                aspect_ratio=aspect,
                joints_seen=joints_seen,
                has_keypoints=True,
                keypoints=tuple(keypoints),
            )

        if self._on_missing == "bbox_only":
            # Legacy fall_detection's fallback, named: only bbox tests can match.
            return _Pose(torso_angle=None, aspect_ratio=aspect, joints_seen=0, has_keypoints=False)
        if self._on_missing == "unknown":
            return None
        raise PrimitiveValueError(
            f"keypoint_pose stage {self._config.stage_name!r} got a {det.entity!r} detection "
            f"with no keypoint above min_keypoint_confidence={self._min_confidence:g} in zone "
            f"{ctx.zone!r} at frame_ts {ctx.frame_ts} ({len(keypoints)} keypoint(s) present). "
            "on_missing_keypoints: error says that is a broken pose model rather than a pose. "
            "Use on_missing_keypoints: unknown to leave such tracks unclassified, or "
            "bbox_only to fall back to the bbox rules the way fall_detection does silently."
        )

    def _classify(self, pose: _Pose) -> str:
        """The first publishable rule this pose satisfies, or :data:`UNKNOWN_POSE`."""
        matched: dict[str, bool] = {}
        result = UNKNOWN_POSE
        for rule in self._rules:
            matched[rule.name] = self._matches(rule, pose, matched)
            if result == UNKNOWN_POSE and matched[rule.name] and rule.name in self._published:
                result = rule.name
        return result

    def _matches(self, rule: PoseRule, pose: _Pose, matched: Mapping[str, bool]) -> bool:
        """Evaluate one rule.  An unmeasurable quantity never matches."""
        if rule.test == "torso_angle_gt":
            return pose.torso_angle is not None and pose.torso_angle > (rule.degrees or 0.0)
        if rule.test == "bbox_aspect_gt":
            return pose.aspect_ratio is not None and pose.aspect_ratio > (rule.ratio or 0.0)
        if rule.test == "any_of":
            return any(matched.get(name, False) for name in rule.of)
        return self._joint_above(rule, pose)

    def _joint_above(self, rule: PoseRule, pose: _Pose) -> bool:
        """``fence_climbing_detection_pose.py:133-144``: a joint above the head reference.

        ``head_ref_y = min(y)`` over the *visible* reference joints -- image coordinates grow
        downwards, so "above" is ``<`` and the highest visible landmark is the smallest ``y``.
        With no visible reference joint the rule does not match, which is legacy's behaviour
        (``:135-136``) and the right one: an unmeasured reference is not a passed test.
        """
        keypoints = pose.keypoints
        if not keypoints:
            return False
        references = [
            keypoints[COCO17_JOINTS[name]].y
            for name in rule.above
            if COCO17_JOINTS[name] < len(keypoints)
            and keypoints[COCO17_JOINTS[name]].confidence >= self._min_confidence
        ]
        if not references:
            return False
        threshold = min(references) - rule.margin
        tested = [
            keypoints[COCO17_JOINTS[name]]
            for name in rule.joint
            if COCO17_JOINTS[name] < len(keypoints)
        ]
        results = [
            kp.confidence >= self._min_confidence and kp.y < threshold for kp in tested
        ]
        if not results:
            return False
        return all(results) if rule.require_all else any(results)

    # -- the window ---------------------------------------------------------

    def _accumulate(self, matches: int, measured: int) -> None:
        """Fold this frame into the window, in the state store (``09`` §4 rule 1, **D6**)."""
        self._state.set(_LAST_MATCHES, matches, lifetime=Lifetime.WINDOW)
        self._state.set(
            _PEAK_MATCHES,
            max(int(self._state.get(_PEAK_MATCHES) or 0), matches),
            lifetime=Lifetime.WINDOW,
        )
        self._state.set(_LAST_MEASURED, measured, lifetime=Lifetime.WINDOW)
        self._state.incr(_WINDOW_FRAMES, 1, lifetime=Lifetime.WINDOW)

    def window(self, frames: Sequence[PrimitiveOutput]) -> WindowOutput:
        """Collapse the window.  ``match_count`` is a level, so it gets **two** names (**PY-1**).

        ``match_count`` is the count on the window's **last** frame and ``match_count_peak`` is
        the **peak concurrent** count; a ``WindowOutput`` is published verbatim, so one name
        could only answer one of those and would answer the other wrongly, in silence.
        ``pose_state`` is the pose the zone spent the most frames in -- the same reading
        ``velocity_state.window`` publishes for its ``state``.

        Args:
            frames: This stage's per-frame outputs for the window, in frame order.  Read for
                the modal pose; the counts come from the store, which is unaffected by the
                frame-retention cap in ``runtime/window.py``.
        """
        state_frames: dict[str, int] = {}
        for frame in frames:
            label = str(frame.values.get("pose_state", UNKNOWN_POSE))
            if label:
                state_frames[label] = state_frames.get(label, 0) + 1
        if not frames and not float(self._state.get(_WINDOW_FRAMES) or 0.0):
            return WindowOutput()
        return WindowOutput(
            values={
                "pose_state": _modal(state_frames),
                "match_count": int(self._state.get(_LAST_MATCHES) or 0),
                "match_count_peak": int(self._state.get(_PEAK_MATCHES) or 0),
                "measured_count": int(self._state.get(_LAST_MEASURED) or 0),
            }
        )

    def reset(self) -> None:
        """Clear the window readings at the aggregation boundary.

        ``end_window()``, not ``clear()``: there is no cumulative total here today, and
        reaching for the full reset is the habit that erases one somewhere else (``09`` §4
        rule 2, **FROZEN-4**).
        """
        self._state.end_window()


def _modal(counts: Mapping[str, int]) -> str:
    """The most common label; a tie goes to the alphabetically first name.

    Sorted first so two runs over the same frames agree: ranking by dict order would make this
    depend on rule insertion order and, once a set is involved anywhere upstream, on
    ``PYTHONHASHSEED`` -- which is **PY-9**.  Same helper shape as
    ``velocity_state._modal``, for the same reason.
    """
    if not counts:
        return UNKNOWN_POSE
    return max(sorted(counts), key=lambda name: counts[name])
