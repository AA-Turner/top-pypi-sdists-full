"""
Main interface for glacier service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_glacier/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_glacier import (
        Client,
        GlacierClient,
        GlacierServiceResource,
        ListJobsPaginator,
        ListMultipartUploadsPaginator,
        ListPartsPaginator,
        ListVaultsPaginator,
        ServiceResource,
        VaultExistsWaiter,
        VaultNotExistsWaiter,
    )

    session = get_session()
    async with session.create_client("glacier") as client:
        client: GlacierClient
        ...


    vault_exists_waiter: VaultExistsWaiter = client.get_waiter("vault_exists")
    vault_not_exists_waiter: VaultNotExistsWaiter = client.get_waiter("vault_not_exists")

    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_multipart_uploads_paginator: ListMultipartUploadsPaginator = client.get_paginator("list_multipart_uploads")
    list_parts_paginator: ListPartsPaginator = client.get_paginator("list_parts")
    list_vaults_paginator: ListVaultsPaginator = client.get_paginator("list_vaults")
    ```
"""

from .client import GlacierClient
from .paginator import (
    ListJobsPaginator,
    ListMultipartUploadsPaginator,
    ListPartsPaginator,
    ListVaultsPaginator,
)
from .waiter import VaultExistsWaiter, VaultNotExistsWaiter

try:
    from .service_resource import GlacierServiceResource
except ImportError:
    from builtins import object as GlacierServiceResource  # type: ignore[assignment]

Client = GlacierClient

ServiceResource = GlacierServiceResource

__all__ = (
    "Client",
    "GlacierClient",
    "GlacierServiceResource",
    "ListJobsPaginator",
    "ListMultipartUploadsPaginator",
    "ListPartsPaginator",
    "ListVaultsPaginator",
    "ServiceResource",
    "VaultExistsWaiter",
    "VaultNotExistsWaiter",
)
