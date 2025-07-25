"""
Type annotations for bedrock-agentcore service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_bedrock_agentcore.client import BedrockAgentCoreDataPlaneFrontingLayerClient
    from types_aiobotocore_bedrock_agentcore.paginator import (
        ListActorsPaginator,
        ListEventsPaginator,
        ListMemoryRecordsPaginator,
        ListSessionsPaginator,
        RetrieveMemoryRecordsPaginator,
    )

    session = get_session()
    with session.create_client("bedrock-agentcore") as client:
        client: BedrockAgentCoreDataPlaneFrontingLayerClient

        list_actors_paginator: ListActorsPaginator = client.get_paginator("list_actors")
        list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
        list_memory_records_paginator: ListMemoryRecordsPaginator = client.get_paginator("list_memory_records")
        list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
        retrieve_memory_records_paginator: RetrieveMemoryRecordsPaginator = client.get_paginator("retrieve_memory_records")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListActorsInputPaginateTypeDef,
    ListActorsOutputTypeDef,
    ListEventsInputPaginateTypeDef,
    ListEventsOutputTypeDef,
    ListMemoryRecordsInputPaginateTypeDef,
    ListMemoryRecordsOutputTypeDef,
    ListSessionsInputPaginateTypeDef,
    ListSessionsOutputTypeDef,
    RetrieveMemoryRecordsInputPaginateTypeDef,
    RetrieveMemoryRecordsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListActorsPaginator",
    "ListEventsPaginator",
    "ListMemoryRecordsPaginator",
    "ListSessionsPaginator",
    "RetrieveMemoryRecordsPaginator",
)

if TYPE_CHECKING:
    _ListActorsPaginatorBase = AioPaginator[ListActorsOutputTypeDef]
else:
    _ListActorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListActorsPaginator(_ListActorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListActors.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListActors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listactorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListActorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListActors.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListActors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listactorspaginator)
        """

if TYPE_CHECKING:
    _ListEventsPaginatorBase = AioPaginator[ListEventsOutputTypeDef]
else:
    _ListEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEventsPaginator(_ListEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListEvents.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListEvents.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listeventspaginator)
        """

if TYPE_CHECKING:
    _ListMemoryRecordsPaginatorBase = AioPaginator[ListMemoryRecordsOutputTypeDef]
else:
    _ListMemoryRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListMemoryRecordsPaginator(_ListMemoryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListMemoryRecords.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListMemoryRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listmemoryrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMemoryRecordsInputPaginateTypeDef]
    ) -> AioPageIterator[ListMemoryRecordsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListMemoryRecords.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListMemoryRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listmemoryrecordspaginator)
        """

if TYPE_CHECKING:
    _ListSessionsPaginatorBase = AioPaginator[ListSessionsOutputTypeDef]
else:
    _ListSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSessionsPaginator(_ListSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListSessions.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listsessionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSessionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSessionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/ListSessions.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.ListSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#listsessionspaginator)
        """

if TYPE_CHECKING:
    _RetrieveMemoryRecordsPaginatorBase = AioPaginator[RetrieveMemoryRecordsOutputTypeDef]
else:
    _RetrieveMemoryRecordsPaginatorBase = AioPaginator  # type: ignore[assignment]

class RetrieveMemoryRecordsPaginator(_RetrieveMemoryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/RetrieveMemoryRecords.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.RetrieveMemoryRecords)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#retrievememoryrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[RetrieveMemoryRecordsInputPaginateTypeDef]
    ) -> AioPageIterator[RetrieveMemoryRecordsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore/paginator/RetrieveMemoryRecords.html#BedrockAgentCoreDataPlaneFrontingLayer.Paginator.RetrieveMemoryRecords.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/paginators/#retrievememoryrecordspaginator)
        """
