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
import TestUTF8 as TestUTF8

# Module: TestTime

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def TestFormat():
        if not((Time.default__.FormatMilliDiff(123456, 123456)) == (_dafny.Seq("0.000"))):
            raise _dafny.HaltException("test/Time.dfy(11,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((Time.default__.FormatMilliDiff(123456, 123457)) == (_dafny.Seq("0.001"))):
            raise _dafny.HaltException("test/Time.dfy(12,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((Time.default__.FormatMilliDiff(123456, 123467)) == (_dafny.Seq("0.011"))):
            raise _dafny.HaltException("test/Time.dfy(13,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((Time.default__.FormatMilliDiff(123456, 123567)) == (_dafny.Seq("0.111"))):
            raise _dafny.HaltException("test/Time.dfy(14,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((Time.default__.FormatMilliDiff(123456, 124567)) == (_dafny.Seq("1.111"))):
            raise _dafny.HaltException("test/Time.dfy(15,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((Time.default__.FormatMilliDiff(123456, 134567)) == (_dafny.Seq("11.111"))):
            raise _dafny.HaltException("test/Time.dfy(16,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((Time.default__.FormatMilliDiff(123456, 234567)) == (_dafny.Seq("111.111"))):
            raise _dafny.HaltException("test/Time.dfy(17,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestNonDecreasing():
        d_0_t1_: int
        out0_: int
        out0_ = Time.default__.CurrentRelativeTime()
        d_0_t1_ = out0_
        d_1_t2_: int
        out1_: int
        out1_ = Time.default__.CurrentRelativeTime()
        d_1_t2_ = out1_
        if not((d_1_t2_) >= (d_0_t1_)):
            raise _dafny.HaltException("test/Time.dfy(23,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestNonDecreasingMilli():
        d_0_t1_: int
        out0_: int
        out0_ = Time.default__.CurrentRelativeTimeMilli()
        d_0_t1_ = out0_
        d_1_t2_: int
        out1_: int
        out1_ = Time.default__.CurrentRelativeTimeMilli()
        d_1_t2_ = out1_
        if not((d_1_t2_) >= (d_0_t1_)):
            raise _dafny.HaltException("test/Time.dfy(29,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestPositiveValues():
        d_0_t1_: int
        out0_: int
        out0_ = Time.default__.CurrentRelativeTime()
        d_0_t1_ = out0_
        d_1_t2_: int
        out1_: int
        out1_ = Time.default__.CurrentRelativeTime()
        d_1_t2_ = out1_
        if not(((d_1_t2_) - (d_0_t1_)) >= (0)):
            raise _dafny.HaltException("test/Time.dfy(35,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestGetCurrentTimeStamp():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out0_: Wrappers.Result
        out0_ = Time.default__.GetCurrentTimeStamp()
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/Time.dfy(40,23): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_CurrentTime_: _dafny.Seq
        d_1_CurrentTime_ = (d_0_valueOrError0_).Extract()
        if not(default__.ISO8601_q(d_1_CurrentTime_)):
            raise _dafny.HaltException("test/Time.dfy(41,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def ISO8601_q(CreateTime):
        return ((((((((len(CreateTime)) == (27)) and (((CreateTime)[4]) == ('-'))) and (((CreateTime)[7]) == ('-'))) and (((CreateTime)[10]) == ('T'))) and (((CreateTime)[13]) == (':'))) and (((CreateTime)[16]) == (':'))) and (((CreateTime)[19]) == ('.'))) and (((CreateTime)[26]) == ('Z'))

