"""
Type annotations for codecommit service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codecommit.client import CodeCommitClient
    from types_aiobotocore_codecommit.paginator import (
        DescribePullRequestEventsPaginator,
        GetCommentsForComparedCommitPaginator,
        GetCommentsForPullRequestPaginator,
        GetDifferencesPaginator,
        ListBranchesPaginator,
        ListPullRequestsPaginator,
        ListRepositoriesPaginator,
    )

    session = get_session()
    with session.create_client("codecommit") as client:
        client: CodeCommitClient

        describe_pull_request_events_paginator: DescribePullRequestEventsPaginator = client.get_paginator("describe_pull_request_events")
        get_comments_for_compared_commit_paginator: GetCommentsForComparedCommitPaginator = client.get_paginator("get_comments_for_compared_commit")
        get_comments_for_pull_request_paginator: GetCommentsForPullRequestPaginator = client.get_paginator("get_comments_for_pull_request")
        get_differences_paginator: GetDifferencesPaginator = client.get_paginator("get_differences")
        list_branches_paginator: ListBranchesPaginator = client.get_paginator("list_branches")
        list_pull_requests_paginator: ListPullRequestsPaginator = client.get_paginator("list_pull_requests")
        list_repositories_paginator: ListRepositoriesPaginator = client.get_paginator("list_repositories")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribePullRequestEventsInputPaginateTypeDef,
    DescribePullRequestEventsOutputTypeDef,
    GetCommentsForComparedCommitInputPaginateTypeDef,
    GetCommentsForComparedCommitOutputTypeDef,
    GetCommentsForPullRequestInputPaginateTypeDef,
    GetCommentsForPullRequestOutputTypeDef,
    GetDifferencesInputPaginateTypeDef,
    GetDifferencesOutputTypeDef,
    ListBranchesInputPaginateTypeDef,
    ListBranchesOutputTypeDef,
    ListPullRequestsInputPaginateTypeDef,
    ListPullRequestsOutputTypeDef,
    ListRepositoriesInputPaginateTypeDef,
    ListRepositoriesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribePullRequestEventsPaginator",
    "GetCommentsForComparedCommitPaginator",
    "GetCommentsForPullRequestPaginator",
    "GetDifferencesPaginator",
    "ListBranchesPaginator",
    "ListPullRequestsPaginator",
    "ListRepositoriesPaginator",
)


if TYPE_CHECKING:
    _DescribePullRequestEventsPaginatorBase = AioPaginator[DescribePullRequestEventsOutputTypeDef]
else:
    _DescribePullRequestEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePullRequestEventsPaginator(_DescribePullRequestEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#describepullrequesteventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePullRequestEventsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribePullRequestEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#describepullrequesteventspaginator)
        """


if TYPE_CHECKING:
    _GetCommentsForComparedCommitPaginatorBase = AioPaginator[
        GetCommentsForComparedCommitOutputTypeDef
    ]
else:
    _GetCommentsForComparedCommitPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCommentsForComparedCommitPaginator(_GetCommentsForComparedCommitPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCommentsForComparedCommitInputPaginateTypeDef]
    ) -> AioPageIterator[GetCommentsForComparedCommitOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
        """


if TYPE_CHECKING:
    _GetCommentsForPullRequestPaginatorBase = AioPaginator[GetCommentsForPullRequestOutputTypeDef]
else:
    _GetCommentsForPullRequestPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetCommentsForPullRequestPaginator(_GetCommentsForPullRequestPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforpullrequestpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCommentsForPullRequestInputPaginateTypeDef]
    ) -> AioPageIterator[GetCommentsForPullRequestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getcommentsforpullrequestpaginator)
        """


if TYPE_CHECKING:
    _GetDifferencesPaginatorBase = AioPaginator[GetDifferencesOutputTypeDef]
else:
    _GetDifferencesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetDifferencesPaginator(_GetDifferencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getdifferencespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDifferencesInputPaginateTypeDef]
    ) -> AioPageIterator[GetDifferencesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#getdifferencespaginator)
        """


if TYPE_CHECKING:
    _ListBranchesPaginatorBase = AioPaginator[ListBranchesOutputTypeDef]
else:
    _ListBranchesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBranchesPaginator(_ListBranchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listbranchespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBranchesInputPaginateTypeDef]
    ) -> AioPageIterator[ListBranchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listbranchespaginator)
        """


if TYPE_CHECKING:
    _ListPullRequestsPaginatorBase = AioPaginator[ListPullRequestsOutputTypeDef]
else:
    _ListPullRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPullRequestsPaginator(_ListPullRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listpullrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPullRequestsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPullRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listpullrequestspaginator)
        """


if TYPE_CHECKING:
    _ListRepositoriesPaginatorBase = AioPaginator[ListRepositoriesOutputTypeDef]
else:
    _ListRepositoriesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRepositoriesPaginator(_ListRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listrepositoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositoriesInputPaginateTypeDef]
    ) -> AioPageIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codecommit/paginators/#listrepositoriespaginator)
        """
