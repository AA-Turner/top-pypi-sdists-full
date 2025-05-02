"""
Main interface for cognito-identity service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cognito_identity/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cognito_identity import (
        Client,
        CognitoIdentityClient,
        ListIdentityPoolsPaginator,
    )

    session = get_session()
    async with session.create_client("cognito-identity") as client:
        client: CognitoIdentityClient
        ...


    list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```
"""

from .client import CognitoIdentityClient
from .paginator import ListIdentityPoolsPaginator

Client = CognitoIdentityClient

__all__ = ("Client", "CognitoIdentityClient", "ListIdentityPoolsPaginator")
