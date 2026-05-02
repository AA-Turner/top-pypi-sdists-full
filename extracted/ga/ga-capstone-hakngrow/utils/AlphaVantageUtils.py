from alpha_vantage.timeseries import TimeSeries

import utils.PostgresUtils as pg


_FMT_PANDAS = 'pandas'
_FMT_CSV = 'csv'
_FMT_LIST = 'list'

_SIZE_FULL = 'full'
_SIZE_COMPACT = 'compact'

_INT_DAILY = 'D'
_INT_WEEKLY = 'W'
_INT_MONTHLY = 'M'
_INT_1MIN = '1'
_INT_5MIN = '5'
_INT_15MIN = '15'
_INT_30MIN = '30'
_INT_60MIN = '60'
_INT_MIN = 'min'

_TIC_MICROSOFT = 'MSFT'
_TIC_APPLE = 'AAPL'


def get_prices(api_key, ticker, interval, size, format=_FMT_PANDAS):

    df_prices = None
    meta_data = None

    ts = TimeSeries(key=api_key, output_format=_FMT_PANDAS)

    if interval == _INT_DAILY:
        df_prices, meta_data = ts.get_daily(symbol=ticker, outputsize=size)
    elif interval == _INT_1MIN:
        df_prices, meta_data = ts.get_intraday(symbol=ticker, interval=_INT_1MIN + _INT_MIN, outputsize=size)
    elif interval == _INT_5MIN:
        df_prices, meta_data = ts.get_intraday(symbol=ticker, interval=_INT_5MIN + _INT_MIN, outputsize=size)
    else:
        df_prices, meta_data = ts.get_daily(symbol=ticker, outputsize=size)

    df_prices.reset_index(level=0, inplace=True)

    df_prices.columns = [pg._COL_DATETIME, pg._COL_OPEN, pg._COL_HIGH, pg._COL_LOW, pg._COL_CLOSE, pg._COL_VOLUME]

    df_prices[pg._COL_TICKER] = ticker
    df_prices[pg._COL_INTERVAL] = interval

    df_prices = df_prices[[pg._COL_TICKER, pg._COL_INTERVAL, pg._COL_DATETIME, pg._COL_OPEN, pg._COL_HIGH, pg._COL_LOW,
                           pg._COL_CLOSE, pg._COL_VOLUME]]

    if format == _FMT_LIST:
        return df_prices.values.tolist()
    elif format == _FMT_PANDAS:
        return df_prices
    else:
        return df_prices
