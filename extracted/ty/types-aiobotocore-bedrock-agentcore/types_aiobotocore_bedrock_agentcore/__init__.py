"""
Main interface for bedrock-agentcore service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_bedrock_agentcore/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_bedrock_agentcore import (
        BedrockAgentCoreClient,
        Client,
        ListActorsPaginator,
        ListEventsPaginator,
        ListMemoryExtractionJobsPaginator,
        ListMemoryRecordsPaginator,
        ListSessionsPaginator,
        RetrieveMemoryRecordsPaginator,
    )

    session = get_session()
    async with session.create_client("bedrock-agentcore") as client:
        client: BedrockAgentCoreClient
        ...


    list_actors_paginator: ListActorsPaginator = client.get_paginator("list_actors")
    list_events_paginator: ListEventsPaginator = client.get_paginator("list_events")
    list_memory_extraction_jobs_paginator: ListMemoryExtractionJobsPaginator = client.get_paginator("list_memory_extraction_jobs")
    list_memory_records_paginator: ListMemoryRecordsPaginator = client.get_paginator("list_memory_records")
    list_sessions_paginator: ListSessionsPaginator = client.get_paginator("list_sessions")
    retrieve_memory_records_paginator: RetrieveMemoryRecordsPaginator = client.get_paginator("retrieve_memory_records")
    ```
"""

from .client import BedrockAgentCoreClient
from .paginator import (
    ListActorsPaginator,
    ListEventsPaginator,
    ListMemoryExtractionJobsPaginator,
    ListMemoryRecordsPaginator,
    ListSessionsPaginator,
    RetrieveMemoryRecordsPaginator,
)

Client = BedrockAgentCoreClient


__all__ = (
    "BedrockAgentCoreClient",
    "Client",
    "ListActorsPaginator",
    "ListEventsPaginator",
    "ListMemoryExtractionJobsPaginator",
    "ListMemoryRecordsPaginator",
    "ListSessionsPaginator",
    "RetrieveMemoryRecordsPaginator",
)
