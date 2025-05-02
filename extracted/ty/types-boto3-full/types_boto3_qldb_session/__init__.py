"""
Main interface for qldb-session service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb_session/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_qldb_session import (
        Client,
        QLDBSessionClient,
    )

    session = Session()
    client: QLDBSessionClient = session.client("qldb-session")
    ```
"""

from .client import QLDBSessionClient

Client = QLDBSessionClient


__all__ = ("Client", "QLDBSessionClient")
