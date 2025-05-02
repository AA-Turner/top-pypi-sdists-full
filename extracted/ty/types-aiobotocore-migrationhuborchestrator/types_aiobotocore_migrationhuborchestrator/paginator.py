"""
Type annotations for migrationhuborchestrator service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_migrationhuborchestrator.client import MigrationHubOrchestratorClient
    from types_aiobotocore_migrationhuborchestrator.paginator import (
        ListPluginsPaginator,
        ListTemplateStepGroupsPaginator,
        ListTemplateStepsPaginator,
        ListTemplatesPaginator,
        ListWorkflowStepGroupsPaginator,
        ListWorkflowStepsPaginator,
        ListWorkflowsPaginator,
    )

    session = get_session()
    with session.create_client("migrationhuborchestrator") as client:
        client: MigrationHubOrchestratorClient

        list_plugins_paginator: ListPluginsPaginator = client.get_paginator("list_plugins")
        list_template_step_groups_paginator: ListTemplateStepGroupsPaginator = client.get_paginator("list_template_step_groups")
        list_template_steps_paginator: ListTemplateStepsPaginator = client.get_paginator("list_template_steps")
        list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
        list_workflow_step_groups_paginator: ListWorkflowStepGroupsPaginator = client.get_paginator("list_workflow_step_groups")
        list_workflow_steps_paginator: ListWorkflowStepsPaginator = client.get_paginator("list_workflow_steps")
        list_workflows_paginator: ListWorkflowsPaginator = client.get_paginator("list_workflows")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListMigrationWorkflowsRequestPaginateTypeDef,
    ListMigrationWorkflowsResponseTypeDef,
    ListMigrationWorkflowTemplatesRequestPaginateTypeDef,
    ListMigrationWorkflowTemplatesResponseTypeDef,
    ListPluginsRequestPaginateTypeDef,
    ListPluginsResponseTypeDef,
    ListTemplateStepGroupsRequestPaginateTypeDef,
    ListTemplateStepGroupsResponseTypeDef,
    ListTemplateStepsRequestPaginateTypeDef,
    ListTemplateStepsResponseTypeDef,
    ListWorkflowStepGroupsRequestPaginateTypeDef,
    ListWorkflowStepGroupsResponseTypeDef,
    ListWorkflowStepsRequestPaginateTypeDef,
    ListWorkflowStepsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListPluginsPaginator",
    "ListTemplateStepGroupsPaginator",
    "ListTemplateStepsPaginator",
    "ListTemplatesPaginator",
    "ListWorkflowStepGroupsPaginator",
    "ListWorkflowStepsPaginator",
    "ListWorkflowsPaginator",
)


if TYPE_CHECKING:
    _ListPluginsPaginatorBase = AioPaginator[ListPluginsResponseTypeDef]
else:
    _ListPluginsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPluginsPaginator(_ListPluginsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListPlugins.html#MigrationHubOrchestrator.Paginator.ListPlugins)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listpluginspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPluginsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPluginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListPlugins.html#MigrationHubOrchestrator.Paginator.ListPlugins.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listpluginspaginator)
        """


if TYPE_CHECKING:
    _ListTemplateStepGroupsPaginatorBase = AioPaginator[ListTemplateStepGroupsResponseTypeDef]
else:
    _ListTemplateStepGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTemplateStepGroupsPaginator(_ListTemplateStepGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateStepGroups.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateStepGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplateStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateStepGroups.html#MigrationHubOrchestrator.Paginator.ListTemplateStepGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepgroupspaginator)
        """


if TYPE_CHECKING:
    _ListTemplateStepsPaginatorBase = AioPaginator[ListTemplateStepsResponseTypeDef]
else:
    _ListTemplateStepsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTemplateStepsPaginator(_ListTemplateStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateSteps.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTemplateStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTemplateStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplateSteps.html#MigrationHubOrchestrator.Paginator.ListTemplateSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatestepspaginator)
        """


if TYPE_CHECKING:
    _ListTemplatesPaginatorBase = AioPaginator[ListMigrationWorkflowTemplatesResponseTypeDef]
else:
    _ListTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTemplatesPaginator(_ListTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplates.html#MigrationHubOrchestrator.Paginator.ListTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMigrationWorkflowTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMigrationWorkflowTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListTemplates.html#MigrationHubOrchestrator.Paginator.ListTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listtemplatespaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowStepGroupsPaginatorBase = AioPaginator[ListWorkflowStepGroupsResponseTypeDef]
else:
    _ListWorkflowStepGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowStepGroupsPaginator(_ListWorkflowStepGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowStepGroups.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowStepGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowStepGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowStepGroups.html#MigrationHubOrchestrator.Paginator.ListWorkflowStepGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepgroupspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowStepsPaginatorBase = AioPaginator[ListWorkflowStepsResponseTypeDef]
else:
    _ListWorkflowStepsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowStepsPaginator(_ListWorkflowStepsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowSteps.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkflowStepsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListWorkflowStepsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflowSteps.html#MigrationHubOrchestrator.Paginator.ListWorkflowSteps.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowstepspaginator)
        """


if TYPE_CHECKING:
    _ListWorkflowsPaginatorBase = AioPaginator[ListMigrationWorkflowsResponseTypeDef]
else:
    _ListWorkflowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListWorkflowsPaginator(_ListWorkflowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflows.html#MigrationHubOrchestrator.Paginator.ListWorkflows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMigrationWorkflowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMigrationWorkflowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migrationhuborchestrator/paginator/ListWorkflows.html#MigrationHubOrchestrator.Paginator.ListWorkflows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/paginators/#listworkflowspaginator)
        """
