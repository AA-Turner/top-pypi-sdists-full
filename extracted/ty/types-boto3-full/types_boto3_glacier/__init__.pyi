"""
Main interface for glacier service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_glacier/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_glacier import (
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

    session = Session()
    client: GlacierClient = session.client("glacier")

    resource: GlacierServiceResource = session.resource("glacier")

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
