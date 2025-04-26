"""
Type annotations for codecommit service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_codecommit.client import CodeCommitClient
    from mypy_boto3_codecommit.paginator import (
        DescribePullRequestEventsPaginator,
        GetCommentsForComparedCommitPaginator,
        GetCommentsForPullRequestPaginator,
        GetDifferencesPaginator,
        ListBranchesPaginator,
        ListPullRequestsPaginator,
        ListRepositoriesPaginator,
    )

    session = Session()
    client: CodeCommitClient = session.client("codecommit")

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

from botocore.paginate import PageIterator, Paginator

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
    _DescribePullRequestEventsPaginatorBase = Paginator[DescribePullRequestEventsOutputTypeDef]
else:
    _DescribePullRequestEventsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribePullRequestEventsPaginator(_DescribePullRequestEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#describepullrequesteventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePullRequestEventsInputPaginateTypeDef]
    ) -> PageIterator[DescribePullRequestEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/DescribePullRequestEvents.html#CodeCommit.Paginator.DescribePullRequestEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#describepullrequesteventspaginator)
        """


if TYPE_CHECKING:
    _GetCommentsForComparedCommitPaginatorBase = Paginator[
        GetCommentsForComparedCommitOutputTypeDef
    ]
else:
    _GetCommentsForComparedCommitPaginatorBase = Paginator  # type: ignore[assignment]


class GetCommentsForComparedCommitPaginator(_GetCommentsForComparedCommitPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCommentsForComparedCommitInputPaginateTypeDef]
    ) -> PageIterator[GetCommentsForComparedCommitOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForComparedCommit.html#CodeCommit.Paginator.GetCommentsForComparedCommit.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforcomparedcommitpaginator)
        """


if TYPE_CHECKING:
    _GetCommentsForPullRequestPaginatorBase = Paginator[GetCommentsForPullRequestOutputTypeDef]
else:
    _GetCommentsForPullRequestPaginatorBase = Paginator  # type: ignore[assignment]


class GetCommentsForPullRequestPaginator(_GetCommentsForPullRequestPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforpullrequestpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetCommentsForPullRequestInputPaginateTypeDef]
    ) -> PageIterator[GetCommentsForPullRequestOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetCommentsForPullRequest.html#CodeCommit.Paginator.GetCommentsForPullRequest.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getcommentsforpullrequestpaginator)
        """


if TYPE_CHECKING:
    _GetDifferencesPaginatorBase = Paginator[GetDifferencesOutputTypeDef]
else:
    _GetDifferencesPaginatorBase = Paginator  # type: ignore[assignment]


class GetDifferencesPaginator(_GetDifferencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getdifferencespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetDifferencesInputPaginateTypeDef]
    ) -> PageIterator[GetDifferencesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/GetDifferences.html#CodeCommit.Paginator.GetDifferences.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#getdifferencespaginator)
        """


if TYPE_CHECKING:
    _ListBranchesPaginatorBase = Paginator[ListBranchesOutputTypeDef]
else:
    _ListBranchesPaginatorBase = Paginator  # type: ignore[assignment]


class ListBranchesPaginator(_ListBranchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listbranchespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBranchesInputPaginateTypeDef]
    ) -> PageIterator[ListBranchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListBranches.html#CodeCommit.Paginator.ListBranches.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listbranchespaginator)
        """


if TYPE_CHECKING:
    _ListPullRequestsPaginatorBase = Paginator[ListPullRequestsOutputTypeDef]
else:
    _ListPullRequestsPaginatorBase = Paginator  # type: ignore[assignment]


class ListPullRequestsPaginator(_ListPullRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listpullrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPullRequestsInputPaginateTypeDef]
    ) -> PageIterator[ListPullRequestsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListPullRequests.html#CodeCommit.Paginator.ListPullRequests.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listpullrequestspaginator)
        """


if TYPE_CHECKING:
    _ListRepositoriesPaginatorBase = Paginator[ListRepositoriesOutputTypeDef]
else:
    _ListRepositoriesPaginatorBase = Paginator  # type: ignore[assignment]


class ListRepositoriesPaginator(_ListRepositoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listrepositoriespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositoriesInputPaginateTypeDef]
    ) -> PageIterator[ListRepositoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codecommit/paginator/ListRepositories.html#CodeCommit.Paginator.ListRepositories.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/paginators/#listrepositoriespaginator)
        """
