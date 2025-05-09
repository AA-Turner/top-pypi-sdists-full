# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.cloud.kms_v1 import gapic_version as package_version

__version__ = package_version.__version__


from .services.autokey import AutokeyAsyncClient, AutokeyClient
from .services.autokey_admin import AutokeyAdminAsyncClient, AutokeyAdminClient
from .services.ekm_service import EkmServiceAsyncClient, EkmServiceClient
from .services.key_management_service import (
    KeyManagementServiceAsyncClient,
    KeyManagementServiceClient,
)
from .types.autokey import (
    CreateKeyHandleMetadata,
    CreateKeyHandleRequest,
    GetKeyHandleRequest,
    KeyHandle,
    ListKeyHandlesRequest,
    ListKeyHandlesResponse,
)
from .types.autokey_admin import (
    AutokeyConfig,
    GetAutokeyConfigRequest,
    ShowEffectiveAutokeyConfigRequest,
    ShowEffectiveAutokeyConfigResponse,
    UpdateAutokeyConfigRequest,
)
from .types.ekm_service import (
    Certificate,
    CreateEkmConnectionRequest,
    EkmConfig,
    EkmConnection,
    GetEkmConfigRequest,
    GetEkmConnectionRequest,
    ListEkmConnectionsRequest,
    ListEkmConnectionsResponse,
    UpdateEkmConfigRequest,
    UpdateEkmConnectionRequest,
    VerifyConnectivityRequest,
    VerifyConnectivityResponse,
)
from .types.resources import (
    AccessReason,
    ChecksummedData,
    CryptoKey,
    CryptoKeyVersion,
    CryptoKeyVersionTemplate,
    ExternalProtectionLevelOptions,
    ImportJob,
    KeyAccessJustificationsPolicy,
    KeyOperationAttestation,
    KeyRing,
    ProtectionLevel,
    PublicKey,
)
from .types.service import (
    AsymmetricDecryptRequest,
    AsymmetricDecryptResponse,
    AsymmetricSignRequest,
    AsymmetricSignResponse,
    CreateCryptoKeyRequest,
    CreateCryptoKeyVersionRequest,
    CreateImportJobRequest,
    CreateKeyRingRequest,
    DecryptRequest,
    DecryptResponse,
    DestroyCryptoKeyVersionRequest,
    Digest,
    EncryptRequest,
    EncryptResponse,
    GenerateRandomBytesRequest,
    GenerateRandomBytesResponse,
    GetCryptoKeyRequest,
    GetCryptoKeyVersionRequest,
    GetImportJobRequest,
    GetKeyRingRequest,
    GetPublicKeyRequest,
    ImportCryptoKeyVersionRequest,
    ListCryptoKeysRequest,
    ListCryptoKeysResponse,
    ListCryptoKeyVersionsRequest,
    ListCryptoKeyVersionsResponse,
    ListImportJobsRequest,
    ListImportJobsResponse,
    ListKeyRingsRequest,
    ListKeyRingsResponse,
    LocationMetadata,
    MacSignRequest,
    MacSignResponse,
    MacVerifyRequest,
    MacVerifyResponse,
    RawDecryptRequest,
    RawDecryptResponse,
    RawEncryptRequest,
    RawEncryptResponse,
    RestoreCryptoKeyVersionRequest,
    UpdateCryptoKeyPrimaryVersionRequest,
    UpdateCryptoKeyRequest,
    UpdateCryptoKeyVersionRequest,
)

__all__ = (
    "AutokeyAdminAsyncClient",
    "AutokeyAsyncClient",
    "EkmServiceAsyncClient",
    "KeyManagementServiceAsyncClient",
    "AccessReason",
    "AsymmetricDecryptRequest",
    "AsymmetricDecryptResponse",
    "AsymmetricSignRequest",
    "AsymmetricSignResponse",
    "AutokeyAdminClient",
    "AutokeyClient",
    "AutokeyConfig",
    "Certificate",
    "ChecksummedData",
    "CreateCryptoKeyRequest",
    "CreateCryptoKeyVersionRequest",
    "CreateEkmConnectionRequest",
    "CreateImportJobRequest",
    "CreateKeyHandleMetadata",
    "CreateKeyHandleRequest",
    "CreateKeyRingRequest",
    "CryptoKey",
    "CryptoKeyVersion",
    "CryptoKeyVersionTemplate",
    "DecryptRequest",
    "DecryptResponse",
    "DestroyCryptoKeyVersionRequest",
    "Digest",
    "EkmConfig",
    "EkmConnection",
    "EkmServiceClient",
    "EncryptRequest",
    "EncryptResponse",
    "ExternalProtectionLevelOptions",
    "GenerateRandomBytesRequest",
    "GenerateRandomBytesResponse",
    "GetAutokeyConfigRequest",
    "GetCryptoKeyRequest",
    "GetCryptoKeyVersionRequest",
    "GetEkmConfigRequest",
    "GetEkmConnectionRequest",
    "GetImportJobRequest",
    "GetKeyHandleRequest",
    "GetKeyRingRequest",
    "GetPublicKeyRequest",
    "ImportCryptoKeyVersionRequest",
    "ImportJob",
    "KeyAccessJustificationsPolicy",
    "KeyHandle",
    "KeyManagementServiceClient",
    "KeyOperationAttestation",
    "KeyRing",
    "ListCryptoKeyVersionsRequest",
    "ListCryptoKeyVersionsResponse",
    "ListCryptoKeysRequest",
    "ListCryptoKeysResponse",
    "ListEkmConnectionsRequest",
    "ListEkmConnectionsResponse",
    "ListImportJobsRequest",
    "ListImportJobsResponse",
    "ListKeyHandlesRequest",
    "ListKeyHandlesResponse",
    "ListKeyRingsRequest",
    "ListKeyRingsResponse",
    "LocationMetadata",
    "MacSignRequest",
    "MacSignResponse",
    "MacVerifyRequest",
    "MacVerifyResponse",
    "ProtectionLevel",
    "PublicKey",
    "RawDecryptRequest",
    "RawDecryptResponse",
    "RawEncryptRequest",
    "RawEncryptResponse",
    "RestoreCryptoKeyVersionRequest",
    "ShowEffectiveAutokeyConfigRequest",
    "ShowEffectiveAutokeyConfigResponse",
    "UpdateAutokeyConfigRequest",
    "UpdateCryptoKeyPrimaryVersionRequest",
    "UpdateCryptoKeyRequest",
    "UpdateCryptoKeyVersionRequest",
    "UpdateEkmConfigRequest",
    "UpdateEkmConnectionRequest",
    "VerifyConnectivityRequest",
    "VerifyConnectivityResponse",
)
