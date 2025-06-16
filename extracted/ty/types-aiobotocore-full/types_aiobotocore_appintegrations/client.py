"""
Type annotations for appintegrations service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appintegrations.client import AppIntegrationsServiceClient

    session = get_session()
    async with session.create_client("appintegrations") as client:
        client: AppIntegrationsServiceClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListApplicationAssociationsPaginator,
    ListApplicationsPaginator,
    ListDataIntegrationAssociationsPaginator,
    ListDataIntegrationsPaginator,
    ListEventIntegrationAssociationsPaginator,
    ListEventIntegrationsPaginator,
)
from .type_defs import (
    CreateApplicationRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateDataIntegrationAssociationRequestTypeDef,
    CreateDataIntegrationAssociationResponseTypeDef,
    CreateDataIntegrationRequestTypeDef,
    CreateDataIntegrationResponseTypeDef,
    CreateEventIntegrationRequestTypeDef,
    CreateEventIntegrationResponseTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteDataIntegrationRequestTypeDef,
    DeleteEventIntegrationRequestTypeDef,
    GetApplicationRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetDataIntegrationRequestTypeDef,
    GetDataIntegrationResponseTypeDef,
    GetEventIntegrationRequestTypeDef,
    GetEventIntegrationResponseTypeDef,
    ListApplicationAssociationsRequestTypeDef,
    ListApplicationAssociationsResponseTypeDef,
    ListApplicationsRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListDataIntegrationAssociationsRequestTypeDef,
    ListDataIntegrationAssociationsResponseTypeDef,
    ListDataIntegrationsRequestTypeDef,
    ListDataIntegrationsResponseTypeDef,
    ListEventIntegrationAssociationsRequestTypeDef,
    ListEventIntegrationAssociationsResponseTypeDef,
    ListEventIntegrationsRequestTypeDef,
    ListEventIntegrationsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateApplicationRequestTypeDef,
    UpdateDataIntegrationAssociationRequestTypeDef,
    UpdateDataIntegrationRequestTypeDef,
    UpdateEventIntegrationRequestTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("AppIntegrationsServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    DuplicateResourceException: Type[BotocoreClientError]
    InternalServiceError: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]


class AppIntegrationsServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations.html#AppIntegrationsService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppIntegrationsServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations.html#AppIntegrationsService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#generate_presigned_url)
        """

    async def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates and persists an Application resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/create_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#create_application)
        """

    async def create_data_integration(
        self, **kwargs: Unpack[CreateDataIntegrationRequestTypeDef]
    ) -> CreateDataIntegrationResponseTypeDef:
        """
        Creates and persists a DataIntegration resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/create_data_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#create_data_integration)
        """

    async def create_data_integration_association(
        self, **kwargs: Unpack[CreateDataIntegrationAssociationRequestTypeDef]
    ) -> CreateDataIntegrationAssociationResponseTypeDef:
        """
        Creates and persists a DataIntegrationAssociation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/create_data_integration_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#create_data_integration_association)
        """

    async def create_event_integration(
        self, **kwargs: Unpack[CreateEventIntegrationRequestTypeDef]
    ) -> CreateEventIntegrationResponseTypeDef:
        """
        Creates an EventIntegration, given a specified name, description, and a
        reference to an Amazon EventBridge bus in your account and a partner event
        source that pushes events to that bus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/create_event_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#create_event_integration)
        """

    async def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the Application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/delete_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#delete_application)
        """

    async def delete_data_integration(
        self, **kwargs: Unpack[DeleteDataIntegrationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the DataIntegration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/delete_data_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#delete_data_integration)
        """

    async def delete_event_integration(
        self, **kwargs: Unpack[DeleteEventIntegrationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified existing event integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/delete_event_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#delete_event_integration)
        """

    async def get_application(
        self, **kwargs: Unpack[GetApplicationRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Get an Application resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_application)
        """

    async def get_data_integration(
        self, **kwargs: Unpack[GetDataIntegrationRequestTypeDef]
    ) -> GetDataIntegrationResponseTypeDef:
        """
        Returns information about the DataIntegration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_data_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_data_integration)
        """

    async def get_event_integration(
        self, **kwargs: Unpack[GetEventIntegrationRequestTypeDef]
    ) -> GetEventIntegrationResponseTypeDef:
        """
        Returns information about the event integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_event_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_event_integration)
        """

    async def list_application_associations(
        self, **kwargs: Unpack[ListApplicationAssociationsRequestTypeDef]
    ) -> ListApplicationAssociationsResponseTypeDef:
        """
        Returns a paginated list of application associations for an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_application_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_application_associations)
        """

    async def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists applications in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_applications)
        """

    async def list_data_integration_associations(
        self, **kwargs: Unpack[ListDataIntegrationAssociationsRequestTypeDef]
    ) -> ListDataIntegrationAssociationsResponseTypeDef:
        """
        Returns a paginated list of DataIntegration associations in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_data_integration_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_data_integration_associations)
        """

    async def list_data_integrations(
        self, **kwargs: Unpack[ListDataIntegrationsRequestTypeDef]
    ) -> ListDataIntegrationsResponseTypeDef:
        """
        Returns a paginated list of DataIntegrations in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_data_integrations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_data_integrations)
        """

    async def list_event_integration_associations(
        self, **kwargs: Unpack[ListEventIntegrationAssociationsRequestTypeDef]
    ) -> ListEventIntegrationAssociationsResponseTypeDef:
        """
        Returns a paginated list of event integration associations in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_event_integration_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_event_integration_associations)
        """

    async def list_event_integrations(
        self, **kwargs: Unpack[ListEventIntegrationsRequestTypeDef]
    ) -> ListEventIntegrationsResponseTypeDef:
        """
        Returns a paginated list of event integrations in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_event_integrations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_event_integrations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#list_tags_for_resource)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds the specified tags to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes the specified tags from the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#untag_resource)
        """

    async def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates and persists an Application resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/update_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#update_application)
        """

    async def update_data_integration(
        self, **kwargs: Unpack[UpdateDataIntegrationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the description of a DataIntegration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/update_data_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#update_data_integration)
        """

    async def update_data_integration_association(
        self, **kwargs: Unpack[UpdateDataIntegrationAssociationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates and persists a DataIntegrationAssociation resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/update_data_integration_association.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#update_data_integration_association)
        """

    async def update_event_integration(
        self, **kwargs: Unpack[UpdateEventIntegrationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the description of an event integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/update_event_integration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#update_event_integration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_application_associations"]
    ) -> ListApplicationAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_integration_associations"]
    ) -> ListDataIntegrationAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_integrations"]
    ) -> ListDataIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_integration_associations"]
    ) -> ListEventIntegrationAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_event_integrations"]
    ) -> ListEventIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations.html#AppIntegrationsService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appintegrations.html#AppIntegrationsService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appintegrations/client/)
        """
