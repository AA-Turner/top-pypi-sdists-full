"""
Type annotations for application-signals service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_application_signals.client import CloudWatchApplicationSignalsClient
    from mypy_boto3_application_signals.paginator import (
        GetInstrumentationConfigurationStatusPaginator,
        ListEntityEventsPaginator,
        ListInstrumentationConfigurationsPaginator,
        ListServiceDependenciesPaginator,
        ListServiceDependentsPaginator,
        ListServiceLevelObjectiveExclusionWindowsPaginator,
        ListServiceLevelObjectivesPaginator,
        ListServiceOperationsPaginator,
        ListServiceStatesPaginator,
        ListServicesPaginator,
    )

    session = Session()
    client: CloudWatchApplicationSignalsClient = session.client("application-signals")

    get_instrumentation_configuration_status_paginator: GetInstrumentationConfigurationStatusPaginator = client.get_paginator("get_instrumentation_configuration_status")
    list_entity_events_paginator: ListEntityEventsPaginator = client.get_paginator("list_entity_events")
    list_instrumentation_configurations_paginator: ListInstrumentationConfigurationsPaginator = client.get_paginator("list_instrumentation_configurations")
    list_service_dependencies_paginator: ListServiceDependenciesPaginator = client.get_paginator("list_service_dependencies")
    list_service_dependents_paginator: ListServiceDependentsPaginator = client.get_paginator("list_service_dependents")
    list_service_level_objective_exclusion_windows_paginator: ListServiceLevelObjectiveExclusionWindowsPaginator = client.get_paginator("list_service_level_objective_exclusion_windows")
    list_service_level_objectives_paginator: ListServiceLevelObjectivesPaginator = client.get_paginator("list_service_level_objectives")
    list_service_operations_paginator: ListServiceOperationsPaginator = client.get_paginator("list_service_operations")
    list_service_states_paginator: ListServiceStatesPaginator = client.get_paginator("list_service_states")
    list_services_paginator: ListServicesPaginator = client.get_paginator("list_services")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    GetInstrumentationConfigurationStatusRequestPaginateTypeDef,
    GetInstrumentationConfigurationStatusResponseTypeDef,
    InstrumentationConfigurationsPageTypeDef,
    ListEntityEventsInputPaginateTypeDef,
    ListEntityEventsOutputTypeDef,
    ListInstrumentationConfigurationsRequestPaginateTypeDef,
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
    ListServiceStatesInputPaginateTypeDef,
    ListServiceStatesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetInstrumentationConfigurationStatusPaginator",
    "ListEntityEventsPaginator",
    "ListInstrumentationConfigurationsPaginator",
    "ListServiceDependenciesPaginator",
    "ListServiceDependentsPaginator",
    "ListServiceLevelObjectiveExclusionWindowsPaginator",
    "ListServiceLevelObjectivesPaginator",
    "ListServiceOperationsPaginator",
    "ListServiceStatesPaginator",
    "ListServicesPaginator",
)


if TYPE_CHECKING:
    _GetInstrumentationConfigurationStatusPaginatorBase = Paginator[
        GetInstrumentationConfigurationStatusResponseTypeDef
    ]
else:
    _GetInstrumentationConfigurationStatusPaginatorBase = Paginator  # type: ignore[assignment]


class GetInstrumentationConfigurationStatusPaginator(
    _GetInstrumentationConfigurationStatusPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/GetInstrumentationConfigurationStatus.html#CloudWatchApplicationSignals.Paginator.GetInstrumentationConfigurationStatus)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#getinstrumentationconfigurationstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetInstrumentationConfigurationStatusRequestPaginateTypeDef]
    ) -> PageIterator[GetInstrumentationConfigurationStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/GetInstrumentationConfigurationStatus.html#CloudWatchApplicationSignals.Paginator.GetInstrumentationConfigurationStatus.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#getinstrumentationconfigurationstatuspaginator)
        """


if TYPE_CHECKING:
    _ListEntityEventsPaginatorBase = Paginator[ListEntityEventsOutputTypeDef]
else:
    _ListEntityEventsPaginatorBase = Paginator  # type: ignore[assignment]


class ListEntityEventsPaginator(_ListEntityEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListEntityEvents.html#CloudWatchApplicationSignals.Paginator.ListEntityEvents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listentityeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEntityEventsInputPaginateTypeDef]
    ) -> PageIterator[ListEntityEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListEntityEvents.html#CloudWatchApplicationSignals.Paginator.ListEntityEvents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listentityeventspaginator)
        """


if TYPE_CHECKING:
    _ListInstrumentationConfigurationsPaginatorBase = Paginator[
        InstrumentationConfigurationsPageTypeDef
    ]
else:
    _ListInstrumentationConfigurationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListInstrumentationConfigurationsPaginator(_ListInstrumentationConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListInstrumentationConfigurations.html#CloudWatchApplicationSignals.Paginator.ListInstrumentationConfigurations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listinstrumentationconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstrumentationConfigurationsRequestPaginateTypeDef]
    ) -> PageIterator[InstrumentationConfigurationsPageTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListInstrumentationConfigurations.html#CloudWatchApplicationSignals.Paginator.ListInstrumentationConfigurations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listinstrumentationconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListServiceDependenciesPaginatorBase = Paginator[ListServiceDependenciesOutputTypeDef]
else:
    _ListServiceDependenciesPaginatorBase = Paginator  # type: ignore[assignment]


class ListServiceDependenciesPaginator(_ListServiceDependenciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependencies.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependenciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceDependenciesInputPaginateTypeDef]
    ) -> PageIterator[ListServiceDependenciesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependencies.html#CloudWatchApplicationSignals.Paginator.ListServiceDependencies.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependenciespaginator)
        """


if TYPE_CHECKING:
    _ListServiceDependentsPaginatorBase = Paginator[ListServiceDependentsOutputTypeDef]
else:
    _ListServiceDependentsPaginatorBase = Paginator  # type: ignore[assignment]


class ListServiceDependentsPaginator(_ListServiceDependentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependents.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceDependentsInputPaginateTypeDef]
    ) -> PageIterator[ListServiceDependentsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceDependents.html#CloudWatchApplicationSignals.Paginator.ListServiceDependents.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicedependentspaginator)
        """


if TYPE_CHECKING:
    _ListServiceLevelObjectiveExclusionWindowsPaginatorBase = Paginator[
        ListServiceLevelObjectiveExclusionWindowsOutputTypeDef
    ]
else:
    _ListServiceLevelObjectiveExclusionWindowsPaginatorBase = Paginator  # type: ignore[assignment]


class ListServiceLevelObjectiveExclusionWindowsPaginator(
    _ListServiceLevelObjectiveExclusionWindowsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectiveExclusionWindows.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectiveExclusionWindows)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectiveexclusionwindowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceLevelObjectiveExclusionWindowsInputPaginateTypeDef]
    ) -> PageIterator[ListServiceLevelObjectiveExclusionWindowsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectiveExclusionWindows.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectiveExclusionWindows.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectiveexclusionwindowspaginator)
        """


if TYPE_CHECKING:
    _ListServiceLevelObjectivesPaginatorBase = Paginator[ListServiceLevelObjectivesOutputTypeDef]
else:
    _ListServiceLevelObjectivesPaginatorBase = Paginator  # type: ignore[assignment]


class ListServiceLevelObjectivesPaginator(_ListServiceLevelObjectivesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectives.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectivespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceLevelObjectivesInputPaginateTypeDef]
    ) -> PageIterator[ListServiceLevelObjectivesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceLevelObjectives.html#CloudWatchApplicationSignals.Paginator.ListServiceLevelObjectives.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicelevelobjectivespaginator)
        """


if TYPE_CHECKING:
    _ListServiceOperationsPaginatorBase = Paginator[ListServiceOperationsOutputTypeDef]
else:
    _ListServiceOperationsPaginatorBase = Paginator  # type: ignore[assignment]


class ListServiceOperationsPaginator(_ListServiceOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceOperations.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listserviceoperationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceOperationsInputPaginateTypeDef]
    ) -> PageIterator[ListServiceOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceOperations.html#CloudWatchApplicationSignals.Paginator.ListServiceOperations.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listserviceoperationspaginator)
        """


if TYPE_CHECKING:
    _ListServiceStatesPaginatorBase = Paginator[ListServiceStatesOutputTypeDef]
else:
    _ListServiceStatesPaginatorBase = Paginator  # type: ignore[assignment]


class ListServiceStatesPaginator(_ListServiceStatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceStates.html#CloudWatchApplicationSignals.Paginator.ListServiceStates)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicestatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServiceStatesInputPaginateTypeDef]
    ) -> PageIterator[ListServiceStatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServiceStates.html#CloudWatchApplicationSignals.Paginator.ListServiceStates.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicestatespaginator)
        """


if TYPE_CHECKING:
    _ListServicesPaginatorBase = Paginator[ListServicesOutputTypeDef]
else:
    _ListServicesPaginatorBase = Paginator  # type: ignore[assignment]


class ListServicesPaginator(_ListServicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServices.html#CloudWatchApplicationSignals.Paginator.ListServices)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListServicesInputPaginateTypeDef]
    ) -> PageIterator[ListServicesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/application-signals/paginator/ListServices.html#CloudWatchApplicationSignals.Paginator.ListServices.paginate)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_application_signals/paginators/#listservicespaginator)
        """
