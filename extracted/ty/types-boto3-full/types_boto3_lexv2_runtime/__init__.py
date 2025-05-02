"""
Main interface for lexv2-runtime service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_lexv2_runtime/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lexv2_runtime import (
        Client,
        LexRuntimeV2Client,
    )

    session = Session()
    client: LexRuntimeV2Client = session.client("lexv2-runtime")
    ```
"""

from .client import LexRuntimeV2Client

Client = LexRuntimeV2Client


__all__ = ("Client", "LexRuntimeV2Client")
