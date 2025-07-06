"""
Type annotations for auditmanager service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_auditmanager.client import AuditManagerClient

    session = get_session()
    async with session.create_client("auditmanager") as client:
        client: AuditManagerClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .type_defs import (
    AssociateAssessmentReportEvidenceFolderRequestTypeDef,
    BatchAssociateAssessmentReportEvidenceRequestTypeDef,
    BatchAssociateAssessmentReportEvidenceResponseTypeDef,
    BatchCreateDelegationByAssessmentRequestTypeDef,
    BatchCreateDelegationByAssessmentResponseTypeDef,
    BatchDeleteDelegationByAssessmentRequestTypeDef,
    BatchDeleteDelegationByAssessmentResponseTypeDef,
    BatchDisassociateAssessmentReportEvidenceRequestTypeDef,
    BatchDisassociateAssessmentReportEvidenceResponseTypeDef,
    BatchImportEvidenceToAssessmentControlRequestTypeDef,
    BatchImportEvidenceToAssessmentControlResponseTypeDef,
    CreateAssessmentFrameworkRequestTypeDef,
    CreateAssessmentFrameworkResponseTypeDef,
    CreateAssessmentReportRequestTypeDef,
    CreateAssessmentReportResponseTypeDef,
    CreateAssessmentRequestTypeDef,
    CreateAssessmentResponseTypeDef,
    CreateControlRequestTypeDef,
    CreateControlResponseTypeDef,
    DeleteAssessmentFrameworkRequestTypeDef,
    DeleteAssessmentFrameworkShareRequestTypeDef,
    DeleteAssessmentReportRequestTypeDef,
    DeleteAssessmentRequestTypeDef,
    DeleteControlRequestTypeDef,
    DeregisterAccountResponseTypeDef,
    DeregisterOrganizationAdminAccountRequestTypeDef,
    DisassociateAssessmentReportEvidenceFolderRequestTypeDef,
    GetAccountStatusResponseTypeDef,
    GetAssessmentFrameworkRequestTypeDef,
    GetAssessmentFrameworkResponseTypeDef,
    GetAssessmentReportUrlRequestTypeDef,
    GetAssessmentReportUrlResponseTypeDef,
    GetAssessmentRequestTypeDef,
    GetAssessmentResponseTypeDef,
    GetChangeLogsRequestTypeDef,
    GetChangeLogsResponseTypeDef,
    GetControlRequestTypeDef,
    GetControlResponseTypeDef,
    GetDelegationsRequestTypeDef,
    GetDelegationsResponseTypeDef,
    GetEvidenceByEvidenceFolderRequestTypeDef,
    GetEvidenceByEvidenceFolderResponseTypeDef,
    GetEvidenceFileUploadUrlRequestTypeDef,
    GetEvidenceFileUploadUrlResponseTypeDef,
    GetEvidenceFolderRequestTypeDef,
    GetEvidenceFolderResponseTypeDef,
    GetEvidenceFoldersByAssessmentControlRequestTypeDef,
    GetEvidenceFoldersByAssessmentControlResponseTypeDef,
    GetEvidenceFoldersByAssessmentRequestTypeDef,
    GetEvidenceFoldersByAssessmentResponseTypeDef,
    GetEvidenceRequestTypeDef,
    GetEvidenceResponseTypeDef,
    GetInsightsByAssessmentRequestTypeDef,
    GetInsightsByAssessmentResponseTypeDef,
    GetInsightsResponseTypeDef,
    GetOrganizationAdminAccountResponseTypeDef,
    GetServicesInScopeResponseTypeDef,
    GetSettingsRequestTypeDef,
    GetSettingsResponseTypeDef,
    ListAssessmentControlInsightsByControlDomainRequestTypeDef,
    ListAssessmentControlInsightsByControlDomainResponseTypeDef,
    ListAssessmentFrameworkShareRequestsRequestTypeDef,
    ListAssessmentFrameworkShareRequestsResponseTypeDef,
    ListAssessmentFrameworksRequestTypeDef,
    ListAssessmentFrameworksResponseTypeDef,
    ListAssessmentReportsRequestTypeDef,
    ListAssessmentReportsResponseTypeDef,
    ListAssessmentsRequestTypeDef,
    ListAssessmentsResponseTypeDef,
    ListControlDomainInsightsByAssessmentRequestTypeDef,
    ListControlDomainInsightsByAssessmentResponseTypeDef,
    ListControlDomainInsightsRequestTypeDef,
    ListControlDomainInsightsResponseTypeDef,
    ListControlInsightsByControlDomainRequestTypeDef,
    ListControlInsightsByControlDomainResponseTypeDef,
    ListControlsRequestTypeDef,
    ListControlsResponseTypeDef,
    ListKeywordsForDataSourceRequestTypeDef,
    ListKeywordsForDataSourceResponseTypeDef,
    ListNotificationsRequestTypeDef,
    ListNotificationsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterAccountRequestTypeDef,
    RegisterAccountResponseTypeDef,
    RegisterOrganizationAdminAccountRequestTypeDef,
    RegisterOrganizationAdminAccountResponseTypeDef,
    StartAssessmentFrameworkShareRequestTypeDef,
    StartAssessmentFrameworkShareResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAssessmentControlRequestTypeDef,
    UpdateAssessmentControlResponseTypeDef,
    UpdateAssessmentControlSetStatusRequestTypeDef,
    UpdateAssessmentControlSetStatusResponseTypeDef,
    UpdateAssessmentFrameworkRequestTypeDef,
    UpdateAssessmentFrameworkResponseTypeDef,
    UpdateAssessmentFrameworkShareRequestTypeDef,
    UpdateAssessmentFrameworkShareResponseTypeDef,
    UpdateAssessmentRequestTypeDef,
    UpdateAssessmentResponseTypeDef,
    UpdateAssessmentStatusRequestTypeDef,
    UpdateAssessmentStatusResponseTypeDef,
    UpdateControlRequestTypeDef,
    UpdateControlResponseTypeDef,
    UpdateSettingsRequestTypeDef,
    UpdateSettingsResponseTypeDef,
    ValidateAssessmentReportIntegrityRequestTypeDef,
    ValidateAssessmentReportIntegrityResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack

__all__ = ("AuditManagerClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class AuditManagerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AuditManagerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#generate_presigned_url)
        """

    async def associate_assessment_report_evidence_folder(
        self, **kwargs: Unpack[AssociateAssessmentReportEvidenceFolderRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Associates an evidence folder to an assessment report in an Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/associate_assessment_report_evidence_folder.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#associate_assessment_report_evidence_folder)
        """

    async def batch_associate_assessment_report_evidence(
        self, **kwargs: Unpack[BatchAssociateAssessmentReportEvidenceRequestTypeDef]
    ) -> BatchAssociateAssessmentReportEvidenceResponseTypeDef:
        """
        Associates a list of evidence to an assessment report in an Audit Manager
        assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_associate_assessment_report_evidence.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#batch_associate_assessment_report_evidence)
        """

    async def batch_create_delegation_by_assessment(
        self, **kwargs: Unpack[BatchCreateDelegationByAssessmentRequestTypeDef]
    ) -> BatchCreateDelegationByAssessmentResponseTypeDef:
        """
        Creates a batch of delegations for an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_create_delegation_by_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#batch_create_delegation_by_assessment)
        """

    async def batch_delete_delegation_by_assessment(
        self, **kwargs: Unpack[BatchDeleteDelegationByAssessmentRequestTypeDef]
    ) -> BatchDeleteDelegationByAssessmentResponseTypeDef:
        """
        Deletes a batch of delegations for an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_delete_delegation_by_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#batch_delete_delegation_by_assessment)
        """

    async def batch_disassociate_assessment_report_evidence(
        self, **kwargs: Unpack[BatchDisassociateAssessmentReportEvidenceRequestTypeDef]
    ) -> BatchDisassociateAssessmentReportEvidenceResponseTypeDef:
        """
        Disassociates a list of evidence from an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_disassociate_assessment_report_evidence.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#batch_disassociate_assessment_report_evidence)
        """

    async def batch_import_evidence_to_assessment_control(
        self, **kwargs: Unpack[BatchImportEvidenceToAssessmentControlRequestTypeDef]
    ) -> BatchImportEvidenceToAssessmentControlResponseTypeDef:
        """
        Adds one or more pieces of evidence to a control in an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/batch_import_evidence_to_assessment_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#batch_import_evidence_to_assessment_control)
        """

    async def create_assessment(
        self, **kwargs: Unpack[CreateAssessmentRequestTypeDef]
    ) -> CreateAssessmentResponseTypeDef:
        """
        Creates an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#create_assessment)
        """

    async def create_assessment_framework(
        self, **kwargs: Unpack[CreateAssessmentFrameworkRequestTypeDef]
    ) -> CreateAssessmentFrameworkResponseTypeDef:
        """
        Creates a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_assessment_framework.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#create_assessment_framework)
        """

    async def create_assessment_report(
        self, **kwargs: Unpack[CreateAssessmentReportRequestTypeDef]
    ) -> CreateAssessmentReportResponseTypeDef:
        """
        Creates an assessment report for the specified assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_assessment_report.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#create_assessment_report)
        """

    async def create_control(
        self, **kwargs: Unpack[CreateControlRequestTypeDef]
    ) -> CreateControlResponseTypeDef:
        """
        Creates a new custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/create_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#create_control)
        """

    async def delete_assessment(
        self, **kwargs: Unpack[DeleteAssessmentRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#delete_assessment)
        """

    async def delete_assessment_framework(
        self, **kwargs: Unpack[DeleteAssessmentFrameworkRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment_framework.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#delete_assessment_framework)
        """

    async def delete_assessment_framework_share(
        self, **kwargs: Unpack[DeleteAssessmentFrameworkShareRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment_framework_share.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#delete_assessment_framework_share)
        """

    async def delete_assessment_report(
        self, **kwargs: Unpack[DeleteAssessmentReportRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_assessment_report.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#delete_assessment_report)
        """

    async def delete_control(self, **kwargs: Unpack[DeleteControlRequestTypeDef]) -> Dict[str, Any]:
        """
        Deletes a custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/delete_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#delete_control)
        """

    async def deregister_account(self) -> DeregisterAccountResponseTypeDef:
        """
        Deregisters an account in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/deregister_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#deregister_account)
        """

    async def deregister_organization_admin_account(
        self, **kwargs: Unpack[DeregisterOrganizationAdminAccountRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the specified Amazon Web Services account as a delegated administrator
        for Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/deregister_organization_admin_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#deregister_organization_admin_account)
        """

    async def disassociate_assessment_report_evidence_folder(
        self, **kwargs: Unpack[DisassociateAssessmentReportEvidenceFolderRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disassociates an evidence folder from the specified assessment report in Audit
        Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/disassociate_assessment_report_evidence_folder.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#disassociate_assessment_report_evidence_folder)
        """

    async def get_account_status(self) -> GetAccountStatusResponseTypeDef:
        """
        Gets the registration status of an account in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_account_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_account_status)
        """

    async def get_assessment(
        self, **kwargs: Unpack[GetAssessmentRequestTypeDef]
    ) -> GetAssessmentResponseTypeDef:
        """
        Gets information about a specified assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_assessment)
        """

    async def get_assessment_framework(
        self, **kwargs: Unpack[GetAssessmentFrameworkRequestTypeDef]
    ) -> GetAssessmentFrameworkResponseTypeDef:
        """
        Gets information about a specified framework.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_assessment_framework.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_assessment_framework)
        """

    async def get_assessment_report_url(
        self, **kwargs: Unpack[GetAssessmentReportUrlRequestTypeDef]
    ) -> GetAssessmentReportUrlResponseTypeDef:
        """
        Gets the URL of an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_assessment_report_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_assessment_report_url)
        """

    async def get_change_logs(
        self, **kwargs: Unpack[GetChangeLogsRequestTypeDef]
    ) -> GetChangeLogsResponseTypeDef:
        """
        Gets a list of changelogs from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_change_logs.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_change_logs)
        """

    async def get_control(
        self, **kwargs: Unpack[GetControlRequestTypeDef]
    ) -> GetControlResponseTypeDef:
        """
        Gets information about a specified control.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_control)
        """

    async def get_delegations(
        self, **kwargs: Unpack[GetDelegationsRequestTypeDef]
    ) -> GetDelegationsResponseTypeDef:
        """
        Gets a list of delegations from an audit owner to a delegate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_delegations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_delegations)
        """

    async def get_evidence(
        self, **kwargs: Unpack[GetEvidenceRequestTypeDef]
    ) -> GetEvidenceResponseTypeDef:
        """
        Gets information about a specified evidence item.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_evidence)
        """

    async def get_evidence_by_evidence_folder(
        self, **kwargs: Unpack[GetEvidenceByEvidenceFolderRequestTypeDef]
    ) -> GetEvidenceByEvidenceFolderResponseTypeDef:
        """
        Gets all evidence from a specified evidence folder in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_by_evidence_folder.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_evidence_by_evidence_folder)
        """

    async def get_evidence_file_upload_url(
        self, **kwargs: Unpack[GetEvidenceFileUploadUrlRequestTypeDef]
    ) -> GetEvidenceFileUploadUrlResponseTypeDef:
        """
        Creates a presigned Amazon S3 URL that can be used to upload a file as manual
        evidence.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_file_upload_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_evidence_file_upload_url)
        """

    async def get_evidence_folder(
        self, **kwargs: Unpack[GetEvidenceFolderRequestTypeDef]
    ) -> GetEvidenceFolderResponseTypeDef:
        """
        Gets an evidence folder from a specified assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_folder.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_evidence_folder)
        """

    async def get_evidence_folders_by_assessment(
        self, **kwargs: Unpack[GetEvidenceFoldersByAssessmentRequestTypeDef]
    ) -> GetEvidenceFoldersByAssessmentResponseTypeDef:
        """
        Gets the evidence folders from a specified assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_folders_by_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_evidence_folders_by_assessment)
        """

    async def get_evidence_folders_by_assessment_control(
        self, **kwargs: Unpack[GetEvidenceFoldersByAssessmentControlRequestTypeDef]
    ) -> GetEvidenceFoldersByAssessmentControlResponseTypeDef:
        """
        Gets a list of evidence folders that are associated with a specified control in
        an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_evidence_folders_by_assessment_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_evidence_folders_by_assessment_control)
        """

    async def get_insights(self) -> GetInsightsResponseTypeDef:
        """
        Gets the latest analytics data for all your current active assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_insights.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_insights)
        """

    async def get_insights_by_assessment(
        self, **kwargs: Unpack[GetInsightsByAssessmentRequestTypeDef]
    ) -> GetInsightsByAssessmentResponseTypeDef:
        """
        Gets the latest analytics data for a specific active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_insights_by_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_insights_by_assessment)
        """

    async def get_organization_admin_account(self) -> GetOrganizationAdminAccountResponseTypeDef:
        """
        Gets the name of the delegated Amazon Web Services administrator account for a
        specified organization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_organization_admin_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_organization_admin_account)
        """

    async def get_services_in_scope(self) -> GetServicesInScopeResponseTypeDef:
        """
        Gets a list of the Amazon Web Services services from which Audit Manager can
        collect evidence.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_services_in_scope.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_services_in_scope)
        """

    async def get_settings(
        self, **kwargs: Unpack[GetSettingsRequestTypeDef]
    ) -> GetSettingsResponseTypeDef:
        """
        Gets the settings for a specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/get_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#get_settings)
        """

    async def list_assessment_control_insights_by_control_domain(
        self, **kwargs: Unpack[ListAssessmentControlInsightsByControlDomainRequestTypeDef]
    ) -> ListAssessmentControlInsightsByControlDomainResponseTypeDef:
        """
        Lists the latest analytics data for controls within a specific control domain
        and a specific active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_control_insights_by_control_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_assessment_control_insights_by_control_domain)
        """

    async def list_assessment_framework_share_requests(
        self, **kwargs: Unpack[ListAssessmentFrameworkShareRequestsRequestTypeDef]
    ) -> ListAssessmentFrameworkShareRequestsResponseTypeDef:
        """
        Returns a list of sent or received share requests for custom frameworks in
        Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_framework_share_requests.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_assessment_framework_share_requests)
        """

    async def list_assessment_frameworks(
        self, **kwargs: Unpack[ListAssessmentFrameworksRequestTypeDef]
    ) -> ListAssessmentFrameworksResponseTypeDef:
        """
        Returns a list of the frameworks that are available in the Audit Manager
        framework library.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_frameworks.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_assessment_frameworks)
        """

    async def list_assessment_reports(
        self, **kwargs: Unpack[ListAssessmentReportsRequestTypeDef]
    ) -> ListAssessmentReportsResponseTypeDef:
        """
        Returns a list of assessment reports created in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessment_reports.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_assessment_reports)
        """

    async def list_assessments(
        self, **kwargs: Unpack[ListAssessmentsRequestTypeDef]
    ) -> ListAssessmentsResponseTypeDef:
        """
        Returns a list of current and past assessments from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_assessments.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_assessments)
        """

    async def list_control_domain_insights(
        self, **kwargs: Unpack[ListControlDomainInsightsRequestTypeDef]
    ) -> ListControlDomainInsightsResponseTypeDef:
        """
        Lists the latest analytics data for control domains across all of your active
        assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_control_domain_insights.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_control_domain_insights)
        """

    async def list_control_domain_insights_by_assessment(
        self, **kwargs: Unpack[ListControlDomainInsightsByAssessmentRequestTypeDef]
    ) -> ListControlDomainInsightsByAssessmentResponseTypeDef:
        """
        Lists analytics data for control domains within a specified active assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_control_domain_insights_by_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_control_domain_insights_by_assessment)
        """

    async def list_control_insights_by_control_domain(
        self, **kwargs: Unpack[ListControlInsightsByControlDomainRequestTypeDef]
    ) -> ListControlInsightsByControlDomainResponseTypeDef:
        """
        Lists the latest analytics data for controls within a specific control domain
        across all active assessments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_control_insights_by_control_domain.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_control_insights_by_control_domain)
        """

    async def list_controls(
        self, **kwargs: Unpack[ListControlsRequestTypeDef]
    ) -> ListControlsResponseTypeDef:
        """
        Returns a list of controls from Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_controls.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_controls)
        """

    async def list_keywords_for_data_source(
        self, **kwargs: Unpack[ListKeywordsForDataSourceRequestTypeDef]
    ) -> ListKeywordsForDataSourceResponseTypeDef:
        """
        Returns a list of keywords that are pre-mapped to the specified control data
        source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_keywords_for_data_source.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_keywords_for_data_source)
        """

    async def list_notifications(
        self, **kwargs: Unpack[ListNotificationsRequestTypeDef]
    ) -> ListNotificationsResponseTypeDef:
        """
        Returns a list of all Audit Manager notifications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_notifications.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_notifications)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of tags for the specified resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#list_tags_for_resource)
        """

    async def register_account(
        self, **kwargs: Unpack[RegisterAccountRequestTypeDef]
    ) -> RegisterAccountResponseTypeDef:
        """
        Enables Audit Manager for the specified Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/register_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#register_account)
        """

    async def register_organization_admin_account(
        self, **kwargs: Unpack[RegisterOrganizationAdminAccountRequestTypeDef]
    ) -> RegisterOrganizationAdminAccountResponseTypeDef:
        """
        Enables an Amazon Web Services account within the organization as the delegated
        administrator for Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/register_organization_admin_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#register_organization_admin_account)
        """

    async def start_assessment_framework_share(
        self, **kwargs: Unpack[StartAssessmentFrameworkShareRequestTypeDef]
    ) -> StartAssessmentFrameworkShareResponseTypeDef:
        """
        Creates a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/start_assessment_framework_share.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#start_assessment_framework_share)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Tags the specified resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> Dict[str, Any]:
        """
        Removes a tag from a resource in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#untag_resource)
        """

    async def update_assessment(
        self, **kwargs: Unpack[UpdateAssessmentRequestTypeDef]
    ) -> UpdateAssessmentResponseTypeDef:
        """
        Edits an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_assessment)
        """

    async def update_assessment_control(
        self, **kwargs: Unpack[UpdateAssessmentControlRequestTypeDef]
    ) -> UpdateAssessmentControlResponseTypeDef:
        """
        Updates a control within an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_assessment_control)
        """

    async def update_assessment_control_set_status(
        self, **kwargs: Unpack[UpdateAssessmentControlSetStatusRequestTypeDef]
    ) -> UpdateAssessmentControlSetStatusResponseTypeDef:
        """
        Updates the status of a control set in an Audit Manager assessment.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_control_set_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_assessment_control_set_status)
        """

    async def update_assessment_framework(
        self, **kwargs: Unpack[UpdateAssessmentFrameworkRequestTypeDef]
    ) -> UpdateAssessmentFrameworkResponseTypeDef:
        """
        Updates a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_framework.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_assessment_framework)
        """

    async def update_assessment_framework_share(
        self, **kwargs: Unpack[UpdateAssessmentFrameworkShareRequestTypeDef]
    ) -> UpdateAssessmentFrameworkShareResponseTypeDef:
        """
        Updates a share request for a custom framework in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_framework_share.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_assessment_framework_share)
        """

    async def update_assessment_status(
        self, **kwargs: Unpack[UpdateAssessmentStatusRequestTypeDef]
    ) -> UpdateAssessmentStatusResponseTypeDef:
        """
        Updates the status of an assessment in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_assessment_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_assessment_status)
        """

    async def update_control(
        self, **kwargs: Unpack[UpdateControlRequestTypeDef]
    ) -> UpdateControlResponseTypeDef:
        """
        Updates a custom control in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_control.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_control)
        """

    async def update_settings(
        self, **kwargs: Unpack[UpdateSettingsRequestTypeDef]
    ) -> UpdateSettingsResponseTypeDef:
        """
        Updates Audit Manager settings for the current account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/update_settings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#update_settings)
        """

    async def validate_assessment_report_integrity(
        self, **kwargs: Unpack[ValidateAssessmentReportIntegrityRequestTypeDef]
    ) -> ValidateAssessmentReportIntegrityResponseTypeDef:
        """
        Validates the integrity of an assessment report in Audit Manager.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager/client/validate_assessment_report_integrity.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/#validate_assessment_report_integrity)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/auditmanager.html#AuditManager.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_auditmanager/client/)
        """
