"""
Main interface for apprunner service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_apprunner/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_apprunner import (
        AppRunnerClient,
        Client,
    )

    session = get_session()
    async with session.create_client("apprunner") as client:
        client: AppRunnerClient
        ...

    ```
"""

from .client import AppRunnerClient

Client = AppRunnerClient

__all__ = ("AppRunnerClient", "Client")
