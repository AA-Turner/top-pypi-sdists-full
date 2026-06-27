from typing import overload
from enum import IntEnum
import datetime
import typing

import QuantConnect
import QuantConnect.Algorithm.Framework.Portfolio.SignalExports
import QuantConnect.Benchmarks
import QuantConnect.Brokerages
import QuantConnect.Commands
import QuantConnect.Data
import QuantConnect.Data.Consolidators
import QuantConnect.Data.Market
import QuantConnect.Indicators
import QuantConnect.Interfaces
import QuantConnect.Orders
import QuantConnect.Orders.Fees
import QuantConnect.Orders.Fills
import QuantConnect.Orders.Slippage
import QuantConnect.Python
import QuantConnect.Securities
import QuantConnect.Securities.Option
import QuantConnect.Securities.Volatility
import System
import System.Collections.Generic
import pandas

QuantConnect_Python_BasePythonWrapper = typing.Any

QuantConnect_Python_BasePythonWrapper_TInterface = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_TInterface")
QuantConnect_Python__EventContainer_Callable = typing.TypeVar("QuantConnect_Python__EventContainer_Callable")
QuantConnect_Python__EventContainer_ReturnType = typing.TypeVar("QuantConnect_Python__EventContainer_ReturnType")
QuantConnect_Python_PandasConverter_GetDataFrame_T = typing.TypeVar("QuantConnect_Python_PandasConverter_GetDataFrame_T")
QuantConnect_Python_PandasConverter_ConcatDataFrames_T = typing.TypeVar("QuantConnect_Python_PandasConverter_ConcatDataFrames_T")
QuantConnect_Python_PythonWrapper_ValidateImplementationOf_TInterface = typing.TypeVar("QuantConnect_Python_PythonWrapper_ValidateImplementationOf_TInterface")
QuantConnect_Python_PythonWrapper_InvokeMethod_T = typing.TypeVar("QuantConnect_Python_PythonWrapper_InvokeMethod_T")
QuantConnect_Python_PythonWrapper_Invoke_T = typing.TypeVar("QuantConnect_Python_PythonWrapper_Invoke_T")
QuantConnect_Python_BasePythonWrapper_GetProperty_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_GetProperty_T")
QuantConnect_Python_BasePythonWrapper_InvokeMethod_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethod_T")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_T")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TKey = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TKey")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TValue = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TValue")
QuantConnect_Python_BasePythonWrapper_InvokeMethodWithOutParameters_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodWithOutParameters_T")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T")
QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T")
QuantConnect_Python_BasePythonWrapper_InvokeMethod_PythonRuntimeChecker_TResult = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethod_PythonRuntimeChecker_TResult")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_PythonRuntimeChecker_TItem = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_PythonRuntimeChecker_TItem")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TKey = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TKey")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TValue = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TValue")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult")
QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetOutParameters_PythonRuntimeChecker_TResult = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetOutParameters_PythonRuntimeChecker_TResult")
QuantConnect_Python_BasePythonWrapper_Convert_PythonRuntimeChecker_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_Convert_PythonRuntimeChecker_T")
QuantConnect_Python_BasePythonWrapper_ConvertAndDispose_PythonRuntimeChecker_T = typing.TypeVar("QuantConnect_Python_BasePythonWrapper_ConvertAndDispose_PythonRuntimeChecker_T")


class BenchmarkPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Benchmarks.IBenchmark], QuantConnect.Benchmarks.IBenchmark):
    """Provides an implementation of IBenchmark that wraps a PyObject object"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the BenchmarkPythonWrapper class with wrapped PyObject object
        
        :param model: Python benchmark model
        """
        ...

    def evaluate(self, time: typing.Union[datetime.datetime, datetime.date]) -> float:
        """
        Evaluates this benchmark at the specified time using the method defined in the Python class
        
        :param time: The time to evaluate the benchmark at
        :returns: The value of the benchmark at the specified time.
        """
        ...


class PythonData(QuantConnect.Data.DynamicData):
    """
    Dynamic data class for Python algorithms.
    Stores properties of python instances in DynamicData dictionary
    """

    @property
    def end_time(self) -> datetime.datetime:
        """
        The end time of this data. Some data covers spans (trade bars)
        and as such we want to know the entire time span covered
        """
        ...

    @end_time.setter
    def end_time(self, value: datetime.datetime) -> None:
        ...

    def __getitem__(self, index: str) -> typing.Any:
        """
        Indexes into this PythonData, where index is key to the dynamic property
        
        :param index: the index
        :returns: Dynamic property of a given index.
        """
        ...

    @overload
    def __init__(self, python_data: typing.Any) -> None:
        """
        Constructor for initializing the PythonData class with wrapped PyObject
        
        :param python_data: 
        """
        ...

    @overload
    def __init__(self) -> None:
        """Constructor for initializing the PythonData class"""
        ...

    def __setitem__(self, index: str, value: typing.Any) -> None:
        """
        Indexes into this PythonData, where index is key to the dynamic property
        
        :param index: the index
        :returns: Dynamic property of a given index.
        """
        ...

    def default_resolution(self) -> QuantConnect.Resolution:
        """Gets the default resolution for this data and security type"""
        ...

    def get_source(self, config: QuantConnect.Data.SubscriptionDataConfig, date: datetime.datetime, is_live_mode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Source Locator for algorithm written in Python.
        
        :param config: Subscription configuration object
        :param date: Date of the data file we're looking for
        :param is_live_mode: true if we're in live mode, false for backtesting mode
        :returns: STRING API Url.
        """
        ...

    def is_of_type(self, type: typing.Type) -> bool:
        """
        Helper method to determine if the current instance is of the provided type
        
        :param type: Target type to check against
        :returns: True if this instance is of the provided type.
        """
        ...

    def is_sparse_data(self) -> bool:
        """
        Indicates that the data set is expected to be sparse
        
        :returns: True if the data set represented by this type is expected to be sparse.
        """
        ...

    def reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: datetime.datetime, is_live_mode: bool) -> QuantConnect.Data.BaseData:
        """
        Generic Reader Implementation for Python Custom Data.
        
        :param config: Subscription configuration
        :param line: CSV line of data from the source
        :param date: Date of the requested line
        :param is_live_mode: true if we're in live mode, false for backtesting mode
        """
        ...

    def requires_mapping(self) -> bool:
        """
        Indicates if there is support for mapping
        
        :returns: True indicates mapping should be used.
        """
        ...

    def supported_resolutions(self) -> typing.List[QuantConnect.Resolution]:
        """Gets the supported resolution for this data and security type"""
        ...


class PandasNonExpandableAttribute(System.Attribute):
    """
    Attribute to mark a class, field or property as non-expandable by the pandas converter.
    The instance will be added to the dataframe as it is, without unwrapping its fields and properties into columns.
    """


class CommandPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Commands.Command]):
    """Python wrapper for a python defined command type"""

    def __init__(self, type: typing.Type, data: str = None) -> None:
        """
        Constructor for initialising the CommandPythonWrapper class with wrapped PyObject object
        
        :param type: Python command type
        :param data: Command data
        """
        ...

    def run(self, algorithm: QuantConnect.Interfaces.IAlgorithm) -> typing.Optional[bool]:
        """
        Run this command using the target algorithm
        
        :param algorithm: The algorithm instance
        :returns: True if success, false otherwise. Returning null will disable command feedback.
        """
        ...

    @staticmethod
    def serialize(command: typing.Any) -> str:
        """Helper method to serialize a command instance"""
        ...


class PythonInitializer(System.Object):
    """Helper class for Python initialization"""

    @staticmethod
    def activate_python_virtual_environment(path_to_virtual_env: str) -> bool:
        """
        "Activate" a virtual Python environment by prepending its library storage to Pythons
        path. This allows the libraries in this venv to be selected prior to our base install.
        Requires PYTHONNET_PYDLL to be set to base install.
        """
        ...

    @staticmethod
    def add_algorithm_location_path(algorithm_location: str) -> None:
        """
        Adds the algorithm location to the python path.
        This will make sure that add_python_paths keeps the algorithm location path
        at the beginning of the pythonpath.
        """
        ...

    @staticmethod
    def add_python_paths(paths: typing.List[str]) -> bool:
        """Adds directories to the python path at runtime"""
        ...

    @staticmethod
    def initialize(begin_allow_threads: bool = True) -> None:
        """
        Initialize python.
        
        In some cases, we might not need to call BeginAllowThreads, like when we're running
        in a python or non-threaded environment.
        In those cases, we can set the begin_allow_threads parameter to false.
        """
        ...

    @staticmethod
    def reset_algorithm_location_path() -> None:
        """Resets the algorithm location path so another can be set"""
        ...

    @staticmethod
    def shutdown() -> None:
        """Shutdown python"""
        ...


class _Typed_PandasConverter_GetDataFrame(typing.Generic[QuantConnect_Python_PandasConverter_GetDataFrame_T]):
    """"""

    @overload
    def __call__(self, data: typing.List[QuantConnect_Python_PandasConverter_GetDataFrame_T], symbol_only_index: bool = False, force_multi_value_symbol: bool = False, flatten: bool = False) -> pandas.DataFrame:
        """
        Converts an enumerable of IBaseData in a pandas.DataFrame
        
        :param data: Enumerable of Slice
        :param symbol_only_index: Whether to make the index only the symbol, without time or any other index levels
        :param force_multi_value_symbol: Useful when the data contains points for multiple symbols.
        If false and symbol_only_index is true, it will assume there is a single point for each symbol,
        and will apply performance improvements for the data frame generation.
        :param flatten: Whether to flatten collections into rows and columns
        :returns: PyObject containing a pandas.DataFrame.
        """
        ...


class _PandasConverter_GetDataFrame:
    """"""

    @overload
    def __call__(self, data: typing.List[QuantConnect.Data.Slice], flatten: bool = False, data_type: typing.Type = None) -> pandas.DataFrame:
        """
        Converts an enumerable of Slice in a pandas.DataFrame
        
        :param data: Enumerable of Slice
        :param flatten: Whether to flatten collections into rows and columns
        :param data_type: Optional type of bars to add to the data frame
        If true, the base data items time will be ignored and only the base data collection time will be used in the index
        :returns: PyObject containing a pandas.DataFrame.
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Python_PandasConverter_GetDataFrame_T]) -> QuantConnect.Python._Typed_PandasConverter_GetDataFrame[QuantConnect_Python_PandasConverter_GetDataFrame_T]:
        ...


class _Typed_PandasConverter_ConcatDataFrames(typing.Generic[QuantConnect_Python_PandasConverter_ConcatDataFrames_T]):
    """"""

    @overload
    def __call__(self, data_frames: typing.List[typing.Any], keys: typing.List[QuantConnect_Python_PandasConverter_ConcatDataFrames_T], names: typing.List[str], sort: bool = True, dropna: bool = True) -> typing.Any:
        """
        Concatenates multiple data frames
        
        :param data_frames: The data frames to concatenate
        :param keys: Optional new keys for a new multi-index level that would be added
        to index each individual data frame in the resulting one
        :param names: The optional names of the new index level (and the existing ones if they need to be changed)
        :param sort: Whether to sort the resulting data frame
        :param dropna: Whether to drop columns containing NA values only (Nan, None, etc)
        :returns: A new data frame result from concatenating the input.
        """
        ...


class _PandasConverter_ConcatDataFrames:
    """"""

    @overload
    def __call__(self, data_frames: typing.List[typing.Any], sort: bool = True, dropna: bool = True) -> typing.Any:
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Python_PandasConverter_ConcatDataFrames_T]) -> QuantConnect.Python._Typed_PandasConverter_ConcatDataFrames[QuantConnect_Python_PandasConverter_ConcatDataFrames_T]:
        ...


class PandasConverter(System.Object):
    """This class has no documentation."""

    @property
    def get_data_frame(self) -> QuantConnect.Python._PandasConverter_GetDataFrame:
        ...

    concat_data_frames: QuantConnect.Python._PandasConverter_ConcatDataFrames

    @overload
    def get_indicator_data_frame(self, data: typing.Any) -> pandas.DataFrame:
        """
        Converts a dictionary with a list of IndicatorDataPoint in a pandas.DataFrame
        
        :param data: PyObject that should be a dictionary (convertible to PyDict) of string to list of IndicatorDataPoint
        :returns: PyObject containing a pandas.DataFrame.
        """
        ...

    @overload
    def get_indicator_data_frame(self, data: typing.List[System.Collections.Generic.KeyValuePair[str, typing.List[QuantConnect.Indicators.IndicatorDataPoint]]], extra_data: typing.List[System.Collections.Generic.KeyValuePair[str, typing.List[System.ValueTuple[datetime.datetime, System.Object]]]] = None) -> pandas.DataFrame:
        """
        Converts a dictionary with a list of IndicatorDataPoint in a pandas.DataFrame
        
        :param data: Dictionary with a list of IndicatorDataPoint
        :param extra_data: Optional dynamic properties to include in the DataFrame.
        :returns: PyObject containing a pandas.DataFrame.
        """
        ...

    def to_string(self) -> str:
        """Returns a string that represent the current object"""
        ...


class MarginCallModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Securities.IMarginCallModel], QuantConnect.Securities.IMarginCallModel):
    """Provides a margin call model that wraps a PyObject object that represents the model responsible for picking which orders should be executed during a margin call"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the MarginCallModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents the model responsible for picking which orders should be executed during a margin call
        """
        ...

    def execute_margin_call(self, generated_margin_call_orders: typing.List[QuantConnect.Orders.SubmitOrderRequest]) -> typing.List[QuantConnect.Orders.OrderTicket]:
        """
        Executes synchronous orders to bring the account within margin requirements.
        
        :param generated_margin_call_orders: These are the margin call orders that were generated
        by individual security margin models.
        :returns: The list of orders that were actually executed.
        """
        ...

    def get_margin_call_orders(self, issue_margin_call_warning: typing.Optional[bool]) -> typing.Tuple[typing.List[QuantConnect.Orders.SubmitOrderRequest], bool]:
        """
        Scan the portfolio and the updated data for a potential margin call situation which may get the holdings below zero!
        If there is a margin call, liquidate the portfolio immediately before the portfolio gets sub zero.
        
        :param issue_margin_call_warning: Set to true if a warning should be issued to the algorithm
        :returns: True for a margin call on the holdings.
        """
        ...


class PythonActivator(System.Object):
    """Provides methods for creating new instances of python custom data objects"""

    @property
    def type(self) -> typing.Type:
        """System.Type of the object we wish to create"""
        ...

    @property
    def factory(self) -> typing.Callable[[typing.List[System.Object]], System.Object]:
        """Method to return an instance of object"""
        ...

    def __init__(self, type: typing.Type, value: typing.Any) -> None:
        """
        Creates a new instance of PythonActivator
        
        :param type: System.Type of the object we wish to create
        :param value: PyObject that contains the python type
        """
        ...


class DataConsolidatorPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Data.Consolidators.IDataConsolidator], QuantConnect.Data.Consolidators.IDataConsolidator):
    """Provides an Data Consolidator that wraps a PyObject object that represents a custom Python consolidator"""

    @property
    def consolidated(self) -> QuantConnect.Data.IBaseData:
        """
        Gets the most recently consolidated piece of data. This will be null if this consolidator
        has not produced any data yet.
        """
        ...

    @property
    def working_data(self) -> QuantConnect.Data.IBaseData:
        """Gets a clone of the data being currently consolidated"""
        ...

    @property
    def input_type(self) -> typing.Type:
        """Gets the type consumed by this consolidator"""
        ...

    @property
    def output_type(self) -> typing.Type:
        """Gets the type produced by this consolidator"""
        ...

    @property
    def data_consolidated(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Data.IBaseData], typing.Any], typing.Any]:
        """Event handler that fires when a new piece of data is produced"""
        ...

    @data_consolidated.setter
    def data_consolidated(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Data.IBaseData], typing.Any], typing.Any]) -> None:
        ...

    def __init__(self, consolidator: typing.Any) -> None:
        """
        Constructor for initialising the DataConsolidatorPythonWrapper class with wrapped PyObject object
        
        :param consolidator: Represents a custom python consolidator
        """
        ...

    def dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def reset(self) -> None:
        """Resets the consolidator"""
        ...

    def scan(self, current_local_time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Scans this consolidator to see if it should emit a bar due to time passing
        
        :param current_local_time: The current time in the local time zone (same as BaseData.time)
        """
        ...

    def update(self, data: QuantConnect.Data.IBaseData) -> None:
        """
        Updates this consolidator with the specified data
        
        :param data: The new data for the consolidator
        """
        ...


class PandasIgnoreAttribute(System.Attribute):
    """
    Attribute to mark a property or field as ignored when converting an instance to a pandas DataFrame row.
    No column will be created for this property or field.
    """


class BuyingPowerModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Securities.IBuyingPowerModel], QuantConnect.Securities.IBuyingPowerModel):
    """Wraps a PyObject object that represents a security's model of buying power"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initializing the BuyingPowerModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a security's model of buying power
        """
        ...

    def get_buying_power(self, parameters: QuantConnect.Securities.BuyingPowerParameters) -> QuantConnect.Securities.BuyingPower:
        """
        Gets the buying power available for a trade
        
        :param parameters: A parameters object containing the algorithm's potrfolio, security, and order direction
        :returns: The buying power available for the trade.
        """
        ...

    def get_initial_margin_required_for_order(self, parameters: QuantConnect.Securities.InitialMarginRequiredForOrderParameters) -> QuantConnect.Securities.InitialMargin:
        """
        Gets the total margin required to execute the specified order in units of the account currency including fees
        
        :param parameters: An object containing the portfolio, the security and the order
        :returns: The total margin in terms of the currency quoted in the order.
        """
        ...

    def get_initial_margin_requirement(self, parameters: QuantConnect.Securities.InitialMarginParameters) -> QuantConnect.Securities.InitialMargin:
        """
        The margin that must be held in order to increase the position by the provided quantity
        
        :param parameters: An object containing the security and quantity
        :returns: The initial margin required for the provided security and quantity.
        """
        ...

    def get_leverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the current leverage of the security
        
        :param security: The security to get leverage for
        :returns: The current leverage in the security.
        """
        ...

    def get_maintenance_margin(self, parameters: QuantConnect.Securities.MaintenanceMarginParameters) -> QuantConnect.Securities.MaintenanceMargin:
        """
        Gets the margin currently allocated to the specified holding
        
        :param parameters: An object containing the security
        :returns: The maintenance margin required for the provided holdings quantity/cost/value.
        """
        ...

    def get_maximum_order_quantity_for_delta_buying_power(self, parameters: QuantConnect.Securities.GetMaximumOrderQuantityForDeltaBuyingPowerParameters) -> QuantConnect.Securities.GetMaximumOrderQuantityResult:
        """
        Get the maximum market order quantity to obtain a delta in the buying power used by a security.
        The deltas sign defines the position side to apply it to, positive long, negative short.
        
        :param parameters: An object containing the portfolio, the security and the delta buying power
        :returns: Returns the maximum allowed market order quantity and if zero, also the reason.
        """
        ...

    def get_maximum_order_quantity_for_target_buying_power(self, parameters: QuantConnect.Securities.GetMaximumOrderQuantityForTargetBuyingPowerParameters) -> QuantConnect.Securities.GetMaximumOrderQuantityResult:
        """
        Get the maximum market order quantity to obtain a position with a given buying power percentage.
        Will not take into account free buying power.
        
        :param parameters: An object containing the portfolio, the security and the target signed buying power percentage
        :returns: Returns the maximum allowed market order quantity and if zero, also the reason.
        """
        ...

    def get_reserved_buying_power_for_position(self, parameters: QuantConnect.Securities.ReservedBuyingPowerForPositionParameters) -> QuantConnect.Securities.ReservedBuyingPowerForPosition:
        """
        Gets the amount of buying power reserved to maintain the specified position
        
        :param parameters: A parameters object containing the security
        :returns: The reserved buying power in account currency.
        """
        ...

    def has_sufficient_buying_power_for_order(self, parameters: QuantConnect.Securities.HasSufficientBuyingPowerForOrderParameters) -> QuantConnect.Securities.HasSufficientBuyingPowerForOrderResult:
        """
        Check if there is sufficient buying power to execute this order.
        
        :param parameters: An object containing the portfolio, the security and the order
        :returns: Returns buying power information for an order.
        """
        ...

    def set_leverage(self, security: QuantConnect.Securities.Security, leverage: float) -> None:
        """
        Sets the leverage for the applicable securities, i.e, equities
        
        :param security: The security to set leverage for
        :param leverage: The new leverage
        """
        ...


class PandasIgnoreMembersAttribute(System.Attribute):
    """Attribute to indicate the pandas converter to ignore all members of the class when converting an instance to a pandas DataFrame row."""


class FeeModelPythonWrapper(QuantConnect.Orders.Fees.FeeModel):
    """Provides an order fee model that wraps a PyObject object that represents a model that simulates order fees"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the FeeModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a model that simulates order fees
        """
        ...

    def get_order_fee(self, parameters: QuantConnect.Orders.Fees.OrderFeeParameters) -> QuantConnect.Orders.Fees.OrderFee:
        """
        Get the fee for this order
        
        :param parameters: A OrderFeeParameters object
        containing the security and order
        :returns: The cost of the order in units of the account currency.
        """
        ...


class SlippageModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Orders.Slippage.ISlippageModel], QuantConnect.Orders.Slippage.ISlippageModel):
    """Wraps a PyObject object that represents a model that simulates market order slippage"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the SlippageModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a model that simulates market order slippage
        """
        ...

    def get_slippage_approximation(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> float:
        """
        Slippage Model. Return a decimal cash slippage approximation on the order.
        
        :param asset: The security matching the order
        :param order: The order to compute slippage for
        :returns: The slippage of the order in units of the account currency.
        """
        ...


class PandasData(System.Object):
    """This class has no documentation."""

    @property
    def is_custom_data(self) -> bool:
        """Gets true if this is a custom data request, false for normal QC data"""
        ...

    @property
    def levels(self) -> int:
        """Implied levels of a multi index pandas.Series (depends on the security type)"""
        ...

    def __init__(self, data: typing.Any, time_as_column: bool = False) -> None:
        """Initializes an instance of PandasData"""
        ...

    @overload
    def add(self, data: typing.Any) -> None:
        """
        Adds security data object to the end of the lists
        
        :param data: IBaseData object that contains security data
        """
        ...

    @overload
    def add(self, trade_bar: QuantConnect.Data.Market.TradeBar, quote_bar: QuantConnect.Data.Market.QuoteBar) -> None:
        """
        Adds Lean data objects to the end of the lists
        
        :param trade_bar: TradeBar object that contains trade bar information of the security
        :param quote_bar: QuoteBar object that contains quote bar information of the security
        """
        ...

    @overload
    def to_pandas_data_frame(self, levels: int = 2, filter_missing_value_columns: bool = True) -> pandas.DataFrame:
        """
        Get the pandas.DataFrame of the current PandasData state
        
        :param levels: Number of levels of the multi index
        :param filter_missing_value_columns: If false, make sure columns with "missing" values only are still added to the dataframe
        :returns: pandas.DataFrame object.
        """
        ...

    @staticmethod
    @overload
    def to_pandas_data_frame(pandas_datas: typing.List[QuantConnect.Python.PandasData], skip_times_column: bool = False) -> typing.Any:
        """Helper method to create a single pandas data frame indexed by symbol"""
        ...


class _Typed_PythonWrapper_ValidateImplementationOf(typing.Generic[QuantConnect_Python_PythonWrapper_ValidateImplementationOf_TInterface]):
    """"""

    @overload
    def __call__(self, model: typing.Any) -> typing.Any:
        """
        Validates that the specified PyObject completely implements the provided interface type
        
        :param model: The model implementing the interface type
        """
        ...


class _PythonWrapper_ValidateImplementationOf:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_PythonWrapper_ValidateImplementationOf_TInterface]) -> QuantConnect.Python._Typed_PythonWrapper_ValidateImplementationOf[QuantConnect_Python_PythonWrapper_ValidateImplementationOf_TInterface]:
        ...


class _Typed_PythonWrapper_InvokeMethod(typing.Generic[QuantConnect_Python_PythonWrapper_InvokeMethod_T]):
    """"""

    @overload
    def __call__(self, model: typing.Any, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> QuantConnect_Python_PythonWrapper_InvokeMethod_T:
        """
        Invokes the specified method on the provided PyObject instance with the specified arguments
        
        :param model: The PyObject instance
        :param method_name: The name of the method to invoke
        :param args: The arguments to call the method with
        :returns: The return value of the called method converted into the t type.
        """
        ...


class _PythonWrapper_InvokeMethod:
    """"""

    @overload
    def __call__(self, model: typing.Any, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> None:
        """
        Invokes the specified method on the provided PyObject instance with the specified arguments
        
        :param model: The PyObject instance
        :param method_name: The name of the method to invoke
        :param args: The arguments to call the method with
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Python_PythonWrapper_InvokeMethod_T]) -> QuantConnect.Python._Typed_PythonWrapper_InvokeMethod[QuantConnect_Python_PythonWrapper_InvokeMethod_T]:
        ...


class _Typed_PythonWrapper_Invoke(typing.Generic[QuantConnect_Python_PythonWrapper_Invoke_T]):
    """"""

    @overload
    def __call__(self, method: typing.Any, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> QuantConnect_Python_PythonWrapper_Invoke_T:
        """
        Invokes the given PyObject method with the specified arguments
        
        :param method: The method to invoke
        :param args: The arguments to call the method with
        :returns: The return value of the called method converted into the t type.
        """
        ...


class _PythonWrapper_Invoke:
    """"""

    @overload
    def __call__(self, method: typing.Any, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Any:
        """
        Invokes the given PyObject method with the specified arguments
        
        :param method: The method to invoke
        :param args: The arguments to call the method with
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Python_PythonWrapper_Invoke_T]) -> QuantConnect.Python._Typed_PythonWrapper_Invoke[QuantConnect_Python_PythonWrapper_Invoke_T]:
        ...


class PythonWrapper(System.Object):
    """Provides extension methods for managing python wrapper classes"""

    validate_implementation_of: QuantConnect.Python._PythonWrapper_ValidateImplementationOf

    invoke_method: QuantConnect.Python._PythonWrapper_InvokeMethod

    invoke: QuantConnect.Python._PythonWrapper_Invoke


class VolatilityModelPythonWrapper(QuantConnect.Securities.Volatility.BaseVolatilityModel):
    """Provides a volatility model that wraps a PyObject object that represents a model that computes the volatility of a security"""

    @property
    def volatility(self) -> float:
        """Gets the volatility of the security as a percentage"""
        ...

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the VolatilityModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a model that computes the volatility of a security
        """
        ...

    def get_history_requirements(self, security: QuantConnect.Securities.Security, utc_time: typing.Union[datetime.datetime, datetime.date]) -> typing.Sequence[QuantConnect.Data.HistoryRequest]:
        """
        Returns history requirements for the volatility model expressed in the form of history request
        
        :param security: The security of the request
        :param utc_time: The date/time of the request
        :returns: History request object list, or empty if no requirements.
        """
        ...

    def set_subscription_data_config_provider(self, subscription_data_config_provider: QuantConnect.Interfaces.ISubscriptionDataConfigProvider) -> None:
        """
        Sets the ISubscriptionDataConfigProvider instance to use.
        
        :param subscription_data_config_provider: Provides access to registered SubscriptionDataConfig
        """
        ...

    def update(self, security: QuantConnect.Securities.Security, data: QuantConnect.Data.BaseData) -> None:
        """
        Updates this model using the new price information in
        the specified security instance
        
        :param security: The security to calculate volatility for
        :param data: The new data used to update the model
        """
        ...


class PythonConsolidator(System.Object, QuantConnect.Data.Consolidators.IDataConsolidator):
    """Provides a base class for python consolidators, necessary to use event handler."""

    @property
    def consolidated(self) -> QuantConnect.Data.IBaseData:
        """
        Gets the most recently consolidated piece of data. This will be null if this consolidator
        has not produced any data yet.
        """
        ...

    @consolidated.setter
    def consolidated(self, value: QuantConnect.Data.IBaseData) -> None:
        ...

    @property
    def working_data(self) -> QuantConnect.Data.IBaseData:
        """Gets a clone of the data being currently consolidated"""
        ...

    @working_data.setter
    def working_data(self, value: QuantConnect.Data.IBaseData) -> None:
        ...

    @property
    def input_type(self) -> typing.Type:
        """Gets the type consumed by this consolidator"""
        ...

    @input_type.setter
    def input_type(self, value: typing.Type) -> None:
        ...

    @property
    def output_type(self) -> typing.Type:
        """Gets the type produced by this consolidator"""
        ...

    @output_type.setter
    def output_type(self, value: typing.Type) -> None:
        ...

    @property
    def data_consolidated(self) -> _EventContainer[typing.Callable[[System.Object, QuantConnect.Data.IBaseData], typing.Any], typing.Any]:
        """Event handler that fires when a new piece of data is produced"""
        ...

    @data_consolidated.setter
    def data_consolidated(self, value: _EventContainer[typing.Callable[[System.Object, QuantConnect.Data.IBaseData], typing.Any], typing.Any]) -> None:
        ...

    def dispose(self) -> None:
        ...

    def on_data_consolidated(self, consolidator: typing.Any, data: QuantConnect.Data.IBaseData) -> None:
        """
        Function to invoke the event handler
        
        :param consolidator: Reference to the consolidator itself
        :param data: The finished data from the consolidator
        """
        ...

    def reset(self) -> None:
        """Resets the consolidator"""
        ...

    def scan(self, current_local_time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Scans this consolidator to see if it should emit a bar due to time passing
        
        :param current_local_time: The current time in the local time zone (same as BaseData.time)
        """
        ...

    def update(self, data: QuantConnect.Data.IBaseData) -> None:
        """
        Updates this consolidator with the specified data
        
        :param data: The new data for the consolidator
        """
        ...


class BrokerageModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Brokerages.IBrokerageModel], QuantConnect.Brokerages.IBrokerageModel):
    """Provides an implementation of IBrokerageModel that wraps a PyObject object"""

    @property
    def account_type(self) -> QuantConnect.AccountType:
        """Gets or sets the account type used by this model"""
        ...

    @property
    def required_free_buying_power_percent(self) -> float:
        """
        Gets the brokerages model percentage factor used to determine the required unused buying power for the account.
        From 1 to 0. Example: 0 means no unused buying power is required. 0.5 means 50% of the buying power should be left unused.
        """
        ...

    @property
    def default_markets(self) -> typing.Dict[QuantConnect.SecurityType, str]:
        """Gets a map of the default markets to be used for each security type"""
        ...

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the BrokerageModelPythonWrapper class with wrapped PyObject object
        
        :param model: Models brokerage transactions, fees, and order
        """
        ...

    def apply_split(self, tickets: typing.List[QuantConnect.Orders.OrderTicket], split: QuantConnect.Data.Market.Split) -> None:
        """
        Applies the split to the specified order ticket
        
        :param tickets: The open tickets matching the split event
        :param split: The split event data
        """
        ...

    def can_execute_order(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order) -> bool:
        """
        Returns true if the brokerage would be able to execute this order at this time assuming
        market prices are sufficient for the fill to take place. This is used to emulate the
        brokerage fills in backtesting and paper trading. For example some brokerages may not perform
        executions during extended market hours. This is not intended to be checking whether or not
        the exchange is open, that is handled in the Security.Exchange property.
        
        :param security: The security being ordered
        :param order: The order to test for execution
        :returns: True if the brokerage would be able to perform the execution, false otherwise.
        """
        ...

    def can_submit_order(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Tuple[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage could accept this order. This takes into account
        order type, security type, and order size limits.
        
        :param security: The security being ordered
        :param order: The order to be processed
        :param message: If this function returns false, a brokerage message detailing why the order may not be submitted
        :returns: True if the brokerage could process the order, false otherwise.
        """
        ...

    def can_update_order(self, security: QuantConnect.Securities.Security, order: QuantConnect.Orders.Order, request: QuantConnect.Orders.UpdateOrderRequest, message: typing.Optional[QuantConnect.Brokerages.BrokerageMessageEvent]) -> typing.Tuple[bool, QuantConnect.Brokerages.BrokerageMessageEvent]:
        """
        Returns true if the brokerage would allow updating the order as specified by the request
        
        :param security: The security of the order
        :param order: The order to be updated
        :param request: The requested updated to be made to the order
        :param message: If this function returns false, a brokerage message detailing why the order may not be updated
        :returns: True if the brokerage would allow updating the order, false otherwise.
        """
        ...

    def get_benchmark(self, securities: QuantConnect.Securities.SecurityManager) -> QuantConnect.Benchmarks.IBenchmark:
        """
        Get the benchmark for this model
        
        :param securities: SecurityService to create the security with if needed
        :returns: The benchmark for this brokerage.
        """
        ...

    def get_buying_power_model(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.IBuyingPowerModel:
        """
        Gets a new buying power model for the security, returning the default model with the security's configured leverage.
        For cash accounts, leverage = 1 is used.
        
        :param security: The security to get a buying power model for
        :returns: The buying power model for this brokerage/security.
        """
        ...

    def get_fee_model(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fees.IFeeModel:
        """
        Gets a new fee model that represents this brokerage's fee structure
        
        :param security: The security to get a fee model for
        :returns: The new fee model for this brokerage.
        """
        ...

    def get_fill_model(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Fills.IFillModel:
        """
        Gets a new fill model that represents this brokerage's fill behavior
        
        :param security: The security to get fill model for
        :returns: The new fill model for this brokerage.
        """
        ...

    def get_leverage(self, security: QuantConnect.Securities.Security) -> float:
        """
        Gets the brokerage's leverage for the specified security
        
        :param security: The security's whose leverage we seek
        :returns: The leverage for the specified security.
        """
        ...

    def get_margin_interest_rate_model(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.IMarginInterestRateModel:
        """
        Gets a new margin interest rate model for the security
        
        :param security: The security to get a margin interest rate model for
        :returns: The margin interest rate model for this brokerage.
        """
        ...

    def get_model(self) -> QuantConnect.Brokerages.IBrokerageModel:
        """
        Convenience method to get the underlying IBrokerageModel object from the wrapper.
        
        :returns: Underlying IBrokerageModel object.
        """
        ...

    def get_settlement_model(self, security: QuantConnect.Securities.Security) -> QuantConnect.Securities.ISettlementModel:
        """
        Gets a new settlement model for the security
        
        :param security: The security to get a settlement model for
        :returns: The settlement model for this brokerage.
        """
        ...

    def get_shortable_provider(self, security: QuantConnect.Securities.Security) -> QuantConnect.Interfaces.IShortableProvider:
        """
        Gets the shortable provider
        
        :returns: Shortable provider.
        """
        ...

    def get_slippage_model(self, security: QuantConnect.Securities.Security) -> QuantConnect.Orders.Slippage.ISlippageModel:
        """
        Gets a new slippage model that represents this brokerage's fill slippage behavior
        
        :param security: The security to get a slippage model for
        :returns: The new slippage model for this brokerage.
        """
        ...

    def shortable(self, algorithm: QuantConnect.Interfaces.IAlgorithm, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], quantity: float) -> bool:
        """
        Determine if this symbol is shortable
        
        :param algorithm: The algorithm running
        :param symbol: The symbol to short
        :param quantity: The amount to short
        """
        ...


class PandasColumnAttribute(System.Attribute):
    """Attribute to rename a property or field when converting an instance to a pandas DataFrame row."""

    @property
    def name(self) -> str:
        """The name of the column in the pandas DataFrame."""
        ...

    def __init__(self, name: str) -> None:
        """
        Initializes a new instance of the PandasColumnAttribute class.
        
        :param name: The name of the column in the pandas DataFrame
        """
        ...


class SettlementModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Securities.ISettlementModel], QuantConnect.Securities.ISettlementModel):
    """Provides an implementation of ISettlementModel that wraps a PyObject object"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the SettlementModelPythonWrapper class with wrapped PyObject object
        
        :param model: Settlement Python Model
        """
        ...

    def apply_funds(self, apply_funds_parameters: QuantConnect.Securities.ApplyFundsSettlementModelParameters) -> None:
        """
        Applies cash settlement rules using the method defined in the Python class
        
        :param apply_funds_parameters: The funds application parameters
        """
        ...

    def get_unsettled_cash(self) -> QuantConnect.Securities.CashAmount:
        """Gets the unsettled cash amount for the security"""
        ...

    def scan(self, settlement_parameters: QuantConnect.Securities.ScanSettlementModelParameters) -> None:
        """
        Scan for pending settlements using the method defined in the Python class
        
        :param settlement_parameters: The settlement parameters
        """
        ...


class RiskFreeInterestRateModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Data.IRiskFreeInterestRateModel], QuantConnect.Data.IRiskFreeInterestRateModel):
    """Wraps a PyObject object that represents a risk-free interest rate model"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initializing the RiskFreeInterestRateModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a security's model of buying power
        """
        ...

    @staticmethod
    def from_py_object(model: typing.Any) -> QuantConnect.Data.IRiskFreeInterestRateModel:
        """
        Converts a PyObject object into a IRiskFreeInterestRateModel object, wrapping it if necessary
        
        :param model: The Python model
        :returns: The converted IRiskFreeInterestRateModel instance.
        """
        ...

    def get_interest_rate(self, date: typing.Union[datetime.datetime, datetime.date]) -> float:
        """
        Get interest rate by a given date
        
        :param date: The date
        :returns: Interest rate on the given date.
        """
        ...


class MarginInterestRateModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Securities.IMarginInterestRateModel], QuantConnect.Securities.IMarginInterestRateModel):
    """Wraps a PyObject object that represents a security's margin interest rate model"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initializing the MarginInterestRateModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a security's model of buying power
        """
        ...

    def apply_margin_interest_rate(self, margin_interest_rate_parameters: QuantConnect.Securities.MarginInterestRateParameters) -> None:
        """
        Apply margin interest rates to the portfolio
        
        :param margin_interest_rate_parameters: The parameters to use
        """
        ...


class SignalExportTargetPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Interfaces.ISignalExportTarget], QuantConnect.Interfaces.ISignalExportTarget):
    """Provides an implementation of ISignalExportTarget that wraps a PyObject object"""

    def __init__(self, instance: typing.Any) -> None:
        """
        Constructor for initialising the SignalExportTargetPythonWrapper class with wrapped PyObject object
        
        :param instance: The underlying python instance
        """
        ...

    def dispose(self) -> None:
        """Performs application-defined tasks associated with freeing, releasing, or resetting unmanaged resources."""
        ...

    def send(self, parameters: QuantConnect.Algorithm.Framework.Portfolio.SignalExports.SignalExportTargetParameters) -> bool:
        """Interface to send positions holdings to different 3rd party API's"""
        ...


class _Typed_BasePythonWrapper_GetProperty(typing.Generic[QuantConnect_Python_BasePythonWrapper_GetProperty_T]):
    """"""

    @overload
    def __call__(self, property_name: str) -> QuantConnect_Python_BasePythonWrapper_GetProperty_T:
        """
        Gets the Python instance property with the specified name
        
        :param property_name: The name of the property
        """
        ...


class _BasePythonWrapper_GetProperty:
    """"""

    @overload
    def __call__(self, property_name: str) -> typing.Any:
        """
        Gets the Python instance property with the specified name
        
        :param property_name: The name of the property
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_GetProperty_T]) -> QuantConnect.Python._Typed_BasePythonWrapper_GetProperty[QuantConnect_Python_BasePythonWrapper_GetProperty_T]:
        ...


class _Typed_BasePythonWrapper_InvokeMethod(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethod_T]):
    """"""

    @overload
    def __call__(self, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> QuantConnect_Python_BasePythonWrapper_InvokeMethod_T:
        """
        Invokes the specified method with the specified arguments
        
        :param method_name: The name of the method
        :param args: The arguments to call the method with
        :returns: The returned valued converted to the given type.
        """
        ...


class _BasePythonWrapper_InvokeMethod:
    """"""

    @overload
    def __call__(self, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Any:
        """
        Invokes the specified method with the specified arguments
        
        :param method_name: The name of the method
        :param args: The arguments to call the method with
        """
        ...

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethod_T]) -> QuantConnect.Python._Typed_BasePythonWrapper_InvokeMethod[QuantConnect_Python_BasePythonWrapper_InvokeMethod_T]:
        ...


class _Typed_BasePythonWrapper_InvokeMethodAndEnumerate(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_T]):
    """"""

    @overload
    def __call__(self, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Sequence[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_T]:
        """
        Invokes the specified method with the specified arguments and iterates over the returned values
        
        :param method_name: The name of the method
        :param args: The arguments to call the method with
        :returns: The returned valued converted to the given type.
        """
        ...


class _BasePythonWrapper_InvokeMethodAndEnumerate:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_T]) -> QuantConnect.Python._Typed_BasePythonWrapper_InvokeMethodAndEnumerate[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_T]:
        ...


class _Typed_BasePythonWrapper_InvokeMethodAndGetDictionary(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TKey]):
    """"""

    @overload
    def __call__(self, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> System.Collections.Generic.Dictionary[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TKey, QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TValue]:
        """
        Invokes the specified method with the specified arguments and iterates over the returned values
        
        :param method_name: The name of the method
        :param args: The arguments to call the method with
        :returns: The returned valued converted to the given type.
        """
        ...


class _BasePythonWrapper_InvokeMethodAndGetDictionary:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TKey]) -> QuantConnect.Python._Typed_BasePythonWrapper_InvokeMethodAndGetDictionary[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_TKey]:
        ...


class _Typed_BasePythonWrapper_InvokeMethodWithOutParameters(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodWithOutParameters_T]):
    """"""

    @overload
    def __call__(self, method_name: str, out_parameters_types: typing.List[typing.Type], out_parameters: typing.Optional[typing.List[System.Object]], *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Tuple[QuantConnect_Python_BasePythonWrapper_InvokeMethodWithOutParameters_T, typing.List[System.Object]]:
        """
        Invokes the specified method with the specified arguments and out parameters
        
        :param method_name: The name of the method
        :param out_parameters_types: The types of the out parameters
        :param out_parameters: The out parameters values
        :param args: The arguments to call the method with
        :returns: The returned valued converted to the given type.
        """
        ...


class _BasePythonWrapper_InvokeMethodWithOutParameters:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodWithOutParameters_T]) -> QuantConnect.Python._Typed_BasePythonWrapper_InvokeMethodWithOutParameters[QuantConnect_Python_BasePythonWrapper_InvokeMethodWithOutParameters_T]:
        ...


class _Typed_BasePythonWrapper_InvokeMethodAndWrapResult(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T]):
    """"""

    @overload
    def __call__(self, method_name: str, wrap_result: typing.Callable[[typing.Any], QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T], *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T:
        """
        Invokes the specified method with the specified arguments and wraps the result
        by calling the given function if the result is not a C# object
        
        :param method_name: The name of the method
        :param wrap_result: Method that wraps a Python object in the corresponding Python Wrapper
        :param args: The arguments to call the method with
        :returns: The returned value wrapped using the given method if the result is not a C# object.
        """
        ...


class _BasePythonWrapper_InvokeMethodAndWrapResult:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T]) -> QuantConnect.Python._Typed_BasePythonWrapper_InvokeMethodAndWrapResult[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_T]:
        ...


class _Typed_BasePythonWrapper_TryInvokePythonOverride(typing.Generic[QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T]):
    """"""

    @overload
    def __call__(self, method_name: str, result: typing.Optional[QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T], *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Tuple[bool, QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T]:
        """
        Attempts to invoke the method if it has been overridden in Python.
        
        
        This Class is protected.
        
        :param method_name: The name of the method to call on the Python instance.
        :param result: When this method returns, contains the method result if the call succeeded.
        :param args: The arguments to pass to the Python method.
        :returns: true if the Python method was successfully invoked, otherwise, false.
        """
        ...


class _BasePythonWrapper_TryInvokePythonOverride:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T]) -> QuantConnect.Python._Typed_BasePythonWrapper_TryInvokePythonOverride[QuantConnect_Python_BasePythonWrapper_TryInvokePythonOverride_T]:
        ...


class BasePythonWrapper(typing.Generic[QuantConnect_Python_BasePythonWrapper_TInterface], System.Object, System.IEquatable[QuantConnect_Python_BasePythonWrapper], System.IDisposable):
    """Base class for Python wrapper classes"""

    class PythonRuntimeChecker(System.Object):
        """Set of helper methods to invoke Python methods with runtime checks for return values and out parameter's conversions."""

        invoke_method: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_InvokeMethod

        invoke_method_and_enumerate: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndEnumerate

        invoke_method_and_get_dictionary: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndGetDictionary

        invoke_method_and_wrap_result: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndWrapResult

        invoke_method_and_get_out_parameters: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndGetOutParameters

        convert: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_Convert

        convert_and_dispose: QuantConnect.Python._BasePythonWrapper.PythonRuntimeChecker_ConvertAndDispose

    @property
    def instance(self) -> typing.Any:
        """
        Gets the underlying python instance
        
        
        This Property is protected.
        """
        ...

    @property
    def get_property(self) -> QuantConnect.Python._BasePythonWrapper_GetProperty:
        ...

    @property
    def invoke_method(self) -> QuantConnect.Python._BasePythonWrapper_InvokeMethod:
        ...

    @property
    def invoke_method_and_enumerate(self) -> QuantConnect.Python._BasePythonWrapper_InvokeMethodAndEnumerate:
        ...

    @property
    def invoke_method_and_get_dictionary(self) -> QuantConnect.Python._BasePythonWrapper_InvokeMethodAndGetDictionary:
        ...

    @property
    def invoke_method_with_out_parameters(self) -> QuantConnect.Python._BasePythonWrapper_InvokeMethodWithOutParameters:
        ...

    @property
    def invoke_method_and_wrap_result(self) -> QuantConnect.Python._BasePythonWrapper_InvokeMethodAndWrapResult:
        ...

    @property
    def try_invoke_python_override(self) -> QuantConnect.Python._BasePythonWrapper_TryInvokePythonOverride:
        ...

    @overload
    def __init__(self, instance: typing.Any, validate_interface: bool = True) -> None:
        """
        Creates a new instance of the BasePythonWrapper{TInterface} class with the specified instance
        
        :param instance: The underlying python instance
        :param validate_interface: Whether to perform validations for interface implementation
        """
        ...

    @overload
    def __init__(self, validate_interface: bool = True) -> None:
        """
        Creates a new instance of the BasePythonWrapper{TInterface} class
        
        :param validate_interface: Whether to perform validations for interface implementation
        """
        ...

    def dispose(self) -> None:
        """Dispose of this instance"""
        ...

    @overload
    def equals(self, other: QuantConnect.Python.BasePythonWrapper[QuantConnect_Python_BasePythonWrapper_TInterface]) -> bool:
        """
        Determines whether the specified instance wraps the same Python object reference as this instance,
        which would indicate that they are equal.
        
        :param other: The other object to compare this with
        :returns: True if both instances are equal, that is if both wrap the same Python object reference.
        """
        ...

    @overload
    def equals(self, obj: typing.Any) -> bool:
        """
        Determines whether the specified object is an instance of BasePythonWrapper{TInterface}
        and wraps the same Python object reference as this instance, which would indicate that they are equal.
        
        :param obj: The other object to compare this with
        :returns: True if both instances are equal, that is if both wrap the same Python object reference.
        """
        ...

    def get_event(self, name: str) -> typing.Any:
        """
        Gets the Python instance event with the specified name
        
        :param name: The name of the event
        """
        ...

    def get_hash_code(self) -> int:
        """
        Gets the hash code for the current instance
        
        :returns: The hash code of the current instance.
        """
        ...

    def get_method(self, method_name: str, python_only: bool = False) -> typing.Any:
        """
        Gets the Python instances method with the specified name and caches it
        
        :param method_name: The name of the method
        :param python_only: Whether to only return python methods
        :returns: The matched method.
        """
        ...

    def has_attr(self, name: str) -> bool:
        """
        Determines whether the Python instance has the specified attribute
        
        :param name: The attribute name
        :returns: Whether the Python instance has the specified attribute.
        """
        ...

    def invoke_void_method(self, method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> None:
        """
        Invokes the specified method with the specified arguments without returning a value
        
        :param method_name: The name of the method
        :param args: The arguments to call the method with
        """
        ...

    def set_property(self, property_name: str, value: typing.Any) -> None:
        """
        Sets the Python instance property with the specified name
        
        :param property_name: The name of the property
        :param value: The property value
        """
        ...

    @overload
    def set_python_instance(self, instance: typing.Any) -> None:
        """
        Sets the python instance
        
        :param instance: The underlying python instance
        """
        ...

    @overload
    def set_python_instance(self, instance: typing.Any, validate_interface: bool) -> None:
        """
        Sets the python instance and sets the validate interface flag
        
        
        This Class is protected.
        
        :param instance: The underlying python instance
        :param validate_interface: Whether to perform validations for interface implementation
        """
        ...


class OptionAssignmentModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Securities.Option.IOptionAssignmentModel], QuantConnect.Securities.Option.IOptionAssignmentModel):
    """Python wrapper for custom option assignment models"""

    def __init__(self, model: typing.Any) -> None:
        """
        Creates a new instance
        
        :param model: The python model to wrapp
        """
        ...

    def get_assignment(self, parameters: QuantConnect.Securities.Option.OptionAssignmentParameters) -> QuantConnect.Securities.Option.OptionAssignmentResult:
        """
        Get's the option assignments to generate if any
        
        :param parameters: The option assignment parameters data transfer class
        :returns: The option assignment result.
        """
        ...


class FillModelPythonWrapper(QuantConnect.Orders.Fills.FillModel):
    """Wraps a PyObject object that represents a model that simulates order fill events"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the FillModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a model that simulates order fill events
        """
        ...

    def combo_leg_limit_fill(self, order: QuantConnect.Orders.Order, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> typing.List[QuantConnect.Orders.OrderEvent]:
        """
        Default combo limit fill model for the base security class. Fills at the limit price for each leg
        
        :param order: Order to fill
        :param parameters: Fill parameters for the order
        :returns: Order fill information detailing the average price and quantity filled for each leg. If any of the fills fails, none of the orders will be filled and the returned list will be empty.
        """
        ...

    def combo_limit_fill(self, order: QuantConnect.Orders.Order, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> typing.List[QuantConnect.Orders.OrderEvent]:
        """
        Default combo limit fill model for the base security class. Fills at the sum of prices for the assets of every leg.
        
        :param order: Order to fill
        :param parameters: Fill parameters for the order
        :returns: Order fill information detailing the average price and quantity filled for each leg. If any of the fills fails, none of the orders will be filled and the returned list will be empty.
        """
        ...

    def combo_market_fill(self, order: QuantConnect.Orders.Order, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> typing.List[QuantConnect.Orders.OrderEvent]:
        """
        Default combo market fill model for the base security class. Fills at the last traded price for each leg.
        
        :param order: Order to fill
        :param parameters: Fill parameters for the order
        :returns: Order fill information detailing the average price and quantity filled for each leg. If any of the fills fails, none of the orders will be filled and the returned list will be empty.
        """
        ...

    def fill(self, parameters: QuantConnect.Orders.Fills.FillModelParameters) -> QuantConnect.Orders.Fills.Fill:
        """
        Return an order event with the fill details
        
        :param parameters: A parameters object containing the security and order
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def get_prices(self, asset: QuantConnect.Securities.Security, direction: QuantConnect.Orders.OrderDirection) -> QuantConnect.Orders.Fills.Prices:
        """
        Get the minimum and maximum price for this security in the last bar:
        
        
        This Class is protected.
        
        :param asset: Security asset we're checking
        :param direction: The order direction, decides whether to pick bid or ask
        """
        ...

    def limit_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.LimitOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Limit Fill Model. Return an order event with the fill details.
        
        :param asset: Stock Object to use to help model limit fill
        :param order: Order to fill. Alter the values directly if filled.
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def limit_if_touched_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.LimitIfTouchedOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Limit if Touched Fill Model. Return an order event with the fill details.
        
        :param asset: Asset we're trading this order
        :param order: LimitIfTouchedOrder Order to Check, return filled if true
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def market_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Model the slippage on a market order: fixed percentage of order price
        
        :param asset: Asset we're trading this order
        :param order: Order to update
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def market_on_close_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOnCloseOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Market on Close Fill Model. Return an order event with the fill details
        
        :param asset: Asset we're trading with this order
        :param order: Order to be filled
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def market_on_open_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.MarketOnOpenOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Market on Open Fill Model. Return an order event with the fill details
        
        :param asset: Asset we're trading with this order
        :param order: Order to be filled
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def stop_limit_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.StopLimitOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Stop Limit Fill Model. Return an order event with the fill details.
        
        :param asset: Asset we're trading this order
        :param order: Stop Limit Order to Check, return filled if true
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def stop_market_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.StopMarketOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Stop Market Fill Model. Return an order event with the fill details.
        
        :param asset: Asset we're trading this order
        :param order: Trailing Stop Order to check, return filled if true
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...

    def trailing_stop_fill(self, asset: QuantConnect.Securities.Security, order: QuantConnect.Orders.TrailingStopOrder) -> QuantConnect.Orders.OrderEvent:
        """
        Trailing Stop Fill Model. Return an order event with the fill details.
        
        :param asset: Asset we're trading this order
        :param order: Stop Order to Check, return filled if true
        :returns: Order fill information detailing the average price and quantity filled.
        """
        ...


class DividendYieldModelPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Data.IDividendYieldModel], QuantConnect.Data.IDividendYieldModel):
    """Wraps a PyObject object that represents a dividend yield model"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initializing the DividendYieldModelPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a security's model of dividend yield
        """
        ...

    @staticmethod
    def from_py_object(model: typing.Any) -> QuantConnect.Data.IDividendYieldModel:
        """
        Converts a PyObject object into a IDividendYieldModel object, wrapping it if necessary
        
        :param model: The Python model
        :returns: The converted IDividendYieldModel instance.
        """
        ...

    @overload
    def get_dividend_yield(self, date: typing.Union[datetime.datetime, datetime.date]) -> float:
        """
        Get dividend yield by a given date of a given symbol
        
        :param date: The date
        :returns: Dividend yield on the given date of the given symbol.
        """
        ...

    @overload
    def get_dividend_yield(self, date: typing.Union[datetime.datetime, datetime.date], security_price: float) -> float:
        """
        Get dividend yield at given date and security price
        
        :param date: The date
        :param security_price: The security price at the given date
        :returns: Dividend yield on the given date of the given symbol.
        """
        ...


class BrokerageMessageHandlerPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Brokerages.IBrokerageMessageHandler], QuantConnect.Brokerages.IBrokerageMessageHandler):
    """Provides a wrapper for IBrokerageMessageHandler implementations written in python"""

    def __init__(self, model: typing.Any) -> None:
        """
        Initializes a new instance of the BrokerageMessageHandlerPythonWrapper class
        
        :param model: The python implementation of IBrokerageMessageHandler
        """
        ...

    def handle_message(self, message: QuantConnect.Brokerages.BrokerageMessageEvent) -> None:
        """
        Handles the message
        
        :param message: The message to be handled
        """
        ...

    def handle_order(self, event_args: QuantConnect.Brokerages.NewBrokerageOrderNotificationEventArgs) -> bool:
        """
        Handles a new order placed manually in the brokerage side
        
        :param event_args: The new order event
        :returns: Whether the order should be added to the transaction handler.
        """
        ...


class SecurityInitializerPythonWrapper(QuantConnect.Python.BasePythonWrapper[QuantConnect.Securities.ISecurityInitializer], QuantConnect.Securities.ISecurityInitializer):
    """Wraps a PyObject object that represents a type capable of initializing a new security"""

    def __init__(self, model: typing.Any) -> None:
        """
        Constructor for initialising the SecurityInitializerPythonWrapper class with wrapped PyObject object
        
        :param model: Represents a type capable of initializing a new security
        """
        ...

    def initialize(self, security: QuantConnect.Securities.Security) -> None:
        """
        Initializes the specified security
        
        :param security: The security to be initialized
        """
        ...


class _EventContainer(typing.Generic[QuantConnect_Python__EventContainer_Callable, QuantConnect_Python__EventContainer_ReturnType]):
    """This class is used to provide accurate autocomplete on events and cannot be imported."""

    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> QuantConnect_Python__EventContainer_ReturnType:
        """Fires the event."""
        ...

    def __iadd__(self, item: QuantConnect_Python__EventContainer_Callable) -> typing.Self:
        """Registers an event handler."""
        ...

    def __isub__(self, item: QuantConnect_Python__EventContainer_Callable) -> typing.Self:
        """Unregisters an event handler."""
        ...


class PythonRuntimeChecker_InvokeMethod:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethod_PythonRuntimeChecker_TResult]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_InvokeMethod[QuantConnect_Python_BasePythonWrapper_InvokeMethod_PythonRuntimeChecker_TResult]:
        ...


class PythonRuntimeChecker_InvokeMethod(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethod_PythonRuntimeChecker_TResult]):
    """"""

    @overload
    def __call__(self, method: typing.Any, python_method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> QuantConnect_Python_BasePythonWrapper_InvokeMethod_PythonRuntimeChecker_TResult:
        """Invokes method method and converts the returned value to type t_result"""
        ...


class PythonRuntimeChecker_InvokeMethodAndEnumerate:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_PythonRuntimeChecker_TItem]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndEnumerate[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_PythonRuntimeChecker_TItem]:
        ...


class PythonRuntimeChecker_InvokeMethodAndEnumerate(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_PythonRuntimeChecker_TItem]):
    """"""

    @overload
    def __call__(self, method: typing.Any, python_method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Sequence[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndEnumerate_PythonRuntimeChecker_TItem]:
        """
        Invokes method method, expecting an enumerable or generator as return value,
        converting each item to type t_item on demand.
        """
        ...


class PythonRuntimeChecker_InvokeMethodAndGetDictionary:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TKey]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndGetDictionary[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TKey]:
        ...


class PythonRuntimeChecker_InvokeMethodAndGetDictionary(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TKey]):
    """"""

    @overload
    def __call__(self, method: typing.Any, python_method_name: str, *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> System.Collections.Generic.Dictionary[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TKey, QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetDictionary_PythonRuntimeChecker_TValue]:
        """
        Invokes method method, expecting a dictionary as return value,
        which then will be converted to a managed dictionary, with type checking on each item conversion.
        """
        ...


class PythonRuntimeChecker_InvokeMethodAndWrapResult:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndWrapResult[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult]:
        ...


class PythonRuntimeChecker_InvokeMethodAndWrapResult(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult]):
    """"""

    @overload
    def __call__(self, method: typing.Any, python_method_name: str, wrap_result: typing.Callable[[typing.Any], QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult], *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> QuantConnect_Python_BasePythonWrapper_InvokeMethodAndWrapResult_PythonRuntimeChecker_TResult:
        """
        Invokes method method and tries to convert the returned value to type t_result.
        If conversion is not possible, the returned PyObject is passed to the provided wrap_result method,
        which should try to do the proper conversion, wrapping or handling of the PyObject.
        """
        ...


class PythonRuntimeChecker_InvokeMethodAndGetOutParameters:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetOutParameters_PythonRuntimeChecker_TResult]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_InvokeMethodAndGetOutParameters[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetOutParameters_PythonRuntimeChecker_TResult]:
        ...


class PythonRuntimeChecker_InvokeMethodAndGetOutParameters(typing.Generic[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetOutParameters_PythonRuntimeChecker_TResult]):
    """"""

    @overload
    def __call__(self, method: typing.Any, python_method_name: str, out_parameters_types: typing.List[typing.Type], out_parameters: typing.Optional[typing.List[System.Object]], *args: typing.Union[System.Object, typing.Iterable[System.Object]]) -> typing.Tuple[QuantConnect_Python_BasePythonWrapper_InvokeMethodAndGetOutParameters_PythonRuntimeChecker_TResult, typing.List[System.Object]]:
        """
        Invokes method method and converts the returned value to type t_result.
        It also makes sure the Python method returns values for the out parameters, converting them into the expected types
        in out_parameters_types and placing them in the out_parameters array.
        """
        ...


class PythonRuntimeChecker_Convert:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_Convert_PythonRuntimeChecker_T]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_Convert[QuantConnect_Python_BasePythonWrapper_Convert_PythonRuntimeChecker_T]:
        ...


class PythonRuntimeChecker_Convert(typing.Generic[QuantConnect_Python_BasePythonWrapper_Convert_PythonRuntimeChecker_T]):
    """"""

    @overload
    def __call__(self, py_object: typing.Any, python_name: str, is_method: bool = True) -> QuantConnect_Python_BasePythonWrapper_Convert_PythonRuntimeChecker_T:
        """
        Converts the given PyObject into the provided t type,
        generating an exception with a user-friendly message if conversion is not possible.
        """
        ...


class PythonRuntimeChecker_ConvertAndDispose:
    """"""

    def __getitem__(self, type: typing.Type[QuantConnect_Python_BasePythonWrapper_ConvertAndDispose_PythonRuntimeChecker_T]) -> QuantConnect.Python._Typed_BasePythonWrapper.PythonRuntimeChecker_ConvertAndDispose[QuantConnect_Python_BasePythonWrapper_ConvertAndDispose_PythonRuntimeChecker_T]:
        ...


class PythonRuntimeChecker_ConvertAndDispose(typing.Generic[QuantConnect_Python_BasePythonWrapper_ConvertAndDispose_PythonRuntimeChecker_T]):
    """"""

    @overload
    def __call__(self, py_object: typing.Any, python_name: str, is_method: bool = True) -> QuantConnect_Python_BasePythonWrapper_ConvertAndDispose_PythonRuntimeChecker_T:
        """
        Converts the given PyObject into the provided t type,
        generating an exception with a user-friendly message if conversion is not possible.
        It will dispose of the source PyObject.
        """
        ...


