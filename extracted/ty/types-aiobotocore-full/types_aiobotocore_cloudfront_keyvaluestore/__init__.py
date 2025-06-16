"""
Main interface for cloudfront-keyvaluestore service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudfront_keyvaluestore/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_cloudfront_keyvaluestore import (
        Client,
        CloudFrontKeyValueStoreClient,
        ListKeysPaginator,
    )

    session = get_session()
    async with session.create_client("cloudfront-keyvaluestore") as client:
        client: CloudFrontKeyValueStoreClient
        ...


    list_keys_paginator: ListKeysPaginator = client.get_paginator("list_keys")
    ```
"""

from .client import CloudFrontKeyValueStoreClient
from .paginator import ListKeysPaginator

Client = CloudFrontKeyValueStoreClient


__all__ = ("Client", "CloudFrontKeyValueStoreClient", "ListKeysPaginator")
