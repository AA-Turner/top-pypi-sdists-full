"""
Type annotations for arc-region-switch service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_arc_region_switch.client import ARCRegionswitchClient
    from types_aiobotocore_arc_region_switch.waiter import (
        PlanEvaluationStatusPassedWaiter,
        PlanExecutionCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("arc-region-switch") as client:
        client: ARCRegionswitchClient

        plan_evaluation_status_passed_waiter: PlanEvaluationStatusPassedWaiter = client.get_waiter("plan_evaluation_status_passed")
        plan_execution_completed_waiter: PlanExecutionCompletedWaiter = client.get_waiter("plan_execution_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import GetPlanEvaluationStatusRequestWaitTypeDef, GetPlanExecutionRequestWaitTypeDef

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("PlanEvaluationStatusPassedWaiter", "PlanExecutionCompletedWaiter")

class PlanEvaluationStatusPassedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/waiter/PlanEvaluationStatusPassed.html#ARCRegionswitch.Waiter.PlanEvaluationStatusPassed)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/waiters/#planevaluationstatuspassedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPlanEvaluationStatusRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/waiter/PlanEvaluationStatusPassed.html#ARCRegionswitch.Waiter.PlanEvaluationStatusPassed.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/waiters/#planevaluationstatuspassedwaiter)
        """

class PlanExecutionCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/waiter/PlanExecutionCompleted.html#ARCRegionswitch.Waiter.PlanExecutionCompleted)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/waiters/#planexecutioncompletedwaiter)
    """
    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPlanExecutionRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/arc-region-switch/waiter/PlanExecutionCompleted.html#ARCRegionswitch.Waiter.PlanExecutionCompleted.wait)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_arc_region_switch/waiters/#planexecutioncompletedwaiter)
        """
