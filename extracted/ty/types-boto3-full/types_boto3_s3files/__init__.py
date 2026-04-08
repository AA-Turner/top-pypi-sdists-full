"""
Main interface for s3files service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3files/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_s3files import (
        Client,
        ListAccessPointsPaginator,
        ListFileSystemsPaginator,
        ListMountTargetsPaginator,
        ListTagsForResourcePaginator,
        S3FilesClient,
    )

    session = Session()
    client: S3FilesClient = session.client("s3files")

    list_access_points_paginator: ListAccessPointsPaginator = client.get_paginator("list_access_points")
    list_file_systems_paginator: ListFileSystemsPaginator = client.get_paginator("list_file_systems")
    list_mount_targets_paginator: ListMountTargetsPaginator = client.get_paginator("list_mount_targets")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from .client import S3FilesClient
from .paginator import (
    ListAccessPointsPaginator,
    ListFileSystemsPaginator,
    ListMountTargetsPaginator,
    ListTagsForResourcePaginator,
)

Client = S3FilesClient


__all__ = (
    "Client",
    "ListAccessPointsPaginator",
    "ListFileSystemsPaginator",
    "ListMountTargetsPaginator",
    "ListTagsForResourcePaginator",
    "S3FilesClient",
)
