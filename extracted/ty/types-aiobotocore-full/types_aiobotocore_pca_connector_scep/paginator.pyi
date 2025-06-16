"""
Type annotations for pca-connector-scep service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_pca_connector_scep.client import PrivateCAConnectorforSCEPClient
    from types_aiobotocore_pca_connector_scep.paginator import (
        ListChallengeMetadataPaginator,
        ListConnectorsPaginator,
    )

    session = get_session()
    with session.create_client("pca-connector-scep") as client:
        client: PrivateCAConnectorforSCEPClient

        list_challenge_metadata_paginator: ListChallengeMetadataPaginator = client.get_paginator("list_challenge_metadata")
        list_connectors_paginator: ListConnectorsPaginator = client.get_paginator("list_connectors")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListChallengeMetadataRequestPaginateTypeDef,
    ListChallengeMetadataResponseTypeDef,
    ListConnectorsRequestPaginateTypeDef,
    ListConnectorsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListChallengeMetadataPaginator", "ListConnectorsPaginator")

if TYPE_CHECKING:
    _ListChallengeMetadataPaginatorBase = AioPaginator[ListChallengeMetadataResponseTypeDef]
else:
    _ListChallengeMetadataPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListChallengeMetadataPaginator(_ListChallengeMetadataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListChallengeMetadata.html#PrivateCAConnectorforSCEP.Paginator.ListChallengeMetadata)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listchallengemetadatapaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChallengeMetadataRequestPaginateTypeDef]
    ) -> AioPageIterator[ListChallengeMetadataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListChallengeMetadata.html#PrivateCAConnectorforSCEP.Paginator.ListChallengeMetadata.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listchallengemetadatapaginator)
        """

if TYPE_CHECKING:
    _ListConnectorsPaginatorBase = AioPaginator[ListConnectorsResponseTypeDef]
else:
    _ListConnectorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListConnectorsPaginator(_ListConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListConnectors.html#PrivateCAConnectorforSCEP.Paginator.ListConnectors)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConnectorsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/pca-connector-scep/paginator/ListConnectors.html#PrivateCAConnectorforSCEP.Paginator.ListConnectors.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_pca_connector_scep/paginators/#listconnectorspaginator)
        """
