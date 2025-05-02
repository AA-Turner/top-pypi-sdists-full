"""
Main interface for workmailmessageflow service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_workmailmessageflow/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_workmailmessageflow import (
        Client,
        WorkMailMessageFlowClient,
    )

    session = get_session()
    async with session.create_client("workmailmessageflow") as client:
        client: WorkMailMessageFlowClient
        ...

    ```
"""

from .client import WorkMailMessageFlowClient

Client = WorkMailMessageFlowClient


__all__ = ("Client", "WorkMailMessageFlowClient")
