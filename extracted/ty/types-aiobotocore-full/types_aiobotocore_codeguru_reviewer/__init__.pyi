"""
Main interface for codeguru-reviewer service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguru_reviewer/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguru_reviewer import (
        Client,
        CodeGuruReviewerClient,
        CodeReviewCompletedWaiter,
        ListRepositoryAssociationsPaginator,
        RepositoryAssociationSucceededWaiter,
    )

    session = get_session()
    async with session.create_client("codeguru-reviewer") as client:
        client: CodeGuruReviewerClient
        ...


    code_review_completed_waiter: CodeReviewCompletedWaiter = client.get_waiter("code_review_completed")
    repository_association_succeeded_waiter: RepositoryAssociationSucceededWaiter = client.get_waiter("repository_association_succeeded")

    list_repository_associations_paginator: ListRepositoryAssociationsPaginator = client.get_paginator("list_repository_associations")
    ```
"""

from .client import CodeGuruReviewerClient
from .paginator import ListRepositoryAssociationsPaginator
from .waiter import CodeReviewCompletedWaiter, RepositoryAssociationSucceededWaiter

Client = CodeGuruReviewerClient

__all__ = (
    "Client",
    "CodeGuruReviewerClient",
    "CodeReviewCompletedWaiter",
    "ListRepositoryAssociationsPaginator",
    "RepositoryAssociationSucceededWaiter",
)
