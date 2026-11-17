"""
Main interface for wellarchitected service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_wellarchitected/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_wellarchitected import (
        AgentOrganizationalReportCompletedWaiter,
        Client,
        ListAgentContextsPaginator,
        ListAgentGoalsPaginator,
        ListAgentOrganizationalReportsPaginator,
        ListAgentProfilesPaginator,
        ListAgentRecommendationGenerationsPaginator,
        ListAgentRecommendationItemsPaginator,
        ListAgentRecommendationsPaginator,
        WellArchitectedClient,
    )

    session = Session()
    client: WellArchitectedClient = session.client("wellarchitected")

    agent_organizational_report_completed_waiter: AgentOrganizationalReportCompletedWaiter = client.get_waiter("agent_organizational_report_completed")

    list_agent_contexts_paginator: ListAgentContextsPaginator = client.get_paginator("list_agent_contexts")
    list_agent_goals_paginator: ListAgentGoalsPaginator = client.get_paginator("list_agent_goals")
    list_agent_organizational_reports_paginator: ListAgentOrganizationalReportsPaginator = client.get_paginator("list_agent_organizational_reports")
    list_agent_profiles_paginator: ListAgentProfilesPaginator = client.get_paginator("list_agent_profiles")
    list_agent_recommendation_generations_paginator: ListAgentRecommendationGenerationsPaginator = client.get_paginator("list_agent_recommendation_generations")
    list_agent_recommendation_items_paginator: ListAgentRecommendationItemsPaginator = client.get_paginator("list_agent_recommendation_items")
    list_agent_recommendations_paginator: ListAgentRecommendationsPaginator = client.get_paginator("list_agent_recommendations")
    ```
"""

from .client import WellArchitectedClient
from .paginator import (
    ListAgentContextsPaginator,
    ListAgentGoalsPaginator,
    ListAgentOrganizationalReportsPaginator,
    ListAgentProfilesPaginator,
    ListAgentRecommendationGenerationsPaginator,
    ListAgentRecommendationItemsPaginator,
    ListAgentRecommendationsPaginator,
)
from .waiter import AgentOrganizationalReportCompletedWaiter

Client = WellArchitectedClient


__all__ = (
    "AgentOrganizationalReportCompletedWaiter",
    "Client",
    "ListAgentContextsPaginator",
    "ListAgentGoalsPaginator",
    "ListAgentOrganizationalReportsPaginator",
    "ListAgentProfilesPaginator",
    "ListAgentRecommendationGenerationsPaginator",
    "ListAgentRecommendationItemsPaginator",
    "ListAgentRecommendationsPaginator",
    "WellArchitectedClient",
)
