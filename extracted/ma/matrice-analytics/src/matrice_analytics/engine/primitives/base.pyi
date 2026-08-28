"""Auto-generated stub for module: base."""
from typing import Any

# Constants
REGISTRY: Any
Scalar: Any

# Functions
def conformance_problems(impl: Any[Any]) -> list[str]:
    """
    Explain why ``impl`` is not a conforming primitive, or return ``[]``.
    
        ``isinstance(x, Primitive)`` answers yes/no; this answers "which member is missing and
        what should its signature be", which is what an app author or a reviewer actually
        needs.  Used by :meth:`PrimitiveRegistry.register` so a bad implementation fails at
        import time rather than on the first frame.
    
        Args:
            impl: The candidate class.
            custom: Check against :class:`CustomPrimitive` (``Config`` + ``process``) rather
                than the full :class:`Primitive`.
    
        Returns:
            A list of human-readable problems, empty when ``impl`` conforms.
    """
    ...
def register(impl: Any[Any] | None = None) -> Any:
    """
    Register on the default :data:`REGISTRY` (see :meth:`PrimitiveRegistry.register`).
    
        Example:
            >>> @register
            ... class ZoneOccupancy:
            ...     name = "zone_occupancy"
            ...     Config = ZoneOccupancyConfig
            ...     ...
    """
    ...
def resolve_value(outputs: Any[str, Any], source: str) -> Any:
    """
    Resolve a ``metrics[].source`` against a frame's stage outputs.
    
        ``<stage>.<value>``, where ``<value>`` may itself contain dots
        (``detect.person.count`` is stage ``detect``, value ``person.count``).
    
        Args:
            outputs: Stage name -> that stage's output, i.e. what
                :attr:`FrameContext.previous` holds.
            source: The manifest source string.
    
        Returns:
            The scalar the manifest asked for.
    
        Raises:
            SourceResolutionError: The stage or the value is missing.  ``09`` §3: *an
                unresolvable source is a manifest load error -- not a metric that reads zero
                forever*.  The message names what *is* available, because the usual cause is a
                one-character typo in ``app.yaml``.
    """
    ...

# Classes
class Clock:
    # The engine's only source of "now".
    #
    #     Injectable so that replay, backfill and generated tests are driven by frame time
    #     rather than by the host's wall clock (**PY-13**).  Windowing
    #     (``engine/runtime/window.py``) consumes this; primitives should read
    #     :attr:`FrameContext.frame_ts` and never call a clock at all.

    def now(self: Any) -> float:
        """
        Current time in epoch seconds.
        """
        ...

class CustomPrimitive:
    # A full pipeline stage written by an app author (``09`` §6).
    #
    #     Narrower than :class:`Primitive` on purpose: no ``name`` (the manifest stage supplies
    #     it) and no ``window`` (the runtime aggregates the ``values`` a custom stage publishes,
    #     using each metric's ``agg_type``).  ``reset`` is optional; the runtime calls it if it
    #     is there.
    #
    #     The loader enforces exactly ``Config`` + ``process``
    #     (``manifest/loader.py:_resolve_custom_impl``), so this protocol and that check must
    #     stay in step.
    #
    #     Custom code must not touch the wire format, re-implement a primitive, do network I/O,
    #     load a model, or spawn a thread -- each is a current pathology with a name in
    #     ``12-defect-register.md`` (**PY-15** for the last one).

    def __init__(self: Any, config: Any, state: Any) -> None: ...

    def process(self: Any, ctx: Any) -> Any: ...

class FrameClock:
    # The default clock: it advances only when a frame says so (**PY-13**).
    #
    #     Feeding it the real frame timestamp makes a replayed hour of footage produce exactly
    #     the windows the live run produced.  ``time.time()`` cannot do that, which is the whole
    #     defect.
    #
    #     Example:
    #         >>> clock = FrameClock()
    #         >>> clock.advance(1_700_000_000.0)
    #         >>> clock.now() == 1_700_000_000.0
    #         True

    def advance(self: Any, frame_ts: float) -> None:
        """
        Move the clock to ``frame_ts``.
        
                Args:
                    frame_ts: The real frame timestamp, epoch seconds.
        
                Raises:
                    ValueError: ``frame_ts`` goes backwards.  Out-of-order frames would reopen a
                        closed window and double-publish it; the caller must decide to drop or to
                        reset, and cannot decide it by accident.
        """
        ...

    def now(self: Any) -> float:
        """
        The timestamp of the most recent frame.
        """
        ...

    def reset(self: Any, frame_ts: float = 0.0) -> None:
        """
        Force the clock to ``frame_ts``, e.g. when a stream restarts.
        """
        ...

class FrameContext:
    # Everything a primitive is given for one frame, in one zone.
    #
    #     A plain frozen dataclass rather than a Pydantic model **on purpose**: this is
    #     constructed once per frame *per zone* -- at 25 fps with four zones that is 100
    #     validations a second per camera -- and its contents have already been validated
    #     upstream (``StreamInfo`` for ``fps``, :class:`PipelineDetection` for the detections).
    #     The models in ``engine/contract`` and ``engine/manifest`` sit on cold paths and stay
    #     Pydantic; the hot path does not.
    #
    #     Frozen, with ``detections`` copied to a tuple and ``previous`` wrapped read-only, so a
    #     primitive cannot mutate the set the next primitive in the pipeline is about to see.

    def camera_id(self: Any) -> str:
        """
        The camera this frame came from, or ``""`` when no stream is attached.
        """
        ...

    def frame_id(self: Any) -> str:
        """
        The frame's media anchor, or ``""``. Useful when raising an event.
        """
        ...

    def of_entity(self: Any, *entities: Any) -> tuple[Any, ...]:
        """
        This frame's detections restricted to ``entities``.
        
                The one convenience on this type.  It is here rather than on a base class because
                every primitive needs it and none of them may inherit anything (``09`` §3) -- and
                it is a filter over data the caller already has, not a shared behaviour that could
                grow into another ``BaseProcessor``.
        """
        ...

    def require_resolution(self: Any, what: str) -> tuple[int, int]:
        """
        ``resolution``, or a loud error naming who needed it and why.
        
                Bounding boxes are normalized 0-1; anything expressed in pixels -- zone polygons,
                a px/s speed threshold, an inset distance -- needs this to be meaningful. Guessing
                a default produces output that is plausible and wrong by the ratio of the guessed
                frame size to the real one, which is far worse than not starting.
        """
        ...

    def resolution(self: Any) -> tuple[int, int] | None:
        """
        ``(width, height)`` in pixels, or ``None`` when unknown.
        
                ``None`` and ``(0, 0)`` both mean "not configured" and both come back as ``None``,
                so callers have one thing to check. Use :meth:`require_resolution` when the
                primitive cannot work without it.
        """
        ...

    def zone_config(self: Any) -> 'Any | None':
        """
        The camera's zone geometry, normalized 0-1, or ``None`` when unconfigured.
        """
        ...

class Keypoint:
    # One pose joint, ``(x, y, confidence)``, **normalized 0-1** like a bounding box.
    #
    #     A tuple rather than a model because that is the wire shape
    #     (``_contracts/04-asis-live-frame-contract.md:678-706``: a fixed-length list of
    #     ``[x, y, confidence]``) and because a skeleton is 17 of these per person per frame --
    #     validating a Pydantic model 425 times a second at 25 fps buys nothing that the intake
    #     parse has not already checked.
    #
    #     **Both coordinate conventions in one field is defect PY-7**, so there is only one here.
    #     The legacy tree's keypoints are absolute pixels -- ``hands_above_head_margin_px`` is
    #     compared directly against a joint ``y`` (``fence_climbing_detection_pose.py:139``) and
    #     ``head_h = shoulder_y - y1`` mixes a joint ``y`` with a bbox edge
    #     (``face_covering_detection_pose.py:175``) -- while every box in this engine is
    #     normalized 0-1 and a box outside that range is rejected outright (**BE-10**/**BE-12**).
    #     Mixing the two in one :class:`FrameContext` is how a silent 1920x error happens, so
    #     ``runtime/session.py`` normalizes at intake and everything downstream reads 0-1.
    #
    #     :attr:`confidence` is the per-joint visibility score.  **A payload with no confidence
    #     channel yields 0.0, never 1.0.**  Legacy forges ``1.0`` (``fall_detection.py:86``,
    #     ``:103``, ``:112``, and the same lines in both siblings), which makes every
    #     ``min_keypoint_confidence`` gate pass unconditionally whatever the manifest says -- a
    #     config field that cannot fail is worse than no field.

    ...
class MaskRef:
    # A segmentation mask as the engine carries it -- **a reference, not pixels**.
    #
    #     Engine-internal like :attr:`PipelineDetection.entity`, with one exception:
    #     :meth:`PipelineDetection.to_wire` re-emits :attr:`rle` (when present) as the wire's
    #     declared, RLE-only ``Detection.segmentation`` field -- never :attr:`polygon` or a
    #     rasterized :attr:`area_px`, since this engine does not encode pixels for the wire (no
    #     numpy/cv2, **PY-20**) and a decoded shape has nothing ready-to-emit.
    #
    #     Three carriers, because the producers ship three and each is cheaper than the last to
    #     turn into an area (``landslide_detection.py:283-313`` cascades over exactly these):
    #
    #     :attr:`area_px`
    #         A foreground pixel count already computed upstream
    #         (``merged_det["segmentation_area"] = mask_info["area_pixels"]``,
    #         ``landslide_detection.py:836``).  Free -- no decode at all.
    #     :attr:`rle`
    #         The base64 ``simple_rle`` the live producer sends
    #         (``_contracts/04-asis-live-frame-contract.md:657-671``).  Decoded by
    #         :func:`~matrice_analytics.engine.primitives.segmentation_area.decode_simple_rle_area`
    #         with ``base64`` and ``int.from_bytes`` -- **no numpy, no cv2** (**PY-20**).
    #     :attr:`polygon`
    #         A contour.  ``cv2.contourArea`` returns the unsigned shoelace area of a simple
    #         polygon, so the pure-Python shoelace in
    #         :func:`~matrice_analytics.engine.primitives.segmentation_area.polygon_area` is
    #         behaviour-preserving rather than an approximation.
    #
    #     :attr:`size` is the mask's **own** array shape, ``(height, width)``, in model input
    #     space.  It is the denominator, which is why ``segmentation_area`` needs no frame
    #     resolution: a mask covers the whole frame in model space, so ``area_px / (h * w)`` is
    #     resolution-free.  That is the choice legacy Tier 1 made
    #     (``landslide_detection.py:285-291``) and the reason this primitive never calls
    #     :meth:`FrameContext.require_resolution`.

    ...
class PipelineDetection:
    # A wire :class:`~matrice_analytics.engine.contract.schemas.Detection` plus the
    #     fields the pipeline adds before a primitive sees it.
    #
    #     ``09`` §3 says ``FrameContext.detections`` are "already entity-remapped and
    #     zone-assigned", but the wire ``Detection`` carries neither an ``entity`` nor a
    #     ``zone``: ``category`` is the *model's* class label, which is precisely what entity
    #     remapping exists to stop primitives from depending on.  Rather than redeclare the
    #     detection (the contract owns it -- **O1**), this subclasses it, so
    #     :class:`~matrice_analytics.engine.contract.schemas.BoundingBox`, the 0-1 range check
    #     (**BE-10**, **BE-12**) and the confidence check keep applying unchanged.
    #
    #     :meth:`to_wire` converts back.  Use it -- the extra two fields must not reach the
    #     payload, and ``extra="forbid"`` on the wire model means a stray one is a hard failure
    #     at emit rather than a silent extra key.

    def from_detection(cls: Any, detection: Any) -> 'Any':
        """
        Attach pipeline fields to a wire detection.
        
                ``mask`` and ``keypoints`` are keyword-only and default to "absent" because the wire
                :class:`~matrice_analytics.engine.contract.schemas.Detection` cannot carry them --
                they come from the raw producer dict, which ``runtime/session.py`` parses.
        """
        ...

    def to_wire(self: Any) -> Any:
        """
        Drop the pipeline-internal fields, yielding the contract's detection.
        
                ``entity`` and ``zone`` are engine concepts: the payload's per-zone structure
                already carries the zone (**FROZEN-2**) and its ``category`` is the model label the
                overlay draws.  Emitting either would be a new, undeclared wire field.
                :attr:`keypoints` is dropped for the same reason.
        
                :attr:`mask` is the one field that conditionally survives: its ``rle`` (when the
                producer sent a ready-to-emit ``simple_rle`` string) becomes ``Detection.segmentation``
                below, byte for byte -- a genuinely declared wire field (:class:`WireSegmentationMask`
                on :class:`Detection`), not a leak, since ``extra="forbid"`` would reject anything not
                named on that model.  A mask that only carries a polygon or a precomputed
                :attr:`~.MaskRef.area_px` has nothing ready-to-emit -- this method never rasterizes or
                encodes pixels (no numpy/cv2, **PY-20**) -- so ``segmentation`` stays ``None`` for it,
                same as for a detector-only stream.  This method still names every wire field
                explicitly rather than copying whatever :class:`PipelineDetection` happens to hold, so
                an engine-internal field cannot leak into a payload by being added upstream.
        """
        ...

class Primitive:
    # The one interface (``09`` §3).  A protocol, so there is nothing to inherit.
    #
    #     An implementation is any class with these members -- no registration in a base class,
    #     no ``super().__init__()``, no ``BaseProcessor``.  That is the point: the ~20 payload
    #     helpers and their duplicate deprecated twins accumulated on
    #     ``core/base.py:617-781`` *because* there was somewhere shared to put them.
    #
    #     Implementations are pure over ``(detections, state, config)``: given the same frames
    #     and the same starting state they produce the same outputs, which is what makes the
    #     generated determinism test (**O5**) meaningful.
    #
    #     Note:
    #         ``isinstance(obj, Primitive)`` checks only that the members exist -- that is all a
    #         ``runtime_checkable`` protocol can do.  Use :func:`conformance_problems` when you
    #         want the *reasons* something does not conform.

    def __init__(self: Any, config: Any, state: Any) -> None:
        """
        Construct with a validated config and an already-scoped state store.
        
                The store is scoped to ``<camera_id>/<app_id>/<zone>/<primitive>`` by the runtime,
                so an implementation writes bare names (``state.set("seen", ...)``) and cannot
                collide with another camera, app, zone or stage.
        
                **All** mutable state goes through ``state``.  A plain ``self._counts`` dict is a
                review defect: it is invisible to a future Redis backing (``09`` §4, **D6**).
        """
        ...

    def process(self: Any, ctx: Any) -> Any:
        """
        Handle one frame, in one zone.  No I/O, no threads, no models (``09`` §6).
        """
        ...

    def reset(self: Any) -> None:
        """
        Clear window-scoped state at the aggregation boundary.
        
                **Not** a full reset.  ``09`` §4 rule 2: window sums clear here; cumulative totals
                clear only when the process does (**FROZEN-4**).  Implementations express this by
                calling :meth:`~matrice_analytics.engine.state.store.StateStore.end_window`, or by
                clearing named keys -- what they must not do is clear a total, because the
                backend's rollup formula assumes those only reset on restart.
        """
        ...

    def window(self: Any, frames: Any[Any]) -> Any:
        """
        Collapse this stage's per-frame outputs into the 60-second aggregation.
        
                Given the outputs this same instance returned from :meth:`process` during the
                window, in frame order.
        """
        ...

class PrimitiveEvent:
    # An **incident candidate** -- something happened, at a frame time.
    #
    #     Deliberately not an incident: severity here is a free string and the runtime maps it
    #     through :func:`matrice_analytics.engine.contract.schemas.parse_severity` on the way to
    #     the wire.  A primitive that imported the wire ``Severity`` enum would know the wire
    #     format, and then so would the next one (**O1**).
    #
    #     Incident *lifecycle* -- confirmation frames, find-or-create on ``incident_id``,
    #     up-only escalation, closing -- belongs to the runtime, not here.  A primitive says
    #     "this is happening now"; nothing more.

    ...
class PrimitiveOutput:
    # What one pipeline stage produces for one frame, in one zone (``09`` §3).

    ...
class PrimitiveRegistrationError:
    # A class cannot be registered as a primitive implementation.

    ...
class PrimitiveRegistry:
    # Manifest primitive name -> implementation class.
    #
    #     This is how the runtime turns a validated manifest into a pipeline without knowing a
    #     single app's name (``09`` §1): it reads ``pipeline[].kind``, looks the class up here,
    #     and constructs it with the stage's already-validated config and a scoped state store.
    #
    #     The key set is closed -- it is
    #     :data:`matrice_analytics.engine.manifest.models.PRIMITIVES`, the same 17 names the
    #     manifest schema accepts.  Registering anything else raises, because a primitive no
    #     manifest can name is dead code and a manifest naming a primitive that is not here must
    #     fail loudly at load, not silently emit nothing.
    #
    #     Example:
    #         >>> registry = PrimitiveRegistry()
    #         >>> @registry.register
    #         ... class Detect:
    #         ...     name = "detect"
    #         ...     Config = DetectConfig
    #         ...     def __init__(self, config, state): ...
    #         ...     def process(self, ctx): return PrimitiveOutput()
    #         ...     def window(self, frames): return WindowOutput()
    #         ...     def reset(self): ...
    #         >>> registry.get("detect") is Detect
    #         True

    def __init__(self: Any) -> None: ...

    def create(self: Any, name: str, config: Any, state: Any) -> Any:
        """
        Instantiate the primitive registered for ``name``.
        
                Args:
                    name: The manifest primitive key.
                    config: The stage's validated config, an instance of the class's ``Config``.
                    state: A store already scoped to
                        ``<camera_id>/<app_id>/<zone>/<primitive>`` (``09`` §4).
        
                Returns:
                    The constructed primitive.
        
                Raises:
                    KeyError: Nothing is registered for ``name``.
                    TypeError: ``config`` is not an instance of the class's ``Config`` model.
        """
        ...

    def get(self: Any, name: str) -> Any[Any]:
        """
        The class registered for ``name``.
        
                Raises:
                    KeyError: Nothing is registered for it.  The message distinguishes "not
                        implemented yet" (``08`` §2 marks four primitives 🔜) from "not a
                        primitive at all", because the fix differs.
        """
        ...

    def missing(self: Any) -> tuple[str, ...]:
        """
        Manifest primitives with no implementation yet, sorted.
        
                The runtime's startup check: a manifest naming one of these must fail loudly
                (``09`` §5), and this is the list it fails against.
        """
        ...

    def names(self: Any) -> tuple[str, ...]:
        """
        Registered primitive names, sorted -- deterministic for tests and logs.
        """
        ...

    def register(self: Any, impl: Any[Any] | None = None) -> Any:
        """
        Register an implementation.  Usable bare or with an explicit name.
        
                ``@registry.register`` takes the key from ``cls.name``;
                ``@registry.register(name="detect")`` states it, and then ``cls.name`` must agree
                (two spellings of one key is how the legacy catalogue ended up with two
                registration lists that disagree -- ``09`` §9).
        
                Args:
                    impl: The class, when used as a bare decorator.
                    name: The manifest primitive key, when stated explicitly.
        
                Returns:
                    The class (bare form) or a decorator (keyword form).
        
                Raises:
                    PrimitiveRegistrationError: The name is unknown to the manifest schema,
                        already taken, disagrees with ``cls.name``, or the class does not conform.
        """
        ...

class PrimitiveValueError:
    # A :attr:`PrimitiveOutput.values` entry is not a publishable scalar.
    #
    #     Caught at construction rather than at emit: by the time the contract rejects a
    #     ``None`` the frame that produced it is gone, and the failure reads as "the payload is
    #     malformed" rather than "this primitive returned nothing for this key".

    ...
class SourceResolutionError:
    # A ``metrics[].source`` does not resolve against the pipeline's outputs.
    #
    #     ``09`` §3: *an unresolvable source is a manifest load error -- not a metric that reads
    #     zero forever*.  The current engine's silent-zero behaviour is indistinguishable from a
    #     genuinely quiet camera, which is why this raises.

    ...
class TrackState:
    # One tracked object as a primitive sees it.
    #
    #     Carried on :attr:`PrimitiveOutput.tracks` so that a later stage (``dwell``,
    #     ``velocity_state``, a custom primitive) can read it without re-implementing tracking --
    #     the thing every use case does today, and the reason 17 of them hand-rolled a dwell
    #     clock.

    def duration_seconds(self: Any) -> float:
        """
        How long this track has been observed, in frame time.
        """
        ...

class WallClock:
    # ``time.time()``, for the few places that genuinely mean wall-clock.
    #
    #     Never the default.  Passing this where a :class:`FrameClock` belongs is exactly
    #     **PY-13** (``engine_session.py:595``), so it is a named type you have to opt into
    #     rather than a bare call buried in a session.

    def now(self: Any) -> float:
        """
        Current wall-clock time in epoch seconds.
        """
        ...

class WindowOutput:
    # What one stage contributes to the 60-second aggregation (``09`` §3).
    #
    #     Separate from :class:`PrimitiveOutput` because it means something different: these
    #     values are already collapsed over the window and are published once, whereas a
    #     ``PrimitiveOutput.values`` entry is a per-frame sample that ``metrics[].agg_type`` still
    #     has to collapse.  Conflating the two is how a percentage gets published as a
    #     60-second *sum* (**PY-1**).
    #
    #     There are no ``tracks`` here: a track is a per-frame fact, and the window is over.

    ...
