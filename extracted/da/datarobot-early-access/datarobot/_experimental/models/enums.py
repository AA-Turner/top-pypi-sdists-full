#
# Copyright 2021 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from strenum import StrEnum

# pylint: disable=unused-import
from datarobot.enums import (  # noqa: F401
    ListChatsSortQueryParams,
    ListComparisonChatsSortQueryParams,
    ListCustomModelValidationsSortQueryParams,
    ListLLMBlueprintsSortQueryParams,
    ListPlaygroundsSortQueryParams,
    ListVectorDatabasesSortQueryParams,
    ModerationGuardAction,
    ModerationGuardConditionOperator,
    NemoLLMType,
    PromptType,
    VectorDatabaseChunkingParameterType,
    VectorDatabaseDatasetLanguages,
    VectorDatabaseEmbeddingModel,
    VectorDatabaseExecutionStatus,
    VectorDatabaseSource,
)

# pylint: enable=unused-import


class VectorDatabaseChunkingMethod(StrEnum):
    """Text chunking method names for VectorDatabases."""

    RECURSIVE = "recursive"
    SEMANTIC = "semantic"


class StorageType(StrEnum):
    """Supported data storages."""

    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    AI_CATALOG = "aicatalog"
    DATASTAGE = "datastage"


class OriginStorageType(StrEnum):
    """Supported data sources."""

    SNOWFLAKE = StorageType.SNOWFLAKE
    BIGQUERY = StorageType.BIGQUERY
    DATABRICKS = StorageType.DATABRICKS
    AI_CATALOG = StorageType.AI_CATALOG


class ChunkingType(StrEnum):
    """Supported chunking types."""

    INCREMENTAL_LEARNING = "incrementalLearning"
    INCREMENTAL_LEARNING_OTV = "incrementalLearningOtv"
    SLICED_OFFSET_LIMIT = "slicedOffsetLimit"


class ChunkStorageType(StrEnum):
    """Supported chunk storage."""

    DATASTAGE = StorageType.DATASTAGE
    AI_CATALOG = StorageType.AI_CATALOG


class ChunkServiceDialect(StrEnum):
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DATABRICKS = "databricks"
    SPARK = "spark"
    POSTGRES = "postgres"


class ChunkingStrategy(StrEnum):
    FEATURES = "features"
    ROWS = "rows"


class ChunkingPartitionMethod(StrEnum):
    RANDOM = "random"
    STRATIFIED = "stratified"
    DATE = "date"


class FeedbackSentiment(StrEnum):
    POSITIVE = "1"
    NEGATIVE = "0"


class GuardConditionComparator(StrEnum):
    """The comparator used in a guard condition."""

    GREATER_THAN = "greaterThan"
    LESS_THAN = "lessThan"
    EQUALS = "equals"
    NOT_EQUALS = "notEquals"
    IS = "is"
    IS_NOT = "isNot"
    MATCHES = "matches"
    DOES_NOT_MATCH = "doesNotMatch"
    CONTAINS = "contains"
    DOES_NOT_CONTAIN = "doesNotContain"


class AggregationType(StrEnum):
    """The type of the metric aggregation."""

    AVERAGE = "average"
    BINARY_PERCENTAGE = "percentYes"
    MULTICLASS_PERCENTAGE = "classPercentCoverage"
    NGRAM_IMPORTANCE = "ngramImportance"
    GUARD_CONDITION_PERCENTAGE = "guardConditionPercentYes"


class GuardType(StrEnum):
    """The type of the guard configuration used for moderation in production."""

    MODEL = "guardModel"
    NEMO = "nemo"  # NVidia NeMo
    OOTB = "ootb"  # 'Out of the box' metric, little or no configuration
    PII = "pii"
    USER_MODEL = "userModel"  # user-defined columns and target type


class VectorDatabaseRetrievers(StrEnum):
    """Vector database retriever names."""

    SINGLE_LOOKUP_RETRIEVER = "SINGLE_LOOKUP_RETRIEVER"
    CONVERSATIONAL_RETRIEVER = "CONVERSATIONAL_RETRIEVER"
    MULTI_STEP_RETRIEVER = "MULTI_STEP_RETRIEVER"


class LLMTestConfigurationType(StrEnum):
    """Supported LLM test configuration types."""

    CUSTOM = "custom"
    OOTB = "ootb"


class GradingResult(StrEnum):
    """Supported LLM test grading results."""

    PASS = "PASS"
    FAIL = "FAIL"


class PromptSamplingStrategy(StrEnum):
    """The prompt sampling strategy for the evaluation dataset configuration."""

    RANDOM_WITHOUT_REPLACEMENT = "random_without_replacement"
    FIRST_N_ROWS = "first_n_rows"
