"""
Type annotations for kms service Client.

[Documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kms.client import KMSClient

    session = get_session()
    async with session.create_client("kms") as client:
        client: KMSClient
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

from .paginator import (
    DescribeCustomKeyStoresPaginator,
    ListAliasesPaginator,
    ListGrantsPaginator,
    ListKeyPoliciesPaginator,
    ListKeyRotationsPaginator,
    ListKeysPaginator,
    ListResourceTagsPaginator,
    ListRetirableGrantsPaginator,
)
from .type_defs import (
    CancelKeyDeletionRequestTypeDef,
    CancelKeyDeletionResponseTypeDef,
    ConnectCustomKeyStoreRequestTypeDef,
    CreateAliasRequestTypeDef,
    CreateCustomKeyStoreRequestTypeDef,
    CreateCustomKeyStoreResponseTypeDef,
    CreateGrantRequestTypeDef,
    CreateGrantResponseTypeDef,
    CreateKeyRequestTypeDef,
    CreateKeyResponseTypeDef,
    DecryptRequestTypeDef,
    DecryptResponseTypeDef,
    DeleteAliasRequestTypeDef,
    DeleteCustomKeyStoreRequestTypeDef,
    DeleteImportedKeyMaterialRequestTypeDef,
    DeleteImportedKeyMaterialResponseTypeDef,
    DeriveSharedSecretRequestTypeDef,
    DeriveSharedSecretResponseTypeDef,
    DescribeCustomKeyStoresRequestTypeDef,
    DescribeCustomKeyStoresResponseTypeDef,
    DescribeKeyRequestTypeDef,
    DescribeKeyResponseTypeDef,
    DisableKeyRequestTypeDef,
    DisableKeyRotationRequestTypeDef,
    DisconnectCustomKeyStoreRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    EnableKeyRequestTypeDef,
    EnableKeyRotationRequestTypeDef,
    EncryptRequestTypeDef,
    EncryptResponseTypeDef,
    GenerateDataKeyPairRequestTypeDef,
    GenerateDataKeyPairResponseTypeDef,
    GenerateDataKeyPairWithoutPlaintextRequestTypeDef,
    GenerateDataKeyPairWithoutPlaintextResponseTypeDef,
    GenerateDataKeyRequestTypeDef,
    GenerateDataKeyResponseTypeDef,
    GenerateDataKeyWithoutPlaintextRequestTypeDef,
    GenerateDataKeyWithoutPlaintextResponseTypeDef,
    GenerateMacRequestTypeDef,
    GenerateMacResponseTypeDef,
    GenerateRandomRequestTypeDef,
    GenerateRandomResponseTypeDef,
    GetKeyPolicyRequestTypeDef,
    GetKeyPolicyResponseTypeDef,
    GetKeyRotationStatusRequestTypeDef,
    GetKeyRotationStatusResponseTypeDef,
    GetParametersForImportRequestTypeDef,
    GetParametersForImportResponseTypeDef,
    GetPublicKeyRequestTypeDef,
    GetPublicKeyResponseTypeDef,
    ImportKeyMaterialRequestTypeDef,
    ImportKeyMaterialResponseTypeDef,
    ListAliasesRequestTypeDef,
    ListAliasesResponseTypeDef,
    ListGrantsRequestTypeDef,
    ListGrantsResponseTypeDef,
    ListKeyPoliciesRequestTypeDef,
    ListKeyPoliciesResponseTypeDef,
    ListKeyRotationsRequestTypeDef,
    ListKeyRotationsResponseTypeDef,
    ListKeysRequestTypeDef,
    ListKeysResponseTypeDef,
    ListResourceTagsRequestTypeDef,
    ListResourceTagsResponseTypeDef,
    ListRetirableGrantsRequestTypeDef,
    PutKeyPolicyRequestTypeDef,
    ReEncryptRequestTypeDef,
    ReEncryptResponseTypeDef,
    ReplicateKeyRequestTypeDef,
    ReplicateKeyResponseTypeDef,
    RetireGrantRequestTypeDef,
    RevokeGrantRequestTypeDef,
    RotateKeyOnDemandRequestTypeDef,
    RotateKeyOnDemandResponseTypeDef,
    ScheduleKeyDeletionRequestTypeDef,
    ScheduleKeyDeletionResponseTypeDef,
    SignRequestTypeDef,
    SignResponseTypeDef,
    TagResourceRequestTypeDef,
    UntagResourceRequestTypeDef,
    UpdateAliasRequestTypeDef,
    UpdateCustomKeyStoreRequestTypeDef,
    UpdateKeyDescriptionRequestTypeDef,
    UpdatePrimaryRegionRequestTypeDef,
    VerifyMacRequestTypeDef,
    VerifyMacResponseTypeDef,
    VerifyRequestTypeDef,
    VerifyResponseTypeDef,
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

__all__ = ("KMSClient",)

class Exceptions(BaseClientExceptions):
    AlreadyExistsException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    CloudHsmClusterInUseException: Type[BotocoreClientError]
    CloudHsmClusterInvalidConfigurationException: Type[BotocoreClientError]
    CloudHsmClusterNotActiveException: Type[BotocoreClientError]
    CloudHsmClusterNotFoundException: Type[BotocoreClientError]
    CloudHsmClusterNotRelatedException: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    CustomKeyStoreHasCMKsException: Type[BotocoreClientError]
    CustomKeyStoreInvalidStateException: Type[BotocoreClientError]
    CustomKeyStoreNameInUseException: Type[BotocoreClientError]
    CustomKeyStoreNotFoundException: Type[BotocoreClientError]
    DependencyTimeoutException: Type[BotocoreClientError]
    DisabledException: Type[BotocoreClientError]
    DryRunOperationException: Type[BotocoreClientError]
    ExpiredImportTokenException: Type[BotocoreClientError]
    IncorrectKeyException: Type[BotocoreClientError]
    IncorrectKeyMaterialException: Type[BotocoreClientError]
    IncorrectTrustAnchorException: Type[BotocoreClientError]
    InvalidAliasNameException: Type[BotocoreClientError]
    InvalidArnException: Type[BotocoreClientError]
    InvalidCiphertextException: Type[BotocoreClientError]
    InvalidGrantIdException: Type[BotocoreClientError]
    InvalidGrantTokenException: Type[BotocoreClientError]
    InvalidImportTokenException: Type[BotocoreClientError]
    InvalidKeyUsageException: Type[BotocoreClientError]
    InvalidMarkerException: Type[BotocoreClientError]
    KMSInternalException: Type[BotocoreClientError]
    KMSInvalidMacException: Type[BotocoreClientError]
    KMSInvalidSignatureException: Type[BotocoreClientError]
    KMSInvalidStateException: Type[BotocoreClientError]
    KeyUnavailableException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    MalformedPolicyDocumentException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TagException: Type[BotocoreClientError]
    UnsupportedOperationException: Type[BotocoreClientError]
    XksKeyAlreadyInUseException: Type[BotocoreClientError]
    XksKeyInvalidConfigurationException: Type[BotocoreClientError]
    XksKeyNotFoundException: Type[BotocoreClientError]
    XksProxyIncorrectAuthenticationCredentialException: Type[BotocoreClientError]
    XksProxyInvalidConfigurationException: Type[BotocoreClientError]
    XksProxyInvalidResponseException: Type[BotocoreClientError]
    XksProxyUriEndpointInUseException: Type[BotocoreClientError]
    XksProxyUriInUseException: Type[BotocoreClientError]
    XksProxyUriUnreachableException: Type[BotocoreClientError]
    XksProxyVpcEndpointServiceInUseException: Type[BotocoreClientError]
    XksProxyVpcEndpointServiceInvalidConfigurationException: Type[BotocoreClientError]
    XksProxyVpcEndpointServiceNotFoundException: Type[BotocoreClientError]

class KMSClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KMSClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/can_paginate.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#can_paginate)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_presigned_url.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_presigned_url)
        """

    async def cancel_key_deletion(
        self, **kwargs: Unpack[CancelKeyDeletionRequestTypeDef]
    ) -> CancelKeyDeletionResponseTypeDef:
        """
        Cancels the deletion of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/cancel_key_deletion.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#cancel_key_deletion)
        """

    async def connect_custom_key_store(
        self, **kwargs: Unpack[ConnectCustomKeyStoreRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Connects or reconnects a <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html">custom
        key store</a> to its backing key store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/connect_custom_key_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#connect_custom_key_store)
        """

    async def create_alias(
        self, **kwargs: Unpack[CreateAliasRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a friendly name for a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/create_alias.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_alias)
        """

    async def create_custom_key_store(
        self, **kwargs: Unpack[CreateCustomKeyStoreRequestTypeDef]
    ) -> CreateCustomKeyStoreResponseTypeDef:
        """
        Creates a <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html">custom
        key store</a> backed by a key store that you own and manage.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/create_custom_key_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_custom_key_store)
        """

    async def create_grant(
        self, **kwargs: Unpack[CreateGrantRequestTypeDef]
    ) -> CreateGrantResponseTypeDef:
        """
        Adds a grant to a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/create_grant.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_grant)
        """

    async def create_key(
        self, **kwargs: Unpack[CreateKeyRequestTypeDef]
    ) -> CreateKeyResponseTypeDef:
        """
        Creates a unique customer managed <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms-keys">KMS
        key</a> in your Amazon Web Services account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/create_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#create_key)
        """

    async def decrypt(self, **kwargs: Unpack[DecryptRequestTypeDef]) -> DecryptResponseTypeDef:
        """
        Decrypts ciphertext that was encrypted by a KMS key using any of the following
        operations:.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/decrypt.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#decrypt)
        """

    async def delete_alias(
        self, **kwargs: Unpack[DeleteAliasRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified alias.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/delete_alias.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_alias)
        """

    async def delete_custom_key_store(
        self, **kwargs: Unpack[DeleteCustomKeyStoreRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html">custom
        key store</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/delete_custom_key_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_custom_key_store)
        """

    async def delete_imported_key_material(
        self, **kwargs: Unpack[DeleteImportedKeyMaterialRequestTypeDef]
    ) -> DeleteImportedKeyMaterialResponseTypeDef:
        """
        Deletes key material that was previously imported.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/delete_imported_key_material.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#delete_imported_key_material)
        """

    async def derive_shared_secret(
        self, **kwargs: Unpack[DeriveSharedSecretRequestTypeDef]
    ) -> DeriveSharedSecretResponseTypeDef:
        """
        Derives a shared secret using a key agreement algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/derive_shared_secret.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#derive_shared_secret)
        """

    async def describe_custom_key_stores(
        self, **kwargs: Unpack[DescribeCustomKeyStoresRequestTypeDef]
    ) -> DescribeCustomKeyStoresResponseTypeDef:
        """
        Gets information about <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html">custom
        key stores</a> in the account and Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/describe_custom_key_stores.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#describe_custom_key_stores)
        """

    async def describe_key(
        self, **kwargs: Unpack[DescribeKeyRequestTypeDef]
    ) -> DescribeKeyResponseTypeDef:
        """
        Provides detailed information about a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/describe_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#describe_key)
        """

    async def disable_key(
        self, **kwargs: Unpack[DisableKeyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the state of a KMS key to disabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/disable_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disable_key)
        """

    async def disable_key_rotation(
        self, **kwargs: Unpack[DisableKeyRotationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Disables <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-enable-disable.html">automatic
        rotation of the key material</a> of the specified symmetric encryption KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/disable_key_rotation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disable_key_rotation)
        """

    async def disconnect_custom_key_store(
        self, **kwargs: Unpack[DisconnectCustomKeyStoreRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Disconnects the <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html">custom
        key store</a> from its backing key store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/disconnect_custom_key_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#disconnect_custom_key_store)
        """

    async def enable_key(
        self, **kwargs: Unpack[EnableKeyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sets the key state of a KMS key to enabled.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/enable_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#enable_key)
        """

    async def enable_key_rotation(
        self, **kwargs: Unpack[EnableKeyRotationRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-enable-disable.html">automatic
        rotation of the key material</a> of the specified symmetric encryption KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/enable_key_rotation.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#enable_key_rotation)
        """

    async def encrypt(self, **kwargs: Unpack[EncryptRequestTypeDef]) -> EncryptResponseTypeDef:
        """
        Encrypts plaintext of up to 4,096 bytes using a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/encrypt.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#encrypt)
        """

    async def generate_data_key(
        self, **kwargs: Unpack[GenerateDataKeyRequestTypeDef]
    ) -> GenerateDataKeyResponseTypeDef:
        """
        Returns a unique symmetric data key for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_data_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key)
        """

    async def generate_data_key_pair(
        self, **kwargs: Unpack[GenerateDataKeyPairRequestTypeDef]
    ) -> GenerateDataKeyPairResponseTypeDef:
        """
        Returns a unique asymmetric data key pair for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_data_key_pair.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_pair)
        """

    async def generate_data_key_pair_without_plaintext(
        self, **kwargs: Unpack[GenerateDataKeyPairWithoutPlaintextRequestTypeDef]
    ) -> GenerateDataKeyPairWithoutPlaintextResponseTypeDef:
        """
        Returns a unique asymmetric data key pair for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_data_key_pair_without_plaintext.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_pair_without_plaintext)
        """

    async def generate_data_key_without_plaintext(
        self, **kwargs: Unpack[GenerateDataKeyWithoutPlaintextRequestTypeDef]
    ) -> GenerateDataKeyWithoutPlaintextResponseTypeDef:
        """
        Returns a unique symmetric data key for use outside of KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_data_key_without_plaintext.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_data_key_without_plaintext)
        """

    async def generate_mac(
        self, **kwargs: Unpack[GenerateMacRequestTypeDef]
    ) -> GenerateMacResponseTypeDef:
        """
        Generates a hash-based message authentication code (HMAC) for a message using
        an HMAC KMS key and a MAC algorithm that the key supports.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_mac.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_mac)
        """

    async def generate_random(
        self, **kwargs: Unpack[GenerateRandomRequestTypeDef]
    ) -> GenerateRandomResponseTypeDef:
        """
        Returns a random byte string that is cryptographically secure.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/generate_random.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#generate_random)
        """

    async def get_key_policy(
        self, **kwargs: Unpack[GetKeyPolicyRequestTypeDef]
    ) -> GetKeyPolicyResponseTypeDef:
        """
        Gets a key policy attached to the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_key_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_key_policy)
        """

    async def get_key_rotation_status(
        self, **kwargs: Unpack[GetKeyRotationStatusRequestTypeDef]
    ) -> GetKeyRotationStatusResponseTypeDef:
        """
        Provides detailed information about the rotation status for a KMS key,
        including whether <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-enable-disable.html">automatic
        rotation of the key material</a> is enabled for the specified KMS key, the <a
        href="https://docs.aws...

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_key_rotation_status.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_key_rotation_status)
        """

    async def get_parameters_for_import(
        self, **kwargs: Unpack[GetParametersForImportRequestTypeDef]
    ) -> GetParametersForImportResponseTypeDef:
        """
        Returns the public key and an import token you need to import or reimport key
        material for a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_parameters_for_import.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_parameters_for_import)
        """

    async def get_public_key(
        self, **kwargs: Unpack[GetPublicKeyRequestTypeDef]
    ) -> GetPublicKeyResponseTypeDef:
        """
        Returns the public key of an asymmetric KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_public_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_public_key)
        """

    async def import_key_material(
        self, **kwargs: Unpack[ImportKeyMaterialRequestTypeDef]
    ) -> ImportKeyMaterialResponseTypeDef:
        """
        Imports or reimports key material into an existing KMS key that was created
        without key material.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/import_key_material.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#import_key_material)
        """

    async def list_aliases(
        self, **kwargs: Unpack[ListAliasesRequestTypeDef]
    ) -> ListAliasesResponseTypeDef:
        """
        Gets a list of aliases in the caller's Amazon Web Services account and region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_aliases.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_aliases)
        """

    async def list_grants(
        self, **kwargs: Unpack[ListGrantsRequestTypeDef]
    ) -> ListGrantsResponseTypeDef:
        """
        Gets a list of all grants for the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_grants.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_grants)
        """

    async def list_key_policies(
        self, **kwargs: Unpack[ListKeyPoliciesRequestTypeDef]
    ) -> ListKeyPoliciesResponseTypeDef:
        """
        Gets the names of the key policies that are attached to a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_key_policies.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_key_policies)
        """

    async def list_key_rotations(
        self, **kwargs: Unpack[ListKeyRotationsRequestTypeDef]
    ) -> ListKeyRotationsResponseTypeDef:
        """
        Returns information about the key materials associated with the specified KMS
        key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_key_rotations.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_key_rotations)
        """

    async def list_keys(self, **kwargs: Unpack[ListKeysRequestTypeDef]) -> ListKeysResponseTypeDef:
        """
        Gets a list of all KMS keys in the caller's Amazon Web Services account and
        Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_keys.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_keys)
        """

    async def list_resource_tags(
        self, **kwargs: Unpack[ListResourceTagsRequestTypeDef]
    ) -> ListResourceTagsResponseTypeDef:
        """
        Returns all tags on the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_resource_tags.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_resource_tags)
        """

    async def list_retirable_grants(
        self, **kwargs: Unpack[ListRetirableGrantsRequestTypeDef]
    ) -> ListGrantsResponseTypeDef:
        """
        Returns information about all grants in the Amazon Web Services account and
        Region that have the specified retiring principal.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/list_retirable_grants.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#list_retirable_grants)
        """

    async def put_key_policy(
        self, **kwargs: Unpack[PutKeyPolicyRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Attaches a key policy to the specified KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/put_key_policy.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#put_key_policy)
        """

    async def re_encrypt(
        self, **kwargs: Unpack[ReEncryptRequestTypeDef]
    ) -> ReEncryptResponseTypeDef:
        """
        Decrypts ciphertext and then reencrypts it entirely within KMS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/re_encrypt.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#re_encrypt)
        """

    async def replicate_key(
        self, **kwargs: Unpack[ReplicateKeyRequestTypeDef]
    ) -> ReplicateKeyResponseTypeDef:
        """
        Replicates a multi-Region key into the specified Region.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/replicate_key.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#replicate_key)
        """

    async def retire_grant(
        self, **kwargs: Unpack[RetireGrantRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/retire_grant.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#retire_grant)
        """

    async def revoke_grant(
        self, **kwargs: Unpack[RevokeGrantRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes the specified grant.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/revoke_grant.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#revoke_grant)
        """

    async def rotate_key_on_demand(
        self, **kwargs: Unpack[RotateKeyOnDemandRequestTypeDef]
    ) -> RotateKeyOnDemandResponseTypeDef:
        """
        Immediately initiates rotation of the key material of the specified symmetric
        encryption KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/rotate_key_on_demand.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#rotate_key_on_demand)
        """

    async def schedule_key_deletion(
        self, **kwargs: Unpack[ScheduleKeyDeletionRequestTypeDef]
    ) -> ScheduleKeyDeletionResponseTypeDef:
        """
        Schedules the deletion of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/schedule_key_deletion.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#schedule_key_deletion)
        """

    async def sign(self, **kwargs: Unpack[SignRequestTypeDef]) -> SignResponseTypeDef:
        """
        Creates a <a href="https://en.wikipedia.org/wiki/Digital_signature">digital
        signature</a> for a message or message digest by using the private key in an
        asymmetric signing KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/sign.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#sign)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds or edits tags on a <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk">customer
        managed key</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/tag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes tags from a <a
        href="https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#customer-cmk">customer
        managed key</a>.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/untag_resource.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#untag_resource)
        """

    async def update_alias(
        self, **kwargs: Unpack[UpdateAliasRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Associates an existing KMS alias with a different KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/update_alias.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_alias)
        """

    async def update_custom_key_store(
        self, **kwargs: Unpack[UpdateCustomKeyStoreRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Changes the properties of a custom key store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/update_custom_key_store.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_custom_key_store)
        """

    async def update_key_description(
        self, **kwargs: Unpack[UpdateKeyDescriptionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the description of a KMS key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/update_key_description.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_key_description)
        """

    async def update_primary_region(
        self, **kwargs: Unpack[UpdatePrimaryRegionRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Changes the primary key of a multi-Region key.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/update_primary_region.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#update_primary_region)
        """

    async def verify(self, **kwargs: Unpack[VerifyRequestTypeDef]) -> VerifyResponseTypeDef:
        """
        Verifies a digital signature that was generated by the <a>Sign</a> operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/verify.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#verify)
        """

    async def verify_mac(
        self, **kwargs: Unpack[VerifyMacRequestTypeDef]
    ) -> VerifyMacResponseTypeDef:
        """
        Verifies the hash-based message authentication code (HMAC) for a specified
        message, HMAC KMS key, and MAC algorithm.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/verify_mac.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#verify_mac)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["describe_custom_key_stores"]
    ) -> DescribeCustomKeyStoresPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_aliases"]
    ) -> ListAliasesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_grants"]
    ) -> ListGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_key_policies"]
    ) -> ListKeyPoliciesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_key_rotations"]
    ) -> ListKeyRotationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_keys"]
    ) -> ListKeysPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_resource_tags"]
    ) -> ListResourceTagsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_retirable_grants"]
    ) -> ListRetirableGrantsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms/client/get_paginator.html)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/#get_paginator)
        """

    async def __aenter__(self) -> Self:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
        """

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kms.html#KMS.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kms/client/)
        """
