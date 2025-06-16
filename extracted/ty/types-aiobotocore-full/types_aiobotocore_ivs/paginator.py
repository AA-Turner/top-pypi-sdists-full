"""
Type annotations for ivs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ivs.client import IVSClient
    from types_aiobotocore_ivs.paginator import (
        ListChannelsPaginator,
        ListPlaybackKeyPairsPaginator,
        ListRecordingConfigurationsPaginator,
        ListStreamKeysPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    with session.create_client("ivs") as client:
        client: IVSClient

        list_channels_paginator: ListChannelsPaginator = client.get_paginator("list_channels")
        list_playback_key_pairs_paginator: ListPlaybackKeyPairsPaginator = client.get_paginator("list_playback_key_pairs")
        list_recording_configurations_paginator: ListRecordingConfigurationsPaginator = client.get_paginator("list_recording_configurations")
        list_stream_keys_paginator: ListStreamKeysPaginator = client.get_paginator("list_stream_keys")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChannelsRequestPaginateTypeDef,
    ListChannelsResponseTypeDef,
    ListPlaybackKeyPairsRequestPaginateTypeDef,
    ListPlaybackKeyPairsResponseTypeDef,
    ListRecordingConfigurationsRequestPaginateTypeDef,
    ListRecordingConfigurationsResponseTypeDef,
    ListStreamKeysRequestPaginateTypeDef,
    ListStreamKeysResponseTypeDef,
    ListStreamsRequestPaginateTypeDef,
    ListStreamsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListChannelsPaginator",
    "ListPlaybackKeyPairsPaginator",
    "ListRecordingConfigurationsPaginator",
    "ListStreamKeysPaginator",
    "ListStreamsPaginator",
)


if TYPE_CHECKING:
    _ListChannelsPaginatorBase = AioPaginator[ListChannelsResponseTypeDef]
else:
    _ListChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListChannelsPaginator(_ListChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListChannels.html#IVS.Paginator.ListChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#listchannelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChannelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChannelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListChannels.html#IVS.Paginator.ListChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#listchannelspaginator)
        """


if TYPE_CHECKING:
    _ListPlaybackKeyPairsPaginatorBase = AioPaginator[ListPlaybackKeyPairsResponseTypeDef]
else:
    _ListPlaybackKeyPairsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPlaybackKeyPairsPaginator(_ListPlaybackKeyPairsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListPlaybackKeyPairs.html#IVS.Paginator.ListPlaybackKeyPairs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#listplaybackkeypairspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPlaybackKeyPairsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPlaybackKeyPairsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListPlaybackKeyPairs.html#IVS.Paginator.ListPlaybackKeyPairs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#listplaybackkeypairspaginator)
        """


if TYPE_CHECKING:
    _ListRecordingConfigurationsPaginatorBase = AioPaginator[
        ListRecordingConfigurationsResponseTypeDef
    ]
else:
    _ListRecordingConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRecordingConfigurationsPaginator(_ListRecordingConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListRecordingConfigurations.html#IVS.Paginator.ListRecordingConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#listrecordingconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRecordingConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRecordingConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListRecordingConfigurations.html#IVS.Paginator.ListRecordingConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#listrecordingconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListStreamKeysPaginatorBase = AioPaginator[ListStreamKeysResponseTypeDef]
else:
    _ListStreamKeysPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStreamKeysPaginator(_ListStreamKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreamKeys.html#IVS.Paginator.ListStreamKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#liststreamkeyspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStreamKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreamKeys.html#IVS.Paginator.ListStreamKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#liststreamkeyspaginator)
        """


if TYPE_CHECKING:
    _ListStreamsPaginatorBase = AioPaginator[ListStreamsResponseTypeDef]
else:
    _ListStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStreamsPaginator(_ListStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreams.html#IVS.Paginator.ListStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#liststreamspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs/paginator/ListStreams.html#IVS.Paginator.ListStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs/paginators/#liststreamspaginator)
        """
