"""
Main interface for kendra service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kendra/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kendra import (
        Client,
        KendraClient,
    )

    session = Session()
    client: KendraClient = session.client("kendra")
    ```
"""

from .client import KendraClient

Client = KendraClient


__all__ = ("Client", "KendraClient")
