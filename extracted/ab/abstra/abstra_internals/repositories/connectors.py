import abc
from dataclasses import dataclass
from typing import Any, List

from abstra_internals.cloud_api.http_client import HTTPClient
from abstra_internals.contracts_generated import (
    CloudApiCliConnectorsConnectionsResponseItem,
    CloudApiCliConnectorsExecuteRequest,
    CloudApiCliConnectorsGetActionResponse,
    CloudApiCliConnectorsSearchActionsResponse,
)


@dataclass
class AccessTokenDTO:
    connectionName: str
    connectorType: str
    projectId: str
    token: str
    expiresAt: str


class ConnectorsRepository(abc.ABC):
    def __init__(self, client: "HTTPClient") -> None:
        self.client = client

    def get_access_token(self, connection_name: str) -> AccessTokenDTO:
        response = self.client.get(
            endpoint=f"connectors/connection/{connection_name}/access-token",
        )
        response.raise_for_status()
        return AccessTokenDTO(**response.json())

    def run_connection_action(
        self, connection_name: str, action: str, payload: dict = {}
    ) -> Any:
        response = self.client.post(
            endpoint=f"connectors/connection/{connection_name}/execute",
            json=CloudApiCliConnectorsExecuteRequest(
                connection_name=connection_name, action_name=action, parameters=payload
            ).to_dict(),
        )
        result = response.raise_for_status()
        result = response.json()
        if result["status"] == "error":
            raise Exception(result["message"])

        return result.get("data")

    def list_connections(self) -> List[CloudApiCliConnectorsConnectionsResponseItem]:
        response = self.client.get(endpoint="connectors/connections")
        response.raise_for_status()
        return [
            CloudApiCliConnectorsConnectionsResponseItem.from_dict(item)
            for item in response.json()
        ]

    def search_connection_actions(
        self,
        connection_name: str,
        search: str = "",
        page: int = 0,
        page_size: int = 100,
    ) -> CloudApiCliConnectorsSearchActionsResponse:
        response = self.client.get(
            endpoint=f"connectors/connection/{connection_name}/actions",
            params={"search": search, "page": page, "pageSize": page_size},
        )
        response.raise_for_status()
        return CloudApiCliConnectorsSearchActionsResponse.from_dict(response.json())

    def get_connection_action_details(
        self, connection_name: str, action_name: str
    ) -> CloudApiCliConnectorsGetActionResponse:
        response = self.client.get(
            endpoint=f"connectors/connection/{connection_name}/action/{action_name}",
        )
        response.raise_for_status()
        return CloudApiCliConnectorsGetActionResponse.from_dict(response.json())
