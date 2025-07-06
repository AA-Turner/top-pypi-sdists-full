"""
Type annotations for finspace-data service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_finspace_data.client import FinSpaceDataClient

    session = get_session()
    async with session.create_client("finspace-data") as client:
        client: FinSpaceDataClient
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
    ListChangesetsPaginator,
    ListDatasetsPaginator,
    ListDataViewsPaginator,
    ListPermissionGroupsPaginator,
    ListUsersPaginator,
)
from .type_defs import (
    AssociateUserToPermissionGroupRequestTypeDef,
    AssociateUserToPermissionGroupResponseTypeDef,
    CreateChangesetRequestTypeDef,
    CreateChangesetResponseTypeDef,
    CreateDatasetRequestTypeDef,
    CreateDatasetResponseTypeDef,
    CreateDataViewRequestTypeDef,
    CreateDataViewResponseTypeDef,
    CreatePermissionGroupRequestTypeDef,
    CreatePermissionGroupResponseTypeDef,
    CreateUserRequestTypeDef,
    CreateUserResponseTypeDef,
    DeleteDatasetRequestTypeDef,
    DeleteDatasetResponseTypeDef,
    DeletePermissionGroupRequestTypeDef,
    DeletePermissionGroupResponseTypeDef,
    DisableUserRequestTypeDef,
    DisableUserResponseTypeDef,
    DisassociateUserFromPermissionGroupRequestTypeDef,
    DisassociateUserFromPermissionGroupResponseTypeDef,
    EnableUserRequestTypeDef,
    EnableUserResponseTypeDef,
    GetChangesetRequestTypeDef,
    GetChangesetResponseTypeDef,
    GetDatasetRequestTypeDef,
    GetDatasetResponseTypeDef,
    GetDataViewRequestTypeDef,
    GetDataViewResponseTypeDef,
    GetExternalDataViewAccessDetailsRequestTypeDef,
    GetExternalDataViewAccessDetailsResponseTypeDef,
    GetPermissionGroupRequestTypeDef,
    GetPermissionGroupResponseTypeDef,
    GetProgrammaticAccessCredentialsRequestTypeDef,
    GetProgrammaticAccessCredentialsResponseTypeDef,
    GetUserRequestTypeDef,
    GetUserResponseTypeDef,
    GetWorkingLocationRequestTypeDef,
    GetWorkingLocationResponseTypeDef,
    ListChangesetsRequestTypeDef,
    ListChangesetsResponseTypeDef,
    ListDatasetsRequestTypeDef,
    ListDatasetsResponseTypeDef,
    ListDataViewsRequestTypeDef,
    ListDataViewsResponseTypeDef,
    ListPermissionGroupsByUserRequestTypeDef,
    ListPermissionGroupsByUserResponseTypeDef,
    ListPermissionGroupsRequestTypeDef,
    ListPermissionGroupsResponseTypeDef,
    ListUsersByPermissionGroupRequestTypeDef,
    ListUsersByPermissionGroupResponseTypeDef,
    ListUsersRequestTypeDef,
    ListUsersResponseTypeDef,
    ResetUserPasswordRequestTypeDef,
    ResetUserPasswordResponseTypeDef,
    UpdateChangesetRequestTypeDef,
    UpdateChangesetResponseTypeDef,
    UpdateDatasetRequestTypeDef,
    UpdateDatasetResponseTypeDef,
    UpdatePermissionGroupRequestTypeDef,
    UpdatePermissionGroupResponseTypeDef,
    UpdateUserRequestTypeDef,
    UpdateUserResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("FinSpaceDataClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class FinSpaceDataClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        FinSpaceDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#generate_presigned_url)
        """

    async def associate_user_to_permission_group(
        self, **kwargs: Unpack[AssociateUserToPermissionGroupRequestTypeDef]
    ) -> AssociateUserToPermissionGroupResponseTypeDef:
        """
        Adds a user to a permission group to grant permissions for actions a user can
        perform in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/associate_user_to_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#associate_user_to_permission_group)
        """

    async def create_changeset(
        self, **kwargs: Unpack[CreateChangesetRequestTypeDef]
    ) -> CreateChangesetResponseTypeDef:
        """
        Creates a new Changeset in a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_changeset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_changeset)
        """

    async def create_data_view(
        self, **kwargs: Unpack[CreateDataViewRequestTypeDef]
    ) -> CreateDataViewResponseTypeDef:
        """
        Creates a Dataview for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_data_view.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_data_view)
        """

    async def create_dataset(
        self, **kwargs: Unpack[CreateDatasetRequestTypeDef]
    ) -> CreateDatasetResponseTypeDef:
        """
        Creates a new FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_dataset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_dataset)
        """

    async def create_permission_group(
        self, **kwargs: Unpack[CreatePermissionGroupRequestTypeDef]
    ) -> CreatePermissionGroupResponseTypeDef:
        """
        Creates a group of permissions for various actions that a user can perform in
        FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_permission_group)
        """

    async def create_user(
        self, **kwargs: Unpack[CreateUserRequestTypeDef]
    ) -> CreateUserResponseTypeDef:
        """
        Creates a new user in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/create_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#create_user)
        """

    async def delete_dataset(
        self, **kwargs: Unpack[DeleteDatasetRequestTypeDef]
    ) -> DeleteDatasetResponseTypeDef:
        """
        Deletes a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/delete_dataset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#delete_dataset)
        """

    async def delete_permission_group(
        self, **kwargs: Unpack[DeletePermissionGroupRequestTypeDef]
    ) -> DeletePermissionGroupResponseTypeDef:
        """
        Deletes a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/delete_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#delete_permission_group)
        """

    async def disable_user(
        self, **kwargs: Unpack[DisableUserRequestTypeDef]
    ) -> DisableUserResponseTypeDef:
        """
        Denies access to the FinSpace web application and API for the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/disable_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#disable_user)
        """

    async def disassociate_user_from_permission_group(
        self, **kwargs: Unpack[DisassociateUserFromPermissionGroupRequestTypeDef]
    ) -> DisassociateUserFromPermissionGroupResponseTypeDef:
        """
        Removes a user from a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/disassociate_user_from_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#disassociate_user_from_permission_group)
        """

    async def enable_user(
        self, **kwargs: Unpack[EnableUserRequestTypeDef]
    ) -> EnableUserResponseTypeDef:
        """
        Allows the specified user to access the FinSpace web application and API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/enable_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#enable_user)
        """

    async def get_changeset(
        self, **kwargs: Unpack[GetChangesetRequestTypeDef]
    ) -> GetChangesetResponseTypeDef:
        """
        Get information about a Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_changeset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_changeset)
        """

    async def get_data_view(
        self, **kwargs: Unpack[GetDataViewRequestTypeDef]
    ) -> GetDataViewResponseTypeDef:
        """
        Gets information about a Dataview.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_data_view.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_data_view)
        """

    async def get_dataset(
        self, **kwargs: Unpack[GetDatasetRequestTypeDef]
    ) -> GetDatasetResponseTypeDef:
        """
        Returns information about a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_dataset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_dataset)
        """

    async def get_external_data_view_access_details(
        self, **kwargs: Unpack[GetExternalDataViewAccessDetailsRequestTypeDef]
    ) -> GetExternalDataViewAccessDetailsResponseTypeDef:
        """
        Returns the credentials to access the external Dataview from an S3 location.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_external_data_view_access_details.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_external_data_view_access_details)
        """

    async def get_permission_group(
        self, **kwargs: Unpack[GetPermissionGroupRequestTypeDef]
    ) -> GetPermissionGroupResponseTypeDef:
        """
        Retrieves the details of a specific permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_permission_group)
        """

    async def get_programmatic_access_credentials(
        self, **kwargs: Unpack[GetProgrammaticAccessCredentialsRequestTypeDef]
    ) -> GetProgrammaticAccessCredentialsResponseTypeDef:
        """
        Request programmatic credentials to use with FinSpace SDK.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_programmatic_access_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_programmatic_access_credentials)
        """

    async def get_user(self, **kwargs: Unpack[GetUserRequestTypeDef]) -> GetUserResponseTypeDef:
        """
        Retrieves details for a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_user)
        """

    async def get_working_location(
        self, **kwargs: Unpack[GetWorkingLocationRequestTypeDef]
    ) -> GetWorkingLocationResponseTypeDef:
        """
        A temporary Amazon S3 location, where you can copy your files from a source
        location to stage or use as a scratch space in FinSpace notebook.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_working_location.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_working_location)
        """

    async def list_changesets(
        self, **kwargs: Unpack[ListChangesetsRequestTypeDef]
    ) -> ListChangesetsResponseTypeDef:
        """
        Lists the FinSpace Changesets for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_changesets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_changesets)
        """

    async def list_data_views(
        self, **kwargs: Unpack[ListDataViewsRequestTypeDef]
    ) -> ListDataViewsResponseTypeDef:
        """
        Lists all available Dataviews for a Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_data_views.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_data_views)
        """

    async def list_datasets(
        self, **kwargs: Unpack[ListDatasetsRequestTypeDef]
    ) -> ListDatasetsResponseTypeDef:
        """
        Lists all of the active Datasets that a user has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_datasets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_datasets)
        """

    async def list_permission_groups(
        self, **kwargs: Unpack[ListPermissionGroupsRequestTypeDef]
    ) -> ListPermissionGroupsResponseTypeDef:
        """
        Lists all available permission groups in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_permission_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_permission_groups)
        """

    async def list_permission_groups_by_user(
        self, **kwargs: Unpack[ListPermissionGroupsByUserRequestTypeDef]
    ) -> ListPermissionGroupsByUserResponseTypeDef:
        """
        Lists all the permission groups that are associated with a specific user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_permission_groups_by_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_permission_groups_by_user)
        """

    async def list_users(
        self, **kwargs: Unpack[ListUsersRequestTypeDef]
    ) -> ListUsersResponseTypeDef:
        """
        Lists all available users in FinSpace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_users.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_users)
        """

    async def list_users_by_permission_group(
        self, **kwargs: Unpack[ListUsersByPermissionGroupRequestTypeDef]
    ) -> ListUsersByPermissionGroupResponseTypeDef:
        """
        Lists details of all the users in a specific permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/list_users_by_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#list_users_by_permission_group)
        """

    async def reset_user_password(
        self, **kwargs: Unpack[ResetUserPasswordRequestTypeDef]
    ) -> ResetUserPasswordResponseTypeDef:
        """
        Resets the password for a specified user ID and generates a temporary one.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/reset_user_password.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#reset_user_password)
        """

    async def update_changeset(
        self, **kwargs: Unpack[UpdateChangesetRequestTypeDef]
    ) -> UpdateChangesetResponseTypeDef:
        """
        Updates a FinSpace Changeset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_changeset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_changeset)
        """

    async def update_dataset(
        self, **kwargs: Unpack[UpdateDatasetRequestTypeDef]
    ) -> UpdateDatasetResponseTypeDef:
        """
        Updates a FinSpace Dataset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_dataset.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_dataset)
        """

    async def update_permission_group(
        self, **kwargs: Unpack[UpdatePermissionGroupRequestTypeDef]
    ) -> UpdatePermissionGroupResponseTypeDef:
        """
        Modifies the details of a permission group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_permission_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_permission_group)
        """

    async def update_user(
        self, **kwargs: Unpack[UpdateUserRequestTypeDef]
    ) -> UpdateUserResponseTypeDef:
        """
        Modifies the details of the specified user.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/update_user.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#update_user)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_changesets"]
    ) -> ListChangesetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_data_views"]
    ) -> ListDataViewsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_datasets"]
    ) -> ListDatasetsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_permission_groups"]
    ) -> ListPermissionGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_users"]
    ) -> ListUsersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/finspace-data.html#FinSpaceData.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_finspace_data/client/)
        """
