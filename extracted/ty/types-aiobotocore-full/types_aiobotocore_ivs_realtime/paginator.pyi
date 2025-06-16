"""
Type annotations for ivs-realtime service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ivs_realtime.client import IvsrealtimeClient
    from types_aiobotocore_ivs_realtime.paginator import (
        ListIngestConfigurationsPaginator,
        ListParticipantReplicasPaginator,
        ListPublicKeysPaginator,
    )

    session = get_session()
    with session.create_client("ivs-realtime") as client:
        client: IvsrealtimeClient

        list_ingest_configurations_paginator: ListIngestConfigurationsPaginator = client.get_paginator("list_ingest_configurations")
        list_participant_replicas_paginator: ListParticipantReplicasPaginator = client.get_paginator("list_participant_replicas")
        list_public_keys_paginator: ListPublicKeysPaginator = client.get_paginator("list_public_keys")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListIngestConfigurationsRequestPaginateTypeDef,
    ListIngestConfigurationsResponseTypeDef,
    ListParticipantReplicasRequestPaginateTypeDef,
    ListParticipantReplicasResponseTypeDef,
    ListPublicKeysRequestPaginateTypeDef,
    ListPublicKeysResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListIngestConfigurationsPaginator",
    "ListParticipantReplicasPaginator",
    "ListPublicKeysPaginator",
)

if TYPE_CHECKING:
    _ListIngestConfigurationsPaginatorBase = AioPaginator[ListIngestConfigurationsResponseTypeDef]
else:
    _ListIngestConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIngestConfigurationsPaginator(_ListIngestConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListIngestConfigurations.html#Ivsrealtime.Paginator.ListIngestConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listingestconfigurationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIngestConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIngestConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListIngestConfigurations.html#Ivsrealtime.Paginator.ListIngestConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listingestconfigurationspaginator)
        """

if TYPE_CHECKING:
    _ListParticipantReplicasPaginatorBase = AioPaginator[ListParticipantReplicasResponseTypeDef]
else:
    _ListParticipantReplicasPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListParticipantReplicasPaginator(_ListParticipantReplicasPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListParticipantReplicas.html#Ivsrealtime.Paginator.ListParticipantReplicas)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listparticipantreplicaspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListParticipantReplicasRequestPaginateTypeDef]
    ) -> AioPageIterator[ListParticipantReplicasResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListParticipantReplicas.html#Ivsrealtime.Paginator.ListParticipantReplicas.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listparticipantreplicaspaginator)
        """

if TYPE_CHECKING:
    _ListPublicKeysPaginatorBase = AioPaginator[ListPublicKeysResponseTypeDef]
else:
    _ListPublicKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPublicKeysPaginator(_ListPublicKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListPublicKeys.html#Ivsrealtime.Paginator.ListPublicKeys)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listpublickeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPublicKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPublicKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ivs-realtime/paginator/ListPublicKeys.html#Ivsrealtime.Paginator.ListPublicKeys.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ivs_realtime/paginators/#listpublickeyspaginator)
        """
