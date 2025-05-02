"""
Type annotations for supplychain service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_supplychain.client import SupplyChainClient
    from types_aiobotocore_supplychain.paginator import (
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListInstancesPaginator,
    )

    session = get_session()
    with session.create_client("supplychain") as client:
        client: SupplyChainClient

        list_data_integration_flows_paginator: ListDataIntegrationFlowsPaginator = client.get_paginator("list_data_integration_flows")
        list_data_lake_datasets_paginator: ListDataLakeDatasetsPaginator = client.get_paginator("list_data_lake_datasets")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDataIntegrationFlowsRequestPaginateTypeDef,
    ListDataIntegrationFlowsResponseTypeDef,
    ListDataLakeDatasetsRequestPaginateTypeDef,
    ListDataLakeDatasetsResponseTypeDef,
    ListInstancesRequestPaginateTypeDef,
    ListInstancesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListDataIntegrationFlowsPaginator",
    "ListDataLakeDatasetsPaginator",
    "ListInstancesPaginator",
)


if TYPE_CHECKING:
    _ListDataIntegrationFlowsPaginatorBase = AioPaginator[ListDataIntegrationFlowsResponseTypeDef]
else:
    _ListDataIntegrationFlowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataIntegrationFlowsPaginator(_ListDataIntegrationFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataIntegrationFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdataintegrationflowspaginator)
        """


if TYPE_CHECKING:
    _ListDataLakeDatasetsPaginatorBase = AioPaginator[ListDataLakeDatasetsResponseTypeDef]
else:
    _ListDataLakeDatasetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataLakeDatasetsPaginator(_ListDataLakeDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakedatasetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataLakeDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listdatalakedatasetspaginator)
        """


if TYPE_CHECKING:
    _ListInstancesPaginatorBase = AioPaginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_supplychain/paginators/#listinstancespaginator)
        """
