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

# Module: TestUUID

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def TestFromBytesSuccess():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_valueOrError0_ = UUID.default__.FromByteArray(default__.byteUuid)
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(23,21): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_fromBytes_: _dafny.Seq
        d_1_fromBytes_ = (d_0_valueOrError0_).Extract()
        if not((d_1_fromBytes_) == (default__.uuid)):
            raise _dafny.HaltException("test/UUID.dfy(24,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestFromBytesFailure():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_valueOrError0_ = UUID.default__.FromByteArray(default__.wrongByteUuid)
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(28,21): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_fromBytes_: _dafny.Seq
        d_1_fromBytes_ = (d_0_valueOrError0_).Extract()
        if not((d_1_fromBytes_) != (default__.uuid)):
            raise _dafny.HaltException("test/UUID.dfy(29,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestToBytesSuccess():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_valueOrError0_ = UUID.default__.ToByteArray(default__.uuid)
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(33,19): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_toBytes_: _dafny.Seq
        d_1_toBytes_ = (d_0_valueOrError0_).Extract()
        if not((d_1_toBytes_) == (default__.byteUuid)):
            raise _dafny.HaltException("test/UUID.dfy(34,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestToBytesFailure():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_valueOrError0_ = UUID.default__.ToByteArray(default__.uuid)
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(38,19): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_toBytes_: _dafny.Seq
        d_1_toBytes_ = (d_0_valueOrError0_).Extract()
        if not((d_1_toBytes_) != (default__.wrongByteUuid)):
            raise _dafny.HaltException("test/UUID.dfy(39,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestRoundTripStringConversion():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_valueOrError0_ = UUID.default__.ToByteArray(default__.uuid)
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(43,25): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_stringToBytes_: _dafny.Seq
        d_1_stringToBytes_ = (d_0_valueOrError0_).Extract()
        if not((len(d_1_stringToBytes_)) == (16)):
            raise _dafny.HaltException("test/UUID.dfy(44,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_2_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_2_valueOrError1_ = UUID.default__.FromByteArray(d_1_stringToBytes_)
        if not(not((d_2_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(45,25): " + _dafny.string_of(d_2_valueOrError1_))
        d_3_bytesToString_: _dafny.Seq
        d_3_bytesToString_ = (d_2_valueOrError1_).Extract()
        if not((d_3_bytesToString_) == (default__.uuid)):
            raise _dafny.HaltException("test/UUID.dfy(46,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestRoundTripByteConversion():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_0_valueOrError0_ = UUID.default__.FromByteArray(default__.byteUuid)
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(50,25): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_bytesToString_: _dafny.Seq
        d_1_bytesToString_ = (d_0_valueOrError0_).Extract()
        d_2_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_2_valueOrError1_ = UUID.default__.ToByteArray(d_1_bytesToString_)
        if not(not((d_2_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(51,25): " + _dafny.string_of(d_2_valueOrError1_))
        d_3_stringToBytes_: _dafny.Seq
        d_3_stringToBytes_ = (d_2_valueOrError1_).Extract()
        if not((len(d_3_stringToBytes_)) == (16)):
            raise _dafny.HaltException("test/UUID.dfy(52,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_3_stringToBytes_) == (default__.byteUuid)):
            raise _dafny.HaltException("test/UUID.dfy(53,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestGenerateAndConversion():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out0_: Wrappers.Result
        out0_ = UUID.default__.GenerateUUID()
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(57,22): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_uuidString_: _dafny.Seq
        d_1_uuidString_ = (d_0_valueOrError0_).Extract()
        d_2_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_2_valueOrError1_ = UUID.default__.ToByteArray(d_1_uuidString_)
        if not(not((d_2_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(58,21): " + _dafny.string_of(d_2_valueOrError1_))
        d_3_uuidBytes_: _dafny.Seq
        d_3_uuidBytes_ = (d_2_valueOrError1_).Extract()
        d_4_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_4_valueOrError2_ = UUID.default__.FromByteArray(d_3_uuidBytes_)
        if not(not((d_4_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(60,25): " + _dafny.string_of(d_4_valueOrError2_))
        d_5_bytesToString_: _dafny.Seq
        d_5_bytesToString_ = (d_4_valueOrError2_).Extract()
        d_6_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_6_valueOrError3_ = UUID.default__.ToByteArray(d_5_bytesToString_)
        if not(not((d_6_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(61,25): " + _dafny.string_of(d_6_valueOrError3_))
        d_7_stringToBytes_: _dafny.Seq
        d_7_stringToBytes_ = (d_6_valueOrError3_).Extract()
        if not((len(d_7_stringToBytes_)) == (16)):
            raise _dafny.HaltException("test/UUID.dfy(62,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_7_stringToBytes_) == (d_3_uuidBytes_)):
            raise _dafny.HaltException("test/UUID.dfy(63,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_8_valueOrError4_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_8_valueOrError4_ = UUID.default__.ToByteArray(d_1_uuidString_)
        if not(not((d_8_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(65,29): " + _dafny.string_of(d_8_valueOrError4_))
        d_9_uuidStringToBytes_: _dafny.Seq
        d_9_uuidStringToBytes_ = (d_8_valueOrError4_).Extract()
        if not((len(d_9_uuidStringToBytes_)) == (16)):
            raise _dafny.HaltException("test/UUID.dfy(66,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_10_valueOrError5_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        d_10_valueOrError5_ = UUID.default__.FromByteArray(d_9_uuidStringToBytes_)
        if not(not((d_10_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("test/UUID.dfy(67,29): " + _dafny.string_of(d_10_valueOrError5_))
        d_11_uuidBytesToString_: _dafny.Seq
        d_11_uuidBytesToString_ = (d_10_valueOrError5_).Extract()
        if not((d_11_uuidBytesToString_) == (d_1_uuidString_)):
            raise _dafny.HaltException("test/UUID.dfy(68,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @_dafny.classproperty
    def byteUuid(instance):
        return _dafny.Seq([146, 56, 38, 88, 183, 160, 77, 151, 156, 73, 206, 228, 230, 114, 163, 179])
    @_dafny.classproperty
    def uuid(instance):
        return _dafny.Seq("92382658-b7a0-4d97-9c49-cee4e672a3b3")
    @_dafny.classproperty
    def wrongByteUuid(instance):
        return _dafny.Seq([146, 56, 38, 88, 183, 160, 77, 151, 156, 73, 206, 228, 230, 114, 163, 178])
