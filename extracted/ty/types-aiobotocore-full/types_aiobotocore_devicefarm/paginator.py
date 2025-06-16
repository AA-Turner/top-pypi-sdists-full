"""
Type annotations for devicefarm service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_devicefarm.client import DeviceFarmClient
    from types_aiobotocore_devicefarm.paginator import (
        GetOfferingStatusPaginator,
        ListArtifactsPaginator,
        ListDeviceInstancesPaginator,
        ListDevicePoolsPaginator,
        ListDevicesPaginator,
        ListInstanceProfilesPaginator,
        ListJobsPaginator,
        ListNetworkProfilesPaginator,
        ListOfferingPromotionsPaginator,
        ListOfferingTransactionsPaginator,
        ListOfferingsPaginator,
        ListProjectsPaginator,
        ListRemoteAccessSessionsPaginator,
        ListRunsPaginator,
        ListSamplesPaginator,
        ListSuitesPaginator,
        ListTestsPaginator,
        ListUniqueProblemsPaginator,
        ListUploadsPaginator,
        ListVPCEConfigurationsPaginator,
    )

    session = get_session()
    with session.create_client("devicefarm") as client:
        client: DeviceFarmClient

        get_offering_status_paginator: GetOfferingStatusPaginator = client.get_paginator("get_offering_status")
        list_artifacts_paginator: ListArtifactsPaginator = client.get_paginator("list_artifacts")
        list_device_instances_paginator: ListDeviceInstancesPaginator = client.get_paginator("list_device_instances")
        list_device_pools_paginator: ListDevicePoolsPaginator = client.get_paginator("list_device_pools")
        list_devices_paginator: ListDevicesPaginator = client.get_paginator("list_devices")
        list_instance_profiles_paginator: ListInstanceProfilesPaginator = client.get_paginator("list_instance_profiles")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_network_profiles_paginator: ListNetworkProfilesPaginator = client.get_paginator("list_network_profiles")
        list_offering_promotions_paginator: ListOfferingPromotionsPaginator = client.get_paginator("list_offering_promotions")
        list_offering_transactions_paginator: ListOfferingTransactionsPaginator = client.get_paginator("list_offering_transactions")
        list_offerings_paginator: ListOfferingsPaginator = client.get_paginator("list_offerings")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_remote_access_sessions_paginator: ListRemoteAccessSessionsPaginator = client.get_paginator("list_remote_access_sessions")
        list_runs_paginator: ListRunsPaginator = client.get_paginator("list_runs")
        list_samples_paginator: ListSamplesPaginator = client.get_paginator("list_samples")
        list_suites_paginator: ListSuitesPaginator = client.get_paginator("list_suites")
        list_tests_paginator: ListTestsPaginator = client.get_paginator("list_tests")
        list_unique_problems_paginator: ListUniqueProblemsPaginator = client.get_paginator("list_unique_problems")
        list_uploads_paginator: ListUploadsPaginator = client.get_paginator("list_uploads")
        list_vpce_configurations_paginator: ListVPCEConfigurationsPaginator = client.get_paginator("list_vpce_configurations")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetOfferingStatusRequestPaginateTypeDef,
    GetOfferingStatusResultTypeDef,
    ListArtifactsRequestPaginateTypeDef,
    ListArtifactsResultTypeDef,
    ListDeviceInstancesRequestPaginateTypeDef,
    ListDeviceInstancesResultTypeDef,
    ListDevicePoolsRequestPaginateTypeDef,
    ListDevicePoolsResultTypeDef,
    ListDevicesRequestPaginateTypeDef,
    ListDevicesResultTypeDef,
    ListInstanceProfilesRequestPaginateTypeDef,
    ListInstanceProfilesResultTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResultTypeDef,
    ListNetworkProfilesRequestPaginateTypeDef,
    ListNetworkProfilesResultTypeDef,
    ListOfferingPromotionsRequestPaginateTypeDef,
    ListOfferingPromotionsResultTypeDef,
    ListOfferingsRequestPaginateTypeDef,
    ListOfferingsResultTypeDef,
    ListOfferingTransactionsRequestPaginateTypeDef,
    ListOfferingTransactionsResultTypeDef,
    ListProjectsRequestPaginateTypeDef,
    ListProjectsResultTypeDef,
    ListRemoteAccessSessionsRequestPaginateTypeDef,
    ListRemoteAccessSessionsResultTypeDef,
    ListRunsRequestPaginateTypeDef,
    ListRunsResultTypeDef,
    ListSamplesRequestPaginateTypeDef,
    ListSamplesResultTypeDef,
    ListSuitesRequestPaginateTypeDef,
    ListSuitesResultTypeDef,
    ListTestsRequestPaginateTypeDef,
    ListTestsResultTypeDef,
    ListUniqueProblemsRequestPaginateTypeDef,
    ListUniqueProblemsResultTypeDef,
    ListUploadsRequestPaginateTypeDef,
    ListUploadsResultTypeDef,
    ListVPCEConfigurationsRequestPaginateTypeDef,
    ListVPCEConfigurationsResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetOfferingStatusPaginator",
    "ListArtifactsPaginator",
    "ListDeviceInstancesPaginator",
    "ListDevicePoolsPaginator",
    "ListDevicesPaginator",
    "ListInstanceProfilesPaginator",
    "ListJobsPaginator",
    "ListNetworkProfilesPaginator",
    "ListOfferingPromotionsPaginator",
    "ListOfferingTransactionsPaginator",
    "ListOfferingsPaginator",
    "ListProjectsPaginator",
    "ListRemoteAccessSessionsPaginator",
    "ListRunsPaginator",
    "ListSamplesPaginator",
    "ListSuitesPaginator",
    "ListTestsPaginator",
    "ListUniqueProblemsPaginator",
    "ListUploadsPaginator",
    "ListVPCEConfigurationsPaginator",
)


if TYPE_CHECKING:
    _GetOfferingStatusPaginatorBase = AioPaginator[GetOfferingStatusResultTypeDef]
else:
    _GetOfferingStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetOfferingStatusPaginator(_GetOfferingStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/GetOfferingStatus.html#DeviceFarm.Paginator.GetOfferingStatus)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#getofferingstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOfferingStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[GetOfferingStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/GetOfferingStatus.html#DeviceFarm.Paginator.GetOfferingStatus.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#getofferingstatuspaginator)
        """


if TYPE_CHECKING:
    _ListArtifactsPaginatorBase = AioPaginator[ListArtifactsResultTypeDef]
else:
    _ListArtifactsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListArtifactsPaginator(_ListArtifactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListArtifacts.html#DeviceFarm.Paginator.ListArtifacts)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listartifactspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListArtifactsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListArtifactsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListArtifacts.html#DeviceFarm.Paginator.ListArtifacts.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listartifactspaginator)
        """


if TYPE_CHECKING:
    _ListDeviceInstancesPaginatorBase = AioPaginator[ListDeviceInstancesResultTypeDef]
else:
    _ListDeviceInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDeviceInstancesPaginator(_ListDeviceInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDeviceInstances.html#DeviceFarm.Paginator.ListDeviceInstances)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdeviceinstancespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDeviceInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDeviceInstancesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDeviceInstances.html#DeviceFarm.Paginator.ListDeviceInstances.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdeviceinstancespaginator)
        """


if TYPE_CHECKING:
    _ListDevicePoolsPaginatorBase = AioPaginator[ListDevicePoolsResultTypeDef]
else:
    _ListDevicePoolsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDevicePoolsPaginator(_ListDevicePoolsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevicePools.html#DeviceFarm.Paginator.ListDevicePools)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicepoolspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicePoolsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevicePoolsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevicePools.html#DeviceFarm.Paginator.ListDevicePools.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicepoolspaginator)
        """


if TYPE_CHECKING:
    _ListDevicesPaginatorBase = AioPaginator[ListDevicesResultTypeDef]
else:
    _ListDevicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDevicesPaginator(_ListDevicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevices.html#DeviceFarm.Paginator.ListDevices)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDevicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDevicesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListDevices.html#DeviceFarm.Paginator.ListDevices.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listdevicespaginator)
        """


if TYPE_CHECKING:
    _ListInstanceProfilesPaginatorBase = AioPaginator[ListInstanceProfilesResultTypeDef]
else:
    _ListInstanceProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListInstanceProfilesPaginator(_ListInstanceProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListInstanceProfiles.html#DeviceFarm.Paginator.ListInstanceProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listinstanceprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListInstanceProfiles.html#DeviceFarm.Paginator.ListInstanceProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listinstanceprofilespaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResultTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListJobs.html#DeviceFarm.Paginator.ListJobs)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListJobs.html#DeviceFarm.Paginator.ListJobs.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListNetworkProfilesPaginatorBase = AioPaginator[ListNetworkProfilesResultTypeDef]
else:
    _ListNetworkProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNetworkProfilesPaginator(_ListNetworkProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListNetworkProfiles.html#DeviceFarm.Paginator.ListNetworkProfiles)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listnetworkprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNetworkProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNetworkProfilesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListNetworkProfiles.html#DeviceFarm.Paginator.ListNetworkProfiles.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listnetworkprofilespaginator)
        """


if TYPE_CHECKING:
    _ListOfferingPromotionsPaginatorBase = AioPaginator[ListOfferingPromotionsResultTypeDef]
else:
    _ListOfferingPromotionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOfferingPromotionsPaginator(_ListOfferingPromotionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingPromotions.html#DeviceFarm.Paginator.ListOfferingPromotions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingpromotionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOfferingPromotionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOfferingPromotionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingPromotions.html#DeviceFarm.Paginator.ListOfferingPromotions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingpromotionspaginator)
        """


if TYPE_CHECKING:
    _ListOfferingTransactionsPaginatorBase = AioPaginator[ListOfferingTransactionsResultTypeDef]
else:
    _ListOfferingTransactionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOfferingTransactionsPaginator(_ListOfferingTransactionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingTransactions.html#DeviceFarm.Paginator.ListOfferingTransactions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingtransactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOfferingTransactionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOfferingTransactionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferingTransactions.html#DeviceFarm.Paginator.ListOfferingTransactions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingtransactionspaginator)
        """


if TYPE_CHECKING:
    _ListOfferingsPaginatorBase = AioPaginator[ListOfferingsResultTypeDef]
else:
    _ListOfferingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOfferingsPaginator(_ListOfferingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferings.html#DeviceFarm.Paginator.ListOfferings)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOfferingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOfferingsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListOfferings.html#DeviceFarm.Paginator.ListOfferings.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listofferingspaginator)
        """


if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsResultTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListProjects.html#DeviceFarm.Paginator.ListProjects)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listprojectspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListProjects.html#DeviceFarm.Paginator.ListProjects.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listprojectspaginator)
        """


if TYPE_CHECKING:
    _ListRemoteAccessSessionsPaginatorBase = AioPaginator[ListRemoteAccessSessionsResultTypeDef]
else:
    _ListRemoteAccessSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRemoteAccessSessionsPaginator(_ListRemoteAccessSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRemoteAccessSessions.html#DeviceFarm.Paginator.ListRemoteAccessSessions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listremoteaccesssessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRemoteAccessSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRemoteAccessSessionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRemoteAccessSessions.html#DeviceFarm.Paginator.ListRemoteAccessSessions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listremoteaccesssessionspaginator)
        """


if TYPE_CHECKING:
    _ListRunsPaginatorBase = AioPaginator[ListRunsResultTypeDef]
else:
    _ListRunsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRunsPaginator(_ListRunsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRuns.html#DeviceFarm.Paginator.ListRuns)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listrunspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRunsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRunsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListRuns.html#DeviceFarm.Paginator.ListRuns.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listrunspaginator)
        """


if TYPE_CHECKING:
    _ListSamplesPaginatorBase = AioPaginator[ListSamplesResultTypeDef]
else:
    _ListSamplesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSamplesPaginator(_ListSamplesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSamples.html#DeviceFarm.Paginator.ListSamples)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsamplespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSamplesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSamplesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSamples.html#DeviceFarm.Paginator.ListSamples.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsamplespaginator)
        """


if TYPE_CHECKING:
    _ListSuitesPaginatorBase = AioPaginator[ListSuitesResultTypeDef]
else:
    _ListSuitesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSuitesPaginator(_ListSuitesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSuites.html#DeviceFarm.Paginator.ListSuites)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsuitespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSuitesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSuitesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListSuites.html#DeviceFarm.Paginator.ListSuites.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listsuitespaginator)
        """


if TYPE_CHECKING:
    _ListTestsPaginatorBase = AioPaginator[ListTestsResultTypeDef]
else:
    _ListTestsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTestsPaginator(_ListTestsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListTests.html#DeviceFarm.Paginator.ListTests)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listtestspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTestsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTestsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListTests.html#DeviceFarm.Paginator.ListTests.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listtestspaginator)
        """


if TYPE_CHECKING:
    _ListUniqueProblemsPaginatorBase = AioPaginator[ListUniqueProblemsResultTypeDef]
else:
    _ListUniqueProblemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUniqueProblemsPaginator(_ListUniqueProblemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUniqueProblems.html#DeviceFarm.Paginator.ListUniqueProblems)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuniqueproblemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUniqueProblemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUniqueProblemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUniqueProblems.html#DeviceFarm.Paginator.ListUniqueProblems.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuniqueproblemspaginator)
        """


if TYPE_CHECKING:
    _ListUploadsPaginatorBase = AioPaginator[ListUploadsResultTypeDef]
else:
    _ListUploadsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListUploadsPaginator(_ListUploadsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUploads.html#DeviceFarm.Paginator.ListUploads)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuploadspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUploadsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUploadsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListUploads.html#DeviceFarm.Paginator.ListUploads.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listuploadspaginator)
        """


if TYPE_CHECKING:
    _ListVPCEConfigurationsPaginatorBase = AioPaginator[ListVPCEConfigurationsResultTypeDef]
else:
    _ListVPCEConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListVPCEConfigurationsPaginator(_ListVPCEConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListVPCEConfigurations.html#DeviceFarm.Paginator.ListVPCEConfigurations)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listvpceconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListVPCEConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListVPCEConfigurationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/devicefarm/paginator/ListVPCEConfigurations.html#DeviceFarm.Paginator.ListVPCEConfigurations.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_devicefarm/paginators/#listvpceconfigurationspaginator)
        """
