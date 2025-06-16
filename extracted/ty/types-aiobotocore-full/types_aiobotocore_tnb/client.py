"""
Type annotations for tnb service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_tnb.client import TelcoNetworkBuilderClient

    session = get_session()
    async with session.create_client("tnb") as client:
        client: TelcoNetworkBuilderClient
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
    ListSolFunctionInstancesPaginator,
    ListSolFunctionPackagesPaginator,
    ListSolNetworkInstancesPaginator,
    ListSolNetworkOperationsPaginator,
    ListSolNetworkPackagesPaginator,
)
from .type_defs import (
    CancelSolNetworkOperationInputTypeDef,
    CreateSolFunctionPackageInputTypeDef,
    CreateSolFunctionPackageOutputTypeDef,
    CreateSolNetworkInstanceInputTypeDef,
    CreateSolNetworkInstanceOutputTypeDef,
    CreateSolNetworkPackageInputTypeDef,
    CreateSolNetworkPackageOutputTypeDef,
    DeleteSolFunctionPackageInputTypeDef,
    DeleteSolNetworkInstanceInputTypeDef,
    DeleteSolNetworkPackageInputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetSolFunctionInstanceInputTypeDef,
    GetSolFunctionInstanceOutputTypeDef,
    GetSolFunctionPackageContentInputTypeDef,
    GetSolFunctionPackageContentOutputTypeDef,
    GetSolFunctionPackageDescriptorInputTypeDef,
    GetSolFunctionPackageDescriptorOutputTypeDef,
    GetSolFunctionPackageInputTypeDef,
    GetSolFunctionPackageOutputTypeDef,
    GetSolNetworkInstanceInputTypeDef,
    GetSolNetworkInstanceOutputTypeDef,
    GetSolNetworkOperationInputTypeDef,
    GetSolNetworkOperationOutputTypeDef,
    GetSolNetworkPackageContentInputTypeDef,
    GetSolNetworkPackageContentOutputTypeDef,
    GetSolNetworkPackageDescriptorInputTypeDef,
    GetSolNetworkPackageDescriptorOutputTypeDef,
    GetSolNetworkPackageInputTypeDef,
    GetSolNetworkPackageOutputTypeDef,
    InstantiateSolNetworkInstanceInputTypeDef,
    InstantiateSolNetworkInstanceOutputTypeDef,
    ListSolFunctionInstancesInputTypeDef,
    ListSolFunctionInstancesOutputTypeDef,
    ListSolFunctionPackagesInputTypeDef,
    ListSolFunctionPackagesOutputTypeDef,
    ListSolNetworkInstancesInputTypeDef,
    ListSolNetworkInstancesOutputTypeDef,
    ListSolNetworkOperationsInputTypeDef,
    ListSolNetworkOperationsOutputTypeDef,
    ListSolNetworkPackagesInputTypeDef,
    ListSolNetworkPackagesOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    PutSolFunctionPackageContentInputTypeDef,
    PutSolFunctionPackageContentOutputTypeDef,
    PutSolNetworkPackageContentInputTypeDef,
    PutSolNetworkPackageContentOutputTypeDef,
    TagResourceInputTypeDef,
    TerminateSolNetworkInstanceInputTypeDef,
    TerminateSolNetworkInstanceOutputTypeDef,
    UntagResourceInputTypeDef,
    UpdateSolFunctionPackageInputTypeDef,
    UpdateSolFunctionPackageOutputTypeDef,
    UpdateSolNetworkInstanceInputTypeDef,
    UpdateSolNetworkInstanceOutputTypeDef,
    UpdateSolNetworkPackageInputTypeDef,
    UpdateSolNetworkPackageOutputTypeDef,
    ValidateSolFunctionPackageContentInputTypeDef,
    ValidateSolFunctionPackageContentOutputTypeDef,
    ValidateSolNetworkPackageContentInputTypeDef,
    ValidateSolNetworkPackageContentOutputTypeDef,
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


__all__ = ("TelcoNetworkBuilderClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class TelcoNetworkBuilderClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb.html#TelcoNetworkBuilder.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        TelcoNetworkBuilderClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb.html#TelcoNetworkBuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#generate_presigned_url)
        """

    async def cancel_sol_network_operation(
        self, **kwargs: Unpack[CancelSolNetworkOperationInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Cancels a network operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/cancel_sol_network_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#cancel_sol_network_operation)
        """

    async def create_sol_function_package(
        self, **kwargs: Unpack[CreateSolFunctionPackageInputTypeDef]
    ) -> CreateSolFunctionPackageOutputTypeDef:
        """
        Creates a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/create_sol_function_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#create_sol_function_package)
        """

    async def create_sol_network_instance(
        self, **kwargs: Unpack[CreateSolNetworkInstanceInputTypeDef]
    ) -> CreateSolNetworkInstanceOutputTypeDef:
        """
        Creates a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/create_sol_network_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#create_sol_network_instance)
        """

    async def create_sol_network_package(
        self, **kwargs: Unpack[CreateSolNetworkPackageInputTypeDef]
    ) -> CreateSolNetworkPackageOutputTypeDef:
        """
        Creates a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/create_sol_network_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#create_sol_network_package)
        """

    async def delete_sol_function_package(
        self, **kwargs: Unpack[DeleteSolFunctionPackageInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/delete_sol_function_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#delete_sol_function_package)
        """

    async def delete_sol_network_instance(
        self, **kwargs: Unpack[DeleteSolNetworkInstanceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/delete_sol_network_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#delete_sol_network_instance)
        """

    async def delete_sol_network_package(
        self, **kwargs: Unpack[DeleteSolNetworkPackageInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/delete_sol_network_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#delete_sol_network_package)
        """

    async def get_sol_function_instance(
        self, **kwargs: Unpack[GetSolFunctionInstanceInputTypeDef]
    ) -> GetSolFunctionInstanceOutputTypeDef:
        """
        Gets the details of a network function instance, including the instantiation
        state and metadata from the function package descriptor in the network function
        package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_function_instance)
        """

    async def get_sol_function_package(
        self, **kwargs: Unpack[GetSolFunctionPackageInputTypeDef]
    ) -> GetSolFunctionPackageOutputTypeDef:
        """
        Gets the details of an individual function package, such as the operational
        state and whether the package is in use.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_function_package)
        """

    async def get_sol_function_package_content(
        self, **kwargs: Unpack[GetSolFunctionPackageContentInputTypeDef]
    ) -> GetSolFunctionPackageContentOutputTypeDef:
        """
        Gets the contents of a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_package_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_function_package_content)
        """

    async def get_sol_function_package_descriptor(
        self, **kwargs: Unpack[GetSolFunctionPackageDescriptorInputTypeDef]
    ) -> GetSolFunctionPackageDescriptorOutputTypeDef:
        """
        Gets a function package descriptor in a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_function_package_descriptor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_function_package_descriptor)
        """

    async def get_sol_network_instance(
        self, **kwargs: Unpack[GetSolNetworkInstanceInputTypeDef]
    ) -> GetSolNetworkInstanceOutputTypeDef:
        """
        Gets the details of the network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_network_instance)
        """

    async def get_sol_network_operation(
        self, **kwargs: Unpack[GetSolNetworkOperationInputTypeDef]
    ) -> GetSolNetworkOperationOutputTypeDef:
        """
        Gets the details of a network operation, including the tasks involved in the
        network operation and the status of the tasks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_operation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_network_operation)
        """

    async def get_sol_network_package(
        self, **kwargs: Unpack[GetSolNetworkPackageInputTypeDef]
    ) -> GetSolNetworkPackageOutputTypeDef:
        """
        Gets the details of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_network_package)
        """

    async def get_sol_network_package_content(
        self, **kwargs: Unpack[GetSolNetworkPackageContentInputTypeDef]
    ) -> GetSolNetworkPackageContentOutputTypeDef:
        """
        Gets the contents of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_package_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_network_package_content)
        """

    async def get_sol_network_package_descriptor(
        self, **kwargs: Unpack[GetSolNetworkPackageDescriptorInputTypeDef]
    ) -> GetSolNetworkPackageDescriptorOutputTypeDef:
        """
        Gets the content of the network service descriptor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_sol_network_package_descriptor.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_sol_network_package_descriptor)
        """

    async def instantiate_sol_network_instance(
        self, **kwargs: Unpack[InstantiateSolNetworkInstanceInputTypeDef]
    ) -> InstantiateSolNetworkInstanceOutputTypeDef:
        """
        Instantiates a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/instantiate_sol_network_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#instantiate_sol_network_instance)
        """

    async def list_sol_function_instances(
        self, **kwargs: Unpack[ListSolFunctionInstancesInputTypeDef]
    ) -> ListSolFunctionInstancesOutputTypeDef:
        """
        Lists network function instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_function_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#list_sol_function_instances)
        """

    async def list_sol_function_packages(
        self, **kwargs: Unpack[ListSolFunctionPackagesInputTypeDef]
    ) -> ListSolFunctionPackagesOutputTypeDef:
        """
        Lists information about function packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_function_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#list_sol_function_packages)
        """

    async def list_sol_network_instances(
        self, **kwargs: Unpack[ListSolNetworkInstancesInputTypeDef]
    ) -> ListSolNetworkInstancesOutputTypeDef:
        """
        Lists your network instances.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_network_instances.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#list_sol_network_instances)
        """

    async def list_sol_network_operations(
        self, **kwargs: Unpack[ListSolNetworkOperationsInputTypeDef]
    ) -> ListSolNetworkOperationsOutputTypeDef:
        """
        Lists details for a network operation, including when the operation started and
        the status of the operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_network_operations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#list_sol_network_operations)
        """

    async def list_sol_network_packages(
        self, **kwargs: Unpack[ListSolNetworkPackagesInputTypeDef]
    ) -> ListSolNetworkPackagesOutputTypeDef:
        """
        Lists network packages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_sol_network_packages.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#list_sol_network_packages)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists tags for AWS TNB resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#list_tags_for_resource)
        """

    async def put_sol_function_package_content(
        self, **kwargs: Unpack[PutSolFunctionPackageContentInputTypeDef]
    ) -> PutSolFunctionPackageContentOutputTypeDef:
        """
        Uploads the contents of a function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/put_sol_function_package_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#put_sol_function_package_content)
        """

    async def put_sol_network_package_content(
        self, **kwargs: Unpack[PutSolNetworkPackageContentInputTypeDef]
    ) -> PutSolNetworkPackageContentOutputTypeDef:
        """
        Uploads the contents of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/put_sol_network_package_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#put_sol_network_package_content)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Tags an AWS TNB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#tag_resource)
        """

    async def terminate_sol_network_instance(
        self, **kwargs: Unpack[TerminateSolNetworkInstanceInputTypeDef]
    ) -> TerminateSolNetworkInstanceOutputTypeDef:
        """
        Terminates a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/terminate_sol_network_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#terminate_sol_network_instance)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Untags an AWS TNB resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#untag_resource)
        """

    async def update_sol_function_package(
        self, **kwargs: Unpack[UpdateSolFunctionPackageInputTypeDef]
    ) -> UpdateSolFunctionPackageOutputTypeDef:
        """
        Updates the operational state of function package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/update_sol_function_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#update_sol_function_package)
        """

    async def update_sol_network_instance(
        self, **kwargs: Unpack[UpdateSolNetworkInstanceInputTypeDef]
    ) -> UpdateSolNetworkInstanceOutputTypeDef:
        """
        Update a network instance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/update_sol_network_instance.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#update_sol_network_instance)
        """

    async def update_sol_network_package(
        self, **kwargs: Unpack[UpdateSolNetworkPackageInputTypeDef]
    ) -> UpdateSolNetworkPackageOutputTypeDef:
        """
        Updates the operational state of a network package.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/update_sol_network_package.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#update_sol_network_package)
        """

    async def validate_sol_function_package_content(
        self, **kwargs: Unpack[ValidateSolFunctionPackageContentInputTypeDef]
    ) -> ValidateSolFunctionPackageContentOutputTypeDef:
        """
        Validates function package content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/validate_sol_function_package_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#validate_sol_function_package_content)
        """

    async def validate_sol_network_package_content(
        self, **kwargs: Unpack[ValidateSolNetworkPackageContentInputTypeDef]
    ) -> ValidateSolNetworkPackageContentOutputTypeDef:
        """
        Validates network package content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/validate_sol_network_package_content.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#validate_sol_network_package_content)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sol_function_instances"]
    ) -> ListSolFunctionInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sol_function_packages"]
    ) -> ListSolFunctionPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sol_network_instances"]
    ) -> ListSolNetworkInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sol_network_operations"]
    ) -> ListSolNetworkOperationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sol_network_packages"]
    ) -> ListSolNetworkPackagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb.html#TelcoNetworkBuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/tnb.html#TelcoNetworkBuilder.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_tnb/client/)
        """
