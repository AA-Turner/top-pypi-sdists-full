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

# Module: TestMultiKeyring

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def getInputEncryptionMaterials(encryptionContext):
        res: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials = None
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(20,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_algorithmSuiteId_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId
        d_2_algorithmSuiteId_ = AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId_ESDK(AwsCryptographyMaterialProvidersTypes.ESDKAlgorithmSuiteId_ALG__AES__256__GCM__IV12__TAG16__NO__KDF())
        d_3_valueOrError1_: Wrappers.Result = None
        d_3_valueOrError1_ = (d_1_mpl_).InitializeEncryptionMaterials(AwsCryptographyMaterialProvidersTypes.InitializeEncryptionMaterialsInput_InitializeEncryptionMaterialsInput(d_2_algorithmSuiteId_, encryptionContext, _dafny.Seq([]), Wrappers.Option_None(), Wrappers.Option_None()))
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(23,33): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_encryptionMaterialsIn_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        d_4_encryptionMaterialsIn_ = (d_3_valueOrError1_).Extract()
        res = d_4_encryptionMaterialsIn_
        return res
        return res

    @staticmethod
    def getInputDecryptionMaterials(encryptionContext):
        res: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials = None
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(37,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_algorithmSuiteId_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId
        d_2_algorithmSuiteId_ = AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId_ESDK(AwsCryptographyMaterialProvidersTypes.ESDKAlgorithmSuiteId_ALG__AES__256__GCM__IV12__TAG16__NO__KDF())
        d_3_valueOrError1_: Wrappers.Result = None
        d_3_valueOrError1_ = (d_1_mpl_).InitializeDecryptionMaterials(AwsCryptographyMaterialProvidersTypes.InitializeDecryptionMaterialsInput_InitializeDecryptionMaterialsInput(d_2_algorithmSuiteId_, encryptionContext, _dafny.Seq([])))
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(40,33): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_decryptionMaterialsIn_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_4_decryptionMaterialsIn_ = (d_3_valueOrError1_).Extract()
        res = d_4_decryptionMaterialsIn_
        return res
        return res

    @staticmethod
    def TestHappyCase():
        d_0_time_: Time.AbsoluteTime
        out0_: Time.AbsoluteTime
        out0_ = Time.default__.GetAbsoluteTime()
        d_0_time_ = out0_
        d_1_valueOrError0_: Wrappers.Result = None
        out1_: Wrappers.Result
        out1_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_1_valueOrError0_ = out1_
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(53,15): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_mpl_: MaterialProviders.MaterialProvidersClient
        d_2_mpl_ = (d_1_valueOrError0_).Extract()
        d_3_encryptionContext_: _dafny.Map
        out2_: _dafny.Map
        out2_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_3_encryptionContext_ = out2_
        d_4_encryptionMaterials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out3_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out3_ = default__.getInputEncryptionMaterials(d_3_encryptionContext_)
        d_4_encryptionMaterials_ = out3_
        d_5_decryptionMaterials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        out4_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        out4_ = default__.getInputDecryptionMaterials(d_3_encryptionContext_)
        d_5_decryptionMaterials_ = out4_
        d_6_rawAESKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out5_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out5_ = default__.setupRawAesKeyring(d_3_encryptionContext_)
        d_6_rawAESKeyring_ = out5_
        d_7_expectedEncryptionMaterials_: Wrappers.Result
        out6_: Wrappers.Result
        out6_ = (d_6_rawAESKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_4_encryptionMaterials_))
        d_7_expectedEncryptionMaterials_ = out6_
        if not((d_7_expectedEncryptionMaterials_).is_Success):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(65,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_expectedPlaintextDataKey_: Wrappers.Option
        d_8_expectedPlaintextDataKey_ = (((d_7_expectedEncryptionMaterials_).value).materials).plaintextDataKey
        if not((d_8_expectedPlaintextDataKey_).is_Some):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(67,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_staticKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out7_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out7_ = default__.SetupStaticKeyring(Wrappers.Option_Some(((d_7_expectedEncryptionMaterials_).value).materials), Wrappers.Option_None())
        d_9_staticKeyring_ = out7_
        d_10_valueOrError1_: Wrappers.Result = None
        out8_: Wrappers.Result
        out8_ = (d_2_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_Some(d_9_staticKeyring_), _dafny.Seq([d_6_rawAESKeyring_])))
        d_10_valueOrError1_ = out8_
        if not(not((d_10_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(71,24): " + _dafny.string_of(d_10_valueOrError1_))
        d_11_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_11_multiKeyring_ = (d_10_valueOrError1_).Extract()
        d_12_valueOrError2_: Wrappers.Result = None
        out9_: Wrappers.Result
        out9_ = (d_11_multiKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_4_encryptionMaterials_))
        d_12_valueOrError2_ = out9_
        if not(not((d_12_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(76,34): " + _dafny.string_of(d_12_valueOrError2_))
        d_13_encryptionMaterialsOut_: AwsCryptographyMaterialProvidersTypes.OnEncryptOutput
        d_13_encryptionMaterialsOut_ = (d_12_valueOrError2_).Extract()
        d_14_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        d_14_valueOrError3_ = (d_2_mpl_).EncryptionMaterialsHasPlaintextDataKey((d_13_encryptionMaterialsOut_).materials)
        if not(not((d_14_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(78,13): " + _dafny.string_of(d_14_valueOrError3_))
        d_15___v0_: tuple
        d_15___v0_ = (d_14_valueOrError3_).Extract()
        if not(((((d_13_encryptionMaterialsOut_).materials).plaintextDataKey).value) == ((d_8_expectedPlaintextDataKey_).value)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(89,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((len(((d_13_encryptionMaterialsOut_).materials).encryptedDataKeys)) == (2)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(103,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out10_: Time.AbsoluteTime
        out10_ = Time.default__.PrintTimeSinceShortChained(d_0_time_)
        d_0_time_ = out10_
        hi0_ = 100
        for d_16_i_ in range(0, hi0_):
            d_17_valueOrError4_: Wrappers.Result = None
            out11_: Wrappers.Result
            out11_ = (d_11_multiKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_4_encryptionMaterials_))
            d_17_valueOrError4_ = out11_
            if not(not((d_17_valueOrError4_).IsFailure())):
                raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(107,32): " + _dafny.string_of(d_17_valueOrError4_))
            d_13_encryptionMaterialsOut_ = (d_17_valueOrError4_).Extract()
        Time.default__.PrintTimeSinceShort(d_0_time_)

    @staticmethod
    def TestChildKeyringFailureEncrypt():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(114,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_rawAESKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_ = default__.setupRawAesKeyring(d_2_encryptionContext_)
        d_3_rawAESKeyring_ = out2_
        d_4_failingKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out3_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out3_ = default__.SetupFailingKeyring()
        d_4_failingKeyring_ = out3_
        d_5_valueOrError1_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_1_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_Some(d_3_rawAESKeyring_), _dafny.Seq([d_4_failingKeyring_])))
        d_5_valueOrError1_ = out4_
        if not(not((d_5_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(124,24): " + _dafny.string_of(d_5_valueOrError1_))
        d_6_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_6_multiKeyring_ = (d_5_valueOrError1_).Extract()
        d_7_encryptionMaterials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_ = default__.getInputEncryptionMaterials(d_2_encryptionContext_)
        d_7_encryptionMaterials_ = out5_
        d_8_result_: Wrappers.Result
        out6_: Wrappers.Result
        out6_ = (d_6_multiKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_7_encryptionMaterials_))
        d_8_result_ = out6_
        if not((d_8_result_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(132,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestGeneratorKeyringFails():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(137,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_failingKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_ = default__.SetupFailingKeyring()
        d_3_failingKeyring_ = out2_
        d_4_rawAESKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out3_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out3_ = default__.setupRawAesKeyring(d_2_encryptionContext_)
        d_4_rawAESKeyring_ = out3_
        d_5_valueOrError1_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_1_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_Some(d_3_failingKeyring_), _dafny.Seq([d_4_rawAESKeyring_])))
        d_5_valueOrError1_ = out4_
        if not(not((d_5_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(150,24): " + _dafny.string_of(d_5_valueOrError1_))
        d_6_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_6_multiKeyring_ = (d_5_valueOrError1_).Extract()
        d_7_encryptionMaterials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out5_ = default__.getInputEncryptionMaterials(d_2_encryptionContext_)
        d_7_encryptionMaterials_ = out5_
        d_8_result_: Wrappers.Result
        out6_: Wrappers.Result
        out6_ = (d_6_multiKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_7_encryptionMaterials_))
        d_8_result_ = out6_
        if not((d_8_result_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(158,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestGeneratorKeyringDoesNotReturnPlaintextDataKey():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(163,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_encryptionMaterials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out2_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out2_ = default__.getInputEncryptionMaterials(d_2_encryptionContext_)
        d_3_encryptionMaterials_ = out2_
        d_4_failingKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out3_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out3_ = default__.SetupStaticKeyring(Wrappers.Option_Some(d_3_encryptionMaterials_), Wrappers.Option_None())
        d_4_failingKeyring_ = out3_
        d_5_valueOrError1_: Wrappers.Result = None
        out4_: Wrappers.Result
        out4_ = (d_1_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_Some(d_4_failingKeyring_), _dafny.Seq([])))
        d_5_valueOrError1_ = out4_
        if not(not((d_5_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(173,24): " + _dafny.string_of(d_5_valueOrError1_))
        d_6_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_6_multiKeyring_ = (d_5_valueOrError1_).Extract()
        d_7_result_: Wrappers.Result
        out5_: Wrappers.Result
        out5_ = (d_6_multiKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_3_encryptionMaterials_))
        d_7_result_ = out5_
        if not((d_7_result_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(179,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestGeneratorAbleToDecrypt():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(184,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_rawAESKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_ = default__.setupRawAesKeyring(d_2_encryptionContext_)
        d_3_rawAESKeyring_ = out2_
        d_4_inputEncryptionMaterials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out3_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out3_ = default__.getInputEncryptionMaterials(d_2_encryptionContext_)
        d_4_inputEncryptionMaterials_ = out3_
        d_5_encryptionMaterials_: Wrappers.Result
        out4_: Wrappers.Result
        out4_ = (d_3_rawAESKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_4_inputEncryptionMaterials_))
        d_5_encryptionMaterials_ = out4_
        if not((d_5_encryptionMaterials_).is_Success):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(198,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_inputDecryptionMaterials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        out5_ = default__.getInputDecryptionMaterials(d_2_encryptionContext_)
        d_6_inputDecryptionMaterials_ = out5_
        d_7_failingKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out6_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out6_ = default__.SetupFailingKeyring()
        d_7_failingKeyring_ = out6_
        d_8_valueOrError1_: Wrappers.Result = None
        out7_: Wrappers.Result
        out7_ = (d_1_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_Some(d_3_rawAESKeyring_), _dafny.Seq([d_7_failingKeyring_])))
        d_8_valueOrError1_ = out7_
        if not(not((d_8_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(204,24): " + _dafny.string_of(d_8_valueOrError1_))
        d_9_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_9_multiKeyring_ = (d_8_valueOrError1_).Extract()
        d_10_onDecryptInput_: AwsCryptographyMaterialProvidersTypes.OnDecryptInput
        d_10_onDecryptInput_ = AwsCryptographyMaterialProvidersTypes.OnDecryptInput_OnDecryptInput(d_6_inputDecryptionMaterials_, (((d_5_encryptionMaterials_).value).materials).encryptedDataKeys)
        d_11_decryptionMaterials_: Wrappers.Result
        out8_: Wrappers.Result
        out8_ = (d_9_multiKeyring_).OnDecrypt(d_10_onDecryptInput_)
        d_11_decryptionMaterials_ = out8_
        if not((d_11_decryptionMaterials_).is_Success):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(214,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((((d_11_decryptionMaterials_).value).materials).plaintextDataKey) == ((((d_5_encryptionMaterials_).value).materials).plaintextDataKey)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(215,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestGeneratorUnableToDecrypt():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(220,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_rawAESKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_ = default__.setupRawAesKeyring(d_2_encryptionContext_)
        d_3_rawAESKeyring_ = out2_
        d_4_inputEncryptionMaterials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out3_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        out3_ = default__.getInputEncryptionMaterials(d_2_encryptionContext_)
        d_4_inputEncryptionMaterials_ = out3_
        d_5_encryptionMaterials_: Wrappers.Result
        out4_: Wrappers.Result
        out4_ = (d_3_rawAESKeyring_).OnEncrypt(AwsCryptographyMaterialProvidersTypes.OnEncryptInput_OnEncryptInput(d_4_inputEncryptionMaterials_))
        d_5_encryptionMaterials_ = out4_
        if not((d_5_encryptionMaterials_).is_Success):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(245,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_inputDecryptionMaterials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        out5_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        out5_ = default__.getInputDecryptionMaterials(d_2_encryptionContext_)
        d_6_inputDecryptionMaterials_ = out5_
        d_7_failingKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out6_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out6_ = default__.SetupFailingKeyring()
        d_7_failingKeyring_ = out6_
        d_8_valueOrError1_: Wrappers.Result = None
        out7_: Wrappers.Result
        out7_ = (d_1_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_Some(d_7_failingKeyring_), _dafny.Seq([d_7_failingKeyring_, d_3_rawAESKeyring_, d_7_failingKeyring_])))
        d_8_valueOrError1_ = out7_
        if not(not((d_8_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(253,24): " + _dafny.string_of(d_8_valueOrError1_))
        d_9_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_9_multiKeyring_ = (d_8_valueOrError1_).Extract()
        d_10_onDecryptInput_: AwsCryptographyMaterialProvidersTypes.OnDecryptInput
        d_10_onDecryptInput_ = AwsCryptographyMaterialProvidersTypes.OnDecryptInput_OnDecryptInput(d_6_inputDecryptionMaterials_, (((d_5_encryptionMaterials_).value).materials).encryptedDataKeys)
        d_11_decryptionMaterials_: Wrappers.Result
        out8_: Wrappers.Result
        out8_ = (d_9_multiKeyring_).OnDecrypt(d_10_onDecryptInput_)
        d_11_decryptionMaterials_ = out8_
        if not((d_11_decryptionMaterials_).is_Success):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(273,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((((d_11_decryptionMaterials_).value).materials).plaintextDataKey) == ((((d_5_encryptionMaterials_).value).materials).plaintextDataKey)):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(274,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestCollectFailuresDecrypt():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(280,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_encryptionContext_: _dafny.Map
        out1_: _dafny.Map
        out1_ = TestUtils.default__.SmallEncryptionContext(TestUtils.SmallEncryptionContextVariation_A())
        d_2_encryptionContext_ = out1_
        d_3_failingKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_: AwsCryptographyMaterialProvidersTypes.IKeyring
        out2_ = default__.SetupFailingKeyring()
        d_3_failingKeyring_ = out2_
        d_4_valueOrError1_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = (d_1_mpl_).CreateMultiKeyring(AwsCryptographyMaterialProvidersTypes.CreateMultiKeyringInput_CreateMultiKeyringInput(Wrappers.Option_None(), _dafny.Seq([d_3_failingKeyring_, d_3_failingKeyring_])))
        d_4_valueOrError1_ = out3_
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(299,24): " + _dafny.string_of(d_4_valueOrError1_))
        d_5_multiKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_5_multiKeyring_ = (d_4_valueOrError1_).Extract()
        d_6_valueOrError2_: Wrappers.Result = None
        d_6_valueOrError2_ = (d_1_mpl_).InitializeDecryptionMaterials(AwsCryptographyMaterialProvidersTypes.InitializeDecryptionMaterialsInput_InitializeDecryptionMaterialsInput(AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteId_ESDK(AwsCryptographyMaterialProvidersTypes.ESDKAlgorithmSuiteId_ALG__AES__256__GCM__IV12__TAG16__NO__KDF()), d_2_encryptionContext_, _dafny.Seq([])))
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(304,21): " + _dafny.string_of(d_6_valueOrError2_))
        d_7_materials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_7_materials_ = (d_6_valueOrError2_).Extract()
        d_8_result_: Wrappers.Result
        out4_: Wrappers.Result
        out4_ = (d_5_multiKeyring_).OnDecrypt(AwsCryptographyMaterialProvidersTypes.OnDecryptInput_OnDecryptInput(d_7_materials_, _dafny.Seq([])))
        d_8_result_ = out4_
        if not((d_8_result_).IsFailure()):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(313,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def setupRawAesKeyring(encryptionContext):
        res: AwsCryptographyMaterialProvidersTypes.IKeyring = None
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = MaterialProviders.default__.MaterialProviders(MaterialProviders.default__.DefaultMaterialProvidersConfig())
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(321,15): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_mpl_: MaterialProviders.MaterialProvidersClient
        d_1_mpl_ = (d_0_valueOrError0_).Extract()
        d_2_namespace_: _dafny.Seq
        d_3_name_: _dafny.Seq
        out1_: _dafny.Seq
        out2_: _dafny.Seq
        out1_, out2_ = TestUtils.default__.NamespaceAndName(0)
        d_2_namespace_ = out1_
        d_3_name_ = out2_
        d_4_valueOrError1_: Wrappers.Result = None
        out3_: Wrappers.Result
        out3_ = (d_1_mpl_).CreateRawAesKeyring(AwsCryptographyMaterialProvidersTypes.CreateRawAesKeyringInput_CreateRawAesKeyringInput(d_2_namespace_, d_3_name_, _dafny.Seq([0 for d_5_i_ in range(32)]), AwsCryptographyMaterialProvidersTypes.AesWrappingAlg_ALG__AES256__GCM__IV12__TAG16()))
        d_4_valueOrError1_ = out3_
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/Keyrings/TestMultiKeyring.dfy(324,25): " + _dafny.string_of(d_4_valueOrError1_))
        d_6_rawAESKeyring_: AwsCryptographyMaterialProvidersTypes.IKeyring
        d_6_rawAESKeyring_ = (d_4_valueOrError1_).Extract()
        res = d_6_rawAESKeyring_
        return res
        return res

    @staticmethod
    def SetupStaticKeyring(encryptionMaterials, decryptionMaterials):
        res: AwsCryptographyMaterialProvidersTypes.IKeyring = None
        nw0_ = StaticKeyring()
        nw0_.ctor__(encryptionMaterials, decryptionMaterials)
        res = nw0_
        return res
        return res

    @staticmethod
    def SetupFailingKeyring():
        res: AwsCryptographyMaterialProvidersTypes.IKeyring = None
        nw0_ = FailingKeyring()
        nw0_.ctor__()
        res = nw0_
        return res
        return res


class StaticKeyring(AwsCryptographyMaterialProvidersTypes.IKeyring):
    def  __init__(self):
        self._encryptionMaterials: Wrappers.Option = Wrappers.Option.default()()
        self._decryptionMaterials: Wrappers.Option = Wrappers.Option.default()()
        pass

    def __dafnystr__(self) -> str:
        return "TestMultiKeyring.StaticKeyring"
    def OnDecrypt(self, input):
        out0_: Wrappers.Result
        out0_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnDecrypt(self, input)
        return out0_

    def OnEncrypt(self, input):
        out0_: Wrappers.Result
        out0_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnEncrypt(self, input)
        return out0_

    def ctor__(self, encryptionMaterials, decryptionMaterials):
        (self)._encryptionMaterials = encryptionMaterials
        (self)._decryptionMaterials = decryptionMaterials

    def OnEncrypt_k(self, input):
        res: Wrappers.Result = None
        if ((self).encryptionMaterials).is_Some:
            res = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnEncryptOutput_OnEncryptOutput(((self).encryptionMaterials).value))
            return res
        elif True:
            d_0_exception_: AwsCryptographyMaterialProvidersTypes.Error
            d_0_exception_ = AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Failure"))
            res = Wrappers.Result_Failure(d_0_exception_)
            return res
        return res

    def OnDecrypt_k(self, input):
        res: Wrappers.Result = None
        if ((self).decryptionMaterials).is_Some:
            res = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnDecryptOutput_OnDecryptOutput(((self).decryptionMaterials).value))
            return res
        elif True:
            d_0_exception_: AwsCryptographyMaterialProvidersTypes.Error
            d_0_exception_ = AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Failure"))
            res = Wrappers.Result_Failure(d_0_exception_)
            return res
        return res

    @property
    def encryptionMaterials(self):
        return self._encryptionMaterials
    @property
    def decryptionMaterials(self):
        return self._decryptionMaterials

class FailingKeyring(AwsCryptographyMaterialProvidersTypes.IKeyring):
    def  __init__(self):
        pass

    def __dafnystr__(self) -> str:
        return "TestMultiKeyring.FailingKeyring"
    def OnDecrypt(self, input):
        out1_: Wrappers.Result
        out1_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnDecrypt(self, input)
        return out1_

    def OnEncrypt(self, input):
        out1_: Wrappers.Result
        out1_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnEncrypt(self, input)
        return out1_

    def ctor__(self):
        pass
        pass

    def OnEncrypt_k(self, input):
        res: Wrappers.Result = None
        d_0_exception_: AwsCryptographyMaterialProvidersTypes.Error
        d_0_exception_ = AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Failure"))
        res = Wrappers.Result_Failure(d_0_exception_)
        return res
        return res

    def OnDecrypt_k(self, input):
        res: Wrappers.Result = None
        d_0_exception_: AwsCryptographyMaterialProvidersTypes.Error
        d_0_exception_ = AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Failure"))
        res = Wrappers.Result_Failure(d_0_exception_)
        return res
        return res

