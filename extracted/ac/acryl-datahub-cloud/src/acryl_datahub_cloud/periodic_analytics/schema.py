from typing import Dict, List, Sequence, Tuple

import polars as pl

BILLABLE_ACTOR_CLASS = "regular"


def actor_class_in_expr(allowed: Sequence[str], column: str = "actor_class") -> pl.Expr:
    """Filter expression for ``actor_class`` membership (billing allowlists)."""
    return pl.col(column).is_in(list(allowed))


# Access-channel keys promoted from events/ dimensions JSON to flat columns on
# *additive* api_usage buckets (MTD/derivation group on these). Serialization
# order matches UsageDimensions.STABLE_KEY_ORDER. usage_operation and
# actor_class are omitted from the JSON when null on the writer side — readers
# must fill_null("") rather than assume presence.
#
# system_usage gauges do NOT use these flat columns; their family-specific keys
# stay in the opaque dimensions blob (see DIMENSION_JSON_ONLY_KEYS / latest
# rollup).
DIMENSION_KEYS: Tuple[str, ...] = (
    "usage_operation",
    "request_api",
    "agent_class",
    "auth_channel",
    "ingestion_runner",
    "actor_class",
)

# Keys that may appear in dimensions JSON but must NOT become shared flat
# bucket columns. Latest rollup preserves them via the opaque dimensions
# string so api_usage's additive schema does not grow when system_usage (or
# another family) adds inventory/gauge dimensions.
DIMENSION_JSON_ONLY_KEYS: Tuple[str, ...] = ("entity_type",)

# Flat dimension columns on additive bucket rows, excluding actor_class — the
# rollup/billing-sync code adds actor_class separately since it also gates
# billability via per-metric billable_actor_classes in
# billing_metric_registry.yaml (recipe may override via metric_registry_override).
DIMENSION_COLUMNS: List[str] = [
    "usage_operation",
    "request_api",
    "agent_class",
    "auth_channel",
    "ingestion_runner",
]

EVENTS_COLUMNS: Dict[str, pl.DataType] = {
    "customer_id": pl.Utf8(),
    "instance_id": pl.Utf8(),
    "metric_family": pl.Utf8(),
    "metric_name": pl.Utf8(),
    "dimensions": pl.Utf8(),
    "schema_version": pl.Utf8(),
    "usage_identity": pl.Utf8(),
    "attribution_type": pl.Utf8(),
    "value": pl.Int64(),
    "window_start_us": pl.Int64(),
    "window_end_us": pl.Int64(),
    "timestamp_ms": pl.Int64(),
    "dt": pl.Utf8(),
}

# Union schema for scanning additive + latest bucket files side-by-side.
# Polars takes the first file's columns unless an explicit schema is supplied;
# missing family-specific columns are inserted as null.
BUCKET_SCAN_SCHEMA: Dict[str, pl.DataType] = {
    "customer_id": pl.Utf8(),
    "instance_id": pl.Utf8(),
    "metric_family": pl.Utf8(),
    "metric_name": pl.Utf8(),
    "usage_operation": pl.Utf8(),
    "request_api": pl.Utf8(),
    "agent_class": pl.Utf8(),
    "auth_channel": pl.Utf8(),
    "ingestion_runner": pl.Utf8(),
    "actor_class": pl.Utf8(),
    "dimensions": pl.Utf8(),
    "value_sum": pl.Int64(),
    "granularity": pl.Utf8(),
    "time_bucket": pl.Utf8(),
    "merge_kind": pl.Utf8(),
    "job_run_id": pl.Utf8(),
    "computed_at": pl.Datetime("us", "UTC"),
    "schema_version": pl.Utf8(),
}


class SchemaContractError(Exception):
    def __init__(self, missing: List[str], mistyped: List[str]) -> None:
        self.missing = missing
        self.mistyped = mistyped
        super().__init__(
            f"events/ schema contract violation — missing={missing} mistyped={mistyped}"
        )


class TenantMismatchError(Exception):
    pass


def assert_events_schema(lf: pl.LazyFrame) -> None:
    actual = lf.collect_schema()
    missing = [c for c in EVENTS_COLUMNS if c not in actual]
    mistyped = [
        f"{c} (expected {expected}, got {actual[c]})"
        for c, expected in EVENTS_COLUMNS.items()
        if c in actual and actual[c] != expected
    ]
    if missing or mistyped:
        raise SchemaContractError(missing=missing, mistyped=mistyped)


def assert_tenant_rows(lf: pl.LazyFrame, customer_id: str, instance_id: str) -> None:
    # NFR3: rows are keyed by path partitions; a mismatch means a job is
    # about to aggregate another tenant's data into this tenant's buckets.
    bad = (
        lf.filter(
            (pl.col("customer_id") != customer_id)
            | (pl.col("instance_id") != instance_id)
        )
        .select(pl.len())
        .collect(engine="streaming")
        .item()
    )
    if bad:
        raise TenantMismatchError(
            f"{bad} row(s) with customer_id/instance_id not matching path tenant "
            f"({customer_id}/{instance_id}) — refusing to aggregate (NFR3)"
        )
