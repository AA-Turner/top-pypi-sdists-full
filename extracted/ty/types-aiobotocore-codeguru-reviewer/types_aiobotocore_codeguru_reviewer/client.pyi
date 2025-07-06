"""
Type annotations for codeguru-reviewer service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguru_reviewer.client import CodeGuruReviewerClient

    session = get_session()
    async with session.create_client("codeguru-reviewer") as client:
        client: CodeGuruReviewerClient
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

from .paginator import ListRepositoryAssociationsPaginator
from .type_defs import (
    AssociateRepositoryRequestTypeDef,
    AssociateRepositoryResponseTypeDef,
    CreateCodeReviewRequestTypeDef,
    CreateCodeReviewResponseTypeDef,
    DescribeCodeReviewRequestTypeDef,
    DescribeCodeReviewResponseTypeDef,
    DescribeRecommendationFeedbackRequestTypeDef,
    DescribeRecommendationFeedbackResponseTypeDef,
    DescribeRepositoryAssociationRequestTypeDef,
    DescribeRepositoryAssociationResponseTypeDef,
    DisassociateRepositoryRequestTypeDef,
    DisassociateRepositoryResponseTypeDef,
    ListCodeReviewsRequestTypeDef,
    ListCodeReviewsResponseTypeDef,
    ListRecommendationFeedbackRequestTypeDef,
    ListRecommendationFeedbackResponseTypeDef,
    ListRecommendationsRequestTypeDef,
    ListRecommendationsResponseTypeDef,
    ListRepositoryAssociationsRequestTypeDef,
    ListRepositoryAssociationsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutRecommendationFeedbackRequestTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)
from .waiter import CodeReviewCompletedWaiter, RepositoryAssociationSucceededWaiter

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

__all__ = ("CodeGuruReviewerClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeGuruReviewerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruReviewerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#generate_presigned_url)
        """

    async def associate_repository(
        self, **kwargs: Unpack[AssociateRepositoryRequestTypeDef]
    ) -> AssociateRepositoryResponseTypeDef:
        """
        Use to associate an Amazon Web Services CodeCommit repository or a repository
        managed by Amazon Web Services CodeStar Connections with Amazon CodeGuru
        Reviewer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/associate_repository.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#associate_repository)
        """

    async def create_code_review(
        self, **kwargs: Unpack[CreateCodeReviewRequestTypeDef]
    ) -> CreateCodeReviewResponseTypeDef:
        """
        Use to create a code review with a <a
        href="https://docs.aws.amazon.com/codeguru/latest/reviewer-api/API_CodeReviewType.html">CodeReviewType</a>
        of <code>RepositoryAnalysis</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/create_code_review.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#create_code_review)
        """

    async def describe_code_review(
        self, **kwargs: Unpack[DescribeCodeReviewRequestTypeDef]
    ) -> DescribeCodeReviewResponseTypeDef:
        """
        Returns the metadata associated with the code review along with its status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/describe_code_review.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#describe_code_review)
        """

    async def describe_recommendation_feedback(
        self, **kwargs: Unpack[DescribeRecommendationFeedbackRequestTypeDef]
    ) -> DescribeRecommendationFeedbackResponseTypeDef:
        """
        Describes the customer feedback for a CodeGuru Reviewer recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/describe_recommendation_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#describe_recommendation_feedback)
        """

    async def describe_repository_association(
        self, **kwargs: Unpack[DescribeRepositoryAssociationRequestTypeDef]
    ) -> DescribeRepositoryAssociationResponseTypeDef:
        """
        Returns a <a
        href="https://docs.aws.amazon.com/codeguru/latest/reviewer-api/API_RepositoryAssociation.html">RepositoryAssociation</a>
        object that contains information about the requested repository association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/describe_repository_association.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#describe_repository_association)
        """

    async def disassociate_repository(
        self, **kwargs: Unpack[DisassociateRepositoryRequestTypeDef]
    ) -> DisassociateRepositoryResponseTypeDef:
        """
        Removes the association between Amazon CodeGuru Reviewer and a repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/disassociate_repository.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#disassociate_repository)
        """

    async def list_code_reviews(
        self, **kwargs: Unpack[ListCodeReviewsRequestTypeDef]
    ) -> ListCodeReviewsResponseTypeDef:
        """
        Lists all the code reviews that the customer has created in the past 90 days.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/list_code_reviews.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#list_code_reviews)
        """

    async def list_recommendation_feedback(
        self, **kwargs: Unpack[ListRecommendationFeedbackRequestTypeDef]
    ) -> ListRecommendationFeedbackResponseTypeDef:
        """
        Returns a list of <a
        href="https://docs.aws.amazon.com/codeguru/latest/reviewer-api/API_RecommendationFeedbackSummary.html">RecommendationFeedbackSummary</a>
        objects that contain customer recommendation feedback for all CodeGuru Reviewer
        users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/list_recommendation_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#list_recommendation_feedback)
        """

    async def list_recommendations(
        self, **kwargs: Unpack[ListRecommendationsRequestTypeDef]
    ) -> ListRecommendationsResponseTypeDef:
        """
        Returns the list of all recommendations for a completed code review.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/list_recommendations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#list_recommendations)
        """

    async def list_repository_associations(
        self, **kwargs: Unpack[ListRepositoryAssociationsRequestTypeDef]
    ) -> ListRepositoryAssociationsResponseTypeDef:
        """
        Returns a list of <a
        href="https://docs.aws.amazon.com/codeguru/latest/reviewer-api/API_RepositoryAssociationSummary.html">RepositoryAssociationSummary</a>
        objects that contain summary information about a repository association.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/list_repository_associations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#list_repository_associations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the list of tags associated with an associated repository resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#list_tags_for_resource)
        """

    async def put_recommendation_feedback(
        self, **kwargs: Unpack[PutRecommendationFeedbackRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Stores customer feedback for a CodeGuru Reviewer recommendation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/put_recommendation_feedback.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#put_recommendation_feedback)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds one or more tags to an associated repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from an associated repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#untag_resource)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_repository_associations"]
    ) -> ListRepositoryAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["code_review_completed"]
    ) -> CodeReviewCompletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["repository_association_succeeded"]
    ) -> RepositoryAssociationSucceededWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer.html#CodeGuruReviewer.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/client/)
        """
