import json
import re
from collections.abc import AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from urllib.parse import urlencode

from pydantic import TypeAdapter

from arraylake.api_utils import ArraylakeHttpClient, handle_response
from arraylake.compute.types import (
    ComputeConfig,
    DeploymentInfo,
    LoadResults,
    ServiceConfig,
)

# type adapters
LIST_SERVICES_ADAPTER = TypeAdapter(list[DeploymentInfo])
DUMP_CONFIGS_ADAPTER = TypeAdapter(dict[str, list[ServiceConfig]])


_VALID_NAME = r"(\w[\w\.\-_]+)"


def _parse_org_and_repo(org_and_repo: str) -> tuple[str, str]:
    expr = f"{_VALID_NAME}/{_VALID_NAME}"
    res = re.fullmatch(expr, org_and_repo)
    if not res:
        raise ValueError(f"Not a valid repo identifier: `{org_and_repo}`. Should have the form `[ORG]/[REPO]`.")
    org, repo_name = res.groups()
    return org, repo_name


@dataclass
class HttpComputeConfig:
    """Encapsulates the configuration for the HttpComputeClient."""

    api_service_url: str
    org: str
    token: str | None = field(default=None, repr=False)  # machine token. id/access/refresh tokens are managed by CustomOauth


class ComputeHttpClient(ArraylakeHttpClient):
    """Class for interacting with the Arraylake Compute API.

    Connects to the Arraylake over HTTP and provides methods for managing
    compute services.
    """

    _config: HttpComputeConfig

    def __init__(self, config: HttpComputeConfig):
        super().__init__(api_url=config.api_service_url, token=config.token)

        self._config = config
        self.api_url = config.api_service_url

    async def get_compute_config(self) -> ComputeConfig:
        """Get the current Bhavachakra configuration for the Arraylake Compute service."""
        response = await self._request("GET", "/compute/config")
        handle_response(response)
        return ComputeConfig.model_validate_json(response.content)

    async def dump_compute_configs(self) -> dict[str, list[ServiceConfig]]:
        """Dump the service configurations for all namespaces in the Arraylake Compute service."""
        response = await self._request("GET", "/compute/dump")
        handle_response(response)
        return DUMP_CONFIGS_ADAPTER.validate_json(response.content)

    async def load_compute_configs(self, configs: dict[str, list[ServiceConfig]]) -> LoadResults:
        """Batch create service configurations for all namespaces in the Arraylake Compute service."""
        configs_json = json.dumps(configs)
        response = await self._request("POST", "/compute/load", content=configs_json)
        handle_response(response)
        return LoadResults.model_validate_json(response.content)

    async def create_compute_service(self, protocol: str, is_public: bool, **kwargs) -> dict[str, Any]:
        """Creates a new Arraylake compute service."""
        service_config = ServiceConfig(
            service_type=protocol,  # type: ignore
            org=self._config.org,
            is_public=is_public,
            **kwargs,
        )
        response = await self._request("POST", f"/compute/orgs/{self._config.org}/services", content=service_config.model_dump_json())
        handle_response(response)
        return response.json()

    async def list_compute_services(self) -> list[DeploymentInfo]:
        """Lists all of the Arraylake compute services for a given organization."""
        response = await self._request("GET", f"/compute/orgs/{self._config.org}/services")
        handle_response(response)
        return LIST_SERVICES_ADAPTER.validate_json(response.content)

    async def get_compute_service_status(self, name: str) -> dict[str, Any]:
        """Gets the status of an Arraylake compute service."""
        response = await self._request("GET", f"/compute/orgs/{self._config.org}/services/{name}")
        handle_response(response)
        return response.json()

    async def get_compute_service_logs(
        self,
        service_id: str,
        *,
        tail: int | None = None,
        follow: bool = False,
        since: datetime | None = None,
        until: datetime | None = None,
        follow_timeout: int = 30,
    ) -> AsyncGenerator[str, None]:
        """Gets a snapshot of the logs of an Arraylake compute service."""
        try:
            url = f"/compute/orgs/{self._config.org}/services/{service_id}/logs"
            params = {
                "follow_timeout": str(follow_timeout),
            }
            if follow:
                params["follow"] = str(follow)
            if tail:
                params["tail"] = str(tail)
            if since:
                params["since"] = since.isoformat()
            if until:
                params["until"] = until.isoformat()
            if len(params) > 0:
                url = url + "?" + urlencode(params)

            async with await self._stream_request("GET", url) as response:
                async for line in response.aiter_lines():
                    yield line
        except Exception as e:
            raise RuntimeError(f"Error getting logs for {service_id}: {e}") from e

    async def delete_compute_service(self, service_id: str) -> dict[str, Any]:
        """Disables an Arraylake compute service."""
        response = await self._request("DELETE", f"/compute/orgs/{self._config.org}/services/{service_id}")
        handle_response(response)
        return response.json()
