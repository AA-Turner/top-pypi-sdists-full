"""
Type annotations for acm service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)

Copyright 2026 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_acm.client import ACMClient

    session = get_session()
    async with session.create_client("acm") as client:
        client: ACMClient
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
    ListAcmeAccountsPaginator,
    ListAcmeDomainValidationsPaginator,
    ListAcmeEndpointsPaginator,
    ListAcmeExternalAccountBindingsPaginator,
    ListCertificatesPaginator,
    SearchCertificatesPaginator,
)
from .type_defs import (
    AddTagsToCertificateRequestTypeDef,
    CreateAcmeDomainValidationRequestTypeDef,
    CreateAcmeDomainValidationResponseTypeDef,
    CreateAcmeEndpointRequestTypeDef,
    CreateAcmeEndpointResponseTypeDef,
    CreateAcmeExternalAccountBindingRequestTypeDef,
    CreateAcmeExternalAccountBindingResponseTypeDef,
    DeleteAcmeDomainValidationRequestTypeDef,
    DeleteAcmeEndpointRequestTypeDef,
    DeleteAcmeExternalAccountBindingRequestTypeDef,
    DeleteCertificateRequestTypeDef,
    DescribeAcmeAccountRequestTypeDef,
    DescribeAcmeAccountResponseTypeDef,
    DescribeAcmeDomainValidationRequestTypeDef,
    DescribeAcmeDomainValidationResponseTypeDef,
    DescribeAcmeEndpointRequestTypeDef,
    DescribeAcmeEndpointResponseTypeDef,
    DescribeAcmeExternalAccountBindingRequestTypeDef,
    DescribeAcmeExternalAccountBindingResponseTypeDef,
    DescribeCertificateRequestTypeDef,
    DescribeCertificateResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportCertificateRequestTypeDef,
    ExportCertificateResponseTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetAcmeExternalAccountBindingCredentialsRequestTypeDef,
    GetAcmeExternalAccountBindingCredentialsResponseTypeDef,
    GetCertificateRequestTypeDef,
    GetCertificateResponseTypeDef,
    ImportCertificateRequestTypeDef,
    ImportCertificateResponseTypeDef,
    ListAcmeAccountsRequestTypeDef,
    ListAcmeAccountsResponseTypeDef,
    ListAcmeDomainValidationsRequestTypeDef,
    ListAcmeDomainValidationsResponseTypeDef,
    ListAcmeEndpointsRequestTypeDef,
    ListAcmeEndpointsResponseTypeDef,
    ListAcmeExternalAccountBindingsRequestTypeDef,
    ListAcmeExternalAccountBindingsResponseTypeDef,
    ListCertificatesRequestTypeDef,
    ListCertificatesResponseTypeDef,
    ListTagsForCertificateRequestTypeDef,
    ListTagsForCertificateResponseTypeDef,
    ListTagsForResourceRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PutAccountConfigurationRequestTypeDef,
    RemoveTagsFromCertificateRequestTypeDef,
    RenewCertificateRequestTypeDef,
    RequestCertificateRequestTypeDef,
    RequestCertificateResponseTypeDef,
    ResendValidationEmailRequestTypeDef,
    RevokeAcmeAccountRequestTypeDef,
    RevokeAcmeExternalAccountBindingRequestTypeDef,
    RevokeCertificateRequestTypeDef,
    RevokeCertificateResponseTypeDef,
    SearchCertificatesRequestTypeDef,
    SearchCertificatesResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAcmeDomainValidationRequestTypeDef,
    UpdateAcmeEndpointRequestTypeDef,
    UpdateCertificateOptionsRequestTypeDef,
)
from .waiter import (
    AcmeDomainValidationDeletedWaiter,
    AcmeDomainValidationValidatedWaiter,
    AcmeEndpointActiveWaiter,
    AcmeEndpointDeletedWaiter,
    CertificateValidatedWaiter,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("ACMClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: type[BotocoreClientError]
    ClientError: type[BotocoreClientError]
    ConflictException: type[BotocoreClientError]
    InternalServerException: type[BotocoreClientError]
    InvalidArgsException: type[BotocoreClientError]
    InvalidArnException: type[BotocoreClientError]
    InvalidDomainValidationOptionsException: type[BotocoreClientError]
    InvalidParameterException: type[BotocoreClientError]
    InvalidStateException: type[BotocoreClientError]
    InvalidTagException: type[BotocoreClientError]
    LimitExceededException: type[BotocoreClientError]
    RequestInProgressException: type[BotocoreClientError]
    ResourceInUseException: type[BotocoreClientError]
    ResourceNotFoundException: type[BotocoreClientError]
    ServiceQuotaExceededException: type[BotocoreClientError]
    TagPolicyException: type[BotocoreClientError]
    ThrottlingException: type[BotocoreClientError]
    TooManyTagsException: type[BotocoreClientError]
    ValidationException: type[BotocoreClientError]

class ACMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ACMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#generate_presigned_url)
        """

    async def add_tags_to_certificate(
        self, **kwargs: Unpack[AddTagsToCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/add_tags_to_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#add_tags_to_certificate)
        """

    async def create_acme_domain_validation(
        self, **kwargs: Unpack[CreateAcmeDomainValidationRequestTypeDef]
    ) -> CreateAcmeDomainValidationResponseTypeDef:
        """
        Creates a domain validation for an ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/create_acme_domain_validation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#create_acme_domain_validation)
        """

    async def create_acme_endpoint(
        self, **kwargs: Unpack[CreateAcmeEndpointRequestTypeDef]
    ) -> CreateAcmeEndpointResponseTypeDef:
        """
        Creates an ACME endpoint, which is a managed ACME server with a unique endpoint
        URL.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/create_acme_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#create_acme_endpoint)
        """

    async def create_acme_external_account_binding(
        self, **kwargs: Unpack[CreateAcmeExternalAccountBindingRequestTypeDef]
    ) -> CreateAcmeExternalAccountBindingResponseTypeDef:
        """
        Creates an external account binding (EAB) for an ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/create_acme_external_account_binding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#create_acme_external_account_binding)
        """

    async def delete_acme_domain_validation(
        self, **kwargs: Unpack[DeleteAcmeDomainValidationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a domain validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/delete_acme_domain_validation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#delete_acme_domain_validation)
        """

    async def delete_acme_endpoint(
        self, **kwargs: Unpack[DeleteAcmeEndpointRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/delete_acme_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#delete_acme_endpoint)
        """

    async def delete_acme_external_account_binding(
        self, **kwargs: Unpack[DeleteAcmeExternalAccountBindingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an external account binding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/delete_acme_external_account_binding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#delete_acme_external_account_binding)
        """

    async def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a certificate and its associated private key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/delete_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#delete_certificate)
        """

    async def describe_acme_account(
        self, **kwargs: Unpack[DescribeAcmeAccountRequestTypeDef]
    ) -> DescribeAcmeAccountResponseTypeDef:
        """
        Returns detailed metadata about the specified ACME account, including its
        status, public key thumbprint, and associated external account binding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_acme_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_acme_account)
        """

    async def describe_acme_domain_validation(
        self, **kwargs: Unpack[DescribeAcmeDomainValidationRequestTypeDef]
    ) -> DescribeAcmeDomainValidationResponseTypeDef:
        """
        Returns detailed metadata about the specified domain validation, including its
        status, domain scope, and DNS resource records required for validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_acme_domain_validation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_acme_domain_validation)
        """

    async def describe_acme_endpoint(
        self, **kwargs: Unpack[DescribeAcmeEndpointRequestTypeDef]
    ) -> DescribeAcmeEndpointResponseTypeDef:
        """
        Returns detailed metadata about the specified ACME endpoint, including its
        status, URL, authorization behavior, and certificate authority configuration.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_acme_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_acme_endpoint)
        """

    async def describe_acme_external_account_binding(
        self, **kwargs: Unpack[DescribeAcmeExternalAccountBindingRequestTypeDef]
    ) -> DescribeAcmeExternalAccountBindingResponseTypeDef:
        """
        Returns detailed metadata about the specified external account binding,
        including the associated IAM role, expiration time, and usage history.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_acme_external_account_binding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_acme_external_account_binding)
        """

    async def describe_certificate(
        self, **kwargs: Unpack[DescribeCertificateRequestTypeDef]
    ) -> DescribeCertificateResponseTypeDef:
        """
        Returns detailed metadata about the specified ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_certificate)
        """

    async def export_certificate(
        self, **kwargs: Unpack[ExportCertificateRequestTypeDef]
    ) -> ExportCertificateResponseTypeDef:
        """
        Exports a private certificate issued by a private certificate authority (CA) or
        a public certificate for use anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/export_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#export_certificate)
        """

    async def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        Returns the account configuration options associated with an Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_account_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_account_configuration)
        """

    async def get_acme_external_account_binding_credentials(
        self, **kwargs: Unpack[GetAcmeExternalAccountBindingCredentialsRequestTypeDef]
    ) -> GetAcmeExternalAccountBindingCredentialsResponseTypeDef:
        """
        Retrieves the key ID and MAC key credentials for an external account binding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_acme_external_account_binding_credentials.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_acme_external_account_binding_credentials)
        """

    async def get_certificate(
        self, **kwargs: Unpack[GetCertificateRequestTypeDef]
    ) -> GetCertificateResponseTypeDef:
        """
        Retrieves a certificate and its certificate chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_certificate)
        """

    async def import_certificate(
        self, **kwargs: Unpack[ImportCertificateRequestTypeDef]
    ) -> ImportCertificateResponseTypeDef:
        """
        Imports a certificate into Certificate Manager (ACM) to use with services that
        are integrated with ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/import_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#import_certificate)
        """

    async def list_acme_accounts(
        self, **kwargs: Unpack[ListAcmeAccountsRequestTypeDef]
    ) -> ListAcmeAccountsResponseTypeDef:
        """
        Retrieves a list of ACME accounts registered with the specified ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_acme_accounts.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_acme_accounts)
        """

    async def list_acme_domain_validations(
        self, **kwargs: Unpack[ListAcmeDomainValidationsRequestTypeDef]
    ) -> ListAcmeDomainValidationsResponseTypeDef:
        """
        Retrieves a list of domain validations for the specified ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_acme_domain_validations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_acme_domain_validations)
        """

    async def list_acme_endpoints(
        self, **kwargs: Unpack[ListAcmeEndpointsRequestTypeDef]
    ) -> ListAcmeEndpointsResponseTypeDef:
        """
        Retrieves a list of ACME endpoints in your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_acme_endpoints.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_acme_endpoints)
        """

    async def list_acme_external_account_bindings(
        self, **kwargs: Unpack[ListAcmeExternalAccountBindingsRequestTypeDef]
    ) -> ListAcmeExternalAccountBindingsResponseTypeDef:
        """
        Retrieves a list of external account bindings for the specified ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_acme_external_account_bindings.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_acme_external_account_bindings)
        """

    async def list_certificates(
        self, **kwargs: Unpack[ListCertificatesRequestTypeDef]
    ) -> ListCertificatesResponseTypeDef:
        """
        Retrieves a list of certificate ARNs and domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_certificates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_certificates)
        """

    async def list_tags_for_certificate(
        self, **kwargs: Unpack[ListTagsForCertificateRequestTypeDef]
    ) -> ListTagsForCertificateResponseTypeDef:
        """
        Lists the tags that have been applied to the ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_tags_for_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_tags_for_certificate)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags associated with an ACM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_tags_for_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_tags_for_resource)
        """

    async def put_account_configuration(
        self, **kwargs: Unpack[PutAccountConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or modifies account-level configurations in ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/put_account_configuration.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#put_account_configuration)
        """

    async def remove_tags_from_certificate(
        self, **kwargs: Unpack[RemoveTagsFromCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove one or more tags from an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/remove_tags_from_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#remove_tags_from_certificate)
        """

    async def renew_certificate(
        self, **kwargs: Unpack[RenewCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renews an <a
        href="https://docs.aws.amazon.com/acm/latest/userguide/managed-renewal.html">eligible
        ACM certificate</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/renew_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#renew_certificate)
        """

    async def request_certificate(
        self, **kwargs: Unpack[RequestCertificateRequestTypeDef]
    ) -> RequestCertificateResponseTypeDef:
        """
        Requests an ACM certificate for use with other Amazon Web Services services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/request_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#request_certificate)
        """

    async def resend_validation_email(
        self, **kwargs: Unpack[ResendValidationEmailRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resends the email that requests domain ownership validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/resend_validation_email.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#resend_validation_email)
        """

    async def revoke_acme_account(
        self, **kwargs: Unpack[RevokeAcmeAccountRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes an ACME account, preventing it from requesting or revoking certificates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/revoke_acme_account.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#revoke_acme_account)
        """

    async def revoke_acme_external_account_binding(
        self, **kwargs: Unpack[RevokeAcmeExternalAccountBindingRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Revokes an external account binding, preventing new ACME accounts from being
        registered using this binding.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/revoke_acme_external_account_binding.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#revoke_acme_external_account_binding)
        """

    async def revoke_certificate(
        self, **kwargs: Unpack[RevokeCertificateRequestTypeDef]
    ) -> RevokeCertificateResponseTypeDef:
        """
        Revokes a public ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/revoke_certificate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#revoke_certificate)
        """

    async def search_certificates(
        self, **kwargs: Unpack[SearchCertificatesRequestTypeDef]
    ) -> SearchCertificatesResponseTypeDef:
        """
        Retrieves a list of certificates matching search criteria.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/search_certificates.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#search_certificates)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an ACM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes one or more tags from an ACM resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#untag_resource)
        """

    async def update_acme_domain_validation(
        self, **kwargs: Unpack[UpdateAcmeDomainValidationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the prevalidation configuration of an existing domain validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/update_acme_domain_validation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#update_acme_domain_validation)
        """

    async def update_acme_endpoint(
        self, **kwargs: Unpack[UpdateAcmeEndpointRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the configuration of an existing ACME endpoint.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/update_acme_endpoint.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#update_acme_endpoint)
        """

    async def update_certificate_options(
        self, **kwargs: Unpack[UpdateCertificateOptionsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/update_certificate_options.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#update_certificate_options)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_acme_accounts"]
    ) -> ListAcmeAccountsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_acme_domain_validations"]
    ) -> ListAcmeDomainValidationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_acme_endpoints"]
    ) -> ListAcmeEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_acme_external_account_bindings"]
    ) -> ListAcmeExternalAccountBindingsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["search_certificates"]
    ) -> SearchCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["acme_domain_validation_deleted"]
    ) -> AcmeDomainValidationDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["acme_domain_validation_validated"]
    ) -> AcmeDomainValidationValidatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["acme_endpoint_active"]
    ) -> AcmeEndpointActiveWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["acme_endpoint_deleted"]
    ) -> AcmeEndpointDeletedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """

    @overload  # type: ignore[override]
    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["certificate_validated"]
    ) -> CertificateValidatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
        """

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
        """
