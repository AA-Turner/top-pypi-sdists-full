"""
Type annotations for devops-agent service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_devops_agent.client import DevOpsAgentServiceClient
    from mypy_boto3_devops_agent.paginator import (
        ListAgentSpacesPaginator,
        ListAssetFilesPaginator,
        ListAssetTypesPaginator,
        ListAssetVersionsPaginator,
        ListAssetsPaginator,
        ListAssociationsPaginator,
        ListBacklogTasksPaginator,
        ListExecutionsPaginator,
        ListGoalsPaginator,
        ListJournalRecordsPaginator,
        ListServicesPaginator,
        ListTriggersPaginator,
    )

    session = Session()
    client: DevOpsAgentServiceClient = session.client("devops-agent")

    list_agent_spaces_paginator: ListAgentSpacesPaginator = client.get_paginator("list_agent_spaces")
    list_asset_files_paginator: ListAssetFilesPaginator = client.get_paginator("list_asset_files")
    list_asset_types_paginator: ListAssetTypesPaginator = client.get_paginator("list_asset_types")
    list_asset_versions_paginator: ListAssetVersionsPaginator = client.get_paginator("list_asset_versions")
    list_assets_paginator: ListAssetsPaginator = client.get_paginator("list_assets")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_backlog_tasks_paginator: ListBacklogTasksPaginator = client.get_paginator("list_backlog_tasks")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_goals_paginator: ListGoalsPaginator = client.get_paginator("list_goals")
    list_journal_records_paginator: ListJournalRecordsPaginator = client.get_paginator("list_journal_records")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    list_triggers_paginator: ListTriggersPaginator = client.get_paginator("list_triggers")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAgentSpacesInputPaginateTypeDef,
    ListAgentSpacesOutputTypeDef,
    ListAssetFilesRequestPaginateTypeDef,
    ListAssetFilesResponseTypeDef,
    ListAssetsRequestPaginateTypeDef,
    ListAssetsResponseTypeDef,
    ListAssetTypesRequestPaginateTypeDef,
    ListAssetTypesResponseTypeDef,
    ListAssetVersionsRequestPaginateTypeDef,
    ListAssetVersionsResponseTypeDef,
    ListAssociationsInputPaginateTypeDef,
    ListAssociationsOutputTypeDef,
    ListBacklogTasksRequestPaginateTypeDef,
    ListBacklogTasksResponseTypeDef,
    ListExecutionsRequestPaginateTypeDef,
    ListExecutionsResponseTypeDef,
    ListGoalsRequestPaginateTypeDef,
    ListGoalsResponseTypeDef,
    ListJournalRecordsRequestPaginateTypeDef,
    ListJournalRecordsResponseTypeDef,
    ListServicesInputPaginateTypeDef,
    ListServicesOutputTypeDef,
    ListTriggersRequestPaginateTypeDef,
    ListTriggersResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAgentSpacesPaginator",
    "ListAssetFilesPaginator",
    "ListAssetTypesPaginator",
    "ListAssetVersionsPaginator",
    "ListAssetsPaginator",
    "ListAssociationsPaginator",
    "ListBacklogTasksPaginator",
    "ListExecutionsPaginator",
    "ListGoalsPaginator",
    "ListJournalRecordsPaginator",
    "ListServicesPaginator",
    "ListTriggersPaginator",
)

if TYPE_CHECKING:
    _ListAgentSpacesPaginatorBase = Paginator[ListAgentSpacesOutputTypeDef]
else:
    _ListAgentSpacesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentSpacesPaginator(_ListAgentSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAgentSpaces.html#DevOpsAgentService.Paginator.ListAgentSpaces)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listagentspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentSpacesInputPaginateTypeDef]
    ) -> PageIterator[ListAgentSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAgentSpaces.html#DevOpsAgentService.Paginator.ListAgentSpaces.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listagentspacespaginator)
        """

if TYPE_CHECKING:
    _ListAssetFilesPaginatorBase = Paginator[ListAssetFilesResponseTypeDef]
else:
    _ListAssetFilesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssetFilesPaginator(_ListAssetFilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssetFiles.html#DevOpsAgentService.Paginator.ListAssetFiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassetfilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetFilesRequestPaginateTypeDef]
    ) -> PageIterator[ListAssetFilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssetFiles.html#DevOpsAgentService.Paginator.ListAssetFiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassetfilespaginator)
        """

if TYPE_CHECKING:
    _ListAssetTypesPaginatorBase = Paginator[ListAssetTypesResponseTypeDef]
else:
    _ListAssetTypesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssetTypesPaginator(_ListAssetTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssetTypes.html#DevOpsAgentService.Paginator.ListAssetTypes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassettypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetTypesRequestPaginateTypeDef]
    ) -> PageIterator[ListAssetTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssetTypes.html#DevOpsAgentService.Paginator.ListAssetTypes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassettypespaginator)
        """

if TYPE_CHECKING:
    _ListAssetVersionsPaginatorBase = Paginator[ListAssetVersionsResponseTypeDef]
else:
    _ListAssetVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssetVersionsPaginator(_ListAssetVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssetVersions.html#DevOpsAgentService.Paginator.ListAssetVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassetversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListAssetVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssetVersions.html#DevOpsAgentService.Paginator.ListAssetVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassetversionspaginator)
        """

if TYPE_CHECKING:
    _ListAssetsPaginatorBase = Paginator[ListAssetsResponseTypeDef]
else:
    _ListAssetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssetsPaginator(_ListAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssets.html#DevOpsAgentService.Paginator.ListAssets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssetsRequestPaginateTypeDef]
    ) -> PageIterator[ListAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssets.html#DevOpsAgentService.Paginator.ListAssets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassetspaginator)
        """

if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = Paginator[ListAssociationsOutputTypeDef]
else:
    _ListAssociationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssociations.html#DevOpsAgentService.Paginator.ListAssociations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsInputPaginateTypeDef]
    ) -> PageIterator[ListAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssociations.html#DevOpsAgentService.Paginator.ListAssociations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassociationspaginator)
        """

if TYPE_CHECKING:
    _ListBacklogTasksPaginatorBase = Paginator[ListBacklogTasksResponseTypeDef]
else:
    _ListBacklogTasksPaginatorBase = Paginator  # type: ignore[assignment]

class ListBacklogTasksPaginator(_ListBacklogTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListBacklogTasks.html#DevOpsAgentService.Paginator.ListBacklogTasks)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listbacklogtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBacklogTasksRequestPaginateTypeDef]
    ) -> PageIterator[ListBacklogTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListBacklogTasks.html#DevOpsAgentService.Paginator.ListBacklogTasks.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listbacklogtaskspaginator)
        """

if TYPE_CHECKING:
    _ListExecutionsPaginatorBase = Paginator[ListExecutionsResponseTypeDef]
else:
    _ListExecutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListExecutionsPaginator(_ListExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListExecutions.html#DevOpsAgentService.Paginator.ListExecutions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListExecutions.html#DevOpsAgentService.Paginator.ListExecutions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListGoalsPaginatorBase = Paginator[ListGoalsResponseTypeDef]
else:
    _ListGoalsPaginatorBase = Paginator  # type: ignore[assignment]

class ListGoalsPaginator(_ListGoalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListGoals.html#DevOpsAgentService.Paginator.ListGoals)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listgoalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGoalsRequestPaginateTypeDef]
    ) -> PageIterator[ListGoalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListGoals.html#DevOpsAgentService.Paginator.ListGoals.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listgoalspaginator)
        """

if TYPE_CHECKING:
    _ListJournalRecordsPaginatorBase = Paginator[ListJournalRecordsResponseTypeDef]
else:
    _ListJournalRecordsPaginatorBase = Paginator  # type: ignore[assignment]

class ListJournalRecordsPaginator(_ListJournalRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListJournalRecords.html#DevOpsAgentService.Paginator.ListJournalRecords)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listjournalrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJournalRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListJournalRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListJournalRecords.html#DevOpsAgentService.Paginator.ListJournalRecords.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listjournalrecordspaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = Paginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = Paginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListServices.html#DevOpsAgentService.Paginator.ListServices)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListServices.html#DevOpsAgentService.Paginator.ListServices.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listservicespaginator)
        """

if TYPE_CHECKING:
    _ListTriggersPaginatorBase = Paginator[ListTriggersResponseTypeDef]
else:
    _ListTriggersPaginatorBase = Paginator  # type: ignore[assignment]

class ListTriggersPaginator(_ListTriggersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListTriggers.html#DevOpsAgentService.Paginator.ListTriggers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listtriggerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTriggersRequestPaginateTypeDef]
    ) -> PageIterator[ListTriggersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListTriggers.html#DevOpsAgentService.Paginator.ListTriggers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listtriggerspaginator)
        """
