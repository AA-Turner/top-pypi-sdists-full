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
import aws_cryptographic_material_providers.internaldafny.generated.RawECDHKeyring as RawECDHKeyring

# Module: RawRSAKeyring


class RawRSAKeyring(Keyring.VerifiableInterface, AwsCryptographyMaterialProvidersTypes.IKeyring):
    def  __init__(self):
        self._cryptoPrimitives: AtomicPrimitives.AtomicPrimitivesClient = None
        self._privateKeyMaterial: Wrappers.Option = Wrappers.Option.default()()
        self._publicKeyMaterial: Wrappers.Option = Wrappers.Option.default()()
        self._publicKey: Wrappers.Option = Wrappers.Option.default()()
        self._privateKey: Wrappers.Option = Wrappers.Option.default()()
        self._keyNamespace: _dafny.Seq = UTF8.ValidUTF8Bytes.default()
        self._keyName: _dafny.Seq = UTF8.ValidUTF8Bytes.default()
        self._paddingScheme: AwsCryptographyPrimitivesTypes.RSAPaddingMode = AwsCryptographyPrimitivesTypes.RSAPaddingMode.default()()
        pass

    def __dafnystr__(self) -> str:
        return "RawRSAKeyring.RawRSAKeyring"
    def OnDecrypt(self, input):
        out3_: Wrappers.Result
        out3_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnDecrypt(self, input)
        return out3_

    def OnEncrypt(self, input):
        out3_: Wrappers.Result
        out3_ = AwsCryptographyMaterialProvidersTypes.IKeyring.OnEncrypt(self, input)
        return out3_

    def ctor__(self, namespace, name, publicKey, privateKey, paddingScheme, cryptoPrimitives):
        (self)._keyNamespace = namespace
        (self)._keyName = name
        (self)._paddingScheme = paddingScheme
        (self)._publicKey = publicKey
        (self)._privateKey = privateKey
        (self)._cryptoPrimitives = cryptoPrimitives
        d_0_localPrivateKeyMaterial_: Wrappers.Option
        d_0_localPrivateKeyMaterial_ = Wrappers.Option_None()
        if (privateKey).is_Some:
            d_1_extract_: _dafny.Seq
            d_1_extract_ = (privateKey).Extract()
            if (len(d_1_extract_)) > (0):
                d_2_unwrap_: RsaUnwrapKeyMaterial
                nw0_ = RsaUnwrapKeyMaterial()
                nw0_.ctor__(d_1_extract_, paddingScheme, cryptoPrimitives)
                d_2_unwrap_ = nw0_
                d_0_localPrivateKeyMaterial_ = Wrappers.Option_Some(d_2_unwrap_)
        d_3_localPublicKeyMaterial_: Wrappers.Option
        d_3_localPublicKeyMaterial_ = Wrappers.Option_None()
        if (publicKey).is_Some:
            d_4_extract_: _dafny.Seq
            d_4_extract_ = (publicKey).Extract()
            if (len(d_4_extract_)) > (0):
                d_5_wrap_: RsaWrapKeyMaterial
                nw1_ = RsaWrapKeyMaterial()
                nw1_.ctor__(d_4_extract_, paddingScheme, cryptoPrimitives)
                d_5_wrap_ = nw1_
                d_3_localPublicKeyMaterial_ = Wrappers.Option_Some(d_5_wrap_)
        (self)._publicKeyMaterial = d_3_localPublicKeyMaterial_
        (self)._privateKeyMaterial = d_0_localPrivateKeyMaterial_

    def OnEncrypt_k(self, input):
        output: Wrappers.Result = None
        d_0_valueOrError0_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_0_valueOrError0_ = Wrappers.default__.Need(((self).publicKeyMaterial).is_Some, AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("A RawRSAKeyring without a public key cannot provide OnEncrypt")))
        if (d_0_valueOrError0_).IsFailure():
            output = (d_0_valueOrError0_).PropagateFailure()
            return output
        d_1_materials_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
        d_1_materials_ = (input).materials
        d_2_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_2_suite_ = (d_1_materials_).algorithmSuite
        d_3_generateAndWrap_: RsaGenerateAndWrapKeyMaterial
        nw0_ = RsaGenerateAndWrapKeyMaterial()
        nw0_.ctor__(((self).publicKey).value, (self).paddingScheme, (self).cryptoPrimitives)
        d_3_generateAndWrap_ = nw0_
        d_4_valueOrError1_: Wrappers.Result = Wrappers.Result.default(EdkWrapping.WrapEdkMaterialOutput.default(RsaWrapInfo.default()))()
        out0_: Wrappers.Result
        out0_ = EdkWrapping.default__.WrapEdkMaterial(d_1_materials_, ((self).publicKeyMaterial).value, d_3_generateAndWrap_)
        d_4_valueOrError1_ = out0_
        if (d_4_valueOrError1_).IsFailure():
            output = (d_4_valueOrError1_).PropagateFailure()
            return output
        d_5_wrapOutput_: EdkWrapping.WrapEdkMaterialOutput
        d_5_wrapOutput_ = (d_4_valueOrError1_).Extract()
        d_6_symmetricSigningKeyList_: Wrappers.Option
        if ((d_5_wrapOutput_).symmetricSigningKey).is_Some:
            d_6_symmetricSigningKeyList_ = Wrappers.Option_Some(_dafny.Seq([((d_5_wrapOutput_).symmetricSigningKey).value]))
        elif True:
            d_6_symmetricSigningKeyList_ = Wrappers.Option_None()
        d_7_edk_: AwsCryptographyMaterialProvidersTypes.EncryptedDataKey
        d_7_edk_ = AwsCryptographyMaterialProvidersTypes.EncryptedDataKey_EncryptedDataKey((self).keyNamespace, (self).keyName, (d_5_wrapOutput_).wrappedMaterial)
        if (d_5_wrapOutput_).is_GenerateAndWrapEdkMaterialOutput:
            d_8_valueOrError2_: Wrappers.Result = None
            d_8_valueOrError2_ = Materials.default__.EncryptionMaterialAddDataKey(d_1_materials_, (d_5_wrapOutput_).plaintextDataKey, _dafny.Seq([d_7_edk_]), d_6_symmetricSigningKeyList_)
            if (d_8_valueOrError2_).IsFailure():
                output = (d_8_valueOrError2_).PropagateFailure()
                return output
            d_9_result_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
            d_9_result_ = (d_8_valueOrError2_).Extract()
            output = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnEncryptOutput_OnEncryptOutput(d_9_result_))
            return output
        elif (d_5_wrapOutput_).is_WrapOnlyEdkMaterialOutput:
            d_10_valueOrError3_: Wrappers.Result = None
            d_10_valueOrError3_ = Materials.default__.EncryptionMaterialAddEncryptedDataKeys(d_1_materials_, _dafny.Seq([d_7_edk_]), d_6_symmetricSigningKeyList_)
            if (d_10_valueOrError3_).IsFailure():
                output = (d_10_valueOrError3_).PropagateFailure()
                return output
            d_11_result_: AwsCryptographyMaterialProvidersTypes.EncryptionMaterials
            d_11_result_ = (d_10_valueOrError3_).Extract()
            output = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnEncryptOutput_OnEncryptOutput(d_11_result_))
            return output
        return output

    def OnDecrypt_k(self, input):
        output: Wrappers.Result = None
        d_0_valueOrError0_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_0_valueOrError0_ = Wrappers.default__.Need(((self).privateKeyMaterial).is_Some, AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("A RawRSAKeyring without a private key cannot provide OnEncrypt")))
        if (d_0_valueOrError0_).IsFailure():
            output = (d_0_valueOrError0_).PropagateFailure()
            return output
        d_1_materials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
        d_1_materials_ = (input).materials
        d_2_valueOrError1_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_2_valueOrError1_ = Wrappers.default__.Need(Materials.default__.DecryptionMaterialsWithoutPlaintextDataKey(d_1_materials_), AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Keyring received decryption materials that already contain a plaintext data key.")))
        if (d_2_valueOrError1_).IsFailure():
            output = (d_2_valueOrError1_).PropagateFailure()
            return output
        d_3_errors_: _dafny.Seq
        d_3_errors_ = _dafny.Seq([])
        hi0_ = len((input).encryptedDataKeys)
        for d_4_i_ in range(0, hi0_):
            if (self).ShouldDecryptEDK(((input).encryptedDataKeys)[d_4_i_]):
                d_5_edk_: AwsCryptographyMaterialProvidersTypes.EncryptedDataKey
                d_5_edk_ = ((input).encryptedDataKeys)[d_4_i_]
                d_6_unwrapOutput_: Wrappers.Result
                out0_: Wrappers.Result
                out0_ = EdkWrapping.default__.UnwrapEdkMaterial((d_5_edk_).ciphertext, d_1_materials_, ((self).privateKeyMaterial).value)
                d_6_unwrapOutput_ = out0_
                if (d_6_unwrapOutput_).is_Success:
                    d_7_valueOrError2_: Wrappers.Result = None
                    d_7_valueOrError2_ = Materials.default__.DecryptionMaterialsAddDataKey(d_1_materials_, ((d_6_unwrapOutput_).value).plaintextDataKey, ((d_6_unwrapOutput_).value).symmetricSigningKey)
                    if (d_7_valueOrError2_).IsFailure():
                        output = (d_7_valueOrError2_).PropagateFailure()
                        return output
                    d_8_returnMaterials_: AwsCryptographyMaterialProvidersTypes.DecryptionMaterials
                    d_8_returnMaterials_ = (d_7_valueOrError2_).Extract()
                    output = Wrappers.Result_Success(AwsCryptographyMaterialProvidersTypes.OnDecryptOutput_OnDecryptOutput(d_8_returnMaterials_))
                    return output
                elif True:
                    d_3_errors_ = (d_3_errors_) + (_dafny.Seq([(d_6_unwrapOutput_).error]))
            elif True:
                d_9_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
                def lambda0_(d_10_e_):
                    return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(d_10_e_)

                d_9_valueOrError3_ = (UTF8.default__.Decode((((input).encryptedDataKeys)[d_4_i_]).keyProviderId)).MapFailure(lambda0_)
                if (d_9_valueOrError3_).IsFailure():
                    output = (d_9_valueOrError3_).PropagateFailure()
                    return output
                d_11_extractedKeyProviderId_: _dafny.Seq
                d_11_extractedKeyProviderId_ = (d_9_valueOrError3_).Extract()
                d_3_errors_ = (d_3_errors_) + (_dafny.Seq([AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(ErrorMessages.default__.IncorrectRawDataKeys(StandardLibrary_String.default__.Base10Int2String(d_4_i_), _dafny.Seq("RSAKeyring"), d_11_extractedKeyProviderId_))]))
        output = Wrappers.Result_Failure(AwsCryptographyMaterialProvidersTypes.Error_CollectionOfErrors(d_3_errors_, _dafny.Seq("Raw RSA Key was unable to decrypt any encrypted data key. The list of encountered Exceptions is available via `list`.")))
        return output
        return output

    def ShouldDecryptEDK(self, edk):
        return (((UTF8.default__.ValidUTF8Seq((edk).keyProviderInfo)) and (((edk).keyProviderInfo) == ((self).keyName))) and (((edk).keyProviderId) == ((self).keyNamespace))) and ((len((edk).ciphertext)) > (0))

    @property
    def cryptoPrimitives(self):
        return self._cryptoPrimitives
    @property
    def privateKeyMaterial(self):
        return self._privateKeyMaterial
    @property
    def publicKeyMaterial(self):
        return self._publicKeyMaterial
    @property
    def publicKey(self):
        return self._publicKey
    @property
    def privateKey(self):
        return self._privateKey
    @property
    def keyNamespace(self):
        return self._keyNamespace
    @property
    def keyName(self):
        return self._keyName
    @property
    def paddingScheme(self):
        return self._paddingScheme

class RsaUnwrapInfo:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [RsaUnwrapInfo_RsaUnwrapInfo()]
    @classmethod
    def default(cls, ):
        return lambda: RsaUnwrapInfo_RsaUnwrapInfo()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_RsaUnwrapInfo(self) -> bool:
        return isinstance(self, RsaUnwrapInfo_RsaUnwrapInfo)

class RsaUnwrapInfo_RsaUnwrapInfo(RsaUnwrapInfo, NamedTuple('RsaUnwrapInfo', [])):
    def __dafnystr__(self) -> str:
        return f'RawRSAKeyring.RsaUnwrapInfo.RsaUnwrapInfo'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, RsaUnwrapInfo_RsaUnwrapInfo)
    def __hash__(self) -> int:
        return super().__hash__()


class RsaWrapInfo:
    @_dafny.classproperty
    def AllSingletonConstructors(cls):
        return [RsaWrapInfo_RsaWrapInfo()]
    @classmethod
    def default(cls, ):
        return lambda: RsaWrapInfo_RsaWrapInfo()
    def __ne__(self, __o: object) -> bool:
        return not self.__eq__(__o)
    @property
    def is_RsaWrapInfo(self) -> bool:
        return isinstance(self, RsaWrapInfo_RsaWrapInfo)

class RsaWrapInfo_RsaWrapInfo(RsaWrapInfo, NamedTuple('RsaWrapInfo', [])):
    def __dafnystr__(self) -> str:
        return f'RawRSAKeyring.RsaWrapInfo.RsaWrapInfo'
    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, RsaWrapInfo_RsaWrapInfo)
    def __hash__(self) -> int:
        return super().__hash__()


class RsaGenerateAndWrapKeyMaterial(MaterialWrapping.GenerateAndWrapMaterial, Actions.ActionWithResult, Actions.Action):
    def  __init__(self):
        self._publicKey: _dafny.Seq = _dafny.Seq({})
        self._paddingScheme: AwsCryptographyPrimitivesTypes.RSAPaddingMode = AwsCryptographyPrimitivesTypes.RSAPaddingMode.default()()
        self._cryptoPrimitives: AtomicPrimitives.AtomicPrimitivesClient = None
        pass

    def __dafnystr__(self) -> str:
        return "RawRSAKeyring.RsaGenerateAndWrapKeyMaterial"
    def ctor__(self, publicKey, paddingScheme, cryptoPrimitives):
        (self)._publicKey = publicKey
        (self)._paddingScheme = paddingScheme
        (self)._cryptoPrimitives = cryptoPrimitives

    def Invoke(self, input):
        res: Wrappers.Result = Wrappers.Result.default(MaterialWrapping.GenerateAndWrapOutput.default(RsaWrapInfo.default()))()
        d_0_generateBytesResult_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = ((self).cryptoPrimitives).GenerateRandomBytes(AwsCryptographyPrimitivesTypes.GenerateRandomBytesInput_GenerateRandomBytesInput(AlgorithmSuites.default__.GetEncryptKeyLength((input).algorithmSuite)))
        d_0_generateBytesResult_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_generateBytesResult_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_plaintextMaterial_: _dafny.Seq
        d_3_plaintextMaterial_ = (d_1_valueOrError0_).Extract()
        d_4_wrap_: RsaWrapKeyMaterial
        nw0_ = RsaWrapKeyMaterial()
        nw0_.ctor__((self).publicKey, (self).paddingScheme, (self).cryptoPrimitives)
        d_4_wrap_ = nw0_
        d_5_valueOrError1_: Wrappers.Result = Wrappers.Result.default(MaterialWrapping.WrapOutput.default(RsaWrapInfo.default()))()
        out1_: Wrappers.Result
        out1_ = (d_4_wrap_).Invoke(MaterialWrapping.WrapInput_WrapInput(d_3_plaintextMaterial_, (input).algorithmSuite, (input).encryptionContext, (input).serializedEC))
        d_5_valueOrError1_ = out1_
        if (d_5_valueOrError1_).IsFailure():
            res = (d_5_valueOrError1_).PropagateFailure()
            return res
        d_6_wrapOutput_: MaterialWrapping.WrapOutput
        d_6_wrapOutput_ = (d_5_valueOrError1_).Extract()
        d_7_output_: MaterialWrapping.GenerateAndWrapOutput
        d_7_output_ = MaterialWrapping.GenerateAndWrapOutput_GenerateAndWrapOutput(d_3_plaintextMaterial_, (d_6_wrapOutput_).wrappedMaterial, RsaWrapInfo_RsaWrapInfo())
        res = Wrappers.Result_Success(d_7_output_)
        return res
        return res

    @property
    def publicKey(self):
        return self._publicKey
    @property
    def paddingScheme(self):
        return self._paddingScheme
    @property
    def cryptoPrimitives(self):
        return self._cryptoPrimitives

class RsaWrapKeyMaterial(MaterialWrapping.WrapMaterial, Actions.ActionWithResult, Actions.Action):
    def  __init__(self):
        self._cryptoPrimitives: AtomicPrimitives.AtomicPrimitivesClient = None
        self._publicKey: _dafny.Seq = _dafny.Seq({})
        self._paddingScheme: AwsCryptographyPrimitivesTypes.RSAPaddingMode = AwsCryptographyPrimitivesTypes.RSAPaddingMode.default()()
        pass

    def __dafnystr__(self) -> str:
        return "RawRSAKeyring.RsaWrapKeyMaterial"
    def ctor__(self, publicKey, paddingScheme, cryptoPrimitives):
        (self)._publicKey = publicKey
        (self)._paddingScheme = paddingScheme
        (self)._cryptoPrimitives = cryptoPrimitives

    def Invoke(self, input):
        res: Wrappers.Result = Wrappers.Result.default(MaterialWrapping.WrapOutput.default(RsaWrapInfo.default()))()
        d_0_RSAEncryptOutput_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = ((self).cryptoPrimitives).RSAEncrypt(AwsCryptographyPrimitivesTypes.RSAEncryptInput_RSAEncryptInput((self).paddingScheme, (self).publicKey, (input).plaintextMaterial))
        d_0_RSAEncryptOutput_ = out0_
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        def lambda0_(d_2_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_2_e_)

        d_1_valueOrError0_ = (d_0_RSAEncryptOutput_).MapFailure(lambda0_)
        if (d_1_valueOrError0_).IsFailure():
            res = (d_1_valueOrError0_).PropagateFailure()
            return res
        d_3_ciphertext_: _dafny.Seq
        d_3_ciphertext_ = (d_1_valueOrError0_).Extract()
        d_4_output_: MaterialWrapping.WrapOutput
        d_4_output_ = MaterialWrapping.WrapOutput_WrapOutput(d_3_ciphertext_, RsaWrapInfo_RsaWrapInfo())
        res = Wrappers.Result_Success(d_4_output_)
        return res
        return res

    @property
    def cryptoPrimitives(self):
        return self._cryptoPrimitives
    @property
    def publicKey(self):
        return self._publicKey
    @property
    def paddingScheme(self):
        return self._paddingScheme

class RsaUnwrapKeyMaterial(MaterialWrapping.UnwrapMaterial, Actions.ActionWithResult, Actions.Action):
    def  __init__(self):
        self._cryptoPrimitives: AtomicPrimitives.AtomicPrimitivesClient = None
        self._privateKey: _dafny.Seq = _dafny.Seq({})
        self._paddingScheme: AwsCryptographyPrimitivesTypes.RSAPaddingMode = AwsCryptographyPrimitivesTypes.RSAPaddingMode.default()()
        pass

    def __dafnystr__(self) -> str:
        return "RawRSAKeyring.RsaUnwrapKeyMaterial"
    def ctor__(self, privateKey, paddingScheme, cryptoPrimitives):
        (self)._privateKey = privateKey
        (self)._paddingScheme = paddingScheme
        (self)._cryptoPrimitives = cryptoPrimitives

    def Invoke(self, input):
        res: Wrappers.Result = Wrappers.Result.default(MaterialWrapping.UnwrapOutput.default(RsaUnwrapInfo.default()))()
        d_0_suite_: AwsCryptographyMaterialProvidersTypes.AlgorithmSuiteInfo
        d_0_suite_ = (input).algorithmSuite
        d_1_wrappedMaterial_: _dafny.Seq
        d_1_wrappedMaterial_ = (input).wrappedMaterial
        d_2_aad_: _dafny.Map
        d_2_aad_ = (input).encryptionContext
        d_3_maybeDecryptResult_: Wrappers.Result
        out0_: Wrappers.Result
        out0_ = ((self).cryptoPrimitives).RSADecrypt(AwsCryptographyPrimitivesTypes.RSADecryptInput_RSADecryptInput((self).paddingScheme, (self).privateKey, d_1_wrappedMaterial_))
        d_3_maybeDecryptResult_ = out0_
        d_4_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        def lambda0_(d_5_e_):
            return AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographyPrimitives(d_5_e_)

        d_4_valueOrError0_ = (d_3_maybeDecryptResult_).MapFailure(lambda0_)
        if (d_4_valueOrError0_).IsFailure():
            res = (d_4_valueOrError0_).PropagateFailure()
            return res
        d_6_decryptResult_: _dafny.Seq
        d_6_decryptResult_ = (d_4_valueOrError0_).Extract()
        d_7_valueOrError1_: Wrappers.Outcome = Wrappers.Outcome.default()()
        d_7_valueOrError1_ = Wrappers.default__.Need((len(d_6_decryptResult_)) == (AlgorithmSuites.default__.GetEncryptKeyLength(d_0_suite_)), AwsCryptographyMaterialProvidersTypes.Error_AwsCryptographicMaterialProvidersException(_dafny.Seq("Invalid plaintext length.")))
        if (d_7_valueOrError1_).IsFailure():
            res = (d_7_valueOrError1_).PropagateFailure()
            return res
        d_8_output_: MaterialWrapping.UnwrapOutput
        d_8_output_ = MaterialWrapping.UnwrapOutput_UnwrapOutput(d_6_decryptResult_, RsaUnwrapInfo_RsaUnwrapInfo())
        res = Wrappers.Result_Success(d_8_output_)
        return res
        return res

    @property
    def cryptoPrimitives(self):
        return self._cryptoPrimitives
    @property
    def privateKey(self):
        return self._privateKey
    @property
    def paddingScheme(self):
        return self._paddingScheme
