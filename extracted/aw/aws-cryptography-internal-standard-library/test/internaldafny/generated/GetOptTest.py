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
import TestComputeSetToOrderedSequenceCharLess as TestComputeSetToOrderedSequenceCharLess
import TestOsLang as TestOsLang
import MemoryMathTest as MemoryMathTest
import TestHexStrings as TestHexStrings

# Module: GetOptTest

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def TestEmpty():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(20,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(21,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(22,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestShort():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("-svsttt"), _dafny.Seq("-t"), _dafny.Seq("stuff"), _dafny.Seq("-v")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(34,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("six"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("seven"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("six"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("tt"))), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("stuff"))), GetOpt.OneArg_OneArg(_dafny.Seq("seven"), Wrappers.Option_None())]))):
            raise _dafny.HaltException("test/GetOpt.dfy(35,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(37,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestLong():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo"), _dafny.Seq("file1"), _dafny.Seq("--bar"), _dafny.Seq("bar1"), _dafny.Seq("-"), _dafny.Seq("--bar=bar2=bar3"), _dafny.Seq("file3"), _dafny.Seq("--"), _dafny.Seq("--this"), _dafny.Seq("-that")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(49,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("bar1"))), GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("bar2=bar3")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(50,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([_dafny.Seq("file1"), _dafny.Seq("-"), _dafny.Seq("file3"), _dafny.Seq("--this"), _dafny.Seq("-that")]))):
            raise _dafny.HaltException("test/GetOpt.dfy(51,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestRequired():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_Required(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo"), _dafny.Seq("file1"), _dafny.Seq("--bar"), _dafny.Seq("bar1"), _dafny.Seq("-"), _dafny.Seq("--bar=bar2=bar3"), _dafny.Seq("file3"), _dafny.Seq("--"), _dafny.Seq("--this"), _dafny.Seq("-that")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(63,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("bar1"))), GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("bar2=bar3")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(64,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([_dafny.Seq("file1"), _dafny.Seq("-"), _dafny.Seq("file3"), _dafny.Seq("--this"), _dafny.Seq("-that")]))):
            raise _dafny.HaltException("test/GetOpt.dfy(65,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_y_: Wrappers.Result
        d_3_y_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo"), _dafny.Seq("file1"), _dafny.Seq("file3"), _dafny.Seq("--"), _dafny.Seq("--this"), _dafny.Seq("-that")]))
        if not((d_3_y_).is_Failure):
            raise _dafny.HaltException("test/GetOpt.dfy(68,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_y_).error) == (_dafny.Seq("Option 'bar' is required, but was not used."))):
            raise _dafny.HaltException("test/GetOpt.dfy(69,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestDeprecated():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Deprecated(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Deprecated(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Deprecated(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo"), _dafny.Seq("--bar=baz"), _dafny.Seq("-svtstuff")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(81,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("seven"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("stuff")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(82,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(83,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestAlias():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq("abc"), _dafny.Seq([_dafny.Seq("def"), _dafny.Seq("ghi")])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Deprecated(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Deprecated(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("-abc"), _dafny.Seq("--def"), _dafny.Seq("--ghi")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(95,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None())]))):
            raise _dafny.HaltException("test/GetOpt.dfy(96,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(97,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestPositionalFail():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_Maybe()), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_Yes())]))
        d_1_x_: Wrappers.Result
        d_1_x_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("stuff"), _dafny.Seq("-123"), _dafny.Seq("--foo")]))
        if not((d_1_x_).is_Failure):
            raise _dafny.HaltException("test/GetOpt.dfy(108,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_1_x_).error) == (_dafny.Seq("Required positional argument 'bar' follows optional positional argument 'two'."))):
            raise _dafny.HaltException("test/GetOpt.dfy(109,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestPositional():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_Yes()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_Maybe())]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("stuff"), _dafny.Seq("-123"), _dafny.Seq("--foo")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(119,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("stuff"))), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("-123"))), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None())]))):
            raise _dafny.HaltException("test/GetOpt.dfy(120,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(121,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_valueOrError1_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_3_valueOrError1_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("stuff"), _dafny.Seq("--two=-123"), _dafny.Seq("--foo")]))
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(123,9): " + _dafny.string_of(d_3_valueOrError1_))
        d_2_x_ = (d_3_valueOrError1_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("stuff"))), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("-123"))), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None())]))):
            raise _dafny.HaltException("test/GetOpt.dfy(124,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(125,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_4_valueOrError2_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_4_valueOrError2_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("stuff"), _dafny.Seq("--two=-123"), _dafny.Seq("--foo"), _dafny.Seq("--bar"), _dafny.Seq("more-stuff")]))
        if not(not((d_4_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(127,9): " + _dafny.string_of(d_4_valueOrError2_))
        d_2_x_ = (d_4_valueOrError2_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("stuff"))), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("-123"))), GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("more-stuff")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(128,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(129,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_5_valueOrError3_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_5_valueOrError3_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("stuff")]))
        if not(not((d_5_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(131,9): " + _dafny.string_of(d_5_valueOrError3_))
        d_2_x_ = (d_5_valueOrError3_).Extract()
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("bar"), Wrappers.Option_Some(_dafny.Seq("stuff")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(132,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(133,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_y_: Wrappers.Result
        d_6_y_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--two=-123"), _dafny.Seq("--foo"), _dafny.Seq("--bar"), _dafny.Seq("more-stuff")]))
        if not((d_6_y_).is_Failure):
            raise _dafny.HaltException("test/GetOpt.dfy(136,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_6_y_).error) == (_dafny.Seq("Positional arg bar matched with invalid positional value '--two=-123'."))):
            raise _dafny.HaltException("test/GetOpt.dfy(137,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_6_y_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd")]))
        if not((d_6_y_).is_Failure):
            raise _dafny.HaltException("test/GetOpt.dfy(140,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_6_y_).error) == (_dafny.Seq("Positional arg 'bar' is required, but we've run out of arguments."))):
            raise _dafny.HaltException("test/GetOpt.dfy(141,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestHelp():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--help")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(153,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        d_3_valueOrError1_: Wrappers.Option = Wrappers.Option.default()()
        d_3_valueOrError1_ = GetOpt.default__.NeedsHelp(d_0_MyOptions_, d_2_x_, _dafny.Seq(""))
        if not(not((d_3_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(154,13): " + _dafny.string_of(d_3_valueOrError1_))
        d_4_y_: _dafny.Seq
        d_4_y_ = (d_3_valueOrError1_).Extract()

    @staticmethod
    def TestHelpFail():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("helpText"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("bar"), _dafny.Seq("helpText"), _dafny.Seq("arg"), GetOpt.default__.NullChar, GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("helpText"), _dafny.Seq("arg"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("helpText"), 's', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Flag(_dafny.Seq("seven"), _dafny.Seq("helpText"), 'v', False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))
        d_1_x_: Wrappers.Result
        d_1_x_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--help"), _dafny.Seq("--foo")]))
        if not((d_1_x_).is_Failure):
            raise _dafny.HaltException("test/GetOpt.dfy(167,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_1_x_).error) == (_dafny.Seq("Option 'help' used with other stuff, but must only be used alone."))):
            raise _dafny.HaltException("test/GetOpt.dfy(168,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestNested():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("Does foo things"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("Does bar things to thingy"), _dafny.Seq("thingy"), 't', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Command(GetOpt.Options_Options(_dafny.Seq("command"), _dafny.Seq("Does command stuff"), _dafny.Seq([GetOpt.Param_Opt(_dafny.Seq("five"), _dafny.Seq("Does five things to thingy"), _dafny.Seq("thingy"), 'h', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("Does six things"), GetOpt.default__.NullChar, False, True, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))), GetOpt.Param_Command(GetOpt.Options_Options(_dafny.Seq("other"), _dafny.Seq("Does other stuff"), _dafny.Seq([GetOpt.Param_Opt(_dafny.Seq("seven"), _dafny.Seq("Does seven things to thingy"), _dafny.Seq("thingy"), 'h', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("eight"), _dafny.Seq("Does eight things"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))])))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("MyProg"), _dafny.Seq("--foo"), _dafny.Seq("other"), _dafny.Seq("--seven=siete"), _dafny.Seq("--eight")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(185,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).command) == (_dafny.Seq("MyProg"))):
            raise _dafny.HaltException("test/GetOpt.dfy(186,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None())]))):
            raise _dafny.HaltException("test/GetOpt.dfy(187,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(188,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).subcommand).is_Some):
            raise _dafny.HaltException("test/GetOpt.dfy(189,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_sub_: GetOpt.Parsed
        d_3_sub_ = ((d_2_x_).subcommand).value
        if not(((d_3_sub_).command) == (_dafny.Seq("other"))):
            raise _dafny.HaltException("test/GetOpt.dfy(191,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("seven"), Wrappers.Option_Some(_dafny.Seq("siete"))), GetOpt.OneArg_OneArg(_dafny.Seq("eight"), Wrappers.Option_None())]))):
            raise _dafny.HaltException("test/GetOpt.dfy(192,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(193,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).subcommand).is_None):
            raise _dafny.HaltException("test/GetOpt.dfy(194,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_4_valueOrError1_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_4_valueOrError1_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("MyProg"), _dafny.Seq("--help")]))
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(196,9): " + _dafny.string_of(d_4_valueOrError1_))
        d_2_x_ = (d_4_valueOrError1_).Extract()
        d_5_valueOrError2_: Wrappers.Option = Wrappers.Option.default()()
        d_5_valueOrError2_ = GetOpt.default__.NeedsHelp(d_0_MyOptions_, d_2_x_, _dafny.Seq(""))
        if not(not((d_5_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(197,13): " + _dafny.string_of(d_5_valueOrError2_))
        d_6_y_: _dafny.Seq
        d_6_y_ = (d_5_valueOrError2_).Extract()
        d_7_valueOrError3_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_7_valueOrError3_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("MyProg"), _dafny.Seq("command"), _dafny.Seq("--help")]))
        if not(not((d_7_valueOrError3_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(199,9): " + _dafny.string_of(d_7_valueOrError3_))
        d_2_x_ = (d_7_valueOrError3_).Extract()
        d_8_valueOrError4_: Wrappers.Option = Wrappers.Option.default()()
        d_8_valueOrError4_ = GetOpt.default__.NeedsHelp(d_0_MyOptions_, d_2_x_, _dafny.Seq(""))
        if not(not((d_8_valueOrError4_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(200,9): " + _dafny.string_of(d_8_valueOrError4_))
        d_6_y_ = (d_8_valueOrError4_).Extract()

    @staticmethod
    def TestDefault():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("MyProg"), _dafny.Seq("does stuff"), _dafny.Seq([GetOpt.Param_Flag(_dafny.Seq("foo"), _dafny.Seq("Does foo things"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([])), GetOpt.Param_Opt(_dafny.Seq("two"), _dafny.Seq("Does bar things to thingy"), _dafny.Seq("thingy"), 't', GetOpt.Unused_Default(_dafny.Seq("two_dflt")), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Command(GetOpt.Options_Options(_dafny.Seq("command"), _dafny.Seq("Does command stuff"), _dafny.Seq([GetOpt.Param_Opt(_dafny.Seq("five"), _dafny.Seq("Does five things to thingy"), _dafny.Seq("thingy"), 'h', GetOpt.Unused_Default(_dafny.Seq("five_dflt")), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("six"), _dafny.Seq("Does six things"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))]))), GetOpt.Param_Command(GetOpt.Options_Options(_dafny.Seq("other"), _dafny.Seq("Does other stuff"), _dafny.Seq([GetOpt.Param_Opt(_dafny.Seq("seven"), _dafny.Seq("Does seven things to thingy"), _dafny.Seq("thingy"), 'h', GetOpt.Unused_Default(_dafny.Seq("seven_dflt")), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No()), GetOpt.Param_Flag(_dafny.Seq("eight"), _dafny.Seq("Does eight things"), GetOpt.default__.NullChar, False, False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]))])))]))
        d_1_valueOrError0_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_1_valueOrError0_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo"), _dafny.Seq("other"), _dafny.Seq("--eight")]))
        if not(not((d_1_valueOrError0_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(224,13): " + _dafny.string_of(d_1_valueOrError0_))
        d_2_x_: GetOpt.Parsed
        d_2_x_ = (d_1_valueOrError0_).Extract()
        if not(((d_2_x_).command) == (_dafny.Seq("cmd"))):
            raise _dafny.HaltException("test/GetOpt.dfy(225,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("two_dflt")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(226,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(227,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).subcommand).is_Some):
            raise _dafny.HaltException("test/GetOpt.dfy(228,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_sub_: GetOpt.Parsed
        d_3_sub_ = ((d_2_x_).subcommand).value
        if not(((d_3_sub_).command) == (_dafny.Seq("other"))):
            raise _dafny.HaltException("test/GetOpt.dfy(230,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("eight"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("seven"), Wrappers.Option_Some(_dafny.Seq("seven_dflt")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(231,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(232,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).subcommand).is_None):
            raise _dafny.HaltException("test/GetOpt.dfy(233,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_4_valueOrError1_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_4_valueOrError1_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo"), _dafny.Seq("command"), _dafny.Seq("--six")]))
        if not(not((d_4_valueOrError1_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(235,9): " + _dafny.string_of(d_4_valueOrError1_))
        d_2_x_ = (d_4_valueOrError1_).Extract()
        if not(((d_2_x_).command) == (_dafny.Seq("cmd"))):
            raise _dafny.HaltException("test/GetOpt.dfy(236,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("two_dflt")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(237,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(238,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).subcommand).is_Some):
            raise _dafny.HaltException("test/GetOpt.dfy(239,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_3_sub_ = ((d_2_x_).subcommand).value
        if not(((d_3_sub_).command) == (_dafny.Seq("command"))):
            raise _dafny.HaltException("test/GetOpt.dfy(241,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("six"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("five"), Wrappers.Option_Some(_dafny.Seq("five_dflt")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(242,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(243,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_3_sub_).subcommand).is_None):
            raise _dafny.HaltException("test/GetOpt.dfy(244,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        d_5_valueOrError2_: Wrappers.Result = Wrappers.Result.default(GetOpt.Parsed.default())()
        d_5_valueOrError2_ = GetOpt.default__.GetOptions(d_0_MyOptions_, _dafny.Seq([_dafny.Seq("cmd"), _dafny.Seq("--foo")]))
        if not(not((d_5_valueOrError2_).IsFailure())):
            raise _dafny.HaltException("test/GetOpt.dfy(246,9): " + _dafny.string_of(d_5_valueOrError2_))
        d_2_x_ = (d_5_valueOrError2_).Extract()
        if not(((d_2_x_).command) == (_dafny.Seq("cmd"))):
            raise _dafny.HaltException("test/GetOpt.dfy(247,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).params) == (_dafny.Seq([GetOpt.OneArg_OneArg(_dafny.Seq("foo"), Wrappers.Option_None()), GetOpt.OneArg_OneArg(_dafny.Seq("two"), Wrappers.Option_Some(_dafny.Seq("two_dflt")))]))):
            raise _dafny.HaltException("test/GetOpt.dfy(248,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).files) == (_dafny.Seq([]))):
            raise _dafny.HaltException("test/GetOpt.dfy(249,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))
        if not(((d_2_x_).subcommand).is_None):
            raise _dafny.HaltException("test/GetOpt.dfy(250,4): " + _dafny.string_of(_dafny.Seq("expectation violation")))

    @staticmethod
    def TestDdbec():
        d_0_MyOptions_: GetOpt.Options
        d_0_MyOptions_ = GetOpt.Options_Options(_dafny.Seq("ddbec"), _dafny.Seq("Test the ddbec"), _dafny.Seq([GetOpt.Param_Command(GetOpt.Options_Options(_dafny.Seq("encrypt"), _dafny.Seq("Encrypts record"), _dafny.Seq([GetOpt.Param_Opt(_dafny.Seq("output"), _dafny.Seq("Write encrypted records to fileName."), _dafny.Seq("fileName"), 'o', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No())]))), GetOpt.Param_Command(GetOpt.Options_Options(_dafny.Seq("decrypt"), _dafny.Seq("Decrypts Records"), _dafny.Seq([GetOpt.Param_Opt(_dafny.Seq("expected"), _dafny.Seq("fileName contains expected plaintext records."), _dafny.Seq("fileName"), 'e', GetOpt.Unused_UnusedOk(), False, GetOpt.Visibility_Normal(), _dafny.Seq([]), _dafny.Seq([]), GetOpt.Tri_No())])))]))

