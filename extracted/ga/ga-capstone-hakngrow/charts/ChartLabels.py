import utils.AlphaVantageUtils as av
import utils.PostgresUtils as pg

_OPT_BASELINE = 'BL'

_OPT_LABEL = 'label'

_OPT_VALUE = 'value'


_LBL_1_MIN = '1 Min'
_LBL_5_MIN = '5 Min'
_LBL_15_MIN = '15 Min'
_LBL_30_MIN = '30 Min'
_LBL_1_HR = '1 Hour'

_LBL_BASELINE = 'Baseline'

_LBL_DAY = 'Day'

_LBL_INTERVAL = 'Interval'

_LBL_MODEL = 'Model'

_LBL_TICKER = 'Ticker'

_LBL_WEEK = 'Week'

_LBL_MONTH = 'Month'

def get_model_options():

    return [

        {_OPT_LABEL: _LBL_BASELINE, _OPT_VALUE: _OPT_BASELINE}
    ]


def get_interval_options():

    return [
        {_OPT_LABEL: _LBL_1_MIN, _OPT_VALUE: av._INT_1MIN},
        {_OPT_LABEL: _LBL_5_MIN, _OPT_VALUE: av._INT_5MIN},
        {_OPT_LABEL: _LBL_15_MIN, _OPT_VALUE: av._INT_15MIN},
        {_OPT_LABEL: _LBL_30_MIN, _OPT_VALUE: av._INT_30MIN},
        {_OPT_LABEL: _LBL_1_HR, _OPT_VALUE: av._INT_60MIN},

        {_OPT_LABEL: _LBL_DAY, _OPT_VALUE: av._INT_DAILY},
        {_OPT_LABEL: _LBL_WEEK, _OPT_VALUE: av._INT_WEEKLY},
        {_OPT_LABEL: _LBL_MONTH, _OPT_VALUE: av._INT_MONTHLY}
    ]


def get_symbol_options():

    return [{_OPT_LABEL: symbol[0], _OPT_VALUE: symbol[1]} for symbol in pg.get_symbols()]


