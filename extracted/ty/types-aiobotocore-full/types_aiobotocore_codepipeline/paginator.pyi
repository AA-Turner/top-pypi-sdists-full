"""
Type annotations for codepipeline service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codepipeline.client import CodePipelineClient
    from types_aiobotocore_codepipeline.paginator import (
        ListActionExecutionsPaginator,
        ListActionTypesPaginator,
        ListDeployActionExecutionTargetsPaginator,
        ListPipelineExecutionsPaginator,
        ListPipelinesPaginator,
        ListRuleExecutionsPaginator,
        ListTagsForResourcePaginator,
        ListWebhooksPaginator,
    )

    session = get_session()
    with session.create_client("codepipeline") as client:
        client: CodePipelineClient

        list_action_executions_paginator: ListActionExecutionsPaginator = client.get_paginator("list_action_executions")
        list_action_types_paginator: ListActionTypesPaginator = client.get_paginator("list_action_types")
        list_deploy_action_execution_targets_paginator: ListDeployActionExecutionTargetsPaginator = client.get_paginator("list_deploy_action_execution_targets")
        list_pipeline_executions_paginator: ListPipelineExecutionsPaginator = client.get_paginator("list_pipeline_executions")
        list_pipelines_paginator: ListPipelinesPaginator = client.get_paginator("list_pipelines")
        list_rule_executions_paginator: ListRuleExecutionsPaginator = client.get_paginator("list_rule_executions")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_webhooks_paginator: ListWebhooksPaginator = client.get_paginator("list_webhooks")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListActionExecutionsInputPaginateTypeDef,
    ListActionExecutionsOutputTypeDef,
    ListActionTypesInputPaginateTypeDef,
    ListActionTypesOutputTypeDef,
    ListDeployActionExecutionTargetsInputPaginateTypeDef,
    ListDeployActionExecutionTargetsOutputTypeDef,
    ListPipelineExecutionsInputPaginateTypeDef,
    ListPipelineExecutionsOutputTypeDef,
    ListPipelinesInputPaginateTypeDef,
    ListPipelinesOutputTypeDef,
    ListRuleExecutionsInputPaginateTypeDef,
    ListRuleExecutionsOutputTypeDef,
    ListTagsForResourceInputPaginateTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWebhooksInputPaginateTypeDef,
    ListWebhooksOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListActionExecutionsPaginator",
    "ListActionTypesPaginator",
    "ListDeployActionExecutionTargetsPaginator",
    "ListPipelineExecutionsPaginator",
    "ListPipelinesPaginator",
    "ListRuleExecutionsPaginator",
    "ListTagsForResourcePaginator",
    "ListWebhooksPaginator",
)

if TYPE_CHECKING:
    _ListActionExecutionsPaginatorBase = AioPaginator[ListActionExecutionsOutputTypeDef]
else:
    _ListActionExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListActionExecutionsPaginator(_ListActionExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionExecutions.html#CodePipeline.Paginator.ListActionExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listactionexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListActionExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionExecutions.html#CodePipeline.Paginator.ListActionExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listactionexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListActionTypesPaginatorBase = AioPaginator[ListActionTypesOutputTypeDef]
else:
    _ListActionTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListActionTypesPaginator(_ListActionTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionTypes.html#CodePipeline.Paginator.ListActionTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listactiontypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActionTypesInputPaginateTypeDef]
    ) -> AioPageIterator[ListActionTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListActionTypes.html#CodePipeline.Paginator.ListActionTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listactiontypespaginator)
        """

if TYPE_CHECKING:
    _ListDeployActionExecutionTargetsPaginatorBase = AioPaginator[
        ListDeployActionExecutionTargetsOutputTypeDef
    ]
else:
    _ListDeployActionExecutionTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDeployActionExecutionTargetsPaginator(_ListDeployActionExecutionTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListDeployActionExecutionTargets.html#CodePipeline.Paginator.ListDeployActionExecutionTargets)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listdeployactionexecutiontargetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeployActionExecutionTargetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListDeployActionExecutionTargetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListDeployActionExecutionTargets.html#CodePipeline.Paginator.ListDeployActionExecutionTargets.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listdeployactionexecutiontargetspaginator)
        """

if TYPE_CHECKING:
    _ListPipelineExecutionsPaginatorBase = AioPaginator[ListPipelineExecutionsOutputTypeDef]
else:
    _ListPipelineExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelineExecutionsPaginator(_ListPipelineExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelineExecutions.html#CodePipeline.Paginator.ListPipelineExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listpipelineexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelineExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListPipelineExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelineExecutions.html#CodePipeline.Paginator.ListPipelineExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listpipelineexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListPipelinesPaginatorBase = AioPaginator[ListPipelinesOutputTypeDef]
else:
    _ListPipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPipelinesPaginator(_ListPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelines.html#CodePipeline.Paginator.ListPipelines)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listpipelinespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPipelinesInputPaginateTypeDef]
    ) -> AioPageIterator[ListPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListPipelines.html#CodePipeline.Paginator.ListPipelines.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listpipelinespaginator)
        """

if TYPE_CHECKING:
    _ListRuleExecutionsPaginatorBase = AioPaginator[ListRuleExecutionsOutputTypeDef]
else:
    _ListRuleExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRuleExecutionsPaginator(_ListRuleExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListRuleExecutions.html#CodePipeline.Paginator.ListRuleExecutions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listruleexecutionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRuleExecutionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListRuleExecutionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListRuleExecutions.html#CodePipeline.Paginator.ListRuleExecutions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listruleexecutionspaginator)
        """

if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceOutputTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListTagsForResource.html#CodePipeline.Paginator.ListTagsForResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listtagsforresourcepaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceInputPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListTagsForResource.html#CodePipeline.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listtagsforresourcepaginator)
        """

if TYPE_CHECKING:
    _ListWebhooksPaginatorBase = AioPaginator[ListWebhooksOutputTypeDef]
else:
    _ListWebhooksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListWebhooksPaginator(_ListWebhooksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListWebhooks.html#CodePipeline.Paginator.ListWebhooks)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listwebhookspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWebhooksInputPaginateTypeDef]
    ) -> AioPageIterator[ListWebhooksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codepipeline/paginator/ListWebhooks.html#CodePipeline.Paginator.ListWebhooks.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codepipeline/paginators/#listwebhookspaginator)
        """
