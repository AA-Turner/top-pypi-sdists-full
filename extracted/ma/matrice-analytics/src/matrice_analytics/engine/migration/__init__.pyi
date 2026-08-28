"""Stub file for engine.migration directory."""
from typing import Any

# Constants
logger: Any = ...  # From harness

# Functions
# From differ
def diff_results_agg(legacy: Any[str, Any] | None, new: Any[str, Any] | None) -> Any:
    """
    Compare two ``results-agg`` payloads structurally and classify every difference.
    
        The three parts of the payload are compared three different ways, because they are
        three different shapes (contract §2):
    
        * **the envelope** -- field by field, split into identity (BREAKING) and label
          (BENIGN) fields;
        * **``tracking_stats``** -- zone-keyed (**FROZEN-2**), and for every zone all four
          count lists (**PY-2**/**FROZEN-5**), matched by ``category``;
        * **``metrics[]``** -- matched by ``(key, zone)``, **never by list position**: the
          array's order is not contractual, the backend indexes by ``key``, and a positional
          comparison both invents differences and hides an ``agg_type`` swap.
    
        Args:
            legacy: The legacy ``results-agg`` payload, or ``None`` when the legacy side
                produced nothing (then ``legacy_error`` should say why).
            new: The new engine's ``results-agg`` payload.
            context: Facts the deliberate-change predicates need.  ``global_counts_agree`` is
                filled in here and any caller-supplied value is overwritten.
            tolerance: What may be forgiven.  See :class:`TolerancePolicy`.
            key_map: The verification-only metric-key correspondence
                (:mod:`~matrice_analytics.engine.migration.keymap`).  Defaults to the map
                registered for ``context.usecase``, or an empty one -- in which case every key
                that differs in spelling is BREAKING, which is the safe default.  Pass
                :data:`~matrice_analytics.engine.migration.keymap.EMPTY_KEY_MAP` explicitly to
                see the raw, unmapped truth.
            legacy_error: Why the legacy side produced nothing.  Forces
                :attr:`Verdict.LEGACY_UNAVAILABLE`.
            notes: Free-text findings for the report.
    
        Returns:
            A :class:`DiffReport`.  :attr:`DiffReport.passed` is the verdict.
    """
    ...

# From harness
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

# From harness
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

# From harness
def dump_frames_to_json(frames: Any[Any], path: str | Any.Any[str]) -> None:
    """
    Write a frame sequence to JSON, so a failing wave can archive its exact input.
    """
    ...

# From harness
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

# From harness
def load_frames_from_json(path: str | Any.Any[str]) -> tuple[Any, ...]:
    """
    Read a frame sequence back from the JSON :func:`dump_frames_to_json` writes.
    
        Recorded frames from a real camera are strictly better evidence than synthetic ones;
        this is the seam for them, and it keeps the format one thing.
    """
    ...

# From harness
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

# From harness
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

# From keymap
def key_map_for(usecase: str) -> Any:
    """
    The verification key map for a legacy use case.
    
        Args:
            usecase: The legacy use-case name, e.g. ``people_counting``.
    
        Returns:
            Its :class:`UsecaseKeyMap`, or :data:`EMPTY_KEY_MAP` when none is registered.  An
            unregistered use case is **not** an error: it means no key correspondence has been
            established yet, and every key difference stays BREAKING until one is.
    """
    ...

# Classes
# From differ
class Classification:
    # What one difference means for a migration wave.

    BENIGN: str
    BREAKING: str
    IMPROVEMENT: str


# From differ
class DeliberateChange:
    # A known, intended behaviour change -- recognised, never flagged as breakage.
    #
    #     The ``citation`` is the point of this class.  Without it, "we meant to do that" is
    #     unfalsifiable, and a real regression that happens to look like an intended change gets
    #     waved through by whoever is running the wave that day.

    def explains(self: Any, difference: Any, context: Any) -> bool:
        """
        Whether this registered change accounts for ``difference``.
        """
        ...


# From differ
class DiffContext:
    # Facts about the port that some classifications depend on.
    #
    #     A difference cannot be classified from its two values alone.  "This zone count moved
    #     by one" is BREAKING for an app that never changed its reference point and an
    #     IMPROVEMENT for one that did -- so the deliberate-change predicates read this.

    ...

# From differ
class DiffReport:
    # The structured answer, plus the one bit a migration wave needs.

    def benign(self: Any) -> tuple[Any, ...]: ...

    def breaking(self: Any) -> tuple[Any, ...]: ...

    def improvements(self: Any) -> tuple[Any, ...]: ...

    def passed(self: Any) -> bool:
        """
        Does this port pass?  True only for :attr:`Verdict.PASS`.
        """
        ...

    def render(self: Any) -> str:
        """
        The readable report the CLI prints.
        """
        ...

    def to_dict(self: Any) -> dict[str, Any]:
        """
        The full JSON report -- what ``--json`` prints and what a wave archives.
        """
        ...

    def verdict(self: Any) -> Any:
        """
        ``PASS`` / ``FAIL`` / ``LEGACY_UNAVAILABLE`` -- see :class:`Verdict`.
        """
        ...


# From differ
class Difference:
    # One place the two payloads disagree, and what that disagreement means.

    def is_breaking(self: Any) -> bool: ...

    def render(self: Any) -> str:
        """
        One line for the human-readable report.
        """
        ...

    def to_dict(self: Any) -> dict[str, Any]:
        """
        The JSON form the ``--json`` CLI mode emits.
        """
        ...


# From differ
class TolerancePolicy:
    # What the comparison is allowed to forgive, stated explicitly.
    #
    #     Every entry exists because the two engines *provably* differ on it for a reason that
    #     cannot reach a consumer.  Nothing here is a convenience.
    #
    #     Attributes:
    #         float_abs_tol: Absolute tolerance on ``metrics[].data``.  ``data`` is a float on
    #             the wire (contract §1 rule 6) and both engines reach it through a different
    #             number of float operations -- a percentage computed as ``a / b * 100`` differs
    #             in the last bit depending on the order.  Counts are **ints** and get no
    #             tolerance at all (see :attr:`int_counts_are_exact`).
    #         float_rel_tol: Relative tolerance, for the same reason at large magnitudes.
    #         timestamps_may_differ: Every timestamp is allowed to differ.  The legacy window
    #             boundary and its ``input_timestamp`` come from ``time.time()``
    #             (``legacy_analytics_bridge.py:3009,3013``); the new engine's come from frame
    #             time (**PY-13**).  They therefore *always* differ, on every run, and a policy
    #             that called that BREAKING would never pass anything.
    #         uuids_may_differ: A value that is a UUID on both sides may differ.  Ids are
    #             opaque to every consumer except the backend's find-or-create, which only needs
    #             them stable *within* a stream, not equal *across* engines.
    #         empty_string_equals_absent: ``""`` and an absent key are the same value for an
    #             optional string.  Contract §1 rule 7 forbids ``None`` and requires ``""``;
    #             ``to_payload`` uses ``exclude_none=True`` so an unset optional simply does not
    #             serialise.  Both spellings reach the Go parser as the zero value.
    #         absent_count_is_zero: A category absent from a count list is a count of zero.
    #             The legacy builder emits an explicit ``{"category": "person", "count": 0}``;
    #             the new engine omits the entry.  A dashboard cannot tell them apart.
    #         int_counts_are_exact: Counts are never tolerated.  ``current_counts`` feeds
    #             ``raw_analytics.count``, the primary series -- one person of drift there is
    #             exactly the class of bug this harness exists to catch.
    #         ignored_paths: Paths never compared, for diagnostics that are not payload.

    def numbers_equal(self: Any, left: float, right: float) -> bool:
        """
        Whether two floats are equal under this policy.
        """
        ...


# From differ
class Verdict:
    # The single answer a migration wave asks for.

    FAIL: str
    LEGACY_UNAVAILABLE: str
    PASS: str


# From harness
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


# From harness
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


# From harness
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


# From keymap
class MetricKeyPair:
    # Two spellings of one measurement: a legacy key and its new-engine counterpart.
    #
    #     Attributes:
    #         legacy_key: ``metrics[].key`` as the legacy bridge publishes it.
    #         new_key: ``metrics[].key`` as the manifest publishes it.
    #         evidence: What settles the claim that these are the same measurement -- a
    #             payload-diff run in which both sides read the same value, or the ``file:line``
    #             that produces each.  **Required.**  Without it the pairing is an opinion, and an
    #             opinion that suppresses a difference is how a regression gets promoted.
    #         note: Anything a reviewer needs beyond the evidence.

    ...

# From keymap
class MetricSide:
    # Which payload a key appears on.

    LEGACY: str
    NEW: str


# From keymap
class UnpairedMetricKey:
    # A key that **deliberately** has no counterpart -- not a key nobody has looked at.
    #
    #     ``occupancy_percentage`` is legacy-only because it is a fraction of a configured
    #     capacity, and the new engine is given no capacity; ``peak_occupancy`` is new-only
    #     because legacy never computed a within-window maximum.  Neither is a rename waiting to
    #     be found, so neither is BREAKING -- but both are *reported*, because a metric that
    #     stops being published is a chart that stops drawing, and the app owner has to know.
    #
    #     Attributes:
    #         key: The metric key.
    #         side: Which payload it appears on.  A key registered ``NEW`` that turns up on the
    #             **legacy** payload is *not* explained by this entry and stays BREAKING -- the
    #             registration is a statement about one side, not a blanket amnesty for the name.
    #         rationale: Why no counterpart exists.  Not "we did not port it": what it measures,
    #             and why the other engine has nothing that measures it.
    #         evidence: Doc section or ``file:line``.  **Required.**

    ...

# From keymap
class UsecaseKeyMap:
    # One legacy use case's metric-key correspondence.
    #
    #     Keyed by the *legacy* use-case name, because that is the side being retired and the side
    #     the harness is invoked with (``payload_diff.py --usecase``).

    def is_empty(self: Any) -> bool:
        """
        Whether this map says nothing -- every key is then unmapped, hence BREAKING.
        """
        ...

    def legacy_key_for(self: Any, new_key: str) -> str | None:
        """
        The legacy key this new-engine key should be compared against.
        """
        ...

    def new_key_for(self: Any, legacy_key: str) -> str | None:
        """
        The new-engine key this legacy key should be compared against.
        """
        ...

    def pair_for_legacy(self: Any, legacy_key: str) -> Any | None:
        """
        The pairing that claims ``legacy_key``, if any.
        """
        ...

    def pair_for_new(self: Any, new_key: str) -> Any | None:
        """
        The pairing that claims ``new_key``, if any.
        """
        ...

    def unpaired_for(self: Any, key: str, side: Any) -> Any | None:
        """
        The "deliberately has no counterpart" entry for ``key`` **on that side**.
        
                Side-sensitive on purpose: ``current_occupancy`` is registered as new-only, so a
                ``current_occupancy`` that shows up on the *legacy* payload is unexplained and stays
                BREAKING.
        """
        ...


from . import differ, harness, keymap