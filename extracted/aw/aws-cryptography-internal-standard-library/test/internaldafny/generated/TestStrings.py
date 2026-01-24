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

# Module: TestStrings

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def TestHasSubStringPos():
        d_0_actual_: Wrappers.Option
        out0_: Wrappers.Option
        out0_ = StandardLibrary_String.default__.HasSubStringPos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), 0)
        d_0_actual_ = out0_
        if not((d_0_actual_) == (Wrappers.Option_Some(0))):
            raise _dafny.HaltException("test/TestString.dfy(19,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out1_: Wrappers.Option
        out1_ = StandardLibrary_String.default__.HasSubStringPos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), 1)
        d_0_actual_ = out1_
        if not((d_0_actual_) == (Wrappers.Option_None())):
            raise _dafny.HaltException("test/TestString.dfy(21,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out2_: Wrappers.Option
        out2_ = StandardLibrary_String.default__.HasSubStringPos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), 0)
        d_0_actual_ = out2_
        if not((d_0_actual_) == (Wrappers.Option_Some(10))):
            raise _dafny.HaltException("test/TestString.dfy(24,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out3_: Wrappers.Option
        out3_ = StandardLibrary_String.default__.HasSubStringPos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), 10)
        d_0_actual_ = out3_
        if not((d_0_actual_) == (Wrappers.Option_Some(10))):
            raise _dafny.HaltException("test/TestString.dfy(26,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out4_: Wrappers.Option
        out4_ = StandardLibrary_String.default__.HasSubStringPos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), 11)
        d_0_actual_ = out4_
        if not((d_0_actual_) == (Wrappers.Option_None())):
            raise _dafny.HaltException("test/TestString.dfy(28,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSearchAndReplace():
        d_0_actual_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = StandardLibrary_String.default__.SearchAndReplace(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Robbie"))
        d_0_actual_ = out0_
        if not((d_0_actual_) == (_dafny.Seq("Robbie is a Dog."))):
            raise _dafny.HaltException("test/TestString.dfy(34,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out1_: _dafny.Seq
        out1_ = StandardLibrary_String.default__.SearchAndReplace(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), _dafny.Seq("good boy"))
        d_0_actual_ = out1_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a good boy."))):
            raise _dafny.HaltException("test/TestString.dfy(36,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out2_: _dafny.Seq
        out2_ = StandardLibrary_String.default__.SearchAndReplace(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog."), _dafny.Seq("good boy!"))
        d_0_actual_ = out2_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a good boy!"))):
            raise _dafny.HaltException("test/TestString.dfy(38,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out3_: _dafny.Seq
        out3_ = StandardLibrary_String.default__.SearchAndReplace(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Robbie"), _dafny.Seq("good boy!"))
        d_0_actual_ = out3_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a Dog."))):
            raise _dafny.HaltException("test/TestString.dfy(40,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out4_: _dafny.Seq
        out4_ = StandardLibrary_String.default__.SearchAndReplace(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Koda"))
        d_0_actual_ = out4_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a Dog."))):
            raise _dafny.HaltException("test/TestString.dfy(42,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestSearchAndReplaceAll():
        d_0_actual_: _dafny.Seq
        out0_: _dafny.Seq
        out0_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Robbie"))
        d_0_actual_ = out0_
        if not((d_0_actual_) == (_dafny.Seq("Robbie is a Dog."))):
            raise _dafny.HaltException("test/TestString.dfy(48,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out1_: _dafny.Seq
        out1_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), _dafny.Seq("good boy"))
        d_0_actual_ = out1_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a good boy."))):
            raise _dafny.HaltException("test/TestString.dfy(50,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out2_: _dafny.Seq
        out2_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog."), _dafny.Seq("good boy!"))
        d_0_actual_ = out2_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a good boy!"))):
            raise _dafny.HaltException("test/TestString.dfy(52,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out3_: _dafny.Seq
        out3_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Robbie"), _dafny.Seq("good boy!"))
        d_0_actual_ = out3_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a Dog."))):
            raise _dafny.HaltException("test/TestString.dfy(54,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out4_: _dafny.Seq
        out4_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Koda"))
        d_0_actual_ = out4_
        if not((d_0_actual_) == (_dafny.Seq("Koda is a Dog."))):
            raise _dafny.HaltException("test/TestString.dfy(56,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out5_: _dafny.Seq
        out5_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("A rose is a rose is a rose."), _dafny.Seq("rose"), _dafny.Seq("daisy"))
        d_0_actual_ = out5_
        if not((d_0_actual_) == (_dafny.Seq("A daisy is a daisy is a daisy."))):
            raise _dafny.HaltException("test/TestString.dfy(59,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out6_: _dafny.Seq
        out6_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("rose is a rose is a rose"), _dafny.Seq("rose"), _dafny.Seq("daisy"))
        d_0_actual_ = out6_
        if not((d_0_actual_) == (_dafny.Seq("daisy is a daisy is a daisy"))):
            raise _dafny.HaltException("test/TestString.dfy(61,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out7_: _dafny.Seq
        out7_ = StandardLibrary_String.default__.SearchAndReplaceAll(_dafny.Seq("rose is a rose is a rose"), _dafny.Seq("rose"), _dafny.Seq("rose_daisy"))
        d_0_actual_ = out7_
        if not((d_0_actual_) == (_dafny.Seq("rose_daisy is a rose_daisy is a rose_daisy"))):
            raise _dafny.HaltException("test/TestString.dfy(63,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestHasSearchAndReplacePos():
        d_0_actual_: tuple
        out0_: tuple
        out0_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Robbie"), 0)
        d_0_actual_ = out0_
        if not((d_0_actual_) == ((_dafny.Seq("Robbie is a Dog."), Wrappers.Option_Some(6)))):
            raise _dafny.HaltException("test/TestString.dfy(69,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out1_: tuple
        out1_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Robbie"), 1)
        d_0_actual_ = out1_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a Dog."), Wrappers.Option_None()))):
            raise _dafny.HaltException("test/TestString.dfy(71,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out2_: tuple
        out2_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), _dafny.Seq("good boy"), 0)
        d_0_actual_ = out2_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a good boy."), Wrappers.Option_Some(18)))):
            raise _dafny.HaltException("test/TestString.dfy(74,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out3_: tuple
        out3_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), _dafny.Seq("good boy"), 10)
        d_0_actual_ = out3_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a good boy."), Wrappers.Option_Some(18)))):
            raise _dafny.HaltException("test/TestString.dfy(76,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out4_: tuple
        out4_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog"), _dafny.Seq("good boy"), 11)
        d_0_actual_ = out4_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a Dog."), Wrappers.Option_None()))):
            raise _dafny.HaltException("test/TestString.dfy(78,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out5_: tuple
        out5_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog."), _dafny.Seq("good boy!"), 0)
        d_0_actual_ = out5_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a good boy!"), Wrappers.Option_Some(19)))):
            raise _dafny.HaltException("test/TestString.dfy(81,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out6_: tuple
        out6_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog."), _dafny.Seq("good boy!"), 10)
        d_0_actual_ = out6_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a good boy!"), Wrappers.Option_Some(19)))):
            raise _dafny.HaltException("test/TestString.dfy(83,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out7_: tuple
        out7_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog."), _dafny.Seq("good boy!"), 11)
        d_0_actual_ = out7_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a Dog."), Wrappers.Option_None()))):
            raise _dafny.HaltException("test/TestString.dfy(85,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out8_: tuple
        out8_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Robbie"), _dafny.Seq("good boy!"), 0)
        d_0_actual_ = out8_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a Dog."), Wrappers.Option_None()))):
            raise _dafny.HaltException("test/TestString.dfy(89,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        out9_: tuple
        out9_ = StandardLibrary_String.default__.SearchAndReplacePos(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"), _dafny.Seq("Koda"), 0)
        d_0_actual_ = out9_
        if not((d_0_actual_) == ((_dafny.Seq("Koda is a Dog."), Wrappers.Option_Some(4)))):
            raise _dafny.HaltException("test/TestString.dfy(91,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestHasSubStringPositive():
        d_0_actual_: Wrappers.Option
        out0_: Wrappers.Option
        out0_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda"))
        d_0_actual_ = out0_
        if not((d_0_actual_) == (Wrappers.Option_Some(0))):
            raise _dafny.HaltException("test/TestString.dfy(97,4): " + _dafny.string_of(_dafny.Seq("'Koda' is in 'Koda is a Dog.' at index 0, but HasSubString does not think so")))
        out1_: Wrappers.Option
        out1_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Koda is a Dog."))
        d_0_actual_ = out1_
        if not((d_0_actual_) == (Wrappers.Option_Some(0))):
            raise _dafny.HaltException("test/TestString.dfy(99,4): " + _dafny.string_of(_dafny.Seq("'Koda is a Dog.' is in 'Koda is a Dog.' at index 0, but HasSubString does not think so")))
        out2_: Wrappers.Option
        out2_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("Koda is a Dog."), _dafny.Seq("Dog."))
        d_0_actual_ = out2_
        if not((d_0_actual_) == (Wrappers.Option_Some(10))):
            raise _dafny.HaltException("test/TestString.dfy(101,4): " + _dafny.string_of(_dafny.Seq("'Dog.' is in 'Koda is a Dog.' at index 10, but HasSubString does not think so")))
        out3_: Wrappers.Option
        out3_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("Koda is a Dog."), _dafny.Seq("."))
        d_0_actual_ = out3_
        if not((d_0_actual_) == (Wrappers.Option_Some(13))):
            raise _dafny.HaltException("test/TestString.dfy(103,4): " + _dafny.string_of(_dafny.Seq("'.' is in 'Koda is a Dog.' at index 13, but HasSubString does not think so")))
        out4_: Wrappers.Option
        out4_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("Koda is a Dog."), _dafny.Seq(""))
        d_0_actual_ = out4_
        if not((d_0_actual_) == (Wrappers.Option_Some(0))):
            raise _dafny.HaltException("test/TestString.dfy(105,4): " + _dafny.string_of(_dafny.Seq("The empty string is in 'Koda is a Dog.' at index 0, but HasSubString does not think so")))

    @staticmethod
    def TestHasSubStringNegative():
        d_0_actual_: Wrappers.Option
        out0_: Wrappers.Option
        out0_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("Robbie is a Dog."), _dafny.Seq("Koda"))
        d_0_actual_ = out0_
        if not((d_0_actual_) == (Wrappers.Option_None())):
            raise _dafny.HaltException("test/TestString.dfy(111,4): " + _dafny.string_of(_dafny.Seq("'Robbie is a Dog.' does not contain Koda")))
        out1_: Wrappers.Option
        out1_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("\t"), _dafny.Seq(" "))
        d_0_actual_ = out1_
        if not((d_0_actual_) == (Wrappers.Option_None())):
            raise _dafny.HaltException("test/TestString.dfy(113,4): " + _dafny.string_of(_dafny.Seq("A tab is not a space")))
        out2_: Wrappers.Option
        out2_ = StandardLibrary_String.default__.HasSubString(_dafny.Seq("large"), _dafny.Seq("larger"))
        d_0_actual_ = out2_
        if not((d_0_actual_) == (Wrappers.Option_None())):
            raise _dafny.HaltException("test/TestString.dfy(115,4): " + _dafny.string_of(_dafny.Seq("Needle larger than haystack")))

    @staticmethod
    def TestFileIO():
        d_0_valueOrError0_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out0_: Wrappers.Result
        out0_ = FileIO.default__.WriteBytesToFile(_dafny.Seq("MyFile"), _dafny.Seq([1, 2, 3, 4, 5]))
        d_0_valueOrError0_ = out0_
        if not(not((d_0_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/TestString.dfy(120,13): " + _dafny.string_of(d_0_valueOrError0_))
        d_1_x_: tuple
        d_1_x_ = (d_0_valueOrError0_).Extract()
        d_2_valueOrError1_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out1_: Wrappers.Result
        out1_ = FileIO.default__.AppendBytesToFile(_dafny.Seq("MyFile"), _dafny.Seq([6, 7, 8, 9, 10]))
        d_2_valueOrError1_ = out1_
        if not(not((d_2_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/TestString.dfy(121,9): " + _dafny.string_of(d_2_valueOrError1_))
        d_1_x_ = (d_2_valueOrError1_).Extract()
        d_3_valueOrError2_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out2_: Wrappers.Result
        out2_ = FileIO.default__.AppendBytesToFile(_dafny.Seq("MyFile"), _dafny.Seq([11, 12, 13, 14, 15]))
        d_3_valueOrError2_ = out2_
        if not(not((d_3_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/TestString.dfy(122,9): " + _dafny.string_of(d_3_valueOrError2_))
        d_1_x_ = (d_3_valueOrError2_).Extract()
        d_4_valueOrError3_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out3_: Wrappers.Result
        out3_ = FileIO.default__.ReadBytesFromFile(_dafny.Seq("MyFile"))
        d_4_valueOrError3_ = out3_
        if not(not((d_4_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/TestString.dfy(123,13): " + _dafny.string_of(d_4_valueOrError3_))
        d_5_y_: _dafny.Seq
        d_5_y_ = (d_4_valueOrError3_).Extract()
        if not((d_5_y_) == (_dafny.Seq([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))):
            raise _dafny.HaltException("test/TestString.dfy(124,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_valueOrError4_: Wrappers.Result = Wrappers.Result.default(_dafny.defaults.tuple())()
        out4_: Wrappers.Result
        out4_ = FileIO.default__.WriteBytesToFile(_dafny.Seq("MyFile"), _dafny.Seq([1, 2, 3, 4, 5]))
        d_6_valueOrError4_ = out4_
        if not(not((d_6_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("test/TestString.dfy(125,9): " + _dafny.string_of(d_6_valueOrError4_))
        d_1_x_ = (d_6_valueOrError4_).Extract()
        d_7_valueOrError5_: Wrappers.Result = Wrappers.Result.default(_dafny.Seq)()
        out5_: Wrappers.Result
        out5_ = FileIO.default__.ReadBytesFromFile(_dafny.Seq("MyFile"))
        d_7_valueOrError5_ = out5_
        if not(not((d_7_valueOrError5_).IsFailure())):
            raise _dafny.HaltException("test/TestString.dfy(126,9): " + _dafny.string_of(d_7_valueOrError5_))
        d_5_y_ = (d_7_valueOrError5_).Extract()
        if not((d_5_y_) == (_dafny.Seq([1, 2, 3, 4, 5]))):
            raise _dafny.HaltException("test/TestString.dfy(127,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def BadFilename():
        if ((OsLang.default__.GetOsShort()) == (_dafny.Seq("Windows"))) and ((OsLang.default__.GetLanguageShort()) == (_dafny.Seq("Dotnet"))):
            return _dafny.Seq("foo:bar:baz")
        elif True:
            return _dafny.Seq("/../../MyFile")

