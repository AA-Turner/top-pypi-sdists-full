"""
Type annotations for application-signals service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_application_signals.client import CloudWatchApplicationSignalsClient
    from types_aiobotocore_application_signals.paginator import (
        ListServiceDependenciesPaginator,
        ListServiceDependentsPaginator,
        ListServiceLevelObjectiveExclusionWindowsPaginator,
        ListServiceLevelObjectivesPaginator,
        ListServiceOperationsPaginator,
        ListServicesPaginator,
    )

    session = get_session()
    with session.create_client("application-signals") as client:
        client: CloudWatchApplicationSignalsClient

        list_service_dependencies_paginator: ListServiceDependenciesPaginator = client.get_paginator("list_service_dependencies")
        list_service_dependents_paginator: ListServiceDependentsPaginator = client.get_paginator("list_service_dependents")
        list_service_level_objective_exclusion_windows_paginator: ListServiceLevelObjectiveExclusionWindowsPaginator = client.get_paginator("list_service_level_objective_exclusion_windows")
        list_service_level_objectives_paginator: ListServiceLevelObjectivesPaginator = client.get_paginator("list_service_level_objectives")
        list_service_operations_paginator: ListServiceOperationsPaginator = client.get_paginator("list_service_operations")
        list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    ListServiceDependenciesInputPaginateTypeDef,
    ListServiceDependenciesOutputTypeDef,
    ListServiceDependentsInputPaginateTypeDef,
    ListServiceDependentsOutputTypeDef,
    ListServiceLevelObjectiveExclusionWindowsInputPaginateTypeDef,
    ListServiceLevelObjectiveExclusionWindowsOutputTypeDef,
    ListServiceLevelObjectivesInputPaginateTypeDef,
    ListServiceLevelObjectivesOutputTypeDef,
    ListServiceOperationsInputPaginateTypeDef,
    ListServiceOperationsOutputTypeDef,
    ListServicesInputPaginateTypeDef,
    ListServicesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListServiceDependenciesPaginator",
    "ListServiceDependentsPaginator",
    "ListServiceLevelObjectiveExclusionWindowsPaginator",
    "ListServiceLevelObjectivesPaginator",
    "ListServiceOperationsPaginator",
    "ListServicesPaginator",
)

if TYPE_CHECKING:
    _ListServiceDependenciesPaginatorBase = AioPaginator[ListServiceDependenciesOutputTypeDef]
else:
    _ListServiceDependenciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceDependenciesPaginator(_ListServiceDependenciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependencies.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicedependenciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceDependenciesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceDependenciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependencies.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicedependenciespaginator)
        """

if TYPE_CHECKING:
    _ListServiceDependentsPaginatorBase = AioPaginator[ListServiceDependentsOutputTypeDef]
else:
    _ListServiceDependentsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceDependentsPaginator(_ListServiceDependentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependents.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicedependentspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceDependentsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceDependentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependents.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicedependentspaginator)
        """

if TYPE_CHECKING:
    _ListServiceLevelObjectiveExclusionWindowsPaginatorBase = AioPaginator[
        ListServiceLevelObjectiveExclusionWindowsOutputTypeDef
    ]
else:
    _ListServiceLevelObjectiveExclusionWindowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceLevelObjectiveExclusionWindowsPaginator(
    _ListServiceLevelObjectiveExclusionWindowsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectiveExclusionWindows.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectiveExclusionWindows)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicelevelobjectiveexclusionwindowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceLevelObjectiveExclusionWindowsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceLevelObjectiveExclusionWindowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectiveExclusionWindows.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectiveExclusionWindows.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicelevelobjectiveexclusionwindowspaginator)
        """

if TYPE_CHECKING:
    _ListServiceLevelObjectivesPaginatorBase = AioPaginator[ListServiceLevelObjectivesOutputTypeDef]
else:
    _ListServiceLevelObjectivesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceLevelObjectivesPaginator(_ListServiceLevelObjectivesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectives.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicelevelobjectivespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceLevelObjectivesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceLevelObjectivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectives.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicelevelobjectivespaginator)
        """

if TYPE_CHECKING:
    _ListServiceOperationsPaginatorBase = AioPaginator[ListServiceOperationsOutputTypeDef]
else:
    _ListServiceOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServiceOperationsPaginator(_ListServiceOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceOperations.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listserviceoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceOperationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListServiceOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceOperations.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listserviceoperationspaginator)
        """

if TYPE_CHECKING:
    _ListServicesPaginatorBase = AioPaginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServices.html#CloudWatchApplicationSignals.Paginator.ListServices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> AioPageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServices.html#CloudWatchApplicationSignals.Paginator.ListServices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_application_signals/paginators/#listservicespaginator)
        """
