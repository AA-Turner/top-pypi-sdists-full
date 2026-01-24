import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import aws_cryptographic_material_providers.internaldafny.generated.module_ as module_
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
import aws_cryptography_primitives.internaldafny.generated.AwsCryptographyPrimitivesTypes as AwsCryptographyPrimitivesTypes
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
import aws_cryptography_internal_dynamodb.internaldafny.generated.ComAmazonawsDynamodbTypes as ComAmazonawsDynamodbTypes
import aws_cryptography_internal_kms.internaldafny.generated.ComAmazonawsKmsTypes as ComAmazonawsKmsTypes
import aws_cryptography_primitives.internaldafny.generated.AesKdfCtr as AesKdfCtr
import smithy_dafny_standard_library.internaldafny.generated.Relations as Relations
import smithy_dafny_standard_library.internaldafny.generated.Seq_MergeSort as Seq_MergeSort
import smithy_dafny_standard_library.internaldafny.generated.Math as Math
import smithy_dafny_standard_library.internaldafny.generated.Seq as Seq
import smithy_dafny_standard_library.internaldafny.generated.Unicode as Unicode
import smithy_dafny_standard_library.internaldafny.generated.Functions as Functions
import smithy_dafny_standard_library.internaldafny.generated.Utf8EncodingForm as Utf8EncodingForm
import smithy_dafny_standard_library.internaldafny.generated.Utf16EncodingForm as Utf16EncodingForm
import smithy_dafny_standard_library.internaldafny.generated.UnicodeStrings as UnicodeStrings
import smithy_dafny_standard_library.internaldafny.generated.FileIO as FileIO
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
import smithy_dafny_standard_library.internaldafny.generated.UUID as UUID
import smithy_dafny_standard_library.internaldafny.generated.OsLang as OsLang
import smithy_dafny_standard_library.internaldafny.generated.Time as Time
import smithy_dafny_standard_library.internaldafny.generated.Streams as Streams
import smithy_dafny_standard_library.internaldafny.generated.Sorting as Sorting
import smithy_dafny_standard_library.internaldafny.generated.SortedSets as SortedSets
import smithy_dafny_standard_library.internaldafny.generated.HexStrings as HexStrings
import smithy_dafny_standard_library.internaldafny.generated.GetOpt as GetOpt
import smithy_dafny_standard_library.internaldafny.generated.FloatCompare as FloatCompare
import smithy_dafny_standard_library.internaldafny.generated.ConcurrentCall as ConcurrentCall
import smithy_dafny_standard_library.internaldafny.generated.Base64 as Base64
import smithy_dafny_standard_library.internaldafny.generated.Base64Lemmas as Base64Lemmas
import smithy_dafny_standard_library.internaldafny.generated.Actions as Actions
import smithy_dafny_standard_library.internaldafny.generated.DafnyLibraries as DafnyLibraries
import aws_cryptographic_material_providers.internaldafny.generated.AwsCryptographyKeyStoreTypes as AwsCryptographyKeyStoreTypes
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
import aws_cryptographic_material_providers.internaldafny.generated.AwsCryptographyKeyStoreOperations as AwsCryptographyKeyStoreOperations
import aws_cryptography_internal_kms.internaldafny.generated.Com_Amazonaws_Kms as Com_Amazonaws_Kms
import aws_cryptography_internal_dynamodb.internaldafny.generated.Com_Amazonaws_Dynamodb as Com_Amazonaws_Dynamodb
import aws_cryptographic_material_providers.internaldafny.generated.KeyStore as KeyStore
import aws_cryptographic_material_providers.internaldafny.generated.AlgorithmSuites as AlgorithmSuites
import aws_cryptographic_material_providers.internaldafny.generated.Materials as Materials
import aws_cryptographic_material_providers.internaldafny.generated.Keyring as Keyring
import aws_cryptographic_material_providers.internaldafny.generated.CanonicalEncryptionContext as CanonicalEncryptionContext
import aws_cryptographic_material_providers.internaldafny.generated.MaterialWrapping as MaterialWrapping
import aws_cryptographic_material_providers.internaldafny.generated.IntermediateKeyWrapping as IntermediateKeyWrapping
import aws_cryptographic_material_providers.internaldafny.generated.EdkWrapping as EdkWrapping
import aws_cryptographic_material_providers.internaldafny.generated.ErrorMessages as ErrorMessages
import aws_cryptographic_material_providers.internaldafny.generated.RawAESKeyring as RawAESKeyring
import aws_cryptographic_material_providers.internaldafny.generated.Constants as Constants
import aws_cryptographic_material_providers.internaldafny.generated.EcdhEdkWrapping as EcdhEdkWrapping

# Module: RawECDHKeyring

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def ValidPublicKeyLength(p):
        d_0_len_ = len(p)
        return (True) and ((((d_0_len_) == (Constants.default__.ECDH__PUBLIC__KEY__LEN__ECC__NIST__256)) or ((d_0_len_) == (Constants.default__.ECDH__PUBLIC__KEY__LEN__ECC__NIST__384))) or ((d_0_len_) == (Constants.default__.ECDH__PUBLIC__KEY__LEN__ECC__NIST__521)))

    @staticmethod
    def ValidCompressedPublicKeyLength(p):
        d_0_len_ = len(p)
        return (True) and ((((d_0_len_) == (Constants.default__.ECDH__PUBLIC__KEY__COMPRESSED__LEN__ECC__NIST__256)) or ((d_0_len_) == (Constants.default__.ECDH__PUBLIC__KEY__COMPRESSED__LEN__ECC__NIST__384))) or ((d_0_len_) == (Constants.default__.ECDH__PUBLIC__KEY__COMPRESSED__LEN__ECC__NIST__521)))

    @staticmethod
    def ValidProviderInfoLength(p):
        d_0_len_ = len(p)
        return (((d_0_len_) == (Constants.default__.ECDH__PROVIDER__INFO__256__LEN)) or ((d_0_len_) == (Constants.default__.ECDH__PROVIDER__INFO__384__LEN))) or ((d_0_len_) == (Constants.default__.ECDH__PROVIDER__INFO__521__LEN))

    @staticmethod
    def LocalDeriveSharedSecret(senderPrivateKey, recipientPublicKey, curveSpec, crypto):
        res: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_maybeSharedSecret_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (crypto).DeriveSharedSecret(AwsCryptographyPrimitivesTypes.DeriveSharedSecretInput_DeriveSharedSecretInput(curveSpec, senderPrivateKey, recipientPublicKey))
        d_0_maybeSharedSecret_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.DeriveSharedSecretOutput.default())()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_maybeSharedSecret_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_sharedSecretOutput_: AwsCryptographyPrimitivesTypes.DeriveSharedSecretOutput
        d_3_sharedSecretOutput_ = (d_1_valueOrError0_).Extract()
        res = Wrappers.Result_Success((d_3_sharedSecretOutput_).sharedSecret)
        return res
        return res

    @staticmethod
    def CompressPublicKey(publicKey, curveSpec, crypto):
        res: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_maybeCompressedPublicKey_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (crypto).CompressPublicKey(AwsCryptographyPrimitivesTypes.CompressPublicKeyInput_CompressPublicKeyInput(publicKey, curveSpec))
        d_0_maybeCompressedPublicKey_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.CompressPublicKeyOutput.default())()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_maybeCompressedPublicKey_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_compressedPublicKey_: AwsCryptographyPrimitivesTypes.CompressPublicKeyOutput
        d_3_compressedPublicKey_ = (d_1_valueOrError0_).Extract()
        res = Wrappers.Result_Success((d_3_compressedPublicKey_).compressedPublicKey)
        return res
        return res

    @staticmethod
    def DecompressPublicKey(publicKey, curveSpec, crypto):
        res: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_maybePublicKey_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (crypto).DecompressPublicKey(AwsCryptographyPrimitivesTypes.DecompressPublicKeyInput_DecompressPublicKeyInput(publicKey, curveSpec))
        d_0_maybePublicKey_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.DecompressPublicKeyOutput.default())()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_maybePublicKey_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_publicKey_: AwsCryptographyPrimitivesTypes.DecompressPublicKeyOutput
        d_3_publicKey_ = (d_1_valueOrError0_).Extract()
        res = Wrappers.Result_Success(((d_3_publicKey_).publicKey).der)
        return res
        return res

    @staticmethod
    def SerializeProviderInfo(senderPublicKey, recipientPublicKey):
        return ((((default__.RAW__ECDH__KEYRING__VERSION) + (StandardLibrary_UInt.default__.UInt32ToSeq(len(recipientPublicKey)))) + (recipientPublicKey)) + (StandardLibrary_UInt.default__.UInt32ToSeq(len(senderPublicKey)))) + (senderPublicKey)

    @staticmethod
    def GenerateEphemeralEccKeyPair(curveSpec, crypto):
        res: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.GenerateECCKeyPairOutput.default())()
        d_0_maybeKeyPair_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (crypto).GenerateECCKeyPair(AwsCryptographyPrimitivesTypes.GenerateECCKeyPairInput_GenerateECCKeyPairInput(curveSpec))
        d_0_maybeKeyPair_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.GenerateECCKeyPairOutput.default())()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_maybeKeyPair_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_keyPair_: AwsCryptographyPrimitivesTypes.GenerateECCKeyPairOutput
        d_3_keyPair_ = (d_1_valueOrError0_).Extract()
        res = Wrappers.Result_Success(d_3_keyPair_)
        return res

    @staticmethod
    def ValidatePublicKey(crypto, curveSpec, publicKey):
        res: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.bool)()
        d_0_maybeValidate_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = (crypto).ValidatePublicKey(AwsCryptographyPrimitivesTypes.ValidatePublicKeyInput_ValidatePublicKeyInput(curveSpec, publicKey))
        d_0_maybeValidate_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.ValidatePublicKeyOutput.default())()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_maybeValidate_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_validate_: AwsCryptographyPrimitivesTypes.ValidatePublicKeyOutput
        d_3_validate_ = (d_1_valueOrError0_).Extract()
        res = Wrappers.Result_Success((d_3_validate_).success)
        return res

    @staticmethod
    def CurveSpecTypeToString(c):
        source0_ = c
        if True:
            if source0_.is_ECC__NIST__P256:
                return _dafny.Seq("p256")
        if True:
            if source0_.is_ECC__NIST__P384:
                return _dafny.Seq("p384")
        if True:
            if source0_.is_ECC__NIST__P521:
                return _dafny.Seq("p521")
        if True:
            return _dafny.Seq("sm2")

    @staticmethod
    def E(s):
        return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(s)

    @_dafny.classproperty
    def RAW__ECDH__KEYRING__VERSION(instance):
        return _dafny.Seq([1])

class RawEcdhKeyring(Keyring.VerifiableInterface, AwsCryptographyMaterialProvidersTypes.IKeyring):
    def  __init__(self):
        self._cryptoPrimitives: AtomicPrimitives.AtomicPrimitivesClient = None
        self._keyAgreementScheme: AwsCryptographyMaterialProvidersTypes.RawEcdhStaticConfigurations = AwsCryptographyMaterialProvidersTypes.RawEcdhStaticConfigurations.default()()
        self._curveSpec: AwsCryptographyPrimitivesTypes.ECDHCurveSpec = AwsCryptographyPrimitivesTypes.ECDHCurveSpec.default()()
        self._recipientPublicKey: AwsCryptographyPrimitivesTypes.ECCPublicKey = AwsCryptographyPrimitivesTypes.ECCPublicKey.default()()
        self._compressedRecipientPublicKey: _dafny.Seq = _dafny.Seq({})
        self._senderPublicKey: AwsCryptographyPrimitivesTypes.ECCPublicKey = AwsCryptographyPrimitivesTypes.ECCPublicKey.default()()
        self._senderPrivateKey: AwsCryptographyPrimitivesTypes.ECCPrivateKey = AwsCryptographyPrimitivesTypes.ECCPrivateKey.default()()
        self._compressedSenderPublicKey: _dafny.Seq = _dafny.Seq({})
        pass

    def __dafnystr__(self) -> str:
        return "RawECDHKeyring.RawEcdhKeyring"
    def OnDecrypt(self, input):
        out2_: Wrappers.Result
        out2_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnDecrypt(self, input)
        return out2_

    def OnEncrypt(self, input):
        out2_: Wrappers.Result
        out2_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnEncrypt(self, input)
        return out2_

    def ctor__(self, keyAgreementScheme, curveSpec, senderPrivateKey, senderPublicKey, recipientPublicKey, compressedSenderPublicKey, compressedRecipientPublicKey, cryptoPrimitives):
        (self)._keyAgreementScheme = keyAgreementScheme
        (self)._curveSpec = curveSpec
        (self)._cryptoPrimitives = cryptoPrimitives
        (self)._recipientPublicKey = AwsCryptographyPrimitivesTypes.ECCPublicKey_ECCPublicKey(recipientPublicKey)
        (self)._compressedRecipientPublicKey = compressedRecipientPublicKey
        if (((senderPublicKey).is_Some) and ((senderPrivateKey).is_Some)) and ((compressedSenderPublicKey).is_Some):
            (self)._senderPublicKey = AwsCryptographyPrimitivesTypes.ECCPublicKey_ECCPublicKey((senderPublicKey).value)
            (self)._senderPrivateKey = AwsCryptographyPrimitivesTypes.ECCPrivateKey_ECCPrivateKey((senderPrivateKey).value)
            (self)._compressedSenderPublicKey = (compressedSenderPublicKey).value
        elif True:
            (self)._senderPublicKey = AwsCryptographyPrimitivesTypes.ECCPublicKey_ECCPublicKey(_dafny.Seq([]))
            (self)._senderPrivateKey = AwsCryptographyPrimitivesTypes.ECCPrivateKey_ECCPrivateKey(_dafny.Seq([]))
            (self)._compressedSenderPublicKey = _dafny.Seq([])

    def OnEncrypt_k(self, input):
        res: Wrappers.Result = None
        if ((self).keyAgreementScheme).is_PublicKeyDiscovery:
            res = Wrappers.Result_Failure(AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("PublicKeyDiscovery Key Agreement Scheme is forbidden on encrypt.")))
            return res
        d_0_operationSenderPrivateKey_: AwsCryptographyPrimitivesTypes.ECCPrivateKey = AwsCryptographyPrimitivesTypes.ECCPrivateKey.default()()
        d_1_operationSenderPublicKey_: AwsCryptographyPrimitivesTypes.ECCPublicKey = AwsCryptographyPrimitivesTypes.ECCPublicKey.default()()
        d_2_operationCompressedSenderPublicKey_: _dafny.Seq = _dafny.Seq({})
        if ((self).keyAgreementScheme).is_EphemeralPrivateKeyToStaticPublicKey:
            d_3_valueOrError0_: Wrappers.Result = Wrappers.Result.default(AwsCryptographyPrimitivesTypes.GenerateECCKeyPairOutput.default())()
            out0_: Wrappers.Result
            out0_ = default__.GenerateEphemeralEccKeyPair((self).curveSpec, (self).cryptoPrimitives)
            d_3_valueOrError0_ = out0_
            if (d_3_valueOrError0_).IsFailure():
                res = (d_3_valueOrError0_).PropagateFailure()
                return res
            d_4_ephemeralKeyPair_: AwsCryptographyPrimitivesTypes.GenerateECCKeyPairOutput
            d_4_ephemeralKeyPair_ = (d_3_valueOrError0_).Extract()
            d_0_operationSenderPrivateKey_ = (d_4_ephemeralKeyPair_).privateKey
            d_1_operationSenderPublicKey_ = (d_4_ephemeralKeyPair_).publicKey
            d_5_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
            out1_: Wrappers.Result
            out1_ = default__.CompressPublicKey(AwsCryptographyPrimitivesTypes.ECCPublicKey_ECCPublicKey((d_1_operationSenderPublicKey_).der), (self).curveSpec, (self).cryptoPrimitives)
            d_5_valueOrError1_ = out1_
            if (d_5_valueOrError1_).IsFailure():
                res = (d_5_valueOrError1_).PropagateFailure()
                return res
            d_6_operationCompressedSenderPublicKey_q_: _dafny.Seq
            d_6_operationCompressedSenderPublicKey_q_ = (d_5_valueOrError1_).Extract()
            d_2_operationCompressedSenderPublicKey_ = d_6_operationCompressedSenderPublicKey_q_
        elif True:
            d_0_operationSenderPrivateKey_ = (self).senderPrivateKey
            d_1_operationSenderPublicKey_ = (self).senderPublicKey
            d_2_operationCompressedSenderPublicKey_ = (self).compressedSenderPublicKey
        d_7_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        d_7_materials_ = (input).materials
        d_8_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_8_suite_ = ((input).materials).algorithmSuite
        d_9_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out2_: Wrappers.Result
        out2_ = default__.LocalDeriveSharedSecret(d_0_operationSenderPrivateKey_, (self).recipientPublicKey, (self).curveSpec, (self).cryptoPrimitives)
        d_9_valueOrError2_ = out2_
        if (d_9_valueOrError2_).IsFailure():
            res = (d_9_valueOrError2_).PropagateFailure()
            return res
        d_10_sharedSecret_: _dafny.Seq
        d_10_sharedSecret_ = (d_9_valueOrError2_).Extract()
        d_11_valueOrError3_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_11_valueOrError3_ = (UTF8.default__.Encode(default__.CurveSpecTypeToString((self).curveSpec))).MapFailure(default__.E)
        if (d_11_valueOrError3_).IsFailure():
            res = (d_11_valueOrError3_).PropagateFailure()
            return res
        d_12_curveSpecUtf8_: _dafny.Seq
        d_12_curveSpecUtf8_ = (d_11_valueOrError3_).Extract()
        d_13_valueOrError4_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_13_valueOrError4_ = CanonicalEncryptionContext.default__.EncryptionContextToAAD(((input).materials).encryptionContext)
        if (d_13_valueOrError4_).IsFailure():
            res = (d_13_valueOrError4_).PropagateFailure()
            return res
        d_14_canonicalizedEC_: _dafny.Seq
        d_14_canonicalizedEC_ = (d_13_valueOrError4_).Extract()
        d_15_fixedInfo_: _dafny.Seq
        d_15_fixedInfo_ = EcdhEdkWrapping.default__.SerializeFixedInfo(Constants.default__.ECDH__KDF__UTF8, d_12_curveSpecUtf8_, d_2_operationCompressedSenderPublicKey_, (self).compressedRecipientPublicKey, d_14_canonicalizedEC_, default__.RAW__ECDH__KEYRING__VERSION)
        d_16_ecdhGenerateAndWrap_: EcdhEdkWrapping.EcdhGenerateAndWrapKeyMaterial
        nw0_ = EcdhEdkWrapping.EcdhGenerateAndWrapKeyMaterial()
        nw0_.ctor__(d_10_sharedSecret_, d_15_fixedInfo_, (self).cryptoPrimitives)
        d_16_ecdhGenerateAndWrap_ = nw0_
        d_17_ecdhWrap_: EcdhEdkWrapping.EcdhWrapKeyMaterial
        nw1_ = EcdhEdkWrapping.EcdhWrapKeyMaterial()
        nw1_.ctor__(d_10_sharedSecret_, d_15_fixedInfo_, (self).cryptoPrimitives)
        d_17_ecdhWrap_ = nw1_
        d_18_valueOrError5_: Wrappers.Result = Wrappers.Result.default(EdkWrapping.WrapEdkMaterialOutput.default(EcdhEdkWrapping.EcdhWrapInfo.default()))()
        out3_: Wrappers.Result
        out3_ = EdkWrapping.default__.WrapEdkMaterial(d_7_materials_, d_17_ecdhWrap_, d_16_ecdhGenerateAndWrap_)
        d_18_valueOrError5_ = out3_
        if (d_18_valueOrError5_).IsFailure():
            res = (d_18_valueOrError5_).PropagateFailure()
            return res
        d_19_wrapOutput_: EdkWrapping.WrapEdkMaterialOutput
        d_19_wrapOutput_ = (d_18_valueOrError5_).Extract()
        d_20_symmetricSigningKeyList_: Wrappers.Option
        if ((d_19_wrapOutput_).symmetricSigningKey).is_Some:
            d_20_symmetricSigningKeyList_ = Wrappers.Option_Some(_dafny.Seq([((d_19_wrapOutput_).symmetricSigningKey).value]))
        elif True:
            d_20_symmetricSigningKeyList_ = Wrappers.Option_None()
        d_21_valueOrError6_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_21_valueOrError6_ = Wrappers.default__.Need((default__.ValidCompressedPublicKeyLength(d_2_operationCompressedSenderPublicKey_)) and (default__.ValidCompressedPublicKeyLength((self).compressedRecipientPublicKey)), default__.E(_dafny.Seq("Invalid compressed public key length.")))
        if (d_21_valueOrError6_).IsFailure():
            res = (d_21_valueOrError6_).PropagateFailure()
            return res
        d_22_edk_: AwsCryptographyMaterialProvidersTypes.EncryptedDataKey
        d_22_edk_ = AwsCryptographyMaterialProvidersTypes.EncryptedDataKey_EncryptedDataKey(Constants.default__.RAW__ECDH__PROVIDER__ID, default__.SerializeProviderInfo(d_2_operationCompressedSenderPublicKey_, (self).compressedRecipientPublicKey), (d_19_wrapOutput_).wrappedMaterial)
        if (d_19_wrapOutput_).is_GenerateAndWrapEdkMaterialOutput:
            d_23_valueOrError7_: Wrappers.Result = None
            d_23_valueOrError7_ = Materials.default__.EncryptionMaterialAddDataKey(d_7_materials_, (d_19_wrapOutput_).plaintextDataKey, _dafny.Seq([d_22_edk_]), d_20_symmetricSigningKeyList_)
            if (d_23_valueOrError7_).IsFailure():
                res = (d_23_valueOrError7_).PropagateFailure()
                return res
            d_24_result_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
            d_24_result_ = (d_23_valueOrError7_).Extract()
            res = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnEncryptOutput_OnEncryptOutput(d_24_result_))
            return res
        elif (d_19_wrapOutput_).is_WrapOnlyEdkMaterialOutput:
            d_25_valueOrError8_: Wrappers.Result = None
            d_25_valueOrError8_ = Materials.default__.EncryptionMaterialAddEncryptedDataKeys(d_7_materials_, _dafny.Seq([d_22_edk_]), d_20_symmetricSigningKeyList_)
            if (d_25_valueOrError8_).IsFailure():
                res = (d_25_valueOrError8_).PropagateFailure()
                return res
            d_26_result_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
            d_26_result_ = (d_25_valueOrError8_).Extract()
            res = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnEncryptOutput_OnEncryptOutput(d_26_result_))
            return res
        return res

    def OnDecrypt_k(self, input):
        res: Wrappers.Result = None
        if ((self).keyAgreementScheme).is_EphemeralPrivateKeyToStaticPublicKey:
            res = Wrappers.Result_Failure(AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("EphemeralPrivateKeyToStaticPublicKey Key Agreement Scheme is forbidden on decrypt.")))
            return res
        d_0_materials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_0_materials_ = (input).materials
        d_1_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_1_suite_ = ((input).materials).algorithmSuite
        d_2_valueOrError0_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_2_valueOrError0_ = Wrappers.default__.Need(Materials.default__.DecryptionMaterialsWithoutPlaintextDataKey(d_0_materials_), default__.E(_dafny.Seq("Keyring received decryption materials that already contain a plaintext data key.")))
        if (d_2_valueOrError0_).IsFailure():
            res = (d_2_valueOrError0_).PropagateFailure()
            return res
        d_3_operationCompressedSenderPublicKey_: Wrappers.Option
        if ((self).compressedSenderPublicKey) == (_dafny.Seq([])):
            d_3_operationCompressedSenderPublicKey_ = Wrappers.Option_None()
        elif True:
            d_3_operationCompressedSenderPublicKey_ = Wrappers.Option_Some((self).compressedSenderPublicKey)
        d_4_filter_: OnDecryptEcdhDataKeyFilter
        nw0_ = OnDecryptEcdhDataKeyFilter()
        nw0_.ctor__((self).keyAgreementScheme, (self).compressedRecipientPublicKey, d_3_operationCompressedSenderPublicKey_)
        d_4_filter_ = nw0_
        d_5_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out0_: Wrappers.Result
        out0_ = Actions.default__.FilterWithResult(d_4_filter_, (input).encryptedDataKeys)
        d_5_valueOrError1_ = out0_
        if (d_5_valueOrError1_).IsFailure():
            res = (d_5_valueOrError1_).PropagateFailure()
            return res
        d_6_edksToAttempt_: _dafny.Seq
        d_6_edksToAttempt_ = (d_5_valueOrError1_).Extract()
        if (0) == (len(d_6_edksToAttempt_)):
            d_7_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
            d_7_valueOrError2_ = ErrorMessages.default__.IncorrectDataKeys((input).encryptedDataKeys, ((input).materials).algorithmSuite, _dafny.Seq(""))
            if (d_7_valueOrError2_).IsFailure():
                res = (d_7_valueOrError2_).PropagateFailure()
                return res
            d_8_errorMessage_: _dafny.Seq
            d_8_errorMessage_ = (d_7_valueOrError2_).Extract()
            res = Wrappers.Result_Failure(default__.E(d_8_errorMessage_))
            return res
        d_9_decryptClosure_: Actions.ActionWithResult
        nw1_ = DecryptSingleEncryptedDataKey()
        nw1_.ctor__(d_0_materials_, (self).cryptoPrimitives, (self).compressedSenderPublicKey, (self).compressedRecipientPublicKey, (self).keyAgreementScheme, (self).curveSpec)
        d_9_decryptClosure_ = nw1_
        d_10_outcome_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = Actions.default__.ReduceToSuccess(d_9_decryptClosure_, d_6_edksToAttempt_)
        d_10_outcome_ = out1_
        d_11_valueOrError3_: Wrappers.Result = None
        def lambda0_(d_12_errors_):
            return AwsCryptographyMaterialProvidersTypes.Error_CollectionOfErrors(d_12_errors_, _dafny.Seq("No Configured Key was able to decrypt the Data Key. The list of encountered Exceptions is available via `list`."))

        d_11_valueOrError3_ = (d_10_outcome_).MapFailure(lambda0_)
        if (d_11_valueOrError3_).IsFailure():
            res = (d_11_valueOrError3_).PropagateFailure()
            return res
        d_13_SealedDecryptionMaterials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_13_SealedDecryptionMaterials_ = (d_11_valueOrError3_).Extract()
        res = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnDecryptOutput_OnDecryptOutput(d_13_SealedDecryptionMaterials_))
        return res
        return res

    @property
    def cryptoPrimitives(self):
        return self._cryptoPrimitives
    @property
    def keyAgreementScheme(self):
        return self._keyAgreementScheme
    @property
    def curveSpec(self):
        return self._curveSpec
    @property
    def recipientPublicKey(self):
        return self._recipientPublicKey
    @property
    def compressedRecipientPublicKey(self):
        return self._compressedRecipientPublicKey
    @property
    def senderPublicKey(self):
        return self._senderPublicKey
    @property
    def senderPrivateKey(self):
        return self._senderPrivateKey
    @property
    def compressedSenderPublicKey(self):
        return self._compressedSenderPublicKey

class OnDecryptEcdhDataKeyFilter(Actions.DeterministicActionWithResult, Actions.DeterministicAction):
    def  __init__(self):
        self._keyAgreementScheme: AwsCryptographyMaterialProvidersTypes.RawEcdhStaticConfigurations = AwsCryptographyMaterialProvidersTypes.RawEcdhStaticConfigurations.default()()
        self._compressedRecipientPublicKey: _dafny.Seq = _dafny.Seq({})
        self._compressedSenderPublicKey: _dafny.Seq = _dafny.Seq({})
        pass

    def __dafnystr__(self) -> str:
        return "RawECDHKeyring.OnDecryptEcdhDataKeyFilter"
    def ctor__(self, keyAgreementScheme, compressedRecipientPublicKey, compressedSenderPublicKey):
        (self)._keyAgreementScheme = keyAgreementScheme
        (self)._compressedRecipientPublicKey = compressedRecipientPublicKey
        if (compressedSenderPublicKey).is_Some:
            (self)._compressedSenderPublicKey = (compressedSenderPublicKey).value
        elif True:
            (self)._compressedSenderPublicKey = _dafny.Seq([])

    def Invoke(self, edk):
        res: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.bool)()
        d_0_providerInfo_: _dafny.Seq
        d_0_providerInfo_ = (edk).keyProviderInfo
        d_1_providerId_: _dafny.Seq
        d_1_providerId_ = (edk).keyProviderId
        if ((d_1_providerId_) != (Constants.default__.RAW__ECDH__PROVIDER__ID)) and ((d_1_providerId_) != (Constants.default__.KMS__ECDH__PROVIDER__ID)):
            res = Wrappers.Result_Success(False)
            return res
        d_2_valueOrError0_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_2_valueOrError0_ = Wrappers.default__.Need(((len(d_0_providerInfo_)) <= (Constants.default__.ECDH__PROVIDER__INFO__521__LEN)) and (default__.ValidProviderInfoLength(d_0_providerInfo_)), default__.E(_dafny.Seq("EDK ProviderInfo longer than expected")))
        if (d_2_valueOrError0_).IsFailure():
            res = (d_2_valueOrError0_).PropagateFailure()
            return res
        d_3_keyringVersion_: int
        d_3_keyringVersion_ = (d_0_providerInfo_)[0]
        d_4_valueOrError1_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_4_valueOrError1_ = Wrappers.default__.Need((_dafny.Seq([d_3_keyringVersion_])) == (default__.RAW__ECDH__KEYRING__VERSION), default__.E(_dafny.Seq("Incorrect Keyring version found in provider info.")))
        if (d_4_valueOrError1_).IsFailure():
            res = (d_4_valueOrError1_).PropagateFailure()
            return res
        d_5_recipientPublicKeyLength_: int
        d_5_recipientPublicKeyLength_ = StandardLibrary_UInt.default__.SeqToUInt32(_dafny.Seq((d_0_providerInfo_)[Constants.default__.ECDH__PROVIDER__INFO__RPL__INDEX:Constants.default__.ECDH__PROVIDER__INFO__RPK__INDEX:]))
        d_6_recipientPublicKeyLengthIndex_: int
        d_6_recipientPublicKeyLengthIndex_ = (Constants.default__.ECDH__PROVIDER__INFO__RPK__INDEX) + (d_5_recipientPublicKeyLength_)
        d_7_senderPublicKeyIndex_: int
        d_7_senderPublicKeyIndex_ = (d_6_recipientPublicKeyLengthIndex_) + (Constants.default__.ECDH__PROVIDER__INFO__PUBLIC__KEY__LEN)
        d_8_valueOrError2_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_8_valueOrError2_ = Wrappers.default__.Need(((d_6_recipientPublicKeyLengthIndex_) + (4)) < (len(d_0_providerInfo_)), default__.E(_dafny.Seq("Key Provider Info Serialization Error. Serialized length less than expected.")))
        if (d_8_valueOrError2_).IsFailure():
            res = (d_8_valueOrError2_).PropagateFailure()
            return res
        d_9_providerInfoRecipientPublicKey_: _dafny.Seq
        d_9_providerInfoRecipientPublicKey_ = _dafny.Seq((d_0_providerInfo_)[Constants.default__.ECDH__PROVIDER__INFO__RPK__INDEX:d_6_recipientPublicKeyLengthIndex_:])
        d_10_providerInfoSenderPublicKey_: _dafny.Seq
        d_10_providerInfoSenderPublicKey_ = _dafny.Seq((d_0_providerInfo_)[d_7_senderPublicKeyIndex_::])
        if ((self).keyAgreementScheme).is_PublicKeyDiscovery:
            res = Wrappers.Result_Success(((self).compressedRecipientPublicKey) == (d_9_providerInfoRecipientPublicKey_))
            return res
        elif True:
            res = Wrappers.Result_Success(((((self).compressedSenderPublicKey) == (d_10_providerInfoSenderPublicKey_)) and (((self).compressedRecipientPublicKey) == (d_9_providerInfoRecipientPublicKey_))) or ((((self).compressedSenderPublicKey) == (d_9_providerInfoRecipientPublicKey_)) and (((self).compressedRecipientPublicKey) == (d_10_providerInfoSenderPublicKey_))))
            return res
        return res

    @property
    def keyAgreementScheme(self):
        return self._keyAgreementScheme
    @property
    def compressedRecipientPublicKey(self):
        return self._compressedRecipientPublicKey
    @property
    def compressedSenderPublicKey(self):
        return self._compressedSenderPublicKey

class DecryptSingleEncryptedDataKey(Actions.ActionWithResult, Actions.Action):
    def  __init__(self):
        self._materials: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials = None
        self._cryptoPrimitives: AtomicPrimitives.AtomicPrimitivesClient = None
        self._recipientPublicKey: _dafny.Seq = _dafny.Seq({})
        self._senderPublicKey: _dafny.Seq = _dafny.Seq({})
        self._keyAgreementScheme: AwsCryptographyMaterialProvidersTypes.RawEcdhStaticConfigurations = AwsCryptographyMaterialProvidersTypes.RawEcdhStaticConfigurations.default()()
        self._curveSpec: AwsCryptographyPrimitivesTypes.ECDHCurveSpec = AwsCryptographyPrimitivesTypes.ECDHCurveSpec.default()()
        pass

    def __dafnystr__(self) -> str:
        return "RawECDHKeyring.DecryptSingleEncryptedDataKey"
    def ctor__(self, materials, cryptoPrimitives, senderPublicKey, recipientPublicKey, keyAgreementScheme, curveSpec):
        (self)._materials = materials
        (self)._cryptoPrimitives = cryptoPrimitives
        (self)._recipientPublicKey = recipientPublicKey
        (self)._senderPublicKey = senderPublicKey
        (self)._keyAgreementScheme = keyAgreementScheme
        (self)._curveSpec = curveSpec

    def Invoke(self, edk):
        res: Wrappers.Result = None
        d_0_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_0_suite_ = ((self).materials).algorithmSuite
        d_1_keyProviderId_: _dafny.Seq
        d_1_keyProviderId_ = (edk).keyProviderId
        d_2_providerInfo_: _dafny.Seq
        d_2_providerInfo_ = (edk).keyProviderInfo
        d_3_ciphertext_: _dafny.Seq
        d_3_ciphertext_ = (edk).ciphertext
        d_4_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_4_valueOrError0_ = EdkWrapping.default__.GetProviderWrappedMaterial(d_3_ciphertext_, d_0_suite_)
        if (d_4_valueOrError0_).IsFailure():
            res = (d_4_valueOrError0_).PropagateFailure()
            return res
        d_5_providerWrappedMaterial_: _dafny.Seq
        d_5_providerWrappedMaterial_ = (d_4_valueOrError0_).Extract()
        d_6_valueOrError1_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_6_valueOrError1_ = Wrappers.default__.Need(((len(d_2_providerInfo_)) <= (Constants.default__.ECDH__PROVIDER__INFO__521__LEN)) and (default__.ValidProviderInfoLength(d_2_providerInfo_)), default__.E(_dafny.Seq("EDK ProviderInfo longer than expected")))
        if (d_6_valueOrError1_).IsFailure():
            res = (d_6_valueOrError1_).PropagateFailure()
            return res
        d_7_keyringVersion_: int
        d_7_keyringVersion_ = (d_2_providerInfo_)[0]
        d_8_valueOrError2_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_8_valueOrError2_ = Wrappers.default__.Need((_dafny.Seq([d_7_keyringVersion_])) == (default__.RAW__ECDH__KEYRING__VERSION), default__.E(_dafny.Seq("Incorrect Keyring version found in provider info.")))
        if (d_8_valueOrError2_).IsFailure():
            res = (d_8_valueOrError2_).PropagateFailure()
            return res
        d_9_recipientPublicKeyLength_: int
        d_9_recipientPublicKeyLength_ = StandardLibrary_UInt.default__.SeqToUInt32(_dafny.Seq((d_2_providerInfo_)[Constants.default__.ECDH__PROVIDER__INFO__RPL__INDEX:Constants.default__.ECDH__PROVIDER__INFO__RPK__INDEX:]))
        d_10_recipientPublicKeyLengthIndex_: int
        d_10_recipientPublicKeyLengthIndex_ = (Constants.default__.ECDH__PROVIDER__INFO__RPK__INDEX) + (d_9_recipientPublicKeyLength_)
        d_11_senderPublicKeyIndex_: int
        d_11_senderPublicKeyIndex_ = (d_10_recipientPublicKeyLengthIndex_) + (Constants.default__.ECDH__PROVIDER__INFO__PUBLIC__KEY__LEN)
        d_12_valueOrError3_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_12_valueOrError3_ = Wrappers.default__.Need(((d_10_recipientPublicKeyLengthIndex_) + (4)) < (len(d_2_providerInfo_)), default__.E(_dafny.Seq("Key Provider Info Serialization Error. Serialized length less than expected.")))
        if (d_12_valueOrError3_).IsFailure():
            res = (d_12_valueOrError3_).PropagateFailure()
            return res
        d_13_providerInfoRecipientPublicKey_: _dafny.Seq
        d_13_providerInfoRecipientPublicKey_ = _dafny.Seq((d_2_providerInfo_)[Constants.default__.ECDH__PROVIDER__INFO__RPK__INDEX:d_10_recipientPublicKeyLengthIndex_:])
        d_14_providerInfoSenderPublicKey_: _dafny.Seq
        d_14_providerInfoSenderPublicKey_ = _dafny.Seq((d_2_providerInfo_)[d_11_senderPublicKeyIndex_::])
        d_15_valueOrError4_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out0_: Wrappers.Result
        out0_ = default__.DecompressPublicKey(d_14_providerInfoSenderPublicKey_, (self).curveSpec, (self).cryptoPrimitives)
        d_15_valueOrError4_ = out0_
        if (d_15_valueOrError4_).IsFailure():
            res = (d_15_valueOrError4_).PropagateFailure()
            return res
        d_16_senderPublicKey_: _dafny.Seq
        d_16_senderPublicKey_ = (d_15_valueOrError4_).Extract()
        d_17_valueOrError5_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out1_: Wrappers.Result
        out1_ = default__.DecompressPublicKey(d_13_providerInfoRecipientPublicKey_, (self).curveSpec, (self).cryptoPrimitives)
        d_17_valueOrError5_ = out1_
        if (d_17_valueOrError5_).IsFailure():
            res = (d_17_valueOrError5_).PropagateFailure()
            return res
        d_18_recipientPublicKey_: _dafny.Seq
        d_18_recipientPublicKey_ = (d_17_valueOrError5_).Extract()
        d_19_valueOrError6_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.bool)()
        out2_: Wrappers.Result
        out2_ = default__.ValidatePublicKey((self).cryptoPrimitives, (self).curveSpec, d_16_senderPublicKey_)
        d_19_valueOrError6_ = out2_
        if (d_19_valueOrError6_).IsFailure():
            res = (d_19_valueOrError6_).PropagateFailure()
            return res
        d_20___v0_: bool
        d_20___v0_ = (d_19_valueOrError6_).Extract()
        d_21_valueOrError7_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.bool)()
        out3_: Wrappers.Result
        out3_ = default__.ValidatePublicKey((self).cryptoPrimitives, (self).curveSpec, d_18_recipientPublicKey_)
        d_21_valueOrError7_ = out3_
        if (d_21_valueOrError7_).IsFailure():
            res = (d_21_valueOrError7_).PropagateFailure()
            return res
        d_22___v1_: bool
        d_22___v1_ = (d_21_valueOrError7_).Extract()
        d_23_sharedSecretPublicKey_: _dafny.Seq = _dafny.Seq({})
        d_24_sharedSecretPrivateKey_: _dafny.Seq = _dafny.Seq({})
        source0_ = (self).keyAgreementScheme
        with _dafny.label("match0"):
            if True:
                if source0_.is_PublicKeyDiscovery:
                    d_25_publicKeyDiscovery_ = source0_.PublicKeyDiscovery
                    if True:
                        d_23_sharedSecretPublicKey_ = d_16_senderPublicKey_
                        d_24_sharedSecretPrivateKey_ = (d_25_publicKeyDiscovery_).recipientStaticPrivateKey
                    raise _dafny.Break("match0")
            if True:
                if source0_.is_RawPrivateKeyToStaticPublicKey:
                    d_26_rawPrivateKeyToStaticPublicKey_ = source0_.RawPrivateKeyToStaticPublicKey
                    if True:
                        d_24_sharedSecretPrivateKey_ = (d_26_rawPrivateKeyToStaticPublicKey_).senderStaticPrivateKey
                        if ((d_26_rawPrivateKeyToStaticPublicKey_).recipientPublicKey) == (d_18_recipientPublicKey_):
                            d_23_sharedSecretPublicKey_ = d_18_recipientPublicKey_
                        elif True:
                            d_23_sharedSecretPublicKey_ = d_16_senderPublicKey_
                    raise _dafny.Break("match0")
            if True:
                if True:
                    res = Wrappers.Result_Failure(default__.E(_dafny.Seq("EphemeralPrivateKeyToStaticPublicKey Not allowed on decrypt")))
                    return res
            pass
        d_27_valueOrError8_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.bool)()
        out4_: Wrappers.Result
        out4_ = default__.ValidatePublicKey((self).cryptoPrimitives, (self).curveSpec, d_23_sharedSecretPublicKey_)
        d_27_valueOrError8_ = out4_
        if (d_27_valueOrError8_).IsFailure():
            res = (d_27_valueOrError8_).PropagateFailure()
            return res
        d_28___v3_: bool
        d_28___v3_ = (d_27_valueOrError8_).Extract()
        d_29_valueOrError9_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out5_: Wrappers.Result
        out5_ = default__.LocalDeriveSharedSecret(AwsCryptographyPrimitivesTypes.ECCPrivateKey_ECCPrivateKey(d_24_sharedSecretPrivateKey_), AwsCryptographyPrimitivesTypes.ECCPublicKey_ECCPublicKey(d_23_sharedSecretPublicKey_), (self).curveSpec, (self).cryptoPrimitives)
        d_29_valueOrError9_ = out5_
        if (d_29_valueOrError9_).IsFailure():
            res = (d_29_valueOrError9_).PropagateFailure()
            return res
        d_30_sharedSecret_: _dafny.Seq
        d_30_sharedSecret_ = (d_29_valueOrError9_).Extract()
        d_31_ecdhUnwrap_: EcdhEdkWrapping.EcdhUnwrap
        nw0_ = EcdhEdkWrapping.EcdhUnwrap()
        nw0_.ctor__(d_14_providerInfoSenderPublicKey_, d_13_providerInfoRecipientPublicKey_, d_30_sharedSecret_, default__.RAW__ECDH__KEYRING__VERSION, (self).curveSpec, (self).cryptoPrimitives)
        d_31_ecdhUnwrap_ = nw0_
        d_32_unwrapOutputRes_: Wrappers.Result
        out6_: Wrappers.Result
        out6_ = EdkWrapping.default__.UnwrapEdkMaterial((edk).ciphertext, (self).materials, d_31_ecdhUnwrap_)
        d_32_unwrapOutputRes_ = out6_
        d_33_valueOrError10_: Wrappers.Result = Wrappers.Result.default(EdkWrapping.UnwrapEdkMaterialOutput.default(EcdhEdkWrapping.EcdhUnwrapInfo.default()))()
        d_33_valueOrError10_ = d_32_unwrapOutputRes_
        if (d_33_valueOrError10_).IsFailure():
            res = (d_33_valueOrError10_).PropagateFailure()
            return res
        d_34_unwrapOutput_: EdkWrapping.UnwrapEdkMaterialOutput
        d_34_unwrapOutput_ = (d_33_valueOrError10_).Extract()
        d_35_valueOrError11_: Wrappers.Result = None
        d_35_valueOrError11_ = Materials.default__.DecryptionMaterialsAddDataKey((self).materials, (d_34_unwrapOutput_).plaintextDataKey, (d_34_unwrapOutput_).symmetricSigningKey)
        if (d_35_valueOrError11_).IsFailure():
            res = (d_35_valueOrError11_).PropagateFailure()
            return res
        d_36_result_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_36_result_ = (d_35_valueOrError11_).Extract()
        res = Wrappers.Result_Success(d_36_result_)
        return res
        return res

    @property
    def materials(self):
        return self._materials
    @property
    def cryptoPrimitives(self):
        return self._cryptoPrimitives
    @property
    def recipientPublicKey(self):
        return self._recipientPublicKey
    @property
    def senderPublicKey(self):
        return self._senderPublicKey
    @property
    def keyAgreementScheme(self):
        return self._keyAgreementScheme
    @property
    def curveSpec(self):
        return self._curveSpec
