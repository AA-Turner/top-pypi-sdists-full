"""
Main interface for partnercentral-benefits service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_partnercentral_benefits/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_partnercentral_benefits import (
        Client,
        ListBenefitAllocationsPaginator,
        ListBenefitApplicationsPaginator,
        ListBenefitsPaginator,
        PartnerCentralBenefitsClient,
    )

    session = get_session()
    async with session.create_client("partnercentral-benefits") as client:
        client: PartnerCentralBenefitsClient
        ...


    list_benefit_allocations_paginator: ListBenefitAllocationsPaginator = client.get_paginator("list_benefit_allocations")
    list_benefit_applications_paginator: ListBenefitApplicationsPaginator = client.get_paginator("list_benefit_applications")
    list_benefits_paginator: ListBenefitsPaginator = client.get_paginator("list_benefits")
    ```
"""

from .client import PartnerCentralBenefitsClient
from .paginator import (
    ListBenefitAllocationsPaginator,
    ListBenefitApplicationsPaginator,
    ListBenefitsPaginator,
)

Client = PartnerCentralBenefitsClient


__all__ = (
    "Client",
    "ListBenefitAllocationsPaginator",
    "ListBenefitApplicationsPaginator",
    "ListBenefitsPaginator",
    "PartnerCentralBenefitsClient",
)
