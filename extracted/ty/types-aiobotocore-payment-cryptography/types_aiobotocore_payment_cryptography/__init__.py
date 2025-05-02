"""
Main interface for payment-cryptography service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_payment_cryptography import (
        Client,
        ListAliasesPaginator,
        ListKeysPaginator,
        ListTagsForResourcePaginator,
        PaymentCryptographyControlPlaneClient,
    )

    session = get_session()
    async with session.create_client("payment-cryptography") as client:
        client: PaymentCryptographyControlPlaneClient
        ...


    list_aliases_paginator: ListAliasesPaginator = client.get_paginator("list_aliases")
    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from .client import PaymentCryptographyControlPlaneClient
from .paginator import ListAliasesPaginator, ListKeysPaginator, ListTagsForResourcePaginator

Client = PaymentCryptographyControlPlaneClient


__all__ = (
    "Client",
    "ListAliasesPaginator",
    "ListKeysPaginator",
    "ListTagsForResourcePaginator",
    "PaymentCryptographyControlPlaneClient",
)
