"""
Type annotations for cloudfront service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_cloudfront.client import CloudFrontClient
    from mypy_boto3_cloudfront.paginator import (
        ListCloudFrontOriginAccessIdentitiesPaginator,
        ListDistributionsPaginator,
        ListInvalidationsPaginator,
        ListKeyValueStoresPaginator,
        ListPublicKeysPaginator,
        ListStreamingDistributionsPaginator,
    )

    session = Session()
    client: CloudFrontClient = session.client("cloudfront")

    list_cloud_front_origin_access_identities_paginator: ListCloudFrontOriginAccessIdentitiesPaginator = client.get_paginator("list_cloud_front_origin_access_identities")
    list_distributions_paginator: ListDistributionsPaginator = client.get_paginator("list_distributions")
    list_invalidations_paginator: ListInvalidationsPaginator = client.get_paginator("list_invalidations")
    list_key_value_stores_paginator: ListKeyValueStoresPaginator = client.get_paginator("list_key_value_stores")
    list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    list_streaming_distributions_paginator: ListStreamingDistributionsPaginator = client.get_paginator("list_streaming_distributions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCloudFrontOriginAccessIdentitiesRequestPaginateTypeDef,
    ListCloudFrontOriginAccessIdentitiesResultTypeDef,
    ListDistributionsRequestPaginateTypeDef,
    ListDistributionsResultTypeDef,
    ListInvalidationsRequestPaginateTypeDef,
    ListInvalidationsResultTypeDef,
    ListKeyValueStoresRequestPaginateTypeDef,
    ListKeyValueStoresResultTypeDef,
    ListPublicKeysRequestPaginateTypeDef,
    ListPublicKeysResultTypeDef,
    ListStreamingDistributionsRequestPaginateTypeDef,
    ListStreamingDistributionsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCloudFrontOriginAccessIdentitiesPaginator",
    "ListDistributionsPaginator",
    "ListInvalidationsPaginator",
    "ListKeyValueStoresPaginator",
    "ListPublicKeysPaginator",
    "ListStreamingDistributionsPaginator",
)

if TYPE_CHECKING:
    _ListCloudFrontOriginAccessIdentitiesPaginatorBase = Paginator[
        ListCloudFrontOriginAccessIdentitiesResultTypeDef
    ]
else:
    _ListCloudFrontOriginAccessIdentitiesPaginatorBase = Paginator  # type: ignore[assignment]

class ListCloudFrontOriginAccessIdentitiesPaginator(
    _ListCloudFrontOriginAccessIdentitiesPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListCloudFrontOriginAccessIdentities.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listcloudfrontoriginaccessidentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudFrontOriginAccessIdentitiesRequestPaginateTypeDef]
    ) -> PageIterator[ListCloudFrontOriginAccessIdentitiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListCloudFrontOriginAccessIdentities.html#CloudFront.Paginator.ListCloudFrontOriginAccessIdentities.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listcloudfrontoriginaccessidentitiespaginator)
        """

if TYPE_CHECKING:
    _ListDistributionsPaginatorBase = Paginator[ListDistributionsResultTypeDef]
else:
    _ListDistributionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDistributionsPaginator(_ListDistributionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListDistributions.html#CloudFront.Paginator.ListDistributions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listdistributionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDistributionsRequestPaginateTypeDef]
    ) -> PageIterator[ListDistributionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListDistributions.html#CloudFront.Paginator.ListDistributions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listdistributionspaginator)
        """

if TYPE_CHECKING:
    _ListInvalidationsPaginatorBase = Paginator[ListInvalidationsResultTypeDef]
else:
    _ListInvalidationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListInvalidationsPaginator(_ListInvalidationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListInvalidations.html#CloudFront.Paginator.ListInvalidations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listinvalidationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvalidationsRequestPaginateTypeDef]
    ) -> PageIterator[ListInvalidationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListInvalidations.html#CloudFront.Paginator.ListInvalidations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listinvalidationspaginator)
        """

if TYPE_CHECKING:
    _ListKeyValueStoresPaginatorBase = Paginator[ListKeyValueStoresResultTypeDef]
else:
    _ListKeyValueStoresPaginatorBase = Paginator  # type: ignore[assignment]

class ListKeyValueStoresPaginator(_ListKeyValueStoresPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListKeyValueStores.html#CloudFront.Paginator.ListKeyValueStores)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listkeyvaluestorespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListKeyValueStoresRequestPaginateTypeDef]
    ) -> PageIterator[ListKeyValueStoresResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListKeyValueStores.html#CloudFront.Paginator.ListKeyValueStores.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listkeyvaluestorespaginator)
        """

if TYPE_CHECKING:
    _ListPublicKeysPaginatorBase = Paginator[ListPublicKeysResultTypeDef]
else:
    _ListPublicKeysPaginatorBase = Paginator  # type: ignore[assignment]

class ListPublicKeysPaginator(_ListPublicKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListPublicKeys.html#CloudFront.Paginator.ListPublicKeys)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listpublickeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPublicKeysRequestPaginateTypeDef]
    ) -> PageIterator[ListPublicKeysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListPublicKeys.html#CloudFront.Paginator.ListPublicKeys.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#listpublickeyspaginator)
        """

if TYPE_CHECKING:
    _ListStreamingDistributionsPaginatorBase = Paginator[ListStreamingDistributionsResultTypeDef]
else:
    _ListStreamingDistributionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListStreamingDistributionsPaginator(_ListStreamingDistributionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListStreamingDistributions.html#CloudFront.Paginator.ListStreamingDistributions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#liststreamingdistributionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamingDistributionsRequestPaginateTypeDef]
    ) -> PageIterator[ListStreamingDistributionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudfront/paginator/ListStreamingDistributions.html#CloudFront.Paginator.ListStreamingDistributions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_cloudfront/paginators/#liststreamingdistributionspaginator)
        """
