from __future__ import annotations

import dataclasses
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Dict, List, Optional

from chalk._gen.chalk.server.v1.integrations_pb2 import (
    DeleteIntegrationRequest,
    GetIntegrationRequest,
    InsertIntegrationRequest,
)
from chalk._gen.chalk.server.v1.integrations_pb2 import Integration as IntegrationProto
from chalk._gen.chalk.server.v1.integrations_pb2 import IntegrationConfigValue
from chalk._gen.chalk.server.v1.integrations_pb2 import IntegrationKind as IntegrationKindProto
from chalk._gen.chalk.server.v1.integrations_pb2 import (
    ListIntegrationsRequest,
    TestIntegrationRequest,
    UpdateIntegrationRequest,
)

if TYPE_CHECKING:
    from chalk.client.client_grpc import StubRefresher


class IntegrationKind(str, Enum):
    ATHENA = "ATHENA"
    BIGQUERY = "BIGQUERY"
    CLICKHOUSE = "CLICKHOUSE"
    DATABRICKS = "DATABRICKS"
    DYNAMODB = "DYNAMODB"
    KAFKA = "KAFKA"
    KINESIS = "KINESIS"
    MSSQL = "MSSQL"
    MYSQL = "MYSQL"
    POSTGRESQL = "POSTGRESQL"
    PUBSUB = "PUBSUB"
    REDSHIFT = "REDSHIFT"
    SNOWFLAKE = "SNOWFLAKE"
    SPANNER = "SPANNER"
    TRINO = "TRINO"


# Map from IntegrationKind -> proto enum name
_KIND_TO_PROTO: Dict[IntegrationKind, str] = {kind: f"INTEGRATION_KIND_{kind.value}" for kind in IntegrationKind}

# Map from proto enum name -> IntegrationKind
_PROTO_TO_KIND: Dict[str, IntegrationKind] = {v: k for k, v in _KIND_TO_PROTO.items()}


def _resolve_integration_kind(kind: str | IntegrationKind) -> str:
    if isinstance(kind, IntegrationKind):
        return _KIND_TO_PROTO[kind]
    normalized = kind.upper().strip()
    try:
        return _KIND_TO_PROTO[IntegrationKind(normalized)]
    except ValueError:
        valid_kinds = ", ".join(sorted(k.value.lower() for k in IntegrationKind))
        raise ValueError(f"Unknown integration kind: {kind!r}. Valid kinds: {valid_kinds}")


def _proto_kind_to_integration_kind(kind: int) -> IntegrationKind:
    name = IntegrationKindProto.Name(kind)
    ik = _PROTO_TO_KIND.get(name)
    if ik is not None:
        return ik
    raise ValueError(f"Unknown proto integration kind: {name}")


@dataclasses.dataclass(frozen=True)
class Datasource:
    id: str
    name: str
    kind: IntegrationKind
    environment_id: str
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_proto(proto: IntegrationProto) -> Datasource:
        return Datasource(
            id=proto.id,
            name=proto.name,
            kind=_proto_kind_to_integration_kind(proto.kind),
            environment_id=proto.environment_id,
            created_at=proto.created_at.ToDatetime(tzinfo=timezone.utc),
            updated_at=proto.updated_at.ToDatetime(tzinfo=timezone.utc),
        )


@dataclasses.dataclass(frozen=True)
class DatasourceTestResult:
    success: bool
    message: str
    latency_seconds: float


def _build_config_map(config: Dict[str, str]) -> Dict[str, IntegrationConfigValue]:
    return {k: IntegrationConfigValue(literal=v) for k, v in config.items()}


class DatasourceAPI:
    def __init__(self, stub_refresher: "StubRefresher"):
        super().__init__()
        self._stub_refresher = stub_refresher

    def list(self) -> List[Datasource]:
        """List all data sources in the current environment."""
        resp = self._stub_refresher.call_integrations_stub(
            lambda stub: stub.ListIntegrations(ListIntegrationsRequest())
        )
        return [Datasource.from_proto(i) for i in resp.integrations]

    def get(self, id: str) -> Datasource:
        """Get a data source by ID.

        Parameters
        ----------
        id
            The integration ID.
        """
        resp = self._stub_refresher.call_integrations_stub(
            lambda stub: stub.GetIntegration(GetIntegrationRequest(integration_id=id))
        )
        return Datasource.from_proto(resp.integration_with_secrets.integration)

    def create(
        self,
        kind: str | IntegrationKind,
        name: str,
        config: Dict[str, str],
    ) -> Datasource:
        """Create a new data source.

        Parameters
        ----------
        kind
            The type of data source. Can be an ``IntegrationKind`` enum or a string
            (e.g. ``"snowflake"``, ``"postgresql"``, ``"bigquery"``, ``"kafka"``).
        name
            A name for this data source integration. Must only contain letters,
            numbers, and underscores.
        config
            A dictionary of configuration values. Keys and values are strings.
            For example, for BigQuery: ``{"BQ_PROJECT": "my-project",
            "BQ_DATASET": "my_dataset", "BQ_CREDENTIALS_BASE64": "..."}``.
        """
        req = InsertIntegrationRequest(
            name=name,
            integration_kind=_resolve_integration_kind(kind),
            config=_build_config_map(config),
        )
        resp = self._stub_refresher.call_integrations_stub(lambda stub: stub.InsertIntegration(req))
        return Datasource.from_proto(resp.integration)

    def update(
        self,
        id: str,
        config: Optional[Dict[str, str]] = None,
        name: Optional[str] = None,
    ) -> Datasource:
        """Update an existing data source.

        Parameters
        ----------
        id
            The integration ID to update.
        config
            Updated configuration values. Only provided keys are updated.
        name
            Optionally update the integration name.
        """
        req = UpdateIntegrationRequest(integration_id=id)
        if name is not None:
            req.name = name
        if config is not None:
            for k, v in _build_config_map(config).items():
                req.config[k].CopyFrom(v)
        resp = self._stub_refresher.call_integrations_stub(lambda stub: stub.UpdateIntegration(req))
        return Datasource.from_proto(resp.integration)

    def delete(self, id: str) -> None:
        """Delete a data source.

        Parameters
        ----------
        id
            The integration ID to delete.
        """
        self._stub_refresher.call_integrations_stub(
            lambda stub: stub.DeleteIntegration(DeleteIntegrationRequest(id=id))
        )

    def test(self, id: str) -> DatasourceTestResult:
        """Test connectivity of an existing data source.

        Parameters
        ----------
        id
            The integration ID to test.
        """
        resp = self._stub_refresher.call_integrations_stub(
            lambda stub: stub.TestIntegration(TestIntegrationRequest(integration_id=id))
        )
        return DatasourceTestResult(
            success=resp.success,
            message=resp.message,
            latency_seconds=resp.latency_seconds,
        )
