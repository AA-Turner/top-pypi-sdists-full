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
import GetOptTest as GetOptTest
import FloatCompareTest as FloatCompareTest
import TestCallMany as TestCallMany
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Views_Core as JSON_Utils_Views_Core
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Views_Writers as JSON_Utils_Views_Writers
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Lexers_Core as JSON_Utils_Lexers_Core
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Lexers_Strings as JSON_Utils_Lexers_Strings
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Cursors as JSON_Utils_Cursors
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Parsers as JSON_Utils_Parsers
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Str_CharStrConversion as JSON_Utils_Str_CharStrConversion
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Str_CharStrEscaping as JSON_Utils_Str_CharStrEscaping
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Str as JSON_Utils_Str
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Seq as JSON_Utils_Seq
import smithy_dafny_standard_library.internaldafny.generated.JSON_Utils_Vectors as JSON_Utils_Vectors
import smithy_dafny_standard_library.internaldafny.generated.JSON_Errors as JSON_Errors
import smithy_dafny_standard_library.internaldafny.generated.JSON_Values as JSON_Values
import smithy_dafny_standard_library.internaldafny.generated.JSON_Spec as JSON_Spec
import smithy_dafny_standard_library.internaldafny.generated.JSON_Grammar as JSON_Grammar
import smithy_dafny_standard_library.internaldafny.generated.JSON_Serializer_ByteStrConversion as JSON_Serializer_ByteStrConversion
import smithy_dafny_standard_library.internaldafny.generated.JSON_Serializer as JSON_Serializer
import smithy_dafny_standard_library.internaldafny.generated.JSON_Deserializer_Uint16StrConversion as JSON_Deserializer_Uint16StrConversion
import smithy_dafny_standard_library.internaldafny.generated.JSON_Deserializer_ByteStrConversion as JSON_Deserializer_ByteStrConversion
import smithy_dafny_standard_library.internaldafny.generated.JSON_Deserializer as JSON_Deserializer
import smithy_dafny_standard_library.internaldafny.generated.JSON_ConcreteSyntax_Spec as JSON_ConcreteSyntax_Spec
import smithy_dafny_standard_library.internaldafny.generated.JSON_ConcreteSyntax_SpecProperties as JSON_ConcreteSyntax_SpecProperties
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Serializer as JSON_ZeroCopy_Serializer
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Core as JSON_ZeroCopy_Deserializer_Core
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Strings as JSON_ZeroCopy_Deserializer_Strings
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Numbers as JSON_ZeroCopy_Deserializer_Numbers
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_ObjectParams as JSON_ZeroCopy_Deserializer_ObjectParams
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Objects as JSON_ZeroCopy_Deserializer_Objects
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_ArrayParams as JSON_ZeroCopy_Deserializer_ArrayParams
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Arrays as JSON_ZeroCopy_Deserializer_Arrays
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Constants as JSON_ZeroCopy_Deserializer_Constants
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_Values as JSON_ZeroCopy_Deserializer_Values
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer_API as JSON_ZeroCopy_Deserializer_API
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_Deserializer as JSON_ZeroCopy_Deserializer
import smithy_dafny_standard_library.internaldafny.generated.JSON_ZeroCopy_API as JSON_ZeroCopy_API
import smithy_dafny_standard_library.internaldafny.generated.JSON_API as JSON_API

# Module: module_

class default__:
    def  __init__(self):
        pass

    @staticmethod
    def Test____Main____(noArgsParameter__):
        d_0_success_: bool
        d_0_success_ = True
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestFromBytesSuccess: ")))
        try:
            if True:
                TestUUID.default__.TestFromBytesSuccess()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_1_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_1_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestFromBytesFailure: ")))
        try:
            if True:
                TestUUID.default__.TestFromBytesFailure()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_2_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_2_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestToBytesSuccess: ")))
        try:
            if True:
                TestUUID.default__.TestToBytesSuccess()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_3_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_3_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestToBytesFailure: ")))
        try:
            if True:
                TestUUID.default__.TestToBytesFailure()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_4_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_4_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestRoundTripStringConversion: ")))
        try:
            if True:
                TestUUID.default__.TestRoundTripStringConversion()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_5_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_5_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestRoundTripByteConversion: ")))
        try:
            if True:
                TestUUID.default__.TestRoundTripByteConversion()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_6_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_6_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUUID.TestGenerateAndConversion: ")))
        try:
            if True:
                TestUUID.default__.TestGenerateAndConversion()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_7_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_7_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.TestEncodeHappyCase: ")))
        try:
            if True:
                TestUTF8.default__.TestEncodeHappyCase()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_8_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_8_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.TestEncodeInvalidUnicode: ")))
        try:
            if True:
                TestUTF8.default__.TestEncodeInvalidUnicode()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_9_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_9_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.TestDecodeHappyCase: ")))
        try:
            if True:
                TestUTF8.default__.TestDecodeHappyCase()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_10_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_10_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.TestDecodeInvalidUnicode: ")))
        try:
            if True:
                TestUTF8.default__.TestDecodeInvalidUnicode()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_11_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_11_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.Test1Byte: ")))
        try:
            if True:
                TestUTF8.default__.Test1Byte()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_12_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_12_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.Test2Bytes: ")))
        try:
            if True:
                TestUTF8.default__.Test2Bytes()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_13_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_13_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.Test3Bytes: ")))
        try:
            if True:
                TestUTF8.default__.Test3Bytes()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_14_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_14_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestUTF8.Test4Bytes: ")))
        try:
            if True:
                TestUTF8.default__.Test4Bytes()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_15_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_15_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestTime.TestFormat: ")))
        try:
            if True:
                TestTime.default__.TestFormat()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_16_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_16_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestTime.TestNonDecreasing: ")))
        try:
            if True:
                TestTime.default__.TestNonDecreasing()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_17_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_17_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestTime.TestNonDecreasingMilli: ")))
        try:
            if True:
                TestTime.default__.TestNonDecreasingMilli()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_18_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_18_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestTime.TestPositiveValues: ")))
        try:
            if True:
                TestTime.default__.TestPositiveValues()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_19_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_19_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestTime.TestGetCurrentTimeStamp: ")))
        try:
            if True:
                TestTime.default__.TestGetCurrentTimeStamp()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_20_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_20_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestHasSubStringPos: ")))
        try:
            if True:
                TestStrings.default__.TestHasSubStringPos()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_21_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_21_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestSearchAndReplace: ")))
        try:
            if True:
                TestStrings.default__.TestSearchAndReplace()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_22_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_22_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestSearchAndReplaceAll: ")))
        try:
            if True:
                TestStrings.default__.TestSearchAndReplaceAll()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_23_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_23_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestHasSearchAndReplacePos: ")))
        try:
            if True:
                TestStrings.default__.TestHasSearchAndReplacePos()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_24_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_24_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestHasSubStringPositive: ")))
        try:
            if True:
                TestStrings.default__.TestHasSubStringPositive()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_25_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_25_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestHasSubStringNegative: ")))
        try:
            if True:
                TestStrings.default__.TestHasSubStringNegative()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_26_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_26_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestStrings.TestFileIO: ")))
        try:
            if True:
                TestStrings.default__.TestFileIO()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_27_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_27_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequenceEmpty: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequenceEmpty()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_28_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_28_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequenceOneItem: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequenceOneItem()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_29_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_29_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequenceSimple: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequenceSimple()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_30_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_30_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequencePrefix: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequencePrefix()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_31_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_31_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequenceComplex: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequenceComplex()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_32_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_32_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequenceComplexReverse: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequenceComplexReverse()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_33_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_33_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetSequence: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetSequence()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_34_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_34_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceUInt8Less.TestSetToOrderedSequenceManyItems: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceUInt8Less.default__.TestSetToOrderedSequenceManyItems()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_35_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_35_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedSequenceEmpty: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedSequenceEmpty()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_36_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_36_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedSequenceOneItem: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedSequenceOneItem()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_37_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_37_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedSequenceSimple: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedSequenceSimple()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_38_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_38_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedSequencePrefix: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedSequencePrefix()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_39_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_39_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedSequenceComplex: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedSequenceComplex()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_40_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_40_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedSequenceComplexReverse: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedSequenceComplexReverse()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_41_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_41_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetSequence: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetSequence()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_42_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_42_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestComputeSetToOrderedSequenceCharLess.TestSetToOrderedComplexUnicode: ")))
        try:
            if True:
                TestComputeSetToOrderedSequenceCharLess.default__.TestSetToOrderedComplexUnicode()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_43_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_43_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestOsLang.TestOsLang: ")))
        try:
            if True:
                TestOsLang.default__.TestOsLang()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_44_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_44_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("MemoryMathTest.BasicTests: ")))
        try:
            if True:
                MemoryMathTest.default__.BasicTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_45_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_45_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestHexStrings.BasicTests: ")))
        try:
            if True:
                TestHexStrings.default__.BasicTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_46_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_46_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestEmpty: ")))
        try:
            if True:
                GetOptTest.default__.TestEmpty()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_47_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_47_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestShort: ")))
        try:
            if True:
                GetOptTest.default__.TestShort()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_48_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_48_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestLong: ")))
        try:
            if True:
                GetOptTest.default__.TestLong()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_49_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_49_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestRequired: ")))
        try:
            if True:
                GetOptTest.default__.TestRequired()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_50_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_50_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestDeprecated: ")))
        try:
            if True:
                GetOptTest.default__.TestDeprecated()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_51_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_51_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestAlias: ")))
        try:
            if True:
                GetOptTest.default__.TestAlias()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_52_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_52_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestPositionalFail: ")))
        try:
            if True:
                GetOptTest.default__.TestPositionalFail()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_53_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_53_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestPositional: ")))
        try:
            if True:
                GetOptTest.default__.TestPositional()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_54_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_54_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestHelp: ")))
        try:
            if True:
                GetOptTest.default__.TestHelp()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_55_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_55_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestHelpFail: ")))
        try:
            if True:
                GetOptTest.default__.TestHelpFail()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_56_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_56_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestNested: ")))
        try:
            if True:
                GetOptTest.default__.TestNested()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_57_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_57_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestDefault: ")))
        try:
            if True:
                GetOptTest.default__.TestDefault()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_58_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_58_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("GetOptTest.TestDdbec: ")))
        try:
            if True:
                GetOptTest.default__.TestDdbec()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_59_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_59_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.TestOneTwoZeroMatrix: ")))
        try:
            if True:
                FloatCompareTest.default__.TestOneTwoZeroMatrix()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_60_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_60_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.SimpleTests: ")))
        try:
            if True:
                FloatCompareTest.default__.SimpleTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_61_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_61_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.SignTests: ")))
        try:
            if True:
                FloatCompareTest.default__.SignTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_62_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_62_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.ExponentTests: ")))
        try:
            if True:
                FloatCompareTest.default__.ExponentTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_63_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_63_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.ZeroTests: ")))
        try:
            if True:
                FloatCompareTest.default__.ZeroTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_64_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_64_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.ExtremeNumTest: ")))
        try:
            if True:
                FloatCompareTest.default__.ExtremeNumTest()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_65_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_65_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("FloatCompareTest.InvalidTests: ")))
        try:
            if True:
                FloatCompareTest.default__.InvalidTests()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_66_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_66_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        _dafny.print(_dafny.string_of(_dafny.Seq("TestCallMany.TestBasic: ")))
        try:
            if True:
                TestCallMany.default__.TestBasic()
                if True:
                    _dafny.print(_dafny.string_of(_dafny.Seq("PASSED\n")))
        except _dafny.HaltException as e:
            d_67_haltMessage_ = e.message
            if True:
                _dafny.print(_dafny.string_of(_dafny.Seq("FAILED\n	")))
                _dafny.print(_dafny.string_of(d_67_haltMessage_))
                _dafny.print(_dafny.string_of(_dafny.Seq("\n")))
                d_0_success_ = False
        if not(d_0_success_):
            raise _dafny.HaltException("<stdin>(1,0): " + _dafny.string_of(_dafny.Seq("Test failures occurred: see above.\n")))

