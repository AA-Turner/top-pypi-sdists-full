"""
Type annotations for cloudformation service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_cloudformation.client import CloudFormationClient
    from types_aiobotocore_cloudformation.paginator import (
        DescribeAccountLimitsPaginator,
        DescribeChangeSetPaginator,
        DescribeStackEventsPaginator,
        DescribeStacksPaginator,
        ListChangeSetsPaginator,
        ListExportsPaginator,
        ListGeneratedTemplatesPaginator,
        ListImportsPaginator,
        ListResourceScanRelatedResourcesPaginator,
        ListResourceScanResourcesPaginator,
        ListResourceScansPaginator,
        ListStackInstancesPaginator,
        ListStackRefactorActionsPaginator,
        ListStackRefactorsPaginator,
        ListStackResourcesPaginator,
        ListStackSetOperationResultsPaginator,
        ListStackSetOperationsPaginator,
        ListStackSetsPaginator,
        ListStacksPaginator,
        ListTypesPaginator,
    )

    session = get_session()
    with session.create_client("cloudformation") as client:
        client: CloudFormationClient

        describe_account_limits_paginator: DescribeAccountLimitsPaginator = client.get_paginator("describe_account_limits")
        describe_change_set_paginator: DescribeChangeSetPaginator = client.get_paginator("describe_change_set")
        describe_stack_events_paginator: DescribeStackEventsPaginator = client.get_paginator("describe_stack_events")
        describe_stacks_paginator: DescribeStacksPaginator = client.get_paginator("describe_stacks")
        list_change_sets_paginator: ListChangeSetsPaginator = client.get_paginator("list_change_sets")
        list_exports_paginator: ListExportsPaginator = client.get_paginator("list_exports")
        list_generated_templates_paginator: ListGeneratedTemplatesPaginator = client.get_paginator("list_generated_templates")
        list_imports_paginator: ListImportsPaginator = client.get_paginator("list_imports")
        list_resource_scan_related_resources_paginator: ListResourceScanRelatedResourcesPaginator = client.get_paginator("list_resource_scan_related_resources")
        list_resource_scan_resources_paginator: ListResourceScanResourcesPaginator = client.get_paginator("list_resource_scan_resources")
        list_resource_scans_paginator: ListResourceScansPaginator = client.get_paginator("list_resource_scans")
        list_stack_instances_paginator: ListStackInstancesPaginator = client.get_paginator("list_stack_instances")
        list_stack_refactor_actions_paginator: ListStackRefactorActionsPaginator = client.get_paginator("list_stack_refactor_actions")
        list_stack_refactors_paginator: ListStackRefactorsPaginator = client.get_paginator("list_stack_refactors")
        list_stack_resources_paginator: ListStackResourcesPaginator = client.get_paginator("list_stack_resources")
        list_stack_set_operation_results_paginator: ListStackSetOperationResultsPaginator = client.get_paginator("list_stack_set_operation_results")
        list_stack_set_operations_paginator: ListStackSetOperationsPaginator = client.get_paginator("list_stack_set_operations")
        list_stack_sets_paginator: ListStackSetsPaginator = client.get_paginator("list_stack_sets")
        list_stacks_paginator: ListStacksPaginator = client.get_paginator("list_stacks")
        list_types_paginator: ListTypesPaginator = client.get_paginator("list_types")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeAccountLimitsInputPaginateTypeDef,
    DescribeAccountLimitsOutputTypeDef,
    DescribeChangeSetInputPaginateTypeDef,
    DescribeChangeSetOutputTypeDef,
    DescribeStackEventsInputPaginateTypeDef,
    DescribeStackEventsOutputTypeDef,
    DescribeStacksInputPaginateTypeDef,
    DescribeStacksOutputTypeDef,
    ListChangeSetsInputPaginateTypeDef,
    ListChangeSetsOutputTypeDef,
    ListExportsInputPaginateTypeDef,
    ListExportsOutputTypeDef,
    ListGeneratedTemplatesInputPaginateTypeDef,
    ListGeneratedTemplatesOutputTypeDef,
    ListImportsInputPaginateTypeDef,
    ListImportsOutputTypeDef,
    ListResourceScanRelatedResourcesInputPaginateTypeDef,
    ListResourceScanRelatedResourcesOutputTypeDef,
    ListResourceScanResourcesInputPaginateTypeDef,
    ListResourceScanResourcesOutputTypeDef,
    ListResourceScansInputPaginateTypeDef,
    ListResourceScansOutputTypeDef,
    ListStackInstancesInputPaginateTypeDef,
    ListStackInstancesOutputTypeDef,
    ListStackRefactorActionsInputPaginateTypeDef,
    ListStackRefactorActionsOutputTypeDef,
    ListStackRefactorsInputPaginateTypeDef,
    ListStackRefactorsOutputTypeDef,
    ListStackResourcesInputPaginateTypeDef,
    ListStackResourcesOutputTypeDef,
    ListStackSetOperationResultsInputPaginateTypeDef,
    ListStackSetOperationResultsOutputTypeDef,
    ListStackSetOperationsInputPaginateTypeDef,
    ListStackSetOperationsOutputTypeDef,
    ListStackSetsInputPaginateTypeDef,
    ListStackSetsOutputTypeDef,
    ListStacksInputPaginateTypeDef,
    ListStacksOutputTypeDef,
    ListTypesInputPaginateTypeDef,
    ListTypesOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "DescribeAccountLimitsPaginator",
    "DescribeChangeSetPaginator",
    "DescribeStackEventsPaginator",
    "DescribeStacksPaginator",
    "ListChangeSetsPaginator",
    "ListExportsPaginator",
    "ListGeneratedTemplatesPaginator",
    "ListImportsPaginator",
    "ListResourceScanRelatedResourcesPaginator",
    "ListResourceScanResourcesPaginator",
    "ListResourceScansPaginator",
    "ListStackInstancesPaginator",
    "ListStackRefactorActionsPaginator",
    "ListStackRefactorsPaginator",
    "ListStackResourcesPaginator",
    "ListStackSetOperationResultsPaginator",
    "ListStackSetOperationsPaginator",
    "ListStackSetsPaginator",
    "ListStacksPaginator",
    "ListTypesPaginator",
)

if TYPE_CHECKING:
    _DescribeAccountLimitsPaginatorBase = AioPaginator[DescribeAccountLimitsOutputTypeDef]
else:
    _DescribeAccountLimitsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeAccountLimitsPaginator(_DescribeAccountLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeAccountLimits.html#CloudFormation.Paginator.DescribeAccountLimits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describeaccountlimitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAccountLimitsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeAccountLimitsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeAccountLimits.html#CloudFormation.Paginator.DescribeAccountLimits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describeaccountlimitspaginator)
        """

if TYPE_CHECKING:
    _DescribeChangeSetPaginatorBase = AioPaginator[DescribeChangeSetOutputTypeDef]
else:
    _DescribeChangeSetPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeChangeSetPaginator(_DescribeChangeSetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeChangeSet.html#CloudFormation.Paginator.DescribeChangeSet)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describechangesetpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeChangeSetInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeChangeSetOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeChangeSet.html#CloudFormation.Paginator.DescribeChangeSet.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describechangesetpaginator)
        """

if TYPE_CHECKING:
    _DescribeStackEventsPaginatorBase = AioPaginator[DescribeStackEventsOutputTypeDef]
else:
    _DescribeStackEventsPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeStackEventsPaginator(_DescribeStackEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStackEvents.html#CloudFormation.Paginator.DescribeStackEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackeventspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStackEventsInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeStackEventsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStackEvents.html#CloudFormation.Paginator.DescribeStackEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackeventspaginator)
        """

if TYPE_CHECKING:
    _DescribeStacksPaginatorBase = AioPaginator[DescribeStacksOutputTypeDef]
else:
    _DescribeStacksPaginatorBase = AioPaginator  # type: ignore[assignment]

class DescribeStacksPaginator(_DescribeStacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStacks.html#CloudFormation.Paginator.DescribeStacks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeStacksInputPaginateTypeDef]
    ) -> AioPageIterator[DescribeStacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/DescribeStacks.html#CloudFormation.Paginator.DescribeStacks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#describestackspaginator)
        """

if TYPE_CHECKING:
    _ListChangeSetsPaginatorBase = AioPaginator[ListChangeSetsOutputTypeDef]
else:
    _ListChangeSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListChangeSetsPaginator(_ListChangeSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListChangeSets.html#CloudFormation.Paginator.ListChangeSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listchangesetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListChangeSetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListChangeSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListChangeSets.html#CloudFormation.Paginator.ListChangeSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listchangesetspaginator)
        """

if TYPE_CHECKING:
    _ListExportsPaginatorBase = AioPaginator[ListExportsOutputTypeDef]
else:
    _ListExportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListExportsPaginator(_ListExportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListExports.html#CloudFormation.Paginator.ListExports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listexportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListExportsInputPaginateTypeDef]
    ) -> AioPageIterator[ListExportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListExports.html#CloudFormation.Paginator.ListExports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listexportspaginator)
        """

if TYPE_CHECKING:
    _ListGeneratedTemplatesPaginatorBase = AioPaginator[ListGeneratedTemplatesOutputTypeDef]
else:
    _ListGeneratedTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListGeneratedTemplatesPaginator(_ListGeneratedTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListGeneratedTemplates.html#CloudFormation.Paginator.ListGeneratedTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listgeneratedtemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGeneratedTemplatesInputPaginateTypeDef]
    ) -> AioPageIterator[ListGeneratedTemplatesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListGeneratedTemplates.html#CloudFormation.Paginator.ListGeneratedTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listgeneratedtemplatespaginator)
        """

if TYPE_CHECKING:
    _ListImportsPaginatorBase = AioPaginator[ListImportsOutputTypeDef]
else:
    _ListImportsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListImportsPaginator(_ListImportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListImports.html#CloudFormation.Paginator.ListImports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listimportspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListImportsInputPaginateTypeDef]
    ) -> AioPageIterator[ListImportsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListImports.html#CloudFormation.Paginator.ListImports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listimportspaginator)
        """

if TYPE_CHECKING:
    _ListResourceScanRelatedResourcesPaginatorBase = AioPaginator[
        ListResourceScanRelatedResourcesOutputTypeDef
    ]
else:
    _ListResourceScanRelatedResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceScanRelatedResourcesPaginator(_ListResourceScanRelatedResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanRelatedResources.html#CloudFormation.Paginator.ListResourceScanRelatedResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanrelatedresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceScanRelatedResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceScanRelatedResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanRelatedResources.html#CloudFormation.Paginator.ListResourceScanRelatedResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanrelatedresourcespaginator)
        """

if TYPE_CHECKING:
    _ListResourceScanResourcesPaginatorBase = AioPaginator[ListResourceScanResourcesOutputTypeDef]
else:
    _ListResourceScanResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceScanResourcesPaginator(_ListResourceScanResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanResources.html#CloudFormation.Paginator.ListResourceScanResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceScanResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceScanResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScanResources.html#CloudFormation.Paginator.ListResourceScanResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanresourcespaginator)
        """

if TYPE_CHECKING:
    _ListResourceScansPaginatorBase = AioPaginator[ListResourceScansOutputTypeDef]
else:
    _ListResourceScansPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListResourceScansPaginator(_ListResourceScansPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScans.html#CloudFormation.Paginator.ListResourceScans)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceScansInputPaginateTypeDef]
    ) -> AioPageIterator[ListResourceScansOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListResourceScans.html#CloudFormation.Paginator.ListResourceScans.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listresourcescanspaginator)
        """

if TYPE_CHECKING:
    _ListStackInstancesPaginatorBase = AioPaginator[ListStackInstancesOutputTypeDef]
else:
    _ListStackInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackInstancesPaginator(_ListStackInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackInstances.html#CloudFormation.Paginator.ListStackInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackInstancesInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackInstancesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackInstances.html#CloudFormation.Paginator.ListStackInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackinstancespaginator)
        """

if TYPE_CHECKING:
    _ListStackRefactorActionsPaginatorBase = AioPaginator[ListStackRefactorActionsOutputTypeDef]
else:
    _ListStackRefactorActionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackRefactorActionsPaginator(_ListStackRefactorActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackRefactorActions.html#CloudFormation.Paginator.ListStackRefactorActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackrefactoractionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackRefactorActionsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackRefactorActionsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackRefactorActions.html#CloudFormation.Paginator.ListStackRefactorActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackrefactoractionspaginator)
        """

if TYPE_CHECKING:
    _ListStackRefactorsPaginatorBase = AioPaginator[ListStackRefactorsOutputTypeDef]
else:
    _ListStackRefactorsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackRefactorsPaginator(_ListStackRefactorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackRefactors.html#CloudFormation.Paginator.ListStackRefactors)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackrefactorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackRefactorsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackRefactorsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackRefactors.html#CloudFormation.Paginator.ListStackRefactors.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackrefactorspaginator)
        """

if TYPE_CHECKING:
    _ListStackResourcesPaginatorBase = AioPaginator[ListStackResourcesOutputTypeDef]
else:
    _ListStackResourcesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackResourcesPaginator(_ListStackResourcesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackResources.html#CloudFormation.Paginator.ListStackResources)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackresourcespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackResourcesInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackResourcesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackResources.html#CloudFormation.Paginator.ListStackResources.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackresourcespaginator)
        """

if TYPE_CHECKING:
    _ListStackSetOperationResultsPaginatorBase = AioPaginator[
        ListStackSetOperationResultsOutputTypeDef
    ]
else:
    _ListStackSetOperationResultsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackSetOperationResultsPaginator(_ListStackSetOperationResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperationResults.html#CloudFormation.Paginator.ListStackSetOperationResults)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationresultspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackSetOperationResultsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackSetOperationResultsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperationResults.html#CloudFormation.Paginator.ListStackSetOperationResults.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationresultspaginator)
        """

if TYPE_CHECKING:
    _ListStackSetOperationsPaginatorBase = AioPaginator[ListStackSetOperationsOutputTypeDef]
else:
    _ListStackSetOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackSetOperationsPaginator(_ListStackSetOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperations.html#CloudFormation.Paginator.ListStackSetOperations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackSetOperationsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackSetOperationsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSetOperations.html#CloudFormation.Paginator.ListStackSetOperations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetoperationspaginator)
        """

if TYPE_CHECKING:
    _ListStackSetsPaginatorBase = AioPaginator[ListStackSetsOutputTypeDef]
else:
    _ListStackSetsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStackSetsPaginator(_ListStackSetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSets.html#CloudFormation.Paginator.ListStackSets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStackSetsInputPaginateTypeDef]
    ) -> AioPageIterator[ListStackSetsOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStackSets.html#CloudFormation.Paginator.ListStackSets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststacksetspaginator)
        """

if TYPE_CHECKING:
    _ListStacksPaginatorBase = AioPaginator[ListStacksOutputTypeDef]
else:
    _ListStacksPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListStacksPaginator(_ListStacksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStacks.html#CloudFormation.Paginator.ListStacks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStacksInputPaginateTypeDef]
    ) -> AioPageIterator[ListStacksOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListStacks.html#CloudFormation.Paginator.ListStacks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#liststackspaginator)
        """

if TYPE_CHECKING:
    _ListTypesPaginatorBase = AioPaginator[ListTypesOutputTypeDef]
else:
    _ListTypesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTypesPaginator(_ListTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListTypes.html#CloudFormation.Paginator.ListTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listtypespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTypesInputPaginateTypeDef]
    ) -> AioPageIterator[ListTypesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudformation/paginator/ListTypes.html#CloudFormation.Paginator.ListTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudformation/paginators/#listtypespaginator)
        """
