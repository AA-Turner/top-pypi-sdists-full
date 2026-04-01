"""
Type annotations for securityagent service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_securityagent.client import SecurityAgentClient

    session = Session()
    client: SecurityAgentClient = session.client("securityagent")
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
    ListAgentSpacesPaginator,
    ListApplicationsPaginator,
    ListArtifactsPaginator,
    ListDiscoveredEndpointsPaginator,
    ListFindingsPaginator,
    ListIntegratedResourcesPaginator,
    ListIntegrationsPaginator,
    ListMembershipsPaginator,
    ListPentestJobsForPentestPaginator,
    ListPentestJobTasksPaginator,
    ListPentestsPaginator,
    ListTargetDomainsPaginator,
)
from .type_defs import (
    AddArtifactInputTypeDef,
    AddArtifactOutputTypeDef,
    BatchDeletePentestsInputTypeDef,
    BatchDeletePentestsOutputTypeDef,
    BatchGetAgentSpacesInputTypeDef,
    BatchGetAgentSpacesOutputTypeDef,
    BatchGetArtifactMetadataInputTypeDef,
    BatchGetArtifactMetadataOutputTypeDef,
    BatchGetFindingsInputTypeDef,
    BatchGetFindingsOutputTypeDef,
    BatchGetPentestJobsInputTypeDef,
    BatchGetPentestJobsOutputTypeDef,
    BatchGetPentestJobTasksInputTypeDef,
    BatchGetPentestJobTasksOutputTypeDef,
    BatchGetPentestsInputTypeDef,
    BatchGetPentestsOutputTypeDef,
    BatchGetTargetDomainsInputTypeDef,
    BatchGetTargetDomainsOutputTypeDef,
    CreateAgentSpaceInputTypeDef,
    CreateAgentSpaceOutputTypeDef,
    CreateApplicationRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateIntegrationInputTypeDef,
    CreateIntegrationOutputTypeDef,
    CreateMembershipRequestTypeDef,
    CreatePentestInputTypeDef,
    CreatePentestOutputTypeDef,
    CreateTargetDomainInputTypeDef,
    CreateTargetDomainOutputTypeDef,
    DeleteAgentSpaceInputTypeDef,
    DeleteAgentSpaceOutputTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteArtifactInputTypeDef,
    DeleteIntegrationInputTypeDef,
    DeleteMembershipRequestTypeDef,
    DeleteTargetDomainInputTypeDef,
    DeleteTargetDomainOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetApplicationRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetArtifactInputTypeDef,
    GetArtifactOutputTypeDef,
    GetIntegrationInputTypeDef,
    GetIntegrationOutputTypeDef,
    InitiateProviderRegistrationInputTypeDef,
    InitiateProviderRegistrationOutputTypeDef,
    ListAgentSpacesInputTypeDef,
    ListAgentSpacesOutputTypeDef,
    ListApplicationsRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListArtifactsInputTypeDef,
    ListArtifactsOutputTypeDef,
    ListDiscoveredEndpointsInputTypeDef,
    ListDiscoveredEndpointsOutputTypeDef,
    ListFindingsInputTypeDef,
    ListFindingsOutputTypeDef,
    ListIntegratedResourcesInputTypeDef,
    ListIntegratedResourcesOutputTypeDef,
    ListIntegrationsInputTypeDef,
    ListIntegrationsOutputTypeDef,
    ListMembershipsRequestTypeDef,
    ListMembershipsResponseTypeDef,
    ListPentestJobsForPentestInputTypeDef,
    ListPentestJobsForPentestOutputTypeDef,
    ListPentestJobTasksInputTypeDef,
    ListPentestJobTasksOutputTypeDef,
    ListPentestsInputTypeDef,
    ListPentestsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTargetDomainsInputTypeDef,
    ListTargetDomainsOutputTypeDef,
    StartCodeRemediationInputTypeDef,
    StartPentestJobInputTypeDef,
    StartPentestJobOutputTypeDef,
    StopPentestJobInputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateAgentSpaceInputTypeDef,
    UpdateAgentSpaceOutputTypeDef,
    UpdateApplicationRequestTypeDef,
    UpdateApplicationResponseTypeDef,
    UpdateFindingInputTypeDef,
    UpdateIntegratedResourcesInputTypeDef,
    UpdatePentestInputTypeDef,
    UpdatePentestOutputTypeDef,
    UpdateTargetDomainInputTypeDef,
    UpdateTargetDomainOutputTypeDef,
    VerifyTargetDomainInputTypeDef,
    VerifyTargetDomainOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("SecurityAgentClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]


class SecurityAgentClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent.html#SecurityAgent.Client)
    [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        SecurityAgentClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent.html#SecurityAgent.Client)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/can_paginate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/generate_presigned_url.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#generate_presigned_url)
        """

    def add_artifact(self, **kwargs: Unpack[AddArtifactInputTypeDef]) -> AddArtifactOutputTypeDef:
        """
        Adds an Artifact for the given agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/add_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#add_artifact)
        """

    def batch_delete_pentests(
        self, **kwargs: Unpack[BatchDeletePentestsInputTypeDef]
    ) -> BatchDeletePentestsOutputTypeDef:
        """
        Deletes multiple pentests in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_delete_pentests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_delete_pentests)
        """

    def batch_get_agent_spaces(
        self, **kwargs: Unpack[BatchGetAgentSpacesInputTypeDef]
    ) -> BatchGetAgentSpacesOutputTypeDef:
        """
        Retrieves multiple agent spaces in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_agent_spaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_agent_spaces)
        """

    def batch_get_artifact_metadata(
        self, **kwargs: Unpack[BatchGetArtifactMetadataInputTypeDef]
    ) -> BatchGetArtifactMetadataOutputTypeDef:
        """
        Retrieve the list of artifact metadata for the given agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_artifact_metadata.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_artifact_metadata)
        """

    def batch_get_findings(
        self, **kwargs: Unpack[BatchGetFindingsInputTypeDef]
    ) -> BatchGetFindingsOutputTypeDef:
        """
        Retrieves multiple findings in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_findings)
        """

    def batch_get_pentest_job_tasks(
        self, **kwargs: Unpack[BatchGetPentestJobTasksInputTypeDef]
    ) -> BatchGetPentestJobTasksOutputTypeDef:
        """
        Retrieves multiple tasks for a pentest job in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_pentest_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_pentest_job_tasks)
        """

    def batch_get_pentest_jobs(
        self, **kwargs: Unpack[BatchGetPentestJobsInputTypeDef]
    ) -> BatchGetPentestJobsOutputTypeDef:
        """
        Retrieves multiple pentest jobs in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_pentest_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_pentest_jobs)
        """

    def batch_get_pentests(
        self, **kwargs: Unpack[BatchGetPentestsInputTypeDef]
    ) -> BatchGetPentestsOutputTypeDef:
        """
        Retrieves multiple pentests in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_pentests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_pentests)
        """

    def batch_get_target_domains(
        self, **kwargs: Unpack[BatchGetTargetDomainsInputTypeDef]
    ) -> BatchGetTargetDomainsOutputTypeDef:
        """
        Retrieves multiple target domains in a single request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_target_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_target_domains)
        """

    def create_agent_space(
        self, **kwargs: Unpack[CreateAgentSpaceInputTypeDef]
    ) -> CreateAgentSpaceOutputTypeDef:
        """
        Creates an agent space record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_agent_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_agent_space)
        """

    def create_application(
        self, **kwargs: Unpack[CreateApplicationRequestTypeDef]
    ) -> CreateApplicationResponseTypeDef:
        """
        Creates a new application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_application)
        """

    def create_integration(
        self, **kwargs: Unpack[CreateIntegrationInputTypeDef]
    ) -> CreateIntegrationOutputTypeDef:
        """
        Creates the Integration of the Security Agent App with an external Provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_integration)
        """

    def create_membership(self, **kwargs: Unpack[CreateMembershipRequestTypeDef]) -> dict[str, Any]:
        """
        Adds a single member to an agent space with specified role.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_membership)
        """

    def create_pentest(
        self, **kwargs: Unpack[CreatePentestInputTypeDef]
    ) -> CreatePentestOutputTypeDef:
        """
        Creates a new pentest configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_pentest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_pentest)
        """

    def create_target_domain(
        self, **kwargs: Unpack[CreateTargetDomainInputTypeDef]
    ) -> CreateTargetDomainOutputTypeDef:
        """
        Creates a target domain record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_target_domain)
        """

    def delete_agent_space(
        self, **kwargs: Unpack[DeleteAgentSpaceInputTypeDef]
    ) -> DeleteAgentSpaceOutputTypeDef:
        """
        Deletes an agent space record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_agent_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_agent_space)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_application)
        """

    def delete_artifact(self, **kwargs: Unpack[DeleteArtifactInputTypeDef]) -> dict[str, Any]:
        """
        Delete an Artifact from the given agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_artifact)
        """

    def delete_integration(self, **kwargs: Unpack[DeleteIntegrationInputTypeDef]) -> dict[str, Any]:
        """
        Deletes the Integration of the Security Agent App with an external Provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_integration)
        """

    def delete_membership(self, **kwargs: Unpack[DeleteMembershipRequestTypeDef]) -> dict[str, Any]:
        """
        Removes a single member associated to an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_membership)
        """

    def delete_target_domain(
        self, **kwargs: Unpack[DeleteTargetDomainInputTypeDef]
    ) -> DeleteTargetDomainOutputTypeDef:
        """
        Deletes a target domain record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_target_domain)
        """

    def get_application(
        self, **kwargs: Unpack[GetApplicationRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Retrieves application details by application ID.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_application)
        """

    def get_artifact(self, **kwargs: Unpack[GetArtifactInputTypeDef]) -> GetArtifactOutputTypeDef:
        """
        Retrieve an Artifact for the given agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_artifact)
        """

    def get_integration(
        self, **kwargs: Unpack[GetIntegrationInputTypeDef]
    ) -> GetIntegrationOutputTypeDef:
        """
        Gets Integration metadata from the provided id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_integration)
        """

    def initiate_provider_registration(
        self, **kwargs: Unpack[InitiateProviderRegistrationInputTypeDef]
    ) -> InitiateProviderRegistrationOutputTypeDef:
        """
        Initiates the registration of Security Agent App for an external Provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/initiate_provider_registration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#initiate_provider_registration)
        """

    def list_agent_spaces(
        self, **kwargs: Unpack[ListAgentSpacesInputTypeDef]
    ) -> ListAgentSpacesOutputTypeDef:
        """
        Lists agent spaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_agent_spaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_agent_spaces)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Lists all applications in the account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_applications)
        """

    def list_artifacts(
        self, **kwargs: Unpack[ListArtifactsInputTypeDef]
    ) -> ListArtifactsOutputTypeDef:
        """
        Lists the artifacts for the associated agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_artifacts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_artifacts)
        """

    def list_discovered_endpoints(
        self, **kwargs: Unpack[ListDiscoveredEndpointsInputTypeDef]
    ) -> ListDiscoveredEndpointsOutputTypeDef:
        """
        Lists discovered endpoints associated with a pentest job with optional URI
        prefix filtering.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_discovered_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_discovered_endpoints)
        """

    def list_findings(
        self, **kwargs: Unpack[ListFindingsInputTypeDef]
    ) -> ListFindingsOutputTypeDef:
        """
        Lists findings with filtering and pagination support.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_findings)
        """

    def list_integrated_resources(
        self, **kwargs: Unpack[ListIntegratedResourcesInputTypeDef]
    ) -> ListIntegratedResourcesOutputTypeDef:
        """
        Lists the integrated resources for an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_integrated_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_integrated_resources)
        """

    def list_integrations(
        self, **kwargs: Unpack[ListIntegrationsInputTypeDef]
    ) -> ListIntegrationsOutputTypeDef:
        """
        Retrieves the Integrations associated with the user's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_integrations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_integrations)
        """

    def list_memberships(
        self, **kwargs: Unpack[ListMembershipsRequestTypeDef]
    ) -> ListMembershipsResponseTypeDef:
        """
        Lists all members associated to an agent space with pagination support.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_memberships.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_memberships)
        """

    def list_pentest_job_tasks(
        self, **kwargs: Unpack[ListPentestJobTasksInputTypeDef]
    ) -> ListPentestJobTasksOutputTypeDef:
        """
        Lists tasks associated with a specific pentest job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_pentest_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_pentest_job_tasks)
        """

    def list_pentest_jobs_for_pentest(
        self, **kwargs: Unpack[ListPentestJobsForPentestInputTypeDef]
    ) -> ListPentestJobsForPentestOutputTypeDef:
        """
        Lists pentest jobs associated with a pentest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_pentest_jobs_for_pentest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_pentest_jobs_for_pentest)
        """

    def list_pentests(
        self, **kwargs: Unpack[ListPentestsInputTypeDef]
    ) -> ListPentestsOutputTypeDef:
        """
        Lists pentests with optional filtering by status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_pentests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_pentests)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists tags for a Security Agent resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_tags_for_resource)
        """

    def list_target_domains(
        self, **kwargs: Unpack[ListTargetDomainsInputTypeDef]
    ) -> ListTargetDomainsOutputTypeDef:
        """
        Lists target domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_target_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_target_domains)
        """

    def start_code_remediation(
        self, **kwargs: Unpack[StartCodeRemediationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Starts code remediation for the specified findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/start_code_remediation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#start_code_remediation)
        """

    def start_pentest_job(
        self, **kwargs: Unpack[StartPentestJobInputTypeDef]
    ) -> StartPentestJobOutputTypeDef:
        """
        Initiates the execution of a pentest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/start_pentest_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#start_pentest_job)
        """

    def stop_pentest_job(self, **kwargs: Unpack[StopPentestJobInputTypeDef]) -> dict[str, Any]:
        """
        Stops the execution of a running pentest.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/stop_pentest_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#stop_pentest_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds tags to a Security Agent resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes tags from a Security Agent resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#untag_resource)
        """

    def update_agent_space(
        self, **kwargs: Unpack[UpdateAgentSpaceInputTypeDef]
    ) -> UpdateAgentSpaceOutputTypeDef:
        """
        Updates an agent space record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_agent_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_agent_space)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestTypeDef]
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates application configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_application)
        """

    def update_finding(self, **kwargs: Unpack[UpdateFindingInputTypeDef]) -> dict[str, Any]:
        """
        Updates an existing security finding with new details or status.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_finding.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_finding)
        """

    def update_integrated_resources(
        self, **kwargs: Unpack[UpdateIntegratedResourcesInputTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the integrated resources for an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_integrated_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_integrated_resources)
        """

    def update_pentest(
        self, **kwargs: Unpack[UpdatePentestInputTypeDef]
    ) -> UpdatePentestOutputTypeDef:
        """
        Updates an existing pentest with new configuration or settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_pentest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_pentest)
        """

    def update_target_domain(
        self, **kwargs: Unpack[UpdateTargetDomainInputTypeDef]
    ) -> UpdateTargetDomainOutputTypeDef:
        """
        Updates a target domain record.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_target_domain)
        """

    def verify_target_domain(
        self, **kwargs: Unpack[VerifyTargetDomainInputTypeDef]
    ) -> VerifyTargetDomainOutputTypeDef:
        """
        Verifies ownership for a registered target domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/verify_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#verify_target_domain)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_agent_spaces"]
    ) -> ListAgentSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_applications"]
    ) -> ListApplicationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_artifacts"]
    ) -> ListArtifactsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_discovered_endpoints"]
    ) -> ListDiscoveredEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_findings"]
    ) -> ListFindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_integrated_resources"]
    ) -> ListIntegratedResourcesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_integrations"]
    ) -> ListIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_memberships"]
    ) -> ListMembershipsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pentest_job_tasks"]
    ) -> ListPentestJobTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pentest_jobs_for_pentest"]
    ) -> ListPentestJobsForPentestPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_pentests"]
    ) -> ListPentestsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_target_domains"]
    ) -> ListTargetDomainsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """
