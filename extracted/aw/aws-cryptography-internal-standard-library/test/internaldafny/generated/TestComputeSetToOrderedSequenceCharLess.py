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
import TestComputeSetToOrderedSequenceUInt8Less as TestComputeSetToOrderedSequenceUInt8Less
import Sets as Sets

# Module: TestComputeSetToOrderedSequenceCharLess

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def CharLess(x, y):
        return (x) < (y)

    @staticmethod
    def CharGreater(x, y):
        return (y) < (x)

    @staticmethod
    def TestSetToOrderedSequenceEmpty():
        d_0_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(_dafny.Set({}), default__.CharLess)
        d_0_output_ = out0_
        d_1_output2_: _dafny.Seq
        d_1_output2_ = SortedSets.default__.SetToOrderedSequence2(_dafny.Set({}), default__.CharLess)
        d_2_expected_: _dafny.Seq
        d_2_expected_ = _dafny.Seq([])
        if not((d_0_output_) == (d_2_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(35,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_1_output2_) == (d_2_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(36,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceOneItem():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("a")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.CharLess)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.CharLess)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq("a")])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(44,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(45,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceSimple():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("ac"), _dafny.Seq("ab")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.CharLess)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.CharLess)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq("ab"), _dafny.Seq("ac")])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(53,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(54,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequencePrefix():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("abc"), _dafny.Seq("ab")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.CharLess)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.CharLess)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq("ab"), _dafny.Seq("abc")])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(62,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(63,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceComplex():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("abc"), _dafny.Seq("bbc"), _dafny.Seq("ab")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.CharLess)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.CharLess)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq("ab"), _dafny.Seq("abc"), _dafny.Seq("bbc")])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(71,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(72,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedSequenceComplexReverse():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("abc"), _dafny.Seq("bbc"), _dafny.Seq("ab")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.CharGreater)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.CharGreater)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq("bbc"), _dafny.Seq("ab"), _dafny.Seq("abc")])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(80,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(81,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetSequence():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("abc"), _dafny.Seq("bbc"), _dafny.Seq("ab")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToSequence(d_0_a_)
        d_1_output_ = out0_
        if not((_dafny.MultiSet(d_1_output_)) == (_dafny.MultiSet(d_0_a_))):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(87,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSetToOrderedComplexUnicode():
        d_0_a_: _dafny.Set
        d_0_a_ = _dafny.Set({_dafny.Seq("\ud801\udc37"), _dafny.Seq("&"), _dafny.Seq("Љ"), _dafny.Seq("ᝀ"), _dafny.Seq("\ud83c\udca1"), _dafny.Seq("｡"), _dafny.Seq("\ud800\udc02")})
        d_1_output_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = SortedSets.default__.SetToOrderedSequence(d_0_a_, default__.CharLess)
        d_1_output_ = out0_
        d_2_output2_: _dafny.Seq
        d_2_output2_ = SortedSets.default__.SetToOrderedSequence2(d_0_a_, default__.CharLess)
        d_3_expected_: _dafny.Seq
        d_3_expected_ = _dafny.Seq([_dafny.Seq("&"), _dafny.Seq("Љ"), _dafny.Seq("ᝀ"), _dafny.Seq("\ud800\udc02"), _dafny.Seq("\ud801\udc37"), _dafny.Seq("\ud83c\udca1"), _dafny.Seq("｡")])
        if not((d_1_output_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(124,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not((d_2_output2_) == (d_3_expected_)):
            raise _dafny.HaltException("test/TestComputeSetToOrderedSequenceCharLess.dfy(125,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

