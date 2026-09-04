"""
Type annotations for bedrock-agentcore-control service client paginators.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session

    from mypy_boto3_bedrock_agentcore_control.client import BedrockAgentCoreControlClient
    from mypy_boto3_bedrock_agentcore_control.paginator import (
        ListAgentRuntimeEndpointsPaginator,
        ListAgentRuntimeVersionsByCapacityProviderPaginator,
        ListAgentRuntimeVersionsPaginator,
        ListAgentRuntimesPaginator,
        ListApiKeyCredentialProvidersPaginator,
        ListBrowserProfilesPaginator,
        ListBrowsersPaginator,
        ListCapacityProvidersPaginator,
        ListCodeInterpretersPaginator,
        ListConfigurationBundleVersionsPaginator,
        ListConfigurationBundlesPaginator,
        ListConsentPortalsPaginator,
        ListDatasetExamplesPaginator,
        ListDatasetVersionsPaginator,
        ListDatasetsPaginator,
        ListEvaluatorsPaginator,
        ListGatewayRateLimitsPaginator,
        ListGatewayRulesPaginator,
        ListGatewayTargetsPaginator,
        ListGatewaysPaginator,
        ListHarnessEndpointsPaginator,
        ListHarnessVersionsPaginator,
        ListHarnessesPaginator,
        ListMemoriesPaginator,
        ListOauth2CredentialProvidersPaginator,
        ListOnlineEvaluationConfigsPaginator,
        ListPaymentConnectorsPaginator,
        ListPaymentCredentialProvidersPaginator,
        ListPaymentManagersPaginator,
        ListPoliciesPaginator,
        ListPolicyEngineSummariesPaginator,
        ListPolicyEnginesPaginator,
        ListPolicyGenerationAssetsPaginator,
        ListPolicyGenerationSummariesPaginator,
        ListPolicyGenerationsPaginator,
        ListPolicySummariesPaginator,
        ListRegistriesPaginator,
        ListRegistryRecordsPaginator,
        ListWorkloadIdentitiesPaginator,
    )

    session = Session()
    client: BedrockAgentCoreControlClient = session.client("bedrock-agentcore-control")

    list_agent_runtime_endpoints_paginator: ListAgentRuntimeEndpointsPaginator = client.get_paginator("list_agent_runtime_endpoints")
    list_agent_runtime_versions_by_capacity_provider_paginator: ListAgentRuntimeVersionsByCapacityProviderPaginator = client.get_paginator("list_agent_runtime_versions_by_capacity_provider")
    list_agent_runtime_versions_paginator: ListAgentRuntimeVersionsPaginator = client.get_paginator("list_agent_runtime_versions")
    list_agent_runtimes_paginator: ListAgentRuntimesPaginator = client.get_paginator("list_agent_runtimes")
    list_api_key_credential_providers_paginator: ListApiKeyCredentialProvidersPaginator = client.get_paginator("list_api_key_credential_providers")
    list_browser_profiles_paginator: ListBrowserProfilesPaginator = client.get_paginator("list_browser_profiles")
    list_browsers_paginator: ListBrowsersPaginator = client.get_paginator("list_browsers")
    list_capacity_providers_paginator: ListCapacityProvidersPaginator = client.get_paginator("list_capacity_providers")
    list_code_interpreters_paginator: ListCodeInterpretersPaginator = client.get_paginator("list_code_interpreters")
    list_configuration_bundle_versions_paginator: ListConfigurationBundleVersionsPaginator = client.get_paginator("list_configuration_bundle_versions")
    list_configuration_bundles_paginator: ListConfigurationBundlesPaginator = client.get_paginator("list_configuration_bundles")
    list_consent_portals_paginator: ListConsentPortalsPaginator = client.get_paginator("list_consent_portals")
    list_dataset_examples_paginator: ListDatasetExamplesPaginator = client.get_paginator("list_dataset_examples")
    list_dataset_versions_paginator: ListDatasetVersionsPaginator = client.get_paginator("list_dataset_versions")
    list_datasets_paginator: ListDatasetsPaginator = client.get_paginator("list_datasets")
    list_evaluators_paginator: ListEvaluatorsPaginator = client.get_paginator("list_evaluators")
    list_gateway_rate_limits_paginator: ListGatewayRateLimitsPaginator = client.get_paginator("list_gateway_rate_limits")
    list_gateway_rules_paginator: ListGatewayRulesPaginator = client.get_paginator("list_gateway_rules")
    list_gateway_targets_paginator: ListGatewayTargetsPaginator = client.get_paginator("list_gateway_targets")
    list_gateways_paginator: ListGatewaysPaginator = client.get_paginator("list_gateways")
    list_harness_endpoints_paginator: ListHarnessEndpointsPaginator = client.get_paginator("list_harness_endpoints")
    list_harness_versions_paginator: ListHarnessVersionsPaginator = client.get_paginator("list_harness_versions")
    list_harnesses_paginator: ListHarnessesPaginator = client.get_paginator("list_harnesses")
    list_memories_paginator: ListMemoriesPaginator = client.get_paginator("list_memories")
    list_oauth2_credential_providers_paginator: ListOauth2CredentialProvidersPaginator = client.get_paginator("list_oauth2_credential_providers")
    list_online_evaluation_configs_paginator: ListOnlineEvaluationConfigsPaginator = client.get_paginator("list_online_evaluation_configs")
    list_payment_connectors_paginator: ListPaymentConnectorsPaginator = client.get_paginator("list_payment_connectors")
    list_payment_credential_providers_paginator: ListPaymentCredentialProvidersPaginator = client.get_paginator("list_payment_credential_providers")
    list_payment_managers_paginator: ListPaymentManagersPaginator = client.get_paginator("list_payment_managers")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_engine_summaries_paginator: ListPolicyEngineSummariesPaginator = client.get_paginator("list_policy_engine_summaries")
    list_policy_engines_paginator: ListPolicyEnginesPaginator = client.get_paginator("list_policy_engines")
    list_policy_generation_assets_paginator: ListPolicyGenerationAssetsPaginator = client.get_paginator("list_policy_generation_assets")
    list_policy_generation_summaries_paginator: ListPolicyGenerationSummariesPaginator = client.get_paginator("list_policy_generation_summaries")
    list_policy_generations_paginator: ListPolicyGenerationsPaginator = client.get_paginator("list_policy_generations")
    list_policy_summaries_paginator: ListPolicySummariesPaginator = client.get_paginator("list_policy_summaries")
    list_registries_paginator: ListRegistriesPaginator = client.get_paginator("list_registries")
    list_registry_records_paginator: ListRegistryRecordsPaginator = client.get_paginator("list_registry_records")
    list_workload_identities_paginator: ListWorkloadIdentitiesPaginator = client.get_paginator("list_workload_identities")
    ```
"""

from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from botocore.paginate import PageIterator, Paginator

from .type_defs import (
    ListAgentRuntimeEndpointsRequestPaginateTypeDef,
    ListAgentRuntimeEndpointsResponseTypeDef,
    ListAgentRuntimesRequestPaginateTypeDef,
    ListAgentRuntimesResponseTypeDef,
    ListAgentRuntimeVersionsByCapacityProviderInputPaginateTypeDef,
    ListAgentRuntimeVersionsByCapacityProviderOutputTypeDef,
    ListAgentRuntimeVersionsRequestPaginateTypeDef,
    ListAgentRuntimeVersionsResponseTypeDef,
    ListApiKeyCredentialProvidersRequestPaginateTypeDef,
    ListApiKeyCredentialProvidersResponseTypeDef,
    ListBrowserProfilesRequestPaginateTypeDef,
    ListBrowserProfilesResponseTypeDef,
    ListBrowsersRequestPaginateTypeDef,
    ListBrowsersResponseTypeDef,
    ListCapacityProvidersInputPaginateTypeDef,
    ListCapacityProvidersOutputTypeDef,
    ListCodeInterpretersRequestPaginateTypeDef,
    ListCodeInterpretersResponseTypeDef,
    ListConfigurationBundlesRequestPaginateTypeDef,
    ListConfigurationBundlesResponseTypeDef,
    ListConfigurationBundleVersionsRequestPaginateTypeDef,
    ListConfigurationBundleVersionsResponseTypeDef,
    ListConsentPortalsRequestPaginateTypeDef,
    ListConsentPortalsResponseTypeDef,
    ListDatasetExamplesRequestPaginateTypeDef,
    ListDatasetExamplesResponseTypeDef,
    ListDatasetsRequestPaginateTypeDef,
    ListDatasetsResponseTypeDef,
    ListDatasetVersionsRequestPaginateTypeDef,
    ListDatasetVersionsResponseTypeDef,
    ListEvaluatorsRequestPaginateTypeDef,
    ListEvaluatorsResponseTypeDef,
    ListGatewayRateLimitsRequestPaginateTypeDef,
    ListGatewayRateLimitsResponseTypeDef,
    ListGatewayRulesRequestPaginateTypeDef,
    ListGatewayRulesResponseTypeDef,
    ListGatewaysRequestPaginateTypeDef,
    ListGatewaysResponseTypeDef,
    ListGatewayTargetsRequestPaginateTypeDef,
    ListGatewayTargetsResponseTypeDef,
    ListHarnessEndpointsRequestPaginateTypeDef,
    ListHarnessEndpointsResponseTypeDef,
    ListHarnessesRequestPaginateTypeDef,
    ListHarnessesResponseTypeDef,
    ListHarnessVersionsRequestPaginateTypeDef,
    ListHarnessVersionsResponseTypeDef,
    ListMemoriesInputPaginateTypeDef,
    ListMemoriesOutputTypeDef,
    ListOauth2CredentialProvidersRequestPaginateTypeDef,
    ListOauth2CredentialProvidersResponseTypeDef,
    ListOnlineEvaluationConfigsRequestPaginateTypeDef,
    ListOnlineEvaluationConfigsResponseTypeDef,
    ListPaymentConnectorsRequestPaginateTypeDef,
    ListPaymentConnectorsResponseTypeDef,
    ListPaymentCredentialProvidersRequestPaginateTypeDef,
    ListPaymentCredentialProvidersResponseTypeDef,
    ListPaymentManagersRequestPaginateTypeDef,
    ListPaymentManagersResponseTypeDef,
    ListPoliciesRequestPaginateTypeDef,
    ListPoliciesResponseTypeDef,
    ListPolicyEnginesRequestPaginateTypeDef,
    ListPolicyEnginesResponseTypeDef,
    ListPolicyEngineSummariesRequestPaginateTypeDef,
    ListPolicyEngineSummariesResponseTypeDef,
    ListPolicyGenerationAssetsRequestPaginateTypeDef,
    ListPolicyGenerationAssetsResponseTypeDef,
    ListPolicyGenerationsRequestPaginateTypeDef,
    ListPolicyGenerationsResponseTypeDef,
    ListPolicyGenerationSummariesRequestPaginateTypeDef,
    ListPolicyGenerationSummariesResponseTypeDef,
    ListPolicySummariesRequestPaginateTypeDef,
    ListPolicySummariesResponseTypeDef,
    ListRegistriesRequestPaginateTypeDef,
    ListRegistriesResponseTypeDef,
    ListRegistryRecordsRequestPaginateTypeDef,
    ListRegistryRecordsResponseTypeDef,
    ListWorkloadIdentitiesRequestPaginateTypeDef,
    ListWorkloadIdentitiesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListAgentRuntimeEndpointsPaginator",
    "ListAgentRuntimeVersionsByCapacityProviderPaginator",
    "ListAgentRuntimeVersionsPaginator",
    "ListAgentRuntimesPaginator",
    "ListApiKeyCredentialProvidersPaginator",
    "ListBrowserProfilesPaginator",
    "ListBrowsersPaginator",
    "ListCapacityProvidersPaginator",
    "ListCodeInterpretersPaginator",
    "ListConfigurationBundleVersionsPaginator",
    "ListConfigurationBundlesPaginator",
    "ListConsentPortalsPaginator",
    "ListDatasetExamplesPaginator",
    "ListDatasetVersionsPaginator",
    "ListDatasetsPaginator",
    "ListEvaluatorsPaginator",
    "ListGatewayRateLimitsPaginator",
    "ListGatewayRulesPaginator",
    "ListGatewayTargetsPaginator",
    "ListGatewaysPaginator",
    "ListHarnessEndpointsPaginator",
    "ListHarnessVersionsPaginator",
    "ListHarnessesPaginator",
    "ListMemoriesPaginator",
    "ListOauth2CredentialProvidersPaginator",
    "ListOnlineEvaluationConfigsPaginator",
    "ListPaymentConnectorsPaginator",
    "ListPaymentCredentialProvidersPaginator",
    "ListPaymentManagersPaginator",
    "ListPoliciesPaginator",
    "ListPolicyEngineSummariesPaginator",
    "ListPolicyEnginesPaginator",
    "ListPolicyGenerationAssetsPaginator",
    "ListPolicyGenerationSummariesPaginator",
    "ListPolicyGenerationsPaginator",
    "ListPolicySummariesPaginator",
    "ListRegistriesPaginator",
    "ListRegistryRecordsPaginator",
    "ListWorkloadIdentitiesPaginator",
)

if TYPE_CHECKING:
    _ListAgentRuntimeEndpointsPaginatorBase = Paginator[ListAgentRuntimeEndpointsResponseTypeDef]
else:
    _ListAgentRuntimeEndpointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRuntimeEndpointsPaginator(_ListAgentRuntimeEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimeEndpoints.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimeEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimeendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRuntimeEndpointsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentRuntimeEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimeEndpoints.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimeEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimeendpointspaginator)
        """

if TYPE_CHECKING:
    _ListAgentRuntimeVersionsByCapacityProviderPaginatorBase = Paginator[
        ListAgentRuntimeVersionsByCapacityProviderOutputTypeDef
    ]
else:
    _ListAgentRuntimeVersionsByCapacityProviderPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRuntimeVersionsByCapacityProviderPaginator(
    _ListAgentRuntimeVersionsByCapacityProviderPaginatorBase
):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimeVersionsByCapacityProvider.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimeVersionsByCapacityProvider)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimeversionsbycapacityproviderpaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRuntimeVersionsByCapacityProviderInputPaginateTypeDef]
    ) -> PageIterator[ListAgentRuntimeVersionsByCapacityProviderOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimeVersionsByCapacityProvider.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimeVersionsByCapacityProvider.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimeversionsbycapacityproviderpaginator)
        """

if TYPE_CHECKING:
    _ListAgentRuntimeVersionsPaginatorBase = Paginator[ListAgentRuntimeVersionsResponseTypeDef]
else:
    _ListAgentRuntimeVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRuntimeVersionsPaginator(_ListAgentRuntimeVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimeVersions.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimeVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimeversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRuntimeVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentRuntimeVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimeVersions.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimeVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimeversionspaginator)
        """

if TYPE_CHECKING:
    _ListAgentRuntimesPaginatorBase = Paginator[ListAgentRuntimesResponseTypeDef]
else:
    _ListAgentRuntimesPaginatorBase = Paginator  # type: ignore[assignment]

class ListAgentRuntimesPaginator(_ListAgentRuntimesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimes.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimes)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListAgentRuntimesRequestPaginateTypeDef]
    ) -> PageIterator[ListAgentRuntimesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListAgentRuntimes.html#BedrockAgentCoreControl.Paginator.ListAgentRuntimes.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listagentruntimespaginator)
        """

if TYPE_CHECKING:
    _ListApiKeyCredentialProvidersPaginatorBase = Paginator[
        ListApiKeyCredentialProvidersResponseTypeDef
    ]
else:
    _ListApiKeyCredentialProvidersPaginatorBase = Paginator  # type: ignore[assignment]

class ListApiKeyCredentialProvidersPaginator(_ListApiKeyCredentialProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListApiKeyCredentialProviders.html#BedrockAgentCoreControl.Paginator.ListApiKeyCredentialProviders)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listapikeycredentialproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListApiKeyCredentialProvidersRequestPaginateTypeDef]
    ) -> PageIterator[ListApiKeyCredentialProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListApiKeyCredentialProviders.html#BedrockAgentCoreControl.Paginator.ListApiKeyCredentialProviders.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listapikeycredentialproviderspaginator)
        """

if TYPE_CHECKING:
    _ListBrowserProfilesPaginatorBase = Paginator[ListBrowserProfilesResponseTypeDef]
else:
    _ListBrowserProfilesPaginatorBase = Paginator  # type: ignore[assignment]

class ListBrowserProfilesPaginator(_ListBrowserProfilesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListBrowserProfiles.html#BedrockAgentCoreControl.Paginator.ListBrowserProfiles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listbrowserprofilespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrowserProfilesRequestPaginateTypeDef]
    ) -> PageIterator[ListBrowserProfilesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListBrowserProfiles.html#BedrockAgentCoreControl.Paginator.ListBrowserProfiles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listbrowserprofilespaginator)
        """

if TYPE_CHECKING:
    _ListBrowsersPaginatorBase = Paginator[ListBrowsersResponseTypeDef]
else:
    _ListBrowsersPaginatorBase = Paginator  # type: ignore[assignment]

class ListBrowsersPaginator(_ListBrowsersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListBrowsers.html#BedrockAgentCoreControl.Paginator.ListBrowsers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listbrowserspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListBrowsersRequestPaginateTypeDef]
    ) -> PageIterator[ListBrowsersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListBrowsers.html#BedrockAgentCoreControl.Paginator.ListBrowsers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listbrowserspaginator)
        """

if TYPE_CHECKING:
    _ListCapacityProvidersPaginatorBase = Paginator[ListCapacityProvidersOutputTypeDef]
else:
    _ListCapacityProvidersPaginatorBase = Paginator  # type: ignore[assignment]

class ListCapacityProvidersPaginator(_ListCapacityProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListCapacityProviders.html#BedrockAgentCoreControl.Paginator.ListCapacityProviders)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listcapacityproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCapacityProvidersInputPaginateTypeDef]
    ) -> PageIterator[ListCapacityProvidersOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListCapacityProviders.html#BedrockAgentCoreControl.Paginator.ListCapacityProviders.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listcapacityproviderspaginator)
        """

if TYPE_CHECKING:
    _ListCodeInterpretersPaginatorBase = Paginator[ListCodeInterpretersResponseTypeDef]
else:
    _ListCodeInterpretersPaginatorBase = Paginator  # type: ignore[assignment]

class ListCodeInterpretersPaginator(_ListCodeInterpretersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListCodeInterpreters.html#BedrockAgentCoreControl.Paginator.ListCodeInterpreters)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listcodeinterpreterspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListCodeInterpretersRequestPaginateTypeDef]
    ) -> PageIterator[ListCodeInterpretersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListCodeInterpreters.html#BedrockAgentCoreControl.Paginator.ListCodeInterpreters.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listcodeinterpreterspaginator)
        """

if TYPE_CHECKING:
    _ListConfigurationBundleVersionsPaginatorBase = Paginator[
        ListConfigurationBundleVersionsResponseTypeDef
    ]
else:
    _ListConfigurationBundleVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListConfigurationBundleVersionsPaginator(_ListConfigurationBundleVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListConfigurationBundleVersions.html#BedrockAgentCoreControl.Paginator.ListConfigurationBundleVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listconfigurationbundleversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationBundleVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListConfigurationBundleVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListConfigurationBundleVersions.html#BedrockAgentCoreControl.Paginator.ListConfigurationBundleVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listconfigurationbundleversionspaginator)
        """

if TYPE_CHECKING:
    _ListConfigurationBundlesPaginatorBase = Paginator[ListConfigurationBundlesResponseTypeDef]
else:
    _ListConfigurationBundlesPaginatorBase = Paginator  # type: ignore[assignment]

class ListConfigurationBundlesPaginator(_ListConfigurationBundlesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListConfigurationBundles.html#BedrockAgentCoreControl.Paginator.ListConfigurationBundles)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listconfigurationbundlespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConfigurationBundlesRequestPaginateTypeDef]
    ) -> PageIterator[ListConfigurationBundlesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListConfigurationBundles.html#BedrockAgentCoreControl.Paginator.ListConfigurationBundles.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listconfigurationbundlespaginator)
        """

if TYPE_CHECKING:
    _ListConsentPortalsPaginatorBase = Paginator[ListConsentPortalsResponseTypeDef]
else:
    _ListConsentPortalsPaginatorBase = Paginator  # type: ignore[assignment]

class ListConsentPortalsPaginator(_ListConsentPortalsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListConsentPortals.html#BedrockAgentCoreControl.Paginator.ListConsentPortals)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listconsentportalspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListConsentPortalsRequestPaginateTypeDef]
    ) -> PageIterator[ListConsentPortalsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListConsentPortals.html#BedrockAgentCoreControl.Paginator.ListConsentPortals.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listconsentportalspaginator)
        """

if TYPE_CHECKING:
    _ListDatasetExamplesPaginatorBase = Paginator[ListDatasetExamplesResponseTypeDef]
else:
    _ListDatasetExamplesPaginatorBase = Paginator  # type: ignore[assignment]

class ListDatasetExamplesPaginator(_ListDatasetExamplesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListDatasetExamples.html#BedrockAgentCoreControl.Paginator.ListDatasetExamples)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listdatasetexamplespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetExamplesRequestPaginateTypeDef]
    ) -> PageIterator[ListDatasetExamplesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListDatasetExamples.html#BedrockAgentCoreControl.Paginator.ListDatasetExamples.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listdatasetexamplespaginator)
        """

if TYPE_CHECKING:
    _ListDatasetVersionsPaginatorBase = Paginator[ListDatasetVersionsResponseTypeDef]
else:
    _ListDatasetVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDatasetVersionsPaginator(_ListDatasetVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListDatasetVersions.html#BedrockAgentCoreControl.Paginator.ListDatasetVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listdatasetversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListDatasetVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListDatasetVersions.html#BedrockAgentCoreControl.Paginator.ListDatasetVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listdatasetversionspaginator)
        """

if TYPE_CHECKING:
    _ListDatasetsPaginatorBase = Paginator[ListDatasetsResponseTypeDef]
else:
    _ListDatasetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListDatasetsPaginator(_ListDatasetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListDatasets.html#BedrockAgentCoreControl.Paginator.ListDatasets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listdatasetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListDatasetsRequestPaginateTypeDef]
    ) -> PageIterator[ListDatasetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListDatasets.html#BedrockAgentCoreControl.Paginator.ListDatasets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listdatasetspaginator)
        """

if TYPE_CHECKING:
    _ListEvaluatorsPaginatorBase = Paginator[ListEvaluatorsResponseTypeDef]
else:
    _ListEvaluatorsPaginatorBase = Paginator  # type: ignore[assignment]

class ListEvaluatorsPaginator(_ListEvaluatorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListEvaluators.html#BedrockAgentCoreControl.Paginator.ListEvaluators)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listevaluatorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListEvaluatorsRequestPaginateTypeDef]
    ) -> PageIterator[ListEvaluatorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListEvaluators.html#BedrockAgentCoreControl.Paginator.ListEvaluators.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listevaluatorspaginator)
        """

if TYPE_CHECKING:
    _ListGatewayRateLimitsPaginatorBase = Paginator[ListGatewayRateLimitsResponseTypeDef]
else:
    _ListGatewayRateLimitsPaginatorBase = Paginator  # type: ignore[assignment]

class ListGatewayRateLimitsPaginator(_ListGatewayRateLimitsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGatewayRateLimits.html#BedrockAgentCoreControl.Paginator.ListGatewayRateLimits)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewayratelimitspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewayRateLimitsRequestPaginateTypeDef]
    ) -> PageIterator[ListGatewayRateLimitsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGatewayRateLimits.html#BedrockAgentCoreControl.Paginator.ListGatewayRateLimits.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewayratelimitspaginator)
        """

if TYPE_CHECKING:
    _ListGatewayRulesPaginatorBase = Paginator[ListGatewayRulesResponseTypeDef]
else:
    _ListGatewayRulesPaginatorBase = Paginator  # type: ignore[assignment]

class ListGatewayRulesPaginator(_ListGatewayRulesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGatewayRules.html#BedrockAgentCoreControl.Paginator.ListGatewayRules)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewayrulespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewayRulesRequestPaginateTypeDef]
    ) -> PageIterator[ListGatewayRulesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGatewayRules.html#BedrockAgentCoreControl.Paginator.ListGatewayRules.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewayrulespaginator)
        """

if TYPE_CHECKING:
    _ListGatewayTargetsPaginatorBase = Paginator[ListGatewayTargetsResponseTypeDef]
else:
    _ListGatewayTargetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListGatewayTargetsPaginator(_ListGatewayTargetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGatewayTargets.html#BedrockAgentCoreControl.Paginator.ListGatewayTargets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewaytargetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewayTargetsRequestPaginateTypeDef]
    ) -> PageIterator[ListGatewayTargetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGatewayTargets.html#BedrockAgentCoreControl.Paginator.ListGatewayTargets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewaytargetspaginator)
        """

if TYPE_CHECKING:
    _ListGatewaysPaginatorBase = Paginator[ListGatewaysResponseTypeDef]
else:
    _ListGatewaysPaginatorBase = Paginator  # type: ignore[assignment]

class ListGatewaysPaginator(_ListGatewaysPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGateways.html#BedrockAgentCoreControl.Paginator.ListGateways)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewayspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListGatewaysRequestPaginateTypeDef]
    ) -> PageIterator[ListGatewaysResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListGateways.html#BedrockAgentCoreControl.Paginator.ListGateways.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listgatewayspaginator)
        """

if TYPE_CHECKING:
    _ListHarnessEndpointsPaginatorBase = Paginator[ListHarnessEndpointsResponseTypeDef]
else:
    _ListHarnessEndpointsPaginatorBase = Paginator  # type: ignore[assignment]

class ListHarnessEndpointsPaginator(_ListHarnessEndpointsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListHarnessEndpoints.html#BedrockAgentCoreControl.Paginator.ListHarnessEndpoints)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listharnessendpointspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHarnessEndpointsRequestPaginateTypeDef]
    ) -> PageIterator[ListHarnessEndpointsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListHarnessEndpoints.html#BedrockAgentCoreControl.Paginator.ListHarnessEndpoints.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listharnessendpointspaginator)
        """

if TYPE_CHECKING:
    _ListHarnessVersionsPaginatorBase = Paginator[ListHarnessVersionsResponseTypeDef]
else:
    _ListHarnessVersionsPaginatorBase = Paginator  # type: ignore[assignment]

class ListHarnessVersionsPaginator(_ListHarnessVersionsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListHarnessVersions.html#BedrockAgentCoreControl.Paginator.ListHarnessVersions)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listharnessversionspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHarnessVersionsRequestPaginateTypeDef]
    ) -> PageIterator[ListHarnessVersionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListHarnessVersions.html#BedrockAgentCoreControl.Paginator.ListHarnessVersions.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listharnessversionspaginator)
        """

if TYPE_CHECKING:
    _ListHarnessesPaginatorBase = Paginator[ListHarnessesResponseTypeDef]
else:
    _ListHarnessesPaginatorBase = Paginator  # type: ignore[assignment]

class ListHarnessesPaginator(_ListHarnessesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListHarnesses.html#BedrockAgentCoreControl.Paginator.ListHarnesses)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listharnessespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListHarnessesRequestPaginateTypeDef]
    ) -> PageIterator[ListHarnessesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListHarnesses.html#BedrockAgentCoreControl.Paginator.ListHarnesses.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listharnessespaginator)
        """

if TYPE_CHECKING:
    _ListMemoriesPaginatorBase = Paginator[ListMemoriesOutputTypeDef]
else:
    _ListMemoriesPaginatorBase = Paginator  # type: ignore[assignment]

class ListMemoriesPaginator(_ListMemoriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListMemories.html#BedrockAgentCoreControl.Paginator.ListMemories)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listmemoriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListMemoriesInputPaginateTypeDef]
    ) -> PageIterator[ListMemoriesOutputTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListMemories.html#BedrockAgentCoreControl.Paginator.ListMemories.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listmemoriespaginator)
        """

if TYPE_CHECKING:
    _ListOauth2CredentialProvidersPaginatorBase = Paginator[
        ListOauth2CredentialProvidersResponseTypeDef
    ]
else:
    _ListOauth2CredentialProvidersPaginatorBase = Paginator  # type: ignore[assignment]

class ListOauth2CredentialProvidersPaginator(_ListOauth2CredentialProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListOauth2CredentialProviders.html#BedrockAgentCoreControl.Paginator.ListOauth2CredentialProviders)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listoauth2credentialproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOauth2CredentialProvidersRequestPaginateTypeDef]
    ) -> PageIterator[ListOauth2CredentialProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListOauth2CredentialProviders.html#BedrockAgentCoreControl.Paginator.ListOauth2CredentialProviders.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listoauth2credentialproviderspaginator)
        """

if TYPE_CHECKING:
    _ListOnlineEvaluationConfigsPaginatorBase = Paginator[
        ListOnlineEvaluationConfigsResponseTypeDef
    ]
else:
    _ListOnlineEvaluationConfigsPaginatorBase = Paginator  # type: ignore[assignment]

class ListOnlineEvaluationConfigsPaginator(_ListOnlineEvaluationConfigsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListOnlineEvaluationConfigs.html#BedrockAgentCoreControl.Paginator.ListOnlineEvaluationConfigs)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listonlineevaluationconfigspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListOnlineEvaluationConfigsRequestPaginateTypeDef]
    ) -> PageIterator[ListOnlineEvaluationConfigsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListOnlineEvaluationConfigs.html#BedrockAgentCoreControl.Paginator.ListOnlineEvaluationConfigs.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listonlineevaluationconfigspaginator)
        """

if TYPE_CHECKING:
    _ListPaymentConnectorsPaginatorBase = Paginator[ListPaymentConnectorsResponseTypeDef]
else:
    _ListPaymentConnectorsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPaymentConnectorsPaginator(_ListPaymentConnectorsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPaymentConnectors.html#BedrockAgentCoreControl.Paginator.ListPaymentConnectors)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpaymentconnectorspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPaymentConnectorsRequestPaginateTypeDef]
    ) -> PageIterator[ListPaymentConnectorsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPaymentConnectors.html#BedrockAgentCoreControl.Paginator.ListPaymentConnectors.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpaymentconnectorspaginator)
        """

if TYPE_CHECKING:
    _ListPaymentCredentialProvidersPaginatorBase = Paginator[
        ListPaymentCredentialProvidersResponseTypeDef
    ]
else:
    _ListPaymentCredentialProvidersPaginatorBase = Paginator  # type: ignore[assignment]

class ListPaymentCredentialProvidersPaginator(_ListPaymentCredentialProvidersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPaymentCredentialProviders.html#BedrockAgentCoreControl.Paginator.ListPaymentCredentialProviders)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpaymentcredentialproviderspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPaymentCredentialProvidersRequestPaginateTypeDef]
    ) -> PageIterator[ListPaymentCredentialProvidersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPaymentCredentialProviders.html#BedrockAgentCoreControl.Paginator.ListPaymentCredentialProviders.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpaymentcredentialproviderspaginator)
        """

if TYPE_CHECKING:
    _ListPaymentManagersPaginatorBase = Paginator[ListPaymentManagersResponseTypeDef]
else:
    _ListPaymentManagersPaginatorBase = Paginator  # type: ignore[assignment]

class ListPaymentManagersPaginator(_ListPaymentManagersPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPaymentManagers.html#BedrockAgentCoreControl.Paginator.ListPaymentManagers)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpaymentmanagerspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPaymentManagersRequestPaginateTypeDef]
    ) -> PageIterator[ListPaymentManagersResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPaymentManagers.html#BedrockAgentCoreControl.Paginator.ListPaymentManagers.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpaymentmanagerspaginator)
        """

if TYPE_CHECKING:
    _ListPoliciesPaginatorBase = Paginator[ListPoliciesResponseTypeDef]
else:
    _ListPoliciesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPoliciesPaginator(_ListPoliciesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicies.html#BedrockAgentCoreControl.Paginator.ListPolicies)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpoliciespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPoliciesRequestPaginateTypeDef]
    ) -> PageIterator[ListPoliciesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicies.html#BedrockAgentCoreControl.Paginator.ListPolicies.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpoliciespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyEngineSummariesPaginatorBase = Paginator[ListPolicyEngineSummariesResponseTypeDef]
else:
    _ListPolicyEngineSummariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPolicyEngineSummariesPaginator(_ListPolicyEngineSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyEngineSummaries.html#BedrockAgentCoreControl.Paginator.ListPolicyEngineSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicyenginesummariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyEngineSummariesRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicyEngineSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyEngineSummaries.html#BedrockAgentCoreControl.Paginator.ListPolicyEngineSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicyenginesummariespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyEnginesPaginatorBase = Paginator[ListPolicyEnginesResponseTypeDef]
else:
    _ListPolicyEnginesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPolicyEnginesPaginator(_ListPolicyEnginesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyEngines.html#BedrockAgentCoreControl.Paginator.ListPolicyEngines)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicyenginespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyEnginesRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicyEnginesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyEngines.html#BedrockAgentCoreControl.Paginator.ListPolicyEngines.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicyenginespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyGenerationAssetsPaginatorBase = Paginator[ListPolicyGenerationAssetsResponseTypeDef]
else:
    _ListPolicyGenerationAssetsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPolicyGenerationAssetsPaginator(_ListPolicyGenerationAssetsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyGenerationAssets.html#BedrockAgentCoreControl.Paginator.ListPolicyGenerationAssets)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicygenerationassetspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyGenerationAssetsRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicyGenerationAssetsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyGenerationAssets.html#BedrockAgentCoreControl.Paginator.ListPolicyGenerationAssets.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicygenerationassetspaginator)
        """

if TYPE_CHECKING:
    _ListPolicyGenerationSummariesPaginatorBase = Paginator[
        ListPolicyGenerationSummariesResponseTypeDef
    ]
else:
    _ListPolicyGenerationSummariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPolicyGenerationSummariesPaginator(_ListPolicyGenerationSummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyGenerationSummaries.html#BedrockAgentCoreControl.Paginator.ListPolicyGenerationSummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicygenerationsummariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyGenerationSummariesRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicyGenerationSummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyGenerationSummaries.html#BedrockAgentCoreControl.Paginator.ListPolicyGenerationSummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicygenerationsummariespaginator)
        """

if TYPE_CHECKING:
    _ListPolicyGenerationsPaginatorBase = Paginator[ListPolicyGenerationsResponseTypeDef]
else:
    _ListPolicyGenerationsPaginatorBase = Paginator  # type: ignore[assignment]

class ListPolicyGenerationsPaginator(_ListPolicyGenerationsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyGenerations.html#BedrockAgentCoreControl.Paginator.ListPolicyGenerations)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicygenerationspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicyGenerationsRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicyGenerationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicyGenerations.html#BedrockAgentCoreControl.Paginator.ListPolicyGenerations.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicygenerationspaginator)
        """

if TYPE_CHECKING:
    _ListPolicySummariesPaginatorBase = Paginator[ListPolicySummariesResponseTypeDef]
else:
    _ListPolicySummariesPaginatorBase = Paginator  # type: ignore[assignment]

class ListPolicySummariesPaginator(_ListPolicySummariesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicySummaries.html#BedrockAgentCoreControl.Paginator.ListPolicySummaries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicysummariespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListPolicySummariesRequestPaginateTypeDef]
    ) -> PageIterator[ListPolicySummariesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListPolicySummaries.html#BedrockAgentCoreControl.Paginator.ListPolicySummaries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listpolicysummariespaginator)
        """

if TYPE_CHECKING:
    _ListRegistriesPaginatorBase = Paginator[ListRegistriesResponseTypeDef]
else:
    _ListRegistriesPaginatorBase = Paginator  # type: ignore[assignment]

class ListRegistriesPaginator(_ListRegistriesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListRegistries.html#BedrockAgentCoreControl.Paginator.ListRegistries)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listregistriespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistriesRequestPaginateTypeDef]
    ) -> PageIterator[ListRegistriesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListRegistries.html#BedrockAgentCoreControl.Paginator.ListRegistries.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listregistriespaginator)
        """

if TYPE_CHECKING:
    _ListRegistryRecordsPaginatorBase = Paginator[ListRegistryRecordsResponseTypeDef]
else:
    _ListRegistryRecordsPaginatorBase = Paginator  # type: ignore[assignment]

class ListRegistryRecordsPaginator(_ListRegistryRecordsPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListRegistryRecords.html#BedrockAgentCoreControl.Paginator.ListRegistryRecords)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listregistryrecordspaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListRegistryRecordsRequestPaginateTypeDef]
    ) -> PageIterator[ListRegistryRecordsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListRegistryRecords.html#BedrockAgentCoreControl.Paginator.ListRegistryRecords.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listregistryrecordspaginator)
        """

if TYPE_CHECKING:
    _ListWorkloadIdentitiesPaginatorBase = Paginator[ListWorkloadIdentitiesResponseTypeDef]
else:
    _ListWorkloadIdentitiesPaginatorBase = Paginator  # type: ignore[assignment]

class ListWorkloadIdentitiesPaginator(_ListWorkloadIdentitiesPaginatorBase):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListWorkloadIdentities.html#BedrockAgentCoreControl.Paginator.ListWorkloadIdentities)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listworkloadidentitiespaginator)
    """
    def paginate(  # type: ignore[override]
        self, **kwargs: Unpack[ListWorkloadIdentitiesRequestPaginateTypeDef]
    ) -> PageIterator[ListWorkloadIdentitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-agentcore-control/paginator/ListWorkloadIdentities.html#BedrockAgentCoreControl.Paginator.ListWorkloadIdentities.paginate)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_bedrock_agentcore_control/paginators/#listworkloadidentitiespaginator)
        """
