"""
Main interface for sagemaker-a2i-runtime service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sagemaker_a2i_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_sagemaker_a2i_runtime import (
        AugmentedAIRuntimeClient,
        Client,
        ListHumanLoopsPaginator,
    )

    session = get_session()
    async with session.create_client("sagemaker-a2i-runtime") as client:
        client: AugmentedAIRuntimeClient
        ...


    list_human_loops_paginator: ListHumanLoopsPaginator = client.get_paginator("list_human_loops")
    ```
"""

from .client import AugmentedAIRuntimeClient
from .paginator import ListHumanLoopsPaginator

Client = AugmentedAIRuntimeClient

__all__ = ("AugmentedAIRuntimeClient", "Client", "ListHumanLoopsPaginator")
