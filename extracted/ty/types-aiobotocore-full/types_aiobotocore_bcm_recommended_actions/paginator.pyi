"""
Type annotations for bcm-recommended-actions service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_recommended_actions/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bcm_recommended_actions.client import BillingandCostManagementRecommendedActionsClient
    from types_aiobotocore_bcm_recommended_actions.paginator import (
        ListRecommendedActionsPaginator,
    )

    session = get_session()
    with session.create_client("bcm-recommended-actions") as client:
        client: BillingandCostManagementRecommendedActionsClient

        list_recommended_actions_paginator: ListRecommendedActionsPaginator = client.get_paginator("list_recommended_actions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListRecommendedActionsRequestPaginateTypeDef,
    ListRecommendedActionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRecommendedActionsPaginator",)

if TYPE_CHECKING:
    _ListRecommendedActionsPaginatorBase = AioPaginator[ListRecommendedActionsResponseTypeDef]
else:
    _ListRecommendedActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRecommendedActionsPaginator(_ListRecommendedActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-recommended-actions/paginator/ListRecommendedActions.html#BillingandCostManagementRecommendedActions.Paginator.ListRecommendedActions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_recommended_actions/paginators/#listrecommendedactionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecommendedActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecommendedActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bcm-recommended-actions/paginator/ListRecommendedActions.html#BillingandCostManagementRecommendedActions.Paginator.ListRecommendedActions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bcm_recommended_actions/paginators/#listrecommendedactionspaginator)
        """
