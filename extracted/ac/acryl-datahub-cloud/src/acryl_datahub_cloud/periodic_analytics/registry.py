from typing import Dict, List, Literal, Optional

import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

from acryl_datahub_cloud.periodic_analytics.bundled_config import read_config_yaml

# Derivation rule names. Literal[...] requires literal string expressions (not
# variables) for static type-checking, so RULE_* below intentionally restates
# them as runtime constants for billing_sync/derivation.py to import rather
# than re-typing the strings — the two must be kept in sync by hand.
DerivationRule = Literal[
    "filter_ingestion_endpoint",
    "multiply_default_cost_units",
    "period_distinct",
    "sum_billable_entity_types",
]

RULE_FILTER_INGESTION_ENDPOINT: DerivationRule = "filter_ingestion_endpoint"
RULE_MULTIPLY_DEFAULT_COST_UNITS: DerivationRule = "multiply_default_cost_units"
RULE_PERIOD_DISTINCT: DerivationRule = "period_distinct"
RULE_SUM_BILLABLE_ENTITY_TYPES: DerivationRule = "sum_billable_entity_types"

RULE_REQUIRED_SOURCE_MERGE_KIND: Dict[str, str] = {
    RULE_FILTER_INGESTION_ENDPOINT: "additive",
    RULE_MULTIPLY_DEFAULT_COST_UNITS: "additive",
    RULE_PERIOD_DISTINCT: "distinct",
    RULE_SUM_BILLABLE_ENTITY_TYPES: "latest",
}

PublishCadence = Literal["hourly", "daily", "monthly"]
FinalizeGrain = Literal["hour", "day", "month"]
# Metronome billable-metric aggregation for this quantity:
#   sum    — signed ledger deltas under properties.count (SUM(count))
#   latest — absolute cumulative_mtd snapshots (LATEST(count)); gauges
#   max    — absolute cumulative_mtd snapshots (MAX(count)); high-water
# latest/max apply to distinct or additive gauges (e.g. MAU, asset counts).
MetronomeAggregation = Literal["sum", "latest", "max"]


class RuleConfig(BaseModel):
    """Optional parameters for a derivation rule (overridable via recipe)."""

    model_config = ConfigDict(extra="forbid")

    entity_types: Optional[List[str]] = Field(
        None,
        description="Allowlist for sum_billable_entity_types "
        "(active + soft_deleted per entity_type).",
    )


_ACTOR_CLASS_FILTER_RULES = frozenset(
    {
        RULE_FILTER_INGESTION_ENDPOINT,
        RULE_MULTIPLY_DEFAULT_COST_UNITS,
        RULE_PERIOD_DISTINCT,
    }
)


class MetricSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    merge_kind: Literal["additive", "distinct", "latest", "max"]
    value_unit: Literal["count", "input_bytes", "output_bytes", "bytes", "cost_units"]
    metronome_batch: bool
    # Required for GMS-emitted metrics (governs when the raw event is recorded).
    # Derived metrics never emit raw events, so the GMS canon omits this field
    # for every derived_metrics entry — optional here, enforced below.
    emit_when: Optional[
        Literal[
            "always",
            "activity_allowlist",
            "reader_activity_allowlist",
            "writer_activity_allowlist",
            "reported",
        ]
    ] = None
    # Optional allowlist of request_api labels (openapi/restli/graphql/...).
    # Empty/omitted = all request APIs. Prefer metronome_dimensions for
    # Metronome product breakout on a single flush metric.
    request_apis: List[str] = Field(default_factory=list)
    distinct_key: Optional[str] = None
    required_dimensions: List[str] = Field(default_factory=list)
    # When set with metronome_batch, billing-sync MTD/publish is keyed by these
    # access-channel columns (e.g. request_api) and stamped onto BillingEvent
    # stringProperties so Metronome billable metrics can filter.
    metronome_dimensions: List[str] = Field(default_factory=list)
    # Free-text documentation carried by GMS canon derived_metrics entries
    # (e.g. explaining the rule in prose). Not read by any billing-sync logic.
    notes: Optional[str] = None
    # A metric is DERIVED when both fields are set: GMS never emits it as a
    # metric_name in events, and billing-sync computes it from derived_from
    # sources via `rule` instead of reading raw bucket rows for its own name.
    derived_from: Optional[List[str]] = None
    rule: Optional[DerivationRule] = None
    # Rule-specific parameters (e.g. entity_types for sum_billable_entity_types).
    # Recipe metric_registry_override can replace this block at runtime.
    rule_config: Optional[RuleConfig] = None
    # actor_class allowlist for Metronome additive/distinct billing-sync paths.
    # Required when metronome_batch and merge_kind is additive/distinct, or when
    # rule filters source rows by actor_class. Override via metric_registry_override.
    billable_actor_classes: Optional[List[str]] = None
    # Billing-sync publish policy (ignored when metronome_batch=false).
    # Evaluated against watermarks/ledger/clock on each wake-up — not cron.
    publish_cadence: PublishCadence = "hourly"
    finalize_grain: FinalizeGrain = "hour"
    # Quantity model for Metronome: sum (signed delta), latest, or max (absolute).
    metronome_aggregation: MetronomeAggregation = "sum"

    @model_validator(mode="after")
    def _distinct_requires_key(self) -> "MetricSpec":
        if self.merge_kind == "distinct" and not self.distinct_key:
            raise ValueError(
                "merge_kind=distinct requires distinct_key — refusing to load a "
                "distinct metric with no identity column"
            )
        return self

    @model_validator(mode="after")
    def _derived_from_and_rule_together(self) -> "MetricSpec":
        if bool(self.derived_from) != bool(self.rule):
            raise ValueError(
                "derived_from and rule must be set together — a metric naming "
                "one without the other is a mis-registered derivation"
            )
        return self

    @model_validator(mode="after")
    def _emit_when_required_unless_derived(self) -> "MetricSpec":
        if not self.is_derived and self.emit_when is None:
            raise ValueError(
                "emit_when is required for non-derived metrics — GMS emits "
                "these as raw events and must declare when. Only a derived "
                "entry (rule set) may omit it"
            )
        return self

    @model_validator(mode="after")
    def _publish_cadence_finalize_grain_combo(self) -> "MetricSpec":
        if not self.metronome_batch:
            return self
        if self.finalize_grain in {"hour", "day"} and self.publish_cadence == "monthly":
            raise ValueError(
                f"finalize_grain={self.finalize_grain} is incompatible with "
                "publish_cadence=monthly — month-only cadence cannot finalize "
                "at a sub-month grain"
            )
        return self

    @model_validator(mode="after")
    def _sum_billable_requires_entity_types(self) -> "MetricSpec":
        if self.rule != RULE_SUM_BILLABLE_ENTITY_TYPES:
            return self
        entity_types = (
            self.rule_config.entity_types if self.rule_config is not None else None
        )
        if not entity_types:
            raise ValueError(
                "rule=sum_billable_entity_types requires "
                "rule_config.entity_types (non-empty allowlist)"
            )
        return self

    @model_validator(mode="after")
    def _billable_actor_classes_when_filtered(self) -> "MetricSpec":
        needs_allowlist = self.rule in _ACTOR_CLASS_FILTER_RULES or (
            self.metronome_batch
            and self.merge_kind in {"additive", "distinct"}
            and not self.is_derived
        )
        if not needs_allowlist:
            return self
        if not self.billable_actor_classes:
            raise ValueError(
                "billable_actor_classes must be a non-empty list for Metronome "
                "additive/distinct metrics and actor_class-filtered derivations"
            )
        return self

    @property
    def is_derived(self) -> bool:
        return self.rule is not None

    @property
    def billable_entity_types(self) -> List[str]:
        """Allowlist for sum_billable_entity_types; empty when not applicable."""
        if self.rule_config is None or not self.rule_config.entity_types:
            return []
        return list(self.rule_config.entity_types)

    def require_billable_actor_classes(self) -> List[str]:
        if not self.billable_actor_classes:
            raise ValueError(
                "billable_actor_classes is required for this metric's billing path"
            )
        return list(self.billable_actor_classes)

    @property
    def uses_absolute_snapshot(self) -> bool:
        """True when Metronome quantity is absolute MTD (latest or max)."""
        return self.metronome_batch and self.metronome_aggregation in {
            "latest",
            "max",
        }

    @property
    def uses_latest_snapshot(self) -> bool:
        return self.metronome_batch and self.metronome_aggregation == "latest"

    @property
    def uses_max_snapshot(self) -> bool:
        return self.metronome_batch and self.metronome_aggregation == "max"

    @property
    def is_month_final(self) -> bool:
        return self.finalize_grain == "month"

    @property
    def is_hour_final(self) -> bool:
        return self.finalize_grain == "hour"

    @property
    def is_day_final(self) -> bool:
        return self.finalize_grain == "day"

    @property
    def is_hour_or_day_final(self) -> bool:
        return self.finalize_grain in {"hour", "day"}


def _is_derived_entry(fields: Dict) -> bool:
    return bool(fields.get("derived_from")) or bool(fields.get("rule"))


def _validate_section_membership(
    family: str, name: str, fields: Dict, *, expect_derived: bool
) -> None:
    is_derived_entry = _is_derived_entry(fields)
    if expect_derived and not is_derived_entry:
        raise ValueError(
            f"{family}.{name} is listed under 'derived_metrics' but declares no "
            "derived_from/rule — every derived_metrics entry must be an actual "
            "derivation, not a raw metric misfiled under the wrong section"
        )
    if not expect_derived and is_derived_entry:
        raise ValueError(
            f"{family}.{name} is listed under 'metric_registry' but declares "
            "derived_from/rule — derived metrics must live under the sibling "
            "'derived_metrics' section, not metric_registry"
        )


def _merge_sections(raw: Dict) -> Dict:
    metric_registry = raw["metric_registry"]
    for family, metrics in metric_registry.items():
        for name, fields in metrics.items():
            _validate_section_membership(family, name, fields, expect_derived=False)
    merged = {family: dict(metrics) for family, metrics in metric_registry.items()}

    # GMS canon (post ACR-7613) carries derived metrics in a sibling top-level
    # `derived_metrics:` section rather than nested inside `metric_registry` —
    # they're not GMS counters, so they don't belong in the section
    # BillingUsageMetricContributor/UsageMetricRegistry read on the GMS side.
    derived_metrics = raw.get("derived_metrics")
    if derived_metrics:
        for family, metrics in derived_metrics.items():
            for name, fields in metrics.items():
                _validate_section_membership(family, name, fields, expect_derived=True)
        merged = _deep_merge(merged, derived_metrics)
    return merged


def _load_bundled(name: str) -> Dict:
    raw = yaml.safe_load(read_config_yaml(name))
    return _merge_sections(raw)


def _deep_merge(base: Dict, overlay: Dict) -> Dict:
    merged = {k: dict(v) for k, v in base.items()}
    for family, metrics in overlay.items():
        merged.setdefault(family, {})
        for metric, fields in metrics.items():
            merged[family].setdefault(metric, {})
            merged[family][metric] = {**merged[family][metric], **fields}
    return merged


def _validate_derived_from(families: Dict[str, Dict[str, MetricSpec]]) -> None:
    for family, metrics in families.items():
        for name, spec in metrics.items():
            if not spec.is_derived:
                continue
            assert spec.rule is not None  # narrows for mypy; enforced by is_derived
            required_kind = RULE_REQUIRED_SOURCE_MERGE_KIND[spec.rule]
            for source_name in spec.derived_from or []:
                source_spec = metrics.get(source_name)
                if source_spec is None:
                    raise ValueError(
                        f"{family}.{name} derived_from references unknown metric "
                        f"'{source_name}' — not found in family '{family}'"
                    )
                if source_spec.merge_kind != required_kind:
                    raise ValueError(
                        f"{family}.{name} rule={spec.rule} requires derived_from "
                        f"sources with merge_kind={required_kind}, but "
                        f"'{source_name}' has merge_kind={source_spec.merge_kind}"
                    )


class MetricRegistry:
    def __init__(self, families: Dict[str, Dict[str, MetricSpec]]):
        self._families = families

    @classmethod
    def load(cls, override: Optional[Dict] = None) -> "MetricRegistry":
        raw = _deep_merge(
            _load_bundled("usage_metric_registry.yaml"),
            _load_bundled("billing_metric_registry.yaml"),
        )
        if override:
            raw = _deep_merge(raw, override)
        families = {
            family: {
                name: MetricSpec.parse_obj(fields) for name, fields in metrics.items()
            }
            for family, metrics in raw.items()
        }
        _validate_derived_from(families)
        return cls(families)

    def metrics(self, family: str) -> Dict[str, MetricSpec]:
        return self._families.get(family, {})

    def spec(self, family: str, name: str) -> MetricSpec:
        return self._families[family][name]

    def additive_names(self, family: str) -> List[str]:
        # Derived metrics never appear in raw events (rollup has nothing to
        # read for them), so they're excluded here even if merge_kind==additive.
        return [
            n
            for n, s in self.metrics(family).items()
            if s.merge_kind == "additive" and not s.is_derived
        ]

    def distinct_names(self, family: str) -> List[str]:
        return [
            n
            for n, s in self.metrics(family).items()
            if s.merge_kind == "distinct" and not s.is_derived
        ]

    def latest_names(self, family: str) -> List[str]:
        """Gauge metrics: events→hour=latest; day/month compact with mean."""
        return [
            n
            for n, s in self.metrics(family).items()
            if s.merge_kind == "latest" and not s.is_derived
        ]

    def metronome_names(self, family: str) -> List[str]:
        # Includes derived metrics — TG-6 validation must still require them
        # when metronome_batch is set, even though billing_sync/derivation.py
        # (not the raw additive/distinct read path) supplies their value.
        return [n for n, s in self.metrics(family).items() if s.metronome_batch]

    def derived_names(self, family: str) -> List[str]:
        return [n for n, s in self.metrics(family).items() if s.is_derived]
