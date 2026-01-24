import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_
import smithy_dafny_standard_library.internaldafny.generated.Wrappers as Wrappers
import smithy_dafny_standard_library.internaldafny.generated.BoundedInts as BoundedInts
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_UInt as StandardLibrary_UInt
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_MemoryMath as StandardLibrary_MemoryMath
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_Sequence as StandardLibrary_Sequence
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_String as StandardLibrary_String
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary as StandardLibrary
import smithy_dafny_standard_library.internaldafny.generated.UTF8 as UTF8
import aws_cryptography_internal_dynamodb.internaldafny.generated.ComAmazonawsDynamodbTypes as ComAmazonawsDynamodbTypes
import aws_cryptography_internal_kms.internaldafny.generated.ComAmazonawsKmsTypes as ComAmazonawsKmsTypes
import aws_cryptographic_material_providers.internaldafny.generated.AwsCryptographyKeyStoreTypes as AwsCryptographyKeyStoreTypes
import smithy_dafny_standard_library.internaldafny.generated.Relations as Relations
import smithy_dafny_standard_library.internaldafny.generated.Seq_MergeSort as Seq_MergeSort
import smithy_dafny_standard_library.internaldafny.generated.Math as Math
import smithy_dafny_standard_library.internaldafny.generated.Seq as Seq
import smithy_dafny_standard_library.internaldafny.generated.Actions as Actions
import aws_cryptography_primitives.internaldafny.generated.AwsCryptographyPrimitivesTypes as AwsCryptographyPrimitivesTypes
import aws_cryptographic_material_providers.internaldafny.generated.AwsCryptographyMaterialProvidersTypes as AwsCryptographyMaterialProvidersTypes
import aws_cryptographic_material_providers.internaldafny.generated.AwsArnParsing as AwsArnParsing
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsMrkMatchForDecrypt as AwsKmsMrkMatchForDecrypt
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsUtils as AwsKmsUtils
import aws_cryptographic_material_providers.internaldafny.generated.KeyStoreErrorMessages as KeyStoreErrorMessages
import aws_cryptographic_material_providers.internaldafny.generated.KmsArn as KmsArn
import aws_cryptographic_material_providers.internaldafny.generated.Structure as Structure
import aws_cryptographic_material_providers.internaldafny.generated.KMSKeystoreOperations as KMSKeystoreOperations
import aws_cryptographic_material_providers.internaldafny.generated.DDBKeystoreOperations as DDBKeystoreOperations
import aws_cryptographic_material_providers.internaldafny.generated.CreateKeys as CreateKeys
import aws_cryptographic_material_providers.internaldafny.generated.CreateKeyStoreTable as CreateKeyStoreTable
import aws_cryptographic_material_providers.internaldafny.generated.GetKeys as GetKeys
import smithy_dafny_standard_library.internaldafny.generated.UUID as UUID
import smithy_dafny_standard_library.internaldafny.generated.OsLang as OsLang
import smithy_dafny_standard_library.internaldafny.generated.FileIO as FileIO
import smithy_dafny_standard_library.internaldafny.generated.Time as Time
import aws_cryptographic_material_providers.internaldafny.generated.AwsCryptographyKeyStoreOperations as AwsCryptographyKeyStoreOperations
import aws_cryptography_internal_kms.internaldafny.generated.Com_Amazonaws_Kms as Com_Amazonaws_Kms
import aws_cryptography_internal_dynamodb.internaldafny.generated.Com_Amazonaws_Dynamodb as Com_Amazonaws_Dynamodb
import aws_cryptographic_material_providers.internaldafny.generated.KeyStore as KeyStore
import smithy_dafny_standard_library.internaldafny.generated.Base64 as Base64
import aws_cryptographic_material_providers.internaldafny.generated.AlgorithmSuites as AlgorithmSuites
import aws_cryptographic_material_providers.internaldafny.generated.Materials as Materials
import aws_cryptographic_material_providers.internaldafny.generated.Keyring as Keyring
import smithy_dafny_standard_library.internaldafny.generated.SortedSets as SortedSets
import aws_cryptographic_material_providers.internaldafny.generated.CanonicalEncryptionContext as CanonicalEncryptionContext
import aws_cryptography_primitives.internaldafny.generated.ExternRandom as ExternRandom
import aws_cryptography_primitives.internaldafny.generated.Random as Random
import aws_cryptography_primitives.internaldafny.generated.AESEncryption as AESEncryption
import aws_cryptography_primitives.internaldafny.generated.ExternDigest as ExternDigest
import aws_cryptography_primitives.internaldafny.generated.Digest as Digest
import aws_cryptography_primitives.internaldafny.generated.HMAC as HMAC
import aws_cryptography_primitives.internaldafny.generated.WrappedHMAC as WrappedHMAC
import aws_cryptography_primitives.internaldafny.generated.HKDF as HKDF
import aws_cryptography_primitives.internaldafny.generated.WrappedHKDF as WrappedHKDF
import aws_cryptography_primitives.internaldafny.generated.Signature as Signature
import aws_cryptography_primitives.internaldafny.generated.KdfCtr as KdfCtr
import aws_cryptography_primitives.internaldafny.generated.RSAEncryption as RSAEncryption
import aws_cryptography_primitives.internaldafny.generated.ECDH as ECDH
import aws_cryptography_primitives.internaldafny.generated.AwsCryptographyPrimitivesOperations as AwsCryptographyPrimitivesOperations
import aws_cryptography_primitives.internaldafny.generated.AtomicPrimitives as AtomicPrimitives
import aws_cryptographic_material_providers.internaldafny.generated.MaterialWrapping as MaterialWrapping
import aws_cryptographic_material_providers.internaldafny.generated.IntermediateKeyWrapping as IntermediateKeyWrapping
import aws_cryptographic_material_providers.internaldafny.generated.EdkWrapping as EdkWrapping
import aws_cryptographic_material_providers.internaldafny.generated.ErrorMessages as ErrorMessages
import aws_cryptographic_material_providers.internaldafny.generated.RawAESKeyring as RawAESKeyring
import aws_cryptographic_material_providers.internaldafny.generated.Constants as Constants
import aws_cryptographic_material_providers.internaldafny.generated.EcdhEdkWrapping as EcdhEdkWrapping
import aws_cryptographic_material_providers.internaldafny.generated.RawECDHKeyring as RawECDHKeyring
import aws_cryptographic_material_providers.internaldafny.generated.RawRSAKeyring as RawRSAKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsKeyring as AwsKmsKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsDiscoveryKeyring as AwsKmsDiscoveryKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsEcdhKeyring as AwsKmsEcdhKeyring
import smithy_dafny_standard_library.internaldafny.generated.DafnyLibraries as DafnyLibraries
import aws_cryptographic_material_providers.internaldafny.generated.LocalCMC as LocalCMC
import aws_cryptographic_material_providers.internaldafny.generated.SynchronizedLocalCMC as SynchronizedLocalCMC
import aws_cryptographic_material_providers.internaldafny.generated.StormTracker as StormTracker
import aws_cryptographic_material_providers.internaldafny.generated.StormTrackingCMC as StormTrackingCMC
import aws_cryptographic_material_providers.internaldafny.generated.CacheConstants as CacheConstants
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsHierarchicalKeyring as AwsKmsHierarchicalKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsMrkDiscoveryKeyring as AwsKmsMrkDiscoveryKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsMrkKeyring as AwsKmsMrkKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsRsaKeyring as AwsKmsRsaKeyring
import aws_cryptographic_material_providers.internaldafny.generated.MultiKeyring as MultiKeyring
import aws_cryptographic_material_providers.internaldafny.generated.AwsKmsMrkAreUnique as AwsKmsMrkAreUnique
import aws_cryptographic_material_providers.internaldafny.generated.StrictMultiKeyring as StrictMultiKeyring
import aws_cryptographic_material_providers.internaldafny.generated.DiscoveryMultiKeyring as DiscoveryMultiKeyring
import aws_cryptographic_material_providers.internaldafny.generated.MrkAwareDiscoveryMultiKeyring as MrkAwareDiscoveryMultiKeyring
import aws_cryptographic_material_providers.internaldafny.generated.MrkAwareStrictMultiKeyring as MrkAwareStrictMultiKeyring
import aws_cryptographic_material_providers.internaldafny.generated.CMM as CMM
import aws_cryptographic_material_providers.internaldafny.generated.Defaults as Defaults
import aws_cryptographic_material_providers.internaldafny.generated.Commitment as Commitment
import aws_cryptographic_material_providers.internaldafny.generated.DefaultCMM as DefaultCMM
import aws_cryptographic_material_providers.internaldafny.generated.DefaultClientSupplier as DefaultClientSupplier
import aws_cryptographic_material_providers.internaldafny.generated.Utils as Utils
import aws_cryptographic_material_providers.internaldafny.generated.RequiredEncryptionContextCMM as RequiredEncryptionContextCMM
import aws_cryptographic_material_providers.internaldafny.generated.AwsCryptographyMaterialProvidersOperations as AwsCryptographyMaterialProvidersOperations
import aws_cryptographic_material_providers.internaldafny.generated.MaterialProviders as MaterialProviders
import aws_cryptography_primitives.internaldafny.generated.AesKdfCtr as AesKdfCtr
import smithy_dafny_standard_library.internaldafny.generated.Unicode as Unicode
import smithy_dafny_standard_library.internaldafny.generated.Functions as Functions
import smithy_dafny_standard_library.internaldafny.generated.Utf8EncodingForm as Utf8EncodingForm
import smithy_dafny_standard_library.internaldafny.generated.Utf16EncodingForm as Utf16EncodingForm
import smithy_dafny_standard_library.internaldafny.generated.UnicodeStrings as UnicodeStrings
import smithy_dafny_standard_library.internaldafny.generated.GeneralInternals as GeneralInternals
import smithy_dafny_standard_library.internaldafny.generated.MulInternalsNonlinear as MulInternalsNonlinear
import smithy_dafny_standard_library.internaldafny.generated.MulInternals as MulInternals
import smithy_dafny_standard_library.internaldafny.generated.Mul as Mul
import smithy_dafny_standard_library.internaldafny.generated.ModInternalsNonlinear as ModInternalsNonlinear
import smithy_dafny_standard_library.internaldafny.generated.DivInternalsNonlinear as DivInternalsNonlinear
import smithy_dafny_standard_library.internaldafny.generated.ModInternals as ModInternals
import smithy_dafny_standard_library.internaldafny.generated.DivInternals as DivInternals
import smithy_dafny_standard_library.internaldafny.generated.DivMod as DivMod
import smithy_dafny_standard_library.internaldafny.generated.Power as Power
import smithy_dafny_standard_library.internaldafny.generated.Logarithm as Logarithm
import smithy_dafny_standard_library.internaldafny.generated.StandardLibraryInterop as StandardLibraryInterop
import smithy_dafny_standard_library.internaldafny.generated.Streams as Streams
import smithy_dafny_standard_library.internaldafny.generated.Sorting as Sorting
import smithy_dafny_standard_library.internaldafny.generated.HexStrings as HexStrings
import smithy_dafny_standard_library.internaldafny.generated.GetOpt as GetOpt
import smithy_dafny_standard_library.internaldafny.generated.FloatCompare as FloatCompare
import smithy_dafny_standard_library.internaldafny.generated.ConcurrentCall as ConcurrentCall
import smithy_dafny_standard_library.internaldafny.generated.Base64Lemmas as Base64Lemmas
import Fixtures as Fixtures
import CleanupItems as CleanupItems
import TestVersionKey as TestVersionKey
import TestLyingBranchKey as TestLyingBranchKey
import TestGetKeys as TestGetKeys
import TestDiscoveryGetKeys as TestDiscoveryGetKeys
import TestCreateKeysWithSpecialECKeys as TestCreateKeysWithSpecialECKeys
import TestCreateKeys as TestCreateKeys
import TestCreateKeyStore as TestCreateKeyStore
import TestConfig as TestConfig
import TestUtils as TestUtils
import TestIntermediateKeyWrapping as TestIntermediateKeyWrapping
import TestErrorMessages as TestErrorMessages
import TestEcdhCalculation as TestEcdhCalculation
import TestDefaultClientProvider as TestDefaultClientProvider
import TestRawRSAKeying as TestRawRSAKeying
import TestRawAESKeyring as TestRawAESKeyring
import TestMultiKeyring as TestMultiKeyring
import TestRawECDHKeyring as TestRawECDHKeyring
import TestAwsKmsRsaKeyring as TestAwsKmsRsaKeyring
import TestAwsKmsEcdhKeyring as TestAwsKmsEcdhKeyring

# Module: TestAwsKmsHierarchicalKeyring

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def GetTestMaterials(suiteId):
        out: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials = None
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(66,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_3_suite_ = AlgorithmSuites.default__.GetSuite(suiteId)
        d_4_valueOrError1_: Wrappers.Result = None
        d_4_valueOrError1_ = (d_1_mpl_).InitializeEncryptionMaterials(AwsCryptographyMaterialProvidersTypes.InitializeEncryptionMaterialsInput_InitializeEncryptionMaterialsInput(suiteId, d_2_encryptionContext_, _dafny.Seq([]), Wrappers.Option_None(), Wrappers.Option_None()))
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(71,33): " + _dafny.string_of(d_4_valueOrError1_))
        d_5_encryptionMaterialsIn_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        d_5_encryptionMaterialsIn_ = (d_4_valueOrError1_).Extract()
        out = d_5_encryptionMaterialsIn_
        return out
        return out

    @staticmethod
    def TestHierarchyClientESDKSuite():
        d_0_branchKeyId_: _dafny.Seq
        d_0_branchKeyId_ = default__.BRANCH__KEY__ID
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(89,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClient()
        d_4_valueOrError1_ = out1_
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(91,21): " + _dafny.string_of(d_4_valueOrError1_))
        d_5_kmsClient_: ComAmazonawsKmsTypes.IKMSClient
        d_5_kmsClient_ = (d_4_valueOrError1_).Extract()
        d_6_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_6_valueOrError2_ = out2_
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(92,21): " + _dafny.string_of(d_6_valueOrError2_))
        d_7_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_7_ddbClient_ = (d_6_valueOrError2_).Extract()
        d_8_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_8_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_9_keyStoreConfig_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_9_keyStoreConfig_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_8_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_7_ddbClient_), Wrappers.Option_Some(d_5_kmsClient_))
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = KeyStore.default__.KeyStore(d_9_keyStoreConfig_)
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(105,20): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_keyStore_: KeyStore.KeyStoreClient
        d_11_keyStore_ = (d_10_valueOrError3_).Extract()
        d_12_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyId_), Wrappers.Option_None(), d_11_keyStore_, d_1_ttl_, Wrappers.Option_None(), Wrappers.Option_None()))
        d_12_valueOrError4_ = out4_
        if not(not((d_12_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(107,28): " + _dafny.string_of(d_12_valueOrError4_))
        d_13_hierarchyKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_13_hierarchyKeyring_ = (d_12_valueOrError4_).Extract()
        d_14_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_ = default__.GetTestMaterials(default__.TEST__ESDK__ALG__SUITE__ID)
        d_14_materials_ = out5_
        default__.TestRoundtrip(d_13_hierarchyKeyring_, d_14_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyId_)
        d_15_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_15_suite_ = AlgorithmSuites.default__.GetSuite(default__.TEST__ESDK__ALG__SUITE__ID)
        d_16_zeroedKey_: _dafny.Seq
        d_16_zeroedKey_ = _dafny.Seq([0 for d_17___v0_ in range(AlgorithmSuites.default__.GetEncryptKeyLength(d_15_suite_))])
        d_18_dt__update__tmp_h0_ = d_14_materials_
        d_19_dt__update_hplaintextDataKey_h0_ = Wrappers.Option_Some(d_16_zeroedKey_)
        d_14_materials_ = AwsCryptographyMaterialProvidersTypes.EncryptionMaterials_EncryptionMaterials((d_18_dt__update__tmp_h0_).algorithmSuite, (d_18_dt__update__tmp_h0_).encryptionContext, (d_18_dt__update__tmp_h0_).encryptedDataKeys, (d_18_dt__update__tmp_h0_).requiredEncryptionContextKeys, d_19_dt__update_hplaintextDataKey_h0_, (d_18_dt__update__tmp_h0_).signingKey, (d_18_dt__update__tmp_h0_).symmetricSigningKeys)
        default__.TestRoundtrip(d_13_hierarchyKeyring_, d_14_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyId_)

    @staticmethod
    def TestHierarchyClientDBESuite():
        d_0_branchKeyId_: _dafny.Seq
        d_0_branchKeyId_ = default__.BRANCH__KEY__ID
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(132,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClient()
        d_4_valueOrError1_ = out1_
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(134,21): " + _dafny.string_of(d_4_valueOrError1_))
        d_5_kmsClient_: ComAmazonawsKmsTypes.IKMSClient
        d_5_kmsClient_ = (d_4_valueOrError1_).Extract()
        d_6_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_6_valueOrError2_ = out2_
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(135,21): " + _dafny.string_of(d_6_valueOrError2_))
        d_7_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_7_ddbClient_ = (d_6_valueOrError2_).Extract()
        d_8_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_8_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_9_keyStoreConfig_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_9_keyStoreConfig_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_8_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_7_ddbClient_), Wrappers.Option_Some(d_5_kmsClient_))
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = KeyStore.default__.KeyStore(d_9_keyStoreConfig_)
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(148,20): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_keyStore_: KeyStore.KeyStoreClient
        d_11_keyStore_ = (d_10_valueOrError3_).Extract()
        d_12_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyId_), Wrappers.Option_None(), d_11_keyStore_, d_1_ttl_, Wrappers.Option_None(), Wrappers.Option_None()))
        d_12_valueOrError4_ = out4_
        if not(not((d_12_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(150,28): " + _dafny.string_of(d_12_valueOrError4_))
        d_13_hierarchyKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_13_hierarchyKeyring_ = (d_12_valueOrError4_).Extract()
        d_14_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_ = default__.GetTestMaterials(default__.TEST__DBE__ALG__SUITE__ID)
        d_14_materials_ = out5_
        default__.TestRoundtrip(d_13_hierarchyKeyring_, d_14_materials_, default__.TEST__DBE__ALG__SUITE__ID, d_0_branchKeyId_)
        d_15_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_15_suite_ = AlgorithmSuites.default__.GetSuite(default__.TEST__DBE__ALG__SUITE__ID)
        d_16_zeroedKey_: _dafny.Seq
        d_16_zeroedKey_ = _dafny.Seq([0 for d_17___v1_ in range(AlgorithmSuites.default__.GetEncryptKeyLength(d_15_suite_))])
        d_18_dt__update__tmp_h0_ = d_14_materials_
        d_19_dt__update_hplaintextDataKey_h0_ = Wrappers.Option_Some(d_16_zeroedKey_)
        d_14_materials_ = AwsCryptographyMaterialProvidersTypes.EncryptionMaterials_EncryptionMaterials((d_18_dt__update__tmp_h0_).algorithmSuite, (d_18_dt__update__tmp_h0_).encryptionContext, (d_18_dt__update__tmp_h0_).encryptedDataKeys, (d_18_dt__update__tmp_h0_).requiredEncryptionContextKeys, d_19_dt__update_hplaintextDataKey_h0_, (d_18_dt__update__tmp_h0_).signingKey, (d_18_dt__update__tmp_h0_).symmetricSigningKeys)
        default__.TestRoundtrip(d_13_hierarchyKeyring_, d_14_materials_, default__.TEST__DBE__ALG__SUITE__ID, d_0_branchKeyId_)

    @staticmethod
    def TestBranchKeyIdSupplier():
        d_0_branchKeyIdSupplier_: AwsCryptographyMaterialProvidersTypes.IBranchKeyIdSupplier
        nw0_ = DummyBranchKeyIdSupplier()
        nw0_.ctor__()
        d_0_branchKeyIdSupplier_ = nw0_
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(176,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClient()
        d_4_valueOrError1_ = out1_
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(178,21): " + _dafny.string_of(d_4_valueOrError1_))
        d_5_kmsClient_: ComAmazonawsKmsTypes.IKMSClient
        d_5_kmsClient_ = (d_4_valueOrError1_).Extract()
        d_6_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_6_valueOrError2_ = out2_
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(179,21): " + _dafny.string_of(d_6_valueOrError2_))
        d_7_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_7_ddbClient_ = (d_6_valueOrError2_).Extract()
        d_8_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_8_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_9_keyStoreConfig_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_9_keyStoreConfig_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_8_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_7_ddbClient_), Wrappers.Option_Some(d_5_kmsClient_))
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = KeyStore.default__.KeyStore(d_9_keyStoreConfig_)
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(192,20): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_keyStore_: KeyStore.KeyStoreClient
        d_11_keyStore_ = (d_10_valueOrError3_).Extract()
        d_12_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_None(), Wrappers.Option_Some(d_0_branchKeyIdSupplier_), d_11_keyStore_, d_1_ttl_, Wrappers.Option_None(), Wrappers.Option_None()))
        d_12_valueOrError4_ = out4_
        if not(not((d_12_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(194,28): " + _dafny.string_of(d_12_valueOrError4_))
        d_13_hierarchyKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_13_hierarchyKeyring_ = (d_12_valueOrError4_).Extract()
        d_14_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_ = default__.GetTestMaterials(default__.TEST__DBE__ALG__SUITE__ID)
        d_14_materials_ = out5_
        d_15_contextCaseA_: _dafny.Map
        d_15_contextCaseA_ = ((d_14_materials_).encryptionContext).set(default__.BRANCH__KEY, default__.CASE__A)
        d_16_dt__update__tmp_h0_ = d_14_materials_
        d_17_dt__update_hencryptionContext_h0_ = d_15_contextCaseA_
        d_14_materials_ = AwsCryptographyMaterialProvidersTypes.EncryptionMaterials_EncryptionMaterials((d_16_dt__update__tmp_h0_).algorithmSuite, d_17_dt__update_hencryptionContext_h0_, (d_16_dt__update__tmp_h0_).encryptedDataKeys, (d_16_dt__update__tmp_h0_).requiredEncryptionContextKeys, (d_16_dt__update__tmp_h0_).plaintextDataKey, (d_16_dt__update__tmp_h0_).signingKey, (d_16_dt__update__tmp_h0_).symmetricSigningKeys)
        default__.TestRoundtrip(d_13_hierarchyKeyring_, d_14_materials_, default__.TEST__DBE__ALG__SUITE__ID, default__.BRANCH__KEY__ID__A)
        d_18_contextCaseB_: _dafny.Map
        d_18_contextCaseB_ = ((d_14_materials_).encryptionContext).set(default__.BRANCH__KEY, default__.CASE__B)
        d_19_dt__update__tmp_h1_ = d_14_materials_
        d_20_dt__update_hencryptionContext_h1_ = d_18_contextCaseB_
        d_14_materials_ = AwsCryptographyMaterialProvidersTypes.EncryptionMaterials_EncryptionMaterials((d_19_dt__update__tmp_h1_).algorithmSuite, d_20_dt__update_hencryptionContext_h1_, (d_19_dt__update__tmp_h1_).encryptedDataKeys, (d_19_dt__update__tmp_h1_).requiredEncryptionContextKeys, (d_19_dt__update__tmp_h1_).plaintextDataKey, (d_19_dt__update__tmp_h1_).signingKey, (d_19_dt__update__tmp_h1_).symmetricSigningKeys)
        default__.TestRoundtrip(d_13_hierarchyKeyring_, d_14_materials_, default__.TEST__DBE__ALG__SUITE__ID, default__.BRANCH__KEY__ID__B)

    @staticmethod
    def TestInvalidDataKeyError():
        d_0_branchKeyIdSupplier_: AwsCryptographyMaterialProvidersTypes.IBranchKeyIdSupplier
        nw0_ = DummyBranchKeyIdSupplier()
        nw0_.ctor__()
        d_0_branchKeyIdSupplier_ = nw0_
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(222,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClient()
        d_4_valueOrError1_ = out1_
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(223,21): " + _dafny.string_of(d_4_valueOrError1_))
        d_5_kmsClient_: ComAmazonawsKmsTypes.IKMSClient
        d_5_kmsClient_ = (d_4_valueOrError1_).Extract()
        d_6_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_6_valueOrError2_ = out2_
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(224,21): " + _dafny.string_of(d_6_valueOrError2_))
        d_7_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_7_ddbClient_ = (d_6_valueOrError2_).Extract()
        d_8_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_8_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_9_keyStoreConfig_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_9_keyStoreConfig_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_8_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_7_ddbClient_), Wrappers.Option_Some(d_5_kmsClient_))
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = KeyStore.default__.KeyStore(d_9_keyStoreConfig_)
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(235,20): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_keyStore_: KeyStore.KeyStoreClient
        d_11_keyStore_ = (d_10_valueOrError3_).Extract()
        d_12_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_None(), Wrappers.Option_Some(d_0_branchKeyIdSupplier_), d_11_keyStore_, d_1_ttl_, Wrappers.Option_None(), Wrappers.Option_None()))
        d_12_valueOrError4_ = out4_
        if not(not((d_12_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(236,28): " + _dafny.string_of(d_12_valueOrError4_))
        d_13_hierarchyKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_13_hierarchyKeyring_ = (d_12_valueOrError4_).Extract()
        d_14_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_ = default__.GetTestMaterials(default__.TEST__DBE__ALG__SUITE__ID)
        d_14_materials_ = out5_
        d_15_contextCaseA_: _dafny.Map
        d_15_contextCaseA_ = ((d_14_materials_).encryptionContext).set(default__.BRANCH__KEY, default__.CASE__A)
        d_16_contextCaseB_: _dafny.Map
        d_16_contextCaseB_ = ((d_14_materials_).encryptionContext).set(default__.BRANCH__KEY, default__.CASE__B)
        d_17_materialsA_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        d_18_dt__update__tmp_h0_ = d_14_materials_
        d_19_dt__update_hencryptionContext_h0_ = d_15_contextCaseA_
        d_17_materialsA_ = AwsCryptographyMaterialProvidersTypes.EncryptionMaterials_EncryptionMaterials((d_18_dt__update__tmp_h0_).algorithmSuite, d_19_dt__update_hencryptionContext_h0_, (d_18_dt__update__tmp_h0_).encryptedDataKeys, (d_18_dt__update__tmp_h0_).requiredEncryptionContextKeys, (d_18_dt__update__tmp_h0_).plaintextDataKey, (d_18_dt__update__tmp_h0_).signingKey, (d_18_dt__update__tmp_h0_).symmetricSigningKeys)
        d_20_materialsB_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        d_21_dt__update__tmp_h1_ = d_14_materials_
        d_22_dt__update_hencryptionContext_h1_ = d_16_contextCaseB_
        d_20_materialsB_ = AwsCryptographyMaterialProvidersTypes.EncryptionMaterials_EncryptionMaterials((d_21_dt__update__tmp_h1_).algorithmSuite, d_22_dt__update_hencryptionContext_h1_, (d_21_dt__update__tmp_h1_).encryptedDataKeys, (d_21_dt__update__tmp_h1_).requiredEncryptionContextKeys, (d_21_dt__update__tmp_h1_).plaintextDataKey, (d_21_dt__update__tmp_h1_).signingKey, (d_21_dt__update__tmp_h1_).symmetricSigningKeys)
        default__.TestInvalidDataKeyFailureCase(d_13_hierarchyKeyring_, d_17_materialsA_, d_20_materialsB_, default__.TEST__DBE__ALG__SUITE__ID)

    @staticmethod
    def TestInvalidDataKeyFailureCase(hierarchyKeyring, encryptionMaterialsInEncrypt, encryptionMaterialsInDecrypt, algorithmSuiteId):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = (hierarchyKeyring).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(encryptionMaterialsInEncrypt))
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(265,34): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_encryptionMaterialsOut_: AwsCryptographyMaterialProvidersTypes.OnEncryptOutput
        d_1_encryptionMaterialsOut_ = (d_0_valueOrError0_).Extract()
        d_2_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError1_ = out1_
        if not(not((d_2_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(269,15): " + _dafny.string_of(d_2_valueOrError1_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError1_).Extract()
        d_4_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        d_4_valueOrError2_ = (d_3_mpl_).EncryptionMaterialsHasPlaintextDataKey((d_1_encryptionMaterialsOut_).materials)
        if not(not((d_4_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(270,13): " + _dafny.string_of(d_4_valueOrError2_))
        d_5___v2_: tuple
        d_5___v2_ = (d_4_valueOrError2_).Extract()
        if not((len(((d_1_encryptionMaterialsOut_).materials).encryptedDataKeys)) == (1)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(272,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_edk_: AwsCryptographyMaterialProvidersTypes.EncryptedDataKey
        d_6_edk_ = (((d_1_encryptionMaterialsOut_).materials).encryptedDataKeys)[0]
        d_7_valueOrError3_: Wrappers.Result = None
        d_7_valueOrError3_ = (d_3_mpl_).InitializeDecryptionMaterials(AwsCryptographyMaterialProvidersTypes.InitializeDecryptionMaterialsInput_InitializeDecryptionMaterialsInput(algorithmSuiteId, (encryptionMaterialsInDecrypt).encryptionContext, _dafny.Seq([])))
        if not(not((d_7_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(276,33): " + _dafny.string_of(d_7_valueOrError3_))
        d_8_decryptionMaterialsIn_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_8_decryptionMaterialsIn_ = (d_7_valueOrError3_).Extract()
        d_9_decryptionMaterialsOut_: Wrappers.Result
        out2_: Wrappers.Result
        out2_ = (hierarchyKeyring).OnDecrypt(AwsCryptographyMaterialProvidersTypes.OnDecryptInput_OnDecryptInput(d_8_decryptionMaterialsIn_, _dafny.Seq([d_6_edk_])))
        d_9_decryptionMaterialsOut_ = out2_
        if not((d_9_decryptionMaterialsOut_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(289,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_9_decryptionMaterialsOut_).error).is_AwsCryptographicMaterialProvidersException):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(290,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError4_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_10_valueOrError4_ = ErrorMessages.default__.IncorrectDataKeys(_dafny.Seq([d_6_edk_]), (d_8_decryptionMaterialsIn_).algorithmSuite, _dafny.Seq(""))
        if not(not((d_10_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(291,32): " + _dafny.string_of(d_10_valueOrError4_))
        d_11_expectedErrorMessage_: _dafny.Seq
        d_11_expectedErrorMessage_ = (d_10_valueOrError4_).Extract()
        if not((((d_9_decryptionMaterialsOut_).error).message) == (d_11_expectedErrorMessage_)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(292,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestRoundtrip(hierarchyKeyring, encryptionMaterialsIn, algorithmSuiteId, expectedBranchKeyId):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = (hierarchyKeyring).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(encryptionMaterialsIn))
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(305,34): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_encryptionMaterialsOut_: AwsCryptographyMaterialProvidersTypes.OnEncryptOutput
        d_1_encryptionMaterialsOut_ = (d_0_valueOrError0_).Extract()
        d_2_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError1_ = out1_
        if not(not((d_2_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(309,15): " + _dafny.string_of(d_2_valueOrError1_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError1_).Extract()
        d_4_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        d_4_valueOrError2_ = (d_3_mpl_).EncryptionMaterialsHasPlaintextDataKey((d_1_encryptionMaterialsOut_).materials)
        if not(not((d_4_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(310,13): " + _dafny.string_of(d_4_valueOrError2_))
        d_5___v3_: tuple
        d_5___v3_ = (d_4_valueOrError2_).Extract()
        if not((len(((d_1_encryptionMaterialsOut_).materials).encryptedDataKeys)) == (1)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(312,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_edk_: AwsCryptographyMaterialProvidersTypes.EncryptedDataKey
        d_6_edk_ = (((d_1_encryptionMaterialsOut_).materials).encryptedDataKeys)[0]
        d_7_valueOrError3_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_7_valueOrError3_ = UTF8.default__.Encode(expectedBranchKeyId)
        if not(not((d_7_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(317,35): " + _dafny.string_of(d_7_valueOrError3_))
        d_8_expectedBranchKeyIdUTF8_: _dafny.Seq
        d_8_expectedBranchKeyIdUTF8_ = (d_7_valueOrError3_).Extract()
        if not(((d_6_edk_).keyProviderInfo) == (d_8_expectedBranchKeyIdUTF8_)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(318,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_valueOrError4_: Wrappers.Result = None
        d_9_valueOrError4_ = (d_3_mpl_).InitializeDecryptionMaterials(AwsCryptographyMaterialProvidersTypes.InitializeDecryptionMaterialsInput_InitializeDecryptionMaterialsInput(algorithmSuiteId, (encryptionMaterialsIn).encryptionContext, _dafny.Seq([])))
        if not(not((d_9_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(320,33): " + _dafny.string_of(d_9_valueOrError4_))
        d_10_decryptionMaterialsIn_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_10_decryptionMaterialsIn_ = (d_9_valueOrError4_).Extract()
        d_11_valueOrError5_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = (hierarchyKeyring).OnDecrypt(AwsCryptographyMaterialProvidersTypes.OnDecryptInput_OnDecryptInput(d_10_decryptionMaterialsIn_, _dafny.Seq([d_6_edk_])))
        d_11_valueOrError5_ = out2_
        if not(not((d_11_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(327,34): " + _dafny.string_of(d_11_valueOrError5_))
        d_12_decryptionMaterialsOut_: AwsCryptographyMaterialProvidersTypes.OnDecryptOutput
        d_12_decryptionMaterialsOut_ = (d_11_valueOrError5_).Extract()
        if not((((d_1_encryptionMaterialsOut_).materials).plaintextDataKey) == (((d_12_decryptionMaterialsOut_).materials).plaintextDataKey)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(339,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSharedCacheWithSamePartitionIdAndSameLogicalKeyStoreName():
        d_0_branchKeyIdWest_: _dafny.Seq
        d_0_branchKeyIdWest_ = default__.BRANCH__KEY__ID
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(348,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_regionWest_: _dafny.Seq
        d_4_regionWest_ = _dafny.Seq("us-west-2")
        d_5_regionEast_: _dafny.Seq
        d_5_regionEast_ = _dafny.Seq("us-east-2")
        d_6_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_4_regionWest_)
        d_6_valueOrError1_ = out1_
        if not(not((d_6_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(353,25): " + _dafny.string_of(d_6_valueOrError1_))
        d_7_kmsClientWest_: ComAmazonawsKmsTypes.IKMSClient
        d_7_kmsClientWest_ = (d_6_valueOrError1_).Extract()
        d_8_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_5_regionEast_)
        d_8_valueOrError2_ = out2_
        if not(not((d_8_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(354,25): " + _dafny.string_of(d_8_valueOrError2_))
        d_9_kmsClientEast_: ComAmazonawsKmsTypes.IKMSClient
        d_9_kmsClientEast_ = (d_8_valueOrError2_).Extract()
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(355,21): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_11_ddbClient_ = (d_10_valueOrError3_).Extract()
        d_12_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_12_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_13_keyStoreConfigClientRegionWest_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_13_keyStoreConfigClientRegionWest_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_7_kmsClientWest_))
        d_14_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = KeyStore.default__.KeyStore(d_13_keyStoreConfigClientRegionWest_)
        d_14_valueOrError4_ = out4_
        if not(not((d_14_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(371,36): " + _dafny.string_of(d_14_valueOrError4_))
        d_15_keyStoreClientRegionWest_: KeyStore.KeyStoreClient
        d_15_keyStoreClientRegionWest_ = (d_14_valueOrError4_).Extract()
        d_16_keyStoreConfigClientRegionEast_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_16_keyStoreConfigClientRegionEast_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_9_kmsClientEast_))
        d_17_valueOrError5_: Wrappers.Result = None
        out5_: Wrappers.Result
        out5_ = KeyStore.default__.KeyStore(d_16_keyStoreConfigClientRegionEast_)
        d_17_valueOrError5_ = out5_
        if not(not((d_17_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(387,36): " + _dafny.string_of(d_17_valueOrError5_))
        d_18_keyStoreClientRegionEast_: KeyStore.KeyStoreClient
        d_18_keyStoreClientRegionEast_ = (d_17_valueOrError5_).Extract()
        d_19_valueOrError6_: Wrappers.Result = None
        out6_: Wrappers.Result
        out6_ = (d_3_mpl_).CreateCryptographicMaterialsCache(AwsCryptographyMaterialProvidersTypes.CreateCryptographicMaterialsCacheInput_CreateCryptographicMaterialsCacheInput(AwsCryptographyMaterialProvidersTypes.CacheType_Default(AwsCryptographyMaterialProvidersTypes.DefaultCache_DefaultCache(100))))
        d_19_valueOrError6_ = out6_
        if not(not((d_19_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(390,28): " + _dafny.string_of(d_19_valueOrError6_))
        d_20_sharedCacheInput_: AwsCryptographyMaterialProvidersTypes.ICryptographicMaterialsCache
        d_20_sharedCacheInput_ = (d_19_valueOrError6_).Extract()
        d_21_sharedCache_: AwsCryptographyMaterialProvidersTypes.CacheType
        d_21_sharedCache_ = AwsCryptographyMaterialProvidersTypes.CacheType_Shared(d_20_sharedCacheInput_)
        d_22_valueOrError7_: Wrappers.Result = None
        out7_: Wrappers.Result
        out7_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_15_keyStoreClientRegionWest_, d_1_ttl_, Wrappers.Option_Some(d_21_sharedCache_), Wrappers.Option_Some(_dafny.Seq("partitionId"))))
        d_22_valueOrError7_ = out7_
        if not(not((d_22_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(408,29): " + _dafny.string_of(d_22_valueOrError7_))
        d_23_hierarchyKeyring1_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_23_hierarchyKeyring1_ = (d_22_valueOrError7_).Extract()
        d_24_valueOrError8_: Wrappers.Result = None
        out8_: Wrappers.Result
        out8_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_18_keyStoreClientRegionEast_, d_1_ttl_, Wrappers.Option_Some(d_21_sharedCache_), Wrappers.Option_Some(_dafny.Seq("partitionId"))))
        d_24_valueOrError8_ = out8_
        if not(not((d_24_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(422,29): " + _dafny.string_of(d_24_valueOrError8_))
        d_25_hierarchyKeyring2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_25_hierarchyKeyring2_ = (d_24_valueOrError8_).Extract()
        d_26_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_ = default__.GetTestMaterials(default__.TEST__ESDK__ALG__SUITE__ID)
        d_26_materials_ = out9_
        d_27_encryptionMaterialsOutMismatchedRegion_: Wrappers.Result
        out10_: Wrappers.Result
        out10_ = (d_25_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_26_materials_))
        d_27_encryptionMaterialsOutMismatchedRegion_ = out10_
        if not((d_27_encryptionMaterialsOutMismatchedRegion_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(449,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        default__.TestRoundtrip(d_23_hierarchyKeyring1_, d_26_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyIdWest_)
        default__.TestRoundtrip(d_25_hierarchyKeyring2_, d_26_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyIdWest_)

    @staticmethod
    def TestSharedCacheWithDifferentUnspecifiedPartitionIdAndSameLogicalKeyStoreName():
        d_0_branchKeyIdWest_: _dafny.Seq
        d_0_branchKeyIdWest_ = default__.BRANCH__KEY__ID
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(488,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_regionWest_: _dafny.Seq
        d_4_regionWest_ = _dafny.Seq("us-west-2")
        d_5_regionEast_: _dafny.Seq
        d_5_regionEast_ = _dafny.Seq("us-east-2")
        d_6_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_4_regionWest_)
        d_6_valueOrError1_ = out1_
        if not(not((d_6_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(493,25): " + _dafny.string_of(d_6_valueOrError1_))
        d_7_kmsClientWest_: ComAmazonawsKmsTypes.IKMSClient
        d_7_kmsClientWest_ = (d_6_valueOrError1_).Extract()
        d_8_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_5_regionEast_)
        d_8_valueOrError2_ = out2_
        if not(not((d_8_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(494,25): " + _dafny.string_of(d_8_valueOrError2_))
        d_9_kmsClientEast_: ComAmazonawsKmsTypes.IKMSClient
        d_9_kmsClientEast_ = (d_8_valueOrError2_).Extract()
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(495,21): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_11_ddbClient_ = (d_10_valueOrError3_).Extract()
        d_12_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_12_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_13_keyStoreConfigClientRegionWest_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_13_keyStoreConfigClientRegionWest_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_7_kmsClientWest_))
        d_14_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = KeyStore.default__.KeyStore(d_13_keyStoreConfigClientRegionWest_)
        d_14_valueOrError4_ = out4_
        if not(not((d_14_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(511,36): " + _dafny.string_of(d_14_valueOrError4_))
        d_15_keyStoreClientRegionWest_: KeyStore.KeyStoreClient
        d_15_keyStoreClientRegionWest_ = (d_14_valueOrError4_).Extract()
        d_16_keyStoreConfigClientRegionEast_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_16_keyStoreConfigClientRegionEast_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_9_kmsClientEast_))
        d_17_valueOrError5_: Wrappers.Result = None
        out5_: Wrappers.Result
        out5_ = KeyStore.default__.KeyStore(d_16_keyStoreConfigClientRegionEast_)
        d_17_valueOrError5_ = out5_
        if not(not((d_17_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(527,36): " + _dafny.string_of(d_17_valueOrError5_))
        d_18_keyStoreClientRegionEast_: KeyStore.KeyStoreClient
        d_18_keyStoreClientRegionEast_ = (d_17_valueOrError5_).Extract()
        d_19_valueOrError6_: Wrappers.Result = None
        out6_: Wrappers.Result
        out6_ = (d_3_mpl_).CreateCryptographicMaterialsCache(AwsCryptographyMaterialProvidersTypes.CreateCryptographicMaterialsCacheInput_CreateCryptographicMaterialsCacheInput(AwsCryptographyMaterialProvidersTypes.CacheType_Default(AwsCryptographyMaterialProvidersTypes.DefaultCache_DefaultCache(100))))
        d_19_valueOrError6_ = out6_
        if not(not((d_19_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(530,28): " + _dafny.string_of(d_19_valueOrError6_))
        d_20_sharedCacheInput_: AwsCryptographyMaterialProvidersTypes.ICryptographicMaterialsCache
        d_20_sharedCacheInput_ = (d_19_valueOrError6_).Extract()
        d_21_sharedCache_: AwsCryptographyMaterialProvidersTypes.CacheType
        d_21_sharedCache_ = AwsCryptographyMaterialProvidersTypes.CacheType_Shared(d_20_sharedCacheInput_)
        d_22_valueOrError7_: Wrappers.Result = None
        out7_: Wrappers.Result
        out7_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_15_keyStoreClientRegionWest_, d_1_ttl_, Wrappers.Option_Some(d_21_sharedCache_), Wrappers.Option_None()))
        d_22_valueOrError7_ = out7_
        if not(not((d_22_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(548,29): " + _dafny.string_of(d_22_valueOrError7_))
        d_23_hierarchyKeyring1_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_23_hierarchyKeyring1_ = (d_22_valueOrError7_).Extract()
        d_24_valueOrError8_: Wrappers.Result = None
        out8_: Wrappers.Result
        out8_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_18_keyStoreClientRegionEast_, d_1_ttl_, Wrappers.Option_Some(d_21_sharedCache_), Wrappers.Option_None()))
        d_24_valueOrError8_ = out8_
        if not(not((d_24_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(562,29): " + _dafny.string_of(d_24_valueOrError8_))
        d_25_hierarchyKeyring2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_25_hierarchyKeyring2_ = (d_24_valueOrError8_).Extract()
        d_26_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_ = default__.GetTestMaterials(default__.TEST__ESDK__ALG__SUITE__ID)
        d_26_materials_ = out9_
        d_27_encryptionMaterialsOutMismatchedRegion_: Wrappers.Result
        out10_: Wrappers.Result
        out10_ = (d_25_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_26_materials_))
        d_27_encryptionMaterialsOutMismatchedRegion_ = out10_
        if not((d_27_encryptionMaterialsOutMismatchedRegion_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(583,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        default__.TestRoundtrip(d_23_hierarchyKeyring1_, d_26_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyIdWest_)
        d_28_encryptionMaterialsOutMismatchedRegionFromCache_: Wrappers.Result
        out11_: Wrappers.Result
        out11_ = (d_25_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_26_materials_))
        d_28_encryptionMaterialsOutMismatchedRegionFromCache_ = out11_
        if not((d_28_encryptionMaterialsOutMismatchedRegionFromCache_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(600,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSharedCacheWithDifferentSpecifiedPartitionIdAndSameLogicalKeyStoreName():
        d_0_branchKeyIdWest_: _dafny.Seq
        d_0_branchKeyIdWest_ = default__.BRANCH__KEY__ID
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(608,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_regionWest_: _dafny.Seq
        d_4_regionWest_ = _dafny.Seq("us-west-2")
        d_5_regionEast_: _dafny.Seq
        d_5_regionEast_ = _dafny.Seq("us-east-2")
        d_6_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_4_regionWest_)
        d_6_valueOrError1_ = out1_
        if not(not((d_6_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(613,25): " + _dafny.string_of(d_6_valueOrError1_))
        d_7_kmsClientWest_: ComAmazonawsKmsTypes.IKMSClient
        d_7_kmsClientWest_ = (d_6_valueOrError1_).Extract()
        d_8_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_5_regionEast_)
        d_8_valueOrError2_ = out2_
        if not(not((d_8_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(614,25): " + _dafny.string_of(d_8_valueOrError2_))
        d_9_kmsClientEast_: ComAmazonawsKmsTypes.IKMSClient
        d_9_kmsClientEast_ = (d_8_valueOrError2_).Extract()
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(615,21): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_11_ddbClient_ = (d_10_valueOrError3_).Extract()
        d_12_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_12_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_13_keyStoreConfigClientRegionWest_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_13_keyStoreConfigClientRegionWest_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_7_kmsClientWest_))
        d_14_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = KeyStore.default__.KeyStore(d_13_keyStoreConfigClientRegionWest_)
        d_14_valueOrError4_ = out4_
        if not(not((d_14_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(631,36): " + _dafny.string_of(d_14_valueOrError4_))
        d_15_keyStoreClientRegionWest_: KeyStore.KeyStoreClient
        d_15_keyStoreClientRegionWest_ = (d_14_valueOrError4_).Extract()
        d_16_keyStoreConfigClientRegionEast_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_16_keyStoreConfigClientRegionEast_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, default__.logicalKeyStoreName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_9_kmsClientEast_))
        d_17_valueOrError5_: Wrappers.Result = None
        out5_: Wrappers.Result
        out5_ = KeyStore.default__.KeyStore(d_16_keyStoreConfigClientRegionEast_)
        d_17_valueOrError5_ = out5_
        if not(not((d_17_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(647,36): " + _dafny.string_of(d_17_valueOrError5_))
        d_18_keyStoreClientRegionEast_: KeyStore.KeyStoreClient
        d_18_keyStoreClientRegionEast_ = (d_17_valueOrError5_).Extract()
        d_19_valueOrError6_: Wrappers.Result = None
        out6_: Wrappers.Result
        out6_ = (d_3_mpl_).CreateCryptographicMaterialsCache(AwsCryptographyMaterialProvidersTypes.CreateCryptographicMaterialsCacheInput_CreateCryptographicMaterialsCacheInput(AwsCryptographyMaterialProvidersTypes.CacheType_Default(AwsCryptographyMaterialProvidersTypes.DefaultCache_DefaultCache(100))))
        d_19_valueOrError6_ = out6_
        if not(not((d_19_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(650,28): " + _dafny.string_of(d_19_valueOrError6_))
        d_20_sharedCacheInput_: AwsCryptographyMaterialProvidersTypes.ICryptographicMaterialsCache
        d_20_sharedCacheInput_ = (d_19_valueOrError6_).Extract()
        d_21_sharedCache_: AwsCryptographyMaterialProvidersTypes.CacheType
        d_21_sharedCache_ = AwsCryptographyMaterialProvidersTypes.CacheType_Shared(d_20_sharedCacheInput_)
        d_22_valueOrError7_: Wrappers.Result = None
        out7_: Wrappers.Result
        out7_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_15_keyStoreClientRegionWest_, d_1_ttl_, Wrappers.Option_Some(d_21_sharedCache_), Wrappers.Option_Some(_dafny.Seq("partitionIdHK1"))))
        d_22_valueOrError7_ = out7_
        if not(not((d_22_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(668,29): " + _dafny.string_of(d_22_valueOrError7_))
        d_23_hierarchyKeyring1_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_23_hierarchyKeyring1_ = (d_22_valueOrError7_).Extract()
        d_24_valueOrError8_: Wrappers.Result = None
        out8_: Wrappers.Result
        out8_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_18_keyStoreClientRegionEast_, d_1_ttl_, Wrappers.Option_Some(d_21_sharedCache_), Wrappers.Option_Some(_dafny.Seq("partitionIdHK2"))))
        d_24_valueOrError8_ = out8_
        if not(not((d_24_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(683,29): " + _dafny.string_of(d_24_valueOrError8_))
        d_25_hierarchyKeyring2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_25_hierarchyKeyring2_ = (d_24_valueOrError8_).Extract()
        d_26_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_ = default__.GetTestMaterials(default__.TEST__ESDK__ALG__SUITE__ID)
        d_26_materials_ = out9_
        d_27_encryptionMaterialsOutMismatchedRegion_: Wrappers.Result
        out10_: Wrappers.Result
        out10_ = (d_25_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_26_materials_))
        d_27_encryptionMaterialsOutMismatchedRegion_ = out10_
        if not((d_27_encryptionMaterialsOutMismatchedRegion_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(704,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        default__.TestRoundtrip(d_23_hierarchyKeyring1_, d_26_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyIdWest_)
        d_28_encryptionMaterialsOutMismatchedRegionFromCache_: Wrappers.Result
        out11_: Wrappers.Result
        out11_ = (d_25_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_26_materials_))
        d_28_encryptionMaterialsOutMismatchedRegionFromCache_ = out11_
        if not((d_28_encryptionMaterialsOutMismatchedRegionFromCache_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(718,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSharedCacheWithSamePartitionIdAndDifferentLogicalKeyStoreName():
        d_0_branchKeyIdWest_: _dafny.Seq
        d_0_branchKeyIdWest_ = default__.BRANCH__KEY__ID
        d_1_ttl_: int
        d_1_ttl_ = ((1) * (60000)) * (10)
        d_2_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_2_valueOrError0_ = out0_
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(726,15): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_mpl_: MaterialProviders.MaterialProvidersClient
        d_3_mpl_ = (d_2_valueOrError0_).Extract()
        d_4_regionWest_: _dafny.Seq
        d_4_regionWest_ = _dafny.Seq("us-west-2")
        d_5_regionEast_: _dafny.Seq
        d_5_regionEast_ = _dafny.Seq("us-east-2")
        d_6_valueOrError1_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_4_regionWest_)
        d_6_valueOrError1_ = out1_
        if not(not((d_6_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(731,25): " + _dafny.string_of(d_6_valueOrError1_))
        d_7_kmsClientWest_: ComAmazonawsKmsTypes.IKMSClient
        d_7_kmsClientWest_ = (d_6_valueOrError1_).Extract()
        d_8_valueOrError2_: Wrappers.Result = None
        out2_: Wrappers.Result
        out2_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(d_5_regionEast_)
        d_8_valueOrError2_ = out2_
        if not(not((d_8_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(732,25): " + _dafny.string_of(d_8_valueOrError2_))
        d_9_kmsClientEast_: ComAmazonawsKmsTypes.IKMSClient
        d_9_kmsClientEast_ = (d_8_valueOrError2_).Extract()
        d_10_valueOrError3_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = Com_Amazonaws_Dynamodb.default__.DynamoDBClient()
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(733,21): " + _dafny.string_of(d_10_valueOrError3_))
        d_11_ddbClient_: ComAmazonawsDynamodbTypes.IDynamoDBClient
        d_11_ddbClient_ = (d_10_valueOrError3_).Extract()
        d_12_kmsConfig_: AwsCryptographyKeyStoreTypes.KMSConfiguration
        d_12_kmsConfig_ = AwsCryptographyKeyStoreTypes.KMSConfiguration_kmsKeyArn(default__.keyArn)
        d_13_logicalKeyStoreName_: _dafny.Seq
        d_13_logicalKeyStoreName_ = default__.logicalKeyStoreName
        d_14_logicalKeyStoreNameNew_: _dafny.Seq
        d_14_logicalKeyStoreNameNew_ = (d_13_logicalKeyStoreName_) + (_dafny.Seq("New"))
        d_15_keyStoreConfigClientRegionWest_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_15_keyStoreConfigClientRegionWest_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, d_13_logicalKeyStoreName_, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_7_kmsClientWest_))
        d_16_valueOrError4_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = KeyStore.default__.KeyStore(d_15_keyStoreConfigClientRegionWest_)
        d_16_valueOrError4_ = out4_
        if not(not((d_16_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(753,36): " + _dafny.string_of(d_16_valueOrError4_))
        d_17_keyStoreClientRegionWest_: KeyStore.KeyStoreClient
        d_17_keyStoreClientRegionWest_ = (d_16_valueOrError4_).Extract()
        d_18_keyStoreConfigClientRegionEast_: AwsCryptographyKeyStoreTypes.KeyStoreConfig
        d_18_keyStoreConfigClientRegionEast_ = AwsCryptographyKeyStoreTypes.KeyStoreConfig_KeyStoreConfig(default__.branchKeyStoreName, d_12_kmsConfig_, d_14_logicalKeyStoreNameNew_, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(d_11_ddbClient_), Wrappers.Option_Some(d_9_kmsClientEast_))
        d_19_valueOrError5_: Wrappers.Result = None
        out5_: Wrappers.Result
        out5_ = KeyStore.default__.KeyStore(d_18_keyStoreConfigClientRegionEast_)
        d_19_valueOrError5_ = out5_
        if not(not((d_19_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(770,36): " + _dafny.string_of(d_19_valueOrError5_))
        d_20_keyStoreClientRegionEast_: KeyStore.KeyStoreClient
        d_20_keyStoreClientRegionEast_ = (d_19_valueOrError5_).Extract()
        d_21_valueOrError6_: Wrappers.Result = None
        out6_: Wrappers.Result
        out6_ = (d_3_mpl_).CreateCryptographicMaterialsCache(AwsCryptographyMaterialProvidersTypes.CreateCryptographicMaterialsCacheInput_CreateCryptographicMaterialsCacheInput(AwsCryptographyMaterialProvidersTypes.CacheType_Default(AwsCryptographyMaterialProvidersTypes.DefaultCache_DefaultCache(100))))
        d_21_valueOrError6_ = out6_
        if not(not((d_21_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(773,28): " + _dafny.string_of(d_21_valueOrError6_))
        d_22_sharedCacheInput_: AwsCryptographyMaterialProvidersTypes.ICryptographicMaterialsCache
        d_22_sharedCacheInput_ = (d_21_valueOrError6_).Extract()
        d_23_sharedCache_: AwsCryptographyMaterialProvidersTypes.CacheType
        d_23_sharedCache_ = AwsCryptographyMaterialProvidersTypes.CacheType_Shared(d_22_sharedCacheInput_)
        d_24_valueOrError7_: Wrappers.Result = None
        out7_: Wrappers.Result
        out7_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_17_keyStoreClientRegionWest_, d_1_ttl_, Wrappers.Option_Some(d_23_sharedCache_), Wrappers.Option_Some(_dafny.Seq("partitionId"))))
        d_24_valueOrError7_ = out7_
        if not(not((d_24_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(791,29): " + _dafny.string_of(d_24_valueOrError7_))
        d_25_hierarchyKeyring1_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_25_hierarchyKeyring1_ = (d_24_valueOrError7_).Extract()
        d_26_valueOrError8_: Wrappers.Result = None
        out8_: Wrappers.Result
        out8_ = (d_3_mpl_).CreateAwsKmsHierarchicalKeyring(AwsCryptographyMaterialProvidersTypes.CreateAwsKmsHierarchicalKeyringInput_CreateAwsKmsHierarchicalKeyringInput(Wrappers.Option_Some(d_0_branchKeyIdWest_), Wrappers.Option_None(), d_20_keyStoreClientRegionEast_, d_1_ttl_, Wrappers.Option_Some(d_23_sharedCache_), Wrappers.Option_Some(_dafny.Seq("partitionId"))))
        d_26_valueOrError8_ = out8_
        if not(not((d_26_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(805,29): " + _dafny.string_of(d_26_valueOrError8_))
        d_27_hierarchyKeyring2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_27_hierarchyKeyring2_ = (d_26_valueOrError8_).Extract()
        d_28_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out9_ = default__.GetTestMaterials(default__.TEST__ESDK__ALG__SUITE__ID)
        d_28_materials_ = out9_
        d_29_encryptionMaterialsOutMismatchedRegion_: Wrappers.Result
        out10_: Wrappers.Result
        out10_ = (d_27_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_28_materials_))
        d_29_encryptionMaterialsOutMismatchedRegion_ = out10_
        if not((d_29_encryptionMaterialsOutMismatchedRegion_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(826,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        default__.TestRoundtrip(d_25_hierarchyKeyring1_, d_28_materials_, default__.TEST__ESDK__ALG__SUITE__ID, d_0_branchKeyIdWest_)
        d_30_encryptionMaterialsOutMismatchedRegionFromCache_: Wrappers.Result
        out11_: Wrappers.Result
        out11_ = (d_27_hierarchyKeyring2_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_28_materials_))
        d_30_encryptionMaterialsOutMismatchedRegionFromCache_ = out11_
        if not((d_30_encryptionMaterialsOutMismatchedRegionFromCache_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/AwsKms/AwsKmsHierarchicalKeyring/TestAwsKmsHierarchicalKeyring.dfy(840,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @_dafny.classproperty
    def branchKeyStoreName(instance):
        return Fixtures.default__.branchKeyStoreName
    @_dafny.classproperty
    def logicalKeyStoreName(instance):
        return default__.branchKeyStoreName
    @_dafny.classproperty
    def BRANCH__KEY__ID(instance):
        return Fixtures.default__.branchKeyId
    @_dafny.classproperty
    def BRANCH__KEY__ID__A(instance):
        return default__.BRANCH__KEY__ID
    @_dafny.classproperty
    def keyArn(instance):
        return Fixtures.default__.keyArn
    @_dafny.classproperty
    def TEST__ESDK__ALG__SUITE__ID(instance):
        return AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId_ESDK(AwsCryptographyMaterialProvidersTypes.ESDKAlgorithmSuiteId_ALG__AES__256__GCM__IV12__TAG16__NO__KDF())
    @_dafny.classproperty
    def TEST__DBE__ALG__SUITE__ID(instance):
        return AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId_DBE(AwsCryptographyMaterialProvidersTypes.DBEAlgorithmSuiteId_ALG__AES__256__GCM__HKDF__SHA512__COMMIT__KEY__SYMSIG__HMAC__SHA384())
    @_dafny.classproperty
    def BRANCH__KEY(instance):
        d_0_s_ = _dafny.Seq([98, 114, 97, 110, 99, 104, 75, 101, 121])
        return d_0_s_
    @_dafny.classproperty
    def CASE__A(instance):
        d_0_s_ = _dafny.Seq([99, 97, 115, 101, 65])
        return d_0_s_
    @_dafny.classproperty
    def CASE__B(instance):
        d_0_s_ = _dafny.Seq([99, 97, 115, 101, 66])
        return d_0_s_
    @_dafny.classproperty
    def BRANCH__KEY__ID__B(instance):
        return Fixtures.default__.branchKeyIdWithEC

class DummyBranchKeyIdSupplier(AwsCryptographyMaterialProvidersTypes.IBranchKeyIdSupplier):
    def  __init__(self):
        pass

    def __dafnystr__(self) -> str:
        return "TestAwsKmsHierarchicalKeyring.DummyBranchKeyIdSupplier"
    def GetBranchKeyId(self, input):
        out0_: Wrappers.Result
        out0_ = AwsCryptographyMaterialProvidersTypes.IBranchKeyIdSupplier.GetBranchKeyId(self, input)
        return out0_

    def ctor__(self):
        pass
        pass

    def GetBranchKeyId_k(self, input):
        output: Wrappers.Result = Wrappers.Result.default(AwsCryptographyMaterialProvidersTypes.GetBranchKeyIdOutput.default())()
        d_0_context_: _dafny.Map
        d_0_context_ = (input).encryptionContext
        if ((default__.BRANCH__KEY) in ((d_0_context_).keys)) and (((d_0_context_)[default__.BRANCH__KEY]) == (default__.CASE__A)):
            output = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.GetBranchKeyIdOutput_GetBranchKeyIdOutput(default__.BRANCH__KEY__ID__A))
            return output
        elif ((default__.BRANCH__KEY) in ((d_0_context_).keys)) and (((d_0_context_)[default__.BRANCH__KEY]) == (default__.CASE__B)):
            output = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.GetBranchKeyIdOutput_GetBranchKeyIdOutput(default__.BRANCH__KEY__ID__B))
            return output
        elif True:
            output = Wrappers.Result_Failure(AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Can't determine branchKeyId from context")))
            return output
        return output

