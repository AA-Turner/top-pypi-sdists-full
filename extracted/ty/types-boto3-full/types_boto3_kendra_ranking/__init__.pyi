"""
Main interface for kendra-ranking service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_kendra_ranking/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_kendra_ranking import (
        Client,
        KendraRankingClient,
    )

    session = Session()
    client: KendraRankingClient = session.client("kendra-ranking")
    ```
"""

from .client import KendraRankingClient

Client = KendraRankingClient

__all__ = ("Client", "KendraRankingClient")
