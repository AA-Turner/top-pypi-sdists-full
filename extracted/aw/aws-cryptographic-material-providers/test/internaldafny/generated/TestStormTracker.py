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
import TestAwsKmsHierarchicalKeyring as TestAwsKmsHierarchicalKeyring
import TestAwsKmsEncryptedDataKeyFilter as TestAwsKmsEncryptedDataKeyFilter

# Module: TestStormTracker

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def MakeMat(data):
        return AwsCryptographyMaterialProvidersTypes.Materials_BranchKey(AwsCryptographyKeyStoreTypes.BranchKeyMaterials_BranchKeyMaterials(_dafny.Seq("spoo"), data, _dafny.Map({}), data))

    @staticmethod
    def MakeGet(data):
        return AwsCryptographyMaterialProvidersTypes.GetCacheEntryInput_GetCacheEntryInput(data, Wrappers.Option_None())

    @staticmethod
    def MakeDel(data):
        return AwsCryptographyMaterialProvidersTypes.DeleteCacheEntryInput_DeleteCacheEntryInput(data)

    @staticmethod
    def MakePut(data, expiryTime):
        return AwsCryptographyMaterialProvidersTypes.PutCacheEntryInput_PutCacheEntryInput(data, default__.MakeMat(data), 123456789, _dafny.euclidian_division(expiryTime, 1000), Wrappers.Option_None(), Wrappers.Option_None())

    @staticmethod
    def MakeGetOutput(data, expiryTime):
        return AwsCryptographyMaterialProvidersTypes.GetCacheEntryOutput_GetCacheEntryOutput(default__.MakeMat(data), 123456789, _dafny.euclidian_division(expiryTime, 1000), 1, 0)

    @staticmethod
    def StormTrackerBasics():
        d_0_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        nw0_.ctor__(StormTracker.default__.DefaultStorm())
        d_0_st_ = nw0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out0_: Wrappers.Result
        out0_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.abc), 10000)
        d_1_valueOrError0_ = out0_
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(96,15): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_res_: StormTracker.CacheState
        d_2_res_ = (d_1_valueOrError0_).Extract()
        if not((d_2_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(97,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.abc), 10000)
        d_3_valueOrError1_ = out1_
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(98,11): " + _dafny.string_of(d_3_valueOrError1_))
        d_2_res_ = (d_3_valueOrError1_).Extract()
        if not((d_2_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(99,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_4_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out2_: Wrappers.Result
        out2_ = (d_0_st_).PutCacheEntry(default__.MakePut(default__.abc, 10000))
        d_4_valueOrError2_ = out2_
        if not(not((d_4_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(100,16): " + _dafny.string_of(d_4_valueOrError2_))
        d_5_res2_: tuple
        d_5_res2_ = (d_4_valueOrError2_).Extract()
        d_6_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out3_: Wrappers.Result
        out3_ = (d_0_st_).PutCacheEntry(default__.MakePut(default__.cde, 10000))
        d_6_valueOrError3_ = out3_
        if not(not((d_6_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(101,12): " + _dafny.string_of(d_6_valueOrError3_))
        d_5_res2_ = (d_6_valueOrError3_).Extract()
        d_7_valueOrError4_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out4_: Wrappers.Result
        out4_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.abc), 11000)
        d_7_valueOrError4_ = out4_
        if not(not((d_7_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(107,11): " + _dafny.string_of(d_7_valueOrError4_))
        d_2_res_ = (d_7_valueOrError4_).Extract()
        if not((d_2_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(108,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError5_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out5_: Wrappers.Result
        out5_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.abc), 11000)
        d_8_valueOrError5_ = out5_
        if not(not((d_8_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(109,11): " + _dafny.string_of(d_8_valueOrError5_))
        d_2_res_ = (d_8_valueOrError5_).Extract()
        if not((d_2_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(110,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_res3_: Wrappers.Result
        out6_: Wrappers.Result
        out6_ = (d_0_st_).GetCacheEntry(default__.MakeGet(default__.abc))
        d_9_res3_ = out6_
        out7_: Wrappers.Result
        out7_ = (d_0_st_).GetCacheEntry(default__.MakeGet(default__.abc))
        d_9_res3_ = out7_
        d_10_res4_: Wrappers.Result
        out8_: Wrappers.Result
        out8_ = (d_0_st_).GetFromCache(default__.MakeGet(default__.abc))
        d_10_res4_ = out8_
        out9_: Wrappers.Result
        out9_ = (d_0_st_).GetFromCache(default__.MakeGet(default__.abc))
        d_10_res4_ = out9_
        d_11_res5_: Wrappers.Result
        out10_: Wrappers.Result
        out10_ = (d_0_st_).DeleteCacheEntry(default__.MakeDel(default__.abc))
        d_11_res5_ = out10_
        out11_: Wrappers.Result
        out11_ = (d_0_st_).DeleteCacheEntry(default__.MakeDel(default__.abc))
        d_11_res5_ = out11_

    @staticmethod
    def StormTrackerFanOut():
        d_0_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        def iife0_(_pat_let5_0):
            def iife1_(d_1_dt__update__tmp_h0_):
                def iife2_(_pat_let6_0):
                    def iife3_(d_2_dt__update_hfanOut_h0_):
                        return AwsCryptographyMaterialProvidersTypes.StormTrackingCache_StormTrackingCache((d_1_dt__update__tmp_h0_).entryCapacity, (d_1_dt__update__tmp_h0_).entryPruningTailSize, (d_1_dt__update__tmp_h0_).gracePeriod, (d_1_dt__update__tmp_h0_).graceInterval, d_2_dt__update_hfanOut_h0_, (d_1_dt__update__tmp_h0_).inFlightTTL, (d_1_dt__update__tmp_h0_).sleepMilli, (d_1_dt__update__tmp_h0_).timeUnits)
                    return iife3_(_pat_let6_0)
                return iife2_(3)
            return iife1_(_pat_let5_0)
        nw0_.ctor__(iife0_(StormTracker.default__.DefaultStorm()))
        d_0_st_ = nw0_
        d_3_valueOrError0_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out0_: Wrappers.Result
        out0_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10000)
        d_3_valueOrError0_ = out0_
        if not(not((d_3_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(124,15): " + _dafny.string_of(d_3_valueOrError0_))
        d_4_res_: StormTracker.CacheState
        d_4_res_ = (d_3_valueOrError0_).Extract()
        if not((d_4_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(125,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_5_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.two), 10000)
        d_5_valueOrError1_ = out1_
        if not(not((d_5_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(126,11): " + _dafny.string_of(d_5_valueOrError1_))
        d_4_res_ = (d_5_valueOrError1_).Extract()
        if not((d_4_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(127,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError2_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out2_: Wrappers.Result
        out2_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.three), 10000)
        d_6_valueOrError2_ = out2_
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(128,11): " + _dafny.string_of(d_6_valueOrError2_))
        d_4_res_ = (d_6_valueOrError2_).Extract()
        if not((d_4_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(129,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_7_valueOrError3_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out3_: Wrappers.Result
        out3_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.four), 10000)
        d_7_valueOrError3_ = out3_
        if not(not((d_7_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(130,11): " + _dafny.string_of(d_7_valueOrError3_))
        d_4_res_ = (d_7_valueOrError3_).Extract()
        if not((d_4_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(131,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def StormTrackerPruneTTL():
        d_0_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        def iife0_(_pat_let7_0):
            def iife1_(d_1_dt__update__tmp_h0_):
                def iife2_(_pat_let8_0):
                    def iife3_(d_2_dt__update_hinFlightTTL_h0_):
                        def iife4_(_pat_let9_0):
                            def iife5_(d_3_dt__update_hfanOut_h0_):
                                def iife6_(_pat_let10_0):
                                    def iife7_(d_4_dt__update_hgraceInterval_h0_):
                                        return AwsCryptographyMaterialProvidersTypes.StormTrackingCache_StormTrackingCache((d_1_dt__update__tmp_h0_).entryCapacity, (d_1_dt__update__tmp_h0_).entryPruningTailSize, (d_1_dt__update__tmp_h0_).gracePeriod, d_4_dt__update_hgraceInterval_h0_, d_3_dt__update_hfanOut_h0_, d_2_dt__update_hinFlightTTL_h0_, (d_1_dt__update__tmp_h0_).sleepMilli, (d_1_dt__update__tmp_h0_).timeUnits)
                                    return iife7_(_pat_let10_0)
                                return iife6_(3)
                            return iife5_(_pat_let9_0)
                        return iife4_(3)
                    return iife3_(_pat_let8_0)
                return iife2_(5)
            return iife1_(_pat_let7_0)
        nw0_.ctor__(iife0_(StormTracker.default__.DefaultStorm()))
        d_0_st_ = nw0_
        d_5_valueOrError0_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out0_: Wrappers.Result
        out0_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10000)
        d_5_valueOrError0_ = out0_
        if not(not((d_5_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(137,15): " + _dafny.string_of(d_5_valueOrError0_))
        d_6_res_: StormTracker.CacheState
        d_6_res_ = (d_5_valueOrError0_).Extract()
        if not((d_6_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(138,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_7_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.two), 10000)
        d_7_valueOrError1_ = out1_
        if not(not((d_7_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(139,11): " + _dafny.string_of(d_7_valueOrError1_))
        d_6_res_ = (d_7_valueOrError1_).Extract()
        if not((d_6_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(140,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError2_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out2_: Wrappers.Result
        out2_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.three), 10000)
        d_8_valueOrError2_ = out2_
        if not(not((d_8_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(141,11): " + _dafny.string_of(d_8_valueOrError2_))
        d_6_res_ = (d_8_valueOrError2_).Extract()
        if not((d_6_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(142,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_valueOrError3_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out3_: Wrappers.Result
        out3_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.four), 10000)
        d_9_valueOrError3_ = out3_
        if not(not((d_9_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(143,11): " + _dafny.string_of(d_9_valueOrError3_))
        d_6_res_ = (d_9_valueOrError3_).Extract()
        if not((d_6_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(144,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError4_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out4_: Wrappers.Result
        out4_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.four), 10001)
        d_10_valueOrError4_ = out4_
        if not(not((d_10_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(145,11): " + _dafny.string_of(d_10_valueOrError4_))
        d_6_res_ = (d_10_valueOrError4_).Extract()
        if not((d_6_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(146,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_11_valueOrError5_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out5_: Wrappers.Result
        out5_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.four), 10003)
        d_11_valueOrError5_ = out5_
        if not(not((d_11_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(147,11): " + _dafny.string_of(d_11_valueOrError5_))
        d_6_res_ = (d_11_valueOrError5_).Extract()
        if not((d_6_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(148,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_12_valueOrError6_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out6_: Wrappers.Result
        out6_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.four), 11000)
        d_12_valueOrError6_ = out6_
        if not(not((d_12_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(152,11): " + _dafny.string_of(d_12_valueOrError6_))
        d_6_res_ = (d_12_valueOrError6_).Extract()
        if not((d_6_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(153,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def StormTrackerGraceInterval():
        d_0_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        def iife0_(_pat_let11_0):
            def iife1_(d_1_dt__update__tmp_h0_):
                def iife2_(_pat_let12_0):
                    def iife3_(d_2_dt__update_hgraceInterval_h0_):
                        return AwsCryptographyMaterialProvidersTypes.StormTrackingCache_StormTrackingCache((d_1_dt__update__tmp_h0_).entryCapacity, (d_1_dt__update__tmp_h0_).entryPruningTailSize, (d_1_dt__update__tmp_h0_).gracePeriod, d_2_dt__update_hgraceInterval_h0_, (d_1_dt__update__tmp_h0_).fanOut, (d_1_dt__update__tmp_h0_).inFlightTTL, (d_1_dt__update__tmp_h0_).sleepMilli, (d_1_dt__update__tmp_h0_).timeUnits)
                    return iife3_(_pat_let12_0)
                return iife2_(3)
            return iife1_(_pat_let11_0)
        nw0_.ctor__(iife0_(StormTracker.default__.DefaultStorm()))
        d_0_st_ = nw0_
        d_3_valueOrError0_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out0_: Wrappers.Result
        out0_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10000)
        d_3_valueOrError0_ = out0_
        if not(not((d_3_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(159,15): " + _dafny.string_of(d_3_valueOrError0_))
        d_4_res_: StormTracker.CacheState
        d_4_res_ = (d_3_valueOrError0_).Extract()
        if not((d_4_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(160,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_5_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10000)
        d_5_valueOrError1_ = out1_
        if not(not((d_5_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(161,11): " + _dafny.string_of(d_5_valueOrError1_))
        d_4_res_ = (d_5_valueOrError1_).Extract()
        if not((d_4_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(162,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError2_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out2_: Wrappers.Result
        out2_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10001)
        d_6_valueOrError2_ = out2_
        if not(not((d_6_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(163,11): " + _dafny.string_of(d_6_valueOrError2_))
        d_4_res_ = (d_6_valueOrError2_).Extract()
        if not((d_4_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(164,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_7_valueOrError3_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out3_: Wrappers.Result
        out3_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10002)
        d_7_valueOrError3_ = out3_
        if not(not((d_7_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(165,11): " + _dafny.string_of(d_7_valueOrError3_))
        d_4_res_ = (d_7_valueOrError3_).Extract()
        if not((d_4_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(166,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError4_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out4_: Wrappers.Result
        out4_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10003)
        d_8_valueOrError4_ = out4_
        if not(not((d_8_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(167,11): " + _dafny.string_of(d_8_valueOrError4_))
        d_4_res_ = (d_8_valueOrError4_).Extract()
        if not((d_4_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(168,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def FullStormTrackerGraceInterval():
        d_0_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        def iife0_(_pat_let13_0):
            def iife1_(d_1_dt__update__tmp_h0_):
                def iife2_(_pat_let14_0):
                    def iife3_(d_2_dt__update_hgracePeriod_h0_):
                        def iife4_(_pat_let15_0):
                            def iife5_(d_3_dt__update_hinFlightTTL_h0_):
                                def iife6_(_pat_let16_0):
                                    def iife7_(d_4_dt__update_hgraceInterval_h0_):
                                        return AwsCryptographyMaterialProvidersTypes.StormTrackingCache_StormTrackingCache((d_1_dt__update__tmp_h0_).entryCapacity, (d_1_dt__update__tmp_h0_).entryPruningTailSize, d_2_dt__update_hgracePeriod_h0_, d_4_dt__update_hgraceInterval_h0_, (d_1_dt__update__tmp_h0_).fanOut, d_3_dt__update_hinFlightTTL_h0_, (d_1_dt__update__tmp_h0_).sleepMilli, (d_1_dt__update__tmp_h0_).timeUnits)
                                    return iife7_(_pat_let16_0)
                                return iife6_(2)
                            return iife5_(_pat_let15_0)
                        return iife4_(3)
                    return iife3_(_pat_let14_0)
                return iife2_(5)
            return iife1_(_pat_let13_0)
        nw0_.ctor__(iife0_(StormTracker.default__.DefaultStorm()))
        d_0_st_ = nw0_
        d_5_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out0_: Wrappers.Result
        out0_ = (d_0_st_).PutCacheEntry(default__.MakePut(default__.one, 10000))
        d_5_valueOrError0_ = out0_
        if not(not((d_5_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(178,13): " + _dafny.string_of(d_5_valueOrError0_))
        d_6___v0_: tuple
        d_6___v0_ = (d_5_valueOrError0_).Extract()
        d_7_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (5))
        d_7_valueOrError1_ = out1_
        if not(not((d_7_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(180,15): " + _dafny.string_of(d_7_valueOrError1_))
        d_8_res_: StormTracker.CacheState
        d_8_res_ = (d_7_valueOrError1_).Extract()
        if not((d_8_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(181,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_valueOrError2_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out2_: Wrappers.Result
        out2_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (5))
        d_9_valueOrError2_ = out2_
        if not(not((d_9_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(182,11): " + _dafny.string_of(d_9_valueOrError2_))
        d_8_res_ = (d_9_valueOrError2_).Extract()
        if not((d_8_res_).is_Full):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(183,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError3_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out3_: Wrappers.Result
        out3_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (4))
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(184,11): " + _dafny.string_of(d_10_valueOrError3_))
        d_8_res_ = (d_10_valueOrError3_).Extract()
        if not((d_8_res_).is_Full):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(185,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_11_valueOrError4_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out4_: Wrappers.Result
        out4_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (3))
        d_11_valueOrError4_ = out4_
        if not(not((d_11_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(186,11): " + _dafny.string_of(d_11_valueOrError4_))
        d_8_res_ = (d_11_valueOrError4_).Extract()
        if not((d_8_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(187,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_12_valueOrError5_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out5_: Wrappers.Result
        out5_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (2))
        d_12_valueOrError5_ = out5_
        if not(not((d_12_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(188,11): " + _dafny.string_of(d_12_valueOrError5_))
        d_8_res_ = (d_12_valueOrError5_).Extract()
        if not((d_8_res_).is_Full):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(189,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_13_valueOrError6_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out6_: Wrappers.Result
        out6_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (1))
        d_13_valueOrError6_ = out6_
        if not(not((d_13_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(190,11): " + _dafny.string_of(d_13_valueOrError6_))
        d_8_res_ = (d_13_valueOrError6_).Extract()
        if not((d_8_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(191,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_14_valueOrError7_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out7_: Wrappers.Result
        out7_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (1))
        d_14_valueOrError7_ = out7_
        if not(not((d_14_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(192,11): " + _dafny.string_of(d_14_valueOrError7_))
        d_8_res_ = (d_14_valueOrError7_).Extract()
        if not((d_8_res_).is_Full):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(193,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_15_valueOrError8_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out8_: Wrappers.Result
        out8_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) - (0))
        d_15_valueOrError8_ = out8_
        if not(not((d_15_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(194,11): " + _dafny.string_of(d_15_valueOrError8_))
        d_8_res_ = (d_15_valueOrError8_).Extract()
        if not((d_8_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(196,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_16_valueOrError9_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out9_: Wrappers.Result
        out9_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), (11000) + (1))
        d_16_valueOrError9_ = out9_
        if not(not((d_16_valueOrError9_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(197,11): " + _dafny.string_of(d_16_valueOrError9_))
        d_8_res_ = (d_16_valueOrError9_).Extract()
        if not((d_8_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(199,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def StormTrackerGracePeriod():
        d_0_config_: AwsCryptographyMaterialProvidersTypes.StormTrackingCache
        d_0_config_ = StormTracker.default__.DefaultStorm()
        d_1_expiryTime_: int
        d_1_expiryTime_ = 100100
        d_2_beforeGracePeriod_: int
        d_2_beforeGracePeriod_ = ((d_1_expiryTime_) - ((d_0_config_).gracePeriod)) - (1000)
        d_3_insideGracePeriod_: int
        d_3_insideGracePeriod_ = ((d_1_expiryTime_) - ((d_0_config_).gracePeriod)) + (1)
        d_4_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        nw0_.ctor__(d_0_config_)
        d_4_st_ = nw0_
        d_5_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out0_: Wrappers.Result
        out0_ = (d_4_st_).PutCacheEntry(default__.MakePut(default__.one, d_1_expiryTime_))
        d_5_valueOrError0_ = out0_
        if not(not((d_5_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(214,16): " + _dafny.string_of(d_5_valueOrError0_))
        d_6_res2_: tuple
        d_6_res2_ = (d_5_valueOrError0_).Extract()
        d_7_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_4_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), d_2_beforeGracePeriod_)
        d_7_valueOrError1_ = out1_
        if not(not((d_7_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(216,15): " + _dafny.string_of(d_7_valueOrError1_))
        d_8_res_: StormTracker.CacheState
        d_8_res_ = (d_7_valueOrError1_).Extract()
        if not((d_8_res_).is_Full):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(217,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_valueOrError2_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out2_: Wrappers.Result
        out2_ = (d_4_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), d_3_insideGracePeriod_)
        d_9_valueOrError2_ = out2_
        if not(not((d_9_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(218,11): " + _dafny.string_of(d_9_valueOrError2_))
        d_8_res_ = (d_9_valueOrError2_).Extract()
        if not((d_8_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(219,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError3_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out3_: Wrappers.Result
        out3_ = (d_4_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), d_3_insideGracePeriod_)
        d_10_valueOrError3_ = out3_
        if not(not((d_10_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(220,11): " + _dafny.string_of(d_10_valueOrError3_))
        d_8_res_ = (d_10_valueOrError3_).Extract()
        if not((d_8_res_).is_Full):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(221,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def EmptyStormTrackerTLLAndInterval():
        d_0_st_: StormTracker.StormTracker
        nw0_ = StormTracker.StormTracker()
        def iife0_(_pat_let17_0):
            def iife1_(d_1_dt__update__tmp_h0_):
                def iife2_(_pat_let18_0):
                    def iife3_(d_2_dt__update_hinFlightTTL_h0_):
                        def iife4_(_pat_let19_0):
                            def iife5_(d_3_dt__update_hgraceInterval_h0_):
                                return AwsCryptographyMaterialProvidersTypes.StormTrackingCache_StormTrackingCache((d_1_dt__update__tmp_h0_).entryCapacity, (d_1_dt__update__tmp_h0_).entryPruningTailSize, (d_1_dt__update__tmp_h0_).gracePeriod, d_3_dt__update_hgraceInterval_h0_, (d_1_dt__update__tmp_h0_).fanOut, d_2_dt__update_hinFlightTTL_h0_, (d_1_dt__update__tmp_h0_).sleepMilli, (d_1_dt__update__tmp_h0_).timeUnits)
                            return iife5_(_pat_let19_0)
                        return iife4_(2)
                    return iife3_(_pat_let18_0)
                return iife2_(3)
            return iife1_(_pat_let17_0)
        nw0_.ctor__(iife0_(StormTracker.default__.DefaultStorm()))
        d_0_st_ = nw0_
        d_4_valueOrError0_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out0_: Wrappers.Result
        out0_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10000)
        d_4_valueOrError0_ = out0_
        if not(not((d_4_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(232,15): " + _dafny.string_of(d_4_valueOrError0_))
        d_5_res_: StormTracker.CacheState
        d_5_res_ = (d_4_valueOrError0_).Extract()
        if not((d_5_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(233,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError1_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out1_: Wrappers.Result
        out1_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10000)
        d_6_valueOrError1_ = out1_
        if not(not((d_6_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(234,11): " + _dafny.string_of(d_6_valueOrError1_))
        d_5_res_ = (d_6_valueOrError1_).Extract()
        if not((d_5_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(235,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_7_valueOrError2_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out2_: Wrappers.Result
        out2_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10001)
        d_7_valueOrError2_ = out2_
        if not(not((d_7_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(236,11): " + _dafny.string_of(d_7_valueOrError2_))
        d_5_res_ = (d_7_valueOrError2_).Extract()
        if not((d_5_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(237,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError3_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out3_: Wrappers.Result
        out3_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10002)
        d_8_valueOrError3_ = out3_
        if not(not((d_8_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(238,11): " + _dafny.string_of(d_8_valueOrError3_))
        d_5_res_ = (d_8_valueOrError3_).Extract()
        if not((d_5_res_).is_EmptyFetch):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(239,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_9_valueOrError4_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out4_: Wrappers.Result
        out4_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10002)
        d_9_valueOrError4_ = out4_
        if not(not((d_9_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(240,11): " + _dafny.string_of(d_9_valueOrError4_))
        d_5_res_ = (d_9_valueOrError4_).Extract()
        if not((d_5_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(241,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError5_: Wrappers.Result = Wrappers.Result.default(StormTracker.CacheState.default())()
        out5_: Wrappers.Result
        out5_ = (d_0_st_).GetFromCacheWithTime(default__.MakeGet(default__.one), 10003)
        d_10_valueOrError5_ = out5_
        if not(not((d_10_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(242,11): " + _dafny.string_of(d_10_valueOrError5_))
        d_5_res_ = (d_10_valueOrError5_).Extract()
        if not((d_5_res_).is_EmptyWait):
            raise _dafny.HaltException("dafny/AwsCryptographicMaterialProviders/test/CMCs/StormTracker.dfy(243,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @_dafny.classproperty
    def abc(instance):
        d_0_s_ = _dafny.Seq([97, 98, 99])
        return d_0_s_
    @_dafny.classproperty
    def cde(instance):
        d_0_s_ = _dafny.Seq([99, 100, 101])
        return d_0_s_
    @_dafny.classproperty
    def one(instance):
        d_0_s_ = _dafny.Seq([111, 110, 101])
        return d_0_s_
    @_dafny.classproperty
    def two(instance):
        d_0_s_ = _dafny.Seq([116, 119, 111])
        return d_0_s_
    @_dafny.classproperty
    def three(instance):
        d_0_s_ = _dafny.Seq([116, 104, 114, 101, 101])
        return d_0_s_
    @_dafny.classproperty
    def four(instance):
        d_0_s_ = _dafny.Seq([102, 111, 117, 114])
        return d_0_s_
