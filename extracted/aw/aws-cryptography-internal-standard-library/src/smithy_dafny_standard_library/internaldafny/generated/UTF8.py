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
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary_String as StandardLibrary_String
import smithy_dafny_standard_library.internaldafny.generated.StandardLibrary as StandardLibrary
import smithy_dafny_standard_library.internaldafny.generated.UUID as UUID

# Module: UTF8

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def CreateEncodeSuccess(bytes):
        return Wrappers.Result_Success(bytes)

    @staticmethod
    def CreateEncodeFailure(error):
        return Wrappers.Result_Failure(error)

    @staticmethod
    def CreateDecodeSuccess(s):
        return Wrappers.Result_Success(s)

    @staticmethod
    def CreateDecodeFailure(error):
        return Wrappers.Result_Failure(error)

    @staticmethod
    def IsASCIIString(s):
        def lambda0_(forall_var_0_):
            d_0_i_: int = forall_var_0_
            return not (((0) <= (d_0_i_)) and ((d_0_i_) < (len(s)))) or ((ord((s)[d_0_i_])) < (128))

        return _dafny.quantifier(_dafny.IntegerRange(0, len(s)), True, lambda0_)

    @staticmethod
    def Uses1Byte(s):
        return ((0) <= ((s)[0])) and (((s)[0]) <= (127))

    @staticmethod
    def Uses2Bytes(s):
        return (((194) <= ((s)[0])) and (((s)[0]) <= (223))) and (((128) <= ((s)[1])) and (((s)[1]) <= (191)))

    @staticmethod
    def Uses3Bytes(s):
        return (((((((s)[0]) == (224)) and (((160) <= ((s)[1])) and (((s)[1]) <= (191)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191)))) or (((((225) <= ((s)[0])) and (((s)[0]) <= (236))) and (((128) <= ((s)[1])) and (((s)[1]) <= (191)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191))))) or (((((s)[0]) == (237)) and (((128) <= ((s)[1])) and (((s)[1]) <= (159)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191))))) or (((((238) <= ((s)[0])) and (((s)[0]) <= (239))) and (((128) <= ((s)[1])) and (((s)[1]) <= (191)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191))))

    @staticmethod
    def Uses4Bytes(s):
        return (((((((s)[0]) == (240)) and (((144) <= ((s)[1])) and (((s)[1]) <= (191)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191)))) and (((128) <= ((s)[3])) and (((s)[3]) <= (191)))) or ((((((241) <= ((s)[0])) and (((s)[0]) <= (243))) and (((128) <= ((s)[1])) and (((s)[1]) <= (191)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191)))) and (((128) <= ((s)[3])) and (((s)[3]) <= (191))))) or ((((((s)[0]) == (244)) and (((128) <= ((s)[1])) and (((s)[1]) <= (143)))) and (((128) <= ((s)[2])) and (((s)[2]) <= (191)))) and (((128) <= ((s)[3])) and (((s)[3]) <= (191))))

    @staticmethod
    def ValidUTF8Range(a, lo, hi):
        hresult_: bool = False
        if StandardLibrary_UInt.default__.HasUint64Len(a):
            hresult_ = default__.BoundedValidUTF8Range(a, lo, hi)
            return hresult_
        if (lo) == (hi):
            hresult_ = True
            return hresult_
        d_0_i_: int
        d_0_i_ = lo
        while (d_0_i_) < (hi):
            if ((d_0_i_) < (hi)) and (((0) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (127))):
                d_0_i_ = (d_0_i_) + (1)
            elif ((((d_0_i_) + (1)) < (hi)) and (((194) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (223)))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191))):
                d_0_i_ = (d_0_i_) + (2)
            elif (((d_0_i_) + (2)) < (hi)) and ((((((((a)[d_0_i_]) == (224)) and (((160) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) or (((((225) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (236))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191))))) or (((((a)[d_0_i_]) == (237)) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (159)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191))))) or (((((238) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (239))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191))))):
                d_0_i_ = (d_0_i_) + (3)
            elif (((d_0_i_) + (3)) < (hi)) and ((((((((a)[d_0_i_]) == (240)) and (((144) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (3)])) and (((a)[(d_0_i_) + (3)]) <= (191)))) or ((((((241) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (243))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (3)])) and (((a)[(d_0_i_) + (3)]) <= (191))))) or ((((((a)[d_0_i_]) == (244)) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (143)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (3)])) and (((a)[(d_0_i_) + (3)]) <= (191))))):
                d_0_i_ = (d_0_i_) + (4)
            elif True:
                hresult_ = False
                return hresult_
        hresult_ = True
        return hresult_
        return hresult_

    @staticmethod
    def BoundedValidUTF8Range(a, lo, hi):
        hresult_: bool = False
        if (lo) == (hi):
            hresult_ = True
            return hresult_
        d_0_i_: int
        d_0_i_ = lo
        while (d_0_i_) < (hi):
            if ((d_0_i_) < (hi)) and (((0) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (127))):
                d_0_i_ = (d_0_i_) + (1)
            elif (((d_0_i_) < ((hi) - (1))) and (((194) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (223)))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191))):
                d_0_i_ = (d_0_i_) + (2)
            elif (((2) <= (hi)) and ((d_0_i_) < ((hi) - (2)))) and ((((((((a)[d_0_i_]) == (224)) and (((160) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) or (((((225) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (236))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191))))) or (((((a)[d_0_i_]) == (237)) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (159)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191))))) or (((((238) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (239))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191))))):
                d_0_i_ = (d_0_i_) + (3)
            elif (((3) <= (hi)) and ((d_0_i_) < ((hi) - (3)))) and ((((((((a)[d_0_i_]) == (240)) and (((144) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (3)])) and (((a)[(d_0_i_) + (3)]) <= (191)))) or ((((((241) <= ((a)[d_0_i_])) and (((a)[d_0_i_]) <= (243))) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (3)])) and (((a)[(d_0_i_) + (3)]) <= (191))))) or ((((((a)[d_0_i_]) == (244)) and (((128) <= ((a)[(d_0_i_) + (1)])) and (((a)[(d_0_i_) + (1)]) <= (143)))) and (((128) <= ((a)[(d_0_i_) + (2)])) and (((a)[(d_0_i_) + (2)]) <= (191)))) and (((128) <= ((a)[(d_0_i_) + (3)])) and (((a)[(d_0_i_) + (3)]) <= (191))))):
                d_0_i_ = (d_0_i_) + (4)
            elif True:
                hresult_ = False
                return hresult_
        hresult_ = True
        return hresult_
        return hresult_

    @staticmethod
    def ValidUTF8Seq(s):
        return default__.ValidUTF8Range(s, 0, len(s))


class ValidUTF8Bytes:
    def  __init__(self):
        pass

    @staticmethod
    def default():
        return _dafny.Seq([])
    def _Is(source__):
        d_0_i_: _dafny.Seq = source__
        return default__.ValidUTF8Seq(d_0_i_)
