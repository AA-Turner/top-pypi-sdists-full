import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import module_ as module_
import _dafny as _dafny
import System_ as System_
import smithy_dafny_standard_library.internaldafny.generated.Wrappers as Wrappers
import smithy_dafny_standard_library.internaldafny.generated.Relations as Relations
import smithy_dafny_standard_library.internaldafny.generated.Seq_MergeSort as Seq_MergeSort
import smithy_dafny_standard_library.internaldafny.generated.Math as Math
import smithy_dafny_standard_library.internaldafny.generated.Seq as Seq
import smithy_dafny_standard_library.internaldafny.generated.BoundedInts as BoundedInts
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
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_UInt as StandardLibrary_UInt
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_MemoryMath as StandardLibrary_MemoryMath
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_Sequence as StandardLibrary_Sequence
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_String as StandardLibrary_String
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary as StandardLibrary
import smithy_dafny_standard_library.internaldafny.generated.UUID as UUID
import smithy_dafny_standard_library.internaldafny.generated.UTF8 as UTF8
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
import TestUUID as TestUUID

# Module: TestUTF8

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def TestEncodeHappyCase():
        d_0_unicodeString_: _dafny.Seq
        d_0_unicodeString_ = _dafny.Seq("abc\u0306\u01FD\u03B2")
        d_1_expectedBytes_: _dafny.Seq
        d_1_expectedBytes_ = _dafny.Seq([97, 98, 99, 204, 134, 199, 189, 206, 178])
        d_2_valueOrError0_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_2_valueOrError0_ = UTF8.default__.Encode(d_0_unicodeString_)
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(14,19): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_encoded_: _dafny.Seq
        d_3_encoded_ = (d_2_valueOrError0_).Extract()
        if not((d_1_expectedBytes_) == (d_3_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(15,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestEncodeInvalidUnicode():
        d_0_invalidUnicode_: _dafny.Seq
        d_0_invalidUnicode_ = _dafny.Seq("abc\uD800")
        d_1_encoded_: Wrappers.Result
        d_1_encoded_ = UTF8.default__.Encode(d_0_invalidUnicode_)
        if not((d_1_encoded_).is_Failure):
            raise _dafny.HaltException("test/UTF8.dfy(22,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestDecodeHappyCase():
        d_0_unicodeBytes_: _dafny.Seq
        d_0_unicodeBytes_ = _dafny.Seq([97, 98, 99, 204, 134, 199, 189, 206, 178])
        d_1_expectedString_: _dafny.Seq
        d_1_expectedString_ = _dafny.Seq("abc\u0306\u01FD\u03B2")
        d_2_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_2_valueOrError0_ = UTF8.default__.Decode(d_0_unicodeBytes_)
        if not(not((d_2_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(32,19): " + _dafny.string_of(d_2_valueOrError0_))
        d_3_decoded_: _dafny.Seq
        d_3_decoded_ = (d_2_valueOrError0_).Extract()
        if not((d_1_expectedString_) == (d_3_decoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(33,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestDecodeInvalidUnicode():
        d_0_invalidUnicode_: _dafny.Seq
        d_0_invalidUnicode_ = _dafny.Seq([97, 98, 99, 237, 160, 128])
        if not(not(UTF8.default__.ValidUTF8Seq(d_0_invalidUnicode_))):
            raise _dafny.HaltException("test/UTF8.dfy(39,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((UTF8.default__.Decode(d_0_invalidUnicode_)).is_Failure):
            raise _dafny.HaltException("test/UTF8.dfy(40,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def Test1Byte():
        d_0_decoded_: _dafny.Seq
        d_0_decoded_ = _dafny.Seq("\u0000")
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_1_valueOrError0_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(46,19): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_encoded_: _dafny.Seq
        d_2_encoded_ = (d_1_valueOrError0_).Extract()
        if not((_dafny.Seq([0])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(47,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses1Byte(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(48,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_3_valueOrError1_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(49,21): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_redecoded_: _dafny.Seq
        d_4_redecoded_ = (d_3_valueOrError1_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(50,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u0020")
        d_5_valueOrError2_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_5_valueOrError2_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_5_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(54,15): " + _dafny.string_of(d_5_valueOrError2_))
        d_2_encoded_ = (d_5_valueOrError2_).Extract()
        if not((_dafny.Seq([32])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(55,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses1Byte(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(56,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_6_valueOrError3_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_6_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(57,17): " + _dafny.string_of(d_6_valueOrError3_))
        d_4_redecoded_ = (d_6_valueOrError3_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(58,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("$")
        d_7_valueOrError4_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_7_valueOrError4_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_7_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(61,15): " + _dafny.string_of(d_7_valueOrError4_))
        d_2_encoded_ = (d_7_valueOrError4_).Extract()
        if not((_dafny.Seq([36])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(62,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses1Byte(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(63,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError5_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_8_valueOrError5_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_8_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(64,17): " + _dafny.string_of(d_8_valueOrError5_))
        d_4_redecoded_ = (d_8_valueOrError5_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(65,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("0")
        d_9_valueOrError6_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_9_valueOrError6_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_9_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(68,15): " + _dafny.string_of(d_9_valueOrError6_))
        d_2_encoded_ = (d_9_valueOrError6_).Extract()
        if not((_dafny.Seq([48])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(69,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses1Byte(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(70,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError7_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_10_valueOrError7_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_10_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(71,17): " + _dafny.string_of(d_10_valueOrError7_))
        d_4_redecoded_ = (d_10_valueOrError7_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(72,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("A")
        d_11_valueOrError8_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_11_valueOrError8_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_11_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(75,15): " + _dafny.string_of(d_11_valueOrError8_))
        d_2_encoded_ = (d_11_valueOrError8_).Extract()
        if not((_dafny.Seq([65])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(76,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses1Byte(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(77,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_12_valueOrError9_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_12_valueOrError9_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_12_valueOrError9_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(78,17): " + _dafny.string_of(d_12_valueOrError9_))
        d_4_redecoded_ = (d_12_valueOrError9_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(79,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("a")
        d_13_valueOrError10_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_13_valueOrError10_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_13_valueOrError10_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(82,15): " + _dafny.string_of(d_13_valueOrError10_))
        d_2_encoded_ = (d_13_valueOrError10_).Extract()
        if not((_dafny.Seq([97])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(83,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses1Byte(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(84,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_14_valueOrError11_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_14_valueOrError11_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_14_valueOrError11_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(85,17): " + _dafny.string_of(d_14_valueOrError11_))
        d_4_redecoded_ = (d_14_valueOrError11_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(86,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def Test2Bytes():
        d_0_decoded_: _dafny.Seq
        d_0_decoded_ = _dafny.Seq("\u00A3")
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_1_valueOrError0_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(92,19): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_encoded_: _dafny.Seq
        d_2_encoded_ = (d_1_valueOrError0_).Extract()
        if not((_dafny.Seq([194, 163])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(93,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses2Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(94,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_3_valueOrError1_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(95,21): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_redecoded_: _dafny.Seq
        d_4_redecoded_ = (d_3_valueOrError1_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(96,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u00A9")
        d_5_valueOrError2_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_5_valueOrError2_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_5_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(100,15): " + _dafny.string_of(d_5_valueOrError2_))
        d_2_encoded_ = (d_5_valueOrError2_).Extract()
        if not((_dafny.Seq([194, 169])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(101,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses2Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(102,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_6_valueOrError3_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_6_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(103,17): " + _dafny.string_of(d_6_valueOrError3_))
        d_4_redecoded_ = (d_6_valueOrError3_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(104,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u00AE")
        d_7_valueOrError4_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_7_valueOrError4_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_7_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(108,15): " + _dafny.string_of(d_7_valueOrError4_))
        d_2_encoded_ = (d_7_valueOrError4_).Extract()
        if not((_dafny.Seq([194, 174])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(109,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses2Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(110,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError5_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_8_valueOrError5_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_8_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(111,17): " + _dafny.string_of(d_8_valueOrError5_))
        d_4_redecoded_ = (d_8_valueOrError5_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(112,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u03C0")
        d_9_valueOrError6_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_9_valueOrError6_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_9_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(116,15): " + _dafny.string_of(d_9_valueOrError6_))
        d_2_encoded_ = (d_9_valueOrError6_).Extract()
        if not((_dafny.Seq([207, 128])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(117,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses2Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(118,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError7_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_10_valueOrError7_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_10_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(119,17): " + _dafny.string_of(d_10_valueOrError7_))
        d_4_redecoded_ = (d_10_valueOrError7_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(120,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def Test3Bytes():
        d_0_decoded_: _dafny.Seq
        d_0_decoded_ = _dafny.Seq("\u2386")
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_1_valueOrError0_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(126,19): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_encoded_: _dafny.Seq
        d_2_encoded_ = (d_1_valueOrError0_).Extract()
        if not((_dafny.Seq([226, 142, 134])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(127,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses3Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(128,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_3_valueOrError1_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(129,21): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_redecoded_: _dafny.Seq
        d_4_redecoded_ = (d_3_valueOrError1_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(130,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u2387")
        d_5_valueOrError2_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_5_valueOrError2_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_5_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(134,15): " + _dafny.string_of(d_5_valueOrError2_))
        d_2_encoded_ = (d_5_valueOrError2_).Extract()
        if not((_dafny.Seq([226, 142, 135])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(135,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses3Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(136,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_6_valueOrError3_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_6_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(137,17): " + _dafny.string_of(d_6_valueOrError3_))
        d_4_redecoded_ = (d_6_valueOrError3_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(138,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u231B")
        d_7_valueOrError4_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_7_valueOrError4_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_7_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(142,15): " + _dafny.string_of(d_7_valueOrError4_))
        d_2_encoded_ = (d_7_valueOrError4_).Extract()
        if not((_dafny.Seq([226, 140, 155])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(143,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses3Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(144,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError5_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_8_valueOrError5_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_8_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(145,17): " + _dafny.string_of(d_8_valueOrError5_))
        d_4_redecoded_ = (d_8_valueOrError5_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(146,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u1D78")
        d_9_valueOrError6_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_9_valueOrError6_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_9_valueOrError6_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(150,15): " + _dafny.string_of(d_9_valueOrError6_))
        d_2_encoded_ = (d_9_valueOrError6_).Extract()
        if not((_dafny.Seq([225, 181, 184])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(151,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses3Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(152,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError7_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_10_valueOrError7_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_10_valueOrError7_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(153,17): " + _dafny.string_of(d_10_valueOrError7_))
        d_4_redecoded_ = (d_10_valueOrError7_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(154,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\u732B")
        d_11_valueOrError8_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_11_valueOrError8_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_11_valueOrError8_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(158,15): " + _dafny.string_of(d_11_valueOrError8_))
        d_2_encoded_ = (d_11_valueOrError8_).Extract()
        if not((_dafny.Seq([231, 140, 171])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(159,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses3Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(160,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_12_valueOrError9_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_12_valueOrError9_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_12_valueOrError9_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(161,17): " + _dafny.string_of(d_12_valueOrError9_))
        d_4_redecoded_ = (d_12_valueOrError9_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(162,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def Test4Bytes():
        d_0_decoded_: _dafny.Seq
        d_0_decoded_ = _dafny.Seq("\uD808\uDC00")
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_1_valueOrError0_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(168,19): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_encoded_: _dafny.Seq
        d_2_encoded_ = (d_1_valueOrError0_).Extract()
        if not((_dafny.Seq([240, 146, 128, 128])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(169,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses4Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(170,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_3_valueOrError1_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(171,21): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_redecoded_: _dafny.Seq
        d_4_redecoded_ = (d_3_valueOrError1_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(172,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_0_decoded_ = _dafny.Seq("\uD835\uDFC1")
        d_5_valueOrError2_: Wrappers.Result = Wrappers.Result.default(UTF8.ValidUTF8Bytes.default)()
        d_5_valueOrError2_ = UTF8.default__.Encode(d_0_decoded_)
        if not(not((d_5_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(176,15): " + _dafny.string_of(d_5_valueOrError2_))
        d_2_encoded_ = (d_5_valueOrError2_).Extract()
        if not((_dafny.Seq([240, 157, 159, 129])) == (d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(177,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(UTF8.default__.Uses4Bytes(d_2_encoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(178,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_6_valueOrError3_ = UTF8.default__.Decode(d_2_encoded_)
        if not(not((d_6_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/UTF8.dfy(179,17): " + _dafny.string_of(d_6_valueOrError3_))
        d_4_redecoded_ = (d_6_valueOrError3_).Extract()
        if not((d_0_decoded_) == (d_4_redecoded_)):
            raise _dafny.HaltException("test/UTF8.dfy(180,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

