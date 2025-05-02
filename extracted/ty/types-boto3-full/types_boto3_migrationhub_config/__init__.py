"""
Main interface for migrationhub-config service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_migrationhub_config/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_migrationhub_config import (
        Client,
        MigrationHubConfigClient,
    )

    session = Session()
    client: MigrationHubConfigClient = session.client("migrationhub-config")
    ```
"""

from .client import MigrationHubConfigClient

Client = MigrationHubConfigClient


__all__ = ("Client", "MigrationHubConfigClient")
