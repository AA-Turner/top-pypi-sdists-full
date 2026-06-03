"""
Type annotations for sagemakerjobruntime service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemakerjobruntime.client import SagemakerJobRuntimeServiceClient

    session = Session()
    client: SagemakerJobRuntimeServiceClient = session.client("sagemakerjobruntime")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    CompleteRolloutRequestTypeDef,
    SampleRequestTypeDef,
    SampleResponseTypeDef,
    SampleWithResponseStreamRequestTypeDef,
    SampleWithResponseStreamResponseTypeDef,
    UpdateRewardRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("SagemakerJobRuntimeServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServiceError: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SagemakerJobRuntimeServiceClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime.html#SagemakerJobRuntimeService.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SagemakerJobRuntimeServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime.html#SagemakerJobRuntimeService.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#generate_presigned_url)
        """

    def complete_rollout(self, **kwargs: Unpack[CompleteRolloutRequestTypeDef]) -> dict[str, Any]:
        """
        Marks a rollout as complete, indicating that no further turns will be appended
        to the trajectory.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime/client/complete_rollout.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#complete_rollout)
        """

    def sample(self, **kwargs: Unpack[SampleRequestTypeDef]) -> SampleResponseTypeDef:
        """
        Sends an inference request to the model during a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime/client/sample.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#sample)
        """

    def sample_with_response_stream(
        self, **kwargs: Unpack[SampleWithResponseStreamRequestTypeDef]
    ) -> SampleWithResponseStreamResponseTypeDef:
        """
        Sends a streaming inference request to the model during a job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime/client/sample_with_response_stream.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#sample_with_response_stream)
        """

    def update_reward(self, **kwargs: Unpack[UpdateRewardRequestTypeDef]) -> dict[str, Any]:
        """
        Updates the reward values for a trajectory and transitions it to
        reward-received status, signaling that it is eligible for processing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sagemakerjobruntime/client/update_reward.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_sagemakerjobruntime/client/#update_reward)
        """
