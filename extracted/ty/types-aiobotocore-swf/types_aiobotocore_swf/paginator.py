"""
Type annotations for swf service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_swf.client import SWFClient
    from types_aiobotocore_swf.paginator import (
        GetWorkflowExecutionHistoryPaginator,
        ListActivityTypesPaginator,
        ListClosedWorkflowExecutionsPaginator,
        ListDomainsPaginator,
        ListOpenWorkflowExecutionsPaginator,
        ListWorkflowTypesPaginator,
        PollForDecisionTaskPaginator,
    )

    session = get_session()
    with session.create_client("swf") as client:
        client: SWFClient

        get_workflow_execution_history_paginator: GetWorkflowExecutionHistoryPaginator = client.get_paginator("get_workflow_execution_history")
        list_activity_types_paginator: ListActivityTypesPaginator = client.get_paginator("list_activity_types")
        list_closed_workflow_executions_paginator: ListClosedWorkflowExecutionsPaginator = client.get_paginator("list_closed_workflow_executions")
        list_domains_paginator: ListDomainsPaginator = client.get_paginator("list_domains")
        list_open_workflow_executions_paginator: ListOpenWorkflowExecutionsPaginator = client.get_paginator("list_open_workflow_executions")
        list_workflow_types_paginator: ListWorkflowTypesPaginator = client.get_paginator("list_workflow_types")
        poll_for_decision_task_paginator: PollForDecisionTaskPaginator = client.get_paginator("poll_for_decision_task")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ActivityTypeInfosTypeDef,
    DecisionTaskTypeDef,
    DomainInfosTypeDef,
    GetWorkflowExecutionHistoryInputPaginateTypeDef,
    HistoryTypeDef,
    ListActivityTypesInputPaginateTypeDef,
    ListClosedWorkflowExecutionsInputPaginateTypeDef,
    ListDomainsInputPaginateTypeDef,
    ListOpenWorkflowExecutionsInputPaginateTypeDef,
    ListWorkflowTypesInputPaginateTypeDef,
    PollForDecisionTaskInputPaginateTypeDef,
    WorkflowExecutionInfosTypeDef,
    WorkflowTypeInfosTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetWorkflowExecutionHistoryPaginator",
    "ListActivityTypesPaginator",
    "ListClosedWorkflowExecutionsPaginator",
    "ListDomainsPaginator",
    "ListOpenWorkflowExecutionsPaginator",
    "ListWorkflowTypesPaginator",
    "PollForDecisionTaskPaginator",
)


if TYPE_CHECKING:
    _GetWorkflowExecutionHistoryPaginatorBase = AioPaginator[HistoryTypeDef]
else:
    _GetWorkflowExecutionHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetWorkflowExecutionHistoryPaginator(_GetWorkflowExecutionHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/GetWorkflowExecutionHistory.html#SWF.Paginator.GetWorkflowExecutionHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#getworkflowexecutionhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetWorkflowExecutionHistoryInputPaginateTypeDef]
    ) -> AioPageIterator[HistoryTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/GetWorkflowExecutionHistory.html#SWF.Paginator.GetWorkflowExecutionHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#getworkflowexecutionhistorypaginator)
        """


if TYPE_CHECKING:
    _ListActivityTypesPaginatorBase = AioPaginator[ActivityTypeInfosTypeDef]
else:
    _ListActivityTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListActivityTypesPaginator(_ListActivityTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListActivityTypes.html#SWF.Paginator.ListActivityTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listactivitytypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActivityTypesInputPaginateTypeDef]
    ) -> AioPageIterator[ActivityTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListActivityTypes.html#SWF.Paginator.ListActivityTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listactivitytypespaginator)
        """


if TYPE_CHECKING:
    _ListClosedWorkflowExecutionsPaginatorBase = AioPaginator[WorkflowExecutionInfosTypeDef]
else:
    _ListClosedWorkflowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListClosedWorkflowExecutionsPaginator(_ListClosedWorkflowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListClosedWorkflowExecutions.html#SWF.Paginator.ListClosedWorkflowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listclosedworkflowexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClosedWorkflowExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListClosedWorkflowExecutions.html#SWF.Paginator.ListClosedWorkflowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listclosedworkflowexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListDomainsPaginatorBase = AioPaginator[DomainInfosTypeDef]
else:
    _ListDomainsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainsPaginator(_ListDomainsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListDomains.html#SWF.Paginator.ListDomains)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listdomainspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainsInputPaginateTypeDef]
    ) -> AioPageIterator[DomainInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListDomains.html#SWF.Paginator.ListDomains.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listdomainspaginator)
        """


if TYPE_CHECKING:
    _ListOpenWorkflowExecutionsPaginatorBase = AioPaginator[WorkflowExecutionInfosTypeDef]
else:
    _ListOpenWorkflowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOpenWorkflowExecutionsPaginator(_ListOpenWorkflowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListOpenWorkflowExecutions.html#SWF.Paginator.ListOpenWorkflowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listopenworkflowexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpenWorkflowExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[WorkflowExecutionInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListOpenWorkflowExecutions.html#SWF.Paginator.ListOpenWorkflowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listopenworkflowexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowTypesPaginatorBase = AioPaginator[WorkflowTypeInfosTypeDef]
else:
    _ListWorkflowTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowTypesPaginator(_ListWorkflowTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListWorkflowTypes.html#SWF.Paginator.ListWorkflowTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listworkflowtypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowTypesInputPaginateTypeDef]
    ) -> AioPageIterator[WorkflowTypeInfosTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/ListWorkflowTypes.html#SWF.Paginator.ListWorkflowTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#listworkflowtypespaginator)
        """


if TYPE_CHECKING:
    _PollForDecisionTaskPaginatorBase = AioPaginator[DecisionTaskTypeDef]
else:
    _PollForDecisionTaskPaginatorBase = AioPaginator  # type: ignore[assignment]


class PollForDecisionTaskPaginator(_PollForDecisionTaskPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/PollForDecisionTask.html#SWF.Paginator.PollForDecisionTask)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#pollfordecisiontaskpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[PollForDecisionTaskInputPaginateTypeDef]
    ) -> AioPageIterator[DecisionTaskTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/swf/paginator/PollForDecisionTask.html#SWF.Paginator.PollForDecisionTask.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_swf/paginators/#pollfordecisiontaskpaginator)
        """
