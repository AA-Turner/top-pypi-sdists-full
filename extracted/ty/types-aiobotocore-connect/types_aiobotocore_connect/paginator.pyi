"""
Type annotations for connect service client paginators.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_connect.client import ConnectClient
    from types_aiobotocore_connect.paginator import (
        GetMetricDataPaginator,
        ListAgentStatusesPaginator,
        ListApprovedOriginsPaginator,
        ListAuthenticationProfilesPaginator,
        ListBotsPaginator,
        ListContactEvaluationsPaginator,
        ListContactFlowModulesPaginator,
        ListContactFlowVersionsPaginator,
        ListContactFlowsPaginator,
        ListContactReferencesPaginator,
        ListDefaultVocabulariesPaginator,
        ListEvaluationFormVersionsPaginator,
        ListEvaluationFormsPaginator,
        ListFlowAssociationsPaginator,
        ListHoursOfOperationOverridesPaginator,
        ListHoursOfOperationsPaginator,
        ListInstanceAttributesPaginator,
        ListInstanceStorageConfigsPaginator,
        ListInstancesPaginator,
        ListIntegrationAssociationsPaginator,
        ListLambdaFunctionsPaginator,
        ListLexBotsPaginator,
        ListPhoneNumbersPaginator,
        ListPhoneNumbersV2Paginator,
        ListPredefinedAttributesPaginator,
        ListPromptsPaginator,
        ListQueueQuickConnectsPaginator,
        ListQueuesPaginator,
        ListQuickConnectsPaginator,
        ListRoutingProfileQueuesPaginator,
        ListRoutingProfilesPaginator,
        ListRulesPaginator,
        ListSecurityKeysPaginator,
        ListSecurityProfileApplicationsPaginator,
        ListSecurityProfilePermissionsPaginator,
        ListSecurityProfilesPaginator,
        ListTaskTemplatesPaginator,
        ListTrafficDistributionGroupUsersPaginator,
        ListTrafficDistributionGroupsPaginator,
        ListUseCasesPaginator,
        ListUserHierarchyGroupsPaginator,
        ListUserProficienciesPaginator,
        ListUsersPaginator,
        ListViewVersionsPaginator,
        ListViewsPaginator,
        SearchAgentStatusesPaginator,
        SearchAvailablePhoneNumbersPaginator,
        SearchContactFlowModulesPaginator,
        SearchContactFlowsPaginator,
        SearchContactsPaginator,
        SearchHoursOfOperationOverridesPaginator,
        SearchHoursOfOperationsPaginator,
        SearchPredefinedAttributesPaginator,
        SearchPromptsPaginator,
        SearchQueuesPaginator,
        SearchQuickConnectsPaginator,
        SearchResourceTagsPaginator,
        SearchRoutingProfilesPaginator,
        SearchSecurityProfilesPaginator,
        SearchUserHierarchyGroupsPaginator,
        SearchUsersPaginator,
        SearchVocabulariesPaginator,
    )

    session = get_session()
    with session.create_client("connect") as client:
        client: ConnectClient

        get_metric_data_paginator: GetMetricDataPaginator = client.get_paginator("get_metric_data")
        list_agent_statuses_paginator: ListAgentStatusesPaginator = client.get_paginator("list_agent_statuses")
        list_approved_origins_paginator: ListApprovedOriginsPaginator = client.get_paginator("list_approved_origins")
        list_authentication_profiles_paginator: ListAuthenticationProfilesPaginator = client.get_paginator("list_authentication_profiles")
        list_bots_paginator: ListBotsPaginator = client.get_paginator("list_bots")
        list_contact_evaluations_paginator: ListContactEvaluationsPaginator = client.get_paginator("list_contact_evaluations")
        list_contact_flow_modules_paginator: ListContactFlowModulesPaginator = client.get_paginator("list_contact_flow_modules")
        list_contact_flow_versions_paginator: ListContactFlowVersionsPaginator = client.get_paginator("list_contact_flow_versions")
        list_contact_flows_paginator: ListContactFlowsPaginator = client.get_paginator("list_contact_flows")
        list_contact_references_paginator: ListContactReferencesPaginator = client.get_paginator("list_contact_references")
        list_default_vocabularies_paginator: ListDefaultVocabulariesPaginator = client.get_paginator("list_default_vocabularies")
        list_evaluation_form_versions_paginator: ListEvaluationFormVersionsPaginator = client.get_paginator("list_evaluation_form_versions")
        list_evaluation_forms_paginator: ListEvaluationFormsPaginator = client.get_paginator("list_evaluation_forms")
        list_flow_associations_paginator: ListFlowAssociationsPaginator = client.get_paginator("list_flow_associations")
        list_hours_of_operation_overrides_paginator: ListHoursOfOperationOverridesPaginator = client.get_paginator("list_hours_of_operation_overrides")
        list_hours_of_operations_paginator: ListHoursOfOperationsPaginator = client.get_paginator("list_hours_of_operations")
        list_instance_attributes_paginator: ListInstanceAttributesPaginator = client.get_paginator("list_instance_attributes")
        list_instance_storage_configs_paginator: ListInstanceStorageConfigsPaginator = client.get_paginator("list_instance_storage_configs")
        list_instances_paginator: ListInstancesPaginator = client.get_paginator("list_instances")
        list_integration_associations_paginator: ListIntegrationAssociationsPaginator = client.get_paginator("list_integration_associations")
        list_lambda_functions_paginator: ListLambdaFunctionsPaginator = client.get_paginator("list_lambda_functions")
        list_lex_bots_paginator: ListLexBotsPaginator = client.get_paginator("list_lex_bots")
        list_phone_numbers_paginator: ListPhoneNumbersPaginator = client.get_paginator("list_phone_numbers")
        list_phone_numbers_v2_paginator: ListPhoneNumbersV2Paginator = client.get_paginator("list_phone_numbers_v2")
        list_predefined_attributes_paginator: ListPredefinedAttributesPaginator = client.get_paginator("list_predefined_attributes")
        list_prompts_paginator: ListPromptsPaginator = client.get_paginator("list_prompts")
        list_queue_quick_connects_paginator: ListQueueQuickConnectsPaginator = client.get_paginator("list_queue_quick_connects")
        list_queues_paginator: ListQueuesPaginator = client.get_paginator("list_queues")
        list_quick_connects_paginator: ListQuickConnectsPaginator = client.get_paginator("list_quick_connects")
        list_routing_profile_queues_paginator: ListRoutingProfileQueuesPaginator = client.get_paginator("list_routing_profile_queues")
        list_routing_profiles_paginator: ListRoutingProfilesPaginator = client.get_paginator("list_routing_profiles")
        list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
        list_security_keys_paginator: ListSecurityKeysPaginator = client.get_paginator("list_security_keys")
        list_security_profile_applications_paginator: ListSecurityProfileApplicationsPaginator = client.get_paginator("list_security_profile_applications")
        list_security_profile_permissions_paginator: ListSecurityProfilePermissionsPaginator = client.get_paginator("list_security_profile_permissions")
        list_security_profiles_paginator: ListSecurityProfilesPaginator = client.get_paginator("list_security_profiles")
        list_task_templates_paginator: ListTaskTemplatesPaginator = client.get_paginator("list_task_templates")
        list_traffic_distribution_group_users_paginator: ListTrafficDistributionGroupUsersPaginator = client.get_paginator("list_traffic_distribution_group_users")
        list_traffic_distribution_groups_paginator: ListTrafficDistributionGroupsPaginator = client.get_paginator("list_traffic_distribution_groups")
        list_use_cases_paginator: ListUseCasesPaginator = client.get_paginator("list_use_cases")
        list_user_hierarchy_groups_paginator: ListUserHierarchyGroupsPaginator = client.get_paginator("list_user_hierarchy_groups")
        list_user_proficiencies_paginator: ListUserProficienciesPaginator = client.get_paginator("list_user_proficiencies")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        list_view_versions_paginator: ListViewVersionsPaginator = client.get_paginator("list_view_versions")
        list_views_paginator: ListViewsPaginator = client.get_paginator("list_views")
        search_agent_statuses_paginator: SearchAgentStatusesPaginator = client.get_paginator("search_agent_statuses")
        search_available_phone_numbers_paginator: SearchAvailablePhoneNumbersPaginator = client.get_paginator("search_available_phone_numbers")
        search_contact_flow_modules_paginator: SearchContactFlowModulesPaginator = client.get_paginator("search_contact_flow_modules")
        search_contact_flows_paginator: SearchContactFlowsPaginator = client.get_paginator("search_contact_flows")
        search_contacts_paginator: SearchContactsPaginator = client.get_paginator("search_contacts")
        search_hours_of_operation_overrides_paginator: SearchHoursOfOperationOverridesPaginator = client.get_paginator("search_hours_of_operation_overrides")
        search_hours_of_operations_paginator: SearchHoursOfOperationsPaginator = client.get_paginator("search_hours_of_operations")
        search_predefined_attributes_paginator: SearchPredefinedAttributesPaginator = client.get_paginator("search_predefined_attributes")
        search_prompts_paginator: SearchPromptsPaginator = client.get_paginator("search_prompts")
        search_queues_paginator: SearchQueuesPaginator = client.get_paginator("search_queues")
        search_quick_connects_paginator: SearchQuickConnectsPaginator = client.get_paginator("search_quick_connects")
        search_resource_tags_paginator: SearchResourceTagsPaginator = client.get_paginator("search_resource_tags")
        search_routing_profiles_paginator: SearchRoutingProfilesPaginator = client.get_paginator("search_routing_profiles")
        search_security_profiles_paginator: SearchSecurityProfilesPaginator = client.get_paginator("search_security_profiles")
        search_user_hierarchy_groups_paginator: SearchUserHierarchyGroupsPaginator = client.get_paginator("search_user_hierarchy_groups")
        search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
        search_vocabularies_paginator: SearchVocabulariesPaginator = client.get_paginator("search_vocabularies")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from aiobotocore.paginate import AioPageIterator, AioPaginator

from .type_defs import (
    GetMetricDataRequestPaginateTypeDef,
    GetMetricDataResponseTypeDef,
    ListAgentStatusRequestPaginateTypeDef,
    ListAgentStatusResponseTypeDef,
    ListApprovedOriginsRequestPaginateTypeDef,
    ListApprovedOriginsResponseTypeDef,
    ListAuthenticationProfilesRequestPaginateTypeDef,
    ListAuthenticationProfilesResponseTypeDef,
    ListBotsRequestPaginateTypeDef,
    ListBotsResponseTypeDef,
    ListContactEvaluationsRequestPaginateTypeDef,
    ListContactEvaluationsResponseTypeDef,
    ListContactFlowModulesRequestPaginateTypeDef,
    ListContactFlowModulesResponseTypeDef,
    ListContactFlowsRequestPaginateTypeDef,
    ListContactFlowsResponseTypeDef,
    ListContactFlowVersionsRequestPaginateTypeDef,
    ListContactFlowVersionsResponseTypeDef,
    ListContactReferencesRequestPaginateTypeDef,
    ListContactReferencesResponseTypeDef,
    ListDefaultVocabulariesRequestPaginateTypeDef,
    ListDefaultVocabulariesResponseTypeDef,
    ListEvaluationFormsRequestPaginateTypeDef,
    ListEvaluationFormsResponseTypeDef,
    ListEvaluationFormVersionsRequestPaginateTypeDef,
    ListEvaluationFormVersionsResponseTypeDef,
    ListFlowAssociationsRequestPaginateTypeDef,
    ListFlowAssociationsResponseTypeDef,
    ListHoursOfOperationOverridesRequestPaginateTypeDef,
    ListHoursOfOperationOverridesResponseTypeDef,
    ListHoursOfOperationsRequestPaginateTypeDef,
    ListHoursOfOperationsResponseTypeDef,
    ListInstanceAttributesRequestPaginateTypeDef,
    ListInstanceAttributesResponseTypeDef,
    ListInstancesRequestPaginateTypeDef,
    ListInstancesResponseTypeDef,
    ListInstanceStorageConfigsRequestPaginateTypeDef,
    ListInstanceStorageConfigsResponseTypeDef,
    ListIntegrationAssociationsRequestPaginateTypeDef,
    ListIntegrationAssociationsResponseTypeDef,
    ListLambdaFunctionsRequestPaginateTypeDef,
    ListLambdaFunctionsResponseTypeDef,
    ListLexBotsRequestPaginateTypeDef,
    ListLexBotsResponseTypeDef,
    ListPhoneNumbersRequestPaginateTypeDef,
    ListPhoneNumbersResponseTypeDef,
    ListPhoneNumbersV2RequestPaginateTypeDef,
    ListPhoneNumbersV2ResponseTypeDef,
    ListPredefinedAttributesRequestPaginateTypeDef,
    ListPredefinedAttributesResponseTypeDef,
    ListPromptsRequestPaginateTypeDef,
    ListPromptsResponseTypeDef,
    ListQueueQuickConnectsRequestPaginateTypeDef,
    ListQueueQuickConnectsResponseTypeDef,
    ListQueuesRequestPaginateTypeDef,
    ListQueuesResponseTypeDef,
    ListQuickConnectsRequestPaginateTypeDef,
    ListQuickConnectsResponseTypeDef,
    ListRoutingProfileQueuesRequestPaginateTypeDef,
    ListRoutingProfileQueuesResponseTypeDef,
    ListRoutingProfilesRequestPaginateTypeDef,
    ListRoutingProfilesResponseTypeDef,
    ListRulesRequestPaginateTypeDef,
    ListRulesResponseTypeDef,
    ListSecurityKeysRequestPaginateTypeDef,
    ListSecurityKeysResponseTypeDef,
    ListSecurityProfileApplicationsRequestPaginateTypeDef,
    ListSecurityProfileApplicationsResponseTypeDef,
    ListSecurityProfilePermissionsRequestPaginateTypeDef,
    ListSecurityProfilePermissionsResponseTypeDef,
    ListSecurityProfilesRequestPaginateTypeDef,
    ListSecurityProfilesResponseTypeDef,
    ListTaskTemplatesRequestPaginateTypeDef,
    ListTaskTemplatesResponseTypeDef,
    ListTrafficDistributionGroupsRequestPaginateTypeDef,
    ListTrafficDistributionGroupsResponseTypeDef,
    ListTrafficDistributionGroupUsersRequestPaginateTypeDef,
    ListTrafficDistributionGroupUsersResponseTypeDef,
    ListUseCasesRequestPaginateTypeDef,
    ListUseCasesResponseTypeDef,
    ListUserHierarchyGroupsRequestPaginateTypeDef,
    ListUserHierarchyGroupsResponseTypeDef,
    ListUserProficienciesRequestPaginateTypeDef,
    ListUserProficienciesResponseTypeDef,
    ListUsersRequestPaginateTypeDef,
    ListUsersResponseTypeDef,
    ListViewsRequestPaginateTypeDef,
    ListViewsResponseTypeDef,
    ListViewVersionsRequestPaginateTypeDef,
    ListViewVersionsResponseTypeDef,
    SearchAgentStatusesRequestPaginateTypeDef,
    SearchAgentStatusesResponseTypeDef,
    SearchAvailablePhoneNumbersRequestPaginateTypeDef,
    SearchAvailablePhoneNumbersResponseTypeDef,
    SearchContactFlowModulesRequestPaginateTypeDef,
    SearchContactFlowModulesResponseTypeDef,
    SearchContactFlowsRequestPaginateTypeDef,
    SearchContactFlowsResponseTypeDef,
    SearchContactsRequestPaginateTypeDef,
    SearchContactsResponseTypeDef,
    SearchHoursOfOperationOverridesRequestPaginateTypeDef,
    SearchHoursOfOperationOverridesResponseTypeDef,
    SearchHoursOfOperationsRequestPaginateTypeDef,
    SearchHoursOfOperationsResponseTypeDef,
    SearchPredefinedAttributesRequestPaginateTypeDef,
    SearchPredefinedAttributesResponseTypeDef,
    SearchPromptsRequestPaginateTypeDef,
    SearchPromptsResponseTypeDef,
    SearchQueuesRequestPaginateTypeDef,
    SearchQueuesResponseTypeDef,
    SearchQuickConnectsRequestPaginateTypeDef,
    SearchQuickConnectsResponseTypeDef,
    SearchResourceTagsRequestPaginateTypeDef,
    SearchResourceTagsResponseTypeDef,
    SearchRoutingProfilesRequestPaginateTypeDef,
    SearchRoutingProfilesResponseTypeDef,
    SearchSecurityProfilesRequestPaginateTypeDef,
    SearchSecurityProfilesResponseTypeDef,
    SearchUserHierarchyGroupsRequestPaginateTypeDef,
    SearchUserHierarchyGroupsResponseTypeDef,
    SearchUsersRequestPaginateTypeDef,
    SearchUsersResponseTypeDef,
    SearchVocabulariesRequestPaginateTypeDef,
    SearchVocabulariesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "GetMetricDataPaginator",
    "ListAgentStatusesPaginator",
    "ListApprovedOriginsPaginator",
    "ListAuthenticationProfilesPaginator",
    "ListBotsPaginator",
    "ListContactEvaluationsPaginator",
    "ListContactFlowModulesPaginator",
    "ListContactFlowVersionsPaginator",
    "ListContactFlowsPaginator",
    "ListContactReferencesPaginator",
    "ListDefaultVocabulariesPaginator",
    "ListEvaluationFormVersionsPaginator",
    "ListEvaluationFormsPaginator",
    "ListFlowAssociationsPaginator",
    "ListHoursOfOperationOverridesPaginator",
    "ListHoursOfOperationsPaginator",
    "ListInstanceAttributesPaginator",
    "ListInstanceStorageConfigsPaginator",
    "ListInstancesPaginator",
    "ListIntegrationAssociationsPaginator",
    "ListLambdaFunctionsPaginator",
    "ListLexBotsPaginator",
    "ListPhoneNumbersPaginator",
    "ListPhoneNumbersV2Paginator",
    "ListPredefinedAttributesPaginator",
    "ListPromptsPaginator",
    "ListQueueQuickConnectsPaginator",
    "ListQueuesPaginator",
    "ListQuickConnectsPaginator",
    "ListRoutingProfileQueuesPaginator",
    "ListRoutingProfilesPaginator",
    "ListRulesPaginator",
    "ListSecurityKeysPaginator",
    "ListSecurityProfileApplicationsPaginator",
    "ListSecurityProfilePermissionsPaginator",
    "ListSecurityProfilesPaginator",
    "ListTaskTemplatesPaginator",
    "ListTrafficDistributionGroupUsersPaginator",
    "ListTrafficDistributionGroupsPaginator",
    "ListUseCasesPaginator",
    "ListUserHierarchyGroupsPaginator",
    "ListUserProficienciesPaginator",
    "ListUsersPaginator",
    "ListViewVersionsPaginator",
    "ListViewsPaginator",
    "SearchAgentStatusesPaginator",
    "SearchAvailablePhoneNumbersPaginator",
    "SearchContactFlowModulesPaginator",
    "SearchContactFlowsPaginator",
    "SearchContactsPaginator",
    "SearchHoursOfOperationOverridesPaginator",
    "SearchHoursOfOperationsPaginator",
    "SearchPredefinedAttributesPaginator",
    "SearchPromptsPaginator",
    "SearchQueuesPaginator",
    "SearchQuickConnectsPaginator",
    "SearchResourceTagsPaginator",
    "SearchRoutingProfilesPaginator",
    "SearchSecurityProfilesPaginator",
    "SearchUserHierarchyGroupsPaginator",
    "SearchUsersPaginator",
    "SearchVocabulariesPaginator",
)

if TYPE_CHECKING:
    _GetMetricDataPaginatorBase = AioPaginator[GetMetricDataResponseTypeDef]
else:
    _GetMetricDataPaginatorBase = AioPaginator  # type: ignore[assignment]

class GetMetricDataPaginator(_GetMetricDataPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/GetMetricData.html#Connect.Paginator.GetMetricData)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#getmetricdatapaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[GetMetricDataRequestPaginateTypeDef]
    ) -> AioPageIterator[GetMetricDataResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/GetMetricData.html#Connect.Paginator.GetMetricData.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#getmetricdatapaginator)
        """

if TYPE_CHECKING:
    _ListAgentStatusesPaginatorBase = AioPaginator[ListAgentStatusResponseTypeDef]
else:
    _ListAgentStatusesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAgentStatusesPaginator(_ListAgentStatusesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html#Connect.Paginator.ListAgentStatuses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listagentstatusespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentStatusRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAgentStatusResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAgentStatuses.html#Connect.Paginator.ListAgentStatuses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listagentstatusespaginator)
        """

if TYPE_CHECKING:
    _ListApprovedOriginsPaginatorBase = AioPaginator[ListApprovedOriginsResponseTypeDef]
else:
    _ListApprovedOriginsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListApprovedOriginsPaginator(_ListApprovedOriginsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListApprovedOrigins.html#Connect.Paginator.ListApprovedOrigins)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listapprovedoriginspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApprovedOriginsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListApprovedOriginsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListApprovedOrigins.html#Connect.Paginator.ListApprovedOrigins.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listapprovedoriginspaginator)
        """

if TYPE_CHECKING:
    _ListAuthenticationProfilesPaginatorBase = AioPaginator[
        ListAuthenticationProfilesResponseTypeDef
    ]
else:
    _ListAuthenticationProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListAuthenticationProfilesPaginator(_ListAuthenticationProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAuthenticationProfiles.html#Connect.Paginator.ListAuthenticationProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listauthenticationprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAuthenticationProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListAuthenticationProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListAuthenticationProfiles.html#Connect.Paginator.ListAuthenticationProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listauthenticationprofilespaginator)
        """

if TYPE_CHECKING:
    _ListBotsPaginatorBase = AioPaginator[ListBotsResponseTypeDef]
else:
    _ListBotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListBotsPaginator(_ListBotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListBots.html#Connect.Paginator.ListBots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listbotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBotsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListBots.html#Connect.Paginator.ListBots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listbotspaginator)
        """

if TYPE_CHECKING:
    _ListContactEvaluationsPaginatorBase = AioPaginator[ListContactEvaluationsResponseTypeDef]
else:
    _ListContactEvaluationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContactEvaluationsPaginator(_ListContactEvaluationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactEvaluations.html#Connect.Paginator.ListContactEvaluations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactevaluationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContactEvaluationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContactEvaluationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactEvaluations.html#Connect.Paginator.ListContactEvaluations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactevaluationspaginator)
        """

if TYPE_CHECKING:
    _ListContactFlowModulesPaginatorBase = AioPaginator[ListContactFlowModulesResponseTypeDef]
else:
    _ListContactFlowModulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContactFlowModulesPaginator(_ListContactFlowModulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowModules.html#Connect.Paginator.ListContactFlowModules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowmodulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContactFlowModulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowModules.html#Connect.Paginator.ListContactFlowModules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowmodulespaginator)
        """

if TYPE_CHECKING:
    _ListContactFlowVersionsPaginatorBase = AioPaginator[ListContactFlowVersionsResponseTypeDef]
else:
    _ListContactFlowVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContactFlowVersionsPaginator(_ListContactFlowVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowVersions.html#Connect.Paginator.ListContactFlowVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContactFlowVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContactFlowVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlowVersions.html#Connect.Paginator.ListContactFlowVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowversionspaginator)
        """

if TYPE_CHECKING:
    _ListContactFlowsPaginatorBase = AioPaginator[ListContactFlowsResponseTypeDef]
else:
    _ListContactFlowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContactFlowsPaginator(_ListContactFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlows.html#Connect.Paginator.ListContactFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContactFlowsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactFlows.html#Connect.Paginator.ListContactFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactflowspaginator)
        """

if TYPE_CHECKING:
    _ListContactReferencesPaginatorBase = AioPaginator[ListContactReferencesResponseTypeDef]
else:
    _ListContactReferencesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListContactReferencesPaginator(_ListContactReferencesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactReferences.html#Connect.Paginator.ListContactReferences)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactreferencespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListContactReferencesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListContactReferencesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListContactReferences.html#Connect.Paginator.ListContactReferences.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listcontactreferencespaginator)
        """

if TYPE_CHECKING:
    _ListDefaultVocabulariesPaginatorBase = AioPaginator[ListDefaultVocabulariesResponseTypeDef]
else:
    _ListDefaultVocabulariesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListDefaultVocabulariesPaginator(_ListDefaultVocabulariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListDefaultVocabularies.html#Connect.Paginator.ListDefaultVocabularies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listdefaultvocabulariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDefaultVocabulariesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListDefaultVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListDefaultVocabularies.html#Connect.Paginator.ListDefaultVocabularies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listdefaultvocabulariespaginator)
        """

if TYPE_CHECKING:
    _ListEvaluationFormVersionsPaginatorBase = AioPaginator[
        ListEvaluationFormVersionsResponseTypeDef
    ]
else:
    _ListEvaluationFormVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEvaluationFormVersionsPaginator(_ListEvaluationFormVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationFormVersions.html#Connect.Paginator.ListEvaluationFormVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEvaluationFormVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEvaluationFormVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationFormVersions.html#Connect.Paginator.ListEvaluationFormVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformversionspaginator)
        """

if TYPE_CHECKING:
    _ListEvaluationFormsPaginatorBase = AioPaginator[ListEvaluationFormsResponseTypeDef]
else:
    _ListEvaluationFormsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListEvaluationFormsPaginator(_ListEvaluationFormsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationForms.html#Connect.Paginator.ListEvaluationForms)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEvaluationFormsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListEvaluationFormsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListEvaluationForms.html#Connect.Paginator.ListEvaluationForms.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listevaluationformspaginator)
        """

if TYPE_CHECKING:
    _ListFlowAssociationsPaginatorBase = AioPaginator[ListFlowAssociationsResponseTypeDef]
else:
    _ListFlowAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListFlowAssociationsPaginator(_ListFlowAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListFlowAssociations.html#Connect.Paginator.ListFlowAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listflowassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListFlowAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListFlowAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListFlowAssociations.html#Connect.Paginator.ListFlowAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listflowassociationspaginator)
        """

if TYPE_CHECKING:
    _ListHoursOfOperationOverridesPaginatorBase = AioPaginator[
        ListHoursOfOperationOverridesResponseTypeDef
    ]
else:
    _ListHoursOfOperationOverridesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHoursOfOperationOverridesPaginator(_ListHoursOfOperationOverridesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperationOverrides.html#Connect.Paginator.ListHoursOfOperationOverrides)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listhoursofoperationoverridespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHoursOfOperationOverridesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHoursOfOperationOverridesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperationOverrides.html#Connect.Paginator.ListHoursOfOperationOverrides.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listhoursofoperationoverridespaginator)
        """

if TYPE_CHECKING:
    _ListHoursOfOperationsPaginatorBase = AioPaginator[ListHoursOfOperationsResponseTypeDef]
else:
    _ListHoursOfOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListHoursOfOperationsPaginator(_ListHoursOfOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperations.html#Connect.Paginator.ListHoursOfOperations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listhoursofoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHoursOfOperationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListHoursOfOperations.html#Connect.Paginator.ListHoursOfOperations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listhoursofoperationspaginator)
        """

if TYPE_CHECKING:
    _ListInstanceAttributesPaginatorBase = AioPaginator[ListInstanceAttributesResponseTypeDef]
else:
    _ListInstanceAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstanceAttributesPaginator(_ListInstanceAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceAttributes.html#Connect.Paginator.ListInstanceAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstanceattributespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceAttributesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceAttributes.html#Connect.Paginator.ListInstanceAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstanceattributespaginator)
        """

if TYPE_CHECKING:
    _ListInstanceStorageConfigsPaginatorBase = AioPaginator[
        ListInstanceStorageConfigsResponseTypeDef
    ]
else:
    _ListInstanceStorageConfigsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstanceStorageConfigsPaginator(_ListInstanceStorageConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceStorageConfigs.html#Connect.Paginator.ListInstanceStorageConfigs)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancestorageconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstanceStorageConfigsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstanceStorageConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstanceStorageConfigs.html#Connect.Paginator.ListInstanceStorageConfigs.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancestorageconfigspaginator)
        """

if TYPE_CHECKING:
    _ListInstancesPaginatorBase = AioPaginator[ListInstancesResponseTypeDef]
else:
    _ListInstancesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListInstancesPaginator(_ListInstancesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstances.html#Connect.Paginator.ListInstances)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListInstancesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListInstancesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListInstances.html#Connect.Paginator.ListInstances.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listinstancespaginator)
        """

if TYPE_CHECKING:
    _ListIntegrationAssociationsPaginatorBase = AioPaginator[
        ListIntegrationAssociationsResponseTypeDef
    ]
else:
    _ListIntegrationAssociationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListIntegrationAssociationsPaginator(_ListIntegrationAssociationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListIntegrationAssociations.html#Connect.Paginator.ListIntegrationAssociations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listintegrationassociationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListIntegrationAssociationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListIntegrationAssociationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListIntegrationAssociations.html#Connect.Paginator.ListIntegrationAssociations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listintegrationassociationspaginator)
        """

if TYPE_CHECKING:
    _ListLambdaFunctionsPaginatorBase = AioPaginator[ListLambdaFunctionsResponseTypeDef]
else:
    _ListLambdaFunctionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLambdaFunctionsPaginator(_ListLambdaFunctionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLambdaFunctions.html#Connect.Paginator.ListLambdaFunctions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlambdafunctionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLambdaFunctionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLambdaFunctionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLambdaFunctions.html#Connect.Paginator.ListLambdaFunctions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlambdafunctionspaginator)
        """

if TYPE_CHECKING:
    _ListLexBotsPaginatorBase = AioPaginator[ListLexBotsResponseTypeDef]
else:
    _ListLexBotsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListLexBotsPaginator(_ListLexBotsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLexBots.html#Connect.Paginator.ListLexBots)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlexbotspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListLexBotsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListLexBotsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListLexBots.html#Connect.Paginator.ListLexBots.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listlexbotspaginator)
        """

if TYPE_CHECKING:
    _ListPhoneNumbersPaginatorBase = AioPaginator[ListPhoneNumbersResponseTypeDef]
else:
    _ListPhoneNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPhoneNumbersPaginator(_ListPhoneNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbers.html#Connect.Paginator.ListPhoneNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPhoneNumbersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbers.html#Connect.Paginator.ListPhoneNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumberspaginator)
        """

if TYPE_CHECKING:
    _ListPhoneNumbersV2PaginatorBase = AioPaginator[ListPhoneNumbersV2ResponseTypeDef]
else:
    _ListPhoneNumbersV2PaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPhoneNumbersV2Paginator(_ListPhoneNumbersV2PaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbersV2.html#Connect.Paginator.ListPhoneNumbersV2)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumbersv2paginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPhoneNumbersV2RequestPaginateTypeDef]
    ) -> AioPageIterator[ListPhoneNumbersV2ResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPhoneNumbersV2.html#Connect.Paginator.ListPhoneNumbersV2.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listphonenumbersv2paginator)
        """

if TYPE_CHECKING:
    _ListPredefinedAttributesPaginatorBase = AioPaginator[ListPredefinedAttributesResponseTypeDef]
else:
    _ListPredefinedAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPredefinedAttributesPaginator(_ListPredefinedAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPredefinedAttributes.html#Connect.Paginator.ListPredefinedAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpredefinedattributespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPredefinedAttributesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPredefinedAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPredefinedAttributes.html#Connect.Paginator.ListPredefinedAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpredefinedattributespaginator)
        """

if TYPE_CHECKING:
    _ListPromptsPaginatorBase = AioPaginator[ListPromptsResponseTypeDef]
else:
    _ListPromptsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListPromptsPaginator(_ListPromptsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPrompts.html#Connect.Paginator.ListPrompts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpromptspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPromptsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListPrompts.html#Connect.Paginator.ListPrompts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listpromptspaginator)
        """

if TYPE_CHECKING:
    _ListQueueQuickConnectsPaginatorBase = AioPaginator[ListQueueQuickConnectsResponseTypeDef]
else:
    _ListQueueQuickConnectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQueueQuickConnectsPaginator(_ListQueueQuickConnectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueueQuickConnects.html#Connect.Paginator.ListQueueQuickConnects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuequickconnectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueueQuickConnectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueueQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueueQuickConnects.html#Connect.Paginator.ListQueueQuickConnects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuequickconnectspaginator)
        """

if TYPE_CHECKING:
    _ListQueuesPaginatorBase = AioPaginator[ListQueuesResponseTypeDef]
else:
    _ListQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQueuesPaginator(_ListQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueues.html#Connect.Paginator.ListQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQueues.html#Connect.Paginator.ListQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listqueuespaginator)
        """

if TYPE_CHECKING:
    _ListQuickConnectsPaginatorBase = AioPaginator[ListQuickConnectsResponseTypeDef]
else:
    _ListQuickConnectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListQuickConnectsPaginator(_ListQuickConnectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQuickConnects.html#Connect.Paginator.ListQuickConnects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listquickconnectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListQuickConnectsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListQuickConnects.html#Connect.Paginator.ListQuickConnects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listquickconnectspaginator)
        """

if TYPE_CHECKING:
    _ListRoutingProfileQueuesPaginatorBase = AioPaginator[ListRoutingProfileQueuesResponseTypeDef]
else:
    _ListRoutingProfileQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoutingProfileQueuesPaginator(_ListRoutingProfileQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfileQueues.html#Connect.Paginator.ListRoutingProfileQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilequeuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutingProfileQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoutingProfileQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfileQueues.html#Connect.Paginator.ListRoutingProfileQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilequeuespaginator)
        """

if TYPE_CHECKING:
    _ListRoutingProfilesPaginatorBase = AioPaginator[ListRoutingProfilesResponseTypeDef]
else:
    _ListRoutingProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRoutingProfilesPaginator(_ListRoutingProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfiles.html#Connect.Paginator.ListRoutingProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRoutingProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRoutingProfiles.html#Connect.Paginator.ListRoutingProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listroutingprofilespaginator)
        """

if TYPE_CHECKING:
    _ListRulesPaginatorBase = AioPaginator[ListRulesResponseTypeDef]
else:
    _ListRulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListRulesPaginator(_ListRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRules.html#Connect.Paginator.ListRules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRulesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListRules.html#Connect.Paginator.ListRules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listrulespaginator)
        """

if TYPE_CHECKING:
    _ListSecurityKeysPaginatorBase = AioPaginator[ListSecurityKeysResponseTypeDef]
else:
    _ListSecurityKeysPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityKeysPaginator(_ListSecurityKeysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityKeys.html#Connect.Paginator.ListSecurityKeys)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecuritykeyspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityKeysRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityKeysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityKeys.html#Connect.Paginator.ListSecurityKeys.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecuritykeyspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityProfileApplicationsPaginatorBase = AioPaginator[
        ListSecurityProfileApplicationsResponseTypeDef
    ]
else:
    _ListSecurityProfileApplicationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityProfileApplicationsPaginator(_ListSecurityProfileApplicationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfileApplications.html#Connect.Paginator.ListSecurityProfileApplications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofileapplicationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityProfileApplicationsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityProfileApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfileApplications.html#Connect.Paginator.ListSecurityProfileApplications.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofileapplicationspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityProfilePermissionsPaginatorBase = AioPaginator[
        ListSecurityProfilePermissionsResponseTypeDef
    ]
else:
    _ListSecurityProfilePermissionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityProfilePermissionsPaginator(_ListSecurityProfilePermissionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfilePermissions.html#Connect.Paginator.ListSecurityProfilePermissions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilepermissionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityProfilePermissionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityProfilePermissionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfilePermissions.html#Connect.Paginator.ListSecurityProfilePermissions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilepermissionspaginator)
        """

if TYPE_CHECKING:
    _ListSecurityProfilesPaginatorBase = AioPaginator[ListSecurityProfilesResponseTypeDef]
else:
    _ListSecurityProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListSecurityProfilesPaginator(_ListSecurityProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfiles.html#Connect.Paginator.ListSecurityProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListSecurityProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListSecurityProfiles.html#Connect.Paginator.ListSecurityProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listsecurityprofilespaginator)
        """

if TYPE_CHECKING:
    _ListTaskTemplatesPaginatorBase = AioPaginator[ListTaskTemplatesResponseTypeDef]
else:
    _ListTaskTemplatesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTaskTemplatesPaginator(_ListTaskTemplatesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTaskTemplates.html#Connect.Paginator.ListTaskTemplates)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtasktemplatespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTaskTemplatesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTaskTemplatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTaskTemplates.html#Connect.Paginator.ListTaskTemplates.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtasktemplatespaginator)
        """

if TYPE_CHECKING:
    _ListTrafficDistributionGroupUsersPaginatorBase = AioPaginator[
        ListTrafficDistributionGroupUsersResponseTypeDef
    ]
else:
    _ListTrafficDistributionGroupUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrafficDistributionGroupUsersPaginator(_ListTrafficDistributionGroupUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroupUsers.html#Connect.Paginator.ListTrafficDistributionGroupUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrafficDistributionGroupUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrafficDistributionGroupUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroupUsers.html#Connect.Paginator.ListTrafficDistributionGroupUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupuserspaginator)
        """

if TYPE_CHECKING:
    _ListTrafficDistributionGroupsPaginatorBase = AioPaginator[
        ListTrafficDistributionGroupsResponseTypeDef
    ]
else:
    _ListTrafficDistributionGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListTrafficDistributionGroupsPaginator(_ListTrafficDistributionGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroups.html#Connect.Paginator.ListTrafficDistributionGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListTrafficDistributionGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListTrafficDistributionGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListTrafficDistributionGroups.html#Connect.Paginator.ListTrafficDistributionGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listtrafficdistributiongroupspaginator)
        """

if TYPE_CHECKING:
    _ListUseCasesPaginatorBase = AioPaginator[ListUseCasesResponseTypeDef]
else:
    _ListUseCasesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUseCasesPaginator(_ListUseCasesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUseCases.html#Connect.Paginator.ListUseCases)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listusecasespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUseCasesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUseCasesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUseCases.html#Connect.Paginator.ListUseCases.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listusecasespaginator)
        """

if TYPE_CHECKING:
    _ListUserHierarchyGroupsPaginatorBase = AioPaginator[ListUserHierarchyGroupsResponseTypeDef]
else:
    _ListUserHierarchyGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserHierarchyGroupsPaginator(_ListUserHierarchyGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserHierarchyGroups.html#Connect.Paginator.ListUserHierarchyGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserhierarchygroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserHierarchyGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserHierarchyGroups.html#Connect.Paginator.ListUserHierarchyGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserhierarchygroupspaginator)
        """

if TYPE_CHECKING:
    _ListUserProficienciesPaginatorBase = AioPaginator[ListUserProficienciesResponseTypeDef]
else:
    _ListUserProficienciesPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUserProficienciesPaginator(_ListUserProficienciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserProficiencies.html#Connect.Paginator.ListUserProficiencies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserproficienciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUserProficienciesRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUserProficienciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUserProficiencies.html#Connect.Paginator.ListUserProficiencies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserproficienciespaginator)
        """

if TYPE_CHECKING:
    _ListUsersPaginatorBase = AioPaginator[ListUsersResponseTypeDef]
else:
    _ListUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListUsersPaginator(_ListUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUsers.html#Connect.Paginator.ListUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[ListUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListUsers.html#Connect.Paginator.ListUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listuserspaginator)
        """

if TYPE_CHECKING:
    _ListViewVersionsPaginatorBase = AioPaginator[ListViewVersionsResponseTypeDef]
else:
    _ListViewVersionsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListViewVersionsPaginator(_ListViewVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViewVersions.html#Connect.Paginator.ListViewVersions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListViewVersionsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListViewVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViewVersions.html#Connect.Paginator.ListViewVersions.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewversionspaginator)
        """

if TYPE_CHECKING:
    _ListViewsPaginatorBase = AioPaginator[ListViewsResponseTypeDef]
else:
    _ListViewsPaginatorBase = AioPaginator  # type: ignore[assignment]

class ListViewsPaginator(_ListViewsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViews.html#Connect.Paginator.ListViews)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListViewsRequestPaginateTypeDef]
    ) -> AioPageIterator[ListViewsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/ListViews.html#Connect.Paginator.ListViews.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#listviewspaginator)
        """

if TYPE_CHECKING:
    _SearchAgentStatusesPaginatorBase = AioPaginator[SearchAgentStatusesResponseTypeDef]
else:
    _SearchAgentStatusesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchAgentStatusesPaginator(_SearchAgentStatusesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAgentStatuses.html#Connect.Paginator.SearchAgentStatuses)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchagentstatusespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchAgentStatusesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchAgentStatusesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAgentStatuses.html#Connect.Paginator.SearchAgentStatuses.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchagentstatusespaginator)
        """

if TYPE_CHECKING:
    _SearchAvailablePhoneNumbersPaginatorBase = AioPaginator[
        SearchAvailablePhoneNumbersResponseTypeDef
    ]
else:
    _SearchAvailablePhoneNumbersPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchAvailablePhoneNumbersPaginator(_SearchAvailablePhoneNumbersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAvailablePhoneNumbers.html#Connect.Paginator.SearchAvailablePhoneNumbers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchavailablephonenumberspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchAvailablePhoneNumbersRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchAvailablePhoneNumbersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchAvailablePhoneNumbers.html#Connect.Paginator.SearchAvailablePhoneNumbers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchavailablephonenumberspaginator)
        """

if TYPE_CHECKING:
    _SearchContactFlowModulesPaginatorBase = AioPaginator[SearchContactFlowModulesResponseTypeDef]
else:
    _SearchContactFlowModulesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchContactFlowModulesPaginator(_SearchContactFlowModulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlowModules.html#Connect.Paginator.SearchContactFlowModules)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowmodulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchContactFlowModulesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchContactFlowModulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlowModules.html#Connect.Paginator.SearchContactFlowModules.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowmodulespaginator)
        """

if TYPE_CHECKING:
    _SearchContactFlowsPaginatorBase = AioPaginator[SearchContactFlowsResponseTypeDef]
else:
    _SearchContactFlowsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchContactFlowsPaginator(_SearchContactFlowsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlows.html#Connect.Paginator.SearchContactFlows)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchContactFlowsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchContactFlowsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContactFlows.html#Connect.Paginator.SearchContactFlows.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactflowspaginator)
        """

if TYPE_CHECKING:
    _SearchContactsPaginatorBase = AioPaginator[SearchContactsResponseTypeDef]
else:
    _SearchContactsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchContactsPaginator(_SearchContactsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContacts.html#Connect.Paginator.SearchContacts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchContactsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchContactsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchContacts.html#Connect.Paginator.SearchContacts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchcontactspaginator)
        """

if TYPE_CHECKING:
    _SearchHoursOfOperationOverridesPaginatorBase = AioPaginator[
        SearchHoursOfOperationOverridesResponseTypeDef
    ]
else:
    _SearchHoursOfOperationOverridesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchHoursOfOperationOverridesPaginator(_SearchHoursOfOperationOverridesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperationOverrides.html#Connect.Paginator.SearchHoursOfOperationOverrides)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchhoursofoperationoverridespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchHoursOfOperationOverridesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchHoursOfOperationOverridesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperationOverrides.html#Connect.Paginator.SearchHoursOfOperationOverrides.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchhoursofoperationoverridespaginator)
        """

if TYPE_CHECKING:
    _SearchHoursOfOperationsPaginatorBase = AioPaginator[SearchHoursOfOperationsResponseTypeDef]
else:
    _SearchHoursOfOperationsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchHoursOfOperationsPaginator(_SearchHoursOfOperationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperations.html#Connect.Paginator.SearchHoursOfOperations)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchhoursofoperationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchHoursOfOperationsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchHoursOfOperationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchHoursOfOperations.html#Connect.Paginator.SearchHoursOfOperations.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchhoursofoperationspaginator)
        """

if TYPE_CHECKING:
    _SearchPredefinedAttributesPaginatorBase = AioPaginator[
        SearchPredefinedAttributesResponseTypeDef
    ]
else:
    _SearchPredefinedAttributesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchPredefinedAttributesPaginator(_SearchPredefinedAttributesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPredefinedAttributes.html#Connect.Paginator.SearchPredefinedAttributes)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpredefinedattributespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchPredefinedAttributesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchPredefinedAttributesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPredefinedAttributes.html#Connect.Paginator.SearchPredefinedAttributes.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpredefinedattributespaginator)
        """

if TYPE_CHECKING:
    _SearchPromptsPaginatorBase = AioPaginator[SearchPromptsResponseTypeDef]
else:
    _SearchPromptsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchPromptsPaginator(_SearchPromptsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPrompts.html#Connect.Paginator.SearchPrompts)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpromptspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchPromptsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchPromptsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchPrompts.html#Connect.Paginator.SearchPrompts.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchpromptspaginator)
        """

if TYPE_CHECKING:
    _SearchQueuesPaginatorBase = AioPaginator[SearchQueuesResponseTypeDef]
else:
    _SearchQueuesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchQueuesPaginator(_SearchQueuesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQueues.html#Connect.Paginator.SearchQueues)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchqueuespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchQueuesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchQueuesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQueues.html#Connect.Paginator.SearchQueues.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchqueuespaginator)
        """

if TYPE_CHECKING:
    _SearchQuickConnectsPaginatorBase = AioPaginator[SearchQuickConnectsResponseTypeDef]
else:
    _SearchQuickConnectsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchQuickConnectsPaginator(_SearchQuickConnectsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQuickConnects.html#Connect.Paginator.SearchQuickConnects)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchquickconnectspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchQuickConnectsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchQuickConnectsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchQuickConnects.html#Connect.Paginator.SearchQuickConnects.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchquickconnectspaginator)
        """

if TYPE_CHECKING:
    _SearchResourceTagsPaginatorBase = AioPaginator[SearchResourceTagsResponseTypeDef]
else:
    _SearchResourceTagsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchResourceTagsPaginator(_SearchResourceTagsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchResourceTags.html#Connect.Paginator.SearchResourceTags)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchresourcetagspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchResourceTagsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchResourceTagsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchResourceTags.html#Connect.Paginator.SearchResourceTags.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchresourcetagspaginator)
        """

if TYPE_CHECKING:
    _SearchRoutingProfilesPaginatorBase = AioPaginator[SearchRoutingProfilesResponseTypeDef]
else:
    _SearchRoutingProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchRoutingProfilesPaginator(_SearchRoutingProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchRoutingProfiles.html#Connect.Paginator.SearchRoutingProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchroutingprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchRoutingProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchRoutingProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchRoutingProfiles.html#Connect.Paginator.SearchRoutingProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchroutingprofilespaginator)
        """

if TYPE_CHECKING:
    _SearchSecurityProfilesPaginatorBase = AioPaginator[SearchSecurityProfilesResponseTypeDef]
else:
    _SearchSecurityProfilesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchSecurityProfilesPaginator(_SearchSecurityProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchSecurityProfiles.html#Connect.Paginator.SearchSecurityProfiles)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchsecurityprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchSecurityProfilesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchSecurityProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchSecurityProfiles.html#Connect.Paginator.SearchSecurityProfiles.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchsecurityprofilespaginator)
        """

if TYPE_CHECKING:
    _SearchUserHierarchyGroupsPaginatorBase = AioPaginator[SearchUserHierarchyGroupsResponseTypeDef]
else:
    _SearchUserHierarchyGroupsPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchUserHierarchyGroupsPaginator(_SearchUserHierarchyGroupsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUserHierarchyGroups.html#Connect.Paginator.SearchUserHierarchyGroups)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserhierarchygroupspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchUserHierarchyGroupsRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchUserHierarchyGroupsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUserHierarchyGroups.html#Connect.Paginator.SearchUserHierarchyGroups.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserhierarchygroupspaginator)
        """

if TYPE_CHECKING:
    _SearchUsersPaginatorBase = AioPaginator[SearchUsersResponseTypeDef]
else:
    _SearchUsersPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchUsersPaginator(_SearchUsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUsers.html#Connect.Paginator.SearchUsers)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchUsersRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchUsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchUsers.html#Connect.Paginator.SearchUsers.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchuserspaginator)
        """

if TYPE_CHECKING:
    _SearchVocabulariesPaginatorBase = AioPaginator[SearchVocabulariesResponseTypeDef]
else:
    _SearchVocabulariesPaginatorBase = AioPaginator  # type: ignore[assignment]

class SearchVocabulariesPaginator(_SearchVocabulariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchVocabularies.html#Connect.Paginator.SearchVocabularies)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchvocabulariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[SearchVocabulariesRequestPaginateTypeDef]
    ) -> AioPageIterator[SearchVocabulariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/connect/paginator/SearchVocabularies.html#Connect.Paginator.SearchVocabularies.paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connect/paginators/#searchvocabulariespaginator)
        """
