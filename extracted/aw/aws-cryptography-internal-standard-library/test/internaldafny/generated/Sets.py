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

# Module: Sets

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def ExtractFromSingleton(s):
        def iife0_(_let_dummy_0):
            d_0_x_: TypeVar('T__') = None
            with _dafny.label("_ASSIGN_SUCH_THAT_d_0"):
                assign_such_that_0_: TypeVar('T__')
                for assign_such_that_0_ in (s).Elements:
                    d_0_x_ = assign_such_that_0_
                    if (d_0_x_) in (s):
                        raise _dafny.Break("_ASSIGN_SUCH_THAT_d_0")
                raise Exception("assign-such-that search produced no value")
                pass
            return d_0_x_
        return iife0_(0)
        

    @staticmethod
    def Map(xs, f):
        def iife0_():
            coll0_ = _dafny.Set()
            compr_0_: TypeVar('X__')
            for compr_0_ in (xs).Elements:
                d_1_x_: TypeVar('X__') = compr_0_
                if (d_1_x_) in (xs):
                    coll0_ = coll0_.union(_dafny.Set([f(d_1_x_)]))
            return _dafny.Set(coll0_)
        d_0_ys_ = iife0_()

        return d_0_ys_

    @staticmethod
    def Filter(xs, f):
        def iife0_():
            coll0_ = _dafny.Set()
            compr_0_: TypeVar('X__')
            for compr_0_ in (xs).Elements:
                d_1_x_: TypeVar('X__') = compr_0_
                if ((d_1_x_) in (xs)) and (f(d_1_x_)):
                    coll0_ = coll0_.union(_dafny.Set([d_1_x_]))
            return _dafny.Set(coll0_)
        d_0_ys_ = iife0_()

        return d_0_ys_

    @staticmethod
    def SetRange(a, b):
        d_0___accumulator_ = _dafny.Set({})
        while True:
            with _dafny.label():
                if (a) == (b):
                    return (_dafny.Set({})) | (d_0___accumulator_)
                elif True:
                    d_0___accumulator_ = (d_0___accumulator_) | (_dafny.Set({a}))
                    in0_ = (a) + (1)
                    in1_ = b
                    a = in0_
                    b = in1_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def SetRangeZeroBound(n):
        return default__.SetRange(0, n)

