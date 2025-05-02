"""
Type annotations for polly service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_polly.client import PollyClient
    from types_aiobotocore_polly.paginator import (
        DescribeVoicesPaginator,
        ListLexiconsPaginator,
        ListSpeechSynthesisTasksPaginator,
    )

    session = get_session()
    with session.create_client("polly") as client:
        client: PollyClient

        describe_voices_paginator: DescribeVoicesPaginator = client.get_paginator("describe_voices")
        list_lexicons_paginator: ListLexiconsPaginator = client.get_paginator("list_lexicons")
        list_speech_synthesis_tasks_paginator: ListSpeechSynthesisTasksPaginator = client.get_paginator("list_speech_synthesis_tasks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeVoicesInputPaginateTypeDef,
    DescribeVoicesOutputTypeDef,
    ListLexiconsInputPaginateTypeDef,
    ListLexiconsOutputTypeDef,
    ListSpeechSynthesisTasksInputPaginateTypeDef,
    ListSpeechSynthesisTasksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("DescribeVoicesPaginator", "ListLexiconsPaginator", "ListSpeechSynthesisTasksPaginator")


if TYPE_CHECKING:
    _DescribeVoicesPaginatorBase = AioPaginator[DescribeVoicesOutputTypeDef]
else:
    _DescribeVoicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeVoicesPaginator(_DescribeVoicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/DescribeVoices.html#Polly.Paginator.DescribeVoices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#describevoicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeVoicesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeVoicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/DescribeVoices.html#Polly.Paginator.DescribeVoices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#describevoicespaginator)
        """


if TYPE_CHECKING:
    _ListLexiconsPaginatorBase = AioPaginator[ListLexiconsOutputTypeDef]
else:
    _ListLexiconsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListLexiconsPaginator(_ListLexiconsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListLexicons.html#Polly.Paginator.ListLexicons)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listlexiconspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLexiconsInputPaginateTypeDef]
    ) -> AioPageIterator[ListLexiconsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListLexicons.html#Polly.Paginator.ListLexicons.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listlexiconspaginator)
        """


if TYPE_CHECKING:
    _ListSpeechSynthesisTasksPaginatorBase = AioPaginator[ListSpeechSynthesisTasksOutputTypeDef]
else:
    _ListSpeechSynthesisTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSpeechSynthesisTasksPaginator(_ListSpeechSynthesisTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListSpeechSynthesisTasks.html#Polly.Paginator.ListSpeechSynthesisTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listspeechsynthesistaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSpeechSynthesisTasksInputPaginateTypeDef]
    ) -> AioPageIterator[ListSpeechSynthesisTasksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly/paginator/ListSpeechSynthesisTasks.html#Polly.Paginator.ListSpeechSynthesisTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_polly/paginators/#listspeechsynthesistaskspaginator)
        """
