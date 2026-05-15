from typing import overload
from enum import IntEnum
import abc
import datetime
import typing

import Common.Util
import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Consolidators
import QuantConnect.Data.Fundamental
import QuantConnect.Data.Market
import QuantConnect.Data.UniverseSelection
import QuantConnect.Interfaces
import QuantConnect.Securities
import QuantConnect.Util
import System
import System.Collections.Generic
import System.Collections.Immutable
import System.Drawing
import System.IO
import System.Text
import System.Text.RegularExpressions
import System.Threading

QuantConnect_Util_MarketHoursDatabaseJsonConverter_MarketHoursDatabaseJson = typing.Any
Expression = typing.Any

QuantConnect_Util_SingleValueListConverter_T = typing.TypeVar("QuantConnect_Util_SingleValueListConverter_T")
QuantConnect_Util_FixedSizeQueue_T = typing.TypeVar("QuantConnect_Util_FixedSizeQueue_T")
QuantConnect_Util_CircularQueue_T = typing.TypeVar("QuantConnect_Util_CircularQueue_T")
QuantConnect_Util_TypeChangeJsonConverter_T = typing.TypeVar("QuantConnect_Util_TypeChangeJsonConverter_T")
QuantConnect_Util_TypeChangeJsonConverter_TResult = typing.TypeVar("QuantConnect_Util_TypeChangeJsonConverter_TResult")
QuantConnect_Util_MemoizingEnumerable_T = typing.TypeVar("QuantConnect_Util_MemoizingEnumerable_T")
QuantConnect_Util_IReadOnlyRef_T = typing.TypeVar("QuantConnect_Util_IReadOnlyRef_T")
QuantConnect_Util_Ref_T = typing.TypeVar("QuantConnect_Util_Ref_T")
QuantConnect_Util_NullStringValueConverter_T = typing.TypeVar("QuantConnect_Util_NullStringValueConverter_T")
QuantConnect_Util_BusyBlockingCollection_T = typing.TypeVar("QuantConnect_Util_BusyBlockingCollection_T")
QuantConnect_Util_FixedSizeHashQueue_T = typing.TypeVar("QuantConnect_Util_FixedSizeHashQueue_T")
QuantConnect_Util_BusyCollection_T = typing.TypeVar("QuantConnect_Util_BusyCollection_T")
QuantConnect_Util_ListComparer_T = typing.TypeVar("QuantConnect_Util_ListComparer_T")
QuantConnect_Util_ConcurrentSet_T = typing.TypeVar("QuantConnect_Util_ConcurrentSet_T")
QuantConnect_Util_ReferenceWrapper_T = typing.TypeVar("QuantConnect_Util_ReferenceWrapper_T")
QuantConnect_Util__EventContainer_Callable = typing.TypeVar("QuantConnect_Util__EventContainer_Callable")
QuantConnect_Util__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Util__EventContainer_ReturnType")
QuantConnect_Util_ExpressionBuilder_MakePropertyOrFieldSelector_T = typing.TypeVar("QuantConnect_Util_ExpressionBuilder_MakePropertyOrFieldSelector_T")
QuantConnect_Util_ExpressionBuilder_MakeBinaryComparisonLambda_T = typing.TypeVar("QuantConnect_Util_ExpressionBuilder_MakeBinaryComparisonLambda_T")
QuantConnect_Util_ExpressionBuilder_OfType_T = typing.TypeVar("QuantConnect_Util_ExpressionBuilder_OfType_T")
QuantConnect_Util_ExpressionBuilder_Single_T = typing.TypeVar("QuantConnect_Util_ExpressionBuilder_Single_T")
QuantConnect_Util_PythonUtil_ToAction_T1 = typing.TypeVar("QuantConnect_Util_PythonUtil_ToAction_T1")
QuantConnect_Util_PythonUtil_ToAction_T2 = typing.TypeVar("QuantConnect_Util_PythonUtil_ToAction_T2")
QuantConnect_Util_PythonUtil_ToFunc_T1 = typing.TypeVar("QuantConnect_Util_PythonUtil_ToFunc_T1")
QuantConnect_Util_PythonUtil_ToFunc_T2 = typing.TypeVar("QuantConnect_Util_PythonUtil_ToFunc_T2")
QuantConnect_Util_PythonUtil_ToFunc_T3 = typing.TypeVar("QuantConnect_Util_PythonUtil_ToFunc_T3")
QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T = typing.TypeVar("QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T")
QuantConnect_Util_Composer_Single_T = typing.TypeVar("QuantConnect_Util_Composer_Single_T")
QuantConnect_Util_Composer_AddPart_T = typing.TypeVar("QuantConnect_Util_Composer_AddPart_T")
QuantConnect_Util_Composer_GetPart_T = typing.TypeVar("QuantConnect_Util_Composer_GetPart_T")
QuantConnect_Util_Composer_GetParts_T = typing.TypeVar("QuantConnect_Util_Composer_GetParts_T")
QuantConnect_Util_Composer_GetExportedTypes_T = typing.TypeVar("QuantConnect_Util_Composer_GetExportedTypes_T")
QuantConnect_Util_Composer_GetExportedValueByTypeName_T = typing.TypeVar("QuantConnect_Util_Composer_GetExportedValueByTypeName_T")
QuantConnect_Util_Composer_GetExportedValues_T = typing.TypeVar("QuantConnect_Util_Composer_GetExportedValues_T")
QuantConnect_Util_Ref_Create_T = typing.TypeVar("QuantConnect_Util_Ref_Create_T")
QuantConnect_Util_Ref_CreateReadOnly_T = typing.TypeVar("QuantConnect_Util_Ref_CreateReadOnly_T")
QuantConnect_Util_ComparisonOperator_Compare_T = typing.TypeVar("QuantConnect_Util_ComparisonOperator_Compare_T")
QuantConnect_Util_EnumeratorExtensions_Where_T = typing.TypeVar("QuantConnect_Util_EnumeratorExtensions_Where_T")
QuantConnect_Util_EnumeratorExtensions_Select_T = typing.TypeVar("QuantConnect_Util_EnumeratorExtensions_Select_T")
QuantConnect_Util_EnumeratorExtensions_Select_TResult = typing.TypeVar("QuantConnect_Util_EnumeratorExtensions_Select_TResult")
QuantConnect_Util_EnumeratorExtensions_SelectMany_T = typing.TypeVar("QuantConnect_Util_EnumeratorExtensions_SelectMany_T")
QuantConnect_Util_EnumeratorExtensions_SelectMany_TResult = typing.TypeVar("QuantConnect_Util_EnumeratorExtensions_SelectMany_TResult")
QuantConnect_Util_ObjectActivator_Clone_T = typing.TypeVar("QuantConnect_Util_ObjectActivator_Clone_T")
QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K")
QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_V = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_V")
QuantConnect_Util_LinqExtensions_ToHashSet_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToHashSet_T")
QuantConnect_Util_LinqExtensions_ToHashSet_TResult = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToHashSet_TResult")
QuantConnect_Util_LinqExtensions_ToList_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToList_T")
QuantConnect_Util_LinqExtensions_ToList_TResult = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToList_TResult")
QuantConnect_Util_LinqExtensions_ToArray_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToArray_T")
QuantConnect_Util_LinqExtensions_ToArray_TResult = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToArray_TResult")
QuantConnect_Util_LinqExtensions_ToImmutableArray_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToImmutableArray_T")
QuantConnect_Util_LinqExtensions_ToImmutableArray_TResult = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToImmutableArray_TResult")
QuantConnect_Util_LinqExtensions_IsNullOrEmpty_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_IsNullOrEmpty_T")
QuantConnect_Util_LinqExtensions_Median_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_Median_T")
QuantConnect_Util_LinqExtensions_Median_TProperty = typing.TypeVar("QuantConnect_Util_LinqExtensions_Median_TProperty")
QuantConnect_Util_LinqExtensions_BinarySearch_TItem = typing.TypeVar("QuantConnect_Util_LinqExtensions_BinarySearch_TItem")
QuantConnect_Util_LinqExtensions_BinarySearch_TSearch = typing.TypeVar("QuantConnect_Util_LinqExtensions_BinarySearch_TSearch")
QuantConnect_Util_LinqExtensions_Memoize_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_Memoize_T")
QuantConnect_Util_LinqExtensions_Range_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_Range_T")
QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T")
QuantConnect_Util_LinqExtensions_AreDifferent_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_AreDifferent_T")
QuantConnect_Util_LinqExtensions_AsEnumerable_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_AsEnumerable_T")
QuantConnect_Util_LinqExtensions_GetValueOrDefault_K = typing.TypeVar("QuantConnect_Util_LinqExtensions_GetValueOrDefault_K")
QuantConnect_Util_LinqExtensions_GetValueOrDefault_V = typing.TypeVar("QuantConnect_Util_LinqExtensions_GetValueOrDefault_V")
QuantConnect_Util_LinqExtensions_DoForEach_T = typing.TypeVar("QuantConnect_Util_LinqExtensions_DoForEach_T")
QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey")
QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue")
QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource")
QuantConnect_Util_LinqExtensions_ToDataDictionary_TValue = typing.TypeVar("QuantConnect_Util_LinqExtensions_ToDataDictionary_TValue")
QuantConnect_Util_XElementExtensions_Get_T = typing.TypeVar("QuantConnect_Util_XElementExtensions_Get_T")
QuantConnect_Util_KeyStringSynchronizer_Execute_T = typing.TypeVar("QuantConnect_Util_KeyStringSynchronizer_Execute_T")


class ChartPointJsonConverter:
    """Json Converter for ChartPoint which handles special reading"""

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determine if this Converter can convert this type
        
        :param object_type: Type that we would like to convert
        :returns: True if Series.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """Reads series from Json"""
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """Write point to Json"""
        ...


class FuncTextWriter(System.IO.TextWriter):
    """Provides an implementation of TextWriter that redirects Write(string) and WriteLine(string)"""

    @property
    def encoding(self) -> System.Text.Encoding:
        ...

    def __init__(self, writer: typing.Callable[[str], typing.Any]) -> None:
        """
        Initializes a new instance of the FuncTextWriter that will direct
        messages to the algorithm's Debug function.
        
        :param writer: The algorithm hosting the Debug function where messages will be directed
        """
        ...

    def write(self, value: str) -> None:
        """
        Writes the string value using the delegate provided at construction
        
        :param value: The string value to be written
        """
        ...

    def write_line(self, value: str) -> None:
        """
        Writes the string value using the delegate provided at construction
        
        :param value: 
        """
        ...


class ColorJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[System.Drawing.Color, str]):
    """
    A JsonConverter implementation that serializes a Color as a string.
    If Color is empty, string is also empty and vice-versa. Meaning that color is autogen.
    """

    @overload
    def convert(self, value: System.Drawing.Color) -> str:
        """
        Converts a .NET Color to a hexadecimal as a string
        
        
        This Class is protected.
        
        :param value: The input value to be converted before serialization
        :returns: Hexadecimal number as a string. If .NET Color is null, returns default #000000.
        """
        ...

    @overload
    def convert(self, value: str) -> System.Drawing.Color:
        """
        Converts the input string to a .NET Color object
        
        
        This Class is protected.
        
        :param value: The deserialized value that needs to be converted to T
        :returns: The converted value.
        """
        ...


class SeriesJsonConverter:
    """Json Converter for Series which handles special Pie Series serialization case"""

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determine if this Converter can convert this type
        
        :param object_type: Type that we would like to convert
        :returns: True if Series.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """Reads series from Json"""
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Write Series to Json
        
        :param writer: The Json Writer to use
        :param value: The value to written to Json
        :param serializer: The Json Serializer to use
        """
        ...


class PerformanceTarget(IntEnum):
    """This class has no documentation."""

    SELECTION = 0

    SUBSCRIPTIONS = 1

    SLICE = 2

    ON_DATA = 3

    SCHEDULE = 4

    CONSOLIDATORS = 5

    SECURITIES = 6

    TRANSACTIONS = 7

    SPLITS_DIVIDENDS_DELISTING = 8


class PerformanceTrackingTool(System.Object):
    """Helper class to track algorithm performance"""

    @property
    def data_points(self) -> int:
        """Gets the number of data points processed per second"""
        ...

    @property
    def history_data_points(self) -> int:
        """Gets the number of data points of algorithm history provider"""
        ...

    def initialize(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> None:
        ...

    def sample(self, data_point_count: int, utc_algo_time: typing.Union[datetime.datetime, datetime.date]) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def start(self, target: QuantConnect.Util.PerformanceTarget) -> None:
        ...

    def stop(self, target: QuantConnect.Util.PerformanceTarget) -> None:
        ...


class JsonRoundingConverter:
    """
    Helper JsonConverter that will round decimal and double types,
    to FRACTIONAL_DIGITS fractional digits
    """

    FRACTIONAL_DIGITS: int = 4
    """The number of fractional digits to round to"""

    @property
    def can_read(self) -> bool:
        """
        Will always return false.
        Gets a value indicating whether this Newtonsoft.Json.JsonConverter can read JSON.
        """
        ...

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param object_type: Type of the object.
        :returns: True if this instance can convert the specified object type.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Not implemented, will throw NotImplementedException
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param object_type: Type of the object.
        :param existing_value: The existing value of object being read.
        :param serializer: The calling serializer.
        """
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class CurrencyPairUtil(System.Object):
    """Utility methods for decomposing and comparing currency pairs"""

    class Match(IntEnum):
        """Represents the relation between two currency pairs"""

        NO_MATCH = 0
        """The two currency pairs don't match each other normally nor when one is reversed"""

        EXACT_MATCH = 1
        """The two currency pairs match each other exactly"""

        INVERSE_MATCH = 2
        """The two currency pairs are the inverse of each other"""

    @staticmethod
    def compare_pair(pair_a: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], base_currency_b: str, quote_currency_b: str) -> QuantConnect.Util.CurrencyPairUtil.Match:
        """
        Returns how two currency pairs are related to each other
        
        :param pair_a: The first pair
        :param base_currency_b: The base currency of the second pair
        :param quote_currency_b: The quote currency of the second pair
        :returns: The Match member that represents the relation between the two pairs.
        """
        ...

    @staticmethod
    @overload
    def currency_pair_dual(currency_pair: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], known_symbol: str) -> str:
        """
        You have currency_pair AB and one known symbol (A or B). This function returns the other symbol (B or A).
        
        :param currency_pair: Currency pair AB
        :param known_symbol: Known part of the currency_pair (either A or B)
        :returns: The other part of currency_pair (either B or A), or null if known symbol is not part of currency_pair.
        """
        ...

    @staticmethod
    @overload
    def currency_pair_dual(base_currency: str, quote_currency: str, known_symbol: str) -> str:
        """
        You have currencyPair AB and one known symbol (A or B). This function returns the other symbol (B or A).
        
        :param base_currency: The base currency of the currency pair
        :param quote_currency: The quote currency of the currency pair
        :param known_symbol: Known part of the currencyPair (either A or B)
        :returns: The other part of currencyPair (either B or A), or null if known symbol is not part of the currency pair.
        """
        ...

    @staticmethod
    def decompose_currency_pair(currency_pair: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], base_currency: typing.Optional[str], quote_currency: typing.Optional[str], default_quote_currency: str = ...) -> typing.Tuple[None, str, str]:
        """
        Decomposes the specified currency pair into a base and quote currency provided as out parameters
        
        :param currency_pair: The input currency pair to be decomposed
        :param base_currency: The output base currency
        :param quote_currency: The output quote currency
        :param default_quote_currency: Optionally can provide a default quote currency
        """
        ...

    @staticmethod
    def is_decomposable(currency_pair: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]) -> bool:
        """
        Checks whether a symbol is decomposable into a base and a quote currency
        
        :param currency_pair: The pair to check for
        :returns: True if the pair can be decomposed into base and quote currencies, false if not.
        """
        ...

    @staticmethod
    def is_forex_decomposable(currency_pair: str) -> bool:
        """
        Checks whether a symbol is decomposable into a base and a quote currency
        
        :param currency_pair: The pair to check for
        :returns: True if the pair can be decomposed into base and quote currencies, false if not.
        """
        ...

    @staticmethod
    def is_valid_security_type(security_type: typing.Optional[QuantConnect.SecurityType], throw_exception: bool) -> bool:
        ...

    @staticmethod
    def try_decompose_currency_pair(currency_pair: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], base_currency: typing.Optional[str], quote_currency: typing.Optional[str]) -> typing.Tuple[bool, str, str]:
        """
        Tries to decomposes the specified currency pair into a base and quote currency provided as out parameters
        
        :param currency_pair: The input currency pair to be decomposed
        :param base_currency: The output base currency
        :param quote_currency: The output quote currency
        :returns: True if was able to decompose the currency pair.
        """
        ...


class MarketHoursDatabaseJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[QuantConnect.Securities.MarketHoursDatabase, QuantConnect_Util_MarketHoursDatabaseJsonConverter_MarketHoursDatabaseJson]):
    """Provides json conversion for the MarketHoursDatabase class"""

    class MarketHoursDatabaseJson(System.Object):
        """Defines the json structure of the market-hours-database.json file"""

        @property
        def entries(self) -> System.Collections.Generic.Dictionary[str, QuantConnect.Util.MarketHoursDatabaseJsonConverter.MarketHoursDatabaseEntryJson]:
            """The entries in the market hours database, keyed by SecurityDatabaseKey"""
            ...

        @entries.setter
        def entries(self, value: System.Collections.Generic.Dictionary[str, QuantConnect.Util.MarketHoursDatabaseJsonConverter.MarketHoursDatabaseEntryJson]) -> None:
            ...

        def __init__(self, database: QuantConnect.Securities.MarketHoursDatabase) -> None:
            """
            Initializes a new instance of the MarketHoursDatabaseJson class
            
            :param database: The database instance to copy
            """
            ...

        def convert(self) -> QuantConnect.Securities.MarketHoursDatabase:
            """
            Converts this json representation to the MarketHoursDatabase type
            
            :returns: A new instance of the MarketHoursDatabase class.
            """
            ...

    class MarketHoursDatabaseEntryJson(System.Object):
        """Defines the json structure of a single entry in the market-hours-database.json file"""

        @property
        def data_time_zone(self) -> str:
            """The data's raw time zone"""
            ...

        @data_time_zone.setter
        def data_time_zone(self, value: str) -> None:
            ...

        @property
        def exchange_time_zone(self) -> str:
            """The exchange's time zone id from the tzdb"""
            ...

        @exchange_time_zone.setter
        def exchange_time_zone(self, value: str) -> None:
            ...

        @property
        def sunday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Sunday market hours segments"""
            ...

        @sunday.setter
        def sunday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def monday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Monday market hours segments"""
            ...

        @monday.setter
        def monday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def tuesday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Tuesday market hours segments"""
            ...

        @tuesday.setter
        def tuesday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def wednesday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Wednesday market hours segments"""
            ...

        @wednesday.setter
        def wednesday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def thursday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Thursday market hours segments"""
            ...

        @thursday.setter
        def thursday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def friday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Friday market hours segments"""
            ...

        @friday.setter
        def friday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def saturday(self) -> typing.List[QuantConnect.Securities.MarketHoursSegment]:
            """Saturday market hours segments"""
            ...

        @saturday.setter
        def saturday(self, value: typing.List[QuantConnect.Securities.MarketHoursSegment]) -> None:
            ...

        @property
        def holidays(self) -> typing.List[str]:
            """Holiday date strings"""
            ...

        @holidays.setter
        def holidays(self, value: typing.List[str]) -> None:
            ...

        @property
        def early_closes(self) -> System.Collections.Generic.Dictionary[str, datetime.timedelta]:
            """Early closes by date"""
            ...

        @early_closes.setter
        def early_closes(self, value: System.Collections.Generic.Dictionary[str, datetime.timedelta]) -> None:
            ...

        @property
        def late_opens(self) -> System.Collections.Generic.Dictionary[str, datetime.timedelta]:
            """Late opens by date"""
            ...

        @late_opens.setter
        def late_opens(self, value: System.Collections.Generic.Dictionary[str, datetime.timedelta]) -> None:
            ...

        @property
        def bank_holidays(self) -> typing.List[str]:
            """Bank holidays date strings"""
            ...

        @bank_holidays.setter
        def bank_holidays(self, value: typing.List[str]) -> None:
            ...

        def __init__(self, entry: QuantConnect.Securities.MarketHoursDatabase.Entry) -> None:
            """
            Initializes a new instance of the MarketHoursDatabaseEntryJson class
            
            :param entry: The entry instance to copy
            """
            ...

        def convert(self, underlying_entry: QuantConnect.Securities.MarketHoursDatabase.Entry, market_entry: QuantConnect.Securities.MarketHoursDatabase.Entry) -> QuantConnect.Securities.MarketHoursDatabase.Entry:
            """
            Converts this json representation to the MarketHoursDatabase.Entry type
            
            :returns: A new instance of the MarketHoursDatabase.Entry class.
            """
            ...

    @overload
    def convert(self, value: QuantConnect.Securities.MarketHoursDatabase) -> QuantConnect.Util.MarketHoursDatabaseJsonConverter.MarketHoursDatabaseJson:
        """
        Convert the input value to a value to be serialzied
        
        
        This Class is protected.
        
        :param value: The input value to be converted before serialziation
        :returns: A new instance of TResult that is to be serialzied.
        """
        ...

    @overload
    def convert(self, value: QuantConnect.Util.MarketHoursDatabaseJsonConverter.MarketHoursDatabaseJson) -> QuantConnect.Securities.MarketHoursDatabase:
        """
        Converts the input value to be deserialized
        
        
        This Class is protected.
        
        :param value: The deserialized value that needs to be converted to T
        :returns: The converted value.
        """
        ...

    def create(self, type: typing.Type, token: typing.Any) -> QuantConnect.Securities.MarketHoursDatabase:
        """
        Creates an instance of the un-projected type to be deserialized
        
        
        This Class is protected.
        
        :param type: The input object type, this is the data held in the token
        :param token: The input data to be converted into a T
        :returns: A new instance of T that is to be serialized using default rules.
        """
        ...


class SingleValueListConverter(typing.Generic[QuantConnect_Util_SingleValueListConverter_T]):
    """Reads json and always produces a List, even if the input has just an object"""

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param object_type: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object. If the JSON represents a singular instance, it will be returned
        in a list.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param object_type: Type of the object.
        :param existing_value: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object. If the instance is not a list then it will
        be wrapped in a list
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class LeanData(System.Object):
    """Provides methods for generating lean data file content"""

    SECURITY_TYPE_AS_DATA_PATH: System.Collections.Generic.HashSet[str]
    """The different SecurityType used for data paths"""

    @staticmethod
    def aggregate_quote_bars(bars: typing.List[QuantConnect.Data.Market.QuoteBar], symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], resolution: datetime.timedelta) -> typing.Sequence[QuantConnect.Data.Market.QuoteBar]:
        """
        Aggregates a list of second/minute bars at the requested resolution
        
        :param bars: List of QuoteBars
        :param symbol: Symbol of all QuoteBars
        :param resolution: Desired resolution for new QuoteBars
        :returns: List of aggregated QuoteBars.
        """
        ...

    @staticmethod
    def aggregate_ticks(ticks: typing.List[QuantConnect.Data.Market.Tick], symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], resolution: datetime.timedelta) -> typing.Sequence[QuantConnect.Data.Market.QuoteBar]:
        """
        Aggregates a list of ticks at the requested resolution
        
        :param ticks: List of quote ticks
        :param symbol: Symbol of all ticks
        :param resolution: Desired resolution for new QuoteBars
        :returns: List of aggregated QuoteBars.
        """
        ...

    @staticmethod
    def aggregate_ticks_to_trade_bars(ticks: typing.List[QuantConnect.Data.Market.Tick], symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], resolution: datetime.timedelta) -> typing.Sequence[QuantConnect.Data.Market.TradeBar]:
        """
        Aggregates a list of ticks at the requested resolution
        
        :param ticks: List of trade ticks
        :param symbol: Symbol of all ticks
        :param resolution: Desired resolution for new TradeBars
        :returns: List of aggregated TradeBars.
        """
        ...

    @staticmethod
    def aggregate_trade_bars(bars: typing.List[QuantConnect.Data.Market.TradeBar], symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], resolution: datetime.timedelta) -> typing.Sequence[QuantConnect.Data.Market.TradeBar]:
        """
        Aggregates a list of second/minute bars at the requested resolution
        
        :param bars: List of TradeBars
        :param symbol: Symbol of all tradeBars
        :param resolution: Desired resolution for new TradeBars
        :returns: List of aggregated TradeBars.
        """
        ...

    @staticmethod
    @overload
    def generate_line(data: QuantConnect.Data.IBaseData, resolution: QuantConnect.Resolution, exchange_time_zone: typing.Any, data_time_zone: typing.Any) -> str:
        """
        Converts the specified base data instance into a lean data file csv line.
        This method takes into account the fake that base data instances typically
        are time stamped in the exchange time zone, but need to be written to disk
        in the data time zone.
        """
        ...

    @staticmethod
    @overload
    def generate_line(data: QuantConnect.Data.IBaseData, security_type: QuantConnect.SecurityType, resolution: QuantConnect.Resolution) -> str:
        """Converts the specified base data instance into a lean data file csv line"""
        ...

    @staticmethod
    def generate_relative_factor_file_path(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]) -> str:
        """Generates relative factor file paths for equities"""
        ...

    @staticmethod
    def generate_relative_universes_directory(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]) -> str:
        """Generates the relative directory to the universe files for the specified symbol"""
        ...

    @staticmethod
    def generate_relative_zip_file_directory(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], resolution: QuantConnect.Resolution) -> str:
        """Generates the relative zip directory for the specified symbol/resolution"""
        ...

    @staticmethod
    @overload
    def generate_relative_zip_file_path(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, tick_type: QuantConnect.TickType) -> str:
        """Generates the relative zip file path rooted in the /Data directory"""
        ...

    @staticmethod
    @overload
    def generate_relative_zip_file_path(symbol: str, security_type: QuantConnect.SecurityType, market: str, date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution) -> str:
        """Generates the relative zip file path rooted in the /Data directory"""
        ...

    @staticmethod
    def generate_universes_directory(data_directory: str, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]) -> str:
        """Generates the directory to the universe files for the specified symbol"""
        ...

    @staticmethod
    def generate_zip_entry_name(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, tick_type: QuantConnect.TickType) -> str:
        """Generate's the zip entry name to hold the specified data."""
        ...

    @staticmethod
    @overload
    def generate_zip_file_name(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, tick_type: QuantConnect.TickType) -> str:
        """Generates the zip file name for the specified date of data."""
        ...

    @staticmethod
    @overload
    def generate_zip_file_name(symbol: str, security_type: QuantConnect.SecurityType, date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, tick_type: typing.Optional[QuantConnect.TickType] = None) -> str:
        """Creates the zip file name for a QC zip data file"""
        ...

    @staticmethod
    @overload
    def generate_zip_file_path(data_directory: str, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution, tick_type: QuantConnect.TickType) -> str:
        """Generates the full zip file path rooted in the data_directory"""
        ...

    @staticmethod
    @overload
    def generate_zip_file_path(data_directory: str, symbol: str, security_type: QuantConnect.SecurityType, market: str, date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution) -> str:
        """Generates the full zip file path rooted in the data_directory"""
        ...

    @staticmethod
    def get_common_tick_type(security_type: QuantConnect.SecurityType) -> QuantConnect.TickType:
        """
        Gets the tick type most commonly associated with the specified security type
        
        :param security_type: The security type
        :returns: The most common tick type for the specified security type.
        """
        ...

    @staticmethod
    def get_common_tick_type_for_common_data_types(type: typing.Type, security_type: QuantConnect.SecurityType) -> QuantConnect.TickType:
        """
        Get the TickType for common Lean data types.
        If not a Lean common data type, return a TickType of Trade.
        
        :param type: A Type used to determine the TickType
        :param security_type: The SecurityType used to determine the TickType
        :returns: A TickType corresponding to the type.
        """
        ...

    @staticmethod
    def get_consolidator_start_time(period: datetime.timedelta, start_time: datetime.timedelta, time: typing.Union[datetime.datetime, datetime.date]) -> datetime.datetime:
        """Helper method to calculate the start time of a consolidator bar given a period, and anchor start time and the current data time"""
        ...

    @staticmethod
    @overload
    def get_daily_calendar(exchange_time_zone_date: typing.Union[datetime.datetime, datetime.date], exchange: QuantConnect.Securities.SecurityExchange, extended_market_hours: bool) -> QuantConnect.Data.Consolidators.CalendarInfo:
        """
        Helper method to return the start time and period of a bar the given point time should be part of
        
        :param exchange_time_zone_date: The point in time we want to get the bar information about
        :param exchange: The associated security exchange
        :param extended_market_hours: True if extended market hours should be taken into consideration
        :returns: The calendar information that holds a start time and a period.
        """
        ...

    @staticmethod
    @overload
    def get_daily_calendar(exchange_time_zone_date: typing.Union[datetime.datetime, datetime.date], exchange_hours: QuantConnect.Securities.SecurityExchangeHours, extended_market_hours: bool) -> QuantConnect.Data.Consolidators.CalendarInfo:
        """
        Helper method to return the start time and period of a bar the given point time should be part of
        
        :param exchange_time_zone_date: The point in time we want to get the bar information about
        :param exchange_hours: The associated exchange hours
        :param extended_market_hours: True if extended market hours should be taken into consideration
        :returns: The calendar information that holds a start time and a period.
        """
        ...

    @staticmethod
    def get_data_type(resolution: QuantConnect.Resolution, tick_type: QuantConnect.TickType) -> typing.Type:
        """
        Gets the data type required for the specified combination of resolution and tick type
        
        :param resolution: The resolution, if Tick, the Type returned is always Tick
        :param tick_type: The TickType that primarily dictates the type returned
        :returns: The Type used to create a subscription.
        """
        ...

    @staticmethod
    def get_next_daily_end_time(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], exchange_time_zone_date: typing.Union[datetime.datetime, datetime.date], exchange_hours: QuantConnect.Securities.SecurityExchangeHours) -> datetime.datetime:
        """Helper method to get the next daily end time, taking into account strict end times if appropriate"""
        ...

    @staticmethod
    def is_common_lean_data_type(base_data_type: typing.Type) -> bool:
        """
        Determines if the Type is a 'common' type used throughout lean
        This method is helpful in creating SubscriptionDataConfig
        
        :param base_data_type: The Type to check
        :returns: A bool indicating whether the type is of type TradeBarQuoteBar or OpenInterest.
        """
        ...

    @staticmethod
    def is_valid_configuration(security_type: QuantConnect.SecurityType, resolution: QuantConnect.Resolution, tick_type: QuantConnect.TickType) -> bool:
        """Helper method to determine if a configuration set is valid"""
        ...

    @staticmethod
    def option_use_scale_factor(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]) -> bool:
        """Helper method that defines the types of options that should use scale factor"""
        ...

    @staticmethod
    def parse_data_security_type(security_type: str) -> QuantConnect.SecurityType:
        """
        Matches a data path security type with the SecurityType
        
        :param security_type: The data path security type
        :returns: The matching security type for the given data path.
        """
        ...

    @staticmethod
    def parse_key(key: str, file_name: typing.Optional[str], entry_name: typing.Optional[str]) -> typing.Tuple[None, str, str]:
        """
        Helper to separate filename and entry from a given key for DataProviders
        
        :param key: The key to parse
        :param file_name: File name extracted
        :param entry_name: Entry name extracted
        """
        ...

    @staticmethod
    def parse_time(line: str, date: typing.Union[datetime.datetime, datetime.date], resolution: QuantConnect.Resolution) -> datetime.datetime:
        """Helper method that will parse a given data line in search of an associated date time"""
        ...

    @staticmethod
    def read_symbol_from_zip_entry(symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], resolution: QuantConnect.Resolution, zip_entry_name: str) -> QuantConnect.Symbol:
        """
        Creates a symbol from the specified zip entry name
        
        :param symbol: The root symbol of the output symbol
        :param resolution: The resolution of the data source producing the zip entry name
        :param zip_entry_name: The zip entry name to be parsed
        :returns: A new symbol representing the zip entry name.
        """
        ...

    @staticmethod
    def set_strict_end_times(base_data: QuantConnect.Data.IBaseData, exchange: QuantConnect.Securities.SecurityExchangeHours) -> bool:
        """
        Helper method that if appropiate, will set the Time and EndTime of the given data point to it's daily strict times
        
        :param base_data: The target data point
        :param exchange: The associated exchange hours
        """
        ...

    @staticmethod
    def supports_extended_market_hours(data_type: typing.Type) -> bool:
        """
        Helper method to determine if the specified data type supports extended market hours
        
        :param data_type: The data type
        :returns: Whether the specified data type supports extended market hours.
        """
        ...

    @staticmethod
    @overload
    def try_parse_path(file_path: str, symbol: typing.Optional[typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]], date: typing.Optional[typing.Union[datetime.datetime, datetime.date]], resolution: typing.Optional[QuantConnect.Resolution], tick_type: typing.Optional[QuantConnect.TickType], data_type: typing.Optional[typing.Type]) -> typing.Tuple[bool, typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], typing.Union[datetime.datetime, datetime.date], QuantConnect.Resolution, QuantConnect.TickType, typing.Type]:
        """
        Parses file name into a Security and DateTime
        
        :param file_path: File path to be parsed
        :param symbol: The symbol as parsed from the fileName
        :param date: Date of data in the file path. Only returned if the resolution is lower than Hourly
        :param resolution: The resolution of the symbol as parsed from the file_path
        :param tick_type: The tick type
        :param data_type: The data type
        """
        ...

    @staticmethod
    @overload
    def try_parse_path(file_name: str, symbol: typing.Optional[typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]], date: typing.Optional[typing.Union[datetime.datetime, datetime.date]], resolution: typing.Optional[QuantConnect.Resolution]) -> typing.Tuple[bool, typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], typing.Union[datetime.datetime, datetime.date], QuantConnect.Resolution]:
        """
        Parses file name into a Security and DateTime
        
        :param file_name: File name to be parsed
        :param symbol: The symbol as parsed from the file_name
        :param date: Date of data in the file path. Only returned if the resolution is lower than Hourly
        :param resolution: The resolution of the symbol as parsed from the filePath
        """
        ...

    @staticmethod
    @overload
    def try_parse_path(file_name: str, symbol: typing.Optional[typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security]], date: typing.Optional[typing.Union[datetime.datetime, datetime.date]], resolution: typing.Optional[QuantConnect.Resolution], is_universes: typing.Optional[bool]) -> typing.Tuple[bool, typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], typing.Union[datetime.datetime, datetime.date], QuantConnect.Resolution, bool]:
        """
        Parses file name into a Security and DateTime
        
        :param file_name: File name to be parsed
        :param symbol: The symbol as parsed from the file_name
        :param date: Date of data in the file path. Only returned if the resolution is lower than Hourly
        :param resolution: The resolution of the symbol as parsed from the filePath
        :param is_universes: Outputs whether the file path represents a universe data file.
        """
        ...

    @staticmethod
    def try_parse_security_type(file_name: str, security_type: typing.Optional[QuantConnect.SecurityType], market: typing.Optional[str]) -> typing.Tuple[bool, QuantConnect.SecurityType, str]:
        """
        Parses file name into a Security and DateTime
        
        :param file_name: File name to be parsed
        :param security_type: The security_type as parsed from the file_name
        :param market: The market as parsed from the file_name
        """
        ...

    @staticmethod
    @overload
    def use_daily_strict_end_times(settings: QuantConnect.Interfaces.IAlgorithmSettings, request: QuantConnect.Data.BaseDataRequest, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], increment: datetime.timedelta, exchange_hours: QuantConnect.Securities.SecurityExchangeHours = None) -> bool:
        """Helper method to determine if we should use strict end time"""
        ...

    @staticmethod
    @overload
    def use_daily_strict_end_times(settings: QuantConnect.Interfaces.IAlgorithmSettings, data_type: typing.Type, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], increment: datetime.timedelta, exchange_hours: QuantConnect.Securities.SecurityExchangeHours) -> bool:
        """Helper method to determine if we should use strict end time"""
        ...

    @staticmethod
    @overload
    def use_daily_strict_end_times(daily_strict_end_time_enabled: bool, data_type: typing.Type, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], increment: datetime.timedelta, exchange_hours: QuantConnect.Securities.SecurityExchangeHours) -> bool:
        """Helper method to determine if we should use strict end time"""
        ...

    @staticmethod
    @overload
    def use_daily_strict_end_times(data_type: typing.Type) -> bool:
        """True if this data type should use strict daily end times"""
        ...

    @staticmethod
    def use_strict_end_time(daily_strict_end_time_enabled: bool, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], increment: datetime.timedelta, exchange_hours: QuantConnect.Securities.SecurityExchangeHours) -> bool:
        """
        Helper method to determine if we should use strict end time
        
        :param symbol: The associated symbol
        :param increment: The datas time increment
        """
        ...


class Validate(System.Object):
    """Provides methods for validating strings following a certain format, such as an email address"""

    class RegularExpression(System.Object):
        """Provides static storage of compiled regular expressions to preclude parsing on each invocation"""

        EMAIL_DOMAIN_NAME: System.Text.RegularExpressions.Regex = ...
        """
        Matches the domain name in an email address ignored@<domain.com>
        Pattern sourced via msdn:
        https://docs.microsoft.com/en-us/dotnet/standard/base-types/how-to-verify-that-strings-are-in-valid-email-format
        """

        EMAIL: System.Text.RegularExpressions.Regex = ...
        """
        Matches a valid email address address@sub.domain.com
        Pattern sourced via msdn:
        https://docs.microsoft.com/en-us/dotnet/standard/base-types/how-to-verify-that-strings-are-in-valid-email-format
        """

    @staticmethod
    def email_address(email_address: str) -> bool:
        """
        Validates the provided email address
        
        :param email_address: The email address to be validated
        :returns: True if the provided email address is valid.
        """
        ...


class _Typed_ExpressionBuilder_MakePropertyOrFieldSelector(typing.Generic[QuantConnect_Util_ExpressionBuilder_MakePropertyOrFieldSelector_T]):
    """"""

    @overload
    def __call__(self, property_or_field: str) -> typing.Any:
        """
        Constructs a selector of the form: x => x.property_or_field where x is an instance of 'type'
        
        :param property_or_field: The name of the property or field to bind to
        :returns: A new lambda expression that represents accessing the property or field on 'type'.
        """
        ...


class _ExpressionBuilder_MakePropertyOrFieldSelector:
    """"""

    @overload
    def __call__(self, type: typing.Type, property_or_field: str) -> typing.Any:
        """
        Constructs a selector of the form: x => x.property_or_field where x is an instance of 'type'
        
        :param type: The type of the parameter in the expression
        :param property_or_field: The name of the property or field to bind to
        :returns: A new lambda expression that represents accessing the property or field on 'type'.
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Util_ExpressionBuilder_MakePropertyOrFieldSelector_T]) -> QuantConnect.Util._Typed_ExpressionBuilder_MakePropertyOrFieldSelector[QuantConnect_Util_ExpressionBuilder_MakePropertyOrFieldSelector_T]:
        ...


class _Typed_ExpressionBuilder_MakeBinaryComparisonLambda(typing.Generic[QuantConnect_Util_ExpressionBuilder_MakeBinaryComparisonLambda_T]):
    """"""

    @overload
    def __call__(self, type: typing.Any) -> typing.Any:
        """
        Constructs a lambda expression that accepts two parameters of type t and applies
        the specified binary comparison and returns the boolean result.
        """
        ...


class _ExpressionBuilder_MakeBinaryComparisonLambda:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_ExpressionBuilder_MakeBinaryComparisonLambda_T]) -> QuantConnect.Util._Typed_ExpressionBuilder_MakeBinaryComparisonLambda[QuantConnect_Util_ExpressionBuilder_MakeBinaryComparisonLambda_T]:
        ...


class _Typed_ExpressionBuilder_OfType(typing.Generic[QuantConnect_Util_ExpressionBuilder_OfType_T]):
    """"""

    @overload
    def __call__(self, expression: typing.Any) -> typing.Sequence[QuantConnect_Util_ExpressionBuilder_OfType_T]:
        """
        Returns all the expressions of the specified type in the given expression tree
        
        :param expression: The expression to search
        :returns: All expressions of the given type in the specified expression.
        """
        ...


class _ExpressionBuilder_OfType:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_ExpressionBuilder_OfType_T]) -> QuantConnect.Util._Typed_ExpressionBuilder_OfType[QuantConnect_Util_ExpressionBuilder_OfType_T]:
        ...


class _Typed_ExpressionBuilder_Single(typing.Generic[QuantConnect_Util_ExpressionBuilder_Single_T]):
    """"""

    @overload
    def __call__(self, expression: typing.Any) -> QuantConnect_Util_ExpressionBuilder_Single_T:
        """
        Returns the single expression of the specified type or throws if none or more than one expression
        of the specified type is contained within the expression.
        
        :param expression: The expression to search
        :returns: Expression of the specified type.
        """
        ...

    @overload
    def __call__(self, expressions: typing.List[Expression]) -> QuantConnect_Util_ExpressionBuilder_Single_T:
        """
        Returns the single expression of the specified type or throws if none or more than one expression
        of the specified type is contained within the expression.
        
        :param expressions: The expressions to search
        :returns: Expression of the specified type.
        """
        ...


class _ExpressionBuilder_Single:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_ExpressionBuilder_Single_T]) -> QuantConnect.Util._Typed_ExpressionBuilder_Single[QuantConnect_Util_ExpressionBuilder_Single_T]:
        ...


class ExpressionBuilder(System.Object):
    """Provides methods for constructing expressions at runtime"""

    make_property_or_field_selector: QuantConnect.Util._ExpressionBuilder_MakePropertyOrFieldSelector

    make_binary_comparison_lambda: QuantConnect.Util._ExpressionBuilder_MakeBinaryComparisonLambda

    of_type: QuantConnect.Util._ExpressionBuilder_OfType

    single: QuantConnect.Util._ExpressionBuilder_Single

    @staticmethod
    def as_enumerable(expression: typing.Any) -> typing.Sequence[Expression]:
        """
        Converts the specified expression into an enumerable of expressions by walking the expression tree
        
        :param expression: The expression to enumerate
        :returns: An enumerable containing all expressions in the input expression.
        """
        ...

    @staticmethod
    def is_binary_comparison(type: typing.Any) -> bool:
        """Determines whether or not the specified type is a binary comparison."""
        ...


class StreamReaderExtensions(System.Object):
    """Extension methods to fetch data from a StreamReader instance"""

    @staticmethod
    def get_char(stream: System.IO.StreamReader, delimiter: str = ...) -> str:
        """
        Gets a character from a stream reader
        
        :param stream: The data stream
        :param delimiter: The data delimiter character to use, default is ','
        :returns: The string instance read.
        """
        ...

    @staticmethod
    def get_date_time(stream: System.IO.StreamReader, format: str = ..., delimiter: str = ...) -> datetime.datetime:
        """
        Gets a date time instance from a stream reader
        
        :param stream: The data stream
        :param format: The format in which the date time is
        :param delimiter: The data delimiter character to use, default is ','
        :returns: The date time instance read.
        """
        ...

    @staticmethod
    @overload
    def get_decimal(stream: System.IO.StreamReader, delimiter: str = ...) -> float:
        """
        Gets a decimal from the provided stream reader
        
        :param stream: The data stream
        :param delimiter: The data delimiter character to use, default is ','
        :returns: The decimal read from the stream.
        """
        ...

    @staticmethod
    @overload
    def get_decimal(stream: System.IO.StreamReader, past_end_line: typing.Optional[bool], delimiter: str = ...) -> typing.Tuple[float, bool]:
        """
        Gets a decimal from the provided stream reader
        
        :param stream: The data stream
        :param delimiter: The data delimiter character to use, default is ','
        :param past_end_line: True if end line was past, useful for consumers to know a line ended
        :returns: The decimal read from the stream.
        """
        ...

    @staticmethod
    def get_int_32(stream: System.IO.StreamReader, delimiter: str = ...) -> int:
        """
        Gets an integer from a stream reader
        
        :param stream: The data stream
        :param delimiter: The data delimiter character to use, default is ','
        :returns: The integer instance read.
        """
        ...

    @staticmethod
    def get_int_64(stream: System.IO.StreamReader, delimiter: str = ...) -> int:
        """
        Gets an integer from a stream reader
        
        :param stream: The data stream
        :param delimiter: The data delimiter character to use, default is ','
        :returns: The integer instance read.
        """
        ...

    @staticmethod
    def get_string(stream: System.IO.StreamReader, delimiter: str = ...) -> str:
        """
        Gets a string from a stream reader
        
        :param stream: The data stream
        :param delimiter: The data delimiter character to use, default is ','
        :returns: The string instance read.
        """
        ...


class FixedSizeQueue(typing.Generic[QuantConnect_Util_FixedSizeQueue_T], System.Collections.Generic.Queue[QuantConnect_Util_FixedSizeQueue_T]):
    """
    Helper method for a limited length queue which self-removes the extra elements.
    http://stackoverflow.com/questions/5852863/fixed-size-queue-which-automatically-dequeues-old-values-upon-new-enques
    """

    @property
    def limit(self) -> int:
        """Max Length"""
        ...

    @limit.setter
    def limit(self, value: int) -> None:
        ...

    def __init__(self, limit: int) -> None:
        """Create a new fixed length queue:"""
        ...

    def enqueue(self, item: QuantConnect_Util_FixedSizeQueue_T) -> None:
        """Enqueue a new item int the generic fixed length queue:"""
        ...


class CandlestickJsonConverter:
    """Candlestick Json Converter"""

    @property
    def can_read(self) -> bool:
        """This converter wont be used to read JSON. Will throw exception if manually called."""
        ...

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determine if this Converter can convert this type
        
        :param object_type: Type that we would like to convert
        :returns: True if Series.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """Json reader implementation which handles backwards compatiblity for old equity chart points"""
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Write Series to Json
        
        :param writer: The Json Writer to use
        :param value: The value to written to Json
        :param serializer: The Json Serializer to use
        """
        ...


class LeanDataPathComponents(System.Object):
    """Type representing the various pieces of information emebedded into a lean data file path"""

    @property
    def date(self) -> datetime.datetime:
        """Gets the date component from the file name"""
        ...

    @property
    def security_type(self) -> QuantConnect.SecurityType:
        """Gets the security type from the path"""
        ...

    @property
    def market(self) -> str:
        """Gets the market from the path"""
        ...

    @property
    def resolution(self) -> QuantConnect.Resolution:
        """Gets the resolution from the path"""
        ...

    @property
    def filename(self) -> str:
        """Gets the file name, not inluding directory information"""
        ...

    @property
    def symbol(self) -> QuantConnect.Symbol:
        """
        Gets the symbol object implied by the path. For options, or any
        multi-entry zip file, this should be the canonical symbol
        """
        ...

    @property
    def tick_type(self) -> QuantConnect.TickType:
        """Gets the tick type from the file name"""
        ...

    def __init__(self, security_type: QuantConnect.SecurityType, market: str, resolution: QuantConnect.Resolution, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], filename: str, date: typing.Union[datetime.datetime, datetime.date], tick_type: QuantConnect.TickType) -> None:
        """Initializes a new instance of the LeanDataPathComponents class"""
        ...

    @staticmethod
    def parse(path: str) -> QuantConnect.Util.LeanDataPathComponents:
        """
        Parses the specified path into a new instance of the LeanDataPathComponents class
        
        :param path: The path to be parsed
        :returns: A new instance of the LeanDataPathComponents class representing the specified path.
        """
        ...


class _Typed_PythonUtil_ToAction(typing.Generic[QuantConnect_Util_PythonUtil_ToAction_T1]):
    """"""

    @overload
    def __call__(self, py_object: typing.Any) -> typing.Callable[[QuantConnect_Util_PythonUtil_ToAction_T1], typing.Any]:
        """
        Encapsulates a python method with a System.Action{T1}
        
        :param py_object: The python method
        :returns: A System.Action{T1} that encapsulates the python method.
        """
        ...

    @overload
    def __call__(self, py_object: typing.Any) -> typing.Callable[[QuantConnect_Util_PythonUtil_ToAction_T1, QuantConnect_Util_PythonUtil_ToAction_T2], typing.Any]:
        """
        Encapsulates a python method with a System.Action{T1, T2}
        
        :param py_object: The python method
        :returns: A System.Action{T1, T2} that encapsulates the python method.
        """
        ...


class _PythonUtil_ToAction:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_PythonUtil_ToAction_T1]) -> QuantConnect.Util._Typed_PythonUtil_ToAction[QuantConnect_Util_PythonUtil_ToAction_T1]:
        ...


class _Typed_PythonUtil_ToFunc(typing.Generic[QuantConnect_Util_PythonUtil_ToFunc_T1]):
    """"""

    @overload
    def __call__(self, py_object: typing.Any) -> typing.Callable[[QuantConnect_Util_PythonUtil_ToFunc_T1], QuantConnect_Util_PythonUtil_ToFunc_T2]:
        """
        Encapsulates a python method with a System.Func{T1, T2}
        
        :param py_object: The python method
        :returns: A System.Func{T1, T2} that encapsulates the python method.
        """
        ...

    @overload
    def __call__(self, py_object: typing.Any) -> typing.Callable[[QuantConnect_Util_PythonUtil_ToFunc_T1, QuantConnect_Util_PythonUtil_ToFunc_T2], QuantConnect_Util_PythonUtil_ToFunc_T3]:
        """
        Encapsulates a python method with a System.Func{T1, T2, T3}
        
        :param py_object: The python method
        :returns: A System.Func{T1, T2, T3} that encapsulates the python method.
        """
        ...


class _PythonUtil_ToFunc:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_PythonUtil_ToFunc_T1]) -> QuantConnect.Util._Typed_PythonUtil_ToFunc[QuantConnect_Util_PythonUtil_ToFunc_T1]:
        ...


class _Typed_PythonUtil_CreateInstanceOrWrapper(typing.Generic[QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T]):
    """"""

    @overload
    def __call__(self, py_object: typing.Any, create_wrapper: typing.Callable[[typing.Any], QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T]) -> QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T:
        """
        Attempts to convert a PyObject into a pure C# instance of t.
        If conversion fails, a wrapper instance is created/>.
        
        :param py_object: The Python object to convert.
        :param create_wrapper: Factory function used to create a wrapper around the Python object
        :returns: A pure C# instance if conversion is possible, otherwise a wrapper instance.
        """
        ...


class _PythonUtil_CreateInstanceOrWrapper:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T]) -> QuantConnect.Util._Typed_PythonUtil_CreateInstanceOrWrapper[QuantConnect_Util_PythonUtil_CreateInstanceOrWrapper_T]:
        ...


class PythonUtil(System.Object):
    """Collection of utils for python objects processing"""

    exception_line_shift: int
    """The python exception stack trace line shift to use"""

    to_action: QuantConnect.Util._PythonUtil_ToAction

    to_func: QuantConnect.Util._PythonUtil_ToFunc

    create_instance_or_wrapper: QuantConnect.Util._PythonUtil_CreateInstanceOrWrapper

    @staticmethod
    def convert_to_symbols(input: typing.Any) -> typing.Sequence[QuantConnect.Symbol]:
        """
        Convert Python input to a list of Symbols
        
        :param input: Object with the desired property
        :returns: List of Symbols.
        """
        ...

    @staticmethod
    def python_exception_message_parser(message: str) -> str:
        """
        Parsers Exception.Message into a readable message
        
        :param message: The python exception message
        :returns: String with relevant part of the stacktrace.
        """
        ...

    @staticmethod
    def python_exception_parser(python_exception: typing.Any) -> str:
        """
        Parsers PythonException into a readable message
        
        :param python_exception: The exception to parse
        :returns: String with relevant part of the stacktrace.
        """
        ...

    @staticmethod
    def python_exception_stack_parser(value: str) -> str:
        """
        Parsers PythonException.StackTrace into a readable message
        
        :param value: String with the stacktrace information
        :returns: String with relevant part of the stacktrace.
        """
        ...

    @staticmethod
    def to_coarse_fundamental_selector(py_object: typing.Any) -> typing.Callable[[typing.Sequence[QuantConnect.Data.UniverseSelection.CoarseFundamental]], typing.Sequence[QuantConnect.Symbol]]:
        """
        Encapsulates a python method in coarse fundamental universe selector.
        
        :param py_object: The python method
        :returns: A Func{T, TResult} (parameter is IEnumerable{CoarseFundamental}, return value is IEnumerable{Symbol}) that encapsulates the python method.
        """
        ...

    @staticmethod
    def to_fine_fundamental_selector(py_object: typing.Any) -> typing.Callable[[typing.Sequence[QuantConnect.Data.Fundamental.FineFundamental]], typing.Sequence[QuantConnect.Symbol]]:
        """
        Encapsulates a python method in fine fundamental universe selector.
        
        :param py_object: The python method
        :returns: A Func{T, TResult} (parameter is IEnumerable{FineFundamental}, return value is IEnumerable{Symbol}) that encapsulates the python method.
        """
        ...


class CircularQueue(typing.Generic[QuantConnect_Util_CircularQueue_T], System.Object):
    """A never ending queue that will dequeue and reenqueue the same item"""

    @property
    def circle_completed(self) -> _EventContainer[typing.Callable[[System.Object, System.EventArgs], typing.Any], typing.Any]:
        """Fired when we do a full circle"""
        ...

    @circle_completed.setter
    def circle_completed(self, value: _EventContainer[typing.Callable[[System.Object, System.EventArgs], typing.Any], typing.Any]) -> None:
        ...

    @overload
    def __init__(self, *items: typing.Union[QuantConnect_Util_CircularQueue_T, typing.Iterable[QuantConnect_Util_CircularQueue_T]]) -> None:
        """
        Initializes a new instance of the CircularQueue{T} class
        
        :param items: The items in the queue
        """
        ...

    @overload
    def __init__(self, items: typing.List[QuantConnect_Util_CircularQueue_T]) -> None:
        """
        Initializes a new instance of the CircularQueue{T} class
        
        :param items: The items in the queue
        """
        ...

    def dequeue(self) -> QuantConnect_Util_CircularQueue_T:
        """
        Dequeues the next item
        
        :returns: The next item.
        """
        ...

    def on_circle_completed(self) -> None:
        """
        Event invocator for the circle_completed evet
        
        
        This Class is protected.
        """
        ...


class DoubleUnixSecondsDateTimeJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[typing.Optional[datetime.datetime], typing.Optional[float]]):
    """Defines a JsonConverter that serializes DateTime use the number of whole and fractional seconds since unix epoch"""

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param object_type: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    @overload
    def convert(self, value: typing.Optional[datetime.datetime]) -> typing.Optional[float]:
        """
        Convert the input value to a value to be serialzied
        
        
        This Class is protected.
        
        :param value: The input value to be converted before serialziation
        :returns: A new instance of TResult that is to be serialzied.
        """
        ...

    @overload
    def convert(self, value: typing.Optional[float]) -> typing.Optional[datetime.datetime]:
        """
        Converts the input value to be deserialized
        
        
        This Class is protected.
        
        :param value: The deserialized value that needs to be converted to T
        :returns: The converted value.
        """
        ...


class DateTimeJsonConverter:
    """Provides a json converter that allows defining the date time format used"""

    @property
    def can_read(self) -> bool:
        """True, can read a json into a date time"""
        ...

    @property
    def can_write(self) -> bool:
        """True, can write a datetime to json"""
        ...

    @overload
    def __init__(self, format: str) -> None:
        """
        Initializes a new instance of the DateTimeJsonConverter class
        
        :param format: >The date time format
        """
        ...

    @overload
    def __init__(self, format: str, format_2: str) -> None:
        """
        Initializes a new instance of the DateTimeJsonConverter class
        
        :param format: >The date time format
        :param format_2: Other format for backwards compatibility
        """
        ...

    @overload
    def __init__(self, format: str, format_2: str, format_3: str) -> None:
        """
        Initializes a new instance of the DateTimeJsonConverter class
        
        :param format: >The date time format
        :param format_2: Other format for backwards compatibility
        :param format_3: Other format for backwards compatibility
        """
        ...

    def can_convert(self, object_type: typing.Type) -> bool:
        """True if can convert the given object type"""
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """Converts the given value"""
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """Writes the given value to json"""
        ...


class TypeChangeJsonConverter(typing.Generic[QuantConnect_Util_TypeChangeJsonConverter_T, QuantConnect_Util_TypeChangeJsonConverter_TResult], metaclass=abc.ABCMeta):
    """
    Provides a base class for a JsonConverter that serializes a
    an input type as some other output type
    """

    @property
    def populate_properties(self) -> bool:
        """
        True will populate TResult object returned by convert(TResult) with json properties
        
        
        This Property is protected.
        """
        ...

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param object_type: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    @overload
    def convert(self, value: QuantConnect_Util_TypeChangeJsonConverter_T) -> QuantConnect_Util_TypeChangeJsonConverter_TResult:
        """
        Convert the input value to a value to be serialized
        
        
        This Class is protected.
        
        :param value: The input value to be converted before serialziation
        :returns: A new instance of TResult that is to be serialzied.
        """
        ...

    @overload
    def convert(self, value: QuantConnect_Util_TypeChangeJsonConverter_TResult) -> QuantConnect_Util_TypeChangeJsonConverter_T:
        """
        Converts the input value to be deserialized
        
        
        This Class is protected.
        
        :param value: The deserialized value that needs to be converted to T
        :returns: The converted value.
        """
        ...

    def create(self, type: typing.Type, token: typing.Any) -> QuantConnect_Util_TypeChangeJsonConverter_T:
        """
        Creates an instance of the un-projected type to be deserialized
        
        
        This Class is protected.
        
        :param type: The input object type, this is the data held in the token
        :param token: The input data to be converted into a T
        :returns: A new instance of T that is to be serialized using default rules.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param object_type: Type of the object.
        :param existing_value: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class _Typed_Composer_Single(typing.Generic[QuantConnect_Util_Composer_Single_T]):
    """"""

    @overload
    def __call__(self, predicate: typing.Callable[[QuantConnect_Util_Composer_Single_T], bool]) -> QuantConnect_Util_Composer_Single_T:
        """
        Gets the export matching the predicate
        
        :param predicate: Function used to pick which imported instance to return, if null the first instance is returned
        :returns: The only export matching the specified predicate.
        """
        ...


class _Composer_Single:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_Single_T]) -> QuantConnect.Util._Typed_Composer_Single[QuantConnect_Util_Composer_Single_T]:
        ...


class _Typed_Composer_AddPart(typing.Generic[QuantConnect_Util_Composer_AddPart_T]):
    """"""

    @overload
    def __call__(self, instance: QuantConnect_Util_Composer_AddPart_T) -> None:
        """
        Adds the specified instance to this instance to allow it to be recalled via GetExportedValueByTypeName
        
        :param instance: The instance to add
        """
        ...


class _Composer_AddPart:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_AddPart_T]) -> QuantConnect.Util._Typed_Composer_AddPart[QuantConnect_Util_Composer_AddPart_T]:
        ...


class _Typed_Composer_GetPart(typing.Generic[QuantConnect_Util_Composer_GetPart_T]):
    """"""

    @overload
    def __call__(self) -> QuantConnect_Util_Composer_GetPart_T:
        """Gets the first type T instance if any"""
        ...

    @overload
    def __call__(self, filter: typing.Callable[[QuantConnect_Util_Composer_GetPart_T], bool]) -> QuantConnect_Util_Composer_GetPart_T:
        """Gets the first type T instance if any"""
        ...


class _Composer_GetPart:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_GetPart_T]) -> QuantConnect.Util._Typed_Composer_GetPart[QuantConnect_Util_Composer_GetPart_T]:
        ...


class _Typed_Composer_GetParts(typing.Generic[QuantConnect_Util_Composer_GetParts_T]):
    """"""

    @overload
    def __call__(self) -> typing.Sequence[QuantConnect_Util_Composer_GetParts_T]:
        """Gets all parts of type T instance if any"""
        ...


class _Composer_GetParts:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_GetParts_T]) -> QuantConnect.Util._Typed_Composer_GetParts[QuantConnect_Util_Composer_GetParts_T]:
        ...


class _Typed_Composer_GetExportedTypes(typing.Generic[QuantConnect_Util_Composer_GetExportedTypes_T]):
    """"""

    @overload
    def __call__(self) -> typing.Sequence[typing.Type]:
        """Will return all loaded types that are assignable to T type"""
        ...


class _Composer_GetExportedTypes:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_GetExportedTypes_T]) -> QuantConnect.Util._Typed_Composer_GetExportedTypes[QuantConnect_Util_Composer_GetExportedTypes_T]:
        ...


class _Typed_Composer_GetExportedValueByTypeName(typing.Generic[QuantConnect_Util_Composer_GetExportedValueByTypeName_T]):
    """"""

    @overload
    def __call__(self, type_name: str, force_type_name_on_existing: bool = True) -> QuantConnect_Util_Composer_GetExportedValueByTypeName_T:
        """
        Extension method to searches the composition container for an export that has a matching type name. This function
        will first try to match on Type.AssemblyQualifiedName, then Type.FullName, and finally on Type.Name
        
        This method will not throw if multiple types are found matching the name, it will just return the first one it finds.
        
        :param type_name: The name of the type to find. This can be an assembly qualified name, a full name, or just the type's name
        :param force_type_name_on_existing: When false, if any existing instance of type T is found, it will be returned even if type name doesn't match.
        This is useful in cases where a single global instance is desired, like for IDataAggregator
        :returns: The export instance.
        """
        ...


class _Composer_GetExportedValueByTypeName:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_GetExportedValueByTypeName_T]) -> QuantConnect.Util._Typed_Composer_GetExportedValueByTypeName[QuantConnect_Util_Composer_GetExportedValueByTypeName_T]:
        ...


class _Typed_Composer_GetExportedValues(typing.Generic[QuantConnect_Util_Composer_GetExportedValues_T]):
    """"""

    @overload
    def __call__(self) -> typing.Sequence[QuantConnect_Util_Composer_GetExportedValues_T]:
        """Gets all exports of type T"""
        ...


class _Composer_GetExportedValues:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Composer_GetExportedValues_T]) -> QuantConnect.Util._Typed_Composer_GetExportedValues[QuantConnect_Util_Composer_GetExportedValues_T]:
        ...


class Composer(System.Object):
    """Provides methods for obtaining exported MEF instances"""

    INSTANCE: QuantConnect.Util.Composer
    """Gets the singleton instance"""

    @property
    def single(self) -> QuantConnect.Util._Composer_Single:
        ...

    @property
    def add_part(self) -> QuantConnect.Util._Composer_AddPart:
        ...

    @property
    def get_part(self) -> QuantConnect.Util._Composer_GetPart:
        ...

    @property
    def get_parts(self) -> QuantConnect.Util._Composer_GetParts:
        ...

    @property
    def get_exported_types(self) -> QuantConnect.Util._Composer_GetExportedTypes:
        ...

    @property
    def get_exported_value_by_type_name(self) -> QuantConnect.Util._Composer_GetExportedValueByTypeName:
        ...

    @property
    def get_exported_values(self) -> QuantConnect.Util._Composer_GetExportedValues:
        ...

    def __init__(self) -> None:
        """
        Initializes a new instance of the Composer class. This type
        is a light wrapper on top of an MEF CompositionContainer
        """
        ...

    def reset(self) -> None:
        """Clears the cache of exported values, causing new instances to be created."""
        ...


class StringDecimalJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[float, str]):
    """Allows for conversion of string numeric values from JSON to the decimal type"""

    def __init__(self, default_on_failure: bool = False) -> None:
        """
        Creates an instance of the class, with an optional flag to default to decimal's default value on failure.
        
        :param default_on_failure: Default to decimal's default value on failure
        """
        ...

    @overload
    def convert(self, value: float) -> str:
        """
        Converts a decimal to a string
        
        
        This Class is protected.
        
        :param value: The input value to be converted before serialization
        :returns: String representation of the decimal.
        """
        ...

    @overload
    def convert(self, value: str) -> float:
        """
        Converts the input string to a decimal
        
        
        This Class is protected.
        
        :param value: The deserialized value that needs to be converted to T
        :returns: The converted value.
        """
        ...


class DisposableExtensions(System.Object):
    """Provides extensions methods for IDisposable"""

    @staticmethod
    @overload
    def dispose_safely(disposable: System.IDisposable) -> bool:
        """
        Calls IDisposable.Dispose within a try/catch and logs any errors.
        
        :param disposable: The IDisposable to be disposed
        :returns: True if the object was successfully disposed, false if an error was thrown.
        """
        ...

    @staticmethod
    @overload
    def dispose_safely(disposable: System.IDisposable, error_handler: typing.Callable[[System.Exception], typing.Any]) -> bool:
        """
        Calls IDisposable.Dispose within a try/catch and invokes the
        error_handler on any errors.
        
        :param disposable: The IDisposable to be disposed
        :param error_handler: Error handler delegate invoked if an exception is thrown
        while calling IDisposable.Dispose
        :returns: True if the object was successfully disposed, false if an error was thrown or
        the specified disposable was null.
        """
        ...


class ReaderWriterLockSlimExtensions(System.Object):
    """Provides extension methods to make working with the ReaderWriterLockSlim class easier"""

    @staticmethod
    def read(reader_writer_lock_slim: System.Threading.ReaderWriterLockSlim) -> System.IDisposable:
        """
        Opens the read lock
        
        :param reader_writer_lock_slim: The lock to open for read
        :returns: A disposable reference which will release the lock upon disposal.
        """
        ...

    @staticmethod
    def write(reader_writer_lock_slim: System.Threading.ReaderWriterLockSlim) -> System.IDisposable:
        """
        Opens the write lock
        
        :param reader_writer_lock_slim: The lock to open for write
        :returns: A disposale reference which will release thelock upon disposal.
        """
        ...


class MemoizingEnumerable(typing.Generic[QuantConnect_Util_MemoizingEnumerable_T], System.Object, typing.Iterable[QuantConnect_Util_MemoizingEnumerable_T]):
    """
    Defines an enumerable that can be enumerated many times while
    only performing a single enumeration of the root enumerable
    """

    @property
    def enabled(self) -> bool:
        """Allow disableing the buffering"""
        ...

    @enabled.setter
    def enabled(self, value: bool) -> None:
        ...

    @property
    def count(self) -> int:
        """Gets the count of items in the enumerable. This will force enumeration of the entire collection if it has not already been enumerated."""
        ...

    def __init__(self, enumerable: typing.List[QuantConnect_Util_MemoizingEnumerable_T]) -> None:
        """
        Initializes a new instance of the MemoizingEnumerable{T} class
        
        :param enumerable: The source enumerable to be memoized
        """
        ...

    def __iter__(self) -> typing.Iterator[QuantConnect_Util_MemoizingEnumerable_T]:
        ...

    def __len__(self) -> int:
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect_Util_MemoizingEnumerable_T]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...


class PerformanceTimer(System.Object):
    """Helper class to keep track of wall time, an efficient stop watch implementation"""

    def get_and_reset(self) -> float:
        ...

    def get_total_time(self) -> float:
        ...

    def start(self) -> None:
        ...

    def stop(self) -> None:
        ...


class SecurityIdentifierJsonConverter(QuantConnect.Util.TypeChangeJsonConverter[QuantConnect.SecurityIdentifier, str]):
    """A JsonConverter implementation that serializes a SecurityIdentifier as a string"""

    @overload
    def convert(self, value: QuantConnect.SecurityIdentifier) -> str:
        """
        Converts as security identifier to a string
        
        
        This Class is protected.
        
        :param value: The input value to be converted before serialziation
        :returns: A new instance of TResult that is to be serialzied.
        """
        ...

    @overload
    def convert(self, value: str) -> QuantConnect.SecurityIdentifier:
        """
        Converts the input string to a security identifier
        
        
        This Class is protected.
        
        :param value: The deserialized value that needs to be converted to T
        :returns: The converted value.
        """
        ...


class IReadOnlyRef(typing.Generic[QuantConnect_Util_IReadOnlyRef_T], metaclass=abc.ABCMeta):
    """Represents a read-only reference to any value, T"""

    @property
    @abc.abstractmethod
    def value(self) -> QuantConnect_Util_IReadOnlyRef_T:
        """Gets the current value this reference points to"""
        ...


class _Typed_Ref_Create(typing.Generic[QuantConnect_Util_Ref_Create_T]):
    """"""

    @overload
    def __call__(self, getter: typing.Callable[[], QuantConnect_Util_Ref_Create_T], setter: typing.Callable[[QuantConnect_Util_Ref_Create_T], typing.Any]) -> QuantConnect.Util.Ref[QuantConnect_Util_Ref_Create_T]:
        """Creates a new Ref{T} instance"""
        ...

    @overload
    def __call__(self, initial_value: QuantConnect_Util_Ref_Create_T) -> QuantConnect.Util.Ref[QuantConnect_Util_Ref_Create_T]:
        """
        Creates a new Ref{T} instance by closing over
        the specified initial_value variable.
        NOTE: This won't close over the variable input to the function,
        but rather a copy of the variable. This reference will use it's
        own storage.
        """
        ...


class _Ref_Create:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Ref_Create_T]) -> QuantConnect.Util._Typed_Ref_Create[QuantConnect_Util_Ref_Create_T]:
        ...


class _Typed_Ref_CreateReadOnly(typing.Generic[QuantConnect_Util_Ref_CreateReadOnly_T]):
    """"""

    @overload
    def __call__(self, getter: typing.Callable[[], QuantConnect_Util_Ref_CreateReadOnly_T]) -> QuantConnect.Util.IReadOnlyRef[QuantConnect_Util_Ref_CreateReadOnly_T]:
        """Creates a new IReadOnlyRef{T} instance"""
        ...


class _Ref_CreateReadOnly:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_Ref_CreateReadOnly_T]) -> QuantConnect.Util._Typed_Ref_CreateReadOnly[QuantConnect_Util_Ref_CreateReadOnly_T]:
        ...


class Ref(typing.Generic[QuantConnect_Util_Ref_T], System.Object, QuantConnect.Util.IReadOnlyRef[QuantConnect_Util_Ref_T]):
    """Represents a reference to any value, T"""

    @property
    def value(self) -> QuantConnect_Util_Ref_T:
        """Gets or sets the value of this reference"""
        ...

    @value.setter
    def value(self, value: QuantConnect_Util_Ref_T) -> None:
        ...

    create: QuantConnect.Util._Ref_Create

    create_read_only: QuantConnect.Util._Ref_CreateReadOnly

    def __init__(self, getter: typing.Callable[[], QuantConnect_Util_Ref_T], setter: typing.Callable[[QuantConnect_Util_Ref_T], typing.Any]) -> None:
        """
        Initializes a new instance of the Ref{T} class
        
        :param getter: A function delegate to get the current value
        :param setter: A function delegate to set the current value
        """
        ...

    def as_read_only(self) -> QuantConnect.Util.IReadOnlyRef[QuantConnect_Util_Ref_T]:
        """
        Returns a read-only version of this instance
        
        :returns: A new instance with read-only semantics/gaurantees.
        """
        ...


class NullStringValueConverter(typing.Generic[QuantConnect_Util_NullStringValueConverter_T]):
    """
    Converts the string "null" into a new instance of T.
    This converter only handles deserialization concerns.
    """

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param object_type: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The Newtonsoft.Json.JsonReader to read from.
        :param object_type: Type of the object.
        :param existing_value: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The Newtonsoft.Json.JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class OptionPayoff(System.Object):
    """Static class containing useful methods related with options payoff"""

    @staticmethod
    def get_intrinsic_value(underlying_price: float, strike: float, right: QuantConnect.OptionRight) -> float:
        """
        Intrinsic value function of the option
        
        :param underlying_price: The price of the underlying
        :param strike: The strike price of the option
        :param right: The option right of the option, call or put
        :returns: The intrinsic value remains for the option at expiry.
        """
        ...

    @staticmethod
    def get_pay_off(underlying_price: float, strike: float, right: QuantConnect.OptionRight) -> float:
        """
        Option payoff function at expiration time
        
        :param underlying_price: The price of the underlying
        :param strike: The strike price of the option
        :param right: The option right of the option, call or put
        """
        ...


class ComparisonOperatorTypes(IntEnum):
    """Comparison operators"""

    EQUALS = 0
    """Check if their operands are equal"""

    NOT_EQUAL = 1
    """Check if their operands are not equal"""

    GREATER = 2
    """Checks left-hand operand is greater than its right-hand operand"""

    GREATER_OR_EQUAL = 3
    """Checks left-hand operand is greater or equal to its right-hand operand"""

    LESS = 4
    """Checks left-hand operand is less than its right-hand operand"""

    LESS_OR_EQUAL = 5
    """Checks left-hand operand is less or equal to its right-hand operand"""


class _Typed_ComparisonOperator_Compare(typing.Generic[QuantConnect_Util_ComparisonOperator_Compare_T]):
    """"""

    @overload
    def __call__(self, op: QuantConnect.Util.ComparisonOperatorTypes, arg_1: QuantConnect_Util_ComparisonOperator_Compare_T, arg_2: QuantConnect_Util_ComparisonOperator_Compare_T) -> bool:
        """
        Compares two values using given operator
        
        :param op: Comparison operator
        :param arg_1: The first value
        :param arg_2: The second value
        :returns: Returns true if its left-hand operand meets the operator value to its right-hand operand, false otherwise.
        """
        ...


class _ComparisonOperator_Compare:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_ComparisonOperator_Compare_T]) -> QuantConnect.Util._Typed_ComparisonOperator_Compare[QuantConnect_Util_ComparisonOperator_Compare_T]:
        ...


class ComparisonOperator(System.Object):
    """Utility Comparison Operator class"""

    compare: QuantConnect.Util._ComparisonOperator_Compare


class RateGate(System.Object, System.IDisposable):
    """Used to control the rate of some occurrence per unit of time."""

    @property
    def occurrences(self) -> int:
        """Number of occurrences allowed per unit of time."""
        ...

    @property
    def time_unit_milliseconds(self) -> int:
        """The length of the time unit, in milliseconds."""
        ...

    @property
    def is_rate_limited(self) -> bool:
        """Flag indicating we are currently being rate limited"""
        ...

    def __init__(self, occurrences: int, time_unit: datetime.timedelta) -> None:
        """
        Initializes a RateGate with a rate of occurrences
        per time_unit.
        
        :param occurrences: Number of occurrences allowed per unit of time.
        :param time_unit: Length of the time unit.
        """
        ...

    @overload
    def dispose(self) -> None:
        """Releases unmanaged resources held by an instance of this class."""
        ...

    @overload
    def dispose(self, is_disposing: bool) -> None:
        """
        Releases unmanaged resources held by an instance of this class.
        
        
        This Class is protected.
        
        :param is_disposing: Whether this object is being disposed.
        """
        ...

    @overload
    def wait_to_proceed(self, milliseconds_timeout: int) -> bool:
        """
        Blocks the current thread until allowed to proceed or until the
        specified timeout elapses.
        
        :param milliseconds_timeout: Number of milliseconds to wait, or -1 to wait indefinitely.
        :returns: true if the thread is allowed to proceed, or false if timed out.
        """
        ...

    @overload
    def wait_to_proceed(self, timeout: datetime.timedelta) -> bool:
        """
        Blocks the current thread until allowed to proceed or until the
        specified timeout elapses.
        
        :param timeout: 
        :returns: true if the thread is allowed to proceed, or false if timed out.
        """
        ...

    @overload
    def wait_to_proceed(self) -> None:
        """Blocks the current thread indefinitely until allowed to proceed."""
        ...


class _Typed_EnumeratorExtensions_Where(typing.Generic[QuantConnect_Util_EnumeratorExtensions_Where_T]):
    """"""

    @overload
    def __call__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_Where_T], predicate: typing.Callable[[QuantConnect_Util_EnumeratorExtensions_Where_T], bool]) -> System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_Where_T]:
        """Filter the enumerator using the specified predicate"""
        ...


class _EnumeratorExtensions_Where:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_EnumeratorExtensions_Where_T]) -> QuantConnect.Util._Typed_EnumeratorExtensions_Where[QuantConnect_Util_EnumeratorExtensions_Where_T]:
        ...


class _Typed_EnumeratorExtensions_Select(typing.Generic[QuantConnect_Util_EnumeratorExtensions_Select_T]):
    """"""

    @overload
    def __call__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_Select_T], selector: typing.Callable[[QuantConnect_Util_EnumeratorExtensions_Select_T], QuantConnect_Util_EnumeratorExtensions_Select_TResult]) -> System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_Select_TResult]:
        """Project the enumerator using the specified selector"""
        ...


class _EnumeratorExtensions_Select:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_EnumeratorExtensions_Select_T]) -> QuantConnect.Util._Typed_EnumeratorExtensions_Select[QuantConnect_Util_EnumeratorExtensions_Select_T]:
        ...


class _Typed_EnumeratorExtensions_SelectMany(typing.Generic[QuantConnect_Util_EnumeratorExtensions_SelectMany_T]):
    """"""

    @overload
    def __call__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_SelectMany_T], selector: typing.Callable[[QuantConnect_Util_EnumeratorExtensions_SelectMany_T], System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_SelectMany_TResult]]) -> System.Collections.Generic.IEnumerator[QuantConnect_Util_EnumeratorExtensions_SelectMany_TResult]:
        """Project the enumerator using the specified selector"""
        ...


class _EnumeratorExtensions_SelectMany:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_EnumeratorExtensions_SelectMany_T]) -> QuantConnect.Util._Typed_EnumeratorExtensions_SelectMany[QuantConnect_Util_EnumeratorExtensions_SelectMany_T]:
        ...


class EnumeratorExtensions(System.Object):
    """Provides convenience of linq extension methods for IEnumerator{T} types"""

    where: QuantConnect.Util._EnumeratorExtensions_Where

    select: QuantConnect.Util._EnumeratorExtensions_Select

    select_many: QuantConnect.Util._EnumeratorExtensions_SelectMany


class StreamReaderEnumerable(System.Object, typing.Iterable[str], System.IDisposable):
    """Converts a StreamReader into an enumerable of string"""

    @overload
    def __init__(self, stream: System.IO.Stream, *disposables: typing.Union[System.IDisposable, typing.Iterable[System.IDisposable]]) -> None:
        """
        Initializes a new instance of the StreamReaderEnumerable class
        
        :param stream: The stream to be read
        :param disposables: Allows specifying other resources that should be disposed when this instance is disposed
        """
        ...

    @overload
    def __init__(self, reader: System.IO.StreamReader, *disposables: typing.Union[System.IDisposable, typing.Iterable[System.IDisposable]]) -> None:
        """
        Initializes a new instance of the StreamReaderEnumerable class
        
        :param reader: The stream reader instance to convert to an enumerable of string
        :param disposables: Allows specifying other resources that should be disposed when this instance is disposed
        """
        ...

    def __iter__(self) -> typing.Iterator[str]:
        ...

    def dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[str]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...


class BusyBlockingCollection(typing.Generic[QuantConnect_Util_BusyBlockingCollection_T], System.Object, QuantConnect.Interfaces.IBusyCollection[QuantConnect_Util_BusyBlockingCollection_T]):
    """
    A small wrapper around BlockingCollection{T} used to communicate busy state of the items
    being processed
    """

    @property
    def wait_handle(self) -> System.Threading.WaitHandle:
        """
        Gets a wait handle that can be used to wait until this instance is done
        processing all of it's item
        """
        ...

    @property
    def count(self) -> int:
        """Gets the number of items held within this collection"""
        ...

    @property
    def is_busy(self) -> bool:
        """Returns true if processing, false otherwise"""
        ...

    @overload
    def __init__(self) -> None:
        """
        Initializes a new instance of the BusyBlockingCollection{T} class
        with a bounded capacity of int.MaxValue
        """
        ...

    @overload
    def __init__(self, bounded_capacity: int) -> None:
        """
        Initializes a new instance of the BusyBlockingCollection{T} class
        with the specified bounded_capacity
        
        :param bounded_capacity: The maximum number of items allowed in the collection
        """
        ...

    @overload
    def add(self, item: QuantConnect_Util_BusyBlockingCollection_T) -> None:
        """
        Adds the items to this collection
        
        :param item: The item to be added
        """
        ...

    @overload
    def add(self, item: QuantConnect_Util_BusyBlockingCollection_T, cancellation_token: System.Threading.CancellationToken) -> None:
        """
        Adds the items to this collection
        
        :param item: The item to be added
        :param cancellation_token: A cancellation token to observer
        """
        ...

    def complete_adding(self) -> None:
        """Marks the BusyBlockingCollection{T} as not accepting any more additions"""
        ...

    def dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @overload
    def get_consuming_enumerable(self) -> typing.Sequence[QuantConnect_Util_BusyBlockingCollection_T]:
        """
        Provides a consuming enumerable for items in this collection.
        
        :returns: An enumerable that removes and returns items from the collection.
        """
        ...

    @overload
    def get_consuming_enumerable(self, cancellation_token: System.Threading.CancellationToken) -> typing.Sequence[QuantConnect_Util_BusyBlockingCollection_T]:
        """
        Provides a consuming enumerable for items in this collection.
        
        :param cancellation_token: A cancellation token to observer
        :returns: An enumerable that removes and returns items from the collection.
        """
        ...


class _Typed_ObjectActivator_Clone(typing.Generic[QuantConnect_Util_ObjectActivator_Clone_T]):
    """"""

    @overload
    def __call__(self, instance_to_clone: QuantConnect_Util_ObjectActivator_Clone_T) -> QuantConnect_Util_ObjectActivator_Clone_T:
        """Clones the specified instance and then casts it to T before returning"""
        ...


class _ObjectActivator_Clone:
    """"""

    @overload
    def __call__(self, instance_to_clone: typing.Any) -> System.Object:
        """
        Clones the specified instance using reflection
        
        :param instance_to_clone: The instance to be cloned
        :returns: A field/property wise, non-recursive clone of the instance.
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Util_ObjectActivator_Clone_T]) -> QuantConnect.Util._Typed_ObjectActivator_Clone[QuantConnect_Util_ObjectActivator_Clone_T]:
        ...


class ObjectActivator(System.Object):
    """Provides methods for creating new instances of objects"""

    clone: QuantConnect.Util._ObjectActivator_Clone

    @staticmethod
    def add_activator(key: typing.Type, value: typing.Callable[[typing.List[System.Object]], System.Object]) -> None:
        """
        Adds method to return an instance of object
        
        :param key: The key of the method to add
        :param value: The value of the method to add
        """
        ...

    @staticmethod
    def get_activator(data_type: typing.Type) -> typing.Callable[[typing.List[System.Object]], System.Object]:
        """
        Fast Object Creator from Generic Type:
        Modified from http://rogeralsing.com/2008/02/28/linq-expressions-creating-objects/
        
        :param data_type: Type of the object we wish to create
        :returns: Method to return an instance of object.
        """
        ...

    @staticmethod
    def reset_activators() -> None:
        """Reset the object activators"""
        ...


class _Typed_LinqExtensions_ToReadOnlyDictionary(typing.Generic[QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[System.Collections.Generic.KeyValuePair[QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K, QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_V]]) -> typing.Dict[QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K, QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_V]:
        """
        Creates a new read-only dictionary from the key value pairs
        
        :param enumerable: The IEnumerable of KeyValuePair instances to convert to a dictionary
        :returns: A read-only dictionary holding the same data as the enumerable.
        """
        ...


class _LinqExtensions_ToReadOnlyDictionary:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K]) -> QuantConnect.Util._Typed_LinqExtensions_ToReadOnlyDictionary[QuantConnect_Util_LinqExtensions_ToReadOnlyDictionary_K]:
        ...


class _Typed_LinqExtensions_ToHashSet(typing.Generic[QuantConnect_Util_LinqExtensions_ToHashSet_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_ToHashSet_T], selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToHashSet_T], QuantConnect_Util_LinqExtensions_ToHashSet_TResult]) -> System.Collections.Generic.HashSet[QuantConnect_Util_LinqExtensions_ToHashSet_TResult]:
        """
        Creates a new HashSet{T} from the elements in the specified enumerable
        
        :param enumerable: The items to be placed into the enumerable
        :param selector: Selects items from the enumerable to be placed into the HashSet{T}
        :returns: A new HashSet{T} containing the items in the enumerable.
        """
        ...


class _LinqExtensions_ToHashSet:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToHashSet_T]) -> QuantConnect.Util._Typed_LinqExtensions_ToHashSet[QuantConnect_Util_LinqExtensions_ToHashSet_T]:
        ...


class _Typed_LinqExtensions_ToList(typing.Generic[QuantConnect_Util_LinqExtensions_ToList_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_ToList_T], selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToList_T], QuantConnect_Util_LinqExtensions_ToList_TResult]) -> typing.List[QuantConnect_Util_LinqExtensions_ToList_TResult]:
        """
        Creates a new IList{T} from the projected elements in the specified enumerable
        
        :param enumerable: The items to be placed into the list
        :param selector: Selects items from the enumerable to be placed into the List{T}
        :returns: A new List{T} containing the items in the enumerable.
        """
        ...


class _LinqExtensions_ToList:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToList_T]) -> QuantConnect.Util._Typed_LinqExtensions_ToList[QuantConnect_Util_LinqExtensions_ToList_T]:
        ...


class _Typed_LinqExtensions_ToArray(typing.Generic[QuantConnect_Util_LinqExtensions_ToArray_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_ToArray_T], selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToArray_T], QuantConnect_Util_LinqExtensions_ToArray_TResult]) -> typing.List[QuantConnect_Util_LinqExtensions_ToArray_TResult]:
        """
        Creates a new array from the projected elements in the specified enumerable
        
        :param enumerable: The items to be placed into the array
        :param selector: Selects items from the enumerable to be placed into the array
        :returns: A new array containing the items in the enumerable.
        """
        ...


class _LinqExtensions_ToArray:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToArray_T]) -> QuantConnect.Util._Typed_LinqExtensions_ToArray[QuantConnect_Util_LinqExtensions_ToArray_T]:
        ...


class _Typed_LinqExtensions_ToImmutableArray(typing.Generic[QuantConnect_Util_LinqExtensions_ToImmutableArray_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_ToImmutableArray_T], selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToImmutableArray_T], QuantConnect_Util_LinqExtensions_ToImmutableArray_TResult]) -> System.Collections.Immutable.ImmutableArray[QuantConnect_Util_LinqExtensions_ToImmutableArray_TResult]:
        """
        Creates a new immutable array from the projected elements in the specified enumerable
        
        :param enumerable: The items to be placed into the array
        :param selector: Selects items from the enumerable to be placed into the array
        :returns: A new array containing the items in the enumerable.
        """
        ...


class _LinqExtensions_ToImmutableArray:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToImmutableArray_T]) -> QuantConnect.Util._Typed_LinqExtensions_ToImmutableArray[QuantConnect_Util_LinqExtensions_ToImmutableArray_T]:
        ...


class _Typed_LinqExtensions_IsNullOrEmpty(typing.Generic[QuantConnect_Util_LinqExtensions_IsNullOrEmpty_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_IsNullOrEmpty_T]) -> bool:
        """
        Returns true if the specified enumerable is null or has no elements
        
        :param enumerable: The enumerable to check for a value
        :returns: True if the enumerable has elements, false otherwise.
        """
        ...


class _LinqExtensions_IsNullOrEmpty:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_IsNullOrEmpty_T]) -> QuantConnect.Util._Typed_LinqExtensions_IsNullOrEmpty[QuantConnect_Util_LinqExtensions_IsNullOrEmpty_T]:
        ...


class _Typed_LinqExtensions_Median(typing.Generic[QuantConnect_Util_LinqExtensions_Median_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_Median_T]) -> QuantConnect_Util_LinqExtensions_Median_T:
        """
        Gets the median value in the collection
        
        :param enumerable: The enumerable of items to search
        :returns: The median value, throws InvalidOperationException if no items are present.
        """
        ...

    @overload
    def __call__(self, collection: typing.List[QuantConnect_Util_LinqExtensions_Median_T], selector: typing.Callable[[QuantConnect_Util_LinqExtensions_Median_T], QuantConnect_Util_LinqExtensions_Median_TProperty]) -> QuantConnect_Util_LinqExtensions_Median_TProperty:
        """
        Gets the median value in the collection
        
        :param collection: The collection of items to search
        :param selector: Function used to select a value from collection items
        :returns: The median value, throws InvalidOperationException if no items are present.
        """
        ...


class _LinqExtensions_Median:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_Median_T]) -> QuantConnect.Util._Typed_LinqExtensions_Median[QuantConnect_Util_LinqExtensions_Median_T]:
        ...


class _Typed_LinqExtensions_BinarySearch(typing.Generic[QuantConnect_Util_LinqExtensions_BinarySearch_TItem]):
    """"""

    @overload
    def __call__(self, list: typing.List[QuantConnect_Util_LinqExtensions_BinarySearch_TItem], value: QuantConnect_Util_LinqExtensions_BinarySearch_TSearch, comparer: typing.Callable[[QuantConnect_Util_LinqExtensions_BinarySearch_TSearch, QuantConnect_Util_LinqExtensions_BinarySearch_TItem], int]) -> int:
        """
        Performs a binary search on the specified collection.
        
        :param list: The list to be searched.
        :param value: The value to search for.
        :param comparer: The comparer that is used to compare the value with the list items.
        :returns: The index of the item if found, otherwise the bitwise complement where the value should be per MSDN specs.
        """
        ...

    @overload
    def __call__(self, list: typing.List[QuantConnect_Util_LinqExtensions_BinarySearch_TItem], value: QuantConnect_Util_LinqExtensions_BinarySearch_TItem) -> int:
        """
        Performs a binary search on the specified collection.
        
        :param list: The list to be searched.
        :param value: The value to search for.
        :returns: The index of the item if found, otherwise the bitwise complement where the value should be per MSDN specs.
        """
        ...

    @overload
    def __call__(self, list: typing.List[QuantConnect_Util_LinqExtensions_BinarySearch_TItem], value: QuantConnect_Util_LinqExtensions_BinarySearch_TItem, comparer: System.Collections.Generic.IComparer[QuantConnect_Util_LinqExtensions_BinarySearch_TItem]) -> int:
        """
        Performs a binary search on the specified collection.
        
        :param list: The list to be searched.
        :param value: The value to search for.
        :param comparer: The comparer that is used to compare the value with the list items.
        :returns: The index of the item if found, otherwise the bitwise complement where the value should be per MSDN specs.
        """
        ...


class _LinqExtensions_BinarySearch:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_BinarySearch_TItem]) -> QuantConnect.Util._Typed_LinqExtensions_BinarySearch[QuantConnect_Util_LinqExtensions_BinarySearch_TItem]:
        ...


class _Typed_LinqExtensions_Memoize(typing.Generic[QuantConnect_Util_LinqExtensions_Memoize_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_Memoize_T]) -> typing.Sequence[QuantConnect_Util_LinqExtensions_Memoize_T]:
        """
        Wraps the specified enumerable such that it will only be enumerated once
        
        :param enumerable: The source enumerable to be wrapped
        :returns: A new enumerable that can be enumerated multiple times without re-enumerating the source enumerable.
        """
        ...


class _LinqExtensions_Memoize:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_Memoize_T]) -> QuantConnect.Util._Typed_LinqExtensions_Memoize[QuantConnect_Util_LinqExtensions_Memoize_T]:
        ...


class _Typed_LinqExtensions_Range(typing.Generic[QuantConnect_Util_LinqExtensions_Range_T]):
    """"""

    @overload
    def __call__(self, start: QuantConnect_Util_LinqExtensions_Range_T, end: QuantConnect_Util_LinqExtensions_Range_T, incrementer: typing.Callable[[QuantConnect_Util_LinqExtensions_Range_T], QuantConnect_Util_LinqExtensions_Range_T], include_end_point: bool = False) -> typing.Sequence[QuantConnect_Util_LinqExtensions_Range_T]:
        """
        Produces the an enumerable of the range of values between start and end using the specified
        incrementing function
        
        :param start: The start of the range
        :param end: The end of the range, non-inclusive by default
        :param incrementer: The incrementing function, with argument of the current item
        :param include_end_point: True to emit the end point, false otherwise
        :returns: An enumerable of the range of items between start and end.
        """
        ...


class _LinqExtensions_Range:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_Range_T]) -> QuantConnect.Util._Typed_LinqExtensions_Range[QuantConnect_Util_LinqExtensions_Range_T]:
        ...


class _Typed_LinqExtensions_GroupAdjacentBy(typing.Generic[QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T]):
    """"""

    @overload
    def __call__(self, enumerable: typing.List[QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T], grouper: typing.Callable[[QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T, QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T], bool]) -> typing.Sequence[typing.Sequence[QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T]]:
        """
        Groups adjacent elements of the enumerale using the specified grouper function
        
        :param enumerable: The source enumerable to be grouped
        :param grouper: A function that accepts the previous value and the next value and returns
        true if the next value belongs in the same group as the previous value, otherwise returns false
        :returns: A new enumerable of the groups defined by grouper. These groups don't have a key
        and are only grouped by being emitted separately from this enumerable.
        """
        ...


class _LinqExtensions_GroupAdjacentBy:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T]) -> QuantConnect.Util._Typed_LinqExtensions_GroupAdjacentBy[QuantConnect_Util_LinqExtensions_GroupAdjacentBy_T]:
        ...


class _Typed_LinqExtensions_AreDifferent(typing.Generic[QuantConnect_Util_LinqExtensions_AreDifferent_T]):
    """"""

    @overload
    def __call__(self, left: System.Collections.Generic.ISet[QuantConnect_Util_LinqExtensions_AreDifferent_T], right: System.Collections.Generic.ISet[QuantConnect_Util_LinqExtensions_AreDifferent_T]) -> bool:
        """
        Determines if there are any differences between the left and right collections.
        This method uses sets to improve performance and also uses lazy evaluation so if a
        difference is found, true is immediately returned and evaluation is halted.
        
        :param left: The left set
        :param right: The right set
        :returns: True if there are any differences between the two sets, false otherwise.
        """
        ...


class _LinqExtensions_AreDifferent:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_AreDifferent_T]) -> QuantConnect.Util._Typed_LinqExtensions_AreDifferent[QuantConnect_Util_LinqExtensions_AreDifferent_T]:
        ...


class _Typed_LinqExtensions_AsEnumerable(typing.Generic[QuantConnect_Util_LinqExtensions_AsEnumerable_T]):
    """"""

    @overload
    def __call__(self, enumerator: System.Collections.Generic.IEnumerator[QuantConnect_Util_LinqExtensions_AsEnumerable_T]) -> typing.Sequence[QuantConnect_Util_LinqExtensions_AsEnumerable_T]:
        """
        Converts an IEnumerator{T} to an IEnumerable{T}
        
        :param enumerator: The enumerator to convert to an enumerable
        :returns: An enumerable wrapping the specified enumerator.
        """
        ...


class _LinqExtensions_AsEnumerable:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_AsEnumerable_T]) -> QuantConnect.Util._Typed_LinqExtensions_AsEnumerable[QuantConnect_Util_LinqExtensions_AsEnumerable_T]:
        ...


class _Typed_LinqExtensions_GetValueOrDefault(typing.Generic[QuantConnect_Util_LinqExtensions_GetValueOrDefault_K]):
    """"""

    @overload
    def __call__(self, dictionary: System.Collections.Generic.IDictionary[QuantConnect_Util_LinqExtensions_GetValueOrDefault_K, QuantConnect_Util_LinqExtensions_GetValueOrDefault_V], key: QuantConnect_Util_LinqExtensions_GetValueOrDefault_K, default_value: QuantConnect_Util_LinqExtensions_GetValueOrDefault_V = ...) -> QuantConnect_Util_LinqExtensions_GetValueOrDefault_V:
        """
        Gets the value associated with the specified key or provided default value if key is not found.
        
        :param dictionary: The dictionary instance
        :param key: Lookup key
        :param default_value: Default value
        :returns: Value associated with the specified key or  default value.
        """
        ...


class _LinqExtensions_GetValueOrDefault:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_GetValueOrDefault_K]) -> QuantConnect.Util._Typed_LinqExtensions_GetValueOrDefault[QuantConnect_Util_LinqExtensions_GetValueOrDefault_K]:
        ...


class _Typed_LinqExtensions_DoForEach(typing.Generic[QuantConnect_Util_LinqExtensions_DoForEach_T]):
    """"""

    @overload
    def __call__(self, source: typing.List[QuantConnect_Util_LinqExtensions_DoForEach_T], action: typing.Callable[[QuantConnect_Util_LinqExtensions_DoForEach_T], typing.Any]) -> None:
        """
        Performs an action for each element in collection source
        
        :param source: Collection source
        :param action: An action to perform
        """
        ...


class _LinqExtensions_DoForEach:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_DoForEach_T]) -> QuantConnect.Util._Typed_LinqExtensions_DoForEach[QuantConnect_Util_LinqExtensions_DoForEach_T]:
        ...


class _Typed_LinqExtensions_ToReadOnlyExtendedDictionary(typing.Generic[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey]):
    """"""

    @overload
    def __call__(self, dictionary: System.Collections.Generic.IDictionary[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey, QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue]) -> Common.Util.ReadOnlyExtendedDictionary[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey, QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue]:
        """Converts a dictionary to a ReadOnlyExtendedDictionary"""
        ...

    @overload
    def __call__(self, source: typing.List[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue], key_selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue], QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey]) -> Common.Util.ReadOnlyExtendedDictionary[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey, QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TValue]:
        """Creates a ReadOnlyExtendedDictionary from an IEnumerable according to specified key selector"""
        ...


class _LinqExtensions_ToReadOnlyExtendedDictionary:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey]) -> QuantConnect.Util._Typed_LinqExtensions_ToReadOnlyExtendedDictionary[QuantConnect_Util_LinqExtensions_ToReadOnlyExtendedDictionary_TKey]:
        ...


class _Typed_LinqExtensions_ToDataDictionary(typing.Generic[QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource]):
    """"""

    @overload
    def __call__(self, source: typing.List[QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource], key_selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource], QuantConnect.Symbol], value_selector: typing.Callable[[QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource], QuantConnect_Util_LinqExtensions_ToDataDictionary_TValue]) -> QuantConnect.Data.Market.DataDictionary[QuantConnect_Util_LinqExtensions_ToDataDictionary_TValue]:
        """Creates a DataDictionary from an IEnumerable according to specified key and value selectors"""
        ...


class _LinqExtensions_ToDataDictionary:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource]) -> QuantConnect.Util._Typed_LinqExtensions_ToDataDictionary[QuantConnect_Util_LinqExtensions_ToDataDictionary_TSource]:
        ...


class LinqExtensions(System.Object):
    """Provides more extension methods for the enumerable types"""

    to_read_only_dictionary: QuantConnect.Util._LinqExtensions_ToReadOnlyDictionary

    to_hash_set: QuantConnect.Util._LinqExtensions_ToHashSet

    to_list: QuantConnect.Util._LinqExtensions_ToList

    to_array: QuantConnect.Util._LinqExtensions_ToArray

    to_immutable_array: QuantConnect.Util._LinqExtensions_ToImmutableArray

    is_null_or_empty: QuantConnect.Util._LinqExtensions_IsNullOrEmpty

    median: QuantConnect.Util._LinqExtensions_Median

    binary_search: QuantConnect.Util._LinqExtensions_BinarySearch

    memoize: QuantConnect.Util._LinqExtensions_Memoize

    range: QuantConnect.Util._LinqExtensions_Range

    group_adjacent_by: QuantConnect.Util._LinqExtensions_GroupAdjacentBy

    are_different: QuantConnect.Util._LinqExtensions_AreDifferent

    as_enumerable: QuantConnect.Util._LinqExtensions_AsEnumerable

    get_value_or_default: QuantConnect.Util._LinqExtensions_GetValueOrDefault

    do_for_each: QuantConnect.Util._LinqExtensions_DoForEach

    to_read_only_extended_dictionary: QuantConnect.Util._LinqExtensions_ToReadOnlyExtendedDictionary

    to_data_dictionary: QuantConnect.Util._LinqExtensions_ToDataDictionary


class FixedSizeHashQueue(typing.Generic[QuantConnect_Util_FixedSizeHashQueue_T], System.Object, typing.Iterable[QuantConnect_Util_FixedSizeHashQueue_T]):
    """Provides an implementation of an add-only fixed length, unique queue system"""

    def __init__(self, size: int) -> None:
        """
        Initializes a new instance of the FixedSizeHashQueue{T} class
        
        :param size: The maximum number of items to hold
        """
        ...

    def __iter__(self) -> typing.Iterator[QuantConnect_Util_FixedSizeHashQueue_T]:
        ...

    def add(self, item: QuantConnect_Util_FixedSizeHashQueue_T) -> bool:
        """Returns true if the item was added and didn't already exists"""
        ...

    def contains(self, item: QuantConnect_Util_FixedSizeHashQueue_T) -> bool:
        """Returns true if the specified item exists in the collection"""
        ...

    def dequeue(self) -> QuantConnect_Util_FixedSizeHashQueue_T:
        """Dequeues and returns the next item in the queue"""
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect_Util_FixedSizeHashQueue_T]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    def try_peek(self, item: typing.Optional[QuantConnect_Util_FixedSizeHashQueue_T]) -> typing.Tuple[bool, QuantConnect_Util_FixedSizeHashQueue_T]:
        """Tries to inspect the first item in the queue"""
        ...


class SecurityExtensions(System.Object):
    """
    Provides useful infrastructure methods to the Security class.
    These are added in this way to avoid mudding the class's public API
    """

    @staticmethod
    def is_internal_feed(security: QuantConnect.Securities.Security) -> bool:
        """Determines if all subscriptions for the security are internal feeds"""
        ...


class BusyCollection(typing.Generic[QuantConnect_Util_BusyCollection_T], System.Object, QuantConnect.Interfaces.IBusyCollection[QuantConnect_Util_BusyCollection_T]):
    """A non blocking IBusyCollection{T} implementation"""

    @property
    def wait_handle(self) -> System.Threading.WaitHandle:
        """
        Gets a wait handle that can be used to wait until this instance is done
        processing all of it's item
        """
        ...

    @property
    def count(self) -> int:
        """Gets the number of items held within this collection"""
        ...

    @property
    def is_busy(self) -> bool:
        """Returns true if processing, false otherwise"""
        ...

    @overload
    def add(self, item: QuantConnect_Util_BusyCollection_T) -> None:
        """
        Adds the items to this collection
        
        :param item: The item to be added
        """
        ...

    @overload
    def add(self, item: QuantConnect_Util_BusyCollection_T, cancellation_token: System.Threading.CancellationToken) -> None:
        """
        Adds the items to this collection
        
        :param item: The item to be added
        :param cancellation_token: A cancellation token to observer
        """
        ...

    def complete_adding(self) -> None:
        """Marks the collection as not accepting any more additions"""
        ...

    def dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    @overload
    def get_consuming_enumerable(self) -> typing.Sequence[QuantConnect_Util_BusyCollection_T]:
        """
        Provides a consuming enumerable for items in this collection.
        
        :returns: An enumerable that removes and returns items from the collection.
        """
        ...

    @overload
    def get_consuming_enumerable(self, cancellation_token: System.Threading.CancellationToken) -> typing.Sequence[QuantConnect_Util_BusyCollection_T]:
        """
        Provides a consuming enumerable for items in this collection.
        
        :param cancellation_token: A cancellation token to observer
        :returns: An enumerable that removes and returns items from the collection.
        """
        ...


class ListComparer(typing.Generic[QuantConnect_Util_ListComparer_T], System.Object, System.Collections.Generic.IEqualityComparer[typing.Sequence[QuantConnect_Util_ListComparer_T]]):
    """
    An implementation of IEqualityComparer{T} for List{T}.
    Useful when using a List{T} as the key of a collection.
    """

    def equals(self, x: typing.Sequence[QuantConnect_Util_ListComparer_T], y: typing.Sequence[QuantConnect_Util_ListComparer_T]) -> bool:
        """
        Determines whether the specified objects are equal.
        
        :returns: true if the specified objects are equal; otherwise, false.
        """
        ...

    def get_hash_code(self, obj: typing.Sequence[QuantConnect_Util_ListComparer_T]) -> int:
        """
        Returns a hash code for the specified object.
        
        :returns: A hash code for the specified object created from combining the hash
        code of all the elements in the collection.
        """
        ...


class DecimalJsonConverter:
    """Json converter to represent decimals as strings"""

    @property
    def can_write(self) -> bool:
        """Gets a value indicating whether this JsonConverter can write JSON."""
        ...

    def can_convert(self, object_type: typing.Type) -> bool:
        """
        Determines whether this instance can convert the specified object type.
        
        :param object_type: Type of the object.
        :returns: true if this instance can convert the specified object type; otherwise, false.
        """
        ...

    def read_json(self, reader: typing.Any, object_type: typing.Type, existing_value: typing.Any, serializer: typing.Any) -> System.Object:
        """
        Reads the JSON representation of the object.
        
        :param reader: The JsonReader to read from.
        :param object_type: Type of the object.
        :param existing_value: The existing value of object being read.
        :param serializer: The calling serializer.
        :returns: The object value.
        """
        ...

    def write_json(self, writer: typing.Any, value: typing.Any, serializer: typing.Any) -> None:
        """
        Writes the JSON representation of the object.
        
        :param writer: The JsonWriter to write to.
        :param value: The value.
        :param serializer: The calling serializer.
        """
        ...


class _Typed_XElementExtensions_Get(typing.Generic[QuantConnect_Util_XElementExtensions_Get_T]):
    """"""

    @overload
    def __call__(self, element: typing.Any, name: str) -> QuantConnect_Util_XElementExtensions_Get_T:
        """
        Gets the value from the element and converts it to the specified type.
        
        :param element: The element to access
        :param name: The attribute name to access on the element
        :returns: The converted value.
        """
        ...


class _XElementExtensions_Get:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Util_XElementExtensions_Get_T]) -> QuantConnect.Util._Typed_XElementExtensions_Get[QuantConnect_Util_XElementExtensions_Get_T]:
        ...


class XElementExtensions(System.Object):
    """Provides extension methods for the XML to LINQ types"""

    get: QuantConnect.Util._XElementExtensions_Get


class WorkerThread(System.Object, System.IDisposable):
    """
    This worker tread is required to guarantee all python operations are
    executed by the same thread, to enable complete debugging functionality.
    We don't use the main thread, to avoid any chance of blocking the process
    """

    instance: QuantConnect.Util.WorkerThread = ...
    """The worker thread instance"""

    @property
    def finished_work_item(self) -> System.Threading.AutoResetEvent:
        """Will be set when the worker thread finishes a work item"""
        ...

    def __init__(self) -> None:
        """
        Creates a new instance, which internally launches a new worker thread
        
        
        This Class is protected.
        """
        ...

    def add(self, action: typing.Callable[[], typing.Any]) -> None:
        """
        Adds a new item of work
        
        :param action: The work item to add
        """
        ...

    def dispose(self) -> None:
        """Disposes the worker thread."""
        ...


class CashAmountUtil(System.Object):
    """Provides utility methods for working with CashAmount instances"""

    @staticmethod
    def should_add_cash_balance(balance: QuantConnect.Securities.CashAmount, account_currency: str) -> bool:
        """
        Determines if a cash balance should be added to the cash book
        
        :param balance: The cash balance to check
        :param account_currency: The algorithm's account currency
        :returns: True if the balance should be added, false otherwise.
        """
        ...


class _Typed_KeyStringSynchronizer_Execute(typing.Generic[QuantConnect_Util_KeyStringSynchronizer_Execute_T]):
    """"""

    @overload
    def __call__(self, key: str, action: typing.Callable[[], QuantConnect_Util_KeyStringSynchronizer_Execute_T]) -> QuantConnect_Util_KeyStringSynchronizer_Execute_T:
        """
        Execute the given function synchronously with any other thread using the same key
        
        :param key: The synchronization key
        :param action: The function to execute
        """
        ...


class _KeyStringSynchronizer_Execute:
    """"""

    @overload
    def __call__(self, key: str, single_execution: bool, action: typing.Callable[[], typing.Any]) -> None:
        """
        Execute the given action synchronously with any other thread using the same key
        
        :param key: The synchronization key
        :param single_execution: True if execution should happen only once at the same time for multiple threads
        :param action: The action to execute
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Util_KeyStringSynchronizer_Execute_T]) -> QuantConnect.Util._Typed_KeyStringSynchronizer_Execute[QuantConnect_Util_KeyStringSynchronizer_Execute_T]:
        ...


class KeyStringSynchronizer(System.Object):
    """Helper class to synchronize execution based on a string key"""

    @property
    def execute(self) -> QuantConnect.Util._KeyStringSynchronizer_Execute:
        ...


class ConcurrentSet(typing.Generic[QuantConnect_Util_ConcurrentSet_T], System.Object, System.Collections.Generic.ISet[QuantConnect_Util_ConcurrentSet_T], typing.Iterable[QuantConnect_Util_ConcurrentSet_T]):
    """
    Provides a thread-safe set collection that mimics the behavior of HashSet{T}
    and will be keep insertion order
    """

    @property
    def count(self) -> int:
        """Gets the number of elements contained in the System.Collections.Generic.ICollection`1."""
        ...

    @property
    def is_read_only(self) -> bool:
        """Gets a value indicating whether the System.Collections.Generic.ICollection`1 is read-only."""
        ...

    def __iter__(self) -> typing.Iterator[QuantConnect_Util_ConcurrentSet_T]:
        ...

    def __len__(self) -> int:
        ...

    def add(self, item: QuantConnect_Util_ConcurrentSet_T) -> bool:
        """
        Adds an element to the current set and returns a value to indicate if the element was successfully added.
        
        :param item: The element to add to the set.
        :returns: true if the element is added to the set; false if the element is already in the set.
        """
        ...

    def clear(self) -> None:
        """Removes all items from the System.Collections.Generic.ICollection`1."""
        ...

    def contains(self, item: QuantConnect_Util_ConcurrentSet_T) -> bool:
        """
        Determines whether the System.Collections.Generic.ICollection`1 contains a specific value.
        
        :param item: The object to locate in the System.Collections.Generic.ICollection`1.
        :returns: true if item is found in the System.Collections.Generic.ICollection`1; otherwise, false.
        """
        ...

    def copy_to(self, array: typing.List[QuantConnect_Util_ConcurrentSet_T], array_index: int) -> None:
        """
        Copies the elements of the System.Collections.Generic.ICollection`1 to an System.Array, starting at a particular System.Array index.
        
        :param array: The one-dimensional System.Array that is the destination of the elements copied from System.Collections.Generic.ICollection`1. The System.Array must have zero-based indexing.
        :param array_index: The zero-based index in array at which copying begins.
        """
        ...

    def except_with(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> None:
        """
        Removes all elements in the specified collection from the current set.
        
        :param other: The collection of items to remove from the set.
        """
        ...

    def get_enumerator(self) -> System.Collections.Generic.IEnumerator[QuantConnect_Util_ConcurrentSet_T]:
        """
        Returns an enumerator that iterates through the collection.
        
        :returns: A System.Collections.Generic.IEnumerator`1 that can be used to iterate through the collection.
        """
        ...

    def intersect_with(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> None:
        """
        Modifies the current set so that it contains only elements that are also in a specified collection.
        
        :param other: The collection to compare to the current set.
        """
        ...

    def is_proper_subset_of(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> bool:
        """
        Determines whether the current set is a proper (strict) subset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is a proper subset of other; otherwise, false.
        """
        ...

    def is_proper_superset_of(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> bool:
        """
        Determines whether the current set is a proper (strict) superset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is a proper superset of other; otherwise, false.
        """
        ...

    def is_subset_of(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> bool:
        """
        Determines whether a set is a subset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is a subset of other; otherwise, false.
        """
        ...

    def is_superset_of(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> bool:
        """
        Determines whether the current set is a superset of a specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is a superset of other; otherwise, false.
        """
        ...

    def overlaps(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> bool:
        """
        Determines whether the current set overlaps with the specified collection.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set and other share at least one common element; otherwise, false.
        """
        ...

    def remove(self, item: QuantConnect_Util_ConcurrentSet_T) -> bool:
        """
        Removes the first occurrence of a specific object from the System.Collections.Generic.ICollection`1.
        
        :param item: The object to remove from the System.Collections.Generic.ICollection`1.
        :returns: true if item was successfully removed from the System.Collections.Generic.ICollection`1; otherwise, false. This method also returns false if item is not found in the original System.Collections.Generic.ICollection`1.
        """
        ...

    def set_equals(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> bool:
        """
        Determines whether the current set and the specified collection contain the same elements.
        
        :param other: The collection to compare to the current set.
        :returns: true if the current set is equal to other; otherwise, false.
        """
        ...

    def symmetric_except_with(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> None:
        """
        Modifies the current set so that it contains only elements that are present either in the current set or in the specified collection, but not both.
        
        :param other: The collection to compare to the current set.
        """
        ...

    def union_with(self, other: typing.List[QuantConnect_Util_ConcurrentSet_T]) -> None:
        """
        Modifies the current set so that it contains all elements that are present in either the current set or the specified collection.
        
        :param other: The collection to compare to the current set.
        """
        ...


class ReferenceWrapper(typing.Generic[QuantConnect_Util_ReferenceWrapper_T], System.Object):
    """
    We wrap a T instance, a value type, with a class, a reference type, to achieve thread safety when assigning new values
    and reading from multiple threads. This is possible because assignments are atomic operations in C# for reference types (among others).
    """

    @property
    def value(self) -> QuantConnect_Util_ReferenceWrapper_T:
        """The current value"""
        ...

    def __init__(self, value: QuantConnect_Util_ReferenceWrapper_T) -> None:
        """
        Creates a new instance
        
        :param value: The value to use
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Util__EventContainer_Callable, QuantConnect_Util__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Util__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Util__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Util__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


