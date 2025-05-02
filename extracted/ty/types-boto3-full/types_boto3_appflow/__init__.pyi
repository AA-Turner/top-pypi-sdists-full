"""
Main interface for appflow service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_appflow/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_appflow import (
        AppflowClient,
        Client,
    )

    session = Session()
    client: AppflowClient = session.client("appflow")
    ```
"""

from .client import AppflowClient

Client = AppflowClient

__all__ = ("AppflowClient", "Client")
