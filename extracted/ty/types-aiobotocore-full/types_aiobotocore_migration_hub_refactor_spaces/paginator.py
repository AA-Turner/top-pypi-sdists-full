"""
Type annotations for migration-hub-refactor-spaces service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_migration_hub_refactor_spaces.client import MigrationHubRefactorSpacesClient
    from types_aiobotocore_migration_hub_refactor_spaces.paginator import (
        ListApplicationsPaginator,
        ListEnvironmentVpcsPaginator,
        ListEnvironmentsPaginator,
        ListRoutesPaginator,
        ListServicesPaginator,
    )

    session = get_session()
    with session.create_client("migration-hub-refactor-spaces") as client:
        client: MigrationHubRefactorSpacesClient

        list_applications_paginator: ListApplicationsPaginator = client.get_paginator("list_applications")
        list_environment_vpcs_paginator: ListEnvironmentVpcsPaginator = client.get_paginator("list_environment_vpcs")
        list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
        list_routes_paginator: ListRoutesPaginator = client.get_paginator("list_routes")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListApplicationsRequestPaginateTypeDef,
    ListApplicationsResponseTypeDef,
    ListEnvironmentsRequestPaginateTypeDef,
    ListEnvironmentsResponseTypeDef,
    ListEnvironmentVpcsRequestPaginateTypeDef,
    ListEnvironmentVpcsResponseTypeDef,
    ListRoutesRequestPaginateTypeDef,
    ListRoutesResponseTypeDef,
    ListServicesRequestPaginateTypeDef,
    ListServicesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListApplicationsPaginator",
    "ListEnvironmentVpcsPaginator",
    "ListEnvironmentsPaginator",
    "ListRoutesPaginator",
    "ListServicesPaginator",
)


if TYPE_CHECKING:
    _ListApplicationsPaginatorBase = AioPaginator[ListApplicationsResponseTypeDef]
else:
    _ListApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListApplicationsPaginator(_ListApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListApplications.html#MigrationHubRefactorSpaces.Paginator.ListApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listapplicationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListApplications.html#MigrationHubRefactorSpaces.Paginator.ListApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listapplicationspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentVpcsPaginatorBase = AioPaginator[ListEnvironmentVpcsResponseTypeDef]
else:
    _ListEnvironmentVpcsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentVpcsPaginator(_ListEnvironmentVpcsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironmentVpcs.html#MigrationHubRefactorSpaces.Paginator.ListEnvironmentVpcs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listenvironmentvpcspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentVpcsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentVpcsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironmentVpcs.html#MigrationHubRefactorSpaces.Paginator.ListEnvironmentVpcs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listenvironmentvpcspaginator)
        """


if TYPE_CHECKING:
    _ListEnvironmentsPaginatorBase = AioPaginator[ListEnvironmentsResponseTypeDef]
else:
    _ListEnvironmentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListEnvironmentsPaginator(_ListEnvironmentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironments.html#MigrationHubRefactorSpaces.Paginator.ListEnvironments)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listenvironmentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEnvironmentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEnvironmentsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListEnvironments.html#MigrationHubRefactorSpaces.Paginator.ListEnvironments.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listenvironmentspaginator)
        """


if TYPE_CHECKING:
    _ListRoutesPaginatorBase = AioPaginator[ListRoutesResponseTypeDef]
else:
    _ListRoutesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRoutesPaginator(_ListRoutesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListRoutes.html#MigrationHubRefactorSpaces.Paginator.ListRoutes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listroutespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoutesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListRoutes.html#MigrationHubRefactorSpaces.Paginator.ListRoutes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listroutespaginator)
        """


if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesResponseTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListServices.html#MigrationHubRefactorSpaces.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListServicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/migration-hub-refactor-spaces/paginator/ListServices.html#MigrationHubRefactorSpaces.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migration_hub_refactor_spaces/paginators/#listservicespaginator)
        """
