"""
Type annotations for observabilityadmin service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient

    session = get_session()
    async with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListResourceTelemetryForOrganizationPaginator, ListResourceTelemetryPaginator
from .type_defs import (
    EmptyResponseMetadataTypeDef,
    GetTelemetryEvaluationStatusForOrganizationOutputTypeDef,
    GetTelemetryEvaluationStatusOutputTypeDef,
    ListResourceTelemetryForOrganizationInputTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputTypeDef,
    ListResourceTelemetryOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("CloudWatchObservabilityAdminServiceClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class CloudWatchObservabilityAdminServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchObservabilityAdminServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#generate_presigned_url)
        """

    async def get_telemetry_evaluation_status(self) -> GetTelemetryEvaluationStatusOutputTypeDef:
        """
        Returns the current onboarding status of the telemetry config feature,
        including the status of the feature and reason the feature failed to start or
        stop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_evaluation_status.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_evaluation_status)
        """

    async def get_telemetry_evaluation_status_for_organization(
        self,
    ) -> GetTelemetryEvaluationStatusForOrganizationOutputTypeDef:
        """
        This returns the onboarding status of the telemetry configuration feature for
        the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_evaluation_status_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_evaluation_status_for_organization)
        """

    async def list_resource_telemetry(
        self, **kwargs: Unpack[ListResourceTelemetryInputTypeDef]
    ) -> ListResourceTelemetryOutputTypeDef:
        """
        Returns a list of telemetry configurations for AWS resources supported by
        telemetry config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_resource_telemetry.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_resource_telemetry)
        """

    async def list_resource_telemetry_for_organization(
        self, **kwargs: Unpack[ListResourceTelemetryForOrganizationInputTypeDef]
    ) -> ListResourceTelemetryForOrganizationOutputTypeDef:
        """
        Returns a list of telemetry configurations for AWS resources supported by
        telemetry config in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_resource_telemetry_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_resource_telemetry_for_organization)
        """

    async def start_telemetry_evaluation(self) -> EmptyResponseMetadataTypeDef:
        """
        This action begins onboarding onboarding the caller AWS account to the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_evaluation)
        """

    async def start_telemetry_evaluation_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        This actions begins onboarding the organization and all member accounts to the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_evaluation_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_evaluation_for_organization)
        """

    async def stop_telemetry_evaluation(self) -> EmptyResponseMetadataTypeDef:
        """
        This action begins offboarding the caller AWS account from the telemetry config
        feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_evaluation.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_evaluation)
        """

    async def stop_telemetry_evaluation_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        This action offboards the Organization of the caller AWS account from thef
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_evaluation_for_organization.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_evaluation_for_organization)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_telemetry_for_organization"]
    ) -> ListResourceTelemetryForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_telemetry"]
    ) -> ListResourceTelemetryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
        """
