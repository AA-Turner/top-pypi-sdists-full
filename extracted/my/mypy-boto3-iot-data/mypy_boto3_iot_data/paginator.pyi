"""
Type annotations for iot-data service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_iot_data.client import IoTDataPlaneClient
    from mypy_boto3_iot_data.paginator import (
        ListRetainedMessagesPaginator,
        ListSubscriptionsPaginator,
    )

    session = Session()
    client: IoTDataPlaneClient = session.client("iot-data")

    list_retained_messages_paginator: ListRetainedMessagesPaginator = client.get_paginator("list_retained_messages")
    list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListRetainedMessagesRequestPaginateTypeDef,
    ListRetainedMessagesResponseTypeDef,
    ListSubscriptionsRequestPaginateTypeDef,
    ListSubscriptionsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListRetainedMessagesPaginator", "ListSubscriptionsPaginator")

if TYPE_CHECKING:
    _ListRetainedMessagesPaginatorBase = Paginator[ListRetainedMessagesResponseTypeDef]
else:
    _ListRetainedMessagesPaginatorBase = Paginator  # type: ignore[assignment]

class ListRetainedMessagesPaginator(_ListRetainedMessagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListRetainedMessages.html#IoTDataPlane.Paginator.ListRetainedMessages)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listretainedmessagespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRetainedMessagesRequestPaginateTypeDef]
    ) -> PageIterator[ListRetainedMessagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListRetainedMessages.html#IoTDataPlane.Paginator.ListRetainedMessages.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listretainedmessagespaginator)
        """

if TYPE_CHECKING:
    _ListSubscriptionsPaginatorBase = Paginator[ListSubscriptionsResponseTypeDef]
else:
    _ListSubscriptionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListSubscriptionsPaginator(_ListSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListSubscriptions.html#IoTDataPlane.Paginator.ListSubscriptions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listsubscriptionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSubscriptionsRequestPaginateTypeDef]
    ) -> PageIterator[ListSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot-data/paginator/ListSubscriptions.html#IoTDataPlane.Paginator.ListSubscriptions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_iot_data/paginators/#listsubscriptionspaginator)
        """
