"""
Type annotations for acm service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)

Copyright 2025 Vlad Emelianov

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
from types import TracebackType
from typing import Any

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListCertificatesPaginator
from .type_defs import (
    AddTagsToCertificateRequestTypeDef,
    DeleteCertificateRequestTypeDef,
    DescribeCertificateRequestTypeDef,
    DescribeCertificateResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    ExportCertificateRequestTypeDef,
    ExportCertificateResponseTypeDef,
    GetAccountConfigurationResponseTypeDef,
    GetCertificateRequestTypeDef,
    GetCertificateResponseTypeDef,
    ImportCertificateRequestTypeDef,
    ImportCertificateResponseTypeDef,
    ListCertificatesRequestTypeDef,
    ListCertificatesResponseTypeDef,
    ListTagsForCertificateRequestTypeDef,
    ListTagsForCertificateResponseTypeDef,
    PutAccountConfigurationRequestTypeDef,
    RemoveTagsFromCertificateRequestTypeDef,
    RenewCertificateRequestTypeDef,
    RequestCertificateRequestTypeDef,
    RequestCertificateResponseTypeDef,
    ResendValidationEmailRequestTypeDef,
    RevokeCertificateRequestTypeDef,
    RevokeCertificateResponseTypeDef,
    UpdateCertificateOptionsRequestTypeDef,
)
from .waiter import CertificateValidatedWaiter

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack

__all__ = ("ACMClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InvalidArgsException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidDomainValidationOptionsException: Type[BotocoreClientError]
    InvalidParameterException: Type[BotocoreClientError]
    InvalidStateException: Type[BotocoreClientError]
    InvalidTagException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    RequestInProgressException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    TagPolicyException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    TooManyTagsException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class ACMClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        ACMClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#can_paginate)
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
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#generate_presigned_url)
        """

    async def add_tags_to_certificate(
        self, **kwargs: Unpack[AddTagsToCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds one or more tags to an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/add_tags_to_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#add_tags_to_certificate)
        """

    async def delete_certificate(
        self, **kwargs: Unpack[DeleteCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a certificate and its associated private key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/delete_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#delete_certificate)
        """

    async def describe_certificate(
        self, **kwargs: Unpack[DescribeCertificateRequestTypeDef]
    ) -> DescribeCertificateResponseTypeDef:
        """
        Returns detailed metadata about the specified ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/describe_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#describe_certificate)
        """

    async def export_certificate(
        self, **kwargs: Unpack[ExportCertificateRequestTypeDef]
    ) -> ExportCertificateResponseTypeDef:
        """
        Exports a private certificate issued by a private certificate authority (CA) or
        public certificate for use anywhere.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/export_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#export_certificate)
        """

    async def get_account_configuration(self) -> GetAccountConfigurationResponseTypeDef:
        """
        Returns the account configuration options associated with an Amazon Web
        Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_account_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_account_configuration)
        """

    async def get_certificate(
        self, **kwargs: Unpack[GetCertificateRequestTypeDef]
    ) -> GetCertificateResponseTypeDef:
        """
        Retrieves a certificate and its certificate chain.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_certificate)
        """

    async def import_certificate(
        self, **kwargs: Unpack[ImportCertificateRequestTypeDef]
    ) -> ImportCertificateResponseTypeDef:
        """
        Imports a certificate into Certificate Manager (ACM) to use with services that
        are integrated with ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/import_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#import_certificate)
        """

    async def list_certificates(
        self, **kwargs: Unpack[ListCertificatesRequestTypeDef]
    ) -> ListCertificatesResponseTypeDef:
        """
        Retrieves a list of certificate ARNs and domain names.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_certificates.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_certificates)
        """

    async def list_tags_for_certificate(
        self, **kwargs: Unpack[ListTagsForCertificateRequestTypeDef]
    ) -> ListTagsForCertificateResponseTypeDef:
        """
        Lists the tags that have been applied to the ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/list_tags_for_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#list_tags_for_certificate)
        """

    async def put_account_configuration(
        self, **kwargs: Unpack[PutAccountConfigurationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or modifies account-level configurations in ACM.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/put_account_configuration.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#put_account_configuration)
        """

    async def remove_tags_from_certificate(
        self, **kwargs: Unpack[RemoveTagsFromCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Remove one or more tags from an ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/remove_tags_from_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#remove_tags_from_certificate)
        """

    async def renew_certificate(
        self, **kwargs: Unpack[RenewCertificateRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renews an <a
        href="https://docs.aws.amazon.com/acm/latest/userguide/managed-renewal.html">eligible
        ACM certificate</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/renew_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#renew_certificate)
        """

    async def request_certificate(
        self, **kwargs: Unpack[RequestCertificateRequestTypeDef]
    ) -> RequestCertificateResponseTypeDef:
        """
        Requests an ACM certificate for use with other Amazon Web Services services.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/request_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#request_certificate)
        """

    async def resend_validation_email(
        self, **kwargs: Unpack[ResendValidationEmailRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Resends the email that requests domain ownership validation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/resend_validation_email.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#resend_validation_email)
        """

    async def revoke_certificate(
        self, **kwargs: Unpack[RevokeCertificateRequestTypeDef]
    ) -> RevokeCertificateResponseTypeDef:
        """
        Revokes a public ACM certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/revoke_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#revoke_certificate)
        """

    async def update_certificate_options(
        self, **kwargs: Unpack[UpdateCertificateOptionsRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a certificate.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/update_certificate_options.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#update_certificate_options)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_certificates"]
    ) -> ListCertificatesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_paginator)
        """

    def get_waiter(  # type: ignore[override]
        self, waiter_name: Literal["certificate_validated"]
    ) -> CertificateValidatedWaiter:
        """
        Returns an object that can wait for some condition.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm/client/get_waiter.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/#get_waiter)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/acm.html#ACM.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_acm/client/)
        """
