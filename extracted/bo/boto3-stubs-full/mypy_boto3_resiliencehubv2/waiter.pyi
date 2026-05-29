"""
Type annotations for resiliencehubv2 service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_resiliencehubv2.client import ResilienceHubV2Client
    from mypy_boto3_resiliencehubv2.waiter import (
        FailureModeAssessmentSuccessWaiter,
        ReportSucceededWaiter,
        ServiceAssessmentCompletedWaiter,
        ServiceResourceDiscoveryCompletedWaiter,
    )

    session = Session()
    client: ResilienceHubV2Client = session.client("resiliencehubv2")

    failure_mode_assessment_success_waiter: FailureModeAssessmentSuccessWaiter = client.get_waiter("failure_mode_assessment_success")
    report_succeeded_waiter: ReportSucceededWaiter = client.get_waiter("report_succeeded")
    service_assessment_completed_waiter: ServiceAssessmentCompletedWaiter = client.get_waiter("service_assessment_completed")
    service_resource_discovery_completed_waiter: ServiceResourceDiscoveryCompletedWaiter = client.get_waiter("service_resource_discovery_completed")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

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

class FailureModeAssessmentSuccessWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/FailureModeAssessmentSuccess.html#ResilienceHubV2.Waiter.FailureModeAssessmentSuccess)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#failuremodeassessmentsuccesswaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListFailureModeAssessmentsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/FailureModeAssessmentSuccess.html#ResilienceHubV2.Waiter.FailureModeAssessmentSuccess.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#failuremodeassessmentsuccesswaiter)
        """

class ReportSucceededWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ReportSucceeded.html#ResilienceHubV2.Waiter.ReportSucceeded)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#reportsucceededwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ReportSucceeded.html#ResilienceHubV2.Waiter.ReportSucceeded.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#reportsucceededwaiter)
        """

class ServiceAssessmentCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceAssessmentCompleted.html#ResilienceHubV2.Waiter.ServiceAssessmentCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#serviceassessmentcompletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceAssessmentCompleted.html#ResilienceHubV2.Waiter.ServiceAssessmentCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#serviceassessmentcompletedwaiter)
        """

class ServiceResourceDiscoveryCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceResourceDiscoveryCompleted.html#ResilienceHubV2.Waiter.ServiceResourceDiscoveryCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#serviceresourcediscoverycompletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetServiceRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/resiliencehubv2/waiter/ServiceResourceDiscoveryCompleted.html#ResilienceHubV2.Waiter.ServiceResourceDiscoveryCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_resiliencehubv2/waiters/#serviceresourcediscoverycompletedwaiter)
        """
