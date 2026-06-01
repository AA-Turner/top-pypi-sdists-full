"""Centralized assertion evaluation source type validation.

Mirrors the canonical Java validator:
  metadata-io/.../validation/AssertionEvaluationSourceValidator.java

SYNC NOTICE: This logic is duplicated in the Java backend and the frontend (TypeScript).
If you change the rules here, you MUST also update:
  - Java: metadata-io/.../validation/AssertionEvaluationSourceValidator.java
  - Frontend: datahub-web-react/.../assertion/builder/utils.tsx (freshness)
  - Frontend: datahub-web-react/.../assertion/builder/steps/volume/utils.tsx
  - Frontend: datahub-web-react/.../assertion/builder/steps/field/utils.ts
See: docs/assertion-source-validation-manifest.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, Union

from acryl_datahub_cloud.sdk.assertion_input.assertion_input import (
    _AllRowsQuery,
    _AllRowsQueryDataHubDatasetProfile,
    _AuditLog,
    _ChangedRowsQuery,
    _DataHubOperation,
    _DatasetProfile,
    _DetectionMechanismTypes,
    _HighWatermarkColumn,
    _InformationSchema,
    _LastModifiedColumn,
    _PlatformApi,
    _Query,
    _SchemaMetadata,
    _TableStatistics,
)
from acryl_datahub_cloud.sdk.errors import SDKUsageError
from datahub.metadata import schema_classes as models
from datahub.metadata.urns import DataPlatformUrn
from datahub.sdk import Dataset

if TYPE_CHECKING:
    from acryl_datahub_cloud.sdk.assertion_input.assertion_input import (
        _AssertionInput,
    )
    from acryl_datahub_cloud.sdk.assertion_input.freshness_assertion_input import (
        FreshnessAssertionScheduleCheckType,
    )

# ── Supported platforms ──
# Platforms whose executor supports active source types (query, audit log,
# information schema, etc.). All other platforms are limited to passive sources.

SUPPORTED_ASSERTION_PLATFORMS: frozenset[str] = frozenset(
    {"snowflake", "bigquery", "redshift", "databricks"}
)

# ── Detection mechanism categories ──

ACTIVE_DETECTION_MECHANISMS: tuple[type[_DetectionMechanismTypes], ...] = (
    _InformationSchema,
    _TableStatistics,
    _AuditLog,
    _LastModifiedColumn,
    _HighWatermarkColumn,
    _Query,
    _AllRowsQuery,
    _ChangedRowsQuery,
    _PlatformApi,
)

PASSIVE_DETECTION_MECHANISMS: tuple[type[_DetectionMechanismTypes], ...] = (
    _DataHubOperation,
    _DatasetProfile,
    _AllRowsQueryDataHubDatasetProfile,
    _SchemaMetadata,
)

# ── Per-platform freshness detection mechanism configs ──

PLATFORM_FRESHNESS_MECHANISMS: dict[str, tuple[type[_DetectionMechanismTypes], ...]] = {
    "snowflake": (
        _AuditLog,
        _InformationSchema,
        _LastModifiedColumn,
        _HighWatermarkColumn,
        _DataHubOperation,
    ),
    "bigquery": (
        _AuditLog,
        _InformationSchema,
        _PlatformApi,
        _LastModifiedColumn,
        _HighWatermarkColumn,
        _DataHubOperation,
    ),
    "redshift": (
        _AuditLog,
        _LastModifiedColumn,
        _HighWatermarkColumn,
        _DataHubOperation,
    ),
    "databricks": (
        _AuditLog,
        _InformationSchema,
        _LastModifiedColumn,
        _HighWatermarkColumn,
        _DataHubOperation,
    ),
}

# ── Per-platform volume detection mechanism configs ──

PLATFORM_VOLUME_MECHANISMS: dict[str, tuple[type[_DetectionMechanismTypes], ...]] = {
    "snowflake": (_InformationSchema, _Query, _DatasetProfile),
    "bigquery": (_InformationSchema, _PlatformApi, _Query, _DatasetProfile),
    "redshift": (_InformationSchema, _Query, _DatasetProfile),
    "databricks": (_TableStatistics, _Query, _DatasetProfile),
}

# ── Tables-only mechanisms (blocked for views) ──

FRESHNESS_TABLES_ONLY_MECHANISMS: tuple[type[_DetectionMechanismTypes], ...] = (
    _AuditLog,
    _InformationSchema,
    _PlatformApi,
)

VOLUME_TABLES_ONLY_MECHANISMS: tuple[type[_DetectionMechanismTypes], ...] = (
    _InformationSchema,
    _PlatformApi,
    _TableStatistics,
)

# ── Field metric types that require a direct query (no profile support) ──

FIELD_METRICS_REQUIRING_CONNECTION: frozenset[str] = frozenset(
    {
        models.FieldMetricTypeClass.EMPTY_COUNT,
        models.FieldMetricTypeClass.EMPTY_PERCENTAGE,
        models.FieldMetricTypeClass.NEGATIVE_COUNT,
        models.FieldMetricTypeClass.NEGATIVE_PERCENTAGE,
        models.FieldMetricTypeClass.ZERO_COUNT,
        models.FieldMetricTypeClass.ZERO_PERCENTAGE,
        models.FieldMetricTypeClass.MAX_LENGTH,
        models.FieldMetricTypeClass.MIN_LENGTH,
    }
)

# ── Field metric types supported by TABLE_STATISTICS (ANALYZE TABLE) ──

FIELD_METRICS_SUPPORTED_BY_TABLE_STATISTICS: frozenset[str] = frozenset(
    {
        models.FieldMetricTypeClass.NULL_COUNT,
        models.FieldMetricTypeClass.NULL_PERCENTAGE,
        models.FieldMetricTypeClass.UNIQUE_COUNT,
        models.FieldMetricTypeClass.UNIQUE_PERCENTAGE,
        models.FieldMetricTypeClass.MIN,
        models.FieldMetricTypeClass.MAX,
    }
)

# ── Platforms that support TABLE_STATISTICS for field metrics ──

TABLE_STATISTICS_FIELD_PLATFORMS: frozenset[str] = frozenset({"databricks"})

# ── View detection ──

_SUBTYPE_VIEW = "view"


def _is_view(entity_subtypes: set[str]) -> bool:
    return any(s.lower() == _SUBTYPE_VIEW for s in entity_subtypes)


# ── Context dataclasses ──


@dataclass(frozen=True)
class FreshnessValidationContext:
    platform: str
    detection_mechanism: _DetectionMechanismTypes
    schedule_type: Optional[Union[str, FreshnessAssertionScheduleCheckType]]
    entity_subtypes: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class VolumeValidationContext:
    platform: str
    detection_mechanism: _DetectionMechanismTypes
    bucketing_enabled: bool
    entity_subtypes: set[str] = field(default_factory=set)


@dataclass(frozen=True)
class FieldValuesValidationContext:
    platform: str
    detection_mechanism: _DetectionMechanismTypes


@dataclass(frozen=True)
class FieldMetricValidationContext:
    platform: str
    detection_mechanism: _DetectionMechanismTypes
    bucketing_enabled: bool
    metric_type: Union[str, models.FieldMetricTypeClass]


# ── Entity subtype resolution ──


def resolve_entity_subtypes(assertion_input: _AssertionInput) -> set[str]:
    """Fetch the entity's subtypes via the cached dataset.

    Reuses the same ``cached_dataset`` that ``_get_schema_field_spec`` populates,
    so for column-based detection mechanisms this is zero-cost.

    Returns an empty set if the dataset cannot be loaded or has no subtypes,
    which means view-gating is skipped (safe default: tables pass all checks).
    """
    if assertion_input.cached_dataset is None:
        assertion_input.cached_dataset = assertion_input.entity_client.get(
            assertion_input.dataset_urn
        )
    dataset = assertion_input.cached_dataset
    if not isinstance(dataset, Dataset):
        return set()
    subtypes_aspect = dataset._get_aspect(models.SubTypesClass)
    if isinstance(subtypes_aspect, models.SubTypesClass) and subtypes_aspect.typeNames:
        return set(subtypes_aspect.typeNames)
    return set()


# ── Platform normalization ──


def _normalize_platform(platform: str) -> str:
    """Extract the short platform name from a full DataPlatformUrn or short name."""
    if platform.startswith("urn:li:dataPlatform:"):
        return DataPlatformUrn.from_string(platform).platform_name
    return platform


# ── Validation functions ──
# Each returns a list of error strings (empty == valid).


def validate_platform_support(
    platform: str,
    detection_mechanism: _DetectionMechanismTypes,
) -> list[str]:
    """Generic check: active detection mechanisms require a supported platform.

    Platforms not in SUPPORTED_ASSERTION_PLATFORMS are limited to passive sources
    (DataHubOperation, DatasetProfile, etc.).
    """
    normalized = _normalize_platform(platform)
    if (
        isinstance(detection_mechanism, ACTIVE_DETECTION_MECHANISMS)
        and normalized not in SUPPORTED_ASSERTION_PLATFORMS
    ):
        return [
            f"Detection mechanism '{type(detection_mechanism).__name__}' requires "
            f"a supported platform ({', '.join(sorted(SUPPORTED_ASSERTION_PLATFORMS))}). "
            f"Platform '{normalized}' is not supported for active assertion evaluation. "
            f"Use a passive detection mechanism instead (e.g., DataHubOperation, DatasetProfile)."
        ]
    return []


def validate_freshness_source(ctx: FreshnessValidationContext) -> list[str]:
    """Validate a freshness assertion's detection mechanism against its context."""
    errors: list[str] = []
    mechanism = ctx.detection_mechanism
    platform = _normalize_platform(ctx.platform)

    # 1. Platform support
    errors.extend(validate_platform_support(platform, mechanism))
    if errors:
        return errors

    # 2. Per-platform mechanism restrictions
    if platform in PLATFORM_FRESHNESS_MECHANISMS:
        allowed = PLATFORM_FRESHNESS_MECHANISMS[platform]
        if not isinstance(mechanism, allowed + (type(None),)):
            errors.append(
                f"Detection mechanism '{type(mechanism).__name__}' is not supported "
                f"for freshness assertions on platform '{platform}'. "
                f"Allowed: {[t.__name__ for t in allowed]}"
            )
            return errors

    # 3. View gating: AUDIT_LOG and INFORMATION_SCHEMA are tables-only
    if _is_view(ctx.entity_subtypes) and isinstance(
        mechanism, FRESHNESS_TABLES_ONLY_MECHANISMS
    ):
        errors.append(
            f"Detection mechanism '{type(mechanism).__name__}' is not supported "
            f"for views (freshness). Tables-only sources (AuditLog, InformationSchema) "
            f"cannot be used on view entities. "
            f"Use FieldValue or DataHubOperation instead."
        )
        return errors

    # 4. High Watermark + FIXED_INTERVAL incompatibility
    if isinstance(mechanism, _HighWatermarkColumn) and _is_fixed_interval(
        ctx.schedule_type
    ):
        errors.append(
            "High watermark column detection is not compatible with FIXED_INTERVAL "
            "schedule type. High watermark only supports CRON and SINCE_THE_LAST_CHECK."
        )

    return errors


def validate_volume_source(ctx: VolumeValidationContext) -> list[str]:
    """Validate a volume assertion's detection mechanism against its context."""
    errors: list[str] = []
    mechanism = ctx.detection_mechanism
    platform = _normalize_platform(ctx.platform)

    # 1. Bucketing requires Query
    if ctx.bucketing_enabled and not isinstance(mechanism, _Query):
        errors.append(
            f"Volume assertions with time bucketing require the Query detection mechanism. "
            f"Got '{type(mechanism).__name__}'. "
            f"Either use DetectionMechanism.QUERY or disable time bucketing."
        )
        return errors

    # 2. Platform support
    errors.extend(validate_platform_support(platform, mechanism))
    if errors:
        return errors

    # 3. Per-platform mechanism restrictions
    if platform in PLATFORM_VOLUME_MECHANISMS:
        allowed = PLATFORM_VOLUME_MECHANISMS[platform]
        if not isinstance(mechanism, allowed + (type(None),)):
            errors.append(
                f"Detection mechanism '{type(mechanism).__name__}' is not supported "
                f"for volume assertions on platform '{platform}'. "
                f"Allowed: {[t.__name__ for t in allowed]}"
            )
            return errors

    # 4. View gating: INFORMATION_SCHEMA is tables-only
    if _is_view(ctx.entity_subtypes) and isinstance(
        mechanism, VOLUME_TABLES_ONLY_MECHANISMS
    ):
        errors.append(
            f"Detection mechanism '{type(mechanism).__name__}' is not supported "
            f"for views (volume). InformationSchema cannot be used on view entities. "
            f"Use Query or DatasetProfile instead."
        )

    return errors


def validate_field_values_source(ctx: FieldValuesValidationContext) -> list[str]:
    """Validate a column value (FIELD_VALUES) assertion's detection mechanism.

    Column value assertions always require a query-based source (AllRowsQuery or
    ChangedRowsQuery) on a supported platform. Profile-based sources are not valid.
    """
    errors: list[str] = []
    mechanism = ctx.detection_mechanism
    platform = _normalize_platform(ctx.platform)

    # 1. Must be a query-based mechanism
    if not isinstance(mechanism, (_AllRowsQuery, _ChangedRowsQuery)):
        errors.append(
            f"Column value assertions require AllRowsQuery or ChangedRowsQuery "
            f"detection mechanism. Got '{type(mechanism).__name__}'."
        )
        return errors

    # 2. Platform support (query sources are active)
    errors.extend(validate_platform_support(platform, mechanism))
    return errors


def validate_field_metric_source(ctx: FieldMetricValidationContext) -> list[str]:
    """Validate a field/column metric assertion's detection mechanism."""
    errors: list[str] = []
    mechanism = ctx.detection_mechanism
    platform = _normalize_platform(ctx.platform)

    # 1. Bucketing requires AllRowsQuery
    if ctx.bucketing_enabled and not isinstance(mechanism, _AllRowsQuery):
        errors.append(
            f"Field metric assertions with time bucketing require the AllRowsQuery "
            f"detection mechanism. Got '{type(mechanism).__name__}'. "
            f"Either use DetectionMechanism.ALL_ROWS_QUERY or disable time bucketing."
        )
        return errors

    # 2. Platform support
    errors.extend(validate_platform_support(platform, mechanism))
    if errors:
        return errors

    # 3. TABLE_STATISTICS: only supported on specific platforms and for specific metrics
    if isinstance(mechanism, _TableStatistics):
        if platform not in TABLE_STATISTICS_FIELD_PLATFORMS:
            errors.append(
                f"Table statistics detection mechanism is not supported for field "
                f"metric assertions on platform '{platform}'. "
                f"Supported platforms: {sorted(TABLE_STATISTICS_FIELD_PLATFORMS)}"
            )
            return errors
        metric_str = (
            ctx.metric_type.value
            if hasattr(ctx.metric_type, "value")
            else str(ctx.metric_type)
        )
        if metric_str not in FIELD_METRICS_SUPPORTED_BY_TABLE_STATISTICS:
            errors.append(
                f"Metric type '{ctx.metric_type}' is not supported by table statistics. "
                f"Use AllRowsQuery or ChangedRowsQuery detection mechanism instead. "
                f"Supported metrics: {sorted(FIELD_METRICS_SUPPORTED_BY_TABLE_STATISTICS)}"
            )
        return errors

    # 4. C3: requiresConnection metric + DatasetProfile → dead-end
    if ctx.metric_type in FIELD_METRICS_REQUIRING_CONNECTION and isinstance(
        mechanism, (_DatasetProfile, _AllRowsQueryDataHubDatasetProfile)
    ):
        errors.append(
            f"Metric type '{ctx.metric_type}' requires a direct query and cannot use "
            f"DataHub Dataset Profile as its source. Use AllRowsQuery or "
            f"ChangedRowsQuery detection mechanism instead."
        )

    return errors


# ── Helpers ──


def _is_fixed_interval(
    schedule_type: Optional[Union[str, FreshnessAssertionScheduleCheckType]],
) -> bool:
    if schedule_type is None:
        return False
    schedule_str = (
        schedule_type.value if hasattr(schedule_type, "value") else str(schedule_type)
    )
    return schedule_str.upper() == "FIXED_INTERVAL"


def _raise_if_errors(errors: list[str]) -> None:
    """Convenience: raise SDKUsageError if there are validation errors."""
    if errors:
        raise SDKUsageError("; ".join(errors))
