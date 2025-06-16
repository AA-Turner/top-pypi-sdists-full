from typing import Dict, Optional
from maleo_foundation.authorization import Authorization
from maleo_foundation.managers.client.base import BearerAuth
from maleo_foundation.managers.client.maleo import MaleoClientHTTPController
from maleo_foundation.models.transfers.results.client.controllers.http \
    import BaseClientHTTPControllerResults
from maleo_foundation.utils.merger import deep_merge
from maleo_metadata.models.transfers.parameters.general.system_role \
    import MaleoMetadataSystemRoleGeneralParametersTransfers
from maleo_metadata.models.transfers.parameters.client.system_role \
    import MaleoMetadataSystemRoleClientParametersTransfers

class MaleoMetadataSystemRoleHTTPController(MaleoClientHTTPController):
    async def get_system_roles(
        self,
        parameters:MaleoMetadataSystemRoleClientParametersTransfers.GetMultiple,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> BaseClientHTTPControllerResults:
        """Fetch system roles from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url}/v1/system-roles/"

            #* Parse parameters to query params
            params = (
                MaleoMetadataSystemRoleClientParametersTransfers
                .GetMultipleQuery
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump(
                    exclude={"sort_columns", "date_filters"},
                    exclude_none=True
                )
            )

            #* Create headers
            base_headers = {
                "Content-Type": "application/json"
            }
            if headers is not None:
                headers = deep_merge(
                    base_headers,
                    headers
                )
            else:
                headers = base_headers

            #* Create auth
            token = None
            if authorization and authorization.scheme == "Bearer":
                token = authorization.credentials
            elif self._service_manager.token:
                token = self._service_manager.token
            auth = BearerAuth(token) if token else None

            #* Send request and wait for response
            response = await client.get(url=url, params=params, headers=headers, auth=auth)
            return BaseClientHTTPControllerResults(response=response)

    async def get_system_role(
        self,
        parameters:MaleoMetadataSystemRoleGeneralParametersTransfers.GetSingle,
        authorization:Optional[Authorization] = None,
        headers:Optional[Dict[str, str]] = None
    ) -> BaseClientHTTPControllerResults:
        """Fetch system role from MaleoMetadata"""
        async with self._manager.get_client() as client:
            #* Define URL
            url = f"{self._manager.url}/v1/system-roles/{parameters.identifier}/{parameters.value}"

            #* Parse parameters to query params
            params = (
                MaleoMetadataSystemRoleGeneralParametersTransfers
                .GetSingleQuery
                .model_validate(
                    parameters.model_dump()
                )
                .model_dump(exclude_none=True)
            )

            #* Create headers
            base_headers = {
                "Content-Type": "application/json"
            }
            if headers is not None:
                headers = deep_merge(
                    base_headers,
                    headers
                )
            else:
                headers = base_headers

            #* Create auth
            token = None
            if authorization and authorization.scheme == "Bearer":
                token = authorization.credentials
            elif self._service_manager.token:
                token = self._service_manager.token
            auth = BearerAuth(token) if token else None

            #* Send request and wait for response
            response = await client.get(url=url, params=params, headers=headers, auth=auth)
            return BaseClientHTTPControllerResults(response=response)