#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import re
import sys
from collections import defaultdict
from copy import copy, deepcopy

# Proto source for reference:
# https://github.com/apache/spark/blob/branch-3.5/connector/connect/common/src/main/protobuf/spark/connect/base.proto#L420
from pathlib import Path
from typing import Any, Dict, Optional

import jpype
import pyspark.sql.connect.proto.base_pb2 as proto_base
from packaging.version import InvalidVersion, parse as parse_version
from tzlocal import get_localzone_name

from snowflake import snowpark
from snowflake.snowpark._internal.analyzer.analyzer_utils import (
    quote_name_without_upper_casing,
    unquote_if_quoted,
)
from snowflake.snowpark.exceptions import SnowparkSQLException
from snowflake.snowpark.types import TimestampTimeZone, TimestampType
from snowflake.snowpark_connect.error.error_codes import ErrorCodes
from snowflake.snowpark_connect.error.error_utils import attach_custom_error_code
from snowflake.snowpark_connect.type_support import set_integral_types_conversion
from snowflake.snowpark_connect.utils.concurrent import SynchronizedDict
from snowflake.snowpark_connect.utils.context import (
    get_jpype_jclass_lock,
    get_spark_session_id,
)
from snowflake.snowpark_connect.utils.session import get_or_create_snowpark_session
from snowflake.snowpark_connect.utils.snowpark_connect_logging import logger
from snowflake.snowpark_connect.utils.spark_session_cache import (
    clear_spark_session_cache,
)
from snowflake.snowpark_connect.utils.telemetry import (
    SnowparkConnectNotImplementedError,
    telemetry,
)
from snowflake.snowpark_connect.version import VERSION as sas_version

# Server parameter for CTE optimization: enabled when Snowpark Connect version >= this value
SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION = (
    "SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION"
)


def str_to_bool(boolean_str: str) -> bool:
    assert boolean_str in (
        "True",
        "true",
        "False",
        "false",
        "1",
        "0",
        "",  # This is the default value, equivalent to False.
    ), f"Invalid boolean value: {boolean_str}"
    return boolean_str in ["True", "true", "1"]


# Spark byte-size suffixes accepted by JavaUtils.byteStringAsBytes. Powers of
# 1024, case-insensitive. See:
# https://github.com/apache/spark/blob/v3.5.3/common/network-common/src/main/java/org/apache/spark/network/util/JavaUtils.java
_SPARK_BYTE_SIZE_SUFFIXES: dict[str, int] = {
    "b": 1,
    "k": 1024,
    "kb": 1024,
    "m": 1024**2,
    "mb": 1024**2,
    "g": 1024**3,
    "gb": 1024**3,
    "t": 1024**4,
    "tb": 1024**4,
    "p": 1024**5,
    "pb": 1024**5,
}

# Snowflake TARGET_FILE_SIZE buckets for Iceberg tables, in (bytes, label)
# pairs, ordered smallest-first. See:
# https://docs.snowflake.com/en/sql-reference/sql/create-iceberg-table
_TARGET_FILE_SIZE_BUCKETS: tuple[tuple[int, str], ...] = (
    (16 * 1024**2, "16MB"),
    (32 * 1024**2, "32MB"),
    (64 * 1024**2, "64MB"),
    (128 * 1024**2, "128MB"),
)


def _parse_spark_byte_size(value: str) -> int:
    """Parse a Spark-style byte-size string into a byte count.

    Mirrors ``JavaUtils.byteStringAsBytes`` from Spark: an integer followed by
    an optional case-insensitive suffix (``b``, ``k``/``kb``, ``m``/``mb``,
    ``g``/``gb``, ``t``/``tb``, ``p``/``pb``). No suffix means raw bytes.
    Suffix multipliers use powers of 1024.

    Raises:
        ValueError: if ``value`` is empty, negative, or unparseable.
    """
    if str(value).strip() == "":
        raise ValueError("Empty byte size string")

    stripped = str(value).strip().lower()
    # Match 2-char suffixes (kb, mb, gb, tb, pb) before 1-char (k, m, g, t, p),
    # so "512mb" is read as 512 * MB and not 51 * 2b.
    for suffix_len in (2, 1):
        if (
            len(stripped) > suffix_len
            and stripped[-suffix_len:] in _SPARK_BYTE_SIZE_SUFFIXES
        ):
            number_part = stripped[:-suffix_len]
            suffix = stripped[-suffix_len:]
            if not number_part.lstrip("-").isdigit():
                raise ValueError(f"Invalid byte size string: {value!r}")
            number = int(number_part)
            if number < 0:
                raise ValueError(f"Negative byte size not allowed: {value!r}")
            return number * _SPARK_BYTE_SIZE_SUFFIXES[suffix]

    if not stripped.lstrip("-").isdigit():
        raise ValueError(f"Invalid byte size string: {value!r}")
    number = int(stripped)
    if number < 0:
        raise ValueError(f"Negative byte size not allowed: {value!r}")
    return number


def _bucket_to_target_file_size(byte_size: int) -> str:
    """Bucket a byte count to a Snowflake ``TARGET_FILE_SIZE`` value.

    Snowflake supports only ``{AUTO, 16MB, 32MB, 64MB, 128MB}`` for Iceberg
    tables. We round *down* to the largest bucket that does not exceed
    ``byte_size`` (so we never produce files larger than the user asked for),
    with a floor of ``16MB`` (smallest supported bucket) and a cap of
    ``128MB`` (largest supported bucket). A non-positive ``byte_size`` returns
    ``AUTO``.
    """
    if byte_size <= 0:
        return "AUTO"

    chosen = _TARGET_FILE_SIZE_BUCKETS[0][1]
    for threshold_bytes, label in _TARGET_FILE_SIZE_BUCKETS:
        if byte_size >= threshold_bytes:
            chosen = label
    return chosen


def spark_max_partition_bytes_to_target_file_size(value: str | None) -> str | None:
    """Translate ``spark.sql.files.maxPartitionBytes`` to Snowflake ``TARGET_FILE_SIZE``.

    Returns ``None`` when ``value`` is unset (caller should ``UNSET`` the
    session parameter), the literal string ``"AUTO"`` (any case) when the user
    explicitly passes ``AUTO``, or a bucketed label such as ``"32MB"``
    otherwise.

    Raises:
        ValueError: if ``value`` is not parseable as a Spark byte-size string.
    """
    if value is None or str(value).strip() == "":
        return None
    stripped = str(value).strip()
    if stripped.upper() == "AUTO":
        return "AUTO"
    byte_size = _parse_spark_byte_size(stripped)
    return _bucket_to_target_file_size(byte_size)


class GlobalConfig:
    """This class contains the global configuration for the Spark Server."""

    default_static_global_config = {
        # Defaults from Spark https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
        "spark.sql.warehouse.dir": None,
        "spark.sql.catalogImplementation": "in-memory",
        "spark.sql.sources.schemaStringLengthThreshold": 4000,
        "spark.sql.filesourceTableRelationCacheSize": 1000,
        "spark.sql.codegen.cache.maxEntries": 100,
        "spark.sql.codegen.comments": False,
        "spark.sql.debug": False,
        "spark.sql.hive.thriftServer.singleSession": False,
        "spark.sql.extensions": None,
        "spark.sql.cache.serializer": "org.apache.spark.sql.execution.columnar.DefaultCachedBatchSerializer",
        "spark.sql.queryExecutionListeners": 1000,
        "spark.sql.shuffleExchange.maxThreadThreshold": 1024,
        "spark.sql.broadcastExchange.maxThreadThreshold": 128,
        "spark.sql.subquery.maxThreadThreshold": 16,
        "spark.sql.resultQueryStage.maxThreadThreshold": 1024,
        "spark.sql.event.truncate.length": sys.maxsize,
        "spark.sql.legacy.sessionInitWithConfigDefaults": False,
        "spark.sql.defaultUrlStreamHandlerFactory.enabled": True,
        "spark.sql.streaming.ui.enabled": True,
        "spark.sql.streaming.ui.retainedProgressUpdates": 100,
        "spark.sql.streaming.ui.retainedQueries": 100,
        "spark.sql.metadataCacheTTLSeconds": -1,
        "spark.sql.streaming.ui.enabledCustomMetricList": None,
        "spark.sql.sources.disabledJdbcConnProviderList": "",
        "spark.python.sql.dataFrameDebugging.enabled": True,
        "spark.sql.extensions.test.loadFromCp": None,
        "spark.sql.streaming.streamingQueryListeners": None,
        # Defaults from Spark https://github.com/apache/spark/blob/master/sql/connect/server/src/main/scala/org/apache/spark/sql/connect/config/Connect.scala
        "spark.connect.grpc.binding.address": 15002,
        "spark.connect.grpc.port.maxRetries": 0,
        "spark.connect.grpc.interceptor.classes": 128 * 1024 * 1024,
        "spark.connect.grpc.maxInboundMessageSize": 128 * 1024 * 1024,
        "spark.connect.grpc.marshallerRecursionLimit": 1024,
        "spark.connect.session.manager.defaultSessionTimeout": True,
        "spark.connect.execute.reattachable.senderMaxStreamDuration": None,
        "spark.connect.extensions.expression.classes": None,
        "spark.connect.extensions.command.classes": None,
        "spark.connect.jvmStacktrace.maxSize": 1024,
        "spark.sql.connect.ui.retainedStatements": 200,
        "spark.connect.copyFromLocalToFs.allowDestLocal": False,
        "spark.sql.connect.ui.retainedSessions": 200,
        "spark.connect.grpc.maxMetadataSize": 1024,
        "spark.connect.session.planCache.maxSize": 16,
        "spark.connect.authenticate.token": True,
        "spark.connect.grpc.binding.port": None,
        "spark.connect.grpc.arrow.maxBatchSize": None,
        # Defaults from Spark https://github.com/apache/spark/blob/master/sql/hive/src/main/scala/org/apache/spark/sql/hive/HiveUtils.scala
        "spark.sql.hive.version": "2.3.9",
        "spark.sql.hive.metastore.version": "2.3.9",
        "spark.sql.hive.metastore.jars": "builtin",
        "spark.sql.hive.metastore.jars.path": None,
        "spark.sql.hive.metastore.sharedPrefixes": [
            "com.mysql.jdbc",
            "com.mysql.cj",
            "org.postgresql",
            "com.microsoft.sqlserver",
            "oracle.jdbc",
        ],
        "spark.sql.hive.metastore.barrierPrefixes": None,
        "spark.sql.globalTempDatabase": "global_temp",
        "spark.sql.catalog.spark_catalog.defaultDatabase": None,
        "spark.sql.ui.retainedExecutions": None,
    }

    readonly_config_list = [
        "snowpark.connect.version",
    ]

    default_global_config = {
        # TODO: This will need to be changed to the actual host of the driver.
        "spark.driver.host": "sc://localhost:15002",
        "spark.sql.pyspark.inferNestedDictAsStruct.enabled": "false",
        "spark.sql.pyspark.legacy.inferArrayTypeFromFirstElement.enabled": "false",
        "spark.sql.repl.eagerEval.enabled": "false",
        "spark.sql.repl.eagerEval.maxNumRows": "20",
        "spark.sql.repl.eagerEval.truncate": "20",
        "spark.sql.session.localRelationCacheThreshold": "2147483647",
        "spark.sql.session.timeZone": get_localzone_name(),  # spark by default uses jvm local timezone
        "spark.sql.timestampType": "TIMESTAMP_LTZ",
        "spark.sql.crossJoin.enabled": "true",
        "spark.sql.caseSensitive": "false",
        "spark.sql.mapKeyDedupPolicy": "EXCEPTION",
        "spark.sql.ansi.enabled": "false",
        # SNOW-3317615: PySpark 3.5.6 config default is ANSI, but V1 Hive/Parquet
        # tables (used by EMR customers) bypass TableOutputResolver entirely,
        # making effective behavior LEGACY. Default to LEGACY to match actual
        # customer experience on EMR.
        "spark.sql.storeAssignmentPolicy": "LEGACY",
        "spark.sql.legacy.allowHashOnMapType": "false",
        "spark.sql.legacy.negativeIndexInArrayInsert": "false",
        "spark.sql.sources.default": "parquet",
        "spark.Catalog.databaseFilterInformationSchema": "false",
        "spark.sql.parser.quotedRegexColumnNames": "false",
        # custom configs
        "snowpark.connect.version": ".".join(map(str, sas_version)),
        "snowpark.connect.temporary.views.create_in_snowflake": "false",
        # Control whether repartition(n) on a DataFrame forces splitting into n files during writes
        # This matches spark behavior more closely, but introduces overhead.
        "snowflake.repartition.for.writes": "false",
        "snowpark.connect.structured_types.fix": "true",
        # Local relation optimization: Use List[Row] for small data, PyArrow for large data
        # Enabled in production by default to improve performance for createDataFrame on small local relations.
        # Disabled in tests by default unless explicitly enabled to stabilize flaky tests that are not applying row ordering.
        # SNOW-2719980: Remove this flag after test fragility issues are resolved
        "snowpark.connect.localRelation.optimizeSmallData": "true",
        "spark.sql.execution.arrow.maxRecordsPerBatch": "10000",  # TODO: no-op
        # USE_LOGICAL_TYPE enables proper handling of Parquet logical types (TIMESTAMP, DATE, DECIMAL).
        # Without useLogicalType set to "true", Parquet TIMESTAMP (INT64 physical) is incorrectly read as NUMBER(38,0).
        # SNOW-3245146: default flipped from "false" to "true" in 1.23.0.
        "snowpark.connect.parquet.useLogicalType": "true",
        # When true, Parquet reads always use the server-side INFER_SCHEMA result
        # as-is and skip SAS's FLATTEN-based fallback discovery in
        # `_merge_variant_schemas`. Use this on deployments that fully trust
        # Snowflake's structured-type INFER_SCHEMA output (requires the backend
        # ENABLE_INFER_SCHEMA_NESTED_SCHEMA_SUPPORT_FOR_SCOS parameter set) and
        # want to avoid the per-read sampling cost of the legacy slow path.
        # Default false to preserve current behavior (fast path for native
        # structured types, slow path otherwise).
        "snowpark.connect.parquet.useServerInferredSchemaOnly": "false",
        "spark.sql.legacy.dataset.nameNonStructGroupingKeyAsValue": "false",
        "snowpark.connect.handleIntegralOverflow": "false",
        "snowpark.connect.scala.version": "2.12",
        # Control whether to convert decimal - to integral types and vice versa: DecimalType(p,0) <-> ByteType/ShortType/IntegerType/LongType
        # Values: "client_default" (behavior based on client type), "enabled", "disabled"
        "snowpark.connect.integralTypesEmulation": "client_default",
        # Artifact Repository for UDF/UDTF/UDAF/Sproc package resolution
        # Set to the name of an artifact repository created in Snowflake (e.g., "MY_PYPI_REPO")
        # When set, packages will be resolved from the specified artifact repository instead of Anaconda
        "snowpark.connect.artifact_repository": "",
        # Resource constraint for UDFs - when set to "x86", UDFs will be created with architecture constraint
        # This requires an x86-compatible warehouse for execution
        "snowpark.connect.udf.resource_constraint.architecture": None,
        # Test-only configuration: Force UDFs/UDTFs to be created in stored procedures
        # regardless of Python version compatibility. This helps test SPROC code paths in local CI.
        "snowpark.connect.test.force_create_sproc": "false",
        "spark.sql.iceberg.merge-schema": "false",
        # When true, use the native __SNOWPARK_INTERNAL_SUBSTRING SQL function
        # for string inputs instead of the CASE/WHEN boundary-check emulation.
        "snowpark.connect.enable_native_sql_for_substring": "true",
        # When true (default), aes_encrypt / aes_decrypt / try_aes_decrypt use the
        # ENCRYPT_RAW / DECRYPT_RAW based implementation (raw binary key, Spark
        # compatible ciphertext layout). When false, fall back to the legacy
        # ENCRYPT / DECRYPT (passphrase-derived key) implementation.
        "snowpark.connect.enable_aes_raw_functions": "true",
        "snowpark.connect.enable_partition_specs_in_show_tables": "false",
        # Nullability tracking for top-level columns.
        # When false (default), all columns are forced to nullable=True.
        # When true, column nullability from type resolvers is preserved.
        "snowpark.connect.nullability.trackColumns": "false",
        # Nullability tracking for complex types (Array, Map, Struct).
        # When false (default), inner nullability of complex types is forced to True
        # (safe: prevents NOT NULL casts in generated SQL that could fail at runtime).
        # When true, real nullability from type resolvers is used. This can produce
        # ARRAY(DOUBLE NOT NULL) casts that fail if an expression silently yields NULL.
        "snowpark.connect.nullability.trackComplexTypes": "false",
        # When true (default), terminal Snowpark actions attach a statement-level
        # JSON QUERY_TAG with caller file/line/fn from the client stack trace.
        "snowpark.connect.addDebugInfoToQueryTag": "true",
        # When true, conf.get(key) raises SparkNoSuchElementException for keys
        # that are not recognized by SCOS (matching Spark behavior). When false
        # (default), unknown keys return None silently and a telemetry event is
        # emitted instead, allowing us to observe impact before enabling the BCR.
        "snowpark.connect.config.raiseForUnknownKeys": "false",
    }

    boolean_config_list = [
        "spark.sql.pyspark.inferNestedDictAsStruct.enabled",
        "spark.sql.pyspark.legacy.inferArrayTypeFromFirstElement.enabled",
        "spark.sql.repl.eagerEval.enabled",
        "spark.sql.crossJoin.enabled",
        "spark.sql.caseSensitive",
        "snowpark.connect.localRelation.optimizeSmallData",
        "snowpark.connect.parquet.useLogicalType",
        "snowpark.connect.parquet.useServerInferredSchemaOnly",
        "spark.sql.ansi.enabled",
        "spark.sql.legacy.allowHashOnMapType",
        "spark.sql.legacy.negativeIndexInArrayInsert",
        "spark.Catalog.databaseFilterInformationSchema",
        "spark.sql.parser.quotedRegexColumnNames",
        "snowflake.repartition.for.writes",
        "spark.sql.legacy.dataset.nameNonStructGroupingKeyAsValue",
        "snowpark.connect.handleIntegralOverflow",
        "snowpark.connect.test.force_create_sproc",
        "snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables",
        "snowpark.connect.sql.returnDmlMetadata",
        "spark.sql.iceberg.merge-schema",
        "snowpark.connect.enable_native_sql_for_substring",
        "snowpark.connect.enable_aes_raw_functions",
        "snowpark.connect.enable_partition_specs_in_show_tables",
        "snowpark.connect.nullability.trackColumns",
        "snowpark.connect.nullability.trackComplexTypes",
        "snowpark.connect.addDebugInfoToQueryTag",
        "snowpark.connect.config.raiseForUnknownKeys",
    ]

    int_config_list = [
        "spark.sql.repl.eagerEval.maxNumRows",
        "spark.sql.repl.eagerEval.truncate",
        "spark.sql.session.localRelationCacheThreshold",
    ]

    # This is a mapping of the configuration key to a function that assigns the
    # configuration value to a Snowpark session. This is only needed for configurations
    # that we need to make available to the Snowpark session.
    snowpark_config_mapping = {
        # Snowpark uses query_tag for the application name.
        "spark.app.name": lambda session, name: setattr(
            session, "query_tag", f"Spark-Connect-App-Name={name}"
        ),
        # TODO SNOW-2896871: Remove with version 1.10.0
        "snowpark.connect.udf.imports": lambda session, imports: parse_imports(
            session, imports, "python"
        ),
        "snowpark.connect.udf.python.imports": lambda session, imports: parse_imports(
            session, imports, "python"
        ),
        "snowpark.connect.udf.java.imports": lambda session, imports: parse_imports(
            session, imports, "java"
        ),
        # When artifact repository changes, cached UDXFs need to be recreated with the new repository
        "snowpark.connect.artifact_repository": lambda session, _: clear_spark_session_cache(
            get_spark_session_id()
        ),
    }

    float_config_list = []

    def __init__(self) -> None:
        self.global_config = SynchronizedDict(copy(self.default_global_config))
        # Keys the user has *explicitly* set (vs. defaults that are pre-loaded
        # into global_config at startup). Spark's RuntimeConfig.get(key, default)
        # only returns a config's built-in value when the key is explicitly set;
        # otherwise it returns the caller-supplied default. We can't tell the two
        # apart from global_config alone (defaults live there too), so we track
        # explicit sets separately. Used as a set (value is always True).
        self.user_set_keys = SynchronizedDict()
        for key in self.global_config.keys():
            setattr(self, key.replace(".", "_"), self._get_config_setting(key))

    def _get_config_setting(self, key: str) -> bool | int | float | str | None:
        """Get the configuration setting for the key based on the setting type."""
        if key in self.boolean_config_list:
            return str_to_bool(self.global_config[key])
        elif key in self.int_config_list:
            return int(self.global_config[key])
        elif key in self.float_config_list:
            return float(self.global_config[key])
        else:
            return self.global_config[key]

    def __getattr__(self, item):
        return self.get(item.replace("_", "."))

    def __getitem__(self, item: str) -> str:
        return self.get(item)

    def __setitem__(self, key: str, value: str) -> None:
        return self.set(key, value)

    def get(self, key, default=None) -> str:
        self._initialize_if_static_config_not_set(key)
        return self.global_config.get(key, default)

    def get_all(self) -> dict[str, str]:
        return self.global_config.copy()

    def set(self, key: str, value: str) -> None:
        # Spark Connect sends us only string values, with empty string being
        # equivalent to None.
        if value == "":
            value = None
        self.global_config[key] = value
        if key in self.snowpark_config_mapping.keys():
            snowpark_session = get_or_create_snowpark_session()
            self.snowpark_config_mapping[key](snowpark_session, value)
        # This is necessary to make the configuration available as an attribute.
        setattr(self, key.replace(".", "_"), self._get_config_setting(key))

    def unset(self, key: str) -> None:
        self.global_config.remove(key)

    def is_modifiable(self, key) -> bool:
        self._initialize_if_static_config_not_set(key)
        return bool(
            (key in self.default_global_config or valid_session_config_key(key))
            and not self.is_static_config(key)
        )

    def _initialize_if_static_config_not_set(self, key):
        """
        Spark maintains set of 'static' config values that are immutable.
        SAS allows static configs only to be set once and only if they were never read before.
        This function initializes static configs with default values if they haven't been set.
        """
        if self.is_static_config(key) and not self.is_set(key):
            default_value = self.default_static_global_config[key]
            self.set(key, default_value)
            snowflake_session = get_or_create_snowpark_session()
            set_snowflake_parameters(key, default_value, snowflake_session)

    def is_static_config(self, key):
        return key in self.default_static_global_config.keys()

    def is_set(self, key):
        return key in self.global_config.keys()

    def mark_user_set(self, key: str) -> None:
        """Record that the user explicitly set this config key."""
        self.user_set_keys[key] = True

    def unmark_user_set(self, key: str) -> None:
        """Forget that the user set this config key (e.g. on unset)."""
        self.user_set_keys.remove(key)

    def is_user_set(self, key: str) -> bool:
        """Whether the user explicitly set this config key (vs. a default)."""
        return key in self.user_set_keys


SESSION_CONFIG_KEY_WHITELIST = {
    "spark.hadoop.fs.s3a.access.key",
    "spark.hadoop.fs.s3a.secret.key",
    "spark.hadoop.fs.s3a.session.token",
    "spark.sql.execution.pythonUDTF.arrow.enabled",
    "spark.sql.tvf.allowMultipleTableArguments.enabled",
    "snowpark.connect.sql.passthrough",
    "snowpark.connect.cte.optimization_enabled",
    "snowpark.connect.iceberg.external_volume",
    "snowpark.connect.iceberg.base_location",
    "snowpark.connect.sql.partition.external_table_location",
    "snowpark.connect.udtf.compatibility_mode",
    "snowpark.connect.views.duplicate_column_names_handling_mode",
    "snowpark.connect.temporary.views.create_in_snowflake",
    "snowpark.connect.enable_snowflake_extension_behavior",
    "spark.hadoop.fs.s3a.server-side-encryption.key",
    "spark.hadoop.fs.s3a.assumed.role.arn",
    "snowpark.connect.describe_cache_ttl_seconds",
    "mapreduce.fileoutputcommitter.marksuccessfuljobs",
    "spark.sql.parquet.enable.summary-metadata",
    "parquet.enable.summary-metadata",
    "spark.sql.sources.partitionOverwriteMode",
    "snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables",
    "snowpark.connect.sql.returnDmlMetadata",
    "snowpark.connect.csv.continueOnError",  # Deprecated: use .option("mode", "DROPMALFORMED")
    # SNOW-3295599: SCOS-internal knob to flip Snowflake's SKIP_BLANK_LINES on
    # CSV reads. Default TRUE preserves Spark-default semantics (Univocity also
    # defaults to skip-empty-lines). Set FALSE to surface blank lines as
    # malformed records (combine with mode=FAILFAST to raise).
    "snowpark.connect.csv.skipBlankLines",
    "spark.sql.parquet.inferTimestampNTZ.enabled",
    "snowpark.connect.io.validations.mode",
    "spark.sql.iceberg.merge-schema",
    "snowpark.connect.read.anchorStagePaths",
    "snowpark.connect.read.hivePartitionPruning",
    "snowpark.connect.large_query_breakdown.enabled",
    "snowpark.connect.large_query_breakdown.complexity_lower_bound",
    "snowpark.connect.large_query_breakdown.complexity_upper_bound",
    "spark.sql.columnNameOfCorruptRecord",
    # SNOW-3674169: Spark's read-side partition-bytes hint; SCOS uses it as a
    # session-scoped default for Iceberg ``TARGET_FILE_SIZE`` on subsequent
    # CREATE ICEBERG TABLE writes (see ``_build_iceberg_config``).
    "spark.sql.files.maxPartitionBytes",
}

# Static Spark configs that nonetheless accept a *per-session* override at
# runtime. Kept separate from SESSION_CONFIG_KEY_WHITELIST because the two drive
# different write paths: whitelist keys are non-static and go through the normal
# set_config_param path (validated, then written to BOTH global_config and the
# session config); these keys are *static* (in default_static_global_config, so
# Spark-accurately report isModifiable=False) and must instead (a) skip the
# static-modification guard and (b) leave the immutable process-global value
# untouched -- only the per-session overlay is written. The process-global value
# (set once at server startup, e.g. via ``--conf`` on EMR-style deployments)
# stays as the fallback. Currently only ``spark.sql.extensions`` (so a session
# can opt into the Iceberg SQL parser without a process-global, parser-replacing
# change). Readers resolve session-overlay first, then global.
SESSION_OVERRIDABLE_STATIC = {"spark.sql.extensions"}
AZURE_ACCOUNT_KEY = re.compile(
    r"^fs\.azure\.sas\.[^\.]+\.[^\.]+\.blob\.core\.windows\.net$"
)
AZURE_SAS_KEY = re.compile(
    r"^fs\.azure\.sas\.fixed\.token\.[^\.]+\.dfs\.core\.windows\.net$"
)


def valid_session_config_key(key: str):
    return (
        key in SESSION_CONFIG_KEY_WHITELIST  # AWS session keys
        or key in SESSION_OVERRIDABLE_STATIC  # e.g. spark.sql.extensions
        or AZURE_SAS_KEY.match(key)  # Azure session keys
        or AZURE_ACCOUNT_KEY.match(key)  # Azure account keys
    )


class SessionConfig:
    """This class contains the session configuration for the Spark Server."""

    default_session_config = {
        "snowpark.connect.sql.passthrough": "false",
        # None means "not explicitly set" - defer to snowpark's server-side parameter
        # When explicitly set to "true" or "false", user's choice takes priority
        "snowpark.connect.cte.optimization_enabled": None,
        "snowpark.connect.udtf.compatibility_mode": "false",
        "snowpark.connect.views.duplicate_column_names_handling_mode": "rename",
        "spark.sql.execution.pythonUDF.arrow.enabled": "false",
        "spark.sql.execution.pythonUDTF.arrow.enabled": "false",
        "spark.sql.execution.pandas.convertToArrowArraySafely": "false",
        "spark.sql.tvf.allowMultipleTableArguments.enabled": "true",
        "snowpark.connect.enable_snowflake_extension_behavior": "false",
        "snowpark.connect.describe_cache_ttl_seconds": "300",
        "snowpark.connect.sql.partition.external_table_location": None,
        "mapreduce.fileoutputcommitter.marksuccessfuljobs": "false",
        "spark.sql.parquet.enable.summary-metadata": "false",
        "parquet.enable.summary-metadata": "false",
        # JDBC driver JARs - comma-separated list of local paths or Maven coordinates
        # Example: "/path/to/driver.jar" or "org.neo4j:neo4j-jdbc-driver:4.0.9"
        "spark.jars": None,
        # Spark reports this default in upper case ("STATIC"); keep the same
        # casing so conf.get returns a value identical to Spark.
        "spark.sql.sources.partitionOverwriteMode": "STATIC",
        "snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables": "false",
        "snowpark.connect.sql.returnDmlMetadata": "false",
        "snowpark.connect.csv.continueOnError": "false",  # Deprecated
        "snowpark.connect.csv.skipBlankLines": "true",  # SNOW-3295599
        "spark.sql.parquet.inferTimestampNTZ.enabled": "true",
        # IO validations mode: "lenient" (default) or "strict"
        # When "strict", enforce Spark-compatible validations (e.g., SPARK-35912)
        "snowpark.connect.io.validations.mode": "lenient",
        "spark.sql.iceberg.merge-schema": "false",
        # When true (default), file/glob read paths are anchored at the SQL
        # boundary using PATTERN/trailing-slash so Snowflake stage prefix
        # matching cannot pull in unintended sibling files or directories
        # (SNOW-3428536). Set to "false" to revert to the legacy unanchored
        # behavior as a safety hatch.
        "snowpark.connect.read.anchorStagePaths": "true",
        # When true (default), static Hive partition predicates on Filter→Read
        # plans narrow stage paths before LIST/COPY (SNOW-3295586 / GAP-018).
        "snowpark.connect.read.hivePartitionPruning": "true",
        # Large query breakdown: None = defer to Snowpark/server default
        "snowpark.connect.large_query_breakdown.enabled": None,
        "snowpark.connect.large_query_breakdown.complexity_lower_bound": None,
        "snowpark.connect.large_query_breakdown.complexity_upper_bound": None,
        # Spark default for the corrupt-record column injected/used by CSV/JSON
        # readers in PERMISSIVE mode. See SQLConf.COLUMN_NAME_OF_CORRUPT_RECORD.
        "spark.sql.columnNameOfCorruptRecord": "_corrupt_record",
        # SNOW-3674169: ``""`` means unset — the Iceberg writer falls back to
        # Snowflake's own ``TARGET_FILE_SIZE`` default (``AUTO``).
        "spark.sql.files.maxPartitionBytes": "",
    }

    def __init__(self) -> None:
        self.config = deepcopy(self.default_session_config)
        self.table_metadata: Dict[str, Dict[str, Any]] = {}

    def __getitem__(self, item: str) -> str:
        return self.get(item)

    def __setitem__(self, key: str, value: str) -> None:
        return self.set(key, value)

    def get(self, key, default="") -> str:
        return self.config.get(key, default)

    def set(self, key: str, value: str) -> None:
        if not valid_session_config_key(key):
            return

        self.config[key] = value


CONFIG_ALLOWED_VALUES: dict[str, tuple] = {
    "snowpark.connect.io.validations.mode": (
        "lenient",
        "strict",
    ),
    "snowpark.connect.views.duplicate_column_names_handling_mode": (
        "rename",
        "fail",
        "drop",
    ),
    "snowpark.connect.integralTypesEmulation": (
        "client_default",
        "enabled",
        "disabled",
    ),
    "spark.sql.sources.partitionOverwriteMode": (
        # Spark accepts this config case-insensitively; allow both the lower-case
        # values users typically pass and the upper-case form Spark reports.
        "static",
        "dynamic",
        "STATIC",
        "DYNAMIC",
    ),
    "spark.sql.storeAssignmentPolicy": (
        "ANSI",
        "LEGACY",
        "STRICT",
    ),
    "snowpark.connect.udf.resource_constraint.architecture": (
        None,
        "",
        "x86",
    ),
}

# Set some default configuration that are necessary for the driver.
global_config = GlobalConfig()
sessions_config: defaultdict[str, SessionConfig] = defaultdict(SessionConfig)


def _config_value_to_proto_str(value: Any) -> str:
    """Stringify a config value for the protobuf KeyValue.value field.

    Spark serializes config booleans as lowercase text ("true"/"false"), but
    SCOS stores some defaults as real Python bools (see
    ``GlobalConfig.default_static_global_config``) whose ``str()`` is
    capitalized ("True"/"False"). Lowercase booleans so the wire format matches
    Spark; every other type uses ``str()`` unchanged.
    """
    if isinstance(value, bool):
        return str(value).lower()
    return str(value)


def _is_known_config(key: str) -> bool:
    """Whether SCOS recognizes ``key`` as a configuration it knows about.

    A key is "known" if it is currently set, is one of SCOS's built-in global
    defaults (including static configs), is a session-level config default, or is
    a valid session config key. Spark distinguishes registered configs (which
    ``RuntimeConfig.get`` returns ``None``/the default for) from completely
    unregistered keys (for which it raises). SCOS approximates Spark's config
    registry with these known-config sources.
    """
    return (
        global_config.is_set(key)
        or global_config.is_static_config(key)
        or key in global_config.default_global_config
        or key in SessionConfig.default_session_config
        or valid_session_config_key(key)
    )


def _sql_conf_not_found_exception(key: str) -> Exception:
    """Build the exception Spark raises from ``conf.get`` for an unknown config.

    The message matches Spark's ``SQL_CONF_NOT_FOUND`` error condition, and the
    exception type (``SparkNoSuchElementException``) is mapped so the client
    reconstructs it the same way it does for a real Spark Connect server.
    """
    from snowflake.snowpark_connect.error.error_utils import SparkNoSuchElementException

    exception = SparkNoSuchElementException(
        f'[SQL_CONF_NOT_FOUND] The SQL config "{key}" cannot be found. '
        "Please verify that the config exists."
    )
    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
    return exception


def route_config_proto(
    config: proto_base.ConfigRequest,
    snowpark_session: snowpark.Session,
) -> proto_base.ConfigResponse:
    global global_config
    global sessions_config

    op_type = config.operation.WhichOneof("op_type")
    telemetry.report_config_op_type(op_type)
    match op_type:
        case "set":
            logger.debug("SET")
            telemetry.report_config_set(config.operation.set.pairs)
            for pair in config.operation.set.pairs:
                # Check if the value field is present, not present when invalid fields are set in conf.
                if not pair.HasField("value"):
                    from pyspark.errors import IllegalArgumentException

                    exception = IllegalArgumentException(
                        f"Cannot set config '{pair.key}' to None"
                    )
                    attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
                    raise exception

                set_config_param(
                    config.session_id, pair.key, pair.value, snowpark_session
                )

            return proto_base.ConfigResponse(session_id=config.session_id)
        case "unset":
            logger.debug("UNSET")
            telemetry.report_config_unset(config.operation.unset.keys)
            for key in config.operation.unset.keys:
                unset_config_param(config.session_id, key, snowpark_session)

            return proto_base.ConfigResponse(session_id=config.session_id)
        case "get":
            logger.debug("GET")
            res = proto_base.ConfigResponse(session_id=config.session_id)
            telemetry.report_config_get(config.operation.get.keys)
            for key in config.operation.get.keys:
                pair = res.pairs.add()
                pair.key = key
                # Mirror Spark's RuntimeConfig.get(key) (no default), which maps
                # to SQLConf.getConfString(key): it returns the config value (or
                # its built-in default), and raises NoSuchElementException when
                # the key is neither set nor a known config with a default.
                val = global_config.get(key)
                if val is None:
                    # Some configs (e.g. partitionOverwriteMode) only carry a
                    # Spark-defined default in the session config, not in
                    # global_config. Fall back to it before deciding the key is
                    # unknown.
                    #
                    # SNOW-3674169: ``spark.sql.files.maxPartitionBytes`` uses
                    # ``""`` in SessionConfig only for the Iceberg write path
                    # (defer to Snowflake AUTO). Spark ``conf.get`` after
                    # ``unset`` must return ``None``, not ``""``.
                    if key != "spark.sql.files.maxPartitionBytes":
                        val = SessionConfig.default_session_config.get(key)
                if val is not None:
                    pair.value = _config_value_to_proto_str(val)
                elif not _is_known_config(key):
                    telemetry.report_unknown_config_get(key)
                    if global_config.snowpark_connect_config_raiseForUnknownKeys:
                        raise _sql_conf_not_found_exception(key)
            return res
        case "get_with_default":
            logger.debug("GET_WITH_DEFAULT")
            telemetry.report_config_get(
                [pair.key for pair in config.operation.get_with_default.pairs]
            )
            result_pairs = []
            for pair in config.operation.get_with_default.pairs:
                default = pair.value if pair.HasField("value") else None
                # Mirror Spark's RuntimeConfig.get(key, default), which maps to
                # SQLConf.getConfString(key, default): when the key was not
                # explicitly set by the user, Spark returns the caller-supplied
                # default rather than the config's built-in default. This holds
                # for both static and runtime configs. SCOS pre-loads runtime
                # defaults (and materializes static defaults on read), so the
                # store alone can't distinguish "user set" from "default"; we
                # consult user_set_keys instead.
                if global_config.is_user_set(pair.key):
                    val = global_config.get(pair.key, default)
                else:
                    val = default
                key_value = proto_base.KeyValue(key=pair.key)
                # protobuf KeyValue.value is a string field, so non-string config
                # values (e.g. Python bool/int from static defaults) must be
                # stringified. None means "no value" and is left unset rather
                # than serialized as the literal "None".
                if val is not None:
                    key_value.value = _config_value_to_proto_str(val)
                result_pairs.append(key_value)
            return proto_base.ConfigResponse(
                session_id=config.session_id,
                pairs=result_pairs,
            )
        case "get_option":
            logger.debug("GET_OPTION")
            res = proto_base.ConfigResponse(session_id=config.session_id)
            telemetry.report_config_get(config.operation.get_option.keys)
            for key in config.operation.get_option.keys:
                pair = res.pairs.add()
                pair.key = key
                val = global_config.get(key, None)
                if val is not None:
                    pair.value = _config_value_to_proto_str(val)
            return res
        case "get_all":
            logger.debug("GET_ALL")
            res = proto_base.ConfigResponse(session_id=config.session_id)
            prefix = (
                config.operation.get_all.prefix
                if config.operation.get_all.HasField("prefix")
                else None
            )
            config_items = global_config.get_all()
            for item in config_items.items():
                if prefix is None or item[0].startswith(prefix):
                    if item[1] is None:
                        continue
                    pair = res.pairs.add()
                    pair.key = (
                        item[0] if prefix is None else item[0].removeprefix(prefix)
                    )
                    pair.value = _config_value_to_proto_str(item[1])
            return res
        case "is_modifiable":
            logger.debug("IS_MODIFIABLE")
            res = proto_base.ConfigResponse(session_id=config.session_id)
            telemetry.report_config_get(config.operation.is_modifiable.keys)
            for key in config.operation.is_modifiable.keys:
                pair = res.pairs.add()
                pair.key = key
                # Change value to lowercase in order to mimic Java boolean type.
                pair.value = str(global_config.is_modifiable(key)).lower()
            return res
        case _:
            exception = SnowparkConnectNotImplementedError(
                f"Unexpected request {config}"
            )
            attach_custom_error_code(exception, ErrorCodes.UNSUPPORTED_OPERATION)
            raise exception


def _load_spark_jars(jars_value: str) -> None:
    """
    Load JDBC driver JARs specified in spark.jars config.

    Supports:
    - Local file paths: "/path/to/driver.jar"
    - Multiple JARs: comma-separated list

    JARs are added to JPype classpath.
    """
    if not jars_value:
        return

    for jar_spec in jars_value.split(","):
        jar_spec = jar_spec.strip()
        if not jar_spec:
            continue

        jar_path = Path(jar_spec)
        if jar_path.exists():
            jpype.addClassPath(str(jar_path))
            logger.info(f"Added JAR to classpath: {jar_path}")
        else:
            exception = RuntimeError(f"JAR file not found: {jar_spec}")
            attach_custom_error_code(
                exception, ErrorCodes.RESOURCE_INITIALIZATION_FAILED
            )
            raise exception


def set_config_param(
    session_id: str, key, val, snowpark_session: snowpark.Session
) -> None:
    # Session-overridable static configs (e.g. ``spark.sql.extensions``): record
    # the value as a per-session overlay and leave the immutable process-global
    # value untouched. This is the one allowed way to "modify" such a static
    # config at runtime, so it must come before the static-config guard.
    if key in SESSION_OVERRIDABLE_STATIC:
        sessions_config[session_id][key] = val
        return

    _verify_static_config_not_modified(key)
    _verify_is_not_readonly_config(key)
    _verify_is_valid_config_value(key, val)

    # Handle spark.jars specially - load JARs into JPype classpath
    if key == "spark.jars" and val:
        _load_spark_jars(val)

    global_config[key] = val
    # This is the only entry point for client-driven `conf.set(...)`, so it is
    # exactly where an "explicit user set" happens (internal default
    # materialization goes through GlobalConfig.set directly and is not marked).
    global_config.mark_user_set(key)

    if valid_session_config_key(key):
        sessions_config[session_id][key] = val
    set_snowflake_parameters(key, val, snowpark_session)


def unset_config_param(
    session_id: str, key, snowpark_session: snowpark.Session
) -> None:
    # Clear the per-session overlay for session-overridable static configs; the
    # process-global value remains the fallback.
    if key in SESSION_OVERRIDABLE_STATIC:
        sessions_config[session_id].set(key, "")
        return

    _verify_static_config_not_modified(key)

    default_value = global_config.default_global_config.get(key, None)

    # Remove the key from global config. For ``spark.sql.files.maxPartitionBytes``
    # the built-in default is ``""`` (meaning "defer to Snowflake AUTO"), but
    # Spark's ``conf.get`` after ``unset`` must return ``None``, not ``""``.
    if default_value is None or (
        key == "spark.sql.files.maxPartitionBytes" and default_value == ""
    ):
        global_config.unset(key)
    else:
        global_config[key] = default_value
    # After unset the key is back to its default, no longer an explicit user set.
    global_config.unmark_user_set(key)

    if valid_session_config_key(key):
        default_session_value = SessionConfig.default_session_config.get(key, "")
        sessions_config[session_id].set(key, default_session_value)
        # Use session default for set_snowflake_parameters if this is a session config key
        default_value = default_session_value

    set_snowflake_parameters(key, default_value, snowpark_session)


def is_iceberg_sql_extensions_enabled() -> bool:
    """True when the Iceberg Spark SQL Extensions parser should be active for the
    current request.

    Resolves ``spark.sql.extensions`` with **session overlay first, then the
    process-global static value** (see ``SESSION_OVERRIDABLE_STATIC``):
    - a session that opted in via ``conf.set("spark.sql.extensions", <iceberg
      extension class>)`` activates the Iceberg parser for that session only, so
      non-iceberg sessions keep the base SCOS parser; and
    - server-configured / EMR-style deployments that set the static, process
      -global ``spark.sql.extensions`` at startup still work via the fallback.
    """
    from snowflake.snowpark_connect.utils.context import get_spark_session_id
    from snowflake.snowpark_connect.utils.jvm_classpath import (
        is_iceberg_sql_extensions_config,
    )

    value = None
    try:
        value = sessions_config[get_spark_session_id()].get("spark.sql.extensions")
    except Exception:
        value = None
    if not value:
        value = global_config.get("spark.sql.extensions")
    return is_iceberg_sql_extensions_config(value)


def _verify_static_config_not_modified(key: str) -> None:
    # https://github.com/apache/spark/blob/v3.5.3/sql/core/src/main/scala/org/apache/spark/sql/RuntimeConfig.scala#L161
    # Spark does not allow to modify static configurations at runtime.
    if global_config.is_static_config(key) and global_config.is_set(key):
        exception = ValueError(f"Cannot modify the value of a static config: {key}")
        attach_custom_error_code(exception, ErrorCodes.CONFIG_CHANGE_NOT_ALLOWED)
        raise exception


def _verify_is_valid_config_value(key: str, value: Any) -> None:
    if key in CONFIG_ALLOWED_VALUES and value not in CONFIG_ALLOWED_VALUES[key]:
        # Use repr() for non-string values (like None) to display them properly,
        # but keep string values unquoted for consistency with existing error messages
        allowed_values_str = ", ".join(
            repr(v) if not isinstance(v, str) else v for v in CONFIG_ALLOWED_VALUES[key]
        )
        exception = ValueError(
            f"Invalid value '{value}' for key '{key}'. Allowed values: {allowed_values_str}."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception
    _verify_max_partition_bytes_config_value(key, value)


def _verify_max_partition_bytes_config_value(key: str, value: Any) -> None:
    """Reject unparseable ``spark.sql.files.maxPartitionBytes`` before persisting."""
    if key != "spark.sql.files.maxPartitionBytes":
        return
    if value is None or str(value).strip() == "":
        return
    try:
        spark_max_partition_bytes_to_target_file_size(value)
    except ValueError as parse_error:
        exception = ValueError(
            f"Invalid value '{value}' for "
            f"'spark.sql.files.maxPartitionBytes': {parse_error}"
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception


def _verify_is_not_readonly_config(key):
    if key in global_config.readonly_config_list:
        exception = ValueError(
            f"Config with key {key} is read-only and cannot be modified."
        )
        attach_custom_error_code(exception, ErrorCodes.CONFIG_CHANGE_NOT_ALLOWED)
        raise exception


# Timezone IDs may only contain characters used by IANA region IDs
# (e.g. "America/Los_Angeles"), fixed offsets ("+05:30", "-08:00") and
# the "UTC"/"GMT" forms. This deliberately excludes quotes, whitespace,
# parentheses and semicolons so a config value can never break out of the
# string literal it is spliced into when generating Java UDF source.
_VALID_TIMEZONE_RE = re.compile(r"[A-Za-z0-9/_+:.-]+")


def validate_session_timezone(timezone_id: str) -> str:
    """
    Validate a ``spark.sql.session.timeZone`` value before it is embedded into
    generated Java source. The value reaches us unvalidated via the Config RPC,
    so an unchecked value such as ``UTC"; Runtime.exec("id");//`` would inject
    arbitrary Java when spliced into a UDF/UDAF body.

    Args:
        timezone_id: The configured timezone string.

    Returns:
        The validated timezone string, unchanged.

    Raises:
        ValueError: If the value contains characters outside the set permitted
            for timezone identifiers.
    """
    # fullmatch (not match + ``$``) so a trailing newline cannot slip a value
    # such as "UTC\n<java>" past the check and inject a new line of source.
    if not _VALID_TIMEZONE_RE.fullmatch(timezone_id):
        exception = ValueError(
            f"Invalid spark.sql.session.timeZone value: {timezone_id!r}. "
            "Timezone must be an IANA region ID (e.g. 'America/Los_Angeles') "
            "or a fixed offset (e.g. '+05:30')."
        )
        attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
        raise exception
    return timezone_id


def set_jvm_timezone(timezone_id: str):
    """
    Set JVM default timezone at runtime (after JVM startup).

    Args:
        timezone_id: Timezone ID like 'America/New_York', 'UTC', 'Europe/London'

    Returns:
        bool: True if successfully set

    Raises:
        RuntimeError: If JVM is not started
    """
    if not jpype.isJVMStarted():
        exception = RuntimeError("JVM must be started before setting timezone")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    try:
        with get_jpype_jclass_lock():
            TimeZone = jpype.JClass("java.util.TimeZone")
        new_timezone = TimeZone.getTimeZone(timezone_id)
        TimeZone.setDefault(new_timezone)

        logger.debug(f"JVM timezone changed to: {new_timezone.getID()}")
    except Exception as e:
        logger.error(f"Failed to set JVM timezone: {e}")


def reset_jvm_timezone_to_system_default():
    """Reset JVM timezone to the system's default timezone"""
    if not jpype.isJVMStarted():
        exception = RuntimeError("JVM must be started first")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception

    try:
        TimeZone = jpype.JClass("java.util.TimeZone")
        TimeZone.setDefault(None)
        logger.debug(
            f"Reset JVM timezone to system default: {TimeZone.getDefault().getID()}"
        )
    except jpype.JException as e:
        exception = RuntimeError(f"Java exception while resetting timezone: {e}")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception
    except Exception as e:
        exception = RuntimeError(f"Unexpected error resetting JVM timezone: {e}")
        attach_custom_error_code(exception, ErrorCodes.INTERNAL_ERROR)
        raise exception


def set_snowflake_parameters(
    key: str, value: Any, snowpark_session: snowpark.Session
) -> None:
    match key:
        case "spark.sql.session.timeZone":
            if value:
                snowpark_session.sql(
                    f"ALTER SESSION SET TIMEZONE = '{value}'"
                ).collect()
            else:
                snowpark_session.sql("ALTER SESSION UNSET TIMEZONE").collect()
        case "spark.sql.globalTempDatabase":
            if not value:
                value = global_config.default_static_global_config.get(key)

            snowpark_name = quote_name_without_upper_casing(value)
            if not global_config.spark_sql_caseSensitive:
                snowpark_name = snowpark_name.upper()

            # Create the schema on demand. Before creating it, however,
            # check if it already exists, to handle the case where the schema exists
            # but the user does not have permissions to execute `CREATE SCHEMA`.
            try:
                snowpark_session.sql(
                    "DESC SCHEMA identifier(?)", [snowpark_name]
                ).collect()
            except SnowparkSQLException:
                db = snowpark_session.get_current_database()
                prev_schema = snowpark_session.get_current_schema()
                # Even though we checked that the schema doesn't exist,
                # use "IF NOT EXISTS" to avoid race conditions.
                snowpark_session.sql(
                    "CREATE SCHEMA IF NOT EXISTS identifier(?)", [snowpark_name]
                ).collect()
                # When schema is created, it is also changed in the context of the session
                match (prev_schema, snowpark_session.get_current_schema()):
                    case (None, curr) if curr is not None:
                        # session.use_schema(None) is not allowed.
                        # Instead, we call `use_database` which will set schema in context to the default one.
                        snowpark_session.use_database(db)
                    case (prev, curr) if prev != curr:
                        snowpark_session.use_schema(prev)
        case "snowpark.connect.cte.optimization_enabled":
            # Set CTE optimization on the snowpark session
            # If value is None (unset/default), restore to snowpark-connect server parameter default
            # If explicitly set to true/false, use user's choice
            if value is None:
                # Restore to snowpark-connect default based on SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION
                cte_enabled = is_cte_optimization_enabled_for_connect_version(
                    snowpark_session
                )
                snowpark_session.cte_optimization_enabled = cte_enabled
                logger.debug(
                    f"Restored snowpark session CTE optimization to server default: {cte_enabled}"
                )
            else:
                cte_enabled = str_to_bool(value)
                snowpark_session.cte_optimization_enabled = cte_enabled
                logger.debug(
                    f"Updated snowpark session CTE optimization (user override): {cte_enabled}"
                )
        case "snowpark.connect.structured_types.fix":
            # TODO: SNOW-2367714 Remove this once the fix is automatically enabled in Snowpark
            snowpark.context._enable_fix_2360274 = str_to_bool(value)
            logger.debug(f"Updated snowpark session structured types fix: {value}")
        case "spark.sql.parquet.outputTimestampType":
            if value == "TIMESTAMP_MICROS":
                snowpark_session.sql(
                    "ALTER SESSION SET UNLOAD_PARQUET_TIME_TIMESTAMP_MILLIS = false"
                ).collect()
            else:
                # Default: TIMESTAMP_MILLIS (or any other value)
                snowpark_session.sql(
                    "ALTER SESSION SET UNLOAD_PARQUET_TIME_TIMESTAMP_MILLIS = true"
                ).collect()
            logger.debug(f"Updated parquet timestamp output type to: {value}")
        case "snowpark.connect.scala.version":
            # force java udf helper recreation
            set_java_udf_creator_initialized_state(False)
        case "snowpark.connect.integralTypesEmulation":
            # "client_default" - don't change, let set_spark_version handle it
            # "enabled" / "disabled" - explicitly set
            if value.lower() == "enabled":
                set_integral_types_conversion(True)
            elif value.lower() == "disabled":
                set_integral_types_conversion(False)
        case "snowpark.connect.large_query_breakdown.enabled":
            if value is None or value == "":
                from snowflake.snowpark.session import (
                    _PYTHON_SNOWPARK_USE_LARGE_QUERY_BREAKDOWN_OPTIMIZATION_VERSION,
                )

                enabled = snowpark_session.is_feature_enabled_for_version(
                    _PYTHON_SNOWPARK_USE_LARGE_QUERY_BREAKDOWN_OPTIMIZATION_VERSION
                )
                snowpark_session.large_query_breakdown_enabled = enabled
                logger.debug(
                    f"Restored large query breakdown enabled to server default: {enabled}"
                )
            else:
                enabled = str_to_bool(value)
                snowpark_session.large_query_breakdown_enabled = enabled
                logger.debug(f"Updated large query breakdown enabled: {enabled}")
        case "snowpark.connect.large_query_breakdown.complexity_lower_bound":
            _set_large_query_breakdown_bound(
                snowpark_session, key, value, bound_index=0
            )
        case "snowpark.connect.large_query_breakdown.complexity_upper_bound":
            _set_large_query_breakdown_bound(
                snowpark_session, key, value, bound_index=1
            )
        case "spark.sql.files.maxPartitionBytes":
            # Validated in ``set_config_param`` via
            # ``_verify_max_partition_bytes_config_value`` before the value is
            # persisted; nothing to do here on the unset path.
            pass
        case _:
            pass


def _set_large_query_breakdown_bound(
    snowpark_session: snowpark.Session,
    key: str,
    value: Any,
    bound_index: int,
) -> None:
    """Update one side of the large query breakdown complexity bounds.

    Args:
        bound_index: 0 for lower bound, 1 for upper bound.
    """
    from snowflake.snowpark.session import (
        DEFAULT_COMPLEXITY_SCORE_LOWER_BOUND,
        DEFAULT_COMPLEXITY_SCORE_UPPER_BOUND,
    )

    defaults = (
        DEFAULT_COMPLEXITY_SCORE_LOWER_BOUND,
        DEFAULT_COMPLEXITY_SCORE_UPPER_BOUND,
    )

    if value is not None and value != "":
        try:
            int_value = int(value)
        except (ValueError, TypeError):
            exception = ValueError(
                f"Invalid value '{value}' for '{key}'. Expected an integer."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
            raise exception
    else:
        int_value = None

    with snowpark_session._lock:
        current_bounds = snowpark_session.large_query_breakdown_complexity_bounds
        bounds_list = list(current_bounds)
        bounds_list[bound_index] = (
            int_value if int_value is not None else defaults[bound_index]
        )
        new_bounds = tuple(bounds_list)
        try:
            snowpark_session.large_query_breakdown_complexity_bounds = new_bounds
        except ValueError:
            other = "upper" if bound_index == 0 else "lower"
            exception = ValueError(
                f"Lower bound ({new_bounds[0]}) must be less than "
                f"upper bound ({new_bounds[1]}). "
                f"Adjust the {other} bound first if needed."
            )
            attach_custom_error_code(exception, ErrorCodes.INVALID_CONFIG_VALUE)
            raise exception

    logger.debug(f"Updated large query breakdown complexity bounds: {new_bounds}")


def get_boolean_session_config_param(name: str) -> bool:
    session_config = sessions_config[get_spark_session_id()]
    return str_to_bool(session_config[name])


def get_string_session_config_param(name: str) -> str:
    session_config = sessions_config[get_spark_session_id()]
    return str(session_config[name])


def get_return_dml_metadata_enabled() -> bool:
    return get_boolean_session_config_param("snowpark.connect.sql.returnDmlMetadata")


def is_add_debug_info_to_query_tag_enabled() -> bool:
    return global_config.snowpark_connect_addDebugInfoToQueryTag


def is_cte_optimization_enabled_for_connect_version(
    snowpark_session: snowpark.Session,
) -> bool:
    """Whether CTE optimization is enabled per Snowpark Connect server parameter.

    Same idea as ``Session.is_feature_enabled_for_version`` in snowpark-python: the
    session parameter is a *minimum* Snowpark Connect version. CTE is enabled when::

        snowpark_connect_version >= SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION

    Example: parameter ``1.20.0`` enables CTE only for Connect 1.20.0 and newer;
    a 1.17.0 client evaluates to False. To enable CTE for 1.17.0, set the
    parameter to ``1.17.0`` (or lower), or upgrade the client.

    Non-string, empty, or unparseable version values are treated as disabled.
    """
    raw = snowpark_session._conn._get_client_side_session_parameter(
        SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION, ""
    )
    connect_ver = ".".join(map(str, sas_version))
    if not isinstance(raw, str) or raw == "":
        return False
    try:
        return parse_version(connect_ver) >= parse_version(raw)
    except InvalidVersion:
        logger.debug(
            "Ignoring invalid %s value %r (not a valid version string); "
            "CTE optimization off",
            SNOWPARK_CONNECT_USE_CTE_OPTIMIZATION_VERSION,
            raw,
        )
        return False


def get_cte_optimization_enabled() -> bool | None:
    """Get the CTE optimization configuration setting.

    Returns:
        True/False if explicitly set by user, None if not set (defer to snowpark-connect server default).
    """
    session_config = sessions_config[get_spark_session_id()]
    value = session_config["snowpark.connect.cte.optimization_enabled"]
    if value is None:
        return None  # Not explicitly set, defer to snowpark's server-side parameter
    return str_to_bool(value)


def get_success_file_generation_enabled() -> bool:
    """Get the _SUCCESS file generation configuration setting."""
    return get_boolean_session_config_param(
        "mapreduce.fileoutputcommitter.marksuccessfuljobs"
    )


def get_parquet_metadata_generation_enabled() -> bool:
    """
    Get the Parquet metadata file generation configuration setting.
    """
    return get_boolean_session_config_param(
        "spark.sql.parquet.enable.summary-metadata"
    ) or get_boolean_session_config_param("parquet.enable.summary-metadata")


def get_describe_cache_ttl_seconds() -> int:
    """Get the describe query cache TTL from session config, with a default fallback."""
    session_config: SessionConfig = sessions_config[get_spark_session_id()]
    default_ttl: str = SessionConfig.default_session_config[
        "snowpark.connect.describe_cache_ttl_seconds"
    ]
    try:
        ttl_str = session_config.get(
            "snowpark.connect.describe_cache_ttl_seconds", default_ttl
        )
        return int(ttl_str)
    except ValueError:  # fallback to default ttl
        return int(default_ttl)


def should_create_temporary_view_in_snowflake() -> bool:
    return str_to_bool(
        global_config["snowpark.connect.temporary.views.create_in_snowflake"]
    )


def is_force_create_sproc_enabled() -> bool:
    """
    Check if the test flag for forcing SPROC creation is enabled.

    This is a test-only configuration that forces UDFs/UDTFs to be created
    in stored procedures regardless of Python version compatibility.
    This helps test SPROC code paths in local CI.
    """
    return str_to_bool(
        global_config.get("snowpark.connect.test.force_create_sproc", "false")
    )


def external_table_location() -> Optional[str]:
    session_config = sessions_config[get_spark_session_id()]
    return session_config.get(
        "snowpark.connect.sql.partition.external_table_location", None
    )


def parse_imports(
    session: snowpark.Session, imports: str | None, language: str
) -> None:
    if not imports:
        return

    # UDF needs to be recreated to include new imports
    clear_spark_session_cache(get_spark_session_id())
    if language == "java":

        set_java_udf_creator_initialized_state(False)

    for udf_import in imports.strip("[] ").split(","):
        udf_import = udf_import.strip()
        if udf_import:
            session.add_import(udf_import)


def get_timestamp_type():
    match global_config["spark.sql.timestampType"]:
        case "TIMESTAMP_LTZ":
            timestamp_type = TimestampType(TimestampTimeZone.LTZ)
        case "TIMESTAMP_NTZ":
            timestamp_type = TimestampType(TimestampTimeZone.NTZ)
        case _:
            # shouldn't happen since `spark.sql.timestampType` is always defined, and `spark.conf.unset` sets it to default (TIMESTAMP_LTZ)
            timestamp_type = TimestampType(TimestampTimeZone.LTZ)
    return timestamp_type


def record_table_metadata(
    table_identifier: str,
    table_type: str,
    data_source: str,
    supports_column_rename: bool = True,
) -> None:
    """
    Record metadata about a table for Spark compatibility checks.

    Args:
        table_identifier: Full table identifier (catalog.database.table)
        table_type: "v1" or "v2"
        data_source: Source format (parquet, csv, iceberg, etc.)
        supports_column_rename: Whether the table supports RENAME COLUMN
    """
    session_id = get_spark_session_id()
    session_config = sessions_config[session_id]

    # Normalize table identifier for consistent lookup
    # Use the full catalog.database.table identifier to avoid conflicts
    normalized_identifier = table_identifier.upper().strip('"')

    session_config.table_metadata[normalized_identifier] = {
        "table_type": table_type,
        "data_source": data_source,
        "supports_column_rename": supports_column_rename,
    }


def get_table_metadata(table_identifier: str) -> Dict[str, Any] | None:
    """
    Get stored metadata for a table.

    Args:
        table_identifier: Full table identifier (catalog.database.table)

    Returns:
        Table metadata dict or None if not found
    """
    session_id = get_spark_session_id()
    session_config = sessions_config[session_id]

    normalized_identifier = unquote_if_quoted(table_identifier).upper()

    return session_config.table_metadata.get(normalized_identifier)


def check_table_supports_operation(table_identifier: str, operation: str) -> bool:
    """
    Check if a table supports a given operation based on metadata and config.

    Args:
        table_identifier: Full table identifier (catalog.database.table)
        operation: Operation to check (e.g., "rename_column")

    Returns:
        True if operation is supported, False if should be blocked
    """
    table_metadata = get_table_metadata(table_identifier)

    if not table_metadata:
        return True

    session_id = get_spark_session_id()
    session_config = sessions_config[session_id]
    enable_extensions = str_to_bool(
        session_config.get(
            "snowpark.connect.enable_snowflake_extension_behavior", "false"
        )
    )

    if enable_extensions:
        return True

    if operation == "rename_column":
        return table_metadata.get("supports_column_rename", True)

    return True


def get_scala_version() -> str:
    return global_config.get("snowpark.connect.scala.version")


def get_artifact_repository() -> Optional[str]:
    """
    Get the artifact repository to use for UDF/UDTF/UDAF/Sproc package resolution.

    Returns:
        The artifact repository name, or None if not configured.

    Example usage via spark.conf.set():
        spark.conf.set("snowpark.connect.artifact_repository", "MY_PYPI_REPO")
    """
    repo = global_config.get("snowpark.connect.artifact_repository", "")
    return repo if repo else None


_java_udf_creator_initialized = False


def is_java_udf_creator_initialized() -> bool:
    global _java_udf_creator_initialized
    return _java_udf_creator_initialized


def set_java_udf_creator_initialized_state(value: bool) -> None:
    global _java_udf_creator_initialized
    _java_udf_creator_initialized = value


def is_column_nullability_tracking_enabled() -> bool:
    return str_to_bool(
        global_config.get("snowpark.connect.nullability.trackColumns", "false")
    )


def is_complex_type_nullability_enabled() -> bool:
    return str_to_bool(
        global_config.get("snowpark.connect.nullability.trackComplexTypes", "false")
    )


def is_dynamic_partition_overwrite_enabled() -> bool:
    return (
        get_string_session_config_param(
            "spark.sql.sources.partitionOverwriteMode"
        ).lower()
        == "dynamic"
    )


def emulate_partition_overwrite_for_fdn_tables() -> bool:
    session_id = get_spark_session_id()
    session_config = sessions_config[session_id]
    return str_to_bool(
        session_config.get(
            "snowpark.connect.sql.emulatePartitionOverwritesForSnowflakeTables", "false"
        )
    )


def is_anchor_stage_paths_enabled() -> bool:
    """
    Whether SCOS anchors stage read paths to defeat Snowflake's prefix
    matching (SNOW-3428536).

    When true (the default), file and glob source paths are translated to a
    Snowflake ``PATTERN``/trailing-slash combination so a read of
    ``@stage/dir/data.json`` does not also pull in ``data.json.gz`` or
    ``@stage/dir_v2/...`` siblings. Disable to revert to legacy behavior if
    a workload relies on the accidental sibling-bleed.
    """
    return get_boolean_session_config_param("snowpark.connect.read.anchorStagePaths")


def is_hive_partition_pruning_enabled() -> bool:
    """Whether static Hive partition predicates are pushed into stage listing."""
    return get_boolean_session_config_param(
        "snowpark.connect.read.hivePartitionPruning"
    )


def get_iceberg_target_file_size_for_writes() -> str | None:
    """Return a session-scoped ``TARGET_FILE_SIZE`` derived from Spark's
    ``spark.sql.files.maxPartitionBytes``, if the user has set it.

    Snowflake's ``TARGET_FILE_SIZE`` parameter is only settable at
    ACCOUNT/SCHEMA/TABLE level (not SESSION), so we cannot translate the Spark
    knob via ``ALTER SESSION``. Instead, the Iceberg write path
    (``_build_iceberg_config``) consults this helper to choose a default
    bucketed value to inject into the ``CREATE ICEBERG TABLE`` DDL. An
    explicit ``tableProperty("write.target-file-size", ...)`` always wins.

    Returns ``None`` when the user has not set ``spark.sql.files.maxPartitionBytes``
    or the stored value can no longer be parsed (we never raise from the
    write path; an invalid value is rejected eagerly at ``conf.set`` time by
    ``set_snowflake_parameters``).
    """
    session_config = sessions_config[get_spark_session_id()]
    raw = session_config.get("spark.sql.files.maxPartitionBytes")
    if raw == "":
        return None
    try:
        return spark_max_partition_bytes_to_target_file_size(raw)
    except ValueError:
        logger.debug(
            "Ignoring unparseable spark.sql.files.maxPartitionBytes=%r "
            "in get_iceberg_target_file_size_for_writes",
            raw,
        )
        return None
