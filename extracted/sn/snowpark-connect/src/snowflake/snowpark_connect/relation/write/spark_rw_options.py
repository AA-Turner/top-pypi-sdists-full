#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#
"""Build SPARK_RW_OPTIONS statement params from Iceberg write options.

SCOS forwards Spark's .option(k, v) write options to GS as a JSON bag via
the SPARK_RW_OPTIONS framework. GS parses, validates values for recognized
keys, and silently ignores unrecognized keys (matching Spark behavior).

SCOS is a pure transport layer — it does NOT validate option keys or values.
"""
from __future__ import annotations

import json

# Keys in the V1 proto options map that are NOT Iceberg write options.
# The V1 DataFrameWriter mixes table properties and internal options into
# the same map as write options. These must be excluded when building the
# SPARK_RW_OPTIONS JSON since GS only expects write options in that bag.
# V2 (DataFrameWriterV2) separates options from table_properties in the
# proto, so this filter is not needed there.
_V1_NON_WRITE_OPTIONS: frozenset[str] = frozenset(
    {
        # Table properties (V1 puts them in the same options map)
        "format-version",
        "iceberg.format-version",
        "comment",
        "max-snapshot-age.ms",
        "iceberg.max-snapshot-age.ms",
        "base_location",
        "location",
        "write.target-file-size",
        "target_file_size",
        "storage_serialization_policy",
        "iceberg.storage_serialization_policy",
        # Snowflake/SCOS-internal (not Iceberg write options)
        "partitionoverwritemode",
        "single",
        "snowflake_max_file_size",
        "truncate",
        "truncate_table",
        "path",
    }
)

# Options consumed locally by SCOS that must NOT be forwarded to GS.
# These are Iceberg write semantics that SCOS handles itself (e.g. column
# ordering/nullability validation). GS does not recognize them and will
# reject them with "not supported" if included in the SPARK_RW_OPTIONS bag.
_SCOS_LOCAL_OPTIONS: frozenset[str] = frozenset(
    {
        "check-ordering",
        "check-nullability",
    }
)


def _to_spark_rw_options_json(options: dict[str, str]) -> dict[str, str] | None:
    """Serialize write options as SPARK_RW_OPTIONS statement params.

    Filters out SCOS-local options (check-ordering, check-nullability) that
    GS does not support. Returns a dict with ENABLE_SPARK_RW_OPTIONS and
    SPARK_RW_OPTIONS keys, or None if no options remain after filtering.
    """
    filtered = {
        k: v for k, v in options.items() if k.lower() not in _SCOS_LOCAL_OPTIONS
    }
    if not filtered:
        return None
    rw_options_json = json.dumps(filtered, separators=(",", ":"))
    return {
        "ENABLE_SPARK_RW_OPTIONS": "true",
        "SPARK_RW_OPTIONS": rw_options_json,
    }


def build_spark_rw_options_params_v2(
    options: dict[str, str],
) -> dict[str, str] | None:
    """Build statement_params for a V2 (DataFrameWriterV2) iceberg write.

    V2 proto cleanly separates write options from table properties, so no
    table-property filtering is needed. SCOS-local options (check-ordering,
    check-nullability) are still stripped since GS does not support them.
    """
    return _to_spark_rw_options_json(options)


def build_spark_rw_options_params_v1(
    options: dict[str, str],
) -> dict[str, str] | None:
    """Build statement_params for a V1 (DataFrameWriter) iceberg write.

    V1 proto mixes table properties and internal options with write options
    in a single map. Filters out non-write-option keys before forwarding.
    """
    forwarded = {
        k: v for k, v in options.items() if k.lower() not in _V1_NON_WRITE_OPTIONS
    }
    return _to_spark_rw_options_json(forwarded)
