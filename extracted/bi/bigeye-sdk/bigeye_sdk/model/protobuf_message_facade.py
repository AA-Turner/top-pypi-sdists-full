from __future__ import annotations

import json
import re
from abc import ABC
from typing import List, Optional, TypeVar, Union

import betterproto
import yaml
from deprecated import deprecated
from pydantic.v1 import validator, Field, root_validator
from pydantic_yaml import YamlStrEnum

from bigeye_sdk.bigconfig_validation.validation_functions import safe_split_dict_entry_lines, must_be_list_validator
from bigeye_sdk.bigconfig_validation.yaml_model_base import YamlModelWithValidatorContext
from bigeye_sdk.bigconfig_validation.yaml_validation_error_messages import FORMATTING_ERRMSG, \
    OVERRIDE_METRIC_TYPE_SAVED_METRIC_ERRMSG, MUST_HAVE_METRIC_TYPE_ERRMSG, MUST_HAVE_METRIC_ID_ERRMSG, \
    METRIC_TYPE_NOT_EXISTS_ERRMSG, POSSIBLE_MATCH_ERRMSG, NO_POSSIBLE_MATCH_ERRMSG, TWO_SCHEDULES_DEFINED, \
    INVALID_THRESHOLD_BOUNDS
from bigeye_sdk.exceptions import InvalidConfigurationException
from bigeye_sdk.functions.search_and_match_functions import fuzzy_match
from bigeye_sdk.functions.table_functions import get_table_column_id
from bigeye_sdk.generated.com.bigeye.models.generated import Threshold, SimpleBoundType, ConstantThreshold, \
    SimpleBound, NamedSchedule, ComparisonColumnMapping, Table, IdAndDisplayName, ColumnNamePair, TimeInterval, \
    MetricParameter, MetricType, PredefinedMetric, TemplateMetric, AutoThreshold, ForecastModelType, RelativeThreshold, \
    StandardDeviationThreshold, FreshnessScheduleThreshold, NotificationChannel, MetricDefinition, MetricConfiguration, \
    Collection, SlackChannelInfo, Webhook, WebhookHeader, MetricSchedule, NoneThreshold, LookbackType
from bigeye_sdk.log import get_logger
from bigeye_sdk.model.base_datawatch_facade import DatawatchFacade
from bigeye_sdk.model.protobuf_enum_facade import SimplePredefinedMetricName, SimpleTimeIntervalType, \
    SimpleAutothresholdSensitivity, SimpleLookbackType, SimpleAggregationType
from bigeye_sdk.serializable import PydanticSubtypeSerializable

log = get_logger(__file__)

freshness_metrics = [
    SimplePredefinedMetricName.HOURS_SINCE_LAST_LOAD,
    SimplePredefinedMetricName.HOURS_SINCE_MAX_DATE,
    SimplePredefinedMetricName.HOURS_SINCE_MAX_TIMESTAMP,
    SimplePredefinedMetricName.FRESHNESS,
    SimplePredefinedMetricName.FRESHNESS_DATA
]

volume_metrics = [
    SimplePredefinedMetricName.VOLUME,
    SimplePredefinedMetricName.ROWS_INSERTED,
    SimplePredefinedMetricName.COUNT_ROWS,
    SimplePredefinedMetricName.VOLUME_DATA
]

pipeline_reliability_metrics = [SimplePredefinedMetricName.COUNT_READ_QUERIES] + freshness_metrics + volume_metrics

completeness_metrics = [
    SimplePredefinedMetricName.PERCENT_NULL,
    SimplePredefinedMetricName.COUNT_NULL,
    SimplePredefinedMetricName.PERCENT_NOT_NULL,
    SimplePredefinedMetricName.COUNT_NOT_NULL,
    SimplePredefinedMetricName.PERCENT_EMPTY_STRING,
    SimplePredefinedMetricName.COUNT_EMPTY_STRING,
    SimplePredefinedMetricName.PERCENT_NAN,
    SimplePredefinedMetricName.COUNT_NAN
]

uniqueness_metrics = [
    SimplePredefinedMetricName.COUNT_DISTINCT,
    SimplePredefinedMetricName.COUNT_DUPLICATES
]

distribution_metrics = [
    SimplePredefinedMetricName.MAX,
    SimplePredefinedMetricName.MIN,
    SimplePredefinedMetricName.AVERAGE,
    SimplePredefinedMetricName.VARIANCE,
    SimplePredefinedMetricName.MEDIAN,
    SimplePredefinedMetricName.SUM,
    SimplePredefinedMetricName.SKEW,
    SimplePredefinedMetricName.KURTOSIS,
    SimplePredefinedMetricName.GEOMETRIC_MEAN,
    SimplePredefinedMetricName.HARMONIC_MEAN,
    SimplePredefinedMetricName.COUNT_FALSE,
    SimplePredefinedMetricName.PERCENT_FALSE,
    SimplePredefinedMetricName.COUNT_TRUE,
    SimplePredefinedMetricName.PERCENT_TRUE
]

validity_metrics = [
    SimplePredefinedMetricName.STRING_LENGTH_MAX,
    SimplePredefinedMetricName.STRING_LENGTH_MIN,
    SimplePredefinedMetricName.STRING_LENGTH_AVERAGE,
    SimplePredefinedMetricName.PERCENT_UUID,
    SimplePredefinedMetricName.COUNT_UUID,
    SimplePredefinedMetricName.COUNT_CUSIP,
    SimplePredefinedMetricName.PERCENT_CUSIP,
    SimplePredefinedMetricName.COUNT_SEDOL,
    SimplePredefinedMetricName.PERCENT_SEDOL,
    SimplePredefinedMetricName.COUNT_ISIN,
    SimplePredefinedMetricName.PERCENT_ISIN,
    SimplePredefinedMetricName.COUNT_LEI,
    SimplePredefinedMetricName.PERCENT_LEI,
    SimplePredefinedMetricName.COUNT_FIGI,
    SimplePredefinedMetricName.PERCENT_FIGI,
    SimplePredefinedMetricName.COUNT_PERM_ID,
    SimplePredefinedMetricName.PERCENT_PERM_ID,
    SimplePredefinedMetricName.COUNT_NAN,
    SimplePredefinedMetricName.PERCENT_NAN,
    SimplePredefinedMetricName.COUNT_LONGITUDE,
    SimplePredefinedMetricName.PERCENT_LONGITUDE,
    SimplePredefinedMetricName.COUNT_LATITUDE,
    SimplePredefinedMetricName.PERCENT_LATITUDE,
    SimplePredefinedMetricName.COUNT_NOT_IN_FUTURE,
    SimplePredefinedMetricName.PERCENT_NOT_IN_FUTURE,
    SimplePredefinedMetricName.COUNT_DATE_NOT_IN_FUTURE,
    SimplePredefinedMetricName.PERCENT_DATE_NOT_IN_FUTURE,
    SimplePredefinedMetricName.COUNT_SSN,
    SimplePredefinedMetricName.PERCENT_SSN,
    SimplePredefinedMetricName.COUNT_EMAIL,
    SimplePredefinedMetricName.PERCENT_EMAIL,
    SimplePredefinedMetricName.COUNT_USA_PHONE,
    SimplePredefinedMetricName.PERCENT_USA_PHONE,
    SimplePredefinedMetricName.COUNT_USA_ZIP_CODE,
    SimplePredefinedMetricName.PERCENT_USA_ZIP_CODE,
    SimplePredefinedMetricName.PERCENT_UUID,
    SimplePredefinedMetricName.COUNT_TIMESTAMP_STRING,
    SimplePredefinedMetricName.PERCENT_TIMESTAMP_STRING,
    SimplePredefinedMetricName.COUNT_USA_STATE_CODE,
    SimplePredefinedMetricName.PERCENT_USA_STATE_CODE,
    SimplePredefinedMetricName.PERCENT_VALUE_IN_LIST,
    SimplePredefinedMetricName.COUNT_VALUE_IN_LIST
]


def get_type_from_dict(obj: betterproto.Message) -> str:
    """A patch for beterproto.which_one_of not working on objects serialized from_dict.   I have reported the bug to
    the maintainers of better proto.  TODO remove when bug is fixed."""
    return list(obj.to_dict(casing=betterproto.Casing.SNAKE).keys())[0]


class SimpleMetricType(PydanticSubtypeSerializable, DatawatchFacade, ABC):
    type: str

    @classmethod
    def get_freshness_metric_types(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=freshness_metrics)

    @classmethod
    def get_volume_metric_types(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=volume_metrics)

    @classmethod
    def get_completeness_metric_types(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=completeness_metrics)

    @classmethod
    def get_uniqueness_metric_types(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=uniqueness_metrics)

    @classmethod
    def get_distribution_metric_types(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=distribution_metrics)

    @classmethod
    def get_validity_metric_types(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=validity_metrics)

    @classmethod
    def get_pipeline_reliability_metrics(cls) -> List[SimplePredefinedMetric]:
        return cls.__get_simple_predefined_metrics(metric_names=pipeline_reliability_metrics)

    @classmethod
    def __get_simple_predefined_metrics(cls, metric_names: List[SimplePredefinedMetricName]):
        return [SimplePredefinedMetric(type="PREDEFINED", predefined_metric=i) for i in metric_names]

    @classmethod
    def is_freshness_metric(cls, predefined_metric):
        return predefined_metric in cls.get_freshness_metric_types()

    @classmethod
    def is_volume_metric(cls, predefined_metric):
        return predefined_metric in cls.get_volume_metric_types()

    @classmethod
    def is_pipeline_reliability(cls, predefined_metric):
        return predefined_metric in cls.get_pipeline_reliability_metrics()

    @classmethod
    def is_completeness_metric(cls, predefined_metric):
        return predefined_metric in cls.get_completeness_metric_types()

    @classmethod
    def is_uniqueness_metric(cls, predefined_metric):
        return predefined_metric in cls.get_uniqueness_metric_types()

    @classmethod
    def is_distribution_metric(cls, predefined_metric):
        return predefined_metric in cls.get_distribution_metric_types()

    @classmethod
    def is_validity_metric(cls, predefined_metric):
        return predefined_metric in cls.get_validity_metric_types()

    @classmethod
    def is_freshness_volume(cls, predefined_metric):
        return predefined_metric in [
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.FRESHNESS),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.VOLUME),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.FRESHNESS_DATA),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.VOLUME_DATA)
        ]

    @classmethod
    def is_table_metric(cls, predefined_metric):
        return predefined_metric in [
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.FRESHNESS),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.VOLUME),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.FRESHNESS_DATA),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.VOLUME_DATA),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.COUNT_ROWS),
            SimplePredefinedMetric(type="PREDEFINED", predefined_metric=SimplePredefinedMetricName.COUNT_READ_QUERIES),
        ]

    @classmethod
    def get_metadata_metrics(cls) -> List[SimplePredefinedMetric]:
        metadata_metrics = [SimplePredefinedMetricName.HOURS_SINCE_LAST_LOAD,
                            SimplePredefinedMetricName.FRESHNESS,
                            SimplePredefinedMetricName.VOLUME,
                            SimplePredefinedMetricName.ROWS_INSERTED,
                            SimplePredefinedMetricName.COUNT_READ_QUERIES,
                            SimplePredefinedMetricName.FRESHNESS_DATA,
                            SimplePredefinedMetricName.VOLUME_DATA
                            ]
        return [SimplePredefinedMetric(type="PREDEFINED", predefined_metric=i) for i in metadata_metrics]

    @classmethod
    def from_datawatch_object(cls, obj: MetricType) -> SimpleMetricType:
        t = betterproto.which_one_of(obj, "metric_type")[0]
        if not t:
            t = get_type_from_dict(obj)
        if t == 'template_metric':
            tm = obj.template_metric
            return SimpleTemplateMetric(type='TEMPLATE',
                                        template_id=tm.template_id,
                                        aggregation_type=SimpleAggregationType.from_datawatch_object(
                                            tm.aggregation_type),
                                        template_name=tm.template_name)
        elif t == 'predefined_metric':
            return SimplePredefinedMetric(
                type='PREDEFINED',
                predefined_metric=SimplePredefinedMetricName.from_datawatch_object(obj.predefined_metric.metric_name)
            )
        else:
            error_message = f"Metric type not supported: {t}"
            raise InvalidConfigurationException(error_message)


class SimplePredefinedMetric(SimpleMetricType, type='PREDEFINED'):
    type: str = 'PREDEFINED'
    predefined_metric: SimplePredefinedMetricName

    @validator('predefined_metric', pre=True, allow_reuse=True)
    def must_be_valid_metric(cls, v):
        try:
            return SimplePredefinedMetricName(v)
        except ValueError:
            is_freshness = fuzzy_match(v,
                                       ['FRESHNESS'],
                                       85)
            possible_matches = fuzzy_match(v,
                                           [e.value for e in SimplePredefinedMetricName],
                                           50)
            if is_freshness:
                possible_match_message = POSSIBLE_MATCH_ERRMSG.format(
                    possible_matches=", ".join([
                        SimplePredefinedMetricName.HOURS_SINCE_MAX_DATE,
                        SimplePredefinedMetricName.HOURS_SINCE_MAX_TIMESTAMP
                    ]))
            elif possible_matches:
                pms = [i[1] for i in possible_matches][:3]
                possible_match_message = POSSIBLE_MATCH_ERRMSG.format(possible_matches=", ".join(pms))
            else:
                possible_match_message = NO_POSSIBLE_MATCH_ERRMSG

            error_message = METRIC_TYPE_NOT_EXISTS_ERRMSG.format(metric=v, match_message=possible_match_message)
            cls.register_validation_error(error_lines=[v],
                                          error_message=error_message)
            return SimplePredefinedMetricName.UNDEFINED

    def to_datawatch_object(self, **kwargs) -> MetricType:
        return MetricType(predefined_metric=PredefinedMetric(metric_name=self.predefined_metric.to_datawatch_object()))


class SimpleTemplateMetric(SimpleMetricType, type='TEMPLATE'):
    type: str = 'TEMPLATE'
    template_id: int = 0
    aggregation_type: SimpleAggregationType
    template_name: Optional[str] = None

    def to_datawatch_object(self, **kwargs) -> MetricType:
        return MetricType(template_metric=TemplateMetric(template_id=self.template_id,
                                                         aggregation_type=self.aggregation_type.to_datawatch_object(),
                                                         template_name=self.template_name))


class SimpleNamedSchedule(YamlModelWithValidatorContext, DatawatchFacade):
    name: str = None
    cron: Optional[str] = None
    id: Optional[int] = None

    @classmethod
    def from_datawatch_object(cls, obj: NamedSchedule, **kwargs) -> SimpleNamedSchedule:
        return SimpleNamedSchedule(name=obj.name, cron=obj.cron, id=obj.id)

    def to_datawatch_object(self) -> NamedSchedule:
        return NamedSchedule(name=self.name, cron=self.cron, id=self.id)


class SimpleColumnMapping(YamlModelWithValidatorContext, DatawatchFacade):
    source_column_name: str
    target_column_name: str
    metrics: List[SimplePredefinedMetric] = Field(default_factory=lambda: [])

    @root_validator(pre=True, allow_reuse=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleColumnMapping, attribute_name='metrics', values=values)

        return values

    @classmethod
    def from_datawatch_object(cls, obj: ComparisonColumnMapping) -> SimpleColumnMapping:
        smt_list: List[SimpleMetricType] = [SimpleMetricType.from_datawatch_object(om) for om in obj.metrics]
        return SimpleColumnMapping(source_column_name=obj.source_column.display_name,
                                   target_column_name=obj.target_column.display_name,
                                   metrics=smt_list)

    def to_datawatch_object(self, source_table: Table, target_table: Table) -> ComparisonColumnMapping:
        cm = ComparisonColumnMapping()
        cm.source_column = IdAndDisplayName(id=get_table_column_id(source_table, self.source_column_name),
                                            display_name=self.source_column_name)
        cm.target_column = IdAndDisplayName(id=get_table_column_id(target_table, self.target_column_name),
                                            display_name=self.target_column_name)
        cm.metrics = [m.to_datawatch_object() for m in self.metrics]
        return cm


class SimpleColumnPair(YamlModelWithValidatorContext, DatawatchFacade):
    source_column_name: str
    target_column_name: str

    @classmethod
    def from_datawatch_object(cls, obj: ColumnNamePair) -> SimpleColumnPair:
        return SimpleColumnPair(source_column_name=obj.source_column_name, target_column_name=obj.target_column_name)

    def to_datawatch_object(self) -> ColumnNamePair:
        return ColumnNamePair(
            source_column_name=self.source_column_name,
            target_column_name=self.target_column_name
        )


class SimpleTimeInterval(YamlModelWithValidatorContext, DatawatchFacade):
    interval_type: SimpleTimeIntervalType
    interval_value: int = 0

    @classmethod
    def from_datawatch_object(cls, obj: TimeInterval) -> Optional[SimpleTimeInterval]:
        if obj.interval_type == 0 and obj.interval_value == 0:
            return None
        return SimpleTimeInterval(interval_type=SimpleTimeIntervalType.from_datawatch_object(obj.interval_type),
                                  interval_value=obj.interval_value)

    def to_datawatch_object(self, **kwargs) -> TimeInterval:
        return TimeInterval(interval_type=self.interval_type.to_datawatch_object(), interval_value=self.interval_value)


class SimpleMetricSchedule(YamlModelWithValidatorContext, DatawatchFacade):
    schedule_frequency: Optional[SimpleTimeInterval] = None
    named_schedule: Optional[SimpleNamedSchedule] = None

    @classmethod
    def from_datawatch_object(cls, obj: MetricSchedule) -> Optional[SimpleMetricSchedule]:
        if obj.schedule_frequency:
            if obj.schedule_frequency.interval_type == 0 and obj.schedule_frequency.interval_value == 0:
                if obj.named_schedule:
                    return SimpleMetricSchedule(
                        named_schedule=SimpleNamedSchedule.from_datawatch_object(obj.named_schedule)
                    )
                else:
                    return None
            else:
                sti = SimpleTimeInterval(
                    interval_type=SimpleTimeIntervalType.from_datawatch_object(
                        obj.schedule_frequency.interval_type),
                    interval_value=obj.schedule_frequency.interval_value
                )
                return SimpleMetricSchedule(schedule_frequency=sti)
        else:
            return SimpleMetricSchedule(
                named_schedule=SimpleNamedSchedule.from_datawatch_object(obj.named_schedule)
            )

    def to_datawatch_object(self) -> MetricSchedule:
        ms = MetricSchedule()
        if self.named_schedule:
            ms.named_schedule = NamedSchedule(
                id=self.named_schedule.id,
                name=self.named_schedule.name,
                cron=self.named_schedule.cron
            )
        elif self.schedule_frequency:
            ms.schedule_frequency = TimeInterval(
                interval_type=self.schedule_frequency.interval_type.to_datawatch_object(),
                interval_value=self.schedule_frequency.interval_value
            )
        return ms


ST = TypeVar('ST', bound='SimpleThreshold')


class SimpleThreshold(PydanticSubtypeSerializable, DatawatchFacade, ABC):
    type: str

    @classmethod
    def from_datawatch_object(cls, obj: List[Threshold]) -> ST:
        t = betterproto.which_one_of(obj[0], "threshold_type")[0]
        if not t:
            t = get_type_from_dict(obj[0])
        if t == 'auto_threshold':
            lower_bound = None
            upper_bound = None
            for i in obj:
                if i.auto_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.auto_threshold.bound.value
                if i.auto_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.auto_threshold.bound.value
            sat = SimpleAutoThreshold(
                type="AUTO",
                sensitivity=SimpleAutothresholdSensitivity.from_datawatch_object(obj[0].auto_threshold.sensitivity),
                upper_bound_only=True if upper_bound and not lower_bound else False,
                lower_bound_only=True if lower_bound and not upper_bound else False
            )
            return sat
        elif t == 'constant_threshold':
            lower_bound = None
            upper_bound = None
            for i in obj:
                if i.constant_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.constant_threshold.bound.value
                if i.constant_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.constant_threshold.bound.value

            sct = SimpleConstantThreshold(type="CONSTANT", lower_bound=lower_bound, upper_bound=upper_bound)

            return sct
        elif t == 'relative_threshold':
            """Relative Threshold"""
            lower_bound = None
            upper_bound = None
            lookback = SimpleTimeInterval.from_datawatch_object(obj[0].relative_threshold.lookback)
            for i in obj:
                if i.relative_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.relative_threshold.bound.value
                if i.relative_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.relative_threshold.bound.value

            srt = SimpleRelativeThreshold(type="RELATIVE",
                                          lower_bound=lower_bound, upper_bound=upper_bound, lookback=lookback)

            return srt
        elif t == 'standard_deviation_threshold':
            """StdDev Threshold"""
            lower_bound = None
            upper_bound = None
            lookback = SimpleTimeInterval.from_datawatch_object(obj[0].standard_deviation_threshold.lookback)
            for i in obj:
                if i.standard_deviation_threshold.bound.bound_type == SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE:
                    lower_bound = i.standard_deviation_threshold.bound.value
                if i.standard_deviation_threshold.bound.bound_type == SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE:
                    upper_bound = i.standard_deviation_threshold.bound.value

            ssdt = SimpleStdDevThreshold(type="STDDEV",
                                         lower_bound=lower_bound, upper_bound=upper_bound, lookback=lookback)

            return ssdt
        elif t == 'freshness_schedule_threshold':
            """Freshness Schedule Threshold"""
            t = obj[0].freshness_schedule_threshold
            bound = t.bound.value
            dau = None if not t.delay_at_update else SimpleTimeInterval.from_datawatch_object(t.delay_at_update)
            ft = SimpleFreshnessThreshold(
                type='FRESHNESS',
                cron=t.cron, timezone=t.timezone, upper_bound=bound, delay_at_update=dau)
            return ft
        elif t == 'none_threshold':
            return SimpleNoneThreshold(type="NONE")
        else:
            error_message = f"Threshold type not supported: {t}"
            raise InvalidConfigurationException(error_message)


class SimpleAutoThreshold(SimpleThreshold, type='AUTO'):
    sensitivity: SimpleAutothresholdSensitivity = SimpleAutothresholdSensitivity.MEDIUM
    upper_bound_only: bool = False
    lower_bound_only: bool = False

    @root_validator(pre=True, allow_reuse=True)
    def check_bounds(cls, values):
        if values.get('upper_bound_only') and values.get('lower_bound_only'):
            errlns = [
                yaml.safe_dump({"upper_bound_only": True}, indent=True, sort_keys=False),
                yaml.safe_dump({"lower_bound_only": True}, indent=True, sort_keys=False),
            ]
            cls.register_validation_error(error_lines=errlns, error_message=INVALID_THRESHOLD_BOUNDS)

        return values


    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=-1.0)
        ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=-1.0)
        mt = ForecastModelType.BOOTSTRAP_THRESHOLD_MODEL_TYPE
        s = self.sensitivity.to_datawatch_object()
        fv = -1.0

        lbat = AutoThreshold(
            bound=lb,
            model_type=mt,
            sensitivity=s,
            forecast_value=fv
        )
        ubat = AutoThreshold(
            bound=ub,
            model_type=mt,
            sensitivity=s,
            forecast_value=fv
        )
        if self.upper_bound_only:
            return [Threshold(auto_threshold=ubat)]
        elif self.lower_bound_only:
            return [Threshold(auto_threshold=lbat)]
        else:
            return [Threshold(auto_threshold=lbat), Threshold(auto_threshold=ubat)]


class SimpleConstantThreshold(SimpleThreshold, type='CONSTANT'):
    upper_bound: Optional[float] = None
    lower_bound: Optional[float] = None

    def to_datawatch_object(self) -> List[Threshold]:
        """
        Creates a list of protobuf Threshold objects from an instance of SimpleConstantThreshold
        :return: a List of Thresholds
        """
        thresholds: List[Threshold] = []
        if self.lower_bound is not None:
            lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=self.lower_bound)
            lbt = Threshold(constant_threshold=ConstantThreshold(bound=lb))
            thresholds.append(lbt)
        if self.upper_bound is not None:
            ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
            ubt = Threshold(constant_threshold=ConstantThreshold(bound=ub))
            thresholds.append(ubt)

        return thresholds


class SimpleFreshnessThreshold(SimpleThreshold, type='FRESHNESS'):
    cron: str
    upper_bound: float = 0
    timezone: Optional[str] = None
    delay_at_update: Optional[SimpleTimeInterval] = SimpleTimeInterval(interval_type=SimpleTimeIntervalType.HOURS,
                                                                       interval_value=0)

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        thresholds: List[Threshold] = []
        ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
        dau = self.delay_at_update.to_datawatch_object()
        ft = FreshnessScheduleThreshold(cron=self.cron, bound=ub, timezone=self.timezone, delay_at_update=dau)
        thresholds.append(Threshold(freshness_schedule_threshold=ft))

        return thresholds


class SimpleRelativeThreshold(SimpleThreshold, type='RELATIVE'):
    lookback: SimpleTimeInterval = None
    upper_bound: Optional[float] = None
    lower_bound: Optional[float] = None
    reference_point: SimpleTimeInterval = None

    @root_validator(pre=True, allow_reuse=True)
    def validate_lookback_or_reference_point_set(cls, values):
        # TODO use field aliases after upgrading pydantic version
        #  https://docs.pydantic.dev/2.3/usage/fields/#aliaspath-and-aliaschoices
        lookback = values.get('lookback')
        reference_point = values.get('reference_point')

        if reference_point:
            values["lookback"] = reference_point

        if not lookback and not reference_point:
            raise ValueError('For relative thresholds, reference_point is required.')

        return values

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        lkbk = self.lookback.to_datawatch_object()

        thresholds: List[Threshold] = []
        if self.lower_bound is not None:
            lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=self.lower_bound)
            lbt = Threshold(relative_threshold=RelativeThreshold(lookback=lkbk, bound=lb))
            thresholds.append(lbt)
        if self.upper_bound is not None:
            ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
            ubt = Threshold(relative_threshold=RelativeThreshold(lookback=lkbk, bound=ub))
            thresholds.append(ubt)

        return thresholds


class SimpleStdDevThreshold(SimpleThreshold, type='STDDEV'):
    lookback: SimpleTimeInterval = None
    upper_bound: Optional[float] = None
    lower_bound: Optional[float] = None
    reference_point: SimpleTimeInterval = None

    @root_validator(pre=True, allow_reuse=True)
    def validate_lookback_or_reference_point_set(cls, values):
        # TODO use field aliases after upgrading pydantic version
        #  https://docs.pydantic.dev/2.3/usage/fields/#aliaspath-and-aliaschoices
        lookback = values.get('lookback')
        reference_point = values.get('reference_point')

        if reference_point:
            values["lookback"] = reference_point

        if not lookback and not reference_point:
            raise ValueError('For standard deviation thresholds, reference_point is required.')

        return values

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        lkbk = self.lookback.to_datawatch_object()

        thresholds: List[Threshold] = []
        if self.lower_bound is not None:
            lb = SimpleBound(bound_type=SimpleBoundType.LOWER_BOUND_SIMPLE_BOUND_TYPE, value=self.lower_bound)
            lbt = Threshold(standard_deviation_threshold=StandardDeviationThreshold(lookback=lkbk, bound=lb))
            thresholds.append(lbt)
        if self.upper_bound is not None:
            ub = SimpleBound(bound_type=SimpleBoundType.UPPER_BOUND_SIMPLE_BOUND_TYPE, value=self.upper_bound)
            ubt = Threshold(standard_deviation_threshold=StandardDeviationThreshold(lookback=lkbk, bound=ub))
            thresholds.append(ubt)

        return thresholds


class SimpleNoneThreshold(SimpleThreshold, type='NONE'):

    def to_datawatch_object(self, **kwargs) -> List[Threshold]:
        return [Threshold(none_threshold=NoneThreshold())]


SNC = TypeVar('SNC', bound='SimpleNotificationChannel')


class SimpleNotificationChannel(PydanticSubtypeSerializable, DatawatchFacade, ABC):
    type: str

    @classmethod
    def from_datawatch_object(cls, obj: NotificationChannel) -> SNC:
        t = betterproto.which_one_of(obj, "notification_channel")[0]
        if not t:
            t = get_type_from_dict(obj)
        if t == 'email':
            return EmailNotificationChannel(type='EMAIL', email=obj.email)
        elif t == 'slack_channel_info':
            return SlackNotificationChannel(
                channel_id=obj.slack_channel_info.channel_id,
                slack=obj.slack_channel_info.channel_name,
                thread_ts=obj.slack_channel_info.thread_ts
            )
        elif t == 'webhook':
            key: Optional[str] = None
            value: Optional[str] = None
            if obj.webhook.webhook_headers:
                key = obj.webhook.webhook_headers[0].key
                value = obj.webhook.webhook_headers[0].value
            return WebhookNotificationChannel(webhook=obj.webhook.webhook_url,
                                              webhook_header_key=key,
                                              webhook_header_value=value)
        else:
            error_message = f"Notification channel type not supported: {t}"
            raise InvalidConfigurationException(error_message)


class EmailNotificationChannel(SimpleNotificationChannel, type='EMAIL'):
    type: str = 'EMAIL'
    email: str

    def to_datawatch_object(self, **kwargs) -> NotificationChannel:
        return NotificationChannel(email=self.email)


class SlackNotificationChannel(SimpleNotificationChannel, type='SLACK'):
    type: str = 'SLACK'
    slack: str  # TODO alias to channel_name?
    channel_id: str = ''
    thread_ts: str = ''

    @validator('slack')
    def must_have_valid_channel_format(cls, v):
        p = re.compile(r'[#@]\S{1,256}')
        if not re.fullmatch(p, v):
            error_message = FORMATTING_ERRMSG.format(s=v)
            cls.register_validation_error(error_lines=[v],
                                          error_message=error_message)

        return v

    def to_datawatch_object(self, **kwargs) -> NotificationChannel:
        sci = SlackChannelInfo(channel_name=self.slack, channel_id=self.channel_id, thread_ts=self.thread_ts)
        return NotificationChannel(slack_channel_info=sci)


class WebhookNotificationChannel(SimpleNotificationChannel, type='WEBHOOK'):
    type: str = 'WEBHOOK'
    webhook: str
    webhook_header_key: Optional[str] = None
    webhook_header_value: Optional[str] = None

    def to_datawatch_object(self, **kwargs) -> NotificationChannel:
        if self.webhook_header_key and self.webhook_header_value:
            header = WebhookHeader(key=self.webhook_header_key, value=self.webhook_header_value)
            return NotificationChannel(webhook=Webhook(webhook_url=self.webhook,
                                                       webhook_headers=[header]))
        else:
            return NotificationChannel(webhook=Webhook(webhook_url=self.webhook))


class SimpleMetricParameter(YamlModelWithValidatorContext, DatawatchFacade):
    key: str
    string_value: Optional[str] = None
    column_name: Optional[str] = None
    number_value: Optional[float] = None

    @classmethod
    def from_datawatch_object(cls, obj: MetricParameter) -> SimpleMetricParameter:
        return SimpleMetricParameter(key=obj.key,
                                     string_value=obj.string_value,
                                     column_name=obj.column_name,
                                     number_value=obj.number_value)

    def to_datawatch_object(self, **kwargs) -> MetricParameter:
        # This is required to handle 0 value defaults that get removed when calling to_json
        if self.number_value == 0.0:
            return MetricParameter(key=self.key,
                                   string_value='0.0',
                                   column_name=self.column_name,
                                   number_value=self.number_value)
        else:
            return MetricParameter(key=self.key,
                                   string_value=self.string_value,
                                   column_name=self.column_name,
                                   number_value=self.number_value)


@deprecated('SimpleSLA is deprecated and will be removed in future versions. Use SimpleCollection instead.')
class SimpleSLA(YamlModelWithValidatorContext, DatawatchFacade):
    name: str
    id: int = None
    description: str = None
    metric_ids: List[int] = None
    notification_channels: List[SimpleNotificationChannel] = Field(default_factory=lambda: [])
    muted_until_timestamp: int = 0

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleSLA, attribute_name='metric_ids', values=values)
        must_be_list_validator(clazz=SimpleSLA, attribute_name='notification_channels', values=values)

        return values

    def merge_for_upsert(self, existing: SimpleSLA, overwrite: bool = True) -> SimpleSLA:
        """
        Merges this SLA and existing SLA.  Attributes that will be merged include: notification channels and metric ids.

        If not overwriting: missing names, descriptions, and muted_until_timestamp will be populated with
        existing values.

        If overwriting: (current default strategy) new attributes will replace the old -- even if empty.

        Args:
            existing: the existing SLA to merge this new SLA with.
            overwrite: true/false

        Returns: The merged SLA

        """
        new_sla = self.copy(deep=True)

        # set existing SLA ID.
        new_sla.id = existing.id

        if not overwrite:
            """If we are not overwriting then we want to merge notification channels and metric ids."""
            if not new_sla.name:
                new_sla.name = existing.name

            if not new_sla.description:
                new_sla.description = existing.description

            if not new_sla.muted_until_timestamp:
                new_sla.muted_until_timestamp = existing.muted_until_timestamp

            if new_sla.notification_channels:
                new_sla.notification_channels.extend(existing.notification_channels)
            else:
                new_sla.notification_channels = existing.notification_channels

            if new_sla.metric_ids:
                new_sla.metric_ids.extend(existing.metric_ids)
            else:
                new_sla.metric_ids = existing.metric_ids

        return new_sla

    @classmethod
    def from_datawatch_object(cls, obj: Collection) -> SimpleSLA:
        sla = SimpleSLA(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            metric_ids=obj.metric_ids,
            muted_until_timestamp=obj.muted_until_timestamp
        )

        if obj.notification_channels:
            sla.notification_channels = [SimpleNotificationChannel.from_datawatch_object(nc)
                                         for nc in obj.notification_channels]

        return sla

    def to_datawatch_object(self) -> Collection:
        c = Collection(
            id=self.id,
            name=self.name,
            description=self.description if self.description else "SDK Generated.",
            metric_ids=self.metric_ids,
            notification_channels=[nc.to_datawatch_object() for nc in self.notification_channels],
            muted_until_timestamp=self.muted_until_timestamp
        )

        return c

    def to_simple_collection(self) -> SimpleCollection:
        return SimpleCollection.parse_obj(self)


class SimpleCollection(YamlModelWithValidatorContext, DatawatchFacade):
    name: str
    id: int = None
    description: str = None
    metric_ids: List[int] = None
    notification_channels: List[SimpleNotificationChannel] = Field(default_factory=lambda: [])
    muted_until_timestamp: int = 0

    def __eq__(self, other: SimpleCollection):
        if self.name == other.name \
                and self.description == other.description \
                and self.metric_ids == other.metric_ids \
                and self.notification_channels == other.notification_channels \
                and self.muted_until_timestamp == other.muted_until_timestamp:
            return True
        else:
            return False

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleCollection, attribute_name='metric_ids', values=values)
        must_be_list_validator(clazz=SimpleCollection, attribute_name='notification_channels', values=values)

        return values

    def merge_for_upsert(self, existing: SimpleCollection) -> SimpleCollection:
        """
        Merges this collection and existing collection.  Attributes that will be merged include: notification channels and metric ids.

        If not overwriting: missing names, descriptions, and muted_until_timestamp will be populated with
        existing values.

        If overwriting: (current default strategy) new attributes will replace the old -- even if empty.

        Args:
            existing: the existing collection to merge this new collection with.
            overwrite: true/false

        Returns: The merged collection

        """
        new_collection = self.copy(deep=True)

        # set existing SLA ID.
        new_collection.id = existing.id

        """We match on name. If users want to edit description or the muted_until_timestamp values."""
        if not new_collection.description:
            new_collection.description = existing.description

        if not new_collection.muted_until_timestamp:
            new_collection.muted_until_timestamp = existing.muted_until_timestamp

        """Notification channels are missing because those will always be controlled by incoming bigconfig."""

        """This will ensure that the collection will retain metrics when the above fields are updated."""
        if new_collection.metric_ids:
            new_collection.metric_ids.extend(existing.metric_ids)
        else:
            new_collection.metric_ids = existing.metric_ids

        return new_collection

    @classmethod
    def from_datawatch_object(cls, obj: Collection) -> SimpleCollection:
        collection = SimpleCollection(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            metric_ids=obj.metric_ids,
            muted_until_timestamp=obj.muted_until_timestamp
        )

        if obj.notification_channels:
            collection.notification_channels = [SimpleNotificationChannel.from_datawatch_object(nc)
                                                for nc in obj.notification_channels]

        return collection

    def to_datawatch_object(self) -> Collection:
        c = Collection(
            id=self.id,
            name=self.name,
            description=self.description if self.description else "SDK Generated.",
            metric_ids=self.metric_ids,
            notification_channels=[nc.to_datawatch_object() for nc in self.notification_channels],
            muted_until_timestamp=self.muted_until_timestamp
        )

        return c


class BucketSize(YamlStrEnum):
    DAY = "DAY"  # 86400
    HOUR = "HOUR"  # 3600

    def to_seconds(self):
        if self == BucketSize.DAY:
            return 86400
        elif self == BucketSize.HOUR:
            return 3600
        else:
            return 86400  # defaults to day.

    @classmethod
    def from_seconds(cls, seconds: int) -> Union[int, BucketSize]:
        if seconds == 86400:
            return BucketSize.DAY
        elif seconds == 3600:
            return BucketSize.HOUR
        else:
            return seconds


class SimpleLookback(YamlModelWithValidatorContext):
    lookback_window: Optional[SimpleTimeInterval] = SimpleTimeInterval(interval_type=SimpleTimeIntervalType.DAYS,
                                                                       interval_value=2)
    lookback_type: Optional[SimpleLookbackType] = SimpleLookbackType.METRIC_TIME
    bucket_size: Optional[Union[int, BucketSize]] = BucketSize.DAY


class SimpleMetricDefinition(YamlModelWithValidatorContext, DatawatchFacade):
    saved_metric_id: Optional[str] = None
    metric_type: SimpleMetricType = None
    metric_name: Optional[str] = None
    description: Optional[str] = None
    schedule_frequency: Optional[SimpleTimeInterval] = None
    conditions: Optional[List[str]] = None
    group_by: Optional[List[str]] = None
    threshold: Optional[SimpleThreshold] = None
    notification_channels: Optional[List[SimpleNotificationChannel]] = None
    parameters: Optional[List[SimpleMetricParameter]] = None
    lookback: Optional[SimpleLookback] = None
    grain_seconds: Optional[int] = 0
    muted_until_epoch_seconds: Optional[int] = 0
    sla_ids: Optional[List[int]] = Field(default_factory=lambda: [])
    collection_ids: Optional[List[int]] = Field(default_factory=lambda: [])
    metric_schedule: Optional[SimpleMetricSchedule] = None
    user_favorites: Optional[List[str]] = None
    rct_overrides: Optional[List[str]] = None
    owner: Optional[str] = None

    @validator('threshold', always=True, pre=False)
    def set_default_threshold(cls, threshold, values):
        metric_type: str = values.get('metric_type')

        if threshold:
            """For the case that a user has specifically defined a metric"""
            return threshold
        elif not metric_type:
            """For the case where this is a saved metric reference."""
            return threshold
        elif metric_type \
                and metric_type.type == 'PREDEFINED' \
                and metric_type in SimpleMetricType.get_freshness_metric_types() \
                and not threshold:
            """Standard is that freshness thresholds always are medium autothresholds with upper bound only."""
            threshold = SimpleAutoThreshold(type='AUTO',
                                            sensitivity=SimpleAutothresholdSensitivity.MEDIUM,
                                            upper_bound_only=True
                                            )
        else:
            """otherwise, if no threshold entered, then should default to a medium autothreshold with upper and
            lower bounds."""
            threshold = SimpleAutoThreshold(type='AUTO',
                                            sensitivity=SimpleAutothresholdSensitivity.MEDIUM,
                                            upper_bound_only=False)

        return threshold

    @root_validator(pre=False)
    def set_default_schedule_frequency(cls, values):
        # TODO: This will change when only utilizing MetricSchedule as part of the MetricConfiguration
        metric_type: str = values.get('metric_type')

        if values.get('schedule_frequency'):
            """For the case that a user has specifically defined a metric"""
            return values
        elif values.get('metric_schedule'):
            """For the case that a user has defined a metric_schedule"""
            return values
        elif not metric_type:
            """For the case where this is a saved metric reference."""
            return values
        elif metric_type \
                and metric_type in SimpleMetricType.get_freshness_metric_types():
            """Freshness metrics should execute every 6 hours by default WIZ-1623"""
            values['schedule_frequency'] = SimpleTimeInterval(
                interval_type=SimpleTimeIntervalType.HOURS, interval_value=6
            )
            return values
        elif metric_type \
                and SimpleMetricType.is_freshness_volume(metric_type):
            """Freshness and volume should execute every 6 hours by default"""
            values['schedule_frequency'] = SimpleTimeInterval(
                interval_type=SimpleTimeIntervalType.HOURS, interval_value=6
            )
            return values
        else:
            """All other metrics should execute every 24 hours by default WIZ-1623"""
            values['schedule_frequency'] = SimpleTimeInterval(
                interval_type=SimpleTimeIntervalType.HOURS, interval_value=24
            )
            return values

    def get_error_lines(self) -> List[str]:
        """
        Override from super.  Returns object serialized to yaml and split to lines.  Used to search files.  If this is
        a saved metric, it returns the saved_metric_id dict because that is what the original file would have contained.
        Otherwise, it returns a full object as string broken down by lines.
        Returns: List of yaml string lines.

        """
        if self.saved_metric_id:
            return safe_split_dict_entry_lines('saved_metric_id', self.saved_metric_id)
        else:
            data = self.json(
                exclude_unset=True, exclude_defaults=True, exclude_none=True, indent=True
            )
            return yaml.safe_dump(json.loads(data)).splitlines()

    @validator('metric_type', pre=True)
    def must_be_dict_type(cls, metric_type):
        if isinstance(metric_type, (SimplePredefinedMetric, SimpleTemplateMetric)):
            return metric_type

        if metric_type and not isinstance(metric_type, dict):
            errlns = yaml.safe_dump({'metric_type': metric_type}, indent=True, sort_keys=False)
            SimpleMetricDefinition.register_validation_error(
                error_lines=[errlns],
                error_message=FORMATTING_ERRMSG.format(
                    s='Metric Type is an object.')
            )

            return {'type': 'PREDEFINED', 'predefined_metric': 'UNDEFINED'}

        return metric_type

    @root_validator(pre=True)
    def must_be_list(cls, values):
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='collection_ids', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='sla_ids', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='conditions', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='group_by', values=values)
        must_be_list_validator(clazz=SimpleMetricDefinition, attribute_name='parameters', values=values)

        return values

    @root_validator(pre=True)
    def warn_and_use_collection(cls, values):
        if values.get('sla_ids'):
            log.warning(
                'sla_id class variable is deprecated and will be removed in future versions. Use collection_ids.')
            values['collection_ids'] = values['sla_ids']

        return values

    @root_validator(pre=True)
    def schedule_check(cls, values):
        sf = values.get('schedule_frequency')
        ms = values.get('metric_schedule')
        if sf and ms:
            errlns = [yaml.safe_dump({'schedule_frequency': sf}, indent=True, sort_keys=False),
                      yaml.safe_dump({'metric_schedule': ms}, indent=True, sort_keys=False)]
            cls.register_validation_error(
                error_lines=errlns,
                error_message=TWO_SCHEDULES_DEFINED
            )
        return values

    def deployment_validations(self, config_error_lines: List[str]):
        """
        Runs all deployment validations for SimpleMetricDefinitions
        Args:
            config_error_lines: The configuration serialized to yaml and split to lines.

        Returns: None
        """
        self.deployments_must_have_metric_type_if_not_saved_metric_id(config_error_lines=config_error_lines)
        self.deployments_cannot_have_metric_type_if_has_saved_metric_id(config_error_lines=config_error_lines)
        self.deployments_freshness_metrics_must_have_valid_lookback_type(config_error_lines=config_error_lines)

    def deployments_must_have_metric_type_if_not_saved_metric_id(self, config_error_lines: List[str]):
        """
        Metric definitions must have a metric type if not referencing a saved metric by id
        (deployment in-line metrics)
        Args:
            config_error_lines: The configuration serialized to yaml and split to lines.

        Returns: None
        """
        if not self.saved_metric_id and not self.metric_type:
            error_message = MUST_HAVE_METRIC_TYPE_ERRMSG.format(config_error_lines=config_error_lines)
            self.register_validation_error(error_lines=self.get_error_lines(),
                                           error_context_lines=config_error_lines,
                                           error_message=error_message)

    def deployments_cannot_have_metric_type_if_has_saved_metric_id(self, config_error_lines: List[str]):
        """Metric definitions cannot have a metric_ type if referencing a saved_metric_id but no metric_type
            (deployment reference of saved metric)
        Args:
            config_error_lines: The configuration serialized to yaml and split to lines.

        Returns: None
        """
        if self.saved_metric_id and self.metric_type:
            error_message = OVERRIDE_METRIC_TYPE_SAVED_METRIC_ERRMSG.format(config_error_lines=config_error_lines)
            self.register_validation_error(error_lines=self.get_error_lines(),
                                           error_context_lines=config_error_lines,
                                           error_message=error_message)

    def deployments_freshness_metrics_must_have_valid_lookback_type(self, config_error_lines: List[str]):
        """
        Freshness metrics must have a data time window type. If any other window type is chosen then log
        a warning message. The valid lookback type is automatically applied to the  metric in the backend, 
        but user should be informed of this to limit confusion. 

        See https://linear.app/torodata/issue/WIZ-2583/[061223]-metric-deployed-via-bigconfig-not-showing-as-clock-time

        Args:
            config_error_lines: The configuration serialized to yaml and split to lines.

        Returns: None
        """
        if SimpleMetricType.is_freshness_metric(self.metric_type) \
                and self.lookback \
                and self.lookback.lookback_type != SimpleLookbackType.DATA_TIME:
            if self.saved_metric_id:
                log.warning(
                    f'Invalid freshness metric configuration. Saved metric id: {self.saved_metric_id} was given a '
                    f'lookback of type {self.lookback.lookback_type.name}. This will be changed to '
                    f'type {SimpleLookbackType.DATA_TIME}')
            else:
                log.warning(
                    f'Invalid freshness metric configuration. Metric: {self.metric_type} was given a lookback of '
                    f'type {self.lookback.lookback_type.name}. This will be changed to '
                    f'type {SimpleLookbackType.DATA_TIME}')

    def saved_metrics_must_have_id(self, config_error_lines: List[str]):
        """
        Saved Metric Definitions must have a saved metric id.
        Args:
            config_error_lines: The configuration serialized to yaml and split to lines.

        Returns: None
        """
        if not self.saved_metric_id:
            error_mesage = MUST_HAVE_METRIC_ID_ERRMSG.format(config_error_lines=config_error_lines)
            self.register_validation_error(error_lines=self.get_error_lines(),
                                           error_context_lines=config_error_lines,
                                           error_message=error_mesage)

    @classmethod
    def from_datawatch_object(cls, obj: Union[MetricDefinition, MetricConfiguration]) -> SimpleMetricDefinition:
        builder = SimpleMetricDefinition()
        builder.metric_type: str = SimpleMetricType.from_datawatch_object(obj.metric_type)
        builder.metric_name = obj.name
        builder.description = obj.description

        builder.schedule_frequency = SimpleTimeInterval.from_datawatch_object(obj.schedule_frequency)

        builder.conditions = obj.filters
        builder.group_by = obj.group_bys

        if obj.thresholds:
            builder.threshold = SimpleThreshold.from_datawatch_object(obj.thresholds)

        builder.notification_channels = [SimpleNotificationChannel.from_datawatch_object(nc)
                                         for nc in obj.notification_channels]

        builder.parameters = [SimpleMetricParameter.from_datawatch_object(p) for p in obj.parameters]

        if obj.lookback_type != LookbackType.UNDEFINED_LOOKBACK_TYPE:
            builder.lookback = SimpleLookback(lookback_window=SimpleTimeInterval.from_datawatch_object(obj.lookback),
                                              lookback_type=SimpleLookbackType.from_datawatch_object(obj.lookback_type),
                                              bucket_size=BucketSize.from_seconds(obj.grain_seconds))

        builder.muted_until_epoch_seconds = obj.muted_until_epoch_seconds
        builder.grain_seconds = obj.grain_seconds

        if isinstance(obj, MetricDefinition):
            builder.collection_ids = obj.collection_ids

        builder.metric_schedule = SimpleMetricSchedule.from_datawatch_object(obj.metric_schedule)

        if isinstance(obj, MetricDefinition):
            builder.rct_overrides = obj.rct_overrides
        if isinstance(obj, MetricConfiguration):
            builder.rct_overrides = obj.rct_override.split(",") if obj.rct_override else None

        if isinstance(obj, MetricDefinition) and obj.owner_id:
            builder.owner = str(obj.owner_id)

        return builder

    def to_datawatch_object(self, to_config: bool = False, **kwargs) -> Union[MetricDefinition, MetricConfiguration]:
        if to_config:
            builder = MetricConfiguration()
        else:
            builder = MetricDefinition()

        # Verifying that metric_type has been set before serializing to datawatch object.
        if self.metric_type:
            builder.metric_type: str = self.metric_type.to_datawatch_object()
        else:
            InvalidConfigurationException(
                "Metric Type cannot be None.  Verify that Saved Metric IDs have been applied.")

        builder.name = self.metric_name
        builder.description = self.description

        if self.schedule_frequency:
            builder.schedule_frequency = self.schedule_frequency.to_datawatch_object()

        builder.filters = self.conditions
        builder.group_bys = self.group_by

        if self.threshold:
            builder.thresholds = self.threshold.to_datawatch_object()

        if self.notification_channels:
            builder.notification_channels = [nc.to_datawatch_object() for nc in self.notification_channels]

        if self.parameters:
            builder.parameters = [p.to_datawatch_object() for p in self.parameters]

        if self.lookback:
            if self.lookback.lookback_window:
                builder.lookback = self.lookback.lookback_window.to_datawatch_object()

            if self.lookback.lookback_type:
                builder.lookback_type: str = self.lookback.lookback_type.to_datawatch_object()

            builder.grain_seconds = self.lookback.bucket_size.to_seconds()

        if SimpleMetricType.is_freshness_volume(self.metric_type):
            builder.grain_seconds = BucketSize.HOUR.to_seconds()

        builder.muted_until_epoch_seconds = self.muted_until_epoch_seconds

        if self.collection_ids:
            builder.collection_ids = self.collection_ids
        if self.metric_schedule:
            builder.metric_schedule = self.metric_schedule.to_datawatch_object()

        if self.user_favorites:
            builder.tags.extend(self.user_favorites)
        if self.owner:
            builder.owner_id = int(self.owner)

        if self.rct_overrides:
            if len(self.rct_overrides) == 1 and self.rct_overrides[0] == "FULL_SCAN":
                builder.rct_overrides = ["bigeye-no-rct"]
            else:
                builder.rct_overrides = self.rct_overrides

        return builder
