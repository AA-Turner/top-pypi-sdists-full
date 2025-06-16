"""
Type annotations for medialive service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_medialive.client import MediaLiveClient
    from types_aiobotocore_medialive.paginator import (
        DescribeSchedulePaginator,
        ListChannelPlacementGroupsPaginator,
        ListChannelsPaginator,
        ListCloudWatchAlarmTemplateGroupsPaginator,
        ListCloudWatchAlarmTemplatesPaginator,
        ListClustersPaginator,
        ListEventBridgeRuleTemplateGroupsPaginator,
        ListEventBridgeRuleTemplatesPaginator,
        ListInputDeviceTransfersPaginator,
        ListInputDevicesPaginator,
        ListInputSecurityGroupsPaginator,
        ListInputsPaginator,
        ListMultiplexProgramsPaginator,
        ListMultiplexesPaginator,
        ListNetworksPaginator,
        ListNodesPaginator,
        ListOfferingsPaginator,
        ListReservationsPaginator,
        ListSdiSourcesPaginator,
        ListSignalMapsPaginator,
    )

    session = get_session()
    with session.create_client("medialive") as client:
        client: MediaLiveClient

        describe_schedule_paginator: DescribeSchedulePaginator = client.get_paginator("describe_schedule")
        list_channel_placement_groups_paginator: ListChannelPlacementGroupsPaginator = client.get_paginator("list_channel_placement_groups")
        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_cloud_watch_alarm_template_groups_paginator: ListCloudWatchAlarmTemplateGroupsPaginator = client.get_paginator("list_cloud_watch_alarm_template_groups")
        list_cloud_watch_alarm_templates_paginator: ListCloudWatchAlarmTemplatesPaginator = client.get_paginator("list_cloud_watch_alarm_templates")
        list_clusters_paginator: ListClustersPaginator = client.get_paginator("list_clusters")
        list_event_bridge_rule_template_groups_paginator: ListEventBridgeRuleTemplateGroupsPaginator = client.get_paginator("list_event_bridge_rule_template_groups")
        list_event_bridge_rule_templates_paginator: ListEventBridgeRuleTemplatesPaginator = client.get_paginator("list_event_bridge_rule_templates")
        list_input_device_transfers_paginator: ListInputDeviceTransfersPaginator = client.get_paginator("list_input_device_transfers")
        list_input_devices_paginator: ListInputDevicesPaginator = client.get_paginator("list_input_devices")
        list_input_security_groups_paginator: ListInputSecurityGroupsPaginator = client.get_paginator("list_input_security_groups")
        list_inputs_paginator: ListInputsPaginator = client.get_paginator("list_inputs")
        list_multiplex_programs_paginator: ListMultiplexProgramsPaginator = client.get_paginator("list_multiplex_programs")
        list_multiplexes_paginator: ListMultiplexesPaginator = client.get_paginator("list_multiplexes")
        list_networks_paginator: ListNetworksPaginator = client.get_paginator("list_networks")
        list_nodes_paginator: ListNodesPaginator = client.get_paginator("list_nodes")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_reservations_paginator: ListReservationsPaginator = client.get_paginator("list_reservations")
        list_sdi_sources_paginator: ListSdiSourcesPaginator = client.get_paginator("list_sdi_sources")
        list_signal_maps_paginator: ListSignalMapsPaginator = client.get_paginator("list_signal_maps")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeScheduleRequestPaginateTypeDef,
    DescribeScheduleResponseTypeDef,
    ListChannelPlacementGroupsRequestPaginateTypeDef,
    ListChannelPlacementGroupsResponseTypeDef,
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListCloudWatchAlarmTemplateGroupsRequestPaginateTypeDef,
    ListCloudWatchAlarmTemplateGroupsResponseTypeDef,
    ListCloudWatchAlarmTemplatesRequestPaginateTypeDef,
    ListCloudWatchAlarmTemplatesResponseTypeDef,
    ListClustersRequestPaginateTypeDef,
    ListClustersResponseTypeDef,
    ListEventBridgeRuleTemplateGroupsRequestPaginateTypeDef,
    ListEventBridgeRuleTemplateGroupsResponseTypeDef,
    ListEventBridgeRuleTemplatesRequestPaginateTypeDef,
    ListEventBridgeRuleTemplatesResponseTypeDef,
    ListInputDevicesRequestPaginateTypeDef,
    ListInputDevicesResponseTypeDef,
    ListInputDeviceTransfersRequestPaginateTypeDef,
    ListInputDeviceTransfersResponseTypeDef,
    ListInputSecurityGroupsRequestPaginateTypeDef,
    ListInputSecurityGroupsResponseTypeDef,
    ListInputsRequestPaginateTypeDef,
    ListInputsResponseTypeDef,
    ListMultiplexesRequestPaginateTypeDef,
    ListMultiplexesResponseTypeDef,
    ListMultiplexProgramsRequestPaginateTypeDef,
    ListMultiplexProgramsResponseTypeDef,
    ListNetworksRequestPaginateTypeDef,
    ListNetworksResponseTypeDef,
    ListNodesRequestPaginateTypeDef,
    ListNodesResponseTypeDef,
    ListOfferingsRequestPaginateTypeDef,
    ListOfferingsResponseTypeDef,
    ListReservationsRequestPaginateTypeDef,
    ListReservationsResponseTypeDef,
    ListSdiSourcesRequestPaginateTypeDef,
    ListSdiSourcesResponseTypeDef,
    ListSignalMapsRequestPaginateTypeDef,
    ListSignalMapsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeSchedulePaginator",
    "ListChannelPlacementGroupsPaginator",
    "ListChannelsPaginator",
    "ListCloudWatchAlarmTemplateGroupsPaginator",
    "ListCloudWatchAlarmTemplatesPaginator",
    "ListClustersPaginator",
    "ListEventBridgeRuleTemplateGroupsPaginator",
    "ListEventBridgeRuleTemplatesPaginator",
    "ListInputDeviceTransfersPaginator",
    "ListInputDevicesPaginator",
    "ListInputSecurityGroupsPaginator",
    "ListInputsPaginator",
    "ListMultiplexProgramsPaginator",
    "ListMultiplexesPaginator",
    "ListNetworksPaginator",
    "ListNodesPaginator",
    "ListOfferingsPaginator",
    "ListReservationsPaginator",
    "ListSdiSourcesPaginator",
    "ListSignalMapsPaginator",
)


if TYPE_CHECKING:
    _DescribeSchedulePaginatorBase = AioPaginator[DescribeScheduleResponseTypeDef]
else:
    _DescribeSchedulePaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSchedulePaginator(_DescribeSchedulePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/DescribeSchedule.html#MediaLive.Paginator.DescribeSchedule)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#describeschedulepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeScheduleRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeScheduleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/DescribeSchedule.html#MediaLive.Paginator.DescribeSchedule.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#describeschedulepaginator)
        """


if TYPE_CHECKING:
    _ListChannelPlacementGroupsPaginatorBase = AioPaginator[
        ListChannelPlacementGroupsResponseTypeDef
    ]
else:
    _ListChannelPlacementGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelPlacementGroupsPaginator(_ListChannelPlacementGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListChannelPlacementGroups.html#MediaLive.Paginator.ListChannelPlacementGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listchannelplacementgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelPlacementGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelPlacementGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListChannelPlacementGroups.html#MediaLive.Paginator.ListChannelPlacementGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listchannelplacementgroupspaginator)
        """


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListChannels.html#MediaLive.Paginator.ListChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListChannels.html#MediaLive.Paginator.ListChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListCloudWatchAlarmTemplateGroupsPaginatorBase = AioPaginator[
        ListCloudWatchAlarmTemplateGroupsResponseTypeDef
    ]
else:
    _ListCloudWatchAlarmTemplateGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCloudWatchAlarmTemplateGroupsPaginator(_ListCloudWatchAlarmTemplateGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListCloudWatchAlarmTemplateGroups.html#MediaLive.Paginator.ListCloudWatchAlarmTemplateGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplategroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudWatchAlarmTemplateGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCloudWatchAlarmTemplateGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListCloudWatchAlarmTemplateGroups.html#MediaLive.Paginator.ListCloudWatchAlarmTemplateGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplategroupspaginator)
        """


if TYPE_CHECKING:
    _ListCloudWatchAlarmTemplatesPaginatorBase = AioPaginator[
        ListCloudWatchAlarmTemplatesResponseTypeDef
    ]
else:
    _ListCloudWatchAlarmTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCloudWatchAlarmTemplatesPaginator(_ListCloudWatchAlarmTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListCloudWatchAlarmTemplates.html#MediaLive.Paginator.ListCloudWatchAlarmTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCloudWatchAlarmTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCloudWatchAlarmTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListCloudWatchAlarmTemplates.html#MediaLive.Paginator.ListCloudWatchAlarmTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listcloudwatchalarmtemplatespaginator)
        """


if TYPE_CHECKING:
    _ListClustersPaginatorBase = AioPaginator[ListClustersResponseTypeDef]
else:
    _ListClustersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListClustersPaginator(_ListClustersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListClusters.html#MediaLive.Paginator.ListClusters)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listclusterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListClustersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListClustersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListClusters.html#MediaLive.Paginator.ListClusters.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listclusterspaginator)
        """


if TYPE_CHECKING:
    _ListEventBridgeRuleTemplateGroupsPaginatorBase = AioPaginator[
        ListEventBridgeRuleTemplateGroupsResponseTypeDef
    ]
else:
    _ListEventBridgeRuleTemplateGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventBridgeRuleTemplateGroupsPaginator(_ListEventBridgeRuleTemplateGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListEventBridgeRuleTemplateGroups.html#MediaLive.Paginator.ListEventBridgeRuleTemplateGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplategroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventBridgeRuleTemplateGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventBridgeRuleTemplateGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListEventBridgeRuleTemplateGroups.html#MediaLive.Paginator.ListEventBridgeRuleTemplateGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplategroupspaginator)
        """


if TYPE_CHECKING:
    _ListEventBridgeRuleTemplatesPaginatorBase = AioPaginator[
        ListEventBridgeRuleTemplatesResponseTypeDef
    ]
else:
    _ListEventBridgeRuleTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventBridgeRuleTemplatesPaginator(_ListEventBridgeRuleTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListEventBridgeRuleTemplates.html#MediaLive.Paginator.ListEventBridgeRuleTemplates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventBridgeRuleTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventBridgeRuleTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListEventBridgeRuleTemplates.html#MediaLive.Paginator.ListEventBridgeRuleTemplates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listeventbridgeruletemplatespaginator)
        """


if TYPE_CHECKING:
    _ListInputDeviceTransfersPaginatorBase = AioPaginator[ListInputDeviceTransfersResponseTypeDef]
else:
    _ListInputDeviceTransfersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInputDeviceTransfersPaginator(_ListInputDeviceTransfersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputDeviceTransfers.html#MediaLive.Paginator.ListInputDeviceTransfers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicetransferspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInputDeviceTransfersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInputDeviceTransfersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputDeviceTransfers.html#MediaLive.Paginator.ListInputDeviceTransfers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicetransferspaginator)
        """


if TYPE_CHECKING:
    _ListInputDevicesPaginatorBase = AioPaginator[ListInputDevicesResponseTypeDef]
else:
    _ListInputDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInputDevicesPaginator(_ListInputDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputDevices.html#MediaLive.Paginator.ListInputDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInputDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInputDevicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputDevices.html#MediaLive.Paginator.ListInputDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputdevicespaginator)
        """


if TYPE_CHECKING:
    _ListInputSecurityGroupsPaginatorBase = AioPaginator[ListInputSecurityGroupsResponseTypeDef]
else:
    _ListInputSecurityGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInputSecurityGroupsPaginator(_ListInputSecurityGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputSecurityGroups.html#MediaLive.Paginator.ListInputSecurityGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputsecuritygroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInputSecurityGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInputSecurityGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputSecurityGroups.html#MediaLive.Paginator.ListInputSecurityGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputsecuritygroupspaginator)
        """


if TYPE_CHECKING:
    _ListInputsPaginatorBase = AioPaginator[ListInputsResponseTypeDef]
else:
    _ListInputsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInputsPaginator(_ListInputsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputs.html#MediaLive.Paginator.ListInputs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInputsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInputsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListInputs.html#MediaLive.Paginator.ListInputs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listinputspaginator)
        """


if TYPE_CHECKING:
    _ListMultiplexProgramsPaginatorBase = AioPaginator[ListMultiplexProgramsResponseTypeDef]
else:
    _ListMultiplexProgramsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMultiplexProgramsPaginator(_ListMultiplexProgramsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListMultiplexPrograms.html#MediaLive.Paginator.ListMultiplexPrograms)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexprogramspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMultiplexProgramsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMultiplexProgramsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListMultiplexPrograms.html#MediaLive.Paginator.ListMultiplexPrograms.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexprogramspaginator)
        """


if TYPE_CHECKING:
    _ListMultiplexesPaginatorBase = AioPaginator[ListMultiplexesResponseTypeDef]
else:
    _ListMultiplexesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMultiplexesPaginator(_ListMultiplexesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListMultiplexes.html#MediaLive.Paginator.ListMultiplexes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMultiplexesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMultiplexesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListMultiplexes.html#MediaLive.Paginator.ListMultiplexes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listmultiplexespaginator)
        """


if TYPE_CHECKING:
    _ListNetworksPaginatorBase = AioPaginator[ListNetworksResponseTypeDef]
else:
    _ListNetworksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNetworksPaginator(_ListNetworksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListNetworks.html#MediaLive.Paginator.ListNetworks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listnetworkspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListNetworks.html#MediaLive.Paginator.ListNetworks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listnetworkspaginator)
        """


if TYPE_CHECKING:
    _ListNodesPaginatorBase = AioPaginator[ListNodesResponseTypeDef]
else:
    _ListNodesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNodesPaginator(_ListNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListNodes.html#MediaLive.Paginator.ListNodes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listnodespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNodesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNodesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListNodes.html#MediaLive.Paginator.ListNodes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listnodespaginator)
        """


if TYPE_CHECKING:
    _ListOfferingsPaginatorBase = AioPaginator[ListOfferingsResponseTypeDef]
else:
    _ListOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOfferingsPaginator(_ListOfferingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListOfferings.html#MediaLive.Paginator.ListOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listofferingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOfferingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOfferingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListOfferings.html#MediaLive.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listofferingspaginator)
        """


if TYPE_CHECKING:
    _ListReservationsPaginatorBase = AioPaginator[ListReservationsResponseTypeDef]
else:
    _ListReservationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListReservationsPaginator(_ListReservationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListReservations.html#MediaLive.Paginator.ListReservations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listreservationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReservationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListReservationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListReservations.html#MediaLive.Paginator.ListReservations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listreservationspaginator)
        """


if TYPE_CHECKING:
    _ListSdiSourcesPaginatorBase = AioPaginator[ListSdiSourcesResponseTypeDef]
else:
    _ListSdiSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSdiSourcesPaginator(_ListSdiSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListSdiSources.html#MediaLive.Paginator.ListSdiSources)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listsdisourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSdiSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSdiSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListSdiSources.html#MediaLive.Paginator.ListSdiSources.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listsdisourcespaginator)
        """


if TYPE_CHECKING:
    _ListSignalMapsPaginatorBase = AioPaginator[ListSignalMapsResponseTypeDef]
else:
    _ListSignalMapsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSignalMapsPaginator(_ListSignalMapsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListSignalMaps.html#MediaLive.Paginator.ListSignalMaps)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listsignalmapspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSignalMapsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSignalMapsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/medialive/paginator/ListSignalMaps.html#MediaLive.Paginator.ListSignalMaps.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_medialive/paginators/#listsignalmapspaginator)
        """
