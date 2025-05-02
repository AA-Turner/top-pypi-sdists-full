"""
Type annotations for inspector service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_inspector.client import InspectorClient
    from types_aiobotocore_inspector.paginator import (
        ListAssessmentRunAgentsPaginator,
        ListAssessmentRunsPaginator,
        ListAssessmentTargetsPaginator,
        ListAssessmentTemplatesPaginator,
        ListEventSubscriptionsPaginator,
        ListExclusionsPaginator,
        ListFindingsPaginator,
        ListRulesPackagesPaginator,
        PreviewAgentsPaginator,
    )

    session = get_session()
    with session.create_client("inspector") as client:
        client: InspectorClient

        list_assessment_run_agents_paginator: ListAssessmentRunAgentsPaginator = client.get_paginator("list_assessment_run_agents")
        list_assessment_runs_paginator: ListAssessmentRunsPaginator = client.get_paginator("list_assessment_runs")
        list_assessment_targets_paginator: ListAssessmentTargetsPaginator = client.get_paginator("list_assessment_targets")
        list_assessment_templates_paginator: ListAssessmentTemplatesPaginator = client.get_paginator("list_assessment_templates")
        list_event_subscriptions_paginator: ListEventSubscriptionsPaginator = client.get_paginator("list_event_subscriptions")
        list_exclusions_paginator: ListExclusionsPaginator = client.get_paginator("list_exclusions")
        list_findings_paginator: ListFindingsPaginator = client.get_paginator("list_findings")
        list_rules_packages_paginator: ListRulesPackagesPaginator = client.get_paginator("list_rules_packages")
        preview_agents_paginator: PreviewAgentsPaginator = client.get_paginator("preview_agents")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListAssessmentRunAgentsRequestPaginateTypeDef,
    ListAssessmentRunAgentsResponseTypeDef,
    ListAssessmentRunsRequestPaginateTypeDef,
    ListAssessmentRunsResponseTypeDef,
    ListAssessmentTargetsRequestPaginateTypeDef,
    ListAssessmentTargetsResponseTypeDef,
    ListAssessmentTemplatesRequestPaginateTypeDef,
    ListAssessmentTemplatesResponseTypeDef,
    ListEventSubscriptionsRequestPaginateTypeDef,
    ListEventSubscriptionsResponseTypeDef,
    ListExclusionsRequestPaginateTypeDef,
    ListExclusionsResponseTypeDef,
    ListFindingsRequestPaginateTypeDef,
    ListFindingsResponseTypeDef,
    ListRulesPackagesRequestPaginateTypeDef,
    ListRulesPackagesResponseTypeDef,
    PreviewAgentsRequestPaginateTypeDef,
    PreviewAgentsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListAssessmentRunAgentsPaginator",
    "ListAssessmentRunsPaginator",
    "ListAssessmentTargetsPaginator",
    "ListAssessmentTemplatesPaginator",
    "ListEventSubscriptionsPaginator",
    "ListExclusionsPaginator",
    "ListFindingsPaginator",
    "ListRulesPackagesPaginator",
    "PreviewAgentsPaginator",
)


if TYPE_CHECKING:
    _ListAssessmentRunAgentsPaginatorBase = AioPaginator[ListAssessmentRunAgentsResponseTypeDef]
else:
    _ListAssessmentRunAgentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssessmentRunAgentsPaginator(_ListAssessmentRunAgentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRunAgents.html#Inspector.Paginator.ListAssessmentRunAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunagentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssessmentRunAgentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssessmentRunAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRunAgents.html#Inspector.Paginator.ListAssessmentRunAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunagentspaginator)
        """


if TYPE_CHECKING:
    _ListAssessmentRunsPaginatorBase = AioPaginator[ListAssessmentRunsResponseTypeDef]
else:
    _ListAssessmentRunsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssessmentRunsPaginator(_ListAssessmentRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRuns.html#Inspector.Paginator.ListAssessmentRuns)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssessmentRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssessmentRunsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentRuns.html#Inspector.Paginator.ListAssessmentRuns.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmentrunspaginator)
        """


if TYPE_CHECKING:
    _ListAssessmentTargetsPaginatorBase = AioPaginator[ListAssessmentTargetsResponseTypeDef]
else:
    _ListAssessmentTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssessmentTargetsPaginator(_ListAssessmentTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTargets.html#Inspector.Paginator.ListAssessmentTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssessmentTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssessmentTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTargets.html#Inspector.Paginator.ListAssessmentTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttargetspaginator)
        """


if TYPE_CHECKING:
    _ListAssessmentTemplatesPaginatorBase = AioPaginator[ListAssessmentTemplatesResponseTypeDef]
else:
    _ListAssessmentTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssessmentTemplatesPaginator(_ListAssessmentTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTemplates.html#Inspector.Paginator.ListAssessmentTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssessmentTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssessmentTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListAssessmentTemplates.html#Inspector.Paginator.ListAssessmentTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listassessmenttemplatespaginator)
        """


if TYPE_CHECKING:
    _ListEventSubscriptionsPaginatorBase = AioPaginator[ListEventSubscriptionsResponseTypeDef]
else:
    _ListEventSubscriptionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEventSubscriptionsPaginator(_ListEventSubscriptionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListEventSubscriptions.html#Inspector.Paginator.ListEventSubscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listeventsubscriptionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEventSubscriptionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEventSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListEventSubscriptions.html#Inspector.Paginator.ListEventSubscriptions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listeventsubscriptionspaginator)
        """


if TYPE_CHECKING:
    _ListExclusionsPaginatorBase = AioPaginator[ListExclusionsResponseTypeDef]
else:
    _ListExclusionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListExclusionsPaginator(_ListExclusionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListExclusions.html#Inspector.Paginator.ListExclusions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listexclusionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExclusionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListExclusionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListExclusions.html#Inspector.Paginator.ListExclusions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listexclusionspaginator)
        """


if TYPE_CHECKING:
    _ListFindingsPaginatorBase = AioPaginator[ListFindingsResponseTypeDef]
else:
    _ListFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFindingsPaginator(_ListFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListFindings.html#Inspector.Paginator.ListFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListFindings.html#Inspector.Paginator.ListFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listfindingspaginator)
        """


if TYPE_CHECKING:
    _ListRulesPackagesPaginatorBase = AioPaginator[ListRulesPackagesResponseTypeDef]
else:
    _ListRulesPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRulesPackagesPaginator(_ListRulesPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListRulesPackages.html#Inspector.Paginator.ListRulesPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listrulespackagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesPackagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRulesPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/ListRulesPackages.html#Inspector.Paginator.ListRulesPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#listrulespackagespaginator)
        """


if TYPE_CHECKING:
    _PreviewAgentsPaginatorBase = AioPaginator[PreviewAgentsResponseTypeDef]
else:
    _PreviewAgentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class PreviewAgentsPaginator(_PreviewAgentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/PreviewAgents.html#Inspector.Paginator.PreviewAgents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#previewagentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[PreviewAgentsRequestPaginateTypeDef]
    ) -> AioPageIterator[PreviewAgentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/inspector/paginator/PreviewAgents.html#Inspector.Paginator.PreviewAgents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_inspector/paginators/#previewagentspaginator)
        """
