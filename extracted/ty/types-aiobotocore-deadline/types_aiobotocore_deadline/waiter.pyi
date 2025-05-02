"""
Type annotations for deadline service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_deadline.client import DeadlineCloudClient
    from types_aiobotocore_deadline.waiter import (
        FleetActiveWaiter,
        JobCreateCompleteWaiter,
        LicenseEndpointDeletedWaiter,
        LicenseEndpointValidWaiter,
        QueueFleetAssociationStoppedWaiter,
        QueueLimitAssociationStoppedWaiter,
        QueueSchedulingBlockedWaiter,
        QueueSchedulingWaiter,
    )

    session = get_session()
    async with session.create_client("deadline") as client:
        client: DeadlineCloudClient

        fleet_active_waiter: FleetActiveWaiter = client.get_waiter("fleet_active")
        job_create_complete_waiter: JobCreateCompleteWaiter = client.get_waiter("job_create_complete")
        license_endpoint_deleted_waiter: LicenseEndpointDeletedWaiter = client.get_waiter("license_endpoint_deleted")
        license_endpoint_valid_waiter: LicenseEndpointValidWaiter = client.get_waiter("license_endpoint_valid")
        queue_fleet_association_stopped_waiter: QueueFleetAssociationStoppedWaiter = client.get_waiter("queue_fleet_association_stopped")
        queue_limit_association_stopped_waiter: QueueLimitAssociationStoppedWaiter = client.get_waiter("queue_limit_association_stopped")
        queue_scheduling_blocked_waiter: QueueSchedulingBlockedWaiter = client.get_waiter("queue_scheduling_blocked")
        queue_scheduling_waiter: QueueSchedulingWaiter = client.get_waiter("queue_scheduling")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetFleetRequestWaitTypeDef,
    GetJobRequestWaitTypeDef,
    GetLicenseEndpointRequestWaitExtraTypeDef,
    GetLicenseEndpointRequestWaitTypeDef,
    GetQueueFleetAssociationRequestWaitTypeDef,
    GetQueueLimitAssociationRequestWaitTypeDef,
    GetQueueRequestWaitExtraTypeDef,
    GetQueueRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "FleetActiveWaiter",
    "JobCreateCompleteWaiter",
    "LicenseEndpointDeletedWaiter",
    "LicenseEndpointValidWaiter",
    "QueueFleetAssociationStoppedWaiter",
    "QueueLimitAssociationStoppedWaiter",
    "QueueSchedulingBlockedWaiter",
    "QueueSchedulingWaiter",
)

class FleetActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/FleetActive.html#DeadlineCloud.Waiter.FleetActive)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#fleetactivewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetFleetRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/FleetActive.html#DeadlineCloud.Waiter.FleetActive.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#fleetactivewaiter)
        """

class JobCreateCompleteWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/JobCreateComplete.html#DeadlineCloud.Waiter.JobCreateComplete)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#jobcreatecompletewaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/JobCreateComplete.html#DeadlineCloud.Waiter.JobCreateComplete.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#jobcreatecompletewaiter)
        """

class LicenseEndpointDeletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointDeleted.html#DeadlineCloud.Waiter.LicenseEndpointDeleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointdeletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLicenseEndpointRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointDeleted.html#DeadlineCloud.Waiter.LicenseEndpointDeleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointdeletedwaiter)
        """

class LicenseEndpointValidWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointValid.html#DeadlineCloud.Waiter.LicenseEndpointValid)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointvalidwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetLicenseEndpointRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/LicenseEndpointValid.html#DeadlineCloud.Waiter.LicenseEndpointValid.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#licenseendpointvalidwaiter)
        """

class QueueFleetAssociationStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueFleetAssociationStopped.html#DeadlineCloud.Waiter.QueueFleetAssociationStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queuefleetassociationstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueueFleetAssociationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueFleetAssociationStopped.html#DeadlineCloud.Waiter.QueueFleetAssociationStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queuefleetassociationstoppedwaiter)
        """

class QueueLimitAssociationStoppedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueLimitAssociationStopped.html#DeadlineCloud.Waiter.QueueLimitAssociationStopped)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queuelimitassociationstoppedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueueLimitAssociationRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueLimitAssociationStopped.html#DeadlineCloud.Waiter.QueueLimitAssociationStopped.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queuelimitassociationstoppedwaiter)
        """

class QueueSchedulingBlockedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueSchedulingBlocked.html#DeadlineCloud.Waiter.QueueSchedulingBlocked)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingblockedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueueRequestWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueSchedulingBlocked.html#DeadlineCloud.Waiter.QueueSchedulingBlocked.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingblockedwaiter)
        """

class QueueSchedulingWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueScheduling.html#DeadlineCloud.Waiter.QueueScheduling)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetQueueRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/deadline/waiter/QueueScheduling.html#DeadlineCloud.Waiter.QueueScheduling.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_deadline/waiters/#queueschedulingwaiter)
        """
