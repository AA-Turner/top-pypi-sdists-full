from enum import Enum

from acryl_datahub_cloud.periodic_analytics import schema

SCHEMA_VERSION = "periodic_analytics_v1"
DEFAULT_METRIC_FAMILY = "api_usage"
SYSTEM_USAGE_METRIC_FAMILY = "system_usage"
MANIFESTS_DIR = "_manifests"

# Run-lock keys are scoped to the source KIND, not the ingestion-source
# entity name, so a restate recipe and the scheduled source for the same
# layer contend for the same lock (see run_lock.py / ObjectStore.lock_key).
ROLLUP_SOURCE_KIND = "rollup"
BILLING_SYNC_SOURCE_KIND = "billing-sync"

# Additive api_usage bucket group keys — flat access-channel columns, not the
# opaque dimensions blob. Sourced from schema.DIMENSION_COLUMNS so additive
# rollups pick up new access-channel dims from one place.
BUCKET_GROUP_KEYS = (
    ["customer_id", "instance_id", "metric_family", "metric_name"]
    + schema.DIMENSION_COLUMNS
    + ["actor_class"]
)

# Latest (gauge) bucket group keys — family-specific dims stay in the opaque
# dimensions JSON (e.g. system_usage entity_type). Shared flats are only
# tenant + actor_class + metric identity; do not reuse BUCKET_GROUP_KEYS.
LATEST_BUCKET_GROUP_KEYS = [
    "customer_id",
    "instance_id",
    "metric_family",
    "metric_name",
    "actor_class",
    "dimensions",
]


class Layer(str, Enum):
    EVENTS = "events"
    HOURLY = "hourly_buckets"
    HOURLY_DISTINCT = "hourly_distinct_sets"
    DAILY_ADDITIVE = "daily_buckets"
    DAILY_DISTINCT = "daily_distinct_sets"
    MONTHLY = "monthly_buckets"
    BILLING_CLOSE = "billing_close"


class RunMode(str, Enum):
    SCHEDULED = "scheduled"
    CATCH_UP = "catch_up"
    RESTATE = "restate"
    PIPELINE_RESTATE = "pipeline_restate"
