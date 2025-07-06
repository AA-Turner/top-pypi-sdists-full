"""
Main interface for support service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_support/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_support import (
        Client,
        DescribeCasesPaginator,
        DescribeCommunicationsPaginator,
        SupportClient,
    )

    session = get_session()
    async with session.create_client("support") as client:
        client: SupportClient
        ...


    describe_cases_paginator: DescribeCasesPaginator = client.get_paginator("describe_cases")
    describe_communications_paginator: DescribeCommunicationsPaginator = client.get_paginator("describe_communications")
    ```
"""

from .client import SupportClient
from .paginator import DescribeCasesPaginator, DescribeCommunicationsPaginator

Client = SupportClient


__all__ = ("Client", "DescribeCasesPaginator", "DescribeCommunicationsPaginator", "SupportClient")
