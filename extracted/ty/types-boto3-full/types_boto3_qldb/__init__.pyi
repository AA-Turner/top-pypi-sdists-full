"""
Main interface for qldb service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_qldb/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_qldb import (
        Client,
        QLDBClient,
    )

    session = Session()
    client: QLDBClient = session.client("qldb")
    ```
"""

from .client import QLDBClient

Client = QLDBClient

__all__ = ("Client", "QLDBClient")
