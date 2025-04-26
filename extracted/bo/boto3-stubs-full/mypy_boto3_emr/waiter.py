"""
Type annotations for emr service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_emr.client import EMRClient
    from mypy_boto3_emr.waiter import (
        ClusterRunningWaiter,
        ClusterTerminatedWaiter,
        StepCompleteWaiter,
    )

    session = Session()
    client: EMRClient = session.client("emr")

    cluster_running_waiter: ClusterRunningWaiter = client.get_waiter("cluster_running")
    cluster_terminated_waiter: ClusterTerminatedWaiter = client.get_waiter("cluster_terminated")
    step_complete_waiter: StepCompleteWaiter = client.get_waiter("step_complete")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    DescribeClusterInputWaitExtraTypeDef,
    DescribeClusterInputWaitTypeDef,
    DescribeStepInputWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("ClusterRunningWaiter", "ClusterTerminatedWaiter", "StepCompleteWaiter")


class ClusterRunningWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterRunning.html#EMR.Waiter.ClusterRunning)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/#clusterrunningwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterRunning.html#EMR.Waiter.ClusterRunning.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/#clusterrunningwaiter)
        """


class ClusterTerminatedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterTerminated.html#EMR.Waiter.ClusterTerminated)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/#clusterterminatedwaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeClusterInputWaitExtraTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/ClusterTerminated.html#EMR.Waiter.ClusterTerminated.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/#clusterterminatedwaiter)
        """


class StepCompleteWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/StepComplete.html#EMR.Waiter.StepComplete)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/#stepcompletewaiter)
    """

    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStepInputWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/emr/waiter/StepComplete.html#EMR.Waiter.StepComplete.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_emr/waiters/#stepcompletewaiter)
        """
