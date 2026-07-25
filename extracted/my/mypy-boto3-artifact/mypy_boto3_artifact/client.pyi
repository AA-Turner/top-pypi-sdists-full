"""
Type annotations for artifact service Client.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_artifact.client import ArtifactClient

    session = Session()
    client: ArtifactClient = session.client("artifact")
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
    ListComplianceInquiriesPaginator,
    ListComplianceInquiryQueriesPaginator,
    ListCustomerAgreementsPaginator,
    ListReportsPaginator,
    ListReportVersionsPaginator,
)
from .type_defs import (
    CreateComplianceInquiryRequestTypeDef,
    CreateComplianceInquiryResponseTypeDef,
    ExportComplianceInquiryRequestTypeDef,
    ExportComplianceInquiryResponseTypeDef,
    GetAccountSettingsResponseTypeDef,
    GetComplianceInquiryMetadataRequestTypeDef,
    GetComplianceInquiryMetadataResponseTypeDef,
    GetReportMetadataRequestTypeDef,
    GetReportMetadataResponseTypeDef,
    GetReportRequestTypeDef,
    GetReportResponseTypeDef,
    GetTermForReportRequestTypeDef,
    GetTermForReportResponseTypeDef,
    ListComplianceInquiriesRequestTypeDef,
    ListComplianceInquiriesResponseTypeDef,
    ListComplianceInquiryQueriesRequestTypeDef,
    ListComplianceInquiryQueriesResponseTypeDef,
    ListCustomerAgreementsRequestTypeDef,
    ListCustomerAgreementsResponseTypeDef,
    ListReportsRequestTypeDef,
    ListReportsResponseTypeDef,
    ListReportVersionsRequestTypeDef,
    ListReportVersionsResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAccountSettingsRequestTypeDef,
    PutAccountSettingsResponseTypeDef,
    PutComplianceInquiryFeedbackRequestTypeDef,
    PutComplianceInquiryFeedbackResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("ArtifactClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ArtifactClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
    [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ArtifactClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact.html#Artifact.Client)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/can_paginate.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/generate_presigned_url.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#generate_presigned_url)
        """

    def create_compliance_inquiry(
        self, **kwargs: Unpack[CreateComplianceInquiryRequestTypeDef]
    ) -> CreateComplianceInquiryResponseTypeDef:
        """
        Create a new compliance inquiry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/create_compliance_inquiry.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#create_compliance_inquiry)
        """

    def export_compliance_inquiry(
        self, **kwargs: Unpack[ExportComplianceInquiryRequestTypeDef]
    ) -> ExportComplianceInquiryResponseTypeDef:
        """
        Export a compliance inquiry report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/export_compliance_inquiry.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#export_compliance_inquiry)
        """

    def get_account_settings(self) -> GetAccountSettingsResponseTypeDef:
        """
        Get the account settings for Artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_account_settings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_account_settings)
        """

    def get_compliance_inquiry_metadata(
        self, **kwargs: Unpack[GetComplianceInquiryMetadataRequestTypeDef]
    ) -> GetComplianceInquiryMetadataResponseTypeDef:
        """
        Get the metadata for a single compliance inquiry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_compliance_inquiry_metadata.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_compliance_inquiry_metadata)
        """

    def get_report(self, **kwargs: Unpack[GetReportRequestTypeDef]) -> GetReportResponseTypeDef:
        """
        Get the content for a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_report.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_report)
        """

    def get_report_metadata(
        self, **kwargs: Unpack[GetReportMetadataRequestTypeDef]
    ) -> GetReportMetadataResponseTypeDef:
        """
        Get the metadata for a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_report_metadata.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_report_metadata)
        """

    def get_term_for_report(
        self, **kwargs: Unpack[GetTermForReportRequestTypeDef]
    ) -> GetTermForReportResponseTypeDef:
        """
        Get the Term content associated with a single report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_term_for_report.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_term_for_report)
        """

    def list_compliance_inquiries(
        self, **kwargs: Unpack[ListComplianceInquiriesRequestTypeDef]
    ) -> ListComplianceInquiriesResponseTypeDef:
        """
        List available compliance inquiries.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_compliance_inquiries.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#list_compliance_inquiries)
        """

    def list_compliance_inquiry_queries(
        self, **kwargs: Unpack[ListComplianceInquiryQueriesRequestTypeDef]
    ) -> ListComplianceInquiryQueriesResponseTypeDef:
        """
        List queries within a compliance inquiry.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_compliance_inquiry_queries.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#list_compliance_inquiry_queries)
        """

    def list_customer_agreements(
        self, **kwargs: Unpack[ListCustomerAgreementsRequestTypeDef]
    ) -> ListCustomerAgreementsResponseTypeDef:
        """
        List active customer-agreements applicable to calling identity.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_customer_agreements.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#list_customer_agreements)
        """

    def list_report_versions(
        self, **kwargs: Unpack[ListReportVersionsRequestTypeDef]
    ) -> ListReportVersionsResponseTypeDef:
        """
        List available report versions for a given report.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_report_versions.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#list_report_versions)
        """

    def list_reports(
        self, **kwargs: Unpack[ListReportsRequestTypeDef]
    ) -> ListReportsResponseTypeDef:
        """
        List available reports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_reports.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#list_reports)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        List tags for a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/list_tags_for_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#list_tags_for_resource)
        """

    def put_account_settings(
        self, **kwargs: Unpack[PutAccountSettingsRequestTypeDef]
    ) -> PutAccountSettingsResponseTypeDef:
        """
        Put the account settings for Artifact.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/put_account_settings.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#put_account_settings)
        """

    def put_compliance_inquiry_feedback(
        self, **kwargs: Unpack[PutComplianceInquiryFeedbackRequestTypeDef]
    ) -> PutComplianceInquiryFeedbackResponseTypeDef:
        """
        Submits feedback on a compliance inquiry response.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/put_compliance_inquiry_feedback.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#put_compliance_inquiry_feedback)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Add tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/tag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#tag_resource)
        """

    def untag_resource(self, **kwargs: Unpack[UntagResourceRequestTypeDef]) -> dict[str, Any]:
        """
        Remove tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/untag_resource.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#untag_resource)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compliance_inquiries"]
    ) -> ListComplianceInquiriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_compliance_inquiry_queries"]
    ) -> ListComplianceInquiryQueriesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_customer_agreements"]
    ) -> ListCustomerAgreementsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_report_versions"]
    ) -> ListReportVersionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_reports"]
    ) -> ListReportsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/artifact/client/get_paginator.html)
        [Show boto3-stubs documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_artifact/client/#get_paginator)
        """
