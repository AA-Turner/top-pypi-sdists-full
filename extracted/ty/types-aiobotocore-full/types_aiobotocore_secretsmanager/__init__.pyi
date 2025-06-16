"""
Main interface for secretsmanager service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_secretsmanager/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_secretsmanager import (
        Client,
        ListSecretsPaginator,
        SecretsManagerClient,
    )

    session = get_session()
    async with session.create_client("secretsmanager") as client:
        client: SecretsManagerClient
        ...


    list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```
"""

from .client import SecretsManagerClient
from .paginator import ListSecretsPaginator

Client = SecretsManagerClient

__all__ = ("Client", "ListSecretsPaginator", "SecretsManagerClient")
