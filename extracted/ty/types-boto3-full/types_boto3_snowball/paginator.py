"""
Type annotations for snowball service client paginators.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from types_boto3_snowball.client import SnowballClient
    from types_boto3_snowball.paginator import (
        DescribeAddressesPaginator,
        ListClusterJobsPaginator,
        ListClustersPaginator,
        ListCompatibleImagesPaginator,
        ListJobsPaginator,
        ListLongTermPricingPaginator,
    )

    session = Session()
    client: SnowballClient = session.client("snowball")

    describe_addresses_paginator: DescribeAddressesPaginator = client.get_paginator("describe_addresses")
    list_cluster_jobs_paginator: ListClusterJobsPaginator = client.get_paginator("list_cluster_jobs")
    list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
    list_compatible_images_paginator: ListCompatibleImagesPaginator = client.get_paginator("list_compatible_images")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_long_term_pricing_paginator: ListLongTermPricingPaginator = client.get_paginator("list_long_term_pricing")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeAddressesRequestPaginateTypeDef,
    DescribeAddressesResultTypeDef,
    ListClusterJobsRequestPaginateTypeDef,
    ListClusterJobsResultTypeDef,
    ListClustersRequestPaginateTypeDef,
    ListClustersResultTypeDef,
    ListCompatibleImagesRequestPaginateTypeDef,
    ListCompatibleImagesResultTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResultTypeDef,
    ListLongTermPricingRequestPaginateTypeDef,
    ListLongTermPricingResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAddressesPaginator",
    "ListClusterJobsPaginator",
    "ListClustersPaginator",
    "ListCompatibleImagesPaginator",
    "ListJobsPaginator",
    "ListLongTermPricingPaginator",
)


if TYPE_CHECKING:
    _DescribeAddressesPaginatorBase = Paginator[DescribeAddressesResultTypeDef]
else:
    _DescribeAddressesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeAddressesPaginator(_DescribeAddressesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/DescribeAddresses.html#Snowball.Paginator.DescribeAddresses)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#describeaddressespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAddressesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeAddressesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/DescribeAddresses.html#Snowball.Paginator.DescribeAddresses.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#describeaddressespaginator)
        """


if TYPE_CHECKING:
    _ListClusterJobsPaginatorBase = Paginator[ListClusterJobsResultTypeDef]
else:
    _ListClusterJobsPaginatorBase = Paginator  # type: ignore[assignment]


class ListClusterJobsPaginator(_ListClusterJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusterJobs.html#Snowball.Paginator.ListClusterJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listclusterjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClusterJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListClusterJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusterJobs.html#Snowball.Paginator.ListClusterJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listclusterjobspaginator)
        """


if TYPE_CHECKING:
    _ListClustersPaginatorBase = Paginator[ListClustersResultTypeDef]
else:
    _ListClustersPaginatorBase = Paginator  # type: ignore[assignment]


class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusters.html#Snowball.Paginator.ListClusters)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> PageIterator[ListClustersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListClusters.html#Snowball.Paginator.ListClusters.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listclusterspaginator)
        """


if TYPE_CHECKING:
    _ListCompatibleImagesPaginatorBase = Paginator[ListCompatibleImagesResultTypeDef]
else:
    _ListCompatibleImagesPaginatorBase = Paginator  # type: ignore[assignment]


class ListCompatibleImagesPaginator(_ListCompatibleImagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListCompatibleImages.html#Snowball.Paginator.ListCompatibleImages)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listcompatibleimagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCompatibleImagesRequestPaginateTypeDef]
    ) -> PageIterator[ListCompatibleImagesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListCompatibleImages.html#Snowball.Paginator.ListCompatibleImages.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listcompatibleimagespaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = Paginator[ListJobsResultTypeDef]
else:
    _ListJobsPaginatorBase = Paginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListJobs.html#Snowball.Paginator.ListJobs)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> PageIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListJobs.html#Snowball.Paginator.ListJobs.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListLongTermPricingPaginatorBase = Paginator[ListLongTermPricingResultTypeDef]
else:
    _ListLongTermPricingPaginatorBase = Paginator  # type: ignore[assignment]


class ListLongTermPricingPaginator(_ListLongTermPricingPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListLongTermPricing.html#Snowball.Paginator.ListLongTermPricing)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listlongtermpricingpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLongTermPricingRequestPaginateTypeDef]
    ) -> PageIterator[ListLongTermPricingResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/snowball/paginator/ListLongTermPricing.html#Snowball.Paginator.ListLongTermPricing.paginate)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snowball/paginators/#listlongtermpricingpaginator)
        """
