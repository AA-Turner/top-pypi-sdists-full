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
    ListCodeReviewJobsForCodeReviewPaginator,
    ListCodeReviewJobTasksPaginator,
    ListCodeReviewsPaginator,
    ListDiscoveredEndpointsPaginator,
    ListFindingsPaginator,
    ListIntegratedResourcesPaginator,
    ListIntegrationsPaginator,
    ListMembershipsPaginator,
    ListPentestJobsForPentestPaginator,
    ListPentestJobTasksPaginator,
    ListPentestsPaginator,
    ListPrivateConnectionsPaginator,
    ListSecurityRequirementPacksPaginator,
    ListSecurityRequirementsPaginator,
    ListTargetDomainsPaginator,
    ListThreatModelJobsPaginator,
    ListThreatModelJobTasksPaginator,
    ListThreatModelsPaginator,
    ListThreatsPaginator,
)
from .type_defs import (
    AddArtifactInputTypeDef,
    AddArtifactOutputTypeDef,
    BatchCreateSecurityRequirementsInputTypeDef,
    BatchCreateSecurityRequirementsOutputTypeDef,
    BatchDeleteCodeReviewsInputTypeDef,
    BatchDeleteCodeReviewsOutputTypeDef,
    BatchDeletePentestsInputTypeDef,
    BatchDeletePentestsOutputTypeDef,
    BatchDeleteSecurityRequirementsInputTypeDef,
    BatchDeleteSecurityRequirementsOutputTypeDef,
    BatchDeleteThreatModelsInputTypeDef,
    BatchDeleteThreatModelsOutputTypeDef,
    BatchGetAgentSpacesInputTypeDef,
    BatchGetAgentSpacesOutputTypeDef,
    BatchGetArtifactMetadataInputTypeDef,
    BatchGetArtifactMetadataOutputTypeDef,
    BatchGetCodeReviewJobsInputTypeDef,
    BatchGetCodeReviewJobsOutputTypeDef,
    BatchGetCodeReviewJobTasksInputTypeDef,
    BatchGetCodeReviewJobTasksOutputTypeDef,
    BatchGetCodeReviewsInputTypeDef,
    BatchGetCodeReviewsOutputTypeDef,
    BatchGetFindingsInputTypeDef,
    BatchGetFindingsOutputTypeDef,
    BatchGetPentestJobsInputTypeDef,
    BatchGetPentestJobsOutputTypeDef,
    BatchGetPentestJobTasksInputTypeDef,
    BatchGetPentestJobTasksOutputTypeDef,
    BatchGetPentestsInputTypeDef,
    BatchGetPentestsOutputTypeDef,
    BatchGetSecurityRequirementsInputTypeDef,
    BatchGetSecurityRequirementsOutputTypeDef,
    BatchGetTargetDomainsInputTypeDef,
    BatchGetTargetDomainsOutputTypeDef,
    BatchGetThreatModelJobsInputTypeDef,
    BatchGetThreatModelJobsOutputTypeDef,
    BatchGetThreatModelJobTasksInputTypeDef,
    BatchGetThreatModelJobTasksOutputTypeDef,
    BatchGetThreatModelsInputTypeDef,
    BatchGetThreatModelsOutputTypeDef,
    BatchGetThreatsInputTypeDef,
    BatchGetThreatsOutputTypeDef,
    BatchUpdateSecurityRequirementsInputTypeDef,
    BatchUpdateSecurityRequirementsOutputTypeDef,
    CreateAgentSpaceInputTypeDef,
    CreateAgentSpaceOutputTypeDef,
    CreateApplicationRequestTypeDef,
    CreateApplicationResponseTypeDef,
    CreateCodeReviewInputTypeDef,
    CreateCodeReviewOutputTypeDef,
    CreateIntegrationInputTypeDef,
    CreateIntegrationOutputTypeDef,
    CreateMembershipRequestTypeDef,
    CreatePentestInputTypeDef,
    CreatePentestOutputTypeDef,
    CreatePrivateConnectionInputTypeDef,
    CreatePrivateConnectionOutputTypeDef,
    CreateSecurityRequirementPackInputTypeDef,
    CreateSecurityRequirementPackOutputTypeDef,
    CreateTargetDomainInputTypeDef,
    CreateTargetDomainOutputTypeDef,
    CreateThreatInputTypeDef,
    CreateThreatModelInputTypeDef,
    CreateThreatModelOutputTypeDef,
    CreateThreatOutputTypeDef,
    DeleteAgentSpaceInputTypeDef,
    DeleteAgentSpaceOutputTypeDef,
    DeleteApplicationRequestTypeDef,
    DeleteArtifactInputTypeDef,
    DeleteIntegrationInputTypeDef,
    DeleteMembershipRequestTypeDef,
    DeletePrivateConnectionInputTypeDef,
    DeletePrivateConnectionOutputTypeDef,
    DeleteSecurityRequirementPackInputTypeDef,
    DeleteTargetDomainInputTypeDef,
    DeleteTargetDomainOutputTypeDef,
    DescribePrivateConnectionInputTypeDef,
    DescribePrivateConnectionOutputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetApplicationRequestTypeDef,
    GetApplicationResponseTypeDef,
    GetArtifactInputTypeDef,
    GetArtifactOutputTypeDef,
    GetIntegrationInputTypeDef,
    GetIntegrationOutputTypeDef,
    GetSecurityRequirementPackInputTypeDef,
    GetSecurityRequirementPackOutputTypeDef,
    ImportSecurityRequirementsInputTypeDef,
    ImportSecurityRequirementsOutputTypeDef,
    InitiateProviderRegistrationInputTypeDef,
    InitiateProviderRegistrationOutputTypeDef,
    ListAgentSpacesInputTypeDef,
    ListAgentSpacesOutputTypeDef,
    ListApplicationsRequestTypeDef,
    ListApplicationsResponseTypeDef,
    ListArtifactsInputTypeDef,
    ListArtifactsOutputTypeDef,
    ListCodeReviewJobsForCodeReviewInputTypeDef,
    ListCodeReviewJobsForCodeReviewOutputTypeDef,
    ListCodeReviewJobTasksInputTypeDef,
    ListCodeReviewJobTasksOutputTypeDef,
    ListCodeReviewsInputTypeDef,
    ListCodeReviewsOutputTypeDef,
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
    ListPrivateConnectionsInputTypeDef,
    ListPrivateConnectionsOutputTypeDef,
    ListSecurityRequirementPacksInputTypeDef,
    ListSecurityRequirementPacksOutputTypeDef,
    ListSecurityRequirementsInputTypeDef,
    ListSecurityRequirementsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTargetDomainsInputTypeDef,
    ListTargetDomainsOutputTypeDef,
    ListThreatModelJobsInputTypeDef,
    ListThreatModelJobsOutputTypeDef,
    ListThreatModelJobTasksInputTypeDef,
    ListThreatModelJobTasksOutputTypeDef,
    ListThreatModelsInputTypeDef,
    ListThreatModelsOutputTypeDef,
    ListThreatsInputTypeDef,
    ListThreatsOutputTypeDef,
    StartCodeRemediationInputTypeDef,
    StartCodeReviewJobInputTypeDef,
    StartCodeReviewJobOutputTypeDef,
    StartPentestJobInputTypeDef,
    StartPentestJobOutputTypeDef,
    StartThreatModelJobInputTypeDef,
    StartThreatModelJobOutputTypeDef,
    StopCodeReviewJobInputTypeDef,
    StopPentestJobInputTypeDef,
    StopThreatModelJobInputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateAgentSpaceInputTypeDef,
    UpdateAgentSpaceOutputTypeDef,
    UpdateApplicationRequestTypeDef,
    UpdateApplicationResponseTypeDef,
    UpdateCodeReviewInputTypeDef,
    UpdateCodeReviewOutputTypeDef,
    UpdateFindingInputTypeDef,
    UpdateIntegratedResourcesInputTypeDef,
    UpdatePentestInputTypeDef,
    UpdatePentestOutputTypeDef,
    UpdatePrivateConnectionCertificateInputTypeDef,
    UpdatePrivateConnectionCertificateOutputTypeDef,
    UpdateSecurityRequirementPackInputTypeDef,
    UpdateSecurityRequirementPackOutputTypeDef,
    UpdateTargetDomainInputTypeDef,
    UpdateTargetDomainOutputTypeDef,
    UpdateThreatInputTypeDef,
    UpdateThreatModelInputTypeDef,
    UpdateThreatModelOutputTypeDef,
    UpdateThreatOutputTypeDef,
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
    ServiceQuotaExceededException: type[BotocoreClientError]
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
        Uploads an artifact to an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/add_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#add_artifact)
        """

    def batch_create_security_requirements(
        self, **kwargs: Unpack[BatchCreateSecurityRequirementsInputTypeDef]
    ) -> BatchCreateSecurityRequirementsOutputTypeDef:
        """
        Batch creates security requirements in a customer managed pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_create_security_requirements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_create_security_requirements)
        """

    def batch_delete_code_reviews(
        self, **kwargs: Unpack[BatchDeleteCodeReviewsInputTypeDef]
    ) -> BatchDeleteCodeReviewsOutputTypeDef:
        """
        Deletes one or more code reviews from an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_delete_code_reviews.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_delete_code_reviews)
        """

    def batch_delete_pentests(
        self, **kwargs: Unpack[BatchDeletePentestsInputTypeDef]
    ) -> BatchDeletePentestsOutputTypeDef:
        """
        Deletes one or more pentests from an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_delete_pentests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_delete_pentests)
        """

    def batch_delete_security_requirements(
        self, **kwargs: Unpack[BatchDeleteSecurityRequirementsInputTypeDef]
    ) -> BatchDeleteSecurityRequirementsOutputTypeDef:
        """
        Batch deletes security requirements from a customer managed pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_delete_security_requirements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_delete_security_requirements)
        """

    def batch_delete_threat_models(
        self, **kwargs: Unpack[BatchDeleteThreatModelsInputTypeDef]
    ) -> BatchDeleteThreatModelsOutputTypeDef:
        """
        Deletes one or more threat models from an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_delete_threat_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_delete_threat_models)
        """

    def batch_get_agent_spaces(
        self, **kwargs: Unpack[BatchGetAgentSpacesInputTypeDef]
    ) -> BatchGetAgentSpacesOutputTypeDef:
        """
        Retrieves information about one or more agent spaces.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_agent_spaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_agent_spaces)
        """

    def batch_get_artifact_metadata(
        self, **kwargs: Unpack[BatchGetArtifactMetadataInputTypeDef]
    ) -> BatchGetArtifactMetadataOutputTypeDef:
        """
        Retrieves metadata for one or more artifacts in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_artifact_metadata.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_artifact_metadata)
        """

    def batch_get_code_review_job_tasks(
        self, **kwargs: Unpack[BatchGetCodeReviewJobTasksInputTypeDef]
    ) -> BatchGetCodeReviewJobTasksOutputTypeDef:
        """
        Retrieves information about one or more tasks within a code review job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_code_review_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_code_review_job_tasks)
        """

    def batch_get_code_review_jobs(
        self, **kwargs: Unpack[BatchGetCodeReviewJobsInputTypeDef]
    ) -> BatchGetCodeReviewJobsOutputTypeDef:
        """
        Retrieves information about one or more code review jobs in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_code_review_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_code_review_jobs)
        """

    def batch_get_code_reviews(
        self, **kwargs: Unpack[BatchGetCodeReviewsInputTypeDef]
    ) -> BatchGetCodeReviewsOutputTypeDef:
        """
        Retrieves information about one or more code reviews in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_code_reviews.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_code_reviews)
        """

    def batch_get_findings(
        self, **kwargs: Unpack[BatchGetFindingsInputTypeDef]
    ) -> BatchGetFindingsOutputTypeDef:
        """
        Retrieves information about one or more security findings in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_findings)
        """

    def batch_get_pentest_job_tasks(
        self, **kwargs: Unpack[BatchGetPentestJobTasksInputTypeDef]
    ) -> BatchGetPentestJobTasksOutputTypeDef:
        """
        Retrieves information about one or more tasks within a pentest job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_pentest_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_pentest_job_tasks)
        """

    def batch_get_pentest_jobs(
        self, **kwargs: Unpack[BatchGetPentestJobsInputTypeDef]
    ) -> BatchGetPentestJobsOutputTypeDef:
        """
        Retrieves information about one or more pentest jobs in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_pentest_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_pentest_jobs)
        """

    def batch_get_pentests(
        self, **kwargs: Unpack[BatchGetPentestsInputTypeDef]
    ) -> BatchGetPentestsOutputTypeDef:
        """
        Retrieves information about one or more pentests in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_pentests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_pentests)
        """

    def batch_get_security_requirements(
        self, **kwargs: Unpack[BatchGetSecurityRequirementsInputTypeDef]
    ) -> BatchGetSecurityRequirementsOutputTypeDef:
        """
        Batch retrieves security requirements from a pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_security_requirements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_security_requirements)
        """

    def batch_get_target_domains(
        self, **kwargs: Unpack[BatchGetTargetDomainsInputTypeDef]
    ) -> BatchGetTargetDomainsOutputTypeDef:
        """
        Retrieves information about one or more target domains.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_target_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_target_domains)
        """

    def batch_get_threat_model_job_tasks(
        self, **kwargs: Unpack[BatchGetThreatModelJobTasksInputTypeDef]
    ) -> BatchGetThreatModelJobTasksOutputTypeDef:
        """
        Retrieves information about one or more tasks within a threat model job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_threat_model_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_threat_model_job_tasks)
        """

    def batch_get_threat_model_jobs(
        self, **kwargs: Unpack[BatchGetThreatModelJobsInputTypeDef]
    ) -> BatchGetThreatModelJobsOutputTypeDef:
        """
        Retrieves information about one or more threat model jobs in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_threat_model_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_threat_model_jobs)
        """

    def batch_get_threat_models(
        self, **kwargs: Unpack[BatchGetThreatModelsInputTypeDef]
    ) -> BatchGetThreatModelsOutputTypeDef:
        """
        Retrieves information about one or more threat models in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_threat_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_threat_models)
        """

    def batch_get_threats(
        self, **kwargs: Unpack[BatchGetThreatsInputTypeDef]
    ) -> BatchGetThreatsOutputTypeDef:
        """
        Retrieves information about one or more threats.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_get_threats.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_get_threats)
        """

    def batch_update_security_requirements(
        self, **kwargs: Unpack[BatchUpdateSecurityRequirementsInputTypeDef]
    ) -> BatchUpdateSecurityRequirementsOutputTypeDef:
        """
        Batch updates security requirements within a customer managed pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/batch_update_security_requirements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#batch_update_security_requirements)
        """

    def create_agent_space(
        self, **kwargs: Unpack[CreateAgentSpaceInputTypeDef]
    ) -> CreateAgentSpaceOutputTypeDef:
        """
        Creates a new agent space.

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

    def create_code_review(
        self, **kwargs: Unpack[CreateCodeReviewInputTypeDef]
    ) -> CreateCodeReviewOutputTypeDef:
        """
        Creates a new code review configuration in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_code_review.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_code_review)
        """

    def create_integration(
        self, **kwargs: Unpack[CreateIntegrationInputTypeDef]
    ) -> CreateIntegrationOutputTypeDef:
        """
        Creates a new integration with a third-party provider, such as GitHub, for code
        review and remediation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_integration)
        """

    def create_membership(self, **kwargs: Unpack[CreateMembershipRequestTypeDef]) -> dict[str, Any]:
        """
        Creates a new membership, granting a user access to an agent space within an
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_membership)
        """

    def create_pentest(
        self, **kwargs: Unpack[CreatePentestInputTypeDef]
    ) -> CreatePentestOutputTypeDef:
        """
        Creates a new pentest configuration in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_pentest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_pentest)
        """

    def create_private_connection(
        self, **kwargs: Unpack[CreatePrivateConnectionInputTypeDef]
    ) -> CreatePrivateConnectionOutputTypeDef:
        """
        Creates a private connection for reaching a self-hosted provider instance over
        private networking using Amazon VPC Lattice.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_private_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_private_connection)
        """

    def create_security_requirement_pack(
        self, **kwargs: Unpack[CreateSecurityRequirementPackInputTypeDef]
    ) -> CreateSecurityRequirementPackOutputTypeDef:
        """
        Creates a customer managed security requirement pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_security_requirement_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_security_requirement_pack)
        """

    def create_target_domain(
        self, **kwargs: Unpack[CreateTargetDomainInputTypeDef]
    ) -> CreateTargetDomainOutputTypeDef:
        """
        Creates a new target domain for penetration testing.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_target_domain)
        """

    def create_threat(
        self, **kwargs: Unpack[CreateThreatInputTypeDef]
    ) -> CreateThreatOutputTypeDef:
        """
        Creates a new threat under a threat model job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_threat.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_threat)
        """

    def create_threat_model(
        self, **kwargs: Unpack[CreateThreatModelInputTypeDef]
    ) -> CreateThreatModelOutputTypeDef:
        """
        Creates a new threat model configuration in an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/create_threat_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#create_threat_model)
        """

    def delete_agent_space(
        self, **kwargs: Unpack[DeleteAgentSpaceInputTypeDef]
    ) -> DeleteAgentSpaceOutputTypeDef:
        """
        Deletes an agent space and all of its associated resources, including pentests,
        findings, and artifacts.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_agent_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_agent_space)
        """

    def delete_application(
        self, **kwargs: Unpack[DeleteApplicationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an application and its associated configuration, including IAM Identity
        Center settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_application)
        """

    def delete_artifact(self, **kwargs: Unpack[DeleteArtifactInputTypeDef]) -> dict[str, Any]:
        """
        Deletes an artifact from an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_artifact)
        """

    def delete_integration(self, **kwargs: Unpack[DeleteIntegrationInputTypeDef]) -> dict[str, Any]:
        """
        Deletes an integration with a third-party provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_integration)
        """

    def delete_membership(self, **kwargs: Unpack[DeleteMembershipRequestTypeDef]) -> dict[str, Any]:
        """
        Deletes a membership, revoking a user's access to an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_membership.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_membership)
        """

    def delete_private_connection(
        self, **kwargs: Unpack[DeletePrivateConnectionInputTypeDef]
    ) -> DeletePrivateConnectionOutputTypeDef:
        """
        Deletes a private connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_private_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_private_connection)
        """

    def delete_security_requirement_pack(
        self, **kwargs: Unpack[DeleteSecurityRequirementPackInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a customer managed security requirement pack and all its associated
        security requirements.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_security_requirement_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_security_requirement_pack)
        """

    def delete_target_domain(
        self, **kwargs: Unpack[DeleteTargetDomainInputTypeDef]
    ) -> DeleteTargetDomainOutputTypeDef:
        """
        Deletes a target domain registration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/delete_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#delete_target_domain)
        """

    def describe_private_connection(
        self, **kwargs: Unpack[DescribePrivateConnectionInputTypeDef]
    ) -> DescribePrivateConnectionOutputTypeDef:
        """
        Retrieves the details of a private connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/describe_private_connection.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#describe_private_connection)
        """

    def get_application(
        self, **kwargs: Unpack[GetApplicationRequestTypeDef]
    ) -> GetApplicationResponseTypeDef:
        """
        Retrieves information about an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_application)
        """

    def get_artifact(self, **kwargs: Unpack[GetArtifactInputTypeDef]) -> GetArtifactOutputTypeDef:
        """
        Retrieves an artifact from an agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_artifact.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_artifact)
        """

    def get_integration(
        self, **kwargs: Unpack[GetIntegrationInputTypeDef]
    ) -> GetIntegrationOutputTypeDef:
        """
        Retrieves information about an integration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_integration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_integration)
        """

    def get_security_requirement_pack(
        self, **kwargs: Unpack[GetSecurityRequirementPackInputTypeDef]
    ) -> GetSecurityRequirementPackOutputTypeDef:
        """
        Retrieves information about a security requirement pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_security_requirement_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_security_requirement_pack)
        """

    def import_security_requirements(
        self, **kwargs: Unpack[ImportSecurityRequirementsInputTypeDef]
    ) -> ImportSecurityRequirementsOutputTypeDef:
        """
        Imports security requirements from uploaded documents into a customer managed
        security requirement pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/import_security_requirements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#import_security_requirements)
        """

    def initiate_provider_registration(
        self, **kwargs: Unpack[InitiateProviderRegistrationInputTypeDef]
    ) -> InitiateProviderRegistrationOutputTypeDef:
        """
        Initiates the OAuth registration flow with a third-party provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/initiate_provider_registration.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#initiate_provider_registration)
        """

    def list_agent_spaces(
        self, **kwargs: Unpack[ListAgentSpacesInputTypeDef]
    ) -> ListAgentSpacesOutputTypeDef:
        """
        Returns a paginated list of agent space summaries in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_agent_spaces.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_agent_spaces)
        """

    def list_applications(
        self, **kwargs: Unpack[ListApplicationsRequestTypeDef]
    ) -> ListApplicationsResponseTypeDef:
        """
        Returns a paginated list of application summaries in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_applications.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_applications)
        """

    def list_artifacts(
        self, **kwargs: Unpack[ListArtifactsInputTypeDef]
    ) -> ListArtifactsOutputTypeDef:
        """
        Returns a paginated list of artifact summaries for the specified agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_artifacts.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_artifacts)
        """

    def list_code_review_job_tasks(
        self, **kwargs: Unpack[ListCodeReviewJobTasksInputTypeDef]
    ) -> ListCodeReviewJobTasksOutputTypeDef:
        """
        Returns a paginated list of task summaries for the specified code review job,
        optionally filtered by step name or category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_code_review_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_code_review_job_tasks)
        """

    def list_code_review_jobs_for_code_review(
        self, **kwargs: Unpack[ListCodeReviewJobsForCodeReviewInputTypeDef]
    ) -> ListCodeReviewJobsForCodeReviewOutputTypeDef:
        """
        Returns a paginated list of code review job summaries for the specified code
        review configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_code_review_jobs_for_code_review.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_code_review_jobs_for_code_review)
        """

    def list_code_reviews(
        self, **kwargs: Unpack[ListCodeReviewsInputTypeDef]
    ) -> ListCodeReviewsOutputTypeDef:
        """
        Returns a paginated list of code review summaries for the specified agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_code_reviews.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_code_reviews)
        """

    def list_discovered_endpoints(
        self, **kwargs: Unpack[ListDiscoveredEndpointsInputTypeDef]
    ) -> ListDiscoveredEndpointsOutputTypeDef:
        """
        Returns a paginated list of endpoints discovered during a pentest job execution.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_discovered_endpoints.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_discovered_endpoints)
        """

    def list_findings(
        self, **kwargs: Unpack[ListFindingsInputTypeDef]
    ) -> ListFindingsOutputTypeDef:
        """
        Lists the security findings for a pentest job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_findings.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_findings)
        """

    def list_integrated_resources(
        self, **kwargs: Unpack[ListIntegratedResourcesInputTypeDef]
    ) -> ListIntegratedResourcesOutputTypeDef:
        """
        Lists the integrated resources for an agent space, optionally filtered by
        integration or resource type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_integrated_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_integrated_resources)
        """

    def list_integrations(
        self, **kwargs: Unpack[ListIntegrationsInputTypeDef]
    ) -> ListIntegrationsOutputTypeDef:
        """
        Lists the integrations in your account, optionally filtered by provider or
        provider type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_integrations.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_integrations)
        """

    def list_memberships(
        self, **kwargs: Unpack[ListMembershipsRequestTypeDef]
    ) -> ListMembershipsResponseTypeDef:
        """
        Returns a paginated list of membership summaries for the specified agent space
        within an application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_memberships.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_memberships)
        """

    def list_pentest_job_tasks(
        self, **kwargs: Unpack[ListPentestJobTasksInputTypeDef]
    ) -> ListPentestJobTasksOutputTypeDef:
        """
        Returns a paginated list of task summaries for the specified pentest job,
        optionally filtered by step name or category.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_pentest_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_pentest_job_tasks)
        """

    def list_pentest_jobs_for_pentest(
        self, **kwargs: Unpack[ListPentestJobsForPentestInputTypeDef]
    ) -> ListPentestJobsForPentestOutputTypeDef:
        """
        Returns a paginated list of pentest job summaries for the specified pentest
        configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_pentest_jobs_for_pentest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_pentest_jobs_for_pentest)
        """

    def list_pentests(
        self, **kwargs: Unpack[ListPentestsInputTypeDef]
    ) -> ListPentestsOutputTypeDef:
        """
        Returns a paginated list of pentest summaries for the specified agent space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_pentests.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_pentests)
        """

    def list_private_connections(
        self, **kwargs: Unpack[ListPrivateConnectionsInputTypeDef]
    ) -> ListPrivateConnectionsOutputTypeDef:
        """
        Lists the private connections in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_private_connections.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_private_connections)
        """

    def list_security_requirement_packs(
        self, **kwargs: Unpack[ListSecurityRequirementPacksInputTypeDef]
    ) -> ListSecurityRequirementPacksOutputTypeDef:
        """
        Lists all security requirement packs in the caller's account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_security_requirement_packs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_security_requirement_packs)
        """

    def list_security_requirements(
        self, **kwargs: Unpack[ListSecurityRequirementsInputTypeDef]
    ) -> ListSecurityRequirementsOutputTypeDef:
        """
        Lists security requirements within a pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_security_requirements.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_security_requirements)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Returns the tags associated with the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_tags_for_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_tags_for_resource)
        """

    def list_target_domains(
        self, **kwargs: Unpack[ListTargetDomainsInputTypeDef]
    ) -> ListTargetDomainsOutputTypeDef:
        """
        Returns a paginated list of target domain summaries in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_target_domains.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_target_domains)
        """

    def list_threat_model_job_tasks(
        self, **kwargs: Unpack[ListThreatModelJobTasksInputTypeDef]
    ) -> ListThreatModelJobTasksOutputTypeDef:
        """
        Returns a paginated list of task summaries for the specified threat model job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_threat_model_job_tasks.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_threat_model_job_tasks)
        """

    def list_threat_model_jobs(
        self, **kwargs: Unpack[ListThreatModelJobsInputTypeDef]
    ) -> ListThreatModelJobsOutputTypeDef:
        """
        Returns a paginated list of threat model job summaries for the specified threat
        model.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_threat_model_jobs.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_threat_model_jobs)
        """

    def list_threat_models(
        self, **kwargs: Unpack[ListThreatModelsInputTypeDef]
    ) -> ListThreatModelsOutputTypeDef:
        """
        Returns a paginated list of threat model summaries for the specified agent
        space.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_threat_models.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_threat_models)
        """

    def list_threats(self, **kwargs: Unpack[ListThreatsInputTypeDef]) -> ListThreatsOutputTypeDef:
        """
        Returns a paginated list of threats for a threat model job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/list_threats.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#list_threats)
        """

    def start_code_remediation(
        self, **kwargs: Unpack[StartCodeRemediationInputTypeDef]
    ) -> dict[str, Any]:
        """
        Initiates code remediation for one or more security findings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/start_code_remediation.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#start_code_remediation)
        """

    def start_code_review_job(
        self, **kwargs: Unpack[StartCodeReviewJobInputTypeDef]
    ) -> StartCodeReviewJobOutputTypeDef:
        """
        Starts a new code review job for a code review configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/start_code_review_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#start_code_review_job)
        """

    def start_pentest_job(
        self, **kwargs: Unpack[StartPentestJobInputTypeDef]
    ) -> StartPentestJobOutputTypeDef:
        """
        Starts a new pentest job for a pentest configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/start_pentest_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#start_pentest_job)
        """

    def start_threat_model_job(
        self, **kwargs: Unpack[StartThreatModelJobInputTypeDef]
    ) -> StartThreatModelJobOutputTypeDef:
        """
        Starts a new threat model job for a threat model configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/start_threat_model_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#start_threat_model_job)
        """

    def stop_code_review_job(
        self, **kwargs: Unpack[StopCodeReviewJobInputTypeDef]
    ) -> dict[str, Any]:
        """
        Stops a running code review job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/stop_code_review_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#stop_code_review_job)
        """

    def stop_pentest_job(self, **kwargs: Unpack[StopPentestJobInputTypeDef]) -> dict[str, Any]:
        """
        Stops a running pentest job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/stop_pentest_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#stop_pentest_job)
        """

    def stop_threat_model_job(
        self, **kwargs: Unpack[StopThreatModelJobInputTypeDef]
    ) -> dict[str, Any]:
        """
        Stops a running threat model job.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/stop_threat_model_job.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#stop_threat_model_job)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/tag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/untag_resource.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#untag_resource)
        """

    def update_agent_space(
        self, **kwargs: Unpack[UpdateAgentSpaceInputTypeDef]
    ) -> UpdateAgentSpaceOutputTypeDef:
        """
        Updates the configuration of an existing agent space, including its name,
        description, AWS resources, target domains, and code review settings.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_agent_space.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_agent_space)
        """

    def update_application(
        self, **kwargs: Unpack[UpdateApplicationRequestTypeDef]
    ) -> UpdateApplicationResponseTypeDef:
        """
        Updates the configuration of an existing application, including the IAM role
        and default KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_application.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_application)
        """

    def update_code_review(
        self, **kwargs: Unpack[UpdateCodeReviewInputTypeDef]
    ) -> UpdateCodeReviewOutputTypeDef:
        """
        Updates an existing code review configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_code_review.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_code_review)
        """

    def update_finding(self, **kwargs: Unpack[UpdateFindingInputTypeDef]) -> dict[str, Any]:
        """
        Updates the status or risk level of a security finding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_finding.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_finding)
        """

    def update_integrated_resources(
        self, **kwargs: Unpack[UpdateIntegratedResourcesInputTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the integrated resources for an agent space, including their
        capabilities.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_integrated_resources.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_integrated_resources)
        """

    def update_pentest(
        self, **kwargs: Unpack[UpdatePentestInputTypeDef]
    ) -> UpdatePentestOutputTypeDef:
        """
        Updates an existing pentest configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_pentest.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_pentest)
        """

    def update_private_connection_certificate(
        self, **kwargs: Unpack[UpdatePrivateConnectionCertificateInputTypeDef]
    ) -> UpdatePrivateConnectionCertificateOutputTypeDef:
        """
        Updates the certificate associated with a private connection.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_private_connection_certificate.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_private_connection_certificate)
        """

    def update_security_requirement_pack(
        self, **kwargs: Unpack[UpdateSecurityRequirementPackInputTypeDef]
    ) -> UpdateSecurityRequirementPackOutputTypeDef:
        """
        Updates a security requirement pack.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_security_requirement_pack.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_security_requirement_pack)
        """

    def update_target_domain(
        self, **kwargs: Unpack[UpdateTargetDomainInputTypeDef]
    ) -> UpdateTargetDomainOutputTypeDef:
        """
        Updates the verification method for a target domain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_target_domain.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_target_domain)
        """

    def update_threat(
        self, **kwargs: Unpack[UpdateThreatInputTypeDef]
    ) -> UpdateThreatOutputTypeDef:
        """
        Updates a threat.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_threat.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_threat)
        """

    def update_threat_model(
        self, **kwargs: Unpack[UpdateThreatModelInputTypeDef]
    ) -> UpdateThreatModelOutputTypeDef:
        """
        Updates an existing threat model configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/update_threat_model.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#update_threat_model)
        """

    def verify_target_domain(
        self, **kwargs: Unpack[VerifyTargetDomainInputTypeDef]
    ) -> VerifyTargetDomainOutputTypeDef:
        """
        Initiates verification of a target domain.

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
        self, operation_name: Literal["list_code_review_job_tasks"]
    ) -> ListCodeReviewJobTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_review_jobs_for_code_review"]
    ) -> ListCodeReviewJobsForCodeReviewPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_code_reviews"]
    ) -> ListCodeReviewsPaginator:
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
        self, operation_name: Literal["list_private_connections"]
    ) -> ListPrivateConnectionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_security_requirement_packs"]
    ) -> ListSecurityRequirementPacksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_security_requirements"]
    ) -> ListSecurityRequirementsPaginator:
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

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_threat_model_job_tasks"]
    ) -> ListThreatModelJobTasksPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_threat_model_jobs"]
    ) -> ListThreatModelJobsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_threat_models"]
    ) -> ListThreatModelsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_threats"]
    ) -> ListThreatsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/securityagent/client/get_paginator.html)
        [Show boto3-stubs-full documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_securityagent/client/#get_paginator)
        """
