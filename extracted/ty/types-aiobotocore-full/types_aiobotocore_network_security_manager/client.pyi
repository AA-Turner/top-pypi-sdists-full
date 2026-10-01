"""
Type annotations for network-security-manager service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_network_security_manager.client import NetworkSecurityManagerCustomerAPIClient

    session = get_session()
    async with session.create_client("network-security-manager") as client:
        client: NetworkSecurityManagerCustomerAPIClient
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
    ListAdminAccountsPaginator,
    ListAggregateResourceSynchronizationStatusesPaginator,
    ListDeploymentSnapshotsPaginator,
    ListDeploymentsPaginator,
    ListPoliciesPaginator,
    ListPolicySnapshotsPaginator,
    ListResourceAssociationsPaginator,
    ListResourceSynchronizationStatusesPaginator,
    ListRuleSnapshotsPaginator,
    ListRulesPaginator,
    ListScopeSnapshotsPaginator,
    ListScopesPaginator,
    ListTemplateSnapshotsPaginator,
    ListTemplatesPaginator,
)
from .type_defs import (
    CreateDeploymentInputTypeDef,
    CreateDeploymentOutputTypeDef,
    CreateDeploymentSnapshotInputTypeDef,
    CreateDeploymentSnapshotOutputTypeDef,
    CreatePolicyInputTypeDef,
    CreatePolicyOutputTypeDef,
    CreatePolicySnapshotInputTypeDef,
    CreatePolicySnapshotOutputTypeDef,
    CreateRuleInputTypeDef,
    CreateRuleOutputTypeDef,
    CreateRuleSnapshotInputTypeDef,
    CreateRuleSnapshotOutputTypeDef,
    CreateScopeInputTypeDef,
    CreateScopeOutputTypeDef,
    CreateScopeSnapshotInputTypeDef,
    CreateScopeSnapshotOutputTypeDef,
    CreateTemplateInputTypeDef,
    CreateTemplateOutputTypeDef,
    CreateTemplateSnapshotInputTypeDef,
    CreateTemplateSnapshotOutputTypeDef,
    DeleteAdminAccountRequestTypeDef,
    DeleteDeploymentInputTypeDef,
    DeletePolicyInputTypeDef,
    DeleteRuleInputTypeDef,
    DeleteScopeInputTypeDef,
    DeleteTemplateInputTypeDef,
    EmptyResponseMetadataTypeDef,
    GenerateRuleConfigurationRequestTypeDef,
    GenerateRuleConfigurationResponseTypeDef,
    GetAdminAccountRequestTypeDef,
    GetAdminAccountResponseTypeDef,
    GetDeploymentInputTypeDef,
    GetDeploymentOutputTypeDef,
    GetPolicyInputTypeDef,
    GetPolicyOutputTypeDef,
    GetRuleInputTypeDef,
    GetRuleOutputTypeDef,
    GetScopeInputTypeDef,
    GetScopeOutputTypeDef,
    GetTemplateInputTypeDef,
    GetTemplateOutputTypeDef,
    ListAdminAccountsRequestTypeDef,
    ListAdminAccountsResponseTypeDef,
    ListAggregateResourceSynchronizationStatusesInputTypeDef,
    ListAggregateResourceSynchronizationStatusesOutputTypeDef,
    ListDeploymentsInputTypeDef,
    ListDeploymentSnapshotsInputTypeDef,
    ListDeploymentSnapshotsOutputTypeDef,
    ListDeploymentsOutputTypeDef,
    ListPoliciesInputTypeDef,
    ListPoliciesOutputTypeDef,
    ListPolicySnapshotsInputTypeDef,
    ListPolicySnapshotsOutputTypeDef,
    ListResourceAssociationsInputTypeDef,
    ListResourceAssociationsOutputTypeDef,
    ListResourceSynchronizationStatusesInputTypeDef,
    ListResourceSynchronizationStatusesOutputTypeDef,
    ListRulesInputTypeDef,
    ListRuleSnapshotsInputTypeDef,
    ListRuleSnapshotsOutputTypeDef,
    ListRulesOutputTypeDef,
    ListScopesInputTypeDef,
    ListScopeSnapshotsInputTypeDef,
    ListScopeSnapshotsOutputTypeDef,
    ListScopesOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTemplatesInputTypeDef,
    ListTemplateSnapshotsInputTypeDef,
    ListTemplateSnapshotsOutputTypeDef,
    ListTemplatesOutputTypeDef,
    PutAdminAccountRequestTypeDef,
    PutAdminAccountResponseTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateDeploymentInputTypeDef,
    UpdateDeploymentOutputTypeDef,
    UpdatePolicyInputTypeDef,
    UpdatePolicyOutputTypeDef,
    UpdateRuleInputTypeDef,
    UpdateRuleOutputTypeDef,
    UpdateScopeInputTypeDef,
    UpdateScopeOutputTypeDef,
    UpdateTemplateInputTypeDef,
    UpdateTemplateOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("NetworkSecurityManagerCustomerAPIClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ServiceUnavailableException: type[BotocoreClientError]
    TagPolicyViolationException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class NetworkSecurityManagerCustomerAPIClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager.html#NetworkSecurityManagerCustomerAPI.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        NetworkSecurityManagerCustomerAPIClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager.html#NetworkSecurityManagerCustomerAPI.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#generate_presigned_url)
        """

    async def create_deployment(
        self, **kwargs: Unpack[CreateDeploymentInputTypeDef]
    ) -> CreateDeploymentOutputTypeDef:
        """
        Creates a deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_deployment)
        """

    async def create_deployment_snapshot(
        self, **kwargs: Unpack[CreateDeploymentSnapshotInputTypeDef]
    ) -> CreateDeploymentSnapshotOutputTypeDef:
        """
        Creates a snapshot of the current published version of the specified deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_deployment_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_deployment_snapshot)
        """

    async def create_policy(
        self, **kwargs: Unpack[CreatePolicyInputTypeDef]
    ) -> CreatePolicyOutputTypeDef:
        """
        Creates a policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_policy)
        """

    async def create_policy_snapshot(
        self, **kwargs: Unpack[CreatePolicySnapshotInputTypeDef]
    ) -> CreatePolicySnapshotOutputTypeDef:
        """
        Creates a snapshot of the current published version of the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_policy_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_policy_snapshot)
        """

    async def create_rule(
        self, **kwargs: Unpack[CreateRuleInputTypeDef]
    ) -> CreateRuleOutputTypeDef:
        """
        Creates a rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_rule)
        """

    async def create_rule_snapshot(
        self, **kwargs: Unpack[CreateRuleSnapshotInputTypeDef]
    ) -> CreateRuleSnapshotOutputTypeDef:
        """
        Creates a snapshot of the current published version of the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_rule_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_rule_snapshot)
        """

    async def create_scope(
        self, **kwargs: Unpack[CreateScopeInputTypeDef]
    ) -> CreateScopeOutputTypeDef:
        """
        Creates a scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_scope)
        """

    async def create_scope_snapshot(
        self, **kwargs: Unpack[CreateScopeSnapshotInputTypeDef]
    ) -> CreateScopeSnapshotOutputTypeDef:
        """
        Creates a snapshot of the current published version of the specified scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_scope_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_scope_snapshot)
        """

    async def create_template(
        self, **kwargs: Unpack[CreateTemplateInputTypeDef]
    ) -> CreateTemplateOutputTypeDef:
        """
        Creates a template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_template)
        """

    async def create_template_snapshot(
        self, **kwargs: Unpack[CreateTemplateSnapshotInputTypeDef]
    ) -> CreateTemplateSnapshotOutputTypeDef:
        """
        Creates a snapshot of the current published version of the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/create_template_snapshot.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#create_template_snapshot)
        """

    async def delete_admin_account(
        self, **kwargs: Unpack[DeleteAdminAccountRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the specified AWS Network Security Manager administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/delete_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#delete_admin_account)
        """

    async def delete_deployment(
        self, **kwargs: Unpack[DeleteDeploymentInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/delete_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#delete_deployment)
        """

    async def delete_policy(
        self, **kwargs: Unpack[DeletePolicyInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/delete_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#delete_policy)
        """

    async def delete_rule(
        self, **kwargs: Unpack[DeleteRuleInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/delete_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#delete_rule)
        """

    async def delete_scope(
        self, **kwargs: Unpack[DeleteScopeInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/delete_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#delete_scope)
        """

    async def delete_template(
        self, **kwargs: Unpack[DeleteTemplateInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/delete_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#delete_template)
        """

    async def generate_rule_configuration(
        self, **kwargs: Unpack[GenerateRuleConfigurationRequestTypeDef]
    ) -> GenerateRuleConfigurationResponseTypeDef:
        """
        Generates a rule configuration from a natural-language description.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/generate_rule_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#generate_rule_configuration)
        """

    async def get_admin_account(
        self, **kwargs: Unpack[GetAdminAccountRequestTypeDef]
    ) -> GetAdminAccountResponseTypeDef:
        """
        Retrieves the details of the specified AWS Network Security Manager
        administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_admin_account)
        """

    async def get_deployment(
        self, **kwargs: Unpack[GetDeploymentInputTypeDef]
    ) -> GetDeploymentOutputTypeDef:
        """
        Retrieves the details of the specified deployment, including coverage
        information and any warnings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_deployment)
        """

    async def get_policy(self, **kwargs: Unpack[GetPolicyInputTypeDef]) -> GetPolicyOutputTypeDef:
        """
        Retrieves the details of the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_policy)
        """

    async def get_rule(self, **kwargs: Unpack[GetRuleInputTypeDef]) -> GetRuleOutputTypeDef:
        """
        Retrieves the details of the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_rule)
        """

    async def get_scope(self, **kwargs: Unpack[GetScopeInputTypeDef]) -> GetScopeOutputTypeDef:
        """
        Retrieves the details of the specified scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_scope)
        """

    async def get_template(
        self, **kwargs: Unpack[GetTemplateInputTypeDef]
    ) -> GetTemplateOutputTypeDef:
        """
        Retrieves the details of the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_template)
        """

    async def list_admin_accounts(
        self, **kwargs: Unpack[ListAdminAccountsRequestTypeDef]
    ) -> ListAdminAccountsResponseTypeDef:
        """
        Lists the AWS Network Security Manager administrator accounts in the
        organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_admin_accounts.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_admin_accounts)
        """

    async def list_aggregate_resource_synchronization_statuses(
        self, **kwargs: Unpack[ListAggregateResourceSynchronizationStatusesInputTypeDef]
    ) -> ListAggregateResourceSynchronizationStatusesOutputTypeDef:
        """
        Lists the aggregated synchronization statuses of resources across the
        deployments in your administrator account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_aggregate_resource_synchronization_statuses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_aggregate_resource_synchronization_statuses)
        """

    async def list_deployment_snapshots(
        self, **kwargs: Unpack[ListDeploymentSnapshotsInputTypeDef]
    ) -> ListDeploymentSnapshotsOutputTypeDef:
        """
        Lists the snapshots of the specified deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_deployment_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_deployment_snapshots)
        """

    async def list_deployments(
        self, **kwargs: Unpack[ListDeploymentsInputTypeDef]
    ) -> ListDeploymentsOutputTypeDef:
        """
        Lists the deployments in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_deployments.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_deployments)
        """

    async def list_policies(
        self, **kwargs: Unpack[ListPoliciesInputTypeDef]
    ) -> ListPoliciesOutputTypeDef:
        """
        Lists the policies in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_policies.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_policies)
        """

    async def list_policy_snapshots(
        self, **kwargs: Unpack[ListPolicySnapshotsInputTypeDef]
    ) -> ListPolicySnapshotsOutputTypeDef:
        """
        Lists the snapshots of the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_policy_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_policy_snapshots)
        """

    async def list_resource_associations(
        self, **kwargs: Unpack[ListResourceAssociationsInputTypeDef]
    ) -> ListResourceAssociationsOutputTypeDef:
        """
        Lists the resources associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_resource_associations.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_resource_associations)
        """

    async def list_resource_synchronization_statuses(
        self, **kwargs: Unpack[ListResourceSynchronizationStatusesInputTypeDef]
    ) -> ListResourceSynchronizationStatusesOutputTypeDef:
        """
        Lists the synchronization statuses of the resources covered by the specified
        deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_resource_synchronization_statuses.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_resource_synchronization_statuses)
        """

    async def list_rule_snapshots(
        self, **kwargs: Unpack[ListRuleSnapshotsInputTypeDef]
    ) -> ListRuleSnapshotsOutputTypeDef:
        """
        Lists the snapshots of the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_rule_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_rule_snapshots)
        """

    async def list_rules(self, **kwargs: Unpack[ListRulesInputTypeDef]) -> ListRulesOutputTypeDef:
        """
        Lists the rules in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_rules.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_rules)
        """

    async def list_scope_snapshots(
        self, **kwargs: Unpack[ListScopeSnapshotsInputTypeDef]
    ) -> ListScopeSnapshotsOutputTypeDef:
        """
        Lists the snapshots of the specified scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_scope_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_scope_snapshots)
        """

    async def list_scopes(
        self, **kwargs: Unpack[ListScopesInputTypeDef]
    ) -> ListScopesOutputTypeDef:
        """
        Lists the scopes in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_scopes.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_scopes)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_tags_for_resource)
        """

    async def list_template_snapshots(
        self, **kwargs: Unpack[ListTemplateSnapshotsInputTypeDef]
    ) -> ListTemplateSnapshotsOutputTypeDef:
        """
        Lists the snapshots of the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_template_snapshots.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_template_snapshots)
        """

    async def list_templates(
        self, **kwargs: Unpack[ListTemplatesInputTypeDef]
    ) -> ListTemplatesOutputTypeDef:
        """
        Lists the templates in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/list_templates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#list_templates)
        """

    async def put_admin_account(
        self, **kwargs: Unpack[PutAdminAccountRequestTypeDef]
    ) -> PutAdminAccountResponseTypeDef:
        """
        Sets the AWS account that serves as an AWS Network Security Manager
        administrator account, and optionally configures the scope of resources that
        the administrator can manage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/put_admin_account.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#put_admin_account)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds or overwrites the specified tags on the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes the specified tags from the given resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#untag_resource)
        """

    async def update_deployment(
        self, **kwargs: Unpack[UpdateDeploymentInputTypeDef]
    ) -> UpdateDeploymentOutputTypeDef:
        """
        Updates the specified deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/update_deployment.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#update_deployment)
        """

    async def update_policy(
        self, **kwargs: Unpack[UpdatePolicyInputTypeDef]
    ) -> UpdatePolicyOutputTypeDef:
        """
        Updates the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/update_policy.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#update_policy)
        """

    async def update_rule(
        self, **kwargs: Unpack[UpdateRuleInputTypeDef]
    ) -> UpdateRuleOutputTypeDef:
        """
        Updates the specified rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/update_rule.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#update_rule)
        """

    async def update_scope(
        self, **kwargs: Unpack[UpdateScopeInputTypeDef]
    ) -> UpdateScopeOutputTypeDef:
        """
        Updates the specified scope.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/update_scope.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#update_scope)
        """

    async def update_template(
        self, **kwargs: Unpack[UpdateTemplateInputTypeDef]
    ) -> UpdateTemplateOutputTypeDef:
        """
        Updates the specified template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/update_template.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#update_template)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_admin_accounts"]
    ) -> ListAdminAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_aggregate_resource_synchronization_statuses"]
    ) -> ListAggregateResourceSynchronizationStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployment_snapshots"]
    ) -> ListDeploymentSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_deployments"]
    ) -> ListDeploymentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policies"]
    ) -> ListPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_policy_snapshots"]
    ) -> ListPolicySnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_associations"]
    ) -> ListResourceAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_synchronization_statuses"]
    ) -> ListResourceSynchronizationStatusesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rule_snapshots"]
    ) -> ListRuleSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_rules"]
    ) -> ListRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scope_snapshots"]
    ) -> ListScopeSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_scopes"]
    ) -> ListScopesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_template_snapshots"]
    ) -> ListTemplateSnapshotsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_templates"]
    ) -> ListTemplatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager.html#NetworkSecurityManagerCustomerAPI.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/network-security-manager.html#NetworkSecurityManagerCustomerAPI.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_network_security_manager/client/)
        """
