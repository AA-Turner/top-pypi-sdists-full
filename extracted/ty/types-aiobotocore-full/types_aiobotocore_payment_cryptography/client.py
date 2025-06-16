"""
Type annotations for payment-cryptography service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_payment_cryptography.client import PaymentCryptographyControlPlaneClient

    session = get_session()
    async with session.create_client("payment-cryptography") as client:
        client: PaymentCryptographyControlPlaneClient
    ```
"""

from __future__ import annotations

import sys
from types import TracebackType
from typing import Any, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListAliasesPaginator, ListKeysPaginator, ListTagsForResourcePaginator
from .type_defs import (
    CreateAliasInputTypeDef,
    CreateAliasOutputTypeDef,
    CreateKeyInputTypeDef,
    CreateKeyOutputTypeDef,
    DeleteAliasInputTypeDef,
    DeleteKeyInputTypeDef,
    DeleteKeyOutputTypeDef,
    ExportKeyInputTypeDef,
    ExportKeyOutputTypeDef,
    GetAliasInputTypeDef,
    GetAliasOutputTypeDef,
    GetKeyInputTypeDef,
    GetKeyOutputTypeDef,
    GetParametersForExportInputTypeDef,
    GetParametersForExportOutputTypeDef,
    GetParametersForImportInputTypeDef,
    GetParametersForImportOutputTypeDef,
    GetPublicKeyCertificateInputTypeDef,
    GetPublicKeyCertificateOutputTypeDef,
    ImportKeyInputTypeDef,
    ImportKeyOutputTypeDef,
    ListAliasesInputTypeDef,
    ListAliasesOutputTypeDef,
    ListKeysInputTypeDef,
    ListKeysOutputTypeDef,
    ListTagsForResourceInputTypeDef,
    ListTagsForResourceOutputTypeDef,
    RestoreKeyInputTypeDef,
    RestoreKeyOutputTypeDef,
    StartKeyUsageInputTypeDef,
    StartKeyUsageOutputTypeDef,
    StopKeyUsageInputTypeDef,
    StopKeyUsageOutputTypeDef,
    TagResourceInputTypeDef,
    UntagResourceInputTypeDef,
    UpdateAliasInputTypeDef,
    UpdateAliasOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Self, Unpack
else:
    from typing_extensions import Literal, Self, Unpack


__all__ = ("PaymentCryptographyControlPlaneClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ServiceUnavailableException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class PaymentCryptographyControlPlaneClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PaymentCryptographyControlPlaneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#generate_presigned_url)
        """

    async def create_alias(
        self, **kwargs: Unpack[CreateAliasInputTypeDef]
    ) -> CreateAliasOutputTypeDef:
        """
        Creates an <i>alias</i>, or a friendly name, for an Amazon Web Services Payment
        Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/create_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#create_alias)
        """

    async def create_key(self, **kwargs: Unpack[CreateKeyInputTypeDef]) -> CreateKeyOutputTypeDef:
        """
        Creates an Amazon Web Services Payment Cryptography key, a logical
        representation of a cryptographic key, that is unique in your account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/create_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#create_key)
        """

    async def delete_alias(self, **kwargs: Unpack[DeleteAliasInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes the alias, but doesn't affect the underlying key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/delete_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#delete_alias)
        """

    async def delete_key(self, **kwargs: Unpack[DeleteKeyInputTypeDef]) -> DeleteKeyOutputTypeDef:
        """
        Deletes the key material and metadata associated with Amazon Web Services
        Payment Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/delete_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#delete_key)
        """

    async def export_key(self, **kwargs: Unpack[ExportKeyInputTypeDef]) -> ExportKeyOutputTypeDef:
        """
        Exports a key from Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/export_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#export_key)
        """

    async def get_alias(self, **kwargs: Unpack[GetAliasInputTypeDef]) -> GetAliasOutputTypeDef:
        """
        Gets the Amazon Web Services Payment Cryptography key associated with the alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_alias)
        """

    async def get_key(self, **kwargs: Unpack[GetKeyInputTypeDef]) -> GetKeyOutputTypeDef:
        """
        Gets the key material for an Amazon Web Services Payment Cryptography key,
        including the immutable and mutable data specified when the key was created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_key)
        """

    async def get_parameters_for_export(
        self, **kwargs: Unpack[GetParametersForExportInputTypeDef]
    ) -> GetParametersForExportOutputTypeDef:
        """
        Gets the export token and the signing key certificate to initiate a TR-34 key
        export from Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_parameters_for_export.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_parameters_for_export)
        """

    async def get_parameters_for_import(
        self, **kwargs: Unpack[GetParametersForImportInputTypeDef]
    ) -> GetParametersForImportOutputTypeDef:
        """
        Gets the import token and the wrapping key certificate in PEM format (base64
        encoded) to initiate a TR-34 WrappedKeyBlock or a RSA WrappedKeyCryptogram
        import into Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_parameters_for_import.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_parameters_for_import)
        """

    async def get_public_key_certificate(
        self, **kwargs: Unpack[GetPublicKeyCertificateInputTypeDef]
    ) -> GetPublicKeyCertificateOutputTypeDef:
        """
        Gets the public key certificate of the asymmetric key pair that exists within
        Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_public_key_certificate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_public_key_certificate)
        """

    async def import_key(self, **kwargs: Unpack[ImportKeyInputTypeDef]) -> ImportKeyOutputTypeDef:
        """
        Imports symmetric keys and public key certificates in PEM format (base64
        encoded) into Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/import_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#import_key)
        """

    async def list_aliases(
        self, **kwargs: Unpack[ListAliasesInputTypeDef]
    ) -> ListAliasesOutputTypeDef:
        """
        Lists the aliases for all keys in the caller's Amazon Web Services account and
        Amazon Web Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/list_aliases.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#list_aliases)
        """

    async def list_keys(self, **kwargs: Unpack[ListKeysInputTypeDef]) -> ListKeysOutputTypeDef:
        """
        Lists the keys in the caller's Amazon Web Services account and Amazon Web
        Services Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/list_keys.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#list_keys)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags for an Amazon Web Services resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/list_tags_for_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#list_tags_for_resource)
        """

    async def restore_key(
        self, **kwargs: Unpack[RestoreKeyInputTypeDef]
    ) -> RestoreKeyOutputTypeDef:
        """
        Cancels a scheduled key deletion during the waiting period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/restore_key.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#restore_key)
        """

    async def start_key_usage(
        self, **kwargs: Unpack[StartKeyUsageInputTypeDef]
    ) -> StartKeyUsageOutputTypeDef:
        """
        Enables an Amazon Web Services Payment Cryptography key, which makes it active
        for cryptographic operations within Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/start_key_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#start_key_usage)
        """

    async def stop_key_usage(
        self, **kwargs: Unpack[StopKeyUsageInputTypeDef]
    ) -> StopKeyUsageOutputTypeDef:
        """
        Disables an Amazon Web Services Payment Cryptography key, which makes it
        inactive within Amazon Web Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/stop_key_usage.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#stop_key_usage)
        """

    async def tag_resource(self, **kwargs: Unpack[TagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Adds or edits tags on an Amazon Web Services Payment Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/tag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#tag_resource)
        """

    async def untag_resource(self, **kwargs: Unpack[UntagResourceInputTypeDef]) -> Dict[str, Any]:
        """
        Deletes a tag from an Amazon Web Services Payment Cryptography key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/untag_resource.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#untag_resource)
        """

    async def update_alias(
        self, **kwargs: Unpack[UpdateAliasInputTypeDef]
    ) -> UpdateAliasOutputTypeDef:
        """
        Associates an existing Amazon Web Services Payment Cryptography alias with a
        different key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/update_alias.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#update_alias)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_aliases"]
    ) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_keys"]
    ) -> ListKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tags_for_resource"]
    ) -> ListTagsForResourcePaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography/client/get_paginator.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography.html#PaymentCryptographyControlPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/client/)
        """
