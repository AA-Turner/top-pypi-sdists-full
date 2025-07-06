"""
Main interface for textract service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_textract/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_textract import (
        Client,
        ListAdapterVersionsPaginator,
        ListAdaptersPaginator,
        TextractClient,
    )

    session = get_session()
    async with session.create_client("textract") as client:
        client: TextractClient
        ...


    list_adapter_versions_paginator: ListAdapterVersionsPaginator = client.get_paginator("list_adapter_versions")
    list_adapters_paginator: ListAdaptersPaginator = client.get_paginator("list_adapters")
    ```
"""

from .client import TextractClient
from .paginator import ListAdaptersPaginator, ListAdapterVersionsPaginator

Client = TextractClient

__all__ = ("Client", "ListAdapterVersionsPaginator", "ListAdaptersPaginator", "TextractClient")
