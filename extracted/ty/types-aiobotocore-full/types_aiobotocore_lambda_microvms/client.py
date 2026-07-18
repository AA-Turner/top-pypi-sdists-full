"""
Type annotations for lambda-microvms service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lambda_microvms.client import LambdaMicroVMsClient

    session = get_session()
    async with session.create_client("lambda-microvms") as client:
        client: LambdaMicroVMsClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListManagedMicrovmImagesPaginator,
    ListManagedMicrovmImageVersionsPaginator,
    ListMicrovmImageBuildsPaginator,
    ListMicrovmImagesPaginator,
    ListMicrovmImageVersionsPaginator,
    ListMicrovmsPaginator,
)
from .type_defs import (
    CreateMicrovmAuthTokenRequestTypeDef,
    CreateMicrovmAuthTokenResponseTypeDef,
    CreateMicrovmImageRequestTypeDef,
    CreateMicrovmImageResponseTypeDef,
    CreateMicrovmShellAuthTokenRequestTypeDef,
    CreateMicrovmShellAuthTokenResponseTypeDef,
    DeleteMicrovmImageInputTypeDef,
    DeleteMicrovmImageOutputTypeDef,
    DeleteMicrovmImageVersionInputTypeDef,
    DeleteMicrovmImageVersionOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetMicrovmImageBuildInputTypeDef,
    GetMicrovmImageBuildOutputTypeDef,
    GetMicrovmImageInputTypeDef,
    GetMicrovmImageOutputTypeDef,
    GetMicrovmImageVersionInputTypeDef,
    GetMicrovmImageVersionOutputTypeDef,
    GetMicrovmRequestTypeDef,
    GetMicrovmResponseTypeDef,
    ListManagedMicrovmImagesInputTypeDef,
    ListManagedMicrovmImagesOutputTypeDef,
    ListManagedMicrovmImageVersionsInputTypeDef,
    ListManagedMicrovmImageVersionsOutputTypeDef,
    ListMicrovmImageBuildsInputTypeDef,
    ListMicrovmImageBuildsOutputTypeDef,
    ListMicrovmImagesRequestTypeDef,
    ListMicrovmImagesResponseTypeDef,
    ListMicrovmImageVersionsInputTypeDef,
    ListMicrovmImageVersionsOutputTypeDef,
    ListMicrovmsRequestTypeDef,
    ListMicrovmsResponseTypeDef,
    ListTagsRequestTypeDef,
    ListTagsResponseTypeDef,
    ResumeMicrovmRequestTypeDef,
    RunMicrovmRequestTypeDef,
    RunMicrovmResponseTypeDef,
    SuspendMicrovmRequestTypeDef,
    TagResourceRequestTypeDef,
    TerminateMicrovmRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateMicrovmImageRequestTypeDef,
    UpdateMicrovmImageResponseTypeDef,
    UpdateMicrovmImageVersionRequestTypeDef,
    UpdateMicrovmImageVersionResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("LambdaMicroVMsClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidParameterValueException: type[BotocoreClientError]
    ResourceConflictException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class LambdaMicroVMsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms.html#LambdaMicroVMs.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LambdaMicroVMsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms.html#LambdaMicroVMs.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#generate_presigned_url)
        """

    async def create_microvm_auth_token(
        self, **kwargs: Unpack[CreateMicrovmAuthTokenRequestTypeDef]
    ) -> CreateMicrovmAuthTokenResponseTypeDef:
        """
        Creates an authentication token for accessing a running MicroVM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/create_microvm_auth_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#create_microvm_auth_token)
        """

    async def create_microvm_image(
        self, **kwargs: Unpack[CreateMicrovmImageRequestTypeDef]
    ) -> CreateMicrovmImageResponseTypeDef:
        """
        Creates a MicroVM image from the specified code artifact and base image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/create_microvm_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#create_microvm_image)
        """

    async def create_microvm_shell_auth_token(
        self, **kwargs: Unpack[CreateMicrovmShellAuthTokenRequestTypeDef]
    ) -> CreateMicrovmShellAuthTokenResponseTypeDef:
        """
        Creates a shell authentication token for interactive shell access to a running
        MicroVM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/create_microvm_shell_auth_token.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#create_microvm_shell_auth_token)
        """

    async def delete_microvm_image(
        self, **kwargs: Unpack[DeleteMicrovmImageInputTypeDef]
    ) -> DeleteMicrovmImageOutputTypeDef:
        """
        Deletes a MicroVM image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/delete_microvm_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#delete_microvm_image)
        """

    async def delete_microvm_image_version(
        self, **kwargs: Unpack[DeleteMicrovmImageVersionInputTypeDef]
    ) -> DeleteMicrovmImageVersionOutputTypeDef:
        """
        Deletes a specific version of a MicroVM image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/delete_microvm_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#delete_microvm_image_version)
        """

    async def get_microvm(
        self, **kwargs: Unpack[GetMicrovmRequestTypeDef]
    ) -> GetMicrovmResponseTypeDef:
        """
        Retrieves the details of a specific MicroVM, including its state, endpoint,
        image information, and configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_microvm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_microvm)
        """

    async def get_microvm_image(
        self, **kwargs: Unpack[GetMicrovmImageInputTypeDef]
    ) -> GetMicrovmImageOutputTypeDef:
        """
        Retrieves the details of a MicroVM image, including its state, versions, and
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_microvm_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_microvm_image)
        """

    async def get_microvm_image_build(
        self, **kwargs: Unpack[GetMicrovmImageBuildInputTypeDef]
    ) -> GetMicrovmImageBuildOutputTypeDef:
        """
        Retrieves the details of a specific MicroVM image build, including its state,
        target architecture, and snapshot information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_microvm_image_build.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_microvm_image_build)
        """

    async def get_microvm_image_version(
        self, **kwargs: Unpack[GetMicrovmImageVersionInputTypeDef]
    ) -> GetMicrovmImageVersionOutputTypeDef:
        """
        Retrieves the details of a specific version of a MicroVM image, including its
        configuration, state, and build information.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_microvm_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_microvm_image_version)
        """

    async def list_managed_microvm_image_versions(
        self, **kwargs: Unpack[ListManagedMicrovmImageVersionsInputTypeDef]
    ) -> ListManagedMicrovmImageVersionsOutputTypeDef:
        """
        Lists versions of a managed MicroVM image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_managed_microvm_image_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_managed_microvm_image_versions)
        """

    async def list_managed_microvm_images(
        self, **kwargs: Unpack[ListManagedMicrovmImagesInputTypeDef]
    ) -> ListManagedMicrovmImagesOutputTypeDef:
        """
        Lists AWS managed MicroVM images available for use as base images.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_managed_microvm_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_managed_microvm_images)
        """

    async def list_microvm_image_builds(
        self, **kwargs: Unpack[ListMicrovmImageBuildsInputTypeDef]
    ) -> ListMicrovmImageBuildsOutputTypeDef:
        """
        Lists builds for a MicroVM image version with optional filtering by
        architecture and chipset.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_microvm_image_builds.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_microvm_image_builds)
        """

    async def list_microvm_image_versions(
        self, **kwargs: Unpack[ListMicrovmImageVersionsInputTypeDef]
    ) -> ListMicrovmImageVersionsOutputTypeDef:
        """
        Lists versions of a MicroVM image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_microvm_image_versions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_microvm_image_versions)
        """

    async def list_microvm_images(
        self, **kwargs: Unpack[ListMicrovmImagesRequestTypeDef]
    ) -> ListMicrovmImagesResponseTypeDef:
        """
        Lists MicroVM images in the account with optional name filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_microvm_images.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_microvm_images)
        """

    async def list_microvms(
        self, **kwargs: Unpack[ListMicrovmsRequestTypeDef]
    ) -> ListMicrovmsResponseTypeDef:
        """
        Lists MicroVMs in the account with optional filtering by image and version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_microvms.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_microvms)
        """

    async def list_tags(self, **kwargs: Unpack[ListTagsRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Lists the tags associated with a Lambda MicroVM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/list_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#list_tags)
        """

    async def resume_microvm(self, **kwargs: Unpack[ResumeMicrovmRequestTypeDef]) -> dict[str, Any]:
        """
        Resumes a suspended MicroVM, restoring it to RUNNING state with all state
        intact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/resume_microvm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#resume_microvm)
        """

    async def run_microvm(
        self, **kwargs: Unpack[RunMicrovmRequestTypeDef]
    ) -> RunMicrovmResponseTypeDef:
        """
        Runs a new MicroVM from the specified image.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/run_microvm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#run_microvm)
        """

    async def suspend_microvm(
        self, **kwargs: Unpack[SuspendMicrovmRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Suspends a running MicroVM, preserving its full memory and disk state.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/suspend_microvm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#suspend_microvm)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a Lambda MicroVM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#tag_resource)
        """

    async def terminate_microvm(
        self, **kwargs: Unpack[TerminateMicrovmRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Terminates a MicroVM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/terminate_microvm.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#terminate_microvm)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a Lambda MicroVM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#untag_resource)
        """

    async def update_microvm_image(
        self, **kwargs: Unpack[UpdateMicrovmImageRequestTypeDef]
    ) -> UpdateMicrovmImageResponseTypeDef:
        """
        Updates the configuration of a MicroVM image and triggers a new version build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/update_microvm_image.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#update_microvm_image)
        """

    async def update_microvm_image_version(
        self, **kwargs: Unpack[UpdateMicrovmImageVersionRequestTypeDef]
    ) -> UpdateMicrovmImageVersionResponseTypeDef:
        """
        Updates the status of a specific MicroVM image version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/update_microvm_image_version.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#update_microvm_image_version)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_microvm_image_versions"]
    ) -> ListManagedMicrovmImageVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_managed_microvm_images"]
    ) -> ListManagedMicrovmImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_microvm_image_builds"]
    ) -> ListMicrovmImageBuildsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_microvm_image_versions"]
    ) -> ListMicrovmImageVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_microvm_images"]
    ) -> ListMicrovmImagesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_microvms"]
    ) -> ListMicrovmsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms.html#LambdaMicroVMs.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-microvms.html#LambdaMicroVMs.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/client/)
        """
