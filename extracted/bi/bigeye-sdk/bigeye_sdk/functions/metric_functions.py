from __future__ import annotations

import datetime
import logging
from typing import List, Union

from bigeye_sdk.class_ext.enum_ext import EnumExtension
from bigeye_sdk.generated.com.bigeye.models.generated import (
    Threshold,
    NotificationChannel,
    MetricRunFailureReason,
    ForecastModelType,
    MetricInfo,
    MetricConfiguration,
    MetricParameter,
    MetricType,
    Table,
    LookbackType,
    ConstantThreshold,
    SimpleBound,
    SimpleBoundType,
    SlackChannelInfo,
    MetricRunStatus, MetricInfoList,
)
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.protobuf_enum_facade import (
    SimpleMetricCategory,
    SimplePredefinedMetricName,
    MetricStatus,
)
from bigeye_sdk.model.protobuf_message_facade import (
    SimplePredefinedMetric,
    SimpleMetricType,
    SimpleThreshold, SimpleTemplateMetric,
)

log = get_logger(__name__)


def _is_table_level_metric(metric_type: SimpleMetricType,
                           table_level_metrics: List[SimplePredefinedMetricName]) -> bool:
    if not isinstance(metric_type, SimplePredefinedMetric):
        return False
    if metric_type.predefined_metric in table_level_metrics:
        return True

    return False


def filter_metrics_by_table_ids(metrics: List[dict], table_ids: List[int]) -> List[dict]:
    """
    Deprecated.  Previously used to filter raw HTTP responses.

    :param metrics: Metrics to filter
    :param table_ids: Table ids to filter it by

    :return: List of raw metric dictionaries.
    """
    log.info('Filtering Metric IDs')
    return [d for d in metrics if d['datasetId'] in table_ids]


def get_metric_ids(metrics: List[dict]) -> List[int]:
    """
    Deprecated.  Previously used to pull the metric ids from a raw list of metric dictionaries.

    :param metrics: list of metric dictionaries.

    :return: list of integers.
    """
    metric_ids = [d['metricConfiguration']['id'] for d in metrics]
    return metric_ids


def is_freshness_metric(metric_name: str) -> bool:
    """
    Indicates whether a particular metric, by name, is a freshness metric.

    :param metric_name:  The metric name.

    :return: Boolean.
    """
    return "HOURS_SINCE_MAX" in metric_name


def is_same_metric(metric: MetricConfiguration, metric_name: str, user_defined_name: str,
                   group_by: List[str], filters: List[str]) -> bool:
    """
    Used to determin whether a particular MetricConfiguration is the same based on metric name, user defined name,
    group by columns, and filters.

    :param metric: Metric Configuration to compare from
    :param metric_name: Metric name to compare to
    :param user_defined_name: User defined name to compare to
    :param group_by: Group by column list to compare to
    :param filters: Filter list to compare to

    :return: Boolean
    """
    both_freshness_metrics = is_freshness_metric(SimpleMetricCategory.get_metric_name(metric.metric_type)) \
                             and is_freshness_metric(metric_name)
    has_same_user_def_name = metric.name == user_defined_name
    is_same_type = SimpleMetricCategory.get_metric_name(metric.metric_type) == metric_name
    same_group_by = [i.lower() for i in metric.group_bys] == [i.lower() for i in group_by]
    same_filters = [i.lower() for i in metric.filters] == [i.lower() for i in filters]
    return (is_same_type or both_freshness_metrics) and has_same_user_def_name and same_filters and same_group_by

    # Deprecated code:
    # keys = ["metricType", "predefinedMetric", "metricName"]
    # result = reduce(lambda val, key: val.get(key) if val else None, keys, metric)
    # if result is None:
    #     return False

    # return result is not None and (result == metric_name or both_metrics_freshness) \
    #        and same_group_by and same_filters


def get_column_name(metric: MetricConfiguration) -> str:
    """
    Pulls the column name from a MetricConfiguration object.

    :param metric: MetricConfiguraiton object

    :return: Column name.
    """
    i: MetricParameter
    for i in metric.parameters:
        if i.key == 'arg1':
            return i.column_name


def is_same_column_metric(metric: MetricConfiguration, column_name):
    """
    Determines whether a particular MetricConfiguration is on a particular column by column name.

    :param metric: MetricConfiguraiton object
    :param column_name: Column Name

    :return: Boolean indicating whether a metric is on a particular column.
    """
    return get_column_name(metric).lower() == column_name.lower()


def get_proto_interval_type(interval_type: str) -> str:
    """
    Determines the correct Protobuf IntervalType for a particular short name.

    :param interval_type:

    :return:

    >>> get_proto_interval_type("hours interval")
    'HOURS_TIME_INTERVAL_TYPE'
    """
    if "minute" in interval_type:
        return "MINUTES_TIME_INTERVAL_TYPE"
    elif "hour" in interval_type:
        return "HOURS_TIME_INTERVAL_TYPE"
    elif "weekday" in interval_type:
        return "WEEKDAYS_TIME_INTERVAL_TYPE"
    elif "market day" in interval_type:
        return "MARKET_DAYS_TIME_INTERVAL_TYPE"
    elif "day" in interval_type:
        return "DAYS_TIME_INTERVAL_TYPE"


def get_max_hours_from_cron(cron):
    """
    Determines the max hours from a cron formatted string.

    :param cron: The cron format to get hours.

    :returns: int

    >>> get_max_hours_from_cron("10 14 * * 1")
    14
    """
    cron_values = cron.split(" ")
    hours = cron_values[1]
    if hours == "*":
        return 0
    return int(hours.split(",")[-1])


def get_days_since_n_weekdays(start_date, n):
    """
    Returns the days since the last business day, based on the start date.

    :param start_date: The date to calculate days since last business day
    :param n: The days to subtract from the start date.

    :returns int:
    """
    days_since_last_business_day = 0
    weekday_ordinal = datetime.date.weekday(start_date - datetime.timedelta(days=n))
    # 5 is Saturday, 6 is Sunday
    if weekday_ordinal >= 5:
        days_since_last_business_day = 2
    return days_since_last_business_day


def get_notification_channels(notifications: List[str]) -> List[NotificationChannel]:
    """
    Converts a list of strings into a list of NotificationChannel objects

    :param notifications: The list of strings to convert.

    :returns: List[NotificationChannel]

    >>> get_notification_channels(['#test', 'user@bigeye.com'])
    [NotificationChannel(email='', slack_channel='#test', webhook=Webhook(webhook_url='', webhook_headers=[])), NotificationChannel(email='user@bigeye.com', slack_channel='', webhook=Webhook(webhook_url='', webhook_headers=[]))]

    """
    channels: List[NotificationChannel] = []

    for n in notifications:
        nc = NotificationChannel()

        if n.startswith('#') or n.startswith('@'):
            nc.slack_channel_info = SlackChannelInfo(channel_name=n)
        elif '@' in n and '.' in n:
            nc.email = n
        else:
            raise Exception(f'Invalid notification format: {n}')

        channels.append(nc)

    return channels


def notification_channels_to_simple_str(notification_channels: List["NotificationChannel"]) -> List[str]:
    """
    Returns a simple string formatted list of notification channels.  ** Does not yet support webhooks.
    :param notification_channels: list of NotificationChannel objects
    :return: list of strings.
    """
    channels: List[str] = []

    for n in notification_channels:
        if n.email:
            channels.append(n.email)
        if n.slack_channel:
            channels.append(n.slack_channel)

    return channels


def get_freshness_metric_name_for_field(table: Table, column_name: str) -> MetricType:
    """
    Gets the freshness metric name for a column in a Table

    :param table: The Table to search
    :param column_name: The column name to get the freshness metric name.

    :returns: MetricType
    """
    for c in table.columns:
        if c.name.lower() == column_name.lower():
            if c.type == "TIMESTAMP_LIKE":
                return SimpleMetricCategory.PREDEFINED.factory("HOURS_SINCE_MAX_TIMESTAMP")
            elif c.type == "DATE_LIKE":
                return SimpleMetricCategory.PREDEFINED.factory("HOURS_SINCE_MAX_DATE")
            else:
                raise Exception(f'Type not compatible with freshness: {c.type}')


def get_file_name_for_metric(m: MetricInfo):
    """
    Formats a name for persisting metrics to files.

    :param m: MetricInfo object from which we build the name.

    :return:  Formatted name: schema_name-dataset_name-field_name-metric_name.json
    """
    mc = m.metric_configuration
    md = m.metric_metadata
    fn = f"{'_'.join(md.schema_name.split('.'))}-{md.dataset_name}-{md.field_name}-{mc.name}.json"
    return fn.replace(' ', '_')


def is_auto_threshold(t: Threshold) -> bool:
    """
    Tests if a Threshold object is an autothreshold.

    :param t: The Threshold to test.

    :returns: bool
    """
    return "autoThreshold" in t.to_dict()


def has_auto_threshold(ts: List[Threshold]) -> bool:
    """
    Checks a list of Threshold objects to check if any are autothresholds.

    :param ts: The List[Threshold] to check.

    :returns: bool
    """
    for t in ts:
        if "autoThreshold" in t.to_dict():
            return True
    return False


def set_default_model_type_for_threshold(thresholds: List[Threshold]) -> List[Threshold]:
    """
    Sets the default model type for a List of Threshold objects.

    :param thresholds: The Thresholds to check

    :returns: List[Threshold]
    """
    for t in thresholds:
        if is_auto_threshold(t):
            if not t.auto_threshold.model_type:
                t.auto_threshold.model_type = ForecastModelType.BOOTSTRAP_THRESHOLD_MODEL_TYPE

    return thresholds


def get_thresholds_for_metric(metric_name: str, timezone: str = None, delay_at_update: str = None,
                              update_schedule: str = None, thresholds: List[dict] = None) -> List[Threshold]:
    """
    Gets a list of appropriate Thresholds for a metric.

    :param metric_name: The name of the metric to create Thresholds
    :param timezone: The timezone for a freshness metric
    :param delay_at_update: The delay time at an update
    :param update_schedule: The time schedule for an update
    :param thresholds: a List of Thresholds defined by a user.

    :returns: List[Threshold]
    """
    if thresholds:
        return [Threshold().from_dict(t) for t in thresholds]
    # If it's a freshness
    elif is_freshness_metric(metric_name):
        tj = {
            "freshnessScheduleThreshold": {
                "bound": {
                    "boundType": "UPPER_BOUND_SIMPLE_BOUND_TYPE",
                    "value": -1
                },
                "cron": update_schedule,
                "timezone": timezone,
                "delayAtUpdate": get_time_interval_for_delay_string(delay_at_update,
                                                                    metric_name,
                                                                    update_schedule)
            }
        }
        return [Threshold().from_dict(tj)]
    # Default to autothresholds
    else:
        return [
            Threshold().from_dict({"autoThreshold": {"bound":
                                                         {"boundType": "LOWER_BOUND_SIMPLE_BOUND_TYPE", "value": -1.0},
                                                     "modelType": "BOOTSTRAP_THRESHOLD_MODEL_TYPE"}}),
            Threshold().from_dict({"autoThreshold": {"bound":
                                                         {"boundType": "UPPER_BOUND_SIMPLE_BOUND_TYPE", "value": -1.0},
                                                     "modelType": "BOOTSTRAP_THRESHOLD_MODEL_TYPE"}})
        ]


# TODO must unit test.  Also refactor to return a TimeInterval instead of a dict!.
def get_time_interval_for_delay_string(delay_at_update: str, metric_type: str, update_schedule: str) -> dict:
    """
    Creates a dictionary of a TimeInterval.

    :param delay_at_update: The string delay at update time.
    :param metric_type: The metric type.
    :param update_schedule: The update schedule as a cron string.

    :returns: dict

    >>> get_time_interval_for_delay_string("1 day", "HOURS_SINCE_MAX_DATE", "10 14 * * 1")
    {'intervalValue': 38, 'intervalType': 'HOURS_TIME_INTERVAL_TYPE'}
    """
    split_input = delay_at_update.split(" ", 1)
    interval_value = int(split_input[0])
    interval_type = get_proto_interval_type(split_input[1])
    if metric_type == "HOURS_SINCE_MAX_DATE":
        hours_from_cron = get_max_hours_from_cron(update_schedule)
        if interval_type == "HOURS_TIME_INTERVAL_TYPE" or interval_type == "MINUTES_TIME_INTERVAL_TYPE":
            logging.warning("Delay granularity for date column must be in days, ignoring value")
            interval_type = "HOURS_TIME_INTERVAL_TYPE"
            interval_value = hours_from_cron
        elif interval_type == "WEEKDAYS_TIME_INTERVAL_TYPE":
            lookback_weekdays = interval_value + 1 if datetime.datetime.utcnow().hour <= hours_from_cron \
                else interval_value
            logging.info("Weekdays to look back {}".format(lookback_weekdays))
            days_since_last_business_day = get_days_since_n_weekdays(datetime.date.today(), lookback_weekdays)
            logging.info("total days to use for delay {}".format(days_since_last_business_day))
            interval_type = "HOURS_TIME_INTERVAL_TYPE"
            interval_value = (days_since_last_business_day + lookback_weekdays) * 24 + hours_from_cron
        else:
            interval_type = "HOURS_TIME_INTERVAL_TYPE"
            interval_value = interval_value * 24 + hours_from_cron
    return {
        "intervalValue": interval_value,
        "intervalType": interval_type
    }


def is_failed(datum: dict) -> bool:
    """
    Checks if the latest metric run contains a failure

    :param datum: The dictionary of datum to check for failure.

    :returns: bool
    """
    if 'latestMetricRuns' in datum and datum['latestMetricRuns']:
        if 'failureReason' in datum['latestMetricRuns'][-1]:
            failure_reason = datum['latestMetricRuns'][-1]['failureReason']
            log.info(failure_reason)
            return failure_reason in MetricRunFailureReason

    return False


def get_failed_code(datum: dict) -> Union[None, str]:
    """
    Gets the failure reason in a datum of the latest metric runs.

    :param datum: The dictionary to check.

    :returns: Union[None, str]
    """
    if 'latestMetricRuns' in datum and datum['latestMetricRuns']:
        if 'failureReason' in datum['latestMetricRuns'][-1]:
            failure_reason = datum['latestMetricRuns'][-1]['failureReason']
            log.info(failure_reason)
            return failure_reason

    return None


def get_seconds_from_window_size(window_size) -> int:
    """
    Gets the seconds based a window size.

    :param window_size: The string to check.

    :returns: int

    >>> get_seconds_from_window_size("1 day")
    86400
    """
    if window_size == "1 day":
        return 86400
    elif window_size == "1 hour":
        return 3600
    else:
        raise Exception("Can only set window size of '1 hour' or '1 day'")


class MetricTimeNotEnabledStats(EnumExtension):
    HOURS_SINCE_MAX_TIMESTAMP = 'HOURS_SINCE_MAX_TIMESTAMP'
    HOURS_SINCE_MAX_DATE = 'HOURS_SINCE_MAX_DATE'
    PERCENT_DATE_NOT_IN_FUTURE = 'PERCENT_DATE_NOT_IN_FUTURE'
    PERCENT_NOT_IN_FUTURE = 'PERCENT_NOT_IN_FUTURE'
    COUNT_DATE_NOT_IN_FUTURE = 'COUNT_DATE_NOT_IN_FUTURE'


def is_metric_time_enabled(predefined_metric_name: str) -> bool:
    """
    Checks if a predefined metric name is part of the MetricTimeNotEnabledStats class.

    :param predefined_metric_name: The predefined metric name to check.

    :returns: bool

    >>> is_metric_time_enabled('HOURS_SINCE_MAX_DATE')
    True
    """
    return predefined_metric_name.upper() in MetricTimeNotEnabledStats.list()


def enforce_lookback_type_defaults(predefined_metric_name: str, lookback_type: str, metric_time_exists: bool):
    """
    Enforces lookback type defaults based on a predefined metric name.

    :param predefined_metric_name: The metric name to check.
    :param lookback_type: If None, return a default. Else return the lookback_type.
    :param metric_time_exists: A boolean if metric time exists.

    :returns: str

    >>> enforce_lookback_type_defaults('HOURS_SINCE_MAX_DATE', None)
    'DATA_TIME_LOOKBACK_TYPE'
    """
    if is_metric_time_enabled(predefined_metric_name=predefined_metric_name):
        lbts = 'DATA_TIME_LOOKBACK_TYPE'
    elif lookback_type is None:
        lbts = "METRIC_TIME_LOOKBACK_TYPE"
    else:
        lbts = lookback_type

    return get_lookback_type(lbts, metric_time_exists)


def get_lookback_type(lbts: str, metric_time_exists: bool):
    """
    Returns a LookbackType object based on a string.

    :param lbts: The string to convert to a LookbackType
    :param metric_time_exists: A boolean specifying if metric time exists.

    :returns: LookbackType

    >>> get_lookback_type('DATA_TIME_LOOKBACK_TYPE', True)
    <LookbackType.DATA_TIME_LOOKBACK_TYPE: 1>
    """
    if metric_time_exists:
        return LookbackType.from_string(lbts)
    else:
        return LookbackType.UNDEFINED_LOOKBACK_TYPE


def get_grain_seconds(lookback_type: LookbackType, window_size_seconds: int):
    """
    Returns the given grain seconds for a METRIC_TIME_LOOKBACK_TYPE.

    :param lookback_type: The LookbackType to check.
    :param window_size_seconds: The seconds to return.

    :returns: int

    >>> get_grain_seconds(LookbackType.METRIC_TIME_LOOKBACK_TYPE, 10)
    10
    """
    if lookback_type == LookbackType.METRIC_TIME_LOOKBACK_TYPE:
        return window_size_seconds


def merge_existing_metric_conf(new_metric: MetricConfiguration, is_freshness_metric: bool, metric_time_exists: bool,
                               existing_metric: MetricConfiguration = None) -> MetricConfiguration:
    """
    Updates/Merges an existing metric configuration with a new metric configuration.  Enforces updatable configurations.
    If existing metric configuration is none the new metric configuration is returned with no changes.

    :param new_metric: new MetricConfiguration
    :param is_freshness_metric: whether it's a freshness metric
    :param metric_time_exists: whether metric time exists on the table.
    :param existing_metric: existing metric configuration.

    :return: Merged MetricConfiguration
    """
    # TODO move to SimpleUpsertMetricRequest as private instance method.  This isnt really intended for reuse.
    if not existing_metric:
        return new_metric
    else:
        existing_metric.name = new_metric.name
        existing_metric.thresholds = new_metric.thresholds
        existing_metric.notification_channels = new_metric.notification_channels if new_metric.notification_channels \
            else []
        existing_metric.schedule_frequency = new_metric.schedule_frequency
        if not is_freshness_metric and metric_time_exists:
            existing_metric.lookback_type = new_metric.lookback_type
            existing_metric.lookback = new_metric.lookback
            existing_metric.grain_seconds = new_metric.grain_seconds
        return existing_metric


def create_constant_threshold(lower_bound: int, upper_bound: int) -> List[Threshold]:
    """
    Creates two Threshold objects based on a lower and upper bound.

    :param lower_bound: Lower bound threshold
    :param upper_bound: Upper bound threshold

    :return: List of 2 thresholds -- one for lower and one for upper bound.
    """
    lb = ConstantThreshold()
    sb = SimpleBound()
    sb.bound_type = SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE
    sb.value = lower_bound
    lb.bound = sb
    sb = SimpleBound()
    sb.bound_type = SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE
    sb.value = upper_bound
    ub = ConstantThreshold()
    ub.bound = sb
    lbt = Threshold()
    lbt.constant_threshold = lb
    ubt = Threshold()
    ubt.constant_threshold = ub
    return [lbt, ubt]


def notification_channels_to_simple_txt(notification_channels: List[NotificationChannel]):
    pass


def get_metric_status(metric_info: MetricInfo) -> MetricStatus:
    status = metric_info.status.name

    healthy_statuses = [
        MetricRunStatus.METRIC_RUN_STATUS_OK,
        MetricRunStatus.METRIC_RUN_STATUS_MUTABLE_OK
    ]
    alerting_statuses = [
        MetricRunStatus.METRIC_RUN_STATUS_LOWERBOUND_CRITICAL,
        MetricRunStatus.METRIC_RUN_STATUS_UPPERBOUND_CRITICAL,
        MetricRunStatus.METRIC_RUN_STATUS_GROUPS_CRITICAL,
        MetricRunStatus.METRIC_RUN_STATUS_MUTABLE_LOWERBOUND_CRITICAL
    ]
    failed_statuses = [
        MetricRunStatus.METRIC_RUN_STATUS_GROUPS_LIMIT_FAILED
    ]

    if status in healthy_statuses:
        return MetricStatus.HEALTHY
    elif status in alerting_statuses:
        return MetricStatus.ALERTING
    elif status in failed_statuses:
        return MetricStatus.FAILED
    else:
        return MetricStatus.UNKNOWN


def get_metric_lookback_window(metric_config: MetricConfiguration) -> str:
    lookback_days = metric_config.lookback.interval_value
    if lookback_days == -1:
        lookback_days_string = "Inferred"
    else:
        lookback_days_string = f"{metric_config.lookback.interval_value} Days"

    if metric_config.lookback_type == LookbackType.METRIC_TIME_LOOKBACK_TYPE:
        return f"Data Time Window ({lookback_days_string})"
    elif metric_config.lookback_type == LookbackType.DATA_TIME_LOOKBACK_TYPE:
        return f"Data Time ({lookback_days_string})"
    elif metric_config.lookback_type == LookbackType.CLOCK_TIME_LOOKBACK_TYPE:
        return f"Clock Time ({lookback_days_string})"
    elif metric_config.lookback_type == LookbackType.UNDEFINED_LOOKBACK_TYPE:
        return "Full Scan"


def create_metric_info_list(metric_infos: dict) -> MetricInfoList:
    mil_current = MetricInfoList()
    infos: List[MetricInfo] = []

    for metric_info in metric_infos["metrics"]:
        try:
            infos.append(MetricInfo().from_dict(metric_info))
        except ValueError:
            pass
    mil_current.metrics = infos
    mil_current.pagination_info = metric_infos["paginationInfo"]

    return mil_current


def metric_template_has_name_without_id(metric_template: SimpleTemplateMetric) -> bool:
    return metric_template.template_name and not metric_template.template_id


if __name__ == "__main__":
    import doctest

    doctest.testmod()
