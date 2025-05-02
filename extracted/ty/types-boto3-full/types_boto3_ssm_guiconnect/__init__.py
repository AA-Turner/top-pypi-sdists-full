"""
Main interface for ssm-guiconnect service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_ssm_guiconnect/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_ssm_guiconnect import (
        Client,
        SSMGUIConnectClient,
    )

    session = Session()
    client: SSMGUIConnectClient = session.client("ssm-guiconnect")
    ```
"""

from .client import SSMGUIConnectClient

Client = SSMGUIConnectClient


__all__ = ("Client", "SSMGUIConnectClient")
