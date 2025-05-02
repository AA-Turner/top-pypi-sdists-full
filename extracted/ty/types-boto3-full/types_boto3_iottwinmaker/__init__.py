"""
Main interface for iottwinmaker service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_iottwinmaker/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_iottwinmaker import (
        Client,
        IoTTwinMakerClient,
    )

    session = Session()
    client: IoTTwinMakerClient = session.client("iottwinmaker")
    ```
"""

from .client import IoTTwinMakerClient

Client = IoTTwinMakerClient


__all__ = ("Client", "IoTTwinMakerClient")
