"""
Main interface for workmailmessageflow service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_workmailmessageflow/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_workmailmessageflow import (
        Client,
        WorkMailMessageFlowClient,
    )

    session = Session()
    client: WorkMailMessageFlowClient = session.client("workmailmessageflow")
    ```
"""

from .client import WorkMailMessageFlowClient

Client = WorkMailMessageFlowClient


__all__ = ("Client", "WorkMailMessageFlowClient")
