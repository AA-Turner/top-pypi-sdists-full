from enum import Enum
from typing import Dict, List, Optional

import click
from tabulate import tabulate

from montecarlodata.common.data import ConnectionType
from montecarlodata.common.user import UserService
from montecarlodata.config import Config
from montecarlodata.errors import complain_and_abort, manage_errors
from montecarlodata.queries.keys import Queries
from montecarlodata.utils import GqlWrapper


# Should be in sync with monolith IntegrationKeyScope: https://github.com/monte-carlo-data/monolith-django/blob/a6f7fce58b5d6e933655c19823067886a826fe48/monolith/service/dynamo/integration_key.py#L14
# and with saas-serverless AuthScope: https://github.com/monte-carlo-data/saas-serverless/blob/3128eb4eea6e10522b0ac34122dd1c008661c8aa/integration-gateway/gateway/base/auth.py#L19
class IntegrationKeyScope(Enum):
    CircuitBreaker = "circuit_breaker"
    DatabricksMetadata = "databricksmetadata"
    DatabricksWebhook = "databricks_webhook"
    DbtCloudWebhook = "dbt_cloud_webhook"
    S3PresignedUrl = "s3_presigned_url"
    Spark = "spark"
    AirflowCallbacks = "airflowcallbacks"
    Agent = "agent"
    SCIM_v2 = "SCIM_v2"
    AzureDevopsWebhook = "azure_devops_webhook"
    MCP = "mcp"

    @classmethod
    def values(cls) -> List[str]:
        return list(map(lambda s: s.name, cls))


class IntegrationKeyService:
    _table_headers = ["Id", "Description", "Scope", "Created", "Created By"]

    def __init__(
        self,
        config: Config,
        command_name: str,
        gql: Optional[GqlWrapper] = None,
        user_service: Optional[UserService] = None,
    ):
        self._command_name = command_name
        self._gql = gql or GqlWrapper(config, command_name=self._command_name)
        self._user_service = user_service or UserService(
            config=config,
            command_name=self._command_name,
        )

        # used by @manage_errors decorator
        self._abort_on_error = True

    @manage_errors
    def create(
        self,
        description: Optional[str],
        scope: str,
        warehouse_ids: Optional[List[Optional[str]]] = None,
    ):
        response = self._gql.make_request_v2(
            query=Queries.create.query,
            operation=Queries.create.operation,
            service="integration_key_service",
            variables=self._resolve_variables(description, scope, warehouse_ids),
        )

        click.echo(f"Key id: {response.data.key.id}")  # type: ignore
        click.echo(f"Key secret: {response.data.key.secret}")  # type: ignore

    def _resolve_variables(
        self,
        description: Optional[str],
        scope: str,
        warehouse_ids: Optional[List[Optional[str]]] = None,
    ) -> Dict:
        variables = {"description": description, "scope": scope}

        if scope.lower() == IntegrationKeyScope.Spark.value:
            variables["warehouseIds"] = [self._resolve_lake_warehouse_id()]
        elif warehouse_ids:
            variables["warehouseIds"] = warehouse_ids

        return variables

    def _resolve_lake_warehouse_id(self) -> Optional[str]:
        lake_warehouse_ids = [
            w["uuid"]
            for w in self._user_service.warehouses
            if w["connectionType"] == ConnectionType.DataLake.value
        ]

        num_lakes = len(lake_warehouse_ids)
        if num_lakes == 0:
            complain_and_abort("Unable to resolve data lake connection: no lake connection found.")
        elif num_lakes > 1:
            complain_and_abort(
                "Unable to resolve data lake connection: multiple lake connections found."
            )
        else:
            return lake_warehouse_ids[0]

    @manage_errors
    def delete(self, key_id: str):
        response = self._gql.make_request_v2(
            query=Queries.delete.query,
            operation=Queries.delete.operation,
            service="integration_key_service",
            variables={"keyId": key_id},
        )

        if response.data.deleted:  # type: ignore
            click.echo("Key has been deleted.")
        else:
            click.echo("Key was not deleted.")

    @manage_errors
    def get_all(
        self,
        scope: Optional[str] = None,
        resource_uuid: Optional[str] = None,
        table_format: str = "fancy_grid",
    ):
        response = self._gql.make_request_v2(
            query=Queries.get_all.query,
            operation=Queries.get_all.operation,
            service="integration_key_service",
            variables={"scope": scope, "resourceUuid": resource_uuid},
        )

        data = [
            [
                key.id,
                key.description,
                key.scope,
                key.createdTime,
                f"{key.createdBy.firstName} {key.createdBy.lastName}",
            ]
            for key in response.data  # type: ignore
        ]

        table = tabulate(data, headers=self._table_headers, tablefmt=table_format)
        click.echo(table)
