import os
from typing import Dict, List, Literal, Optional, Set

from pydantic import Field, model_validator

from acryl_datahub_cloud.periodic_analytics.constants import (
    DEFAULT_METRIC_FAMILY,
    SYSTEM_USAGE_METRIC_FAMILY,
    Layer,
    RunMode,
)
from acryl_datahub_cloud.periodic_analytics.object_storage_uri import (
    merge_prefix,
    parse_object_storage_uri,
)
from datahub.configuration.common import ConfigModel

_SCHEME_BY_PROVIDER = {"s3": "s3://", "gcs": "gs://"}
# Identity fields used for the "all blank → unconfigured no-op" check. uri is
# included so a recipe that only has uri set is not treated as unconfigured.
_OBJECT_STORAGE_UNSET_FIELDS = ("uri", "bucket", "customer_id", "instance_id")

_ENV_OBJECT_STORAGE_URI = "DATAHUB_OBJECT_STORAGE_URI"
_ENV_BILLING_ARCHIVE_PATH_PREFIX = "BILLING_ARCHIVE_PATH_PREFIX"
_ENV_BILLING_CUSTOMER_ID = "BILLING_CUSTOMER_ID"
_ENV_BILLING_INSTANCE_ID = "BILLING_INSTANCE_ID"
_DEFAULT_BILLING_ARCHIVE_PATH_PREFIX = "analytics/billing"
# Deliberately generous: a lease that expires too early lets two runs
# overlap and double-write buckets/ledgers/watermarks -- the exact failure
# the run lock exists to prevent -- whereas one that's too long only ever
# costs a single skipped run when a real overrun holds it past expiry (safe;
# see the "not configured" no-op warning above for the same skip-not-fail
# philosophy). Bump this per-tenant if a legitimate run regularly approaches
# it, rather than guessing at a tighter default.
_LOCK_LEASE_MINUTES_DESCRIPTION = (
    "Minutes before this source's run-lock lease is considered expired and "
    "may be stolen by another run. Generous by design -- see config.py."
)
# Executor clocks are assumed NTP-synced but not perfectly -- without this
# buffer, a stealer whose clock runs ahead of the lease holder's could steal
# a lease the holder still considers live. Keep this well under
# lock_lease_minutes; it only needs to cover realistic clock drift, not
# legitimate run overrun.
_LOCK_STEAL_SKEW_MINUTES_DESCRIPTION = (
    "Minutes beyond lock_lease_minutes' own expiry before a lease is "
    "actually stolen, to absorb clock drift between executors. See "
    "config.py."
)

GrainName = Literal["hourly", "daily", "monthly"]
# Input may use provider "file"; the before-validator normalizes it to "local".
ObjectStorageProvider = Literal["s3", "gcs", "local"]


def _default_grains() -> List[GrainName]:
    return ["hourly", "daily", "monthly"]


def _default_rollup_metric_families() -> List[str]:
    return [DEFAULT_METRIC_FAMILY, SYSTEM_USAGE_METRIC_FAMILY]


def _blank(value: object) -> bool:
    return not str(value or "").strip()


def _env_or_empty(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def _apply_object_storage_env_fallback(raw: Dict) -> Dict:
    data = dict(raw)
    if _blank(data.get("uri")):
        env_uri = _env_or_empty(_ENV_OBJECT_STORAGE_URI)
        if env_uri:
            data["uri"] = env_uri
    if _blank(data.get("prefix")):
        env_prefix = _env_or_empty(_ENV_BILLING_ARCHIVE_PATH_PREFIX)
        data["prefix"] = env_prefix or _DEFAULT_BILLING_ARCHIVE_PATH_PREFIX
    if _blank(data.get("customer_id")):
        env_customer = _env_or_empty(_ENV_BILLING_CUSTOMER_ID)
        if env_customer:
            data["customer_id"] = env_customer
    if _blank(data.get("instance_id")):
        env_instance = _env_or_empty(_ENV_BILLING_INSTANCE_ID)
        if env_instance:
            data["instance_id"] = env_instance
    return data


def _object_storage_is_unset(raw: object) -> bool:
    # Bootstrap recipes render object_storage identity fields from
    # DATAHUB_PERIODIC_ANALYTICS_*_BOOTSTRAP_VALUES with no Mustache fallback.
    # After env fallback, the all-blank shape means "not configured yet" and
    # should be a no-op rather than a hard failure.
    if not isinstance(raw, dict):
        return False
    return all(_blank(raw.get(field)) for field in _OBJECT_STORAGE_UNSET_FIELDS)


def _skip_object_storage_when_unconfigured(data: object) -> object:
    if not isinstance(data, dict):
        return data
    storage = data.get("object_storage")
    if storage is None:
        return data
    if not isinstance(storage, dict):
        return data
    storage = _apply_object_storage_env_fallback(storage)
    if _object_storage_is_unset(storage):
        return {**data, "object_storage": None}
    return {**data, "object_storage": storage}


def _resolve_object_storage_dict(data: object) -> object:
    if not isinstance(data, dict):
        return data
    resolved = _apply_object_storage_env_fallback(data)

    provider = str(resolved.get("provider") or "").strip().lower()
    if provider == "file":
        resolved["provider"] = "local"

    uri = str(resolved.get("uri") or "").strip()
    if uri:
        parsed = parse_object_storage_uri(uri)
        resolved["provider"] = parsed.provider
        if parsed.provider == "local":
            resolved["bucket"] = parsed.local_root or ""
        else:
            resolved["bucket"] = parsed.bucket or ""
            resolved["prefix"] = merge_prefix(parsed.key_prefix, resolved.get("prefix"))
        # Keep uri on the model for round-trip / debugging; storage uses
        # provider+bucket+prefix after resolution.
    elif _blank(resolved.get("prefix")):
        resolved["prefix"] = _DEFAULT_BILLING_ARCHIVE_PATH_PREFIX

    return resolved


class ObjectStorageConfig(ConfigModel):
    uri: Optional[str] = Field(
        None,
        description="Object-storage root URI (DATAHUB_OBJECT_STORAGE_URI equivalent). "
        "Supports s3://bucket[/prefix], gs://bucket[/prefix], or file:///absolute/path. "
        "When set, provider and bucket are derived from the URI.",
    )
    provider: ObjectStorageProvider = Field(
        description="Object store backend. 'local' is for local debug runs; "
        "input may also use 'file' which is normalized to 'local'."
    )
    bucket: str = Field(
        description="Bucket name (or base directory for provider=local)."
    )
    prefix: str = Field(
        _DEFAULT_BILLING_ARCHIVE_PATH_PREFIX,
        description="Root prefix inside the bucket (matches BILLING_ARCHIVE_PATH_PREFIX).",
    )
    customer_id: str = Field(
        description="Tenant customer id. Required — jobs refuse to start without it (billing RFC NFR3)."
    )
    instance_id: str = Field(
        description="Tenant instance id. Required — jobs refuse to start without it (billing RFC NFR3)."
    )

    @model_validator(mode="before")
    @classmethod
    def _resolve_uri_and_env(cls, data: object) -> object:
        return _resolve_object_storage_dict(data)

    @model_validator(mode="after")
    def _validate(self) -> "ObjectStorageConfig":
        if not self.customer_id or not self.customer_id.strip():
            raise ValueError("customer_id is required and must be non-empty (NFR3)")
        if not self.instance_id or not self.instance_id.strip():
            raise ValueError("instance_id is required and must be non-empty (NFR3)")
        for provider, scheme in _SCHEME_BY_PROVIDER.items():
            if self.bucket.startswith(scheme) and self.provider != provider:
                raise ValueError(
                    f"bucket '{self.bucket}' looks like {provider} but provider is "
                    f"'{self.provider}' — refusing ambiguous storage target"
                )
        return self


class InputLagConfig(ConfigModel):
    hourly_minutes: int = Field(
        15, description="Minutes after hour end before the hour is considered complete."
    )


class RestateConfig(ConfigModel):
    start_partition: str = Field(
        description="Inclusive UTC start, YYYY-MM-DD or YYYY-MM-DDTHH."
    )
    end_partition: str = Field(description="Inclusive UTC end, same format as start.")
    targets: List[Layer] = Field(description="Output layers to recompute.")


class RollupSourceConfig(ConfigModel):
    object_storage: Optional[ObjectStorageConfig] = Field(
        None,
        description="Required to actually roll up data. Left as None only when "
        "the bootstrap recipe rendered uri/bucket/customer_id/instance_id all "
        "blank and env fallback could not fill them — the source then configures "
        "cleanly and no-ops instead of failing. A partially-filled block still "
        "fails ObjectStorageConfig's own validation (NFR3).",
    )
    metric_families: List[str] = Field(
        default_factory=_default_rollup_metric_families,
        description="Metric families to roll up in this recipe. Default is both "
        "api_usage and system_usage. Narrow to e.g. [api_usage] or "
        "[system_usage] to run a single family.",
    )
    run_mode: RunMode = RunMode.SCHEDULED
    lock_lease_minutes: int = Field(60, description=_LOCK_LEASE_MINUTES_DESCRIPTION)
    lock_steal_skew_minutes: int = Field(
        5, description=_LOCK_STEAL_SKEW_MINUTES_DESCRIPTION
    )
    auto_catch_up: bool = True
    max_partitions_per_run: int = Field(24, description="NFR2 bound per invocation.")
    input_lag: InputLagConfig = InputLagConfig()
    zero_init_archive_grace_hours: int = Field(
        6,
        description="Leading empty-hour zero-initialization only seals a day "
        "once now >= day end + max(input_lag, this grace). Emptiness is judged "
        "by the absence of archived event parquet, so a recent day whose "
        "events may still be in flight from the upstream archiver is not "
        "batch-watermarked as zero — its hours wait for ordinary capped "
        "rollup instead.",
    )
    restate: Optional[RestateConfig] = Field(
        None, description="Required when run_mode is restate/pipeline_restate."
    )
    metric_registry_override: Optional[Dict] = Field(
        None, description="Deep-merged over bundled registries."
    )
    grains: List[GrainName] = Field(
        default_factory=_default_grains,
        description="Which rollup tiers this recipe executes. Split tiers across "
        "recipes/schedules by narrowing this list.",
    )

    @model_validator(mode="before")
    @classmethod
    def _skip_unconfigured_object_storage(cls, data: object) -> object:
        return _skip_object_storage_when_unconfigured(data)

    @model_validator(mode="after")
    def _restate_required(self) -> "RollupSourceConfig":
        if (
            self.run_mode in (RunMode.RESTATE, RunMode.PIPELINE_RESTATE)
            and not self.restate
        ):
            raise ValueError(f"run_mode={self.run_mode.value} requires a restate block")
        return self

    @model_validator(mode="after")
    def _grains_non_empty(self) -> "RollupSourceConfig":
        if not self.grains:
            raise ValueError("grains must not be empty — at least one tier is required")
        return self

    @model_validator(mode="after")
    def _metric_families_non_empty(self) -> "RollupSourceConfig":
        if not self.metric_families:
            raise ValueError(
                "metric_families must be non-empty — set e.g. [api_usage], "
                "[system_usage], or both (the default)"
            )
        seen: Set[str] = set()
        deduped: List[str] = []
        for name in self.metric_families:
            key = str(name or "").strip()
            if not key:
                raise ValueError("metric_families entries must be non-empty strings")
            if key not in seen:
                seen.add(key)
                deduped.append(key)
        self.metric_families = deduped
        return self


class BillingSyncSourceConfig(ConfigModel):
    object_storage: Optional[ObjectStorageConfig] = Field(
        None,
        description="Required to actually sync billing. Left as None only when "
        "the bootstrap recipe rendered uri/bucket/customer_id/instance_id all "
        "blank and env fallback could not fill them — the source then configures "
        "cleanly and no-ops instead of failing. A partially-filled block still "
        "fails ObjectStorageConfig's own validation (NFR3).",
    )
    metric_family: str = DEFAULT_METRIC_FAMILY
    lock_lease_minutes: int = Field(60, description=_LOCK_LEASE_MINUTES_DESCRIPTION)
    lock_steal_skew_minutes: int = Field(
        5, description=_LOCK_STEAL_SKEW_MINUTES_DESCRIPTION
    )
    billing_excluded_identities: List[str] = Field(
        default_factory=list,
        description="DP-25 identities excluded from Metronome MTD.",
    )
    stabilization_seconds_after_close: int = Field(
        3600,
        ge=0,
        description="Seconds after UTC month-end (00:00 on the 1st) before the "
        "period is marked finalized and locked. Captures late-arriving data; "
        "default 3600 (1 hour). Must not exceed metronome_invoice_grace_seconds "
        "— after Metronome finalizes an invoice, further usage events no longer "
        "adjust that invoice.",
    )
    metronome_invoice_grace_seconds: int = Field(
        86400,
        ge=0,
        description="Configured Metronome invoice grace period in seconds "
        "(default 86400 = 24h, matching Metronome's default). Ops must set "
        "this to the contract grace; billing-sync refuses to start when "
        "stabilization_seconds_after_close exceeds it.",
    )
    publish_enabled: bool = Field(
        False, description="When false, log the publish payload instead of calling GMS."
    )
    gms_publish_url: Optional[str] = Field(
        None,
        description="GMS billing publish endpoint. Optional when publish_enabled: "
        "defaults to {graph.server}/openapi/v1/billing/usage from the pipeline "
        "graph (default datahub-rest sink / executor DATAHUB_GMS_*).",
    )
    gms_entity_counts_url: Optional[str] = Field(
        None,
        description="OpenAPI entity counts URL used when the sealed system_usage "
        "hourly_buckets partition has no LATEST samples. Defaults to deriving "
        "/openapi/v1/entities/counts from gms_publish_url (or the same "
        "graph.server fallback used for publish) when unset.",
    )
    publish_product: Optional[str] = Field(
        None,
        description="Product name to stamp on published usage requests (naming convention pending confirmation).",
    )
    allow_mtd_correction: bool = Field(
        False,
        description="Allow the publish ledger to send a negative delta (signed "
        "adjustment) when computed MTD drops below the last-ingested MTD for a "
        "metric. Off by default — a decrease is refused with an error naming "
        "the metric. When enabled, corrections bump the metric's ledger "
        "revision rather than silently rewriting history.",
    )
    metric_registry_override: Optional[Dict] = Field(
        None,
        description="Deep-merged over bundled registries.",
    )
    billable_entity_types: Optional[List[str]] = Field(
        None,
        description="Optional recipe override for data_assets_stored allowlist. "
        "When unset, uses registry "
        "system_usage.data_assets_stored.rule_config.entity_types. "
        "Bootstrap MCP omits this field unless BOOTSTRAP_VALUES includes a "
        "non-empty JSON array billable_entity_types.",
    )
    usage_operations_path: Optional[str] = Field(
        None,
        description="Path to a usage_operations.yaml taxonomy (ingestion_endpoint, "
        "default_cost_units per usage_operation), used by derived-metric rules in "
        "billing_sync/derivation.py. Defaults to the bundled copy at "
        "registries/usage_operations.yaml.",
    )
    input_lag: InputLagConfig = Field(
        default_factory=InputLagConfig,
        description="Minutes after hour end before an hour is eligible for "
        "billing-sync as_of and hour/day finalization (month finalization uses "
        "stabilization_seconds_after_close).",
    )

    @model_validator(mode="before")
    @classmethod
    def _skip_unconfigured_object_storage(cls, data: object) -> object:
        return _skip_object_storage_when_unconfigured(data)

    @model_validator(mode="after")
    def _billable_entity_types_override_non_empty(self) -> "BillingSyncSourceConfig":
        if self.billable_entity_types is not None and not self.billable_entity_types:
            raise ValueError(
                "billable_entity_types override must be non-empty when set "
                "(omit the field to use the registry allowlist)"
            )
        return self

    @model_validator(mode="after")
    def _stabilization_within_metronome_grace(self) -> "BillingSyncSourceConfig":
        if (
            self.stabilization_seconds_after_close
            > self.metronome_invoice_grace_seconds
        ):
            raise ValueError(
                "stabilization_seconds_after_close "
                f"({self.stabilization_seconds_after_close}) must be ≤ "
                "metronome_invoice_grace_seconds "
                f"({self.metronome_invoice_grace_seconds}) — month-final "
                "emits after Metronome invoice finalization would not adjust "
                "that invoice"
            )
        return self
