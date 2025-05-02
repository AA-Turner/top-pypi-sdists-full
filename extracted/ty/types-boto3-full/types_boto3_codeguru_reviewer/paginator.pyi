"""
Type annotations for codeguru-reviewer service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_reviewer/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_codeguru_reviewer.client import CodeGuruReviewerClient
    from types_boto3_codeguru_reviewer.paginator import (
        ListRepositoryAssociationsPaginator,
    )

    session = Session()
    client: CodeGuruReviewerClient = session.client("codeguru-reviewer")

    list_repository_associations_paginator: ListRepositoryAssociationsPaginator = client.get_paginator("list_repository_associations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListRepositoryAssociationsRequestPaginateTypeDef,
    ListRepositoryAssociationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRepositoryAssociationsPaginator",)

if TYPE_CHECKING:
    _ListRepositoryAssociationsPaginatorBase = Paginator[ListRepositoryAssociationsResponseTypeDef]
else:
    _ListRepositoryAssociationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListRepositoryAssociationsPaginator(_ListRepositoryAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/paginator/ListRepositoryAssociations.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_reviewer/paginators/#listrepositoryassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRepositoryAssociationsRequestPaginateTypeDef]
    ) -> PageIterator[ListRepositoryAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguru-reviewer/paginator/ListRepositoryAssociations.html#CodeGuruReviewer.Paginator.ListRepositoryAssociations.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeguru_reviewer/paginators/#listrepositoryassociationspaginator)
        """
