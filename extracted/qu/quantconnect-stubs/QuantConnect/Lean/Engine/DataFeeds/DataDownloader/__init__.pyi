from typing import overload
from enum import IntEnum
import datetime
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Data.Market
import QuantConnect.Interfaces
import QuantConnect.Lean.Engine.DataFeeds.DataDownloader
import QuantConnect.Securities
import System


class CanonicalDataDownloaderDecorator(System.Object, QuantConnect.IDataDownloader):
    """
    Decorates an IDataDownloader to support canonical symbols by automatically
    resolving their option or future contract chains and downloading data for each constituent contract.
    """

    def __init__(self, data_downloader: QuantConnect.IDataDownloader, data_provider: QuantConnect.Interfaces.IDataProvider, map_file_provider: QuantConnect.Interfaces.IMapFileProvider, factor_file_provider: QuantConnect.Interfaces.IFactorFileProvider) -> None:
        """
        Initializes a new instance of the CanonicalDataDownloaderDecorator class.
        
        :param data_downloader: The underlying data downloader to decorate with canonical symbol support.
        :param data_provider: The data provider used for initializing chain providers.
        :param map_file_provider: The map file provider used for initializing chain providers.
        :param factor_file_provider: The factor file provider used for initializing chain providers.
        """
        ...

    def get(self, data_downloader_get_parameters: QuantConnect.DataDownloaderGetParameters) -> typing.Sequence[QuantConnect.Data.BaseData]:
        """
        Get historical data enumerable for a single symbol, type and resolution given this start and end time (in UTC).
        For canonical symbols, automatically resolves and downloads data for all underlying contracts.
        
        :param data_downloader_get_parameters: model class for passing in parameters for historical data
        :returns: Enumerable of base data for this symbol.
        """
        ...

    @staticmethod
    def try_adjust_date_range_for_contract(contract: typing.Union[QuantConnect.Symbol, str, QuantConnect.Data.Market.BaseContract, QuantConnect.Securities.Security], original_start_date_utc: typing.Union[datetime.datetime, datetime.date], original_end_date_utc: typing.Union[datetime.datetime, datetime.date], adjusted_start_date_utc: typing.Optional[typing.Union[datetime.datetime, datetime.date]], adjusted_end_date_utc: typing.Optional[typing.Union[datetime.datetime, datetime.date]]) -> typing.Tuple[bool, typing.Union[datetime.datetime, datetime.date], typing.Union[datetime.datetime, datetime.date]]:
        """
        Tries to adjust the date range for a given contract based on its security type and expiry date.
        The start date is clamped to a minimum look-back period and the end date is clamped to the contract expiry date.
        Returns false if the minimum look-back period exceeds the requested end date, meaning no valid range exists.
        
        :param contract: The contract symbol containing the security type and expiry date.
        :param original_start_date_utc: The requested start date in UTC.
        :param original_end_date_utc: The requested end date in UTC.
        :param adjusted_start_date_utc: The adjusted start date in UTC, or default if no valid range exists.
        :param adjusted_end_date_utc: The adjusted end date in UTC, or default if no valid range exists.
        :returns: True if a valid adjusted date range was found, false otherwise.
        """
        ...


class DataDownloaderSelector(System.Object, System.IDisposable):
    """Selects the appropriate data downloader based on the data type."""

    def __init__(self, base_data_downloader: QuantConnect.IDataDownloader, map_file_provider: QuantConnect.Interfaces.IMapFileProvider, data_provider: QuantConnect.Interfaces.IDataProvider, factor_file_provider: QuantConnect.Interfaces.IFactorFileProvider = None) -> None:
        """
        Initializes a new instance of the DataDownloaderSelector class.
        
        :param base_data_downloader: The base data downloader instance.
        :param map_file_provider: The map file provider used for initializing chain providers.
        :param data_provider: The data provider used for initializing chain providers.
        :param factor_file_provider: The factor file provider used for initializing chain providers.
        """
        ...

    def dispose(self) -> None:
        """Disposes the base downloader and the decorator if it was initialized."""
        ...

    def get_data_downloader(self, data_type: typing.Type) -> QuantConnect.IDataDownloader:
        """
        Returns the appropriate downloader for the given data type.
        
        :param data_type: The type of data to download.
        :returns: The base downloader for common lean data types, otherwise the canonical decorator.
        """
        ...


