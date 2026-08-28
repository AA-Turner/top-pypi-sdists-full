"""Auto-generated stub for module: keypoint_pose."""
from typing import Any

# Constants
logger: Any

# Functions
def joint_midpoint(keypoints: Any[Any], first: int, second: int, min_confidence: float) -> tuple[float, float] | None:
    """
    Midpoint of two joints, or ``None`` when either is not confidently visible.
    
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
    ...
def torso_angle_degrees(keypoints: Any[Any], min_confidence: float) -> float | None:
    """
    Angle of the torso away from upright, in degrees, or ``None`` when unmeasurable.
    
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
    ...

# Classes
class KeypointPose:
    # Per-frame pose classification for one zone, published per track.
    #
    #     Outputs (:attr:`~.base.PrimitiveOutput.values`):
    #
    #     ``pose_state``
    #         The modal rule name across this frame's tracks, ``""`` when none matched -- the
    #         ``velocity_state.state`` convention.
    #     ``match_count``
    #         Tracks matching any published rule this frame.
    #     ``measured_count``
    #         Tracks that had usable keypoints.  **The pose-model outage signal**: a detector-only
    #         stream makes this ``0`` while ``detect`` reports a busy scene, and legacy has no
    #         equivalent -- ``fence_climbing_detection_pose`` publishes zero climbing alerts forever
    #         in that situation (``:130-131``) while its zone counting continues normally, so the app
    #         looks healthy.
    #
    #     Plus :attr:`~.base.PrimitiveOutput.tracks`, where each matching track carries
    #     ``state = <rule name>`` and ``attributes = {"torso_angle_deg": ..., "keypoints_seen": ...}``.
    #     **That per-track state is the load-bearing output**, because it is what ``dwell.gate``
    #     reads; the scalars above are for dashboards.
    #
    #     Rule resolution, stated because it is not inferable:
    #
    #     * Rules are evaluated in manifest order and the **first matching** one names the track.
    #     * A rule referenced by some ``any_of``'s ``of`` list is an **ingredient**: it is evaluated,
    #       but it never names a track and never counts towards ``match_count``.  That is what lets
    #       ``fall_detection`` publish one label ``down`` over the ``angle OR aspect`` pair instead of
    #       leaking the two helper names into ``pose_state`` and breaking ``dwell.gate``.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Parse and validate the rule set once, at startup.
        
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
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Classify every tracked object in this zone, for this frame.
        
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
        ...

    def reset(self: Any) -> None:
        """
        Clear the window readings at the aggregation boundary.
        
                ``end_window()``, not ``clear()``: there is no cumulative total here today, and
                reaching for the full reset is the habit that erases one somewhere else (``09`` §4
                rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``match_count`` is a level, so it gets **two** names (**PY-1**).
        
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
        ...

class PoseRule:
    # One named pose predicate, parsed and validated from a manifest ``rules[]`` entry.
    #
    #     A frozen dataclass in this module rather than a Pydantic model in ``manifest/models.py``
    #     only because the config model still declares ``rules: list[dict[str, Any]]``; the field set
    #     below is what that model should carry (see the port report).  :meth:`parse` accepts either
    #     the raw mapping or an already-typed object, so nothing here changes when it does.

    def parse(cls: Any, raw: Any, index: int, known: Any[str]) -> 'Any':
        """
        Validate one manifest rule entry.
        
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
        ...

