"""State module for managing Scaling policies."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    auto_scaling_group_name: str,
    resource_id: str = None,
    policy_type: str = None,
    adjustment_type: str = None,
    min_adjustment_step: int = None,
    min_adjustment_magnitude: int = None,
    scaling_adjustment: int = None,
    cooldown: int = None,
    metric_aggregation_type: str = None,
    step_adjustments: List[
        make_dataclass(
            "StepAdjustment",
            [
                ("ScalingAdjustment", int),
                ("MetricIntervalLowerBound", float, field(default=None)),
                ("MetricIntervalUpperBound", float, field(default=None)),
            ],
        )
    ] = None,
    estimated_instance_warmup: int = None,
    target_tracking_configuration: make_dataclass(
        "TargetTrackingConfiguration",
        [
            ("TargetValue", float),
            (
                "PredefinedMetricSpecification",
                make_dataclass(
                    "PredefinedMetricSpecification",
                    [
                        ("PredefinedMetricType", str),
                        ("ResourceLabel", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "CustomizedMetricSpecification",
                make_dataclass(
                    "CustomizedMetricSpecification",
                    [
                        ("MetricName", str),
                        ("Namespace", str),
                        ("Statistic", str),
                        (
                            "Dimensions",
                            List[
                                make_dataclass(
                                    "MetricDimension", [("Name", str), ("Value", str)]
                                )
                            ],
                            field(default=None),
                        ),
                        ("Unit", str, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            ("DisableScaleIn", bool, field(default=None)),
        ],
    ) = None,
    enabled: bool = None,
    predictive_scaling_configuration: make_dataclass(
        "PredictiveScalingConfiguration",
        [
            (
                "MetricSpecifications",
                List[
                    make_dataclass(
                        "PredictiveScalingMetricSpecification",
                        [
                            ("TargetValue", float),
                            (
                                "PredefinedMetricPairSpecification",
                                make_dataclass(
                                    "PredictiveScalingPredefinedMetricPair",
                                    [
                                        ("PredefinedMetricType", str),
                                        ("ResourceLabel", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "PredefinedScalingMetricSpecification",
                                make_dataclass(
                                    "PredictiveScalingPredefinedScalingMetric",
                                    [
                                        ("PredefinedMetricType", str),
                                        ("ResourceLabel", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "PredefinedLoadMetricSpecification",
                                make_dataclass(
                                    "PredictiveScalingPredefinedLoadMetric",
                                    [
                                        ("PredefinedMetricType", str),
                                        ("ResourceLabel", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "CustomizedScalingMetricSpecification",
                                make_dataclass(
                                    "PredictiveScalingCustomizedScalingMetric",
                                    [
                                        (
                                            "MetricDataQueries",
                                            List[
                                                make_dataclass(
                                                    "MetricDataQuery",
                                                    [
                                                        ("Id", str),
                                                        (
                                                            "Expression",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "MetricStat",
                                                            make_dataclass(
                                                                "MetricStat",
                                                                [
                                                                    (
                                                                        "Metric",
                                                                        make_dataclass(
                                                                            "Metric",
                                                                            [
                                                                                (
                                                                                    "Namespace",
                                                                                    str,
                                                                                ),
                                                                                (
                                                                                    "MetricName",
                                                                                    str,
                                                                                ),
                                                                                (
                                                                                    "Dimensions",
                                                                                    List[
                                                                                        make_dataclass(
                                                                                            "MetricDimension",
                                                                                            [
                                                                                                (
                                                                                                    "Name",
                                                                                                    str,
                                                                                                ),
                                                                                                (
                                                                                                    "Value",
                                                                                                    str,
                                                                                                ),
                                                                                            ],
                                                                                        )
                                                                                    ],
                                                                                    field(
                                                                                        default=None
                                                                                    ),
                                                                                ),
                                                                            ],
                                                                        ),
                                                                    ),
                                                                    ("Stat", str),
                                                                    (
                                                                        "Unit",
                                                                        str,
                                                                        field(
                                                                            default=None
                                                                        ),
                                                                    ),
                                                                ],
                                                            ),
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "Label",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "ReturnData",
                                                            bool,
                                                            field(default=None),
                                                        ),
                                                    ],
                                                )
                                            ],
                                        )
                                    ],
                                ),
                                field(default=None),
                            ),
                            (
                                "CustomizedLoadMetricSpecification",
                                make_dataclass(
                                    "PredictiveScalingCustomizedLoadMetric",
                                    [("MetricDataQueries", List["MetricDataQuery"])],
                                ),
                                field(default=None),
                            ),
                            (
                                "CustomizedCapacityMetricSpecification",
                                make_dataclass(
                                    "PredictiveScalingCustomizedCapacityMetric",
                                    [("MetricDataQueries", List["MetricDataQuery"])],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
            ),
            ("Mode", str, field(default=None)),
            ("SchedulingBufferTime", int, field(default=None)),
            ("MaxCapacityBreachBehavior", str, field(default=None)),
            ("MaxCapacityBuffer", int, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """Creates or updates a scaling policy for an Auto Scaling group.

    Scaling policies are used to scale an Auto Scaling group based on configurable metrics. If no policies are defined,
    the dynamic scaling and predictive scaling features are not used.

    For more information about using dynamic scaling, see Target tracking scaling policies and Step and simple scaling
    policies in the Amazon EC2 Auto Scaling User Guide.

    For more information about using predictive scaling, see Predictive scaling for Amazon EC2 Auto Scaling in the
    Amazon EC2 Auto Scaling User Guide.

    You can view the scaling policies for an Auto Scaling group using the DescribePolicies API
    call. If you are no longer using a scaling policy, you can delete it by calling the DeletePolicy API.

    Args:
        name(str):
            The name of the scaling policy.

        auto_scaling_group_name(str):
            The name of the Auto Scaling group.

        resource_id(str, Optional):
            policy name of an autoScalingGroup's policy.

        policy_type(str, Optional):
            One of the following policy types:
                * TargetTrackingScaling
                * StepScaling
                * SimpleScaling (default)
                * PredictiveScaling.

        adjustment_type(str, Optional):
            Specifies how the scaling adjustment is interpreted (for example, an absolute number or a
            percentage). The valid values are ChangeInCapacity, ExactCapacity, and PercentChangeInCapacity.

            Required if the policy type is StepScaling or SimpleScaling. For more information, see Scaling
            adjustment types in the Amazon EC2 Auto Scaling User Guide.
            Defaults to None.

        min_adjustment_step(int, Optional):
            Available for backward compatibility. Use MinAdjustmentMagnitude instead. Defaults to None.

        min_adjustment_magnitude(int, Optional):
            The minimum value to scale by when the adjustment type is PercentChangeInCapacity. For example,
            suppose that you create a step scaling policy to scale out an Auto Scaling group by 25 percent
            and you specify a MinAdjustmentMagnitude of 2. If the group has 4 instances and the scaling
            policy is performed, 25 percent of 4 is 1. However, because you specified a MinAdjustmentMagnitude of 2,
            Amazon EC2 Auto Scaling scales out the group by 2 instances.

            Valid only if the policy type is StepScaling or SimpleScaling. For more information, see Scaling
            adjustment types in the Amazon EC2 Auto Scaling User Guide.

            .. Note::
                Some Auto Scaling groups use instance weights. In this case, set the MinAdjustmentMagnitude to a value
                that is at least as large as your largest instance weight.

            Defaults to None.

        scaling_adjustment(int, Optional):
            The amount by which to scale, based on the specified adjustment type. A positive value adds to the current
            capacity while a negative number removes from the current capacity. For exact capacity, you must specify a
            positive value.

            Required if the policy type is SimpleScaling. (Not used with any other policy type.)
            Defaults to None.

        cooldown(int, Optional):
            The duration of the policy's cooldown period, in seconds. When a cooldown period is specified here, it
            overrides the default cooldown period defined for the Auto Scaling group.

            Valid only if the policy type is SimpleScaling. For more information, see Scaling cooldowns for Amazon EC2
            Auto Scaling in the Amazon EC2 Auto Scaling User Guide.

            Defaults to None.

        metric_aggregation_type(str, Optional):
            The aggregation type for the CloudWatch metrics. The valid values are Minimum, Maximum, and
            Average. If the aggregation type is null, the value is treated as Average.

            Valid only if the policy type is StepScaling. Defaults to None.

        step_adjustments(list[dict[str, Any]], Optional):
            A set of adjustments that enable you to scale based on the size of the alarm breach.

            Required if the policy type is StepScaling. (Not used with any other policy type.) Defaults to None.

            * MetricIntervalLowerBound (float, Optional):
                The lower bound for the difference between the alarm threshold and the CloudWatch metric. If the
                metric value is above the breach threshold, the lower bound is inclusive (the metric must be
                greater than or equal to the threshold plus the lower bound). Otherwise, it is exclusive (the
                metric must be greater than the threshold plus the lower bound). A null value indicates negative
                infinity.

            * MetricIntervalUpperBound (float, Optional):
                The upper bound for the difference between the alarm threshold and the CloudWatch metric. If the
                metric value is above the breach threshold, the upper bound is exclusive (the metric must be
                less than the threshold plus the upper bound). Otherwise, it is inclusive (the metric must be
                less than or equal to the threshold plus the upper bound). A null value indicates positive
                infinity.

                The upper bound must be greater than the lower bound.

            * ScalingAdjustment (int):
                The amount by which to scale, based on the specified adjustment type. A positive value adds to
                the current capacity while a negative number removes from the current capacity.

        estimated_instance_warmup(int, Optional):
            The estimated time, in seconds, until a newly launched instance can contribute to the CloudWatch
            metrics. This warm-up period applies to instances launched due to a specific target tracking or step
            scaling policy. When a warm-up period is specified here, it overrides the default instance warmup.

            Valid only if the policy type is TargetTrackingScaling or StepScaling. Defaults to None.

            .. Note::
                The default is to use the value for the default instance warmup defined for the group. If default
                instance warmup is null, then EstimatedInstanceWarmup falls back to the value of default cooldown.

        target_tracking_configuration(dict[str, Any], Optional):
            A target tracking scaling policy. Provides support for predefined or custom metrics.

            The following predefined metrics are available:
                * ASGAverageCPUUtilization
                * ASGAverageNetworkIn
                * ASGAverageNetworkOut
                * ALBRequestCountPerTarget

            If you specify ALBRequestCountPerTarget for the metric, you must specify the ResourceLabel parameter with
            the PredefinedMetricSpecification.

            For more information, see TargetTrackingConfiguration in the Amazon EC2 Auto Scaling API
            Reference.

            Required if the policy type is TargetTrackingScaling. Defaults to None.

            * PredefinedMetricSpecification (dict[str, Any], Optional):
                A predefined metric. You must specify either a predefined metric or a customized metric.

                * PredefinedMetricType (str):
                    The metric type. The following predefined metrics are available:

                    * ASGAverageCPUUtilization - Average CPU utilization of the Auto Scaling group.

                    * ASGAverageNetworkIn - Average number of bytes received (per instance per minute) for the Auto
                      Scaling group.

                    * ASGAverageNetworkOut - Average number of bytes sent out (per instance per minute) for the Auto
                      Scaling group.

                    * ALBRequestCountPerTarget - Average Application Load Balancer request count (per target per minute)
                      for your Auto Scaling group.

                * ResourceLabel (str, Optional):
                    A label that uniquely identifies a specific Application Load Balancer target group from which to
                    determine the average request count served by your Auto Scaling group. You can't specify a
                    resource label unless the target group is attached to the Auto Scaling group.

                    You create the resource label by appending the final portion of the load balancer ARN and the
                    final portion of the target group ARN into a single value, separated by a forward slash (/). The
                    format of the resource label is: `app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/
                    943f017f100becff`.

                    Where:

                    * app/<load-balancer-name>/<load-balancer-id> is the final portion of the load balancer ARN
                    * targetgroup/<target-group-name>/<target-group-id> is the final portion of the target group ARN.

                    To find the ARN for an Application Load Balancer, use the DescribeLoadBalancers API operation. To
                    find the ARN for the target group, use the DescribeTargetGroups API operation.

            * CustomizedMetricSpecification (dict[str, Any], Optional):
                A customized metric. You must specify either a predefined metric or a customized metric.

                * MetricName (str):
                    The name of the metric. To get the exact metric name, namespace, and dimensions, inspect the Metric
                    object that is returned by a call to ListMetrics.

                * Namespace (str):
                    The namespace of the metric.

                * Dimensions (list[dict[str, Any]], Optional):
                    The dimensions of the metric.

                    Conditional: If you published your metric with dimensions, you must specify the same dimensions in
                    your scaling policy.

                    * Name (str):
                        The name of the dimension.
                    * Value (str):
                        The value of the dimension.

                * Statistic (str):
                    The statistic of the metric.

                * Unit (str, Optional):
                    The unit of the metric. For a complete list of the units that CloudWatch supports, see the
                    MetricDatum data type in the Amazon CloudWatch API Reference.

            * TargetValue (float):
                The target value for the metric.

                .. Note::
                    Some metrics are based on a count instead of a percentage, such as the request count for an
                    Application Load Balancer or the number of messages in an SQS queue. If the scaling policy
                    specifies one of these metrics, specify the target utilization as the optimal average request or
                    message count per instance during any one-minute interval.

            * DisableScaleIn (bool, Optional):
                Indicates whether scaling in by the target tracking scaling policy is disabled. If scaling in is
                disabled, the target tracking scaling policy doesn't remove instances from the Auto Scaling
                group. Otherwise, the target tracking scaling policy can remove instances from the Auto Scaling
                group. The default is false.

        enabled(bool, Optional):
            Indicates whether the scaling policy is enabled or disabled. The default is enabled. For more
            information, see Disabling a scaling policy for an Auto Scaling group in the Amazon EC2 Auto
            Scaling User Guide. Defaults to None.

        predictive_scaling_configuration(dict[str, Any], Optional):
            A predictive scaling policy. Provides support for predefined and custom metrics.

            Predefined metrics include CPU utilization, network in/out, and the Application Load Balancer request count.

            For more information, see PredictiveScalingConfiguration in the Amazon EC2 Auto Scaling API Reference.

            Required if the policy type is PredictiveScaling. Defaults to None.

            * MetricSpecifications (list[dict[str, Any]]):
                This structure includes the metrics and target utilization to use for predictive scaling.

                This is an array, but we currently only support a single metric specification. That is, you can
                specify a target value and a single metric pair, or a target value and one scaling metric and
                one load metric.

                * TargetValue (float):
                    Specifies the target utilization.

                    .. Note::
                        Some metrics are based on a count instead of a percentage, such as the request count for an
                        Application Load Balancer or the number of messages in an SQS queue. If the scaling policy
                        specifies one of these metrics, specify the target utilization as the optimal average request
                        or message count per instance during any one-minute interval.

                * PredefinedMetricPairSpecification (dict[str, Any], Optional):
                    The predefined metric pair specification from which Amazon EC2 Auto Scaling determines the
                    appropriate scaling metric and load metric to use.

                    * PredefinedMetricType (str):
                        Indicates which metrics to use. There are two different types of metrics for each metric type:
                        one is a load metric and one is a scaling metric. For example, if the metric type is
                        ASGCPUUtilization, the Auto Scaling group's total CPU metric is used as the load metric, and the
                        average CPU metric is used for the scaling metric.

                    * ResourceLabel (str, Optional):
                        A label that uniquely identifies a specific Application Load Balancer target group from which to
                        determine the total and average request count served by your Auto Scaling group. You can't
                        specify a resource label unless the target group is attached to the Auto Scaling group.

                        You create the resource label by appending the final portion of the load balancer ARN and the
                        final portion of the target group ARN into a single value, separated by a forward slash (/). The
                        format of the resource label is: `app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-group/
                        943f017f100becff`.

                        Where:

                        * app/<load-balancer-name>/<load-balancer-id> is the final portion of the load balancer ARN
                        * targetgroup/<target-group-name>/<target-group-id> is the final portion of the target group ARN

                        To find the ARN for an Application Load Balancer, use the DescribeLoadBalancers API operation.
                        To find the ARN for the target group, use the DescribeTargetGroups API operation.

                * PredefinedScalingMetricSpecification (dict[str, Any], Optional):
                    The predefined scaling metric specification.

                    * PredefinedMetricType (str):
                        The metric type.

                    * ResourceLabel (str, Optional):
                        A label that uniquely identifies a specific Application Load Balancer target group from which to
                        determine the average request count served by your Auto Scaling group. You can't specify a
                        resource label unless the target group is attached to the Auto Scaling group.

                        You create the resource label by appending the final portion of the load balancer ARN and the
                        final portion of the target group ARN into a single value, separated by a forward slash (/).
                        The format of the resource label is: `app/my-alb/778d41231b141a0f/targetgroup/
                        my-alb-target-group/943f017f100becff`.

                        Where:

                        * app/<load-balancer-name>/<load-balancer-id> is the final portion of the load balancer ARN
                        * targetgroup/<target-group-name>/<target-group-id> is the final portion of the target group ARN

                        To find the ARN for an Application Load Balancer, use the DescribeLoadBalancers API operation.
                        To find the ARN for the target group, use the DescribeTargetGroups API operation.

                * PredefinedLoadMetricSpecification (dict[str, Any], Optional):
                    The predefined load metric specification.

                    * PredefinedMetricType (str):
                        The metric type.

                    * ResourceLabel (str, Optional):
                        A label that uniquely identifies a specific Application Load Balancer target group from which to
                        determine the request count served by your Auto Scaling group. You can't specify a resource
                        label unless the target group is attached to the Auto Scaling group.

                        You create the resource label by appending the final portion of the load balancer ARN and the
                        final portion of the target group ARN into a single value, separated by a forward slash (/).
                        The format of the resource label is: `app/my-alb/778d41231b141a0f/targetgroup/my-alb-target-
                        group/943f017f100becff`.

                        Where:

                        * app/<load-balancer-name>/<load-balancer-id> is the final portion of the load balancer ARN
                        * targetgroup/<target-group-name>/<target-group-id> is the final portion of the target group ARN

                        To find the ARN for an Application Load Balancer, use the DescribeLoadBalancers API operation.
                        To find the ARN for the target group, use the DescribeTargetGroups API operation.

                * CustomizedScalingMetricSpecification (dict[str, Any], Optional):
                    The customized scaling metric specification.

                    * MetricDataQueries (list[dict[str, Any]]):
                        One or more metric data queries to provide the data points for a scaling metric. Use multiple
                        metric data queries only if you are performing a math expression on returned data.

                        * Id (str):
                            A short name that identifies the object's results in the response. This name must be unique
                            among all MetricDataQuery objects specified for a single scaling policy. If you are
                            performing math expressions on this set of data, this name represents that data and can
                            serve as a variable in the mathematical expression. The valid characters are letters,
                            numbers, and underscores. The first character must be a lowercase letter.

                        * Expression (str, Optional):
                            The math expression to perform on the returned data, if this object is performing a math
                            expression. This expression can use the Id of the other metrics to refer to those metrics,
                            and can also use the Id of other expressions to use the result of those expressions.

                            Conditional: Within each MetricDataQuery object, you must specify either Expression or
                            MetricStat, but not both.

                        * MetricStat (dict[str, Any], Optional):
                            Information about the metric data to return.

                            Conditional: Within each MetricDataQuery object, you must specify either Expression or
                            MetricStat, but not both.

                            * Metric (dict[str, Any]):
                                The CloudWatch metric to return, including the metric name, namespace, and dimensions.
                                To get the exact metric name, namespace, and dimensions, inspect the Metric object that
                                is returned by a call to ListMetrics.

                                * Namespace (str):
                                    The namespace of the metric. For more information, see the table in Amazon Web
                                    Services services that publish CloudWatch metrics  in the Amazon CloudWatch User
                                    Guide.

                                * MetricName (str):
                                    The name of the metric.

                                * Dimensions (list[dict[str, Any]], Optional):
                                    The dimensions for the metric. For the list of available dimensions, see the Amazon
                                    Web Services documentation available from the table in Amazon Web Services services
                                    that publish CloudWatch metrics  in the Amazon CloudWatch User Guide.

                                    Conditional: If you published your metric with dimensions, you must specify the
                                    same dimensions in your scaling policy.

                                    * Name (str):
                                        The name of the dimension.
                                    * Value (str):
                                        The value of the dimension.

                            * Stat (str):
                                The statistic to return. It can include any CloudWatch statistic or extended statistic.
                                For a list of valid values, see the table in Statistics in the Amazon CloudWatch User
                                Guide.

                                The most commonly used metrics for predictive scaling are Average and Sum.

                            * Unit (str, Optional):
                                The unit to use for the returned data points. For a complete list of the units that
                                CloudWatch supports, see the MetricDatum data type in the Amazon CloudWatch API
                                Reference.

                        * Label (str, Optional):
                            A human-readable label for this metric or expression. This is especially useful if this is a
                            math expression, so that you know what the value represents.

                        * ReturnData (bool, Optional):
                            Indicates whether to return the timestamps and raw data values of this metric.

                            If you use any math expressions, specify true for this value for only the final math
                            expression that the metric specification is based on. You must specify false for ReturnData
                            for all the other metrics and expressions used in the metric specification.

                            If you are only retrieving metrics and not performing any math expressions, do not specify
                            anything for ReturnData. This sets it to its default (true).

                * CustomizedLoadMetricSpecification (dict[str, Any], Optional):
                    The customized load metric specification.

                    * MetricDataQueries (list['MetricDataQuery']):
                        One or more metric data queries to provide the data points for a load metric. Use multiple
                        metric data queries only if you are performing a math expression on returned data.

                * CustomizedCapacityMetricSpecification (dict[str, Any], Optional):
                    The customized capacity metric specification.

                    * MetricDataQueries (list['MetricDataQuery']):
                        One or more metric data queries to provide the data points for a capacity metric. Use multiple
                        metric data queries only if you are performing a math expression on returned data.

            * Mode (str, Optional):
                The predictive scaling mode. Defaults to ForecastOnly if not specified.

            * SchedulingBufferTime (int, Optional):
                The amount of time, in seconds, by which the instance launch time can be advanced. For example,
                the forecast says to add capacity at 10:00 AM, and you choose to pre-launch instances by 5
                minutes. In that case, the instances will be launched at 9:55 AM. The intention is to give
                resources time to be provisioned. It can take a few minutes to launch an EC2 instance. The
                actual amount of time required depends on several factors, such as the size of the instance and
                whether there are startup scripts to complete.

                The value must be less than the forecast interval duration of 3600 seconds (60 minutes). Defaults to
                300 seconds if not specified.

            * MaxCapacityBreachBehavior (str, Optional):
                Defines the behavior that should be applied if the forecast capacity approaches or exceeds the
                maximum capacity of the Auto Scaling group. Defaults to HonorMaxCapacity if not specified.

                The following are possible values:

                * HonorMaxCapacity - Amazon EC2 Auto Scaling cannot scale out capacity higher than the maximum
                  capacity. The maximum capacity is enforced as a hard limit.

                * IncreaseMaxCapacity - Amazon EC2 Auto Scaling can scale out capacity higher than the maximum
                  capacity when the forecast capacity is close to or exceeds the maximum capacity. The upper limit is
                  determined by the forecasted capacity and the value for MaxCapacityBuffer.

            * MaxCapacityBuffer (int, Optional):
                The size of the capacity buffer to use when the forecast capacity is close to or exceeds the
                maximum capacity. The value is specified as a percentage relative to the forecast capacity. For
                example, if the buffer is 10, this means a 10 percent buffer, such that if the forecast capacity
                is 50, and the maximum capacity is 40, then the effective maximum capacity is 55.

                If set to 0, Amazon EC2 Auto Scaling may scale capacity higher than the maximum capacity to equal but
                not exceed forecast capacity.

                Required if the MaxCapacityBreachBehavior property is set to IncreaseMaxCapacity, and cannot be used
                otherwise.

    Request Syntax:
        .. code-block:: sls

            [scaling_policy_name]:
              aws.autoscaling.scaling_policy.present:
                - name: "string"
                - policy_name: "string"
                - auto_scaling_group_name: "string"
                - policy_type: "string"
                - adjustment_type: "string"
                - min_adjustment_step: "int"
                - min_adjustment_magnitude: "int"
                - scaling_adjustment: "int"
                - cooldown: "int"
                - metric_aggregation_type: "string"
                - step_adjustments:
                    - ScalingAdjustment: "int"
                      MetricIntervalLowerBound: "float"
                      MetricIntervalUpperBound: "float"
                - estimated_instance_warmup: "int"
                - target_tracking_configuration:
                    TargetValue: "float"
                    PredefinedMetricSpecification:
                      PredefinedMetricType: "string"
                      ResourceLabel: "string"
                    CustomizedMetricSpecification:
                      MetricName: "string"
                      Namespace: "string"
                      Statistic:
                        Dimensions:
                          - MetricDimension:
                              - Name: "string"
                                Value: "string"
                      Unit: "string"
                    DisableScaleIn: "boolean"
                - enabled: "boolean"
                - predictive_scaling_configuration:
                    MetricSpecifications:
                      - TargetValue: "float"
                        PredefinedMetricPairSpecification:
                          PredefinedMetricType: "string"
                          ResourceLabel: "string"
                        PredefinedScalingMetricSpecification:
                          PredefinedMetricType: "string"
                          ResourceLabel: "string"
                        PredefinedLoadMetricSpecification:
                          PredefinedMetricType: "string"
                          ResourceLabel: "string"
                        CustomizedScalingMetricSpecification:
                          MetricDataQueries:
                            - Id: "string"
                              Expression: "string"
                              MetricStat:
                                Metric:
                                  Namespace: "string"
                                  MetricName: "string"
                                  Dimensions:
                                    - Name: "string"
                                      Value: "string"
                                Stat: "string"
                                Unit: "string"
                              Label: "string"
                              ReturnData: "string"
                        CustomizedLoadMetricSpecification:
                          MetricDataQueries:
                            - Id: "string"
                              Expression: "string"
                              MetricStat:
                                Metric:
                                  Namespace: "string"
                                  MetricName: "string"
                                  Dimensions:
                                    - Name: "string"
                                      Value: "string"
                                Stat: "string"
                                Unit: "string"
                              Label: "string"
                              ReturnData: "string"
                        CustomizedCapacityMetricSpecification:
                          MetricDataQueries:
                            - Id: "string"
                              Expression: "string"
                              MetricStat:
                                Metric:
                                  Namespace: "string"
                                  MetricName: "string"
                                  Dimensions:
                                    - Name: "string"
                                      Value: "string"
                                Stat: "string"
                                Unit: "string"
                              Label: "string"
                              ReturnData: "string"
                    SchedulingBufferTime: "int"
                    MaxCapacityBreachBehavior: "string"
                    MaxCapacityBuffer: "int"


    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_autoscaling_policy:
              aws.autoscaling.scaling_policy.present:
                - auto_scaling_group_name: idem-test-autoscaling-group
                - policy_name: idem-test-scaling-policy
                - policy_type: StepScaling
                - adjustment_type: PercentChangeInCapacity
                - min_adjustment_step: 1
                - min_adjustment_magnitude: 1
                - cooldown: 20
                - metric_aggregation_type: Average
                - enabled: true
                - step_adjustments:
                    - MetricIntervalLowerBound: 0.0
                      MetricIntervalUpperBound: 15.0
                      ScalingAdjustment: 1
                    - MetricIntervalLowerBound: 15.0
                      MetricIntervalUpperBound: 25.0
                      ScalingAdjustment: 2
                    - MetricIntervalLowerBound: 25.0
                      ScalingAdjustment: 3

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    plan_state = None

    if resource_id:
        before = await hub.exec.aws.autoscaling.scaling_policy.get(
            ctx=ctx,
            name=name,
            resource_id=resource_id,
            auto_scaling_group_name=auto_scaling_group_name,
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        update_ret = await hub.tool.aws.autoscaling.scaling_policy.update(
            ctx=ctx,
            name=name,
            resource_id=resource_id,
            before=result["old_state"],
            auto_scaling_group_name=auto_scaling_group_name,
            policy_type=policy_type,
            adjustment_type=adjustment_type,
            min_adjustment_step=min_adjustment_step,
            min_adjustment_magnitude=min_adjustment_magnitude,
            scaling_adjustment=scaling_adjustment,
            cooldown=cooldown,
            metric_aggregation_type=metric_aggregation_type,
            step_adjustments=step_adjustments,
            estimated_instance_warmup=estimated_instance_warmup,
            target_tracking_configuration=target_tracking_configuration,
            enabled=enabled,
            predictive_scaling_configuration=predictive_scaling_configuration,
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            for modified_param in update_ret["ret"]:
                plan_state[modified_param] = update_ret["ret"][modified_param]
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.autoscaling.scaling_policy", name=name
            )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "auto_scaling_group_name": auto_scaling_group_name,
                    "policy_type": policy_type,
                    "adjustment_type": adjustment_type,
                    "min_adjustment_step": min_adjustment_step,
                    "min_adjustment_magnitude": min_adjustment_magnitude,
                    "scaling_adjustment": scaling_adjustment,
                    "cooldown": cooldown,
                    "metric_aggregation_type": metric_aggregation_type,
                    "step_adjustments": step_adjustments,
                    "estimated_instance_warmup": estimated_instance_warmup,
                    "target_tracking_configuration": target_tracking_configuration,
                    "enabled": enabled,
                    "predictive_scaling_configuration": predictive_scaling_configuration,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.autoscaling.scaling_policy", name=name
            )
            return result
        ret = await hub.exec.boto3.client.autoscaling.put_scaling_policy(
            ctx,
            AutoScalingGroupName=auto_scaling_group_name,
            PolicyName=name,
            PolicyType=policy_type,
            AdjustmentType=adjustment_type,
            MinAdjustmentStep=min_adjustment_step,
            MinAdjustmentMagnitude=min_adjustment_magnitude,
            ScalingAdjustment=scaling_adjustment,
            Cooldown=cooldown,
            MetricAggregationType=metric_aggregation_type,
            StepAdjustments=step_adjustments,
            EstimatedInstanceWarmup=estimated_instance_warmup,
            TargetTrackingConfiguration=target_tracking_configuration,
            Enabled=enabled,
            PredictiveScalingConfiguration=predictive_scaling_configuration,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.autoscaling.scaling_policy", name=name
        )
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not result["old_state"]) or resource_updated:
            after = await hub.exec.aws.autoscaling.scaling_policy.get(
                ctx=ctx,
                name=name,
                resource_id=resource_id,
                auto_scaling_group_name=auto_scaling_group_name,
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    auto_scaling_group_name: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the specified scaling policy.

    Deleting either a step scaling policy or a simple scaling policy deletes the underlying alarm action, but does not
    delete the alarm, even if it no longer has an associated action.

    Args:
        name(str):
            The name or Amazon Resource Name (ARN) of the scaling policy.

        auto_scaling_group_name(str, Optional):
            The name of the Auto Scaling group.

        resource_id(str, Optional):
            policy name of an autoScalingGroup's policy.

    Request Syntax:
        .. code-block:: sls

            [rds_scaling_policy_name]:
              aws.autoscaling.scaling_policy.absent:
                - name: 'string'
                - auto_scaling_group_name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            rds_scaling_policy_name:
              aws.autoscaling.scaling_policy.absent:
                - name: rds_scaling_policy
                - auto_scaling_group_name: rds_autoscaling_group
                - resource_id: rds_autoscaling_group/rds_autoscaling_policy
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.autoscaling.scaling_policy", name=name
        )
        return result
    if not auto_scaling_group_name:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.autoscaling.scaling_policy",
            name=name,
            args=["auto_scaling_group_name"],
        )
        result["result"] = False
        return result
    before = await hub.exec.aws.autoscaling.scaling_policy.get(
        ctx=ctx,
        name=name,
        resource_id=resource_id,
        auto_scaling_group_name=auto_scaling_group_name,
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.autoscaling.scaling_policy", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.autoscaling.scaling_policy", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.autoscaling.delete_policy(
            ctx,
            PolicyName=resource_id,
            AutoScalingGroupName=auto_scaling_group_name,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.autoscaling.scaling_policy", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes the AutoScaling scaling policies in the account and Region.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.autoscaling.scaling_policy
    """
    result = {}

    ret = await hub.exec.boto3.client.autoscaling.describe_policies(ctx)
    if not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.autoscaling.scaling_policy. {ret['comment']}"
        )
        return {}
    for scaling_policy in ret["ret"]["ScalingPolicies"]:
        resource_key = f"{scaling_policy.get('AutoScalingGroupName')}/{scaling_policy.get('PolicyName')}"
        resource_translated = hub.tool.aws.autoscaling.conversion_utils.convert_raw_scaling_policy_to_present(
            ctx, raw_resource=scaling_policy
        )
        result[resource_key] = {
            "aws.autoscaling.scaling_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
