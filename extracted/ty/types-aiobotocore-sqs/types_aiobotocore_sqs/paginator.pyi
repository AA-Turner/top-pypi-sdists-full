"""
Type annotations for sqs service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sqs.client import SQSClient
    from types_aiobotocore_sqs.paginator import (
        ListDeadLetterSourceQueuesPaginator,
        ListQueuesPaginator,
    )

    session = get_session()
    with session.create_client("sqs") as client:
        client: SQSClient

        list_dead_letter_source_queues_paginator: ListDeadLetterSourceQueuesPaginator = client.get_paginator("list_dead_letter_source_queues")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListDeadLetterSourceQueuesRequestPaginateTypeDef,
    ListDeadLetterSourceQueuesResultTypeDef,
    ListQueuesRequestPaginateTypeDef,
    ListQueuesResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("ListDeadLetterSourceQueuesPaginator", "ListQueuesPaginator")

if TYPE_CHECKING:
    _ListDeadLetterSourceQueuesPaginatorBase = AioPaginator[ListDeadLetterSourceQueuesResultTypeDef]
else:
    _ListDeadLetterSourceQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDeadLetterSourceQueuesPaginator(_ListDeadLetterSourceQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/paginator/ListDeadLetterSourceQueues.html#SQS.Paginator.ListDeadLetterSourceQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listdeadlettersourcequeuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeadLetterSourceQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeadLetterSourceQueuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/paginator/ListDeadLetterSourceQueues.html#SQS.Paginator.ListDeadLetterSourceQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listdeadlettersourcequeuespaginator)
        """

if TYPE_CHECKING:
    _ListQueuesPaginatorBase = AioPaginator[ListQueuesResultTypeDef]
else:
    _ListQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQueuesPaginator(_ListQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/paginator/ListQueues.html#SQS.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listqueuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueuesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/paginator/ListQueues.html#SQS.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/paginators/#listqueuespaginator)
        """
