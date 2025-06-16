"""
Type annotations for iot-data service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot_data.client import IoTDataPlaneClient
    from types_aiobotocore_iot_data.paginator import (
        ListRetainedMessagesPaginator,
    )

    session = get_session()
    with session.create_client("iot-data") as client:
        client: IoTDataPlaneClient

        list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListRetainedMessagesRequestPaginateTypeDef,
    ListRetainedMessagesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRetainedMessagesPaginator",)

if TYPE_CHECKING:
    _ListRetainedMessagesPaginatorBase = AioPaginator[ListRetainedMessagesResponseTypeDef]
else:
    _ListRetainedMessagesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRetainedMessagesPaginator(_ListRetainedMessagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListRetainedMessages.html#IoTDataPlane.Paginator.ListRetainedMessages)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/paginators/#listretainedmessagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRetainedMessagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRetainedMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListRetainedMessages.html#IoTDataPlane.Paginator.ListRetainedMessages.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot_data/paginators/#listretainedmessagespaginator)
        """
