import typing as t

from query_cache_common.models.services import (
    client_telemetry_service_models,
    sql_service_models,
    clone_service_models,
)
from dbt.contracts.graph.nodes import (
    GenericTestNode,
    ModelNode,
    SnapshotNode,
    SingularTestNode,
    SeedNode,
)


SQLSubmitResponse = t.Union[
    sql_service_models.ReadyToExecuteResponse,
    sql_service_models.SkipExecutionResponse,
    clone_service_models.ReadyToCloneResponse,
]

SpeculativeSubmitResponse = t.Union[
    sql_service_models.ReadyToExecuteUntrackedResponse,
    sql_service_models.SkipExecutionResponse,
    clone_service_models.ReadyToCloneResponse,
    sql_service_models.UndecidedResponse,
]


ModelOrSnapshotNode = t.Union[ModelNode, SnapshotNode]
ModelOrSnapshotOrTestNode = t.Union[ModelNode, SnapshotNode, GenericTestNode, SingularTestNode]
ModelOrSnapshotOrSeedNode = t.Union[ModelNode, SnapshotNode, SeedNode]
ModelOrSnapshotOrTestOrSeedNode = t.Union[
    ModelNode, SnapshotNode, GenericTestNode, SingularTestNode, SeedNode
]

ClientEvent = t.Union[
    client_telemetry_service_models.SessionStartRequest,
    client_telemetry_service_models.ClientPrepareEnrichedSQLRequest,
    client_telemetry_service_models.SessionEndRequest,
]
