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
import aws_cryptography_internal_kms.internaldafny.generated.ComAmazonawsKmsTypes as ComAmazonawsKmsTypes
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
import aws_cryptography_internal_kms.internaldafny.generated.Com_Amazonaws_Kms as Com_Amazonaws_Kms

# Module: TestComAmazonawsKms

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def workAround(literal):
        return literal

    @staticmethod
    def BasicDecryptTests():
        d_0_CiphertextBlob_: _dafny.Seq
        d_0_CiphertextBlob_ = _dafny.Seq([1, 1, 1, 0, 120, 64, 243, 140, 39, 94, 49, 9, 116, 22, 193, 7, 41, 81, 80, 87, 25, 100, 173, 163, 239, 28, 33, 233, 76, 139, 160, 189, 188, 157, 15, 180, 20, 0, 0, 0, 98, 48, 96, 6, 9, 42, 134, 72, 134, 247, 13, 1, 7, 6, 160, 83, 48, 81, 2, 1, 0, 48, 76, 6, 9, 42, 134, 72, 134, 247, 13, 1, 7, 1, 48, 30, 6, 9, 96, 134, 72, 1, 101, 3, 4, 1, 46, 48, 17, 4, 12, 196, 249, 60, 7, 21, 231, 87, 70, 216, 12, 31, 13, 2, 1, 16, 128, 31, 222, 119, 162, 112, 88, 153, 39, 197, 21, 182, 116, 176, 120, 174, 107, 82, 182, 223, 160, 201, 15, 29, 3, 254, 3, 208, 72, 171, 64, 207, 175])
        default__.BasicDecryptTest(ComAmazonawsKmsTypes.DecryptRequest_DecryptRequest(default__.workAround(d_0_CiphertextBlob_), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(default__.keyId), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()), _dafny.Seq([165, 191, 67, 62]), default__.keyId)

    @staticmethod
    def BasicGenerateTests():
        default__.BasicGenerateTest(ComAmazonawsKmsTypes.GenerateDataKeyRequest_GenerateDataKeyRequest(default__.keyId, Wrappers.Option_None(), Wrappers.Option_Some(32), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))

    @staticmethod
    def BasicGenerateWithoutPlaintextTests():
        default__.BasicGenerateWithoutPlaintextTest(ComAmazonawsKmsTypes.GenerateDataKeyWithoutPlaintextRequest_GenerateDataKeyWithoutPlaintextRequest(default__.keyIdGenerateWOPlain, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(32), Wrappers.Option_None(), Wrappers.Option_None()))

    @staticmethod
    def BasicEncryptTests():
        default__.BasicEncryptTest(ComAmazonawsKmsTypes.EncryptRequest_EncryptRequest(default__.keyId, _dafny.Seq([97, 115, 100, 102]), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))

    @staticmethod
    def BasicFailTests():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(117,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_ret_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).GenerateDataKeyWithoutPlaintext(default__.failingInput)
        d_2_ret_ = out1_
        if not((d_2_ret_).is_Failure):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(119,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_err_: ComAmazonawsKmsTypes.Error
        d_3_err_ = (d_2_ret_).error
        if not((d_3_err_).is_OpaqueWithText):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(121,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        source0_ = d_3_err_
        with _dafny.label("match0"):
            if True:
                if source0_.is_OpaqueWithText:
                    d_4_obj_ = source0_.obj
                    d_5_objMessage_ = source0_.objMessage
                    if not(True):
                        raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(123,46): " + _dafny.string_of(_dafny.Seq("expectation violation")))
                    raise _dafny.Break("match0")
            if True:
                if not(False):
                    raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(124,16): " + _dafny.string_of(_dafny.Seq("Failing KMS Key MUST cause an OpaqueError that can later be unwrapped to a proper but generic KMS Exception.")))
            pass

    @staticmethod
    def BasicDecryptTest(input, expectedPlaintext, expectedKeyId):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(134,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_ret_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).Decrypt(input)
        d_2_ret_ = out1_
        if not((d_2_ret_).is_Success):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(140,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        let_tmp_rhs0_ = (d_2_ret_).value
        d_3_KeyId_ = let_tmp_rhs0_.KeyId
        d_4_Plaintext_ = let_tmp_rhs0_.Plaintext
        d_5_EncryptionAlgorithm_ = let_tmp_rhs0_.EncryptionAlgorithm
        d_6_CiphertextBlob_ = let_tmp_rhs0_.CiphertextForRecipient
        if not((d_4_Plaintext_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(144,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_3_KeyId_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(145,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_4_Plaintext_).value) == (expectedPlaintext)):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(146,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_KeyId_).value) == (expectedKeyId)):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(147,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def BasicGenerateTest(input):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(155,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_ret_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).GenerateDataKey(input)
        d_2_ret_ = out1_
        if not((d_2_ret_).is_Success):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(159,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        let_tmp_rhs0_ = (d_2_ret_).value
        d_3_CiphertextBlob_ = let_tmp_rhs0_.CiphertextBlob
        d_4_Plaintext_ = let_tmp_rhs0_.Plaintext
        d_5_KeyId_ = let_tmp_rhs0_.KeyId
        d_6_CiphertextForRecipient_ = let_tmp_rhs0_.CiphertextForRecipient
        if not((d_3_CiphertextBlob_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(163,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_4_Plaintext_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(164,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_5_KeyId_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(165,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((len((d_4_Plaintext_).value)) == (((input).NumberOfBytes).value)):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(166,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_7_decryptInput_: ComAmazonawsKmsTypes.DecryptRequest
        d_7_decryptInput_ = ComAmazonawsKmsTypes.DecryptRequest_DecryptRequest((d_3_CiphertextBlob_).value, (input).EncryptionContext, (input).GrantTokens, Wrappers.Option_Some((d_5_KeyId_).value), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None())
        default__.BasicDecryptTest(d_7_decryptInput_, (d_4_Plaintext_).value, (input).KeyId)

    @staticmethod
    def BasicGenerateWithoutPlaintextTest(input):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(188,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_retGenerate_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).GenerateDataKeyWithoutPlaintext(input)
        d_2_retGenerate_ = out1_
        if not((d_2_retGenerate_).is_Success):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(192,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        let_tmp_rhs0_ = (d_2_retGenerate_).value
        d_3_CiphertextBlob_ = let_tmp_rhs0_.CiphertextBlob
        d_4_KeyId_ = let_tmp_rhs0_.KeyId
        if not((d_3_CiphertextBlob_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(196,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_4_KeyId_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(197,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_5_decryptInput_: ComAmazonawsKmsTypes.DecryptRequest
        d_5_decryptInput_ = ComAmazonawsKmsTypes.DecryptRequest_DecryptRequest((d_3_CiphertextBlob_).value, (input).EncryptionContext, (input).GrantTokens, Wrappers.Option_Some((d_4_KeyId_).value), Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None())
        d_6_ret_: Wrappers.Result
        out2_: Wrappers.Result
        out2_ = (d_1_client_).Decrypt(d_5_decryptInput_)
        d_6_ret_ = out2_
        if not((d_6_ret_).is_Success):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(208,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        let_tmp_rhs1_ = (d_6_ret_).value
        d_7_KeyIdTwo_ = let_tmp_rhs1_.KeyId
        d_8_Plaintext_ = let_tmp_rhs1_.Plaintext
        d_9_EncryptionAlgorithm_ = let_tmp_rhs1_.EncryptionAlgorithm
        d_10_CiphertextBlobTwo_ = let_tmp_rhs1_.CiphertextForRecipient
        if not((d_7_KeyIdTwo_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(211,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_7_KeyIdTwo_).value) == ((d_4_KeyId_).value)):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(212,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def BasicEncryptTest(input):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(219,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_ret_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).Encrypt(input)
        d_2_ret_ = out1_
        if not((d_2_ret_).is_Success):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(223,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        let_tmp_rhs0_ = (d_2_ret_).value
        d_3_CiphertextBlob_ = let_tmp_rhs0_.CiphertextBlob
        d_4_KeyId_ = let_tmp_rhs0_.KeyId
        d_5_EncryptionAlgorithm_ = let_tmp_rhs0_.EncryptionAlgorithm
        if not((d_3_CiphertextBlob_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(227,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_4_KeyId_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(228,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_decryptInput_: ComAmazonawsKmsTypes.DecryptRequest
        d_6_decryptInput_ = ComAmazonawsKmsTypes.DecryptRequest_DecryptRequest((d_3_CiphertextBlob_).value, (input).EncryptionContext, (input).GrantTokens, Wrappers.Option_Some((d_4_KeyId_).value), (input).EncryptionAlgorithm, Wrappers.Option_None(), Wrappers.Option_None())
        default__.BasicDecryptTest(d_6_decryptInput_, (input).Plaintext, (input).KeyId)

    @staticmethod
    def RegionMatchTest():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(248,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_region_: Wrappers.Option
        d_2_region_ = Com_Amazonaws_Kms.default__.RegionMatch(d_1_client_, default__.TEST__REGION)
        if not(((d_2_region_).is_None) or ((d_2_region_).value)):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(250,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def EmptyStringIsDefaultRegion():
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(_dafny.Seq(""))
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(255,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()

    @staticmethod
    def BasicDeriveSharedSecretTests(input):
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(262,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_ret_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).DeriveSharedSecret(ComAmazonawsKmsTypes.DeriveSharedSecretRequest_DeriveSharedSecretRequest((input).KeyId, (input).KeyAgreementAlgorithm, (input).PublicKey, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))
        d_2_ret_ = out1_
        if (d_2_ret_).is_Success:
            let_tmp_rhs0_ = (d_2_ret_).value
            d_3_KeyId_ = let_tmp_rhs0_.KeyId
            d_4_SharedSecret_ = let_tmp_rhs0_.SharedSecret
            d_5_CiphertextForRecipient_ = let_tmp_rhs0_.CiphertextForRecipient
            d_6_KeyAgreementAlgorithm_ = let_tmp_rhs0_.KeyAgreementAlgorithm
            d_7_KeyOrigin_ = let_tmp_rhs0_.KeyOrigin
            if not((d_4_SharedSecret_).is_Some):
                raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(275,6): " + _dafny.string_of(_dafny.Seq("expectation violation")))
            if not((d_3_KeyId_).is_Some):
                raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(276,6): " + _dafny.string_of(_dafny.Seq("expectation violation")))
            if not(((d_3_KeyId_).value) == ((input).KeyId)):
                raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(278,6): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        elif True:
            if not((d_2_ret_).is_Failure):
                raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(281,6): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def GetPublicKeyHelper(input):
        publicKey: _dafny.Seq = None
        d_0_valueOrError0_: Wrappers.Result = None
        out0_: Wrappers.Result
        out0_ = Com_Amazonaws_Kms.default__.KMSClientForRegion(default__.TEST__REGION)
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(292,18): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_client_: ComAmazonawsKmsTypes.IKMSClient
        d_1_client_ = (d_0_valueOrError0_).Extract()
        d_2_ret_: Wrappers.Result
        out1_: Wrappers.Result
        out1_ = (d_1_client_).GetPublicKey(ComAmazonawsKmsTypes.GetPublicKeyRequest_GetPublicKeyRequest((input).KeyId, (input).GrantTokens))
        d_2_ret_ = out1_
        if not((d_2_ret_).is_Success):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(299,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        let_tmp_rhs0_ = (d_2_ret_).value
        d_3___v1_ = let_tmp_rhs0_.KeyId
        d_4_PublicKey_ = let_tmp_rhs0_.PublicKey
        d_5___v2_ = let_tmp_rhs0_.CustomerMasterKeySpec
        d_6___v3_ = let_tmp_rhs0_.KeySpec
        d_7___v4_ = let_tmp_rhs0_.KeyUsage
        d_8___v5_ = let_tmp_rhs0_.EncryptionAlgorithms
        d_9___v6_ = let_tmp_rhs0_.SigningAlgorithms
        d_10___v7_ = let_tmp_rhs0_.KeyAgreementAlgorithms
        if not((d_4_PublicKey_).is_Some):
            raise _dafny.HaltException("test/TestComAmazonawsKms.dfy(302,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        publicKey = (d_4_PublicKey_).value
        return publicKey
        return publicKey

    @staticmethod
    def DeriveSharedSecretTestSuccess():
        d_0_recipientPublicKey_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = default__.GetPublicKeyHelper(ComAmazonawsKmsTypes.GetPublicKeyRequest_GetPublicKeyRequest(default__.recipientKmsKey, Wrappers.Option_None()))
        d_0_recipientPublicKey_ = out0_
        default__.BasicDeriveSharedSecretTests(ComAmazonawsKmsTypes.DeriveSharedSecretRequest_DeriveSharedSecretRequest(default__.senderKmsKey, ComAmazonawsKmsTypes.KeyAgreementAlgorithmSpec_ECDH(), d_0_recipientPublicKey_, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))

    @staticmethod
    def DeriveSharedSecretTestFailure():
        d_0_recipientPublicKeyOnWrongCurve_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = default__.GetPublicKeyHelper(ComAmazonawsKmsTypes.GetPublicKeyRequest_GetPublicKeyRequest(default__.incorrectEccCurveKey, Wrappers.Option_None()))
        d_0_recipientPublicKeyOnWrongCurve_ = out0_
        default__.BasicDeriveSharedSecretTests(ComAmazonawsKmsTypes.DeriveSharedSecretRequest_DeriveSharedSecretRequest(default__.senderKmsKey, ComAmazonawsKmsTypes.KeyAgreementAlgorithmSpec_ECDH(), d_0_recipientPublicKeyOnWrongCurve_, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_None()))

    @staticmethod
    def CreateNoneForEncryptionContext():
        return Wrappers.Option_None()

    @staticmethod
    def CreateNoneForKeySpec():
        return Wrappers.Option_None()

    @staticmethod
    def CreateNoneForNumberOfBytes():
        return Wrappers.Option_None()

    @staticmethod
    def CreateNoneForGrantTokens():
        return Wrappers.Option_None()

    @staticmethod
    def CreateNoneForDryRun():
        return Wrappers.Option_None()

    @_dafny.classproperty
    def TEST__REGION(instance):
        return _dafny.Seq("us-west-2")
    @_dafny.classproperty
    def keyId(instance):
        return _dafny.Seq("arn:aws:kms:us-west-2:658956600833:key/b3537ef1-d8dc-4780-9f5a-55776cbb2f7f")
    @_dafny.classproperty
    def keyIdGenerateWOPlain(instance):
        return _dafny.Seq("arn:aws:kms:us-west-2:370957321024:key/9d989aa2-2f9c-438c-a745-cc57d3ad0126")
    @_dafny.classproperty
    def failingKeyId(instance):
        return _dafny.Seq("arn:aws:kms:us-west-2:370957321024:key/e20ac7b8-3d95-46ee-b3d5-f5dca6393945")
    @_dafny.classproperty
    def failingInput(instance):
        return ComAmazonawsKmsTypes.GenerateDataKeyWithoutPlaintextRequest_GenerateDataKeyWithoutPlaintextRequest(default__.failingKeyId, Wrappers.Option_None(), Wrappers.Option_None(), Wrappers.Option_Some(32), Wrappers.Option_None(), Wrappers.Option_None())
    @_dafny.classproperty
    def recipientKmsKey(instance):
        return _dafny.Seq("arn:aws:kms:us-west-2:370957321024:key/0265c8e9-5b6a-4055-8f70-63719e09fda5")
    @_dafny.classproperty
    def senderKmsKey(instance):
        return _dafny.Seq("arn:aws:kms:us-west-2:370957321024:key/eabdf483-6be2-4d2d-8ee4-8c2583d416e9")
    @_dafny.classproperty
    def incorrectEccCurveKey(instance):
        return _dafny.Seq("arn:aws:kms:us-west-2:370957321024:key/7f35a704-f4fb-469d-98b1-62a1fa2cc44e")
