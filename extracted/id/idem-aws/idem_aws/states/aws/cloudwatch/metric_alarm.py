"""State module for managing AWS CloudWatch Metric Alarms."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

RESOURCE_TYPE = "aws.cloudwatch.metric_alarm"


async def present(
    hub,
    ctx,
    name: str,
    period: int,
    evaluation_periods: int,
    comparison_operator: str,
    resource_id: str = None,
    alarm_description: str = None,
    actions_enabled: bool = True,
    ok_actions: List[str] = None,
    alarm_actions: List[str] = None,
    insufficient_data_actions: List[str] = None,
    metric_name: str = None,
    namespace: str = None,
    statistic: str = None,
    extended_statistic: str = None,
    dimensions: List[
        make_dataclass("Dimension", [("Name", str), ("Value", str)])
    ] = None,
    unit: str = None,
    datapoints_to_alarm: int = None,
    threshold: float = None,
    treat_missing_data: str = None,
    evaluate_low_sample_count_percentile: str = None,
    metrics: List[
        make_dataclass(
            "MetricDataQuery",
            [
                ("Id", str),
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
                                        ("Namespace", str, field(default=None)),
                                        ("MetricName", str, field(default=None)),
                                        (
                                            "Dimensions",
                                            List[
                                                make_dataclass(
                                                    "Dimension",
                                                    [("Name", str), ("Value", str)],
                                                )
                                            ],
                                            field(default=None),
                                        ),
                                    ],
                                ),
                            ),
                            ("Period", int),
                            ("Stat", str),
                            ("Unit", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("Expression", str, field(default=None)),
                ("Label", str, field(default=None)),
                ("ReturnData", bool, field(default=None)),
                ("Period", int, field(default=None)),
                ("AccountId", str, field(default=None)),
            ],
        )
    ] = None,
    threshold_metric_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
):
    """Creates or updates an alarm and associates it with the specified metric, metric math expression, or anomaly detection model.

    Alarms based on anomaly detection models cannot have Auto Scaling actions.

    When this operation creates an alarm, the alarm state is immediately set to INSUFFICIENT_DATA. The alarm is then
    evaluated and its state is set appropriately. Any actions associated with the new state are then executed.

    When you update an existing alarm, its state is left unchanged, but the update completely overwrites the previous
    configuration of the alarm.

    If you are an IAM user, you must have Amazon EC2 permissions for some alarm operations:
      * The iam:CreateServiceLinkedRole for all alarms with EC2 actions
      * The iam:CreateServiceLinkedRole to create an alarm with Systems Manager OpsItem actions.

    The first time you create an alarm in the Amazon Web Services Management Console, the CLI, or by using the
    PutMetricAlarm API, CloudWatch creates the necessary service-linked role for you. The service-linked roles are
    called AWSServiceRoleForCloudWatchEvents and AWSServiceRoleForCloudWatchAlarms_ActionSSM.

    Args:
        name(str):
            The name for the alarm. This name must be unique within the Region.

        resource_id(str):
            The AWS name of the metric alarm.

        alarm_description(str, Optional):
            The description for the alarm.

        actions_enabled(bool, Optional):
            Indicates whether actions should be executed during any changes to the alarm state. The default is TRUE.

        ok_actions(list, Optional):
            The actions to execute when this alarm transitions to an OK state from any other state.
            Each action is specified as an Amazon Resource Name (ARN).

            Valid Values:
                * arn:aws:automate:*region*:ec2:stop
                * arn:aws:automate:*region*:ec2:terminate
                * arn:aws:automate:*region*:ec2:recover
                * arn:aws:automate:*region*:ec2:reboot
                * arn:aws:sns:*region*:*account-id*:*sns-topic-name*
                * arn:aws:autoscaling:*region*:*account-id*:scalingPolicy:*policy-id*:autoScalingGroupName/*group-friendly-name*:policyName/*policy-friendly-name*
            Valid Values (for use with IAM roles):
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Stop/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Terminate/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Reboot/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Recover/1.0

        alarm_actions(list, Optional):
            The actions to execute when this alarm transitions to the ALARM state from any other state.
            Each action is specified as an Amazon Resource Name (ARN).

            Valid Values:
                * arn:aws:automate:*region*:ec2:stop
                * arn:aws:automate:*region*:ec2:terminate
                * arn:aws:automate:*region*:ec2:recover
                * arn:aws:automate:*region*:ec2:reboot
                * arn:aws:sns:*region*:*account-id*:*sns-topic-name*
                * arn:aws:autoscaling:*region*:*account-id*:scalingPolicy:*policy-id*:autoScalingGroupName/*group-friendly-name*:policyName/*policy-friendly-name*
                * arn:aws:ssm:*region*:*account-id*:opsitem:*severity*
                * arn:aws:ssm-incidents:*region*:*account-id*:response-plan:*response-plan-name*

            Valid Values (for use with IAM roles):
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Stop/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Terminate/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Reboot/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Recover/1.0

        insufficient_data_actions(list, Optional):
            The actions to execute when this alarm transitions to the INSUFFICIENT_DATA state from any other state.
            Each action is specified as an Amazon Resource Name (ARN).

            Valid Values:
                * arn:aws:automate:*region*:ec2:stop
                * arn:aws:automate:*region*:ec2:terminate
                * arn:aws:automate:*region*:ec2:recover
                * arn:aws:automate:*region*:ec2:reboot
                * arn:aws:sns:*region*:*account-id*:*sns-topic-name*
                * arn:aws:autoscaling:*region*:*account-id*:scalingPolicy:*policy-id*:autoScalingGroupName/*group-friendly-name*:policyName/*policy-friendly-name*

            Valid Values (for use with IAM roles):
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Stop/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Terminate/1.0
                * arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Reboot/1.0

        metric_name(str, Optional):
            The name for the metric associated with the alarm. For each PutMetricAlarm operation, you must specify
            either MetricName or a Metrics array.

        namespace(str, Optional):
            The namespace for the metric associated specified in MetricName.

        statistic(str, Optional):
            The statistic for the metric specified in MetricName , other than percentile. For percentile statistics,
            use ExtendedStatistic. When you call PutMetricAlarm and specify a MetricName, you must specify either
            Statistic or ExtendedStatistic, but not both.

        extended_statistic(str, Optional):
            The percentile statistic for the metric specified in MetricName. Specify a value between p0.0 and p100.
            When you call PutMetricAlarm and specify a MetricName, you must specify either Statistic or
            ExtendedStatistic, but not both.

        dimensions(list[dict[str, Any]], Optional):
            The dimensions for the metric specified in MetricName. Defaults to None.

            * Name (str): The name of the dimension. Dimension names must contain only ASCII characters, must include at
              least one non-whitespace character, and cannot start with a colon (:).

            * Value (str): The value of the dimension. Dimension values must contain only ASCII characters and must
              include at least one non-whitespace character.

        period(int):
            The length, in seconds, used each time the metric specified in MetricName is evaluated.
            Valid values are 10, 30, and any multiple of 60.

        unit(str, Optional):
            The unit of measure for the statistic. For example, the units for the Amazon EC2 NetworkIn metric are
            Bytes because NetworkIn tracks the number of bytes that an instance receives on all network interfaces.
            You can also specify a unit when you create a custom metric. Units help provide conceptual meaning to your
            data. Metric data points that specify a unit of measure, such as Percent, are aggregated separately.

        evaluation_periods(int):
            The number of periods over which data is compared to the specified threshold.
            If you are setting an alarm that requires that a number of consecutive data points be breaching to trigger
            the alarm, this value specifies that number. If you are setting an "M out of N" alarm, this value is the N.

            An alarm's total current evaluation period can be no longer than one day, so this number multiplied by
            Period cannot be more than 86,400 seconds.

        datapoints_to_alarm(int, Optional):
            The number of data points that must be breaching to trigger the alarm.
            This is used only if you are setting an "M out of N" alarm. In that case, this value is the M.

        threshold(float, Optional):
            The value against which the specified statistic is compared.

            This parameter is required for alarms based on static thresholds, but should not be used for alarms based
            on anomaly detection models.

        comparison_operator(str):
            The arithmetic operation to use when comparing the specified statistic and threshold. The specified
            statistic value is used as the first operand.

            The values LessThanLowerOrGreaterThanUpperThreshold, LessThanLowerThreshold, and GreaterThanUpperThreshold
            are used only for alarms based on anomaly detection models.

        treat_missing_data(str, Optional):
            Sets how this alarm is to handle missing data points. If TreatMissingData is omitted, the default behavior
            of missing is used.

            Valid Values: breaching | notBreaching | ignore | missing

        evaluate_low_sample_count_percentile(str, Optional):
            Used only for alarms based on percentiles. If you specify ignore, the alarm state does not change during
            periods with too few data points to be statistically significant. If you specify evaluate or omit this
            parameter, the alarm is always evaluated and possibly changes state no matter how many data points are
            available.

            Valid Values: evaluate | ignore

        metrics(list[dict[str, Any]], Optional):
            An array of MetricDataQuery structures that enable you to create an alarm based on the result of a metric
            math expression. For each PutMetricAlarm operation, you must specify either MetricName or a Metrics array.

            Each item in the Metrics array either retrieves a metric or performs a math expression.

            One item in the Metrics array is the expression that the alarm watches. You
            designate this expression by setting ReturnData to true for this object in the array. For more
            information, see MetricDataQuery.

            If you use the Metrics parameter, you cannot include the MetricName, Dimensions, Period, Namespace,
            Statistic, or ExtendedStatistic parameters of PutMetricAlarm in the same operation. Instead, you retrieve
            the metrics you are using in your math expression as part of the Metrics array.

            Defaults to None.

            * Id (str):
                A short name used to tie this object to the results in the response. This name must be unique
                within a single call to GetMetricData. If you are performing math expressions on this set of
                data, this name represents that data and can serve as a variable in the mathematical expression.
                The valid characters are letters, numbers, and underscore. The first character must be a
                lowercase letter.

            * MetricStat (dict[str, Any], Optional):
                The metric to be returned, along with statistics, period, and units. Use this parameter only if
                this object is retrieving a metric and not performing a math expression on returned data.

                Within one MetricDataQuery object, you must specify either Expression or MetricStat but not both.

                * Metric (dict[str, Any]): The metric to return, including the metric name, namespace, and dimensions.
                    * Namespace (str, Optional): The namespace of the metric.

                    * MetricName (str, Optional): The name of the metric. This is a required field.

                    * Dimensions (list[dict[str, Any]], Optional): The dimensions for the metric.
                        * Name (str): The name of the dimension. Dimension names must contain only ASCII characters,
                          must include at least one non-whitespace character, and cannot start with a colon (:).

                        * Value (str): The value of the dimension. Dimension values must contain only ASCII characters
                          and must include at least one non-whitespace character.

                * Period (int):
                    The granularity, in seconds, of the returned data points. For metrics with regular resolution, a
                    period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution
                    metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30,
                    60, or any multiple of 60. High-resolution metrics are those metrics stored by a PutMetricData call
                    that includes a StorageResolution of 1 second.

                    If the StartTime parameter specifies a time stamp that is greater than 3 hours ago, you must
                    specify the period as follows or no data points in that time range is returned:

                    * Start time between 3 hours and 15 days ago - Use a multiple of 60 seconds (1 minute).
                    * Start time between 15 and 63 days ago - Use a multiple of 300 seconds (5 minutes).
                    * Start time greater than 63 days ago - Use a multiple of 3600 seconds (1 hour).

                * Stat (str):
                    The statistic to return. It can include any CloudWatch statistic or extended statistic.

                * Unit (str, Optional):
                    When you are using a Put operation, this defines what unit you want to use when storing the
                    metric.

                    In a Get operation, if you omit Unit then all data that was collected with any unit is returned,
                    along with the corresponding units that were specified when the data was reported to CloudWatch. If
                    you specify a unit, the operation returns only data that was collected with that unit specified. If
                    you specify a unit that does not match the data collected, the results of the operation are null.
                    CloudWatch does not perform unit conversions.

            * Expression (str, Optional):
                This field can contain either a Metrics Insights query, or a metric math expression to be
                performed on the returned data. For more information about Metrics Insights queries, see Metrics
                Insights query components and syntax in the Amazon CloudWatch User Guide.

                A math expression can use the ID of the other metrics or queries to refer to those metrics, and can
                also use the ID of other expressions to use the result of those expressions. For more information about
                metric math expressions, see Metric Math Syntax and Functions in the Amazon CloudWatch User Guide.

                Within each MetricDataQuery object, you must specify either Expression or MetricStat but not both.

            * Label (str, Optional):
                A human-readable label for this metric or expression. This is especially useful if this is an
                expression, so that you know what the value represents. If the metric or expression is shown in
                a CloudWatch dashboard widget, the label is shown. If Label is omitted, CloudWatch generates a
                default.

                You can put dynamic expressions into a label, so that it is more descriptive. For more information,
                see Using Dynamic Labels.

            * ReturnData (bool, Optional):
                When used in GetMetricData, this option indicates whether to return the timestamps and raw data
                values of this metric. If you are performing this call just to do math expressions and do not
                also need the raw data returned, you can specify False. If you omit this, the default of True is used.

                When used in PutMetricAlarm, specify True for the one expression result to use as the alarm. For all
                other metrics and expressions in the same PutMetricAlarm operation, specify ReturnData as False.

            * Period (int, Optional):
                The granularity, in seconds, of the returned data points. For metrics with regular resolution, a
                period can be as short as one minute (60 seconds) and must be a multiple of 60. For high-resolution
                metrics that are collected at intervals of less than one minute, the period can be 1, 5, 10, 30, 60,
                or any multiple of 60. High-resolution metrics are those metrics stored by a PutMetricData operation
                that includes a StorageResolution of 1 second.

            * AccountId (str, Optional):
                The ID of the account where the metrics are located, if this is a cross-account alarm.

                Use this field only for PutMetricAlarm operations. It is not used in GetMetricData operations.

        tags(list or dict, Optional):
            A List of tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
            {tag-key: tag-value} to associate with the alarm. You can associate as many as 50 tags with
            an alarm.

            Tags can help you organize and categorize your resources. You can also use them to scope user permissions
            by granting a user permission to access or change only resources with certain tag values.

            If you are using this operation to update an existing alarm, any tags you specify in this parameter are
            ignored. To change the tags of an existing alarm, use TagResource or UntagResource. Defaults to None.

            * (Key): A string that you can use to assign a value. The combination of tag keys and values can help you
              organize and categorize your resources.

            * (Value): The value for the specified tag key.

        threshold_metric_id(str):
            If this is an alarm based on an anomaly detection model, make this value match the ID of the
            ANOMALY_DETECTION_BAND function.

            If your alarm uses this parameter, it cannot have Auto Scaling actions.

    Request Syntax:
        .. code-block:: sls

            [metric-alarm-name]:
              aws.cloudwatch.metric_alarm.present:
                - name: 'string'
                - alarm_description: 'string'
                - actions_enabled: True|False
                - ok_actions: ['string']
                - alarm_actions: ['string']
                - insufficient_data_actions: ['string']
                - metric_name: 'string'
                - namespace: 'string'
                - statistic: 'string'
                - dimensions: 'list'
                - period: 'integer'
                - unit: 'string'
                - evaluation_periods: 'integer'
                - datapoints_to_alarm: 'integer'
                - threshold: 'integer'
                - comparison_operator: 'string'
                - treat_missing_data: 'string'
                - evaluate_low_sample_count_percentile: 'string'
                - metrics: 'list'
                - threshold_metric_id: 'string'
                - tags:
                    - Key: 'string'
                      Value: 'string'

    Returns:
         Dict[str, Any]

    Examples:
        .. code-block:: sls

            awsec2-i-0f36e2b10a7463129-LessThanOrEqualToThreshold-CPUUtilization:
              aws.cloudwatch.metric_alarm.present:
                - name: awsec2-i-0f36e2b10a7463129-LessThanOrEqualToThreshold-CPUUtilization
                - alarm_description: "stop EC2 instance if it utilizes CPU less than 5"
                - actions_enabled: True
                - alarm_actions:
                  - arn:aws:swf:*region*:*account-id*:action/actions/AWS_EC2.InstanceId.Stop/1.0
                - insufficient_data_actions: []
                - metric_name: CPUUtilization
                - namespace: AWS/EC2
                - statistic: Average
                - dimensions:
                  - Name: InstanceId
                    Value: i-0f36e2b10a7463129
                - period: 60
                - evaluation_periods: 1
                - datapoints_to_alarm: 1
                - threshold: 20
                - comparison_operator: LessThanThreshold
                - tags:
                  - Key: type
                    Value: metric_alarm

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before = None

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    resource_parameters = {
        "AlarmName": name,
        "AlarmDescription": alarm_description,
        "ActionsEnabled": actions_enabled,
        "OKActions": ok_actions,
        "AlarmActions": alarm_actions,
        "InsufficientDataActions": insufficient_data_actions,
        "MetricName": metric_name,
        "Namespace": namespace,
        "Statistic": statistic,
        "ExtendedStatistic": extended_statistic,
        "Dimensions": dimensions,
        "Period": period,
        "Unit": unit,
        "EvaluationPeriods": evaluation_periods,
        "DatapointsToAlarm": datapoints_to_alarm,
        "Threshold": threshold,
        "ComparisonOperator": comparison_operator,
        "TreatMissingData": treat_missing_data,
        "EvaluateLowSampleCountPercentile": evaluate_low_sample_count_percentile,
        "Metrics": metrics,
        "ThresholdMetricId": threshold_metric_id,
        "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
    }

    if resource_id:
        resource = await hub.tool.boto3.resource.create(
            ctx, "cloudwatch", "Alarm", resource_id
        )
        before = await hub.tool.boto3.resource.describe(resource)

    try:
        if before:
            convert_ret = await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_metric_alarm_to_present_async(
                ctx, raw_resource=before, idem_resource_name=name
            )
            result["result"] = convert_ret["result"]
            if not result["result"]:
                result["comment"] += convert_ret["comment"]
            result["old_state"] = convert_ret["ret"]

            plan_state = copy.deepcopy(result["old_state"])
            # Update metric alarm
            update_ret = await hub.tool.aws.cloudwatch.metric_alarm.update_metric(
                ctx,
                alarm_name=name,
                raw_resource=before,
                resource_parameters=resource_parameters,
            )
            result["comment"] += update_ret["comment"]
            result["result"] = update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if update_ret["ret"] and ctx.get("test", False):
                for key in [
                    "alarm_description",
                    "actions_enabled",
                    "ok_actions",
                    "alarm_actions",
                    "metric_name",
                    "namespace",
                    "statistic",
                    "dimensions",
                    "period",
                    "evaluation_periods",
                    "datapoints_to_alarm",
                    "threshold",
                    "comparison_operator",
                ]:
                    if key in update_ret["ret"]:
                        plan_state[key] = update_ret["ret"][key]
            if tags is not None and tags != result["old_state"].get("tags"):
                # Update tags
                update_tag_ret = (
                    await hub.tool.aws.cloudwatch.metric_alarm.update_metric_tags(
                        ctx=ctx,
                        alarm_arn=before.get("AlarmArn"),
                        old_tags=result["old_state"].get("tags", {}),
                        new_tags=tags,
                    )
                )
                result["result"] = result["result"] and update_tag_ret["result"]
                result["comment"] += update_tag_ret["comment"]
                resource_updated = resource_updated or bool(update_tag_ret["result"])

                if ctx.get("test", False) and update_tag_ret["ret"] is not None:
                    plan_state["tags"] = update_tag_ret["ret"]

            if not resource_updated:
                result["comment"] += [
                    f"aws.cloudwatch.metric_alarm '{name}' already present."
                ]
            else:
                if resource_updated and ctx.get("test", False):
                    result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                        resource_type=RESOURCE_TYPE, name=name
                    )
        else:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "alarm_description": alarm_description,
                        "actions_enabled": actions_enabled,
                        "ok_actions": ok_actions,
                        "alarm_actions": alarm_actions,
                        "insufficient_data_actions": insufficient_data_actions,
                        "metric_name": metric_name,
                        "namespace": namespace,
                        "statistic": statistic,
                        "extended_statistic": extended_statistic,
                        "dimensions": dimensions,
                        "period": period,
                        "unit": unit,
                        "evaluation_periods": evaluation_periods,
                        "datapoints_to_alarm": datapoints_to_alarm,
                        "threshold": threshold,
                        "comparison_operator": comparison_operator,
                        "treat_missing_data": treat_missing_data,
                        "evaluate_low_sample_count_percentile": evaluate_low_sample_count_percentile,
                        "metrics": metrics,
                        "tags": tags,
                        "threshold_metric_id": threshold_metric_id,
                    },
                )
                result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                    resource_type=RESOURCE_TYPE, name=name
                )
                return result

            # Create metric alarm
            ret = await hub.exec.boto3.client.cloudwatch.put_metric_alarm(
                ctx, **resource_parameters
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.create_comment(RESOURCE_TYPE, name)

        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            resource = await hub.tool.boto3.resource.create(
                ctx, "cloudwatch", "Alarm", name
            )
            after = await hub.tool.boto3.resource.describe(resource)
            convert_ret = await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_metric_alarm_to_present_async(
                ctx, raw_resource=after, idem_resource_name=name
            )
            result["result"] = convert_ret["result"]
            if not result["result"]:
                result["comment"] += convert_ret["comment"]
            result["new_state"] = convert_ret["ret"]
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified alarms.

    You can delete up to 100 alarms in one operation. However, this total can include no
    more than one composite alarm. For example, you could delete 99 metric alarms and one composite alarms with one
    operation, but you can't delete two composite alarms with one operation.

    Args:
        name(str): An Idem name of the metric alarm.
        resource_id(str, Optional): The AWS name of the metric alarm. Idem automatically considers this resource
         being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [alarm name]:
               aws.cloudwatch.metric_alarm.absent:
                 - resource_id: value

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            [alarm name]:
               aws.cloudwatch.metric_alarm.absent:
                 - resource_id: value

    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=RESOURCE_TYPE, name=name
        )
        return result
    resource = await hub.tool.boto3.resource.create(
        ctx, "cloudwatch", "Alarm", resource_id
    )
    before = await hub.tool.boto3.resource.describe(resource)

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=RESOURCE_TYPE, name=name
        )
    elif ctx.get("test", False):
        convert_ret = await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_metric_alarm_to_present_async(
            ctx, raw_resource=before, idem_resource_name=name
        )
        result["result"] = convert_ret["result"]
        if not result["result"]:
            result["comment"] += convert_ret["comment"]
        result["old_state"] = convert_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type=RESOURCE_TYPE, name=name
        )
        return result
    else:
        try:
            convert_ret = await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_metric_alarm_to_present_async(
                ctx, raw_resource=before, idem_resource_name=name
            )
            result["result"] = convert_ret["result"]
            if not result["result"]:
                result["comment"] += convert_ret["comment"]
            result["old_state"] = convert_ret["ret"]
            ret = await hub.exec.boto3.client.cloudwatch.delete_alarms(
                ctx, AlarmNames=[resource_id]
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type=RESOURCE_TYPE, name=name
            )

        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Retrieves the specified alarms.

    You can filter the results by specifying a prefix for the alarm name, the alarm state, or a prefix for any action.
    To use this operation and return information about composite alarms, you must be signed on with the
    cloudwatch:DescribeAlarms permission that is scoped to * . You can't return information about composite alarms if
    your cloudwatch:DescribeAlarms permission has a narrower scope.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.cloudwatch.metric_alarm
    """
    result = {}
    ret = await hub.exec.boto3.client.cloudwatch.describe_alarms(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe alarm metrics {ret['comment']}")
        return {}

    for resource in ret["ret"]["MetricAlarms"]:
        alarm_name = resource["AlarmName"]
        convert_ret = await hub.tool.aws.cloudwatch.conversion_utils.convert_raw_metric_alarm_to_present_async(
            ctx, raw_resource=resource, idem_resource_name=alarm_name
        )
        if not convert_ret["result"]:
            hub.log.warning(
                f"Could not describe alarm metrics '{alarm_name}' with error {convert_ret['comment']}"
            )
            continue
        translated_resource = convert_ret["ret"]
        result[translated_resource["resource_id"]] = {
            "aws.cloudwatch.metric_alarm.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
