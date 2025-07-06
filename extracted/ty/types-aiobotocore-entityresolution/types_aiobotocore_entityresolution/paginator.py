"""
Type annotations for entityresolution service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_entityresolution.client import EntityResolutionClient
    from types_aiobotocore_entityresolution.paginator import (
        ListIdMappingJobsPaginator,
        ListIdMappingWorkflowsPaginator,
        ListIdNamespacesPaginator,
        ListMatchingJobsPaginator,
        ListMatchingWorkflowsPaginator,
        ListProviderServicesPaginator,
        ListSchemaMappingsPaginator,
    )

    session = get_session()
    with session.create_client("entityresolution") as client:
        client: EntityResolutionClient

        list_id_mapping_jobs_paginator: ListIdMappingJobsPaginator = client.get_paginator("list_id_mapping_jobs")
        list_id_mapping_workflows_paginator: ListIdMappingWorkflowsPaginator = client.get_paginator("list_id_mapping_workflows")
        list_id_namespaces_paginator: ListIdNamespacesPaginator = client.get_paginator("list_id_namespaces")
        list_matching_jobs_paginator: ListMatchingJobsPaginator = client.get_paginator("list_matching_jobs")
        list_matching_workflows_paginator: ListMatchingWorkflowsPaginator = client.get_paginator("list_matching_workflows")
        list_provider_services_paginator: ListProviderServicesPaginator = client.get_paginator("list_provider_services")
        list_schema_mappings_paginator: ListSchemaMappingsPaginator = client.get_paginator("list_schema_mappings")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListIdMappingJobsInputPaginateTypeDef,
    ListIdMappingJobsOutputTypeDef,
    ListIdMappingWorkflowsInputPaginateTypeDef,
    ListIdMappingWorkflowsOutputTypeDef,
    ListIdNamespacesInputPaginateTypeDef,
    ListIdNamespacesOutputTypeDef,
    ListMatchingJobsInputPaginateTypeDef,
    ListMatchingJobsOutputTypeDef,
    ListMatchingWorkflowsInputPaginateTypeDef,
    ListMatchingWorkflowsOutputTypeDef,
    ListProviderServicesInputPaginateTypeDef,
    ListProviderServicesOutputTypeDef,
    ListSchemaMappingsInputPaginateTypeDef,
    ListSchemaMappingsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListIdMappingJobsPaginator",
    "ListIdMappingWorkflowsPaginator",
    "ListIdNamespacesPaginator",
    "ListMatchingJobsPaginator",
    "ListMatchingWorkflowsPaginator",
    "ListProviderServicesPaginator",
    "ListSchemaMappingsPaginator",
)


if TYPE_CHECKING:
    _ListIdMappingJobsPaginatorBase = AioPaginator[ListIdMappingJobsOutputTypeDef]
else:
    _ListIdMappingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIdMappingJobsPaginator(_ListIdMappingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingJobs.html#EntityResolution.Paginator.ListIdMappingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdMappingJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdMappingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingJobs.html#EntityResolution.Paginator.ListIdMappingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingjobspaginator)
        """


if TYPE_CHECKING:
    _ListIdMappingWorkflowsPaginatorBase = AioPaginator[ListIdMappingWorkflowsOutputTypeDef]
else:
    _ListIdMappingWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIdMappingWorkflowsPaginator(_ListIdMappingWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingWorkflows.html#EntityResolution.Paginator.ListIdMappingWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingworkflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdMappingWorkflowsInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdMappingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdMappingWorkflows.html#EntityResolution.Paginator.ListIdMappingWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidmappingworkflowspaginator)
        """


if TYPE_CHECKING:
    _ListIdNamespacesPaginatorBase = AioPaginator[ListIdNamespacesOutputTypeDef]
else:
    _ListIdNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIdNamespacesPaginator(_ListIdNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdNamespaces.html#EntityResolution.Paginator.ListIdNamespaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidnamespacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIdNamespacesInputPaginateTypeDef]
    ) -> AioPageIterator[ListIdNamespacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListIdNamespaces.html#EntityResolution.Paginator.ListIdNamespaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listidnamespacespaginator)
        """


if TYPE_CHECKING:
    _ListMatchingJobsPaginatorBase = AioPaginator[ListMatchingJobsOutputTypeDef]
else:
    _ListMatchingJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMatchingJobsPaginator(_ListMatchingJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingJobs.html#EntityResolution.Paginator.ListMatchingJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMatchingJobsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMatchingJobsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingJobs.html#EntityResolution.Paginator.ListMatchingJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingjobspaginator)
        """


if TYPE_CHECKING:
    _ListMatchingWorkflowsPaginatorBase = AioPaginator[ListMatchingWorkflowsOutputTypeDef]
else:
    _ListMatchingWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMatchingWorkflowsPaginator(_ListMatchingWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingWorkflows.html#EntityResolution.Paginator.ListMatchingWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingworkflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMatchingWorkflowsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMatchingWorkflowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListMatchingWorkflows.html#EntityResolution.Paginator.ListMatchingWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listmatchingworkflowspaginator)
        """


if TYPE_CHECKING:
    _ListProviderServicesPaginatorBase = AioPaginator[ListProviderServicesOutputTypeDef]
else:
    _ListProviderServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProviderServicesPaginator(_ListProviderServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListProviderServices.html#EntityResolution.Paginator.ListProviderServices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listproviderservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProviderServicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListProviderServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListProviderServices.html#EntityResolution.Paginator.ListProviderServices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listproviderservicespaginator)
        """


if TYPE_CHECKING:
    _ListSchemaMappingsPaginatorBase = AioPaginator[ListSchemaMappingsOutputTypeDef]
else:
    _ListSchemaMappingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSchemaMappingsPaginator(_ListSchemaMappingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListSchemaMappings.html#EntityResolution.Paginator.ListSchemaMappings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listschemamappingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSchemaMappingsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSchemaMappingsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/entityresolution/paginator/ListSchemaMappings.html#EntityResolution.Paginator.ListSchemaMappings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_entityresolution/paginators/#listschemamappingspaginator)
        """
