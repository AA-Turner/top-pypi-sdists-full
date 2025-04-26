"""
Type annotations for supplychain service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_supplychain.client import SupplyChainClient
    from mypy_boto3_supplychain.paginator import (
        ListDataIntegrationFlowsPaginator,
        ListDataLakeDatasetsPaginator,
        ListInstancesPaginator,
    )

    session = Session()
    client: SupplyChainClient = session.client("supplychain")

    list_data_integration_flows_paginator: ListDataIntegrationFlowsPaginator = client.get_paginator("list_data_integration_flows")
    list_data_lake_datasets_paginator: ListDataLakeDatasetsPaginator = client.get_paginator("list_data_lake_datasets")
    list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

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
    _ListDataIntegrationFlowsPaginatorBase = Paginator[ListDataIntegrationFlowsResponseTypeDef]
else:
    _ListDataIntegrationFlowsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataIntegrationFlowsPaginator(_ListDataIntegrationFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataIntegrationFlowsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataIntegrationFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataIntegrationFlows.html#SupplyChain.Paginator.ListDataIntegrationFlows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdataintegrationflowspaginator)
        """

if TYPE_CHECKING:
    _ListDataLakeDatasetsPaginatorBase = Paginator[ListDataLakeDatasetsResponseTypeDef]
else:
    _ListDataLakeDatasetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDataLakeDatasetsPaginator(_ListDataLakeDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakedatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataLakeDatasetsRequestPaginateTypeDef]
    ) -> PageIterator[ListDataLakeDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListDataLakeDatasets.html#SupplyChain.Paginator.ListDataLakeDatasets.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listdatalakedatasetspaginator)
        """

if TYPE_CHECKING:
    _ListInstancesPaginatorBase = Paginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = Paginator  # type: ignore[assignment]

class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> PageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/supplychain/paginator/ListInstances.html#SupplyChain.Paginator.ListInstances.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/paginators/#listinstancespaginator)
        """
