"""
Type annotations for payment-cryptography-data service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_payment_cryptography_data.client import PaymentCryptographyDataPlaneClient

    session = get_session()
    async with session.create_client("payment-cryptography-data") as client:
        client: PaymentCryptographyDataPlaneClient
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
    DecryptDataInputTypeDef,
    DecryptDataOutputTypeDef,
    EncryptDataInputTypeDef,
    EncryptDataOutputTypeDef,
    GenerateCardValidationDataInputTypeDef,
    GenerateCardValidationDataOutputTypeDef,
    GenerateMacEmvPinChangeInputTypeDef,
    GenerateMacEmvPinChangeOutputTypeDef,
    GenerateMacInputTypeDef,
    GenerateMacOutputTypeDef,
    GeneratePinDataInputTypeDef,
    GeneratePinDataOutputTypeDef,
    ReEncryptDataInputTypeDef,
    ReEncryptDataOutputTypeDef,
    TranslatePinDataInputTypeDef,
    TranslatePinDataOutputTypeDef,
    VerifyAuthRequestCryptogramInputTypeDef,
    VerifyAuthRequestCryptogramOutputTypeDef,
    VerifyCardValidationDataInputTypeDef,
    VerifyCardValidationDataOutputTypeDef,
    VerifyMacInputTypeDef,
    VerifyMacOutputTypeDef,
    VerifyPinDataInputTypeDef,
    VerifyPinDataOutputTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Self, Unpack
else:
    from typing_extensions import Self, Unpack


__all__ = ("PaymentCryptographyDataPlaneClient",)


class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]
    VerificationFailedException: Type[BotocoreClientError]


class PaymentCryptographyDataPlaneClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data.html#PaymentCryptographyDataPlane.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        PaymentCryptographyDataPlaneClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data.html#PaymentCryptographyDataPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/can_paginate.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/generate_presigned_url.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#generate_presigned_url)
        """

    async def decrypt_data(
        self, **kwargs: Unpack[DecryptDataInputTypeDef]
    ) -> DecryptDataOutputTypeDef:
        """
        Decrypts ciphertext data to plaintext using a symmetric (TDES, AES), asymmetric
        (RSA), or derived (DUKPT or EMV) encryption key scheme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/decrypt_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#decrypt_data)
        """

    async def encrypt_data(
        self, **kwargs: Unpack[EncryptDataInputTypeDef]
    ) -> EncryptDataOutputTypeDef:
        """
        Encrypts plaintext data to ciphertext using a symmetric (TDES, AES), asymmetric
        (RSA), or derived (DUKPT or EMV) encryption key scheme.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/encrypt_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#encrypt_data)
        """

    async def generate_card_validation_data(
        self, **kwargs: Unpack[GenerateCardValidationDataInputTypeDef]
    ) -> GenerateCardValidationDataOutputTypeDef:
        """
        Generates card-related validation data using algorithms such as Card
        Verification Values (CVV/CVV2), Dynamic Card Verification Values (dCVV/dCVV2),
        or Card Security Codes (CSC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/generate_card_validation_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#generate_card_validation_data)
        """

    async def generate_mac(
        self, **kwargs: Unpack[GenerateMacInputTypeDef]
    ) -> GenerateMacOutputTypeDef:
        """
        Generates a Message Authentication Code (MAC) cryptogram within Amazon Web
        Services Payment Cryptography.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/generate_mac.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#generate_mac)
        """

    async def generate_mac_emv_pin_change(
        self, **kwargs: Unpack[GenerateMacEmvPinChangeInputTypeDef]
    ) -> GenerateMacEmvPinChangeOutputTypeDef:
        """
        Generates an issuer script mac for EMV payment cards that use offline PINs as
        the cardholder verification method (CVM).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/generate_mac_emv_pin_change.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#generate_mac_emv_pin_change)
        """

    async def generate_pin_data(
        self, **kwargs: Unpack[GeneratePinDataInputTypeDef]
    ) -> GeneratePinDataOutputTypeDef:
        """
        Generates pin-related data such as PIN, PIN Verification Value (PVV), PIN
        Block, and PIN Offset during new card issuance or reissuance.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/generate_pin_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#generate_pin_data)
        """

    async def re_encrypt_data(
        self, **kwargs: Unpack[ReEncryptDataInputTypeDef]
    ) -> ReEncryptDataOutputTypeDef:
        """
        Re-encrypt ciphertext using DUKPT or Symmetric data encryption keys.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/re_encrypt_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#re_encrypt_data)
        """

    async def translate_pin_data(
        self, **kwargs: Unpack[TranslatePinDataInputTypeDef]
    ) -> TranslatePinDataOutputTypeDef:
        """
        Translates encrypted PIN block from and to ISO 9564 formats 0,1,3,4.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/translate_pin_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#translate_pin_data)
        """

    async def verify_auth_request_cryptogram(
        self, **kwargs: Unpack[VerifyAuthRequestCryptogramInputTypeDef]
    ) -> VerifyAuthRequestCryptogramOutputTypeDef:
        """
        Verifies Authorization Request Cryptogram (ARQC) for a EMV chip payment card
        authorization.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/verify_auth_request_cryptogram.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#verify_auth_request_cryptogram)
        """

    async def verify_card_validation_data(
        self, **kwargs: Unpack[VerifyCardValidationDataInputTypeDef]
    ) -> VerifyCardValidationDataOutputTypeDef:
        """
        Verifies card-related validation data using algorithms such as Card
        Verification Values (CVV/CVV2), Dynamic Card Verification Values (dCVV/dCVV2)
        and Card Security Codes (CSC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/verify_card_validation_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#verify_card_validation_data)
        """

    async def verify_mac(self, **kwargs: Unpack[VerifyMacInputTypeDef]) -> VerifyMacOutputTypeDef:
        """
        Verifies a Message Authentication Code (MAC).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/verify_mac.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#verify_mac)
        """

    async def verify_pin_data(
        self, **kwargs: Unpack[VerifyPinDataInputTypeDef]
    ) -> VerifyPinDataOutputTypeDef:
        """
        Verifies pin-related data such as PIN and PIN Offset using algorithms including
        VISA PVV and IBM3624.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data/client/verify_pin_data.html)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/#verify_pin_data)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data.html#PaymentCryptographyDataPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/payment-cryptography-data.html#PaymentCryptographyDataPlane.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography_data/client/)
        """
