"""
Type annotations for stepfunctions service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_stepfunctions.client import SFNClient
    from types_aiobotocore_stepfunctions.paginator import (
        GetExecutionHistoryPaginator,
        ListActivitiesPaginator,
        ListExecutionsPaginator,
        ListMapRunsPaginator,
        ListStateMachinesPaginator,
    )

    session = get_session()
    with session.create_client("stepfunctions") as client:
        client: SFNClient

        get_execution_history_paginator: GetExecutionHistoryPaginator = client.get_paginator("get_execution_history")
        list_activities_paginator: ListActivitiesPaginator = client.get_paginator("list_activities")
        list_executions_paginator: ListExecutionsPaginator = client.get_paginator("list_executions")
        list_map_runs_paginator: ListMapRunsPaginator = client.get_paginator("list_map_runs")
        list_state_machines_paginator: ListStateMachinesPaginator = client.get_paginator("list_state_machines")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetExecutionHistoryInputPaginateTypeDef,
    GetExecutionHistoryOutputTypeDef,
    ListActivitiesInputPaginateTypeDef,
    ListActivitiesOutputTypeDef,
    ListExecutionsInputPaginateTypeDef,
    ListExecutionsOutputTypeDef,
    ListMapRunsInputPaginateTypeDef,
    ListMapRunsOutputTypeDef,
    ListStateMachinesInputPaginateTypeDef,
    ListStateMachinesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetExecutionHistoryPaginator",
    "ListActivitiesPaginator",
    "ListExecutionsPaginator",
    "ListMapRunsPaginator",
    "ListStateMachinesPaginator",
)


if TYPE_CHECKING:
    _GetExecutionHistoryPaginatorBase = AioPaginator[GetExecutionHistoryOutputTypeDef]
else:
    _GetExecutionHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetExecutionHistoryPaginator(_GetExecutionHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/GetExecutionHistory.html#SFN.Paginator.GetExecutionHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#getexecutionhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetExecutionHistoryInputPaginateTypeDef]
    ) -> AioPageIterator[GetExecutionHistoryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/GetExecutionHistory.html#SFN.Paginator.GetExecutionHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#getexecutionhistorypaginator)
        """


if TYPE_CHECKING:
    _ListActivitiesPaginatorBase = AioPaginator[ListActivitiesOutputTypeDef]
else:
    _ListActivitiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListActivitiesPaginator(_ListActivitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListActivities.html#SFN.Paginator.ListActivities)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listactivitiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActivitiesInputPaginateTypeDef]
    ) -> AioPageIterator[ListActivitiesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListActivities.html#SFN.Paginator.ListActivities.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listactivitiespaginator)
        """


if TYPE_CHECKING:
    _ListExecutionsPaginatorBase = AioPaginator[ListExecutionsOutputTypeDef]
else:
    _ListExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExecutionsPaginator(_ListExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListExecutions.html#SFN.Paginator.ListExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListExecutions.html#SFN.Paginator.ListExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListMapRunsPaginatorBase = AioPaginator[ListMapRunsOutputTypeDef]
else:
    _ListMapRunsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMapRunsPaginator(_ListMapRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListMapRuns.html#SFN.Paginator.ListMapRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listmaprunspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMapRunsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMapRunsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListMapRuns.html#SFN.Paginator.ListMapRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#listmaprunspaginator)
        """


if TYPE_CHECKING:
    _ListStateMachinesPaginatorBase = AioPaginator[ListStateMachinesOutputTypeDef]
else:
    _ListStateMachinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStateMachinesPaginator(_ListStateMachinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListStateMachines.html#SFN.Paginator.ListStateMachines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#liststatemachinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStateMachinesInputPaginateTypeDef]
    ) -> AioPageIterator[ListStateMachinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/paginator/ListStateMachines.html#SFN.Paginator.ListStateMachines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_stepfunctions/paginators/#liststatemachinespaginator)
        """
