"""
Type annotations for m2 service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_m2.client import MainframeModernizationClient
    from types_aiobotocore_m2.paginator import (
        ListApplicationVersionsPaginator,
        ListApplicationsPaginator,
        ListBatchJobDefinitionsPaginator,
        ListBatchJobExecutionsPaginator,
        ListDataSetExportHistoryPaginator,
        ListDataSetImportHistoryPaginator,
        ListDataSetsPaginator,
        ListDeploymentsPaginator,
        ListEngineVersionsPaginator,
        ListEnvironmentsPaginator,
    )

    session = get_session()
    with session.create_client("m2") as client:
        client: MainframeModernizationClient

        list_application_versions_paginator: ListApplicationVersionsPaginator = client.get_paginator("list_application_versions")
        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_batch_job_definitions_paginator: ListBatchJobDefinitionsPaginator = client.get_paginator("list_batch_job_definitions")
        list_batch_job_executions_paginator: ListBatchJobExecutionsPaginator = client.get_paginator("list_batch_job_executions")
        list_data_set_export_history_paginator: ListDataSetExportHistoryPaginator = client.get_paginator("list_data_set_export_history")
        list_data_set_import_history_paginator: ListDataSetImportHistoryPaginator = client.get_paginator("list_data_set_import_history")
        list_data_sets_paginator: ListDataSetsPaginator = client.get_paginator("list_data_sets")
        list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
        list_engine_versions_paginator: ListEngineVersionsPaginator = client.get_paginator("list_engine_versions")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListApplicationVersionsRequestPaginateTypeDef,
    ListApplicationVersionsResponseTypeDef,
    ListBatchJobDefinitionsRequestPaginateTypeDef,
    ListBatchJobDefinitionsResponseTypeDef,
    ListBatchJobExecutionsRequestPaginateTypeDef,
    ListBatchJobExecutionsResponseTypeDef,
    ListDataSetExportHistoryRequestPaginateTypeDef,
    ListDataSetExportHistoryResponseTypeDef,
    ListDataSetImportHistoryRequestPaginateTypeDef,
    ListDataSetImportHistoryResponseTypeDef,
    ListDataSetsRequestPaginateTypeDef,
    ListDataSetsResponseTypeDef,
    ListDeploymentsRequestPaginateTypeDef,
    ListDeploymentsResponseTypeDef,
    ListEngineVersionsRequestPaginateTypeDef,
    ListEngineVersionsResponseTypeDef,
    ListEnvironmentsRequestPaginateTypeDef,
    ListEnvironmentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationVersionsPaginator",
    "ListApplicationsPaginator",
    "ListBatchJobDefinitionsPaginator",
    "ListBatchJobExecutionsPaginator",
    "ListDataSetExportHistoryPaginator",
    "ListDataSetImportHistoryPaginator",
    "ListDataSetsPaginator",
    "ListDeploymentsPaginator",
    "ListEngineVersionsPaginator",
    "ListEnvironmentsPaginator",
)


if TYPE_CHECKING:
    _ListApplicationVersionsPaginatorBase = AioPaginator[ListApplicationVersionsResponseTypeDef]
else:
    _ListApplicationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationVersionsPaginator(_ListApplicationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListApplicationVersions.html#MainframeModernization.Paginator.ListApplicationVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listapplicationversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListApplicationVersions.html#MainframeModernization.Paginator.ListApplicationVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listapplicationversionspaginator)
        """


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListApplications.html#MainframeModernization.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListApplications.html#MainframeModernization.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListBatchJobDefinitionsPaginatorBase = AioPaginator[ListBatchJobDefinitionsResponseTypeDef]
else:
    _ListBatchJobDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBatchJobDefinitionsPaginator(_ListBatchJobDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListBatchJobDefinitions.html#MainframeModernization.Paginator.ListBatchJobDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listbatchjobdefinitionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBatchJobDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBatchJobDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListBatchJobDefinitions.html#MainframeModernization.Paginator.ListBatchJobDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listbatchjobdefinitionspaginator)
        """


if TYPE_CHECKING:
    _ListBatchJobExecutionsPaginatorBase = AioPaginator[ListBatchJobExecutionsResponseTypeDef]
else:
    _ListBatchJobExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBatchJobExecutionsPaginator(_ListBatchJobExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListBatchJobExecutions.html#MainframeModernization.Paginator.ListBatchJobExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listbatchjobexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBatchJobExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBatchJobExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListBatchJobExecutions.html#MainframeModernization.Paginator.ListBatchJobExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listbatchjobexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListDataSetExportHistoryPaginatorBase = AioPaginator[ListDataSetExportHistoryResponseTypeDef]
else:
    _ListDataSetExportHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataSetExportHistoryPaginator(_ListDataSetExportHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDataSetExportHistory.html#MainframeModernization.Paginator.ListDataSetExportHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdatasetexporthistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSetExportHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSetExportHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDataSetExportHistory.html#MainframeModernization.Paginator.ListDataSetExportHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdatasetexporthistorypaginator)
        """


if TYPE_CHECKING:
    _ListDataSetImportHistoryPaginatorBase = AioPaginator[ListDataSetImportHistoryResponseTypeDef]
else:
    _ListDataSetImportHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataSetImportHistoryPaginator(_ListDataSetImportHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDataSetImportHistory.html#MainframeModernization.Paginator.ListDataSetImportHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdatasetimporthistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSetImportHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSetImportHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDataSetImportHistory.html#MainframeModernization.Paginator.ListDataSetImportHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdatasetimporthistorypaginator)
        """


if TYPE_CHECKING:
    _ListDataSetsPaginatorBase = AioPaginator[ListDataSetsResponseTypeDef]
else:
    _ListDataSetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDataSetsPaginator(_ListDataSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDataSets.html#MainframeModernization.Paginator.ListDataSets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdatasetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDataSetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDataSetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDataSets.html#MainframeModernization.Paginator.ListDataSets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdatasetspaginator)
        """


if TYPE_CHECKING:
    _ListDeploymentsPaginatorBase = AioPaginator[ListDeploymentsResponseTypeDef]
else:
    _ListDeploymentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeploymentsPaginator(_ListDeploymentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDeployments.html#MainframeModernization.Paginator.ListDeployments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdeploymentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeploymentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeploymentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListDeployments.html#MainframeModernization.Paginator.ListDeployments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listdeploymentspaginator)
        """


if TYPE_CHECKING:
    _ListEngineVersionsPaginatorBase = AioPaginator[ListEngineVersionsResponseTypeDef]
else:
    _ListEngineVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEngineVersionsPaginator(_ListEngineVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListEngineVersions.html#MainframeModernization.Paginator.ListEngineVersions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listengineversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEngineVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEngineVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListEngineVersions.html#MainframeModernization.Paginator.ListEngineVersions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listengineversionspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListEnvironments.html#MainframeModernization.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/m2/paginator/ListEnvironments.html#MainframeModernization.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/paginators/#listenvironmentspaginator)
        """
