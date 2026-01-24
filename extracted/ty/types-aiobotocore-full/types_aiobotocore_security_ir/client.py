"""
Type annotations for security-ir service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_security_ir.client import SecurityIncidentResponseClient

    session = get_session()
    async with session.create_client("security-ir") as client:
        client: SecurityIncidentResponseClient
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
    ListCaseEditsPaginator,
    ListCasesPaginator,
    ListCommentsPaginator,
    ListInvestigationsPaginator,
    ListMembershipsPaginator,
)
from .type_defs import (
    BatchGetMemberAccountDetailsRequestTypeDef,
    BatchGetMemberAccountDetailsResponseTypeDef,
    CancelMembershipRequestTypeDef,
    CancelMembershipResponseTypeDef,
    CloseCaseRequestTypeDef,
    CloseCaseResponseTypeDef,
    CreateCaseCommentRequestTypeDef,
    CreateCaseCommentResponseTypeDef,
    CreateCaseRequestTypeDef,
    CreateCaseResponseTypeDef,
    CreateMembershipRequestTypeDef,
    CreateMembershipResponseTypeDef,
    GetCaseAttachmentDownloadUrlRequestTypeDef,
    GetCaseAttachmentDownloadUrlResponseTypeDef,
    GetCaseAttachmentUploadUrlRequestTypeDef,
    GetCaseAttachmentUploadUrlResponseTypeDef,
    GetCaseRequestTypeDef,
    GetCaseResponseTypeDef,
    GetMembershipRequestTypeDef,
    GetMembershipResponseTypeDef,
    ListCaseEditsRequestTypeDef,
    ListCaseEditsResponseTypeDef,
    ListCasesRequestTypeDef,
    ListCasesResponseTypeDef,
    ListCommentsRequestTypeDef,
    ListCommentsResponseTypeDef,
    ListInvestigationsRequestTypeDef,
    ListInvestigationsResponseTypeDef,
    ListMembershipsRequestTypeDef,
    ListMembershipsResponseTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    SendFeedbackRequestTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateCaseCommentRequestTypeDef,
    UpdateCaseCommentResponseTypeDef,
    UpdateCaseRequestTypeDef,
    UpdateCaseStatusRequestTypeDef,
    UpdateCaseStatusResponseTypeDef,
    UpdateMembershipRequestTypeDef,
    UpdateResolverTypeRequestTypeDef,
    UpdateResolverTypeResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("SecurityIncidentResponseClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidTokenException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    SecurityIncidentResponseNotActiveException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SecurityIncidentResponseClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir.html#SecurityIncidentResponse.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityIncidentResponseClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir.html#SecurityIncidentResponse.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#generate_presigned_url)
        """

    async def batch_get_member_account_details(
        self, **kwargs: Unpack[BatchGetMemberAccountDetailsRequestTypeDef]
    ) -> BatchGetMemberAccountDetailsResponseTypeDef:
        """
        Provides information on whether the supplied account IDs are associated with a
        membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/batch_get_member_account_details.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#batch_get_member_account_details)
        """

    async def cancel_membership(
        self, **kwargs: Unpack[CancelMembershipRequestTypeDef]
    ) -> CancelMembershipResponseTypeDef:
        """
        Cancels an existing membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/cancel_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#cancel_membership)
        """

    async def close_case(
        self, **kwargs: Unpack[CloseCaseRequestTypeDef]
    ) -> CloseCaseResponseTypeDef:
        """
        Closes an existing case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/close_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#close_case)
        """

    async def create_case(
        self, **kwargs: Unpack[CreateCaseRequestTypeDef]
    ) -> CreateCaseResponseTypeDef:
        """
        Creates a new case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/create_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#create_case)
        """

    async def create_case_comment(
        self, **kwargs: Unpack[CreateCaseCommentRequestTypeDef]
    ) -> CreateCaseCommentResponseTypeDef:
        """
        Adds a comment to an existing case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/create_case_comment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#create_case_comment)
        """

    async def create_membership(
        self, **kwargs: Unpack[CreateMembershipRequestTypeDef]
    ) -> CreateMembershipResponseTypeDef:
        """
        Creates a new membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/create_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#create_membership)
        """

    async def get_case(self, **kwargs: Unpack[GetCaseRequestTypeDef]) -> GetCaseResponseTypeDef:
        """
        Returns the attributes of a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_case)
        """

    async def get_case_attachment_download_url(
        self, **kwargs: Unpack[GetCaseAttachmentDownloadUrlRequestTypeDef]
    ) -> GetCaseAttachmentDownloadUrlResponseTypeDef:
        """
        Returns a Pre-Signed URL for uploading attachments into a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_case_attachment_download_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_case_attachment_download_url)
        """

    async def get_case_attachment_upload_url(
        self, **kwargs: Unpack[GetCaseAttachmentUploadUrlRequestTypeDef]
    ) -> GetCaseAttachmentUploadUrlResponseTypeDef:
        """
        Uploads an attachment to a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_case_attachment_upload_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_case_attachment_upload_url)
        """

    async def get_membership(
        self, **kwargs: Unpack[GetMembershipRequestTypeDef]
    ) -> GetMembershipResponseTypeDef:
        """
        Returns the attributes of a membership.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_membership)
        """

    async def list_case_edits(
        self, **kwargs: Unpack[ListCaseEditsRequestTypeDef]
    ) -> ListCaseEditsResponseTypeDef:
        """
        Views the case history for edits made to a designated case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_case_edits.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#list_case_edits)
        """

    async def list_cases(
        self, **kwargs: Unpack[ListCasesRequestTypeDef]
    ) -> ListCasesResponseTypeDef:
        """
        Lists all cases the requester has access to.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_cases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#list_cases)
        """

    async def list_comments(
        self, **kwargs: Unpack[ListCommentsRequestTypeDef]
    ) -> ListCommentsResponseTypeDef:
        """
        Returns comments for a designated case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_comments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#list_comments)
        """

    async def list_investigations(
        self, **kwargs: Unpack[ListInvestigationsRequestTypeDef]
    ) -> ListInvestigationsResponseTypeDef:
        """
        Investigation performed by an agent for a security incident...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_investigations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#list_investigations)
        """

    async def list_memberships(
        self, **kwargs: Unpack[ListMembershipsRequestTypeDef]
    ) -> ListMembershipsResponseTypeDef:
        """
        Returns the memberships that the calling principal can access.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_memberships.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#list_memberships)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns currently configured tags on a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#list_tags_for_resource)
        """

    async def send_feedback(self, **kwargs: Unpack[SendFeedbackRequestTypeDef]) -> dict[str, Any]:
        """
        Send feedback based on response investigation action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/send_feedback.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#send_feedback)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds a tag(s) to a designated resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes a tag(s) from a designate resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#untag_resource)
        """

    async def update_case(self, **kwargs: Unpack[UpdateCaseRequestTypeDef]) -> dict[str, Any]:
        """
        Updates an existing case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_case.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#update_case)
        """

    async def update_case_comment(
        self, **kwargs: Unpack[UpdateCaseCommentRequestTypeDef]
    ) -> UpdateCaseCommentResponseTypeDef:
        """
        Updates an existing case comment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_case_comment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#update_case_comment)
        """

    async def update_case_status(
        self, **kwargs: Unpack[UpdateCaseStatusRequestTypeDef]
    ) -> UpdateCaseStatusResponseTypeDef:
        """
        Updates the state transitions for a designated cases.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_case_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#update_case_status)
        """

    async def update_membership(
        self, **kwargs: Unpack[UpdateMembershipRequestTypeDef]
    ) -> dict[str, Any]:
        """
        Updates membership configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_membership.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#update_membership)
        """

    async def update_resolver_type(
        self, **kwargs: Unpack[UpdateResolverTypeRequestTypeDef]
    ) -> UpdateResolverTypeResponseTypeDef:
        """
        Updates the resolver type for a case.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/update_resolver_type.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#update_resolver_type)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_case_edits"]
    ) -> ListCaseEditsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_cases"]
    ) -> ListCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_comments"]
    ) -> ListCommentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_investigations"]
    ) -> ListInvestigationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memberships"]
    ) -> ListMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir.html#SecurityIncidentResponse.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/security-ir.html#SecurityIncidentResponse.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_security_ir/client/)
        """
