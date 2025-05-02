"""
Main interface for apprunner service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_apprunner/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_apprunner import (
        AppRunnerClient,
        Client,
    )

    session = Session()
    client: AppRunnerClient = session.client("apprunner")
    ```
"""

from .client import AppRunnerClient

Client = AppRunnerClient


__all__ = ("AppRunnerClient", "Client")
