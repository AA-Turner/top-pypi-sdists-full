"""
Main interface for pi service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_pi/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_pi import (
        Client,
        PIClient,
    )

    session = Session()
    client: PIClient = session.client("pi")
    ```
"""

from .client import PIClient

Client = PIClient


__all__ = ("Client", "PIClient")
