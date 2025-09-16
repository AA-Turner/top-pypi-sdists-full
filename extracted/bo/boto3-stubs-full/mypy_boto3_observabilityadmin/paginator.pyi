"""
Type annotations for observabilityadmin service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient
    from mypy_boto3_observabilityadmin.paginator import (
        ListCentralizationRulesForOrganizationPaginator,
        ListResourceTelemetryForOrganizationPaginator,
        ListResourceTelemetryPaginator,
        ListTelemetryRulesForOrganizationPaginator,
        ListTelemetryRulesPaginator,
    )

    session = Session()
    client: CloudWatchObservabilityAdminServiceClient = session.client("observabilityadmin")

    list_centralization_rules_for_organization_paginator: ListCentralizationRulesForOrganizationPaginator = client.get_paginator("list_centralization_rules_for_organization")
    list_resource_telemetry_for_organization_paginator: ListResourceTelemetryForOrganizationPaginator = client.get_paginator("list_resource_telemetry_for_organization")
    list_resource_telemetry_paginator: ListResourceTelemetryPaginator = client.get_paginator("list_resource_telemetry")
    list_telemetry_rules_for_organization_paginator: ListTelemetryRulesForOrganizationPaginator = client.get_paginator("list_telemetry_rules_for_organization")
    list_telemetry_rules_paginator: ListTelemetryRulesPaginator = client.get_paginator("list_telemetry_rules")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListCentralizationRulesForOrganizationInputPaginateTypeDef,
    ListCentralizationRulesForOrganizationOutputTypeDef,
    ListResourceTelemetryForOrganizationInputPaginateTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputPaginateTypeDef,
    ListResourceTelemetryOutputTypeDef,
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
    "ListTelemetryRulesForOrganizationPaginator",
    "ListTelemetryRulesPaginator",
)

if TYPE_CHECKING:
    _ListCentralizationRulesForOrganizationPaginatorBase = Paginator[
        ListCentralizationRulesForOrganizationOutputTypeDef
    ]
else:
    _ListCentralizationRulesForOrganizationPaginatorBase = Paginator  # type: ignore[assignment]

class ListCentralizationRulesForOrganizationPaginator(
    _ListCentralizationRulesForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListCentralizationRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListCentralizationRulesForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listcentralizationrulesfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCentralizationRulesForOrganizationInputPaginateTypeDef]
    ) -> PageIterator[ListCentralizationRulesForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListCentralizationRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListCentralizationRulesForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listcentralizationrulesfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListResourceTelemetryForOrganizationPaginatorBase = Paginator[
        ListResourceTelemetryForOrganizationOutputTypeDef
    ]
else:
    _ListResourceTelemetryForOrganizationPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourceTelemetryForOrganizationPaginator(
    _ListResourceTelemetryForOrganizationPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTelemetryForOrganizationInputPaginateTypeDef]
    ) -> PageIterator[ListResourceTelemetryForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetryForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetryForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listresourcetelemetryfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListResourceTelemetryPaginatorBase = Paginator[ListResourceTelemetryOutputTypeDef]
else:
    _ListResourceTelemetryPaginatorBase = Paginator  # type: ignore[assignment]

class ListResourceTelemetryPaginator(_ListResourceTelemetryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listresourcetelemetrypaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceTelemetryInputPaginateTypeDef]
    ) -> PageIterator[ListResourceTelemetryOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListResourceTelemetry.html#CloudWatchObservabilityAdminService.Paginator.ListResourceTelemetry.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listresourcetelemetrypaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryRulesForOrganizationPaginatorBase = Paginator[
        ListTelemetryRulesForOrganizationOutputTypeDef
    ]
else:
    _ListTelemetryRulesForOrganizationPaginatorBase = Paginator  # type: ignore[assignment]

class ListTelemetryRulesForOrganizationPaginator(_ListTelemetryRulesForOrganizationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRulesForOrganization)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listtelemetryrulesfororganizationpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryRulesForOrganizationInputPaginateTypeDef]
    ) -> PageIterator[ListTelemetryRulesForOrganizationOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRulesForOrganization.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRulesForOrganization.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listtelemetryrulesfororganizationpaginator)
        """

if TYPE_CHECKING:
    _ListTelemetryRulesPaginatorBase = Paginator[ListTelemetryRulesOutputTypeDef]
else:
    _ListTelemetryRulesPaginatorBase = Paginator  # type: ignore[assignment]

class ListTelemetryRulesPaginator(_ListTelemetryRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRules.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRules)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listtelemetryrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTelemetryRulesInputPaginateTypeDef]
    ) -> PageIterator[ListTelemetryRulesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/paginator/ListTelemetryRules.html#CloudWatchObservabilityAdminService.Paginator.ListTelemetryRules.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_observabilityadmin/paginators/#listtelemetryrulespaginator)
        """
