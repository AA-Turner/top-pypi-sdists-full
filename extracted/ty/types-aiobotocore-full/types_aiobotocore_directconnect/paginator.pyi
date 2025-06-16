"""
Type annotations for directconnect service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_directconnect.client import DirectConnectClient
    from types_aiobotocore_directconnect.paginator import (
        DescribeDirectConnectGatewayAssociationsPaginator,
        DescribeDirectConnectGatewayAttachmentsPaginator,
        DescribeDirectConnectGatewaysPaginator,
    )

    session = get_session()
    with session.create_client("directconnect") as client:
        client: DirectConnectClient

        describe_direct_connect_gateway_associations_paginator: DescribeDirectConnectGatewayAssociationsPaginator = client.get_paginator("describe_direct_connect_gateway_associations")
        describe_direct_connect_gateway_attachments_paginator: DescribeDirectConnectGatewayAttachmentsPaginator = client.get_paginator("describe_direct_connect_gateway_attachments")
        describe_direct_connect_gateways_paginator: DescribeDirectConnectGatewaysPaginator = client.get_paginator("describe_direct_connect_gateways")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeDirectConnectGatewayAssociationsRequestPaginateTypeDef,
    DescribeDirectConnectGatewayAssociationsResultTypeDef,
    DescribeDirectConnectGatewayAttachmentsRequestPaginateTypeDef,
    DescribeDirectConnectGatewayAttachmentsResultTypeDef,
    DescribeDirectConnectGatewaysRequestPaginateTypeDef,
    DescribeDirectConnectGatewaysResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeDirectConnectGatewayAssociationsPaginator",
    "DescribeDirectConnectGatewayAttachmentsPaginator",
    "DescribeDirectConnectGatewaysPaginator",
)

if TYPE_CHECKING:
    _DescribeDirectConnectGatewayAssociationsPaginatorBase = AioPaginator[
        DescribeDirectConnectGatewayAssociationsResultTypeDef
    ]
else:
    _DescribeDirectConnectGatewayAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDirectConnectGatewayAssociationsPaginator(
    _DescribeDirectConnectGatewayAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAssociations.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAssociations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/#describedirectconnectgatewayassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDirectConnectGatewayAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDirectConnectGatewayAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAssociations.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAssociations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/#describedirectconnectgatewayassociationspaginator)
        """

if TYPE_CHECKING:
    _DescribeDirectConnectGatewayAttachmentsPaginatorBase = AioPaginator[
        DescribeDirectConnectGatewayAttachmentsResultTypeDef
    ]
else:
    _DescribeDirectConnectGatewayAttachmentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDirectConnectGatewayAttachmentsPaginator(
    _DescribeDirectConnectGatewayAttachmentsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAttachments.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAttachments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/#describedirectconnectgatewayattachmentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDirectConnectGatewayAttachmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDirectConnectGatewayAttachmentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGatewayAttachments.html#DirectConnect.Paginator.DescribeDirectConnectGatewayAttachments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/#describedirectconnectgatewayattachmentspaginator)
        """

if TYPE_CHECKING:
    _DescribeDirectConnectGatewaysPaginatorBase = AioPaginator[
        DescribeDirectConnectGatewaysResultTypeDef
    ]
else:
    _DescribeDirectConnectGatewaysPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeDirectConnectGatewaysPaginator(_DescribeDirectConnectGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGateways.html#DirectConnect.Paginator.DescribeDirectConnectGateways)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/#describedirectconnectgatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeDirectConnectGatewaysRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeDirectConnectGatewaysResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/directconnect/paginator/DescribeDirectConnectGateways.html#DirectConnect.Paginator.DescribeDirectConnectGateways.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_directconnect/paginators/#describedirectconnectgatewayspaginator)
        """
