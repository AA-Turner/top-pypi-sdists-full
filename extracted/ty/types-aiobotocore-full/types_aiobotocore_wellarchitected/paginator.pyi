"""
Type annotations for wellarchitected service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_wellarchitected.client import WellArchitectedClient
    from types_aiobotocore_wellarchitected.paginator import (
        ListAgentContextsPaginator,
        ListAgentGoalsPaginator,
        ListAgentProfilesPaginator,
        ListAgentRecommendationGenerationsPaginator,
        ListAgentRecommendationItemsPaginator,
        ListAgentRecommendationsPaginator,
    )

    session = get_session()
    with session.create_client("wellarchitected") as client:
        client: WellArchitectedClient

        list_agent_contexts_paginator: ListAgentContextsPaginator = client.get_paginator("list_agent_contexts")
        list_agent_goals_paginator: ListAgentGoalsPaginator = client.get_paginator("list_agent_goals")
        list_agent_profiles_paginator: ListAgentProfilesPaginator = client.get_paginator("list_agent_profiles")
        list_agent_recommendation_generations_paginator: ListAgentRecommendationGenerationsPaginator = client.get_paginator("list_agent_recommendation_generations")
        list_agent_recommendation_items_paginator: ListAgentRecommendationItemsPaginator = client.get_paginator("list_agent_recommendation_items")
        list_agent_recommendations_paginator: ListAgentRecommendationsPaginator = client.get_paginator("list_agent_recommendations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAgentContextsRequestPaginateTypeDef,
    ListAgentContextsResponseTypeDef,
    ListAgentGoalsRequestPaginateTypeDef,
    ListAgentGoalsResponseTypeDef,
    ListAgentProfilesRequestPaginateTypeDef,
    ListAgentProfilesResponseTypeDef,
    ListAgentRecommendationGenerationsRequestPaginateTypeDef,
    ListAgentRecommendationGenerationsResponseTypeDef,
    ListAgentRecommendationItemsRequestPaginateTypeDef,
    ListAgentRecommendationItemsResponseTypeDef,
    ListAgentRecommendationsRequestPaginateTypeDef,
    ListAgentRecommendationsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAgentContextsPaginator",
    "ListAgentGoalsPaginator",
    "ListAgentProfilesPaginator",
    "ListAgentRecommendationGenerationsPaginator",
    "ListAgentRecommendationItemsPaginator",
    "ListAgentRecommendationsPaginator",
)

if TYPE_CHECKING:
    _ListAgentContextsPaginatorBase = AioPaginator[ListAgentContextsResponseTypeDef]
else:
    _ListAgentContextsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentContextsPaginator(_ListAgentContextsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentContexts.html#WellArchitected.Paginator.ListAgentContexts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentcontextspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentContextsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentContexts.html#WellArchitected.Paginator.ListAgentContexts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentcontextspaginator)
        """

if TYPE_CHECKING:
    _ListAgentGoalsPaginatorBase = AioPaginator[ListAgentGoalsResponseTypeDef]
else:
    _ListAgentGoalsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentGoalsPaginator(_ListAgentGoalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentGoals.html#WellArchitected.Paginator.ListAgentGoals)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentgoalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentGoalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentGoalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentGoals.html#WellArchitected.Paginator.ListAgentGoals.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentgoalspaginator)
        """

if TYPE_CHECKING:
    _ListAgentProfilesPaginatorBase = AioPaginator[ListAgentProfilesResponseTypeDef]
else:
    _ListAgentProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentProfilesPaginator(_ListAgentProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentProfiles.html#WellArchitected.Paginator.ListAgentProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentProfiles.html#WellArchitected.Paginator.ListAgentProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentprofilespaginator)
        """

if TYPE_CHECKING:
    _ListAgentRecommendationGenerationsPaginatorBase = AioPaginator[
        ListAgentRecommendationGenerationsResponseTypeDef
    ]
else:
    _ListAgentRecommendationGenerationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentRecommendationGenerationsPaginator(_ListAgentRecommendationGenerationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationGenerations.html#WellArchitected.Paginator.ListAgentRecommendationGenerations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentrecommendationgenerationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRecommendationGenerationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentRecommendationGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationGenerations.html#WellArchitected.Paginator.ListAgentRecommendationGenerations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentrecommendationgenerationspaginator)
        """

if TYPE_CHECKING:
    _ListAgentRecommendationItemsPaginatorBase = AioPaginator[
        ListAgentRecommendationItemsResponseTypeDef
    ]
else:
    _ListAgentRecommendationItemsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentRecommendationItemsPaginator(_ListAgentRecommendationItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationItems.html#WellArchitected.Paginator.ListAgentRecommendationItems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentrecommendationitemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRecommendationItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentRecommendationItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationItems.html#WellArchitected.Paginator.ListAgentRecommendationItems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentrecommendationitemspaginator)
        """

if TYPE_CHECKING:
    _ListAgentRecommendationsPaginatorBase = AioPaginator[ListAgentRecommendationsResponseTypeDef]
else:
    _ListAgentRecommendationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentRecommendationsPaginator(_ListAgentRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendations.html#WellArchitected.Paginator.ListAgentRecommendations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentrecommendationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRecommendationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendations.html#WellArchitected.Paginator.ListAgentRecommendations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_wellarchitected/paginators/#listagentrecommendationspaginator)
        """
