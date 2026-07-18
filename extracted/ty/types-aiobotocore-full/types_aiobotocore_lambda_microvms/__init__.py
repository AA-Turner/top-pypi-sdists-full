"""
Main interface for lambda-microvms service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda_microvms/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_lambda_microvms import (
        Client,
        LambdaMicroVMsClient,
        ListManagedMicrovmImageVersionsPaginator,
        ListManagedMicrovmImagesPaginator,
        ListMicrovmImageBuildsPaginator,
        ListMicrovmImageVersionsPaginator,
        ListMicrovmImagesPaginator,
        ListMicrovmsPaginator,
    )

    session = get_session()
    async with session.create_client("lambda-microvms") as client:
        client: LambdaMicroVMsClient
        ...


    list_managed_microvm_image_versions_paginator: ListManagedMicrovmImageVersionsPaginator = client.get_paginator("list_managed_microvm_image_versions")
    list_managed_microvm_images_paginator: ListManagedMicrovmImagesPaginator = client.get_paginator("list_managed_microvm_images")
    list_microvm_image_builds_paginator: ListMicrovmImageBuildsPaginator = client.get_paginator("list_microvm_image_builds")
    list_microvm_image_versions_paginator: ListMicrovmImageVersionsPaginator = client.get_paginator("list_microvm_image_versions")
    list_microvm_images_paginator: ListMicrovmImagesPaginator = client.get_paginator("list_microvm_images")
    list_microvms_paginator: ListMicrovmsPaginator = client.get_paginator("list_microvms")
    ```
"""

from .client import LambdaMicroVMsClient
from .paginator import (
    ListManagedMicrovmImagesPaginator,
    ListManagedMicrovmImageVersionsPaginator,
    ListMicrovmImageBuildsPaginator,
    ListMicrovmImagesPaginator,
    ListMicrovmImageVersionsPaginator,
    ListMicrovmsPaginator,
)

Client = LambdaMicroVMsClient


__all__ = (
    "Client",
    "LambdaMicroVMsClient",
    "ListManagedMicrovmImageVersionsPaginator",
    "ListManagedMicrovmImagesPaginator",
    "ListMicrovmImageBuildsPaginator",
    "ListMicrovmImageVersionsPaginator",
    "ListMicrovmImagesPaginator",
    "ListMicrovmsPaginator",
)
