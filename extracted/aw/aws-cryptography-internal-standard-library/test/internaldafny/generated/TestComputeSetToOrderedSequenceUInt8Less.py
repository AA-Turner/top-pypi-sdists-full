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
import TestTime as TestTime
import TestStrings as TestStrings

# Module: TestComputeSetToOrderedSequenceUInt8Less

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def UInt8Greater(x, y):
        return (y) < (x)

    @staticmethod
    def TestSetToOrderedSequenceEmpty():
        d_0_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(_dafny.Set({}), StandardLibrary_UInt.default__.UInt8Less)
        d_0_output_ = out0_
        d_1_output2_: _dafny.Seq
        d_1_output2_ = SortedSets.default__.SetToOrderedSequence2(_dafny.Set({}), StandardLibrary_UInt.default__.UInt8Less)
        d_2_expected_: _dafny.Seq
        d_2_expected_ = _dafny.Seq([])
        if not((d_0_output_) == (d_2_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(31,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_1_output2_) == (d_2_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(32,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceOneItem():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq([0])})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq([0])])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(40,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(41,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceSimple():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq([0, 2]), _dafny.Seq([0, 1])})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq([0, 1]), _dafny.Seq([0, 2])])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(49,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(50,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequencePrefix():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq([0, 1, 2]), _dafny.Seq([0, 1])})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq([0, 1]), _dafny.Seq([0, 1, 2])])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(58,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(59,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceComplex():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq([0, 1, 2]), _dafny.Seq([1, 1, 2]), _dafny.Seq([0, 1])})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq([0, 1]), _dafny.Seq([0, 1, 2]), _dafny.Seq([1, 1, 2])])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(67,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(68,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceComplexReverse():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq([0, 1, 2]), _dafny.Seq([1, 1, 2]), _dafny.Seq([0, 1])})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.UInt8Greater)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.UInt8Greater)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq([1, 1, 2]), _dafny.Seq([0, 1]), _dafny.Seq([0, 1, 2])])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(76,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(77,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetSequence():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq([0, 1, 2]), _dafny.Seq([1, 1, 2]), _dafny.Seq([0, 1])})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToSequence(d_0_a_)
        d_1_output_ = out0_
        if not((_dafny.MultiSet(d_1_output_)) == (_dafny.MultiSet(d_0_a_))):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(83,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceManyItems():
        d_0_time_: Time.AbsoluteTime
        out0_: Time.AbsoluteTime
        out0_ = Time.default__.GetAbsoluteTime()
        d_0_time_ = out0_
        d_1_a_: _dafny.Set
        def iife0_():
            coll0_ = _dafny.Set()
            compr_0_: int
            for compr_0_ in _dafny.IntegerRange(0, BoundedInts.default__.TWO__TO__THE__16):
                d_2_x_: int = compr_0_
                if True:
                    if ((0) <= (d_2_x_)) and ((d_2_x_) < (65535)):
                        coll0_ = coll0_.union(_dafny.Set([StandardLibrary_UInt.default__.UInt16ToSeq(d_2_x_)]))
            return _dafny.Set(coll0_)
        d_1_a_ = iife0_()
        
        out1_: Time.AbsoluteTime
        out1_ = Time.default__.PrintTimeSinceShortChained(d_0_time_)
        d_0_time_ = out1_
        d_3_output_: _dafny.Seq
        out2_: _dafny.Seq
        out2_ = SortedSets.default__.SetToOrderedSequence(d_1_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_3_output_ = out2_
        d_4_output2_: _dafny.Seq
        d_4_output2_ = SortedSets.default__.SetToOrderedSequence2(d_1_a_, StandardLibrary_UInt.default__.UInt8Less)
        d_5_expected_: _dafny.Seq
        d_5_expected_ = _dafny.Seq([StandardLibrary_UInt.default__.UInt16ToSeq(d_6_i_) for d_6_i_ in range(65535)])
        if not((d_3_output_) == (d_5_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(93,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_4_output2_) == (d_5_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceUInt8Less.dfy(94,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        Time.default__.PrintTimeSinceShort(d_0_time_)

