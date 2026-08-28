"""Auto-generated stub for module: segmentation_area."""
from typing import Any

# Constants
logger: Any

# Functions
def decode_simple_rle_area(counts: str) -> int:
    """
    Foreground pixel count from a base64 ``simple_rle`` run-length string.
    
        The decoded bytes are little-endian ``uint32`` run lengths that alternate
        background/foreground **starting with background**, laid out row-major over the mask's
        ``size`` (contract ``04`` §5.1).  The foreground area is therefore the sum of the runs at
        **odd** indices -- no allocation of the mask itself, no numpy, ``O(runs)``.
    
        Args:
            counts: The base64 ``counts`` string as the producer sends it.
    
        Returns:
            Total foreground pixels.  ``0`` for an empty string, which is a legitimate
            "nothing segmented" rather than an error.
    
        Raises:
            ValueError: The string is not base64, or its decoded length is not a multiple of 4.
                Both mean the payload is not what it claims to be, and a truncated final run
                would silently under-report the area.
    
        Example:
            >>> import base64, struct
            >>> counts = base64.b64encode(struct.pack("<4I", 2, 3, 4, 7)).decode()
            >>> decode_simple_rle_area(counts)  # 3 + 7 foreground pixels
            10
    """
    ...
def measure_mask(mask: Any | None) -> Any | None:
    """
    Measure one mask, or return ``None`` when it carries nothing usable.
    
        The three-tier cascade of ``landslide_detection.py:283-313``, minus its silent tiers:
        a pre-computed :attr:`~.base.MaskRef.area_px`, then :attr:`~.base.MaskRef.rle`, then
        :attr:`~.base.MaskRef.polygon`.  The denominator is always the mask's own
        :attr:`~.base.MaskRef.size`, which is the correction to legacy's Tier 2 -- that tier
        divides a polygon area by the *frame* area while Tier 1 divides by the mask's, so the two
        tiers of one function publish two different quantities under one name.
    
        A polygon with no ``size`` is treated as already normalized 0-1, because that is the only
        other coordinate space this engine has.
    
        Returns:
            The measurement, or ``None`` when there is no mask, no usable size, or no carrier.
            ``None`` is what :attr:`SegmentationArea.on_missing_mask` then decides about -- it is
            never quietly turned into ``0.0``.
    
        Raises:
            ValueError: The mask claims an encoding this module cannot decode, or its ``rle`` is
                malformed.  Loud, because a mis-decoded mask is a plausible wrong number.
    """
    ...
def polygon_area(points: Any[Any[float]]) -> float:
    """
    Unsigned area of a simple polygon, by the shoelace formula.
    
        ``cv2.contourArea`` returns exactly this for a simple (non-self-intersecting) contour, so
        replacing the legacy call (``landslide_detection.py:302``) with 4 lines of stdlib is
        behaviour-preserving rather than an approximation -- and it removes a cv2 import from a
        module the engine is forbidden to have one in (**PY-20**).
    
        Args:
            points: ``[(x, y), ...]`` vertices, in either winding order, in any one unit.
    
        Returns:
            The area in that unit squared; ``0.0`` for fewer than three vertices, which is a
            degenerate contour and not an error.
    """
    ...

# Classes
class MaskMeasurement:
    # One detection's mask, measured.
    #
    #     A named triple rather than three parallel lists, because the three travel together and
    #     :attr:`measured` is what separates "0 % coverage" from "no mask at all" -- exactly the
    #     distinction legacy loses when Tier 3 substitutes the bounding box.

    ...
class SegmentationArea:
    # Mask coverage for one zone, one frame -- as a fraction, never a percent.
    #
    #     Outputs (:attr:`~.base.PrimitiveOutput.values`), each resolvable as ``<stage>.<name>``:
    #
    #     ``area_ratio``
    #         The reduced coverage, ``0-1``.  ``max`` of the instances by default, ``sum`` when
    #         ``reduce: sum`` reproduces ``landslide_detection``'s total.  Clamped to ``1.0``
    #         unless ``clamp: false``.
    #     ``max_area_ratio``
    #         The largest single instance, whatever ``reduce`` is.  Legacy publishes both
    #         (``max_landslide_area_pct`` ``:1337``, ``total_landslide_area_pct`` ``:1338``) and an
    #         operator reads them differently: one answers "how big is the biggest slide", the
    #         other "how much ground is moving".
    #     ``instance_count``
    #         Detections of ``classes`` in this zone this frame.
    #     ``measured_count``
    #         How many of them carried a real mask.  **``measured_count < instance_count`` is the
    #         mask-outage signal**, and it exists because legacy's silent bounding-box proxy has
    #         none: a dead mask stage there publishes plausible coverage forever.
    #     ``area_px``
    #         The reduced foreground pixel count in the masks' own space -- a **diagnostic**, not a
    #         metric.  It is resolution-dependent by construction and only comparable when every
    #         mask in the frame shares one ``size``; ``area_ratio`` is the number a manifest should
    #         threshold on.  It is published because the config model declares it today (see the
    #         schema corrections in this module's port report).
    #
    #     At window scope (:meth:`window`) ``area_ratio`` is the **last** frame's coverage and
    #     ``area_ratio_peak`` is the window's high-water mark, because a ``WindowOutput`` is
    #     published verbatim and one name cannot answer both (**PY-1**).
    #
    #     Not here, on purpose: severity (that is ``incident_quantise`` or a manifest
    #     ``severity_from``), smoothing (``state_machine``), cooldown (the incident lifecycle), and
    #     ``flood_detection``'s *filter* semantics -- a primitive cannot remove a detection from the
    #     frame the next stage sees, and one that could would be action at a distance.  See the port
    #     report for that fidelity limit.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Bind a validated config to a state store already scoped to this stage.
        
                Args:
                    config: The validated ``segmentation_area:`` block.
                    state: Scoped to ``<camera_id>/<app_id>/<zone>/<stage>`` by the runtime.  The
                        window peak lives here rather than in an instance attribute (``09`` §4 rule 1,
                        **D6**), which is also why ``__slots__`` leaves no room for one.
        
                Raises:
                    ValueError: ``normalize: none`` -- see the message.  Refused at construction, so
                        it is a startup failure (``09`` §5) rather than a metric nobody can use.
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Measure this zone's masks for one frame.
        
                Args:
                    ctx: The frame.  Only ``detections`` are read -- there is no clock call and no
                        :meth:`~.base.FrameContext.require_resolution`, because the masks carry their
                        own denominator.
        
                Returns:
                    The five values above.  Never any events: coverage becomes an incident through a
                    manifest threshold, which is the runtime's decision (**O1**).
        
                Raises:
                    PrimitiveValueError: A detection of ``classes`` carries no usable mask and
                        ``on_missing_mask`` is ``error`` (the default), or a mask is malformed.  A
                        mask-free frame on a segmentation app is a broken deployment, and a
                        bounding-box proxy for it is plausible and wrong.
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear the window accumulators at the aggregation boundary.
        
                :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, not ``clear()``:
                this stage keeps no cumulative total today, and reaching for the full reset is the
                habit that erases one somewhere else (``09`` §4 rule 2, **FROZEN-4**).
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse the window.  ``area_ratio`` is a level, so it gets **two** names (**PY-1**).
        
                ``area_ratio`` here is the coverage on the window's **last** frame and
                ``area_ratio_peak`` is the window's **maximum**.  A ``WindowOutput`` is published
                verbatim -- the runtime does not re-apply ``metrics[].agg_type`` to a registered
                primitive -- so a single name would answer one of those questions and answer the other
                one wrongly, in silence.  ``max_area_ratio`` at window scope is the largest single
                instance seen **anywhere in the window**, which is the only reading of a per-frame
                maximum that an operator asks for.
        
                Args:
                    frames: This stage's per-frame outputs for the window, in frame order.  Unused:
                        the accumulators in the state store hold the same data already folded, and
                        they survive a window whose retained frames were capped
                        (``runtime/window.py`` truncates at ``max_frames``, which would silently
                        lower a peak computed from this list).
        
                Returns:
                    The five window keys, or an empty output for a window with no frames -- an empty
                    aggregation is not a coverage of zero.
        """
        ...

