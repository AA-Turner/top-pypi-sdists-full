"""
Type annotations for observabilityadmin service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_observabilityadmin.client import CloudWatchObservabilityAdminServiceClient

    session = get_session()
    async with session.create_client("observabilityadmin") as client:
        client: CloudWatchObservabilityAdminServiceClient
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
    ListCentralizationRulesForOrganizationPaginator,
    ListResourceTelemetryForOrganizationPaginator,
    ListResourceTelemetryPaginator,
    ListS3TableIntegrationsPaginator,
    ListTelemetryPipelinesPaginator,
    ListTelemetryRulesForOrganizationPaginator,
    ListTelemetryRulesPaginator,
)
from .type_defs import (
    CreateCentralizationRuleForOrganizationInputTypeDef,
    CreateCentralizationRuleForOrganizationOutputTypeDef,
    CreateS3TableIntegrationInputTypeDef,
    CreateS3TableIntegrationOutputTypeDef,
    CreateTelemetryPipelineInputTypeDef,
    CreateTelemetryPipelineOutputTypeDef,
    CreateTelemetryRuleForOrganizationInputTypeDef,
    CreateTelemetryRuleForOrganizationOutputTypeDef,
    CreateTelemetryRuleInputTypeDef,
    CreateTelemetryRuleOutputTypeDef,
    DeleteCentralizationRuleForOrganizationInputTypeDef,
    DeleteS3TableIntegrationInputTypeDef,
    DeleteTelemetryPipelineInputTypeDef,
    DeleteTelemetryRuleForOrganizationInputTypeDef,
    DeleteTelemetryRuleInputTypeDef,
    EmptyResponseMetadataTypeDef,
    GetCentralizationRuleForOrganizationInputTypeDef,
    GetCentralizationRuleForOrganizationOutputTypeDef,
    GetS3TableIntegrationInputTypeDef,
    GetS3TableIntegrationOutputTypeDef,
    GetTelemetryEnrichmentStatusOutputTypeDef,
    GetTelemetryEvaluationStatusForOrganizationOutputTypeDef,
    GetTelemetryEvaluationStatusOutputTypeDef,
    GetTelemetryPipelineInputTypeDef,
    GetTelemetryPipelineOutputTypeDef,
    GetTelemetryRuleForOrganizationInputTypeDef,
    GetTelemetryRuleForOrganizationOutputTypeDef,
    GetTelemetryRuleInputTypeDef,
    GetTelemetryRuleOutputTypeDef,
    ListCentralizationRulesForOrganizationInputTypeDef,
    ListCentralizationRulesForOrganizationOutputTypeDef,
    ListResourceTelemetryForOrganizationInputTypeDef,
    ListResourceTelemetryForOrganizationOutputTypeDef,
    ListResourceTelemetryInputTypeDef,
    ListResourceTelemetryOutputTypeDef,
    ListS3TableIntegrationsInputTypeDef,
    ListS3TableIntegrationsOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    ListTelemetryPipelinesInputTypeDef,
    ListTelemetryPipelinesOutputTypeDef,
    ListTelemetryRulesForOrganizationInputTypeDef,
    ListTelemetryRulesForOrganizationOutputTypeDef,
    ListTelemetryRulesInputTypeDef,
    ListTelemetryRulesOutputTypeDef,
    StartTelemetryEnrichmentOutputTypeDef,
    StopTelemetryEnrichmentOutputTypeDef,
    TagResourceInputTypeDef,
    TestTelemetryPipelineInputTypeDef,
    TestTelemetryPipelineOutputTypeDef,
    UntagResourceInputTypeDef,
    UpdateCentralizationRuleForOrganizationInputTypeDef,
    UpdateCentralizationRuleForOrganizationOutputTypeDef,
    UpdateTelemetryPipelineInputTypeDef,
    UpdateTelemetryRuleForOrganizationInputTypeDef,
    UpdateTelemetryRuleForOrganizationOutputTypeDef,
    UpdateTelemetryRuleInputTypeDef,
    UpdateTelemetryRuleOutputTypeDef,
    ValidateTelemetryPipelineConfigurationInputTypeDef,
    ValidateTelemetryPipelineConfigurationOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("CloudWatchObservabilityAdminServiceClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidStateException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TooManyRequestsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class CloudWatchObservabilityAdminServiceClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchObservabilityAdminServiceClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#generate_presigned_url)
        """

    async def create_centralization_rule_for_organization(
        self, **kwargs: Unpack[CreateCentralizationRuleForOrganizationInputTypeDef]
    ) -> CreateCentralizationRuleForOrganizationOutputTypeDef:
        """
        Creates a centralization rule that applies across an Amazon Web Services
        Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/create_centralization_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#create_centralization_rule_for_organization)
        """

    async def create_s3_table_integration(
        self, **kwargs: Unpack[CreateS3TableIntegrationInputTypeDef]
    ) -> CreateS3TableIntegrationOutputTypeDef:
        """
        Creates an integration between CloudWatch and S3 Tables for analytics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/create_s3_table_integration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#create_s3_table_integration)
        """

    async def create_telemetry_pipeline(
        self, **kwargs: Unpack[CreateTelemetryPipelineInputTypeDef]
    ) -> CreateTelemetryPipelineOutputTypeDef:
        """
        Creates a telemetry pipeline for processing and transforming telemetry data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/create_telemetry_pipeline.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#create_telemetry_pipeline)
        """

    async def create_telemetry_rule(
        self, **kwargs: Unpack[CreateTelemetryRuleInputTypeDef]
    ) -> CreateTelemetryRuleOutputTypeDef:
        """
        Creates a telemetry rule that defines how telemetry should be configured for
        Amazon Web Services resources in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/create_telemetry_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#create_telemetry_rule)
        """

    async def create_telemetry_rule_for_organization(
        self, **kwargs: Unpack[CreateTelemetryRuleForOrganizationInputTypeDef]
    ) -> CreateTelemetryRuleForOrganizationOutputTypeDef:
        """
        Creates a telemetry rule that applies across an Amazon Web Services
        Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/create_telemetry_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#create_telemetry_rule_for_organization)
        """

    async def delete_centralization_rule_for_organization(
        self, **kwargs: Unpack[DeleteCentralizationRuleForOrganizationInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an organization-wide centralization rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/delete_centralization_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#delete_centralization_rule_for_organization)
        """

    async def delete_s3_table_integration(
        self, **kwargs: Unpack[DeleteS3TableIntegrationInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an S3 Table integration and its associated data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/delete_s3_table_integration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#delete_s3_table_integration)
        """

    async def delete_telemetry_pipeline(
        self, **kwargs: Unpack[DeleteTelemetryPipelineInputTypeDef]
    ) -> dict[str, Any]:
        """
        Deletes a telemetry pipeline and its associated resources.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/delete_telemetry_pipeline.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#delete_telemetry_pipeline)
        """

    async def delete_telemetry_rule(
        self, **kwargs: Unpack[DeleteTelemetryRuleInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a telemetry rule from your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/delete_telemetry_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#delete_telemetry_rule)
        """

    async def delete_telemetry_rule_for_organization(
        self, **kwargs: Unpack[DeleteTelemetryRuleForOrganizationInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an organization-wide telemetry rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/delete_telemetry_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#delete_telemetry_rule_for_organization)
        """

    async def get_centralization_rule_for_organization(
        self, **kwargs: Unpack[GetCentralizationRuleForOrganizationInputTypeDef]
    ) -> GetCentralizationRuleForOrganizationOutputTypeDef:
        """
        Retrieves the details of a specific organization centralization rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_centralization_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_centralization_rule_for_organization)
        """

    async def get_s3_table_integration(
        self, **kwargs: Unpack[GetS3TableIntegrationInputTypeDef]
    ) -> GetS3TableIntegrationOutputTypeDef:
        """
        Retrieves information about a specific S3 Table integration, including its
        configuration, status, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_s3_table_integration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_s3_table_integration)
        """

    async def get_telemetry_enrichment_status(self) -> GetTelemetryEnrichmentStatusOutputTypeDef:
        """
        Returns the current status of the resource tags for telemetry feature, which
        enhances telemetry data with additional resource metadata from Resource
        Explorer.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_enrichment_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_enrichment_status)
        """

    async def get_telemetry_evaluation_status(self) -> GetTelemetryEvaluationStatusOutputTypeDef:
        """
        Returns the current onboarding status of the telemetry config feature,
        including the status of the feature and reason the feature failed to start or
        stop.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_evaluation_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_evaluation_status)
        """

    async def get_telemetry_evaluation_status_for_organization(
        self,
    ) -> GetTelemetryEvaluationStatusForOrganizationOutputTypeDef:
        """
        This returns the onboarding status of the telemetry configuration feature for
        the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_evaluation_status_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_evaluation_status_for_organization)
        """

    async def get_telemetry_pipeline(
        self, **kwargs: Unpack[GetTelemetryPipelineInputTypeDef]
    ) -> GetTelemetryPipelineOutputTypeDef:
        """
        Retrieves information about a specific telemetry pipeline, including its
        configuration, status, and metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_pipeline.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_pipeline)
        """

    async def get_telemetry_rule(
        self, **kwargs: Unpack[GetTelemetryRuleInputTypeDef]
    ) -> GetTelemetryRuleOutputTypeDef:
        """
        Retrieves the details of a specific telemetry rule in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_rule)
        """

    async def get_telemetry_rule_for_organization(
        self, **kwargs: Unpack[GetTelemetryRuleForOrganizationInputTypeDef]
    ) -> GetTelemetryRuleForOrganizationOutputTypeDef:
        """
        Retrieves the details of a specific organization telemetry rule.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_telemetry_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_telemetry_rule_for_organization)
        """

    async def list_centralization_rules_for_organization(
        self, **kwargs: Unpack[ListCentralizationRulesForOrganizationInputTypeDef]
    ) -> ListCentralizationRulesForOrganizationOutputTypeDef:
        """
        Lists all centralization rules in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_centralization_rules_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_centralization_rules_for_organization)
        """

    async def list_resource_telemetry(
        self, **kwargs: Unpack[ListResourceTelemetryInputTypeDef]
    ) -> ListResourceTelemetryOutputTypeDef:
        """
        Returns a list of telemetry configurations for Amazon Web Services resources
        supported by telemetry config.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_resource_telemetry.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_resource_telemetry)
        """

    async def list_resource_telemetry_for_organization(
        self, **kwargs: Unpack[ListResourceTelemetryForOrganizationInputTypeDef]
    ) -> ListResourceTelemetryForOrganizationOutputTypeDef:
        """
        Returns a list of telemetry configurations for Amazon Web Services resources
        supported by telemetry config in the organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_resource_telemetry_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_resource_telemetry_for_organization)
        """

    async def list_s3_table_integrations(
        self, **kwargs: Unpack[ListS3TableIntegrationsInputTypeDef]
    ) -> ListS3TableIntegrationsOutputTypeDef:
        """
        Lists all S3 Table integrations in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_s3_table_integrations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_s3_table_integrations)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists all tags attached to the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_tags_for_resource)
        """

    async def list_telemetry_pipelines(
        self, **kwargs: Unpack[ListTelemetryPipelinesInputTypeDef]
    ) -> ListTelemetryPipelinesOutputTypeDef:
        """
        Returns a list of telemetry pipelines in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_telemetry_pipelines.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_telemetry_pipelines)
        """

    async def list_telemetry_rules(
        self, **kwargs: Unpack[ListTelemetryRulesInputTypeDef]
    ) -> ListTelemetryRulesOutputTypeDef:
        """
        Lists all telemetry rules in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_telemetry_rules.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_telemetry_rules)
        """

    async def list_telemetry_rules_for_organization(
        self, **kwargs: Unpack[ListTelemetryRulesForOrganizationInputTypeDef]
    ) -> ListTelemetryRulesForOrganizationOutputTypeDef:
        """
        Lists all telemetry rules in your organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/list_telemetry_rules_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#list_telemetry_rules_for_organization)
        """

    async def start_telemetry_enrichment(self) -> StartTelemetryEnrichmentOutputTypeDef:
        """
        Enables the resource tags for telemetry feature for your account, which
        enhances telemetry data with additional resource metadata from Resource
        Explorer to provide richer context for monitoring and observability.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_enrichment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_enrichment)
        """

    async def start_telemetry_evaluation(self) -> EmptyResponseMetadataTypeDef:
        """
        This action begins onboarding the caller Amazon Web Services account to the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_evaluation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_evaluation)
        """

    async def start_telemetry_evaluation_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        This actions begins onboarding the organization and all member accounts to the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/start_telemetry_evaluation_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#start_telemetry_evaluation_for_organization)
        """

    async def stop_telemetry_enrichment(self) -> StopTelemetryEnrichmentOutputTypeDef:
        """
        Disables the resource tags for telemetry feature for your account, stopping the
        enhancement of telemetry data with additional resource metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_enrichment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_enrichment)
        """

    async def stop_telemetry_evaluation(self) -> EmptyResponseMetadataTypeDef:
        """
        This action begins offboarding the caller Amazon Web Services account from the
        telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_evaluation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_evaluation)
        """

    async def stop_telemetry_evaluation_for_organization(self) -> EmptyResponseMetadataTypeDef:
        """
        This action offboards the Organization of the caller Amazon Web Services
        account from the telemetry config feature.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/stop_telemetry_evaluation_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#stop_telemetry_evaluation_for_organization)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or updates tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#tag_resource)
        """

    async def test_telemetry_pipeline(
        self, **kwargs: Unpack[TestTelemetryPipelineInputTypeDef]
    ) -> TestTelemetryPipelineOutputTypeDef:
        """
        Tests a pipeline configuration with sample records to validate data processing
        before deployment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/test_telemetry_pipeline.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#test_telemetry_pipeline)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#untag_resource)
        """

    async def update_centralization_rule_for_organization(
        self, **kwargs: Unpack[UpdateCentralizationRuleForOrganizationInputTypeDef]
    ) -> UpdateCentralizationRuleForOrganizationOutputTypeDef:
        """
        Updates an existing centralization rule that applies across an Amazon Web
        Services Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/update_centralization_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#update_centralization_rule_for_organization)
        """

    async def update_telemetry_pipeline(
        self, **kwargs: Unpack[UpdateTelemetryPipelineInputTypeDef]
    ) -> dict[str, Any]:
        """
        Updates the configuration of an existing telemetry pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/update_telemetry_pipeline.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#update_telemetry_pipeline)
        """

    async def update_telemetry_rule(
        self, **kwargs: Unpack[UpdateTelemetryRuleInputTypeDef]
    ) -> UpdateTelemetryRuleOutputTypeDef:
        """
        Updates an existing telemetry rule in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/update_telemetry_rule.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#update_telemetry_rule)
        """

    async def update_telemetry_rule_for_organization(
        self, **kwargs: Unpack[UpdateTelemetryRuleForOrganizationInputTypeDef]
    ) -> UpdateTelemetryRuleForOrganizationOutputTypeDef:
        """
        Updates an existing telemetry rule that applies across an Amazon Web Services
        Organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/update_telemetry_rule_for_organization.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#update_telemetry_rule_for_organization)
        """

    async def validate_telemetry_pipeline_configuration(
        self, **kwargs: Unpack[ValidateTelemetryPipelineConfigurationInputTypeDef]
    ) -> ValidateTelemetryPipelineConfigurationOutputTypeDef:
        """
        Validates a pipeline configuration without creating the pipeline.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/validate_telemetry_pipeline_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#validate_telemetry_pipeline_configuration)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_centralization_rules_for_organization"]
    ) -> ListCentralizationRulesForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_telemetry_for_organization"]
    ) -> ListResourceTelemetryForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_telemetry"]
    ) -> ListResourceTelemetryPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_s3_table_integrations"]
    ) -> ListS3TableIntegrationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_telemetry_pipelines"]
    ) -> ListTelemetryPipelinesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_telemetry_rules_for_organization"]
    ) -> ListTelemetryRulesForOrganizationPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_telemetry_rules"]
    ) -> ListTelemetryRulesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/observabilityadmin.html#CloudWatchObservabilityAdminService.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_observabilityadmin/client/)
        """
