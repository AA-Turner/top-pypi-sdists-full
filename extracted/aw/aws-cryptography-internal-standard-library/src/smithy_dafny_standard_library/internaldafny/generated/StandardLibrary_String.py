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
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_Sequence as StandardLibrary_Sequence

# Module: StandardLibrary_String

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Int2Digits(n, base):
        d_0___accumulator_ = _dafny.Seq([])
        while True:
            with _dafny.label():
                if (n) == (0):
                    return (_dafny.Seq([])) + (d_0___accumulator_)
                elif True:
                    d_0___accumulator_ = (_dafny.Seq([_dafny.euclidian_modulus(n, base)])) + (d_0___accumulator_)
                    in0_ = _dafny.euclidian_division(n, base)
                    in1_ = base
                    n = in0_
                    base = in1_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def Digits2String(digits, chars):
        d_0___accumulator_ = _dafny.Seq([])
        while True:
            with _dafny.label():
                if (digits) == (_dafny.Seq([])):
                    return (d_0___accumulator_) + (_dafny.Seq(""))
                elif True:
                    d_0___accumulator_ = (d_0___accumulator_) + (_dafny.Seq([(chars)[(digits)[0]]]))
                    in0_ = _dafny.Seq((digits)[1::])
                    in1_ = chars
                    digits = in0_
                    chars = in1_
                    raise _dafny.TailCall()
                break

    @staticmethod
    def Int2String(n, chars):
        d_0_base_ = len(chars)
        if (n) == (0):
            return _dafny.Seq("0")
        elif (n) > (0):
            return default__.Digits2String(default__.Int2Digits(n, d_0_base_), chars)
        elif True:
            return (_dafny.Seq("-")) + (default__.Digits2String(default__.Int2Digits((0) - (n), d_0_base_), chars))

    @staticmethod
    def Base10Int2String(n):
        return default__.Int2String(n, default__.Base10)

    @staticmethod
    def SearchAndReplace(source, old__str, new__str):
        o: _dafny.Seq = _dafny.Seq({})
        d_0_old__pos_: Wrappers.Option
        out0_: Wrappers.Option
        out0_ = default__.HasSubString(source, old__str)
        d_0_old__pos_ = out0_
        if (d_0_old__pos_).is_None:
            o = source
            return o
        elif True:
            d_1_pos_: int
            d_1_pos_ = (d_0_old__pos_).value
            d_2_source__len_: int
            d_2_source__len_ = len(source)
            d_3_old__str__len_: int
            d_3_old__str__len_ = len(old__str)
            o = ((_dafny.Seq((source)[:d_1_pos_:])) + (new__str)) + (_dafny.Seq((source)[(d_1_pos_) + (d_3_old__str__len_)::]))
            return o
        return o

    @staticmethod
    def SearchAndReplacePos(source, old__str, new__str, pos):
        o: tuple = (_dafny.Seq({}), Wrappers.Option.default()())
        d_0_old__pos_: Wrappers.Option
        out0_: Wrappers.Option
        out0_ = default__.HasSubStringPos(source, old__str, pos)
        d_0_old__pos_ = out0_
        if (d_0_old__pos_).is_None:
            o = (source, Wrappers.Option_None())
            return o
        elif True:
            d_1_source__len_: int
            d_1_source__len_ = len(source)
            d_2_old__str__len_: int
            d_2_old__str__len_ = len(old__str)
            d_3_new__str__len_: int
            d_3_new__str__len_ = len(new__str)
            o = (((_dafny.Seq((source)[:(d_0_old__pos_).value:])) + (new__str)) + (_dafny.Seq((source)[((d_0_old__pos_).value) + (d_2_old__str__len_)::])), Wrappers.Option_Some(StandardLibrary_MemoryMath.default__.Add((d_0_old__pos_).value, d_3_new__str__len_)))
            o = o
            return o
        return o

    @staticmethod
    def SearchAndReplaceAll(source__in, old__str, new__str):
        o: _dafny.Seq = _dafny.Seq({})
        d_0_pos_: int
        d_0_pos_ = 0
        d_1_source_: _dafny.Seq
        d_1_source_ = source__in
        while True:
            d_2_res_: tuple
            out0_: tuple
            out0_ = default__.SearchAndReplacePos(d_1_source_, old__str, new__str, d_0_pos_)
            d_2_res_ = out0_
            if ((d_2_res_)[1]).is_None:
                d_0_pos_ = len(d_1_source_)
                o = (d_2_res_)[0]
                return o
            d_1_source_ = (d_2_res_)[0]
            d_0_pos_ = ((d_2_res_)[1]).value
        return o

    @staticmethod
    def HasSubString(haystack, needle):
        o: Wrappers.Option = Wrappers.Option.default()()
        if (len(haystack)) < (len(needle)):
            o = Wrappers.Option_None()
            return o
        d_0_size_: int
        d_0_size_ = len(needle)
        d_1_limit_: int
        d_1_limit_ = StandardLibrary_MemoryMath.default__.Add((len(haystack)) - (d_0_size_), 1)
        hi0_ = d_1_limit_
        for d_2_index_ in range(0, hi0_):
            if StandardLibrary_Sequence.default__.SequenceEqual(haystack, needle, d_2_index_, 0, d_0_size_):
                o = Wrappers.Option_Some(d_2_index_)
                return o
        o = Wrappers.Option_None()
        return o
        return o

    @staticmethod
    def HasSubStringPos(haystack, needle, pos):
        o: Wrappers.Option = Wrappers.Option.default()()
        if ((len(haystack)) - (pos)) < (len(needle)):
            o = Wrappers.Option_None()
            return o
        d_0_size_: int
        d_0_size_ = len(needle)
        d_1_limit_: int
        d_1_limit_ = StandardLibrary_MemoryMath.default__.Add((len(haystack)) - (d_0_size_), 1)
        hi0_ = d_1_limit_
        for d_2_index_ in range(pos, hi0_):
            if StandardLibrary_Sequence.default__.SequenceEqual(haystack, needle, d_2_index_, 0, d_0_size_):
                o = Wrappers.Option_Some(d_2_index_)
                return o
        o = Wrappers.Option_None()
        return o
        return o

    @_dafny.classproperty
    def Base10(instance):
        return _dafny.Seq(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
