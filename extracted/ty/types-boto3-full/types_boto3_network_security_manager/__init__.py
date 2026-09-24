"""
Main interface for network-security-manager service.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_network_security_manager/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_network_security_manager import (
        Client,
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
        NetworkSecurityManagerCustomerAPIClient,
    )

    session = Session()
    client: NetworkSecurityManagerCustomerAPIClient = session.client("network-security-manager")

    list_admin_accounts_paginator: ListAdminAccountsPaginator = client.get_paginator("list_admin_accounts")
    list_aggregate_resource_synchronization_statuses_paginator: ListAggregateResourceSynchronizationStatusesPaginator = client.get_paginator("list_aggregate_resource_synchronization_statuses")
    list_deployment_snapshots_paginator: ListDeploymentSnapshotsPaginator = client.get_paginator("list_deployment_snapshots")
    list_deployments_paginator: ListDeploymentsPaginator = client.get_paginator("list_deployments")
    list_policies_paginator: ListPoliciesPaginator = client.get_paginator("list_policies")
    list_policy_snapshots_paginator: ListPolicySnapshotsPaginator = client.get_paginator("list_policy_snapshots")
    list_resource_associations_paginator: ListResourceAssociationsPaginator = client.get_paginator("list_resource_associations")
    list_resource_synchronization_statuses_paginator: ListResourceSynchronizationStatusesPaginator = client.get_paginator("list_resource_synchronization_statuses")
    list_rule_snapshots_paginator: ListRuleSnapshotsPaginator = client.get_paginator("list_rule_snapshots")
    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    list_scope_snapshots_paginator: ListScopeSnapshotsPaginator = client.get_paginator("list_scope_snapshots")
    list_scopes_paginator: ListScopesPaginator = client.get_paginator("list_scopes")
    list_template_snapshots_paginator: ListTemplateSnapshotsPaginator = client.get_paginator("list_template_snapshots")
    list_templates_paginator: ListTemplatesPaginator = client.get_paginator("list_templates")
    ```
"""

from .client import NetworkSecurityManagerCustomerAPIClient
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

Client = NetworkSecurityManagerCustomerAPIClient


__all__ = (
    "Client",
    "ListAdminAccountsPaginator",
    "ListAggregateResourceSynchronizationStatusesPaginator",
    "ListDeploymentSnapshotsPaginator",
    "ListDeploymentsPaginator",
    "ListPoliciesPaginator",
    "ListPolicySnapshotsPaginator",
    "ListResourceAssociationsPaginator",
    "ListResourceSynchronizationStatusesPaginator",
    "ListRuleSnapshotsPaginator",
    "ListRulesPaginator",
    "ListScopeSnapshotsPaginator",
    "ListScopesPaginator",
    "ListTemplateSnapshotsPaginator",
    "ListTemplatesPaginator",
    "NetworkSecurityManagerCustomerAPIClient",
)
