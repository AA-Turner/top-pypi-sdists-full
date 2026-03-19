"""
Type annotations for lexv2-models service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lexv2_models.client import LexModelsV2Client
    from types_aiobotocore_lexv2_models.paginator import (
        DescribeBotAnalyzerRecommendationPaginator,
        ListBotAnalyzerHistoryPaginator,
    )

    session = get_session()
    with session.create_client("lexv2-models") as client:
        client: LexModelsV2Client

        describe_bot_analyzer_recommendation_paginator: DescribeBotAnalyzerRecommendationPaginator = client.get_paginator("describe_bot_analyzer_recommendation")
        list_bot_analyzer_history_paginator: ListBotAnalyzerHistoryPaginator = client.get_paginator("list_bot_analyzer_history")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeBotAnalyzerRecommendationRequestPaginateTypeDef,
    DescribeBotAnalyzerRecommendationResponseTypeDef,
    ListBotAnalyzerHistoryRequestPaginateTypeDef,
    ListBotAnalyzerHistoryResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("DescribeBotAnalyzerRecommendationPaginator", "ListBotAnalyzerHistoryPaginator")

if TYPE_CHECKING:
    _DescribeBotAnalyzerRecommendationPaginatorBase = AioPaginator[
        DescribeBotAnalyzerRecommendationResponseTypeDef
    ]
else:
    _DescribeBotAnalyzerRecommendationPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeBotAnalyzerRecommendationPaginator(_DescribeBotAnalyzerRecommendationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/paginator/DescribeBotAnalyzerRecommendation.html#LexModelsV2.Paginator.DescribeBotAnalyzerRecommendation)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/paginators/#describebotanalyzerrecommendationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeBotAnalyzerRecommendationRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeBotAnalyzerRecommendationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/paginator/DescribeBotAnalyzerRecommendation.html#LexModelsV2.Paginator.DescribeBotAnalyzerRecommendation.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/paginators/#describebotanalyzerrecommendationpaginator)
        """

if TYPE_CHECKING:
    _ListBotAnalyzerHistoryPaginatorBase = AioPaginator[ListBotAnalyzerHistoryResponseTypeDef]
else:
    _ListBotAnalyzerHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBotAnalyzerHistoryPaginator(_ListBotAnalyzerHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/paginator/ListBotAnalyzerHistory.html#LexModelsV2.Paginator.ListBotAnalyzerHistory)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/paginators/#listbotanalyzerhistorypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBotAnalyzerHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBotAnalyzerHistoryResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lexv2-models/paginator/ListBotAnalyzerHistory.html#LexModelsV2.Paginator.ListBotAnalyzerHistory.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lexv2_models/paginators/#listbotanalyzerhistorypaginator)
        """
