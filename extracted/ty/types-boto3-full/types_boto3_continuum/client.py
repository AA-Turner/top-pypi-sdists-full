"""
Type annotations for continuum service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_continuum.client import ContinuumClient

    session = Session()
    client: ContinuumClient = session.client("continuum")
    ```
"""

from __future__ import annotations

import sys
from collections.abc import Mapping
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

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
from .type_defs import (
    AssociateCollectorInputTypeDef,
    AssociateCollectorOutputTypeDef,
    CreateCodeFindingInputTypeDef,
    CreateCodeFindingOutputTypeDef,
    CreateCodeScanInputTypeDef,
    CreateCodeScanOutputTypeDef,
    CreateCollectorInputTypeDef,
    CreateCollectorOutputTypeDef,
    CreateEnvironmentInputTypeDef,
    CreateEnvironmentOutputTypeDef,
    CreateIntegrationInputTypeDef,
    CreateIntegrationOutputTypeDef,
    DeleteCollectorInputTypeDef,
    DeleteEnvironmentInputTypeDef,
    DeleteIntegrationInputTypeDef,
    DisassociateCollectorInputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCodeFindingInputTypeDef,
    GetCodeFindingOutputTypeDef,
    GetCodeIssueArtifactInputTypeDef,
    GetCodeIssueArtifactOutputTypeDef,
    GetCodeIssueInputTypeDef,
    GetCodeIssueOutputTypeDef,
    GetCodeScanInputTypeDef,
    GetCodeScanOutputTypeDef,
    GetCollectorDataAccessAuthorizationInputTypeDef,
    GetCollectorInputTypeDef,
    GetCollectorOutputTypeDef,
    GetEnvironmentInputTypeDef,
    GetEnvironmentOutputTypeDef,
    GetIntegrationInputTypeDef,
    GetIntegrationOutputTypeDef,
    GetResourcePolicyInputTypeDef,
    GetResourcePolicyOutputTypeDef,
    ListAssociatedCollectorsInputTypeDef,
    ListAssociatedCollectorsOutputTypeDef,
    ListAssociatedEnvironmentsInputTypeDef,
    ListAssociatedEnvironmentsOutputTypeDef,
    ListCodeFindingsInputTypeDef,
    ListCodeFindingsOutputTypeDef,
    ListCodeIssueArtifactsInputTypeDef,
    ListCodeIssueArtifactsOutputTypeDef,
    ListCodeIssuesInputTypeDef,
    ListCodeIssuesOutputTypeDef,
    ListCodeScansInputTypeDef,
    ListCodeScansOutputTypeDef,
    ListCollectorsOutputTypeDef,
    ListEnvironmentsInputTypeDef,
    ListEnvironmentsOutputTypeDef,
    ListIntegrationsInputTypeDef,
    ListIntegrationsOutputTypeDef,
    PutResourcePolicyInputTypeDef,
    PutResourcePolicyOutputTypeDef,
    StartIntegrationAuthorizationInputTypeDef,
    StartIntegrationAuthorizationOutputTypeDef,
    UpdateCollectorInputTypeDef,
    UpdateCollectorOutputTypeDef,
    UpdateEnvironmentInputTypeDef,
    UpdateEnvironmentOutputTypeDef,
    UpdateIntegrationInputTypeDef,
    UpdateIntegrationOutputTypeDef,
)
from .waiter import CodeScanSucceededWaiter

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("ContinuumClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class ContinuumClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum.html#Continuum.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ContinuumClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum.html#Continuum.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#generate_presigned_url)
        """

    def associate_collector(
        self, **kwargs: Unpack[AssociateCollectorInputTypeDef]
    ) -> AssociateCollectorOutputTypeDef:
        """
        Associates one Collector with this Environment and configures the customer role
        Continuum uses to authorize access to associated Collector data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/associate_collector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#associate_collector)
        """

    def create_code_finding(
        self, **kwargs: Unpack[CreateCodeFindingInputTypeDef]
    ) -> CreateCodeFindingOutputTypeDef:
        """
        Ingests a customer-supplied security finding into an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/create_code_finding.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#create_code_finding)
        """

    def create_code_scan(
        self, **kwargs: Unpack[CreateCodeScanInputTypeDef]
    ) -> CreateCodeScanOutputTypeDef:
        """
        Creates an explicit scan request for one environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/create_code_scan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#create_code_scan)
        """

    def create_collector(
        self, **kwargs: Unpack[CreateCollectorInputTypeDef]
    ) -> CreateCollectorOutputTypeDef:
        """
        Creates the Collector for the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/create_collector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#create_collector)
        """

    def create_environment(
        self, **kwargs: Unpack[CreateEnvironmentInputTypeDef]
    ) -> CreateEnvironmentOutputTypeDef:
        """
        Creates an environment and starts its validation and any requested provisioning.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/create_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#create_environment)
        """

    def create_integration(
        self, **kwargs: Unpack[CreateIntegrationInputTypeDef]
    ) -> CreateIntegrationOutputTypeDef:
        """
        Creates a new integration with an external source provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/create_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#create_integration)
        """

    def delete_collector(
        self, **kwargs: Unpack[DeleteCollectorInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the Collector for the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/delete_collector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#delete_collector)
        """

    def delete_environment(
        self, **kwargs: Unpack[DeleteEnvironmentInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an environment and its associated resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/delete_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#delete_environment)
        """

    def delete_integration(
        self, **kwargs: Unpack[DeleteIntegrationInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an integration and releases its name and account quota.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/delete_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#delete_integration)
        """

    def disassociate_collector(
        self, **kwargs: Unpack[DisassociateCollectorInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one Collector association from this Environment, preserving its other
        associations.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/disassociate_collector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#disassociate_collector)
        """

    def get_code_finding(
        self, **kwargs: Unpack[GetCodeFindingInputTypeDef]
    ) -> GetCodeFindingOutputTypeDef:
        """
        Retrieves the current state and details of a finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_code_finding.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_code_finding)
        """

    def get_code_issue(
        self, **kwargs: Unpack[GetCodeIssueInputTypeDef]
    ) -> GetCodeIssueOutputTypeDef:
        """
        Retrieves the current state and details of an issue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_code_issue.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_code_issue)
        """

    def get_code_issue_artifact(
        self, **kwargs: Unpack[GetCodeIssueArtifactInputTypeDef]
    ) -> GetCodeIssueArtifactOutputTypeDef:
        """
        Retrieves one immutable artifact attached to an issue, including its content.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_code_issue_artifact.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_code_issue_artifact)
        """

    def get_code_scan(self, **kwargs: Unpack[GetCodeScanInputTypeDef]) -> GetCodeScanOutputTypeDef:
        """
        Retrieves one customer-visible environment scan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_code_scan.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_code_scan)
        """

    def get_collector(
        self, **kwargs: Unpack[GetCollectorInputTypeDef]
    ) -> GetCollectorOutputTypeDef:
        """
        Retrieves the current state of the Collector for the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_collector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_collector)
        """

    def get_collector_data_access_authorization(
        self, **kwargs: Unpack[GetCollectorDataAccessAuthorizationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Authorizes an Environment's access to a Collector's data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_collector_data_access_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_collector_data_access_authorization)
        """

    def get_environment(
        self, **kwargs: Unpack[GetEnvironmentInputTypeDef]
    ) -> GetEnvironmentOutputTypeDef:
        """
        Retrieves the current state and configuration of an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_environment)
        """

    def get_integration(
        self, **kwargs: Unpack[GetIntegrationInputTypeDef]
    ) -> GetIntegrationOutputTypeDef:
        """
        Retrieves information about an integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_integration)
        """

    def get_resource_policy(
        self, **kwargs: Unpack[GetResourcePolicyInputTypeDef]
    ) -> GetResourcePolicyOutputTypeDef:
        """
        Retrieves the resource policy attached to a Continuum resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_resource_policy)
        """

    def list_associated_collectors(
        self, **kwargs: Unpack[ListAssociatedCollectorsInputTypeDef]
    ) -> ListAssociatedCollectorsOutputTypeDef:
        """
        Lists the Collectors currently associated with one Environment in ascending
        collectorId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_associated_collectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_associated_collectors)
        """

    def list_associated_environments(
        self, **kwargs: Unpack[ListAssociatedEnvironmentsInputTypeDef]
    ) -> ListAssociatedEnvironmentsOutputTypeDef:
        """
        Lists the Environments currently associated with one Collector in
        lexicographically ascending environmentArn order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_associated_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_associated_environments)
        """

    def list_code_findings(
        self, **kwargs: Unpack[ListCodeFindingsInputTypeDef]
    ) -> ListCodeFindingsOutputTypeDef:
        """
        Lists the findings in an environment in descending findingId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_code_findings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_code_findings)
        """

    def list_code_issue_artifacts(
        self, **kwargs: Unpack[ListCodeIssueArtifactsInputTypeDef]
    ) -> ListCodeIssueArtifactsOutputTypeDef:
        """
        Lists the artifacts attached to an issue in descending artifactId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_code_issue_artifacts.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_code_issue_artifacts)
        """

    def list_code_issues(
        self, **kwargs: Unpack[ListCodeIssuesInputTypeDef]
    ) -> ListCodeIssuesOutputTypeDef:
        """
        Lists the issues in an environment in descending issueId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_code_issues.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_code_issues)
        """

    def list_code_scans(
        self, **kwargs: Unpack[ListCodeScansInputTypeDef]
    ) -> ListCodeScansOutputTypeDef:
        """
        Lists customer-visible scans for one environment in descending scanRunId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_code_scans.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_code_scans)
        """

    def list_collectors(self) -> ListCollectorsOutputTypeDef:
        """
        Lists the Collectors owned by the authenticated caller's account, including a
        Collector whose deletion is in progress.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_collectors.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_collectors)
        """

    def list_environments(
        self, **kwargs: Unpack[ListEnvironmentsInputTypeDef]
    ) -> ListEnvironmentsOutputTypeDef:
        """
        Lists all environments in your account in descending environmentId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_environments.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_environments)
        """

    def list_integrations(
        self, **kwargs: Unpack[ListIntegrationsInputTypeDef]
    ) -> ListIntegrationsOutputTypeDef:
        """
        Lists the integrations in your account in descending integrationId order.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/list_integrations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#list_integrations)
        """

    def put_resource_policy(
        self, **kwargs: Unpack[PutResourcePolicyInputTypeDef]
    ) -> PutResourcePolicyOutputTypeDef:
        """
        Creates or replaces the resource policy attached to a Continuum resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/put_resource_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#put_resource_policy)
        """

    def start_integration_authorization(
        self, **kwargs: Unpack[StartIntegrationAuthorizationInputTypeDef]
    ) -> StartIntegrationAuthorizationOutputTypeDef:
        """
        Starts an OAuth authorization for a new integration and returns the values the
        caller sends to the provider's authorization endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/start_integration_authorization.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#start_integration_authorization)
        """

    def update_collector(
        self, **kwargs: Unpack[UpdateCollectorInputTypeDef]
    ) -> UpdateCollectorOutputTypeDef:
        """
        Updates the customer-controlled mutable properties of a Collector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/update_collector.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#update_collector)
        """

    def update_environment(
        self, **kwargs: Unpack[UpdateEnvironmentInputTypeDef]
    ) -> UpdateEnvironmentOutputTypeDef:
        """
        Updates the customer-controlled mutable properties of an environment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/update_environment.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#update_environment)
        """

    def update_integration(
        self, **kwargs: Unpack[UpdateIntegrationInputTypeDef]
    ) -> UpdateIntegrationOutputTypeDef:
        """
        Rotates the credentials used by an Amazon S3 integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/update_integration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#update_integration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associated_collectors"]
    ) -> ListAssociatedCollectorsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_associated_environments"]
    ) -> ListAssociatedEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_findings"]
    ) -> ListCodeFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_issue_artifacts"]
    ) -> ListCodeIssueArtifactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_issues"]
    ) -> ListCodeIssuesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_scans"]
    ) -> ListCodeScansPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_environments"]
    ) -> ListEnvironmentsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_integrations"]
    ) -> ListIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["code_scan_succeeded"]
    ) -> CodeScanSucceededWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/continuum/client/get_waiter.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_continuum/client/#get_waiter)
        """
