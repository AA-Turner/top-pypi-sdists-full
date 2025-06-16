"""
Main interface for ssm-guiconnect service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm_guiconnect/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ssm_guiconnect import (
        Client,
        SSMGUIConnectClient,
    )

    session = get_session()
    async with session.create_client("ssm-guiconnect") as client:
        client: SSMGUIConnectClient
        ...

    ```
"""

from .client import SSMGUIConnectClient

Client = SSMGUIConnectClient


__all__ = ("Client", "SSMGUIConnectClient")
