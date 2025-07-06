"""
Type annotations for redshift-serverless service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_redshift_serverless.client import RedshiftServerlessClient
    from types_aiobotocore_redshift_serverless.paginator import (
        ListCustomDomainAssociationsPaginator,
        ListEndpointAccessPaginator,
        ListManagedWorkgroupsPaginator,
        ListNamespacesPaginator,
        ListRecoveryPointsPaginator,
        ListReservationOfferingsPaginator,
        ListReservationsPaginator,
        ListScheduledActionsPaginator,
        ListSnapshotCopyConfigurationsPaginator,
        ListSnapshotsPaginator,
        ListTableRestoreStatusPaginator,
        ListTracksPaginator,
        ListUsageLimitsPaginator,
        ListWorkgroupsPaginator,
    )

    session = get_session()
    with session.create_client("redshift-serverless") as client:
        client: RedshiftServerlessClient

        list_custom_domain_associations_paginator: ListCustomDomainAssociationsPaginator = client.get_paginator("list_custom_domain_associations")
        list_endpoint_access_paginator: ListEndpointAccessPaginator = client.get_paginator("list_endpoint_access")
        list_managed_workgroups_paginator: ListManagedWorkgroupsPaginator = client.get_paginator("list_managed_workgroups")
        list_namespaces_paginator: ListNamespacesPaginator = client.get_paginator("list_namespaces")
        list_recovery_points_paginator: ListRecoveryPointsPaginator = client.get_paginator("list_recovery_points")
        list_reservation_offerings_paginator: ListReservationOfferingsPaginator = client.get_paginator("list_reservation_offerings")
        list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
        list_scheduled_actions_paginator: ListScheduledActionsPaginator = client.get_paginator("list_scheduled_actions")
        list_snapshot_copy_configurations_paginator: ListSnapshotCopyConfigurationsPaginator = client.get_paginator("list_snapshot_copy_configurations")
        list_snapshots_paginator: ListSnapshotsPaginator = client.get_paginator("list_snapshots")
        list_table_restore_status_paginator: ListTableRestoreStatusPaginator = client.get_paginator("list_table_restore_status")
        list_tracks_paginator: ListTracksPaginator = client.get_paginator("list_tracks")
        list_usage_limits_paginator: ListUsageLimitsPaginator = client.get_paginator("list_usage_limits")
        list_workgroups_paginator: ListWorkgroupsPaginator = client.get_paginator("list_workgroups")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCustomDomainAssociationsRequestPaginateTypeDef,
    ListCustomDomainAssociationsResponseTypeDef,
    ListEndpointAccessRequestPaginateTypeDef,
    ListEndpointAccessResponseTypeDef,
    ListManagedWorkgroupsRequestPaginateTypeDef,
    ListManagedWorkgroupsResponseTypeDef,
    ListNamespacesRequestPaginateTypeDef,
    ListNamespacesResponseTypeDef,
    ListRecoveryPointsRequestPaginateTypeDef,
    ListRecoveryPointsResponseTypeDef,
    ListReservationOfferingsRequestPaginateTypeDef,
    ListReservationOfferingsResponseTypeDef,
    ListReservationsRequestPaginateTypeDef,
    ListReservationsResponseTypeDef,
    ListScheduledActionsRequestPaginateTypeDef,
    ListScheduledActionsResponseTypeDef,
    ListSnapshotCopyConfigurationsRequestPaginateTypeDef,
    ListSnapshotCopyConfigurationsResponseTypeDef,
    ListSnapshotsRequestPaginateTypeDef,
    ListSnapshotsResponseTypeDef,
    ListTableRestoreStatusRequestPaginateTypeDef,
    ListTableRestoreStatusResponseTypeDef,
    ListTracksRequestPaginateTypeDef,
    ListTracksResponseTypeDef,
    ListUsageLimitsRequestPaginateTypeDef,
    ListUsageLimitsResponseTypeDef,
    ListWorkgroupsRequestPaginateTypeDef,
    ListWorkgroupsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListCustomDomainAssociationsPaginator",
    "ListEndpointAccessPaginator",
    "ListManagedWorkgroupsPaginator",
    "ListNamespacesPaginator",
    "ListRecoveryPointsPaginator",
    "ListReservationOfferingsPaginator",
    "ListReservationsPaginator",
    "ListScheduledActionsPaginator",
    "ListSnapshotCopyConfigurationsPaginator",
    "ListSnapshotsPaginator",
    "ListTableRestoreStatusPaginator",
    "ListTracksPaginator",
    "ListUsageLimitsPaginator",
    "ListWorkgroupsPaginator",
)


if TYPE_CHECKING:
    _ListCustomDomainAssociationsPaginatorBase = AioPaginator[
        ListCustomDomainAssociationsResponseTypeDef
    ]
else:
    _ListCustomDomainAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomDomainAssociationsPaginator(_ListCustomDomainAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListCustomDomainAssociations.html#RedshiftServerless.Paginator.ListCustomDomainAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listcustomdomainassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomDomainAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomDomainAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListCustomDomainAssociations.html#RedshiftServerless.Paginator.ListCustomDomainAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listcustomdomainassociationspaginator)
        """


if TYPE_CHECKING:
    _ListEndpointAccessPaginatorBase = AioPaginator[ListEndpointAccessResponseTypeDef]
else:
    _ListEndpointAccessPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEndpointAccessPaginator(_ListEndpointAccessPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListEndpointAccess.html#RedshiftServerless.Paginator.ListEndpointAccess)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listendpointaccesspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEndpointAccessRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEndpointAccessResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListEndpointAccess.html#RedshiftServerless.Paginator.ListEndpointAccess.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listendpointaccesspaginator)
        """


if TYPE_CHECKING:
    _ListManagedWorkgroupsPaginatorBase = AioPaginator[ListManagedWorkgroupsResponseTypeDef]
else:
    _ListManagedWorkgroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedWorkgroupsPaginator(_ListManagedWorkgroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListManagedWorkgroups.html#RedshiftServerless.Paginator.ListManagedWorkgroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listmanagedworkgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedWorkgroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedWorkgroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListManagedWorkgroups.html#RedshiftServerless.Paginator.ListManagedWorkgroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listmanagedworkgroupspaginator)
        """


if TYPE_CHECKING:
    _ListNamespacesPaginatorBase = AioPaginator[ListNamespacesResponseTypeDef]
else:
    _ListNamespacesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNamespacesPaginator(_ListNamespacesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListNamespaces.html#RedshiftServerless.Paginator.ListNamespaces)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listnamespacespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNamespacesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNamespacesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListNamespaces.html#RedshiftServerless.Paginator.ListNamespaces.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listnamespacespaginator)
        """


if TYPE_CHECKING:
    _ListRecoveryPointsPaginatorBase = AioPaginator[ListRecoveryPointsResponseTypeDef]
else:
    _ListRecoveryPointsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecoveryPointsPaginator(_ListRecoveryPointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListRecoveryPoints.html#RedshiftServerless.Paginator.ListRecoveryPoints)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listrecoverypointspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecoveryPointsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecoveryPointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListRecoveryPoints.html#RedshiftServerless.Paginator.ListRecoveryPoints.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listrecoverypointspaginator)
        """


if TYPE_CHECKING:
    _ListReservationOfferingsPaginatorBase = AioPaginator[ListReservationOfferingsResponseTypeDef]
else:
    _ListReservationOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListReservationOfferingsPaginator(_ListReservationOfferingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListReservationOfferings.html#RedshiftServerless.Paginator.ListReservationOfferings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listreservationofferingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReservationOfferingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReservationOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListReservationOfferings.html#RedshiftServerless.Paginator.ListReservationOfferings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listreservationofferingspaginator)
        """


if TYPE_CHECKING:
    _ListReservationsPaginatorBase = AioPaginator[ListReservationsResponseTypeDef]
else:
    _ListReservationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListReservationsPaginator(_ListReservationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListReservations.html#RedshiftServerless.Paginator.ListReservations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listreservationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReservationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReservationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListReservations.html#RedshiftServerless.Paginator.ListReservations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listreservationspaginator)
        """


if TYPE_CHECKING:
    _ListScheduledActionsPaginatorBase = AioPaginator[ListScheduledActionsResponseTypeDef]
else:
    _ListScheduledActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScheduledActionsPaginator(_ListScheduledActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListScheduledActions.html#RedshiftServerless.Paginator.ListScheduledActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listscheduledactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduledActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListScheduledActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListScheduledActions.html#RedshiftServerless.Paginator.ListScheduledActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listscheduledactionspaginator)
        """


if TYPE_CHECKING:
    _ListSnapshotCopyConfigurationsPaginatorBase = AioPaginator[
        ListSnapshotCopyConfigurationsResponseTypeDef
    ]
else:
    _ListSnapshotCopyConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSnapshotCopyConfigurationsPaginator(_ListSnapshotCopyConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshotCopyConfigurations.html#RedshiftServerless.Paginator.ListSnapshotCopyConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listsnapshotcopyconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSnapshotCopyConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSnapshotCopyConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshotCopyConfigurations.html#RedshiftServerless.Paginator.ListSnapshotCopyConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listsnapshotcopyconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListSnapshotsPaginatorBase = AioPaginator[ListSnapshotsResponseTypeDef]
else:
    _ListSnapshotsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSnapshotsPaginator(_ListSnapshotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshots.html#RedshiftServerless.Paginator.ListSnapshots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listsnapshotspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSnapshotsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSnapshotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListSnapshots.html#RedshiftServerless.Paginator.ListSnapshots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listsnapshotspaginator)
        """


if TYPE_CHECKING:
    _ListTableRestoreStatusPaginatorBase = AioPaginator[ListTableRestoreStatusResponseTypeDef]
else:
    _ListTableRestoreStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTableRestoreStatusPaginator(_ListTableRestoreStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListTableRestoreStatus.html#RedshiftServerless.Paginator.ListTableRestoreStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listtablerestorestatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTableRestoreStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTableRestoreStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListTableRestoreStatus.html#RedshiftServerless.Paginator.ListTableRestoreStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listtablerestorestatuspaginator)
        """


if TYPE_CHECKING:
    _ListTracksPaginatorBase = AioPaginator[ListTracksResponseTypeDef]
else:
    _ListTracksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTracksPaginator(_ListTracksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListTracks.html#RedshiftServerless.Paginator.ListTracks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listtrackspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTracksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTracksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListTracks.html#RedshiftServerless.Paginator.ListTracks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listtrackspaginator)
        """


if TYPE_CHECKING:
    _ListUsageLimitsPaginatorBase = AioPaginator[ListUsageLimitsResponseTypeDef]
else:
    _ListUsageLimitsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUsageLimitsPaginator(_ListUsageLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListUsageLimits.html#RedshiftServerless.Paginator.ListUsageLimits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listusagelimitspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsageLimitsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsageLimitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListUsageLimits.html#RedshiftServerless.Paginator.ListUsageLimits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listusagelimitspaginator)
        """


if TYPE_CHECKING:
    _ListWorkgroupsPaginatorBase = AioPaginator[ListWorkgroupsResponseTypeDef]
else:
    _ListWorkgroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkgroupsPaginator(_ListWorkgroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListWorkgroups.html#RedshiftServerless.Paginator.ListWorkgroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listworkgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkgroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkgroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift-serverless/paginator/ListWorkgroups.html#RedshiftServerless.Paginator.ListWorkgroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_redshift_serverless/paginators/#listworkgroupspaginator)
        """
