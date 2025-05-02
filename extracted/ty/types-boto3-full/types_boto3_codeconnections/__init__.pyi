"""
Main interface for codeconnections service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codeconnections/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codeconnections import (
        Client,
        CodeConnectionsClient,
    )

    session = Session()
    client: CodeConnectionsClient = session.client("codeconnections")
    ```
"""

from .client import CodeConnectionsClient

Client = CodeConnectionsClient

__all__ = ("Client", "CodeConnectionsClient")
