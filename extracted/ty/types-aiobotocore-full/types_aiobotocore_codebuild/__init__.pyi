"""
Main interface for codebuild service.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codebuild/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codebuild import (
        Client,
        CodeBuildClient,
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
    async with session.create_client("codebuild") as client:
        client: CodeBuildClient
        ...


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

from .client import CodeBuildClient
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

Client = CodeBuildClient

__all__ = (
    "Client",
    "CodeBuildClient",
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
