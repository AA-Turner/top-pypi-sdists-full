"""
Main interface for lambda-microvms service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_lambda_microvms/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lambda_microvms import (
        Client,
        LambdaMicroVMsClient,
        ListManagedMicrovmImageVersionsPaginator,
        ListManagedMicrovmImagesPaginator,
        ListMicrovmImageBuildsPaginator,
        ListMicrovmImageVersionsPaginator,
        ListMicrovmImagesPaginator,
        ListMicrovmsPaginator,
    )

    session = Session()
    client: LambdaMicroVMsClient = session.client("lambda-microvms")

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
