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

# Module: Base64

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def IsBase64Char(c):
        return (((((c) == ('+')) or ((c) == ('/'))) or ((('0') <= (c)) and ((c) <= ('9')))) or ((('A') <= (c)) and ((c) <= ('Z')))) or ((('a') <= (c)) and ((c) <= ('z')))

    @staticmethod
    def IsUnpaddedBase64String(s):
        hresult_: bool = False
        d_0_size_: int
        d_0_size_ = len(s)
        if (_dafny.euclidian_modulus(d_0_size_, 4)) != (0):
            hresult_ = False
            return hresult_
        hi0_ = d_0_size_
        for d_1_i_ in range(0, hi0_):
            if not(default__.IsBase64Char((s)[d_1_i_])):
                hresult_ = False
                return hresult_
        hresult_ = True
        return hresult_
        return hresult_

    @staticmethod
    def IndexToChar(i):
        if (i) == (63):
            return '/'
        elif (i) == (62):
            return '+'
        elif ((52) <= (i)) and ((i) <= (61)):
            return chr((i) - (4))
        elif ((26) <= (i)) and ((i) <= (51)):
            return chr((i) + (71))
        elif True:
            return chr((i) + (65))

    @staticmethod
    def CharToIndex(c):
        if (c) == ('/'):
            return 63
        elif (c) == ('+'):
            return 62
        elif (('0') <= (c)) and ((c) <= ('9')):
            return (ord(c)) + (4)
        elif (('a') <= (c)) and ((c) <= ('z')):
            return (ord(c)) - (71)
        elif True:
            return (ord(c)) - (65)

    @staticmethod
    def UInt24ToSeq(x):
        d_0_b0_ = _dafny.euclidian_division(x, 65536)
        d_1_x0_ = (x) - ((d_0_b0_) * (65536))
        d_2_b1_ = _dafny.euclidian_division(d_1_x0_, 256)
        d_3_b2_ = _dafny.euclidian_modulus(d_1_x0_, 256)
        return _dafny.Seq([d_0_b0_, d_2_b1_, d_3_b2_])

    @staticmethod
    def SeqToUInt24(s):
        return ((((s)[0]) * (65536)) + (((s)[1]) * (256))) + ((s)[2])

    @staticmethod
    def SeqPosToUInt24(s, pos):
        return ((((s)[pos]) * (65536)) + (((s)[(pos) + (1)]) * (256))) + ((s)[(pos) + (2)])

    @staticmethod
    def UInt24ToIndexSeq(x):
        d_0_b0_ = _dafny.euclidian_division(x, 262144)
        d_1_x0_ = (x) - ((d_0_b0_) * (262144))
        d_2_b1_ = _dafny.euclidian_division(d_1_x0_, 4096)
        d_3_x1_ = (d_1_x0_) - ((d_2_b1_) * (4096))
        d_4_b2_ = _dafny.euclidian_division(d_3_x1_, 64)
        d_5_b3_ = _dafny.euclidian_modulus(d_3_x1_, 64)
        return _dafny.Seq([d_0_b0_, d_2_b1_, d_4_b2_, d_5_b3_])

    @staticmethod
    def IndexSeqToUInt24(s):
        return (((((s)[0]) * (262144)) + (((s)[1]) * (4096))) + (((s)[2]) * (64))) + ((s)[3])

    @staticmethod
    def IndexSeqPosToUInt24(s, pos):
        return (((((s)[pos]) * (262144)) + (((s)[(pos) + (1)]) * (4096))) + (((s)[(pos) + (2)]) * (64))) + ((s)[(pos) + (3)])

    @staticmethod
    def DecodeBlock(s):
        return default__.UInt24ToSeq(default__.IndexSeqToUInt24(s))

    @staticmethod
    def DecodeBlockPos(s, pos):
        return default__.UInt24ToSeq(default__.IndexSeqPosToUInt24(s, pos))

    @staticmethod
    def EncodeBlock(s):
        return default__.UInt24ToIndexSeq(default__.SeqToUInt24(s))

    @staticmethod
    def EncodeBlockPos(s, pos):
        return default__.UInt24ToIndexSeq(default__.SeqPosToUInt24(s, pos))

    @staticmethod
    def DecodeRecursively(s):
        b: _dafny.Seq = _dafny.Seq({})
        d_0_i_: int
        d_0_i_ = len(s)
        d_1_result_: _dafny.Seq
        d_1_result_ = _dafny.Seq([])
        while (d_0_i_) > (0):
            d_1_result_ = (default__.DecodeBlockPos(s, (d_0_i_) - (4))) + (d_1_result_)
            d_0_i_ = (d_0_i_) - (4)
        b = d_1_result_
        return b
        return b

    @staticmethod
    def EncodeRecursively(b):
        s: _dafny.Seq = _dafny.Seq({})
        d_0_i_: int
        d_0_i_ = len(b)
        d_1_result_: _dafny.Seq
        d_1_result_ = _dafny.Seq([])
        while (d_0_i_) > (0):
            d_1_result_ = (default__.EncodeBlockPos(b, (d_0_i_) - (3))) + (d_1_result_)
            d_0_i_ = (d_0_i_) - (3)
        s = d_1_result_
        return s
        return s

    @staticmethod
    def FromCharsToIndices(s):
        b: _dafny.Seq = _dafny.Seq({})
        d_0_result_: _dafny.Seq
        d_0_result_ = _dafny.Seq([])
        hi0_ = len(s)
        for d_1_i_ in range(0, hi0_):
            d_0_result_ = (d_0_result_) + (_dafny.Seq([default__.CharToIndex((s)[d_1_i_])]))
        b = d_0_result_
        return b
        return b

    @staticmethod
    def FromIndicesToChars(b):
        s: _dafny.Seq = _dafny.Seq("")
        d_0_result_: _dafny.Seq
        d_0_result_ = _dafny.Seq([])
        hi0_ = len(b)
        for d_1_i_ in range(0, hi0_):
            d_0_result_ = (d_0_result_) + (_dafny.Seq([default__.IndexToChar((b)[d_1_i_])]))
        s = d_0_result_
        return s
        return s

    @staticmethod
    def DecodeUnpadded(s):
        return default__.DecodeRecursively(default__.FromCharsToIndices(s))

    @staticmethod
    def EncodeUnpadded(b):
        return default__.FromIndicesToChars(default__.EncodeRecursively(b))

    @staticmethod
    def Is1Padding(s):
        return ((((((len(s)) == (4)) and (default__.IsBase64Char((s)[0]))) and (default__.IsBase64Char((s)[1]))) and (default__.IsBase64Char((s)[2]))) and ((_dafny.euclidian_modulus(default__.CharToIndex((s)[2]), 4)) == (0))) and (((s)[3]) == ('='))

    @staticmethod
    def Decode1Padding(s):
        d_0_d_ = default__.DecodeBlock(_dafny.Seq([default__.CharToIndex((s)[0]), default__.CharToIndex((s)[1]), default__.CharToIndex((s)[2]), 0]))
        return _dafny.Seq([(d_0_d_)[0], (d_0_d_)[1]])

    @staticmethod
    def Encode1Padding(b):
        d_0_e_ = default__.EncodeBlock(_dafny.Seq([(b)[0], (b)[1], 0]))
        return _dafny.Seq([default__.IndexToChar((d_0_e_)[0]), default__.IndexToChar((d_0_e_)[1]), default__.IndexToChar((d_0_e_)[2]), '='])

    @staticmethod
    def Is2Padding(s):
        return ((((((len(s)) == (4)) and (default__.IsBase64Char((s)[0]))) and (default__.IsBase64Char((s)[1]))) and ((_dafny.euclidian_modulus(default__.CharToIndex((s)[1]), 16)) == (0))) and (((s)[2]) == ('='))) and (((s)[3]) == ('='))

    @staticmethod
    def Decode2Padding(s):
        d_0_d_ = default__.DecodeBlock(_dafny.Seq([default__.CharToIndex((s)[0]), default__.CharToIndex((s)[1]), 0, 0]))
        return _dafny.Seq([(d_0_d_)[0]])

    @staticmethod
    def Encode2Padding(b):
        d_0_e_ = default__.EncodeBlock(_dafny.Seq([(b)[0], 0, 0]))
        return _dafny.Seq([default__.IndexToChar((d_0_e_)[0]), default__.IndexToChar((d_0_e_)[1]), '=', '='])

    @staticmethod
    def IsBase64String(s):
        d_0_size_ = len(s)
        return ((_dafny.euclidian_modulus(d_0_size_, 4)) == (0)) and ((default__.IsUnpaddedBase64String(s)) or ((default__.IsUnpaddedBase64String(_dafny.Seq((s)[:(d_0_size_) - (4):]))) and ((default__.Is1Padding(_dafny.Seq((s)[(d_0_size_) - (4)::]))) or (default__.Is2Padding(_dafny.Seq((s)[(d_0_size_) - (4)::]))))))

    @staticmethod
    def DecodeValid(s):
        d_0_size_ = len(s)
        if (d_0_size_) == (0):
            return _dafny.Seq([])
        elif True:
            d_1_finalBlockStart_ = (d_0_size_) - (4)
            d_2_prefix_ = _dafny.Seq((s)[:d_1_finalBlockStart_:])
            d_3_suffix_ = _dafny.Seq((s)[d_1_finalBlockStart_::])
            if default__.Is1Padding(d_3_suffix_):
                return (default__.DecodeUnpadded(d_2_prefix_)) + (default__.Decode1Padding(d_3_suffix_))
            elif default__.Is2Padding(d_3_suffix_):
                return (default__.DecodeUnpadded(d_2_prefix_)) + (default__.Decode2Padding(d_3_suffix_))
            elif True:
                return default__.DecodeUnpadded(s)

    @staticmethod
    def Decode(s):
        if default__.IsBase64String(s):
            return Wrappers.Result_Success(default__.DecodeValid(s))
        elif True:
            return Wrappers.Result_Failure(_dafny.Seq("The encoding is malformed"))

    @staticmethod
    def Encode(b):
        d_0_size_ = len(b)
        d_1_mod_ = _dafny.euclidian_modulus(d_0_size_, 3)
        if (d_1_mod_) == (0):
            d_2_s_ = default__.EncodeUnpadded(b)
            return d_2_s_
        elif (d_1_mod_) == (1):
            d_3_s1_ = default__.EncodeUnpadded(_dafny.Seq((b)[:(d_0_size_) - (1):]))
            d_4_s2_ = default__.Encode2Padding(_dafny.Seq((b)[(d_0_size_) - (1)::]))
            d_5_s_ = (d_3_s1_) + (d_4_s2_)
            return d_5_s_
        elif True:
            d_6_s1_ = default__.EncodeUnpadded(_dafny.Seq((b)[:(d_0_size_) - (2):]))
            d_7_s2_ = default__.Encode1Padding(_dafny.Seq((b)[(d_0_size_) - (2)::]))
            d_8_s_ = (d_6_s1_) + (d_7_s2_)
            return d_8_s_


class index:
    def  __init__(self):
        pass

    @staticmethod
    def default():
        return int(0)
    def _Is(source__):
        d_0_x_: int = source__
        return ((0) <= (d_0_x_)) and ((d_0_x_) < (64))

class uint24:
    def  __init__(self):
        pass

    @staticmethod
    def default():
        return int(0)
    def _Is(source__):
        d_1_x_: int = source__
        return ((0) <= (d_1_x_)) and ((d_1_x_) < (16777216))
