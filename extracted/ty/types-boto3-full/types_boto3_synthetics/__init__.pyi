"""
Main interface for synthetics service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_synthetics/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_synthetics import (
        Client,
        SyntheticsClient,
    )

    session = Session()
    client: SyntheticsClient = session.client("synthetics")
    ```
"""

from .client import SyntheticsClient

Client = SyntheticsClient

__all__ = ("Client", "SyntheticsClient")
