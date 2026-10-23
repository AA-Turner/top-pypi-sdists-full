"""
Main interface for continuum service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_continuum/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_continuum import (
        Client,
        CodeScanSucceededWaiter,
        ContinuumClient,
        ListAssociatedCollectorsPaginator,
        ListAssociatedEnvironmentsPaginator,
        ListCodeFindingsPaginator,
        ListCodeIssueArtifactsPaginator,
        ListCodeIssuesPaginator,
        ListCodeScansPaginator,
        ListEnvironmentsPaginator,
        ListIntegrationsPaginator,
    )

    session = Session()
    client: ContinuumClient = session.client("continuum")

    code_scan_succeeded_waiter: CodeScanSucceededWaiter = client.get_waiter("code_scan_succeeded")

    list_associated_collectors_paginator: ListAssociatedCollectorsPaginator = client.get_paginator("list_associated_collectors")
    list_associated_environments_paginator: ListAssociatedEnvironmentsPaginator = client.get_paginator("list_associated_environments")
    list_code_findings_paginator: ListCodeFindingsPaginator = client.get_paginator("list_code_findings")
    list_code_issue_artifacts_paginator: ListCodeIssueArtifactsPaginator = client.get_paginator("list_code_issue_artifacts")
    list_code_issues_paginator: ListCodeIssuesPaginator = client.get_paginator("list_code_issues")
    list_code_scans_paginator: ListCodeScansPaginator = client.get_paginator("list_code_scans")
    list_environments_paginator: ListEnvironmentsPaginator = client.get_paginator("list_environments")
    list_integrations_paginator: ListIntegrationsPaginator = client.get_paginator("list_integrations")
    ```
"""

from .client import ContinuumClient
from .paginator import (
    ListAssociatedCollectorsPaginator,
    ListAssociatedEnvironmentsPaginator,
    ListCodeFindingsPaginator,
    ListCodeIssueArtifactsPaginator,
    ListCodeIssuesPaginator,
    ListCodeScansPaginator,
    ListEnvironmentsPaginator,
    ListIntegrationsPaginator,
)
from .waiter import CodeScanSucceededWaiter

Client = ContinuumClient

__all__ = (
    "Client",
    "CodeScanSucceededWaiter",
    "ContinuumClient",
    "ListAssociatedCollectorsPaginator",
    "ListAssociatedEnvironmentsPaginator",
    "ListCodeFindingsPaginator",
    "ListCodeIssueArtifactsPaginator",
    "ListCodeIssuesPaginator",
    "ListCodeScansPaginator",
    "ListEnvironmentsPaginator",
    "ListIntegrationsPaginator",
)
