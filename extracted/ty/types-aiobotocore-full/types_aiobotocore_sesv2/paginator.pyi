"""
Type annotations for sesv2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sesv2.client import SESV2Client
    from types_aiobotocore_sesv2.paginator import (
        ListMultiRegionEndpointsPaginator,
        ListReputationEntitiesPaginator,
        ListResourceTenantsPaginator,
        ListTenantResourcesPaginator,
        ListTenantsPaginator,
    )

    session = get_session()
    with session.create_client("sesv2") as client:
        client: SESV2Client

        list_multi_region_endpoints_paginator: ListMultiRegionEndpointsPaginator = client.get_paginator("list_multi_region_endpoints")
        list_reputation_entities_paginator: ListReputationEntitiesPaginator = client.get_paginator("list_reputation_entities")
        list_resource_tenants_paginator: ListResourceTenantsPaginator = client.get_paginator("list_resource_tenants")
        list_tenant_resources_paginator: ListTenantResourcesPaginator = client.get_paginator("list_tenant_resources")
        list_tenants_paginator: ListTenantsPaginator = client.get_paginator("list_tenants")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListMultiRegionEndpointsRequestPaginateTypeDef,
    ListMultiRegionEndpointsResponseTypeDef,
    ListReputationEntitiesRequestPaginateTypeDef,
    ListReputationEntitiesResponseTypeDef,
    ListResourceTenantsRequestPaginateTypeDef,
    ListResourceTenantsResponseTypeDef,
    ListTenantResourcesRequestPaginateTypeDef,
    ListTenantResourcesResponseTypeDef,
    ListTenantsRequestPaginateTypeDef,
    ListTenantsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListMultiRegionEndpointsPaginator",
    "ListReputationEntitiesPaginator",
    "ListResourceTenantsPaginator",
    "ListTenantResourcesPaginator",
    "ListTenantsPaginator",
)

if TYPE_CHECKING:
    _ListMultiRegionEndpointsPaginatorBase = AioPaginator[ListMultiRegionEndpointsResponseTypeDef]
else:
    _ListMultiRegionEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMultiRegionEndpointsPaginator(_ListMultiRegionEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listmultiregionendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMultiRegionEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMultiRegionEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListMultiRegionEndpoints.html#SESV2.Paginator.ListMultiRegionEndpoints.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listmultiregionendpointspaginator)
        """

if TYPE_CHECKING:
    _ListReputationEntitiesPaginatorBase = AioPaginator[ListReputationEntitiesResponseTypeDef]
else:
    _ListReputationEntitiesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReputationEntitiesPaginator(_ListReputationEntitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListReputationEntities.html#SESV2.Paginator.ListReputationEntities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listreputationentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReputationEntitiesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReputationEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListReputationEntities.html#SESV2.Paginator.ListReputationEntities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listreputationentitiespaginator)
        """

if TYPE_CHECKING:
    _ListResourceTenantsPaginatorBase = AioPaginator[ListResourceTenantsResponseTypeDef]
else:
    _ListResourceTenantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceTenantsPaginator(_ListResourceTenantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListResourceTenants.html#SESV2.Paginator.ListResourceTenants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listresourcetenantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTenantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceTenantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListResourceTenants.html#SESV2.Paginator.ListResourceTenants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listresourcetenantspaginator)
        """

if TYPE_CHECKING:
    _ListTenantResourcesPaginatorBase = AioPaginator[ListTenantResourcesResponseTypeDef]
else:
    _ListTenantResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTenantResourcesPaginator(_ListTenantResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListTenantResources.html#SESV2.Paginator.ListTenantResources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listtenantresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTenantResourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTenantResourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListTenantResources.html#SESV2.Paginator.ListTenantResources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listtenantresourcespaginator)
        """

if TYPE_CHECKING:
    _ListTenantsPaginatorBase = AioPaginator[ListTenantsResponseTypeDef]
else:
    _ListTenantsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTenantsPaginator(_ListTenantsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListTenants.html#SESV2.Paginator.ListTenants)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listtenantspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTenantsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTenantsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sesv2/paginator/ListTenants.html#SESV2.Paginator.ListTenants.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sesv2/paginators/#listtenantspaginator)
        """
