"""
Type annotations for mediatailor service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_mediatailor.client import MediaTailorClient
    from types_aiobotocore_mediatailor.paginator import (
        GetChannelSchedulePaginator,
        ListAlertsPaginator,
        ListChannelsPaginator,
        ListLiveSourcesPaginator,
        ListPlaybackConfigurationsPaginator,
        ListPrefetchSchedulesPaginator,
        ListSourceLocationsPaginator,
        ListVodSourcesPaginator,
    )

    session = get_session()
    with session.create_client("mediatailor") as client:
        client: MediaTailorClient

        get_channel_schedule_paginator: GetChannelSchedulePaginator = client.get_paginator("get_channel_schedule")
        list_alerts_paginator: ListAlertsPaginator = client.get_paginator("list_alerts")
        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_live_sources_paginator: ListLiveSourcesPaginator = client.get_paginator("list_live_sources")
        list_playback_configurations_paginator: ListPlaybackConfigurationsPaginator = client.get_paginator("list_playback_configurations")
        list_prefetch_schedules_paginator: ListPrefetchSchedulesPaginator = client.get_paginator("list_prefetch_schedules")
        list_source_locations_paginator: ListSourceLocationsPaginator = client.get_paginator("list_source_locations")
        list_vod_sources_paginator: ListVodSourcesPaginator = client.get_paginator("list_vod_sources")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetChannelScheduleRequestPaginateTypeDef,
    GetChannelScheduleResponseTypeDef,
    ListAlertsRequestPaginateTypeDef,
    ListAlertsResponseTypeDef,
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListLiveSourcesRequestPaginateTypeDef,
    ListLiveSourcesResponseTypeDef,
    ListPlaybackConfigurationsRequestPaginateTypeDef,
    ListPlaybackConfigurationsResponseTypeDef,
    ListPrefetchSchedulesRequestPaginateTypeDef,
    ListPrefetchSchedulesResponseTypeDef,
    ListSourceLocationsRequestPaginateTypeDef,
    ListSourceLocationsResponseTypeDef,
    ListVodSourcesRequestPaginateTypeDef,
    ListVodSourcesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetChannelSchedulePaginator",
    "ListAlertsPaginator",
    "ListChannelsPaginator",
    "ListLiveSourcesPaginator",
    "ListPlaybackConfigurationsPaginator",
    "ListPrefetchSchedulesPaginator",
    "ListSourceLocationsPaginator",
    "ListVodSourcesPaginator",
)


if TYPE_CHECKING:
    _GetChannelSchedulePaginatorBase = AioPaginator[GetChannelScheduleResponseTypeDef]
else:
    _GetChannelSchedulePaginatorBase = AioPaginator  # type: ignore[assignment]


class GetChannelSchedulePaginator(_GetChannelSchedulePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/GetChannelSchedule.html#MediaTailor.Paginator.GetChannelSchedule)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#getchannelschedulepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetChannelScheduleRequestPaginateTypeDef]
    ) -> AioPageIterator[GetChannelScheduleResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/GetChannelSchedule.html#MediaTailor.Paginator.GetChannelSchedule.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#getchannelschedulepaginator)
        """


if TYPE_CHECKING:
    _ListAlertsPaginatorBase = AioPaginator[ListAlertsResponseTypeDef]
else:
    _ListAlertsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAlertsPaginator(_ListAlertsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListAlerts.html#MediaTailor.Paginator.ListAlerts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listalertspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAlertsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAlertsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListAlerts.html#MediaTailor.Paginator.ListAlerts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listalertspaginator)
        """


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListChannels.html#MediaTailor.Paginator.ListChannels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListChannels.html#MediaTailor.Paginator.ListChannels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListLiveSourcesPaginatorBase = AioPaginator[ListLiveSourcesResponseTypeDef]
else:
    _ListLiveSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLiveSourcesPaginator(_ListLiveSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListLiveSources.html#MediaTailor.Paginator.ListLiveSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listlivesourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLiveSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLiveSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListLiveSources.html#MediaTailor.Paginator.ListLiveSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listlivesourcespaginator)
        """


if TYPE_CHECKING:
    _ListPlaybackConfigurationsPaginatorBase = AioPaginator[
        ListPlaybackConfigurationsResponseTypeDef
    ]
else:
    _ListPlaybackConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPlaybackConfigurationsPaginator(_ListPlaybackConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPlaybackConfigurations.html#MediaTailor.Paginator.ListPlaybackConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listplaybackconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlaybackConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlaybackConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPlaybackConfigurations.html#MediaTailor.Paginator.ListPlaybackConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listplaybackconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListPrefetchSchedulesPaginatorBase = AioPaginator[ListPrefetchSchedulesResponseTypeDef]
else:
    _ListPrefetchSchedulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrefetchSchedulesPaginator(_ListPrefetchSchedulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPrefetchSchedules.html#MediaTailor.Paginator.ListPrefetchSchedules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listprefetchschedulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrefetchSchedulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPrefetchSchedulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListPrefetchSchedules.html#MediaTailor.Paginator.ListPrefetchSchedules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listprefetchschedulespaginator)
        """


if TYPE_CHECKING:
    _ListSourceLocationsPaginatorBase = AioPaginator[ListSourceLocationsResponseTypeDef]
else:
    _ListSourceLocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSourceLocationsPaginator(_ListSourceLocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListSourceLocations.html#MediaTailor.Paginator.ListSourceLocations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listsourcelocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSourceLocationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSourceLocationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListSourceLocations.html#MediaTailor.Paginator.ListSourceLocations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listsourcelocationspaginator)
        """


if TYPE_CHECKING:
    _ListVodSourcesPaginatorBase = AioPaginator[ListVodSourcesResponseTypeDef]
else:
    _ListVodSourcesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVodSourcesPaginator(_ListVodSourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListVodSources.html#MediaTailor.Paginator.ListVodSources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listvodsourcespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVodSourcesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVodSourcesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediatailor/paginator/ListVodSources.html#MediaTailor.Paginator.ListVodSources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediatailor/paginators/#listvodsourcespaginator)
        """
