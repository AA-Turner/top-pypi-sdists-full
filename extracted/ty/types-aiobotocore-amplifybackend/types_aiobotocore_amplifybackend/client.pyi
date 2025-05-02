"""
Type annotations for amplifybackend service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_amplifybackend.client import AmplifyBackendClient

    session = get_session()
    async with session.create_client("amplifybackend") as client:
        client: AmplifyBackendClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListBackendJobsPaginator
from .type_defs import (
    CloneBackendRequestTypeDef,
    CloneBackendResponseTypeDef,
    CreateBackendAPIRequestTypeDef,
    CreateBackendAPIResponseTypeDef,
    CreateBackendAuthRequestTypeDef,
    CreateBackendAuthResponseTypeDef,
    CreateBackendConfigRequestTypeDef,
    CreateBackendConfigResponseTypeDef,
    CreateBackendRequestTypeDef,
    CreateBackendResponseTypeDef,
    CreateBackendStorageRequestTypeDef,
    CreateBackendStorageResponseTypeDef,
    CreateTokenRequestTypeDef,
    CreateTokenResponseTypeDef,
    DeleteBackendAPIRequestTypeDef,
    DeleteBackendAPIResponseTypeDef,
    DeleteBackendAuthRequestTypeDef,
    DeleteBackendAuthResponseTypeDef,
    DeleteBackendRequestTypeDef,
    DeleteBackendResponseTypeDef,
    DeleteBackendStorageRequestTypeDef,
    DeleteBackendStorageResponseTypeDef,
    DeleteTokenRequestTypeDef,
    DeleteTokenResponseTypeDef,
    GenerateBackendAPIModelsRequestTypeDef,
    GenerateBackendAPIModelsResponseTypeDef,
    GetBackendAPIModelsRequestTypeDef,
    GetBackendAPIModelsResponseTypeDef,
    GetBackendAPIRequestTypeDef,
    GetBackendAPIResponseTypeDef,
    GetBackendAuthRequestTypeDef,
    GetBackendAuthResponseTypeDef,
    GetBackendJobRequestTypeDef,
    GetBackendJobResponseTypeDef,
    GetBackendRequestTypeDef,
    GetBackendResponseTypeDef,
    GetBackendStorageRequestTypeDef,
    GetBackendStorageResponseTypeDef,
    GetTokenRequestTypeDef,
    GetTokenResponseTypeDef,
    ImportBackendAuthRequestTypeDef,
    ImportBackendAuthResponseTypeDef,
    ImportBackendStorageRequestTypeDef,
    ImportBackendStorageResponseTypeDef,
    ListBackendJobsRequestTypeDef,
    ListBackendJobsResponseTypeDef,
    ListS3BucketsRequestTypeDef,
    ListS3BucketsResponseTypeDef,
    RemoveAllBackendsRequestTypeDef,
    RemoveAllBackendsResponseTypeDef,
    RemoveBackendConfigRequestTypeDef,
    RemoveBackendConfigResponseTypeDef,
    UpdateBackendAPIRequestTypeDef,
    UpdateBackendAPIResponseTypeDef,
    UpdateBackendAuthRequestTypeDef,
    UpdateBackendAuthResponseTypeDef,
    UpdateBackendConfigRequestTypeDef,
    UpdateBackendConfigResponseTypeDef,
    UpdateBackendJobRequestTypeDef,
    UpdateBackendJobResponseTypeDef,
    UpdateBackendStorageRequestTypeDef,
    UpdateBackendStorageResponseTypeDef,
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

__all__ = ("AmplifyBackendClient",)

class Exceptions(BaseClientExceptions):
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    GatewayTimeoutException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class AmplifyBackendClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AmplifyBackendClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#generate_presigned_url)
        """

    async def clone_backend(
        self, **kwargs: Unpack[CloneBackendRequestTypeDef]
    ) -> CloneBackendResponseTypeDef:
        """
        This operation clones an existing backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/clone_backend.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#clone_backend)
        """

    async def create_backend(
        self, **kwargs: Unpack[CreateBackendRequestTypeDef]
    ) -> CreateBackendResponseTypeDef:
        """
        This operation creates a backend for an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend)
        """

    async def create_backend_api(
        self, **kwargs: Unpack[CreateBackendAPIRequestTypeDef]
    ) -> CreateBackendAPIResponseTypeDef:
        """
        Creates a new backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_api.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_api)
        """

    async def create_backend_auth(
        self, **kwargs: Unpack[CreateBackendAuthRequestTypeDef]
    ) -> CreateBackendAuthResponseTypeDef:
        """
        Creates a new backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_auth)
        """

    async def create_backend_config(
        self, **kwargs: Unpack[CreateBackendConfigRequestTypeDef]
    ) -> CreateBackendConfigResponseTypeDef:
        """
        Creates a config object for a backend.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_config)
        """

    async def create_backend_storage(
        self, **kwargs: Unpack[CreateBackendStorageRequestTypeDef]
    ) -> CreateBackendStorageResponseTypeDef:
        """
        Creates a backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_backend_storage.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_backend_storage)
        """

    async def create_token(
        self, **kwargs: Unpack[CreateTokenRequestTypeDef]
    ) -> CreateTokenResponseTypeDef:
        """
        Generates a one-time challenge code to authenticate a user into your Amplify
        Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/create_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#create_token)
        """

    async def delete_backend(
        self, **kwargs: Unpack[DeleteBackendRequestTypeDef]
    ) -> DeleteBackendResponseTypeDef:
        """
        Removes an existing environment from your Amplify project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend)
        """

    async def delete_backend_api(
        self, **kwargs: Unpack[DeleteBackendAPIRequestTypeDef]
    ) -> DeleteBackendAPIResponseTypeDef:
        """
        Deletes an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend_api.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend_api)
        """

    async def delete_backend_auth(
        self, **kwargs: Unpack[DeleteBackendAuthRequestTypeDef]
    ) -> DeleteBackendAuthResponseTypeDef:
        """
        Deletes an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend_auth)
        """

    async def delete_backend_storage(
        self, **kwargs: Unpack[DeleteBackendStorageRequestTypeDef]
    ) -> DeleteBackendStorageResponseTypeDef:
        """
        Removes the specified backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_backend_storage.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_backend_storage)
        """

    async def delete_token(
        self, **kwargs: Unpack[DeleteTokenRequestTypeDef]
    ) -> DeleteTokenResponseTypeDef:
        """
        Deletes the challenge token based on the given appId and sessionId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/delete_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#delete_token)
        """

    async def generate_backend_api_models(
        self, **kwargs: Unpack[GenerateBackendAPIModelsRequestTypeDef]
    ) -> GenerateBackendAPIModelsResponseTypeDef:
        """
        Generates a model schema for an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/generate_backend_api_models.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#generate_backend_api_models)
        """

    async def get_backend(
        self, **kwargs: Unpack[GetBackendRequestTypeDef]
    ) -> GetBackendResponseTypeDef:
        """
        Provides project-level details for your Amplify UI project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend)
        """

    async def get_backend_api(
        self, **kwargs: Unpack[GetBackendAPIRequestTypeDef]
    ) -> GetBackendAPIResponseTypeDef:
        """
        Gets the details for a backend API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_api.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_api)
        """

    async def get_backend_api_models(
        self, **kwargs: Unpack[GetBackendAPIModelsRequestTypeDef]
    ) -> GetBackendAPIModelsResponseTypeDef:
        """
        Gets a model introspection schema for an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_api_models.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_api_models)
        """

    async def get_backend_auth(
        self, **kwargs: Unpack[GetBackendAuthRequestTypeDef]
    ) -> GetBackendAuthResponseTypeDef:
        """
        Gets a backend auth details.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_auth)
        """

    async def get_backend_job(
        self, **kwargs: Unpack[GetBackendJobRequestTypeDef]
    ) -> GetBackendJobResponseTypeDef:
        """
        Returns information about a specific job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_job)
        """

    async def get_backend_storage(
        self, **kwargs: Unpack[GetBackendStorageRequestTypeDef]
    ) -> GetBackendStorageResponseTypeDef:
        """
        Gets details for a backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_backend_storage.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_backend_storage)
        """

    async def get_token(self, **kwargs: Unpack[GetTokenRequestTypeDef]) -> GetTokenResponseTypeDef:
        """
        Gets the challenge token based on the given appId and sessionId.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_token.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_token)
        """

    async def import_backend_auth(
        self, **kwargs: Unpack[ImportBackendAuthRequestTypeDef]
    ) -> ImportBackendAuthResponseTypeDef:
        """
        Imports an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/import_backend_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#import_backend_auth)
        """

    async def import_backend_storage(
        self, **kwargs: Unpack[ImportBackendStorageRequestTypeDef]
    ) -> ImportBackendStorageResponseTypeDef:
        """
        Imports an existing backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/import_backend_storage.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#import_backend_storage)
        """

    async def list_backend_jobs(
        self, **kwargs: Unpack[ListBackendJobsRequestTypeDef]
    ) -> ListBackendJobsResponseTypeDef:
        """
        Lists the jobs for the backend of an Amplify app.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/list_backend_jobs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#list_backend_jobs)
        """

    async def list_s3_buckets(
        self, **kwargs: Unpack[ListS3BucketsRequestTypeDef]
    ) -> ListS3BucketsResponseTypeDef:
        """
        The list of S3 buckets in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/list_s3_buckets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#list_s3_buckets)
        """

    async def remove_all_backends(
        self, **kwargs: Unpack[RemoveAllBackendsRequestTypeDef]
    ) -> RemoveAllBackendsResponseTypeDef:
        """
        Removes all backend environments from your Amplify project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/remove_all_backends.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#remove_all_backends)
        """

    async def remove_backend_config(
        self, **kwargs: Unpack[RemoveBackendConfigRequestTypeDef]
    ) -> RemoveBackendConfigResponseTypeDef:
        """
        Removes the AWS resources required to access the Amplify Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/remove_backend_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#remove_backend_config)
        """

    async def update_backend_api(
        self, **kwargs: Unpack[UpdateBackendAPIRequestTypeDef]
    ) -> UpdateBackendAPIResponseTypeDef:
        """
        Updates an existing backend API resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_api.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_api)
        """

    async def update_backend_auth(
        self, **kwargs: Unpack[UpdateBackendAuthRequestTypeDef]
    ) -> UpdateBackendAuthResponseTypeDef:
        """
        Updates an existing backend authentication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_auth.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_auth)
        """

    async def update_backend_config(
        self, **kwargs: Unpack[UpdateBackendConfigRequestTypeDef]
    ) -> UpdateBackendConfigResponseTypeDef:
        """
        Updates the AWS resources required to access the Amplify Admin UI.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_config.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_config)
        """

    async def update_backend_job(
        self, **kwargs: Unpack[UpdateBackendJobRequestTypeDef]
    ) -> UpdateBackendJobResponseTypeDef:
        """
        Updates a specific job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_job.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_job)
        """

    async def update_backend_storage(
        self, **kwargs: Unpack[UpdateBackendStorageRequestTypeDef]
    ) -> UpdateBackendStorageResponseTypeDef:
        """
        Updates an existing backend storage resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/update_backend_storage.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#update_backend_storage)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_backend_jobs"]
    ) -> ListBackendJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amplifybackend.html#AmplifyBackend.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_amplifybackend/client/)
        """
