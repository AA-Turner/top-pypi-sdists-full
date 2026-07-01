"""
Type annotations for observabilityadmin service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient
    from types_aiobotocore_observabilityadmin.paginator import (
        ListCentralizationRulesForOrganizationPaginator,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
        ListS3TableIntegrationsPaginator,
        ListTelemetryPipelinesPaginator,
        ListTelemetryRulesForOrganizationPaginator,
        ListTelemetryRulesPaginator,
    )

    session = get_session()
    with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient

        list_centralization_rules_for_organization_paginator: ListCentralizationRulesForOrganizationPaginator = client.get_paginator("list_centralization_rules_for_organization")
        list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
        list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
        list_s3_table_integrations_paginator: ListS3TableIntegrationsPaginator = client.get_paginator("list_s3_table_integrations")
        list_telemetry_pipelines_paginator: ListTelemetryPipelinesPaginator = client.get_paginator("list_telemetry_pipelines")
        list_telemetry_rules_for_organization_paginator: ListTelemetryRulesForOrganizationPaginator = client.get_paginator("list_telemetry_rules_for_organization")
        list_telemetry_rules_paginator: ListTelemetryRulesPaginator = client.get_paginator("list_telemetry_rules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListCentralizationRulesForOrganizationInputPaginateTypeDef,
    ListCentralizationRulesForOrganizationOutputTypeDef,
    ListResourceTelemetryForOrganizationInputPaginateTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputPaginateTypeDef,
    ListResourceTelemetryOutputTypeDef,
    ListS3TableIntegrationsInputPaginateTypeDef,
    ListS3TableIntegrationsOutputTypeDef,
    ListTelemetryPipelinesInputPaginateTypeDef,
    ListTelemetryPipelinesOutputTypeDef,
    ListTelemetryRulesForOrganizationInputPaginateTypeDef,
    ListTelemetryRulesForOrganizationOutputTypeDef,
    ListTelemetryRulesInputPaginateTypeDef,
    ListTelemetryRulesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListCentralizationRulesForOrganizationPaginator",
    "ListResourceTelemetryForOrganizationPaginator",
    "ListResourceTelemetryPaginator",
    "ListS3TableIntegrationsPaginator",
    "ListTelemetryPipelinesPaginator",
    "ListTelemetryRulesForOrganizationPaginator",
    "ListTelemetryRulesPaginator",
)

if TYPE_CHECKING:
    _ListCentralizationRulesForOrganizationPaginatorBase = AioPaginator[
        ListCentralizationRulesForOrganizationOutputTypeDef
    ]
else:
    _ListCentralizationRulesForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCentralizationRulesForOrganizationPaginator(
    _ListCentralizationRulesForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListCentralizationRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListCentralizationRulesForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listcentralizationrulesfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCentralizationRulesForOrganizationInputPaginateTypeDef]
    ) -> AioPageIterator[ListCentralizationRulesForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListCentralizationRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListCentralizationRulesForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listcentralizationrulesfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListResourceTelemetryForOrganizationPaginatorBase = AioPaginator[
        ListResourceTelemetryForOrganizationOutputTypeDef
    ]
else:
    _ListResourceTelemetryForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceTelemetryForOrganizationPaginator(
    _ListResourceTelemetryForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTelemetryForOrganizationInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceTelemetryForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListResourceTelemetryPaginatorBase = AioPaginator[ListResourceTelemetryOutputTypeDef]
else:
    _ListResourceTelemetryPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceTelemetryPaginator(_ListResourceTelemetryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetrypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTelemetryInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceTelemetryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listresourcetelemetrypaginator)
        """

if TYPE_CHECKING:
    _ListS3TableIntegrationsPaginatorBase = AioPaginator[ListS3TableIntegrationsOutputTypeDef]
else:
    _ListS3TableIntegrationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListS3TableIntegrationsPaginator(_ListS3TableIntegrationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListS3TableIntegrations.html#CloudWatchObservabilityAdminService.Paginator.ListS3TableIntegrations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#lists3tableintegrationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListS3TableIntegrationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListS3TableIntegrationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListS3TableIntegrations.html#CloudWatchObservabilityAdminService.Paginator.ListS3TableIntegrations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#lists3tableintegrationspaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryPipelinesPaginatorBase = AioPaginator[ListTelemetryPipelinesOutputTypeDef]
else:
    _ListTelemetryPipelinesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTelemetryPipelinesPaginator(_ListTelemetryPipelinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryPipelines.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryPipelines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listtelemetrypipelinespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryPipelinesInputPaginateTypeDef]
    ) -> AioPageIterator[ListTelemetryPipelinesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryPipelines.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryPipelines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listtelemetrypipelinespaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryRulesForOrganizationPaginatorBase = AioPaginator[
        ListTelemetryRulesForOrganizationOutputTypeDef
    ]
else:
    _ListTelemetryRulesForOrganizationPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTelemetryRulesForOrganizationPaginator(_ListTelemetryRulesForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRulesForOrganization)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listtelemetryrulesfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryRulesForOrganizationInputPaginateTypeDef]
    ) -> AioPageIterator[ListTelemetryRulesForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRulesForOrganization.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listtelemetryrulesfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryRulesPaginatorBase = AioPaginator[ListTelemetryRulesOutputTypeDef]
else:
    _ListTelemetryRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTelemetryRulesPaginator(_ListTelemetryRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRules.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listtelemetryrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryRulesInputPaginateTypeDef]
    ) -> AioPageIterator[ListTelemetryRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRules.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/paginators/#listtelemetryrulespaginator)
        """
