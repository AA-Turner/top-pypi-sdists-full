"""
Type annotations for ssm service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ssm.client import SSMClient
    from types_aiobotocore_ssm.paginator import (
        DescribeActivationsPaginator,
        DescribeAssociationExecutionTargetsPaginator,
        DescribeAssociationExecutionsPaginator,
        DescribeAutomationExecutionsPaginator,
        DescribeAutomationStepExecutionsPaginator,
        DescribeAvailablePatchesPaginator,
        DescribeEffectiveInstanceAssociationsPaginator,
        DescribeEffectivePatchesForPatchBaselinePaginator,
        DescribeInstanceAssociationsStatusPaginator,
        DescribeInstanceInformationPaginator,
        DescribeInstancePatchStatesForPatchGroupPaginator,
        DescribeInstancePatchStatesPaginator,
        DescribeInstancePatchesPaginator,
        DescribeInstancePropertiesPaginator,
        DescribeInventoryDeletionsPaginator,
        DescribeMaintenanceWindowExecutionTaskInvocationsPaginator,
        DescribeMaintenanceWindowExecutionTasksPaginator,
        DescribeMaintenanceWindowExecutionsPaginator,
        DescribeMaintenanceWindowSchedulePaginator,
        DescribeMaintenanceWindowTargetsPaginator,
        DescribeMaintenanceWindowTasksPaginator,
        DescribeMaintenanceWindowsForTargetPaginator,
        DescribeMaintenanceWindowsPaginator,
        DescribeOpsItemsPaginator,
        DescribeParametersPaginator,
        DescribePatchBaselinesPaginator,
        DescribePatchGroupsPaginator,
        DescribePatchPropertiesPaginator,
        DescribeSessionsPaginator,
        GetInventoryPaginator,
        GetInventorySchemaPaginator,
        GetOpsSummaryPaginator,
        GetParameterHistoryPaginator,
        GetParametersByPathPaginator,
        GetResourcePoliciesPaginator,
        ListAssociationVersionsPaginator,
        ListAssociationsPaginator,
        ListCommandInvocationsPaginator,
        ListCommandsPaginator,
        ListComplianceItemsPaginator,
        ListComplianceSummariesPaginator,
        ListDocumentVersionsPaginator,
        ListDocumentsPaginator,
        ListNodesPaginator,
        ListNodesSummaryPaginator,
        ListOpsItemEventsPaginator,
        ListOpsItemRelatedItemsPaginator,
        ListOpsMetadataPaginator,
        ListResourceComplianceSummariesPaginator,
        ListResourceDataSyncPaginator,
    )

    session = get_session()
    with session.create_client("ssm") as client:
        client: SSMClient

        describe_activations_paginator: DescribeActivationsPaginator = client.get_paginator("describe_activations")
        describe_association_execution_targets_paginator: DescribeAssociationExecutionTargetsPaginator = client.get_paginator("describe_association_execution_targets")
        describe_association_executions_paginator: DescribeAssociationExecutionsPaginator = client.get_paginator("describe_association_executions")
        describe_automation_executions_paginator: DescribeAutomationExecutionsPaginator = client.get_paginator("describe_automation_executions")
        describe_automation_step_executions_paginator: DescribeAutomationStepExecutionsPaginator = client.get_paginator("describe_automation_step_executions")
        describe_available_patches_paginator: DescribeAvailablePatchesPaginator = client.get_paginator("describe_available_patches")
        describe_effective_instance_associations_paginator: DescribeEffectiveInstanceAssociationsPaginator = client.get_paginator("describe_effective_instance_associations")
        describe_effective_patches_for_patch_baseline_paginator: DescribeEffectivePatchesForPatchBaselinePaginator = client.get_paginator("describe_effective_patches_for_patch_baseline")
        describe_instance_associations_status_paginator: DescribeInstanceAssociationsStatusPaginator = client.get_paginator("describe_instance_associations_status")
        describe_instance_information_paginator: DescribeInstanceInformationPaginator = client.get_paginator("describe_instance_information")
        describe_instance_patch_states_for_patch_group_paginator: DescribeInstancePatchStatesForPatchGroupPaginator = client.get_paginator("describe_instance_patch_states_for_patch_group")
        describe_instance_patch_states_paginator: DescribeInstancePatchStatesPaginator = client.get_paginator("describe_instance_patch_states")
        describe_instance_patches_paginator: DescribeInstancePatchesPaginator = client.get_paginator("describe_instance_patches")
        describe_instance_properties_paginator: DescribeInstancePropertiesPaginator = client.get_paginator("describe_instance_properties")
        describe_inventory_deletions_paginator: DescribeInventoryDeletionsPaginator = client.get_paginator("describe_inventory_deletions")
        describe_maintenance_window_execution_task_invocations_paginator: DescribeMaintenanceWindowExecutionTaskInvocationsPaginator = client.get_paginator("describe_maintenance_window_execution_task_invocations")
        describe_maintenance_window_execution_tasks_paginator: DescribeMaintenanceWindowExecutionTasksPaginator = client.get_paginator("describe_maintenance_window_execution_tasks")
        describe_maintenance_window_executions_paginator: DescribeMaintenanceWindowExecutionsPaginator = client.get_paginator("describe_maintenance_window_executions")
        describe_maintenance_window_schedule_paginator: DescribeMaintenanceWindowSchedulePaginator = client.get_paginator("describe_maintenance_window_schedule")
        describe_maintenance_window_targets_paginator: DescribeMaintenanceWindowTargetsPaginator = client.get_paginator("describe_maintenance_window_targets")
        describe_maintenance_window_tasks_paginator: DescribeMaintenanceWindowTasksPaginator = client.get_paginator("describe_maintenance_window_tasks")
        describe_maintenance_windows_for_target_paginator: DescribeMaintenanceWindowsForTargetPaginator = client.get_paginator("describe_maintenance_windows_for_target")
        describe_maintenance_windows_paginator: DescribeMaintenanceWindowsPaginator = client.get_paginator("describe_maintenance_windows")
        describe_ops_items_paginator: DescribeOpsItemsPaginator = client.get_paginator("describe_ops_items")
        describe_parameters_paginator: DescribeParametersPaginator = client.get_paginator("describe_parameters")
        describe_patch_baselines_paginator: DescribePatchBaselinesPaginator = client.get_paginator("describe_patch_baselines")
        describe_patch_groups_paginator: DescribePatchGroupsPaginator = client.get_paginator("describe_patch_groups")
        describe_patch_properties_paginator: DescribePatchPropertiesPaginator = client.get_paginator("describe_patch_properties")
        describe_sessions_paginator: DescribeSessionsPaginator = client.get_paginator("describe_sessions")
        get_inventory_paginator: GetInventoryPaginator = client.get_paginator("get_inventory")
        get_inventory_schema_paginator: GetInventorySchemaPaginator = client.get_paginator("get_inventory_schema")
        get_ops_summary_paginator: GetOpsSummaryPaginator = client.get_paginator("get_ops_summary")
        get_parameter_history_paginator: GetParameterHistoryPaginator = client.get_paginator("get_parameter_history")
        get_parameters_by_path_paginator: GetParametersByPathPaginator = client.get_paginator("get_parameters_by_path")
        get_resource_policies_paginator: GetResourcePoliciesPaginator = client.get_paginator("get_resource_policies")
        list_association_versions_paginator: ListAssociationVersionsPaginator = client.get_paginator("list_association_versions")
        list_associations_paginator: ListAssociationsPaginator = client.get_paginator("list_associations")
        list_command_invocations_paginator: ListCommandInvocationsPaginator = client.get_paginator("list_command_invocations")
        list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
        list_compliance_items_paginator: ListComplianceItemsPaginator = client.get_paginator("list_compliance_items")
        list_compliance_summaries_paginator: ListComplianceSummariesPaginator = client.get_paginator("list_compliance_summaries")
        list_document_versions_paginator: ListDocumentVersionsPaginator = client.get_paginator("list_document_versions")
        list_documents_paginator: ListDocumentsPaginator = client.get_paginator("list_documents")
        list_nodes_paginator: ListNodesPaginator = client.get_paginator("list_nodes")
        list_nodes_summary_paginator: ListNodesSummaryPaginator = client.get_paginator("list_nodes_summary")
        list_ops_item_events_paginator: ListOpsItemEventsPaginator = client.get_paginator("list_ops_item_events")
        list_ops_item_related_items_paginator: ListOpsItemRelatedItemsPaginator = client.get_paginator("list_ops_item_related_items")
        list_ops_metadata_paginator: ListOpsMetadataPaginator = client.get_paginator("list_ops_metadata")
        list_resource_compliance_summaries_paginator: ListResourceComplianceSummariesPaginator = client.get_paginator("list_resource_compliance_summaries")
        list_resource_data_sync_paginator: ListResourceDataSyncPaginator = client.get_paginator("list_resource_data_sync")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    DescribeActivationsRequestPaginateTypeDef,
    DescribeActivationsResultTypeDef,
    DescribeAssociationExecutionsRequestPaginateTypeDef,
    DescribeAssociationExecutionsResultTypeDef,
    DescribeAssociationExecutionTargetsRequestPaginateTypeDef,
    DescribeAssociationExecutionTargetsResultTypeDef,
    DescribeAutomationExecutionsRequestPaginateTypeDef,
    DescribeAutomationExecutionsResultTypeDef,
    DescribeAutomationStepExecutionsRequestPaginateTypeDef,
    DescribeAutomationStepExecutionsResultTypeDef,
    DescribeAvailablePatchesRequestPaginateTypeDef,
    DescribeAvailablePatchesResultTypeDef,
    DescribeEffectiveInstanceAssociationsRequestPaginateTypeDef,
    DescribeEffectiveInstanceAssociationsResultTypeDef,
    DescribeEffectivePatchesForPatchBaselineRequestPaginateTypeDef,
    DescribeEffectivePatchesForPatchBaselineResultTypeDef,
    DescribeInstanceAssociationsStatusRequestPaginateTypeDef,
    DescribeInstanceAssociationsStatusResultTypeDef,
    DescribeInstanceInformationRequestPaginateTypeDef,
    DescribeInstanceInformationResultTypeDef,
    DescribeInstancePatchesRequestPaginateTypeDef,
    DescribeInstancePatchesResultTypeDef,
    DescribeInstancePatchStatesForPatchGroupRequestPaginateTypeDef,
    DescribeInstancePatchStatesForPatchGroupResultTypeDef,
    DescribeInstancePatchStatesRequestPaginateTypeDef,
    DescribeInstancePatchStatesResultTypeDef,
    DescribeInstancePropertiesRequestPaginateTypeDef,
    DescribeInstancePropertiesResultTypeDef,
    DescribeInventoryDeletionsRequestPaginateTypeDef,
    DescribeInventoryDeletionsResultTypeDef,
    DescribeMaintenanceWindowExecutionsRequestPaginateTypeDef,
    DescribeMaintenanceWindowExecutionsResultTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsRequestPaginateTypeDef,
    DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef,
    DescribeMaintenanceWindowExecutionTasksRequestPaginateTypeDef,
    DescribeMaintenanceWindowExecutionTasksResultTypeDef,
    DescribeMaintenanceWindowScheduleRequestPaginateTypeDef,
    DescribeMaintenanceWindowScheduleResultTypeDef,
    DescribeMaintenanceWindowsForTargetRequestPaginateTypeDef,
    DescribeMaintenanceWindowsForTargetResultTypeDef,
    DescribeMaintenanceWindowsRequestPaginateTypeDef,
    DescribeMaintenanceWindowsResultTypeDef,
    DescribeMaintenanceWindowTargetsRequestPaginateTypeDef,
    DescribeMaintenanceWindowTargetsResultTypeDef,
    DescribeMaintenanceWindowTasksRequestPaginateTypeDef,
    DescribeMaintenanceWindowTasksResultTypeDef,
    DescribeOpsItemsRequestPaginateTypeDef,
    DescribeOpsItemsResponseTypeDef,
    DescribeParametersRequestPaginateTypeDef,
    DescribeParametersResultTypeDef,
    DescribePatchBaselinesRequestPaginateTypeDef,
    DescribePatchBaselinesResultTypeDef,
    DescribePatchGroupsRequestPaginateTypeDef,
    DescribePatchGroupsResultTypeDef,
    DescribePatchPropertiesRequestPaginateTypeDef,
    DescribePatchPropertiesResultTypeDef,
    DescribeSessionsRequestPaginateTypeDef,
    DescribeSessionsResponseTypeDef,
    GetInventoryRequestPaginateTypeDef,
    GetInventoryResultTypeDef,
    GetInventorySchemaRequestPaginateTypeDef,
    GetInventorySchemaResultTypeDef,
    GetOpsSummaryRequestPaginateTypeDef,
    GetOpsSummaryResultTypeDef,
    GetParameterHistoryRequestPaginateTypeDef,
    GetParameterHistoryResultTypeDef,
    GetParametersByPathRequestPaginateTypeDef,
    GetParametersByPathResultTypeDef,
    GetResourcePoliciesRequestPaginateTypeDef,
    GetResourcePoliciesResponseTypeDef,
    ListAssociationsRequestPaginateTypeDef,
    ListAssociationsResultTypeDef,
    ListAssociationVersionsRequestPaginateTypeDef,
    ListAssociationVersionsResultTypeDef,
    ListCommandInvocationsRequestPaginateTypeDef,
    ListCommandInvocationsResultTypeDef,
    ListCommandsRequestPaginateTypeDef,
    ListCommandsResultTypeDef,
    ListComplianceItemsRequestPaginateTypeDef,
    ListComplianceItemsResultTypeDef,
    ListComplianceSummariesRequestPaginateTypeDef,
    ListComplianceSummariesResultTypeDef,
    ListDocumentsRequestPaginateTypeDef,
    ListDocumentsResultTypeDef,
    ListDocumentVersionsRequestPaginateTypeDef,
    ListDocumentVersionsResultTypeDef,
    ListNodesRequestPaginateTypeDef,
    ListNodesResultTypeDef,
    ListNodesSummaryRequestPaginateTypeDef,
    ListNodesSummaryResultTypeDef,
    ListOpsItemEventsRequestPaginateTypeDef,
    ListOpsItemEventsResponseTypeDef,
    ListOpsItemRelatedItemsRequestPaginateTypeDef,
    ListOpsItemRelatedItemsResponseTypeDef,
    ListOpsMetadataRequestPaginateTypeDef,
    ListOpsMetadataResultTypeDef,
    ListResourceComplianceSummariesRequestPaginateTypeDef,
    ListResourceComplianceSummariesResultTypeDef,
    ListResourceDataSyncRequestPaginateTypeDef,
    ListResourceDataSyncResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeActivationsPaginator",
    "DescribeAssociationExecutionTargetsPaginator",
    "DescribeAssociationExecutionsPaginator",
    "DescribeAutomationExecutionsPaginator",
    "DescribeAutomationStepExecutionsPaginator",
    "DescribeAvailablePatchesPaginator",
    "DescribeEffectiveInstanceAssociationsPaginator",
    "DescribeEffectivePatchesForPatchBaselinePaginator",
    "DescribeInstanceAssociationsStatusPaginator",
    "DescribeInstanceInformationPaginator",
    "DescribeInstancePatchStatesForPatchGroupPaginator",
    "DescribeInstancePatchStatesPaginator",
    "DescribeInstancePatchesPaginator",
    "DescribeInstancePropertiesPaginator",
    "DescribeInventoryDeletionsPaginator",
    "DescribeMaintenanceWindowExecutionTaskInvocationsPaginator",
    "DescribeMaintenanceWindowExecutionTasksPaginator",
    "DescribeMaintenanceWindowExecutionsPaginator",
    "DescribeMaintenanceWindowSchedulePaginator",
    "DescribeMaintenanceWindowTargetsPaginator",
    "DescribeMaintenanceWindowTasksPaginator",
    "DescribeMaintenanceWindowsForTargetPaginator",
    "DescribeMaintenanceWindowsPaginator",
    "DescribeOpsItemsPaginator",
    "DescribeParametersPaginator",
    "DescribePatchBaselinesPaginator",
    "DescribePatchGroupsPaginator",
    "DescribePatchPropertiesPaginator",
    "DescribeSessionsPaginator",
    "GetInventoryPaginator",
    "GetInventorySchemaPaginator",
    "GetOpsSummaryPaginator",
    "GetParameterHistoryPaginator",
    "GetParametersByPathPaginator",
    "GetResourcePoliciesPaginator",
    "ListAssociationVersionsPaginator",
    "ListAssociationsPaginator",
    "ListCommandInvocationsPaginator",
    "ListCommandsPaginator",
    "ListComplianceItemsPaginator",
    "ListComplianceSummariesPaginator",
    "ListDocumentVersionsPaginator",
    "ListDocumentsPaginator",
    "ListNodesPaginator",
    "ListNodesSummaryPaginator",
    "ListOpsItemEventsPaginator",
    "ListOpsItemRelatedItemsPaginator",
    "ListOpsMetadataPaginator",
    "ListResourceComplianceSummariesPaginator",
    "ListResourceDataSyncPaginator",
)


if TYPE_CHECKING:
    _DescribeActivationsPaginatorBase = AioPaginator[DescribeActivationsResultTypeDef]
else:
    _DescribeActivationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeActivationsPaginator(_DescribeActivationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeActivations.html#SSM.Paginator.DescribeActivations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeactivationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeActivationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeActivationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeActivations.html#SSM.Paginator.DescribeActivations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeactivationspaginator)
        """


if TYPE_CHECKING:
    _DescribeAssociationExecutionTargetsPaginatorBase = AioPaginator[
        DescribeAssociationExecutionTargetsResultTypeDef
    ]
else:
    _DescribeAssociationExecutionTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAssociationExecutionTargetsPaginator(
    _DescribeAssociationExecutionTargetsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutionTargets.html#SSM.Paginator.DescribeAssociationExecutionTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutiontargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssociationExecutionTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAssociationExecutionTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutionTargets.html#SSM.Paginator.DescribeAssociationExecutionTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutiontargetspaginator)
        """


if TYPE_CHECKING:
    _DescribeAssociationExecutionsPaginatorBase = AioPaginator[
        DescribeAssociationExecutionsResultTypeDef
    ]
else:
    _DescribeAssociationExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAssociationExecutionsPaginator(_DescribeAssociationExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutions.html#SSM.Paginator.DescribeAssociationExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAssociationExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAssociationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAssociationExecutions.html#SSM.Paginator.DescribeAssociationExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeassociationexecutionspaginator)
        """


if TYPE_CHECKING:
    _DescribeAutomationExecutionsPaginatorBase = AioPaginator[
        DescribeAutomationExecutionsResultTypeDef
    ]
else:
    _DescribeAutomationExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAutomationExecutionsPaginator(_DescribeAutomationExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationExecutions.html#SSM.Paginator.DescribeAutomationExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAutomationExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAutomationExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationExecutions.html#SSM.Paginator.DescribeAutomationExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationexecutionspaginator)
        """


if TYPE_CHECKING:
    _DescribeAutomationStepExecutionsPaginatorBase = AioPaginator[
        DescribeAutomationStepExecutionsResultTypeDef
    ]
else:
    _DescribeAutomationStepExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAutomationStepExecutionsPaginator(_DescribeAutomationStepExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationStepExecutions.html#SSM.Paginator.DescribeAutomationStepExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationstepexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAutomationStepExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAutomationStepExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAutomationStepExecutions.html#SSM.Paginator.DescribeAutomationStepExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeautomationstepexecutionspaginator)
        """


if TYPE_CHECKING:
    _DescribeAvailablePatchesPaginatorBase = AioPaginator[DescribeAvailablePatchesResultTypeDef]
else:
    _DescribeAvailablePatchesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeAvailablePatchesPaginator(_DescribeAvailablePatchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAvailablePatches.html#SSM.Paginator.DescribeAvailablePatches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeavailablepatchespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeAvailablePatchesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeAvailablePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeAvailablePatches.html#SSM.Paginator.DescribeAvailablePatches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeavailablepatchespaginator)
        """


if TYPE_CHECKING:
    _DescribeEffectiveInstanceAssociationsPaginatorBase = AioPaginator[
        DescribeEffectiveInstanceAssociationsResultTypeDef
    ]
else:
    _DescribeEffectiveInstanceAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEffectiveInstanceAssociationsPaginator(
    _DescribeEffectiveInstanceAssociationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectiveInstanceAssociations.html#SSM.Paginator.DescribeEffectiveInstanceAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEffectiveInstanceAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEffectiveInstanceAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectiveInstanceAssociations.html#SSM.Paginator.DescribeEffectiveInstanceAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectiveinstanceassociationspaginator)
        """


if TYPE_CHECKING:
    _DescribeEffectivePatchesForPatchBaselinePaginatorBase = AioPaginator[
        DescribeEffectivePatchesForPatchBaselineResultTypeDef
    ]
else:
    _DescribeEffectivePatchesForPatchBaselinePaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeEffectivePatchesForPatchBaselinePaginator(
    _DescribeEffectivePatchesForPatchBaselinePaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectivePatchesForPatchBaseline.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeEffectivePatchesForPatchBaselineRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeEffectivePatchesForPatchBaselineResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeEffectivePatchesForPatchBaseline.html#SSM.Paginator.DescribeEffectivePatchesForPatchBaseline.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeeffectivepatchesforpatchbaselinepaginator)
        """


if TYPE_CHECKING:
    _DescribeInstanceAssociationsStatusPaginatorBase = AioPaginator[
        DescribeInstanceAssociationsStatusResultTypeDef
    ]
else:
    _DescribeInstanceAssociationsStatusPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInstanceAssociationsStatusPaginator(_DescribeInstanceAssociationsStatusPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceAssociationsStatus.html#SSM.Paginator.DescribeInstanceAssociationsStatus)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceassociationsstatuspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstanceAssociationsStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstanceAssociationsStatusResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceAssociationsStatus.html#SSM.Paginator.DescribeInstanceAssociationsStatus.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceassociationsstatuspaginator)
        """


if TYPE_CHECKING:
    _DescribeInstanceInformationPaginatorBase = AioPaginator[
        DescribeInstanceInformationResultTypeDef
    ]
else:
    _DescribeInstanceInformationPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInstanceInformationPaginator(_DescribeInstanceInformationPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceInformation.html#SSM.Paginator.DescribeInstanceInformation)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceinformationpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstanceInformationRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstanceInformationResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceInformation.html#SSM.Paginator.DescribeInstanceInformation.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstanceinformationpaginator)
        """


if TYPE_CHECKING:
    _DescribeInstancePatchStatesForPatchGroupPaginatorBase = AioPaginator[
        DescribeInstancePatchStatesForPatchGroupResultTypeDef
    ]
else:
    _DescribeInstancePatchStatesForPatchGroupPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInstancePatchStatesForPatchGroupPaginator(
    _DescribeInstancePatchStatesForPatchGroupPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStatesForPatchGroup.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancePatchStatesForPatchGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstancePatchStatesForPatchGroupResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStatesForPatchGroup.html#SSM.Paginator.DescribeInstancePatchStatesForPatchGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatesforpatchgrouppaginator)
        """


if TYPE_CHECKING:
    _DescribeInstancePatchStatesPaginatorBase = AioPaginator[
        DescribeInstancePatchStatesResultTypeDef
    ]
else:
    _DescribeInstancePatchStatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInstancePatchStatesPaginator(_DescribeInstancePatchStatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStates.html#SSM.Paginator.DescribeInstancePatchStates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancePatchStatesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstancePatchStatesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatchStates.html#SSM.Paginator.DescribeInstancePatchStates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchstatespaginator)
        """


if TYPE_CHECKING:
    _DescribeInstancePatchesPaginatorBase = AioPaginator[DescribeInstancePatchesResultTypeDef]
else:
    _DescribeInstancePatchesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInstancePatchesPaginator(_DescribeInstancePatchesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatches.html#SSM.Paginator.DescribeInstancePatches)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancePatchesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstancePatchesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstancePatches.html#SSM.Paginator.DescribeInstancePatches.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepatchespaginator)
        """


if TYPE_CHECKING:
    _DescribeInstancePropertiesPaginatorBase = AioPaginator[DescribeInstancePropertiesResultTypeDef]
else:
    _DescribeInstancePropertiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInstancePropertiesPaginator(_DescribeInstancePropertiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceProperties.html#SSM.Paginator.DescribeInstanceProperties)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepropertiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInstancePropertiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInstancePropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInstanceProperties.html#SSM.Paginator.DescribeInstanceProperties.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinstancepropertiespaginator)
        """


if TYPE_CHECKING:
    _DescribeInventoryDeletionsPaginatorBase = AioPaginator[DescribeInventoryDeletionsResultTypeDef]
else:
    _DescribeInventoryDeletionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeInventoryDeletionsPaginator(_DescribeInventoryDeletionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInventoryDeletions.html#SSM.Paginator.DescribeInventoryDeletions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinventorydeletionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeInventoryDeletionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeInventoryDeletionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeInventoryDeletions.html#SSM.Paginator.DescribeInventoryDeletions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeinventorydeletionspaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowExecutionTaskInvocationsPaginatorBase = AioPaginator[
        DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowExecutionTaskInvocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowExecutionTaskInvocationsPaginator(
    _DescribeMaintenanceWindowExecutionTaskInvocationsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTaskInvocations.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self,
        **kwargs: Unpack[DescribeMaintenanceWindowExecutionTaskInvocationsRequestPaginateTypeDef],
    ) -> AioPageIterator[DescribeMaintenanceWindowExecutionTaskInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTaskInvocations.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTaskInvocations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskinvocationspaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowExecutionTasksPaginatorBase = AioPaginator[
        DescribeMaintenanceWindowExecutionTasksResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowExecutionTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowExecutionTasksPaginator(
    _DescribeMaintenanceWindowExecutionTasksPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTasks.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowExecutionTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowExecutionTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutionTasks.html#SSM.Paginator.DescribeMaintenanceWindowExecutionTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutiontaskspaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowExecutionsPaginatorBase = AioPaginator[
        DescribeMaintenanceWindowExecutionsResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowExecutionsPaginator(
    _DescribeMaintenanceWindowExecutionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutions.html#SSM.Paginator.DescribeMaintenanceWindowExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowExecutionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowExecutions.html#SSM.Paginator.DescribeMaintenanceWindowExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowexecutionspaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowSchedulePaginatorBase = AioPaginator[
        DescribeMaintenanceWindowScheduleResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowSchedulePaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowSchedulePaginator(_DescribeMaintenanceWindowSchedulePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowSchedule.html#SSM.Paginator.DescribeMaintenanceWindowSchedule)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowschedulepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowScheduleRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowScheduleResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowSchedule.html#SSM.Paginator.DescribeMaintenanceWindowSchedule.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowschedulepaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowTargetsPaginatorBase = AioPaginator[
        DescribeMaintenanceWindowTargetsResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowTargetsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowTargetsPaginator(_DescribeMaintenanceWindowTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTargets.html#SSM.Paginator.DescribeMaintenanceWindowTargets)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtargetspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowTargetsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowTargetsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTargets.html#SSM.Paginator.DescribeMaintenanceWindowTargets.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtargetspaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowTasksPaginatorBase = AioPaginator[
        DescribeMaintenanceWindowTasksResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowTasksPaginator(_DescribeMaintenanceWindowTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTasks.html#SSM.Paginator.DescribeMaintenanceWindowTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowTasksResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowTasks.html#SSM.Paginator.DescribeMaintenanceWindowTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowtaskspaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowsForTargetPaginatorBase = AioPaginator[
        DescribeMaintenanceWindowsForTargetResultTypeDef
    ]
else:
    _DescribeMaintenanceWindowsForTargetPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowsForTargetPaginator(
    _DescribeMaintenanceWindowsForTargetPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowsForTarget.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowsForTargetRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowsForTargetResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindowsForTarget.html#SSM.Paginator.DescribeMaintenanceWindowsForTarget.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowsfortargetpaginator)
        """


if TYPE_CHECKING:
    _DescribeMaintenanceWindowsPaginatorBase = AioPaginator[DescribeMaintenanceWindowsResultTypeDef]
else:
    _DescribeMaintenanceWindowsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeMaintenanceWindowsPaginator(_DescribeMaintenanceWindowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindows.html#SSM.Paginator.DescribeMaintenanceWindows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeMaintenanceWindowsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeMaintenanceWindowsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeMaintenanceWindows.html#SSM.Paginator.DescribeMaintenanceWindows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describemaintenancewindowspaginator)
        """


if TYPE_CHECKING:
    _DescribeOpsItemsPaginatorBase = AioPaginator[DescribeOpsItemsResponseTypeDef]
else:
    _DescribeOpsItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeOpsItemsPaginator(_DescribeOpsItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeOpsItems.html#SSM.Paginator.DescribeOpsItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeopsitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeOpsItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeOpsItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeOpsItems.html#SSM.Paginator.DescribeOpsItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeopsitemspaginator)
        """


if TYPE_CHECKING:
    _DescribeParametersPaginatorBase = AioPaginator[DescribeParametersResultTypeDef]
else:
    _DescribeParametersPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeParametersPaginator(_DescribeParametersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeParameters.html#SSM.Paginator.DescribeParameters)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeparameterspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeParametersRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeParametersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeParameters.html#SSM.Paginator.DescribeParameters.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describeparameterspaginator)
        """


if TYPE_CHECKING:
    _DescribePatchBaselinesPaginatorBase = AioPaginator[DescribePatchBaselinesResultTypeDef]
else:
    _DescribePatchBaselinesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePatchBaselinesPaginator(_DescribePatchBaselinesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchBaselines.html#SSM.Paginator.DescribePatchBaselines)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchbaselinespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePatchBaselinesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribePatchBaselinesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchBaselines.html#SSM.Paginator.DescribePatchBaselines.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchbaselinespaginator)
        """


if TYPE_CHECKING:
    _DescribePatchGroupsPaginatorBase = AioPaginator[DescribePatchGroupsResultTypeDef]
else:
    _DescribePatchGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePatchGroupsPaginator(_DescribePatchGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchGroups.html#SSM.Paginator.DescribePatchGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchgroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePatchGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribePatchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchGroups.html#SSM.Paginator.DescribePatchGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchgroupspaginator)
        """


if TYPE_CHECKING:
    _DescribePatchPropertiesPaginatorBase = AioPaginator[DescribePatchPropertiesResultTypeDef]
else:
    _DescribePatchPropertiesPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribePatchPropertiesPaginator(_DescribePatchPropertiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchProperties.html#SSM.Paginator.DescribePatchProperties)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchpropertiespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribePatchPropertiesRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribePatchPropertiesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribePatchProperties.html#SSM.Paginator.DescribePatchProperties.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describepatchpropertiespaginator)
        """


if TYPE_CHECKING:
    _DescribeSessionsPaginatorBase = AioPaginator[DescribeSessionsResponseTypeDef]
else:
    _DescribeSessionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class DescribeSessionsPaginator(_DescribeSessionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeSessions.html#SSM.Paginator.DescribeSessions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describesessionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[DescribeSessionsRequestPaginateTypeDef]
    ) -> AioPageIterator[DescribeSessionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/DescribeSessions.html#SSM.Paginator.DescribeSessions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#describesessionspaginator)
        """


if TYPE_CHECKING:
    _GetInventoryPaginatorBase = AioPaginator[GetInventoryResultTypeDef]
else:
    _GetInventoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetInventoryPaginator(_GetInventoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventory.html#SSM.Paginator.GetInventory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetInventoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetInventoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventory.html#SSM.Paginator.GetInventory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventorypaginator)
        """


if TYPE_CHECKING:
    _GetInventorySchemaPaginatorBase = AioPaginator[GetInventorySchemaResultTypeDef]
else:
    _GetInventorySchemaPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetInventorySchemaPaginator(_GetInventorySchemaPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventorySchema.html#SSM.Paginator.GetInventorySchema)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventoryschemapaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetInventorySchemaRequestPaginateTypeDef]
    ) -> AioPageIterator[GetInventorySchemaResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetInventorySchema.html#SSM.Paginator.GetInventorySchema.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getinventoryschemapaginator)
        """


if TYPE_CHECKING:
    _GetOpsSummaryPaginatorBase = AioPaginator[GetOpsSummaryResultTypeDef]
else:
    _GetOpsSummaryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetOpsSummaryPaginator(_GetOpsSummaryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetOpsSummary.html#SSM.Paginator.GetOpsSummary)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getopssummarypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetOpsSummaryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetOpsSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetOpsSummary.html#SSM.Paginator.GetOpsSummary.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getopssummarypaginator)
        """


if TYPE_CHECKING:
    _GetParameterHistoryPaginatorBase = AioPaginator[GetParameterHistoryResultTypeDef]
else:
    _GetParameterHistoryPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetParameterHistoryPaginator(_GetParameterHistoryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParameterHistory.html#SSM.Paginator.GetParameterHistory)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparameterhistorypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetParameterHistoryRequestPaginateTypeDef]
    ) -> AioPageIterator[GetParameterHistoryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParameterHistory.html#SSM.Paginator.GetParameterHistory.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparameterhistorypaginator)
        """


if TYPE_CHECKING:
    _GetParametersByPathPaginatorBase = AioPaginator[GetParametersByPathResultTypeDef]
else:
    _GetParametersByPathPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetParametersByPathPaginator(_GetParametersByPathPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParametersByPath.html#SSM.Paginator.GetParametersByPath)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparametersbypathpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetParametersByPathRequestPaginateTypeDef]
    ) -> AioPageIterator[GetParametersByPathResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetParametersByPath.html#SSM.Paginator.GetParametersByPath.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getparametersbypathpaginator)
        """


if TYPE_CHECKING:
    _GetResourcePoliciesPaginatorBase = AioPaginator[GetResourcePoliciesResponseTypeDef]
else:
    _GetResourcePoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetResourcePoliciesPaginator(_GetResourcePoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetResourcePolicies.html#SSM.Paginator.GetResourcePolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getresourcepoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetResourcePoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetResourcePoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/GetResourcePolicies.html#SSM.Paginator.GetResourcePolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#getresourcepoliciespaginator)
        """


if TYPE_CHECKING:
    _ListAssociationVersionsPaginatorBase = AioPaginator[ListAssociationVersionsResultTypeDef]
else:
    _ListAssociationVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociationVersionsPaginator(_ListAssociationVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociationVersions.html#SSM.Paginator.ListAssociationVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociationVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociationVersions.html#SSM.Paginator.ListAssociationVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationversionspaginator)
        """


if TYPE_CHECKING:
    _ListAssociationsPaginatorBase = AioPaginator[ListAssociationsResultTypeDef]
else:
    _ListAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAssociationsPaginator(_ListAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociations.html#SSM.Paginator.ListAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAssociationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListAssociations.html#SSM.Paginator.ListAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listassociationspaginator)
        """


if TYPE_CHECKING:
    _ListCommandInvocationsPaginatorBase = AioPaginator[ListCommandInvocationsResultTypeDef]
else:
    _ListCommandInvocationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCommandInvocationsPaginator(_ListCommandInvocationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommandInvocations.html#SSM.Paginator.ListCommandInvocations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandinvocationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommandInvocationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommandInvocationsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommandInvocations.html#SSM.Paginator.ListCommandInvocations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandinvocationspaginator)
        """


if TYPE_CHECKING:
    _ListCommandsPaginatorBase = AioPaginator[ListCommandsResultTypeDef]
else:
    _ListCommandsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCommandsPaginator(_ListCommandsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommands.html#SSM.Paginator.ListCommands)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommandsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommandsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListCommands.html#SSM.Paginator.ListCommands.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcommandspaginator)
        """


if TYPE_CHECKING:
    _ListComplianceItemsPaginatorBase = AioPaginator[ListComplianceItemsResultTypeDef]
else:
    _ListComplianceItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListComplianceItemsPaginator(_ListComplianceItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceItems.html#SSM.Paginator.ListComplianceItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcomplianceitemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComplianceItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComplianceItemsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceItems.html#SSM.Paginator.ListComplianceItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcomplianceitemspaginator)
        """


if TYPE_CHECKING:
    _ListComplianceSummariesPaginatorBase = AioPaginator[ListComplianceSummariesResultTypeDef]
else:
    _ListComplianceSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListComplianceSummariesPaginator(_ListComplianceSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceSummaries.html#SSM.Paginator.ListComplianceSummaries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcompliancesummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListComplianceSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListComplianceSummaries.html#SSM.Paginator.ListComplianceSummaries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listcompliancesummariespaginator)
        """


if TYPE_CHECKING:
    _ListDocumentVersionsPaginatorBase = AioPaginator[ListDocumentVersionsResultTypeDef]
else:
    _ListDocumentVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDocumentVersionsPaginator(_ListDocumentVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocumentVersions.html#SSM.Paginator.ListDocumentVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDocumentVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDocumentVersionsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocumentVersions.html#SSM.Paginator.ListDocumentVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentversionspaginator)
        """


if TYPE_CHECKING:
    _ListDocumentsPaginatorBase = AioPaginator[ListDocumentsResultTypeDef]
else:
    _ListDocumentsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDocumentsPaginator(_ListDocumentsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocuments.html#SSM.Paginator.ListDocuments)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDocumentsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDocumentsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListDocuments.html#SSM.Paginator.ListDocuments.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listdocumentspaginator)
        """


if TYPE_CHECKING:
    _ListNodesPaginatorBase = AioPaginator[ListNodesResultTypeDef]
else:
    _ListNodesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNodesPaginator(_ListNodesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodes.html#SSM.Paginator.ListNodes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listnodespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNodesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNodesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodes.html#SSM.Paginator.ListNodes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listnodespaginator)
        """


if TYPE_CHECKING:
    _ListNodesSummaryPaginatorBase = AioPaginator[ListNodesSummaryResultTypeDef]
else:
    _ListNodesSummaryPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListNodesSummaryPaginator(_ListNodesSummaryPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodesSummary.html#SSM.Paginator.ListNodesSummary)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listnodessummarypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListNodesSummaryRequestPaginateTypeDef]
    ) -> AioPageIterator[ListNodesSummaryResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListNodesSummary.html#SSM.Paginator.ListNodesSummary.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listnodessummarypaginator)
        """


if TYPE_CHECKING:
    _ListOpsItemEventsPaginatorBase = AioPaginator[ListOpsItemEventsResponseTypeDef]
else:
    _ListOpsItemEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOpsItemEventsPaginator(_ListOpsItemEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemEvents.html#SSM.Paginator.ListOpsItemEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpsItemEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOpsItemEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemEvents.html#SSM.Paginator.ListOpsItemEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemeventspaginator)
        """


if TYPE_CHECKING:
    _ListOpsItemRelatedItemsPaginatorBase = AioPaginator[ListOpsItemRelatedItemsResponseTypeDef]
else:
    _ListOpsItemRelatedItemsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOpsItemRelatedItemsPaginator(_ListOpsItemRelatedItemsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemRelatedItems.html#SSM.Paginator.ListOpsItemRelatedItems)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemrelateditemspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpsItemRelatedItemsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOpsItemRelatedItemsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsItemRelatedItems.html#SSM.Paginator.ListOpsItemRelatedItems.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsitemrelateditemspaginator)
        """


if TYPE_CHECKING:
    _ListOpsMetadataPaginatorBase = AioPaginator[ListOpsMetadataResultTypeDef]
else:
    _ListOpsMetadataPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOpsMetadataPaginator(_ListOpsMetadataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsMetadata.html#SSM.Paginator.ListOpsMetadata)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsmetadatapaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOpsMetadataRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOpsMetadataResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListOpsMetadata.html#SSM.Paginator.ListOpsMetadata.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listopsmetadatapaginator)
        """


if TYPE_CHECKING:
    _ListResourceComplianceSummariesPaginatorBase = AioPaginator[
        ListResourceComplianceSummariesResultTypeDef
    ]
else:
    _ListResourceComplianceSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceComplianceSummariesPaginator(_ListResourceComplianceSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceComplianceSummaries.html#SSM.Paginator.ListResourceComplianceSummaries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcecompliancesummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceComplianceSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceComplianceSummariesResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceComplianceSummaries.html#SSM.Paginator.ListResourceComplianceSummaries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcecompliancesummariespaginator)
        """


if TYPE_CHECKING:
    _ListResourceDataSyncPaginatorBase = AioPaginator[ListResourceDataSyncResultTypeDef]
else:
    _ListResourceDataSyncPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListResourceDataSyncPaginator(_ListResourceDataSyncPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceDataSync.html#SSM.Paginator.ListResourceDataSync)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcedatasyncpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListResourceDataSyncRequestPaginateTypeDef]
    ) -> AioPageIterator[ListResourceDataSyncResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/paginator/ListResourceDataSync.html#SSM.Paginator.ListResourceDataSync.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ssm/paginators/#listresourcedatasyncpaginator)
        """
