"""
Type annotations for wellarchitected service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_wellarchitected.client import WellArchitectedClient
    from mypy_boto3_wellarchitected.paginator import (
        ListAgentContextsPaginator,
        ListAgentGoalsPaginator,
        ListAgentProfilesPaginator,
        ListAgentRecommendationGenerationsPaginator,
        ListAgentRecommendationItemsPaginator,
        ListAgentRecommendationsPaginator,
    )

    session = Session()
    client: WellArchitectedClient = session.client("wellarchitected")

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

from botocore.paginate import PageIterator, Paginator

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
    _ListAgentContextsPaginatorBase = Paginator[ListAgentContextsResponseTypeDef]
else:
    _ListAgentContextsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentContextsPaginator(_ListAgentContextsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentContexts.html#WellArchitected.Paginator.ListAgentContexts)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentcontextspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentContextsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentContextsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentContexts.html#WellArchitected.Paginator.ListAgentContexts.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentcontextspaginator)
        """

if TYPE_CHECKING:
    _ListAgentGoalsPaginatorBase = Paginator[ListAgentGoalsResponseTypeDef]
else:
    _ListAgentGoalsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentGoalsPaginator(_ListAgentGoalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentGoals.html#WellArchitected.Paginator.ListAgentGoals)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentgoalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentGoalsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentGoalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentGoals.html#WellArchitected.Paginator.ListAgentGoals.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentgoalspaginator)
        """

if TYPE_CHECKING:
    _ListAgentProfilesPaginatorBase = Paginator[ListAgentProfilesResponseTypeDef]
else:
    _ListAgentProfilesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentProfilesPaginator(_ListAgentProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentProfiles.html#WellArchitected.Paginator.ListAgentProfiles)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentProfilesRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentProfiles.html#WellArchitected.Paginator.ListAgentProfiles.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentprofilespaginator)
        """

if TYPE_CHECKING:
    _ListAgentRecommendationGenerationsPaginatorBase = Paginator[
        ListAgentRecommendationGenerationsResponseTypeDef
    ]
else:
    _ListAgentRecommendationGenerationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRecommendationGenerationsPaginator(_ListAgentRecommendationGenerationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationGenerations.html#WellArchitected.Paginator.ListAgentRecommendationGenerations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentrecommendationgenerationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRecommendationGenerationsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentRecommendationGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationGenerations.html#WellArchitected.Paginator.ListAgentRecommendationGenerations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentrecommendationgenerationspaginator)
        """

if TYPE_CHECKING:
    _ListAgentRecommendationItemsPaginatorBase = Paginator[
        ListAgentRecommendationItemsResponseTypeDef
    ]
else:
    _ListAgentRecommendationItemsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRecommendationItemsPaginator(_ListAgentRecommendationItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationItems.html#WellArchitected.Paginator.ListAgentRecommendationItems)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentrecommendationitemspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRecommendationItemsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentRecommendationItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendationItems.html#WellArchitected.Paginator.ListAgentRecommendationItems.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentrecommendationitemspaginator)
        """

if TYPE_CHECKING:
    _ListAgentRecommendationsPaginatorBase = Paginator[ListAgentRecommendationsResponseTypeDef]
else:
    _ListAgentRecommendationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRecommendationsPaginator(_ListAgentRecommendationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendations.html#WellArchitected.Paginator.ListAgentRecommendations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentrecommendationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRecommendationsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentRecommendationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/wellarchitected/paginator/ListAgentRecommendations.html#WellArchitected.Paginator.ListAgentRecommendations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_wellarchitected/paginators/#listagentrecommendationspaginator)
        """
