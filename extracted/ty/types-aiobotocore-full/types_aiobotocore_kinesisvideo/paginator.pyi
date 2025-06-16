"""
Type annotations for kinesisvideo service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_kinesisvideo.client import KinesisVideoClient
    from types_aiobotocore_kinesisvideo.paginator import (
        DescribeMappedResourceConfigurationPaginator,
        ListEdgeAgentConfigurationsPaginator,
        ListSignalingChannelsPaginator,
        ListStreamsPaginator,
    )

    session = get_session()
    with session.create_client("kinesisvideo") as client:
        client: KinesisVideoClient

        describe_mapped_resource_configuration_paginator: DescribeMappedResourceConfigurationPaginator = client.get_paginator("describe_mapped_resource_configuration")
        list_edge_agent_configurations_paginator: ListEdgeAgentConfigurationsPaginator = client.get_paginator("list_edge_agent_configurations")
        list_signaling_channels_paginator: ListSignalingChannelsPaginator = client.get_paginator("list_signaling_channels")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeMappedResourceConfigurationInputPaginateTypeDef,
    DescribeMappedResourceConfigurationOutputTypeDef,
    ListEdgeAgentConfigurationsInputPaginateTypeDef,
    ListEdgeAgentConfigurationsOutputTypeDef,
    ListSignalingChannelsInputPaginateTypeDef,
    ListSignalingChannelsOutputTypeDef,
    ListStreamsInputPaginateTypeDef,
    ListStreamsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeMappedResourceConfigurationPaginator",
    "ListEdgeAgentConfigurationsPaginator",
    "ListSignalingChannelsPaginator",
    "ListStreamsPaginator",
)

if TYPE_CHECKING:
    _DescribeMappedResourceConfigurationPaginatorBase = AioPaginator[
        DescribeMappedResourceConfigurationOutputTypeDef
    ]
else:
    _DescribeMappedResourceConfigurationPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeMappedResourceConfigurationPaginator(
    _DescribeMappedResourceConfigurationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/DescribeMappedResourceConfiguration.html#KinesisVideo.Paginator.DescribeMappedResourceConfiguration)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#describemappedresourceconfigurationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMappedResourceConfigurationInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeMappedResourceConfigurationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/DescribeMappedResourceConfiguration.html#KinesisVideo.Paginator.DescribeMappedResourceConfiguration.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#describemappedresourceconfigurationpaginator)
        """

if TYPE_CHECKING:
    _ListEdgeAgentConfigurationsPaginatorBase = AioPaginator[
        ListEdgeAgentConfigurationsOutputTypeDef
    ]
else:
    _ListEdgeAgentConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEdgeAgentConfigurationsPaginator(_ListEdgeAgentConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListEdgeAgentConfigurations.html#KinesisVideo.Paginator.ListEdgeAgentConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#listedgeagentconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEdgeAgentConfigurationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListEdgeAgentConfigurationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListEdgeAgentConfigurations.html#KinesisVideo.Paginator.ListEdgeAgentConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#listedgeagentconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListSignalingChannelsPaginatorBase = AioPaginator[ListSignalingChannelsOutputTypeDef]
else:
    _ListSignalingChannelsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSignalingChannelsPaginator(_ListSignalingChannelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListSignalingChannels.html#KinesisVideo.Paginator.ListSignalingChannels)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#listsignalingchannelspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSignalingChannelsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSignalingChannelsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListSignalingChannels.html#KinesisVideo.Paginator.ListSignalingChannels.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#listsignalingchannelspaginator)
        """

if TYPE_CHECKING:
    _ListStreamsPaginatorBase = AioPaginator[ListStreamsOutputTypeDef]
else:
    _ListStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStreamsPaginator(_ListStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListStreams.html#KinesisVideo.Paginator.ListStreams)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#liststreamspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStreamsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kinesisvideo/paginator/ListStreams.html#KinesisVideo.Paginator.ListStreams.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kinesisvideo/paginators/#liststreamspaginator)
        """
