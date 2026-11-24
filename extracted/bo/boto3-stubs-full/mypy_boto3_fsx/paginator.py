"""
Type annotations for fsx service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_fsx.client import FSxClient
    from mypy_boto3_fsx.paginator import (
        DescribeBackupsPaginator,
        DescribeClusterPeersPaginator,
        DescribeFileSystemsPaginator,
        DescribeS3AccessPointAttachmentsPaginator,
        DescribeSnapmirrorPoliciesPaginator,
        DescribeSnapmirrorRelationshipsPaginator,
        DescribeSnapshotPoliciesPaginator,
        DescribeSnapshotsPaginator,
        DescribeStorageVirtualMachinePeersPaginator,
        DescribeStorageVirtualMachinesPaginator,
        DescribeVolumesPaginator,
        ListTagsForResourcePaginator,
    )

    session = Session()
    client: FSxClient = session.client("fsx")

    describe_backups_paginator: DescribeBackupsPaginator = client.get_paginator("describe_backups")
    describe_cluster_peers_paginator: DescribeClusterPeersPaginator = client.get_paginator("describe_cluster_peers")
    describe_file_systems_paginator: DescribeFileSystemsPaginator = client.get_paginator("describe_file_systems")
    describe_s3_access_point_attachments_paginator: DescribeS3AccessPointAttachmentsPaginator = client.get_paginator("describe_s3_access_point_attachments")
    describe_snapmirror_policies_paginator: DescribeSnapmirrorPoliciesPaginator = client.get_paginator("describe_snapmirror_policies")
    describe_snapmirror_relationships_paginator: DescribeSnapmirrorRelationshipsPaginator = client.get_paginator("describe_snapmirror_relationships")
    describe_snapshot_policies_paginator: DescribeSnapshotPoliciesPaginator = client.get_paginator("describe_snapshot_policies")
    describe_snapshots_paginator: DescribeSnapshotsPaginator = client.get_paginator("describe_snapshots")
    describe_storage_virtual_machine_peers_paginator: DescribeStorageVirtualMachinePeersPaginator = client.get_paginator("describe_storage_virtual_machine_peers")
    describe_storage_virtual_machines_paginator: DescribeStorageVirtualMachinesPaginator = client.get_paginator("describe_storage_virtual_machines")
    describe_volumes_paginator: DescribeVolumesPaginator = client.get_paginator("describe_volumes")
    list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    DescribeBackupsRequestPaginateTypeDef,
    DescribeBackupsResponsePaginatorTypeDef,
    DescribeBackupsResponseTypeDef,
    DescribeClusterPeersRequestPaginateTypeDef,
    DescribeClusterPeersResponseTypeDef,
    DescribeFileSystemsRequestPaginateTypeDef,
    DescribeFileSystemsResponsePaginatorTypeDef,
    DescribeS3AccessPointAttachmentsRequestPaginateTypeDef,
    DescribeS3AccessPointAttachmentsResponseTypeDef,
    DescribeSnapmirrorPoliciesRequestPaginateTypeDef,
    DescribeSnapmirrorPoliciesResponseTypeDef,
    DescribeSnapmirrorRelationshipsRequestPaginateTypeDef,
    DescribeSnapmirrorRelationshipsResponseTypeDef,
    DescribeSnapshotPoliciesRequestPaginateTypeDef,
    DescribeSnapshotPoliciesResponseTypeDef,
    DescribeSnapshotsRequestPaginateTypeDef,
    DescribeSnapshotsResponsePaginatorTypeDef,
    DescribeStorageVirtualMachinePeersRequestPaginateTypeDef,
    DescribeStorageVirtualMachinePeersResponseTypeDef,
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
    "DescribeClusterPeersPaginator",
    "DescribeFileSystemsPaginator",
    "DescribeS3AccessPointAttachmentsPaginator",
    "DescribeSnapmirrorPoliciesPaginator",
    "DescribeSnapmirrorRelationshipsPaginator",
    "DescribeSnapshotPoliciesPaginator",
    "DescribeSnapshotsPaginator",
    "DescribeStorageVirtualMachinePeersPaginator",
    "DescribeStorageVirtualMachinesPaginator",
    "DescribeVolumesPaginator",
    "ListTagsForResourcePaginator",
)


if TYPE_CHECKING:
    _DescribeBackupsPaginatorBase = Paginator[DescribeBackupsResponseTypeDef]
else:
    _DescribeBackupsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeBackupsPaginator(_DescribeBackupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeBackups.html#FSx.Paginator.DescribeBackups)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describebackupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBackupsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeBackupsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeBackups.html#FSx.Paginator.DescribeBackups.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describebackupspaginator)
        """


if TYPE_CHECKING:
    _DescribeClusterPeersPaginatorBase = Paginator[DescribeClusterPeersResponseTypeDef]
else:
    _DescribeClusterPeersPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeClusterPeersPaginator(_DescribeClusterPeersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeClusterPeers.html#FSx.Paginator.DescribeClusterPeers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describeclusterpeerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterPeersRequestPaginateTypeDef]
    ) -> PageIterator[DescribeClusterPeersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeClusterPeers.html#FSx.Paginator.DescribeClusterPeers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describeclusterpeerspaginator)
        """


if TYPE_CHECKING:
    _DescribeFileSystemsPaginatorBase = Paginator[DescribeFileSystemsResponsePaginatorTypeDef]
else:
    _DescribeFileSystemsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeFileSystemsPaginator(_DescribeFileSystemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeFileSystems.html#FSx.Paginator.DescribeFileSystems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describefilesystemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeFileSystemsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeFileSystemsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeFileSystems.html#FSx.Paginator.DescribeFileSystems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describefilesystemspaginator)
        """


if TYPE_CHECKING:
    _DescribeS3AccessPointAttachmentsPaginatorBase = Paginator[
        DescribeS3AccessPointAttachmentsResponseTypeDef
    ]
else:
    _DescribeS3AccessPointAttachmentsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeS3AccessPointAttachmentsPaginator(_DescribeS3AccessPointAttachmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeS3AccessPointAttachments.html#FSx.Paginator.DescribeS3AccessPointAttachments)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describes3accesspointattachmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeS3AccessPointAttachmentsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeS3AccessPointAttachmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeS3AccessPointAttachments.html#FSx.Paginator.DescribeS3AccessPointAttachments.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describes3accesspointattachmentspaginator)
        """


if TYPE_CHECKING:
    _DescribeSnapmirrorPoliciesPaginatorBase = Paginator[DescribeSnapmirrorPoliciesResponseTypeDef]
else:
    _DescribeSnapmirrorPoliciesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeSnapmirrorPoliciesPaginator(_DescribeSnapmirrorPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapmirrorPolicies.html#FSx.Paginator.DescribeSnapmirrorPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapmirrorpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapmirrorPoliciesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeSnapmirrorPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapmirrorPolicies.html#FSx.Paginator.DescribeSnapmirrorPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapmirrorpoliciespaginator)
        """


if TYPE_CHECKING:
    _DescribeSnapmirrorRelationshipsPaginatorBase = Paginator[
        DescribeSnapmirrorRelationshipsResponseTypeDef
    ]
else:
    _DescribeSnapmirrorRelationshipsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeSnapmirrorRelationshipsPaginator(_DescribeSnapmirrorRelationshipsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapmirrorRelationships.html#FSx.Paginator.DescribeSnapmirrorRelationships)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapmirrorrelationshipspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapmirrorRelationshipsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeSnapmirrorRelationshipsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapmirrorRelationships.html#FSx.Paginator.DescribeSnapmirrorRelationships.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapmirrorrelationshipspaginator)
        """


if TYPE_CHECKING:
    _DescribeSnapshotPoliciesPaginatorBase = Paginator[DescribeSnapshotPoliciesResponseTypeDef]
else:
    _DescribeSnapshotPoliciesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeSnapshotPoliciesPaginator(_DescribeSnapshotPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapshotPolicies.html#FSx.Paginator.DescribeSnapshotPolicies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapshotpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapshotPoliciesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeSnapshotPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapshotPolicies.html#FSx.Paginator.DescribeSnapshotPolicies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapshotpoliciespaginator)
        """


if TYPE_CHECKING:
    _DescribeSnapshotsPaginatorBase = Paginator[DescribeSnapshotsResponsePaginatorTypeDef]
else:
    _DescribeSnapshotsPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeSnapshotsPaginator(_DescribeSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapshots.html#FSx.Paginator.DescribeSnapshots)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSnapshotsRequestPaginateTypeDef]
    ) -> PageIterator[DescribeSnapshotsResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeSnapshots.html#FSx.Paginator.DescribeSnapshots.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describesnapshotspaginator)
        """


if TYPE_CHECKING:
    _DescribeStorageVirtualMachinePeersPaginatorBase = Paginator[
        DescribeStorageVirtualMachinePeersResponseTypeDef
    ]
else:
    _DescribeStorageVirtualMachinePeersPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeStorageVirtualMachinePeersPaginator(_DescribeStorageVirtualMachinePeersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachinePeers.html#FSx.Paginator.DescribeStorageVirtualMachinePeers)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describestoragevirtualmachinepeerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStorageVirtualMachinePeersRequestPaginateTypeDef]
    ) -> PageIterator[DescribeStorageVirtualMachinePeersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachinePeers.html#FSx.Paginator.DescribeStorageVirtualMachinePeers.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describestoragevirtualmachinepeerspaginator)
        """


if TYPE_CHECKING:
    _DescribeStorageVirtualMachinesPaginatorBase = Paginator[
        DescribeStorageVirtualMachinesResponseTypeDef
    ]
else:
    _DescribeStorageVirtualMachinesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeStorageVirtualMachinesPaginator(_DescribeStorageVirtualMachinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachines.html#FSx.Paginator.DescribeStorageVirtualMachines)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describestoragevirtualmachinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStorageVirtualMachinesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeStorageVirtualMachinesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeStorageVirtualMachines.html#FSx.Paginator.DescribeStorageVirtualMachines.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describestoragevirtualmachinespaginator)
        """


if TYPE_CHECKING:
    _DescribeVolumesPaginatorBase = Paginator[DescribeVolumesResponsePaginatorTypeDef]
else:
    _DescribeVolumesPaginatorBase = Paginator  # type: ignore[assignment]


class DescribeVolumesPaginator(_DescribeVolumesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeVolumes.html#FSx.Paginator.DescribeVolumes)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describevolumespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVolumesRequestPaginateTypeDef]
    ) -> PageIterator[DescribeVolumesResponsePaginatorTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/DescribeVolumes.html#FSx.Paginator.DescribeVolumes.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#describevolumespaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = Paginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = Paginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/ListTagsForResource.html#FSx.Paginator.ListTagsForResource)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> PageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/fsx/paginator/ListTagsForResource.html#FSx.Paginator.ListTagsForResource.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fsx/paginators/#listtagsforresourcepaginator)
        """
