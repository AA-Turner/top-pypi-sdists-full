"""
Main interface for databrew service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_databrew/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_databrew import (
        Client,
        GlueDataBrewClient,
        ListDatasetsPaginator,
        ListJobRunsPaginator,
        ListJobsPaginator,
        ListProjectsPaginator,
        ListRecipeVersionsPaginator,
        ListRecipesPaginator,
        ListRulesetsPaginator,
        ListSchedulesPaginator,
    )

    session = get_session()
    async with session.create_client("databrew") as client:
        client: GlueDataBrewClient
        ...


    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_job_runs_paginator: ListJobRunsPaginator = client.get_paginator("list_job_runs")
    list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
    list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
    list_recipe_versions_paginator: ListRecipeVersionsPaginator = client.get_paginator("list_recipe_versions")
    list_recipes_paginator: ListRecipesPaginator = client.get_paginator("list_recipes")
    list_rulesets_paginator: ListRulesetsPaginator = client.get_paginator("list_rulesets")
    list_schedules_paginator: ListSchedulesPaginator = client.get_paginator("list_schedules")
    ```
"""

from .client import GlueDataBrewClient
from .paginator import (
    ListDatasetsPaginator,
    ListJobRunsPaginator,
    ListJobsPaginator,
    ListProjectsPaginator,
    ListRecipesPaginator,
    ListRecipeVersionsPaginator,
    ListRulesetsPaginator,
    ListSchedulesPaginator,
)

Client = GlueDataBrewClient

__all__ = (
    "Client",
    "GlueDataBrewClient",
    "ListDatasetsPaginator",
    "ListJobRunsPaginator",
    "ListJobsPaginator",
    "ListProjectsPaginator",
    "ListRecipeVersionsPaginator",
    "ListRecipesPaginator",
    "ListRulesetsPaginator",
    "ListSchedulesPaginator",
)
