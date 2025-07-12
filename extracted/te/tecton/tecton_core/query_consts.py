from typing import Optional

from tecton_core.compute_mode import ComputeMode
from tecton_core.specs import TimeWindowSpec


TECTON_TEMP_AGGREGATION_SECONDARY_KEY_COL: str = "_tecton_temp_agg_secondary_key_col"
TECTON_TEMP_STRUCT_PREFIX: str = "_tecton_internal_temp_struct"
MOCK_COLUMN_SEPARATOR: str = "__"


def default_case(field_name: str, compute_mode: Optional[ComputeMode] = None) -> str:
    # TODO (#BAT-15396): Clean up this as part of snowflake removal
    return field_name


def anchor_time() -> str:
    return "_anchor_time"


def effective_timestamp() -> str:
    return "_effective_timestamp"


def expiration_timestamp() -> str:
    return "_expiration_timestamp"


def timestamp_plus_ttl() -> str:
    return "_timestamp_plus_ttl"


def tecton_secondary_key_aggregation_indicator_col() -> str:
    return "_tecton_secondary_key_aggregation_indicator"


def temp_indictor_column_name(window: TimeWindowSpec) -> str:
    return f"{tecton_secondary_key_aggregation_indicator_col()}_{window.to_string()}"


def temp_intermediate_partial_aggregate_column_name(materialized_column_name: str, window: TimeWindowSpec) -> str:
    return f"{materialized_column_name}_{window.to_string()}"


def temp_struct_column_name(window: TimeWindowSpec) -> str:
    return f"{TECTON_TEMP_STRUCT_PREFIX}_{window.to_string()}"


def tecton_unique_id_col() -> str:
    return "_tecton_unique_id"


def tecton_spine_row_id_col() -> str:
    return "_tecton_spine_row_id"


def udf_internal() -> str:
    """Namespace used in `FeatureDefinitionAndJoinConfig` for dependent feature view
    columns. Dependent FVs to ODFVs have this prefix in the name and are
    filtered out before being returned to the user.
    """
    return "_udf_internal"


def odfv_internal_staging_table() -> str:
    return "_odfv_internal_table"


def aggregation_group_id() -> str:
    return "_tecton_aggregation_window_id"


def aggregation_tile_id() -> str:
    return "_tecton_aggregation_tile_id"


def aggregation_tile_list() -> str:
    return "_tecton_aggregation_tile_list"


def inclusive_start_time() -> str:
    return "_tecton_inclusive_start_time"


def exclusive_end_time() -> str:
    return "_tecton_exclusive_end_time"


def window_end_column_name() -> str:
    return "tile_end_time"


def valid_from() -> str:
    return "_valid_from"


def valid_to() -> str:
    return "_valid_to"


def interval_start_time() -> str:
    return "_interval_start_time"


def interval_end_time() -> str:
    return "_interval_end_time"


# Columns used for sawtooth aggregations.
def anchor_time_for_day_sawtooth() -> str:
    return "_anchor_time_for_day_sawtooth"


def anchor_time_for_hour_sawtooth() -> str:
    return "_anchor_time_for_hour_sawtooth"


def anchor_time_for_non_sawtooth() -> str:
    return "_anchor_time_for_non_sawtooth"


def is_day_sawtooth() -> str:
    return "_is_day_sawtooth_partition_column"


def is_hour_sawtooth() -> str:
    return "_is_hour_sawtooth_partition_column"


def is_non_sawtooth() -> str:
    return "_is_non_sawtooth_partition_column"


def time_partition_column_for_date() -> str:
    return "_tecton_date_partition_column"


def time_partition_column_for_hour() -> str:
    return "_tecton_hour_partition_column"


def time_partition_column_for_minute() -> str:
    return "_tecton_minute_partition_column"


def partition_key() -> str:
    return "_partition_key"
