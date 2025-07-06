"""
Type annotations for emr-containers service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_emr_containers.client import EMRContainersClient
    from types_aiobotocore_emr_containers.paginator import (
        ListJobRunsPaginator,
        ListJobTemplatesPaginator,
        ListManagedEndpointsPaginator,
        ListSecurityConfigurationsPaginator,
        ListVirtualClustersPaginator,
    )

    session = get_session()
    with session.create_client("emr-containers") as client:
        client: EMRContainersClient

        list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_managed_endpoints_paginator: ListManagedEndpointsPaginator = client.get_paginator("list_managed_endpoints")
        list_security_configurations_paginator: ListSecurityConfigurationsPaginator = client.get_paginator("list_security_configurations")
        list_virtual_clusters_paginator: ListVirtualClustersPaginator = client.get_paginator("list_virtual_clusters")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListJobRunsRequestPaginateTypeDef,
    ListJobRunsResponsePaginatorTypeDef,
    ListJobRunsResponseTypeDef,
    ListJobTemplatesRequestPaginateTypeDef,
    ListJobTemplatesResponsePaginatorTypeDef,
    ListManagedEndpointsRequestPaginateTypeDef,
    ListManagedEndpointsResponsePaginatorTypeDef,
    ListSecurityConfigurationsRequestPaginateTypeDef,
    ListSecurityConfigurationsResponseTypeDef,
    ListVirtualClustersRequestPaginateTypeDef,
    ListVirtualClustersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListJobRunsPaginator",
    "ListJobTemplatesPaginator",
    "ListManagedEndpointsPaginator",
    "ListSecurityConfigurationsPaginator",
    "ListVirtualClustersPaginator",
)

if TYPE_CHECKING:
    _ListJobRunsPaginatorBase = AioPaginator[ListJobRunsResponseTypeDef]
else:
    _ListJobRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobRunsPaginator(_ListJobRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobRuns.html#EMRContainers.Paginator.ListJobRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobRunsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobRuns.html#EMRContainers.Paginator.ListJobRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobrunspaginator)
        """

if TYPE_CHECKING:
    _ListJobTemplatesPaginatorBase = AioPaginator[ListJobTemplatesResponsePaginatorTypeDef]
else:
    _ListJobTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListJobTemplatesPaginator(_ListJobTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobTemplates.html#EMRContainers.Paginator.ListJobTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobTemplatesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListJobTemplates.html#EMRContainers.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listjobtemplatespaginator)
        """

if TYPE_CHECKING:
    _ListManagedEndpointsPaginatorBase = AioPaginator[ListManagedEndpointsResponsePaginatorTypeDef]
else:
    _ListManagedEndpointsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListManagedEndpointsPaginator(_ListManagedEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListManagedEndpoints.html#EMRContainers.Paginator.ListManagedEndpoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listmanagedendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedEndpointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedEndpointsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListManagedEndpoints.html#EMRContainers.Paginator.ListManagedEndpoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listmanagedendpointspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityConfigurationsPaginatorBase = AioPaginator[
        ListSecurityConfigurationsResponseTypeDef
    ]
else:
    _ListSecurityConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityConfigurationsPaginator(_ListSecurityConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListSecurityConfigurations.html#EMRContainers.Paginator.ListSecurityConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listsecurityconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListSecurityConfigurations.html#EMRContainers.Paginator.ListSecurityConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listsecurityconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListVirtualClustersPaginatorBase = AioPaginator[ListVirtualClustersResponseTypeDef]
else:
    _ListVirtualClustersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListVirtualClustersPaginator(_ListVirtualClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListVirtualClusters.html#EMRContainers.Paginator.ListVirtualClusters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listvirtualclusterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVirtualClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVirtualClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr-containers/paginator/ListVirtualClusters.html#EMRContainers.Paginator.ListVirtualClusters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_emr_containers/paginators/#listvirtualclusterspaginator)
        """
