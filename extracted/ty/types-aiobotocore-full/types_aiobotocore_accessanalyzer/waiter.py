"""
Type annotations for accessanalyzer service client waiters.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_accessanalyzer.client import AccessAnalyzerClient
    from types_aiobotocore_accessanalyzer.waiter import (
        PolicyPreviewConfigurationActiveWaiter,
        PolicyPreviewJobCompletedWaiter,
    )

    session = get_session()
    async with session.create_client("accessanalyzer") as client:
        client: AccessAnalyzerClient

        policy_preview_configuration_active_waiter: PolicyPreviewConfigurationActiveWaiter = client.get_waiter("policy_preview_configuration_active")
        policy_preview_job_completed_waiter: PolicyPreviewJobCompletedWaiter = client.get_waiter("policy_preview_job_completed")
    ```
"""

from __future__ import annotations

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetPolicyPreviewConfigurationRequestTypeDef,
    GetPolicyPreviewJobRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("PolicyPreviewConfigurationActiveWaiter", "PolicyPreviewJobCompletedWaiter")


class PolicyPreviewConfigurationActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewConfigurationActive.html#AccessAnalyzer.Waiter.PolicyPreviewConfigurationActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/waiters/#policypreviewconfigurationactivewaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyPreviewConfigurationRequestTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewConfigurationActive.html#AccessAnalyzer.Waiter.PolicyPreviewConfigurationActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/waiters/#policypreviewconfigurationactivewaiter)
        """


class PolicyPreviewJobCompletedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewJobCompleted.html#AccessAnalyzer.Waiter.PolicyPreviewJobCompleted)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/waiters/#policypreviewjobcompletedwaiter)
    """

    async def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyPreviewJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewJobCompleted.html#AccessAnalyzer.Waiter.PolicyPreviewJobCompleted.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_accessanalyzer/waiters/#policypreviewjobcompletedwaiter)
        """
