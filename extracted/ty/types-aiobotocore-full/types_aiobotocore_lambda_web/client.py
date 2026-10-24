"""
Type annotations for lambda-web service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lambda_web.client import LambdaWebClient

    session = get_session()
    async with session.create_client("lambda-web") as client:
        client: LambdaWebClient
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
    ListWebFunctionEndpointsPaginator,
    ListWebFunctionRevisionsPaginator,
    ListWebFunctionsPaginator,
)
from .type_defs import (
    CreateWebFunctionEndpointRequestTypeDef,
    CreateWebFunctionEndpointResponseTypeDef,
    CreateWebFunctionRequestTypeDef,
    CreateWebFunctionResponseTypeDef,
    CreateWebFunctionRevisionRequestTypeDef,
    CreateWebFunctionRevisionResponseTypeDef,
    DeleteResourcePolicyRequestTypeDef,
    DeleteWebFunctionEndpointRequestTypeDef,
    DeleteWebFunctionRequestTypeDef,
    DeleteWebFunctionRevisionRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetResourcePolicyRequestTypeDef,
    GetResourcePolicyResponseTypeDef,
    GetWebAccountSettingsResponseTypeDef,
    GetWebFunctionEndpointRequestTypeDef,
    GetWebFunctionEndpointResponseTypeDef,
    GetWebFunctionRequestTypeDef,
    GetWebFunctionResponseTypeDef,
    GetWebFunctionRevisionRequestTypeDef,
    GetWebFunctionRevisionResponseTypeDef,
    ListTagsRequestTypeDef,
    ListTagsResponseTypeDef,
    ListWebFunctionEndpointsRequestTypeDef,
    ListWebFunctionEndpointsResponseTypeDef,
    ListWebFunctionRevisionsRequestTypeDef,
    ListWebFunctionRevisionsResponseTypeDef,
    ListWebFunctionsRequestTypeDef,
    ListWebFunctionsResponseTypeDef,
    PutResourcePolicyRequestTypeDef,
    PutResourcePolicyResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateWebFunctionEndpointRequestTypeDef,
    UpdateWebFunctionEndpointResponseTypeDef,
)
from .waiter import (
    WebFunctionActiveWaiter,
    WebFunctionDeletedWaiter,
    WebFunctionEndpointActiveWaiter,
    WebFunctionEndpointDeletedWaiter,
    WebFunctionEndpointUpdatedWaiter,
    WebFunctionRevisionActiveWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("LambdaWebClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class LambdaWebClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web.html#LambdaWeb.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LambdaWebClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web.html#LambdaWeb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#generate_presigned_url)
        """

    async def create_web_function(
        self, **kwargs: Unpack[CreateWebFunctionRequestTypeDef]
    ) -> CreateWebFunctionResponseTypeDef:
        """
        Creates a web function with an initial revision and endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/create_web_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#create_web_function)
        """

    async def create_web_function_endpoint(
        self, **kwargs: Unpack[CreateWebFunctionEndpointRequestTypeDef]
    ) -> CreateWebFunctionEndpointResponseTypeDef:
        """
        Creates an endpoint for a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/create_web_function_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#create_web_function_endpoint)
        """

    async def create_web_function_revision(
        self, **kwargs: Unpack[CreateWebFunctionRevisionRequestTypeDef]
    ) -> CreateWebFunctionRevisionResponseTypeDef:
        """
        Creates an immutable revision for a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/create_web_function_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#create_web_function_revision)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the resource-based policy from a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/delete_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#delete_resource_policy)
        """

    async def delete_web_function(
        self, **kwargs: Unpack[DeleteWebFunctionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a web function and all of its associated revisions and endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/delete_web_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#delete_web_function)
        """

    async def delete_web_function_endpoint(
        self, **kwargs: Unpack[DeleteWebFunctionEndpointRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a web function endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/delete_web_function_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#delete_web_function_endpoint)
        """

    async def delete_web_function_revision(
        self, **kwargs: Unpack[DeleteWebFunctionRevisionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a web function revision.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/delete_web_function_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#delete_web_function_revision)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyRequestTypeDef]
    ) -> GetResourcePolicyResponseTypeDef:
        """
        Retrieves the resource-based policy attached to a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_resource_policy)
        """

    async def get_web_account_settings(self) -> GetWebAccountSettingsResponseTypeDef:
        """
        Retrieves details about your AWS Lambda Web Functions account settings for the
        current AWS Region, including the quotas that apply to web functions and your
        current usage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_web_account_settings.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_web_account_settings)
        """

    async def get_web_function(
        self, **kwargs: Unpack[GetWebFunctionRequestTypeDef]
    ) -> GetWebFunctionResponseTypeDef:
        """
        Retrieves details about a web function, including its current state and
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_web_function.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_web_function)
        """

    async def get_web_function_endpoint(
        self, **kwargs: Unpack[GetWebFunctionEndpointRequestTypeDef]
    ) -> GetWebFunctionEndpointResponseTypeDef:
        """
        Retrieves details about a web function endpoint, including its current state,
        configuration, and domain name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_web_function_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_web_function_endpoint)
        """

    async def get_web_function_revision(
        self, **kwargs: Unpack[GetWebFunctionRevisionRequestTypeDef]
    ) -> GetWebFunctionRevisionResponseTypeDef:
        """
        Retrieves details about a web function revision, including its state and
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_web_function_revision.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_web_function_revision)
        """

    async def list_tags(self, **kwargs: Unpack[ListTagsRequestTypeDef]) -> ListTagsResponseTypeDef:
        """
        Returns a list of tags applied to a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/list_tags.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#list_tags)
        """

    async def list_web_function_endpoints(
        self, **kwargs: Unpack[ListWebFunctionEndpointsRequestTypeDef]
    ) -> ListWebFunctionEndpointsResponseTypeDef:
        """
        Lists endpoints for a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/list_web_function_endpoints.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#list_web_function_endpoints)
        """

    async def list_web_function_revisions(
        self, **kwargs: Unpack[ListWebFunctionRevisionsRequestTypeDef]
    ) -> ListWebFunctionRevisionsResponseTypeDef:
        """
        Lists revisions for a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/list_web_function_revisions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#list_web_function_revisions)
        """

    async def list_web_functions(
        self, **kwargs: Unpack[ListWebFunctionsRequestTypeDef]
    ) -> ListWebFunctionsResponseTypeDef:
        """
        Lists web functions in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/list_web_functions.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#list_web_functions)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyRequestTypeDef]
    ) -> PutResourcePolicyResponseTypeDef:
        """
        Adds or updates a resource-based policy on a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/put_resource_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#put_resource_policy)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds tags to a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a web function.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#untag_resource)
        """

    async def update_web_function_endpoint(
        self, **kwargs: Unpack[UpdateWebFunctionEndpointRequestTypeDef]
    ) -> UpdateWebFunctionEndpointResponseTypeDef:
        """
        Updates the configuration of a web function endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/update_web_function_endpoint.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#update_web_function_endpoint)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_web_function_endpoints"]
    ) -> ListWebFunctionEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_web_function_revisions"]
    ) -> ListWebFunctionRevisionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_web_functions"]
    ) -> ListWebFunctionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["web_function_active"]
    ) -> WebFunctionActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["web_function_deleted"]
    ) -> WebFunctionDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["web_function_endpoint_active"]
    ) -> WebFunctionEndpointActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["web_function_endpoint_deleted"]
    ) -> WebFunctionEndpointDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["web_function_endpoint_updated"]
    ) -> WebFunctionEndpointUpdatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["web_function_revision_active"]
    ) -> WebFunctionRevisionActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web.html#LambdaWeb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda-web.html#LambdaWeb.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_web/client/)
        """
