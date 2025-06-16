"""
Type annotations for bedrock-agent-runtime service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agent_runtime.client import AgentsforBedrockRuntimeClient
    from types_aiobotocore_bedrock_agent_runtime.paginator import (
        GetAgentMemoryPaginator,
        ListFlowExecutionEventsPaginator,
        ListFlowExecutionsPaginator,
        ListInvocationStepsPaginator,
        ListInvocationsPaginator,
        ListSessionsPaginator,
        RerankPaginator,
        RetrievePaginator,
    )

    session = get_session()
    with session.create_client("bedrock-agent-runtime") as client:
        client: AgentsforBedrockRuntimeClient

        get_agent_memory_paginator: GetAgentMemoryPaginator = client.get_paginator("get_agent_memory")
        list_flow_execution_events_paginator: ListFlowExecutionEventsPaginator = client.get_paginator("list_flow_execution_events")
        list_flow_executions_paginator: ListFlowExecutionsPaginator = client.get_paginator("list_flow_executions")
        list_invocation_steps_paginator: ListInvocationStepsPaginator = client.get_paginator("list_invocation_steps")
        list_invocations_paginator: ListInvocationsPaginator = client.get_paginator("list_invocations")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
        rerank_paginator: RerankPaginator = client.get_paginator("rerank")
        retrieve_paginator: RetrievePaginator = client.get_paginator("retrieve")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetAgentMemoryRequestPaginateTypeDef,
    GetAgentMemoryResponseTypeDef,
    ListFlowExecutionEventsRequestPaginateTypeDef,
    ListFlowExecutionEventsResponseTypeDef,
    ListFlowExecutionsRequestPaginateTypeDef,
    ListFlowExecutionsResponseTypeDef,
    ListInvocationsRequestPaginateTypeDef,
    ListInvocationsResponseTypeDef,
    ListInvocationStepsRequestPaginateTypeDef,
    ListInvocationStepsResponseTypeDef,
    ListSessionsRequestPaginateTypeDef,
    ListSessionsResponseTypeDef,
    RerankRequestPaginateTypeDef,
    RerankResponseTypeDef,
    RetrieveRequestPaginateTypeDef,
    RetrieveResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetAgentMemoryPaginator",
    "ListFlowExecutionEventsPaginator",
    "ListFlowExecutionsPaginator",
    "ListInvocationStepsPaginator",
    "ListInvocationsPaginator",
    "ListSessionsPaginator",
    "RerankPaginator",
    "RetrievePaginator",
)


if TYPE_CHECKING:
    _GetAgentMemoryPaginatorBase = AioPaginator[GetAgentMemoryResponseTypeDef]
else:
    _GetAgentMemoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetAgentMemoryPaginator(_GetAgentMemoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetAgentMemoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetAgentMemoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/GetAgentMemory.html#AgentsforBedrockRuntime.Paginator.GetAgentMemory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#getagentmemorypaginator)
        """


if TYPE_CHECKING:
    _ListFlowExecutionEventsPaginatorBase = AioPaginator[ListFlowExecutionEventsResponseTypeDef]
else:
    _ListFlowExecutionEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFlowExecutionEventsPaginator(_ListFlowExecutionEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListFlowExecutionEvents.html#AgentsforBedrockRuntime.Paginator.ListFlowExecutionEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listflowexecutioneventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowExecutionEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowExecutionEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListFlowExecutionEvents.html#AgentsforBedrockRuntime.Paginator.ListFlowExecutionEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listflowexecutioneventspaginator)
        """


if TYPE_CHECKING:
    _ListFlowExecutionsPaginatorBase = AioPaginator[ListFlowExecutionsResponseTypeDef]
else:
    _ListFlowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFlowExecutionsPaginator(_ListFlowExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListFlowExecutions.html#AgentsforBedrockRuntime.Paginator.ListFlowExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listflowexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListFlowExecutions.html#AgentsforBedrockRuntime.Paginator.ListFlowExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listflowexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListInvocationStepsPaginatorBase = AioPaginator[ListInvocationStepsResponseTypeDef]
else:
    _ListInvocationStepsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInvocationStepsPaginator(_ListInvocationStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListInvocationSteps.html#AgentsforBedrockRuntime.Paginator.ListInvocationSteps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listinvocationstepspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvocationStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInvocationStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListInvocationSteps.html#AgentsforBedrockRuntime.Paginator.ListInvocationSteps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listinvocationstepspaginator)
        """


if TYPE_CHECKING:
    _ListInvocationsPaginatorBase = AioPaginator[ListInvocationsResponseTypeDef]
else:
    _ListInvocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInvocationsPaginator(_ListInvocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListInvocations.html#AgentsforBedrockRuntime.Paginator.ListInvocations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listinvocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInvocationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInvocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListInvocations.html#AgentsforBedrockRuntime.Paginator.ListInvocations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listinvocationspaginator)
        """


if TYPE_CHECKING:
    _ListSessionsPaginatorBase = AioPaginator[ListSessionsResponseTypeDef]
else:
    _ListSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSessionsPaginator(_ListSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListSessions.html#AgentsforBedrockRuntime.Paginator.ListSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listsessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/ListSessions.html#AgentsforBedrockRuntime.Paginator.ListSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#listsessionspaginator)
        """


if TYPE_CHECKING:
    _RerankPaginatorBase = AioPaginator[RerankResponseTypeDef]
else:
    _RerankPaginatorBase = AioPaginator  # type: ignore[assignment]


class RerankPaginator(_RerankPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#rerankpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RerankRequestPaginateTypeDef]
    ) -> AioPageIterator[RerankResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Rerank.html#AgentsforBedrockRuntime.Paginator.Rerank.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#rerankpaginator)
        """


if TYPE_CHECKING:
    _RetrievePaginatorBase = AioPaginator[RetrieveResponseTypeDef]
else:
    _RetrievePaginatorBase = AioPaginator  # type: ignore[assignment]


class RetrievePaginator(_RetrievePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#retrievepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RetrieveRequestPaginateTypeDef]
    ) -> AioPageIterator[RetrieveResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agent-runtime/paginator/Retrieve.html#AgentsforBedrockRuntime.Paginator.Retrieve.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agent_runtime/paginators/#retrievepaginator)
        """
