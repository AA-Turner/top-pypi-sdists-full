"""Auto-generated stub for module: harness."""
from typing import Any

# Constants
logger: Any

# Functions
def compare_usecase(legacy_usecase: str, manifest_path: str | Any.Any[str], frames: Any[Any] | Any) -> Any:
    """
    Feed identical frames to both engines and diff the ``results-agg`` they emit.
    
        This is the whole gate.  Both engines get the *same* :class:`SyntheticFrame` sequence
        and the *same* untyped ``stream_info``; the only conversion is normalized-to-pixel for
        the legacy side, which is that tree's stated input contract
        (``runtime/post_proc_runner.py``, "bbox contract").
    
        Args:
            legacy_usecase: The legacy use-case name being retired.
            manifest_path: The new app's folder or ``app.yaml``.
            frames: A :class:`FrameSequence` or any sequence of :class:`SyntheticFrame`.
            stream_info: The untyped worker dict.  Defaults to :func:`default_stream_info`
                with ``application_key_name`` set to ``legacy_usecase``.
            resolution: Source ``(width, height)``.
            tolerance: What may be forgiven.  See
                :class:`~matrice_analytics.engine.migration.differ.TolerancePolicy`.
            legacy_category: The legacy registry category, when the lookup cannot find it.
    
        Returns:
            A :class:`~matrice_analytics.engine.migration.differ.DiffReport`.
            :attr:`~...DiffReport.passed` is the verdict a wave acts on.
    """
    ...
def default_stream_info() -> dict[str, Any]:
    """
    The untyped worker ``stream_info`` dict both engines are given (surface S4).
    
        Intentionally the *nested, mixed-casing* shape a real worker sends rather than the
        typed model: ``engine_session.py:263-389`` reverse-engineers this across five nested
        lookup paths in two casings, and that function *is* the undocumented input contract.
        Feeding both engines the identical dict is the only way a payload difference can be
        attributed to the pipeline rather than to the two parsers.
    
        Every identity field is written at **both** the top level and inside ``camera_info``,
        because the two parsers do not read the same path: the new engine's
        :func:`~...runtime.stream_info.resolve_stream_info` prefers ``camera_info.camera_group``
        while the legacy ``extract_stream_context`` reads only
        ``stream_info["camera_group"]`` / ``input_settings["camera_group"]`` and otherwise
        substitutes the literal ``"default_group"``
        (``utils/legacy_analytics_bridge.py:1337``).  Supplying the union is not papering over
        anything -- it removes a *parser* difference from a comparison that is about the
        *analytics*.  That the union is necessary at all is the input contract's own defect and
        is reported separately, not silenced.
    """
    ...
def dump_frames_to_json(frames: Any[Any], path: str | Any.Any[str]) -> None:
    """
    Write a frame sequence to JSON, so a failing wave can archive its exact input.
    """
    ...
def generate_frames(frames: int = 250) -> Any:
    """
    Build a deterministic synthetic detection sequence.
    
        The sequence exercises the four temporal behaviours the counting/geometry/temporal
        primitives are built around, so a diff over it is not just a diff over "some boxes":
    
        * **entering and leaving** -- object ``k`` appears at frame ``k*frames//(2*objects)``
          and disappears at ``frames - k*frames//(4*objects)``, so the population rises and
          falls and ``current_counts`` is not a constant.  A constant occupancy makes ``sum``,
          ``mean``, ``max`` and ``last`` indistinguishable, which is exactly the four agg types
          **PY-1** confuses.
        * **crossing a line** -- two thirds of the objects traverse the frame horizontally,
          crossing ``x = 0.5`` once, at a frame determined only by their entry frame.  One of
          them travels right-to-left so a direction-aware counter sees both signs.
        * **dwelling in a zone** -- every third object sits inside :data:`DWELL_ZONE` for its
          whole life with a small, periodic, integer-driven wobble, so ``dwell`` measures a
          duration a test can predict and ``velocity_state`` reports ``stationary``.
        * **stable ids** -- motion per frame is a fraction of a box width, which is what lets
          both trackers keep an object's identity across frames.  Without that, ``unique_count``
          counts each person once per frame: the classic "the numbers are far too high" report.
    
        There is **no randomness**: every position is a closed-form function of
        ``(object index, frame index)``.  ``random.Random(seed)`` would also be reproducible,
        but only for as long as nobody adds a draw in the middle, and the failure is silent.
    
        Args:
            frames: How many frames to generate.  At the default 25 fps, 250 frames is 10 s of
                frame time -- comfortably inside one 60-second aggregation window, so both
                engines produce exactly one comparable window.
            objects: How many distinct objects appear over the sequence.
            fps: Frame rate, used for the frame timestamps.  Must be > 0.
            base_ts: Epoch seconds for frame 0.
            category: The model label every detection carries.  Must match the right-hand side
                of the app's ``model.entity_mapping`` character for character, or the new engine
                counts every detection as unmapped and every number is zero.
            resolution: Source ``(width, height)``, for :meth:`SyntheticFrame.pixel_detections`.
    
        Returns:
            A :class:`FrameSequence`.
    
        Raises:
            ValueError: ``frames`` < 1, ``objects`` < 1 or ``fps`` <= 0.
    """
    ...
def load_frames_from_json(path: str | Any.Any[str]) -> tuple[Any, ...]:
    """
    Read a frame sequence back from the JSON :func:`dump_frames_to_json` writes.
    
        Recorded frames from a real camera are strictly better evidence than synthetic ones;
        this is the seam for them, and it keeps the format one thing.
    """
    ...
def run_legacy(usecase: str, frames: Any[Any]) -> Any:
    """
    Run the legacy ``PostProcessor`` over ``frames`` and collect its ``results-agg``.
    
        **Every import here is lazy and local.**  ``matrice_analytics.post_processing``
        executes ~180 modules and pulls in torch and cv2 (**PY-20**, fixed for the engine
        only), so importing this harness must not pay that cost and must not fail on a box
        without those wheels.
    
        Two adjustments are made to the legacy accumulator, both because its window boundary is
        wall-clock (``legacy_analytics_bridge.py:3009``) and the comparison needs a window that
        covers the same frames as the new engine's:
    
        1. ``last_agg_publish_ts`` is pinned to *now* before the first frame and re-pinned after
           every frame.  Without the first pin the very first frame publishes an **empty**
           window, because the gate is ``if not force and self.last_agg_publish_ts and ...`` and
           zero is falsy.  Without the re-pin, a sequence that takes over 60 s of wall time
           splits into windows at positions that depend on how busy the machine is.
        2. Exactly one publish is then forced (``force=True``), covering every frame.
    
        Args:
            usecase: The legacy use-case name, e.g. ``people_counting``.
            frames: The sequence from :func:`generate_frames`.
            stream_info: The untyped worker dict -- the *same* one the new engine gets.
            resolution: Source ``(width, height)``; the legacy tree is fed pixel boxes.
            index_to_category: Class index -> model label.  Derive it from the manifest so both
                engines see the same class list.
            legacy_category: The registry category the use case is registered under.  Resolved
                from the legacy registry when omitted.
            config_overrides: Extra keys merged into the legacy config dict.
    
        Returns:
            An :class:`EngineRun`.  ``error`` is set rather than raised: "the legacy side will
            not run" is a finding, and it is the finding that decides whether an app can be
            diffed at all.
    """
    ...
def run_new_engine(manifest_path: str | Any.Any[str], frames: Any[Any]) -> tuple[Any, Session]:
    """
    Run the new engine over ``frames``: ``load_app_bundle -> Session -> process_frame``.
    
        The chain is ``STAGE_BC_PLAN`` §4's, with nothing stubbed but the transport.
    
        Args:
            manifest_path: The app folder or ``app.yaml`` -- anything
                :func:`~matrice_analytics.engine.manifest.loader.load_app_bundle` resolves.
            frames: The sequence from :func:`generate_frames`.
            stream_info: The untyped worker dict.  Defaults to :func:`default_stream_info`.
    
        Returns:
            ``(run, session)``.  The session is returned because the comparison needs facts
            only it knows -- ``emission_zones`` and the resolved reference point -- to build the
            :class:`~matrice_analytics.engine.migration.differ.DiffContext`.
    
        Raises:
            AppLoadError: The manifest is invalid.  A migration wave should not swallow that.
            SessionError: The manifest cannot run against this stream.
    """
    ...

# Classes
class EngineRun:
    # Everything one engine emitted over one frame sequence.

    def window(self: Any) -> dict[str, Any] | None:
        """
        The ``results-agg`` payload to compare -- the **last** one published.
        
                Both adapters are arranged so exactly one window covers the whole sequence.  When
                more than one arrives (a sequence longer than 60 s of frame time, or a legacy
                wall-clock boundary that fired anyway) the last is the complete one and a note says
                how many there were.
        """
        ...

class FrameSequence:
    # A generated sequence plus the facts a test or a report wants to state.

    def digest(self: Any) -> str:
        """
        sha256 of the canonical JSON of every detection, ids included.
        
                The determinism assertion in one value: two runs of :func:`generate_frames` with
                the same arguments have the same digest, on any machine, under any
                ``PYTHONHASHSEED``.  That last part is not hypothetical -- **PY-9** was a tracker
                namespace randomised by the hash seed.
        """
        ...

    def span_seconds(self: Any) -> float:
        """
        Frame-time span.  Under 60 s means exactly one aggregation window.
        """
        ...

    def unique_objects(self: Any) -> int:
        """
        How many distinct ground-truth ids appear at all.
        """
        ...

class SyntheticFrame:
    # One frame of detections, in the shape the inference pipeline really sends.

    def pixel_detections(self: Any, resolution: tuple[int, int]) -> list[dict[str, Any]]:
        """
        The same detections in source-pixel coordinates.
        
                The legacy tree is fed source-pixel boxes -- ``runtime/post_proc_runner.py`` states
                it as the caller's contract ("Callers must supply detections already in
                SOURCE-PIXEL coordinates") -- while the new engine is normalized 0-1 by contract §4.
                Converting here, from one generator, is what keeps "the same input" true.
        """
        ...

