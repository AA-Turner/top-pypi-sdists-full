from __future__ import annotations

import typing as t

from query_cache_common.decorators import proto_dataclass, proto_enum
from query_cache_common.models.base import BaseSerDeModel, BaseSerDeEnum
from query_cache_protobuf.query_cache import shared_pb2


@proto_enum(shared_pb2.ModelExecutionType)
class ModelExecutionType(BaseSerDeEnum):
    UNSPECIFIED = "UNSPECIFIED"
    FULL = "FULL"
    APPEND = "APPEND"
    MERGE = "MERGE"
    INSERT_OVERWRITE = "INSERT_OVERWRITE"
    DELETE_INSERT = "DELETE_INSERT"
    MICROBATCH = "MICROBATCH"
    SNAPSHOT = "SNAPSHOT"
    DBT_DATA_TEST = "DBT_DATA_TEST"
    VALUES = "VALUES"
    VIEW = "VIEW"
    DBT_CUSTOM = "DBT_CUSTOM"


@proto_dataclass(shared_pb2.TableModifiedInfo)
class TableModifiedInfo(BaseSerDeModel):
    name: str
    last_modified_epoch: int = 0


@proto_dataclass(shared_pb2.QueryDependency)
class QueryDependency(BaseSerDeModel):
    name: str
    query: str
    default_catalog: str
    default_schema: str


@proto_enum(shared_pb2.RejectionReason)
class RejectionReason(BaseSerDeEnum):
    _UNSUPPORTED = "_UNSUPPORTED"

    NO_FINGERPRINT_MATCH = "NO_FINGERPRINT_MATCH"  # Deprecated
    NO_SUITABLE_MATCH_FOUND = "NO_SUITABLE_MATCH_FOUND"
    TARGET_TABLE_MISMATCH = "TARGET_TABLE_MISMATCH"
    TARGET_TABLE_MATCH = "TARGET_TABLE_MATCH"
    EXECUTION_TYPE_MISMATCH = "EXECUTION_TYPE_MISMATCH"
    EXECUTION_TYPE_NOT_FULL = "EXECUTION_TYPE_NOT_FULL"
    TARGET_TABLE_DOES_NOT_EXIST = "TARGET_TABLE_DOES_NOT_EXIST"
    FORCED_NOT_ELIGIBLE = "FORCED_NOT_ELIGIBLE"
    LATEST_QUERY_HASH_NOT_MATCH = "LATEST_QUERY_HASH_NOT_MATCH"
    OUTSIDE_TIME_TRAVEL_WINDOW = "OUTSIDE_TIME_TRAVEL_WINDOW"
    CLONE_CHAIN_LIMIT_EXCEEDED = "CLONE_CHAIN_LIMIT_EXCEEDED"


@proto_enum(shared_pb2.SubmitSQLResultType)
class SubmitSQLResultType(BaseSerDeEnum):
    _UNSUPPORTED = "_UNSUPPORTED"

    SKIP_EXECUTION = "SKIP_EXECUTION"
    READY_TO_EXECUTE = "READY_TO_EXECUTE"
    READY_TO_CLONE = "READY_TO_CLONE"
    UNKNOWN = "UNKNOWN"

    @property
    def label(self) -> str:
        labels = {
            SubmitSQLResultType.READY_TO_EXECUTE: "Execute",
            SubmitSQLResultType.SKIP_EXECUTION: "No-op",
            SubmitSQLResultType.READY_TO_CLONE: "Clone",
            SubmitSQLResultType.UNKNOWN: "Unknown",
        }
        return labels[self]


@proto_enum(shared_pb2.StaleUpstreamPolicy)
class StaleUpstreamPolicy(BaseSerDeEnum):
    ANY = "ANY"
    ALL = "ALL"

    def is_any(self) -> bool:
        return self == StaleUpstreamPolicy.ANY

    def is_all(self) -> bool:
        return self == StaleUpstreamPolicy.ALL


@proto_dataclass(shared_pb2.ExplainedDecision)
class ExplainedDecision(BaseSerDeModel):
    decision: SubmitSQLResultType
    skip_rejection_reason: t.Optional[RejectionReason] = None
    clone_rejection_reason: t.Optional[RejectionReason] = None
    is_stale: bool = False
    decision_description: str = ""

    @staticmethod
    def no_match_explained_decision() -> ExplainedDecision:
        return ExplainedDecision(
            decision=SubmitSQLResultType.READY_TO_EXECUTE,
            skip_rejection_reason=RejectionReason.NO_SUITABLE_MATCH_FOUND,
            clone_rejection_reason=RejectionReason.NO_SUITABLE_MATCH_FOUND,
            is_stale=False,
        )


@proto_dataclass(shared_pb2.DbtNodeState)
class DbtNodeState(BaseSerDeModel):
    node_unique_id: str
    target_name: str
    project_name: str
    resource_type: str
    node_hash: str
    profile_name: str
    node_body_hash: t.Optional[str] = None
    node_configs_hash: t.Optional[str] = None
    node_macros_hash: t.Optional[str] = None
    node_contract_hash: t.Optional[str] = None
    node_persisted_descriptions_hash: t.Optional[str] = None
    project_id: t.Optional[str] = None
    node_database_representation: t.Optional[str] = None
