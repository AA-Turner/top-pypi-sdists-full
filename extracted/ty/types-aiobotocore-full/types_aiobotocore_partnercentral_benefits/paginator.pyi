"""
Type annotations for partnercentral-benefits service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_partnercentral_benefits.client import PartnerCentralBenefitsClient
    from types_aiobotocore_partnercentral_benefits.paginator import (
        ListBenefitAllocationsPaginator,
        ListBenefitApplicationsPaginator,
        ListBenefitsPaginator,
    )

    session = get_session()
    with session.create_client("partnercentral-benefits") as client:
        client: PartnerCentralBenefitsClient

        list_benefit_allocations_paginator: ListBenefitAllocationsPaginator = client.get_paginator("list_benefit_allocations")
        list_benefit_applications_paginator: ListBenefitApplicationsPaginator = client.get_paginator("list_benefit_applications")
        list_benefits_paginator: ListBenefitsPaginator = client.get_paginator("list_benefits")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListBenefitAllocationsInputPaginateTypeDef,
    ListBenefitAllocationsOutputTypeDef,
    ListBenefitApplicationsInputPaginateTypeDef,
    ListBenefitApplicationsOutputTypeDef,
    ListBenefitsInputPaginateTypeDef,
    ListBenefitsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListBenefitAllocationsPaginator",
    "ListBenefitApplicationsPaginator",
    "ListBenefitsPaginator",
)

if TYPE_CHECKING:
    _ListBenefitAllocationsPaginatorBase = AioPaginator[ListBenefitAllocationsOutputTypeDef]
else:
    _ListBenefitAllocationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBenefitAllocationsPaginator(_ListBenefitAllocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-benefits/paginator/ListBenefitAllocations.html#PartnerCentralBenefits.Paginator.ListBenefitAllocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/#listbenefitallocationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBenefitAllocationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBenefitAllocationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-benefits/paginator/ListBenefitAllocations.html#PartnerCentralBenefits.Paginator.ListBenefitAllocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/#listbenefitallocationspaginator)
        """

if TYPE_CHECKING:
    _ListBenefitApplicationsPaginatorBase = AioPaginator[ListBenefitApplicationsOutputTypeDef]
else:
    _ListBenefitApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBenefitApplicationsPaginator(_ListBenefitApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-benefits/paginator/ListBenefitApplications.html#PartnerCentralBenefits.Paginator.ListBenefitApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/#listbenefitapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBenefitApplicationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBenefitApplicationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-benefits/paginator/ListBenefitApplications.html#PartnerCentralBenefits.Paginator.ListBenefitApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/#listbenefitapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListBenefitsPaginatorBase = AioPaginator[ListBenefitsOutputTypeDef]
else:
    _ListBenefitsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBenefitsPaginator(_ListBenefitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-benefits/paginator/ListBenefits.html#PartnerCentralBenefits.Paginator.ListBenefits)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/#listbenefitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBenefitsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBenefitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/partnercentral-benefits/paginator/ListBenefits.html#PartnerCentralBenefits.Paginator.ListBenefits.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/paginators/#listbenefitspaginator)
        """
