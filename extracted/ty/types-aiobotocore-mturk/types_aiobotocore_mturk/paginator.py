"""
Type annotations for mturk service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mturk.client import MTurkClient
    from types_aiobotocore_mturk.paginator import (
        ListAssignmentsForHITPaginator,
        ListBonusPaymentsPaginator,
        ListHITsForQualificationTypePaginator,
        ListHITsPaginator,
        ListQualificationRequestsPaginator,
        ListQualificationTypesPaginator,
        ListReviewableHITsPaginator,
        ListWorkerBlocksPaginator,
        ListWorkersWithQualificationTypePaginator,
    )

    session = get_session()
    with session.create_client("mturk") as client:
        client: MTurkClient

        list_assignments_for_hit_paginator: ListAssignmentsForHITPaginator = client.get_paginator("list_assignments_for_hit")
        list_bonus_payments_paginator: ListBonusPaymentsPaginator = client.get_paginator("list_bonus_payments")
        list_hits_for_qualification_type_paginator: ListHITsForQualificationTypePaginator = client.get_paginator("list_hits_for_qualification_type")
        list_hits_paginator: ListHITsPaginator = client.get_paginator("list_hits")
        list_qualification_requests_paginator: ListQualificationRequestsPaginator = client.get_paginator("list_qualification_requests")
        list_qualification_types_paginator: ListQualificationTypesPaginator = client.get_paginator("list_qualification_types")
        list_reviewable_hits_paginator: ListReviewableHITsPaginator = client.get_paginator("list_reviewable_hits")
        list_worker_blocks_paginator: ListWorkerBlocksPaginator = client.get_paginator("list_worker_blocks")
        list_workers_with_qualification_type_paginator: ListWorkersWithQualificationTypePaginator = client.get_paginator("list_workers_with_qualification_type")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssignmentsForHITRequestPaginateTypeDef,
    ListAssignmentsForHITResponseTypeDef,
    ListBonusPaymentsRequestPaginateTypeDef,
    ListBonusPaymentsResponseTypeDef,
    ListHITsForQualificationTypeRequestPaginateTypeDef,
    ListHITsForQualificationTypeResponseTypeDef,
    ListHITsRequestPaginateTypeDef,
    ListHITsResponseTypeDef,
    ListQualificationRequestsRequestPaginateTypeDef,
    ListQualificationRequestsResponseTypeDef,
    ListQualificationTypesRequestPaginateTypeDef,
    ListQualificationTypesResponseTypeDef,
    ListReviewableHITsRequestPaginateTypeDef,
    ListReviewableHITsResponseTypeDef,
    ListWorkerBlocksRequestPaginateTypeDef,
    ListWorkerBlocksResponseTypeDef,
    ListWorkersWithQualificationTypeRequestPaginateTypeDef,
    ListWorkersWithQualificationTypeResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssignmentsForHITPaginator",
    "ListBonusPaymentsPaginator",
    "ListHITsForQualificationTypePaginator",
    "ListHITsPaginator",
    "ListQualificationRequestsPaginator",
    "ListQualificationTypesPaginator",
    "ListReviewableHITsPaginator",
    "ListWorkerBlocksPaginator",
    "ListWorkersWithQualificationTypePaginator",
)


if TYPE_CHECKING:
    _ListAssignmentsForHITPaginatorBase = AioPaginator[ListAssignmentsForHITResponseTypeDef]
else:
    _ListAssignmentsForHITPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssignmentsForHITPaginator(_ListAssignmentsForHITPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListAssignmentsForHIT.html#MTurk.Paginator.ListAssignmentsForHIT)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listassignmentsforhitpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssignmentsForHITRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssignmentsForHITResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListAssignmentsForHIT.html#MTurk.Paginator.ListAssignmentsForHIT.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listassignmentsforhitpaginator)
        """


if TYPE_CHECKING:
    _ListBonusPaymentsPaginatorBase = AioPaginator[ListBonusPaymentsResponseTypeDef]
else:
    _ListBonusPaymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBonusPaymentsPaginator(_ListBonusPaymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListBonusPayments.html#MTurk.Paginator.ListBonusPayments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listbonuspaymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBonusPaymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBonusPaymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListBonusPayments.html#MTurk.Paginator.ListBonusPayments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listbonuspaymentspaginator)
        """


if TYPE_CHECKING:
    _ListHITsForQualificationTypePaginatorBase = AioPaginator[
        ListHITsForQualificationTypeResponseTypeDef
    ]
else:
    _ListHITsForQualificationTypePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHITsForQualificationTypePaginator(_ListHITsForQualificationTypePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListHITsForQualificationType.html#MTurk.Paginator.ListHITsForQualificationType)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitsforqualificationtypepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHITsForQualificationTypeRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHITsForQualificationTypeResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListHITsForQualificationType.html#MTurk.Paginator.ListHITsForQualificationType.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitsforqualificationtypepaginator)
        """


if TYPE_CHECKING:
    _ListHITsPaginatorBase = AioPaginator[ListHITsResponseTypeDef]
else:
    _ListHITsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHITsPaginator(_ListHITsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListHITs.html#MTurk.Paginator.ListHITs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHITsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHITsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListHITs.html#MTurk.Paginator.ListHITs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listhitspaginator)
        """


if TYPE_CHECKING:
    _ListQualificationRequestsPaginatorBase = AioPaginator[ListQualificationRequestsResponseTypeDef]
else:
    _ListQualificationRequestsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQualificationRequestsPaginator(_ListQualificationRequestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListQualificationRequests.html#MTurk.Paginator.ListQualificationRequests)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationrequestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQualificationRequestsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQualificationRequestsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListQualificationRequests.html#MTurk.Paginator.ListQualificationRequests.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationrequestspaginator)
        """


if TYPE_CHECKING:
    _ListQualificationTypesPaginatorBase = AioPaginator[ListQualificationTypesResponseTypeDef]
else:
    _ListQualificationTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQualificationTypesPaginator(_ListQualificationTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListQualificationTypes.html#MTurk.Paginator.ListQualificationTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationtypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQualificationTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQualificationTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListQualificationTypes.html#MTurk.Paginator.ListQualificationTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listqualificationtypespaginator)
        """


if TYPE_CHECKING:
    _ListReviewableHITsPaginatorBase = AioPaginator[ListReviewableHITsResponseTypeDef]
else:
    _ListReviewableHITsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListReviewableHITsPaginator(_ListReviewableHITsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListReviewableHITs.html#MTurk.Paginator.ListReviewableHITs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listreviewablehitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReviewableHITsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReviewableHITsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListReviewableHITs.html#MTurk.Paginator.ListReviewableHITs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listreviewablehitspaginator)
        """


if TYPE_CHECKING:
    _ListWorkerBlocksPaginatorBase = AioPaginator[ListWorkerBlocksResponseTypeDef]
else:
    _ListWorkerBlocksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkerBlocksPaginator(_ListWorkerBlocksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListWorkerBlocks.html#MTurk.Paginator.ListWorkerBlocks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerblockspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkerBlocksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkerBlocksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListWorkerBlocks.html#MTurk.Paginator.ListWorkerBlocks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerblockspaginator)
        """


if TYPE_CHECKING:
    _ListWorkersWithQualificationTypePaginatorBase = AioPaginator[
        ListWorkersWithQualificationTypeResponseTypeDef
    ]
else:
    _ListWorkersWithQualificationTypePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkersWithQualificationTypePaginator(_ListWorkersWithQualificationTypePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListWorkersWithQualificationType.html#MTurk.Paginator.ListWorkersWithQualificationType)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerswithqualificationtypepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkersWithQualificationTypeRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkersWithQualificationTypeResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mturk/paginator/ListWorkersWithQualificationType.html#MTurk.Paginator.ListWorkersWithQualificationType.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mturk/paginators/#listworkerswithqualificationtypepaginator)
        """
