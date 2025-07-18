"""
Type annotations for fsx service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_fsx.client import FSxClient
    from types_aiobotocore_fsx.paginator import (
        DescribeBackupsPaginator,
        DescribeFileSystemsPaginator,
        DescribeS3AccessPointAttachmentsPaginator,
        DescribeSnapshotsPaginator,
        DescribeStorageVirtualMachinesPaginator,
        DescribeVolumesPaginator,
        ListTagsForResourcePaginator,
    )

    session = get_session()
    with session.create_client("fsx") as client:
        client: FSxClient

        describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
        describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
        describe_s3_access_point_attachments_paginator: DescribeS3AccessPointAttachmentsPaginator = client.get_paginator("describe_s3_access_point_attachments")
        describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
        describe_storage_virtual_machines_paginator: DescribeStorageVirtualMachinesPaginator = client.get_paginator("describe_storage_virtual_machines")
        describe_volumes_paginator: DescribeVolumesPaginator = client.get_paginator("describe_volumes")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeBackupsRequestPaginateTypeDef,
    DescribeBackupsResponsePaginatorTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeFileSystemsRequestPaginateTypeDef,
    DescribeFileSystemsResponsePaginatorTypeDef,
    DescribeS3AccessPointAttachmentsRequestPaginateTypeDef,
    DescribeS3AccessPointAttachmentsResponseTypeDef,
    DescribeSnapshotsRequestPaginateTypeDef,
    DescribeSnapshotsResponsePaginatorTypeDef,
    DescribeStorageVirtualMachinesRequestPaginateTypeDef,
    DescribeStorageVirtualMachinesResponseTypeDef,
    DescribeVolumesRequestPaginateTypeDef,
    DescribeVolumesResponsePaginatorTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeBackupsPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeS3AccessPointAttachmentsPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeStorageVirtualMachinesPaginator",
    "DescribeVolumesPaginator",
    "ListTagsForResourcePaginator",
)


if TYPE_CHECKING:
    _DescribeBackupsPaginatorBase = AioPaginator[DescribeBackupsResponseTypeDef]
else:
    _DescribeBackupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeBackupsPaginator(_DescribeBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeBackups.html#FSx.Paginator.DescribeBackups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describebackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBackupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBackupsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeBackups.html#FSx.Paginator.DescribeBackups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describebackupspaginator)
        """


if TYPE_CHECKING:
    _DescribeFileSystemsPaginatorBase = AioPaginator[DescribeFileSystemsResponsePaginatorTypeDef]
else:
    _DescribeFileSystemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeFileSystemsPaginator(_DescribeFileSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeFileSystems.html#FSx.Paginator.DescribeFileSystems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describefilesystemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFileSystemsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeFileSystemsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeFileSystems.html#FSx.Paginator.DescribeFileSystems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describefilesystemspaginator)
        """


if TYPE_CHECKING:
    _DescribeS3AccessPointAttachmentsPaginatorBase = AioPaginator[
        DescribeS3AccessPointAttachmentsResponseTypeDef
    ]
else:
    _DescribeS3AccessPointAttachmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeS3AccessPointAttachmentsPaginator(_DescribeS3AccessPointAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeS3AccessPointAttachments.html#FSx.Paginator.DescribeS3AccessPointAttachments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describes3accesspointattachmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeS3AccessPointAttachmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeS3AccessPointAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeS3AccessPointAttachments.html#FSx.Paginator.DescribeS3AccessPointAttachments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describes3accesspointattachmentspaginator)
        """


if TYPE_CHECKING:
    _DescribeSnapshotsPaginatorBase = AioPaginator[DescribeSnapshotsResponsePaginatorTypeDef]
else:
    _DescribeSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSnapshotsPaginator(_DescribeSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapshots.html#FSx.Paginator.DescribeSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSnapshotsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapshots.html#FSx.Paginator.DescribeSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describesnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeStorageVirtualMachinesPaginatorBase = AioPaginator[
        DescribeStorageVirtualMachinesResponseTypeDef
    ]
else:
    _DescribeStorageVirtualMachinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeStorageVirtualMachinesPaginator(_DescribeStorageVirtualMachinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachines.html#FSx.Paginator.DescribeStorageVirtualMachines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describestoragevirtualmachinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStorageVirtualMachinesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeStorageVirtualMachinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachines.html#FSx.Paginator.DescribeStorageVirtualMachines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describestoragevirtualmachinespaginator)
        """


if TYPE_CHECKING:
    _DescribeVolumesPaginatorBase = AioPaginator[DescribeVolumesResponsePaginatorTypeDef]
else:
    _DescribeVolumesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeVolumesPaginator(_DescribeVolumesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeVolumes.html#FSx.Paginator.DescribeVolumes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describevolumespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVolumesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeVolumesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeVolumes.html#FSx.Paginator.DescribeVolumes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#describevolumespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/ListTagsForResource.html#FSx.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/ListTagsForResource.html#FSx.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_fsx/paginators/#listtagsforresourcepaginator)
        """
