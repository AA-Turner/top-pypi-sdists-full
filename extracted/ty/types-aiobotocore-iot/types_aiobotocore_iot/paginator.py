"""
Type annotations for iot service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_iot.client import IoTClient
    from types_aiobotocore_iot.paginator import (
        GetBehaviorModelTrainingSummariesPaginator,
        ListActiveViolationsPaginator,
        ListAttachedPoliciesPaginator,
        ListAuditFindingsPaginator,
        ListAuditMitigationActionsExecutionsPaginator,
        ListAuditMitigationActionsTasksPaginator,
        ListAuditSuppressionsPaginator,
        ListAuditTasksPaginator,
        ListAuthorizersPaginator,
        ListBillingGroupsPaginator,
        ListCACertificatesPaginator,
        ListCertificatesByCAPaginator,
        ListCertificatesPaginator,
        ListCommandExecutionsPaginator,
        ListCommandsPaginator,
        ListCustomMetricsPaginator,
        ListDetectMitigationActionsExecutionsPaginator,
        ListDetectMitigationActionsTasksPaginator,
        ListDimensionsPaginator,
        ListDomainConfigurationsPaginator,
        ListFleetMetricsPaginator,
        ListIndicesPaginator,
        ListJobExecutionsForJobPaginator,
        ListJobExecutionsForThingPaginator,
        ListJobTemplatesPaginator,
        ListJobsPaginator,
        ListManagedJobTemplatesPaginator,
        ListMetricValuesPaginator,
        ListMitigationActionsPaginator,
        ListOTAUpdatesPaginator,
        ListOutgoingCertificatesPaginator,
        ListPackageVersionsPaginator,
        ListPackagesPaginator,
        ListPoliciesPaginator,
        ListPolicyPrincipalsPaginator,
        ListPrincipalPoliciesPaginator,
        ListPrincipalThingsPaginator,
        ListPrincipalThingsV2Paginator,
        ListProvisioningTemplateVersionsPaginator,
        ListProvisioningTemplatesPaginator,
        ListRelatedResourcesForAuditFindingPaginator,
        ListRoleAliasesPaginator,
        ListSbomValidationResultsPaginator,
        ListScheduledAuditsPaginator,
        ListSecurityProfilesForTargetPaginator,
        ListSecurityProfilesPaginator,
        ListStreamsPaginator,
        ListTagsForResourcePaginator,
        ListTargetsForPolicyPaginator,
        ListTargetsForSecurityProfilePaginator,
        ListThingGroupsForThingPaginator,
        ListThingGroupsPaginator,
        ListThingPrincipalsPaginator,
        ListThingPrincipalsV2Paginator,
        ListThingRegistrationTaskReportsPaginator,
        ListThingRegistrationTasksPaginator,
        ListThingTypesPaginator,
        ListThingsInBillingGroupPaginator,
        ListThingsInThingGroupPaginator,
        ListThingsPaginator,
        ListTopicRuleDestinationsPaginator,
        ListTopicRulesPaginator,
        ListV2LoggingLevelsPaginator,
        ListViolationEventsPaginator,
    )

    session = get_session()
    with session.create_client("iot") as client:
        client: IoTClient

        get_behavior_model_training_summaries_paginator: GetBehaviorModelTrainingSummariesPaginator = client.get_paginator("get_behavior_model_training_summaries")
        list_active_violations_paginator: ListActiveViolationsPaginator = client.get_paginator("list_active_violations")
        list_attached_policies_paginator: ListAttachedPoliciesPaginator = client.get_paginator("list_attached_policies")
        list_audit_findings_paginator: ListAuditFindingsPaginator = client.get_paginator("list_audit_findings")
        list_audit_mitigation_actions_executions_paginator: ListAuditMitigationActionsExecutionsPaginator = client.get_paginator("list_audit_mitigation_actions_executions")
        list_audit_mitigation_actions_tasks_paginator: ListAuditMitigationActionsTasksPaginator = client.get_paginator("list_audit_mitigation_actions_tasks")
        list_audit_suppressions_paginator: ListAuditSuppressionsPaginator = client.get_paginator("list_audit_suppressions")
        list_audit_tasks_paginator: ListAuditTasksPaginator = client.get_paginator("list_audit_tasks")
        list_authorizers_paginator: ListAuthorizersPaginator = client.get_paginator("list_authorizers")
        list_billing_groups_paginator: ListBillingGroupsPaginator = client.get_paginator("list_billing_groups")
        list_ca_certificates_paginator: ListCACertificatesPaginator = client.get_paginator("list_ca_certificates")
        list_certificates_by_ca_paginator: ListCertificatesByCAPaginator = client.get_paginator("list_certificates_by_ca")
        list_certificates_paginator: ListCertificatesPaginator = client.get_paginator("list_certificates")
        list_command_executions_paginator: ListCommandExecutionsPaginator = client.get_paginator("list_command_executions")
        list_commands_paginator: ListCommandsPaginator = client.get_paginator("list_commands")
        list_custom_metrics_paginator: ListCustomMetricsPaginator = client.get_paginator("list_custom_metrics")
        list_detect_mitigation_actions_executions_paginator: ListDetectMitigationActionsExecutionsPaginator = client.get_paginator("list_detect_mitigation_actions_executions")
        list_detect_mitigation_actions_tasks_paginator: ListDetectMitigationActionsTasksPaginator = client.get_paginator("list_detect_mitigation_actions_tasks")
        list_dimensions_paginator: ListDimensionsPaginator = client.get_paginator("list_dimensions")
        list_domain_configurations_paginator: ListDomainConfigurationsPaginator = client.get_paginator("list_domain_configurations")
        list_fleet_metrics_paginator: ListFleetMetricsPaginator = client.get_paginator("list_fleet_metrics")
        list_indices_paginator: ListIndicesPaginator = client.get_paginator("list_indices")
        list_job_executions_for_job_paginator: ListJobExecutionsForJobPaginator = client.get_paginator("list_job_executions_for_job")
        list_job_executions_for_thing_paginator: ListJobExecutionsForThingPaginator = client.get_paginator("list_job_executions_for_thing")
        list_job_templates_paginator: ListJobTemplatesPaginator = client.get_paginator("list_job_templates")
        list_jobs_paginator: ListJobsPaginator = client.get_paginator("list_jobs")
        list_managed_job_templates_paginator: ListManagedJobTemplatesPaginator = client.get_paginator("list_managed_job_templates")
        list_metric_values_paginator: ListMetricValuesPaginator = client.get_paginator("list_metric_values")
        list_mitigation_actions_paginator: ListMitigationActionsPaginator = client.get_paginator("list_mitigation_actions")
        list_ota_updates_paginator: ListOTAUpdatesPaginator = client.get_paginator("list_ota_updates")
        list_outgoing_certificates_paginator: ListOutgoingCertificatesPaginator = client.get_paginator("list_outgoing_certificates")
        list_package_versions_paginator: ListPackageVersionsPaginator = client.get_paginator("list_package_versions")
        list_packages_paginator: ListPackagesPaginator = client.get_paginator("list_packages")
        list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
        list_policy_principals_paginator: ListPolicyPrincipalsPaginator = client.get_paginator("list_policy_principals")
        list_principal_policies_paginator: ListPrincipalPoliciesPaginator = client.get_paginator("list_principal_policies")
        list_principal_things_paginator: ListPrincipalThingsPaginator = client.get_paginator("list_principal_things")
        list_principal_things_v2_paginator: ListPrincipalThingsV2Paginator = client.get_paginator("list_principal_things_v2")
        list_provisioning_template_versions_paginator: ListProvisioningTemplateVersionsPaginator = client.get_paginator("list_provisioning_template_versions")
        list_provisioning_templates_paginator: ListProvisioningTemplatesPaginator = client.get_paginator("list_provisioning_templates")
        list_related_resources_for_audit_finding_paginator: ListRelatedResourcesForAuditFindingPaginator = client.get_paginator("list_related_resources_for_audit_finding")
        list_role_aliases_paginator: ListRoleAliasesPaginator = client.get_paginator("list_role_aliases")
        list_sbom_validation_results_paginator: ListSbomValidationResultsPaginator = client.get_paginator("list_sbom_validation_results")
        list_scheduled_audits_paginator: ListScheduledAuditsPaginator = client.get_paginator("list_scheduled_audits")
        list_security_profiles_for_target_paginator: ListSecurityProfilesForTargetPaginator = client.get_paginator("list_security_profiles_for_target")
        list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
        list_streams_paginator: ListStreamsPaginator = client.get_paginator("list_streams")
        list_tags_for_resource_paginator: ListTagsForResourcePaginator = client.get_paginator("list_tags_for_resource")
        list_targets_for_policy_paginator: ListTargetsForPolicyPaginator = client.get_paginator("list_targets_for_policy")
        list_targets_for_security_profile_paginator: ListTargetsForSecurityProfilePaginator = client.get_paginator("list_targets_for_security_profile")
        list_thing_groups_for_thing_paginator: ListThingGroupsForThingPaginator = client.get_paginator("list_thing_groups_for_thing")
        list_thing_groups_paginator: ListThingGroupsPaginator = client.get_paginator("list_thing_groups")
        list_thing_principals_paginator: ListThingPrincipalsPaginator = client.get_paginator("list_thing_principals")
        list_thing_principals_v2_paginator: ListThingPrincipalsV2Paginator = client.get_paginator("list_thing_principals_v2")
        list_thing_registration_task_reports_paginator: ListThingRegistrationTaskReportsPaginator = client.get_paginator("list_thing_registration_task_reports")
        list_thing_registration_tasks_paginator: ListThingRegistrationTasksPaginator = client.get_paginator("list_thing_registration_tasks")
        list_thing_types_paginator: ListThingTypesPaginator = client.get_paginator("list_thing_types")
        list_things_in_billing_group_paginator: ListThingsInBillingGroupPaginator = client.get_paginator("list_things_in_billing_group")
        list_things_in_thing_group_paginator: ListThingsInThingGroupPaginator = client.get_paginator("list_things_in_thing_group")
        list_things_paginator: ListThingsPaginator = client.get_paginator("list_things")
        list_topic_rule_destinations_paginator: ListTopicRuleDestinationsPaginator = client.get_paginator("list_topic_rule_destinations")
        list_topic_rules_paginator: ListTopicRulesPaginator = client.get_paginator("list_topic_rules")
        list_v2_logging_levels_paginator: ListV2LoggingLevelsPaginator = client.get_paginator("list_v2_logging_levels")
        list_violation_events_paginator: ListViolationEventsPaginator = client.get_paginator("list_violation_events")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetBehaviorModelTrainingSummariesRequestPaginateTypeDef,
    GetBehaviorModelTrainingSummariesResponseTypeDef,
    ListActiveViolationsRequestPaginateTypeDef,
    ListActiveViolationsResponseTypeDef,
    ListAttachedPoliciesRequestPaginateTypeDef,
    ListAttachedPoliciesResponseTypeDef,
    ListAuditFindingsRequestPaginateTypeDef,
    ListAuditFindingsResponseTypeDef,
    ListAuditMitigationActionsExecutionsRequestPaginateTypeDef,
    ListAuditMitigationActionsExecutionsResponseTypeDef,
    ListAuditMitigationActionsTasksRequestPaginateTypeDef,
    ListAuditMitigationActionsTasksResponseTypeDef,
    ListAuditSuppressionsRequestPaginateTypeDef,
    ListAuditSuppressionsResponseTypeDef,
    ListAuditTasksRequestPaginateTypeDef,
    ListAuditTasksResponseTypeDef,
    ListAuthorizersRequestPaginateTypeDef,
    ListAuthorizersResponseTypeDef,
    ListBillingGroupsRequestPaginateTypeDef,
    ListBillingGroupsResponseTypeDef,
    ListCACertificatesRequestPaginateTypeDef,
    ListCACertificatesResponseTypeDef,
    ListCertificatesByCARequestPaginateTypeDef,
    ListCertificatesByCAResponseTypeDef,
    ListCertificatesRequestPaginateTypeDef,
    ListCertificatesResponseTypeDef,
    ListCommandExecutionsRequestPaginateTypeDef,
    ListCommandExecutionsResponseTypeDef,
    ListCommandsRequestPaginateTypeDef,
    ListCommandsResponseTypeDef,
    ListCustomMetricsRequestPaginateTypeDef,
    ListCustomMetricsResponseTypeDef,
    ListDetectMitigationActionsExecutionsRequestPaginateTypeDef,
    ListDetectMitigationActionsExecutionsResponseTypeDef,
    ListDetectMitigationActionsTasksRequestPaginateTypeDef,
    ListDetectMitigationActionsTasksResponseTypeDef,
    ListDimensionsRequestPaginateTypeDef,
    ListDimensionsResponseTypeDef,
    ListDomainConfigurationsRequestPaginateTypeDef,
    ListDomainConfigurationsResponseTypeDef,
    ListFleetMetricsRequestPaginateTypeDef,
    ListFleetMetricsResponseTypeDef,
    ListIndicesRequestPaginateTypeDef,
    ListIndicesResponseTypeDef,
    ListJobExecutionsForJobRequestPaginateTypeDef,
    ListJobExecutionsForJobResponseTypeDef,
    ListJobExecutionsForThingRequestPaginateTypeDef,
    ListJobExecutionsForThingResponseTypeDef,
    ListJobsRequestPaginateTypeDef,
    ListJobsResponseTypeDef,
    ListJobTemplatesRequestPaginateTypeDef,
    ListJobTemplatesResponseTypeDef,
    ListManagedJobTemplatesRequestPaginateTypeDef,
    ListManagedJobTemplatesResponseTypeDef,
    ListMetricValuesRequestPaginateTypeDef,
    ListMetricValuesResponseTypeDef,
    ListMitigationActionsRequestPaginateTypeDef,
    ListMitigationActionsResponseTypeDef,
    ListOTAUpdatesRequestPaginateTypeDef,
    ListOTAUpdatesResponseTypeDef,
    ListOutgoingCertificatesRequestPaginateTypeDef,
    ListOutgoingCertificatesResponseTypeDef,
    ListPackagesRequestPaginateTypeDef,
    ListPackagesResponseTypeDef,
    ListPackageVersionsRequestPaginateTypeDef,
    ListPackageVersionsResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyPrincipalsRequestPaginateTypeDef,
    ListPolicyPrincipalsResponseTypeDef,
    ListPrincipalPoliciesRequestPaginateTypeDef,
    ListPrincipalPoliciesResponseTypeDef,
    ListPrincipalThingsRequestPaginateTypeDef,
    ListPrincipalThingsResponseTypeDef,
    ListPrincipalThingsV2RequestPaginateTypeDef,
    ListPrincipalThingsV2ResponseTypeDef,
    ListProvisioningTemplatesRequestPaginateTypeDef,
    ListProvisioningTemplatesResponseTypeDef,
    ListProvisioningTemplateVersionsRequestPaginateTypeDef,
    ListProvisioningTemplateVersionsResponseTypeDef,
    ListRelatedResourcesForAuditFindingRequestPaginateTypeDef,
    ListRelatedResourcesForAuditFindingResponseTypeDef,
    ListRoleAliasesRequestPaginateTypeDef,
    ListRoleAliasesResponseTypeDef,
    ListSbomValidationResultsRequestPaginateTypeDef,
    ListSbomValidationResultsResponseTypeDef,
    ListScheduledAuditsRequestPaginateTypeDef,
    ListScheduledAuditsResponseTypeDef,
    ListSecurityProfilesForTargetRequestPaginateTypeDef,
    ListSecurityProfilesForTargetResponseTypeDef,
    ListSecurityProfilesRequestPaginateTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListStreamsRequestPaginateTypeDef,
    ListStreamsResponseTypeDef,
    ListTagsForResourceRequestPaginateTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTargetsForPolicyRequestPaginateTypeDef,
    ListTargetsForPolicyResponseTypeDef,
    ListTargetsForSecurityProfileRequestPaginateTypeDef,
    ListTargetsForSecurityProfileResponseTypeDef,
    ListThingGroupsForThingRequestPaginateTypeDef,
    ListThingGroupsForThingResponseTypeDef,
    ListThingGroupsRequestPaginateTypeDef,
    ListThingGroupsResponseTypeDef,
    ListThingPrincipalsRequestPaginateTypeDef,
    ListThingPrincipalsResponseTypeDef,
    ListThingPrincipalsV2RequestPaginateTypeDef,
    ListThingPrincipalsV2ResponseTypeDef,
    ListThingRegistrationTaskReportsRequestPaginateTypeDef,
    ListThingRegistrationTaskReportsResponseTypeDef,
    ListThingRegistrationTasksRequestPaginateTypeDef,
    ListThingRegistrationTasksResponseTypeDef,
    ListThingsInBillingGroupRequestPaginateTypeDef,
    ListThingsInBillingGroupResponseTypeDef,
    ListThingsInThingGroupRequestPaginateTypeDef,
    ListThingsInThingGroupResponseTypeDef,
    ListThingsRequestPaginateTypeDef,
    ListThingsResponseTypeDef,
    ListThingTypesRequestPaginateTypeDef,
    ListThingTypesResponseTypeDef,
    ListTopicRuleDestinationsRequestPaginateTypeDef,
    ListTopicRuleDestinationsResponseTypeDef,
    ListTopicRulesRequestPaginateTypeDef,
    ListTopicRulesResponseTypeDef,
    ListV2LoggingLevelsRequestPaginateTypeDef,
    ListV2LoggingLevelsResponseTypeDef,
    ListViolationEventsRequestPaginateTypeDef,
    ListViolationEventsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "GetBehaviorModelTrainingSummariesPaginator",
    "ListActiveViolationsPaginator",
    "ListAttachedPoliciesPaginator",
    "ListAuditFindingsPaginator",
    "ListAuditMitigationActionsExecutionsPaginator",
    "ListAuditMitigationActionsTasksPaginator",
    "ListAuditSuppressionsPaginator",
    "ListAuditTasksPaginator",
    "ListAuthorizersPaginator",
    "ListBillingGroupsPaginator",
    "ListCACertificatesPaginator",
    "ListCertificatesByCAPaginator",
    "ListCertificatesPaginator",
    "ListCommandExecutionsPaginator",
    "ListCommandsPaginator",
    "ListCustomMetricsPaginator",
    "ListDetectMitigationActionsExecutionsPaginator",
    "ListDetectMitigationActionsTasksPaginator",
    "ListDimensionsPaginator",
    "ListDomainConfigurationsPaginator",
    "ListFleetMetricsPaginator",
    "ListIndicesPaginator",
    "ListJobExecutionsForJobPaginator",
    "ListJobExecutionsForThingPaginator",
    "ListJobTemplatesPaginator",
    "ListJobsPaginator",
    "ListManagedJobTemplatesPaginator",
    "ListMetricValuesPaginator",
    "ListMitigationActionsPaginator",
    "ListOTAUpdatesPaginator",
    "ListOutgoingCertificatesPaginator",
    "ListPackageVersionsPaginator",
    "ListPackagesPaginator",
    "ListPoliciesPaginator",
    "ListPolicyPrincipalsPaginator",
    "ListPrincipalPoliciesPaginator",
    "ListPrincipalThingsPaginator",
    "ListPrincipalThingsV2Paginator",
    "ListProvisioningTemplateVersionsPaginator",
    "ListProvisioningTemplatesPaginator",
    "ListRelatedResourcesForAuditFindingPaginator",
    "ListRoleAliasesPaginator",
    "ListSbomValidationResultsPaginator",
    "ListScheduledAuditsPaginator",
    "ListSecurityProfilesForTargetPaginator",
    "ListSecurityProfilesPaginator",
    "ListStreamsPaginator",
    "ListTagsForResourcePaginator",
    "ListTargetsForPolicyPaginator",
    "ListTargetsForSecurityProfilePaginator",
    "ListThingGroupsForThingPaginator",
    "ListThingGroupsPaginator",
    "ListThingPrincipalsPaginator",
    "ListThingPrincipalsV2Paginator",
    "ListThingRegistrationTaskReportsPaginator",
    "ListThingRegistrationTasksPaginator",
    "ListThingTypesPaginator",
    "ListThingsInBillingGroupPaginator",
    "ListThingsInThingGroupPaginator",
    "ListThingsPaginator",
    "ListTopicRuleDestinationsPaginator",
    "ListTopicRulesPaginator",
    "ListV2LoggingLevelsPaginator",
    "ListViolationEventsPaginator",
)


if TYPE_CHECKING:
    _GetBehaviorModelTrainingSummariesPaginatorBase = AioPaginator[
        GetBehaviorModelTrainingSummariesResponseTypeDef
    ]
else:
    _GetBehaviorModelTrainingSummariesPaginatorBase = AioPaginator  # type: ignore[assignment]


class GetBehaviorModelTrainingSummariesPaginator(_GetBehaviorModelTrainingSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/GetBehaviorModelTrainingSummaries.html#IoT.Paginator.GetBehaviorModelTrainingSummaries)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetBehaviorModelTrainingSummariesRequestPaginateTypeDef]
    ) -> AioPageIterator[GetBehaviorModelTrainingSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/GetBehaviorModelTrainingSummaries.html#IoT.Paginator.GetBehaviorModelTrainingSummaries.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#getbehaviormodeltrainingsummariespaginator)
        """


if TYPE_CHECKING:
    _ListActiveViolationsPaginatorBase = AioPaginator[ListActiveViolationsResponseTypeDef]
else:
    _ListActiveViolationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListActiveViolationsPaginator(_ListActiveViolationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListActiveViolations.html#IoT.Paginator.ListActiveViolations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listactiveviolationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListActiveViolationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListActiveViolationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListActiveViolations.html#IoT.Paginator.ListActiveViolations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listactiveviolationspaginator)
        """


if TYPE_CHECKING:
    _ListAttachedPoliciesPaginatorBase = AioPaginator[ListAttachedPoliciesResponseTypeDef]
else:
    _ListAttachedPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAttachedPoliciesPaginator(_ListAttachedPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAttachedPolicies.html#IoT.Paginator.ListAttachedPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listattachedpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAttachedPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAttachedPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAttachedPolicies.html#IoT.Paginator.ListAttachedPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listattachedpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListAuditFindingsPaginatorBase = AioPaginator[ListAuditFindingsResponseTypeDef]
else:
    _ListAuditFindingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAuditFindingsPaginator(_ListAuditFindingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditFindings.html#IoT.Paginator.ListAuditFindings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditfindingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuditFindingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuditFindingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditFindings.html#IoT.Paginator.ListAuditFindings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditfindingspaginator)
        """


if TYPE_CHECKING:
    _ListAuditMitigationActionsExecutionsPaginatorBase = AioPaginator[
        ListAuditMitigationActionsExecutionsResponseTypeDef
    ]
else:
    _ListAuditMitigationActionsExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAuditMitigationActionsExecutionsPaginator(
    _ListAuditMitigationActionsExecutionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsExecutions.html#IoT.Paginator.ListAuditMitigationActionsExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionsexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuditMitigationActionsExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuditMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsExecutions.html#IoT.Paginator.ListAuditMitigationActionsExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionsexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListAuditMitigationActionsTasksPaginatorBase = AioPaginator[
        ListAuditMitigationActionsTasksResponseTypeDef
    ]
else:
    _ListAuditMitigationActionsTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAuditMitigationActionsTasksPaginator(_ListAuditMitigationActionsTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsTasks.html#IoT.Paginator.ListAuditMitigationActionsTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionstaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuditMitigationActionsTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuditMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditMitigationActionsTasks.html#IoT.Paginator.ListAuditMitigationActionsTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditmitigationactionstaskspaginator)
        """


if TYPE_CHECKING:
    _ListAuditSuppressionsPaginatorBase = AioPaginator[ListAuditSuppressionsResponseTypeDef]
else:
    _ListAuditSuppressionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAuditSuppressionsPaginator(_ListAuditSuppressionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditSuppressions.html#IoT.Paginator.ListAuditSuppressions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditsuppressionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuditSuppressionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuditSuppressionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditSuppressions.html#IoT.Paginator.ListAuditSuppressions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauditsuppressionspaginator)
        """


if TYPE_CHECKING:
    _ListAuditTasksPaginatorBase = AioPaginator[ListAuditTasksResponseTypeDef]
else:
    _ListAuditTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAuditTasksPaginator(_ListAuditTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditTasks.html#IoT.Paginator.ListAuditTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listaudittaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuditTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuditTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuditTasks.html#IoT.Paginator.ListAuditTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listaudittaskspaginator)
        """


if TYPE_CHECKING:
    _ListAuthorizersPaginatorBase = AioPaginator[ListAuthorizersResponseTypeDef]
else:
    _ListAuthorizersPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListAuthorizersPaginator(_ListAuthorizersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuthorizers.html#IoT.Paginator.ListAuthorizers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauthorizerspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuthorizersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuthorizersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListAuthorizers.html#IoT.Paginator.ListAuthorizers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listauthorizerspaginator)
        """


if TYPE_CHECKING:
    _ListBillingGroupsPaginatorBase = AioPaginator[ListBillingGroupsResponseTypeDef]
else:
    _ListBillingGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListBillingGroupsPaginator(_ListBillingGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListBillingGroups.html#IoT.Paginator.ListBillingGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listbillinggroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBillingGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBillingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListBillingGroups.html#IoT.Paginator.ListBillingGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listbillinggroupspaginator)
        """


if TYPE_CHECKING:
    _ListCACertificatesPaginatorBase = AioPaginator[ListCACertificatesResponseTypeDef]
else:
    _ListCACertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCACertificatesPaginator(_ListCACertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCACertificates.html#IoT.Paginator.ListCACertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcacertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCACertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCACertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCACertificates.html#IoT.Paginator.ListCACertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcacertificatespaginator)
        """


if TYPE_CHECKING:
    _ListCertificatesByCAPaginatorBase = AioPaginator[ListCertificatesByCAResponseTypeDef]
else:
    _ListCertificatesByCAPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCertificatesByCAPaginator(_ListCertificatesByCAPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificatesByCA.html#IoT.Paginator.ListCertificatesByCA)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatesbycapaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificatesByCARequestPaginateTypeDef]
    ) -> AioPageIterator[ListCertificatesByCAResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificatesByCA.html#IoT.Paginator.ListCertificatesByCA.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatesbycapaginator)
        """


if TYPE_CHECKING:
    _ListCertificatesPaginatorBase = AioPaginator[ListCertificatesResponseTypeDef]
else:
    _ListCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCertificatesPaginator(_ListCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificates.html#IoT.Paginator.ListCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCertificates.html#IoT.Paginator.ListCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcertificatespaginator)
        """


if TYPE_CHECKING:
    _ListCommandExecutionsPaginatorBase = AioPaginator[ListCommandExecutionsResponseTypeDef]
else:
    _ListCommandExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCommandExecutionsPaginator(_ListCommandExecutionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommandExecutions.html#IoT.Paginator.ListCommandExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcommandexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommandExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommandExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommandExecutions.html#IoT.Paginator.ListCommandExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcommandexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListCommandsPaginatorBase = AioPaginator[ListCommandsResponseTypeDef]
else:
    _ListCommandsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCommandsPaginator(_ListCommandsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommands.html#IoT.Paginator.ListCommands)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcommandspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCommandsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCommandsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCommands.html#IoT.Paginator.ListCommands.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcommandspaginator)
        """


if TYPE_CHECKING:
    _ListCustomMetricsPaginatorBase = AioPaginator[ListCustomMetricsResponseTypeDef]
else:
    _ListCustomMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListCustomMetricsPaginator(_ListCustomMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCustomMetrics.html#IoT.Paginator.ListCustomMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcustommetricspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCustomMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListCustomMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListCustomMetrics.html#IoT.Paginator.ListCustomMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listcustommetricspaginator)
        """


if TYPE_CHECKING:
    _ListDetectMitigationActionsExecutionsPaginatorBase = AioPaginator[
        ListDetectMitigationActionsExecutionsResponseTypeDef
    ]
else:
    _ListDetectMitigationActionsExecutionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDetectMitigationActionsExecutionsPaginator(
    _ListDetectMitigationActionsExecutionsPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsExecutions.html#IoT.Paginator.ListDetectMitigationActionsExecutions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDetectMitigationActionsExecutionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDetectMitigationActionsExecutionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsExecutions.html#IoT.Paginator.ListDetectMitigationActionsExecutions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionsexecutionspaginator)
        """


if TYPE_CHECKING:
    _ListDetectMitigationActionsTasksPaginatorBase = AioPaginator[
        ListDetectMitigationActionsTasksResponseTypeDef
    ]
else:
    _ListDetectMitigationActionsTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDetectMitigationActionsTasksPaginator(_ListDetectMitigationActionsTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsTasks.html#IoT.Paginator.ListDetectMitigationActionsTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionstaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDetectMitigationActionsTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDetectMitigationActionsTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDetectMitigationActionsTasks.html#IoT.Paginator.ListDetectMitigationActionsTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdetectmitigationactionstaskspaginator)
        """


if TYPE_CHECKING:
    _ListDimensionsPaginatorBase = AioPaginator[ListDimensionsResponseTypeDef]
else:
    _ListDimensionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDimensionsPaginator(_ListDimensionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDimensions.html#IoT.Paginator.ListDimensions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdimensionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDimensionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDimensionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDimensions.html#IoT.Paginator.ListDimensions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdimensionspaginator)
        """


if TYPE_CHECKING:
    _ListDomainConfigurationsPaginatorBase = AioPaginator[ListDomainConfigurationsResponseTypeDef]
else:
    _ListDomainConfigurationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListDomainConfigurationsPaginator(_ListDomainConfigurationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDomainConfigurations.html#IoT.Paginator.ListDomainConfigurations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdomainconfigurationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDomainConfigurationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDomainConfigurationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListDomainConfigurations.html#IoT.Paginator.ListDomainConfigurations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listdomainconfigurationspaginator)
        """


if TYPE_CHECKING:
    _ListFleetMetricsPaginatorBase = AioPaginator[ListFleetMetricsResponseTypeDef]
else:
    _ListFleetMetricsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListFleetMetricsPaginator(_ListFleetMetricsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListFleetMetrics.html#IoT.Paginator.ListFleetMetrics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listfleetmetricspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFleetMetricsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFleetMetricsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListFleetMetrics.html#IoT.Paginator.ListFleetMetrics.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listfleetmetricspaginator)
        """


if TYPE_CHECKING:
    _ListIndicesPaginatorBase = AioPaginator[ListIndicesResponseTypeDef]
else:
    _ListIndicesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListIndicesPaginator(_ListIndicesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListIndices.html#IoT.Paginator.ListIndices)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listindicespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIndicesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIndicesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListIndices.html#IoT.Paginator.ListIndices.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listindicespaginator)
        """


if TYPE_CHECKING:
    _ListJobExecutionsForJobPaginatorBase = AioPaginator[ListJobExecutionsForJobResponseTypeDef]
else:
    _ListJobExecutionsForJobPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobExecutionsForJobPaginator(_ListJobExecutionsForJobPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForJob.html#IoT.Paginator.ListJobExecutionsForJob)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforjobpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobExecutionsForJobRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobExecutionsForJobResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForJob.html#IoT.Paginator.ListJobExecutionsForJob.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforjobpaginator)
        """


if TYPE_CHECKING:
    _ListJobExecutionsForThingPaginatorBase = AioPaginator[ListJobExecutionsForThingResponseTypeDef]
else:
    _ListJobExecutionsForThingPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobExecutionsForThingPaginator(_ListJobExecutionsForThingPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForThing.html#IoT.Paginator.ListJobExecutionsForThing)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforthingpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobExecutionsForThingRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobExecutionsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobExecutionsForThing.html#IoT.Paginator.ListJobExecutionsForThing.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobexecutionsforthingpaginator)
        """


if TYPE_CHECKING:
    _ListJobTemplatesPaginatorBase = AioPaginator[ListJobTemplatesResponseTypeDef]
else:
    _ListJobTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobTemplatesPaginator(_ListJobTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobTemplates.html#IoT.Paginator.ListJobTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobTemplates.html#IoT.Paginator.ListJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobtemplatespaginator)
        """


if TYPE_CHECKING:
    _ListJobsPaginatorBase = AioPaginator[ListJobsResponseTypeDef]
else:
    _ListJobsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListJobsPaginator(_ListJobsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobs.html#IoT.Paginator.ListJobs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListJobsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListJobsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListJobs.html#IoT.Paginator.ListJobs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listjobspaginator)
        """


if TYPE_CHECKING:
    _ListManagedJobTemplatesPaginatorBase = AioPaginator[ListManagedJobTemplatesResponseTypeDef]
else:
    _ListManagedJobTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListManagedJobTemplatesPaginator(_ListManagedJobTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListManagedJobTemplates.html#IoT.Paginator.ListManagedJobTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmanagedjobtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListManagedJobTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListManagedJobTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListManagedJobTemplates.html#IoT.Paginator.ListManagedJobTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmanagedjobtemplatespaginator)
        """


if TYPE_CHECKING:
    _ListMetricValuesPaginatorBase = AioPaginator[ListMetricValuesResponseTypeDef]
else:
    _ListMetricValuesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMetricValuesPaginator(_ListMetricValuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMetricValues.html#IoT.Paginator.ListMetricValues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmetricvaluespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMetricValuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMetricValuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMetricValues.html#IoT.Paginator.ListMetricValues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmetricvaluespaginator)
        """


if TYPE_CHECKING:
    _ListMitigationActionsPaginatorBase = AioPaginator[ListMitigationActionsResponseTypeDef]
else:
    _ListMitigationActionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListMitigationActionsPaginator(_ListMitigationActionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMitigationActions.html#IoT.Paginator.ListMitigationActions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmitigationactionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMitigationActionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListMitigationActionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListMitigationActions.html#IoT.Paginator.ListMitigationActions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listmitigationactionspaginator)
        """


if TYPE_CHECKING:
    _ListOTAUpdatesPaginatorBase = AioPaginator[ListOTAUpdatesResponseTypeDef]
else:
    _ListOTAUpdatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOTAUpdatesPaginator(_ListOTAUpdatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOTAUpdates.html#IoT.Paginator.ListOTAUpdates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listotaupdatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOTAUpdatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOTAUpdatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOTAUpdates.html#IoT.Paginator.ListOTAUpdates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listotaupdatespaginator)
        """


if TYPE_CHECKING:
    _ListOutgoingCertificatesPaginatorBase = AioPaginator[ListOutgoingCertificatesResponseTypeDef]
else:
    _ListOutgoingCertificatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListOutgoingCertificatesPaginator(_ListOutgoingCertificatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOutgoingCertificates.html#IoT.Paginator.ListOutgoingCertificates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listoutgoingcertificatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOutgoingCertificatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListOutgoingCertificatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListOutgoingCertificates.html#IoT.Paginator.ListOutgoingCertificates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listoutgoingcertificatespaginator)
        """


if TYPE_CHECKING:
    _ListPackageVersionsPaginatorBase = AioPaginator[ListPackageVersionsResponseTypeDef]
else:
    _ListPackageVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPackageVersionsPaginator(_ListPackageVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackageVersions.html#IoT.Paginator.ListPackageVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackageversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackageVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackageVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackageVersions.html#IoT.Paginator.ListPackageVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackageversionspaginator)
        """


if TYPE_CHECKING:
    _ListPackagesPaginatorBase = AioPaginator[ListPackagesResponseTypeDef]
else:
    _ListPackagesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPackagesPaginator(_ListPackagesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackages.html#IoT.Paginator.ListPackages)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackagespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPackagesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPackagesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPackages.html#IoT.Paginator.ListPackages.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpackagespaginator)
        """


if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = AioPaginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicies.html#IoT.Paginator.ListPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicies.html#IoT.Paginator.ListPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListPolicyPrincipalsPaginatorBase = AioPaginator[ListPolicyPrincipalsResponseTypeDef]
else:
    _ListPolicyPrincipalsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPolicyPrincipalsPaginator(_ListPolicyPrincipalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicyPrincipals.html#IoT.Paginator.ListPolicyPrincipals)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpolicyprincipalspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyPrincipalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPolicyPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPolicyPrincipals.html#IoT.Paginator.ListPolicyPrincipals.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listpolicyprincipalspaginator)
        """


if TYPE_CHECKING:
    _ListPrincipalPoliciesPaginatorBase = AioPaginator[ListPrincipalPoliciesResponseTypeDef]
else:
    _ListPrincipalPoliciesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrincipalPoliciesPaginator(_ListPrincipalPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalPolicies.html#IoT.Paginator.ListPrincipalPolicies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalpoliciespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrincipalPoliciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPrincipalPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalPolicies.html#IoT.Paginator.ListPrincipalPolicies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalpoliciespaginator)
        """


if TYPE_CHECKING:
    _ListPrincipalThingsPaginatorBase = AioPaginator[ListPrincipalThingsResponseTypeDef]
else:
    _ListPrincipalThingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrincipalThingsPaginator(_ListPrincipalThingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThings.html#IoT.Paginator.ListPrincipalThings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalthingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrincipalThingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPrincipalThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThings.html#IoT.Paginator.ListPrincipalThings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalthingspaginator)
        """


if TYPE_CHECKING:
    _ListPrincipalThingsV2PaginatorBase = AioPaginator[ListPrincipalThingsV2ResponseTypeDef]
else:
    _ListPrincipalThingsV2PaginatorBase = AioPaginator  # type: ignore[assignment]


class ListPrincipalThingsV2Paginator(_ListPrincipalThingsV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThingsV2.html#IoT.Paginator.ListPrincipalThingsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalthingsv2paginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPrincipalThingsV2RequestPaginateTypeDef]
    ) -> AioPageIterator[ListPrincipalThingsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListPrincipalThingsV2.html#IoT.Paginator.ListPrincipalThingsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprincipalthingsv2paginator)
        """


if TYPE_CHECKING:
    _ListProvisioningTemplateVersionsPaginatorBase = AioPaginator[
        ListProvisioningTemplateVersionsResponseTypeDef
    ]
else:
    _ListProvisioningTemplateVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProvisioningTemplateVersionsPaginator(_ListProvisioningTemplateVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplateVersions.html#IoT.Paginator.ListProvisioningTemplateVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplateversionspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisioningTemplateVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProvisioningTemplateVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplateVersions.html#IoT.Paginator.ListProvisioningTemplateVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplateversionspaginator)
        """


if TYPE_CHECKING:
    _ListProvisioningTemplatesPaginatorBase = AioPaginator[ListProvisioningTemplatesResponseTypeDef]
else:
    _ListProvisioningTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListProvisioningTemplatesPaginator(_ListProvisioningTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplates.html#IoT.Paginator.ListProvisioningTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplatespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListProvisioningTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListProvisioningTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListProvisioningTemplates.html#IoT.Paginator.ListProvisioningTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listprovisioningtemplatespaginator)
        """


if TYPE_CHECKING:
    _ListRelatedResourcesForAuditFindingPaginatorBase = AioPaginator[
        ListRelatedResourcesForAuditFindingResponseTypeDef
    ]
else:
    _ListRelatedResourcesForAuditFindingPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRelatedResourcesForAuditFindingPaginator(
    _ListRelatedResourcesForAuditFindingPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRelatedResourcesForAuditFinding.html#IoT.Paginator.ListRelatedResourcesForAuditFinding)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrelatedresourcesforauditfindingpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRelatedResourcesForAuditFindingRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRelatedResourcesForAuditFindingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRelatedResourcesForAuditFinding.html#IoT.Paginator.ListRelatedResourcesForAuditFinding.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrelatedresourcesforauditfindingpaginator)
        """


if TYPE_CHECKING:
    _ListRoleAliasesPaginatorBase = AioPaginator[ListRoleAliasesResponseTypeDef]
else:
    _ListRoleAliasesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListRoleAliasesPaginator(_ListRoleAliasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRoleAliases.html#IoT.Paginator.ListRoleAliases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrolealiasespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoleAliasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoleAliasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListRoleAliases.html#IoT.Paginator.ListRoleAliases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listrolealiasespaginator)
        """


if TYPE_CHECKING:
    _ListSbomValidationResultsPaginatorBase = AioPaginator[ListSbomValidationResultsResponseTypeDef]
else:
    _ListSbomValidationResultsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSbomValidationResultsPaginator(_ListSbomValidationResultsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSbomValidationResults.html#IoT.Paginator.ListSbomValidationResults)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsbomvalidationresultspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSbomValidationResultsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSbomValidationResultsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSbomValidationResults.html#IoT.Paginator.ListSbomValidationResults.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsbomvalidationresultspaginator)
        """


if TYPE_CHECKING:
    _ListScheduledAuditsPaginatorBase = AioPaginator[ListScheduledAuditsResponseTypeDef]
else:
    _ListScheduledAuditsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListScheduledAuditsPaginator(_ListScheduledAuditsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListScheduledAudits.html#IoT.Paginator.ListScheduledAudits)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listscheduledauditspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListScheduledAuditsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListScheduledAuditsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListScheduledAudits.html#IoT.Paginator.ListScheduledAudits.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listscheduledauditspaginator)
        """


if TYPE_CHECKING:
    _ListSecurityProfilesForTargetPaginatorBase = AioPaginator[
        ListSecurityProfilesForTargetResponseTypeDef
    ]
else:
    _ListSecurityProfilesForTargetPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecurityProfilesForTargetPaginator(_ListSecurityProfilesForTargetPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfilesForTarget.html#IoT.Paginator.ListSecurityProfilesForTarget)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilesfortargetpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityProfilesForTargetRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityProfilesForTargetResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfilesForTarget.html#IoT.Paginator.ListSecurityProfilesForTarget.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilesfortargetpaginator)
        """


if TYPE_CHECKING:
    _ListSecurityProfilesPaginatorBase = AioPaginator[ListSecurityProfilesResponseTypeDef]
else:
    _ListSecurityProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListSecurityProfilesPaginator(_ListSecurityProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfiles.html#IoT.Paginator.ListSecurityProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListSecurityProfiles.html#IoT.Paginator.ListSecurityProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listsecurityprofilespaginator)
        """


if TYPE_CHECKING:
    _ListStreamsPaginatorBase = AioPaginator[ListStreamsResponseTypeDef]
else:
    _ListStreamsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListStreamsPaginator(_ListStreamsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListStreams.html#IoT.Paginator.ListStreams)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#liststreamspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListStreamsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListStreamsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListStreams.html#IoT.Paginator.ListStreams.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#liststreamspaginator)
        """


if TYPE_CHECKING:
    _ListTagsForResourcePaginatorBase = AioPaginator[ListTagsForResourceResponseTypeDef]
else:
    _ListTagsForResourcePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTagsForResourcePaginator(_ListTagsForResourcePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTagsForResource.html#IoT.Paginator.ListTagsForResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtagsforresourcepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTagsForResourceRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTagsForResourceResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTagsForResource.html#IoT.Paginator.ListTagsForResource.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtagsforresourcepaginator)
        """


if TYPE_CHECKING:
    _ListTargetsForPolicyPaginatorBase = AioPaginator[ListTargetsForPolicyResponseTypeDef]
else:
    _ListTargetsForPolicyPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetsForPolicyPaginator(_ListTargetsForPolicyPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForPolicy.html#IoT.Paginator.ListTargetsForPolicy)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforpolicypaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetsForPolicyRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetsForPolicyResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForPolicy.html#IoT.Paginator.ListTargetsForPolicy.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforpolicypaginator)
        """


if TYPE_CHECKING:
    _ListTargetsForSecurityProfilePaginatorBase = AioPaginator[
        ListTargetsForSecurityProfileResponseTypeDef
    ]
else:
    _ListTargetsForSecurityProfilePaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTargetsForSecurityProfilePaginator(_ListTargetsForSecurityProfilePaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForSecurityProfile.html#IoT.Paginator.ListTargetsForSecurityProfile)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforsecurityprofilepaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTargetsForSecurityProfileRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTargetsForSecurityProfileResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTargetsForSecurityProfile.html#IoT.Paginator.ListTargetsForSecurityProfile.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtargetsforsecurityprofilepaginator)
        """


if TYPE_CHECKING:
    _ListThingGroupsForThingPaginatorBase = AioPaginator[ListThingGroupsForThingResponseTypeDef]
else:
    _ListThingGroupsForThingPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingGroupsForThingPaginator(_ListThingGroupsForThingPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroupsForThing.html#IoT.Paginator.ListThingGroupsForThing)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupsforthingpaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingGroupsForThingRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingGroupsForThingResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroupsForThing.html#IoT.Paginator.ListThingGroupsForThing.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupsforthingpaginator)
        """


if TYPE_CHECKING:
    _ListThingGroupsPaginatorBase = AioPaginator[ListThingGroupsResponseTypeDef]
else:
    _ListThingGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingGroupsPaginator(_ListThingGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroups.html#IoT.Paginator.ListThingGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingGroups.html#IoT.Paginator.ListThingGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthinggroupspaginator)
        """


if TYPE_CHECKING:
    _ListThingPrincipalsPaginatorBase = AioPaginator[ListThingPrincipalsResponseTypeDef]
else:
    _ListThingPrincipalsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingPrincipalsPaginator(_ListThingPrincipalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipals.html#IoT.Paginator.ListThingPrincipals)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingprincipalspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingPrincipalsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingPrincipalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipals.html#IoT.Paginator.ListThingPrincipals.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingprincipalspaginator)
        """


if TYPE_CHECKING:
    _ListThingPrincipalsV2PaginatorBase = AioPaginator[ListThingPrincipalsV2ResponseTypeDef]
else:
    _ListThingPrincipalsV2PaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingPrincipalsV2Paginator(_ListThingPrincipalsV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipalsV2.html#IoT.Paginator.ListThingPrincipalsV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingprincipalsv2paginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingPrincipalsV2RequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingPrincipalsV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingPrincipalsV2.html#IoT.Paginator.ListThingPrincipalsV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingprincipalsv2paginator)
        """


if TYPE_CHECKING:
    _ListThingRegistrationTaskReportsPaginatorBase = AioPaginator[
        ListThingRegistrationTaskReportsResponseTypeDef
    ]
else:
    _ListThingRegistrationTaskReportsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingRegistrationTaskReportsPaginator(_ListThingRegistrationTaskReportsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTaskReports.html#IoT.Paginator.ListThingRegistrationTaskReports)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskreportspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingRegistrationTaskReportsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingRegistrationTaskReportsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTaskReports.html#IoT.Paginator.ListThingRegistrationTaskReports.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskreportspaginator)
        """


if TYPE_CHECKING:
    _ListThingRegistrationTasksPaginatorBase = AioPaginator[
        ListThingRegistrationTasksResponseTypeDef
    ]
else:
    _ListThingRegistrationTasksPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingRegistrationTasksPaginator(_ListThingRegistrationTasksPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTasks.html#IoT.Paginator.ListThingRegistrationTasks)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingRegistrationTasksRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingRegistrationTasksResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingRegistrationTasks.html#IoT.Paginator.ListThingRegistrationTasks.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingregistrationtaskspaginator)
        """


if TYPE_CHECKING:
    _ListThingTypesPaginatorBase = AioPaginator[ListThingTypesResponseTypeDef]
else:
    _ListThingTypesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingTypesPaginator(_ListThingTypesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingTypes.html#IoT.Paginator.ListThingTypes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingtypespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingTypesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingTypes.html#IoT.Paginator.ListThingTypes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingtypespaginator)
        """


if TYPE_CHECKING:
    _ListThingsInBillingGroupPaginatorBase = AioPaginator[ListThingsInBillingGroupResponseTypeDef]
else:
    _ListThingsInBillingGroupPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingsInBillingGroupPaginator(_ListThingsInBillingGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInBillingGroup.html#IoT.Paginator.ListThingsInBillingGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinbillinggrouppaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingsInBillingGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingsInBillingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInBillingGroup.html#IoT.Paginator.ListThingsInBillingGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinbillinggrouppaginator)
        """


if TYPE_CHECKING:
    _ListThingsInThingGroupPaginatorBase = AioPaginator[ListThingsInThingGroupResponseTypeDef]
else:
    _ListThingsInThingGroupPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingsInThingGroupPaginator(_ListThingsInThingGroupPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInThingGroup.html#IoT.Paginator.ListThingsInThingGroup)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinthinggrouppaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingsInThingGroupRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingsInThingGroupResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThingsInThingGroup.html#IoT.Paginator.ListThingsInThingGroup.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingsinthinggrouppaginator)
        """


if TYPE_CHECKING:
    _ListThingsPaginatorBase = AioPaginator[ListThingsResponseTypeDef]
else:
    _ListThingsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListThingsPaginator(_ListThingsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThings.html#IoT.Paginator.ListThings)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListThingsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListThingsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListThings.html#IoT.Paginator.ListThings.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listthingspaginator)
        """


if TYPE_CHECKING:
    _ListTopicRuleDestinationsPaginatorBase = AioPaginator[ListTopicRuleDestinationsResponseTypeDef]
else:
    _ListTopicRuleDestinationsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTopicRuleDestinationsPaginator(_ListTopicRuleDestinationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRuleDestinations.html#IoT.Paginator.ListTopicRuleDestinations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicruledestinationspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTopicRuleDestinationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTopicRuleDestinationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRuleDestinations.html#IoT.Paginator.ListTopicRuleDestinations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicruledestinationspaginator)
        """


if TYPE_CHECKING:
    _ListTopicRulesPaginatorBase = AioPaginator[ListTopicRulesResponseTypeDef]
else:
    _ListTopicRulesPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListTopicRulesPaginator(_ListTopicRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRules.html#IoT.Paginator.ListTopicRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicrulespaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTopicRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTopicRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListTopicRules.html#IoT.Paginator.ListTopicRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listtopicrulespaginator)
        """


if TYPE_CHECKING:
    _ListV2LoggingLevelsPaginatorBase = AioPaginator[ListV2LoggingLevelsResponseTypeDef]
else:
    _ListV2LoggingLevelsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListV2LoggingLevelsPaginator(_ListV2LoggingLevelsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListV2LoggingLevels.html#IoT.Paginator.ListV2LoggingLevels)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listv2logginglevelspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListV2LoggingLevelsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListV2LoggingLevelsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListV2LoggingLevels.html#IoT.Paginator.ListV2LoggingLevels.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listv2logginglevelspaginator)
        """


if TYPE_CHECKING:
    _ListViolationEventsPaginatorBase = AioPaginator[ListViolationEventsResponseTypeDef]
else:
    _ListViolationEventsPaginatorBase = AioPaginator  # type: ignore[assignment]


class ListViolationEventsPaginator(_ListViolationEventsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListViolationEvents.html#IoT.Paginator.ListViolationEvents)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listviolationeventspaginator)
    """

    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListViolationEventsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListViolationEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iot/paginator/ListViolationEvents.html#IoT.Paginator.ListViolationEvents.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iot/paginators/#listviolationeventspaginator)
        """
