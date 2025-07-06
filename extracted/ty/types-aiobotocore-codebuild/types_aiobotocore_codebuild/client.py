"""
Type annotations for codebuild service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codebuild.client import CodeBuildClient

    session = get_session()
    async with session.create_client("codebuild") as client:
        client: CodeBuildClient
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

from .paginator import (
    DescribeCodeCoveragesPaginator,
    DescribeTestCasesPaginator,
    ListBuildBatchesForProjectPaginator,
    ListBuildBatchesPaginator,
    ListBuildsForProjectPaginator,
    ListBuildsPaginator,
    ListCommandExecutionsForSandboxPaginator,
    ListProjectsPaginator,
    ListReportGroupsPaginator,
    ListReportsForReportGroupPaginator,
    ListReportsPaginator,
    ListSandboxesForProjectPaginator,
    ListSandboxesPaginator,
    ListSharedProjectsPaginator,
    ListSharedReportGroupsPaginator,
)
from .type_defs import (
    BatchDeleteBuildsInputTypeDef,
    BatchDeleteBuildsOutputTypeDef,
    BatchGetBuildBatchesInputTypeDef,
    BatchGetBuildBatchesOutputTypeDef,
    BatchGetBuildsInputTypeDef,
    BatchGetBuildsOutputTypeDef,
    BatchGetCommandExecutionsInputTypeDef,
    BatchGetCommandExecutionsOutputTypeDef,
    BatchGetFleetsInputTypeDef,
    BatchGetFleetsOutputTypeDef,
    BatchGetProjectsInputTypeDef,
    BatchGetProjectsOutputTypeDef,
    BatchGetReportGroupsInputTypeDef,
    BatchGetReportGroupsOutputTypeDef,
    BatchGetReportsInputTypeDef,
    BatchGetReportsOutputTypeDef,
    BatchGetSandboxesInputTypeDef,
    BatchGetSandboxesOutputTypeDef,
    CreateFleetInputTypeDef,
    CreateFleetOutputTypeDef,
    CreateProjectInputTypeDef,
    CreateProjectOutputTypeDef,
    CreateReportGroupInputTypeDef,
    CreateReportGroupOutputTypeDef,
    CreateWebhookInputTypeDef,
    CreateWebhookOutputTypeDef,
    DeleteBuildBatchInputTypeDef,
    DeleteBuildBatchOutputTypeDef,
    DeleteFleetInputTypeDef,
    DeleteProjectInputTypeDef,
    DeleteReportGroupInputTypeDef,
    DeleteReportInputTypeDef,
    DeleteResourcePolicyInputTypeDef,
    DeleteSourceCredentialsInputTypeDef,
    DeleteSourceCredentialsOutputTypeDef,
    DeleteWebhookInputTypeDef,
    DescribeCodeCoveragesInputTypeDef,
    DescribeCodeCoveragesOutputTypeDef,
    DescribeTestCasesInputTypeDef,
    DescribeTestCasesOutputTypeDef,
    GetReportGroupTrendInputTypeDef,
    GetReportGroupTrendOutputTypeDef,
    GetResourcePolicyInputTypeDef,
    GetResourcePolicyOutputTypeDef,
    ImportSourceCredentialsInputTypeDef,
    ImportSourceCredentialsOutputTypeDef,
    InvalidateProjectCacheInputTypeDef,
    ListBuildBatchesForProjectInputTypeDef,
    ListBuildBatchesForProjectOutputTypeDef,
    ListBuildBatchesInputTypeDef,
    ListBuildBatchesOutputTypeDef,
    ListBuildsForProjectInputTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsInputTypeDef,
    ListBuildsOutputTypeDef,
    ListCommandExecutionsForSandboxInputTypeDef,
    ListCommandExecutionsForSandboxOutputTypeDef,
    ListCuratedEnvironmentImagesOutputTypeDef,
    ListFleetsInputTypeDef,
    ListFleetsOutputTypeDef,
    ListProjectsInputTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsInputTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupInputTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsInputTypeDef,
    ListReportsOutputTypeDef,
    ListSandboxesForProjectInputTypeDef,
    ListSandboxesForProjectOutputTypeDef,
    ListSandboxesInputTypeDef,
    ListSandboxesOutputTypeDef,
    ListSharedProjectsInputTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsInputTypeDef,
    ListSharedReportGroupsOutputTypeDef,
    ListSourceCredentialsOutputTypeDef,
    PutResourcePolicyInputTypeDef,
    PutResourcePolicyOutputTypeDef,
    RetryBuildBatchInputTypeDef,
    RetryBuildBatchOutputTypeDef,
    RetryBuildInputTypeDef,
    RetryBuildOutputTypeDef,
    StartBuildBatchInputTypeDef,
    StartBuildBatchOutputTypeDef,
    StartBuildInputTypeDef,
    StartBuildOutputTypeDef,
    StartCommandExecutionInputTypeDef,
    StartCommandExecutionOutputTypeDef,
    StartSandboxConnectionInputTypeDef,
    StartSandboxConnectionOutputTypeDef,
    StartSandboxInputTypeDef,
    StartSandboxOutputTypeDef,
    StopBuildBatchInputTypeDef,
    StopBuildBatchOutputTypeDef,
    StopBuildInputTypeDef,
    StopBuildOutputTypeDef,
    StopSandboxInputTypeDef,
    StopSandboxOutputTypeDef,
    UpdateFleetInputTypeDef,
    UpdateFleetOutputTypeDef,
    UpdateProjectInputTypeDef,
    UpdateProjectOutputTypeDef,
    UpdateProjectVisibilityInputTypeDef,
    UpdateProjectVisibilityOutputTypeDef,
    UpdateReportGroupInputTypeDef,
    UpdateReportGroupOutputTypeDef,
    UpdateWebhookInputTypeDef,
    UpdateWebhookOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("CodeBuildClient",)


class Exceptions(BaseClientExceptions):
    AccountLimitExceededException: Type[BotocoreClientError]
    AccountSuspendedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InvalidInputException: Type[BotocoreClientError]
    OAuthProviderException: Type[BotocoreClientError]
    ResourceAlreadyExistsException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]


class CodeBuildClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeBuildClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#generate_presigned_url)
        """

    async def batch_delete_builds(
        self, **kwargs: Unpack[BatchDeleteBuildsInputTypeDef]
    ) -> BatchDeleteBuildsOutputTypeDef:
        """
        Deletes one or more builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_delete_builds.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_delete_builds)
        """

    async def batch_get_build_batches(
        self, **kwargs: Unpack[BatchGetBuildBatchesInputTypeDef]
    ) -> BatchGetBuildBatchesOutputTypeDef:
        """
        Retrieves information about one or more batch builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_build_batches.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_build_batches)
        """

    async def batch_get_builds(
        self, **kwargs: Unpack[BatchGetBuildsInputTypeDef]
    ) -> BatchGetBuildsOutputTypeDef:
        """
        Gets information about one or more builds.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_builds.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_builds)
        """

    async def batch_get_command_executions(
        self, **kwargs: Unpack[BatchGetCommandExecutionsInputTypeDef]
    ) -> BatchGetCommandExecutionsOutputTypeDef:
        """
        Gets information about the command executions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_command_executions.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_command_executions)
        """

    async def batch_get_fleets(
        self, **kwargs: Unpack[BatchGetFleetsInputTypeDef]
    ) -> BatchGetFleetsOutputTypeDef:
        """
        Gets information about one or more compute fleets.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_fleets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_fleets)
        """

    async def batch_get_projects(
        self, **kwargs: Unpack[BatchGetProjectsInputTypeDef]
    ) -> BatchGetProjectsOutputTypeDef:
        """
        Gets information about one or more build projects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_projects.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_projects)
        """

    async def batch_get_report_groups(
        self, **kwargs: Unpack[BatchGetReportGroupsInputTypeDef]
    ) -> BatchGetReportGroupsOutputTypeDef:
        """
        Returns an array of report groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_report_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_report_groups)
        """

    async def batch_get_reports(
        self, **kwargs: Unpack[BatchGetReportsInputTypeDef]
    ) -> BatchGetReportsOutputTypeDef:
        """
        Returns an array of reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_reports.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_reports)
        """

    async def batch_get_sandboxes(
        self, **kwargs: Unpack[BatchGetSandboxesInputTypeDef]
    ) -> BatchGetSandboxesOutputTypeDef:
        """
        Gets information about the sandbox status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/batch_get_sandboxes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#batch_get_sandboxes)
        """

    async def create_fleet(
        self, **kwargs: Unpack[CreateFleetInputTypeDef]
    ) -> CreateFleetOutputTypeDef:
        """
        Creates a compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/create_fleet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_fleet)
        """

    async def create_project(
        self, **kwargs: Unpack[CreateProjectInputTypeDef]
    ) -> CreateProjectOutputTypeDef:
        """
        Creates a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/create_project.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_project)
        """

    async def create_report_group(
        self, **kwargs: Unpack[CreateReportGroupInputTypeDef]
    ) -> CreateReportGroupOutputTypeDef:
        """
        Creates a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/create_report_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_report_group)
        """

    async def create_webhook(
        self, **kwargs: Unpack[CreateWebhookInputTypeDef]
    ) -> CreateWebhookOutputTypeDef:
        """
        For an existing CodeBuild build project that has its source code stored in a
        GitHub or Bitbucket repository, enables CodeBuild to start rebuilding the
        source code every time a code change is pushed to the repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/create_webhook.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#create_webhook)
        """

    async def delete_build_batch(
        self, **kwargs: Unpack[DeleteBuildBatchInputTypeDef]
    ) -> DeleteBuildBatchOutputTypeDef:
        """
        Deletes a batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_build_batch.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_build_batch)
        """

    async def delete_fleet(self, **kwargs: Unpack[DeleteFleetInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_fleet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_fleet)
        """

    async def delete_project(self, **kwargs: Unpack[DeleteProjectInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_project.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_project)
        """

    async def delete_report(self, **kwargs: Unpack[DeleteReportInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_report.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_report)
        """

    async def delete_report_group(
        self, **kwargs: Unpack[DeleteReportGroupInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_report_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_report_group)
        """

    async def delete_resource_policy(
        self, **kwargs: Unpack[DeleteResourcePolicyInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a resource policy that is identified by its resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_resource_policy)
        """

    async def delete_source_credentials(
        self, **kwargs: Unpack[DeleteSourceCredentialsInputTypeDef]
    ) -> DeleteSourceCredentialsOutputTypeDef:
        """
        Deletes a set of GitHub, GitHub Enterprise, or Bitbucket source credentials.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_source_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_source_credentials)
        """

    async def delete_webhook(self, **kwargs: Unpack[DeleteWebhookInputTypeDef]) -> Dict[str, Any]:
        """
        For an existing CodeBuild build project that has its source code stored in a
        GitHub or Bitbucket repository, stops CodeBuild from rebuilding the source code
        every time a code change is pushed to the repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/delete_webhook.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#delete_webhook)
        """

    async def describe_code_coverages(
        self, **kwargs: Unpack[DescribeCodeCoveragesInputTypeDef]
    ) -> DescribeCodeCoveragesOutputTypeDef:
        """
        Retrieves one or more code coverage reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/describe_code_coverages.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#describe_code_coverages)
        """

    async def describe_test_cases(
        self, **kwargs: Unpack[DescribeTestCasesInputTypeDef]
    ) -> DescribeTestCasesOutputTypeDef:
        """
        Returns a list of details about test cases for a report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/describe_test_cases.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#describe_test_cases)
        """

    async def get_report_group_trend(
        self, **kwargs: Unpack[GetReportGroupTrendInputTypeDef]
    ) -> GetReportGroupTrendOutputTypeDef:
        """
        Analyzes and accumulates test report values for the specified test reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_report_group_trend.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_report_group_trend)
        """

    async def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Gets a resource policy that is identified by its resource ARN.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_resource_policy)
        """

    async def import_source_credentials(
        self, **kwargs: Unpack[ImportSourceCredentialsInputTypeDef]
    ) -> ImportSourceCredentialsOutputTypeDef:
        """
        Imports the source repository credentials for an CodeBuild project that has its
        source code stored in a GitHub, GitHub Enterprise, GitLab, GitLab Self Managed,
        or Bitbucket repository.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/import_source_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#import_source_credentials)
        """

    async def invalidate_project_cache(
        self, **kwargs: Unpack[InvalidateProjectCacheInputTypeDef]
    ) -> Dict[str, Any]:
        """
        Resets the cache for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/invalidate_project_cache.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#invalidate_project_cache)
        """

    async def list_build_batches(
        self, **kwargs: Unpack[ListBuildBatchesInputTypeDef]
    ) -> ListBuildBatchesOutputTypeDef:
        """
        Retrieves the identifiers of your build batches in the current region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_build_batches.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_build_batches)
        """

    async def list_build_batches_for_project(
        self, **kwargs: Unpack[ListBuildBatchesForProjectInputTypeDef]
    ) -> ListBuildBatchesForProjectOutputTypeDef:
        """
        Retrieves the identifiers of the build batches for a specific project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_build_batches_for_project.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_build_batches_for_project)
        """

    async def list_builds(
        self, **kwargs: Unpack[ListBuildsInputTypeDef]
    ) -> ListBuildsOutputTypeDef:
        """
        Gets a list of build IDs, with each build ID representing a single build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_builds.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_builds)
        """

    async def list_builds_for_project(
        self, **kwargs: Unpack[ListBuildsForProjectInputTypeDef]
    ) -> ListBuildsForProjectOutputTypeDef:
        """
        Gets a list of build identifiers for the specified build project, with each
        build identifier representing a single build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_builds_for_project.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_builds_for_project)
        """

    async def list_command_executions_for_sandbox(
        self, **kwargs: Unpack[ListCommandExecutionsForSandboxInputTypeDef]
    ) -> ListCommandExecutionsForSandboxOutputTypeDef:
        """
        Gets a list of command executions for a sandbox.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_command_executions_for_sandbox.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_command_executions_for_sandbox)
        """

    async def list_curated_environment_images(self) -> ListCuratedEnvironmentImagesOutputTypeDef:
        """
        Gets information about Docker images that are managed by CodeBuild.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_curated_environment_images.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_curated_environment_images)
        """

    async def list_fleets(
        self, **kwargs: Unpack[ListFleetsInputTypeDef]
    ) -> ListFleetsOutputTypeDef:
        """
        Gets a list of compute fleet names with each compute fleet name representing a
        single compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_fleets.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_fleets)
        """

    async def list_projects(
        self, **kwargs: Unpack[ListProjectsInputTypeDef]
    ) -> ListProjectsOutputTypeDef:
        """
        Gets a list of build project names, with each build project name representing a
        single build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_projects.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_projects)
        """

    async def list_report_groups(
        self, **kwargs: Unpack[ListReportGroupsInputTypeDef]
    ) -> ListReportGroupsOutputTypeDef:
        """
        Gets a list ARNs for the report groups in the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_report_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_report_groups)
        """

    async def list_reports(
        self, **kwargs: Unpack[ListReportsInputTypeDef]
    ) -> ListReportsOutputTypeDef:
        """
        Returns a list of ARNs for the reports in the current Amazon Web Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_reports.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_reports)
        """

    async def list_reports_for_report_group(
        self, **kwargs: Unpack[ListReportsForReportGroupInputTypeDef]
    ) -> ListReportsForReportGroupOutputTypeDef:
        """
        Returns a list of ARNs for the reports that belong to a
        <code>ReportGroup</code>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_reports_for_report_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_reports_for_report_group)
        """

    async def list_sandboxes(
        self, **kwargs: Unpack[ListSandboxesInputTypeDef]
    ) -> ListSandboxesOutputTypeDef:
        """
        Gets a list of sandboxes.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_sandboxes.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_sandboxes)
        """

    async def list_sandboxes_for_project(
        self, **kwargs: Unpack[ListSandboxesForProjectInputTypeDef]
    ) -> ListSandboxesForProjectOutputTypeDef:
        """
        Gets a list of sandboxes for a given project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_sandboxes_for_project.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_sandboxes_for_project)
        """

    async def list_shared_projects(
        self, **kwargs: Unpack[ListSharedProjectsInputTypeDef]
    ) -> ListSharedProjectsOutputTypeDef:
        """
        Gets a list of projects that are shared with other Amazon Web Services accounts
        or users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_shared_projects.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_shared_projects)
        """

    async def list_shared_report_groups(
        self, **kwargs: Unpack[ListSharedReportGroupsInputTypeDef]
    ) -> ListSharedReportGroupsOutputTypeDef:
        """
        Gets a list of report groups that are shared with other Amazon Web Services
        accounts or users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_shared_report_groups.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_shared_report_groups)
        """

    async def list_source_credentials(self) -> ListSourceCredentialsOutputTypeDef:
        """
        Returns a list of <code>SourceCredentialsInfo</code> objects.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/list_source_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#list_source_credentials)
        """

    async def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputTypeDef]
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Stores a resource policy for the ARN of a <code>Project</code> or
        <code>ReportGroup</code> object.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/put_resource_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#put_resource_policy)
        """

    async def retry_build(
        self, **kwargs: Unpack[RetryBuildInputTypeDef]
    ) -> RetryBuildOutputTypeDef:
        """
        Restarts a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/retry_build.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#retry_build)
        """

    async def retry_build_batch(
        self, **kwargs: Unpack[RetryBuildBatchInputTypeDef]
    ) -> RetryBuildBatchOutputTypeDef:
        """
        Restarts a failed batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/retry_build_batch.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#retry_build_batch)
        """

    async def start_build(
        self, **kwargs: Unpack[StartBuildInputTypeDef]
    ) -> StartBuildOutputTypeDef:
        """
        Starts running a build with the settings defined in the project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/start_build.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_build)
        """

    async def start_build_batch(
        self, **kwargs: Unpack[StartBuildBatchInputTypeDef]
    ) -> StartBuildBatchOutputTypeDef:
        """
        Starts a batch build for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/start_build_batch.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_build_batch)
        """

    async def start_command_execution(
        self, **kwargs: Unpack[StartCommandExecutionInputTypeDef]
    ) -> StartCommandExecutionOutputTypeDef:
        """
        Starts a command execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/start_command_execution.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_command_execution)
        """

    async def start_sandbox(
        self, **kwargs: Unpack[StartSandboxInputTypeDef]
    ) -> StartSandboxOutputTypeDef:
        """
        Starts a sandbox.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/start_sandbox.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_sandbox)
        """

    async def start_sandbox_connection(
        self, **kwargs: Unpack[StartSandboxConnectionInputTypeDef]
    ) -> StartSandboxConnectionOutputTypeDef:
        """
        Starts a sandbox connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/start_sandbox_connection.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#start_sandbox_connection)
        """

    async def stop_build(self, **kwargs: Unpack[StopBuildInputTypeDef]) -> StopBuildOutputTypeDef:
        """
        Attempts to stop running a build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/stop_build.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#stop_build)
        """

    async def stop_build_batch(
        self, **kwargs: Unpack[StopBuildBatchInputTypeDef]
    ) -> StopBuildBatchOutputTypeDef:
        """
        Stops a running batch build.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/stop_build_batch.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#stop_build_batch)
        """

    async def stop_sandbox(
        self, **kwargs: Unpack[StopSandboxInputTypeDef]
    ) -> StopSandboxOutputTypeDef:
        """
        Stops a sandbox.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/stop_sandbox.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#stop_sandbox)
        """

    async def update_fleet(
        self, **kwargs: Unpack[UpdateFleetInputTypeDef]
    ) -> UpdateFleetOutputTypeDef:
        """
        Updates a compute fleet.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/update_fleet.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_fleet)
        """

    async def update_project(
        self, **kwargs: Unpack[UpdateProjectInputTypeDef]
    ) -> UpdateProjectOutputTypeDef:
        """
        Changes the settings of a build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/update_project.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_project)
        """

    async def update_project_visibility(
        self, **kwargs: Unpack[UpdateProjectVisibilityInputTypeDef]
    ) -> UpdateProjectVisibilityOutputTypeDef:
        """
        Changes the public visibility for a project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/update_project_visibility.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_project_visibility)
        """

    async def update_report_group(
        self, **kwargs: Unpack[UpdateReportGroupInputTypeDef]
    ) -> UpdateReportGroupOutputTypeDef:
        """
        Updates a report group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/update_report_group.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_report_group)
        """

    async def update_webhook(
        self, **kwargs: Unpack[UpdateWebhookInputTypeDef]
    ) -> UpdateWebhookOutputTypeDef:
        """
        Updates the webhook associated with an CodeBuild build project.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/update_webhook.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#update_webhook)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_code_coverages"]
    ) -> DescribeCodeCoveragesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_test_cases"]
    ) -> DescribeTestCasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_build_batches_for_project"]
    ) -> ListBuildBatchesForProjectPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_build_batches"]
    ) -> ListBuildBatchesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_builds_for_project"]
    ) -> ListBuildsForProjectPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_builds"]
    ) -> ListBuildsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_command_executions_for_sandbox"]
    ) -> ListCommandExecutionsForSandboxPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_projects"]
    ) -> ListProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_report_groups"]
    ) -> ListReportGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_reports_for_report_group"]
    ) -> ListReportsForReportGroupPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_reports"]
    ) -> ListReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sandboxes_for_project"]
    ) -> ListSandboxesForProjectPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_sandboxes"]
    ) -> ListSandboxesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_shared_projects"]
    ) -> ListSharedProjectsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_shared_report_groups"]
    ) -> ListSharedReportGroupsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild.html#CodeBuild.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/client/)
        """
