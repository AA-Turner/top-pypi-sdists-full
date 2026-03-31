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
        ListAssociationsPaginator,
        ListBacklogTasksPaginator,
        ListExecutionsPaginator,
        ListGoalsPaginator,
        ListJournalRecordsPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: DevOpsAgentServiceClient = session.client("devops-agent")

    list_agent_spaces_paginator: ListAgentSpacesPaginator = client.get_paginator("list_agent_spaces")
    list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
    list_backlog_tasks_paginator: ListBacklogTasksPaginator = client.get_paginator("list_backlog_tasks")
    list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
    list_goals_paginator: ListGoalsPaginator = client.get_paginator("list_goals")
    list_journal_records_paginator: ListJournalRecordsPaginator = client.get_paginator("list_journal_records")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAgentSpacesInputPaginateTypeDef,
    ListAgentSpacesOutputTypeDef,
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
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAgentSpacesPaginator",
    "ListAssociationsPaginator",
    "ListBacklogTasksPaginator",
    "ListExecutionsPaginator",
    "ListGoalsPaginator",
    "ListJournalRecordsPaginator",
    "ListServicesPaginator",
)

if TYPE_CHECKING:
    _ListAgentSpacesPaginatorBase = Paginator[ListAgentSpacesOutputTypeDef]
else:
    _ListAgentSpacesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentSpacesPaginator(_ListAgentSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAgentSpaces.html#DevOpsAgentService.Paginator.ListAgentSpaces)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listagentspacespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentSpacesInputPaginateTypeDef]
    ) -> PageIterator[ListAgentSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAgentSpaces.html#DevOpsAgentService.Paginator.ListAgentSpaces.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listagentspacespaginator)
        """

if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = Paginator[ListAssociationsOutputTypeDef]
else:
    _ListAssociationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssociations.html#DevOpsAgentService.Paginator.ListAssociations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsInputPaginateTypeDef]
    ) -> PageIterator[ListAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssociations.html#DevOpsAgentService.Paginator.ListAssociations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listassociationspaginator)
        """

if TYPE_CHECKING:
    _ListBacklogTasksPaginatorBase = Paginator[ListBacklogTasksResponseTypeDef]
else:
    _ListBacklogTasksPaginatorBase = Paginator  # type: ignore[assignment]

class ListBacklogTasksPaginator(_ListBacklogTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListBacklogTasks.html#DevOpsAgentService.Paginator.ListBacklogTasks)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listbacklogtaskspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBacklogTasksRequestPaginateTypeDef]
    ) -> PageIterator[ListBacklogTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListBacklogTasks.html#DevOpsAgentService.Paginator.ListBacklogTasks.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listbacklogtaskspaginator)
        """

if TYPE_CHECKING:
    _ListExecutionsPaginatorBase = Paginator[ListExecutionsResponseTypeDef]
else:
    _ListExecutionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListExecutionsPaginator(_ListExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListExecutions.html#DevOpsAgentService.Paginator.ListExecutions)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExecutionsRequestPaginateTypeDef]
    ) -> PageIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListExecutions.html#DevOpsAgentService.Paginator.ListExecutions.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListGoalsPaginatorBase = Paginator[ListGoalsResponseTypeDef]
else:
    _ListGoalsPaginatorBase = Paginator  # type: ignore[assignment]

class ListGoalsPaginator(_ListGoalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListGoals.html#DevOpsAgentService.Paginator.ListGoals)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listgoalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGoalsRequestPaginateTypeDef]
    ) -> PageIterator[ListGoalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListGoals.html#DevOpsAgentService.Paginator.ListGoals.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listgoalspaginator)
        """

if TYPE_CHECKING:
    _ListJournalRecordsPaginatorBase = Paginator[ListJournalRecordsResponseTypeDef]
else:
    _ListJournalRecordsPaginatorBase = Paginator  # type: ignore[assignment]

class ListJournalRecordsPaginator(_ListJournalRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListJournalRecords.html#DevOpsAgentService.Paginator.ListJournalRecords)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listjournalrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJournalRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListJournalRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListJournalRecords.html#DevOpsAgentService.Paginator.ListJournalRecords.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listjournalrecordspaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = Paginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = Paginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListServices.html#DevOpsAgentService.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListServices.html#DevOpsAgentService.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_devops_agent/paginators/#listservicespaginator)
        """
