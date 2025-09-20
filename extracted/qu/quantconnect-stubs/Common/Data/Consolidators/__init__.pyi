from typing import overload
from enum import Enum
import datetime
import typing

import Common.Data.Consolidators
import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Consolidators
import QuantConnect.Data.Market
import QuantConnect.Securities


class DollarVolumeRenkoConsolidator(QuantConnect.Data.Consolidators.VolumeRenkoConsolidator):
    """
    This consolidator transforms a stream of BaseData instances into a stream of RenkoBar
    with a constant dollar volume for each bar.
    """

    def __init__(self, bar_size: float) -> None:
        """
        Initializes a new instance of the DollarVolumeRenkoConsolidator class using the specified .
        
        :param bar_size: The constant dollar volume size of each bar
        """
        ...

    def adjust_volume(self, volume: float, price: float) -> float:
        """
        Converts raw volume into dollar volume by multiplying it with the trade price.
        
        This method is protected.
        
        :param volume: The raw trade volume
        :param price: The trade price
        :returns: The dollar volume.
        """
        ...


class SessionConsolidator(QuantConnect.Data.Consolidators.PeriodCountConsolidatorBase[QuantConnect.Data.BaseData, QuantConnect.Data.Market.SessionBar]):
    """Consolidates intraday market data into a single daily SessionBar (OHLCV + OpenInterest)."""

    def __init__(self, exchange_hours: QuantConnect.Securities.SecurityExchangeHours, source_tick_type: QuantConnect.TickType, symbol: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract]) -> None:
        """
        Initializes a new instance of the SessionConsolidator class.
        
        :param exchange_hours: The exchange hours
        :param source_tick_type: Type of the source tick
        :param symbol: The symbol
        """
        ...

    def aggregate_bar(self, working_bar: QuantConnect.Data.Market.SessionBar, data: QuantConnect.Data.BaseData) -> None:
        """
        Aggregates the new 'data' into the 'working_bar'
        
        This method is protected.
        
        :param working_bar: The bar we're building, null if the event was just fired and we're starting a new trade bar
        :param data: The new data
        """
        ...

    def on_data_consolidated(self, e: QuantConnect.Data.Market.SessionBar) -> None:
        """
        Event handler that fires when a new piece of data is produced
        
        This method is protected.
        """
        ...

    def reset(self) -> None:
        """Resets the consolidator"""
        ...

    def reset_working_bar(self) -> None:
        """
        Resets the working bar
        
        This method is protected.
        """
        ...

    def validate_and_scan(self, current_local_time: typing.Union[datetime.datetime, datetime.date]) -> None:
        """
        Validates the current local time and triggers Scan() if a new day is detected.
        
        :param current_local_time: The current local time.
        """
        ...


