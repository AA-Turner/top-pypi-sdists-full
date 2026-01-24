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

# Module: CleanupItems

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def DeleteVersion(branchKeyIdentifier, branchKeyVersion, ddbClient):
        d_0___v0_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (ddbClient).DeleteItem(ComAmazonawsDynamodbTypes.DeleteItemInput_DeleteItemInput(Fixtures.default__.branchKeyStoreName, _dafny.Map({Structure.default__.BRANCH__KEY__IDENTIFIER__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S(branchKeyIdentifier), Structure.default__.TYPE__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S((Structure.default__.BRANCH__KEY__TYPE__PREFIX) + (branchKeyVersion))}), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))
        d_0___v0_ = out0_

    @staticmethod
    def DeleteActive(branchKeyIdentifier, ddbClient):
        d_0___v1_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (ddbClient).DeleteItem(ComAmazonawsDynamodbTypes.DeleteItemInput_DeleteItemInput(Fixtures.default__.branchKeyStoreName, _dafny.Map({Structure.default__.BRANCH__KEY__IDENTIFIER__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S(branchKeyIdentifier), Structure.default__.TYPE__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S(Structure.default__.BRANCH__KEY__ACTIVE__TYPE)}), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))
        d_0___v1_ = out0_
        d_1___v2_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (ddbClient).DeleteItem(ComAmazonawsDynamodbTypes.DeleteItemInput_DeleteItemInput(Fixtures.default__.branchKeyStoreName, _dafny.Map({Structure.default__.BRANCH__KEY__IDENTIFIER__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S(branchKeyIdentifier), Structure.default__.TYPE__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S(Structure.default__.BEACON__KEY__TYPE__VALUE)}), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))
        d_1___v2_ = out1_

    @staticmethod
    def DeleteBranchKey(Identifier, tableName, ddbClient):
        output: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.bool)()
        d_0_ExpressionAttributeNames_: _dafny.Map
        d_0_ExpressionAttributeNames_ = _dafny.Map({_dafny.Seq("#pk"): Structure.default__.BRANCH__KEY__IDENTIFIER__FIELD})
        d_1_ExpressionAttributeValues_: _dafny.Map
        d_1_ExpressionAttributeValues_ = _dafny.Map({_dafny.Seq(":pk"): ComAmazonawsDynamodbTypes.AttributeValue_S(Identifier)})
        d_2_queryReq_: ComAmazonawsDynamodbTypes.QueryInput
        d_2_queryReq_ = ComAmazonawsDynamodbTypes.QueryInput_QueryInput(tableName, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(_dafny.Seq("#pk = :pk")), Wrappers.Option_Some(d_0_ExpressionAttributeNames_), Wrappers.Option_Some(d_1_ExpressionAttributeValues_))
        d_3_valueOrError0_: Wrappers.Result = Wrappers.Result.default(ComAmazonawsDynamodbTypes.QueryOutput.default())()
        out0_: Wrappers.Result
        out0_ = (ddbClient).Query(d_2_queryReq_)
        d_3_valueOrError0_ = out0_
        if (d_3_valueOrError0_).IsFailure():
            output = (d_3_valueOrError0_).PropagateFailure()
            return output
        d_4_queryRes_: ComAmazonawsDynamodbTypes.QueryOutput
        d_4_queryRes_ = (d_3_valueOrError0_).Extract()
        if ((d_4_queryRes_).Items).is_None:
            output = Wrappers.Result_Success(True)
            return output
        d_5_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        def lambda0_(d_6_Identifier_, d_7_tableName_):
            def lambda1_(d_8_item_):
                def iife0_(_pat_let2_0):
                    def iife1_(d_9_valueOrError1_):
                        return ((d_9_valueOrError1_).PropagateFailure() if (d_9_valueOrError1_).IsFailure() else Wrappers.Result_Success(ComAmazonawsDynamodbTypes.TransactWriteItem_TransactWriteItem(Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(ComAmazonawsDynamodbTypes.Delete_Delete(_dafny.Map({Structure.default__.BRANCH__KEY__IDENTIFIER__FIELD: ComAmazonawsDynamodbTypes.AttributeValue_S(d_6_Identifier_), Structure.default__.TYPE__FIELD: (d_8_item_)[Structure.default__.TYPE__FIELD]}), d_7_tableName_, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None())), Wrappers.Option_None())))
                    return iife1_(_pat_let2_0)
                return iife0_(Wrappers.default__.Need((Structure.default__.TYPE__FIELD) in (d_8_item_), ComAmazonawsDynamodbTypes.Error_InternalServerError(Wrappers.Option_Some(default__.NOT__BK__ERR__MSG))))

            return lambda1_

        d_5_valueOrError2_ = Seq.default__.MapWithResult(lambda0_(Identifier, tableName), ((d_4_queryRes_).Items).value)
        if (d_5_valueOrError2_).IsFailure():
            output = (d_5_valueOrError2_).PropagateFailure()
            return output
        d_10_deleteItems_: _dafny.Seq
        d_10_deleteItems_ = (d_5_valueOrError2_).Extract()
        if (0) == (len(d_10_deleteItems_)):
            output = Wrappers.Result_Success(True)
            return output
        if (100) < (len(d_10_deleteItems_)):
            d_10_deleteItems_ = _dafny.Seq((d_10_deleteItems_)[:100:])
        d_11_deleteReq_: ComAmazonawsDynamodbTypes.TransactWriteItemsInput
        d_11_deleteReq_ = ComAmazonawsDynamodbTypes.TransactWriteItemsInput_TransactWriteItemsInput(d_10_deleteItems_, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None())
        d_12_valueOrError3_: Wrappers.Result = Wrappers.Result.default(ComAmazonawsDynamodbTypes.TransactWriteItemsOutput.default())()
        out1_: Wrappers.Result
        out1_ = (ddbClient).TransactWriteItems(d_11_deleteReq_)
        d_12_valueOrError3_ = out1_
        if (d_12_valueOrError3_).IsFailure():
            output = (d_12_valueOrError3_).PropagateFailure()
            return output
        d_13___v3_: ComAmazonawsDynamodbTypes.TransactWriteItemsOutput
        d_13___v3_ = (d_12_valueOrError3_).Extract()
        output = Wrappers.Result_Success((False if (100) < (len(((d_4_queryRes_).Items).value)) else True))
        return output
        return output

    @_dafny.classproperty
    def NOT__BK__ERR__MSG(instance):
        return (_dafny.Seq("NOT a DDB Internal Server Error, but an MPL Testing error.")) + (_dafny.Seq(" DDB query to gather and delete a BK returned a non-BK item."))
