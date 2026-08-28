"""The app-manifest schema — Pydantic v2 models, and the source of truth for ``app.yaml``.

Normative references:

* ``_contracts/08-tobe-app-manifest.md``      — the schema itself
* ``_contracts/06-vocabularies.md`` §1 §2 §10 — categories, severity ladder, units registry
* ``ml-applications/guidelines/FIELD_REFERENCE.md``    — every field, every default, written for app authors

Two design rules run through the whole module:

1. **Nothing here knows an app's name.** No ``if app.id == "footfall"``. If the engine would need
   to know, this schema is missing a field (``09-tobe-engine-architecture.md`` §1).
2. **A manifest that cannot work must not load.** Every rule below exists because the old engine
   accepted the mistake and then silently emitted nothing, or emitted the wrong number. Each rule
   carries the defect id it prevents. Failing loudly at startup is the entire point (``09`` §5).

The JSON Schema shipped for editor completion is *generated* from these models
(:mod:`matrice_analytics.engine.manifest.jsonschema`) — it is an artefact, never a second source
of truth.
"""

from __future__ import annotations

import difflib
import logging
import re
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Annotated, Any, ClassVar, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# A hard dependency on the contract layer, unlike the *vocabularies* below which this
# module deliberately keeps narrower (see _check_vocabularies). The difference: an enum is
# a policy the two layers may legitimately disagree about, whereas the zone-identity rule
# is a key derivation that must be byte-identical on both sides or the manifest declares an
# output the primitive never publishes -- which is exactly the bug this import fixes.
from matrice_analytics.engine.contract.schemas import GLOBAL_ZONE, UNASSIGNED_ZONE, zone_identity

# The derived-metric grammar. A sibling module rather than code in here because it is a
# parser with its own tests, and rather than `primitives/derived.py` because
# `contract/schemas.py:160` states the layering rule that forbids it: **manifest must not
# import primitives** (every primitive imports this module, so the reverse edge is a cycle).
from matrice_analytics.engine.manifest.expr import (
    DerivedExpression,
    ExpressionError,
    parse_expression,
)

logger = logging.getLogger(__name__)

__all__ = [
    "AGG_TYPES",
    "ANALYTICS_CATEGORIES",
    "MANIFEST_SCHEMA_VERSION",
    "MIN_CONFIRM_FRAMES",
    "PRIMITIVES",
    "SEVERITY_LEVELS",
    "THRESHOLD_OPERATORS",
    "UNIT_DIMENSIONS",
    "AggTypeLiteral",
    "AppManifest",
    "AppSpec",
    "CategoryLiteral",
    "CustomConfig",
    "DerivedMetricSpec",
    "DerivedScopeLiteral",
    "DetectConfig",
    "DwellConfig",
    "EmissionSpec",
    "GeometryRequirement",
    "IdentityMatchConfig",
    "IncidentLifecycle",
    "IncidentQuantiseConfig",
    "IncidentSpec",
    "IncidentType",
    "KeypointPoseConfig",
    "LineCrossingConfig",
    "MetricSpec",
    "MetricThreshold",
    "ModelSpec",
    "PipelineStage",
    "PrimitiveConfig",
    "ProximityConfig",
    "QuantiseLevel",
    "RatioComplianceConfig",
    "ResolvedDerived",
    "ResolvedSource",
    "SegmentationAreaConfig",
    "SeverityLiteral",
    "SmoothingConfig",
    "StateMachineConfig",
    "TestsSpec",
    "TrackConfig",
    "UniqueCountConfig",
    "VelocityStateConfig",
    "ZoneOccupancyConfig",
    "ZonesSpec",
    "resolve_derived",
    "resolve_source",
]


# ---------------------------------------------------------------------------
# Vocabularies
#
# These live here rather than being imported wholesale from the contract because the manifest
# vocabulary is deliberately *narrower* than the wire vocabulary. The wire still carries values
# this schema rejects (`IDENTITY`, `SPECIAL`, `avg`) because legacy producers emit them; a new
# manifest must not be able to.
# ---------------------------------------------------------------------------

MANIFEST_SCHEMA_VERSION = 1

#: ``sum|mean|min|max|last``. See ``MetricSpec._check_agg_type`` for why ``avg``/``median`` are out.
AGG_TYPES: frozenset[str] = frozenset({"sum", "mean", "min", "max", "last"})

#: The only three categories with backend meaning (``06-vocabularies.md`` §1).
ANALYTICS_CATEGORIES: frozenset[str] = frozenset({"VOLUME", "SAFETY", "QUALITY"})

#: Lowercase on the wire (``06-vocabularies.md`` §2). Old manifests used ``HIGH``; that is rejected.
SEVERITY_LEVELS: tuple[str, ...] = ("info", "low", "medium", "high", "critical")

#: ``state_machine`` / incident-lifecycle confirmation floor. Below this the old engine silently
#: raised the value to 3 (``base_processor.py:78``, defect **PY-11**).
MIN_CONFIRM_FRAMES = 3


#: Analytics category. ``IDENTITY`` and ``SPECIAL`` were py_analytics-internal processor
#: categories; they reach ClickHouse as literal strings no UI surface groups by, so a metric tagged
#: with one is unfilterable forever (``06-vocabularies.md`` §1).
CategoryLiteral = Literal["VOLUME", "SAFETY", "QUALITY"]

#: How 60 seconds of per-frame values collapse into one published number. ``avg`` and ``median``
#: are absent on purpose — see :meth:`MetricSpec._check_agg_type` for the two defects that caused.
AggTypeLiteral = Literal["sum", "mean", "min", "max", "last"]

#: Wire severity ladder, lowercase (``06-vocabularies.md`` §2).
SeverityLiteral = Literal["info", "low", "medium", "high", "critical"]

#: How a ``zone: per_zone`` metric collapses across zones when something needs **one** number
#: for the whole camera.
#:
#: This is a *different axis* from :data:`AggTypeLiteral`, which says how 60 seconds collapse
#: into one published number. ``results-agg`` never needs this one -- it publishes a row per
#: zone, each carrying its own ``zone`` field -- but the per-frame ``result["metrics"]`` map is
#: flat, so a per-zone metric has no zone to be reported under and must be reduced.
#:
#: ``agg_type`` cannot stand in for it. A manifest routinely declares ``agg_type: last`` for a
#: count, an average and a maximum alike, because at window scope all three are "whatever the
#: registered primitive published"; reusing it here would sum every one of them. Summing two
#: zones' 1.8-second averages into 3.6 is the defect this field exists to make expressible.
#:
#: The default is ``sum`` because that is what counts want -- "how many, anywhere on this
#: camera" -- and because it is what the engine already did, so adding this field changes no
#: existing behaviour until a manifest opts in.
AcrossZonesLiteral = Literal["sum", "max", "mean"]


def _cross_check_contract_vocabulary() -> None:
    """Warn if ``engine.contract.schemas`` and this schema disagree about the vocabularies.

    The contract owns what crosses the wire and legitimately still *accepts* values a new manifest
    must not be able to *declare* (legacy producers emit ``IDENTITY``). So the manifest keeps its
    own, narrower literals rather than importing the contract enums wholesale — but a contract that
    no longer contains one of our values would mean this schema can emit something unroutable, and
    that is worth a log line at import time.
    """
    try:
        from matrice_analytics.engine.contract.schemas import (  # noqa: PLC0415
            AggType,
            Category,
        )
    except ImportError:  # pragma: no cover - the contract module is a sibling change
        return
    for enum_type, expected, label in (
        (Category, ANALYTICS_CATEGORIES, "category"),
        (AggType, AGG_TYPES, "agg_type"),
    ):
        try:
            available = {str(getattr(member, "value", member)) for member in enum_type}
        except TypeError:  # pragma: no cover - not an iterable enum after all
            continue
        missing = expected - available
        if missing:
            logger.warning(
                "manifest %s vocabulary %s is not present in engine.contract.schemas; a manifest "
                "could declare a value the wire cannot carry",
                label,
                sorted(missing),
            )


#: Accepted unit spellings → dimension. Verbatim from ``06-vocabularies.md`` §10, which mirrors
#: ``be-analytics internal/utils/units.go:136-150``. Alert-rule creation is rejected by the backend
#: when the threshold unit and the metric unit do not share a dimension — one of the very few
#: things that *is* validated server-side, so getting it right here is worth an error.
UNIT_DIMENSIONS: dict[str, str] = {
    # time — base: seconds
    **dict.fromkeys(
        (
            "ms",
            "millisecond",
            "milliseconds",
            "s",
            "sec",
            "secs",
            "second",
            "seconds",
            "min",
            "mins",
            "minute",
            "minutes",
            "h",
            "hr",
            "hrs",
            "hour",
            "hours",
            "day",
            "days",
        ),
        "time",
    ),
    # ratio — base: fraction
    **dict.fromkeys(("fraction", "ratio", "percent", "percentage", "pct", "%"), "ratio"),
    # count — base: raw
    **dict.fromkeys(
        ("count", "counts", "raw", "n", "people", "persons", "vehicles", "items", "unit", "units"),
        "count",
    ),
}

_APP_ID_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_ENTITY_RE = re.compile(r"^[a-z][a-z0-9_]*$")
_METRIC_KEY_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_VERSION_RE = re.compile(r"^\d+(\.\d+)*([-+][A-Za-z0-9.]+)?$")
_IMPL_RE = re.compile(r"^(?P<module>[^:]+):(?P<symbol>[A-Za-z_][A-Za-z0-9_]*)$")
_INTERPOLATION_RE = re.compile(r"\{([^{}]+)\}")

#: Comparison operators accepted by ``incidents.types[].severity_from``.
THRESHOLD_OPERATORS: tuple[str, ...] = (">", ">=", "<", "<=", "==", "!=")


def _did_you_mean(value: str, candidates: Iterable[object], *, cutoff: float = 0.6) -> str:
    """Return a ``" Did you mean 'x'?"`` suffix, or ``""``.

    Every rejection in this module names the bad value and the fix; a near-miss suggestion is the
    difference between a two-minute fix and a support ticket.
    """
    pool = sorted(str(c) for c in candidates)
    close = difflib.get_close_matches(value, pool, n=1, cutoff=cutoff)
    return f" Did you mean {close[0]!r}?" if close else ""


def _joined(values: Iterable[object], limit: int = 24) -> str:
    items = sorted(str(v) for v in values)
    if len(items) > limit:
        return ", ".join(items[:limit]) + f", … (+{len(items) - limit} more)"
    return ", ".join(items) if items else "(none)"


class ManifestModel(BaseModel):
    """Base for every manifest node.

    ``extra="forbid"`` is not pedantry: an ignored key is how ``alerts:`` looked functional for two
    years while doing nothing (**PY-12**), and how a misspelt ``confidence_treshold`` reads as the
    default forever.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        populate_by_name=True,
    )


# ---------------------------------------------------------------------------
# app:
# ---------------------------------------------------------------------------


class AppSpec(ManifestModel):
    """``app:`` — identity. The registry key and its dashboard grouping."""

    id: str = Field(description="Registry key. Must equal post_processing_config.json → usecase.")
    name: str = Field(min_length=1, description="Human-readable name shown in the appstore.")
    version: str = Field(description='App version, quoted: "1.6". Must equal the version folder.')
    category: CategoryLiteral = Field(
        description="Primary analytics category: VOLUME | SAFETY | QUALITY."
    )
    description: str | None = None

    @field_validator("id")
    @classmethod
    def _check_id(cls, value: str) -> str:
        """``app.id`` is used as a state-store key prefix and as the registry key, so it must be a
        plain lowercase identifier — no spaces, hyphens or capitals to normalise inconsistently."""
        if not _APP_ID_RE.match(value):
            raise ValueError(
                f"app.id {value!r} is not a valid app id. It must match ^[a-z][a-z0-9_]*$ — "
                f"lowercase letters, digits and underscores, starting with a letter. "
                f"Try {_suggest_id(value)!r}."
            )
        return value

    @field_validator("version", mode="before")
    @classmethod
    def _version_must_be_quoted(cls, value: Any) -> Any:
        """``version: 1.6`` unquoted is a YAML *float*, and ``1.60`` would then silently equal
        ``1.6``. Versions are strings and are compared as strings."""
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            raise ValueError(
                f'app.version must be a quoted string: write version: "{value}". '
                f'Unquoted {value} is parsed by YAML as a number, so "1.60" and "1.6" would '
                f"become the same version."
            )
        return value

    @field_validator("version")
    @classmethod
    def _check_version(cls, value: str) -> str:
        if not _VERSION_RE.match(value):
            raise ValueError(
                f"app.version {value!r} is not a version. Use a dotted numeric version such as "
                f'"1.6" or "2.0" — it must equal the version folder name (v1.6/).'
            )
        return value

    @field_validator("category", mode="before")
    @classmethod
    def _check_category(cls, value: Any) -> Any:
        return _validate_category(value, "app.category")


def _suggest_id(value: str) -> str:
    """Best-effort repair of an app id, used only inside the error message."""
    slug = re.sub(r"[^a-z0-9_]+", "_", str(value).strip().lower()).strip("_")
    slug = re.sub(r"_+", "_", slug)
    return slug if slug and slug[0].isalpha() else f"app_{slug or 'unnamed'}"


def _validate_category(value: Any, where: str) -> Any:
    """Shared category gate. Rejects the two py_analytics-internal categories by name."""
    raw = str(value).strip()
    upper = raw.upper()
    if upper in {"IDENTITY", "SPECIAL"}:
        raise ValueError(
            f"{where}: {raw!r} is not a backend analytics category. {upper} was a py_analytics "
            f"internal processor category; metrics tagged with it land in ClickHouse as a literal "
            f"string that no dashboard filters on. Use one of: VOLUME, SAFETY, QUALITY."
        )
    if upper not in ANALYTICS_CATEGORIES:
        raise ValueError(
            f"{where}: {raw!r} is not a valid category. Use one of: VOLUME, SAFETY, QUALITY."
            f"{_did_you_mean(upper, ANALYTICS_CATEGORIES)}"
        )
    if raw != upper:
        raise ValueError(
            f"{where}: {raw!r} must be UPPERCASE — write {upper!r}. The backend enum is uppercase "
            f"and nothing normalises it on ingest."
        )
    return upper


# ---------------------------------------------------------------------------
# model:
# ---------------------------------------------------------------------------


class ModelSpec(ManifestModel):
    """``model:`` — how the detector's class labels become analytics entities.

    The right-hand side of ``entity_mapping`` is the single most common cause of an empty
    dashboard: it must match the model's labels character for character, including spaces and
    capitals (``FIELD_REFERENCE`` §4). Nothing can validate that here — we only have the manifest —
    so the schema validates everything around it and leaves the spelling to the author.
    """

    entity_mapping: dict[str, list[str]] = Field(
        description="analytics entity → model label, or a list of labels forming an alias set.",
    )
    index_to_category: dict[int, str] | None = Field(
        default=None,
        description="Fallback class-index map for deployments that do not supply one.",
    )
    confidence_threshold: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Global confidence floor; a detect stage may override it.",
    )

    @field_validator("entity_mapping", mode="before")
    @classmethod
    def _normalise_mapping(cls, value: Any) -> Any:
        """A scalar right-hand side becomes a one-element alias set, so downstream code has exactly
        one shape to handle."""
        if not isinstance(value, dict):
            return value
        out: dict[str, Any] = {}
        for entity, labels in value.items():
            if labels is None:
                raise ValueError(
                    f"model.entity_mapping.{entity} has no model label. Write '{entity}: <the label your model emits>'."
                )
            out[entity] = [labels] if isinstance(labels, str) else labels
        return out

    @field_validator("entity_mapping")
    @classmethod
    def _check_mapping(cls, value: dict[str, list[str]]) -> dict[str, list[str]]:
        if not value:
            raise ValueError(
                "model.entity_mapping is empty. Map at least one analytics entity to a model "
                "label, e.g. 'person: Person'. With no mapping every detection is discarded."
            )
        seen_labels: dict[str, str] = {}
        for entity, labels in value.items():
            if not _ENTITY_RE.match(entity):
                raise ValueError(
                    f"model.entity_mapping key {entity!r} is not a valid entity name. Entity names "
                    f"must match ^[a-z][a-z0-9_]*$ because they appear inside metric sources "
                    f"(e.g. 'detect.{entity}.count'), where a dot or a space would be ambiguous."
                )
            if not labels:
                raise ValueError(
                    f"model.entity_mapping.{entity} maps to an empty alias set. Give it at least "
                    f"one model label, or delete the entry."
                )
            for label in labels:
                if not isinstance(label, str) or not label.strip():
                    raise ValueError(
                        f"model.entity_mapping.{entity} contains an empty model label. Every alias "
                        f"must be the label string your model emits."
                    )
                previous = seen_labels.setdefault(label, entity)
                if previous != entity:
                    raise ValueError(
                        f"model label {label!r} is mapped to two entities ({previous!r} and "
                        f"{entity!r}). One detection cannot be both; the winner would depend on "
                        f"dict order. Map it once."
                    )
        return value

    @field_validator("index_to_category")
    @classmethod
    def _check_index_map(cls, value: dict[int, str] | None) -> dict[int, str] | None:
        if value is None:
            return value
        for index, label in value.items():
            if index < 0:
                raise ValueError(
                    f"model.index_to_category has a negative class index ({index}). Class indices "
                    f"are the model's output positions and start at 0."
                )
            if not str(label).strip():
                raise ValueError(
                    f"model.index_to_category[{index}] is empty; give it a model label."
                )
        return value

    @property
    def entities(self) -> frozenset[str]:
        """The analytics entity names an app may refer to anywhere else in the manifest."""
        return frozenset(self.entity_mapping)


# ---------------------------------------------------------------------------
# pipeline: — one config model per primitive
#
# Every primitive in the vocabulary gets a config model, including the ones the runtime has not
# implemented yet (08 §2 marks them 🔜). A manifest that declares `dwell` must validate *today*, so
# that app authors can write and review the manifest before the primitive lands. The runtime
# refuses to *run* an unimplemented primitive; the schema does not refuse to *describe* it.
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class GeometryRequirement:
    """A runtime geometry precondition that the manifest can state but cannot check.

    Zone and line geometry is per-camera installation data on ``StreamInfo``, not manifest data
    (``08`` §5). ``line_crossing.method: abline`` nevertheless *implies* exactly two lines will be
    drawn. Recording the implication here lets the runtime fail loudly at session start with the
    manifest's own words, rather than counting zero crossings forever.
    """

    stage: str
    kind: Literal["lines", "zones"]
    exact: int | None = None
    minimum: int | None = None
    reason: str = ""

    def describe(self) -> str:
        if self.exact is not None:
            want = f"exactly {self.exact} {self.kind}"
        elif self.minimum is not None:
            want = f"at least {self.minimum} {self.kind}"
        else:  # pragma: no cover - defensive; every construction sets one of the two
            want = f"{self.kind}"
        return f"{self.stage} requires {want} configured on the camera. {self.reason}".strip()


class PrimitiveConfig(ManifestModel):
    """Base class for every pipeline primitive config.

    Subclasses declare:

    ``PRIMITIVE``              the YAML key (``- detect:``) and the metric-source namespace
    ``STATIC_OUTPUTS``         the fixed **per-frame** ``values`` keys a metric may point at
    ``STATIC_WINDOW_OUTPUTS``  the fixed **window** keys, when they differ from the per-frame set
    ``REQUIRES``               primitives that must appear *earlier* in the pipeline

    **Why the two output sets are separate.**  A registered primitive's
    :meth:`~matrice_analytics.engine.primitives.base.Primitive.window` output is published
    *as-is* — the stage already aggregated, so the runtime does not re-apply
    ``metrics[].agg_type`` on top (that re-application is **PY-1**).  A window key is therefore
    **already a specific reading**: ``detect.person.count`` at window scope is the count on the
    window's last frame and ``detect.person.count_peak`` is the window's high-water mark, and
    ``agg_type`` cannot turn one into the other.  Declaring the two sets apart is what lets a
    reviewer — and :func:`resolve_source`, via
    :attr:`ResolvedSource.window_aggregated` — say which of a stage's outputs ignore
    ``agg_type`` and which are per-frame samples the runtime really does collapse with it.
    """

    PRIMITIVE: ClassVar[str] = ""
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset()
    #: Window-scope keys when they are *not* the same set as :attr:`STATIC_OUTPUTS`. ``None``
    #: means "``window()`` republishes exactly the per-frame key set", which is the common case.
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = None
    #: ``True`` only for ``custom`` — its outputs live in the author's Python, not the manifest.
    OPEN_OUTPUTS: ClassVar[bool] = False
    REQUIRES: ClassVar[tuple[str, ...]] = ()
    #: ``False`` for primitives the runtime has not implemented yet (``08`` §2). Informational:
    #: the manifest still validates, so authors can write apps ahead of the engine.
    IMPLEMENTED: ClassVar[bool] = True

    name: str | None = Field(
        default=None,
        description=(
            "Optional stage name, used as the metric-source namespace. Defaults to the primitive "
            "name. Needed only when the same primitive appears twice in one pipeline."
        ),
    )

    @property
    def stage_name(self) -> str:
        """The namespace ``metrics[].source`` resolves against."""
        return self.name or self.PRIMITIVE

    @property
    def all_in_one(self) -> bool:
        """Whether this stage runs **once over the whole frame** instead of once per zone.

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
        return False

    def frame_output_names(self) -> frozenset[str]:
        """Concrete ``values`` keys ``process()`` publishes **every frame**, given *this* config.

        These are per-frame samples.  A metric sourcing one of them that the stage's
        ``window()`` does not republish is the only case where this engine applies
        ``metrics[].agg_type`` to a registered primitive.
        """
        return self.STATIC_OUTPUTS

    def window_output_names(self) -> frozenset[str]:
        """Concrete ``values`` keys ``window()`` publishes at the aggregation boundary.

        Already aggregated, and published verbatim — see the class docstring.  Defaults to
        :meth:`frame_output_names` because most primitives republish the same key set.
        """
        if self.STATIC_WINDOW_OUTPUTS is None:
            return self.frame_output_names()
        return self.STATIC_WINDOW_OUTPUTS

    def output_names(self) -> frozenset[str]:
        """Every key a ``metrics[].source`` may name: the per-frame set ∪ the window set."""
        return self.frame_output_names() | self.window_output_names()

    def output_patterns(self) -> tuple[re.Pattern[str], ...]:
        """Patterns for outputs whose names are only known at runtime (per-zone counts)."""
        return ()

    def window_output_patterns(self) -> tuple[re.Pattern[str], ...]:
        """The subset of :meth:`output_patterns` that ``window()`` publishes.

        Defaults to all of them; only ``zone_occupancy`` has runtime-named outputs at all, and
        it publishes every one of them at both scopes.
        """
        return self.output_patterns()

    def silent_buckets(self, *, zoned: bool = False) -> frozenset[str]:
        """Buckets where this stage runs but publishes **nothing**, by construction.

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
        return frozenset()

    def geometry_requirements(self) -> tuple[GeometryRequirement, ...]:
        return ()

    def describe_outputs(self) -> str:
        parts = sorted(self.output_names())
        parts += [p.pattern.strip("^$").replace("\\.", ".") for p in self.output_patterns()]
        return _joined(parts)


# --- detect ----------------------------------------------------------------


class SmoothingConfig(ManifestModel):
    """The five-field bbox-smoothing block that 105 of 123 existing configs carry *identically*.

    First-class with defaults precisely so nobody writes it again (``08`` §1).
    """

    enabled: bool = True
    algorithm: Literal["window", "ema"] = "window"
    window_size: int = Field(default=5, ge=1)
    cooldown_frames: int = Field(
        default=3,
        ge=0,
        description=(
            "How many frames an unseen object keeps its smoothing window before the record is "
            "dropped. A record in cooldown contributes no count of its own; it only survives a "
            "brief detector dropout so the object does not have to re-ramp its window from "
            "empty. 0 drops a record the first frame it is missed. The legacy tree declared "
            "this field, documented it and never read it (smoothing_utils.py:97,110 creates, "
            "clears and counts object_cooldowns but never writes it); the new detect primitive "
            "does read it, so it now changes behaviour."
        ),
    )
    confidence_range_factor: float = Field(default=0.2, ge=0.0, le=1.0)


class DetectConfig(PrimitiveConfig):
    """``detect`` — thresholded class presence and counts. Universal; always first.

    ``<entity>.count`` and ``total`` are *levels*, so the window publishes two genuinely
    different readings of each under two names: the value on the window's **last frame**
    (``detect.person.count`` — what ``agg_type: last`` means) and the window's **peak**
    (``detect.person.count_peak`` — what ``agg_type: max`` means).  Sourcing one name with two
    ``agg_type``\\ s cannot produce two numbers, because the stage aggregated already; source the
    two names instead.
    """

    PRIMITIVE: ClassVar[str] = "detect"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset({"total", "max_confidence"})
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {"total", "total_peak", "max_confidence"}
    )

    kind: Literal["detect"] = "detect"
    classes: list[str] = Field(min_length=1, description="Entity names from model.entity_mapping.")
    min_confidence: float | None = Field(
        default=None, ge=0.0, le=1.0, description="Overrides model.confidence_threshold."
    )
    min_confidence_per_class: dict[str, Annotated[float, Field(ge=0.0, le=1.0)]] = Field(
        default_factory=dict,
        description=(
            "Per-entity floors, overriding min_confidence for the entities named. Entity names "
            "from model.entity_mapping, and each must also appear in this stage's 'classes'."
        ),
    )
    smoothing: SmoothingConfig = Field(default_factory=SmoothingConfig)

    def frame_output_names(self) -> frozenset[str]:
        return self.STATIC_OUTPUTS | {f"{entity}.count" for entity in self.classes}

    def window_output_names(self) -> frozenset[str]:
        counts = {f"{entity}.count" for entity in self.classes}
        peaks = {f"{entity}.count_peak" for entity in self.classes}
        return (self.STATIC_WINDOW_OUTPUTS or frozenset()) | counts | peaks


# --- track -----------------------------------------------------------------


class TrackConfig(PrimitiveConfig):
    """``track`` — ID association.

    These knobs are hard-coded in ``engine_session.py:483`` today and no manifest can influence
    them; that is why every use case ships its own tracker copy.
    """

    PRIMITIVE: ClassVar[str] = "track"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset({"active_tracks"})
    #: ``active_tracks`` is a level, so the window names its two readings separately: the count
    #: on the last frame, and ``active_tracks_peak`` for the busiest moment.
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {"active_tracks", "active_tracks_peak"}
    )

    kind: Literal["track"] = "track"
    method: Literal["advanced", "bytetrack", "botsort", "sort", "oc_sort", "deepsort"] = "advanced"
    max_time_lost: int = Field(default=1200, ge=1, description="Frames. Raise for heavy occlusion.")
    track_buffer: int = Field(
        default=600,
        ge=1,
        description=(
            "How many retired tracks the re-identification pool keeps. The pool is what lets an "
            "object that was lost and then re-found keep its original track id; this bounds it by "
            "number of entries rather than by seconds, so a replay re-identifies exactly as a "
            "live stream does (the legacy pool expired on time.time() — PY-13). The legacy "
            "AdvancedTracker declared this field, documented it in its README and never read it; "
            "it now has this job, so raising it lengthens re-ID memory and 1 disables it."
        ),
    )
    match_thresh: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description=(
            "Maximum association COST, not a similarity — the name is inherited from the legacy "
            "tracker and reads backwards. The cost of a track/detection pair is 1 - IoU "
            "(optionally weighted by detection confidence), so the default 0.8 accepts any pair "
            "down to IoU 0.2, and LOWERING this makes matching stricter. Semantics are preserved "
            "rather than quietly inverted, because inverting them would change the behaviour of "
            "every migrated app."
        ),
    )
    new_track_thresh: float = Field(default=0.3, ge=0.0, le=1.0)
    min_hits: int | None = Field(
        default=None,
        ge=1,
        description=(
            "Frames of evidence a new track must accumulate before it is confirmed, emitted and "
            "counted. Null keeps the chosen method's own default: advanced, bytetrack and botsort "
            "use 1 (a track is emitted on its first frame), sort uses 2, oc_sort and deepsort use "
            "3. Set 3 to reproduce legacy footfall's confirmation window "
            "(post_processing/usecases/people_counting.py:1196-1213), which the default method "
            "(advanced, min_hits=1) does not: with it a one-frame ghost detection — a shadow, a "
            "reflection — counts. Raising it trades a small latency for far fewer spurious "
            "tracks; it never changes the per-method defaults themselves."
        ),
    )


# --- unique_count ----------------------------------------------------------


class UniqueCountConfig(PrimitiveConfig):
    """``unique_count`` — "how many distinct ones have I seen".

    ``total`` means *since the process last restarted*, not all time. The backend's rollup formula
    depends on exactly that (FROZEN-4); do not try to make it absolute.
    """

    PRIMITIVE: ClassVar[str] = "unique_count"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset({"new", "new_in_window", "total"})
    REQUIRES: ClassVar[tuple[str, ...]] = ("track",)

    kind: Literal["unique_count"] = "unique_count"
    by: Literal["track_id"] = "track_id"
    categories: list[str] = Field(min_length=1, description="Entity names to de-duplicate.")

    def frame_output_names(self) -> frozenset[str]:
        # window() republishes exactly these four: `new` is genuinely additive over the window,
        # `new_in_window` is the running total the window collapses to (the same reading, read
        # one frame earlier -- source it with agg_type: last for a live arrivals-so-far figure),
        # and `total` / `per_category.*` are cumulative levels. No key here has a second reading
        # that a peak would name.
        return self.STATIC_OUTPUTS | {f"per_category.{c}" for c in self.categories}


# --- zone_occupancy --------------------------------------------------------


class ZoneOccupancyConfig(PrimitiveConfig):
    """``zone_occupancy`` — polygon membership and per-zone counts.

    ``peak_occupancy`` / ``avg_occupancy`` are published **both** per frame and at the window
    boundary: per frame they are the high-water mark and mean *so far this window* (the same
    accumulators the window reading reads, exposed one frame earlier); at the boundary they are
    the window's final answer.  ``unassigned_count`` is this window's loss and
    ``unassigned_total`` the loss since process start (**FROZEN-4**).  All four were published
    and *not declared here* at one time or another, which made ``source:
    zone_occupancy.peak_occupancy`` a load error for a number the stage was already computing —
    the same mistake, twice, is why both output sets are declared explicitly rather than assumed.
    """

    PRIMITIVE: ClassVar[str] = "zone_occupancy"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"occupancy", "peak_occupancy", "avg_occupancy", "unassigned_count"}
    )
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {
            "occupancy",
            "peak_occupancy",
            "avg_occupancy",
            "unassigned_count",
            "unassigned_total",
            "frames",
        }
    )

    kind: Literal["zone_occupancy"] = "zone_occupancy"
    zones: Literal["all"] | list[str] = Field(
        default="all", description="'all', or the zone names as drawn in the streaming UI."
    )
    reference_point: Literal["foot_center", "bbox_center", "foot_75"] = "foot_center"
    on_no_match: Literal["unassigned", "drop", "error"] = "unassigned"

    @field_validator("zones")
    @classmethod
    def _check_zones(cls, value: Literal["all"] | list[str]) -> Literal["all"] | list[str]:
        if isinstance(value, list):
            if not value:
                raise ValueError(
                    "zone_occupancy.zones is an empty list, which matches no zone at all. Use "
                    "'all' (the default) or name the zones drawn in the streaming UI."
                )
            duplicates = {z for z in value if value.count(z) > 1}
            if duplicates:
                raise ValueError(
                    f"zone_occupancy.zones lists {_joined(duplicates)} more than once."
                )
        return value

    def frame_output_names(self) -> frozenset[str]:
        names = set(self.STATIC_OUTPUTS)
        names |= {f"per_zone.{identity}.count" for identity in self._zone_identities()}
        return frozenset(names)

    def window_output_names(self) -> frozenset[str]:
        names = set(self.STATIC_WINDOW_OUTPUTS or frozenset())
        for identity in self._zone_identities():
            # Three named readings per zone, for the same reason `occupancy` has three: a
            # per-zone headcount is a level, and last / peak / mean are different numbers.
            names |= {
                f"per_zone.{identity}.count",
                f"per_zone.{identity}.count_peak",
                f"per_zone.{identity}.avg",
            }
        return frozenset(names)

    def _zone_identities(self) -> tuple[str, ...]:
        """The zone identities this stage will publish, or ``()`` under ``zones: all``.

        ``zone_identity``, not the raw name: a drawn name may contain a dot ("Gate 1.2"), which
        would break the ``per_zone.<zone>.count`` key it is spliced into. The primitive publishes
        the identity, so declaring the raw name here meant the declared output never resolved.
        """
        if isinstance(self.zones, list):
            return tuple(zone_identity(zone) for zone in self.zones)
        return ()

    def output_patterns(self) -> tuple[re.Pattern[str], ...]:
        # With `zones: all` the zone names arrive at runtime from StreamInfo, so the manifest can
        # only check the *shape* of a per-zone source, not the zone name itself. `count` is
        # published at both scopes; `count_peak` and `avg` are window-only readings of it.
        if self.zones == "all":
            return (re.compile(r"^per_zone\.[^.]+\.(?:count|count_peak|avg)$"),)
        return ()

    def geometry_requirements(self) -> tuple[GeometryRequirement, ...]:
        return (
            GeometryRequirement(
                stage=self.stage_name,
                kind="zones",
                minimum=1,
                reason="With no zone geometry every detection lands in the 'unassigned' bucket.",
            ),
        )


# --- line_crossing ---------------------------------------------------------


class LineCrossingConfig(PrimitiveConfig):
    """``line_crossing`` — directional A/B counting.

    Nothing here needs a ``_peak`` name: ``in`` / ``out`` / ``net`` / ``untracked`` are counts of
    *events*, so the window's sum is the only reading of them, and ``total_*`` are cumulative
    levels whose current value is the only reading of *those*.  ``present`` is the one exception
    and is deliberately **frame-only**: the stage publishes no window value for it, so the
    runtime collapses its per-frame samples with the metric's own ``agg_type`` — the one place
    ``agg_type`` is load-bearing against a registered primitive.
    """

    PRIMITIVE: ClassVar[str] = "line_crossing"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"in", "out", "net", "total_in", "total_out", "total_net", "present", "untracked"}
    )
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {"in", "out", "net", "total_in", "total_out", "total_net", "untracked"}
    )
    REQUIRES: ClassVar[tuple[str, ...]] = ("track",)

    kind: Literal["line_crossing"] = "line_crossing"
    method: Literal["abline", "polygon"] = Field(
        description="abline = exactly 2 lines; polygon = 1 zone with an auto-inset inner boundary."
    )
    in_direction: Literal["A_to_B", "B_to_A"] = "A_to_B"
    reference_point: Literal["foot_center", "bbox_center", "foot_75"] = Field(
        default="foot_center",
        description=(
            "foot_center (100% down, default) or bbox_center (50% down) for a new app. "
            "foot_75 (75% down) exists only for bit-for-bit parity with specific legacy "
            "ground-truth benchmarks (VectorABLineCounter's own default calibration, "
            "counting_utils.py:612) -- see geometry.ReferencePoint."
        ),
    )
    inset_px: int | None = Field(
        default=None, ge=1, description="polygon only — inner boundary offset. Default 20."
    )
    expose_corridor_state: bool = Field(
        default=False,
        description=(
            "abline only. When true, publishes three extra things for the tracks currently "
            "*between* the two lines, labeled by which one they most recently crossed "
            "(in_direction-aware): per-frame `live_category.in` / `live_category.out` counts "
            "(feeds tracking_stats.current_counts / total_current_counts via a `custom`-style "
            "live snapshot), cumulative `per_category.in` / `per_category.out` mirroring "
            "total_in / total_out (feeds tracking_stats.total_counts / current_new_counts), "
            "and a `wire_detections` override so the frame's published detections list shows "
            "only these tracks, categorized `in`/`out` instead of the model's raw class. "
            "Off by default: every existing app keeps today's behaviour untouched."
        ),
    )
    include_completed_crossings: bool = Field(
        default=False,
        description=(
            "abline only. A track that COMPLETES a crossing this frame -- the frame it leaves "
            "the between-the-lines corridor, which is also the frame `in`/`out` increments -- "
            "is, by construction, no longer 'currently between the lines', so "
            "`expose_corridor_state` never includes it: that mechanism and the "
            "crossing-completion event are two different track populations on any given "
            "frame, and there was previously no way for a downstream stage to learn WHICH "
            "track_id caused this frame's `in`/`out` (only the aggregate counts). When this "
            "is true, publishes `in_track_ids` / `out_track_ids` -- comma-separated track_id "
            "strings (empty string when none), one entry per track that completed a crossing "
            "in that direction this exact frame. Plain string values, not "
            "`live_category.*`/`per_category.*`/`wire_detections` -- deliberately independent "
            "of `expose_corridor_state`'s corridor-occupancy meaning, so a downstream custom "
            "stage can read `ctx.previous['line_crossing'].values['in_track_ids']` (e.g. "
            "tailgating_detection's per-person suspect labeling) without also leaking `in`/"
            "`out` categories into tracking_stats alongside whatever categories that custom "
            "stage publishes itself, and without a second stage fighting over "
            "`wire_detections`. Off by default: every existing app keeps today's behaviour "
            "untouched."
        ),
    )

    @model_validator(mode="after")
    def _inset_is_polygon_only(self) -> LineCrossingConfig:
        if self.method == "abline" and self.inset_px is not None:
            raise ValueError(
                "line_crossing.inset_px applies to method: polygon only — it is the offset of the "
                "auto-generated inner boundary. With method: abline there is no polygon to inset; "
                "remove inset_px, or switch to method: polygon."
            )
        return self

    @model_validator(mode="after")
    def _corridor_state_is_abline_only(self) -> LineCrossingConfig:
        if self.method == "polygon" and self.expose_corridor_state:
            raise ValueError(
                "line_crossing.expose_corridor_state applies to method: abline only — it labels "
                "tracks by which of the two lines they most recently crossed, and method: polygon "
                "has no second line to define that. Remove expose_corridor_state, or switch to "
                "method: abline."
            )
        return self

    @model_validator(mode="after")
    def _completed_crossings_is_abline_only(self) -> LineCrossingConfig:
        if self.method == "polygon" and self.include_completed_crossings:
            raise ValueError(
                "line_crossing.include_completed_crossings applies to method: abline only — it "
                "labels a track by which of the two lines it just finished crossing, and method: "
                "polygon has no second line to define that. Remove include_completed_crossings, "
                "or switch to method: abline."
            )
        return self

    def frame_output_names(self) -> frozenset[str]:
        """The static set, plus conditional keys from ``expose_corridor_state`` and/or
        ``include_completed_crossings``.

        ``live_category.in``/``.out`` and ``per_category.in``/``.out`` only exist in
        ``process()``'s output when ``expose_corridor_state`` is on; ``in_track_ids``/
        ``out_track_ids`` only exist when ``include_completed_crossings`` is on (see each
        field's own docstring) — declaring them unconditionally in ``STATIC_OUTPUTS`` would let
        a metric source them on a manifest that never enables the flag, and the source would
        resolve at load time but read zero (or an empty string) forever at runtime, which is
        exactly the silent failure this conditional-set split exists to prevent.
        """
        names = self.STATIC_OUTPUTS
        if self.expose_corridor_state:
            names = names | {
                "live_category.in",
                "live_category.out",
                "per_category.in",
                "per_category.out",
            }
        if self.include_completed_crossings:
            names = names | {"in_track_ids", "out_track_ids"}
        return names

    def geometry_requirements(self) -> tuple[GeometryRequirement, ...]:
        """``abline`` infers direction from the order two parallel lines are crossed in.

        With one line there is no order and with three there is no pairing, so the direction is
        undefined and the counter silently reports zero. The runtime must fail loudly instead —
        this requirement is what it fails against.
        """
        if self.method == "abline":
            return (
                GeometryRequirement(
                    stage=self.stage_name,
                    kind="lines",
                    exact=2,
                    reason=(
                        "method: abline infers direction from the order in which two parallel "
                        "lines are crossed; with any other number the direction is undefined."
                    ),
                ),
            )
        return (
            GeometryRequirement(
                stage=self.stage_name,
                kind="zones",
                exact=1,
                reason="method: polygon counts entries across a band inset from one zone boundary.",
            ),
        )


# --- dwell -----------------------------------------------------------------


class DwellConfig(PrimitiveConfig):
    """``dwell`` — time-in-state per track. Written privately by 17 use cases, abstracted zero times."""

    PRIMITIVE: ClassVar[str] = "dwell"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"avg_seconds", "max_seconds", "over_threshold_count", "active_count"}
    )
    #: ``active_count`` is a level — how many are dwelling *now* — so the window names the last
    #: frame's value and ``active_count_peak`` separately.  ``over_threshold_count`` needs no
    #: peak: at window scope it is the number of **distinct tracks** that crossed the threshold,
    #: which is neither the last frame's value nor the peak and cannot be derived from either.
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {
            "avg_seconds",
            "max_seconds",
            # ``over_threshold_count`` keeps a third meaning at window scope: the number of
            # DISTINCT tracks that crossed the threshold, which is neither the last frame's
            # value nor the peak. The gauge the primitive computes every frame therefore gets
            # two names of its own rather than redefining that one -- renaming it would move
            # ``illegal_parking``'s live ``total_violations`` series under its own dashboard.
            # The ``_last`` suffix is explicit because the bare name is already taken.
            "over_threshold_count",
            "over_threshold_count_last",
            "over_threshold_count_peak",
            "active_count",
            "active_count_peak",
        }
    )
    REQUIRES: ClassVar[tuple[str, ...]] = ("track",)
    IMPLEMENTED: ClassVar[bool] = True

    kind: Literal["dwell"] = "dwell"
    state: Literal["in_zone", "present", "stationary"]
    threshold_seconds: float = Field(gt=0, description="The dwell duration that 'counts'.")
    min_presence_seconds: float = Field(
        default=1.0, ge=0, description="Ignore flickers below this."
    )
    track_timeout_seconds: float = Field(
        default=10.0, gt=0, description="Track lost ⇒ session ends."
    )
    gate: dict[str, str] | None = Field(
        default=None,
        description="Only accumulate while another primitive reports a state, e.g. {velocity_state: stationary}.",
    )

    def silent_buckets(self, *, zoned: bool = False) -> frozenset[str]:
        """``state: in_zone`` measures nothing without a zone, so it publishes nothing there.

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
        if self.state != "in_zone":
            return frozenset()
        return frozenset({UNASSIGNED_ZONE, GLOBAL_ZONE} if zoned else {UNASSIGNED_ZONE})

    @model_validator(mode="after")
    def _check_windows(self) -> DwellConfig:
        if self.min_presence_seconds >= self.threshold_seconds:
            raise ValueError(
                f"dwell.min_presence_seconds ({self.min_presence_seconds}) must be smaller than "
                f"dwell.threshold_seconds ({self.threshold_seconds}). min_presence_seconds "
                f"suppresses flickers before the clock starts; if it is not smaller than the "
                f"threshold, over_threshold_count can never be non-zero."
            )
        if self.gate is not None and not self.gate:
            raise ValueError(
                "dwell.gate is empty. Either remove it, or name the primitive and state that must "
                "hold, e.g. gate: {velocity_state: stationary}."
            )
        return self


# --- velocity_state --------------------------------------------------------


class VelocityStateConfig(PrimitiveConfig):
    """``velocity_state`` — per-track speed, heading and stationarity.

    Consolidates ten spellings of one concept found across six use cases
    (``velocity_threshold_px_per_sec``, ``short_term_displacement_threshold_px``,
    ``movement_threshold_percent``, …). Naming it once is most of the value (``08`` §2).
    """

    PRIMITIVE: ClassVar[str] = "velocity_state"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"state", "avg_speed", "stationary_count", "wrong_way_count"}
    )
    #: ``stationary_count`` is a level, so last and peak get separate names.  ``wrong_way_count``
    #: does not: at window scope it counts **distinct tracks** that went the wrong way, which a
    #: peak of a per-frame gauge cannot express.
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {
            "state",
            "avg_speed",
            "stationary_count",
            "stationary_count_peak",
            # ``wrong_way_count`` counts DISTINCT tracks that went the wrong way. That meaning
            # is kept; the per-frame gauge gets ``wrong_way_count_last`` -- which is what the
            # legacy ``current_wrong_way_count`` actually published -- and a peak beside it.
            "wrong_way_count",
            "wrong_way_count_last",
            "wrong_way_count_peak",
        }
    )
    REQUIRES: ClassVar[tuple[str, ...]] = ("track",)
    IMPLEMENTED: ClassVar[bool] = True

    kind: Literal["velocity_state"] = "velocity_state"
    window_seconds: float = Field(default=3.0, gt=0)
    stationary_below_px_per_sec: float = Field(default=5.0, ge=0)
    classes: dict[str, list[float | None]] = Field(
        default_factory=lambda: {
            "stationary": [0.0, 5.0],
            "slow": [5.0, 40.0],
            "moving": [40.0, None],
        },
        description="state name → [min_px_per_sec, max_px_per_sec]; null max means unbounded.",
    )
    heading: bool = Field(default=False, description="Emit heading; required for wrong-way logic.")
    expected_heading_deg: float | None = Field(default=None, ge=-360.0, le=360.0)
    heading_tolerance_deg: float = Field(default=60.0, gt=0, le=180.0)
    heading_from_line: bool = Field(
        default=False,
        description=(
            "Derive expected_heading_deg from a single drawn line's start->end direction "
            "(in drawing order) instead of a hand-typed angle. Requires heading: true, "
            "exactly one line drawn on the camera, and expected_heading_deg unset -- the two "
            "are alternative sources for one value, not additive. Exists for apps such as "
            "wrong-way driving where the correct direction is naturally 'the way this drawn "
            "line points', which an operator can set by drawing (the same two-point-line "
            "workflow line_crossing.method: abline uses), and a hand-typed compass bearing in "
            "an unconfirmed convention is not: a static angle with no relationship to what is "
            "drawn is unusably easy to get wrong or leave unset."
        ),
    )
    expose_wrong_way_state: bool = Field(
        default=False,
        description=(
            "heading: true only. When true, publishes a `wire_detections` override so the "
            "frame's published detections list shows every track with a DETERMINED heading "
            "state (enough samples in window_seconds to have been classified one way or the "
            "other) categorized `wrong_way` / `correct_way` instead of its detected class -- "
            "the same mechanism line_crossing.expose_corridor_state uses for `in`/`out`, "
            "reusing the SAME per-track wrong-way flag that already computes wrong_way_count "
            "rather than a second implementation. Tracks still accumulating their first "
            "window_seconds of samples, or classified stationary/unknown, are left unlabeled "
            "-- their detected class passes through unchanged, the same 'leave the undecided "
            "ones alone' choice expose_corridor_state makes for tracks not yet in its "
            "corridor. Also publishes per-frame `live_category.wrong_way` / "
            "`live_category.correct_way` counts (feeds tracking_stats.current_counts via the "
            "live_category.<entity> convention). Off by default: every existing app keeps "
            "today's vehicle-class-labeled behaviour untouched."
        ),
    )
    heading_auto_learn_fallback: bool = Field(
        default=False,
        description=(
            "heading_from_line: true only. Backup source for the expected direction when "
            "the camera has no line drawn yet: instead of refusing to start, learn the "
            "dominant traffic direction from observed tracks -- the same dominant-direction "
            "estimator wrong_way_tracker.py (the legacy usecase this primitive replaces) used "
            "as its own AUTO reference source. Wrong-way is not evaluated (every track reads "
            "not-wrong-way) until enough distinct, moving tracks agree on one direction; a "
            "camera that already has a line drawn is unaffected and keeps using it. This is "
            "a fallback for heading_from_line's missing-line case, not a third independent "
            "source -- it requires heading_from_line: true and never combines with "
            "expected_heading_deg."
        ),
    )

    @field_validator("classes")
    @classmethod
    def _check_classes(cls, value: dict[str, list[float | None]]) -> dict[str, list[float | None]]:
        for name, bounds in value.items():
            if len(bounds) != 2:
                raise ValueError(
                    f"velocity_state.classes.{name} must be a two-element range "
                    f"[min_px_per_sec, max_px_per_sec]; got {bounds!r}. Use null for an open "
                    f"upper bound, e.g. [40, null]."
                )
            low, high = bounds
            if low is None:
                raise ValueError(
                    f"velocity_state.classes.{name} has a null lower bound. Only the upper bound "
                    f"may be null (meaning unbounded); the lower bound must be a number."
                )
            if high is not None and high <= low:
                raise ValueError(
                    f"velocity_state.classes.{name} range [{low}, {high}] is empty — the upper "
                    f"bound must be greater than the lower bound, so no track can ever be "
                    f"classified {name!r}."
                )
        return value

    @model_validator(mode="after")
    def _heading_fields_need_heading(self) -> VelocityStateConfig:
        if self.expected_heading_deg is not None and not self.heading:
            raise ValueError(
                "velocity_state.expected_heading_deg is set but heading: false, so no heading is "
                "computed and wrong_way_count would always be 0. Set heading: true."
            )
        if self.heading_from_line and not self.heading:
            raise ValueError(
                "velocity_state.heading_from_line is set but heading: false, so no heading is "
                "computed and wrong_way_count would always be 0. Set heading: true."
            )
        return self

    @model_validator(mode="after")
    def _heading_source_is_one_thing(self) -> VelocityStateConfig:
        if self.heading_from_line and self.expected_heading_deg is not None:
            raise ValueError(
                "velocity_state declares both heading_from_line: true and "
                f"expected_heading_deg: {self.expected_heading_deg}. They are two alternative "
                "sources for the same one value -- pick a hand-typed angle or a drawn line, "
                "not both. Remove expected_heading_deg to use the drawn line, or set "
                "heading_from_line: false to use the angle."
            )
        if self.heading_auto_learn_fallback and not self.heading_from_line:
            raise ValueError(
                "velocity_state.heading_auto_learn_fallback is set but heading_from_line is "
                "not. heading_auto_learn_fallback is a backup for heading_from_line's "
                "missing-line case, not an independent source -- set heading_from_line: true "
                "as well, or drop heading_auto_learn_fallback and use expected_heading_deg "
                "for a fixed angle instead."
            )
        return self

    @model_validator(mode="after")
    def _expose_wrong_way_state_needs_heading(self) -> VelocityStateConfig:
        if self.expose_wrong_way_state and not self.heading:
            raise ValueError(
                "velocity_state.expose_wrong_way_state is set but heading: false, so no track "
                "is ever classified wrong-way or correct-way and every box would be left "
                "unlabeled. Set heading: true."
            )
        return self

    def frame_output_names(self) -> frozenset[str]:
        """The static set, plus `live_category.*` when `expose_wrong_way_state` is set.

        Mirrors ``LineCrossingConfig.frame_output_names`` -- see its docstring for why these
        are conditional rather than always declared in ``STATIC_OUTPUTS``: a metric sourcing
        ``live_category.wrong_way`` on a manifest that never sets the flag would resolve at
        load time but read zero forever at runtime, the exact silent failure the conditional
        split exists to prevent.
        """
        names = self.STATIC_OUTPUTS
        if self.expose_wrong_way_state:
            names = names | {"live_category.wrong_way", "live_category.correct_way"}
        return names

    def geometry_requirements(self) -> tuple[GeometryRequirement, ...]:
        """``heading_from_line`` needs exactly one line to have an unambiguous direction.

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
        if self.heading_from_line and not self.heading_auto_learn_fallback:
            return (
                GeometryRequirement(
                    stage=self.stage_name,
                    kind="lines",
                    exact=1,
                    reason=(
                        "heading_from_line derives the expected direction from one drawn "
                        "line's start->end vector; with any other number the reference "
                        "direction is undefined. Set heading_auto_learn_fallback: true to "
                        "learn the direction from traffic instead of requiring a line."
                    ),
                ),
            )
        return ()


# --- ratio_compliance ------------------------------------------------------


class RatioComplianceConfig(PrimitiveConfig):
    """``ratio_compliance`` — "what fraction of X satisfies Y"."""

    PRIMITIVE: ClassVar[str] = "ratio_compliance"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"subject_count", "compliant_count", "violation_count", "compliance_pct", "violation_pct"}
    )
    #: The window republishes **only** the two percentages, as the mean over the frames that had
    #: a subject — a ratio is neither summable nor the ratio of the window's totals.  The counts
    #: are deliberately absent, so the runtime collapses their per-frame samples with the
    #: metric's own ``agg_type``; that is why ``violation_count`` with ``agg_type: sum`` works.
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {"compliance_pct", "violation_pct"}
    )

    kind: Literal["ratio_compliance"] = "ratio_compliance"
    subject: str = Field(description="The entity being assessed — usually 'person'.")
    required: list[str] = Field(
        default_factory=list, description="ALL must be present for the subject to count compliant."
    )
    violations: list[str] = Field(
        default_factory=list, description="Explicit negative classes, e.g. no_hardhat."
    )
    iou_threshold: float = Field(default=0.1, ge=0.0, le=1.0)
    emit: list[str] | None = Field(
        default=None, description="Restrict the published values to this subset of the outputs."
    )

    @field_validator("emit", mode="before")
    @classmethod
    def _normalise_emit(cls, value: Any) -> Any:
        """``08`` §2.1 writes ``emit: {compliant_count, violation_count}``, which YAML parses as a
        mapping with null values. Accept that spelling and the list form."""
        if isinstance(value, dict):
            return list(value)
        return value

    @model_validator(mode="after")
    def _check_attributes(self) -> RatioComplianceConfig:
        if not self.required and not self.violations:
            raise ValueError(
                "ratio_compliance declares neither 'required' nor 'violations', so every subject "
                "is trivially compliant and compliance_pct is always 100. Give it at least one "
                "required attribute (e.g. required: [hardhat]) or one violation class "
                "(e.g. violations: [defect])."
            )
        overlap = set(self.required) & set(self.violations)
        if overlap:
            raise ValueError(
                f"ratio_compliance lists {_joined(overlap)} as both required and a violation. The "
                f"same class cannot make a subject compliant and non-compliant."
            )
        if self.subject in set(self.required) | set(self.violations):
            raise ValueError(
                f"ratio_compliance.subject {self.subject!r} also appears as an attribute. The "
                f"subject is who is assessed; attributes are what is looked for on them."
            )
        if self.emit is not None:
            unknown = set(self.emit) - self.output_names()
            if unknown:
                raise ValueError(
                    f"ratio_compliance.emit names {_joined(unknown)}, which this primitive does "
                    f"not produce. Available: {_joined(self.output_names())}."
                )
        return self

    def frame_output_names(self) -> frozenset[str]:
        attrs = list(self.required) + list(self.violations)
        return self.STATIC_OUTPUTS | {f"{a}_count" for a in attrs}


# --- incident_quantise -----------------------------------------------------


class QuantiseLevel(ManifestModel):
    """One rung of the severity ladder: at or above ``percentage``, the severity is ``level``."""

    level: SeverityLiteral
    percentage: float = Field(ge=0.0, le=100.0)

    @field_validator("level", mode="before")
    @classmethod
    def _lowercase_only(cls, value: Any) -> Any:
        return _validate_severity(value, "incident_quantise.levels[].level")


def _validate_severity(value: Any, where: str) -> Any:
    """Severity is lowercase on the wire; old manifests wrote ``HIGH`` (``06`` §2).

    Nothing validates severity on ingest, so an uppercase value is stored verbatim and the
    backend's escalation check then defaults it to "this is an escalation" — a stuck-critical
    incident. Reject rather than normalise, so the manifest says what actually ships.
    """
    raw = str(value).strip()
    if raw in SEVERITY_LEVELS:
        return raw
    if raw.lower() in SEVERITY_LEVELS:
        raise ValueError(
            f"{where}: severity {raw!r} must be lowercase — write {raw.lower()!r}. The wire "
            f"vocabulary is lowercase and nothing normalises it on ingest, so an uppercase value "
            f"is stored verbatim and compares unequal to every known level."
        )
    raise ValueError(
        f"{where}: {raw!r} is not a severity level. Use one of: {', '.join(SEVERITY_LEVELS)}."
        f"{_did_you_mean(raw.lower(), SEVERITY_LEVELS)}"
    )


class IncidentQuantiseConfig(PrimitiveConfig):
    """``incident_quantise`` — magnitude → severity.

    Pick the strategy from what actually makes the situation worse: a bigger fire is a worse fire
    (``area_ratio``); one confidently-detected pistol is critical at any size (``max_confidence``);
    more potholes is worse (``count_based``).
    """

    PRIMITIVE: ClassVar[str] = "incident_quantise"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"level", "level_rank", "area", "confidence"}
    )

    kind: Literal["incident_quantise"] = "incident_quantise"
    strategy: Literal["area_ratio", "max_confidence", "count_based"]
    threshold_area: float | None = Field(
        default=None,
        gt=0,
        le=1.0,
        description=(
            "area_ratio only. A NORMALIZED area fraction in (0, 1] -- the share of the "
            "frame the detection covers, not a pixel count."
        ),
    )
    count_threshold: int | None = Field(default=None, gt=0, description="count_based only.")
    area_source: str = Field(
        default="",
        description=(
            "area_ratio only. Name of an earlier 'segmentation_area' stage whose area_ratio "
            "(true mask coverage, 0-1) replaces this stage's own bounding-box area sum as the "
            "area_ratio strategy's magnitude. Unset (default) keeps the bounding-box sum -- the "
            "right choice for a plain detector (fire/smoke boxes ARE the hazard's extent). Set "
            "this when the model is a segmentation model and an irregular mask's true coverage "
            "differs meaningfully from its bounding box (e.g. landslide, flood): a diagonal or "
            "L-shaped hazard's box can overstate coverage severalfold."
        ),
    )
    levels: list[QuantiseLevel] = Field(min_length=1)
    order: Literal["ascending", "descending"] = "ascending"

    @model_validator(mode="after")
    def _check_strategy_fields(self) -> IncidentQuantiseConfig:
        needs = {"area_ratio": "threshold_area", "count_based": "count_threshold"}
        required_field = needs.get(self.strategy)
        if required_field and getattr(self, required_field) is None:
            raise ValueError(
                f"incident_quantise.strategy: {self.strategy} needs {required_field}. It is the "
                f"denominator the level percentages are measured against; without it every "
                f"detection quantises to the lowest level."
            )
        for field_name, owner in (
            ("threshold_area", "area_ratio"),
            ("count_threshold", "count_based"),
        ):
            if getattr(self, field_name) is not None and self.strategy != owner:
                raise ValueError(
                    f"incident_quantise.{field_name} applies to strategy: {owner} only, but this "
                    f"stage uses strategy: {self.strategy}. Remove it, or change the strategy."
                )
        if self.area_source and self.strategy != "area_ratio":
            raise ValueError(
                f"incident_quantise.area_source applies to strategy: area_ratio only, but this "
                f"stage uses strategy: {self.strategy}. Remove it, or change the strategy."
            )

        percentages = [level.percentage for level in self.levels]
        ordered = sorted(percentages, reverse=self.order == "descending")
        if percentages != ordered:
            raise ValueError(
                f"incident_quantise.levels percentages {percentages} are not in {self.order} "
                f"order. The runtime walks the ladder in order; out-of-order rungs make the "
                f"severity depend on list position rather than magnitude. Sort them, or set "
                f"order: {'descending' if self.order == 'ascending' else 'ascending'}."
            )
        if len(set(percentages)) != len(percentages):
            raise ValueError(
                f"incident_quantise.levels reuses a percentage ({percentages}). Two rungs at the "
                f"same magnitude make the resulting severity depend on list order."
            )
        seen_levels = [level.level for level in self.levels]
        repeated = {level for level in seen_levels if seen_levels.count(level) > 1}
        if repeated:
            raise ValueError(
                f"incident_quantise.levels declares {_joined(repeated)} more than once. Each "
                f"severity is one rung of the ladder; a repeat makes the mapping from magnitude "
                f"to severity depend on list order."
            )
        return self


# --- state_machine ---------------------------------------------------------


def _validate_confirm_frames(value: Any, where: str) -> Any:
    """``confirm_frames`` below 3 is rejected, never silently raised.

    The old engine clamped it to 3 (``base_processor.py:78``) so the manifest said one thing and
    the runtime did another — defect **PY-11**. Rejecting is the whole difference: the author
    learns their value was impossible instead of believing it took effect.
    """
    # A bool is an int subclass, and pydantic's lax mode coerces both `True` and
    # `1.0` to `1`. Returning early for them -- as this validator first did --
    # skipped the floor check and let the coercion produce a 1 anyway, so
    # `confirm_frames: 1.0` and `confirm_frames: true` both reinstated exactly
    # the PY-11 behaviour this function exists to prevent. Found by the Stage A
    # verification pass as finding F3.
    if isinstance(value, bool):
        raise ValueError(
            f"{where}: expected a whole number of frames, got the boolean {value!r}. "
            f"Set {where.rsplit('.', 1)[-1]}: {MIN_CONFIRM_FRAMES} or higher."
        )
    if isinstance(value, float):
        if not value.is_integer():
            return value  # a fractional frame count; let int coercion complain
        value = int(value)
    if not isinstance(value, int):
        return value  # let the normal int coercion produce its own message
    if value < MIN_CONFIRM_FRAMES:
        raise ValueError(
            f"{where}: {value} is below the minimum of {MIN_CONFIRM_FRAMES}. Fewer than "
            f"{MIN_CONFIRM_FRAMES} frames of confirmation cannot reject single-frame artefacts. "
            f"The old engine silently raised values below {MIN_CONFIRM_FRAMES} to "
            f"{MIN_CONFIRM_FRAMES} (defect PY-11); this schema rejects them instead, so the "
            f"manifest states what actually runs. Set {where.rsplit('.', 1)[-1]}: "
            f"{MIN_CONFIRM_FRAMES} or higher."
        )
    return value


class StateMachineConfig(PrimitiveConfig):
    """``state_machine`` — N-of-M confirmation with persistence/recovery hysteresis."""

    PRIMITIVE: ClassVar[str] = "state_machine"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"state", "active", "confirmed_frames", "confirmed_new"}
    )
    #: ``confirmed_frames`` is the evidence counter, a level: the window names its current value
    #: and ``confirmed_frames_peak`` separately.  ``active`` needs no peak — it is a 0/1 flag
    #: whose window reading is "held at any point", which *is* its maximum.
    #:
    #: ``confirmed_new`` is the odd one out: an *event* count, not a level, so it needs no peak
    #: either -- it is 1 on the frame the machine transitions into CONFIRMED and 0 every other
    #: frame, and at window scope it is the number of such transitions this window (summed, same
    #: shape as ``unique_count.new``). It exists for exactly the case ``unique_count`` cannot
    #: cover: counting distinct *episodes* of a condition that has no object identity to
    #: deduplicate by (no bounding box, no track id -- a whole-frame classifier). A tracker's
    #: re-identification pool (``track.track_buffer``) will happily re-associate a second,
    #: unrelated episode with the first one's track id when the "object" is a stationary,
    #: featureless full-frame box, which makes ``unique_count.new`` under-count episodes that
    #: recur after a gap. This counter has no such pool -- it is a plain hits/confirmed flag with
    #: no memory of a previous episode -- so it cannot make that mistake.
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {"state", "active", "confirmed_frames", "confirmed_frames_peak", "confirmed_new"}
    )

    kind: Literal["state_machine"] = "state_machine"
    confirm_frames: int = Field(
        default=5, description=f"N-of-M confirmation. Minimum {MIN_CONFIRM_FRAMES}."
    )
    recovery_frames: int = Field(
        default=3, ge=1, description="Clear frames before the state drops."
    )
    decay: Literal["soft", "hard"] = Field(
        default="soft", description="soft = a miss decrements by 1; hard = a miss resets to 0."
    )

    @field_validator("confirm_frames", mode="before")
    @classmethod
    def _check_confirm_frames(cls, value: Any) -> Any:
        return _validate_confirm_frames(value, "state_machine.confirm_frames")


# --- proximity -------------------------------------------------------------


class ProximityConfig(PrimitiveConfig):
    """``proximity`` — inter-object distance.

    Pixel↔metre calibration has no home in ``StreamInfo`` today (``08`` §10), so ``calibration``
    is a free-form block until that is settled; distances are in pixels meanwhile.
    """

    PRIMITIVE: ClassVar[str] = "proximity"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset({"violation_count", "min_observed"})
    IMPLEMENTED: ClassVar[bool] = False

    kind: Literal["proximity"] = "proximity"
    subject: str
    target: str
    min_distance_px: float = Field(gt=0)
    calibration: dict[str, float] | None = Field(
        default=None, description="Optional pixel↔metre calibration, e.g. {px_per_metre: 42.0}."
    )


# --- keypoint_pose ---------------------------------------------------------


class KeypointPoseConfig(PrimitiveConfig):
    """``keypoint_pose`` — skeleton-derived logic (fall detection, posture)."""

    PRIMITIVE: ClassVar[str] = "keypoint_pose"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset({"pose_state", "match_count"})
    IMPLEMENTED: ClassVar[bool] = True

    kind: Literal["keypoint_pose"] = "keypoint_pose"
    skeleton_type: Literal["coco17", "coco18", "custom"] = "coco17"
    rules: list[dict[str, Any]] = Field(
        min_length=1, description="Named pose rules over keypoints."
    )


# --- segmentation_area -----------------------------------------------------


class SegmentationAreaConfig(PrimitiveConfig):
    """``segmentation_area`` — mask area over frame area."""

    PRIMITIVE: ClassVar[str] = "segmentation_area"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset(
        {"area_ratio", "max_area_ratio", "instance_count", "measured_count", "area_px"}
    )
    STATIC_WINDOW_OUTPUTS: ClassVar[frozenset[str] | None] = frozenset(
        {"area_ratio", "area_ratio_peak", "max_area_ratio", "instance_count", "measured_count"}
    )
    IMPLEMENTED: ClassVar[bool] = True

    kind: Literal["segmentation_area"] = "segmentation_area"
    classes: list[str] = Field(min_length=1)
    normalize: Literal["frame", "none"] = "frame"
    reduce: Literal["max", "sum"] = Field(
        default="max",
        description=(
            "How multiple instances' coverage collapses to one area_ratio. max: the largest "
            "single instance (flood_detection's semantics). sum: total coverage across every "
            "instance, double-counting any overlap (landslide_detection's "
            "total_landslide_area_pct semantics) -- the only behavioural difference between "
            "the two legacy apps this primitive replaces."
        ),
    )
    clamp: bool = Field(
        default=True,
        description="Clamp the reduced area_ratio to 1.0. Only affects reduce: sum, which can exceed it.",
    )
    on_missing_mask: Literal["error", "bbox_proxy", "zero"] = Field(
        default="error",
        description=(
            "A detection of 'classes' with no usable mask: error (default) fails loudly -- a "
            "mask-free frame on a segmentation app means the mask half of the pipeline is not "
            "running. bbox_proxy substitutes the bounding-box area (legacy's silent fallback, "
            "named and counted in measured_count here). zero counts it as no coverage."
        ),
    )


class IdentityMatchConfig(PrimitiveConfig):
    """``identity_match`` — watchlist match (plates, faces).

    Not implemented. No primitive registers under ``identity_match``, so a manifest that used
    it validated cleanly and then failed at pipeline build with a bare registry ``KeyError``.
    ``IMPLEMENTED = False`` moves that discovery to load time, where
    :meth:`AppManifest.unimplemented_primitives` reports it and the loader logs it — the
    manifest still validates on purpose (``08`` §2), so an author can write the config ahead
    of the runtime.
    """

    PRIMITIVE: ClassVar[str] = "identity_match"
    STATIC_OUTPUTS: ClassVar[frozenset[str]] = frozenset({"match_count", "matched_ids"})
    IMPLEMENTED: ClassVar[bool] = False

    kind: Literal["identity_match"] = "identity_match"
    watchlist_source: str = Field(description="Where the watchlist comes from, e.g. 'deployment'.")
    match_field: str = Field(description="The detection field compared against the watchlist.")


# --- custom ----------------------------------------------------------------


class CustomConfig(PrimitiveConfig):
    """``custom`` — the escape hatch (``08`` §9, ``09`` §6).

    Custom code never touches the wire format, never re-implements a primitive, and never does
    network I/O or loads a model. Its ``values`` keys are known only to its Python, so metric
    sources under this namespace cannot be verified from the manifest alone; the loader checks the
    symbol and its ``Config`` instead.
    """

    PRIMITIVE: ClassVar[str] = "custom"
    OPEN_OUTPUTS: ClassVar[bool] = True

    kind: Literal["custom"] = "custom"
    impl: str = Field(description='"./logic.py:ClassName" — a file in the app folder and a symbol.')
    config: dict[str, Any] = Field(
        default_factory=dict, description="Validated at load time against the class's Config model."
    )
    zones: Literal["per_zone", "all_in_one"] = Field(
        default="per_zone",
        description=(
            "per_zone (default): one instance per zone bucket, each seeing only its own zone — "
            "the standard partition. all_in_one: one instance, in the 'global' bucket only, "
            "seeing every detection with det.zone still carrying the zone each one was assigned "
            "to. Opt into it only for logic that must observe a TRANSITION between zones."
        ),
    )

    @property
    def all_in_one(self) -> bool:
        """``zones: all_in_one`` — the whole frame in one call, zones still on the detections.

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
        return self.zones == "all_in_one"

    @field_validator("impl")
    @classmethod
    def _check_impl(cls, value: str) -> str:
        match = _IMPL_RE.match(value)
        if not match:
            raise ValueError(
                f"custom.impl {value!r} is not a valid reference. Write "
                f"'impl: \"./logic.py:ClassName\"' — a path to a Python file inside the app "
                f"folder, a colon, and the class name."
            )
        module = match.group("module").strip()
        if not module.endswith(".py"):
            raise ValueError(
                f"custom.impl {value!r} must point at a .py file inside the app folder, "
                f'e.g. "./logic.py:ClassName". Got module part {module!r}.'
            )
        if (
            module.startswith(("/", "\\"))
            or re.match(r"^[A-Za-z]:", module)
            or ".." in module.split("/")
        ):
            raise ValueError(
                f"custom.impl {value!r} must stay inside the app folder: no absolute paths and no "
                f"'..' segments. An app that reaches outside its own folder cannot be shipped as "
                f"a zip."
            )
        return value

    def output_patterns(self) -> tuple[re.Pattern[str], ...]:
        return (re.compile(r"^[^\s]+$"),)

    def describe_outputs(self) -> str:
        return "whatever the custom class returns in PrimitiveOutput.values"


# --- the union -------------------------------------------------------------

PipelineStage = Annotated[
    Union[  # noqa: UP007 - Field(discriminator=...) needs the explicit Union form
        DetectConfig,
        TrackConfig,
        UniqueCountConfig,
        ZoneOccupancyConfig,
        LineCrossingConfig,
        DwellConfig,
        VelocityStateConfig,
        RatioComplianceConfig,
        IncidentQuantiseConfig,
        StateMachineConfig,
        ProximityConfig,
        KeypointPoseConfig,
        SegmentationAreaConfig,
        IdentityMatchConfig,
        CustomConfig,
    ],
    Field(discriminator="kind"),
]

#: primitive name → config model. Built once, used by the pipeline parser, the error messages and
#: the JSON Schema generator.
PRIMITIVES: dict[str, type[PrimitiveConfig]] = {
    model.PRIMITIVE: model
    for model in (
        DetectConfig,
        TrackConfig,
        UniqueCountConfig,
        ZoneOccupancyConfig,
        LineCrossingConfig,
        DwellConfig,
        VelocityStateConfig,
        RatioComplianceConfig,
        IncidentQuantiseConfig,
        StateMachineConfig,
        ProximityConfig,
        KeypointPoseConfig,
        SegmentationAreaConfig,
        IdentityMatchConfig,
        CustomConfig,
    )
}

#: Primitives that were retired rather than renamed, with the reason. Naming them in the error is
#: cheaper than the author reading the whole vocabulary to find out why their key is unknown.
_REJECTED_PRIMITIVES: dict[str, str] = {
    "spatial_heatmap": (
        "Retired 2026-07-31 after auditing what it would replace. Three independent reasons, any "
        "one sufficient: (1) the legacy producer has never worked -- heatmaps.py and "
        "crowd_density_heatmaps.py both divide by context.frame_shape, which ProcessingContext "
        "does not have (core/base.py:41-78), and the AttributeError is swallowed by an enclosing "
        "bare except, so the grid has always been all zeros; (2) no consumer exists -- grepping "
        "fe-streaming, be-analytics and be-media-server for it returns nothing; (3) it could not "
        "be emitted anyway, because PrimitiveOutput.values takes scalars and the output is an "
        "image-shaped array. If per-pixel density is genuinely wanted, it needs a consumer and a "
        "wire surface designed first -- not a primitive."
    ),
    "attribute_classify": (
        "Retired 2026-08-01: secondary inference moves upstream (backlog Q6, decided), so the "
        "model emits the attribute on the detection and post-processing receives it ready to "
        "use. Needed by 11 use cases on paper and by zero as specified: seven are pure "
        "label-readers whose attribute is already a model class, which detect + unique_count "
        "covers today (mask_type_detection, cardiomegaly_classification, "
        "skin_cancer_classification_img, face_emotion, gender_detection, age_detection, "
        "age_gender_detection -- face_emotion.py imports torch for one softmax over a 7-vector); "
        "the two that genuinely classify need onnxruntime/torch and raw pixels inside "
        "post-processing, which is inference, not analytics; and the 'attribute attached to a "
        "parent detection' shape this config model implies does not exist -- every legacy join "
        "is exact track_id equality. There IS a real primitive hiding inside -- per-track "
        "attribute stabilisation, written four times with four different algorithms (EMA, "
        "majority vote, running mean, modal) -- but it is not what this schema describes and it "
        "needs its own name and its own outputs. Ask for that one."
    ),
    "ocr_text": (
        "OCR is inference, not analytics — it belongs upstream of post-processing (08 §2). "
        "Have the model emit the text as a detection field."
    ),
    "alerts": (
        "Alerting is not a pipeline stage. Raise incidents from the 'incidents:' block, or let "
        "the customer build a backend alert rule on one of your metrics."
    ),
    "smoothing": (
        "Smoothing is not a stage — it is the 'smoothing:' block inside 'detect', and its "
        "defaults already match what 105 of 123 existing configs use."
    ),
    "zones": (
        "Zone interpretation is the top-level 'zones:' block; per-zone counting is the 'zone_occupancy' primitive."
    ),
}


# ---------------------------------------------------------------------------
# metrics:
# ---------------------------------------------------------------------------


def _validate_metric_key(value: str, where: str) -> str:
    """Shared key gate for ``metrics[]`` and ``derived[]``.

    Both lists publish into the *same* wire namespace — a ``MetricEntry.key`` — so a key that
    is legal in one and not the other would be a distinction with no downstream meaning.
    """
    if not _METRIC_KEY_RE.match(value):
        raise ValueError(
            f"{where} {value!r} is not a valid metric key. Keys must match "
            f"^[A-Za-z][A-Za-z0-9_]*$ — no spaces, dots or hyphens. A dot would collide with "
            f"the source syntax and a space breaks the {{key}} interpolation in human_text. "
            f"snake_case is the house style."
        )
    return value


def _validate_agg_type(value: Any, where: str) -> Any:
    """Shared ``agg_type`` gate. ``avg``/``average``/``median`` are rejected by name."""
    raw = str(value).strip()
    replacement = {"avg": "mean", "average": "mean", "median": "mean"}.get(raw.lower())
    if replacement:
        why = (
            "the backend's vocabulary is 'mean'; accepting both spellings is how PY-1 shipped, "
            "where the unknown value fell back to 'sum' and every percentage was published as "
            "a 60-second sum (~150,000% at 25fps)"
            if raw.lower() != "median"
            else "the backend silently computes a mean for 'median' (BE-1), so declaring it "
            "would be a lie about what the dashboard shows"
        )
        raise ValueError(f"{where} {raw!r} is rejected — use {replacement!r} instead: {why}.")
    if raw not in AGG_TYPES:
        raise ValueError(
            f"{where} {raw!r} is not valid. Use one of: "
            f"{', '.join(sorted(AGG_TYPES))}. Counts of events are 'sum', rates and "
            f"percentages are 'mean', a current level is 'last', a window peak is 'max'."
            f"{_did_you_mean(raw.lower(), AGG_TYPES)}"
        )
    return raw


def _validate_unit(value: str | None, where: str) -> str | None:
    """Shared units-registry gate (``06-vocabularies.md`` §10)."""
    if value is None:
        return value
    raw = value.strip()
    if raw not in UNIT_DIMENSIONS:
        by_dimension: dict[str, list[str]] = {}
        for spelling, dimension in UNIT_DIMENSIONS.items():
            by_dimension.setdefault(dimension, []).append(spelling)
        listing = "; ".join(
            f"{dimension}: {', '.join(sorted(spellings))}"
            for dimension, spellings in sorted(by_dimension.items())
        )
        raise ValueError(
            f"{where} {raw!r} is not in the units registry, so the backend will reject "
            f"any alert rule built on this metric. Omit the unit, or use one of — {listing}."
            f"{_did_you_mean(raw.lower(), UNIT_DIMENSIONS)}"
        )
    return raw


@dataclass(frozen=True)
class ResolvedSource:
    """A ``metrics[].source`` that has been checked against the pipeline."""

    source: str
    stage: str
    value: str
    #: ``True`` when the producing stage is ``custom``, whose outputs live in the author's Python
    #: and therefore cannot be verified from the manifest.
    unverified: bool = False
    #: ``True`` when the producing stage's ``window()`` publishes this value name — i.e. the
    #: number is **already aggregated** and the engine publishes it verbatim, so this metric's
    #: ``agg_type`` does not choose it.  ``False`` for a ``custom`` stage (which has no
    #: ``window()``) and for a frame-only output such as ``line_crossing.present``, where the
    #: runtime really does collapse the retained per-frame samples with ``agg_type``.
    #:
    #: Two metrics sharing one already-aggregated source **cannot** hold two different numbers
    #: however their ``agg_type``\\ s differ; that is the defect this flag exists to make
    #: reviewable, and the reason ``detect`` publishes ``person.count`` *and*
    #: ``person.count_peak``.
    window_aggregated: bool = False
    #: ``True`` when the operand was written ``global.<stage>.<value>`` and must therefore be
    #: read from the ``global`` bucket rather than from the zone the metric is being computed
    #: for.  Only ``derived[].expr`` may ask for this (:func:`resolve_source` rejects it
    #: elsewhere), and only a ``zone: per_zone`` metric has anything to gain: it is what lets
    #: a per-zone expression divide by a **frame-wide** number.
    #:
    #: Without it there is no way to write "this zone's share of the whole frame": every
    #: operand resolves inside one bucket, so a zone's count over a zone's count is the same
    #: population twice and reads 100%, while mixing an occlusion-surviving numerator with an
    #: instantaneous denominator reads *over* 100%.  The global bucket holds the whole frame
    #: (``Session._partition``), so the number already exists -- this only addresses it.
    from_global: bool = False


class MetricSpec(ManifestModel):
    """One entry in ``metrics:`` — one series on the dashboard.

    ``key`` is a *shared, producer-defined namespace*: it must match ``metrics.json``'s ``key``
    and ``widgets.json``'s ``dataKey`` character for character, and nothing anywhere validates the
    join (``06-vocabularies.md`` §13). Renaming one silently empties every chart and alert rule built
    on it, which is why a rename is a manifest ``version`` bump with a recorded migration.
    """

    key: str = Field(
        description="Metric namespace. Must match metrics.json key / widgets.json dataKey."
    )
    agg_type: AggTypeLiteral = Field(description="sum | mean | min | max | last.")
    category: CategoryLiteral
    source: str = Field(description="<primitive>.<value>, resolved against the pipeline.")
    unit: str | None = Field(default=None, description="From the units registry. Needed to alert.")
    zone: Literal["per_zone", "global", "collapsed"] = "global"
    """Which series this metric is.

    ``global``
        One row, read from the whole-frame bucket.
    ``per_zone``
        One row **per emission zone**, each labelled with its zone. The breakdown.
    ``collapsed``
        One row, labelled ``global``, holding the ``across_zones`` reduction over the drawn
        zones. The same number ``result['metrics']`` already carried per frame, now on
        ``results-agg`` too.

    ``collapsed`` exists because ``(key, zone)`` is the primary key on the wire and ``key``
    alone is the primary key in ``widgets.json`` -- a widget names one ``dataKey`` and draws one
    line. A ``per_zone`` metric therefore arrives at a dashboard as N rows sharing a timestamp,
    and every consumer that flattens without reading ``zone`` shows them as duplicates or keeps
    whichever arrived last. Declaring ``collapsed`` lets the app author say which of the two a
    key is, instead of leaving it to the consumer to guess.

    On an unzoned app ``collapsed`` is identical to ``global``: there is one bucket, so the
    reduction is over one number.
    """

    across_zones: AcrossZonesLiteral = Field(
        default="sum",
        description=(
            "How the zones collapse into ONE number: sum (default, for counts), max (for a "
            "max_* reading) or mean (for an average or a percentage). Used by the flat "
            "per-frame result['metrics'] map for zone: per_zone, and by zone: collapsed for "
            "its single results-agg row. Ignored for zone: global, which already has exactly "
            "one zone. zone: per_zone still publishes one results-agg row per zone."
        ),
    )

    @field_validator("key")
    @classmethod
    def _check_key(cls, value: str) -> str:
        return _validate_metric_key(value, "metrics[].key")

    @field_validator("agg_type", mode="before")
    @classmethod
    def _check_agg_type(cls, value: Any) -> Any:
        return _validate_agg_type(value, "metrics[].agg_type")

    @field_validator("category", mode="before")
    @classmethod
    def _check_category(cls, value: Any) -> Any:
        return _validate_category(value, "metrics[].category")

    @field_validator("unit")
    @classmethod
    def _check_unit(cls, value: str | None) -> str | None:
        """A unit outside the registry makes *backend alert-rule creation* fail with an unhelpful
        message, long after the manifest shipped (``06-vocabularies.md`` §10)."""
        return _validate_unit(value, "metrics[].unit")

    @field_validator("source")
    @classmethod
    def _check_source_shape(cls, value: str) -> str:
        """Shape only; resolution against the pipeline happens on the whole manifest."""
        raw = value.strip()
        if "." not in raw or any(not part for part in raw.split(".")) or re.search(r"\s", raw):
            raise ValueError(
                f"metrics[].source {value!r} is not a source reference. Write "
                f"'<primitive>.<value>', e.g. 'unique_count.new' or 'detect.person.count'."
            )
        return raw

    @property
    def dimension(self) -> str | None:
        """The unit's dimension, or ``None`` when no unit is declared."""
        return UNIT_DIMENSIONS.get(self.unit) if self.unit else None


# ---------------------------------------------------------------------------
# derived:
#
# The one thing no primitive can do: divide one stage's output by another's. Three shipped
# apps lose their headline KPI to that gap -- `car_damage_detection.defect_rate`,
# `vehicle_monitoring_wrong_way.violation_rate` and `loitering_detection.loitering_percentage`
# (_migration/wave-d1/group{2,3}/PORT_REPORT.md). It is declarative rather than Python
# because a use case is a YAML file (objective **O3**): a division should not cost an app a
# `logic.py`, a test module and a code review.
# ---------------------------------------------------------------------------

#: Where a derived value is computed, which decides whether ``agg_type`` does anything.
#: See :class:`DerivedMetricSpec` for the whole argument; the one-line version is that a
#: value computed from already-aggregated window outputs **is** already aggregated.
DerivedScopeLiteral = Literal["window", "frame"]

#: Unit spellings whose dimension makes a metric a rate. ``sum`` over 60 seconds of these is
#: **PY-1** in numeric form (~150,000% at 25fps), so ``derived[]`` rejects the combination.
_RATIO_DIMENSION = "ratio"


class DerivedMetricSpec(ManifestModel):
    """One entry in ``derived:`` — a metric computed from other stages' outputs.

    ::

        derived:
          - key: defect_rate
            agg_type: mean
            category: QUALITY
            unit: percent
            expr: defect_unique.new / inspected_unique.new * 100

    On the wire this is an ordinary :class:`~matrice_analytics.engine.contract.schemas.MetricEntry`
    — the dashboard cannot tell a derived series from a sourced one, and must not be able to.
    The separate block is for the *author* and the *reviewer*: ``metrics[]`` reads one number a
    stage published, ``derived[]`` computes one, and those have different failure modes.

    **``agg_type`` on a derived value — the rule this block exists to get right.**

    ``scope`` decides it, and the default is inferred from the operands:

    ``scope: window`` (the default when **every** operand is a window output)
        The expression is evaluated **once**, at the aggregation boundary, over numbers the
        producing stages already collapsed.  The result is therefore *already aggregated* and
        is published verbatim — the engine does **not** apply ``agg_type`` to it, for exactly
        the reason it does not apply ``agg_type`` to a
        :class:`~matrice_analytics.engine.primitives.base.WindowOutput` value (**PY-1**, §6b
        coupling 4).  ``agg_type`` still travels on the wire, because it is how the *backend*
        collapses these 60-second readings into its five-minute rollup.
        :attr:`ResolvedDerived.window_aggregated` is ``True``, which is the same flag
        :class:`ResolvedSource` uses to say the same thing.

    ``scope: frame`` (the default when any operand is frame-only, e.g. ``line_crossing.present``
    or a ``custom`` stage's value)
        The expression is evaluated **per retained frame** and the samples are collapsed with
        ``agg_type`` (:func:`~matrice_analytics.engine.runtime.window.collapse`).  Here
        ``agg_type`` is load-bearing, and ``mean`` means "the mean of the per-frame rate over
        the frames that had one" — which is precisely what legacy ``loitering_percentage``
        published (``legacy_analytics_bridge.py``:1680-1686, 2561-2564).

    Declaring a ``scope`` the operands cannot support is a load error rather than a silent
    reinterpretation.  So is mixing a window-only operand with a frame-only one: there is no
    scope in which that expression has a value, and the engine will not invent one.

    **A zero denominator publishes 0.0.**  ``expr`` is evaluated by
    :mod:`matrice_analytics.engine.manifest.expr`, which returns *undefined* for a zero
    denominator; an undefined reading contributes no sample, and a metric with no samples
    publishes ``0.0``.  That matches all four legacy rate producers and it is the only
    behaviour that cannot put ``NaN`` on the wire, which costs the whole window (finding
    **F1**).
    """

    key: str = Field(
        description="Metric namespace. Must match metrics.json key / widgets.json dataKey."
    )
    agg_type: AggTypeLiteral = Field(
        description=(
            "How the BACKEND collapses these 60-second readings into its five-minute rollup. "
            "At scope: window the engine does not re-apply it (the value is already "
            "aggregated); at scope: frame it also chooses how per-frame samples collapse. "
            "A percentage is 'mean', never 'sum'."
        )
    )
    category: CategoryLiteral
    expr: str = Field(
        description=(
            "Arithmetic over '<stage>.<value>' sources: + - * / and parentheses, e.g. "
            "'dwell.over_threshold_count / detect.person.count * 100'. Every operand is "
            "resolved against the pipeline at load time."
        )
    )
    unit: str | None = Field(default=None, description="From the units registry. Needed to alert.")
    zone: Literal["per_zone", "global", "collapsed"] = "global"
    """As :attr:`MetricSpec.zone`. ``collapsed`` publishes one ``results-agg`` row holding the
    ``across_zones`` reduction, which for a percentage is what a dashboard can actually draw."""

    across_zones: AcrossZonesLiteral = Field(
        default="sum",
        description=(
            "With zone: per_zone or zone: collapsed, how the zones collapse into ONE number. "
            "A percentage or a ratio almost always "
            "wants 'mean' -- summing two zones' percentages is how a percent metric reads "
            "over 100. See metrics[].across_zones."
        ),
    )
    scope: DerivedScopeLiteral | None = Field(
        default=None,
        description=(
            "'window' evaluates once at the boundary over already-aggregated outputs; 'frame' "
            "evaluates per frame and collapses the samples with agg_type. Omit it and the "
            "engine infers the only scope the operands support."
        ),
    )

    @field_validator("key")
    @classmethod
    def _check_key(cls, value: str) -> str:
        return _validate_metric_key(value, "derived[].key")

    @field_validator("agg_type", mode="before")
    @classmethod
    def _check_agg_type(cls, value: Any) -> Any:
        return _validate_agg_type(value, "derived[].agg_type")

    @field_validator("category", mode="before")
    @classmethod
    def _check_category(cls, value: Any) -> Any:
        return _validate_category(value, "derived[].category")

    @field_validator("unit")
    @classmethod
    def _check_unit(cls, value: str | None) -> str | None:
        return _validate_unit(value, "derived[].unit")

    @field_validator("expr", mode="before")
    @classmethod
    def _check_expr(cls, value: Any) -> Any:
        """Syntax only. Operands are resolved against the pipeline by the whole-manifest pass.

        Parsing here rather than at first use is the difference between a rejected manifest and
        a stack trace out of a 3am aggregation boundary.
        """
        try:
            parse_expression(value)
        except ExpressionError as error:
            raise ValueError(f"derived[].expr: {error}") from error
        return str(value).strip()

    @model_validator(mode="after")
    def _a_rate_is_never_a_sum(self) -> DerivedMetricSpec:
        """``unit: percent`` with ``agg_type: sum`` is **PY-1** written out longhand.

        Summing a percentage over a rollup window produces ~150,000% at 25fps, which is what
        shipped when an unknown ``agg_type`` fell back to ``sum``.  A derived metric is
        overwhelmingly a rate, so this is the one combination the block refuses outright.
        """
        if self.dimension == _RATIO_DIMENSION and self.agg_type == "sum":
            raise ValueError(
                f"derived[] {self.key!r} declares unit {self.unit!r} (a ratio) with "
                f"agg_type: sum. A rate is never summed: the backend would add every "
                f"60-second reading in its five-minute rollup and chart ~500% for a steady "
                f"100%, which is PY-1 in numeric form. Use agg_type: mean."
            )
        return self

    @property
    def dimension(self) -> str | None:
        """The unit's dimension, or ``None`` when no unit is declared."""
        return UNIT_DIMENSIONS.get(self.unit) if self.unit else None

    @property
    def expression(self) -> DerivedExpression:
        """The parsed :attr:`expr`.

        Re-parsed on access, which costs microseconds and happens at load and at session
        setup only — never per frame.  The runtime keeps the parsed object in its plan
        (:func:`~matrice_analytics.engine.runtime.window.derived_plan`).
        """
        return parse_expression(self.expr)


@dataclass(frozen=True)
class ResolvedDerived:
    """A ``derived[]`` entry whose expression has been checked against the pipeline."""

    spec: DerivedMetricSpec
    expression: DerivedExpression
    #: Where the expression is evaluated: ``"window"`` (once, over already-aggregated outputs)
    #: or ``"frame"`` (per frame, samples collapsed with ``agg_type``).
    scope: DerivedScopeLiteral
    #: Every operand, resolved, in first-appearance order.
    operands: tuple[ResolvedSource, ...]

    @property
    def window_aggregated(self) -> bool:
        """``True`` when the engine must publish this value **verbatim**.

        The same statement :attr:`ResolvedSource.window_aggregated` makes, for the same
        reason: a number computed from already-aggregated inputs is already aggregated, and
        re-applying ``metrics[].agg_type`` to it is **PY-1**.
        """
        return self.scope == "window"


# ---------------------------------------------------------------------------
# incidents:
# ---------------------------------------------------------------------------


class ThresholdLevel(ManifestModel):
    """One rung of a graded ``severity_from`` threshold."""

    value: float
    level: SeverityLiteral

    @field_validator("level", mode="before")
    @classmethod
    def _lowercase_only(cls, value: Any) -> Any:
        return _validate_severity(value, "severity_from.levels[].level")


class MetricThreshold(ManifestModel):
    """The ``{">": 15}`` form of ``severity_from``, optionally graded by ``levels``."""

    gt: float | None = Field(default=None, alias=">")
    gte: float | None = Field(default=None, alias=">=")
    lt: float | None = Field(default=None, alias="<")
    lte: float | None = Field(default=None, alias="<=")
    eq: float | None = Field(default=None, alias="==")
    ne: float | None = Field(default=None, alias="!=")
    levels: list[ThresholdLevel] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    @model_validator(mode="after")
    def _needs_a_condition(self) -> MetricThreshold:
        operators = {
            ">": self.gt,
            ">=": self.gte,
            "<": self.lt,
            "<=": self.lte,
            "==": self.eq,
            "!=": self.ne,
        }
        if not any(v is not None for v in operators.values()) and not self.levels:
            raise ValueError(
                "severity_from threshold has no condition. Give it a comparison "
                "(e.g. {\">\": 0}) or a graded 'levels' list; an empty threshold never fires, so "
                "the incident type would be dead config."
            )
        if self.levels:
            values = [level.value for level in self.levels]
            if values != sorted(values):
                raise ValueError(
                    f"severity_from levels {values} are not in ascending order of 'value'. The "
                    f"runtime walks them in order, so out-of-order rungs make the severity depend "
                    f"on list position."
                )
        return self

    @property
    def operators(self) -> dict[str, float]:
        pairs = {
            ">": self.gt,
            ">=": self.gte,
            "<": self.lt,
            "<=": self.lte,
            "==": self.eq,
            "!=": self.ne,
        }
        return {op: value for op, value in pairs.items() if value is not None}


class IncidentType(ManifestModel):
    """One incident type — what reaches ``incident_res`` and becomes an alert in the UI."""

    key: str = Field(description="snake_case; must match the app version's incidentTypes[].key.")
    name: str | None = Field(default=None, description="Display name.")
    severity_from: str | dict[str, MetricThreshold] = Field(
        description=(
            "'incident_quantise' (take a quantiser stage's level), a fixed severity level, or "
            "{metric_key: {'>': value}} thresholds."
        )
    )
    human_text: str = Field(
        min_length=1,
        description=(
            "User-facing alert title with {metric_key} interpolation. An operator reads this on a "
            "phone at 3am — write it for them, not for a log grep."
        ),
    )
    category: CategoryLiteral

    @field_validator("key")
    @classmethod
    def _check_key(cls, value: str) -> str:
        if not _APP_ID_RE.match(value):
            raise ValueError(
                f"incidents.types[].key {value!r} must match ^[a-z][a-z0-9_]*$ (snake_case). It is "
                f"joined to the app version's incidentTypes[].key by exact string match."
            )
        return value

    @field_validator("category", mode="before")
    @classmethod
    def _check_category(cls, value: Any) -> Any:
        return _validate_category(value, "incidents.types[].category")

    @field_validator("severity_from", mode="before")
    @classmethod
    def _check_severity_from_shape(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, dict):
            if not value:
                raise ValueError(
                    "incidents.types[].severity_from is empty. Use 'incident_quantise', a fixed "
                    "severity level, or {metric_key: {'>': value}}."
                )
            return value
        raise ValueError(
            f"incidents.types[].severity_from must be a primitive name, a fixed severity level, or "
            f"a {{metric_key: {{operator: value}}}} mapping; got {type(value).__name__}."
        )

    def interpolated_keys(self) -> tuple[str, ...]:
        """The ``{metric_key}`` placeholders in ``human_text``."""
        return tuple(
            match.group(1).strip() for match in _INTERPOLATION_RE.finditer(self.human_text)
        )


class IncidentLifecycle(ManifestModel):
    """When an incident opens, escalates and closes.

    Two behaviours that surprise people and are not configurable: incidents cannot de-escalate (the
    backend ignores a downward severity change), and only an end time closes one — which is what
    ``close_after_empty_frames`` produces.
    """

    confirm_frames: int = Field(default=5, description=f"Minimum {MIN_CONFIRM_FRAMES}.")
    close_after_empty_frames: int = Field(default=101, ge=1, description="~4s at 25fps.")
    emit_on: Literal["transition", "never"] = Field(
        default="transition",
        description=(
            "'transition' is the only sensible value and the default — the backend does up-only "
            "escalation and treats a repeat of the same severity as a no-op. Written explicitly "
            "so the behaviour is visible rather than implied."
        ),
    )

    @field_validator("confirm_frames", mode="before")
    @classmethod
    def _check_confirm_frames(cls, value: Any) -> Any:
        return _validate_confirm_frames(value, "incidents.lifecycle.confirm_frames")


class IncidentSpec(ManifestModel):
    """``incidents:`` — what reaches ``incident_res``."""

    types: list[IncidentType] = Field(min_length=1)
    lifecycle: IncidentLifecycle = Field(default_factory=IncidentLifecycle)

    @field_validator("types")
    @classmethod
    def _unique_keys(cls, value: list[IncidentType]) -> list[IncidentType]:
        seen: set[str] = set()
        for incident in value:
            if incident.key in seen:
                raise ValueError(
                    f"incidents.types declares {incident.key!r} twice. Incident keys are the join "
                    f"to the app version's incidentTypes[] and to the alert feed; duplicates make "
                    f"the second definition unreachable."
                )
            seen.add(incident.key)
        return value


# ---------------------------------------------------------------------------
# zones: / emission: / tests:
# ---------------------------------------------------------------------------


class ZonesSpec(ManifestModel):
    """``zones:`` — how per-camera geometry is interpreted. Not the geometry itself.

    Geometry is per-camera installation data on ``StreamInfo``, normalized 0-1. The manifest
    describes the use case, not the installation (``08`` §5).
    """

    required: bool = Field(
        default=False,
        description=(
            "true ⇒ a camera with no geometry is a startup error. Set it when the app is "
            "meaningless without zones; the alternative is silent degradation that presents as "
            "'the numbers look wrong'."
        ),
    )
    source: Literal["stream_info"] = "stream_info"
    on_no_match: Literal["unassigned", "drop", "error"] = Field(
        default="unassigned",
        description=(
            "Detections outside every zone. Today they are silently dropped with no counter "
            "(PY-10); 'unassigned' routes them to a visible bucket so the loss is countable."
        ),
    )
    on_overlap: Literal["first_match", "all_match", "error"] = Field(
        default="first_match",
        description=(
            "Today first-match wins by dict insertion order, i.e. undefined. Declaring it makes "
            "an overlap either a deliberate choice or a validation error."
        ),
    )


class EmissionSpec(ManifestModel):
    """``emission:`` — cadence and windowing."""

    window_seconds: int = Field(
        default=60, gt=0, le=3600, description="results-agg cadence. The backend buckets at 5 min."
    )
    emit_empty_windows: bool = Field(
        default=True,
        description=(
            "false ⇒ the app publishes nothing on results-agg when no tracking was seen, and is "
            "invisible on every volume dashboard. That is today's behaviour "
            "(legacy_analytics_bridge.py:3007); the flag makes it a choice."
        ),
    )
    frame_summary: bool = Field(
        default=True, description="Populate agg_summary on the frame return."
    )


class SkipEntry(ManifestModel):
    """A skipped generated test, and why.

    A bare skip is how a suite rots: nobody can tell an intentional gap from an abandoned one.
    """

    test: str = Field(min_length=1, description="The generated test to skip.")
    reason: str = Field(min_length=1, description="Why. Required — a skip without one is rot.")


class TestsSpec(ManifestModel):
    """``tests:`` — extra configuration for the *generated* suite (``08`` §7).

    An empty block is the norm. A config-only app writes no tests at all.
    """

    fixtures: list[str] = Field(
        default_factory=list, description="Real detection frames, e.g. samples/*.json."
    )
    golden: str | None = Field(
        default=None, description="Golden output file, regenerated with --update-golden."
    )
    skip: list[SkipEntry] = Field(default_factory=list)

    @field_validator("skip", mode="before")
    @classmethod
    def _skip_needs_reason(cls, value: Any) -> Any:
        if isinstance(value, list):
            for entry in value:
                if isinstance(entry, str):
                    raise ValueError(
                        f"tests.skip entry {entry!r} has no reason. Every skip needs a written "
                        f"justification: '- {{test: {entry}, reason: <why>}}'. Skipping silently "
                        f"is how a suite rots."
                    )
        return value

    @field_validator("fixtures", "golden")
    @classmethod
    def _paths_stay_inside_the_app(cls, value: Any) -> Any:
        """Fixture paths are resolved relative to the app folder, which may be an unpacked zip."""
        paths = value if isinstance(value, list) else ([value] if value else [])
        for path in paths:
            text = str(path).replace("\\", "/")
            if text.startswith("/") or re.match(r"^[A-Za-z]:", text) or ".." in text.split("/"):
                raise ValueError(
                    f"tests path {path!r} must be relative to the app folder, with no '..' "
                    f"segments — the app has to work as an unpacked zip on another machine."
                )
        return value


# ---------------------------------------------------------------------------
# The manifest
# ---------------------------------------------------------------------------

#: Top-level keys from the pre-refactor manifest format, with what to do instead. Matching by name
#: turns "extra inputs are not permitted" into a migration instruction.
_LEGACY_TOP_LEVEL_KEYS: dict[str, str] = {
    "alerts": (
        "The 'alerts:' block is gone. In the old format it was parsed (engine.py:95) and then "
        "completely ignored — base_processor.py:142 hard-coded alerts=[] — so it looked live to "
        "whoever wrote a manifest and did nothing (defect PY-12). Thresholds now belong either in "
        "'incidents:' (evaluated by the engine, raising an operator-visible incident) or in a "
        "backend alert rule built on one of your metrics (evaluated by be-analytics on the cron "
        "tick, and configured by the customer in the UI)."
    ),
    "categories": (
        "Top-level 'categories:' is gone. Each metric now carries its own 'category:', and "
        "'app.category' is the app's primary grouping."
    ),
    "entity_mapping": "Move 'entity_mapping' under the 'model:' section.",
    "index_to_category": "Move 'index_to_category' under the 'model:' section.",
    "safety": "The per-category module blocks are replaced by 'pipeline:' — see 08 §2.",
    "volume": "The per-category module blocks are replaced by 'pipeline:' — see 08 §2.",
    "quality": "The per-category module blocks are replaced by 'pipeline:' — see 08 §2.",
    "identity": "The per-category module blocks are replaced by 'pipeline:' — see 08 §2.",
    "special": "The per-category module blocks are replaced by 'pipeline:' — see 08 §2.",
    "tracking": "Tracker settings are the 'track' primitive in 'pipeline:'.",
    "smoothing": "Smoothing is the 'smoothing:' block inside the 'detect' primitive.",
    "incident_config": "Renamed to 'incidents:' — see 08 §4.",
}


class AppManifest(ManifestModel):
    """A complete ``app.yaml``.

    Construct it through :func:`matrice_analytics.engine.manifest.loader.load_app` rather than
    directly, so that custom code and sibling files are checked too.
    """

    schema_version: int = Field(description="This schema's version, not the app's. Always 1 today.")
    app: AppSpec
    model: ModelSpec
    pipeline: list[PipelineStage] = Field(min_length=1)
    metrics: list[MetricSpec] = Field(default_factory=list)
    derived: list[DerivedMetricSpec] = Field(
        default_factory=list,
        description="Metrics computed from other stages' outputs, e.g. a rate. See DerivedMetricSpec.",
    )
    incidents: IncidentSpec | None = None
    zones: ZonesSpec | None = None
    emission: EmissionSpec = Field(default_factory=EmissionSpec)
    tests: TestsSpec = Field(default_factory=TestsSpec)

    # -- pre-parse ---------------------------------------------------------

    @model_validator(mode="before")
    @classmethod
    def _reject_legacy_top_level(cls, data: Any) -> Any:
        """Name every retired top-level key explicitly.

        ``extra="forbid"`` alone would say "extra inputs are not permitted", which tells an author
        migrating a 2024 manifest nothing about where the block went.
        """
        if not isinstance(data, dict):
            return data
        for key, guidance in _LEGACY_TOP_LEVEL_KEYS.items():
            if key in data:
                raise ValueError(f"'{key}:' is not part of the app manifest. {guidance}")
        return data

    @field_validator("schema_version", mode="before")
    @classmethod
    def _check_schema_version(cls, value: Any) -> Any:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(
                f"schema_version must be the integer {MANIFEST_SCHEMA_VERSION}; got {value!r}. It "
                f"is this schema's version, not your app's — app.version is where yours goes."
            )
        if value != MANIFEST_SCHEMA_VERSION:
            raise ValueError(
                f"schema_version {value} is not supported by this engine, which understands "
                f"version {MANIFEST_SCHEMA_VERSION}. Either the manifest is from a newer engine, "
                f"or you meant app.version."
            )
        return value

    @field_validator("pipeline", mode="before")
    @classmethod
    def _parse_pipeline_entries(cls, value: Any) -> Any:
        """Turn the on-disk ``- detect: {...}`` form into the tagged form the union discriminates on.

        On disk a stage is a one-key mapping whose key is the primitive name; internally every
        config carries ``kind`` so the union is a real Pydantic tagged union (fast, and it produces
        a ``oneOf`` with a discriminator in the generated JSON Schema).
        """
        if not isinstance(value, list):
            return value

        parsed: list[Any] = []
        for index, entry in enumerate(value):
            where = f"pipeline[{index}]"

            # `- track` with no config at all.
            if isinstance(entry, str):
                entry = {entry: {}}

            if not isinstance(entry, dict):
                raise ValueError(
                    f"{where} must be a single-key mapping naming one primitive, e.g. "
                    f"'- detect: {{classes: [person]}}'; got {type(entry).__name__}."
                )

            # Already tagged (constructed in Python rather than parsed from YAML).
            if "kind" in entry:
                parsed.append(entry)
                continue

            if len(entry) != 1:
                raise ValueError(
                    f"{where} names {len(entry)} primitives ({_joined(entry)}) in one list entry. "
                    f"Each pipeline entry is one primitive — the order of the list is the order "
                    f"they run in, so give each its own '- ' entry."
                )

            ((primitive, config),) = entry.items()
            if primitive not in PRIMITIVES:
                reason = _REJECTED_PRIMITIVES.get(str(primitive))
                if reason:
                    raise ValueError(
                        f"{where}: '{primitive}' is not a pipeline primitive. {reason}"
                    )
                raise ValueError(
                    f"{where}: '{primitive}' is not a known primitive. Available: "
                    f"{_joined(PRIMITIVES)}.{_did_you_mean(str(primitive), PRIMITIVES)}"
                )

            if config is None:  # `- track:` with an empty body
                config = {}
            if not isinstance(config, dict):
                raise ValueError(
                    f"{where}: '{primitive}' must be given a mapping of settings (or nothing at "
                    f"all); got {type(config).__name__}."
                )
            parsed.append({**config, "kind": primitive})
        return parsed

    # -- cross-field validation -------------------------------------------

    @model_validator(mode="after")
    def _validate_manifest(self) -> AppManifest:
        """Every check that needs more than one section. Order matters: the cheapest and most
        explanatory failures come first, because Pydantic reports the first raise."""
        self._check_stage_names()
        self._check_entities()
        self._check_detect_floors()
        self._check_ordering()
        self._check_emits_something()
        self._check_metric_sources()
        self._check_derived()
        self._check_metric_zones()
        self._check_incidents()
        return self

    def _check_stage_names(self) -> None:
        """A source is ``<stage>.<value>``, so stage names must be unique."""
        seen: dict[str, int] = {}
        for index, stage in enumerate(self.pipeline):
            name = stage.stage_name
            if name in seen:
                raise ValueError(
                    f"pipeline[{index}] and pipeline[{seen[name]}] both resolve to the stage name "
                    f"{name!r}, so 'source: {name}.<value>' would be ambiguous. Give one of them a "
                    f"'name:' (e.g. 'name: {name}_secondary') and reference that instead."
                )
            seen[name] = index

    def _check_entities(self) -> None:
        """Every entity referenced by a primitive must exist in ``model.entity_mapping``.

        An unmapped class name is the single most common cause of an empty dashboard, and it
        produces no error today at all (``FIELD_REFERENCE`` §14).
        """
        known = self.model.entities

        def check(values: object, where: str) -> None:
            for entity in values:  # type: ignore[union-attr]
                if entity not in known:
                    raise ValueError(
                        f"{where}: {entity!r} is not in model.entity_mapping, so it can never "
                        f"match a detection. Declared entities: {_joined(known)}."
                        f"{_did_you_mean(str(entity), known)}"
                    )

        for index, stage in enumerate(self.pipeline):
            where = f"pipeline[{index}].{stage.stage_name}"
            if isinstance(stage, DetectConfig):
                check(stage.classes, f"{where}.classes")
                check(stage.min_confidence_per_class, f"{where}.min_confidence_per_class")
            elif isinstance(stage, UniqueCountConfig):
                check(stage.categories, f"{where}.categories")
            elif isinstance(stage, RatioComplianceConfig):
                check([stage.subject], f"{where}.subject")
                check(stage.required, f"{where}.required")
                check(stage.violations, f"{where}.violations")
            elif isinstance(stage, SegmentationAreaConfig):
                check(stage.classes, f"{where}.classes")
            elif isinstance(stage, ProximityConfig):
                check([stage.subject], f"{where}.subject")
                check([stage.target], f"{where}.target")

    def _check_detect_floors(self) -> None:
        """A ``min_confidence_per_class`` floor for a class the stage does not detect is dead.

        Runs *after* :meth:`_check_entities`, so an unmapped name is reported as unmapped —
        the more useful of the two answers, and the one that catches a typo. What is left for
        this check is the entity that exists but is not in **this stage's** ``classes``: the
        floor is then never consulted, and a threshold that silently does nothing is worse than
        no threshold, because someone will tune it. ``NO-Hardhat`` at 0.91 is exactly the
        number that must not go quiet (``usecases/ppe_compliance.py:220-244``).
        """
        for index, stage in enumerate(self.pipeline):
            if not isinstance(stage, DetectConfig):
                continue
            unused = [e for e in stage.min_confidence_per_class if e not in stage.classes]
            if unused:
                raise ValueError(
                    f"pipeline[{index}].{stage.stage_name}.min_confidence_per_class names "
                    f"{_joined(unused)}, which this stage does not detect — its 'classes' are "
                    f"{_joined(stage.classes)}. The floor would never be consulted. Add the "
                    f"entity to 'classes', or drop the floor."
                    f"{_did_you_mean(unused[0], stage.classes)}"
                )

    def _check_ordering(self) -> None:
        """Primitives that consume track ids must come after ``track``; ``dwell.gate`` must point
        at a stage that already ran."""
        seen: list[str] = []
        for index, stage in enumerate(self.pipeline):
            for dependency in stage.REQUIRES:
                if dependency not in seen:
                    raise ValueError(
                        f"pipeline[{index}].{stage.stage_name} needs a '{dependency}' stage before "
                        f"it in the pipeline. Without {dependency!r} it sees each frame in "
                        f"isolation — for unique_count that means counting the same object once "
                        f"per frame, which is the classic 'counts far too high' report."
                    )
            if isinstance(stage, DwellConfig) and stage.gate:
                for gated_on in stage.gate:
                    if gated_on not in seen:
                        raise ValueError(
                            f"pipeline[{index}].{stage.stage_name}.gate refers to {gated_on!r}, "
                            f"which is not a stage declared before it. Stages so far: "
                            f"{_joined(seen)}.{_did_you_mean(gated_on, list(PRIMITIVES))}"
                        )
            seen.append(stage.stage_name)
            if stage.PRIMITIVE not in seen:
                # Reference either by explicit name or by primitive name.
                seen.append(stage.PRIMITIVE)

    def _check_emits_something(self) -> None:
        if not self.metrics and not self.derived and self.incidents is None:
            raise ValueError(
                "This manifest declares neither 'metrics:' nor 'derived:' nor 'incidents:', so the "
                "app computes a pipeline and publishes nothing. Declare at least one metric, or an "
                "incident type."
            )

    def _check_metric_sources(self) -> None:
        """``source`` must resolve to an output of a declared primitive.

        This is the rule the whole schema exists for: today a typo produces a metric that reads
        zero forever and nothing anywhere says so (``09`` §3).
        """
        for index, metric in enumerate(self.metrics):
            resolve_source(self, metric.source, where=f"metrics[{index}] ({metric.key})")

    def _check_derived(self) -> None:
        """Every ``derived[].expr`` operand must resolve, and the scope must be one that works.

        The same rule ``metrics[].source`` gets, through the same function: an operand that
        does not resolve is a **load error**, never a metric that silently reads zero
        (``09`` §3). The extra work here is the scope, because a derived value's ``agg_type``
        means one thing over window outputs and another over per-frame samples.
        """
        declared = {metric.key for metric in self.metrics}
        for index, spec in enumerate(self.derived):
            where = f"derived[{index}] ({spec.key})"
            if spec.key in declared:
                raise ValueError(
                    f"{where}: {spec.key!r} is already declared in this manifest. One key is one "
                    f"series on the dashboard, so two definitions publish two rows with the same "
                    f"key in one message and whichever the backend keeps is undefined. Rename one, "
                    f"or delete the duplicate."
                )
            declared.add(spec.key)
            resolve_derived(self, spec, where=where)

    def _check_metric_zones(self) -> None:
        """A zone-scoped metric without zone assignment publishes one series called 'global'.

        ``collapsed`` needs a partition for the same reason ``per_zone`` does: with nothing
        assigning detections there is one bucket, so the reduction is over one number and the
        key silently means "the global bucket" -- which is what ``zone: global`` says plainly.
        """
        zoned_scopes = {"per_zone", "collapsed"}
        offenders = [(m.key, m.zone) for m in self.metrics if m.zone in zoned_scopes]
        offenders += [(d.key, d.zone) for d in self.derived if d.zone in zoned_scopes]
        if not offenders:
            return
        has_zone_stage = any(isinstance(stage, ZoneOccupancyConfig) for stage in self.pipeline)
        if not has_zone_stage and self.zones is None:
            scopes = sorted({scope for _key, scope in offenders})
            declared = " / ".join(f"zone: {scope}" for scope in scopes)
            raise ValueError(
                f"metric(s) {_joined([key for key, _scope in offenders])} declare {declared}, but "
                f"nothing in this manifest assigns detections to zones — so every value would "
                f"land in the single 'global' bucket. Add a 'zone_occupancy' stage, or a "
                f"top-level 'zones:' block, or use 'zone: global'."
            )
        self._check_all_in_one_sources()
        # Not inside `_check_all_in_one_sources`: that one returns early when the pipeline has
        # no `all_in_one` stage, which is almost every app, and would silently skip this.
        self._check_named_zone_sources()

    def _check_all_in_one_sources(self) -> None:
        """A ``zone: per_zone`` metric cannot source a ``zones: all_in_one`` stage.

        An ``all_in_one`` stage runs **once**, in the ``global`` bucket, so it produces no
        output in any zone bucket and a per-zone series over it would be empty in every zone.
        That is precisely the metric-that-reads-nothing-forever this schema exists to catch
        (``09`` §3), and it is invisible in a green test run because "metric present" is
        satisfied by zeros.
        """
        all_in_one = {stage.stage_name for stage in self.pipeline if stage.all_in_one}
        if not all_in_one:
            return
        for index, metric in enumerate(self.metrics):
            if metric.zone != "per_zone":
                continue
            stage = resolve_source(self, metric.source, where=f"metrics[{index}]").stage
            if stage in all_in_one:
                raise ValueError(
                    f"metrics[{index}] ({metric.key}) declares 'zone: per_zone' but sources "
                    f"{metric.source!r}, and stage {stage!r} declares 'zones: all_in_one' — it "
                    f"runs once over the whole frame, in the 'global' bucket, and publishes "
                    f"nothing in any zone bucket. The per-zone series would be empty in every "
                    f"zone. Use 'zone: global' for this metric, or drop 'zones: all_in_one' from "
                    f"the stage."
                )
        for index, spec in enumerate(self.derived):
            if spec.zone != "per_zone":
                continue
            for operand in resolve_derived(self, spec, where=f"derived[{index}]").operands:
                if operand.stage in all_in_one:
                    raise ValueError(
                        f"derived[{index}] ({spec.key}) declares 'zone: per_zone' but its "
                        f"expression reads {operand.source!r}, and stage {operand.stage!r} "
                        f"declares 'zones: all_in_one' — it runs once over the whole frame and "
                        f"publishes nothing in any zone bucket, so the per-zone series would be "
                        f"empty in every zone. Use 'zone: global'."
                    )

    def _check_named_zone_sources(self) -> None:
        """A zone-scoped metric cannot source ``zone_occupancy.per_zone.<X>.*``.

        That source names **one fixed zone**. Every other bucket re-tests the polygons against
        detections that are already restricted to itself, so ``per_zone.Left.count`` reads its
        real value in ``Left`` and ``0`` in every other zone -- and ``results-agg`` then ships
        N-1 permanent zero rows beside the real one. It is the same
        metric-that-reads-zero-forever defect as the ``all_in_one`` case above, arriving by a
        different route.

        There is no reason to write it: ``zone_occupancy.occupancy`` under ``zone: per_zone``
        already answers "how many in *this* zone" correctly in every bucket, because the bucket
        has already restricted the detections. So this is rejected rather than accommodated --
        no shipped app uses the form, and a stage-level ``silent_buckets`` cannot express it
        (the silent set would depend on the metric's source string, not on the stage).
        """
        named = re.compile(r"^(?:[A-Za-z_][A-Za-z0-9_]*\.)?per_zone\.[^.]+\.")

        def offending(source: str) -> bool:
            return bool(named.match(source))

        for index, metric in enumerate(self.metrics):
            if metric.zone == "global" or not offending(metric.source):
                continue
            raise ValueError(
                f"metrics[{index}] ({metric.key}) declares 'zone: {metric.zone}' but sources "
                f"{metric.source!r}, which names ONE fixed zone — every other bucket publishes "
                f"0 for it, so results-agg ships a permanent zero row per other zone beside the "
                f"real one. Use 'source: zone_occupancy.occupancy' with 'zone: per_zone' (the "
                f"bucket already restricts the detections to that zone), or keep this source and "
                f"declare 'zone: global'."
            )
        for index, spec in enumerate(self.derived):
            if spec.zone == "global":
                continue
            for operand in resolve_derived(self, spec, where=f"derived[{index}]").operands:
                if operand.from_global or not offending(operand.source):
                    continue
                raise ValueError(
                    f"derived[{index}] ({spec.key}) declares 'zone: {spec.zone}' but its "
                    f"expression reads {operand.source!r}, which names ONE fixed zone — it "
                    f"resolves to 0 in every other bucket, so the derived value is wrong "
                    f"everywhere but there. Read 'zone_occupancy.occupancy' instead, or declare "
                    f"'zone: global'."
                )

    def _check_incidents(self) -> None:
        if self.incidents is None:
            return
        metric_keys = {metric.key for metric in self.metrics}
        derived_keys = {spec.key for spec in self.derived}
        stage_names = {stage.stage_name for stage in self.pipeline} | {
            stage.PRIMITIVE for stage in self.pipeline
        }

        def reject_derived(placeholder: str, what: str, where: str) -> None:
            """Refuse a ``derived[]`` key in a **severity threshold**, which cannot see one.

            A threshold is evaluated from ``runtime/session.py``'s ``_active_for``, which reads
            ``_metric_values`` -- :func:`~matrice_analytics.engine.runtime.window.metric_plan`,
            i.e. ``metrics[]`` only. A derived key there would never be evaluated, so the
            incident would never fire: dead config that *looks* live, which is the defect class
            this schema exists to remove (**PY-12**).

            ``human_text`` is **not** subject to this and deliberately no longer calls it.
            Interpolation resolves against ``_resolved_values`` (``_metric_values`` *plus*
            ``_derived_frame_values``), which evaluates every ``derived[]`` expression against
            the frame's own operand readings. That method exists precisely to close this gap --
            its docstring records that a derived metric used to be absent from an incident's
            ``human_text`` on every frame -- so rejecting one here outlived its reason and cost
            apps the only way to state a unit-scaled number in an alert title.
            """
            if placeholder in derived_keys:
                raise ValueError(
                    f"{where} {what} {placeholder!r}, which is a 'derived:' metric. A severity "
                    f"threshold is evaluated per frame against 'metrics:' only, so this would "
                    f"never fire. Threshold one of the expression's operands instead — declare "
                    f"it in 'metrics:' and point at that — or compute the condition in a "
                    f"'custom' stage, which can raise a PrimitiveEvent per frame. "
                    f"(A 'derived:' key IS resolvable in human_text; only thresholds are "
                    f"restricted.)"
                )

        for index, incident in enumerate(self.incidents.types):
            where = f"incidents.types[{index}] ({incident.key})"

            if isinstance(incident.severity_from, str):
                value = incident.severity_from
                if value in SEVERITY_LEVELS:
                    pass  # a fixed level — always this severity while the incident is open
                elif value in stage_names:
                    stage = self._stage_by_name(value)
                    if stage is not None and not isinstance(
                        stage, (IncidentQuantiseConfig, CustomConfig)
                    ):
                        raise ValueError(
                            f"{where}.severity_from names the {value!r} stage, which does not "
                            f"produce a severity level. Point it at an 'incident_quantise' stage, "
                            f"a fixed level ({', '.join(SEVERITY_LEVELS)}), or a metric threshold "
                            f"such as {{{next(iter(metric_keys), 'my_metric')}: {{'>': 0}}}}."
                        )
                else:
                    raise ValueError(
                        f"{where}.severity_from is {value!r}, which is neither a severity level "
                        f"({', '.join(SEVERITY_LEVELS)}) nor a stage in this pipeline "
                        f"({_joined(stage_names)}). To threshold a metric instead, write "
                        f"severity_from: {{{value}: {{'>': 0}}}}."
                        f"{_did_you_mean(value, stage_names | set(SEVERITY_LEVELS))}"
                    )
            else:
                for metric_key in incident.severity_from:
                    reject_derived(metric_key, "thresholds", f"{where}.severity_from")
                    if metric_key not in metric_keys:
                        raise ValueError(
                            f"{where}.severity_from thresholds {metric_key!r}, which is not a "
                            f"declared metric — the threshold would never be evaluated. Declared "
                            f"metrics: {_joined(metric_keys)}."
                            f"{_did_you_mean(metric_key, metric_keys)}"
                        )

            # `metrics[]` OR `derived[]`: interpolation reads `_resolved_values`, which is both.
            # A derived key is the only way to state a metric in the units an operator reads --
            # `human_text` renders a bare number and appends no unit, so a 0-1 fraction reaches
            # the night shift as "0.00" for a real event. See `reject_derived` above.
            interpolatable = metric_keys | derived_keys
            for placeholder in incident.interpolated_keys():
                if placeholder not in interpolatable:
                    raise ValueError(
                        f"{where}.human_text interpolates {{{placeholder}}}, which is not a "
                        f"declared metric, so operators would see the literal text "
                        f"'{{{placeholder}}}' in the alert title. Declared metrics: "
                        f"{_joined(interpolatable)}."
                        f"{_did_you_mean(placeholder, interpolatable)}"
                    )

    # -- accessors ---------------------------------------------------------

    def _stage_by_name(self, name: str) -> PrimitiveConfig | None:
        for stage in self.pipeline:
            if name in (stage.stage_name, stage.PRIMITIVE):
                return stage
        return None

    @property
    def stages(self) -> dict[str, PrimitiveConfig]:
        """Stage name → config, in pipeline order."""
        return {stage.stage_name: stage for stage in self.pipeline}

    @property
    def metric_keys(self) -> tuple[str, ...]:
        """``metrics[]`` keys only — the sourced ones.

        Deliberately **not** widened to include ``derived[]``: this property answers "which
        keys does a stage output back", which is what the generated-test suite checks it for
        (``testing/generate.py``), and a derived key has no single stage behind it. Use
        :attr:`published_keys` for "every key that reaches the wire".
        """
        return tuple(metric.key for metric in self.metrics)

    @property
    def derived_keys(self) -> tuple[str, ...]:
        return tuple(spec.key for spec in self.derived)

    @property
    def published_keys(self) -> tuple[str, ...]:
        """Every metric key this manifest puts on ``results-agg``, sourced and derived.

        The two lists share one namespace — the wire cannot tell them apart — so uniqueness is
        checked across both (:meth:`_check_derived`).
        """
        return self.metric_keys + self.derived_keys

    def resolved_sources(self) -> tuple[ResolvedSource, ...]:
        """Every metric source, already checked. Empty for an incident-only app."""
        return tuple(resolve_source(self, metric.source) for metric in self.metrics)

    def resolved_derived(self) -> tuple[ResolvedDerived, ...]:
        """Every ``derived[]`` entry, already checked, with its inferred scope."""
        return tuple(
            resolve_derived(self, spec, where=f"derived[{index}] ({spec.key})")
            for index, spec in enumerate(self.derived)
        )

    def unimplemented_primitives(self) -> tuple[str, ...]:
        """Declared primitives the runtime has not built yet (``08`` §2).

        Not an error: the manifest is allowed to describe an app before the engine can run it. The
        runtime refuses at session start; the loader only reports.
        """
        return tuple(sorted({stage.PRIMITIVE for stage in self.pipeline if not stage.IMPLEMENTED}))

    def geometry_requirements(self) -> tuple[GeometryRequirement, ...]:
        """Per-camera geometry this app needs, so the runtime can fail loudly instead of counting
        zero (see :class:`GeometryRequirement`)."""
        requirements: list[GeometryRequirement] = []
        for stage in self.pipeline:
            requirements.extend(stage.geometry_requirements())
        if self.zones is not None and self.zones.required:
            requirements.append(
                GeometryRequirement(
                    stage="zones",
                    kind="zones",
                    minimum=1,
                    reason="zones.required is true, so a camera with no geometry is a startup error.",
                )
            )
        return tuple(requirements)

    def custom_stages(self) -> tuple[CustomConfig, ...]:
        return tuple(stage for stage in self.pipeline if isinstance(stage, CustomConfig))


def resolve_source(
    manifest: AppManifest,
    source: str,
    *,
    where: str = "metrics[].source",
    allow_global_prefix: bool = False,
) -> ResolvedSource:
    """Resolve ``<stage>.<value>`` against a manifest's pipeline, or raise ``ValueError``.

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
    stages = {stage.stage_name: stage for stage in manifest.pipeline}
    from_global = False
    # `source` stays the text the manifest wrote: it is the key the evaluator looks the operand
    # up by (`_window_operand_values` fills `values[operand.source]`), so stripping it here
    # would build a map the expression cannot read. `path` is the part that names the stage.
    path = source
    if allow_global_prefix and source.startswith(f"{GLOBAL_ZONE}.") and GLOBAL_ZONE not in stages:
        from_global = True
        path = source[len(GLOBAL_ZONE) + 1 :]
    elif source.startswith(f"{GLOBAL_ZONE}.") and GLOBAL_ZONE not in stages:
        raise ValueError(
            f"{where}: source {source!r} starts with {GLOBAL_ZONE + '.'!r}, which addresses the "
            f"whole-frame bucket and is only meaningful in a derived[].expr, where one "
            f"expression is evaluated once per zone. A metrics[] entry states the bucket it "
            f"reads with 'zone: global' or 'zone: per_zone' instead."
        )
    # A stage renamed with `name:` is still addressable by its primitive name, but only while that
    # is unambiguous — two `custom` stages must each be addressed by their own name.
    by_primitive: dict[str, list[PrimitiveConfig]] = {}
    for stage in manifest.pipeline:
        by_primitive.setdefault(stage.PRIMITIVE, []).append(stage)
    for primitive, group in by_primitive.items():
        if len(group) == 1:
            stages.setdefault(primitive, group[0])

    stage_name, _, value = path.partition(".")
    config = stages.get(stage_name)
    if config is None:
        declared = {s.stage_name for s in manifest.pipeline}
        raise ValueError(
            f"{where}: source {source!r} names {stage_name!r}, which is not a stage in this "
            f"pipeline. Declared stages, in order: {', '.join(s.stage_name for s in manifest.pipeline)}."
            f"{_did_you_mean(stage_name, declared)} An unresolvable source is a load error rather "
            f"than a metric that reads zero forever."
        )

    if config.OPEN_OUTPUTS:
        # `custom` — the value keys live in the author's Python. The loader imports the class; the
        # manifest cannot know the names, so the source is recorded as unverified rather than
        # rejected.
        return ResolvedSource(
            source=source, stage=stage_name, value=value, unverified=True, from_global=from_global
        )

    if value in config.output_names() or any(p.match(value) for p in config.output_patterns()):
        aggregated = value in config.window_output_names() or any(
            p.match(value) for p in config.window_output_patterns()
        )
        return ResolvedSource(
            source=source,
            stage=stage_name,
            value=value,
            window_aggregated=aggregated,
            from_global=from_global,
        )

    raise ValueError(
        f"{where}: source {source!r} does not resolve — the {stage_name!r} stage produces no value "
        f"named {value!r}. It produces: {config.describe_outputs()}."
        f"{_did_you_mean(value, config.output_names())}"
    )


def _operand_availability(manifest: AppManifest, resolved: ResolvedSource) -> tuple[bool, bool]:
    """``(published_per_frame, published_at_window_scope)`` for one resolved operand.

    The two are independent — see :class:`PrimitiveConfig` — and a derived expression can only
    be evaluated in a scope where *every* operand has a value.

    A ``custom`` stage is frame-only by construction: it has no ``window()``, which is why the
    runtime collapses its per-frame values with ``agg_type`` at all.
    """
    config = manifest._stage_by_name(resolved.stage)  # noqa: SLF001 - same module, same rule
    if config is None:  # pragma: no cover - resolve_source already proved the stage exists
        return (False, False)
    if config.OPEN_OUTPUTS:
        return (True, False)
    # `output_patterns()` is the frame-scope pattern set. For `zone_occupancy` with
    # `zones: all` it is one pattern covering count / count_peak / avg, so a per-frame
    # operand naming a window-only per-zone reading (`count_peak`) is accepted here and then
    # finds no sample at runtime -- the window logs it and skips the metric, which is a
    # visible gap rather than a wrong number. Tightening that pattern is a change to
    # `ZoneOccupancyConfig`'s declared outputs and belongs with that stage, not here.
    frame = resolved.value in config.frame_output_names() or any(
        pattern.match(resolved.value) for pattern in config.output_patterns()
    )
    return (frame, resolved.window_aggregated)


def resolve_derived(
    manifest: AppManifest, spec: DerivedMetricSpec, *, where: str = "derived[]"
) -> ResolvedDerived:
    """Resolve one ``derived[]`` entry against the pipeline, or raise ``ValueError``.

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
    expression = spec.expression
    operands: list[ResolvedSource] = []
    frame_only: list[str] = []
    window_only: list[str] = []

    for operand in expression.operands:
        resolved = resolve_source(
            manifest,
            operand,
            where=f"{where}.expr operand {operand!r}",
            allow_global_prefix=True,
        )
        operands.append(resolved)
        frame, window = _operand_availability(manifest, resolved)
        if not frame:
            window_only.append(operand)
        if not window:
            frame_only.append(operand)

    if spec.scope == "window" and frame_only:
        raise ValueError(
            f"{where} declares scope: window, but {_joined(frame_only)} is published per frame "
            f"only — nothing publishes it at the aggregation boundary, so the expression has no "
            f"value there. Use scope: frame, and the expression is evaluated per frame with the "
            f"samples collapsed by agg_type; or omit 'scope' and the engine infers it."
        )
    if spec.scope == "frame" and window_only:
        raise ValueError(
            f"{where} declares scope: frame, but {_joined(window_only)} is a window-scope "
            f"reading — the producing stage computes it once at the boundary, so there is no "
            f"per-frame sample of it to average. Point at the per-frame name instead (e.g. "
            f"'detect.person.count' rather than 'detect.person.count_peak'), or use "
            f"scope: window."
        )

    scope: DerivedScopeLiteral
    if spec.scope is not None:
        scope = spec.scope
    elif not frame_only:
        # Every operand is already aggregated: evaluate once at the boundary. The result is
        # itself already aggregated, so the engine publishes it verbatim (PY-1, §6b coupling 4).
        scope = "window"
    elif not window_only:
        scope = "frame"
    else:
        raise ValueError(
            f"{where}.expr mixes scopes: {_joined(window_only)} exists only at window scope and "
            f"{_joined(frame_only)} exists only per frame, so there is no scope in which this "
            f"expression has a value. Pick operands from one scope — usually the per-frame "
            f"names, with scope: frame — rather than dividing a window total by a per-frame "
            f"sample, which is a number with no meaning."
        )

    return ResolvedDerived(spec=spec, expression=expression, scope=scope, operands=tuple(operands))


_cross_check_contract_vocabulary()
