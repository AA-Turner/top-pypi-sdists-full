# Copyright (c) Fireworks AI, Inc. and affiliates.
#
# All Rights Reserved.

from datetime import timedelta
import functools
import os
from typing import List, Optional, TypeVar

from grpclib.client import Channel
import httpx
from betterproto.lib.std.google.protobuf import FieldMask
from fireworks._util import async_lru_cache
from fireworks.control_plane.generated.protos.gateway import (
    AutoscalingPolicy,
    CreateDeploymentRequest,
    Deployment,
    GatewayStub,
    GetDeploymentRequest,
    ListDeploymentsRequest,
    ListModelsRequest,
    ListModelsResponse,
    Model,
    ScaleDeploymentRequest,
    UpdateDeploymentRequest,
)


def _get_api_key_from_env() -> Optional[str]:
    """
    Attempts to obtain API key from the environment variable.

    Returns:
        API key retrieved from env variable or None if missing.
    """
    return os.environ.get("FIREWORKS_API_KEY")


R = TypeVar("R")


class Gateway:
    """
    Control plane gateway client that exposes its endpoints through
    convenient APIs.

    Keep the API consistent with `gateway.proto`.
    """

    def __init__(
        self,
        *,
        server_addr: str = "gateway.fireworks.ai:443",
        api_key: Optional[str] = None,
    ) -> None:
        """
        Args:
            server_addr: the network address of the gateway server.
            api_key: the API key to use for authentication.
        """
        self._server_addr = server_addr
        if not api_key:
            api_key = _get_api_key_from_env()
            if not api_key:
                raise ValueError(
                    "Fireworks API key not found. Please provide an API key either as a parameter "
                    "or by setting the FIREWORKS_API_KEY environment variable. "
                    "You can create a new API key at https://fireworks.ai/settings/users/api-keys or "
                    "by using `firectl create api-key --key-name <key-name>` command."
                )
        self._api_key = api_key
        self._host = self._server_addr.split(":")[0]
        self._port = int(self._server_addr.split(":")[1])
        channel = Channel(host=self._host, port=self._port, ssl=True)
        self._stub = GatewayStub(channel, metadata=[("x-api-key", api_key)])

    async def list_models(
        self,
        *,
        parent: str = "",
        filter: str = "",
        order_by: str = "",
        include_deployed_model_refs: bool = False,
    ) -> List[Model]:
        """
        Paginates through the list of available models and returns all of them.

        Args:
            parent: resource name of the parent account,
            filter: only models satisfying the provided filter (if specified)
                will be returned. See https://google.aip.dev/160 for the filter
                grammar,
            order_by: a comma-separated list of fields to order by. e.g. "foo,bar".
                The default sort order is ascending. To specify a descending order
                for a field, append a " desc" suffix. e.g. "foo desc,bar"
                Subfields are specified with a "." character. e.g. "foo.bar".
                If not specified, the default order is by "name".

        Returns:
            list of models satisfying the retrieval criteria.
        """
        result = []
        page_token = None
        while True:
            request = ListModelsRequest(
                parent=parent,
                filter=filter,
                order_by=order_by,
                include_deployed_model_refs=include_deployed_model_refs,
                page_size=200,
            )
            if page_token is not None:
                request.page_token = page_token
            response: ListModelsResponse = await self._stub.list_models(request)
            result.extend(response.models)
            if response.total_size < len(result):
                return result
            elif response.total_size == len(result):
                return result
            page_token = response.next_page_token

    async def list_deployments(self, filter: str = ""):
        account_id = await self.account_id()
        deployments = await self._stub.list_deployments(
            ListDeploymentsRequest(parent=f"accounts/{account_id}", filter=filter)
        )
        return deployments.deployments

    async def create_deployment(self, model: str, autoscaling_policy: Optional[AutoscalingPolicy] = None):
        deployment = Deployment(base_model=model)
        if autoscaling_policy is not None:
            deployment.autoscaling_policy = autoscaling_policy
        account_id = await self.account_id()
        request = CreateDeploymentRequest(parent=f"accounts/{account_id}", deployment=deployment)
        deployment = await self._stub.create_deployment(request)
        return deployment

    async def scale_deployment(self, name: str, replicas: int):
        await self._stub.scale_deployment(ScaleDeploymentRequest(name=name, replica_count=replicas))

    async def update_deployment(self, name: str, autoscaling_policy: Optional[AutoscalingPolicy] = None):
        deployment = Deployment(name=name)
        update_mask = FieldMask(paths=[])
        if autoscaling_policy is not None:
            deployment.autoscaling_policy = autoscaling_policy
            update_mask.paths.append("autoscaling_policy")
        if len(update_mask.paths) == 0:
            return
        await self._stub.update_deployment(UpdateDeploymentRequest(deployment=deployment, update_mask=update_mask))

    async def get_deployment(self, name: str) -> Deployment:
        return await self._stub.get_deployment(GetDeploymentRequest(name=name))

    @async_lru_cache()
    async def account_id(self) -> str:
        # make curl -v -H "Authorization: Bearer XXX" https://api.fireworks.ai/verifyApiKey
        # and read x-fireworks-account-id from headers of the response
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.fireworks.ai/verifyApiKey",
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                },
            )
            return response.headers["x-fireworks-account-id"]
