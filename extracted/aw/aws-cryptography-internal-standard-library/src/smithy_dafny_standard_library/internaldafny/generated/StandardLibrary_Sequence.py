import sys
from typing import Callable, Any, TypeVar, NamedTuple
from math import floor
from itertools import count

import smithy_dafny_standard_library.internaldafny.generated.module_ as module_
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

# Module: StandardLibrary_Sequence

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def MapWithResult(f, xs, pos, acc):
        while True:
            with _dafny.label():
                if (len(xs)) == (pos):
                    return Wrappers.Result_Success(acc)
                elif True:
                    d_0_valueOrError0_ = f((xs)[pos])
                    if (d_0_valueOrError0_).IsFailure():
                        return (d_0_valueOrError0_).PropagateFailure()
                    elif True:
                        d_1_head_ = (d_0_valueOrError0_).Extract()
                        in0_ = f
                        in1_ = xs
                        in2_ = (pos) + (1)
                        in3_ = (acc) + (_dafny.Seq([d_1_head_]))
                        f = in0_
                        xs = in1_
                        pos = in2_
                        acc = in3_
                        raise _dafny.TailCall()
                break

    @staticmethod
    def Flatten(xs, pos, acc):
        while True:
            with _dafny.label():
                if (len(xs)) == (pos):
                    return acc
                elif True:
                    in0_ = xs
                    in1_ = (pos) + (1)
                    in2_ = (acc) + ((xs)[pos])
                    xs = in0_
                    pos = in1_
                    acc = in2_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def SequenceEqualNat(seq1, seq2, start1, start2, size):
        return default__.SequenceEqual(seq1, seq2, start1, start2, size)

    @staticmethod
    def SequenceEqual(seq1, seq2, start1, start2, size):
        ret: bool = False
        d_0_j_: int
        d_0_j_ = start2
        hi0_ = (start1) + (size)
        for d_1_i_ in range(start1, hi0_):
            if ((seq1)[d_1_i_]) != ((seq2)[d_0_j_]):
                ret = False
                return ret
            d_0_j_ = (d_0_j_) + (1)
        ret = True
        return ret
        return ret

