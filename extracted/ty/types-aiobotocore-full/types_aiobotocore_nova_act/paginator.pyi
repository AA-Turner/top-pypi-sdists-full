"""
Type annotations for nova-act service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_nova_act.client import NovaActServiceClient
    from types_aiobotocore_nova_act.paginator import (
        ListActsPaginator,
        ListSessionsPaginator,
        ListWorkflowDefinitionsPaginator,
        ListWorkflowRunsPaginator,
    )

    session = get_session()
    with session.create_client("nova-act") as client:
        client: NovaActServiceClient

        list_acts_paginator: ListActsPaginator = client.get_paginator("list_acts")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
        list_workflow_definitions_paginator: ListWorkflowDefinitionsPaginator = client.get_paginator("list_workflow_definitions")
        list_workflow_runs_paginator: ListWorkflowRunsPaginator = client.get_paginator("list_workflow_runs")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListActsRequestPaginateTypeDef,
    ListActsResponseTypeDef,
    ListSessionsRequestPaginateTypeDef,
    ListSessionsResponseTypeDef,
    ListWorkflowDefinitionsRequestPaginateTypeDef,
    ListWorkflowDefinitionsResponseTypeDef,
    ListWorkflowRunsRequestPaginateTypeDef,
    ListWorkflowRunsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListActsPaginator",
    "ListSessionsPaginator",
    "ListWorkflowDefinitionsPaginator",
    "ListWorkflowRunsPaginator",
)

if TYPE_CHECKING:
    _ListActsPaginatorBase = AioPaginator[ListActsResponseTypeDef]
else:
    _ListActsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListActsPaginator(_ListActsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListActs.html#NovaActService.Paginator.ListActs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListActsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListActs.html#NovaActService.Paginator.ListActs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listactspaginator)
        """

if TYPE_CHECKING:
    _ListSessionsPaginatorBase = AioPaginator[ListSessionsResponseTypeDef]
else:
    _ListSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSessionsPaginator(_ListSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListSessions.html#NovaActService.Paginator.ListSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListSessions.html#NovaActService.Paginator.ListSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listsessionspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowDefinitionsPaginatorBase = AioPaginator[ListWorkflowDefinitionsResponseTypeDef]
else:
    _ListWorkflowDefinitionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowDefinitionsPaginator(_ListWorkflowDefinitionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListWorkflowDefinitions.html#NovaActService.Paginator.ListWorkflowDefinitions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listworkflowdefinitionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowDefinitionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowDefinitionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListWorkflowDefinitions.html#NovaActService.Paginator.ListWorkflowDefinitions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listworkflowdefinitionspaginator)
        """

if TYPE_CHECKING:
    _ListWorkflowRunsPaginatorBase = AioPaginator[ListWorkflowRunsResponseTypeDef]
else:
    _ListWorkflowRunsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWorkflowRunsPaginator(_ListWorkflowRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListWorkflowRuns.html#NovaActService.Paginator.ListWorkflowRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listworkflowrunspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/nova-act/paginator/ListWorkflowRuns.html#NovaActService.Paginator.ListWorkflowRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_nova_act/paginators/#listworkflowrunspaginator)
        """
