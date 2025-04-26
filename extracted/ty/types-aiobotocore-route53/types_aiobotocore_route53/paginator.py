"""
Type annotations for route53 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_route53.client import Route53Client
    from types_aiobotocore_route53.paginator import (
        ListCidrBlocksPaginator,
        ListCidrCollectionsPaginator,
        ListCidrLocationsPaginator,
        ListHealthChecksPaginator,
        ListHostedZonesPaginator,
        ListQueryLoggingConfigsPaginator,
        ListResourceRecordSetsPaginator,
        ListVPCAssociationAuthorizationsPaginator,
    )

    session = get_session()
    with session.create_client("route53") as client:
        client: Route53Client

        list_cidr_blocks_paginator: ListCidrBlocksPaginator = client.get_paginator("list_cidr_blocks")
        list_cidr_collections_paginator: ListCidrCollectionsPaginator = client.get_paginator("list_cidr_collections")
        list_cidr_locations_paginator: ListCidrLocationsPaginator = client.get_paginator("list_cidr_locations")
        list_health_checks_paginator: ListHealthChecksPaginator = client.get_paginator("list_health_checks")
        list_hosted_zones_paginator: ListHostedZonesPaginator = client.get_paginator("list_hosted_zones")
        list_query_logging_configs_paginator: ListQueryLoggingConfigsPaginator = client.get_paginator("list_query_logging_configs")
        list_resource_record_sets_paginator: ListResourceRecordSetsPaginator = client.get_paginator("list_resource_record_sets")
        list_vpc_association_authorizations_paginator: ListVPCAssociationAuthorizationsPaginator = client.get_paginator("list_vpc_association_authorizations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCidrBlocksRequestPaginateTypeDef,
    ListCidrBlocksResponseTypeDef,
    ListCidrCollectionsRequestPaginateTypeDef,
    ListCidrCollectionsResponseTypeDef,
    ListCidrLocationsRequestPaginateTypeDef,
    ListCidrLocationsResponseTypeDef,
    ListHealthChecksRequestPaginateTypeDef,
    ListHealthChecksResponseTypeDef,
    ListHostedZonesRequestPaginateTypeDef,
    ListHostedZonesResponseTypeDef,
    ListQueryLoggingConfigsRequestPaginateTypeDef,
    ListQueryLoggingConfigsResponseTypeDef,
    ListResourceRecordSetsRequestPaginateTypeDef,
    ListResourceRecordSetsResponseTypeDef,
    ListVPCAssociationAuthorizationsRequestPaginateTypeDef,
    ListVPCAssociationAuthorizationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCidrBlocksPaginator",
    "ListCidrCollectionsPaginator",
    "ListCidrLocationsPaginator",
    "ListHealthChecksPaginator",
    "ListHostedZonesPaginator",
    "ListQueryLoggingConfigsPaginator",
    "ListResourceRecordSetsPaginator",
    "ListVPCAssociationAuthorizationsPaginator",
)


if TYPE_CHECKING:
    _ListCidrBlocksPaginatorBase = AioPaginator[ListCidrBlocksResponseTypeDef]
else:
    _ListCidrBlocksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCidrBlocksPaginator(_ListCidrBlocksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrBlocks.html#Route53.Paginator.ListCidrBlocks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listcidrblockspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCidrBlocksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCidrBlocksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrBlocks.html#Route53.Paginator.ListCidrBlocks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listcidrblockspaginator)
        """


if TYPE_CHECKING:
    _ListCidrCollectionsPaginatorBase = AioPaginator[ListCidrCollectionsResponseTypeDef]
else:
    _ListCidrCollectionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCidrCollectionsPaginator(_ListCidrCollectionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrCollections.html#Route53.Paginator.ListCidrCollections)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listcidrcollectionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCidrCollectionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCidrCollectionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrCollections.html#Route53.Paginator.ListCidrCollections.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listcidrcollectionspaginator)
        """


if TYPE_CHECKING:
    _ListCidrLocationsPaginatorBase = AioPaginator[ListCidrLocationsResponseTypeDef]
else:
    _ListCidrLocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCidrLocationsPaginator(_ListCidrLocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrLocations.html#Route53.Paginator.ListCidrLocations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listcidrlocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCidrLocationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCidrLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListCidrLocations.html#Route53.Paginator.ListCidrLocations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listcidrlocationspaginator)
        """


if TYPE_CHECKING:
    _ListHealthChecksPaginatorBase = AioPaginator[ListHealthChecksResponseTypeDef]
else:
    _ListHealthChecksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHealthChecksPaginator(_ListHealthChecksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHealthChecks.html#Route53.Paginator.ListHealthChecks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhealthcheckspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHealthChecksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHealthChecksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHealthChecks.html#Route53.Paginator.ListHealthChecks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhealthcheckspaginator)
        """


if TYPE_CHECKING:
    _ListHostedZonesPaginatorBase = AioPaginator[ListHostedZonesResponseTypeDef]
else:
    _ListHostedZonesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListHostedZonesPaginator(_ListHostedZonesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHostedZones.html#Route53.Paginator.ListHostedZones)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhostedzonespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHostedZonesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHostedZonesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListHostedZones.html#Route53.Paginator.ListHostedZones.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listhostedzonespaginator)
        """


if TYPE_CHECKING:
    _ListQueryLoggingConfigsPaginatorBase = AioPaginator[ListQueryLoggingConfigsResponseTypeDef]
else:
    _ListQueryLoggingConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListQueryLoggingConfigsPaginator(_ListQueryLoggingConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListQueryLoggingConfigs.html#Route53.Paginator.ListQueryLoggingConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listqueryloggingconfigspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueryLoggingConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueryLoggingConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListQueryLoggingConfigs.html#Route53.Paginator.ListQueryLoggingConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listqueryloggingconfigspaginator)
        """


if TYPE_CHECKING:
    _ListResourceRecordSetsPaginatorBase = AioPaginator[ListResourceRecordSetsResponseTypeDef]
else:
    _ListResourceRecordSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceRecordSetsPaginator(_ListResourceRecordSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListResourceRecordSets.html#Route53.Paginator.ListResourceRecordSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listresourcerecordsetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceRecordSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceRecordSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListResourceRecordSets.html#Route53.Paginator.ListResourceRecordSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listresourcerecordsetspaginator)
        """


if TYPE_CHECKING:
    _ListVPCAssociationAuthorizationsPaginatorBase = AioPaginator[
        ListVPCAssociationAuthorizationsResponseTypeDef
    ]
else:
    _ListVPCAssociationAuthorizationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVPCAssociationAuthorizationsPaginator(_ListVPCAssociationAuthorizationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListVPCAssociationAuthorizations.html#Route53.Paginator.ListVPCAssociationAuthorizations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listvpcassociationauthorizationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVPCAssociationAuthorizationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVPCAssociationAuthorizationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/route53/paginator/ListVPCAssociationAuthorizations.html#Route53.Paginator.ListVPCAssociationAuthorizations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_route53/paginators/#listvpcassociationauthorizationspaginator)
        """
