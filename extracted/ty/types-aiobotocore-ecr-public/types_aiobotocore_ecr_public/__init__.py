"""
Main interface for ecr-public service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ecr_public/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_ecr_public import (
        Client,
        DescribeImageTagsPaginator,
        DescribeImagesPaginator,
        DescribeRegistriesPaginator,
        DescribeRepositoriesPaginator,
        ECRPublicClient,
    )

    session = get_session()
    async with session.create_client("ecr-public") as client:
        client: ECRPublicClient
        ...


    describe_image_tags_paginator: DescribeImageTagsPaginator = client.get_paginator("describe_image_tags")
    describe_images_paginator: DescribeImagesPaginator = client.get_paginator("describe_images")
    describe_registries_paginator: DescribeRegistriesPaginator = client.get_paginator("describe_registries")
    describe_repositories_paginator: DescribeRepositoriesPaginator = client.get_paginator("describe_repositories")
    ```
"""

from .client import ECRPublicClient
from .paginator import (
    DescribeImagesPaginator,
    DescribeImageTagsPaginator,
    DescribeRegistriesPaginator,
    DescribeRepositoriesPaginator,
)

Client = ECRPublicClient


__all__ = (
    "Client",
    "DescribeImageTagsPaginator",
    "DescribeImagesPaginator",
    "DescribeRegistriesPaginator",
    "DescribeRepositoriesPaginator",
    "ECRPublicClient",
)
