import datetime
import types

# *********************************************************************************************************************
#
# IMPORTANT: This file is a manual mirror of client/packages/webserver/app/src/utilities/sharedDefinition.constants.ts.
# Do not change anything here without changing the source.
#
# *********************************************************************************************************************


# refer QUARTZ_CRON_PENDING_INPUT in sharedDefinition.constants.ts
QUARTZ_CRON_PENDING_INPUT = '59 59 23 31 12 ? 2099'

# refer DURATION_SCALAR_UNITS in sharedDefinition.constants.ts
DURATION_SCALAR_UNITS = [
    's', 'second', 'seconds', 'min', 'minute', 'minutes', 'h', 'hr', 'hrs', 'hour', 'hours', 'day', 'd', 'days',
    'week', 'wk', 'weeks', 'month', 'mo', 'months', 'year', 'y', 'yr', 'years',
    'ns', 'ms'
]

# refer OFFSET_DIRECTION in sharedDefinition.constants.ts
OFFSET_DIRECTION = types.SimpleNamespace(
    PAST='past',
    FUTURE='future'
)

# refer CAPSULE_SELECTION in sharedDefinition.constants.ts
CAPSULE_SELECTION = types.SimpleNamespace(
    STRATEGY=types.SimpleNamespace(
        CLOSEST_TO='closestTo',
        OFFSET_BY='offsetBy',
    ),
    REFERENCE=types.SimpleNamespace(
        START='start',
        END='end',
    ),
)

# refer DEFAULT_DATE_RANGE in sharedDefinition.constants.ts
DEFAULT_DATE_RANGE = {
    'auto': {
        'enabled': False,
        'duration': datetime.timedelta(days=1).total_seconds() * 1000,
        'offset': {'value': 0, 'units': 'min'},
        'offsetDirection': OFFSET_DIRECTION.PAST,
        'cronSchedule': [QUARTZ_CRON_PENDING_INPUT],
        'noCapsuleFound': False,
    },
    'condition': {
        'strategy': CAPSULE_SELECTION.STRATEGY.CLOSEST_TO,
        'reference': CAPSULE_SELECTION.REFERENCE.END,
        'offset': 1,
        'range': {},
    },
    'range': {},
    'enabled': True,
}

# refer AgGridAggregationFunctions in sharedDefinition.constants.ts
AG_GRID_AGGREGATION_FUNCTIONS = {
    'none', 'sum', 'min', 'max', 'count', 'avg', 'range', 'stdDev', 'first', 'last'
}


# refer LABEL_LOCATIONS in sharedDefinition.constants.ts
class LABEL_LOCATIONS:
    OFF = 'off'
    LANE = 'lane'
    AXIS = 'axis'


# refer LABEL_PROPERTIES in sharedDefinition.constants.ts
class LABEL_PROPERTIES:
    NAME = 'name'
    DESCRIPTION = 'description'
    ASSET = 'asset'
    LINE = 'line'
    ASSET_PATH_LEVELS = 'assetPathLevels'
    UOM = 'unitOfMeasure'
    CUSTOM = 'custom'


# refer TrendColorMode in sharedDefinition.constants.ts
class TREND_COLOR_MODE:
    ITEM = 'item'
    PROPERTY = 'capsuleProperty'
    GRADIENT = 'capsulePropertyGradient'


# refer TableBuilderMode in sharedDefinition.constants.ts
class TABLE_BUILDER_MODE:
    SIMPLE = 'simple'
    CONDITION = 'condition'


# refer TREND_PANELS.CAPSULES/.CHART_CAPSULES in client/packages/webserver/app/src/trendData/trendData.constants.ts.
# That enum has other members not relevant to SPy, so it isn't fully mirrored here; TypeScript enum members can't
# reference this constant either, so keep both sides in sync manually.
class TREND_PANELS:
    CAPSULES = 'CAPSULES'
    CHART_CAPSULES = 'CHART_CAPSULES'


# refer TableBuilderHeaderType in sharedDefinition.constants.ts
class TABLE_BUILDER_HEADER_TYPE:
    NONE = 'none'
    START = 'start'
    END = 'end'
    START_END = 'startEnd'
    CAPSULE_PROPERTY = 'capsuleProperty'


# refer DASH_STYLES in sharedDefinition.constants.ts
class DASH_STYLES:
    SOLID = 'Solid'
    SHORT_DASH = 'ShortDash'
    SHORT_DASH_DOT = 'ShortDashDot'
    SHORT_DASH_DOT_DOT = 'ShortDashDotDot'
    DOT = 'Dot'
    DASH = 'Dash'
    LONG_DASH = 'LongDash'
    DASH_DOT = 'DashDot'
    LONG_DASH_DOT = 'LongDashDot'
    LONG_DASH_DOT_DOT = 'LongDashDotDot'


# refer SAMPLE_OPTIONS in sharedDefinition.constants.ts
class SAMPLE_OPTIONS:
    LINE = 'line'
    SAMPLES = 'sample'
    LINE_AND_SAMPLE = 'lineAndSample'
    BAR = 'bar'


# refer Y_AXIS_TYPES in sharedDefinition.constants.ts
class Y_AXIS_TYPES:
    LOGARITHMIC = 'logarithmic'
    LINEAR = 'linear'


# refer WORKSHEET_VIEW_KEYS in sharedDefinition.constants.ts.
# Note: This is only the subset of worksheet.constants.ts's  WORKSHEET_VIEW that SPy needs.
class WORKSHEET_VIEW:
    TREND = 'TREND'
    SCATTER_PLOT = 'SCATTER_PLOT'
    TREEMAP = 'TREEMAP'
    TABLE = 'TABLE'
    ASSET_GROUP_EDITOR = 'ASSET_GROUP_EDITOR'


# refer TREND_SIGNAL_STATS in sharedDefinition.constants.ts
def get_trend_signal_statistic_function_map():
    return {
        "delta": "statistics.delta",
        "maximum": "statistics.maximum",
        "minimum": "statistics.minimum",
        "value at end": "statistics.endValue",
        "count": "statistics.count",
        "range": "statistics.range",
        "average": "statistics.average",
        "percent good": "statistics.percentGood",
        "standard deviation": "statistics.stdDev",
    }
