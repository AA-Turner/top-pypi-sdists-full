"""
Type annotations for accessanalyzer service client waiters.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/waiters/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_accessanalyzer.client import AccessAnalyzerClient
    from mypy_boto3_accessanalyzer.waiter import (
        PolicyPreviewConfigurationActiveWaiter,
        PolicyPreviewJobCompletedWaiter,
    )

    session = Session()
    client: AccessAnalyzerClient = session.client("accessanalyzer")

    policy_preview_configuration_active_waiter: PolicyPreviewConfigurationActiveWaiter = client.get_waiter("policy_preview_configuration_active")
    policy_preview_job_completed_waiter: PolicyPreviewJobCompletedWaiter = client.get_waiter("policy_preview_job_completed")
    ```
"""

from __future__ import annotations

import sys

from botocore.waiter import Waiter

from .type_defs import (
    GetPolicyPreviewConfigurationRequestTypeDef,
    GetPolicyPreviewJobRequestWaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("PolicyPreviewConfigurationActiveWaiter", "PolicyPreviewJobCompletedWaiter")

class PolicyPreviewConfigurationActiveWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewConfigurationActive.html#AccessAnalyzer.Waiter.PolicyPreviewConfigurationActive)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/waiters/#policypreviewconfigurationactivewaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyPreviewConfigurationRequestTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewConfigurationActive.html#AccessAnalyzer.Waiter.PolicyPreviewConfigurationActive.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/waiters/#policypreviewconfigurationactivewaiter)
        """

class PolicyPreviewJobCompletedWaiter(Waiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewJobCompleted.html#AccessAnalyzer.Waiter.PolicyPreviewJobCompleted)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/waiters/#policypreviewjobcompletedwaiter)
    """
    def wait(  # type: ignore[override]
        self, **kwargs: Unpack[GetPolicyPreviewJobRequestWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/accessanalyzer/waiter/PolicyPreviewJobCompleted.html#AccessAnalyzer.Waiter.PolicyPreviewJobCompleted.wait)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_accessanalyzer/waiters/#policypreviewjobcompletedwaiter)
        """
