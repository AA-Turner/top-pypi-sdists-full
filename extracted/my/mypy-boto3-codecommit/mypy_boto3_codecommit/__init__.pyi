"""
Main interface for codecommit service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_codecommit/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_codecommit import (
        Client,
        CodeCommitClient,
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

from .client import CodeCommitClient
from .paginator import (
    DescribePullRequestEventsPaginator,
    GetCommentsForComparedCommitPaginator,
    GetCommentsForPullRequestPaginator,
    GetDifferencesPaginator,
    ListBranchesPaginator,
    ListPullRequestsPaginator,
    ListRepositoriesPaginator,
)

Client = CodeCommitClient

__all__ = (
    "Client",
    "CodeCommitClient",
    "DescribePullRequestEventsPaginator",
    "GetCommentsForComparedCommitPaginator",
    "GetCommentsForPullRequestPaginator",
    "GetDifferencesPaginator",
    "ListBranchesPaginator",
    "ListPullRequestsPaginator",
    "ListRepositoriesPaginator",
)
