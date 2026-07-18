"""
Type annotations for resiliencehubv2 service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_resiliencehubv2.client import ResilienceHubV2Client
    from types_aiobotocore_resiliencehubv2.waiter import (
        FailureModeAssessmentSuccessWaiter,
        ReportSucceededWaiter,
        ServiceAssessmentCompletedWaiter,
        ServiceResourceDiscoveryCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("resiliencehubv2") as client:
        client: ResilienceHubV2Client

        failure_mode_assessment_success_waiter: FailureModeAssessmentSuccessWaiter = client.get_waiter("failure_mode_assessment_success")
        report_succeeded_waiter: ReportSucceededWaiter = client.get_waiter("report_succeeded")
        service_assessment_completed_waiter: ServiceAssessmentCompletedWaiter = client.get_waiter("service_assessment_completed")
        service_resource_discovery_completed_waiter: ServiceResourceDiscoveryCompletedWaiter = client.get_waiter("service_resource_discovery_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetServiceRequestWaitExtraTypeDef,
    GetServiceRequestWaitTypeDef,
    ListFailureModeAssessmentsRequestWaitTypeDef,
    ListReportsRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "FailureModeAssessmentSuccessWaiter",
    "ReportSucceededWaiter",
    "ServiceAssessmentCompletedWaiter",
    "ServiceResourceDiscoveryCompletedWaiter",
)

class FailureModeAssessmentSuccessWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/FailureModeAssessmentSuccess.html#ResilienceHubV2.Waiter.FailureModeAssessmentSuccess)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#failuremodeassessmentsuccesswaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListFailureModeAssessmentsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/FailureModeAssessmentSuccess.html#ResilienceHubV2.Waiter.FailureModeAssessmentSuccess.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#failuremodeassessmentsuccesswaiter)
        """

class ReportSucceededWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ReportSucceeded.html#ResilienceHubV2.Waiter.ReportSucceeded)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#reportsucceededwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ReportSucceeded.html#ResilienceHubV2.Waiter.ReportSucceeded.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#reportsucceededwaiter)
        """

class ServiceAssessmentCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceAssessmentCompleted.html#ResilienceHubV2.Waiter.ServiceAssessmentCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#serviceassessmentcompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceAssessmentCompleted.html#ResilienceHubV2.Waiter.ServiceAssessmentCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#serviceassessmentcompletedwaiter)
        """

class ServiceResourceDiscoveryCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceResourceDiscoveryCompleted.html#ResilienceHubV2.Waiter.ServiceResourceDiscoveryCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#serviceresourcediscoverycompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceResourceDiscoveryCompleted.html#ResilienceHubV2.Waiter.ServiceResourceDiscoveryCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_resiliencehubv2/waiters/#serviceresourcediscoverycompletedwaiter)
        """
