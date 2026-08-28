"""Auto-generated stub for module: models."""
from typing import Any

# Constants
AcrossZonesLiteral: Any
AggTypeLiteral: Any
CategoryLiteral: Any
DerivedScopeLiteral: Any
MANIFEST_SCHEMA_VERSION: int
MIN_CONFIRM_FRAMES: int
PipelineStage: Any
SeverityLiteral: Any
logger: Any

# Functions
def resolve_derived(manifest: Any, spec: Any) -> Any:
    """
    Resolve one ``derived[]`` entry against the pipeline, or raise ``ValueError``.
    
        Three things happen here, and each of them is a load error rather than a runtime surprise:
    
        1. **every operand resolves**, through :func:`resolve_source` — the same function and the
           same message a bad ``metrics[].source`` gets;
        2. **the scope is one the operands support** — window if they are all already-aggregated
           window outputs, frame if they are all per-frame samples;
        3. **the two are not mixed** — an expression over one window-only and one frame-only
           operand has no scope at all, and the engine will not pick one and hope.
    
        Called by :meth:`AppManifest._check_derived` at load and by
        :func:`~matrice_analytics.engine.runtime.window.derived_plan` at session setup, so the
        scope the runtime uses is by construction the scope the loader approved.
    """
    ...
def resolve_source(manifest: Any, source: str) -> Any:
    """
    Resolve ``<stage>.<value>`` against a manifest's pipeline, or raise ``ValueError``.
    
        The stage name is the part before the first dot; everything after it is the value path, so
        dotted values (``detect.person.count``, ``unique_count.per_category.person``) resolve fine.
    
        With *allow_global_prefix*, a leading ``global.`` names the **bucket** instead of a stage:
        ``global.detect.person.count`` is "``detect.person.count``, read from the whole frame".
        Only ``derived[].expr`` passes this, because it is the only place that evaluates the same
        expression once per zone and can therefore need a number from outside the zone. A
        ``metrics[].source`` says which bucket it wants with ``zone:``, so the prefix there would
        be a second, contradictable way to state the same thing.
    
        A pipeline that really does contain a stage named ``global`` keeps it: the prefix is only
        stripped when ``global`` is *not* a declared stage, so an existing manifest cannot change
        meaning by acquiring this feature.
    """
    ...

# Classes
class AppManifest:
    # A complete ``app.yaml``.
    #
    #     Construct it through :func:`matrice_analytics.engine.manifest.loader.load_app` rather than
    #     directly, so that custom code and sibling files are checked too.

    def custom_stages(self: Any) -> tuple[Any, ...]: ...

    def derived_keys(self: Any) -> tuple[str, ...]: ...

    def geometry_requirements(self: Any) -> tuple[Any, ...]:
        """
        Per-camera geometry this app needs, so the runtime can fail loudly instead of counting
                zero (see :class:`GeometryRequirement`).
        """
        ...

    def metric_keys(self: Any) -> tuple[str, ...]:
        """
        ``metrics[]`` keys only — the sourced ones.
        
                Deliberately **not** widened to include ``derived[]``: this property answers "which
                keys does a stage output back", which is what the generated-test suite checks it for
                (``testing/generate.py``), and a derived key has no single stage behind it. Use
                :attr:`published_keys` for "every key that reaches the wire".
        """
        ...

    def published_keys(self: Any) -> tuple[str, ...]:
        """
        Every metric key this manifest puts on ``results-agg``, sourced and derived.
        
                The two lists share one namespace — the wire cannot tell them apart — so uniqueness is
                checked across both (:meth:`_check_derived`).
        """
        ...

    def resolved_derived(self: Any) -> tuple[Any, ...]:
        """
        Every ``derived[]`` entry, already checked, with its inferred scope.
        """
        ...

    def resolved_sources(self: Any) -> tuple[Any, ...]:
        """
        Every metric source, already checked. Empty for an incident-only app.
        """
        ...

    def stages(self: Any) -> dict[str, Any]:
        """
        Stage name → config, in pipeline order.
        """
        ...

    def unimplemented_primitives(self: Any) -> tuple[str, ...]:
        """
        Declared primitives the runtime has not built yet (``08`` §2).
        
                Not an error: the manifest is allowed to describe an app before the engine can run it. The
                runtime refuses at session start; the loader only reports.
        """
        ...

class AppSpec:
    # ``app:`` — identity. The registry key and its dashboard grouping.

    ...
class CustomConfig:
    # ``custom`` — the escape hatch (``08`` §9, ``09`` §6).
    #
    #     Custom code never touches the wire format, never re-implements a primitive, and never does
    #     network I/O or loads a model. Its ``values`` keys are known only to its Python, so metric
    #     sources under this namespace cannot be verified from the manifest alone; the loader checks the
    #     symbol and its ``Config`` instead.

    def all_in_one(self: Any) -> bool:
        """
        ``zones: all_in_one`` — the whole frame in one call, zones still on the detections.
        
                **The limitation it removes.** Zone assignment happens once, before the pipeline, and
                every stage then runs per zone bucket. That is right for every registered primitive and
                wrong for exactly one thing: a custom stage cannot observe a *transition* between
                zones — queue→counter, entry→exit, owner-leaves-object. In the ``Queue`` bucket every
                detection is stamped ``Queue`` by construction, the ``Counter`` bucket has its own
                isolated state scope, and the ``global`` bucket sees the whole frame but with no zone on
                any detection. No bucket sees the handoff, so the app has to redo point-in-polygon by
                hand — which is the one thing the partition exists to stop.
        
                **What the flag gives.** The stage runs **once**, in the ``global`` bucket, over every
                detection the partition kept, and each detection carries ``zone`` — the zone the
                session's own partition assigned it to, not one the app re-derived. So the transition is
                readable as ``det.zone``, and ``point_in_polygon`` stays out of app code.
        
                **State.** One instance means one store: ``<camera>/<app>/global/<stage>``. There is no
                per-zone store for this stage, because there is no per-zone instance to own one — which
                is the point, since a handoff clock written under ``Queue`` was invisible under
                ``Counter``.
        
                **Two caveats, both deliberate.** ``ctx.zone`` is ``"global"`` (the stage really is
                running in the whole-frame bucket; the per-detection zone is on the detections).  And
                under ``zones.on_overlap: all_match`` a detection is in several zone buckets but appears
                **once** here, carrying its first matching zone in drawing order — a whole-frame view
                that repeated it would double-count, and a handoff needs each track in one place.
        """
        ...

    def describe_outputs(self: Any) -> str: ...

    def output_patterns(self: Any) -> tuple[Any.Any[str], ...]: ...

class DerivedMetricSpec:
    # One entry in ``derived:`` — a metric computed from other stages' outputs.
    #
    #     ::
    #
    #         derived:
    #           - key: defect_rate
    #             agg_type: mean
    #             category: QUALITY
    #             unit: percent
    #             expr: defect_unique.new / inspected_unique.new * 100
    #
    #     On the wire this is an ordinary :class:`~matrice_analytics.engine.contract.schemas.MetricEntry`
    #     — the dashboard cannot tell a derived series from a sourced one, and must not be able to.
    #     The separate block is for the *author* and the *reviewer*: ``metrics[]`` reads one number a
    #     stage published, ``derived[]`` computes one, and those have different failure modes.
    #
    #     **``agg_type`` on a derived value — the rule this block exists to get right.**
    #
    #     ``scope`` decides it, and the default is inferred from the operands:
    #
    #     ``scope: window`` (the default when **every** operand is a window output)
    #         The expression is evaluated **once**, at the aggregation boundary, over numbers the
    #         producing stages already collapsed.  The result is therefore *already aggregated* and
    #         is published verbatim — the engine does **not** apply ``agg_type`` to it, for exactly
    #         the reason it does not apply ``agg_type`` to a
    #         :class:`~matrice_analytics.engine.primitives.base.WindowOutput` value (**PY-1**, §6b
    #         coupling 4).  ``agg_type`` still travels on the wire, because it is how the *backend*
    #         collapses these 60-second readings into its five-minute rollup.
    #         :attr:`ResolvedDerived.window_aggregated` is ``True``, which is the same flag
    #         :class:`ResolvedSource` uses to say the same thing.
    #
    #     ``scope: frame`` (the default when any operand is frame-only, e.g. ``line_crossing.present``
    #     or a ``custom`` stage's value)
    #         The expression is evaluated **per retained frame** and the samples are collapsed with
    #         ``agg_type`` (:func:`~matrice_analytics.engine.runtime.window.collapse`).  Here
    #         ``agg_type`` is load-bearing, and ``mean`` means "the mean of the per-frame rate over
    #         the frames that had one" — which is precisely what legacy ``loitering_percentage``
    #         published (``legacy_analytics_bridge.py``:1680-1686, 2561-2564).
    #
    #     Declaring a ``scope`` the operands cannot support is a load error rather than a silent
    #     reinterpretation.  So is mixing a window-only operand with a frame-only one: there is no
    #     scope in which that expression has a value, and the engine will not invent one.
    #
    #     **A zero denominator publishes 0.0.**  ``expr`` is evaluated by
    #     :mod:`matrice_analytics.engine.manifest.expr`, which returns *undefined* for a zero
    #     denominator; an undefined reading contributes no sample, and a metric with no samples
    #     publishes ``0.0``.  That matches all four legacy rate producers and it is the only
    #     behaviour that cannot put ``NaN`` on the wire, which costs the whole window (finding
    #     **F1**).

    def dimension(self: Any) -> str | None:
        """
        The unit's dimension, or ``None`` when no unit is declared.
        """
        ...

    def expression(self: Any) -> Any:
        """
        The parsed :attr:`expr`.
        
                Re-parsed on access, which costs microseconds and happens at load and at session
                setup only — never per frame.  The runtime keeps the parsed object in its plan
                (:func:`~matrice_analytics.engine.runtime.window.derived_plan`).
        """
        ...

class DetectConfig:
    # ``detect`` — thresholded class presence and counts. Universal; always first.
    #
    #     ``<entity>.count`` and ``total`` are *levels*, so the window publishes two genuinely
    #     different readings of each under two names: the value on the window's **last frame**
    #     (``detect.person.count`` — what ``agg_type: last`` means) and the window's **peak**
    #     (``detect.person.count_peak`` — what ``agg_type: max`` means).  Sourcing one name with two
    #     ``agg_type``\ s cannot produce two numbers, because the stage aggregated already; source the
    #     two names instead.

    def frame_output_names(self: Any) -> Any[str]: ...

    def window_output_names(self: Any) -> Any[str]: ...

class DwellConfig:
    # ``dwell`` — time-in-state per track. Written privately by 17 use cases, abstracted zero times.

    def silent_buckets(self: Any) -> Any[str]:
        """
        ``state: in_zone`` measures nothing without a zone, so it publishes nothing there.
        
                Two such buckets. ``unassigned`` holds the detections that matched *no* zone, which is
                the one place a time-in-zone reading cannot exist; publishing ``0`` instead put a
                permanent zero series on the wire next to the real per-zone one, and since ``unassigned``
                is an emission zone every window shipped both.
        
                ``global`` is silent for the same reason, but **only when the app is zoned**. There the
                bucket is every detection regardless of polygon, so no ``in_zone`` session opens; the
                published ``0`` fed a ``zone: global`` metric and, worse, every metric-threshold incident
                -- ``Session._active_for`` evaluates those in this bucket, so a threshold over a dwell
                metric could never fire on a zoned camera. When the app is **not** zoned, ``global`` is
                the whole frame and an ``in_zone`` dwell against it is a manifest error that
                ``primitives/dwell.py`` raises ``DwellGateError`` for -- silence would hide it.
        
                See ``primitives/dwell.py``, ``_measures_nothing``, which this must agree with exactly.
        """
        ...

class EmissionSpec:
    # ``emission:`` — cadence and windowing.

    ...
class GeometryRequirement:
    # A runtime geometry precondition that the manifest can state but cannot check.
    #
    #     Zone and line geometry is per-camera installation data on ``StreamInfo``, not manifest data
    #     (``08`` §5). ``line_crossing.method: abline`` nevertheless *implies* exactly two lines will be
    #     drawn. Recording the implication here lets the runtime fail loudly at session start with the
    #     manifest's own words, rather than counting zero crossings forever.

    def describe(self: Any) -> str: ...

class IdentityMatchConfig:
    # ``identity_match`` — watchlist match (plates, faces).
    #
    #     Not implemented. No primitive registers under ``identity_match``, so a manifest that used
    #     it validated cleanly and then failed at pipeline build with a bare registry ``KeyError``.
    #     ``IMPLEMENTED = False`` moves that discovery to load time, where
    #     :meth:`AppManifest.unimplemented_primitives` reports it and the loader logs it — the
    #     manifest still validates on purpose (``08`` §2), so an author can write the config ahead
    #     of the runtime.

    ...
class IncidentLifecycle:
    # When an incident opens, escalates and closes.
    #
    #     Two behaviours that surprise people and are not configurable: incidents cannot de-escalate (the
    #     backend ignores a downward severity change), and only an end time closes one — which is what
    #     ``close_after_empty_frames`` produces.

    ...
class IncidentQuantiseConfig:
    # ``incident_quantise`` — magnitude → severity.
    #
    #     Pick the strategy from what actually makes the situation worse: a bigger fire is a worse fire
    #     (``area_ratio``); one confidently-detected pistol is critical at any size (``max_confidence``);
    #     more potholes is worse (``count_based``).

    ...
class IncidentSpec:
    # ``incidents:`` — what reaches ``incident_res``.

    ...
class IncidentType:
    # One incident type — what reaches ``incident_res`` and becomes an alert in the UI.

    def interpolated_keys(self: Any) -> tuple[str, ...]:
        """
        The ``{metric_key}`` placeholders in ``human_text``.
        """
        ...

class KeypointPoseConfig:
    # ``keypoint_pose`` — skeleton-derived logic (fall detection, posture).

    ...
class LineCrossingConfig:
    # ``line_crossing`` — directional A/B counting.
    #
    #     Nothing here needs a ``_peak`` name: ``in`` / ``out`` / ``net`` / ``untracked`` are counts of
    #     *events*, so the window's sum is the only reading of them, and ``total_*`` are cumulative
    #     levels whose current value is the only reading of *those*.  ``present`` is the one exception
    #     and is deliberately **frame-only**: the stage publishes no window value for it, so the
    #     runtime collapses its per-frame samples with the metric's own ``agg_type`` — the one place
    #     ``agg_type`` is load-bearing against a registered primitive.

    def frame_output_names(self: Any) -> Any[str]:
        """
        The static set, plus conditional keys from ``expose_corridor_state`` and/or
                ``include_completed_crossings``.
        
                ``live_category.in``/``.out`` and ``per_category.in``/``.out`` only exist in
                ``process()``'s output when ``expose_corridor_state`` is on; ``in_track_ids``/
                ``out_track_ids`` only exist when ``include_completed_crossings`` is on (see each
                field's own docstring) — declaring them unconditionally in ``STATIC_OUTPUTS`` would let
                a metric source them on a manifest that never enables the flag, and the source would
                resolve at load time but read zero (or an empty string) forever at runtime, which is
                exactly the silent failure this conditional-set split exists to prevent.
        """
        ...

    def geometry_requirements(self: Any) -> tuple[Any, ...]:
        """
        ``abline`` infers direction from the order two parallel lines are crossed in.
        
                With one line there is no order and with three there is no pairing, so the direction is
                undefined and the counter silently reports zero. The runtime must fail loudly instead —
                this requirement is what it fails against.
        """
        ...

class ManifestModel:
    # Base for every manifest node.
    #
    #     ``extra="forbid"`` is not pedantry: an ignored key is how ``alerts:`` looked functional for two
    #     years while doing nothing (**PY-12**), and how a misspelt ``confidence_treshold`` reads as the
    #     default forever.

    model_config: Any

class MetricSpec:
    # One entry in ``metrics:`` — one series on the dashboard.
    #
    #     ``key`` is a *shared, producer-defined namespace*: it must match ``metrics.json``'s ``key``
    #     and ``widgets.json``'s ``dataKey`` character for character, and nothing anywhere validates the
    #     join (``06-vocabularies.md`` §13). Renaming one silently empties every chart and alert rule built
    #     on it, which is why a rename is a manifest ``version`` bump with a recorded migration.

    def dimension(self: Any) -> str | None:
        """
        The unit's dimension, or ``None`` when no unit is declared.
        """
        ...

class MetricThreshold:
    # The ``{">": 15}`` form of ``severity_from``, optionally graded by ``levels``.

    model_config: Any

    def operators(self: Any) -> dict[str, float]: ...

class ModelSpec:
    # ``model:`` — how the detector's class labels become analytics entities.
    #
    #     The right-hand side of ``entity_mapping`` is the single most common cause of an empty
    #     dashboard: it must match the model's labels character for character, including spaces and
    #     capitals (``FIELD_REFERENCE`` §4). Nothing can validate that here — we only have the manifest —
    #     so the schema validates everything around it and leaves the spelling to the author.

    def entities(self: Any) -> Any[str]:
        """
        The analytics entity names an app may refer to anywhere else in the manifest.
        """
        ...

class PrimitiveConfig:
    # Base class for every pipeline primitive config.
    #
    #     Subclasses declare:
    #
    #     ``PRIMITIVE``              the YAML key (``- detect:``) and the metric-source namespace
    #     ``STATIC_OUTPUTS``         the fixed **per-frame** ``values`` keys a metric may point at
    #     ``STATIC_WINDOW_OUTPUTS``  the fixed **window** keys, when they differ from the per-frame set
    #     ``REQUIRES``               primitives that must appear *earlier* in the pipeline
    #
    #     **Why the two output sets are separate.**  A registered primitive's
    #     :meth:`~matrice_analytics.engine.primitives.base.Primitive.window` output is published
    #     *as-is* — the stage already aggregated, so the runtime does not re-apply
    #     ``metrics[].agg_type`` on top (that re-application is **PY-1**).  A window key is therefore
    #     **already a specific reading**: ``detect.person.count`` at window scope is the count on the
    #     window's last frame and ``detect.person.count_peak`` is the window's high-water mark, and
    #     ``agg_type`` cannot turn one into the other.  Declaring the two sets apart is what lets a
    #     reviewer — and :func:`resolve_source`, via
    #     :attr:`ResolvedSource.window_aggregated` — say which of a stage's outputs ignore
    #     ``agg_type`` and which are per-frame samples the runtime really does collapse with it.

    def all_in_one(self: Any) -> bool:
        """
        Whether this stage runs **once over the whole frame** instead of once per zone.
        
                ``False`` here, and overridden only by :class:`CustomConfig` — see its ``zones:``
                field for the argument. Every registered primitive is written against one zone
                bucket: ``zone_occupancy`` counts the bucket it was handed, ``detect``'s counts feed
                ``zone: per_zone`` metrics, and the emission layer keys ``tracking_stats`` and
                ``agg_summary`` **by bucket**. A built-in that ran only in ``global`` would therefore
                publish nothing at all for the per-zone series, which is the silent-zero this engine
                exists to remove. The flag is a property rather than a field on this base class
                precisely so that ``zones: all_in_one`` under ``- detect:`` is an ``extra="forbid"``
                error at load rather than a setting that quietly empties a dashboard.
        """
        ...

    def describe_outputs(self: Any) -> str: ...

    def frame_output_names(self: Any) -> Any[str]:
        """
        Concrete ``values`` keys ``process()`` publishes **every frame**, given *this* config.
        
                These are per-frame samples.  A metric sourcing one of them that the stage's
                ``window()`` does not republish is the only case where this engine applies
                ``metrics[].agg_type`` to a registered primitive.
        """
        ...

    def geometry_requirements(self: Any) -> tuple[Any, ...]: ...

    def output_names(self: Any) -> Any[str]:
        """
        Every key a ``metrics[].source`` may name: the per-frame set ∪ the window set.
        """
        ...

    def output_patterns(self: Any) -> tuple[Any.Any[str], ...]:
        """
        Patterns for outputs whose names are only known at runtime (per-zone counts).
        """
        ...

    def silent_buckets(self: Any) -> Any[str]:
        """
        Buckets where this stage runs but publishes **nothing**, by construction.
        
                Almost always empty: a stage runs in every bucket and has a reading for each. ``dwell``
                with ``state: in_zone`` is the exception -- ``unassigned`` is the *absence* of a zone,
                so no session can open there and the honest answer is silence, not ``0`` (``09`` §3).
        
                Declared on the config rather than discovered from the primitive because the callers
                that need it -- the generated ``metric_presence`` check, which would otherwise report
                the silence as an unpublished series -- read the manifest and never construct a
                primitive. Same reason :attr:`STATIC_OUTPUTS` lives here.
        
                Args:
                    zoned: Whether the app partitions detections at all. Keyword-only with a default so
                        every existing caller keeps working; it matters only to ``dwell``, where the
                        ``global`` bucket is silent when zoned and a hard error when not.
        """
        ...

    def stage_name(self: Any) -> str:
        """
        The namespace ``metrics[].source`` resolves against.
        """
        ...

    def window_output_names(self: Any) -> Any[str]:
        """
        Concrete ``values`` keys ``window()`` publishes at the aggregation boundary.
        
                Already aggregated, and published verbatim — see the class docstring.  Defaults to
                :meth:`frame_output_names` because most primitives republish the same key set.
        """
        ...

    def window_output_patterns(self: Any) -> tuple[Any.Any[str], ...]:
        """
        The subset of :meth:`output_patterns` that ``window()`` publishes.
        
                Defaults to all of them; only ``zone_occupancy`` has runtime-named outputs at all, and
                it publishes every one of them at both scopes.
        """
        ...

class ProximityConfig:
    # ``proximity`` — inter-object distance.
    #
    #     Pixel↔metre calibration has no home in ``StreamInfo`` today (``08`` §10), so ``calibration``
    #     is a free-form block until that is settled; distances are in pixels meanwhile.

    ...
class QuantiseLevel:
    # One rung of the severity ladder: at or above ``percentage``, the severity is ``level``.

    ...
class RatioComplianceConfig:
    # ``ratio_compliance`` — "what fraction of X satisfies Y".

    def frame_output_names(self: Any) -> Any[str]: ...

class ResolvedDerived:
    # A ``derived[]`` entry whose expression has been checked against the pipeline.

    def window_aggregated(self: Any) -> bool:
        """
        ``True`` when the engine must publish this value **verbatim**.
        
                The same statement :attr:`ResolvedSource.window_aggregated` makes, for the same
                reason: a number computed from already-aggregated inputs is already aggregated, and
                re-applying ``metrics[].agg_type`` to it is **PY-1**.
        """
        ...

class ResolvedSource:
    # A ``metrics[].source`` that has been checked against the pipeline.

    ...
class SegmentationAreaConfig:
    # ``segmentation_area`` — mask area over frame area.

    ...
class SkipEntry:
    # A skipped generated test, and why.
    #
    #     A bare skip is how a suite rots: nobody can tell an intentional gap from an abandoned one.

    ...
class SmoothingConfig:
    # The five-field bbox-smoothing block that 105 of 123 existing configs carry *identically*.
    #
    #     First-class with defaults precisely so nobody writes it again (``08`` §1).

    ...
class StateMachineConfig:
    # ``state_machine`` — N-of-M confirmation with persistence/recovery hysteresis.

    ...
class TestsSpec:
    # ``tests:`` — extra configuration for the *generated* suite (``08`` §7).
    #
    #     An empty block is the norm. A config-only app writes no tests at all.

    ...
class ThresholdLevel:
    # One rung of a graded ``severity_from`` threshold.

    ...
class TrackConfig:
    # ``track`` — ID association.
    #
    #     These knobs are hard-coded in ``engine_session.py:483`` today and no manifest can influence
    #     them; that is why every use case ships its own tracker copy.

    ...
class UniqueCountConfig:
    # ``unique_count`` — "how many distinct ones have I seen".
    #
    #     ``total`` means *since the process last restarted*, not all time. The backend's rollup formula
    #     depends on exactly that (FROZEN-4); do not try to make it absolute.

    def frame_output_names(self: Any) -> Any[str]: ...

class VelocityStateConfig:
    # ``velocity_state`` — per-track speed, heading and stationarity.
    #
    #     Consolidates ten spellings of one concept found across six use cases
    #     (``velocity_threshold_px_per_sec``, ``short_term_displacement_threshold_px``,
    #     ``movement_threshold_percent``, …). Naming it once is most of the value (``08`` §2).

    def frame_output_names(self: Any) -> Any[str]:
        """
        The static set, plus `live_category.*` when `expose_wrong_way_state` is set.
        
                Mirrors ``LineCrossingConfig.frame_output_names`` -- see its docstring for why these
                are conditional rather than always declared in ``STATIC_OUTPUTS``: a metric sourcing
                ``live_category.wrong_way`` on a manifest that never sets the flag would resolve at
                load time but read zero forever at runtime, the exact silent failure the conditional
                split exists to prevent.
        """
        ...

    def geometry_requirements(self: Any) -> tuple[Any, ...]:
        """
        ``heading_from_line`` needs exactly one line to have an unambiguous direction.
        
                With no line there is nothing to derive a direction from; with two or more, which one
                is "the" reference direction is undefined -- the same reasoning
                ``LineCrossingConfig.geometry_requirements`` applies to ``abline``'s two lines, one line
                short of it here.
        
                ``heading_auto_learn_fallback`` turns "no line" from a fatal precondition into a
                supported, if temporary, state -- zero lines is no longer declared as a startup
                requirement here, matching ``zone_occupancy``'s own documented no-geometry fallback
                (``09._check_geometry``'s ``minimum``, warning-only branch). Two or more lines stays
                undefined regardless: the fallback exists for "nothing drawn yet", not "which of these
                do you mean", so that case is still refused, at construction
                (:meth:`VelocityState._resolve_expected`) rather than declared here.
        """
        ...

class ZoneOccupancyConfig:
    # ``zone_occupancy`` — polygon membership and per-zone counts.
    #
    #     ``peak_occupancy`` / ``avg_occupancy`` are published **both** per frame and at the window
    #     boundary: per frame they are the high-water mark and mean *so far this window* (the same
    #     accumulators the window reading reads, exposed one frame earlier); at the boundary they are
    #     the window's final answer.  ``unassigned_count`` is this window's loss and
    #     ``unassigned_total`` the loss since process start (**FROZEN-4**).  All four were published
    #     and *not declared here* at one time or another, which made ``source:
    #     zone_occupancy.peak_occupancy`` a load error for a number the stage was already computing —
    #     the same mistake, twice, is why both output sets are declared explicitly rather than assumed.

    def frame_output_names(self: Any) -> Any[str]: ...

    def geometry_requirements(self: Any) -> tuple[Any, ...]: ...

    def output_patterns(self: Any) -> tuple[Any.Any[str], ...]: ...

    def window_output_names(self: Any) -> Any[str]: ...

class ZonesSpec:
    # ``zones:`` — how per-camera geometry is interpreted. Not the geometry itself.
    #
    #     Geometry is per-camera installation data on ``StreamInfo``, normalized 0-1. The manifest
    #     describes the use case, not the installation (``08`` §5).

    ...
