r'''
# Amazon EventBridge Scheduler Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to `aws-cdk-lib/aws-scheduler`.

[Amazon EventBridge Scheduler](https://aws.amazon.com/blogs/compute/introducing-amazon-eventbridge-scheduler/) is a feature from Amazon EventBridge
that allows you to create, run, and manage scheduled tasks at scale. With EventBridge Scheduler, you can schedule millions of one-time or recurring tasks across various AWS services without provisioning or managing underlying infrastructure.

1. **Schedule**: A schedule is the main resource you create, configure, and manage using Amazon EventBridge Scheduler. Every schedule has a schedule expression that determines when, and with what frequency, the schedule runs. EventBridge Scheduler supports three types of schedules: rate, cron, and one-time schedules. When you create a schedule, you configure a target for the schedule to invoke.
2. **Target**: A target is an API operation that EventBridge Scheduler calls on your behalf every time your schedule runs. EventBridge Scheduler
   supports two types of targets: templated targets and universal targets. Templated targets invoke common API operations across a core groups of
   services. For example, EventBridge Scheduler supports templated targets for invoking AWS Lambda Function or starting execution of Step Functions state
   machine. For API operations that are not supported by templated targets you can use customizable universal targets. Universal targets support calling
   more than 6,000 API operations across over 270 AWS services.
3. **Schedule Group**: A schedule group is an Amazon EventBridge Scheduler resource that you use to organize your schedules. Your AWS account comes
   with a default scheduler group. A new schedule will always be added to a scheduling group. If you do not provide a scheduling group to add to, it
   will be added to the default scheduling group. You can create up to 500 schedule groups in your AWS account. Groups can be used to organize the
   schedules logically, access the schedule metrics and manage permissions at group granularity (see details below). Schedule groups support tagging.
   With EventBridge Scheduler, you apply tags to schedule groups, not to individual schedules to organize your resources.

## Defining a schedule

```python
# fn: lambda.Function


target = targets.LambdaInvoke(fn,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    description="This is a test schedule that invokes a lambda function every 10 minutes."
)
```

### Schedule Expressions

You can choose from three schedule types when configuring your schedule: rate-based, cron-based, and one-time schedules.

Both rate-based and cron-based schedules are recurring schedules. You can configure each recurring schedule type using a schedule expression.

For
cron-based schedules you can specify a time zone in which EventBridge Scheduler evaluates the expression.

```python
# target: targets.LambdaInvoke


rate_based_schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    description="This is a test rate-based schedule"
)

cron_based_schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.cron(
        minute="0",
        hour="23",
        day="20",
        month="11",
        time_zone=TimeZone.AMERICA_NEW_YORK
    ),
    target=target,
    description="This is a test cron-based schedule that will run at 11:00 PM, on day 20 of the month, only in November in New York timezone"
)
```

A one-time schedule is a schedule that invokes a target only once. You configure a one-time schedule by specifying the time of day, date,
and time zone in which EventBridge Scheduler evaluates the schedule.

```python
# target: targets.LambdaInvoke


one_time_schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.at(
        Date(2022, 10, 20, 19, 20, 23), TimeZone.AMERICA_NEW_YORK),
    target=target,
    description="This is a one-time schedule in New York timezone"
)
```

### Grouping Schedules

Your AWS account comes with a default scheduler group. You can access the default group in CDK with:

```python
default_schedule_group = ScheduleGroup.from_default_schedule_group(self, "DefaultGroup")
```

You can add a schedule to a custom scheduling group managed by you. If a custom group is not specified, the schedule is added to the default group.

```python
# target: targets.LambdaInvoke


schedule_group = ScheduleGroup(self, "ScheduleGroup",
    schedule_group_name="MyScheduleGroup"
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    schedule_group=schedule_group
)
```

### Disabling Schedules

By default, a schedule will be enabled. You can disable a schedule by setting the `enabled` property to false:

```python
# target: targets.LambdaInvoke


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    enabled=False
)
```

### Configuring a start and end time of the Schedule

If you choose a recurring schedule, you can set the start and end time of the Schedule by specifying the `start` and `end`.

```python
# target: targets.LambdaInvoke


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(cdk.Duration.hours(12)),
    target=target,
    start=Date("2023-01-01T00:00:00.000Z"),
    end=Date("2023-02-01T00:00:00.000Z")
)
```

## Scheduler Targets

The `@aws-cdk/aws-scheduler-targets-alpha` module includes classes that implement the `IScheduleTarget` interface for
various AWS services. EventBridge Scheduler supports two types of targets:

1. **Templated targets** which invoke common API
   operations across a core groups of services, and
2. **Universal targets** that you can customize to call more
   than 6,000 operations across over 270 services.

A list of supported targets can be found at `@aws-cdk/aws-scheduler-targets-alpha`.

### Input

Targets can be invoked with a custom input. The `ScheduleTargetInput` class supports free-form text input and JSON-formatted object input:

```python
input = ScheduleTargetInput.from_object({
    "QueueName": "MyQueue"
})
```

You can include context attributes in your target payload. EventBridge Scheduler will replace each keyword with
its respective value and deliver it to the target. See
[full list of supported context attributes](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-context-attributes.html):

1. `ContextAttribute.scheduleArn()` – The ARN of the schedule.
2. `ContextAttribute.scheduledTime()` – The time you specified for the schedule to invoke its target, e.g., 2022-03-22T18:59:43Z.
3. `ContextAttribute.executionId()` – The unique ID that EventBridge Scheduler assigns for each attempted invocation of a target, e.g., d32c5kddcf5bb8c3.
4. `ContextAttribute.attemptNumber()` – A counter that identifies the attempt number for the current invocation, e.g., 1.

```python
text = f"Attempt number: {ContextAttribute.attemptNumber}"
input = ScheduleTargetInput.from_text(text)
```

### Specifying an execution role

An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

The classes for templated schedule targets automatically create an IAM role with all the minimum necessary
permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
will grant minimal required permissions. For example, the `LambdaInvoke` target will grant the
IAM execution role `lambda:InvokeFunction` permission to invoke the Lambda function.

```python
# fn: lambda.Function


role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("scheduler.amazonaws.com")
)

target = targets.LambdaInvoke(fn,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    }),
    role=role
)
```

### Specifying an encryption key

EventBridge Scheduler integrates with AWS Key Management Service (AWS KMS) to encrypt and decrypt your data using an AWS KMS key.
EventBridge Scheduler supports two types of KMS keys: AWS owned keys, and customer managed keys.

By default, all events in Scheduler are encrypted with a key that AWS owns and manages.
If you wish you can also provide a customer managed key to encrypt and decrypt the payload that your schedule delivers to its target using the `key` property.
Target classes will automatically add AWS `kms:Decrypt` permission to your schedule's execution role permissions policy.

```python
# key: kms.Key
# fn: lambda.Function


target = targets.LambdaInvoke(fn,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(10)),
    target=target,
    key=key
)
```

> See [Data protection in Amazon EventBridge Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/data-protection.html) for more details.

## Configuring flexible time windows

You can configure flexible time windows by specifying the `timeWindow` property.
Flexible time windows are disabled by default.

```python
# target: targets.LambdaInvoke


schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(12)),
    target=target,
    time_window=TimeWindow.flexible(Duration.hours(10))
)
```

> See [Configuring flexible time windows](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-flexible-time-windows.html) for more details.

## Error-handling

You can configure how your schedule handles failures, when EventBridge Scheduler is unable to deliver an event
successfully to a target, by using two primary mechanisms: a retry policy, and a dead-letter queue (DLQ).

A retry policy determines the number of times EventBridge Scheduler must retry a failed event, and how long
to keep an unprocessed event.

A DLQ is a standard Amazon SQS queue EventBridge Scheduler uses to deliver failed events to, after the retry
policy has been exhausted. You can use a DLQ to troubleshoot issues with your schedule or its downstream target.
If you've configured a retry policy for your schedule, EventBridge Scheduler delivers the dead-letter event after
exhausting the maximum number of retries you set in the retry policy.

```python
# fn: lambda.Function


dlq = sqs.Queue(self, "DLQ",
    queue_name="MyDLQ"
)

target = targets.LambdaInvoke(fn,
    dead_letter_queue=dlq,
    max_event_age=Duration.minutes(1),
    retry_attempts=3
)
```

## Monitoring

You can monitor Amazon EventBridge Scheduler using CloudWatch, which collects raw data
and processes it into readable, near real-time metrics. EventBridge Scheduler emits
a set of metrics for all schedules, and an additional set of metrics for schedules that
have an associated dead-letter queue (DLQ). If you configure a DLQ for your schedule,
EventBridge Scheduler publishes additional metrics when your schedule exhausts its retry policy.

### Metrics for all schedules

The `Schedule` class provides static methods for accessing all schedules metrics with default configuration, such as `metricAllErrors` for viewing errors when executing targets.

```python
cloudwatch.Alarm(self, "SchedulesErrorAlarm",
    metric=Schedule.metric_all_errors(),
    threshold=0,
    evaluation_periods=1
)
```

### Metrics for a Schedule Group

To view metrics for a specific group you can use methods on class `ScheduleGroup`:

```python
schedule_group = ScheduleGroup(self, "ScheduleGroup",
    schedule_group_name="MyScheduleGroup"
)

cloudwatch.Alarm(self, "MyGroupErrorAlarm",
    metric=schedule_group.metric_target_errors(),
    evaluation_periods=1,
    threshold=0
)

# Or use default group
default_schedule_group = ScheduleGroup.from_default_schedule_group(self, "DefaultScheduleGroup")
cloudwatch.Alarm(self, "DefaultScheduleGroupErrorAlarm",
    metric=default_schedule_group.metric_target_errors(),
    evaluation_periods=1,
    threshold=0
)
```

See full list of metrics and their description at
[Monitoring Using CloudWatch Metrics](https://docs.aws.amazon.com/scheduler/latest/UserGuide/monitoring-cloudwatch.html)
in the *AWS EventBridge Scheduler User Guide*.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kms as _aws_cdk_aws_kms_ceddda9d
import aws_cdk.aws_scheduler as _aws_cdk_aws_scheduler_ceddda9d
import constructs as _constructs_77d1e7e8


class ContextAttribute(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ContextAttribute",
):
    '''(deprecated) A set of convenient static methods representing the Scheduler Context Attributes.

    These Context Attributes keywords can be used inside a ScheduleTargetInput.

    :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-context-attributes.html
    :stability: deprecated
    '''

    @jsii.member(jsii_name="fromName")
    @builtins.classmethod
    def from_name(cls, name: builtins.str) -> builtins.str:
        '''(deprecated) Escape hatch for other Context Attributes that may be added in the future.

        :param name: - name will replace xxx in <aws.scheduler.xxx>.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3298180583c0ddbdf4d5fc4310e8726157d1b4b991a42e01360362e1c7d731)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "fromName", [name]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(deprecated) Convert the path to the field in the event pattern to JSON.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="attemptNumber")
    def attempt_number(cls) -> builtins.str:
        '''(deprecated) A counter that identifies the attempt number for the current invocation, for example, 1.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "attemptNumber"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="executionId")
    def execution_id(cls) -> builtins.str:
        '''(deprecated) The unique ID that EventBridge Scheduler assigns for each attempted invocation of a target, for example, d32c5kddcf5bb8c3.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "executionId"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(cls) -> builtins.str:
        '''(deprecated) The ARN of the schedule.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "scheduleArn"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="scheduledTime")
    def scheduled_time(cls) -> builtins.str:
        '''(deprecated) The time you specified for the schedule to invoke its target, for example, 2022-03-22T18:59:43Z.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.sget(cls, "scheduledTime"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.CronOptionsWithTimezone",
    jsii_struct_bases=[_aws_cdk_aws_events_ceddda9d.CronOptions],
    name_mapping={
        "day": "day",
        "hour": "hour",
        "minute": "minute",
        "month": "month",
        "week_day": "weekDay",
        "year": "year",
        "time_zone": "timeZone",
    },
)
class CronOptionsWithTimezone(_aws_cdk_aws_events_ceddda9d.CronOptions):
    def __init__(
        self,
        *,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
    ) -> None:
        '''(deprecated) Options to configure a cron expression.

        All fields are strings so you can use complex expressions. Absence of
        a field implies '*' or '?', whichever one is appropriate.

        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year
        :param time_zone: (deprecated) The timezone to run the schedule in. Default: - TimeZone.ETC_UTC

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions
        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # target: targets.LambdaInvoke
            
            
            rate_based_schedule = Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(10)),
                target=target,
                description="This is a test rate-based schedule"
            )
            
            cron_based_schedule = Schedule(self, "Schedule",
                schedule=ScheduleExpression.cron(
                    minute="0",
                    hour="23",
                    day="20",
                    month="11",
                    time_zone=TimeZone.AMERICA_NEW_YORK
                ),
                target=target,
                description="This is a test cron-based schedule that will run at 11:00 PM, on day 20 of the month, only in November in New York timezone"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b93c2b718a23f23063cb14b1618a13104c926d0bdf7230ce719160d882d285a)
            check_type(argname="argument day", value=day, expected_type=type_hints["day"])
            check_type(argname="argument hour", value=hour, expected_type=type_hints["hour"])
            check_type(argname="argument minute", value=minute, expected_type=type_hints["minute"])
            check_type(argname="argument month", value=month, expected_type=type_hints["month"])
            check_type(argname="argument week_day", value=week_day, expected_type=type_hints["week_day"])
            check_type(argname="argument year", value=year, expected_type=type_hints["year"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if day is not None:
            self._values["day"] = day
        if hour is not None:
            self._values["hour"] = hour
        if minute is not None:
            self._values["minute"] = minute
        if month is not None:
            self._values["month"] = month
        if week_day is not None:
            self._values["week_day"] = week_day
        if year is not None:
            self._values["year"] = year
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def day(self) -> typing.Optional[builtins.str]:
        '''The day of the month to run this rule at.

        :default: - Every day of the month
        '''
        result = self._values.get("day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour(self) -> typing.Optional[builtins.str]:
        '''The hour to run this rule at.

        :default: - Every hour
        '''
        result = self._values.get("hour")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minute(self) -> typing.Optional[builtins.str]:
        '''The minute to run this rule at.

        :default: - Every minute
        '''
        result = self._values.get("minute")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def month(self) -> typing.Optional[builtins.str]:
        '''The month to run this rule at.

        :default: - Every month
        '''
        result = self._values.get("month")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def week_day(self) -> typing.Optional[builtins.str]:
        '''The day of the week to run this rule at.

        :default: - Any day of the week
        '''
        result = self._values.get("week_day")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def year(self) -> typing.Optional[builtins.str]:
        '''The year to run this rule at.

        :default: - Every year
        '''
        result = self._values.get("year")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[_aws_cdk_ceddda9d.TimeZone]:
        '''(deprecated) The timezone to run the schedule in.

        :default: - TimeZone.ETC_UTC

        :stability: deprecated
        '''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.TimeZone], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronOptionsWithTimezone(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.GroupProps",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "removal_policy": "removalPolicy"},
)
class GroupProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param group_name: (deprecated) The name of the schedule group. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated
        :param removal_policy: (deprecated) The removal policy for the group. If the group is removed also all schedules are removed. Default: RemovalPolicy.RETAIN

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_alpha as scheduler_alpha
            import aws_cdk as cdk
            
            group_props = scheduler_alpha.GroupProps(
                group_name="groupName",
                removal_policy=cdk.RemovalPolicy.DESTROY
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e70812dffd651250e3c32989b91d882f629f2973738808560a5d95625eae32a)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the schedule group.

        Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed.

        :default: - A unique name will be generated

        :stability: deprecated
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(deprecated) The removal policy for the group.

        If the group is removed also all schedules are removed.

        :default: RemovalPolicy.RETAIN

        :stability: deprecated
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.IGroup")
class IGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''
    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricSentToDLQTruncated")
    def metric_sent_to_dlq_truncated(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        ...


class _IGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''
    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.IGroup"

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c255656ab6f0e3e078e7dc1cbbab1d697e65780cb1fd98622b8baec835090ab)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0687870c381a3baca7f4b904f4ac04af882c393c4e921edbb46354180efea008)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDeleteSchedules", [identity]))

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4571a0b7363df77ef9266187c2d8848e8e0b8cca1b1f257361cdb5d92b4ee58c)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadSchedules", [identity]))

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc852d9860959f89dec6e107ee923432ec16c8be00fc5dab3b66420d63b4c7b7)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWriteSchedules", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5498dc1be7bc114f9e319e391ca23bdddccb5e44e4c81bce04e4fb998e6c54a)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricAttempts", [props]))

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDropped", [props]))

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581616256867e412b78ad27c6b1df8ab52f755a908f2e868750a96f4ea7d9db6)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQ", [props]))

    @jsii.member(jsii_name="metricSentToDLQTruncated")
    def metric_sent_to_dlq_truncated(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQTruncated", [props]))

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetErrors", [props]))

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetThrottled", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricThrottled", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroup).__jsii_proxy_class__ = lambda : _IGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.ISchedule")
class ISchedule(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(deprecated) Interface representing a created or an imported ``Schedule``.

    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scheduleName")
    def schedule_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[IGroup]:
        '''(deprecated) The schedule group associated with this schedule.

        :deprecated: Use ``scheduleGroup`` instead. ``group`` will be removed when this module is stabilized.

        :stability: deprecated
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scheduleGroup")
    def schedule_group(self) -> typing.Optional["IScheduleGroup"]:
        '''(deprecated) The schedule group associated with this schedule.

        :stability: deprecated
        '''
        ...


class _IScheduleProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(deprecated) Interface representing a created or an imported ``Schedule``.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.ISchedule"

    @builtins.property
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduleName")
    def schedule_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleName"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[IGroup]:
        '''(deprecated) The schedule group associated with this schedule.

        :deprecated: Use ``scheduleGroup`` instead. ``group`` will be removed when this module is stabilized.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[IGroup], jsii.get(self, "group"))

    @builtins.property
    @jsii.member(jsii_name="scheduleGroup")
    def schedule_group(self) -> typing.Optional["IScheduleGroup"]:
        '''(deprecated) The schedule group associated with this schedule.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional["IScheduleGroup"], jsii.get(self, "scheduleGroup"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISchedule).__jsii_proxy_class__ = lambda : _IScheduleProxy


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.IScheduleGroup")
class IScheduleGroup(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    '''(deprecated) Interface representing a created or an imported ``ScheduleGroup``.

    :stability: deprecated
    '''

    @builtins.property
    @jsii.member(jsii_name="scheduleGroupArn")
    def schedule_group_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="scheduleGroupName")
    def schedule_group_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricSentToDLQTruncated")
    def metric_sent_to_dlq_truncated(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        ...


class _IScheduleGroupProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    '''(deprecated) Interface representing a created or an imported ``ScheduleGroup``.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.IScheduleGroup"

    @builtins.property
    @jsii.member(jsii_name="scheduleGroupArn")
    def schedule_group_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduleGroupName")
    def schedule_group_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule group.

        :stability: deprecated
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleGroupName"))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34e07e8a1dfe089f41f512daea38cf3568b9eae574d49317cd3403eab8716360)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9f5c46b8a7eeb02fd0f1ee2f8375cde7e414121ca766da04e2478a30dfeebd8)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDeleteSchedules", [identity]))

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e4ca0890a31ad28043e3b209ff9c88befe72900044a98b367f0c5187d0dbf4)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadSchedules", [identity]))

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35699979ed895e0f4803f54100299062cd002e2176dd7e7c0a27ac9262a00fc8)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWriteSchedules", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612234981843f6273d98d6daf9e74486f3388cd8931cab797f291e54e02c3ac5)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricAttempts", [props]))

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDropped", [props]))

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeb48fb07f0b3ca9ae2a80d69af787e7d8ce6124e2c613eb0e8afcd235229d3e)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQ", [props]))

    @jsii.member(jsii_name="metricSentToDLQTruncated")
    def metric_sent_to_dlq_truncated(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQTruncated", [props]))

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetErrors", [props]))

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetThrottled", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricThrottled", [props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScheduleGroup).__jsii_proxy_class__ = lambda : _IScheduleGroupProxy


@jsii.interface(jsii_type="@aws-cdk/aws-scheduler-alpha.IScheduleTarget")
class IScheduleTarget(typing_extensions.Protocol):
    '''(deprecated) Interface representing a Event Bridge Schedule Target.

    :stability: deprecated
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, _schedule: ISchedule) -> "ScheduleTargetConfig":
        '''(deprecated) Returns the schedule target specification.

        :param _schedule: a schedule the target should be added to.

        :stability: deprecated
        '''
        ...


class _IScheduleTargetProxy:
    '''(deprecated) Interface representing a Event Bridge Schedule Target.

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-scheduler-alpha.IScheduleTarget"

    @jsii.member(jsii_name="bind")
    def bind(self, _schedule: ISchedule) -> "ScheduleTargetConfig":
        '''(deprecated) Returns the schedule target specification.

        :param _schedule: a schedule the target should be added to.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f28f823649c05e2eae45e2c63b5b0684fe861a38416935dbe55bcf0d10451241)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast("ScheduleTargetConfig", jsii.invoke(self, "bind", [_schedule]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IScheduleTarget).__jsii_proxy_class__ = lambda : _IScheduleTargetProxy


@jsii.implements(ISchedule)
class Schedule(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.Schedule",
):
    '''(deprecated) An EventBridge Schedule.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesisfirehose as firehose
        # delivery_stream: firehose.IDeliveryStream
        
        
        payload = {
            "Data": "record"
        }
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.FirehosePutRecord(delivery_stream,
                input=ScheduleTargetInput.from_object(payload)
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        schedule: "ScheduleExpression",
        target: IScheduleTarget,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        end: typing.Optional[datetime.datetime] = None,
        group: typing.Optional[IGroup] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        schedule_group: typing.Optional[IScheduleGroup] = None,
        schedule_name: typing.Optional[builtins.str] = None,
        start: typing.Optional[datetime.datetime] = None,
        time_window: typing.Optional["TimeWindow"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param schedule: (deprecated) The expression that defines when the schedule runs. Can be either a ``at``, ``rate`` or ``cron`` expression.
        :param target: (deprecated) The schedule's target details.
        :param description: (deprecated) The description you specify for the schedule. Default: - no value
        :param enabled: (deprecated) Indicates whether the schedule is enabled. Default: true
        :param end: (deprecated) The date, in UTC, before which the schedule can invoke its target. EventBridge Scheduler ignores end for one-time schedules. Default: - no value
        :param group: (deprecated) The schedule's group. Default: - By default a schedule will be associated with the ``default`` group.
        :param key: (deprecated) The customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data. Default: - All events in Scheduler are encrypted with a key that AWS owns and manages.
        :param schedule_group: (deprecated) The schedule's group. Default: - By default a schedule will be associated with the ``default`` group.
        :param schedule_name: (deprecated) The name of the schedule. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated
        :param start: (deprecated) The date, in UTC, after which the schedule can begin invoking its target. EventBridge Scheduler ignores start for one-time schedules. Default: - no value
        :param time_window: (deprecated) A time window during which EventBridge Scheduler invokes the schedule. Default: TimeWindow.off()

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5630933e51396e7fd66637b557fe7dc9cd565a88ca9ae1d5517435215dbc0220)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduleProps(
            schedule=schedule,
            target=target,
            description=description,
            enabled=enabled,
            end=end,
            group=group,
            key=key,
            schedule_group=schedule_group,
            schedule_name=schedule_name,
            start=start,
            time_window=time_window,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromScheduleArn")
    @builtins.classmethod
    def from_schedule_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        schedule_arn: builtins.str,
    ) -> ISchedule:
        '''(deprecated) Import an existing schedule using the ARN.

        :param scope: -
        :param id: -
        :param schedule_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19c18655ca4e88a10cb1ad96fb4f6f2bf28e3d59822dbc8b6b4f6712157ef87a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument schedule_arn", value=schedule_arn, expected_type=type_hints["schedule_arn"])
        return typing.cast(ISchedule, jsii.sinvoke(cls, "fromScheduleArn", [scope, id, schedule_arn]))

    @jsii.member(jsii_name="metricAll")
    @builtins.classmethod
    def metric_all(
        cls,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for all schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f37ee6db443dc24e3f6d1a5637cadc09747e660e677d6747cc097fe79449b71)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAll", [metric_name, props]))

    @jsii.member(jsii_name="metricAllAttempts")
    @builtins.classmethod
    def metric_all_attempts(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts across all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllAttempts", [props]))

    @jsii.member(jsii_name="metricAllDropped")
    @builtins.classmethod
    def metric_all_dropped(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        Metric is calculated for all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllDropped", [props]))

    @jsii.member(jsii_name="metricAllErrors")
    @builtins.classmethod
    def metric_all_errors(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API across all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllErrors", [props]))

    @jsii.member(jsii_name="metricAllFailedToBeSentToDLQ")
    @builtins.classmethod
    def metric_all_failed_to_be_sent_to_dlq(
        cls,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ across all schedules.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62821614a5bcae649421f9a96e53e7d8e27a994271616230dada86709f98a394)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricAllSentToDLQ")
    @builtins.classmethod
    def metric_all_sent_to_dlq(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ across all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllSentToDLQ", [props]))

    @jsii.member(jsii_name="metricAllSentToDLQTruncated")
    @builtins.classmethod
    def metric_all_sent_to_dlq_truncated(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        Metric is calculated for all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllSentToDLQTruncated", [props]))

    @jsii.member(jsii_name="metricAllTargetThrottled")
    @builtins.classmethod
    def metric_all_target_throttled(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target across all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllTargetThrottled", [props]))

    @jsii.member(jsii_name="metricAllThrottled")
    @builtins.classmethod
    def metric_all_throttled(
        cls,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled across all schedules.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.sinvoke(cls, "metricAllThrottled", [props]))

    @builtins.property
    @jsii.member(jsii_name="scheduleArn")
    def schedule_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduleName")
    def schedule_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleName"))

    @builtins.property
    @jsii.member(jsii_name="group")
    def group(self) -> typing.Optional[IGroup]:
        '''(deprecated) The schedule group associated with this schedule.

        :deprecated: Use ``scheduleGroup`` instead. ``group`` will be removed when this module is stabilized.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[IGroup], jsii.get(self, "group"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(deprecated) The customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], jsii.get(self, "key"))

    @builtins.property
    @jsii.member(jsii_name="scheduleGroup")
    def schedule_group(self) -> typing.Optional[IScheduleGroup]:
        '''(deprecated) The schedule group associated with this schedule.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[IScheduleGroup], jsii.get(self, "scheduleGroup"))


class ScheduleExpression(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleExpression",
):
    '''(deprecated) ScheduleExpression for EventBridge Schedule.

    You can choose from three schedule types when configuring your schedule: rate-based, cron-based, and one-time schedules.
    Both rate-based and cron-based schedules are recurring schedules.

    :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html
    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesisfirehose as firehose
        # delivery_stream: firehose.IDeliveryStream
        
        
        payload = {
            "Data": "record"
        }
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.FirehosePutRecord(delivery_stream,
                input=ScheduleTargetInput.from_object(payload)
            )
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: deprecated
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="at")
    @builtins.classmethod
    def at(
        cls,
        date: datetime.datetime,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
    ) -> "ScheduleExpression":
        '''(deprecated) Construct a one-time schedule from a date.

        :param date: The date and time to use. The millisecond part will be ignored.
        :param time_zone: The time zone to use for interpreting the date. Default: - UTC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf0285b6946b1db006663f64ebff2eb43720129f53e712d42b59f3d29620873)
            check_type(argname="argument date", value=date, expected_type=type_hints["date"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "at", [date, time_zone]))

    @jsii.member(jsii_name="cron")
    @builtins.classmethod
    def cron(
        cls,
        *,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
        day: typing.Optional[builtins.str] = None,
        hour: typing.Optional[builtins.str] = None,
        minute: typing.Optional[builtins.str] = None,
        month: typing.Optional[builtins.str] = None,
        week_day: typing.Optional[builtins.str] = None,
        year: typing.Optional[builtins.str] = None,
    ) -> "ScheduleExpression":
        '''(deprecated) Create a recurring schedule from a set of cron fields and time zone.

        :param time_zone: (deprecated) The timezone to run the schedule in. Default: - TimeZone.ETC_UTC
        :param day: The day of the month to run this rule at. Default: - Every day of the month
        :param hour: The hour to run this rule at. Default: - Every hour
        :param minute: The minute to run this rule at. Default: - Every minute
        :param month: The month to run this rule at. Default: - Every month
        :param week_day: The day of the week to run this rule at. Default: - Any day of the week
        :param year: The year to run this rule at. Default: - Every year

        :stability: deprecated
        '''
        options = CronOptionsWithTimezone(
            time_zone=time_zone,
            day=day,
            hour=hour,
            minute=minute,
            month=month,
            week_day=week_day,
            year=year,
        )

        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "cron", [options]))

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(
        cls,
        expression: builtins.str,
        time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
    ) -> "ScheduleExpression":
        '''(deprecated) Construct a schedule from a literal schedule expression.

        :param expression: The expression to use. Must be in a format that EventBridge will recognize
        :param time_zone: The time zone to use for interpreting the expression. Default: - UTC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0634c4b66b6d96653bcec6e5c37e7587eb5123a94680df0694878cb2276e874)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "expression", [expression, time_zone]))

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, duration: _aws_cdk_ceddda9d.Duration) -> "ScheduleExpression":
        '''(deprecated) Construct a recurring schedule from an interval and a time unit.

        Rates may be defined with any unit of time, but when converted into minutes, the duration must be a positive whole number of minutes.

        :param duration: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f7ba7d57267bb20d2ff8fd156c360c31850c2fb0387099338165ebc5ba04a4)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
        return typing.cast("ScheduleExpression", jsii.sinvoke(cls, "rate", [duration]))

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    @abc.abstractmethod
    def expression_string(self) -> builtins.str:
        '''(deprecated) Retrieve the expression for this schedule.

        :stability: deprecated
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    @abc.abstractmethod
    def time_zone(self) -> typing.Optional[_aws_cdk_ceddda9d.TimeZone]:
        '''(deprecated) Retrieve the expression for this schedule.

        :stability: deprecated
        '''
        ...


class _ScheduleExpressionProxy(ScheduleExpression):
    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> builtins.str:
        '''(deprecated) Retrieve the expression for this schedule.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "expressionString"))

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> typing.Optional[_aws_cdk_ceddda9d.TimeZone]:
        '''(deprecated) Retrieve the expression for this schedule.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.TimeZone], jsii.get(self, "timeZone"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleExpression).__jsii_proxy_class__ = lambda : _ScheduleExpressionProxy


@jsii.implements(IScheduleGroup)
class ScheduleGroup(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleGroup",
):
    '''(deprecated) A Schedule Group.

    :stability: deprecated
    :resource: AWS::Scheduler::ScheduleGroup
    :exampleMetadata: infused

    Example::

        # target: targets.LambdaInvoke
        
        
        schedule_group = ScheduleGroup(self, "ScheduleGroup",
            schedule_group_name="MyScheduleGroup"
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            schedule_group=schedule_group
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param removal_policy: (deprecated) The removal policy for the group. If the group is removed also all schedules are removed. Default: RemovalPolicy.RETAIN
        :param schedule_group_name: (deprecated) The name of the schedule group. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13730f3d1f701d8e7177cba12334ffbe8fd175d54f7acf38355aa7cad6a8f24)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ScheduleGroupProps(
            removal_policy=removal_policy, schedule_group_name=schedule_group_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDefaultScheduleGroup")
    @builtins.classmethod
    def from_default_schedule_group(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> IScheduleGroup:
        '''(deprecated) Import a default schedule group.

        :param scope: construct scope.
        :param id: construct id.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ec235463cbe1f41ffa067dc08263431b84133dd8c70bf158762338ef36b49e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(IScheduleGroup, jsii.sinvoke(cls, "fromDefaultScheduleGroup", [scope, id]))

    @jsii.member(jsii_name="fromScheduleGroupArn")
    @builtins.classmethod
    def from_schedule_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        schedule_group_arn: builtins.str,
    ) -> IScheduleGroup:
        '''(deprecated) Import an external schedule group by ARN.

        :param scope: construct scope.
        :param id: construct id.
        :param schedule_group_arn: the ARN of the schedule group to import (e.g. ``arn:aws:scheduler:region:account-id:schedule-group/group-name``).

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eea364e3a1a81a4681d5990e56526ae367314d1bd9996770bb39645f08e3203)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument schedule_group_arn", value=schedule_group_arn, expected_type=type_hints["schedule_group_arn"])
        return typing.cast(IScheduleGroup, jsii.sinvoke(cls, "fromScheduleGroupArn", [scope, id, schedule_group_arn]))

    @jsii.member(jsii_name="fromScheduleGroupName")
    @builtins.classmethod
    def from_schedule_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        schedule_group_name: builtins.str,
    ) -> IScheduleGroup:
        '''(deprecated) Import an existing schedule group with a given name.

        :param scope: construct scope.
        :param id: construct id.
        :param schedule_group_name: the name of the existing schedule group to import.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35822f05ecb3bcbae1b6efb86c563c42a0a4611e0c0413881dd39f5abd3f6e54)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument schedule_group_name", value=schedule_group_name, expected_type=type_hints["schedule_group_name"])
        return typing.cast(IScheduleGroup, jsii.sinvoke(cls, "fromScheduleGroupName", [scope, id, schedule_group_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the indicated permissions on this schedule group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d40930695a98cfdb1135030c0c145d6b6b03fd00965d92337b071c377a50e087)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fa5830f0863d274b45102949f1dca859bd73eca7005ad8bba067fc90e65cfb)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDeleteSchedules", [identity]))

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7a08c60b259997961f596f5733131291b79cae474b33fed7bf570c7ec11e36b)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadSchedules", [identity]))

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ca05991fda7e020a9af9d0e721b6c05f49b627d6b69c721e5e32e1ea2fae43)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWriteSchedules", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this schedule group.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a36ea8268b72f5c25d9f527c2da762ee1df5c7ebf3165e024dcf1785e052e6)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricAttempts", [props]))

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDropped", [props]))

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ce529803807a25fe94c307a0ff20b2b21690a986a2764396c0d7063bdc340da)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQ", [props]))

    @jsii.member(jsii_name="metricSentToDLQTruncated")
    def metric_sent_to_dlq_truncated(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQTruncated", [props]))

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetErrors", [props]))

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetThrottled", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricThrottled", [props]))

    @builtins.property
    @jsii.member(jsii_name="scheduleGroupArn")
    def schedule_group_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule group.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="scheduleGroupName")
    def schedule_group_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule group.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "scheduleGroupName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "removal_policy": "removalPolicy",
        "schedule_group_name": "scheduleGroupName",
    },
)
class ScheduleGroupProps:
    def __init__(
        self,
        *,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
        schedule_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Properties for a Schedule Group.

        :param removal_policy: (deprecated) The removal policy for the group. If the group is removed also all schedules are removed. Default: RemovalPolicy.RETAIN
        :param schedule_group_name: (deprecated) The name of the schedule group. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            # target: targets.LambdaInvoke
            
            
            schedule_group = ScheduleGroup(self, "ScheduleGroup",
                schedule_group_name="MyScheduleGroup"
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(10)),
                target=target,
                schedule_group=schedule_group
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dcabbd203a7f18f4f09abf539eeeb787da4e0294f740ce55e6f0b24179d92eb)
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument schedule_group_name", value=schedule_group_name, expected_type=type_hints["schedule_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if schedule_group_name is not None:
            self._values["schedule_group_name"] = schedule_group_name

    @builtins.property
    def removal_policy(self) -> typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy]:
        '''(deprecated) The removal policy for the group.

        If the group is removed also all schedules are removed.

        :default: RemovalPolicy.RETAIN

        :stability: deprecated
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy], result)

    @builtins.property
    def schedule_group_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the schedule group.

        Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed.

        :default: - A unique name will be generated

        :stability: deprecated
        '''
        result = self._values.get("schedule_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleProps",
    jsii_struct_bases=[],
    name_mapping={
        "schedule": "schedule",
        "target": "target",
        "description": "description",
        "enabled": "enabled",
        "end": "end",
        "group": "group",
        "key": "key",
        "schedule_group": "scheduleGroup",
        "schedule_name": "scheduleName",
        "start": "start",
        "time_window": "timeWindow",
    },
)
class ScheduleProps:
    def __init__(
        self,
        *,
        schedule: ScheduleExpression,
        target: IScheduleTarget,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        end: typing.Optional[datetime.datetime] = None,
        group: typing.Optional[IGroup] = None,
        key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
        schedule_group: typing.Optional[IScheduleGroup] = None,
        schedule_name: typing.Optional[builtins.str] = None,
        start: typing.Optional[datetime.datetime] = None,
        time_window: typing.Optional["TimeWindow"] = None,
    ) -> None:
        '''(deprecated) Construction properties for ``Schedule``.

        :param schedule: (deprecated) The expression that defines when the schedule runs. Can be either a ``at``, ``rate`` or ``cron`` expression.
        :param target: (deprecated) The schedule's target details.
        :param description: (deprecated) The description you specify for the schedule. Default: - no value
        :param enabled: (deprecated) Indicates whether the schedule is enabled. Default: true
        :param end: (deprecated) The date, in UTC, before which the schedule can invoke its target. EventBridge Scheduler ignores end for one-time schedules. Default: - no value
        :param group: (deprecated) The schedule's group. Default: - By default a schedule will be associated with the ``default`` group.
        :param key: (deprecated) The customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data. Default: - All events in Scheduler are encrypted with a key that AWS owns and manages.
        :param schedule_group: (deprecated) The schedule's group. Default: - By default a schedule will be associated with the ``default`` group.
        :param schedule_name: (deprecated) The name of the schedule. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated
        :param start: (deprecated) The date, in UTC, after which the schedule can begin invoking its target. EventBridge Scheduler ignores start for one-time schedules. Default: - no value
        :param time_window: (deprecated) A time window during which EventBridge Scheduler invokes the schedule. Default: TimeWindow.off()

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_kinesisfirehose as firehose
            # delivery_stream: firehose.IDeliveryStream
            
            
            payload = {
                "Data": "record"
            }
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(60)),
                target=targets.FirehosePutRecord(delivery_stream,
                    input=ScheduleTargetInput.from_object(payload)
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec894279ff23a2f409c8409807ceac73af12e448ac28d2398385477bf6c2e20)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument schedule_group", value=schedule_group, expected_type=type_hints["schedule_group"])
            check_type(argname="argument schedule_name", value=schedule_name, expected_type=type_hints["schedule_name"])
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument time_window", value=time_window, expected_type=type_hints["time_window"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "schedule": schedule,
            "target": target,
        }
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if end is not None:
            self._values["end"] = end
        if group is not None:
            self._values["group"] = group
        if key is not None:
            self._values["key"] = key
        if schedule_group is not None:
            self._values["schedule_group"] = schedule_group
        if schedule_name is not None:
            self._values["schedule_name"] = schedule_name
        if start is not None:
            self._values["start"] = start
        if time_window is not None:
            self._values["time_window"] = time_window

    @builtins.property
    def schedule(self) -> ScheduleExpression:
        '''(deprecated) The expression that defines when the schedule runs.

        Can be either a ``at``, ``rate``
        or ``cron`` expression.

        :stability: deprecated
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast(ScheduleExpression, result)

    @builtins.property
    def target(self) -> IScheduleTarget:
        '''(deprecated) The schedule's target details.

        :stability: deprecated
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(IScheduleTarget, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The description you specify for the schedule.

        :default: - no value

        :stability: deprecated
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Indicates whether the schedule is enabled.

        :default: true

        :stability: deprecated
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def end(self) -> typing.Optional[datetime.datetime]:
        '''(deprecated) The date, in UTC, before which the schedule can invoke its target.

        EventBridge Scheduler ignores end for one-time schedules.

        :default: - no value

        :stability: deprecated
        '''
        result = self._values.get("end")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def group(self) -> typing.Optional[IGroup]:
        '''(deprecated) The schedule's group.

        :default: - By default a schedule will be associated with the ``default`` group.

        :deprecated: Use ``scheduleGroup`` instead. ``group`` will be removed when this module is stabilized.

        :stability: deprecated
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[IGroup], result)

    @builtins.property
    def key(self) -> typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey]:
        '''(deprecated) The customer managed KMS key that EventBridge Scheduler will use to encrypt and decrypt your data.

        :default: - All events in Scheduler are encrypted with a key that AWS owns and manages.

        :stability: deprecated
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey], result)

    @builtins.property
    def schedule_group(self) -> typing.Optional[IScheduleGroup]:
        '''(deprecated) The schedule's group.

        :default: - By default a schedule will be associated with the ``default`` group.

        :stability: deprecated
        '''
        result = self._values.get("schedule_group")
        return typing.cast(typing.Optional[IScheduleGroup], result)

    @builtins.property
    def schedule_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the schedule.

        Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed.

        :default: - A unique name will be generated

        :stability: deprecated
        '''
        result = self._values.get("schedule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start(self) -> typing.Optional[datetime.datetime]:
        '''(deprecated) The date, in UTC, after which the schedule can begin invoking its target.

        EventBridge Scheduler ignores start for one-time schedules.

        :default: - no value

        :stability: deprecated
        '''
        result = self._values.get("start")
        return typing.cast(typing.Optional[datetime.datetime], result)

    @builtins.property
    def time_window(self) -> typing.Optional["TimeWindow"]:
        '''(deprecated) A time window during which EventBridge Scheduler invokes the schedule.

        :default: TimeWindow.off()

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-flexible-time-windows.html
        :stability: deprecated
        '''
        result = self._values.get("time_window")
        return typing.cast(typing.Optional["TimeWindow"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleTargetConfig",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "role": "role",
        "dead_letter_config": "deadLetterConfig",
        "ecs_parameters": "ecsParameters",
        "event_bridge_parameters": "eventBridgeParameters",
        "input": "input",
        "kinesis_parameters": "kinesisParameters",
        "retry_policy": "retryPolicy",
        "sage_maker_pipeline_parameters": "sageMakerPipelineParameters",
        "sqs_parameters": "sqsParameters",
    },
)
class ScheduleTargetConfig:
    def __init__(
        self,
        *,
        arn: builtins.str,
        role: _aws_cdk_aws_iam_ceddda9d.IRole,
        dead_letter_config: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        ecs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        event_bridge_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        input: typing.Optional["ScheduleTargetInput"] = None,
        kinesis_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        retry_policy: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
        sqs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(deprecated) Config of a Schedule Target used during initialization of Schedule.

        :param arn: (deprecated) The Amazon Resource Name (ARN) of the target.
        :param role: (deprecated) Role to use to invoke this event target.
        :param dead_letter_config: (deprecated) An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule. If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue. Default: - No dead-letter queue
        :param ecs_parameters: (deprecated) The templated target type for the Amazon ECS RunTask API Operation. Default: - No parameters
        :param event_bridge_parameters: (deprecated) The templated target type for the EventBridge PutEvents API operation. Default: - No parameters
        :param input: (deprecated) What input to pass to the target. Default: - No input
        :param kinesis_parameters: (deprecated) The templated target type for the Amazon Kinesis PutRecord API operation. Default: - No parameters
        :param retry_policy: (deprecated) A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target. Default: - Maximum retry attempts of 185 and maximum age of 86400 seconds (1 day)
        :param sage_maker_pipeline_parameters: (deprecated) The templated target type for the Amazon SageMaker StartPipelineExecution API operation. Default: - No parameters
        :param sqs_parameters: (deprecated) The templated target type for the Amazon SQS SendMessage API Operation. Default: - No parameters

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_alpha as scheduler_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            # schedule_target_input: scheduler_alpha.ScheduleTargetInput
            # tags: Any
            
            schedule_target_config = scheduler_alpha.ScheduleTargetConfig(
                arn="arn",
                role=role,
            
                # the properties below are optional
                dead_letter_config=DeadLetterConfigProperty(
                    arn="arn"
                ),
                ecs_parameters=EcsParametersProperty(
                    task_definition_arn="taskDefinitionArn",
            
                    # the properties below are optional
                    capacity_provider_strategy=[CapacityProviderStrategyItemProperty(
                        capacity_provider="capacityProvider",
            
                        # the properties below are optional
                        base=123,
                        weight=123
                    )],
                    enable_ecs_managed_tags=False,
                    enable_execute_command=False,
                    group="group",
                    launch_type="launchType",
                    network_configuration=NetworkConfigurationProperty(
                        awsvpc_configuration=AwsVpcConfigurationProperty(
                            subnets=["subnets"],
            
                            # the properties below are optional
                            assign_public_ip="assignPublicIp",
                            security_groups=["securityGroups"]
                        )
                    ),
                    placement_constraints=[PlacementConstraintProperty(
                        expression="expression",
                        type="type"
                    )],
                    placement_strategy=[PlacementStrategyProperty(
                        field="field",
                        type="type"
                    )],
                    platform_version="platformVersion",
                    propagate_tags="propagateTags",
                    reference_id="referenceId",
                    tags=tags,
                    task_count=123
                ),
                event_bridge_parameters=EventBridgeParametersProperty(
                    detail_type="detailType",
                    source="source"
                ),
                input=schedule_target_input,
                kinesis_parameters=KinesisParametersProperty(
                    partition_key="partitionKey"
                ),
                retry_policy=RetryPolicyProperty(
                    maximum_event_age_in_seconds=123,
                    maximum_retry_attempts=123
                ),
                sage_maker_pipeline_parameters=SageMakerPipelineParametersProperty(
                    pipeline_parameter_list=[SageMakerPipelineParameterProperty(
                        name="name",
                        value="value"
                    )]
                ),
                sqs_parameters=SqsParametersProperty(
                    message_group_id="messageGroupId"
                )
            )
        '''
        if isinstance(dead_letter_config, dict):
            dead_letter_config = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty(**dead_letter_config)
        if isinstance(ecs_parameters, dict):
            ecs_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty(**ecs_parameters)
        if isinstance(event_bridge_parameters, dict):
            event_bridge_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty(**event_bridge_parameters)
        if isinstance(kinesis_parameters, dict):
            kinesis_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty(**kinesis_parameters)
        if isinstance(retry_policy, dict):
            retry_policy = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty(**retry_policy)
        if isinstance(sage_maker_pipeline_parameters, dict):
            sage_maker_pipeline_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty(**sage_maker_pipeline_parameters)
        if isinstance(sqs_parameters, dict):
            sqs_parameters = _aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty(**sqs_parameters)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b43e95c111929dc4535529e66b018946277654e960b5110e44115e299a6c11)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument dead_letter_config", value=dead_letter_config, expected_type=type_hints["dead_letter_config"])
            check_type(argname="argument ecs_parameters", value=ecs_parameters, expected_type=type_hints["ecs_parameters"])
            check_type(argname="argument event_bridge_parameters", value=event_bridge_parameters, expected_type=type_hints["event_bridge_parameters"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument kinesis_parameters", value=kinesis_parameters, expected_type=type_hints["kinesis_parameters"])
            check_type(argname="argument retry_policy", value=retry_policy, expected_type=type_hints["retry_policy"])
            check_type(argname="argument sage_maker_pipeline_parameters", value=sage_maker_pipeline_parameters, expected_type=type_hints["sage_maker_pipeline_parameters"])
            check_type(argname="argument sqs_parameters", value=sqs_parameters, expected_type=type_hints["sqs_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
            "role": role,
        }
        if dead_letter_config is not None:
            self._values["dead_letter_config"] = dead_letter_config
        if ecs_parameters is not None:
            self._values["ecs_parameters"] = ecs_parameters
        if event_bridge_parameters is not None:
            self._values["event_bridge_parameters"] = event_bridge_parameters
        if input is not None:
            self._values["input"] = input
        if kinesis_parameters is not None:
            self._values["kinesis_parameters"] = kinesis_parameters
        if retry_policy is not None:
            self._values["retry_policy"] = retry_policy
        if sage_maker_pipeline_parameters is not None:
            self._values["sage_maker_pipeline_parameters"] = sage_maker_pipeline_parameters
        if sqs_parameters is not None:
            self._values["sqs_parameters"] = sqs_parameters

    @builtins.property
    def arn(self) -> builtins.str:
        '''(deprecated) The Amazon Resource Name (ARN) of the target.

        :stability: deprecated
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role(self) -> _aws_cdk_aws_iam_ceddda9d.IRole:
        '''(deprecated) Role to use to invoke this event target.

        :stability: deprecated
        '''
        result = self._values.get("role")
        assert result is not None, "Required property 'role' is missing"
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.IRole, result)

    @builtins.property
    def dead_letter_config(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty]:
        '''(deprecated) An object that contains information about an Amazon SQS queue that EventBridge Scheduler uses as a dead-letter queue for your schedule.

        If specified, EventBridge Scheduler delivers failed events that could not be successfully delivered to a target to the queue.

        :default: - No dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_config")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty], result)

    @builtins.property
    def ecs_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty]:
        '''(deprecated) The templated target type for the Amazon ECS RunTask API Operation.

        :default: - No parameters

        :stability: deprecated
        '''
        result = self._values.get("ecs_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty], result)

    @builtins.property
    def event_bridge_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty]:
        '''(deprecated) The templated target type for the EventBridge PutEvents API operation.

        :default: - No parameters

        :stability: deprecated
        '''
        result = self._values.get("event_bridge_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty], result)

    @builtins.property
    def input(self) -> typing.Optional["ScheduleTargetInput"]:
        '''(deprecated) What input to pass to the target.

        :default: - No input

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional["ScheduleTargetInput"], result)

    @builtins.property
    def kinesis_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty]:
        '''(deprecated) The templated target type for the Amazon Kinesis PutRecord API operation.

        :default: - No parameters

        :stability: deprecated
        '''
        result = self._values.get("kinesis_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty], result)

    @builtins.property
    def retry_policy(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty]:
        '''(deprecated) A ``RetryPolicy`` object that includes information about the retry policy settings, including the maximum age of an event, and the maximum number of times EventBridge Scheduler will try to deliver the event to a target.

        :default: - Maximum retry attempts of 185 and maximum age of 86400 seconds (1 day)

        :stability: deprecated
        '''
        result = self._values.get("retry_policy")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty], result)

    @builtins.property
    def sage_maker_pipeline_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty]:
        '''(deprecated) The templated target type for the Amazon SageMaker StartPipelineExecution API operation.

        :default: - No parameters

        :stability: deprecated
        '''
        result = self._values.get("sage_maker_pipeline_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty], result)

    @builtins.property
    def sqs_parameters(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty]:
        '''(deprecated) The templated target type for the Amazon SQS SendMessage API Operation.

        :default: - No parameters

        :stability: deprecated
        '''
        result = self._values.get("sqs_parameters")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleTargetInput(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-alpha.ScheduleTargetInput",
):
    '''(deprecated) The text or well-formed JSON input passed to the target of the schedule.

    Tokens and ContextAttribute may be used in the input.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # fn: lambda.Function
        
        
        target = targets.LambdaInvoke(fn,
            input=ScheduleTargetInput.from_object({
                "payload": "useful"
            })
        )
        
        schedule = Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(10)),
            target=target,
            description="This is a test schedule that invokes a lambda function every 10 minutes."
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: deprecated
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromObject")
    @builtins.classmethod
    def from_object(cls, obj: typing.Any) -> "ScheduleTargetInput":
        '''(deprecated) Pass a JSON object to the target.

        The object will be transformed into a well-formed JSON string in the final template.

        :param obj: object to use to convert to JSON to use as input for the target.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8ad466ed6529e9804ae78b120437ef13be3ec57499e1adc15762a5e00bccce)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("ScheduleTargetInput", jsii.sinvoke(cls, "fromObject", [obj]))

    @jsii.member(jsii_name="fromText")
    @builtins.classmethod
    def from_text(cls, text: builtins.str) -> "ScheduleTargetInput":
        '''(deprecated) Pass simple text to the target.

        For passing complex values like JSON object to a target use method
        ``ScheduleTargetInput.fromObject()`` instead.

        :param text: Text to use as the input for the target.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574fe803ab70d3031262c0aa59859d86504152f998a9cb5954d8eda9a4714e7d)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        return typing.cast("ScheduleTargetInput", jsii.sinvoke(cls, "fromText", [text]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, schedule: ISchedule) -> builtins.str:
        '''(deprecated) Return the input properties for this input object.

        :param schedule: -

        :stability: deprecated
        '''
        ...


class _ScheduleTargetInputProxy(ScheduleTargetInput):
    @jsii.member(jsii_name="bind")
    def bind(self, schedule: ISchedule) -> builtins.str:
        '''(deprecated) Return the input properties for this input object.

        :param schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82eb20b61ddff46bbd14d8fd0a9b321cedc42dd29e60faa8e2d03dc8d7e9c9d)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(builtins.str, jsii.invoke(self, "bind", [schedule]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleTargetInput).__jsii_proxy_class__ = lambda : _ScheduleTargetInputProxy


class TimeWindow(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.TimeWindow",
):
    '''(deprecated) A time window during which EventBridge Scheduler invokes the schedule.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        # target: targets.LambdaInvoke
        
        
        schedule = Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(12)),
            target=target,
            time_window=TimeWindow.flexible(Duration.hours(10))
        )
    '''

    @jsii.member(jsii_name="flexible")
    @builtins.classmethod
    def flexible(cls, max_window: _aws_cdk_ceddda9d.Duration) -> "TimeWindow":
        '''(deprecated) TimeWindow is enabled.

        :param max_window: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41dba91a8cf13066837d23ccd050de69942c85758f9a131ceacfafb284826769)
            check_type(argname="argument max_window", value=max_window, expected_type=type_hints["max_window"])
        return typing.cast("TimeWindow", jsii.sinvoke(cls, "flexible", [max_window]))

    @jsii.member(jsii_name="off")
    @builtins.classmethod
    def off(cls) -> "TimeWindow":
        '''(deprecated) TimeWindow is disabled.

        :stability: deprecated
        '''
        return typing.cast("TimeWindow", jsii.sinvoke(cls, "off", []))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        '''(deprecated) Determines whether the schedule is invoked within a flexible time window.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @builtins.property
    @jsii.member(jsii_name="maxWindow")
    def max_window(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum time window during which the schedule can be invoked.

        Must be between 1 to 1440 minutes.

        :default: - no value

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "maxWindow"))


@jsii.implements(IGroup)
class Group(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-alpha.Group",
):
    '''
    :deprecated: Use ``ScheduleGroup`` instead. ``Group`` will be removed when this module is stabilized.

    :stability: deprecated
    :resource: AWS::Scheduler::ScheduleGroup
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_scheduler_alpha as scheduler_alpha
        import aws_cdk as cdk
        
        group = scheduler_alpha.Group(self, "MyGroup",
            group_name="groupName",
            removal_policy=cdk.RemovalPolicy.DESTROY
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        group_name: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param group_name: (deprecated) The name of the schedule group. Up to 64 letters (uppercase and lowercase), numbers, hyphens, underscores and dots are allowed. Default: - A unique name will be generated
        :param removal_policy: (deprecated) The removal policy for the group. If the group is removed also all schedules are removed. Default: RemovalPolicy.RETAIN

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03833d1cdfd53d17a515f405994c670d3db76eb8e1b7b0644cc3e79b5f7cdebf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GroupProps(group_name=group_name, removal_policy=removal_policy)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromDefaultGroup")
    @builtins.classmethod
    def from_default_group(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
    ) -> IGroup:
        '''(deprecated) Import a default schedule group.

        :param scope: construct scope.
        :param id: construct id.

        :deprecated: Use ``ScheduleGroup.fromDefaultScheduleGroup()`` instead.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2398434fe0af2499acd254ee14ed1a1ddf03cdb183b9f4a5eb1acf3100f1dee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromDefaultGroup", [scope, id]))

    @jsii.member(jsii_name="fromGroupArn")
    @builtins.classmethod
    def from_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_arn: builtins.str,
    ) -> IGroup:
        '''(deprecated) Import an external group by ARN.

        :param scope: construct scope.
        :param id: construct id.
        :param group_arn: the ARN of the group to import (e.g. ``arn:aws:scheduler:region:account-id:schedule-group/group-name``).

        :deprecated: Use ``ScheduleGroup.fromScheduleGroupArn()`` instead.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fca853fb3786085103e508aab2df418bf2a27504e961904ee0917c8d59159fbc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_arn", value=group_arn, expected_type=type_hints["group_arn"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupArn", [scope, id, group_arn]))

    @jsii.member(jsii_name="fromGroupName")
    @builtins.classmethod
    def from_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_name: builtins.str,
    ) -> IGroup:
        '''(deprecated) Import an existing group with a given name.

        :param scope: construct scope.
        :param id: construct id.
        :param group_name: the name of the existing group to import.

        :deprecated: Use ``ScheduleGroup.fromScheduleGroupName()`` instead.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f3f5c8b704bfb81fab0017945f521fa1f85feb0992a204ad6bf13fcc162a66c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupName", [scope, id, group_name]))

    @jsii.member(jsii_name="grant")
    def grant(
        self,
        grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
        *actions: builtins.str,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant the indicated permissions on this group to the given principal.

        :param grantee: -
        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0337793d10fce9f5892ef4024bd3c27eba273469e53a2a4f232c8776713de290)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantDeleteSchedules")
    def grant_delete_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant delete schedule permission for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6279e157b2be9015bedaa73842f155a806c3c23dcda4080b96a88b4760e4d281)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantDeleteSchedules", [identity]))

    @jsii.member(jsii_name="grantReadSchedules")
    def grant_read_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant list and get schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9fd27c6fa3b2fe7be510afbf27f59a845a71e1c9e2e83462272d01e99adbd9f)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantReadSchedules", [identity]))

    @jsii.member(jsii_name="grantWriteSchedules")
    def grant_write_schedules(
        self,
        identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    ) -> _aws_cdk_aws_iam_ceddda9d.Grant:
        '''(deprecated) Grant create and update schedule permissions for schedules in this group to the given principal.

        :param identity: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__670c70dc050cb016f9eb04b7f5b099251cb74c7489f34f6a48991d1ca421271a)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_aws_cdk_aws_iam_ceddda9d.Grant, jsii.invoke(self, "grantWriteSchedules", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Return the given named metric for this group schedules.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f218efce492e06a45099719a7de7cf0d34b4457ee121c7b854b4ccb99c19405)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricAttempts")
    def metric_attempts(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for all invocation attempts.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricAttempts", [props]))

    @jsii.member(jsii_name="metricDropped")
    def metric_dropped(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for dropped invocations when EventBridge Scheduler stops attempting to invoke the target after a schedule's retry policy has been exhausted.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricDropped", [props]))

    @jsii.member(jsii_name="metricFailedToBeSentToDLQ")
    def metric_failed_to_be_sent_to_dlq(
        self,
        error_code: typing.Optional[builtins.str] = None,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for failed invocations that also failed to deliver to DLQ.

        :param error_code: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1252a3e7553c8408b06da1170a1703b3ecb7419c8f88133f82bc0efcda0a0c8)
            check_type(argname="argument error_code", value=error_code, expected_type=type_hints["error_code"])
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricFailedToBeSentToDLQ", [error_code, props]))

    @jsii.member(jsii_name="metricSentToDLQ")
    def metric_sent_to_dlq(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocations delivered to the DLQ.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQ", [props]))

    @jsii.member(jsii_name="metricSentToDLQTruncated")
    def metric_sent_to_dlq_truncated(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for delivery of failed invocations to DLQ when the payload of the event sent to the DLQ exceeds the maximum size allowed by Amazon SQS.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricSentToDLQTruncated", [props]))

    @jsii.member(jsii_name="metricTargetErrors")
    def metric_target_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Emitted when the target returns an exception after EventBridge Scheduler calls the target API.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetErrors", [props]))

    @jsii.member(jsii_name="metricTargetThrottled")
    def metric_target_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for invocation failures due to API throttling by the target.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricTargetThrottled", [props]))

    @jsii.member(jsii_name="metricThrottled")
    def metric_throttled(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        region: typing.Optional[builtins.str] = None,
        stack_account: typing.Optional[builtins.str] = None,
        stack_region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
    ) -> _aws_cdk_aws_cloudwatch_ceddda9d.Metric:
        '''(deprecated) Metric for the number of invocations that were throttled because it exceeds your service quotas.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions_map: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param stack_account: Account of the stack this metric is attached to. Default: - Deployment account.
        :param stack_region: Region of the stack this metric is attached to. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Use the ``aws_cloudwatch.Stats`` helper class to construct valid input strings. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" - "tmNN.NN" | "tm(NN.NN%:NN.NN%)" - "iqm" - "wmNN.NN" | "wm(NN.NN%:NN.NN%)" - "tcNN.NN" | "tc(NN.NN%:NN.NN%)" - "tsNN.NN" | "ts(NN.NN%:NN.NN%)" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :default: - sum over 5 minutes

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/scheduler-quotas.html
        :stability: deprecated
        '''
        props = _aws_cdk_aws_cloudwatch_ceddda9d.MetricOptions(
            account=account,
            color=color,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            stack_account=stack_account,
            stack_region=stack_region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.Metric, jsii.invoke(self, "metricThrottled", [props]))

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(deprecated) The arn of the schedule group.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(deprecated) The name of the schedule group.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))


__all__ = [
    "ContextAttribute",
    "CronOptionsWithTimezone",
    "Group",
    "GroupProps",
    "IGroup",
    "ISchedule",
    "IScheduleGroup",
    "IScheduleTarget",
    "Schedule",
    "ScheduleExpression",
    "ScheduleGroup",
    "ScheduleGroupProps",
    "ScheduleProps",
    "ScheduleTargetConfig",
    "ScheduleTargetInput",
    "TimeWindow",
]

publication.publish()

def _typecheckingstub__fa3298180583c0ddbdf4d5fc4310e8726157d1b4b991a42e01360362e1c7d731(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b93c2b718a23f23063cb14b1618a13104c926d0bdf7230ce719160d882d285a(
    *,
    day: typing.Optional[builtins.str] = None,
    hour: typing.Optional[builtins.str] = None,
    minute: typing.Optional[builtins.str] = None,
    month: typing.Optional[builtins.str] = None,
    week_day: typing.Optional[builtins.str] = None,
    year: typing.Optional[builtins.str] = None,
    time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e70812dffd651250e3c32989b91d882f629f2973738808560a5d95625eae32a(
    *,
    group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c255656ab6f0e3e078e7dc1cbbab1d697e65780cb1fd98622b8baec835090ab(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0687870c381a3baca7f4b904f4ac04af882c393c4e921edbb46354180efea008(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4571a0b7363df77ef9266187c2d8848e8e0b8cca1b1f257361cdb5d92b4ee58c(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc852d9860959f89dec6e107ee923432ec16c8be00fc5dab3b66420d63b4c7b7(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5498dc1be7bc114f9e319e391ca23bdddccb5e44e4c81bce04e4fb998e6c54a(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581616256867e412b78ad27c6b1df8ab52f755a908f2e868750a96f4ea7d9db6(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e07e8a1dfe089f41f512daea38cf3568b9eae574d49317cd3403eab8716360(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9f5c46b8a7eeb02fd0f1ee2f8375cde7e414121ca766da04e2478a30dfeebd8(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e4ca0890a31ad28043e3b209ff9c88befe72900044a98b367f0c5187d0dbf4(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35699979ed895e0f4803f54100299062cd002e2176dd7e7c0a27ac9262a00fc8(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612234981843f6273d98d6daf9e74486f3388cd8931cab797f291e54e02c3ac5(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeb48fb07f0b3ca9ae2a80d69af787e7d8ce6124e2c613eb0e8afcd235229d3e(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f28f823649c05e2eae45e2c63b5b0684fe861a38416935dbe55bcf0d10451241(
    _schedule: ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5630933e51396e7fd66637b557fe7dc9cd565a88ca9ae1d5517435215dbc0220(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    schedule: ScheduleExpression,
    target: IScheduleTarget,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    end: typing.Optional[datetime.datetime] = None,
    group: typing.Optional[IGroup] = None,
    key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    schedule_group: typing.Optional[IScheduleGroup] = None,
    schedule_name: typing.Optional[builtins.str] = None,
    start: typing.Optional[datetime.datetime] = None,
    time_window: typing.Optional[TimeWindow] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19c18655ca4e88a10cb1ad96fb4f6f2bf28e3d59822dbc8b6b4f6712157ef87a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    schedule_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f37ee6db443dc24e3f6d1a5637cadc09747e660e677d6747cc097fe79449b71(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62821614a5bcae649421f9a96e53e7d8e27a994271616230dada86709f98a394(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf0285b6946b1db006663f64ebff2eb43720129f53e712d42b59f3d29620873(
    date: datetime.datetime,
    time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0634c4b66b6d96653bcec6e5c37e7587eb5123a94680df0694878cb2276e874(
    expression: builtins.str,
    time_zone: typing.Optional[_aws_cdk_ceddda9d.TimeZone] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f7ba7d57267bb20d2ff8fd156c360c31850c2fb0387099338165ebc5ba04a4(
    duration: _aws_cdk_ceddda9d.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13730f3d1f701d8e7177cba12334ffbe8fd175d54f7acf38355aa7cad6a8f24(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ec235463cbe1f41ffa067dc08263431b84133dd8c70bf158762338ef36b49e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eea364e3a1a81a4681d5990e56526ae367314d1bd9996770bb39645f08e3203(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    schedule_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35822f05ecb3bcbae1b6efb86c563c42a0a4611e0c0413881dd39f5abd3f6e54(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    schedule_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d40930695a98cfdb1135030c0c145d6b6b03fd00965d92337b071c377a50e087(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fa5830f0863d274b45102949f1dca859bd73eca7005ad8bba067fc90e65cfb(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7a08c60b259997961f596f5733131291b79cae474b33fed7bf570c7ec11e36b(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ca05991fda7e020a9af9d0e721b6c05f49b627d6b69c721e5e32e1ea2fae43(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a36ea8268b72f5c25d9f527c2da762ee1df5c7ebf3165e024dcf1785e052e6(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ce529803807a25fe94c307a0ff20b2b21690a986a2764396c0d7063bdc340da(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dcabbd203a7f18f4f09abf539eeeb787da4e0294f740ce55e6f0b24179d92eb(
    *,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
    schedule_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec894279ff23a2f409c8409807ceac73af12e448ac28d2398385477bf6c2e20(
    *,
    schedule: ScheduleExpression,
    target: IScheduleTarget,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    end: typing.Optional[datetime.datetime] = None,
    group: typing.Optional[IGroup] = None,
    key: typing.Optional[_aws_cdk_aws_kms_ceddda9d.IKey] = None,
    schedule_group: typing.Optional[IScheduleGroup] = None,
    schedule_name: typing.Optional[builtins.str] = None,
    start: typing.Optional[datetime.datetime] = None,
    time_window: typing.Optional[TimeWindow] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b43e95c111929dc4535529e66b018946277654e960b5110e44115e299a6c11(
    *,
    arn: builtins.str,
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
    dead_letter_config: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.DeadLetterConfigProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ecs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EcsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    event_bridge_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.EventBridgeParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    input: typing.Optional[ScheduleTargetInput] = None,
    kinesis_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.KinesisParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    retry_policy: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.RetryPolicyProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    sage_maker_pipeline_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SageMakerPipelineParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    sqs_parameters: typing.Optional[typing.Union[_aws_cdk_aws_scheduler_ceddda9d.CfnSchedule.SqsParametersProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8ad466ed6529e9804ae78b120437ef13be3ec57499e1adc15762a5e00bccce(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574fe803ab70d3031262c0aa59859d86504152f998a9cb5954d8eda9a4714e7d(
    text: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82eb20b61ddff46bbd14d8fd0a9b321cedc42dd29e60faa8e2d03dc8d7e9c9d(
    schedule: ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41dba91a8cf13066837d23ccd050de69942c85758f9a131ceacfafb284826769(
    max_window: _aws_cdk_ceddda9d.Duration,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03833d1cdfd53d17a515f405994c670d3db76eb8e1b7b0644cc3e79b5f7cdebf(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_name: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_aws_cdk_ceddda9d.RemovalPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2398434fe0af2499acd254ee14ed1a1ddf03cdb183b9f4a5eb1acf3100f1dee(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fca853fb3786085103e508aab2df418bf2a27504e961904ee0917c8d59159fbc(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f3f5c8b704bfb81fab0017945f521fa1f85feb0992a204ad6bf13fcc162a66c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0337793d10fce9f5892ef4024bd3c27eba273469e53a2a4f232c8776713de290(
    grantee: _aws_cdk_aws_iam_ceddda9d.IGrantable,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6279e157b2be9015bedaa73842f155a806c3c23dcda4080b96a88b4760e4d281(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9fd27c6fa3b2fe7be510afbf27f59a845a71e1c9e2e83462272d01e99adbd9f(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__670c70dc050cb016f9eb04b7f5b099251cb74c7489f34f6a48991d1ca421271a(
    identity: _aws_cdk_aws_iam_ceddda9d.IGrantable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f218efce492e06a45099719a7de7cf0d34b4457ee121c7b854b4ccb99c19405(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1252a3e7553c8408b06da1170a1703b3ecb7419c8f88133f82bc0efcda0a0c8(
    error_code: typing.Optional[builtins.str] = None,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    region: typing.Optional[builtins.str] = None,
    stack_account: typing.Optional[builtins.str] = None,
    stack_region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_aws_cdk_aws_cloudwatch_ceddda9d.Unit] = None,
) -> None:
    """Type checking stubs"""
    pass
