"""
Main interface for codestar-connections service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_codestar_connections/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codestar_connections import (
        Client,
        CodeStarconnectionsClient,
    )

    session = Session()
    client: CodeStarconnectionsClient = session.client("codestar-connections")
    ```
"""

from .client import CodeStarconnectionsClient

Client = CodeStarconnectionsClient


__all__ = ("Client", "CodeStarconnectionsClient")
