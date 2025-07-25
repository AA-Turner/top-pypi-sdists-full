"""
Main interface for b2bi service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_b2bi/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_b2bi import (
        B2BIClient,
        Client,
        ListCapabilitiesPaginator,
        ListPartnershipsPaginator,
        ListProfilesPaginator,
        ListTransformersPaginator,
        TransformerJobSucceededWaiter,
    )

    session = get_session()
    async with session.create_client("b2bi") as client:
        client: B2BIClient
        ...


    transformer_job_succeeded_waiter: TransformerJobSucceededWaiter = client.get_waiter("transformer_job_succeeded")

    list_capabilities_paginator: ListCapabilitiesPaginator = client.get_paginator("list_capabilities")
    list_partnerships_paginator: ListPartnershipsPaginator = client.get_paginator("list_partnerships")
    list_profiles_paginator: ListProfilesPaginator = client.get_paginator("list_profiles")
    list_transformers_paginator: ListTransformersPaginator = client.get_paginator("list_transformers")
    ```
"""

from .client import B2BIClient
from .paginator import (
    ListCapabilitiesPaginator,
    ListPartnershipsPaginator,
    ListProfilesPaginator,
    ListTransformersPaginator,
)
from .waiter import TransformerJobSucceededWaiter

Client = B2BIClient


__all__ = (
    "B2BIClient",
    "Client",
    "ListCapabilitiesPaginator",
    "ListPartnershipsPaginator",
    "ListProfilesPaginator",
    "ListTransformersPaginator",
    "TransformerJobSucceededWaiter",
)
