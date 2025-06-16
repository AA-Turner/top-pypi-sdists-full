"""
Type annotations for appstream service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_appstream.client import AppStreamClient

    session = get_session()
    async with session.create_client("appstream") as client:
        client: AppStreamClient
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
    DescribeDirectoryConfigsPaginator,
    DescribeFleetsPaginator,
    DescribeImageBuildersPaginator,
    DescribeImagesPaginator,
    DescribeSessionsPaginator,
    DescribeStacksPaginator,
    DescribeUsersPaginator,
    DescribeUserStackAssociationsPaginator,
    ListAssociatedFleetsPaginator,
    ListAssociatedStacksPaginator,
)
from .type_defs import (
    AssociateAppBlockBuilderAppBlockRequestTypeDef,
    AssociateAppBlockBuilderAppBlockResultTypeDef,
    AssociateApplicationFleetRequestTypeDef,
    AssociateApplicationFleetResultTypeDef,
    AssociateApplicationToEntitlementRequestTypeDef,
    AssociateFleetRequestTypeDef,
    BatchAssociateUserStackRequestTypeDef,
    BatchAssociateUserStackResultTypeDef,
    BatchDisassociateUserStackRequestTypeDef,
    BatchDisassociateUserStackResultTypeDef,
    CopyImageRequestTypeDef,
    CopyImageResponseTypeDef,
    CreateAppBlockBuilderRequestTypeDef,
    CreateAppBlockBuilderResultTypeDef,
    CreateAppBlockBuilderStreamingURLRequestTypeDef,
    CreateAppBlockBuilderStreamingURLResultTypeDef,
    CreateAppBlockRequestTypeDef,
    CreateAppBlockResultTypeDef,
    CreateApplicationRequestTypeDef,
    CreateApplicationResultTypeDef,
    CreateDirectoryConfigRequestTypeDef,
    CreateDirectoryConfigResultTypeDef,
    CreateEntitlementRequestTypeDef,
    CreateEntitlementResultTypeDef,
    CreateFleetRequestTypeDef,
    CreateFleetResultTypeDef,
    CreateImageBuilderRequestTypeDef,
    CreateImageBuilderResultTypeDef,
    CreateImageBuilderStreamingURLRequestTypeDef,
    CreateImageBuilderStreamingURLResultTypeDef,
    CreateStackRequestTypeDef,
    CreateStackResultTypeDef,
    CreateStreamingURLRequestTypeDef,
    CreateStreamingURLResultTypeDef,
    CreateThemeForStackRequestTypeDef,
    CreateThemeForStackResultTypeDef,
    CreateUpdatedImageRequestTypeDef,
    CreateUpdatedImageResultTypeDef,
    CreateUsageReportSubscriptionResultTypeDef,
    CreateUserRequestTypeDef,
    DeleteAppBlockBuilderRequestTypeDef,
    DeleteAppBlockRequestTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteDirectoryConfigRequestTypeDef,
    DeleteEntitlementRequestTypeDef,
    DeleteFleetRequestTypeDef,
    DeleteImageBuilderRequestTypeDef,
    DeleteImageBuilderResultTypeDef,
    DeleteImagePermissionsRequestTypeDef,
    DeleteImageRequestTypeDef,
    DeleteImageResultTypeDef,
    DeleteStackRequestTypeDef,
    DeleteThemeForStackRequestTypeDef,
    DeleteUserRequestTypeDef,
    DescribeAppBlockBuilderAppBlockAssociationsRequestTypeDef,
    DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef,
    DescribeAppBlockBuildersRequestTypeDef,
    DescribeAppBlockBuildersResultTypeDef,
    DescribeAppBlocksRequestTypeDef,
    DescribeAppBlocksResultTypeDef,
    DescribeApplicationFleetAssociationsRequestTypeDef,
    DescribeApplicationFleetAssociationsResultTypeDef,
    DescribeApplicationsRequestTypeDef,
    DescribeApplicationsResultTypeDef,
    DescribeDirectoryConfigsRequestTypeDef,
    DescribeDirectoryConfigsResultTypeDef,
    DescribeEntitlementsRequestTypeDef,
    DescribeEntitlementsResultTypeDef,
    DescribeFleetsRequestTypeDef,
    DescribeFleetsResultTypeDef,
    DescribeImageBuildersRequestTypeDef,
    DescribeImageBuildersResultTypeDef,
    DescribeImagePermissionsRequestTypeDef,
    DescribeImagePermissionsResultTypeDef,
    DescribeImagesRequestTypeDef,
    DescribeImagesResultTypeDef,
    DescribeSessionsRequestTypeDef,
    DescribeSessionsResultTypeDef,
    DescribeStacksRequestTypeDef,
    DescribeStacksResultTypeDef,
    DescribeThemeForStackRequestTypeDef,
    DescribeThemeForStackResultTypeDef,
    DescribeUsageReportSubscriptionsRequestTypeDef,
    DescribeUsageReportSubscriptionsResultTypeDef,
    DescribeUsersRequestTypeDef,
    DescribeUsersResultTypeDef,
    DescribeUserStackAssociationsRequestTypeDef,
    DescribeUserStackAssociationsResultTypeDef,
    DisableUserRequestTypeDef,
    DisassociateAppBlockBuilderAppBlockRequestTypeDef,
    DisassociateApplicationFleetRequestTypeDef,
    DisassociateApplicationFromEntitlementRequestTypeDef,
    DisassociateFleetRequestTypeDef,
    EnableUserRequestTypeDef,
    ExpireSessionRequestTypeDef,
    ListAssociatedFleetsRequestTypeDef,
    ListAssociatedFleetsResultTypeDef,
    ListAssociatedStacksRequestTypeDef,
    ListAssociatedStacksResultTypeDef,
    ListEntitledApplicationsRequestTypeDef,
    ListEntitledApplicationsResultTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    StartAppBlockBuilderRequestTypeDef,
    StartAppBlockBuilderResultTypeDef,
    StartFleetRequestTypeDef,
    StartImageBuilderRequestTypeDef,
    StartImageBuilderResultTypeDef,
    StopAppBlockBuilderRequestTypeDef,
    StopAppBlockBuilderResultTypeDef,
    StopFleetRequestTypeDef,
    StopImageBuilderRequestTypeDef,
    StopImageBuilderResultTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAppBlockBuilderRequestTypeDef,
    UpdateAppBlockBuilderResultTypeDef,
    UpdateApplicationRequestTypeDef,
    UpdateApplicationResultTypeDef,
    UpdateDirectoryConfigRequestTypeDef,
    UpdateDirectoryConfigResultTypeDef,
    UpdateEntitlementRequestTypeDef,
    UpdateEntitlementResultTypeDef,
    UpdateFleetRequestTypeDef,
    UpdateFleetResultTypeDef,
    UpdateImagePermissionsRequestTypeDef,
    UpdateStackRequestTypeDef,
    UpdateStackResultTypeDef,
    UpdateThemeForStackRequestTypeDef,
    UpdateThemeForStackResultTypeDef,
)
from .waiter import FleetStartedWaiter, FleetStoppedWaiter

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

__all__ = ("AppStreamClient",)

class Exceptions(BaseClientExceptions):
    ClientError: Type[BotocoreClientError]
    ConcurrentModificationException: Type[BotocoreClientError]
    EntitlementAlreadyExistsException: Type[BotocoreClientError]
    EntitlementNotFoundException: Type[BotocoreClientError]
    IncompatibleImageException: Type[BotocoreClientError]
    InvalidAccountStatusException: Type[BotocoreClientError]
    InvalidParameterCombinationException: Type[BotocoreClientError]
    InvalidRoleException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    OperationNotPermittedException: Type[BotocoreClientError]
    RequestLimitExceededException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotAvailableException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class AppStreamClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AppStreamClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#generate_presigned_url)
        """

    async def associate_app_block_builder_app_block(
        self, **kwargs: Unpack[AssociateAppBlockBuilderAppBlockRequestTypeDef]
    ) -> AssociateAppBlockBuilderAppBlockResultTypeDef:
        """
        Associates the specified app block builder with the specified app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/associate_app_block_builder_app_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_app_block_builder_app_block)
        """

    async def associate_application_fleet(
        self, **kwargs: Unpack[AssociateApplicationFleetRequestTypeDef]
    ) -> AssociateApplicationFleetResultTypeDef:
        """
        Associates the specified application with the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/associate_application_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_application_fleet)
        """

    async def associate_application_to_entitlement(
        self, **kwargs: Unpack[AssociateApplicationToEntitlementRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an application to entitle.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/associate_application_to_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_application_to_entitlement)
        """

    async def associate_fleet(
        self, **kwargs: Unpack[AssociateFleetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates the specified fleet with the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/associate_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#associate_fleet)
        """

    async def batch_associate_user_stack(
        self, **kwargs: Unpack[BatchAssociateUserStackRequestTypeDef]
    ) -> BatchAssociateUserStackResultTypeDef:
        """
        Associates the specified users with the specified stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/batch_associate_user_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#batch_associate_user_stack)
        """

    async def batch_disassociate_user_stack(
        self, **kwargs: Unpack[BatchDisassociateUserStackRequestTypeDef]
    ) -> BatchDisassociateUserStackResultTypeDef:
        """
        Disassociates the specified users from the specified stacks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/batch_disassociate_user_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#batch_disassociate_user_stack)
        """

    async def copy_image(
        self, **kwargs: Unpack[CopyImageRequestTypeDef]
    ) -> CopyImageResponseTypeDef:
        """
        Copies the image within the same region or to a new region within the same AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/copy_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#copy_image)
        """

    async def create_app_block(
        self, **kwargs: Unpack[CreateAppBlockRequestTypeDef]
    ) -> CreateAppBlockResultTypeDef:
        """
        Creates an app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_app_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_app_block)
        """

    async def create_app_block_builder(
        self, **kwargs: Unpack[CreateAppBlockBuilderRequestTypeDef]
    ) -> CreateAppBlockBuilderResultTypeDef:
        """
        Creates an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_app_block_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_app_block_builder)
        """

    async def create_app_block_builder_streaming_url(
        self, **kwargs: Unpack[CreateAppBlockBuilderStreamingURLRequestTypeDef]
    ) -> CreateAppBlockBuilderStreamingURLResultTypeDef:
        """
        Creates a URL to start a create app block builder streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_app_block_builder_streaming_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_app_block_builder_streaming_url)
        """

    async def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestTypeDef]
    ) -> CreateApplicationResultTypeDef:
        """
        Creates an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_application)
        """

    async def create_directory_config(
        self, **kwargs: Unpack[CreateDirectoryConfigRequestTypeDef]
    ) -> CreateDirectoryConfigResultTypeDef:
        """
        Creates a Directory Config object in AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_directory_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_directory_config)
        """

    async def create_entitlement(
        self, **kwargs: Unpack[CreateEntitlementRequestTypeDef]
    ) -> CreateEntitlementResultTypeDef:
        """
        Creates a new entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_entitlement)
        """

    async def create_fleet(
        self, **kwargs: Unpack[CreateFleetRequestTypeDef]
    ) -> CreateFleetResultTypeDef:
        """
        Creates a fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_fleet)
        """

    async def create_image_builder(
        self, **kwargs: Unpack[CreateImageBuilderRequestTypeDef]
    ) -> CreateImageBuilderResultTypeDef:
        """
        Creates an image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_image_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_image_builder)
        """

    async def create_image_builder_streaming_url(
        self, **kwargs: Unpack[CreateImageBuilderStreamingURLRequestTypeDef]
    ) -> CreateImageBuilderStreamingURLResultTypeDef:
        """
        Creates a URL to start an image builder streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_image_builder_streaming_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_image_builder_streaming_url)
        """

    async def create_stack(
        self, **kwargs: Unpack[CreateStackRequestTypeDef]
    ) -> CreateStackResultTypeDef:
        """
        Creates a stack to start streaming applications to users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_stack)
        """

    async def create_streaming_url(
        self, **kwargs: Unpack[CreateStreamingURLRequestTypeDef]
    ) -> CreateStreamingURLResultTypeDef:
        """
        Creates a temporary URL to start an AppStream 2.0 streaming session for the
        specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_streaming_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_streaming_url)
        """

    async def create_theme_for_stack(
        self, **kwargs: Unpack[CreateThemeForStackRequestTypeDef]
    ) -> CreateThemeForStackResultTypeDef:
        """
        Creates custom branding that customizes the appearance of the streaming
        application catalog page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_theme_for_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_theme_for_stack)
        """

    async def create_updated_image(
        self, **kwargs: Unpack[CreateUpdatedImageRequestTypeDef]
    ) -> CreateUpdatedImageResultTypeDef:
        """
        Creates a new image with the latest Windows operating system updates, driver
        updates, and AppStream 2.0 agent software.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_updated_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_updated_image)
        """

    async def create_usage_report_subscription(self) -> CreateUsageReportSubscriptionResultTypeDef:
        """
        Creates a usage report subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_usage_report_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_usage_report_subscription)
        """

    async def create_user(self, **kwargs: Unpack[CreateUserRequestTypeDef]) -> Dict[str, Any]:
        """
        Creates a new user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/create_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#create_user)
        """

    async def delete_app_block(
        self, **kwargs: Unpack[DeleteAppBlockRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_app_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_app_block)
        """

    async def delete_app_block_builder(
        self, **kwargs: Unpack[DeleteAppBlockBuilderRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_app_block_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_app_block_builder)
        """

    async def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_application)
        """

    async def delete_directory_config(
        self, **kwargs: Unpack[DeleteDirectoryConfigRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified Directory Config object from AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_directory_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_directory_config)
        """

    async def delete_entitlement(
        self, **kwargs: Unpack[DeleteEntitlementRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_entitlement)
        """

    async def delete_fleet(self, **kwargs: Unpack[DeleteFleetRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_fleet)
        """

    async def delete_image(
        self, **kwargs: Unpack[DeleteImageRequestTypeDef]
    ) -> DeleteImageResultTypeDef:
        """
        Deletes the specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_image)
        """

    async def delete_image_builder(
        self, **kwargs: Unpack[DeleteImageBuilderRequestTypeDef]
    ) -> DeleteImageBuilderResultTypeDef:
        """
        Deletes the specified image builder and releases the capacity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_image_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_image_builder)
        """

    async def delete_image_permissions(
        self, **kwargs: Unpack[DeleteImagePermissionsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes permissions for the specified private image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_image_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_image_permissions)
        """

    async def delete_stack(self, **kwargs: Unpack[DeleteStackRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_stack)
        """

    async def delete_theme_for_stack(
        self, **kwargs: Unpack[DeleteThemeForStackRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes custom branding that customizes the appearance of the streaming
        application catalog page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_theme_for_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_theme_for_stack)
        """

    async def delete_usage_report_subscription(self) -> Dict[str, Any]:
        """
        Disables usage report generation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_usage_report_subscription.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_usage_report_subscription)
        """

    async def delete_user(self, **kwargs: Unpack[DeleteUserRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a user from the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/delete_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#delete_user)
        """

    async def describe_app_block_builder_app_block_associations(
        self, **kwargs: Unpack[DescribeAppBlockBuilderAppBlockAssociationsRequestTypeDef]
    ) -> DescribeAppBlockBuilderAppBlockAssociationsResultTypeDef:
        """
        Retrieves a list that describes one or more app block builder associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_app_block_builder_app_block_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_app_block_builder_app_block_associations)
        """

    async def describe_app_block_builders(
        self, **kwargs: Unpack[DescribeAppBlockBuildersRequestTypeDef]
    ) -> DescribeAppBlockBuildersResultTypeDef:
        """
        Retrieves a list that describes one or more app block builders.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_app_block_builders.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_app_block_builders)
        """

    async def describe_app_blocks(
        self, **kwargs: Unpack[DescribeAppBlocksRequestTypeDef]
    ) -> DescribeAppBlocksResultTypeDef:
        """
        Retrieves a list that describes one or more app blocks.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_app_blocks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_app_blocks)
        """

    async def describe_application_fleet_associations(
        self, **kwargs: Unpack[DescribeApplicationFleetAssociationsRequestTypeDef]
    ) -> DescribeApplicationFleetAssociationsResultTypeDef:
        """
        Retrieves a list that describes one or more application fleet associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_application_fleet_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_application_fleet_associations)
        """

    async def describe_applications(
        self, **kwargs: Unpack[DescribeApplicationsRequestTypeDef]
    ) -> DescribeApplicationsResultTypeDef:
        """
        Retrieves a list that describes one or more applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_applications)
        """

    async def describe_directory_configs(
        self, **kwargs: Unpack[DescribeDirectoryConfigsRequestTypeDef]
    ) -> DescribeDirectoryConfigsResultTypeDef:
        """
        Retrieves a list that describes one or more specified Directory Config objects
        for AppStream 2.0, if the names for these objects are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_directory_configs.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_directory_configs)
        """

    async def describe_entitlements(
        self, **kwargs: Unpack[DescribeEntitlementsRequestTypeDef]
    ) -> DescribeEntitlementsResultTypeDef:
        """
        Retrieves a list that describes one of more entitlements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_entitlements.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_entitlements)
        """

    async def describe_fleets(
        self, **kwargs: Unpack[DescribeFleetsRequestTypeDef]
    ) -> DescribeFleetsResultTypeDef:
        """
        Retrieves a list that describes one or more specified fleets, if the fleet
        names are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_fleets)
        """

    async def describe_image_builders(
        self, **kwargs: Unpack[DescribeImageBuildersRequestTypeDef]
    ) -> DescribeImageBuildersResultTypeDef:
        """
        Retrieves a list that describes one or more specified image builders, if the
        image builder names are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_image_builders.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_image_builders)
        """

    async def describe_image_permissions(
        self, **kwargs: Unpack[DescribeImagePermissionsRequestTypeDef]
    ) -> DescribeImagePermissionsResultTypeDef:
        """
        Retrieves a list that describes the permissions for shared AWS account IDs on a
        private image that you own.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_image_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_image_permissions)
        """

    async def describe_images(
        self, **kwargs: Unpack[DescribeImagesRequestTypeDef]
    ) -> DescribeImagesResultTypeDef:
        """
        Retrieves a list that describes one or more specified images, if the image
        names or image ARNs are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_images)
        """

    async def describe_sessions(
        self, **kwargs: Unpack[DescribeSessionsRequestTypeDef]
    ) -> DescribeSessionsResultTypeDef:
        """
        Retrieves a list that describes the streaming sessions for a specified stack
        and fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_sessions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_sessions)
        """

    async def describe_stacks(
        self, **kwargs: Unpack[DescribeStacksRequestTypeDef]
    ) -> DescribeStacksResultTypeDef:
        """
        Retrieves a list that describes one or more specified stacks, if the stack
        names are provided.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_stacks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_stacks)
        """

    async def describe_theme_for_stack(
        self, **kwargs: Unpack[DescribeThemeForStackRequestTypeDef]
    ) -> DescribeThemeForStackResultTypeDef:
        """
        Retrieves a list that describes the theme for a specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_theme_for_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_theme_for_stack)
        """

    async def describe_usage_report_subscriptions(
        self, **kwargs: Unpack[DescribeUsageReportSubscriptionsRequestTypeDef]
    ) -> DescribeUsageReportSubscriptionsResultTypeDef:
        """
        Retrieves a list that describes one or more usage report subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_usage_report_subscriptions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_usage_report_subscriptions)
        """

    async def describe_user_stack_associations(
        self, **kwargs: Unpack[DescribeUserStackAssociationsRequestTypeDef]
    ) -> DescribeUserStackAssociationsResultTypeDef:
        """
        Retrieves a list that describes the UserStackAssociation objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_user_stack_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_user_stack_associations)
        """

    async def describe_users(
        self, **kwargs: Unpack[DescribeUsersRequestTypeDef]
    ) -> DescribeUsersResultTypeDef:
        """
        Retrieves a list that describes one or more specified users in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/describe_users.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#describe_users)
        """

    async def disable_user(self, **kwargs: Unpack[DisableUserRequestTypeDef]) -> Dict[str, Any]:
        """
        Disables the specified user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/disable_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disable_user)
        """

    async def disassociate_app_block_builder_app_block(
        self, **kwargs: Unpack[DisassociateAppBlockBuilderAppBlockRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates a specified app block builder from a specified app block.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/disassociate_app_block_builder_app_block.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_app_block_builder_app_block)
        """

    async def disassociate_application_fleet(
        self, **kwargs: Unpack[DisassociateApplicationFleetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified application from the fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/disassociate_application_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_application_fleet)
        """

    async def disassociate_application_from_entitlement(
        self, **kwargs: Unpack[DisassociateApplicationFromEntitlementRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified application from the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/disassociate_application_from_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_application_from_entitlement)
        """

    async def disassociate_fleet(
        self, **kwargs: Unpack[DisassociateFleetRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates the specified fleet from the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/disassociate_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#disassociate_fleet)
        """

    async def enable_user(self, **kwargs: Unpack[EnableUserRequestTypeDef]) -> Dict[str, Any]:
        """
        Enables a user in the user pool.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/enable_user.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#enable_user)
        """

    async def expire_session(self, **kwargs: Unpack[ExpireSessionRequestTypeDef]) -> Dict[str, Any]:
        """
        Immediately stops the specified streaming session.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/expire_session.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#expire_session)
        """

    async def list_associated_fleets(
        self, **kwargs: Unpack[ListAssociatedFleetsRequestTypeDef]
    ) -> ListAssociatedFleetsResultTypeDef:
        """
        Retrieves the name of the fleet that is associated with the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/list_associated_fleets.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_associated_fleets)
        """

    async def list_associated_stacks(
        self, **kwargs: Unpack[ListAssociatedStacksRequestTypeDef]
    ) -> ListAssociatedStacksResultTypeDef:
        """
        Retrieves the name of the stack with which the specified fleet is associated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/list_associated_stacks.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_associated_stacks)
        """

    async def list_entitled_applications(
        self, **kwargs: Unpack[ListEntitledApplicationsRequestTypeDef]
    ) -> ListEntitledApplicationsResultTypeDef:
        """
        Retrieves a list of entitled applications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/list_entitled_applications.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_entitled_applications)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Retrieves a list of all tags for the specified AppStream 2.0 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#list_tags_for_resource)
        """

    async def start_app_block_builder(
        self, **kwargs: Unpack[StartAppBlockBuilderRequestTypeDef]
    ) -> StartAppBlockBuilderResultTypeDef:
        """
        Starts an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/start_app_block_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#start_app_block_builder)
        """

    async def start_fleet(self, **kwargs: Unpack[StartFleetRequestTypeDef]) -> Dict[str, Any]:
        """
        Starts the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/start_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#start_fleet)
        """

    async def start_image_builder(
        self, **kwargs: Unpack[StartImageBuilderRequestTypeDef]
    ) -> StartImageBuilderResultTypeDef:
        """
        Starts the specified image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/start_image_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#start_image_builder)
        """

    async def stop_app_block_builder(
        self, **kwargs: Unpack[StopAppBlockBuilderRequestTypeDef]
    ) -> StopAppBlockBuilderResultTypeDef:
        """
        Stops an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/stop_app_block_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#stop_app_block_builder)
        """

    async def stop_fleet(self, **kwargs: Unpack[StopFleetRequestTypeDef]) -> Dict[str, Any]:
        """
        Stops the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/stop_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#stop_fleet)
        """

    async def stop_image_builder(
        self, **kwargs: Unpack[StopImageBuilderRequestTypeDef]
    ) -> StopImageBuilderResultTypeDef:
        """
        Stops the specified image builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/stop_image_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#stop_image_builder)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds or overwrites one or more tags for the specified AppStream 2.0 resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Disassociates one or more specified tags from the specified AppStream 2.0
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#untag_resource)
        """

    async def update_app_block_builder(
        self, **kwargs: Unpack[UpdateAppBlockBuilderRequestTypeDef]
    ) -> UpdateAppBlockBuilderResultTypeDef:
        """
        Updates an app block builder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_app_block_builder.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_app_block_builder)
        """

    async def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestTypeDef]
    ) -> UpdateApplicationResultTypeDef:
        """
        Updates the specified application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_application.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_application)
        """

    async def update_directory_config(
        self, **kwargs: Unpack[UpdateDirectoryConfigRequestTypeDef]
    ) -> UpdateDirectoryConfigResultTypeDef:
        """
        Updates the specified Directory Config object in AppStream 2.0.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_directory_config.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_directory_config)
        """

    async def update_entitlement(
        self, **kwargs: Unpack[UpdateEntitlementRequestTypeDef]
    ) -> UpdateEntitlementResultTypeDef:
        """
        Updates the specified entitlement.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_entitlement.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_entitlement)
        """

    async def update_fleet(
        self, **kwargs: Unpack[UpdateFleetRequestTypeDef]
    ) -> UpdateFleetResultTypeDef:
        """
        Updates the specified fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_fleet.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_fleet)
        """

    async def update_image_permissions(
        self, **kwargs: Unpack[UpdateImagePermissionsRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds or updates permissions for the specified private image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_image_permissions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_image_permissions)
        """

    async def update_stack(
        self, **kwargs: Unpack[UpdateStackRequestTypeDef]
    ) -> UpdateStackResultTypeDef:
        """
        Updates the specified fields for the specified stack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_stack)
        """

    async def update_theme_for_stack(
        self, **kwargs: Unpack[UpdateThemeForStackRequestTypeDef]
    ) -> UpdateThemeForStackResultTypeDef:
        """
        Updates custom branding that customizes the appearance of the streaming
        application catalog page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/update_theme_for_stack.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#update_theme_for_stack)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_directory_configs"]
    ) -> DescribeDirectoryConfigsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_fleets"]
    ) -> DescribeFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_image_builders"]
    ) -> DescribeImageBuildersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_images"]
    ) -> DescribeImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_sessions"]
    ) -> DescribeSessionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_stacks"]
    ) -> DescribeStacksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_user_stack_associations"]
    ) -> DescribeUserStackAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_users"]
    ) -> DescribeUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associated_fleets"]
    ) -> ListAssociatedFleetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associated_stacks"]
    ) -> ListAssociatedStacksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fleet_started"]
    ) -> FleetStartedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["fleet_stopped"]
    ) -> FleetStoppedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/appstream.html#AppStream.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_appstream/client/)
        """
