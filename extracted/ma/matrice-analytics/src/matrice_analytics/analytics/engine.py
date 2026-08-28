"""AnalyticsEngine — main orchestrator for the category-processor framework.

Loads a YAML manifest, instantiates the corresponding category processors,
and dispatches per-frame detections. Manages the 1-minute aggregation timer.

Zone analytics is always active for every metric-based category (VOLUME,
QUALITY, SAFETY, ...).  When no explicit zone polygons are configured, a
default ``"global"`` zone is used that covers the entire frame.  When zone
polygons are present in ``StreamInfo.zone_config.zones``, one processor of
each loaded metric category is instantiated **per zone**, and detections
are assigned by point-in-polygon containment before reaching any processor.

INCIDENT is intentionally zone-agnostic: it consumes all detections and
drives the standalone lifecycle state machine.

Usage::

    engine = AnalyticsEngine("people_counting_new")
    for frame in frames:
        result = engine.process_frame(frame.detections, frame.ts, frame.id)
        if engine.should_aggregate(frame.ts):
            agg = engine.aggregate()
"""
from __future__ import annotations

import importlib
import logging
from pathlib import Path
from typing import Any

import yaml

from .base_processor import BaseMetricProcessor
from .geometry import assign_detections_to_zones, build_zone_polygons_px
from .schemas import (
    AggregationResult,
    FrameResult,
    FrameSummaryEntry,
    IncidentEvent,
    IncidentMessage,
    InputStreamEntry,
    InputStreamInfo,
    ResultValue,
    ResultWrapper,
    StreamInfo,
    TrackingStats,
)


logger = logging.getLogger(__name__)

# Default aggregation interval in seconds
_DEFAULT_AGG_INTERVAL_SEC = 60.0


class AnalyticsEngine:
    """Orchestrator that reads a YAML manifest and dispatches frames to processors.

    Zone analytics is always active for every metric-based category.  When
    ``StreamInfo.zone_config.zones`` contains named polygons, one processor
    of each loaded metric category (VOLUME, QUALITY, SAFETY, ...) is created
    **per zone** and detections are assigned via point-in-polygon containment
    before reaching any processor.  Otherwise a single ``"global"`` zone
    receives all detections.

    Internal layout:

    - ``_zone_metric_processors``: ``{zone_name: {category: processor}}``
      — all zone-aware processors, nested by zone then category.
    - ``_incident_processor``: the standalone INCIDENT processor (no zones).
    """

    def __init__(
        self,
        manifest_path_or_name: str,
        stream_info: StreamInfo | dict[str, Any] | None = None,
    ) -> None:
        """Load a YAML manifest and instantiate category processors.

        Args:
            manifest_path_or_name: Absolute path or bare name (resolved under
                ``config/``) of the YAML analytics manifest.
            stream_info: Camera, application, and geometry context
                (:class:`~matrice_analytics.analytics.schemas.StreamInfo`),
                or a dict accepted by ``StreamInfo.model_validate``. Values
                populate aggregation output; ``zone_config`` and ``resolution``
                are merged with manifest ``volume.counter`` for geometry.
        """
        self._stream_info = self._coerce_stream_info(stream_info)
        self._manifest = self._load_manifest(manifest_path_or_name)

        # Parse manifest sections
        self._app_info: dict[str, Any] = self._manifest.get("app", {})
        self._entity_mapping: dict = self._manifest.get("entity_mapping", {})
        self._alerts_config: dict[str, Any] = self._manifest.get("alerts", {})

        # Build manifest_config passed to each processor
        self._manifest_config: dict[str, Any] = {
            "app": self._app_info,
            "entity_mapping": self._entity_mapping,
            "alerts": self._alerts_config,
        }

        # Add category-specific sections (e.g. "volume", "zone") if present
        categories = self._manifest.get("categories", [])
        for cat in categories:
            cat_key = cat.lower()
            if cat_key in self._manifest:
                self._manifest_config[cat_key] = self._manifest[cat_key]

        # Separate INCIDENT (standalone, zone-agnostic) from metric categories
        # (zone-aware: VOLUME, QUALITY, SAFETY, ...).
        self._incident_processor: Any = None
        self._metric_category_classes: dict[str, type[BaseMetricProcessor]] = {}

        for cat in categories:
            if cat == "INCIDENT":
                from .processors.incident import IncidentProcessor

                self._incident_processor = IncidentProcessor(
                    manifest_config=self._manifest_config,
                )
                logger.info("Loaded INCIDENT processor for app '%s'", self._app_info.get("id", "?"))
            else:
                processor_cls = self._resolve_processor_class(cat)
                if processor_cls is not None:
                    self._metric_category_classes[cat] = processor_cls
                    logger.info("Resolved %s processor for app '%s'", cat, self._app_info.get("id", "?"))
                else:
                    logger.warning("No processor found for category '%s'", cat)

        # Aggregation timer (uses frame timestamps, not wall clock)
        self._last_agg_time: float | None = None
        self._agg_interval: float = _DEFAULT_AGG_INTERVAL_SEC

        # Per-zone metric processors — always active (defaults to "global" zone).
        # Nested dict: ``{zone_name: {category: processor}}``.
        self._zone_polygons_px: dict[str, Any] = {}
        self._zone_metric_processors: dict[str, dict[str, BaseMetricProcessor]] = {}
        self._use_foot_center_for_zones: bool = False
        self._setup_zone_processors()

        # Merge manifest volume.counter + StreamInfo zone_config / resolution
        # Must run AFTER _setup_zone_processors so geometry targets the
        # correct VOLUME processor (the "global" zone processor for footfall).
        self._apply_zone_config()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process_frame(
        self,
        detections: list[dict[str, Any]],
        frame_ts: float,
        frame_id: str = "",
    ) -> dict[str, Any]:
        """Process a single frame through all category processors.

        Assigns detections to zones (or the default ``"global"`` zone),
        runs every loaded metric processor (VOLUME, QUALITY, SAFETY, ...)
        per zone against the zone-filtered detections, then runs the
        standalone INCIDENT processor on all detections.

        Only the VOLUME processor in each zone contributes
        ``tracking_stats`` (``human_text`` + ``detections``) to the frame
        summary.  QUALITY/SAFETY contributions merge into the same zone's
        ``business_analytics`` and ``alerts``.

        Args:
            detections: List of detection dicts with track_id pre-assigned.
            frame_ts: Frame timestamp (seconds).
            frame_id: Frame identifier string.

        Returns:
            Combined FrameResult dict with zone-keyed ``agg_summary``.
        """
        if self._last_agg_time is None:
            self._last_agg_time = frame_ts

        # 1. Assign detections to zones (or pass-through for "global")
        zone_detections = self._assign_to_zones(detections)

        # 2. Run every metric processor per zone against zone-filtered detections
        agg_summary: dict[str, FrameSummaryEntry] = {}

        for zone_name, category_procs in self._zone_metric_processors.items():
            zone_dets = zone_detections.get(zone_name, [])

            zone_business: dict[str, Any] = {}
            zone_alerts: list[dict[str, Any]] = []
            zone_tracking_stats = TrackingStats()

            # Run VOLUME first (if present) — it owns tracking_stats for the zone
            volume_proc = category_procs.get("VOLUME")
            if volume_proc is not None:
                output = volume_proc.process_frame(zone_dets, frame_ts, frame_id)
                zone_business.update(output.business_analytics)
                zone_alerts.extend(output.alerts)
                zone_tracking_stats = TrackingStats(
                    human_text=output.human_text,
                    detections=output.detections,
                )

            # Run remaining metric processors (QUALITY, SAFETY, ...) for this zone.
            # Their per-frame business_analytics + alerts merge into the same
            # zone summary so the UI sees one consistent view per zone.
            for cat, proc in category_procs.items():
                if cat == "VOLUME":
                    continue
                output = proc.process_frame(zone_dets, frame_ts, frame_id)
                zone_business.update(output.business_analytics)
                zone_alerts.extend(output.alerts)
                # If VOLUME was not loaded for this app, fall back to the first
                # other category's detections so the UI still has bboxes to draw.
                if volume_proc is None and not zone_tracking_stats.detections:
                    zone_tracking_stats = TrackingStats(
                        human_text=output.human_text,
                        detections=output.detections,
                    )

            agg_summary[zone_name] = FrameSummaryEntry(
                tracking_stats=zone_tracking_stats,
                business_analytics=zone_business,
                alerts=zone_alerts,
            )

        # 3. Run the standalone INCIDENT processor on ALL detections (no zones)
        if self._incident_processor:
            self._incident_processor.process_frame(detections, frame_ts, frame_id)

        # 4. Build result
        input_streams: list[InputStreamEntry] = []
        if self._stream_info.original_fps > 0:
            input_streams.append(
                InputStreamEntry(
                    input_stream=InputStreamInfo(original_fps=self._stream_info.original_fps),
                )
            )

        combined = FrameResult(
            result=ResultWrapper(
                value=ResultValue(
                    input_streams=input_streams,
                    agg_summary=agg_summary,
                )
            ),
        )
        return combined.model_dump()

    def should_aggregate(self, frame_ts: float) -> bool:
        """Check if enough time has elapsed to trigger 1-minute aggregation."""
        if self._last_agg_time is None:
            return False
        return (frame_ts - self._last_agg_time) >= self._agg_interval

    def aggregate(self) -> AggregationResult:
        """Trigger 1-minute aggregation across all processors.

        For each zone, aggregates every loaded metric processor
        (VOLUME, QUALITY, SAFETY, ...).  Metrics are tagged with the
        zone name.  Only VOLUME processors contribute ``tracking_stats``
        (keyed per zone); QUALITY and SAFETY deliberately do not emit
        tracking_stats at aggregation time.
        """
        all_metrics: list[dict[str, Any]] = []
        zone_tracking_stats: dict[str, Any] = {}

        for zone_name, category_procs in self._zone_metric_processors.items():
            for cat, proc in category_procs.items():
                agg = proc.aggregate_1min()
                for m in agg.metrics:
                    m["zone"] = zone_name
                    if not m.get("category"):
                        m["category"] = proc._metric_category({"category": cat})
                    all_metrics.append(m)
                if cat == "VOLUME" and agg.tracking_stats:
                    zone_tracking_stats[zone_name] = agg.tracking_stats

        si = self._stream_info
        app_name = si.application_name or self._app_info.get("name", "")
        app_key = si.application_key_name or (app_name.lower().replace(" ", "_") if app_name else "")
        result = AggregationResult(
            camera_id=si.camera_id,
            camera_name=si.camera_name,
            app_deployment_id=si.app_deployment_id,
            app_id=si.app_id or self._app_info.get("id", ""),
            camera_group=si.camera_group or "default_group",
            locationId=si.location_id,
            location=si.location or "Unknown Location",
            application_name=app_name,
            application_key_name=app_key,
            application_version=si.application_version or self._app_info.get("version", "1.0"),
            tracking_stats=zone_tracking_stats,
            metrics=all_metrics,
        )

        self._last_agg_time = None

        return result

    def reset(self) -> None:
        """Full reset of all processors and engine state."""
        for category_procs in self._zone_metric_processors.values():
            for processor in category_procs.values():
                processor.reset()
        if self._incident_processor:
            self._incident_processor.reset()
        self._last_agg_time = None

    # ------------------------------------------------------------------
    # Zone processor setup
    # ------------------------------------------------------------------

    def _setup_zone_processors(self) -> None:
        """Create per-zone metric processors.  Always creates at least a ``"global"`` zone.

        When ``ZoneConfig.zones`` is present with valid resolution, creates
        one instance of each loaded metric-category processor per named zone
        (``VolumeProcessor(zone_id="A")``, ``QualityProcessor(zone_id="A")``,
        ``SafetyProcessor(zone_id="A")``, ...).  Otherwise, creates a single
        set of processors under the ``"global"`` zone key that receives all
        detections without polygon testing.

        Every processor class in ``_metric_category_classes`` (populated
        from the manifest ``categories`` list minus ``INCIDENT``) is
        instantiated per zone.  VOLUME is always present as a default for
        apps that don't declare it in their manifest, so the frame summary
        has a ``tracking_stats`` source even for QUALITY-only or SAFETY-only
        deployments.
        """
        from .processors.volume import VolumeProcessor

        si = self._stream_info
        zc = si.zone_config
        has_named_zones = False
        zone_names: list[str] = []

        if zc is not None and zc.zones:
            res = si.resolution
            if res and len(res) >= 2 and int(res[0]) > 0 and int(res[1]) > 0:
                width, height = int(res[0]), int(res[1])
                self._zone_polygons_px = build_zone_polygons_px(zc.zones, width, height)

                if self._zone_polygons_px:
                    volume_section = self._manifest_config.get("volume", {})
                    counter = volume_section.get("counter") if isinstance(volume_section, dict) else {}
                    counter = counter if isinstance(counter, dict) else {}
                    self._use_foot_center_for_zones = bool(counter.get("use_foot_center", False))

                    zone_names = list(self._zone_polygons_px.keys())
                    has_named_zones = True
                else:
                    logger.warning("No valid zone polygons after denormalization, falling back to global")
            else:
                logger.warning("Invalid resolution for zone analytics, falling back to global")

        if not has_named_zones:
            zone_names = ["global"]

        # For every zone, instantiate one processor of each loaded metric category.
        for zone_name in zone_names:
            procs: dict[str, BaseMetricProcessor] = {}

            for cat, cls in self._metric_category_classes.items():
                procs[cat] = cls(
                    category=cat,
                    manifest_config=self._manifest_config,
                    zone_id=zone_name,
                )

            # Ensure VOLUME exists even when the manifest didn't declare it so
            # every zone has a ``tracking_stats`` source for the frame summary.
            if "VOLUME" not in procs:
                procs["VOLUME"] = VolumeProcessor(
                    category="VOLUME",
                    manifest_config=self._manifest_config,
                    zone_id=zone_name,
                )

            self._zone_metric_processors[zone_name] = procs

        logger.info(
            "Zone processors initialised: zones=%s categories=%s",
            ", ".join(zone_names),
            ", ".join(sorted({cat for procs in self._zone_metric_processors.values() for cat in procs})),
        )

    def _assign_to_zones(
        self,
        detections: list[dict[str, Any]],
    ) -> dict[str, list[dict[str, Any]]]:
        """Assign detections to zones.

        For the default ``"global"`` zone, all detections are assigned
        without polygon testing.  For named zones, uses point-in-polygon
        containment via :func:`assign_detections_to_zones`.
        """
        if "global" in self._zone_metric_processors and len(self._zone_metric_processors) == 1:
            return {"global": detections}

        return assign_detections_to_zones(
            detections,
            self._zone_polygons_px,
            use_foot_center=self._use_foot_center_for_zones,
        )

    # ------------------------------------------------------------------
    # Zone config (geometry) forwarding
    # ------------------------------------------------------------------

    def set_zone_config(
        self,
        zone_config: dict[str, Any],
        width: int,
        height: int,
        method: str | None = None,
        in_direction: str = "A_to_B",
        use_foot_center: bool = False,
    ) -> None:
        """Set geometry on the global VOLUME processor for entry/exit counting.

        Named-zone polygons are already configured at construction time via
        ``StreamInfo.zone_config.zones``; this helper is for apps that use
        line/polygon counters in the default ``"global"`` zone (footfall,
        people_counting, etc.).

        Args:
            zone_config: Dict with ``"lines"`` and/or ``"zones"`` in normalized
                (0-1) coordinates.
            width: Frame width in pixels.
            height: Frame height in pixels.
            method: ``"abline"`` or ``"polygon"``.
            in_direction: For abline -- ``"A_to_B"`` or ``"B_to_A"``.
            use_foot_center: Use bottom-center of bbox instead of center.
        """
        volume = self._get_volume_processor()
        if volume is None:
            logger.warning("set_zone_config: no VOLUME processor loaded")
            return

        if method is None:
            # No geometry used for this zone
            logger.warning("set_zone_config: no geometry used for this zone")
            return

        volume.set_zone_config(zone_config, width, height, method=method, in_direction=in_direction, use_foot_center=use_foot_center)

    def _get_volume_processor(self) -> Any:
        """Return the VOLUME processor for the ``"global"`` zone if present, else None."""
        global_procs = self._zone_metric_processors.get("global")
        if global_procs:
            return global_procs.get("VOLUME")
        return None

    # ------------------------------------------------------------------
    # Incident support
    # ------------------------------------------------------------------

    def drain_incident_events(self) -> list[dict[str, Any]]:
        """Return and clear pending incident events as serialized ``IncidentMessage`` dicts.

        Each event is wrapped with :class:`IncidentMessage.from_event` using
        the engine's :attr:`stream_info`, producing dicts ready for Redis
        publishing.  Returns an empty list if no INCIDENT processor is loaded.
        """
        if self._incident_processor is None:
            return []
        raw_events: list[IncidentEvent] = self._incident_processor.drain_events()
        return [
            IncidentMessage.from_event(event, stream_info=self._stream_info).model_dump()
            for event in raw_events
        ]

    def update_incident_thresholds(
        self,
        camera_id: str,
        thresholds: list[dict[str, Any]],
        incident_type: str = "",
    ) -> None:
        """Update incident thresholds for a camera at runtime.

        Convenience method that delegates to the INCIDENT processor.
        Called by the config-polling caller when new thresholds arrive.
        """
        if self._incident_processor is None:
            logger.warning("update_incident_thresholds: no INCIDENT processor loaded")
            return
        self._incident_processor.update_thresholds(camera_id, thresholds, incident_type)

    def get_incident_state(self, camera_id: str) -> Any:
        """Debug access to per-camera incident lifecycle state.

        Returns an :class:`IncidentLifecycleState` copy or ``None``.
        """
        if self._incident_processor is None:
            return None
        return self._incident_processor.get_lifecycle_state(camera_id)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def app_id(self) -> str:
        """Application ID from the manifest."""
        return self._app_info.get("id", "")

    @property
    def app_name(self) -> str:
        """Application name from the manifest."""
        return self._app_info.get("name", "")

    @property
    def categories(self) -> list[str]:
        """List of active category names (e.g. ``["VOLUME", "QUALITY", "INCIDENT"]``).

        Derived from the actual per-zone processor set so that any
        auto-created VOLUME fallback (for apps that don't declare VOLUME
        in their manifest) is still surfaced.
        """
        cats: set[str] = {
            cat
            for procs in self._zone_metric_processors.values()
            for cat in procs
        }
        sorted_cats = sorted(cats)
        if self._incident_processor is not None:
            sorted_cats.append("INCIDENT")
        return sorted_cats

    @property
    def processors(self) -> dict[str, BaseMetricProcessor]:
        """Flat mapping of category name → processor instance for the ``"global"`` zone.

        Provided for backwards compatibility with callers that expect a
        per-category view.  When named zones are active, this returns the
        processors of the first zone (typically still representative of
        per-category wiring).  Prefer :attr:`zone_metric_processors` for
        the full nested view.
        """
        if "global" in self._zone_metric_processors:
            return dict(self._zone_metric_processors["global"])
        # Named zones active — return the first zone's processors as a proxy
        if self._zone_metric_processors:
            first_zone = next(iter(self._zone_metric_processors))
            return dict(self._zone_metric_processors[first_zone])
        return {}

    @property
    def incident_processor(self) -> Any:
        """The standalone incident processor, or ``None`` if not loaded."""
        return self._incident_processor

    @property
    def zones_active(self) -> bool:
        """Whether named zone analytics is active (not just the default global)."""
        return not (len(self._zone_metric_processors) == 1 and "global" in self._zone_metric_processors)

    @property
    def zone_processors(self) -> dict[str, Any]:
        """Mapping of zone name to that zone's ``VolumeProcessor`` instance.

        Kept for backwards compatibility with tests and debug tooling that
        expect a flat ``{zone: VolumeProcessor}`` view.  Use
        :attr:`zone_metric_processors` for the full nested
        ``{zone: {category: processor}}`` view.
        """
        return {
            zone_name: procs["VOLUME"]
            for zone_name, procs in self._zone_metric_processors.items()
            if "VOLUME" in procs
        }

    @property
    def zone_metric_processors(self) -> dict[str, dict[str, BaseMetricProcessor]]:
        """Nested mapping of zone name → category → processor instance.

        This is the canonical runtime layout: every zone has one processor
        per loaded metric category.  INCIDENT is not included here (it is
        standalone and zone-agnostic — see :attr:`incident_processor`).
        """
        return self._zone_metric_processors

    @property
    def stream_info(self) -> StreamInfo:
        """Resolved stream metadata and geometry context."""
        return self._stream_info

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _coerce_stream_info(stream_info: StreamInfo | dict[str, Any] | None) -> StreamInfo:
        """Normalize constructor input to :class:`StreamInfo`."""
        if stream_info is None:
            return StreamInfo()
        if isinstance(stream_info, StreamInfo):
            return stream_info
        return StreamInfo.model_validate(stream_info)

    def _load_manifest(self, path_or_name: str) -> dict[str, Any]:
        """Load YAML manifest from config/ directory or absolute path."""
        path = Path(path_or_name)

        # If not an absolute path, resolve relative to config/ directory
        if not path.is_absolute():
            config_dir = Path(__file__).parent / "config"
            # Try with and without .yaml extension
            if not path_or_name.endswith(".yaml"):
                path = config_dir / f"{path_or_name}.yaml"
            else:
                path = config_dir / path_or_name

        if not path.exists():
            raise FileNotFoundError(f"Manifest not found: {path}")

        with path.open(encoding="utf-8") as f:
            manifest = yaml.safe_load(f)

        if not isinstance(manifest, dict):
            raise TypeError(f"Invalid manifest format in {path}: expected dict, got {type(manifest)}")

        logger.info("Loaded manifest from %s", path)
        return manifest

    def _apply_zone_config(self) -> None:
        """Apply geometry from ``StreamInfo.zone_config`` using manifest ``volume.counter``.

        ``volume.counter`` supplies ``method``, ``in_direction``, and
        ``use_foot_center``. ``StreamInfo.zone_config`` supplies ``lines`` and
        ``zones``; ``StreamInfo.resolution`` supplies frame width and height in
        pixels.

        When ``volume.counter`` declares ``method: abline`` (or it defaults to
        abline), exactly two named lines must exist in ``StreamInfo.zone_config.lines``.
        """
        volume_section = self._manifest_config.get("volume", {})
        if not isinstance(volume_section, dict):
            return

        counter: dict[str, Any] = volume_section.get("counter")
        counter = counter if isinstance(counter, dict) else {}

        si = self._stream_info
        zc = si.zone_config
        if zc is None:
            if counter and counter.get("method", "abline") == "abline":
                raise ValueError(
                    "volume.counter uses method abline but StreamInfo.zone_config is missing "
                    "(two named lines required)."
                )
            return

        has_lines = bool(zc.lines)
        has_zones = bool(zc.zones)
        if not has_lines and not has_zones:
            if counter and counter.get("method", "abline") == "abline":
                raise ValueError(
                    "volume.counter uses method abline but StreamInfo.zone_config has no lines "
                    "(two named lines required)."
                )
            return

        method = counter.get("method", None)
        method = str(method) if method is not None else None
        if method is None:
            return  # No counting method configured — nothing to set
        in_direction = str(counter.get("in_direction", "A_to_B"))
        use_foot_center = bool(counter.get("use_foot_center", False))

        if method == "abline" and len(zc.lines) != 2:
            raise ValueError(
                "abline counter method requires exactly two named lines in StreamInfo.zone_config.lines; "
                f"got {len(zc.lines)} line(s)."
            )

        res = si.resolution
        if not res or not isinstance(res, (list, tuple)) or len(res) < 2 or int(res[0]) <= 0 or int(res[1]) <= 0:
            logger.warning(
                "StreamInfo.resolution must be [width, height] with positive values; skipping geometry apply",
            )
            return

        width, height = int(res[0]), int(res[1])
        geom = zc.model_dump()
        self.set_zone_config(
            geom,
            width,
            height,
            method=method,
            in_direction=in_direction,
            use_foot_center=use_foot_center,
        )
        logger.info("Applied zone_config from StreamInfo (method=%s)", method)

    def _resolve_processor_class(self, category_name: str) -> type[BaseMetricProcessor] | None:
        """Dynamically import and return the processor class for a category.

        For category "VOLUME", imports ``processors.volume.VolumeProcessor``.
        """
        module_name = category_name.lower()
        class_name = f"{category_name.capitalize()}Processor"

        try:
            module = importlib.import_module(f".processors.{module_name}", package=__package__)
            cls = getattr(module, class_name)
            if not (isinstance(cls, type) and issubclass(cls, BaseMetricProcessor)):
                logger.error(
                    "%s.%s is not a BaseMetricProcessor subclass",
                    module_name,
                    class_name,
                )
                return None
        except (ImportError, AttributeError):
            logger.exception(
                "Failed to load processor for category '%s'",
                category_name,
            )
            return None
        else:
            return cls
