"""
Type annotations for supportauthz service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_supportauthz.client import SupportAuthZClient

    session = Session()
    client: SupportAuthZClient = session.client("supportauthz")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListActionsPaginator,
    ListSupportPermitRequestsPaginator,
    ListSupportPermitsPaginator,
)
from .type_defs import (
    CreateSupportPermitInputTypeDef,
    CreateSupportPermitOutputTypeDef,
    DeleteSupportPermitInputTypeDef,
    DeleteSupportPermitOutputTypeDef,
    GetActionInputTypeDef,
    GetActionOutputTypeDef,
    GetSupportPermitInputTypeDef,
    GetSupportPermitOutputTypeDef,
    ListActionsInputTypeDef,
    ListActionsOutputTypeDef,
    ListSupportPermitRequestsInputTypeDef,
    ListSupportPermitRequestsOutputTypeDef,
    ListSupportPermitsInputTypeDef,
    ListSupportPermitsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    RejectSupportPermitRequestInputTypeDef,
    RejectSupportPermitRequestOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SupportAuthZClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SupportAuthZClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz.html#SupportAuthZ.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SupportAuthZClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz.html#SupportAuthZ.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#generate_presigned_url)
        """

    def create_support_permit(
        self, **kwargs: Unpack[CreateSupportPermitInputTypeDef]
    ) -> CreateSupportPermitOutputTypeDef:
        """
        Creates a support permit that authorizes an AWS support operator to perform
        specified actions on specified resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/create_support_permit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#create_support_permit)
        """

    def delete_support_permit(
        self, **kwargs: Unpack[DeleteSupportPermitInputTypeDef]
    ) -> DeleteSupportPermitOutputTypeDef:
        """
        Deletes a support permit, revoking the authorization previously granted to the
        AWS support operator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/delete_support_permit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#delete_support_permit)
        """

    def get_action(self, **kwargs: Unpack[GetActionInputTypeDef]) -> GetActionOutputTypeDef:
        """
        Retrieves the description of a specific support action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_action.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#get_action)
        """

    def get_support_permit(
        self, **kwargs: Unpack[GetSupportPermitInputTypeDef]
    ) -> GetSupportPermitOutputTypeDef:
        """
        Retrieves the details of a support permit by its ARN or name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_support_permit.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#get_support_permit)
        """

    def list_actions(self, **kwargs: Unpack[ListActionsInputTypeDef]) -> ListActionsOutputTypeDef:
        """
        Lists available support actions for a specified AWS service.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_actions.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#list_actions)
        """

    def list_support_permit_requests(
        self, **kwargs: Unpack[ListSupportPermitRequestsInputTypeDef]
    ) -> ListSupportPermitRequestsOutputTypeDef:
        """
        Lists permit requests from AWS support operators.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_support_permit_requests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#list_support_permit_requests)
        """

    def list_support_permits(
        self, **kwargs: Unpack[ListSupportPermitsInputTypeDef]
    ) -> ListSupportPermitsOutputTypeDef:
        """
        Lists all support permits in the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_support_permits.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#list_support_permits)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with a support permit resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#list_tags_for_resource)
        """

    def reject_support_permit_request(
        self, **kwargs: Unpack[RejectSupportPermitRequestInputTypeDef]
    ) -> RejectSupportPermitRequestOutputTypeDef:
        """
        Rejects a permit request from an AWS support operator.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/reject_support_permit_request.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#reject_support_permit_request)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds or overwrites one or more tags for a support permit resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes one or more tags from a support permit resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_actions"]
    ) -> ListActionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_support_permit_requests"]
    ) -> ListSupportPermitRequestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_support_permits"]
    ) -> ListSupportPermitsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supportauthz/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supportauthz/client/#get_paginator)
        """
