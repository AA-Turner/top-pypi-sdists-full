"""
Type annotations for b2bi service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_b2bi.client import B2BIClient
    from types_aiobotocore_b2bi.paginator import (
        ListCapabilitiesPaginator,
        ListPartnershipsPaginator,
        ListProfilesPaginator,
        ListTransformersPaginator,
    )

    session = get_session()
    with session.create_client("b2bi") as client:
        client: B2BIClient

        list_capabilities_paginator: ListCapabilitiesPaginator = client.get_paginator("list_capabilities")
        list_partnerships_paginator: ListPartnershipsPaginator = client.get_paginator("list_partnerships")
        list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
        list_transformers_paginator: ListTransformersPaginator = client.get_paginator("list_transformers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCapabilitiesRequestPaginateTypeDef,
    ListCapabilitiesResponseTypeDef,
    ListPartnershipsRequestPaginateTypeDef,
    ListPartnershipsResponseTypeDef,
    ListProfilesRequestPaginateTypeDef,
    ListProfilesResponseTypeDef,
    ListTransformersRequestPaginateTypeDef,
    ListTransformersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCapabilitiesPaginator",
    "ListPartnershipsPaginator",
    "ListProfilesPaginator",
    "ListTransformersPaginator",
)

if TYPE_CHECKING:
    _ListCapabilitiesPaginatorBase = AioPaginator[ListCapabilitiesResponseTypeDef]
else:
    _ListCapabilitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCapabilitiesPaginator(_ListCapabilitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListCapabilities.html#B2BI.Paginator.ListCapabilities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listcapabilitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCapabilitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCapabilitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListCapabilities.html#B2BI.Paginator.ListCapabilities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listcapabilitiespaginator)
        """

if TYPE_CHECKING:
    _ListPartnershipsPaginatorBase = AioPaginator[ListPartnershipsResponseTypeDef]
else:
    _ListPartnershipsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPartnershipsPaginator(_ListPartnershipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListPartnerships.html#B2BI.Paginator.ListPartnerships)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listpartnershipspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPartnershipsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPartnershipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListPartnerships.html#B2BI.Paginator.ListPartnerships.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listpartnershipspaginator)
        """

if TYPE_CHECKING:
    _ListProfilesPaginatorBase = AioPaginator[ListProfilesResponseTypeDef]
else:
    _ListProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProfilesPaginator(_ListProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListProfiles.html#B2BI.Paginator.ListProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListProfiles.html#B2BI.Paginator.ListProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listprofilespaginator)
        """

if TYPE_CHECKING:
    _ListTransformersPaginatorBase = AioPaginator[ListTransformersResponseTypeDef]
else:
    _ListTransformersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTransformersPaginator(_ListTransformersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListTransformers.html#B2BI.Paginator.ListTransformers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listtransformerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTransformersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTransformersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/b2bi/paginator/ListTransformers.html#B2BI.Paginator.ListTransformers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/paginators/#listtransformerspaginator)
        """
