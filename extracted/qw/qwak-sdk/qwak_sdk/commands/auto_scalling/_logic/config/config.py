from dataclasses import dataclass, field
from enum import Enum
from typing import List

from _qwak_proto.qwak.auto_scaling.v1.auto_scaling_pb2 import (
    AGGREGATION_TYPE_AVERAGE,
    AGGREGATION_TYPE_MAX,
    AGGREGATION_TYPE_MIN,
    AGGREGATION_TYPE_P50,
    AGGREGATION_TYPE_P90,
    AGGREGATION_TYPE_P95,
    AGGREGATION_TYPE_P99,
    AGGREGATION_TYPE_SUM,
    METRIC_TYPE_CPU,
    METRIC_TYPE_ERROR_RATE,
    METRIC_TYPE_GPU,
    METRIC_TYPE_LATENCY,
    METRIC_TYPE_MEMORY,
    METRIC_TYPE_THROUGHPUT,
    AutoScalingConfig,
    PrometheusTrigger,
    QuerySpec,
    Trigger,
    Triggers,
)

from qwak_sdk.exceptions import QwakCommandException


class MetricType(Enum):
    cpu = METRIC_TYPE_CPU
    gpu = METRIC_TYPE_GPU
    latency = METRIC_TYPE_LATENCY
    memory = METRIC_TYPE_MEMORY
    throughput = METRIC_TYPE_THROUGHPUT
    error_rate = METRIC_TYPE_ERROR_RATE

    @classmethod
    def get_metric_type(cls, metric_type: str) -> "MetricType":
        """
        Converts a string representation of a metric type to its corresponding `MetricType` enum.
        The method performs a case-insensitive lookup. If the provided metric type does not exist
        in the `MetricType` enum, a `QwakCommandException` is raised.

        :param metric_type: The name of the metric type to retrieve.
        :return: The corresponding `MetricType` enum.
        :raises: QwakCommandException if the provided `metric_type` does not match any member
        """

        try:
            return cls[metric_type.lower()]
        except KeyError as exception:
            raise QwakCommandException(
                f"The metric type {metric_type} doesn't exist"
            ) from exception


class AggregationType(Enum):
    avg = AGGREGATION_TYPE_AVERAGE
    max = AGGREGATION_TYPE_MAX
    min = AGGREGATION_TYPE_MIN
    sum = AGGREGATION_TYPE_SUM
    p50 = AGGREGATION_TYPE_P50
    p90 = AGGREGATION_TYPE_P90
    p95 = AGGREGATION_TYPE_P95
    p99 = AGGREGATION_TYPE_P99

    @classmethod
    def get_aggregation_type(cls, aggregation_type: str) -> "AggregationType":
        """
        Converts a string representation of an aggregation type to its corresponding `AggregationType` enum.
        The method performs a case-insensitive lookup. If the provided aggregation type does not exist
        in the `AggregationType` enum, a `QwakCommandException` is raised.

        :param aggregation_type: The name of the aggregation type to retrieve
        :return: The corresponding `AggregationType` enum.
        :raises: QwakCommandException if the provided `aggregation_type` does not match
        """
        try:
            return cls[aggregation_type.lower()]
        except KeyError as exception:
            raise QwakCommandException(
                f"The aggregation type {aggregation_type} doesn't exist"
            ) from exception


@dataclass
class AutoScaling:
    @dataclass
    class Triggers:
        @dataclass
        class PrometheusTrigger:
            @dataclass
            class QuerySpec:
                metric_type: str = field(default=None)
                aggregation_type: str = field(default=None)
                time_period: int = field(default=None)
                error_code: str = field(default=None)

            query_spec: QuerySpec = field(default=QuerySpec)
            threshold: int = field(default=None)

        prometheus_trigger: List[PrometheusTrigger] = field(default_factory=list)

    min_replica_count: int = field(default=None)
    max_replica_count: int = field(default=None)
    polling_interval: int = field(default=None)
    cool_down_period: int = field(default=None)
    triggers: Triggers = field(default_factory=Triggers)

    def to_autoscaling_api(self) -> AutoScalingConfig:
        triggers = Triggers()
        for trigger in self.triggers.prometheus_trigger:
            metric_type: MetricType = MetricType.get_metric_type(
                trigger.query_spec.metric_type
            )
            aggregation_type: AggregationType = AggregationType.get_aggregation_type(
                trigger.query_spec.aggregation_type
            )
            triggers.triggers.append(
                Trigger(
                    prometheus_trigger=PrometheusTrigger(
                        query_spec=QuerySpec(
                            metric_type=metric_type.value,
                            aggregation_type=aggregation_type.value,
                            time_period=trigger.query_spec.time_period,
                            error_code=trigger.query_spec.error_code,
                        ),
                        threshold=trigger.threshold,
                    )
                )
            )
        return AutoScalingConfig(
            min_replica_count=self.min_replica_count,
            max_replica_count=self.max_replica_count,
            polling_interval=self.polling_interval,
            cool_down_period=self.cool_down_period,
            triggers=triggers,
        )


@dataclass
class Spec:
    model_id: str = field(default="")
    variation_name: str = field(default="")
    auto_scaling: AutoScaling = field(default=AutoScaling)


@dataclass
class Config:
    spec: Spec = field(default=Spec)
    api_version: str = field(default="v1")
