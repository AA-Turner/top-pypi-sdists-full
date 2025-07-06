"""
Type annotations for greengrassv2 service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_greengrassv2.client import GreengrassV2Client

    session = get_session()
    async with session.create_client("greengrassv2") as client:
        client: GreengrassV2Client
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
    ListClientDevicesAssociatedWithCoreDevicePaginator,
    ListComponentsPaginator,
    ListComponentVersionsPaginator,
    ListCoreDevicesPaginator,
    ListDeploymentsPaginator,
    ListEffectiveDeploymentsPaginator,
    ListInstalledComponentsPaginator,
)
from .type_defs import (
    AssociateServiceRoleToAccountRequestTypeDef,
    AssociateServiceRoleToAccountResponseTypeDef,
    BatchAssociateClientDeviceWithCoreDeviceRequestTypeDef,
    BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef,
    BatchDisassociateClientDeviceFromCoreDeviceRequestTypeDef,
    BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef,
    CancelDeploymentRequestTypeDef,
    CancelDeploymentResponseTypeDef,
    CreateComponentVersionRequestTypeDef,
    CreateComponentVersionResponseTypeDef,
    CreateDeploymentRequestTypeDef,
    CreateDeploymentResponseTypeDef,
    DeleteComponentRequestTypeDef,
    DeleteCoreDeviceRequestTypeDef,
    DeleteDeploymentRequestTypeDef,
    DescribeComponentRequestTypeDef,
    DescribeComponentResponseTypeDef,
    DisassociateServiceRoleFromAccountResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetComponentRequestTypeDef,
    GetComponentResponseTypeDef,
    GetComponentVersionArtifactRequestTypeDef,
    GetComponentVersionArtifactResponseTypeDef,
    GetConnectivityInfoRequestTypeDef,
    GetConnectivityInfoResponseTypeDef,
    GetCoreDeviceRequestTypeDef,
    GetCoreDeviceResponseTypeDef,
    GetDeploymentRequestTypeDef,
    GetDeploymentResponseTypeDef,
    GetServiceRoleForAccountResponseTypeDef,
    ListClientDevicesAssociatedWithCoreDeviceRequestTypeDef,
    ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef,
    ListComponentsRequestTypeDef,
    ListComponentsResponseTypeDef,
    ListComponentVersionsRequestTypeDef,
    ListComponentVersionsResponseTypeDef,
    ListCoreDevicesRequestTypeDef,
    ListCoreDevicesResponseTypeDef,
    ListDeploymentsRequestTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEffectiveDeploymentsRequestTypeDef,
    ListEffectiveDeploymentsResponseTypeDef,
    ListInstalledComponentsRequestTypeDef,
    ListInstalledComponentsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ResolveComponentCandidatesRequestTypeDef,
    ResolveComponentCandidatesResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateConnectivityInfoRequestTypeDef,
    UpdateConnectivityInfoResponseTypeDef,
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


__all__ = ("GreengrassV2Client",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    RequestAlreadyInProgressException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class GreengrassV2Client(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        GreengrassV2Client exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#generate_presigned_url)
        """

    async def associate_service_role_to_account(
        self, **kwargs: Unpack[AssociateServiceRoleToAccountRequestTypeDef]
    ) -> AssociateServiceRoleToAccountResponseTypeDef:
        """
        Associates a Greengrass service role with IoT Greengrass for your Amazon Web
        Services account in this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/associate_service_role_to_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#associate_service_role_to_account)
        """

    async def batch_associate_client_device_with_core_device(
        self, **kwargs: Unpack[BatchAssociateClientDeviceWithCoreDeviceRequestTypeDef]
    ) -> BatchAssociateClientDeviceWithCoreDeviceResponseTypeDef:
        """
        Associates a list of client devices with a core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/batch_associate_client_device_with_core_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#batch_associate_client_device_with_core_device)
        """

    async def batch_disassociate_client_device_from_core_device(
        self, **kwargs: Unpack[BatchDisassociateClientDeviceFromCoreDeviceRequestTypeDef]
    ) -> BatchDisassociateClientDeviceFromCoreDeviceResponseTypeDef:
        """
        Disassociates a list of client devices from a core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/batch_disassociate_client_device_from_core_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#batch_disassociate_client_device_from_core_device)
        """

    async def cancel_deployment(
        self, **kwargs: Unpack[CancelDeploymentRequestTypeDef]
    ) -> CancelDeploymentResponseTypeDef:
        """
        Cancels a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/cancel_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#cancel_deployment)
        """

    async def create_component_version(
        self, **kwargs: Unpack[CreateComponentVersionRequestTypeDef]
    ) -> CreateComponentVersionResponseTypeDef:
        """
        Creates a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/create_component_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#create_component_version)
        """

    async def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentRequestTypeDef]
    ) -> CreateDeploymentResponseTypeDef:
        """
        Creates a continuous deployment for a target, which is a Greengrass core device
        or group of core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/create_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#create_deployment)
        """

    async def delete_component(
        self, **kwargs: Unpack[DeleteComponentRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a version of a component from IoT Greengrass.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/delete_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#delete_component)
        """

    async def delete_core_device(
        self, **kwargs: Unpack[DeleteCoreDeviceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a Greengrass core device, which is an IoT thing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/delete_core_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#delete_core_device)
        """

    async def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/delete_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#delete_deployment)
        """

    async def describe_component(
        self, **kwargs: Unpack[DescribeComponentRequestTypeDef]
    ) -> DescribeComponentResponseTypeDef:
        """
        Retrieves metadata for a version of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/describe_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#describe_component)
        """

    async def disassociate_service_role_from_account(
        self,
    ) -> DisassociateServiceRoleFromAccountResponseTypeDef:
        """
        Disassociates the Greengrass service role from IoT Greengrass for your Amazon
        Web Services account in this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/disassociate_service_role_from_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#disassociate_service_role_from_account)
        """

    async def get_component(
        self, **kwargs: Unpack[GetComponentRequestTypeDef]
    ) -> GetComponentResponseTypeDef:
        """
        Gets the recipe for a version of a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_component.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_component)
        """

    async def get_component_version_artifact(
        self, **kwargs: Unpack[GetComponentVersionArtifactRequestTypeDef]
    ) -> GetComponentVersionArtifactResponseTypeDef:
        """
        Gets the pre-signed URL to download a public or a Lambda component artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_component_version_artifact.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_component_version_artifact)
        """

    async def get_connectivity_info(
        self, **kwargs: Unpack[GetConnectivityInfoRequestTypeDef]
    ) -> GetConnectivityInfoResponseTypeDef:
        """
        Retrieves connectivity information for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_connectivity_info.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_connectivity_info)
        """

    async def get_core_device(
        self, **kwargs: Unpack[GetCoreDeviceRequestTypeDef]
    ) -> GetCoreDeviceResponseTypeDef:
        """
        Retrieves metadata for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_core_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_core_device)
        """

    async def get_deployment(
        self, **kwargs: Unpack[GetDeploymentRequestTypeDef]
    ) -> GetDeploymentResponseTypeDef:
        """
        Gets a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_deployment)
        """

    async def get_service_role_for_account(self) -> GetServiceRoleForAccountResponseTypeDef:
        """
        Gets the service role associated with IoT Greengrass for your Amazon Web
        Services account in this Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_service_role_for_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_service_role_for_account)
        """

    async def list_client_devices_associated_with_core_device(
        self, **kwargs: Unpack[ListClientDevicesAssociatedWithCoreDeviceRequestTypeDef]
    ) -> ListClientDevicesAssociatedWithCoreDeviceResponseTypeDef:
        """
        Retrieves a paginated list of client devices that are associated with a core
        device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_client_devices_associated_with_core_device.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_client_devices_associated_with_core_device)
        """

    async def list_component_versions(
        self, **kwargs: Unpack[ListComponentVersionsRequestTypeDef]
    ) -> ListComponentVersionsResponseTypeDef:
        """
        Retrieves a paginated list of all versions for a component.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_component_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_component_versions)
        """

    async def list_components(
        self, **kwargs: Unpack[ListComponentsRequestTypeDef]
    ) -> ListComponentsResponseTypeDef:
        """
        Retrieves a paginated list of component summaries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_components.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_components)
        """

    async def list_core_devices(
        self, **kwargs: Unpack[ListCoreDevicesRequestTypeDef]
    ) -> ListCoreDevicesResponseTypeDef:
        """
        Retrieves a paginated list of Greengrass core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_core_devices.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_core_devices)
        """

    async def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsRequestTypeDef]
    ) -> ListDeploymentsResponseTypeDef:
        """
        Retrieves a paginated list of deployments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_deployments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_deployments)
        """

    async def list_effective_deployments(
        self, **kwargs: Unpack[ListEffectiveDeploymentsRequestTypeDef]
    ) -> ListEffectiveDeploymentsResponseTypeDef:
        """
        Retrieves a paginated list of deployment jobs that IoT Greengrass sends to
        Greengrass core devices.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_effective_deployments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_effective_deployments)
        """

    async def list_installed_components(
        self, **kwargs: Unpack[ListInstalledComponentsRequestTypeDef]
    ) -> ListInstalledComponentsResponseTypeDef:
        """
        Retrieves a paginated list of the components that a Greengrass core device runs.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_installed_components.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_installed_components)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves the list of tags for an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#list_tags_for_resource)
        """

    async def resolve_component_candidates(
        self, **kwargs: Unpack[ResolveComponentCandidatesRequestTypeDef]
    ) -> ResolveComponentCandidatesResponseTypeDef:
        """
        Retrieves a list of components that meet the component, version, and platform
        requirements of a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/resolve_component_candidates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#resolve_component_candidates)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from an IoT Greengrass resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#untag_resource)
        """

    async def update_connectivity_info(
        self, **kwargs: Unpack[UpdateConnectivityInfoRequestTypeDef]
    ) -> UpdateConnectivityInfoResponseTypeDef:
        """
        Updates connectivity information for a Greengrass core device.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/update_connectivity_info.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#update_connectivity_info)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_client_devices_associated_with_core_device"]
    ) -> ListClientDevicesAssociatedWithCoreDevicePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_component_versions"]
    ) -> ListComponentVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_components"]
    ) -> ListComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_core_devices"]
    ) -> ListCoreDevicesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_effective_deployments"]
    ) -> ListEffectiveDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_installed_components"]
    ) -> ListInstalledComponentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/greengrassv2.html#GreengrassV2.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_greengrassv2/client/)
        """
