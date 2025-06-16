"""
Type annotations for ssm-sap service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_sap.client import SsmSapClient

    session = get_session()
    async with session.create_client("ssm-sap") as client:
        client: SsmSapClient
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
    ListApplicationsPaginator,
    ListComponentsPaginator,
    ListDatabasesPaginator,
    ListOperationEventsPaginator,
    ListOperationsPaginator,
)
from .type_defs import (
    DeleteResourcePermissionInputTypeDef,
    DeleteResourcePermissionOutputTypeDef,
    DeregisterApplicationInputTypeDef,
    GetApplicationInputTypeDef,
    GetApplicationOutputTypeDef,
    GetComponentInputTypeDef,
    GetComponentOutputTypeDef,
    GetDatabaseInputTypeDef,
    GetDatabaseOutputTypeDef,
    GetOperationInputTypeDef,
    GetOperationOutputTypeDef,
    GetResourcePermissionInputTypeDef,
    GetResourcePermissionOutputTypeDef,
    ListApplicationsInputTypeDef,
    ListApplicationsOutputTypeDef,
    ListComponentsInputTypeDef,
    ListComponentsOutputTypeDef,
    ListDatabasesInputTypeDef,
    ListDatabasesOutputTypeDef,
    ListOperationEventsInputTypeDef,
    ListOperationEventsOutputTypeDef,
    ListOperationsInputTypeDef,
    ListOperationsOutputTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutResourcePermissionInputTypeDef,
    PutResourcePermissionOutputTypeDef,
    RegisterApplicationInputTypeDef,
    RegisterApplicationOutputTypeDef,
    StartApplicationInputTypeDef,
    StartApplicationOutputTypeDef,
    StartApplicationRefreshInputTypeDef,
    StartApplicationRefreshOutputTypeDef,
    StopApplicationInputTypeDef,
    StopApplicationOutputTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateApplicationSettingsInputTypeDef,
    UpdateApplicationSettingsOutputTypeDef,
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

__all__ = ("SsmSapClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    UnauthorizedException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class SsmSapClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap.html#SsmSap.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SsmSapClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap.html#SsmSap.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#generate_presigned_url)
        """

    async def delete_resource_permission(
        self, **kwargs: Unpack[DeleteResourcePermissionInputTypeDef]
    ) -> DeleteResourcePermissionOutputTypeDef:
        """
        Removes permissions associated with the target database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/delete_resource_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#delete_resource_permission)
        """

    async def deregister_application(
        self, **kwargs: Unpack[DeregisterApplicationInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deregister an SAP application with AWS Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/deregister_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#deregister_application)
        """

    async def get_application(
        self, **kwargs: Unpack[GetApplicationInputTypeDef]
    ) -> GetApplicationOutputTypeDef:
        """
        Gets an application registered with AWS Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_application)
        """

    async def get_component(
        self, **kwargs: Unpack[GetComponentInputTypeDef]
    ) -> GetComponentOutputTypeDef:
        """
        Gets the component of an application registered with AWS Systems Manager for
        SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_component.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_component)
        """

    async def get_database(
        self, **kwargs: Unpack[GetDatabaseInputTypeDef]
    ) -> GetDatabaseOutputTypeDef:
        """
        Gets the SAP HANA database of an application registered with AWS Systems
        Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_database.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_database)
        """

    async def get_operation(
        self, **kwargs: Unpack[GetOperationInputTypeDef]
    ) -> GetOperationOutputTypeDef:
        """
        Gets the details of an operation by specifying the operation ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_operation)
        """

    async def get_resource_permission(
        self, **kwargs: Unpack[GetResourcePermissionInputTypeDef]
    ) -> GetResourcePermissionOutputTypeDef:
        """
        Gets permissions associated with the target database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_resource_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_resource_permission)
        """

    async def list_applications(
        self, **kwargs: Unpack[ListApplicationsInputTypeDef]
    ) -> ListApplicationsOutputTypeDef:
        """
        Lists all the applications registered with AWS Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/list_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#list_applications)
        """

    async def list_components(
        self, **kwargs: Unpack[ListComponentsInputTypeDef]
    ) -> ListComponentsOutputTypeDef:
        """
        Lists all the components registered with AWS Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/list_components.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#list_components)
        """

    async def list_databases(
        self, **kwargs: Unpack[ListDatabasesInputTypeDef]
    ) -> ListDatabasesOutputTypeDef:
        """
        Lists the SAP HANA databases of an application registered with AWS Systems
        Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/list_databases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#list_databases)
        """

    async def list_operation_events(
        self, **kwargs: Unpack[ListOperationEventsInputTypeDef]
    ) -> ListOperationEventsOutputTypeDef:
        """
        Returns a list of operations events.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/list_operation_events.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#list_operation_events)
        """

    async def list_operations(
        self, **kwargs: Unpack[ListOperationsInputTypeDef]
    ) -> ListOperationsOutputTypeDef:
        """
        Lists the operations performed by AWS Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/list_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#list_operations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists all tags on an SAP HANA application and/or database registered with AWS
        Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#list_tags_for_resource)
        """

    async def put_resource_permission(
        self, **kwargs: Unpack[PutResourcePermissionInputTypeDef]
    ) -> PutResourcePermissionOutputTypeDef:
        """
        Adds permissions to the target database.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/put_resource_permission.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#put_resource_permission)
        """

    async def register_application(
        self, **kwargs: Unpack[RegisterApplicationInputTypeDef]
    ) -> RegisterApplicationOutputTypeDef:
        """
        Register an SAP application with AWS Systems Manager for SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/register_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#register_application)
        """

    async def start_application(
        self, **kwargs: Unpack[StartApplicationInputTypeDef]
    ) -> StartApplicationOutputTypeDef:
        """
        Request is an operation which starts an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/start_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#start_application)
        """

    async def start_application_refresh(
        self, **kwargs: Unpack[StartApplicationRefreshInputTypeDef]
    ) -> StartApplicationRefreshOutputTypeDef:
        """
        Refreshes a registered application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/start_application_refresh.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#start_application_refresh)
        """

    async def stop_application(
        self, **kwargs: Unpack[StopApplicationInputTypeDef]
    ) -> StopApplicationOutputTypeDef:
        """
        Request is an operation to stop an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/stop_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#stop_application)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates tag for a resource by specifying the ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Delete the tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#untag_resource)
        """

    async def update_application_settings(
        self, **kwargs: Unpack[UpdateApplicationSettingsInputTypeDef]
    ) -> UpdateApplicationSettingsOutputTypeDef:
        """
        Updates the settings of an application registered with AWS Systems Manager for
        SAP.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/update_application_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#update_application_settings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_components"]
    ) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_databases"]
    ) -> ListDatabasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_operation_events"]
    ) -> ListOperationEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_operations"]
    ) -> ListOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap.html#SsmSap.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm-sap.html#SsmSap.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_sap/client/)
        """
