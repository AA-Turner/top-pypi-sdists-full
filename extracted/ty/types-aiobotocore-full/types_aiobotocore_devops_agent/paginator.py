"""
Type annotations for devops-agent service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devops_agent.client import DevOpsAgentServiceClient
    from types_aiobotocore_devops_agent.paginator import (
        ListAgentSpacesPaginator,
        ListAssociationsPaginator,
        ListBacklogTasksPaginator,
        ListExecutionsPaginator,
        ListGoalsPaginator,
        ListJournalRecordsPaginator,
        ListServicesPaginator,
    )

    session = get_session()
    with session.create_client("devops-agent") as client:
        client: DevOpsAgentServiceClient

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

from aiobotocore.paginate import AioPageIterator, AioPaginator

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
    _ListAgentSpacesPaginatorBase = AioPaginator[ListAgentSpacesOutputTypeDef]
else:
    _ListAgentSpacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAgentSpacesPaginator(_ListAgentSpacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAgentSpaces.html#DevOpsAgentService.Paginator.ListAgentSpaces)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listagentspacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentSpacesInputPaginateTypeDef]
    ) -> AioPageIterator[ListAgentSpacesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAgentSpaces.html#DevOpsAgentService.Paginator.ListAgentSpaces.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listagentspacespaginator)
        """


if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = AioPaginator[ListAssociationsOutputTypeDef]
else:
    _ListAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssociations.html#DevOpsAgentService.Paginator.ListAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListAssociationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListAssociations.html#DevOpsAgentService.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listassociationspaginator)
        """


if TYPE_CHECKING:
    _ListBacklogTasksPaginatorBase = AioPaginator[ListBacklogTasksResponseTypeDef]
else:
    _ListBacklogTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBacklogTasksPaginator(_ListBacklogTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListBacklogTasks.html#DevOpsAgentService.Paginator.ListBacklogTasks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listbacklogtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBacklogTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBacklogTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListBacklogTasks.html#DevOpsAgentService.Paginator.ListBacklogTasks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listbacklogtaskspaginator)
        """


if TYPE_CHECKING:
    _ListExecutionsPaginatorBase = AioPaginator[ListExecutionsResponseTypeDef]
else:
    _ListExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExecutionsPaginator(_ListExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListExecutions.html#DevOpsAgentService.Paginator.ListExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListExecutions.html#DevOpsAgentService.Paginator.ListExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListGoalsPaginatorBase = AioPaginator[ListGoalsResponseTypeDef]
else:
    _ListGoalsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListGoalsPaginator(_ListGoalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListGoals.html#DevOpsAgentService.Paginator.ListGoals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listgoalspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGoalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListGoalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListGoals.html#DevOpsAgentService.Paginator.ListGoals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listgoalspaginator)
        """


if TYPE_CHECKING:
    _ListJournalRecordsPaginatorBase = AioPaginator[ListJournalRecordsResponseTypeDef]
else:
    _ListJournalRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJournalRecordsPaginator(_ListJournalRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListJournalRecords.html#DevOpsAgentService.Paginator.ListJournalRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listjournalrecordspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJournalRecordsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJournalRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListJournalRecords.html#DevOpsAgentService.Paginator.ListJournalRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listjournalrecordspaginator)
        """


if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListServices.html#DevOpsAgentService.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devops-agent/paginator/ListServices.html#DevOpsAgentService.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devops_agent/paginators/#listservicespaginator)
        """
