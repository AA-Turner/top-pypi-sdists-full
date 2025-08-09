"""
Type annotations for outposts service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_outposts.client import OutpostsClient
    from types_aiobotocore_outposts.paginator import (
        GetOutpostBillingInformationPaginator,
        GetOutpostInstanceTypesPaginator,
        GetOutpostSupportedInstanceTypesPaginator,
        ListAssetInstancesPaginator,
        ListAssetsPaginator,
        ListBlockingInstancesForCapacityTaskPaginator,
        ListCapacityTasksPaginator,
        ListCatalogItemsPaginator,
        ListOrdersPaginator,
        ListOutpostsPaginator,
        ListSitesPaginator,
    )

    session = get_session()
    with session.create_client("outposts") as client:
        client: OutpostsClient

        get_outpost_billing_information_paginator: GetOutpostBillingInformationPaginator = client.get_paginator("get_outpost_billing_information")
        get_outpost_instance_types_paginator: GetOutpostInstanceTypesPaginator = client.get_paginator("get_outpost_instance_types")
        get_outpost_supported_instance_types_paginator: GetOutpostSupportedInstanceTypesPaginator = client.get_paginator("get_outpost_supported_instance_types")
        list_asset_instances_paginator: ListAssetInstancesPaginator = client.get_paginator("list_asset_instances")
        list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
        list_blocking_instances_for_capacity_task_paginator: ListBlockingInstancesForCapacityTaskPaginator = client.get_paginator("list_blocking_instances_for_capacity_task")
        list_capacity_tasks_paginator: ListCapacityTasksPaginator = client.get_paginator("list_capacity_tasks")
        list_catalog_items_paginator: ListCatalogItemsPaginator = client.get_paginator("list_catalog_items")
        list_orders_paginator: ListOrdersPaginator = client.get_paginator("list_orders")
        list_outposts_paginator: ListOutpostsPaginator = client.get_paginator("list_outposts")
        list_sites_paginator: ListSitesPaginator = client.get_paginator("list_sites")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetOutpostBillingInformationInputPaginateTypeDef,
    GetOutpostBillingInformationOutputTypeDef,
    GetOutpostInstanceTypesInputPaginateTypeDef,
    GetOutpostInstanceTypesOutputTypeDef,
    GetOutpostSupportedInstanceTypesInputPaginateTypeDef,
    GetOutpostSupportedInstanceTypesOutputTypeDef,
    ListAssetInstancesInputPaginateTypeDef,
    ListAssetInstancesOutputTypeDef,
    ListAssetsInputPaginateTypeDef,
    ListAssetsOutputTypeDef,
    ListBlockingInstancesForCapacityTaskInputPaginateTypeDef,
    ListBlockingInstancesForCapacityTaskOutputTypeDef,
    ListCapacityTasksInputPaginateTypeDef,
    ListCapacityTasksOutputTypeDef,
    ListCatalogItemsInputPaginateTypeDef,
    ListCatalogItemsOutputTypeDef,
    ListOrdersInputPaginateTypeDef,
    ListOrdersOutputTypeDef,
    ListOutpostsInputPaginateTypeDef,
    ListOutpostsOutputTypeDef,
    ListSitesInputPaginateTypeDef,
    ListSitesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetOutpostBillingInformationPaginator",
    "GetOutpostInstanceTypesPaginator",
    "GetOutpostSupportedInstanceTypesPaginator",
    "ListAssetInstancesPaginator",
    "ListAssetsPaginator",
    "ListBlockingInstancesForCapacityTaskPaginator",
    "ListCapacityTasksPaginator",
    "ListCatalogItemsPaginator",
    "ListOrdersPaginator",
    "ListOutpostsPaginator",
    "ListSitesPaginator",
)

if TYPE_CHECKING:
    _GetOutpostBillingInformationPaginatorBase = AioPaginator[
        GetOutpostBillingInformationOutputTypeDef
    ]
else:
    _GetOutpostBillingInformationPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetOutpostBillingInformationPaginator(_GetOutpostBillingInformationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostBillingInformation.html#Outposts.Paginator.GetOutpostBillingInformation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostbillinginformationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutpostBillingInformationInputPaginateTypeDef]
    ) -> AioPageIterator[GetOutpostBillingInformationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostBillingInformation.html#Outposts.Paginator.GetOutpostBillingInformation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostbillinginformationpaginator)
        """

if TYPE_CHECKING:
    _GetOutpostInstanceTypesPaginatorBase = AioPaginator[GetOutpostInstanceTypesOutputTypeDef]
else:
    _GetOutpostInstanceTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetOutpostInstanceTypesPaginator(_GetOutpostInstanceTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostInstanceTypes.html#Outposts.Paginator.GetOutpostInstanceTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostinstancetypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutpostInstanceTypesInputPaginateTypeDef]
    ) -> AioPageIterator[GetOutpostInstanceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostInstanceTypes.html#Outposts.Paginator.GetOutpostInstanceTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostinstancetypespaginator)
        """

if TYPE_CHECKING:
    _GetOutpostSupportedInstanceTypesPaginatorBase = AioPaginator[
        GetOutpostSupportedInstanceTypesOutputTypeDef
    ]
else:
    _GetOutpostSupportedInstanceTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetOutpostSupportedInstanceTypesPaginator(_GetOutpostSupportedInstanceTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostSupportedInstanceTypes.html#Outposts.Paginator.GetOutpostSupportedInstanceTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostsupportedinstancetypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOutpostSupportedInstanceTypesInputPaginateTypeDef]
    ) -> AioPageIterator[GetOutpostSupportedInstanceTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/GetOutpostSupportedInstanceTypes.html#Outposts.Paginator.GetOutpostSupportedInstanceTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#getoutpostsupportedinstancetypespaginator)
        """

if TYPE_CHECKING:
    _ListAssetInstancesPaginatorBase = AioPaginator[ListAssetInstancesOutputTypeDef]
else:
    _ListAssetInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetInstancesPaginator(_ListAssetInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssetInstances.html#Outposts.Paginator.ListAssetInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listassetinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAssetInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssetInstances.html#Outposts.Paginator.ListAssetInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listassetinstancespaginator)
        """

if TYPE_CHECKING:
    _ListAssetsPaginatorBase = AioPaginator[ListAssetsOutputTypeDef]
else:
    _ListAssetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAssetsPaginator(_ListAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssets.html#Outposts.Paginator.ListAssets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listassetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAssetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListAssets.html#Outposts.Paginator.ListAssets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listassetspaginator)
        """

if TYPE_CHECKING:
    _ListBlockingInstancesForCapacityTaskPaginatorBase = AioPaginator[
        ListBlockingInstancesForCapacityTaskOutputTypeDef
    ]
else:
    _ListBlockingInstancesForCapacityTaskPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBlockingInstancesForCapacityTaskPaginator(
    _ListBlockingInstancesForCapacityTaskPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListBlockingInstancesForCapacityTask.html#Outposts.Paginator.ListBlockingInstancesForCapacityTask)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listblockinginstancesforcapacitytaskpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBlockingInstancesForCapacityTaskInputPaginateTypeDef]
    ) -> AioPageIterator[ListBlockingInstancesForCapacityTaskOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListBlockingInstancesForCapacityTask.html#Outposts.Paginator.ListBlockingInstancesForCapacityTask.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listblockinginstancesforcapacitytaskpaginator)
        """

if TYPE_CHECKING:
    _ListCapacityTasksPaginatorBase = AioPaginator[ListCapacityTasksOutputTypeDef]
else:
    _ListCapacityTasksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCapacityTasksPaginator(_ListCapacityTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCapacityTasks.html#Outposts.Paginator.ListCapacityTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcapacitytaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCapacityTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListCapacityTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCapacityTasks.html#Outposts.Paginator.ListCapacityTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcapacitytaskspaginator)
        """

if TYPE_CHECKING:
    _ListCatalogItemsPaginatorBase = AioPaginator[ListCatalogItemsOutputTypeDef]
else:
    _ListCatalogItemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCatalogItemsPaginator(_ListCatalogItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCatalogItems.html#Outposts.Paginator.ListCatalogItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcatalogitemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCatalogItemsInputPaginateTypeDef]
    ) -> AioPageIterator[ListCatalogItemsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListCatalogItems.html#Outposts.Paginator.ListCatalogItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listcatalogitemspaginator)
        """

if TYPE_CHECKING:
    _ListOrdersPaginatorBase = AioPaginator[ListOrdersOutputTypeDef]
else:
    _ListOrdersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOrdersPaginator(_ListOrdersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOrders.html#Outposts.Paginator.ListOrders)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listorderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOrdersInputPaginateTypeDef]
    ) -> AioPageIterator[ListOrdersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOrders.html#Outposts.Paginator.ListOrders.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listorderspaginator)
        """

if TYPE_CHECKING:
    _ListOutpostsPaginatorBase = AioPaginator[ListOutpostsOutputTypeDef]
else:
    _ListOutpostsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListOutpostsPaginator(_ListOutpostsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOutposts.html#Outposts.Paginator.ListOutposts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listoutpostspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOutpostsInputPaginateTypeDef]
    ) -> AioPageIterator[ListOutpostsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListOutposts.html#Outposts.Paginator.ListOutposts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listoutpostspaginator)
        """

if TYPE_CHECKING:
    _ListSitesPaginatorBase = AioPaginator[ListSitesOutputTypeDef]
else:
    _ListSitesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSitesPaginator(_ListSitesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListSites.html#Outposts.Paginator.ListSites)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listsitespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSitesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSitesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/outposts/paginator/ListSites.html#Outposts.Paginator.ListSites.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_outposts/paginators/#listsitespaginator)
        """
