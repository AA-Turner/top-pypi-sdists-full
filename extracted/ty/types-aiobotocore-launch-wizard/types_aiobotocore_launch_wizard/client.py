"""
Type annotations for launch-wizard service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_launch_wizard.client import LaunchWizardClient

    session = get_session()
    async with session.create_client("launch-wizard") as client:
        client: LaunchWizardClient
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListDeploymentEventsPaginator,
    ListDeploymentPatternVersionsPaginator,
    ListDeploymentsPaginator,
    ListWorkloadDeploymentPatternsPaginator,
    ListWorkloadsPaginator,
)
from .type_defs import (
    CreateDeploymentInputTypeDef,
    CreateDeploymentOutputTypeDef,
    DeleteDeploymentInputTypeDef,
    DeleteDeploymentOutputTypeDef,
    GetDeploymentInputTypeDef,
    GetDeploymentOutputTypeDef,
    GetDeploymentPatternVersionInputTypeDef,
    GetDeploymentPatternVersionOutputTypeDef,
    GetWorkloadDeploymentPatternInputTypeDef,
    GetWorkloadDeploymentPatternOutputTypeDef,
    GetWorkloadInputTypeDef,
    GetWorkloadOutputTypeDef,
    ListDeploymentEventsInputTypeDef,
    ListDeploymentEventsOutputTypeDef,
    ListDeploymentPatternVersionsInputTypeDef,
    ListDeploymentPatternVersionsOutputTypeDef,
    ListDeploymentsInputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListWorkloadDeploymentPatternsInputTypeDef,
    ListWorkloadDeploymentPatternsOutputTypeDef,
    ListWorkloadsInputTypeDef,
    ListWorkloadsOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateDeploymentInputTypeDef,
    UpdateDeploymentOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("LaunchWizardClient",)


class Exceptions(BaseClientExceptions):
    ClientError: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceLimitException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class LaunchWizardClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LaunchWizardClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#generate_presigned_url)
        """

    async def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentInputTypeDef]
    ) -> CreateDeploymentOutputTypeDef:
        """
        Creates a deployment for the given workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/create_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#create_deployment)
        """

    async def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentInputTypeDef]
    ) -> DeleteDeploymentOutputTypeDef:
        """
        Deletes a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/delete_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#delete_deployment)
        """

    async def get_deployment(
        self, **kwargs: Unpack[GetDeploymentInputTypeDef]
    ) -> GetDeploymentOutputTypeDef:
        """
        Returns information about the deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_deployment)
        """

    async def get_deployment_pattern_version(
        self, **kwargs: Unpack[GetDeploymentPatternVersionInputTypeDef]
    ) -> GetDeploymentPatternVersionOutputTypeDef:
        """
        Returns information about a deployment pattern version.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_deployment_pattern_version.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_deployment_pattern_version)
        """

    async def get_workload(
        self, **kwargs: Unpack[GetWorkloadInputTypeDef]
    ) -> GetWorkloadOutputTypeDef:
        """
        Returns information about a workload.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_workload.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_workload)
        """

    async def get_workload_deployment_pattern(
        self, **kwargs: Unpack[GetWorkloadDeploymentPatternInputTypeDef]
    ) -> GetWorkloadDeploymentPatternOutputTypeDef:
        """
        Returns details for a given workload and deployment pattern, including the
        available specifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_workload_deployment_pattern.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_workload_deployment_pattern)
        """

    async def list_deployment_events(
        self, **kwargs: Unpack[ListDeploymentEventsInputTypeDef]
    ) -> ListDeploymentEventsOutputTypeDef:
        """
        Lists the events of a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_deployment_events.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#list_deployment_events)
        """

    async def list_deployment_pattern_versions(
        self, **kwargs: Unpack[ListDeploymentPatternVersionsInputTypeDef]
    ) -> ListDeploymentPatternVersionsOutputTypeDef:
        """
        Lists the deployment pattern versions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_deployment_pattern_versions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#list_deployment_pattern_versions)
        """

    async def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsInputTypeDef]
    ) -> ListDeploymentsOutputTypeDef:
        """
        Lists the deployments that have been created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_deployments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#list_deployments)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#list_tags_for_resource)
        """

    async def list_workload_deployment_patterns(
        self, **kwargs: Unpack[ListWorkloadDeploymentPatternsInputTypeDef]
    ) -> ListWorkloadDeploymentPatternsOutputTypeDef:
        """
        Lists the workload deployment patterns for a given workload name.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_workload_deployment_patterns.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#list_workload_deployment_patterns)
        """

    async def list_workloads(
        self, **kwargs: Unpack[ListWorkloadsInputTypeDef]
    ) -> ListWorkloadsOutputTypeDef:
        """
        Lists the available workload names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/list_workloads.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#list_workloads)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds the specified tags to the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#untag_resource)
        """

    async def update_deployment(
        self, **kwargs: Unpack[UpdateDeploymentInputTypeDef]
    ) -> UpdateDeploymentOutputTypeDef:
        """
        Updates a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/update_deployment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#update_deployment)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployment_events"]
    ) -> ListDeploymentEventsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployment_pattern_versions"]
    ) -> ListDeploymentPatternVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workload_deployment_patterns"]
    ) -> ListWorkloadDeploymentPatternsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_workloads"]
    ) -> ListWorkloadsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/launch-wizard.html#LaunchWizard.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_launch_wizard/client/)
        """
