"""
Type annotations for codebuild service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_codebuild.client import CodeBuildClient
    from types_aiobotocore_codebuild.paginator import (
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

    session = get_session()
    with session.create_client("codebuild") as client:
        client: CodeBuildClient

        describe_code_coverages_paginator: DescribeCodeCoveragesPaginator = client.get_paginator("describe_code_coverages")
        describe_test_cases_paginator: DescribeTestCasesPaginator = client.get_paginator("describe_test_cases")
        list_build_batches_for_project_paginator: ListBuildBatchesForProjectPaginator = client.get_paginator("list_build_batches_for_project")
        list_build_batches_paginator: ListBuildBatchesPaginator = client.get_paginator("list_build_batches")
        list_builds_for_project_paginator: ListBuildsForProjectPaginator = client.get_paginator("list_builds_for_project")
        list_builds_paginator: ListBuildsPaginator = client.get_paginator("list_builds")
        list_command_executions_for_sandbox_paginator: ListCommandExecutionsForSandboxPaginator = client.get_paginator("list_command_executions_for_sandbox")
        list_projects_paginator: ListProjectsPaginator = client.get_paginator("list_projects")
        list_report_groups_paginator: ListReportGroupsPaginator = client.get_paginator("list_report_groups")
        list_reports_for_report_group_paginator: ListReportsForReportGroupPaginator = client.get_paginator("list_reports_for_report_group")
        list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
        list_sandboxes_for_project_paginator: ListSandboxesForProjectPaginator = client.get_paginator("list_sandboxes_for_project")
        list_sandboxes_paginator: ListSandboxesPaginator = client.get_paginator("list_sandboxes")
        list_shared_projects_paginator: ListSharedProjectsPaginator = client.get_paginator("list_shared_projects")
        list_shared_report_groups_paginator: ListSharedReportGroupsPaginator = client.get_paginator("list_shared_report_groups")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeCodeCoveragesInputPaginateTypeDef,
    DescribeCodeCoveragesOutputTypeDef,
    DescribeTestCasesInputPaginateTypeDef,
    DescribeTestCasesOutputTypeDef,
    ListBuildBatchesForProjectInputPaginateTypeDef,
    ListBuildBatchesForProjectOutputTypeDef,
    ListBuildBatchesInputPaginateTypeDef,
    ListBuildBatchesOutputTypeDef,
    ListBuildsForProjectInputPaginateTypeDef,
    ListBuildsForProjectOutputTypeDef,
    ListBuildsInputPaginateTypeDef,
    ListBuildsOutputTypeDef,
    ListCommandExecutionsForSandboxInputPaginateTypeDef,
    ListCommandExecutionsForSandboxOutputTypeDef,
    ListProjectsInputPaginateTypeDef,
    ListProjectsOutputTypeDef,
    ListReportGroupsInputPaginateTypeDef,
    ListReportGroupsOutputTypeDef,
    ListReportsForReportGroupInputPaginateTypeDef,
    ListReportsForReportGroupOutputTypeDef,
    ListReportsInputPaginateTypeDef,
    ListReportsOutputTypeDef,
    ListSandboxesForProjectInputPaginateTypeDef,
    ListSandboxesForProjectOutputTypeDef,
    ListSandboxesInputPaginateTypeDef,
    ListSandboxesOutputTypeDef,
    ListSharedProjectsInputPaginateTypeDef,
    ListSharedProjectsOutputTypeDef,
    ListSharedReportGroupsInputPaginateTypeDef,
    ListSharedReportGroupsOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeCodeCoveragesPaginator",
    "DescribeTestCasesPaginator",
    "ListBuildBatchesForProjectPaginator",
    "ListBuildBatchesPaginator",
    "ListBuildsForProjectPaginator",
    "ListBuildsPaginator",
    "ListCommandExecutionsForSandboxPaginator",
    "ListProjectsPaginator",
    "ListReportGroupsPaginator",
    "ListReportsForReportGroupPaginator",
    "ListReportsPaginator",
    "ListSandboxesForProjectPaginator",
    "ListSandboxesPaginator",
    "ListSharedProjectsPaginator",
    "ListSharedReportGroupsPaginator",
)

if TYPE_CHECKING:
    _DescribeCodeCoveragesPaginatorBase = AioPaginator[DescribeCodeCoveragesOutputTypeDef]
else:
    _DescribeCodeCoveragesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeCodeCoveragesPaginator(_DescribeCodeCoveragesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeCodeCoverages.html#CodeBuild.Paginator.DescribeCodeCoverages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describecodecoveragespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeCodeCoveragesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeCodeCoveragesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeCodeCoverages.html#CodeBuild.Paginator.DescribeCodeCoverages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describecodecoveragespaginator)
        """

if TYPE_CHECKING:
    _DescribeTestCasesPaginatorBase = AioPaginator[DescribeTestCasesOutputTypeDef]
else:
    _DescribeTestCasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeTestCasesPaginator(_DescribeTestCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeTestCases.html#CodeBuild.Paginator.DescribeTestCases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describetestcasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeTestCasesInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeTestCasesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/DescribeTestCases.html#CodeBuild.Paginator.DescribeTestCases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#describetestcasespaginator)
        """

if TYPE_CHECKING:
    _ListBuildBatchesForProjectPaginatorBase = AioPaginator[ListBuildBatchesForProjectOutputTypeDef]
else:
    _ListBuildBatchesForProjectPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBuildBatchesForProjectPaginator(_ListBuildBatchesForProjectPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatchesForProject.html#CodeBuild.Paginator.ListBuildBatchesForProject)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchesforprojectpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBuildBatchesForProjectInputPaginateTypeDef]
    ) -> AioPageIterator[ListBuildBatchesForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatchesForProject.html#CodeBuild.Paginator.ListBuildBatchesForProject.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchesforprojectpaginator)
        """

if TYPE_CHECKING:
    _ListBuildBatchesPaginatorBase = AioPaginator[ListBuildBatchesOutputTypeDef]
else:
    _ListBuildBatchesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBuildBatchesPaginator(_ListBuildBatchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatches.html#CodeBuild.Paginator.ListBuildBatches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBuildBatchesInputPaginateTypeDef]
    ) -> AioPageIterator[ListBuildBatchesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildBatches.html#CodeBuild.Paginator.ListBuildBatches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildbatchespaginator)
        """

if TYPE_CHECKING:
    _ListBuildsForProjectPaginatorBase = AioPaginator[ListBuildsForProjectOutputTypeDef]
else:
    _ListBuildsForProjectPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBuildsForProjectPaginator(_ListBuildsForProjectPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildsForProject.html#CodeBuild.Paginator.ListBuildsForProject)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildsforprojectpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBuildsForProjectInputPaginateTypeDef]
    ) -> AioPageIterator[ListBuildsForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuildsForProject.html#CodeBuild.Paginator.ListBuildsForProject.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildsforprojectpaginator)
        """

if TYPE_CHECKING:
    _ListBuildsPaginatorBase = AioPaginator[ListBuildsOutputTypeDef]
else:
    _ListBuildsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBuildsPaginator(_ListBuildsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuilds.html#CodeBuild.Paginator.ListBuilds)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBuildsInputPaginateTypeDef]
    ) -> AioPageIterator[ListBuildsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListBuilds.html#CodeBuild.Paginator.ListBuilds.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listbuildspaginator)
        """

if TYPE_CHECKING:
    _ListCommandExecutionsForSandboxPaginatorBase = AioPaginator[
        ListCommandExecutionsForSandboxOutputTypeDef
    ]
else:
    _ListCommandExecutionsForSandboxPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListCommandExecutionsForSandboxPaginator(_ListCommandExecutionsForSandboxPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListCommandExecutionsForSandbox.html#CodeBuild.Paginator.ListCommandExecutionsForSandbox)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listcommandexecutionsforsandboxpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommandExecutionsForSandboxInputPaginateTypeDef]
    ) -> AioPageIterator[ListCommandExecutionsForSandboxOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListCommandExecutionsForSandbox.html#CodeBuild.Paginator.ListCommandExecutionsForSandbox.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listcommandexecutionsforsandboxpaginator)
        """

if TYPE_CHECKING:
    _ListProjectsPaginatorBase = AioPaginator[ListProjectsOutputTypeDef]
else:
    _ListProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListProjectsPaginator(_ListProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListProjects.html#CodeBuild.Paginator.ListProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProjectsInputPaginateTypeDef]
    ) -> AioPageIterator[ListProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListProjects.html#CodeBuild.Paginator.ListProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listprojectspaginator)
        """

if TYPE_CHECKING:
    _ListReportGroupsPaginatorBase = AioPaginator[ListReportGroupsOutputTypeDef]
else:
    _ListReportGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportGroupsPaginator(_ListReportGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportGroups.html#CodeBuild.Paginator.ListReportGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListReportGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportGroups.html#CodeBuild.Paginator.ListReportGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportgroupspaginator)
        """

if TYPE_CHECKING:
    _ListReportsForReportGroupPaginatorBase = AioPaginator[ListReportsForReportGroupOutputTypeDef]
else:
    _ListReportsForReportGroupPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportsForReportGroupPaginator(_ListReportsForReportGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportsForReportGroup.html#CodeBuild.Paginator.ListReportsForReportGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportsforreportgrouppaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsForReportGroupInputPaginateTypeDef]
    ) -> AioPageIterator[ListReportsForReportGroupOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReportsForReportGroup.html#CodeBuild.Paginator.ListReportsForReportGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportsforreportgrouppaginator)
        """

if TYPE_CHECKING:
    _ListReportsPaginatorBase = AioPaginator[ListReportsOutputTypeDef]
else:
    _ListReportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListReportsPaginator(_ListReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReports.html#CodeBuild.Paginator.ListReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListReportsInputPaginateTypeDef]
    ) -> AioPageIterator[ListReportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListReports.html#CodeBuild.Paginator.ListReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listreportspaginator)
        """

if TYPE_CHECKING:
    _ListSandboxesForProjectPaginatorBase = AioPaginator[ListSandboxesForProjectOutputTypeDef]
else:
    _ListSandboxesForProjectPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSandboxesForProjectPaginator(_ListSandboxesForProjectPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSandboxesForProject.html#CodeBuild.Paginator.ListSandboxesForProject)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsandboxesforprojectpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSandboxesForProjectInputPaginateTypeDef]
    ) -> AioPageIterator[ListSandboxesForProjectOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSandboxesForProject.html#CodeBuild.Paginator.ListSandboxesForProject.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsandboxesforprojectpaginator)
        """

if TYPE_CHECKING:
    _ListSandboxesPaginatorBase = AioPaginator[ListSandboxesOutputTypeDef]
else:
    _ListSandboxesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSandboxesPaginator(_ListSandboxesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSandboxes.html#CodeBuild.Paginator.ListSandboxes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsandboxespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSandboxesInputPaginateTypeDef]
    ) -> AioPageIterator[ListSandboxesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSandboxes.html#CodeBuild.Paginator.ListSandboxes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsandboxespaginator)
        """

if TYPE_CHECKING:
    _ListSharedProjectsPaginatorBase = AioPaginator[ListSharedProjectsOutputTypeDef]
else:
    _ListSharedProjectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSharedProjectsPaginator(_ListSharedProjectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedProjects.html#CodeBuild.Paginator.ListSharedProjects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedprojectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSharedProjectsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSharedProjectsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedProjects.html#CodeBuild.Paginator.ListSharedProjects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedprojectspaginator)
        """

if TYPE_CHECKING:
    _ListSharedReportGroupsPaginatorBase = AioPaginator[ListSharedReportGroupsOutputTypeDef]
else:
    _ListSharedReportGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSharedReportGroupsPaginator(_ListSharedReportGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedReportGroups.html#CodeBuild.Paginator.ListSharedReportGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedreportgroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSharedReportGroupsInputPaginateTypeDef]
    ) -> AioPageIterator[ListSharedReportGroupsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codebuild/paginator/ListSharedReportGroups.html#CodeBuild.Paginator.ListSharedReportGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/paginators/#listsharedreportgroupspaginator)
        """
