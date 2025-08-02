r'''
# Amazon EventBridge Scheduler Targets Construct Library

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

All constructs moved to `aws-cdk-lib/aws-scheduler-targets`.

[Amazon EventBridge Scheduler](https://aws.amazon.com/blogs/compute/introducing-amazon-eventbridge-scheduler/) is a feature from Amazon EventBridge
that allows you to create, run, and manage scheduled tasks at scale. With EventBridge Scheduler, you can schedule millions of one-time or recurring tasks across various AWS services without provisioning or managing underlying infrastructure.

This library contains integration classes for Amazon EventBridge Scheduler to call any
number of supported AWS Services.

The following targets are supported:

1. `targets.LambdaInvoke`: [Invoke an AWS Lambda function](#invoke-a-lambda-function)
2. `targets.StepFunctionsStartExecution`: [Start an AWS Step Function](#start-an-aws-step-function)
3. `targets.CodeBuildStartBuild`: [Start a CodeBuild job](#start-a-codebuild-job)
4. `targets.SqsSendMessage`: [Send a Message to an Amazon SQS Queue](#send-a-message-to-an-sqs-queue)
5. `targets.SnsPublish`: [Publish messages to an Amazon SNS topic](#publish-messages-to-an-amazon-sns-topic)
6. `targets.EventBridgePutEvents`: [Put Events on EventBridge](#send-events-to-an-eventbridge-event-bus)
7. `targets.InspectorStartAssessmentRun`: [Start an Amazon Inspector assessment run](#start-an-amazon-inspector-assessment-run)
8. `targets.KinesisStreamPutRecord`: [Put a record to an Amazon Kinesis Data Stream](#put-a-record-to-an-amazon-kinesis-data-stream)
9. `targets.FirehosePutRecord`: [Put a record to an Amazon Data Firehose](#put-a-record-to-an-amazon-data-firehose)
10. `targets.CodePipelineStartPipelineExecution`: [Start a CodePipeline execution](#start-a-codepipeline-execution)
11. `targets.SageMakerStartPipelineExecution`: [Start a SageMaker pipeline execution](#start-a-sagemaker-pipeline-execution)
12. `targets.EcsRunTask`: [Start a new ECS task](#schedule-an-ecs-task-run)
13. `targets.Universal`: [Invoke a wider set of AWS API](#invoke-a-wider-set-of-aws-api)

## Invoke a Lambda function

Use the `LambdaInvoke` target to invoke a lambda function.

The code snippet below creates an event rule with a Lambda function as a target
called every hour by EventBridge Scheduler with a custom payload. You can optionally attach a
[dead letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/rule-dlq.html).

```python
import aws_cdk.aws_lambda as lambda_


fn = lambda_.Function(self, "MyFunc",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_inline("exports.handler = handler.toString()")
)

dlq = sqs.Queue(self, "DLQ",
    queue_name="MyDLQ"
)

target = targets.LambdaInvoke(fn,
    dead_letter_queue=dlq,
    max_event_age=Duration.minutes(1),
    retry_attempts=3,
    input=ScheduleTargetInput.from_object({
        "payload": "useful"
    })
)

schedule = Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```

## Start an AWS Step Function

Use the `StepFunctionsStartExecution` target to start a new execution on a StepFunction.

The code snippet below creates an event rule with a Step Function as a target
called every hour by EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks


payload = {
    "Name": "MyParameter",
    "Value": "🌥️"
}

put_parameter_step = tasks.CallAwsService(self, "PutParameter",
    service="ssm",
    action="putParameter",
    iam_resources=["*"],
    parameters={
        "Name.$": "$.Name",
        "Value.$": "$.Value",
        "Type": "String",
        "Overwrite": True
    }
)

state_machine = sfn.StateMachine(self, "StateMachine",
    definition_body=sfn.DefinitionBody.from_chainable(put_parameter_step)
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=targets.StepFunctionsStartExecution(state_machine,
        input=ScheduleTargetInput.from_object(payload)
    )
)
```

## Start a CodeBuild job

Use the `CodeBuildStartBuild` target to start a new build run on a CodeBuild project.

The code snippet below creates an event rule with a CodeBuild project as target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_codebuild as codebuild

# project: codebuild.Project


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.CodeBuildStartBuild(project)
)
```

## Send a Message To an SQS Queue

Use the `SqsSendMessage` target to send a message to an SQS Queue.

The code snippet below creates an event rule with an SQS Queue as a target
called every hour by EventBridge Scheduler with a custom payload.

Contains the `messageGroupId` to use when the target is a FIFO queue. If you specify
a FIFO queue as a target, the queue must have content-based deduplication enabled.

```python
payload = "test"
message_group_id = "id"
queue = sqs.Queue(self, "MyQueue",
    fifo=True,
    content_based_deduplication=True
)

target = targets.SqsSendMessage(queue,
    input=ScheduleTargetInput.from_text(payload),
    message_group_id=message_group_id
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(1)),
    target=target
)
```

## Publish messages to an Amazon SNS topic

Use the `SnsPublish` target to publish messages to an Amazon SNS topic.

The code snippets below create an event rule with a Amazon SNS topic as a target.
It's called every hour by Amazon EventBridge Scheduler with a custom payload.

```python
import aws_cdk.aws_sns as sns


topic = sns.Topic(self, "Topic")

payload = {
    "message": "Hello scheduler!"
}

target = targets.SnsPublish(topic,
    input=ScheduleTargetInput.from_object(payload)
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=target
)
```

## Send events to an EventBridge event bus

Use the `EventBridgePutEvents` target to send events to an EventBridge event bus.

The code snippet below creates an event rule with an EventBridge event bus as a target
called every hour by EventBridge Scheduler with a custom event payload.

```python
import aws_cdk.aws_events as events


event_bus = events.EventBus(self, "EventBus",
    event_bus_name="DomainEvents"
)

event_entry = targets.EventBridgePutEventsEntry(
    event_bus=event_bus,
    source="PetService",
    detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
    detail_type="🐶"
)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.hours(1)),
    target=targets.EventBridgePutEvents(event_entry)
)
```

## Start an Amazon Inspector assessment run

Use the `InspectorStartAssessmentRun` target to start an Inspector assessment run.

The code snippet below creates an event rule with an assessment template as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_inspector as inspector

# cfn_assessment_template: inspector.CfnAssessmentTemplate


assessment_template = inspector.AssessmentTemplate.from_cfn_assessment_template(self, "MyAssessmentTemplate", cfn_assessment_template)

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.InspectorStartAssessmentRun(assessment_template)
)
```

## Put a record to an Amazon Kinesis Data Stream

Use the `KinesisStreamPutRecord` target to put a record to an Amazon Kinesis Data Stream.

The code snippet below creates an event rule with a stream as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_kinesis as kinesis


stream = kinesis.Stream(self, "MyStream")

Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.KinesisStreamPutRecord(stream,
        partition_key="key"
    )
)
```

## Put a record to an Amazon Data Firehose

Use the `FirehosePutRecord` target to put a record to an Amazon Data Firehose delivery stream.

The code snippet below creates an event rule with a delivery stream as a target
called every hour by EventBridge Scheduler with a custom payload.

```python
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
```

## Start a CodePipeline execution

Use the `CodePipelineStartPipelineExecution` target to start a new execution for a CodePipeline pipeline.

The code snippet below creates an event rule with a CodePipeline pipeline as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_codepipeline as codepipeline

# pipeline: codepipeline.Pipeline


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.CodePipelineStartPipelineExecution(pipeline)
)
```

## Start a SageMaker pipeline execution

Use the `SageMakerStartPipelineExecution` target to start a new execution for a SageMaker pipeline.

The code snippet below creates an event rule with a SageMaker pipeline as the target which is
called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_sagemaker as sagemaker

# pipeline: sagemaker.IPipeline


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.SageMakerStartPipelineExecution(pipeline,
        pipeline_parameter_list=[targets.SageMakerPipelineParameter(
            name="parameter-name",
            value="parameter-value"
        )]
    )
)
```

## Schedule an ECS task run

Use the `EcsRunTask` target to schedule an ECS task run for a cluster.

The code snippet below creates an event rule with a Fargate task definition and cluster as the target which is called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_ecs as ecs

# cluster: ecs.ICluster
# task_definition: ecs.FargateTaskDefinition


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
    target=targets.EcsRunFargateTask(cluster,
        task_definition=task_definition
    )
)
```

The code snippet below creates an event rule with a EC2 task definition and cluster as the target which is called every hour by EventBridge Scheduler.

```python
import aws_cdk.aws_ecs as ecs

# cluster: ecs.ICluster
# task_definition: ecs.Ec2TaskDefinition


Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
    target=targets.EcsRunEc2Task(cluster,
        task_definition=task_definition
    )
)
```

## Invoke a wider set of AWS API

Use the `Universal` target to invoke AWS API. See [https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html)

The code snippet below creates an event rule with AWS API as the target which is
called at midnight every day by EventBridge Scheduler.

```python
Schedule(self, "Schedule",
    schedule=ScheduleExpression.cron(
        minute="0",
        hour="0"
    ),
    target=targets.Universal(
        service="rds",
        action="stopDBCluster",
        input=ScheduleTargetInput.from_object({
            "DbClusterIdentifier": "my-db"
        })
    )
)
```

The `service` must be in lowercase and the `action` must be in camelCase.

By default, an IAM policy for the Scheduler is extracted from the API call. The action in the policy is constructed using the `service` and `action` prop.
Re-using the example above, the action will be `rds:stopDBCluster`. Note that not all IAM actions follow the same pattern. In such scenario, please use the
`policyStatements` prop to override the policy:

```python
Schedule(self, "Schedule",
    schedule=ScheduleExpression.rate(Duration.minutes(60)),
    target=targets.Universal(
        service="sqs",
        action="sendMessage",
        policy_statements=[
            iam.PolicyStatement(
                actions=["sqs:SendMessage"],
                resources=["arn:aws:sqs:us-east-1:123456789012:my_queue"]
            ),
            iam.PolicyStatement(
                actions=["kms:Decrypt", "kms:GenerateDataKey*"],
                resources=["arn:aws:kms:us-east-1:123456789012:key/0987dcba-09fe-87dc-65ba-ab0987654321"]
            )
        ]
    )
)
```

> Note: The default policy uses `*` in the resources field as CDK does not have a straight forward way to auto-discover the resources permission required.
> It is recommended that you scope the field down to specific resources to have a better security posture.
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
import aws_cdk.aws_codebuild as _aws_cdk_aws_codebuild_ceddda9d
import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_ceddda9d
import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_ceddda9d
import aws_cdk.aws_ecs as _aws_cdk_aws_ecs_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_inspector as _aws_cdk_aws_inspector_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_sagemaker as _aws_cdk_aws_sagemaker_ceddda9d
import aws_cdk.aws_scheduler_alpha as _aws_cdk_aws_scheduler_alpha_61df44e1
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EventBridgePutEventsEntry",
    jsii_struct_bases=[],
    name_mapping={
        "detail": "detail",
        "detail_type": "detailType",
        "event_bus": "eventBus",
        "source": "source",
    },
)
class EventBridgePutEventsEntry:
    def __init__(
        self,
        *,
        detail: _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput,
        detail_type: builtins.str,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        source: builtins.str,
    ) -> None:
        '''(deprecated) An entry to be sent to EventBridge.

        :param detail: (deprecated) The event body. Can either be provided as an object or as a JSON-serialized string
        :param detail_type: (deprecated) Used along with the source field to help identify the fields and values expected in the detail field. For example, events by CloudTrail have detail type "AWS API Call via CloudTrail"
        :param event_bus: (deprecated) The event bus the entry will be sent to.
        :param source: (deprecated) The service or application that caused this event to be generated. Example value: ``com.example.service``

        :see: https://docs.aws.amazon.com/eventbridge/latest/APIReference/API_PutEventsRequestEntry.html
        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_events as events
            
            
            event_bus = events.EventBus(self, "EventBus",
                event_bus_name="DomainEvents"
            )
            
            event_entry = targets.EventBridgePutEventsEntry(
                event_bus=event_bus,
                source="PetService",
                detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
                detail_type="🐶"
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.hours(1)),
                target=targets.EventBridgePutEvents(event_entry)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b15c35d804ca95ff64ca0a6f312aaf0cec9780ee78849d0052cf3f113afad9)
            check_type(argname="argument detail", value=detail, expected_type=type_hints["detail"])
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detail": detail,
            "detail_type": detail_type,
            "event_bus": event_bus,
            "source": source,
        }

    @builtins.property
    def detail(self) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput:
        '''(deprecated) The event body.

        Can either be provided as an object or as a JSON-serialized string

        :stability: deprecated

        Example::

            ScheduleTargetInput.from_text("{\"instance-id\": \"i-1234567890abcdef0\", \"state\": \"terminated\"}")
            ScheduleTargetInput.from_object({"Message": "Hello from a friendly event :)"})
        '''
        result = self._values.get("detail")
        assert result is not None, "Required property 'detail' is missing"
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput, result)

    @builtins.property
    def detail_type(self) -> builtins.str:
        '''(deprecated) Used along with the source field to help identify the fields and values expected in the detail field.

        For example, events by CloudTrail have detail type "AWS API Call via CloudTrail"

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html
        :stability: deprecated
        '''
        result = self._values.get("detail_type")
        assert result is not None, "Required property 'detail_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_bus(self) -> _aws_cdk_aws_events_ceddda9d.IEventBus:
        '''(deprecated) The event bus the entry will be sent to.

        :stability: deprecated
        '''
        result = self._values.get("event_bus")
        assert result is not None, "Required property 'event_bus' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.IEventBus, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''(deprecated) The service or application that caused this event to be generated.

        Example value: ``com.example.service``

        :see: https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html
        :stability: deprecated
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBridgePutEventsEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SageMakerPipelineParameter",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "value": "value"},
)
class SageMakerPipelineParameter:
    def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
        '''(deprecated) Properties for a pipeline parameter.

        :param name: (deprecated) Name of parameter to start execution of a SageMaker Model Building Pipeline.
        :param value: (deprecated) Value of parameter to start execution of a SageMaker Model Building Pipeline.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_targets_alpha as scheduler_targets_alpha
            
            sage_maker_pipeline_parameter = scheduler_targets_alpha.SageMakerPipelineParameter(
                name="name",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1b671700562aea93d2c9aa01ca3ab4bbfcb0da81f14e336b02e175cc0e96bd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''(deprecated) Name of parameter to start execution of a SageMaker Model Building Pipeline.

        :stability: deprecated
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(deprecated) Value of parameter to start execution of a SageMaker Model Building Pipeline.

        :stability: deprecated
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerPipelineParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ScheduleTargetBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.ScheduleTargetBase",
):
    '''(deprecated) Base class for Schedule Targets.

    :stability: deprecated
    '''

    def __init__(
        self,
        base_props: typing.Union["ScheduleTargetBaseProps", typing.Dict[builtins.str, typing.Any]],
        target_arn: builtins.str,
    ) -> None:
        '''
        :param base_props: -
        :param target_arn: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10e59e7b340dc335b31c4a0d18b1845659c5a575671ec4c54fa176892cb9bd54)
            check_type(argname="argument base_props", value=base_props, expected_type=type_hints["base_props"])
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
        jsii.create(self.__class__, self, [base_props, target_arn])

    @jsii.member(jsii_name="addTargetActionToRole")
    @abc.abstractmethod
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''(deprecated) Create a return a Schedule Target Configuration for the given schedule.

        :param schedule: -

        :return: a Schedule Target Configuration

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e82b6bad0ce8e66d78921fb69afc41cc589ff68e7fde7d3a116a558622ba0b)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bind", [schedule]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d8230d421e6fe144b04cf440bae3b93c14a1af6ea5635fc876670037e3a4ee)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def _target_arn(self) -> builtins.str:
        '''
        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


class _ScheduleTargetBaseProxy(ScheduleTargetBase):
    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__610cc83281b440576390d0e3dbfaa9a65adba95233cb7ffdfba72197abc9da29)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, ScheduleTargetBase).__jsii_proxy_class__ = lambda : _ScheduleTargetBaseProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.ScheduleTargetBaseProps",
    jsii_struct_bases=[],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
    },
)
class ScheduleTargetBaseProps:
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(deprecated) Base properties for a Schedule Target.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

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
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e05948e70de09bca87c06a271bef4e0b3a07893d3e2112141ebdce3856e9e80)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ScheduleTargetBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class SnsPublish(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SnsPublish",
):
    '''(deprecated) Use an Amazon SNS topic as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "Topic")
        
        payload = {
            "message": "Hello scheduler!"
        }
        
        target = targets.SnsPublish(topic,
            input=ScheduleTargetInput.from_object(payload)
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(1)),
            target=target
        )
    '''

    def __init__(
        self,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param topic: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b00545abc5c0db54c2d2809ed5b2f135fc5c44b02c318bc15d3634020e4633)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [topic, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6baf1dcdf0de6e124cffb230fe4fdc6f44a348db6477f1070fe2c1b55ef82665)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class SqsSendMessage(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SqsSendMessage",
):
    '''(deprecated) Use an Amazon SQS Queue as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        payload = "test"
        message_group_id = "id"
        queue = sqs.Queue(self, "MyQueue",
            fifo=True,
            content_based_deduplication=True
        )
        
        target = targets.SqsSendMessage(queue,
            input=ScheduleTargetInput.from_text(payload),
            message_group_id=message_group_id
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(1)),
            target=target
        )
    '''

    def __init__(
        self,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        *,
        message_group_id: typing.Optional[builtins.str] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param queue: -
        :param message_group_id: (deprecated) The FIFO message group ID to use as the target. This must be specified when the target is a FIFO queue. If you specify a FIFO queue as a target, the queue must have content-based deduplication enabled. A length of ``messageGroupId`` must be between 1 and 128. Default: - no message group ID
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4813eef9ae399e4e7240ac6b9346c654577bf97511e9a71e43ce8856a8293f77)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        props = SqsSendMessageProps(
            message_group_id=message_group_id,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [queue, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5ab2b88a54bc5208c7d14e9744c6597c0f0301de5b4c60bb95d90849069e33)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b4e499db09ce4b94c98ac3cf9054d519de93d540d51895429b6af27d162a12)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SqsSendMessageProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "message_group_id": "messageGroupId",
    },
)
class SqsSendMessageProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Properties for a SQS Queue Target.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param message_group_id: (deprecated) The FIFO message group ID to use as the target. This must be specified when the target is a FIFO queue. If you specify a FIFO queue as a target, the queue must have content-based deduplication enabled. A length of ``messageGroupId`` must be between 1 and 128. Default: - no message group ID

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            payload = "test"
            message_group_id = "id"
            queue = sqs.Queue(self, "MyQueue",
                fifo=True,
                content_based_deduplication=True
            )
            
            target = targets.SqsSendMessage(queue,
                input=ScheduleTargetInput.from_text(payload),
                message_group_id=message_group_id
            )
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(1)),
                target=target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b54bd4b76ef8c8d82a414b1afa05a0f9628f07ff40b7ecdd1db2ed2ee30fd9c7)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The FIFO message group ID to use as the target.

        This must be specified when the target is a FIFO queue. If you specify
        a FIFO queue as a target, the queue must have content-based deduplication enabled.

        A length of ``messageGroupId`` must be between 1 and 128.

        :default: - no message group ID

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sqsparameters.html#cfn-scheduler-schedule-sqsparameters-messagegroupid
        :stability: deprecated
        '''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsSendMessageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class StepFunctionsStartExecution(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.StepFunctionsStartExecution",
):
    '''(deprecated) Use an AWS Step function as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_stepfunctions as sfn
        import aws_cdk.aws_stepfunctions_tasks as tasks
        
        
        payload = {
            "Name": "MyParameter",
            "Value": "🌥️"
        }
        
        put_parameter_step = tasks.CallAwsService(self, "PutParameter",
            service="ssm",
            action="putParameter",
            iam_resources=["*"],
            parameters={
                "Name.$": "$.Name",
                "Value.$": "$.Value",
                "Type": "String",
                "Overwrite": True
            }
        )
        
        state_machine = sfn.StateMachine(self, "StateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(put_parameter_step)
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(1)),
            target=targets.StepFunctionsStartExecution(state_machine,
                input=ScheduleTargetInput.from_object(payload)
            )
        )
    '''

    def __init__(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param state_machine: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df2f5731f4fe761fad561cdd5177904d0685abe6cc827da58894e4519f3104d2)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [state_machine, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16c6a822df4449b80b3088cf438b74a5c925845e7b3fe17b5671a96deceef76)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.Tag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Tag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''(deprecated) Metadata that you apply to a resource to help categorize and organize the resource.

        Each tag consists of a key and an optional value, both of which you define.

        :param key: (deprecated) Key is the name of the tag.
        :param value: (deprecated) Value is the metadata contents of the tag.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_targets_alpha as scheduler_targets_alpha
            
            tag = scheduler_targets_alpha.Tag(
                key="key",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1726cc4bf58e2c200057667121a8ee2d9d93fcadffd2f641734413739895d69)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''(deprecated) Key is the name of the tag.

        :stability: deprecated
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(deprecated) Value is the metadata contents of the tag.

        :stability: deprecated
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class Universal(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.Universal",
):
    '''(deprecated) Use a wider set of AWS API as a target for AWS EventBridge Scheduler.

    :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html
    :stability: deprecated
    :exampleMetadata: infused

    Example::

        Schedule(self, "Schedule",
            schedule=ScheduleExpression.cron(
                minute="0",
                hour="0"
            ),
            target=targets.Universal(
                service="rds",
                action="stopDBCluster",
                input=ScheduleTargetInput.from_object({
                    "DbClusterIdentifier": "my-db"
                })
            )
        )
    '''

    def __init__(
        self,
        *,
        action: builtins.str,
        service: builtins.str,
        policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param action: (deprecated) The API action to call. Must be camelCase. You cannot use read-only API actions such as common GET operations.
        :param service: (deprecated) The AWS service to call. This must be in lowercase.
        :param policy_statements: (deprecated) The IAM policy statements needed to invoke the target. These statements are attached to the Scheduler's role. Note that the default may not be the correct actions as not all AWS services follows the same IAM action pattern, or there may be more actions needed to invoke the target. Default: - Policy with ``service:action`` action only.
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        props = UniversalTargetProps(
            action=action,
            service=service,
            policy_statements=policy_statements,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b165e37b986acfbce2c5790c15119e3cc82a80d92b64614b117e0dd3321a95)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.UniversalTargetProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "action": "action",
        "service": "service",
        "policy_statements": "policyStatements",
    },
)
class UniversalTargetProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        action: builtins.str,
        service: builtins.str,
        policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
    ) -> None:
        '''(deprecated) Properties for a Universal Target.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param action: (deprecated) The API action to call. Must be camelCase. You cannot use read-only API actions such as common GET operations.
        :param service: (deprecated) The AWS service to call. This must be in lowercase.
        :param policy_statements: (deprecated) The IAM policy statements needed to invoke the target. These statements are attached to the Scheduler's role. Note that the default may not be the correct actions as not all AWS services follows the same IAM action pattern, or there may be more actions needed to invoke the target. Default: - Policy with ``service:action`` action only.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            Schedule(self, "Schedule",
                schedule=ScheduleExpression.cron(
                    minute="0",
                    hour="0"
                ),
                target=targets.Universal(
                    service="rds",
                    action="stopDBCluster",
                    input=ScheduleTargetInput.from_object({
                        "DbClusterIdentifier": "my-db"
                    })
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9231c0ef7eec0af506feba01c6040b845d12fdfff9ba460bb02a9743da1166)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument policy_statements", value=policy_statements, expected_type=type_hints["policy_statements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "service": service,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if policy_statements is not None:
            self._values["policy_statements"] = policy_statements

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def action(self) -> builtins.str:
        '''(deprecated) The API action to call. Must be camelCase.

        You cannot use read-only API actions such as common GET operations.

        :see: https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html#unsupported-api-actions
        :stability: deprecated
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''(deprecated) The AWS service to call.

        This must be in lowercase.

        :stability: deprecated
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_statements(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]]:
        '''(deprecated) The IAM policy statements needed to invoke the target. These statements are attached to the Scheduler's role.

        Note that the default may not be the correct actions as not all AWS services follows the same IAM action pattern, or there may be more actions needed to invoke the target.

        :default: - Policy with ``service:action`` action only.

        :stability: deprecated
        '''
        result = self._values.get("policy_statements")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UniversalTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class CodeBuildStartBuild(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.CodeBuildStartBuild",
):
    '''(deprecated) Use an AWS CodeBuild as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codebuild as codebuild
        
        # project: codebuild.Project
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.CodeBuildStartBuild(project)
        )
    '''

    def __init__(
        self,
        project: _aws_cdk_aws_codebuild_ceddda9d.IProject,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param project: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eee4f6daae6be7c2365ab2dfb373e3d4a03c594923664bb691da6e3795d41b16)
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [project, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__474fd9928553c6c25206d5a8cd8a15397a1e8091bdc5173fc92abdd167cfda07)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class CodePipelineStartPipelineExecution(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.CodePipelineStartPipelineExecution",
):
    '''(deprecated) Use an AWS CodePipeline pipeline as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codepipeline as codepipeline
        
        # pipeline: codepipeline.Pipeline
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.CodePipelineStartPipelineExecution(pipeline)
        )
    '''

    def __init__(
        self,
        pipeline: _aws_cdk_aws_codepipeline_ceddda9d.IPipeline,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1179b8a788d46a78ad80abd38cd8f227eaf4ff63c93fb2ce58abfb9cf84a57aa)
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [pipeline, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f97647f2f639edabbd7fc4d342abe0f255a5960ef5840c029bfc32962fa9769)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class EcsRunTask(
    ScheduleTargetBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EcsRunTask",
):
    '''(deprecated) Schedule an ECS Task using AWS EventBridge Scheduler.

    :stability: deprecated
    '''

    def __init__(
        self,
        cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
        *,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_execute_command: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        reference_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_count: typing.Optional[jsii.Number] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param cluster: -
        :param task_definition: (deprecated) The task definition to use for scheduled tasks. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions If you want to run a RunTask with an imported task definition, consider using a Universal target.
        :param capacity_provider_strategies: (deprecated) The capacity provider strategy to use for the task. Default: - No capacity provider strategy
        :param enable_ecs_managed_tags: (deprecated) Specifies whether to enable Amazon ECS managed tags for the task. Default: - false
        :param enable_execute_command: (deprecated) Whether to enable execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
        :param group: (deprecated) Specifies an ECS task group for the task. Default: - No group
        :param propagate_tags: (deprecated) Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Default: - No tag propagation
        :param reference_id: (deprecated) The reference ID to use for the task. Default: - No reference ID.
        :param security_groups: (deprecated) The security groups associated with the task. These security groups must all be in the same VPC. Controls inbound and outbound network access for the task. Default: - The security group for the VPC is used.
        :param tags: (deprecated) The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. Default: - No tags
        :param task_count: (deprecated) The number of tasks to create based on TaskDefinition. Default: 1
        :param vpc_subnets: (deprecated) The subnets associated with the task. These subnets must all be in the same VPC. The task will be launched in these subnets. Default: - all private subnets of the VPC are selected.
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85532c687b6f71d597a01494dbe986934143e5ca7ec87233c62cf9c8f1a089e7)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        props = EcsRunTaskBaseProps(
            task_definition=task_definition,
            capacity_provider_strategies=capacity_provider_strategies,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_execute_command=enable_execute_command,
            group=group,
            propagate_tags=propagate_tags,
            reference_id=reference_id,
            security_groups=security_groups,
            tags=tags,
            task_count=task_count,
            vpc_subnets=vpc_subnets,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [cluster, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466075cb50bd1b9d2bb19177d085bd137eee1bc35dcaaaa426c57a806bdedb24)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18807a341be4453df8cbab1b8803ad0e87c5baea5794dd8f389c391387b171ed)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def _cluster(self) -> _aws_cdk_aws_ecs_ceddda9d.ICluster:
        '''
        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.ICluster, jsii.get(self, "cluster"))

    @builtins.property
    @jsii.member(jsii_name="props")
    def _props(self) -> "EcsRunTaskBaseProps":
        '''
        :stability: deprecated
        '''
        return typing.cast("EcsRunTaskBaseProps", jsii.get(self, "props"))


class _EcsRunTaskProxy(
    EcsRunTask,
    jsii.proxy_for(ScheduleTargetBase), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, EcsRunTask).__jsii_proxy_class__ = lambda : _EcsRunTaskProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EcsRunTaskBaseProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "task_definition": "taskDefinition",
        "capacity_provider_strategies": "capacityProviderStrategies",
        "enable_ecs_managed_tags": "enableEcsManagedTags",
        "enable_execute_command": "enableExecuteCommand",
        "group": "group",
        "propagate_tags": "propagateTags",
        "reference_id": "referenceId",
        "security_groups": "securityGroups",
        "tags": "tags",
        "task_count": "taskCount",
        "vpc_subnets": "vpcSubnets",
    },
)
class EcsRunTaskBaseProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_execute_command: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        reference_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_count: typing.Optional[jsii.Number] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(deprecated) Parameters for scheduling ECS Run Task (common to EC2 and Fargate launch types).

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param task_definition: (deprecated) The task definition to use for scheduled tasks. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions If you want to run a RunTask with an imported task definition, consider using a Universal target.
        :param capacity_provider_strategies: (deprecated) The capacity provider strategy to use for the task. Default: - No capacity provider strategy
        :param enable_ecs_managed_tags: (deprecated) Specifies whether to enable Amazon ECS managed tags for the task. Default: - false
        :param enable_execute_command: (deprecated) Whether to enable execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
        :param group: (deprecated) Specifies an ECS task group for the task. Default: - No group
        :param propagate_tags: (deprecated) Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Default: - No tag propagation
        :param reference_id: (deprecated) The reference ID to use for the task. Default: - No reference ID.
        :param security_groups: (deprecated) The security groups associated with the task. These security groups must all be in the same VPC. Controls inbound and outbound network access for the task. Default: - The security group for the VPC is used.
        :param tags: (deprecated) The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. Default: - No tags
        :param task_count: (deprecated) The number of tasks to create based on TaskDefinition. Default: 1
        :param vpc_subnets: (deprecated) The subnets associated with the task. These subnets must all be in the same VPC. The task will be launched in these subnets. Default: - all private subnets of the VPC are selected.

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_scheduler_alpha as scheduler_alpha
            import aws_cdk.aws_scheduler_targets_alpha as scheduler_targets_alpha
            import aws_cdk as cdk
            from aws_cdk import aws_ec2 as ec2
            from aws_cdk import aws_ecs as ecs
            from aws_cdk import aws_iam as iam
            from aws_cdk import aws_sqs as sqs
            
            # queue: sqs.Queue
            # role: iam.Role
            # schedule_target_input: scheduler_alpha.ScheduleTargetInput
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # task_definition: ecs.TaskDefinition
            
            ecs_run_task_base_props = scheduler_targets_alpha.EcsRunTaskBaseProps(
                task_definition=task_definition,
            
                # the properties below are optional
                capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                    capacity_provider="capacityProvider",
            
                    # the properties below are optional
                    base=123,
                    weight=123
                )],
                dead_letter_queue=queue,
                enable_ecs_managed_tags=False,
                enable_execute_command=False,
                group="group",
                input=schedule_target_input,
                max_event_age=cdk.Duration.minutes(30),
                propagate_tags=False,
                reference_id="referenceId",
                retry_attempts=123,
                role=role,
                security_groups=[security_group],
                tags=[scheduler_targets_alpha.Tag(
                    key="key",
                    value="value"
                )],
                task_count=123,
                vpc_subnets=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.PRIVATE_ISOLATED
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f400535c3d9712c95444200b98975962e82c73d2cbe880613a73dd38bd615a13)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument capacity_provider_strategies", value=capacity_provider_strategies, expected_type=type_hints["capacity_provider_strategies"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition": task_definition,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if capacity_provider_strategies is not None:
            self._values["capacity_provider_strategies"] = capacity_provider_strategies
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_execute_command is not None:
            self._values["enable_execute_command"] = enable_execute_command
        if group is not None:
            self._values["group"] = group
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if reference_id is not None:
            self._values["reference_id"] = reference_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if task_count is not None:
            self._values["task_count"] = task_count
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_ceddda9d.TaskDefinition:
        '''(deprecated) The task definition to use for scheduled tasks.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        If you want to run a RunTask with an imported task definition,
        consider using a Universal target.

        :stability: deprecated
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.TaskDefinition, result)

    @builtins.property
    def capacity_provider_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]]:
        '''(deprecated) The capacity provider strategy to use for the task.

        :default: - No capacity provider strategy

        :stability: deprecated
        '''
        result = self._values.get("capacity_provider_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether to enable Amazon ECS managed tags for the task.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_execute_command(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether to enable execute command functionality for the containers in this task.

        If true, this enables execute command functionality on all containers in the task.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("enable_execute_command")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Specifies an ECS task group for the task.

        :default: - No group

        :stability: deprecated
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether to propagate the tags from the task definition to the task.

        If no value is specified, the tags are not propagated.

        :default: - No tag propagation

        :stability: deprecated
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reference_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The reference ID to use for the task.

        :default: - No reference ID.

        :stability: deprecated
        '''
        result = self._values.get("reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(deprecated) The security groups associated with the task.

        These security groups must all be in the same VPC.
        Controls inbound and outbound network access for the task.

        :default: - The security group for the VPC is used.

        :stability: deprecated
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[Tag]]:
        '''(deprecated) The metadata that you apply to the task to help you categorize and organize them.

        Each tag consists of a key and an optional value, both of which you define.

        :default: - No tags

        :stability: deprecated
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[Tag]], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The number of tasks to create based on TaskDefinition.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(deprecated) The subnets associated with the task.

        These subnets must all be in the same VPC.
        The task will be launched in these subnets.

        :default: - all private subnets of the VPC are selected.

        :stability: deprecated
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcsRunTaskBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class EventBridgePutEvents(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EventBridgePutEvents",
):
    '''(deprecated) Send an event to an AWS EventBridge by AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_events as events
        
        
        event_bus = events.EventBus(self, "EventBus",
            event_bus_name="DomainEvents"
        )
        
        event_entry = targets.EventBridgePutEventsEntry(
            event_bus=event_bus,
            source="PetService",
            detail=ScheduleTargetInput.from_object({"Name": "Fluffy"}),
            detail_type="🐶"
        )
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.hours(1)),
            target=targets.EventBridgePutEvents(event_entry)
        )
    '''

    def __init__(
        self,
        entry: typing.Union[EventBridgePutEventsEntry, typing.Dict[builtins.str, typing.Any]],
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param entry: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae28df8ed7b4d4cf0069c2078c852156338afac2e79eb10ab690c790a1efde31)
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [entry, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4d3987aace1577c0609c760b353ffad7b4806705694003c15c7ef457008811e)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe563fb16e465141154d47511f2ad5007930fbbc4c511a584457cd7a4285e684)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.FargateTaskProps",
    jsii_struct_bases=[EcsRunTaskBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "task_definition": "taskDefinition",
        "capacity_provider_strategies": "capacityProviderStrategies",
        "enable_ecs_managed_tags": "enableEcsManagedTags",
        "enable_execute_command": "enableExecuteCommand",
        "group": "group",
        "propagate_tags": "propagateTags",
        "reference_id": "referenceId",
        "security_groups": "securityGroups",
        "tags": "tags",
        "task_count": "taskCount",
        "vpc_subnets": "vpcSubnets",
        "assign_public_ip": "assignPublicIp",
        "platform_version": "platformVersion",
    },
)
class FargateTaskProps(EcsRunTaskBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_execute_command: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        reference_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_count: typing.Optional[jsii.Number] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
    ) -> None:
        '''(deprecated) Properties for scheduling an ECS Fargate Task.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param task_definition: (deprecated) The task definition to use for scheduled tasks. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions If you want to run a RunTask with an imported task definition, consider using a Universal target.
        :param capacity_provider_strategies: (deprecated) The capacity provider strategy to use for the task. Default: - No capacity provider strategy
        :param enable_ecs_managed_tags: (deprecated) Specifies whether to enable Amazon ECS managed tags for the task. Default: - false
        :param enable_execute_command: (deprecated) Whether to enable execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
        :param group: (deprecated) Specifies an ECS task group for the task. Default: - No group
        :param propagate_tags: (deprecated) Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Default: - No tag propagation
        :param reference_id: (deprecated) The reference ID to use for the task. Default: - No reference ID.
        :param security_groups: (deprecated) The security groups associated with the task. These security groups must all be in the same VPC. Controls inbound and outbound network access for the task. Default: - The security group for the VPC is used.
        :param tags: (deprecated) The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. Default: - No tags
        :param task_count: (deprecated) The number of tasks to create based on TaskDefinition. Default: 1
        :param vpc_subnets: (deprecated) The subnets associated with the task. These subnets must all be in the same VPC. The task will be launched in these subnets. Default: - all private subnets of the VPC are selected.
        :param assign_public_ip: (deprecated) Specifies whether the task's elastic network interface receives a public IP address. If true, the task will receive a public IP address and be accessible from the internet. Should only be set to true when using public subnets. Default: - true if the subnet type is PUBLIC, otherwise false
        :param platform_version: (deprecated) Specifies the platform version for the task. Specify only the numeric portion of the platform version, such as 1.1.0. Platform versions determine the underlying runtime environment for the task. Default: - LATEST

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecs as ecs
            
            # cluster: ecs.ICluster
            # task_definition: ecs.FargateTaskDefinition
            
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
                target=targets.EcsRunFargateTask(cluster,
                    task_definition=task_definition
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380374bd55cffc9977204bd6a28dd2ed054acaba3cf086012f6df8a51b726028)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument capacity_provider_strategies", value=capacity_provider_strategies, expected_type=type_hints["capacity_provider_strategies"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument assign_public_ip", value=assign_public_ip, expected_type=type_hints["assign_public_ip"])
            check_type(argname="argument platform_version", value=platform_version, expected_type=type_hints["platform_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition": task_definition,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if capacity_provider_strategies is not None:
            self._values["capacity_provider_strategies"] = capacity_provider_strategies
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_execute_command is not None:
            self._values["enable_execute_command"] = enable_execute_command
        if group is not None:
            self._values["group"] = group
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if reference_id is not None:
            self._values["reference_id"] = reference_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if task_count is not None:
            self._values["task_count"] = task_count
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if assign_public_ip is not None:
            self._values["assign_public_ip"] = assign_public_ip
        if platform_version is not None:
            self._values["platform_version"] = platform_version

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_ceddda9d.TaskDefinition:
        '''(deprecated) The task definition to use for scheduled tasks.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        If you want to run a RunTask with an imported task definition,
        consider using a Universal target.

        :stability: deprecated
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.TaskDefinition, result)

    @builtins.property
    def capacity_provider_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]]:
        '''(deprecated) The capacity provider strategy to use for the task.

        :default: - No capacity provider strategy

        :stability: deprecated
        '''
        result = self._values.get("capacity_provider_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether to enable Amazon ECS managed tags for the task.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_execute_command(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether to enable execute command functionality for the containers in this task.

        If true, this enables execute command functionality on all containers in the task.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("enable_execute_command")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Specifies an ECS task group for the task.

        :default: - No group

        :stability: deprecated
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether to propagate the tags from the task definition to the task.

        If no value is specified, the tags are not propagated.

        :default: - No tag propagation

        :stability: deprecated
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reference_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The reference ID to use for the task.

        :default: - No reference ID.

        :stability: deprecated
        '''
        result = self._values.get("reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(deprecated) The security groups associated with the task.

        These security groups must all be in the same VPC.
        Controls inbound and outbound network access for the task.

        :default: - The security group for the VPC is used.

        :stability: deprecated
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[Tag]]:
        '''(deprecated) The metadata that you apply to the task to help you categorize and organize them.

        Each tag consists of a key and an optional value, both of which you define.

        :default: - No tags

        :stability: deprecated
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[Tag]], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The number of tasks to create based on TaskDefinition.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(deprecated) The subnets associated with the task.

        These subnets must all be in the same VPC.
        The task will be launched in these subnets.

        :default: - all private subnets of the VPC are selected.

        :stability: deprecated
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether the task's elastic network interface receives a public IP address.

        If true, the task will receive a public IP address and be accessible from the internet.
        Should only be set to true when using public subnets.

        :default: - true if the subnet type is PUBLIC, otherwise false

        :stability: deprecated
        '''
        result = self._values.get("assign_public_ip")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def platform_version(
        self,
    ) -> typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion]:
        '''(deprecated) Specifies the platform version for the task.

        Specify only the numeric portion of the platform version, such as 1.1.0.
        Platform versions determine the underlying runtime environment for the task.

        :default: - LATEST

        :stability: deprecated
        '''
        result = self._values.get("platform_version")
        return typing.cast(typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateTaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class FirehosePutRecord(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.FirehosePutRecord",
):
    '''(deprecated) Use an Amazon Data Firehose as a target for AWS EventBridge Scheduler.

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
        delivery_stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param delivery_stream: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d684916d9897133cc3263e5d11aea8dfa003e41c2d8e0deb7a1e1488f6d5a775)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [delivery_stream, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56c16109037f37fad1c95c9415fa5d65603ebae6c28a2daaec1156e2c04f2ab)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class InspectorStartAssessmentRun(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.InspectorStartAssessmentRun",
):
    '''(deprecated) Use an Amazon Inspector as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_inspector as inspector
        
        # cfn_assessment_template: inspector.CfnAssessmentTemplate
        
        
        assessment_template = inspector.AssessmentTemplate.from_cfn_assessment_template(self, "MyAssessmentTemplate", cfn_assessment_template)
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.InspectorStartAssessmentRun(assessment_template)
        )
    '''

    def __init__(
        self,
        template: _aws_cdk_aws_inspector_ceddda9d.IAssessmentTemplate,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param template: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d7bbb3c9d358edb684284e6061143edea14a918d787e7b0de0abe8074adc3a8)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [template, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f62115ee3101d95125c22cd00ce69aefcbf38ba32a31ec38c5fe32386b72a485)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class KinesisStreamPutRecord(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.KinesisStreamPutRecord",
):
    '''(deprecated) Use an Amazon Kinesis Data Streams as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesis as kinesis
        
        
        stream = kinesis.Stream(self, "MyStream")
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.KinesisStreamPutRecord(stream,
                partition_key="key"
            )
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
        *,
        partition_key: builtins.str,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param stream: -
        :param partition_key: (deprecated) The shard to which EventBridge Scheduler sends the event. The length must be between 1 and 256.
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3da8609af671f7e313f5b3391e0c519b97069ce30e7f39aaae4028df271ad968)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = KinesisStreamPutRecordProps(
            partition_key=partition_key,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [stream, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00e0c64cae92c47512d2b31480147546bdac967e14a67f989fced9ea65977ab)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901c2c170b31144628352155381f9212d91d6a15a1323004e8a2a1fc86211850)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.KinesisStreamPutRecordProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "partition_key": "partitionKey",
    },
)
class KinesisStreamPutRecordProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        partition_key: builtins.str,
    ) -> None:
        '''(deprecated) Properties for a Kinesis Data Streams Target.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param partition_key: (deprecated) The shard to which EventBridge Scheduler sends the event. The length must be between 1 and 256.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_kinesis as kinesis
            
            
            stream = kinesis.Stream(self, "MyStream")
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(60)),
                target=targets.KinesisStreamPutRecord(stream,
                    partition_key="key"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450b2e09dbbdf0b1ab8f7ab50d92ab0bc3784cd7aebcc42382aa41af77149cf6)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''(deprecated) The shard to which EventBridge Scheduler sends the event.

        The length must be between 1 and 256.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-kinesisparameters.html
        :stability: deprecated
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisStreamPutRecordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class LambdaInvoke(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.LambdaInvoke",
):
    '''(deprecated) Use an AWS Lambda function as a target for AWS EventBridge Scheduler.

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

    def __init__(
        self,
        func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param func: -
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cee0b6faf4f1c2dcade061e69cf02b9c302a868d55e47f591978024f5da0075)
            check_type(argname="argument func", value=func, expected_type=type_hints["func"])
        props = ScheduleTargetBaseProps(
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [func, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5bceedc3f4419f27eac20d417a223b3233c972e163393fd278acd75b7129d89)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))


@jsii.implements(_aws_cdk_aws_scheduler_alpha_61df44e1.IScheduleTarget)
class SageMakerStartPipelineExecution(
    ScheduleTargetBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SageMakerStartPipelineExecution",
):
    '''(deprecated) Use a SageMaker pipeline as a target for AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sagemaker as sagemaker
        
        # pipeline: sagemaker.IPipeline
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(Duration.minutes(60)),
            target=targets.SageMakerStartPipelineExecution(pipeline,
                pipeline_parameter_list=[targets.SageMakerPipelineParameter(
                    name="parameter-name",
                    value="parameter-value"
                )]
            )
        )
    '''

    def __init__(
        self,
        pipeline: _aws_cdk_aws_sagemaker_ceddda9d.IPipeline,
        *,
        pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param pipeline_parameter_list: (deprecated) List of parameter names and values to use when executing the SageMaker Model Building Pipeline. The length must be between 0 and 200. Default: - no pipeline parameter list
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cd1e092f776a22386cfd27fc1778ae00bc42ca6e1f29df07ab3c760bf88329)
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
        props = SageMakerStartPipelineExecutionProps(
            pipeline_parameter_list=pipeline_parameter_list,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [pipeline, props])

    @jsii.member(jsii_name="addTargetActionToRole")
    def _add_target_action_to_role(self, role: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''
        :param role: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a618244e0553e568cdf781844a2bbc64b2127af3cf8d23bbd6e2083ab5b1838)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "addTargetActionToRole", [role]))

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0401259d77c4f97bb1b7a40ff1a9f35512d38224dee98a520446b9b7876f9acd)
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [schedule]))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.SageMakerStartPipelineExecutionProps",
    jsii_struct_bases=[ScheduleTargetBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "pipeline_parameter_list": "pipelineParameterList",
    },
)
class SageMakerStartPipelineExecutionProps(ScheduleTargetBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(deprecated) Properties for a SageMaker Target.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param pipeline_parameter_list: (deprecated) List of parameter names and values to use when executing the SageMaker Model Building Pipeline. The length must be between 0 and 200. Default: - no pipeline parameter list

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sagemaker as sagemaker
            
            # pipeline: sagemaker.IPipeline
            
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(Duration.minutes(60)),
                target=targets.SageMakerStartPipelineExecution(pipeline,
                    pipeline_parameter_list=[targets.SageMakerPipelineParameter(
                        name="parameter-name",
                        value="parameter-value"
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c01c7fd9ffc99ab1f2f2a61c89fe87963adc09f9e04fb878a3007c33ce123c)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument pipeline_parameter_list", value=pipeline_parameter_list, expected_type=type_hints["pipeline_parameter_list"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if pipeline_parameter_list is not None:
            self._values["pipeline_parameter_list"] = pipeline_parameter_list

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def pipeline_parameter_list(
        self,
    ) -> typing.Optional[typing.List[SageMakerPipelineParameter]]:
        '''(deprecated) List of parameter names and values to use when executing the SageMaker Model Building Pipeline.

        The length must be between 0 and 200.

        :default: - no pipeline parameter list

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-scheduler-schedule-sagemakerpipelineparameters.html#cfn-scheduler-schedule-sagemakerpipelineparameters-pipelineparameterlist
        :stability: deprecated
        '''
        result = self._values.get("pipeline_parameter_list")
        return typing.cast(typing.Optional[typing.List[SageMakerPipelineParameter]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerStartPipelineExecutionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.Ec2TaskProps",
    jsii_struct_bases=[EcsRunTaskBaseProps],
    name_mapping={
        "dead_letter_queue": "deadLetterQueue",
        "input": "input",
        "max_event_age": "maxEventAge",
        "retry_attempts": "retryAttempts",
        "role": "role",
        "task_definition": "taskDefinition",
        "capacity_provider_strategies": "capacityProviderStrategies",
        "enable_ecs_managed_tags": "enableEcsManagedTags",
        "enable_execute_command": "enableExecuteCommand",
        "group": "group",
        "propagate_tags": "propagateTags",
        "reference_id": "referenceId",
        "security_groups": "securityGroups",
        "tags": "tags",
        "task_count": "taskCount",
        "vpc_subnets": "vpcSubnets",
        "placement_constraints": "placementConstraints",
        "placement_strategies": "placementStrategies",
    },
)
class Ec2TaskProps(EcsRunTaskBaseProps):
    def __init__(
        self,
        *,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_execute_command: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        reference_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_count: typing.Optional[jsii.Number] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]] = None,
    ) -> None:
        '''(deprecated) Properties for scheduling an ECS Task on EC2.

        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target
        :param task_definition: (deprecated) The task definition to use for scheduled tasks. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions If you want to run a RunTask with an imported task definition, consider using a Universal target.
        :param capacity_provider_strategies: (deprecated) The capacity provider strategy to use for the task. Default: - No capacity provider strategy
        :param enable_ecs_managed_tags: (deprecated) Specifies whether to enable Amazon ECS managed tags for the task. Default: - false
        :param enable_execute_command: (deprecated) Whether to enable execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
        :param group: (deprecated) Specifies an ECS task group for the task. Default: - No group
        :param propagate_tags: (deprecated) Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Default: - No tag propagation
        :param reference_id: (deprecated) The reference ID to use for the task. Default: - No reference ID.
        :param security_groups: (deprecated) The security groups associated with the task. These security groups must all be in the same VPC. Controls inbound and outbound network access for the task. Default: - The security group for the VPC is used.
        :param tags: (deprecated) The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. Default: - No tags
        :param task_count: (deprecated) The number of tasks to create based on TaskDefinition. Default: 1
        :param vpc_subnets: (deprecated) The subnets associated with the task. These subnets must all be in the same VPC. The task will be launched in these subnets. Default: - all private subnets of the VPC are selected.
        :param placement_constraints: (deprecated) The rules that must be met in order to place a task on a container instance. Default: - No placement constraints.
        :param placement_strategies: (deprecated) The algorithm for selecting container instances for task placement. Default: - No placement strategies.

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_ecs as ecs
            
            # cluster: ecs.ICluster
            # task_definition: ecs.Ec2TaskDefinition
            
            
            Schedule(self, "Schedule",
                schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
                target=targets.EcsRunEc2Task(cluster,
                    task_definition=task_definition
                )
            )
        '''
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _aws_cdk_aws_ec2_ceddda9d.SubnetSelection(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f492ba7877199e36fb5d299cbd93a8254f2a7ed12ec7c2a1a213be9399f002)
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument task_definition", value=task_definition, expected_type=type_hints["task_definition"])
            check_type(argname="argument capacity_provider_strategies", value=capacity_provider_strategies, expected_type=type_hints["capacity_provider_strategies"])
            check_type(argname="argument enable_ecs_managed_tags", value=enable_ecs_managed_tags, expected_type=type_hints["enable_ecs_managed_tags"])
            check_type(argname="argument enable_execute_command", value=enable_execute_command, expected_type=type_hints["enable_execute_command"])
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
            check_type(argname="argument propagate_tags", value=propagate_tags, expected_type=type_hints["propagate_tags"])
            check_type(argname="argument reference_id", value=reference_id, expected_type=type_hints["reference_id"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument task_count", value=task_count, expected_type=type_hints["task_count"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument placement_constraints", value=placement_constraints, expected_type=type_hints["placement_constraints"])
            check_type(argname="argument placement_strategies", value=placement_strategies, expected_type=type_hints["placement_strategies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "task_definition": task_definition,
        }
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if input is not None:
            self._values["input"] = input
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if role is not None:
            self._values["role"] = role
        if capacity_provider_strategies is not None:
            self._values["capacity_provider_strategies"] = capacity_provider_strategies
        if enable_ecs_managed_tags is not None:
            self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_execute_command is not None:
            self._values["enable_execute_command"] = enable_execute_command
        if group is not None:
            self._values["group"] = group
        if propagate_tags is not None:
            self._values["propagate_tags"] = propagate_tags
        if reference_id is not None:
            self._values["reference_id"] = reference_id
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if tags is not None:
            self._values["tags"] = tags
        if task_count is not None:
            self._values["task_count"] = task_count
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if placement_constraints is not None:
            self._values["placement_constraints"] = placement_constraints
        if placement_strategies is not None:
            self._values["placement_strategies"] = placement_strategies

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue]:
        '''(deprecated) The SQS queue to be used as deadLetterQueue.

        The events not successfully delivered are automatically retried for a specified period of time,
        depending on the retry policy of the target.
        If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue.

        :default: - no dead-letter queue

        :stability: deprecated
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue], result)

    @builtins.property
    def input(
        self,
    ) -> typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput]:
        '''(deprecated) Input passed to the target.

        :default: - no input.

        :stability: deprecated
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput], result)

    @builtins.property
    def max_event_age(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''(deprecated) The maximum age of a request that Scheduler sends to a target for processing.

        Minimum value of 60.
        Maximum value of 86400.

        :default: Duration.hours(24)

        :stability: deprecated
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The maximum number of times to retry when the target returns an error.

        Minimum value of 0.
        Maximum value of 185.

        :default: 185

        :stability: deprecated
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf.

        If none provided templates target will automatically create an IAM role with all the minimum necessary
        permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets
        will grant minimal required permissions.

        :default: - created by target

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def task_definition(self) -> _aws_cdk_aws_ecs_ceddda9d.TaskDefinition:
        '''(deprecated) The task definition to use for scheduled tasks.

        Note: this must be TaskDefinition, and not ITaskDefinition,
        as it requires properties that are not known for imported task definitions
        If you want to run a RunTask with an imported task definition,
        consider using a Universal target.

        :stability: deprecated
        '''
        result = self._values.get("task_definition")
        assert result is not None, "Required property 'task_definition' is missing"
        return typing.cast(_aws_cdk_aws_ecs_ceddda9d.TaskDefinition, result)

    @builtins.property
    def capacity_provider_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]]:
        '''(deprecated) The capacity provider strategy to use for the task.

        :default: - No capacity provider strategy

        :stability: deprecated
        '''
        result = self._values.get("capacity_provider_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy]], result)

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether to enable Amazon ECS managed tags for the task.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("enable_ecs_managed_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enable_execute_command(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether to enable execute command functionality for the containers in this task.

        If true, this enables execute command functionality on all containers in the task.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("enable_execute_command")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def group(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Specifies an ECS task group for the task.

        :default: - No group

        :stability: deprecated
        '''
        result = self._values.get("group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def propagate_tags(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Specifies whether to propagate the tags from the task definition to the task.

        If no value is specified, the tags are not propagated.

        :default: - No tag propagation

        :stability: deprecated
        '''
        result = self._values.get("propagate_tags")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reference_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The reference ID to use for the task.

        :default: - No reference ID.

        :stability: deprecated
        '''
        result = self._values.get("reference_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_groups(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]]:
        '''(deprecated) The security groups associated with the task.

        These security groups must all be in the same VPC.
        Controls inbound and outbound network access for the task.

        :default: - The security group for the VPC is used.

        :stability: deprecated
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[Tag]]:
        '''(deprecated) The metadata that you apply to the task to help you categorize and organize them.

        Each tag consists of a key and an optional value, both of which you define.

        :default: - No tags

        :stability: deprecated
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[Tag]], result)

    @builtins.property
    def task_count(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The number of tasks to create based on TaskDefinition.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("task_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection]:
        '''(deprecated) The subnets associated with the task.

        These subnets must all be in the same VPC.
        The task will be launched in these subnets.

        :default: - all private subnets of the VPC are selected.

        :stability: deprecated
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection], result)

    @builtins.property
    def placement_constraints(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]]:
        '''(deprecated) The rules that must be met in order to place a task on a container instance.

        :default: - No placement constraints.

        :stability: deprecated
        '''
        result = self._values.get("placement_constraints")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]], result)

    @builtins.property
    def placement_strategies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]]:
        '''(deprecated) The algorithm for selecting container instances for task placement.

        :default: - No placement strategies.

        :stability: deprecated
        '''
        result = self._values.get("placement_strategies")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Ec2TaskProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcsRunEc2Task(
    EcsRunTask,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EcsRunEc2Task",
):
    '''(deprecated) Schedule an ECS Task on EC2 using AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ecs as ecs
        
        # cluster: ecs.ICluster
        # task_definition: ecs.Ec2TaskDefinition
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
            target=targets.EcsRunEc2Task(cluster,
                task_definition=task_definition
            )
        )
    '''

    def __init__(
        self,
        cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
        *,
        placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]] = None,
        placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]] = None,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_execute_command: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        reference_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_count: typing.Optional[jsii.Number] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param cluster: -
        :param placement_constraints: (deprecated) The rules that must be met in order to place a task on a container instance. Default: - No placement constraints.
        :param placement_strategies: (deprecated) The algorithm for selecting container instances for task placement. Default: - No placement strategies.
        :param task_definition: (deprecated) The task definition to use for scheduled tasks. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions If you want to run a RunTask with an imported task definition, consider using a Universal target.
        :param capacity_provider_strategies: (deprecated) The capacity provider strategy to use for the task. Default: - No capacity provider strategy
        :param enable_ecs_managed_tags: (deprecated) Specifies whether to enable Amazon ECS managed tags for the task. Default: - false
        :param enable_execute_command: (deprecated) Whether to enable execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
        :param group: (deprecated) Specifies an ECS task group for the task. Default: - No group
        :param propagate_tags: (deprecated) Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Default: - No tag propagation
        :param reference_id: (deprecated) The reference ID to use for the task. Default: - No reference ID.
        :param security_groups: (deprecated) The security groups associated with the task. These security groups must all be in the same VPC. Controls inbound and outbound network access for the task. Default: - The security group for the VPC is used.
        :param tags: (deprecated) The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. Default: - No tags
        :param task_count: (deprecated) The number of tasks to create based on TaskDefinition. Default: 1
        :param vpc_subnets: (deprecated) The subnets associated with the task. These subnets must all be in the same VPC. The task will be launched in these subnets. Default: - all private subnets of the VPC are selected.
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cdfb98c0bca4d09075fa6400ac5fceb88642531739e078397d8551c17a5f6b0)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        props = Ec2TaskProps(
            placement_constraints=placement_constraints,
            placement_strategies=placement_strategies,
            task_definition=task_definition,
            capacity_provider_strategies=capacity_provider_strategies,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_execute_command=enable_execute_command,
            group=group,
            propagate_tags=propagate_tags,
            reference_id=reference_id,
            security_groups=security_groups,
            tags=tags,
            task_count=task_count,
            vpc_subnets=vpc_subnets,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [cluster, props])

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__740ba283c77351f16257e62be68268db0ced00821d327d5a97d1b6e9f3fabd5b)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


class EcsRunFargateTask(
    EcsRunTask,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-scheduler-targets-alpha.EcsRunFargateTask",
):
    '''(deprecated) Schedule an ECS Task on Fargate using AWS EventBridge Scheduler.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_ecs as ecs
        
        # cluster: ecs.ICluster
        # task_definition: ecs.FargateTaskDefinition
        
        
        Schedule(self, "Schedule",
            schedule=ScheduleExpression.rate(cdk.Duration.minutes(60)),
            target=targets.EcsRunFargateTask(cluster,
                task_definition=task_definition
            )
        )
    '''

    def __init__(
        self,
        cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
        *,
        assign_public_ip: typing.Optional[builtins.bool] = None,
        platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
        task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
        capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
        enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
        enable_execute_command: typing.Optional[builtins.bool] = None,
        group: typing.Optional[builtins.str] = None,
        propagate_tags: typing.Optional[builtins.bool] = None,
        reference_id: typing.Optional[builtins.str] = None,
        security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        task_count: typing.Optional[jsii.Number] = None,
        vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
        input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
        max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param cluster: -
        :param assign_public_ip: (deprecated) Specifies whether the task's elastic network interface receives a public IP address. If true, the task will receive a public IP address and be accessible from the internet. Should only be set to true when using public subnets. Default: - true if the subnet type is PUBLIC, otherwise false
        :param platform_version: (deprecated) Specifies the platform version for the task. Specify only the numeric portion of the platform version, such as 1.1.0. Platform versions determine the underlying runtime environment for the task. Default: - LATEST
        :param task_definition: (deprecated) The task definition to use for scheduled tasks. Note: this must be TaskDefinition, and not ITaskDefinition, as it requires properties that are not known for imported task definitions If you want to run a RunTask with an imported task definition, consider using a Universal target.
        :param capacity_provider_strategies: (deprecated) The capacity provider strategy to use for the task. Default: - No capacity provider strategy
        :param enable_ecs_managed_tags: (deprecated) Specifies whether to enable Amazon ECS managed tags for the task. Default: - false
        :param enable_execute_command: (deprecated) Whether to enable execute command functionality for the containers in this task. If true, this enables execute command functionality on all containers in the task. Default: - false
        :param group: (deprecated) Specifies an ECS task group for the task. Default: - No group
        :param propagate_tags: (deprecated) Specifies whether to propagate the tags from the task definition to the task. If no value is specified, the tags are not propagated. Default: - No tag propagation
        :param reference_id: (deprecated) The reference ID to use for the task. Default: - No reference ID.
        :param security_groups: (deprecated) The security groups associated with the task. These security groups must all be in the same VPC. Controls inbound and outbound network access for the task. Default: - The security group for the VPC is used.
        :param tags: (deprecated) The metadata that you apply to the task to help you categorize and organize them. Each tag consists of a key and an optional value, both of which you define. Default: - No tags
        :param task_count: (deprecated) The number of tasks to create based on TaskDefinition. Default: 1
        :param vpc_subnets: (deprecated) The subnets associated with the task. These subnets must all be in the same VPC. The task will be launched in these subnets. Default: - all private subnets of the VPC are selected.
        :param dead_letter_queue: (deprecated) The SQS queue to be used as deadLetterQueue. The events not successfully delivered are automatically retried for a specified period of time, depending on the retry policy of the target. If an event is not delivered before all retry attempts are exhausted, it will be sent to the dead letter queue. Default: - no dead-letter queue
        :param input: (deprecated) Input passed to the target. Default: - no input.
        :param max_event_age: (deprecated) The maximum age of a request that Scheduler sends to a target for processing. Minimum value of 60. Maximum value of 86400. Default: Duration.hours(24)
        :param retry_attempts: (deprecated) The maximum number of times to retry when the target returns an error. Minimum value of 0. Maximum value of 185. Default: 185
        :param role: (deprecated) An execution role is an IAM role that EventBridge Scheduler assumes in order to interact with other AWS services on your behalf. If none provided templates target will automatically create an IAM role with all the minimum necessary permissions to interact with the templated target. If you wish you may specify your own IAM role, then the templated targets will grant minimal required permissions. Default: - created by target

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e931f353f803a008bac926a0f16b3c22d5cae32589b845b84974c4acbce3168)
            check_type(argname="argument cluster", value=cluster, expected_type=type_hints["cluster"])
        props = FargateTaskProps(
            assign_public_ip=assign_public_ip,
            platform_version=platform_version,
            task_definition=task_definition,
            capacity_provider_strategies=capacity_provider_strategies,
            enable_ecs_managed_tags=enable_ecs_managed_tags,
            enable_execute_command=enable_execute_command,
            group=group,
            propagate_tags=propagate_tags,
            reference_id=reference_id,
            security_groups=security_groups,
            tags=tags,
            task_count=task_count,
            vpc_subnets=vpc_subnets,
            dead_letter_queue=dead_letter_queue,
            input=input,
            max_event_age=max_event_age,
            retry_attempts=retry_attempts,
            role=role,
        )

        jsii.create(self.__class__, self, [cluster, props])

    @jsii.member(jsii_name="bindBaseTargetConfig")
    def _bind_base_target_config(
        self,
        _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
    ) -> _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig:
        '''
        :param _schedule: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cabb218da3dcdf740cfc52e1ad263c6b7def347f5d466c25560b9436f302812)
            check_type(argname="argument _schedule", value=_schedule, expected_type=type_hints["_schedule"])
        return typing.cast(_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetConfig, jsii.invoke(self, "bindBaseTargetConfig", [_schedule]))


__all__ = [
    "CodeBuildStartBuild",
    "CodePipelineStartPipelineExecution",
    "Ec2TaskProps",
    "EcsRunEc2Task",
    "EcsRunFargateTask",
    "EcsRunTask",
    "EcsRunTaskBaseProps",
    "EventBridgePutEvents",
    "EventBridgePutEventsEntry",
    "FargateTaskProps",
    "FirehosePutRecord",
    "InspectorStartAssessmentRun",
    "KinesisStreamPutRecord",
    "KinesisStreamPutRecordProps",
    "LambdaInvoke",
    "SageMakerPipelineParameter",
    "SageMakerStartPipelineExecution",
    "SageMakerStartPipelineExecutionProps",
    "ScheduleTargetBase",
    "ScheduleTargetBaseProps",
    "SnsPublish",
    "SqsSendMessage",
    "SqsSendMessageProps",
    "StepFunctionsStartExecution",
    "Tag",
    "Universal",
    "UniversalTargetProps",
]

publication.publish()

def _typecheckingstub__c3b15c35d804ca95ff64ca0a6f312aaf0cec9780ee78849d0052cf3f113afad9(
    *,
    detail: _aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput,
    detail_type: builtins.str,
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1b671700562aea93d2c9aa01ca3ab4bbfcb0da81f14e336b02e175cc0e96bd(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10e59e7b340dc335b31c4a0d18b1845659c5a575671ec4c54fa176892cb9bd54(
    base_props: typing.Union[ScheduleTargetBaseProps, typing.Dict[builtins.str, typing.Any]],
    target_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50e82b6bad0ce8e66d78921fb69afc41cc589ff68e7fde7d3a116a558622ba0b(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d8230d421e6fe144b04cf440bae3b93c14a1af6ea5635fc876670037e3a4ee(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__610cc83281b440576390d0e3dbfaa9a65adba95233cb7ffdfba72197abc9da29(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e05948e70de09bca87c06a271bef4e0b3a07893d3e2112141ebdce3856e9e80(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b00545abc5c0db54c2d2809ed5b2f135fc5c44b02c318bc15d3634020e4633(
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6baf1dcdf0de6e124cffb230fe4fdc6f44a348db6477f1070fe2c1b55ef82665(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4813eef9ae399e4e7240ac6b9346c654577bf97511e9a71e43ce8856a8293f77(
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    *,
    message_group_id: typing.Optional[builtins.str] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5ab2b88a54bc5208c7d14e9744c6597c0f0301de5b4c60bb95d90849069e33(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b4e499db09ce4b94c98ac3cf9054d519de93d540d51895429b6af27d162a12(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b54bd4b76ef8c8d82a414b1afa05a0f9628f07ff40b7ecdd1db2ed2ee30fd9c7(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df2f5731f4fe761fad561cdd5177904d0685abe6cc827da58894e4519f3104d2(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16c6a822df4449b80b3088cf438b74a5c925845e7b3fe17b5671a96deceef76(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1726cc4bf58e2c200057667121a8ee2d9d93fcadffd2f641734413739895d69(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b165e37b986acfbce2c5790c15119e3cc82a80d92b64614b117e0dd3321a95(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9231c0ef7eec0af506feba01c6040b845d12fdfff9ba460bb02a9743da1166(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    action: builtins.str,
    service: builtins.str,
    policy_statements: typing.Optional[typing.Sequence[_aws_cdk_aws_iam_ceddda9d.PolicyStatement]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eee4f6daae6be7c2365ab2dfb373e3d4a03c594923664bb691da6e3795d41b16(
    project: _aws_cdk_aws_codebuild_ceddda9d.IProject,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__474fd9928553c6c25206d5a8cd8a15397a1e8091bdc5173fc92abdd167cfda07(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1179b8a788d46a78ad80abd38cd8f227eaf4ff63c93fb2ce58abfb9cf84a57aa(
    pipeline: _aws_cdk_aws_codepipeline_ceddda9d.IPipeline,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f97647f2f639edabbd7fc4d342abe0f255a5960ef5840c029bfc32962fa9769(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85532c687b6f71d597a01494dbe986934143e5ca7ec87233c62cf9c8f1a089e7(
    cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
    *,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_execute_command: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    reference_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466075cb50bd1b9d2bb19177d085bd137eee1bc35dcaaaa426c57a806bdedb24(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18807a341be4453df8cbab1b8803ad0e87c5baea5794dd8f389c391387b171ed(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f400535c3d9712c95444200b98975962e82c73d2cbe880613a73dd38bd615a13(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_execute_command: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    reference_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae28df8ed7b4d4cf0069c2078c852156338afac2e79eb10ab690c790a1efde31(
    entry: typing.Union[EventBridgePutEventsEntry, typing.Dict[builtins.str, typing.Any]],
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4d3987aace1577c0609c760b353ffad7b4806705694003c15c7ef457008811e(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe563fb16e465141154d47511f2ad5007930fbbc4c511a584457cd7a4285e684(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380374bd55cffc9977204bd6a28dd2ed054acaba3cf086012f6df8a51b726028(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_execute_command: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    reference_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d684916d9897133cc3263e5d11aea8dfa003e41c2d8e0deb7a1e1488f6d5a775(
    delivery_stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56c16109037f37fad1c95c9415fa5d65603ebae6c28a2daaec1156e2c04f2ab(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d7bbb3c9d358edb684284e6061143edea14a918d787e7b0de0abe8074adc3a8(
    template: _aws_cdk_aws_inspector_ceddda9d.IAssessmentTemplate,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f62115ee3101d95125c22cd00ce69aefcbf38ba32a31ec38c5fe32386b72a485(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3da8609af671f7e313f5b3391e0c519b97069ce30e7f39aaae4028df271ad968(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
    *,
    partition_key: builtins.str,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00e0c64cae92c47512d2b31480147546bdac967e14a67f989fced9ea65977ab(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901c2c170b31144628352155381f9212d91d6a15a1323004e8a2a1fc86211850(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450b2e09dbbdf0b1ab8f7ab50d92ab0bc3784cd7aebcc42382aa41af77149cf6(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cee0b6faf4f1c2dcade061e69cf02b9c302a868d55e47f591978024f5da0075(
    func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5bceedc3f4419f27eac20d417a223b3233c972e163393fd278acd75b7129d89(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cd1e092f776a22386cfd27fc1778ae00bc42ca6e1f29df07ab3c760bf88329(
    pipeline: _aws_cdk_aws_sagemaker_ceddda9d.IPipeline,
    *,
    pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a618244e0553e568cdf781844a2bbc64b2127af3cf8d23bbd6e2083ab5b1838(
    role: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0401259d77c4f97bb1b7a40ff1a9f35512d38224dee98a520446b9b7876f9acd(
    schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c01c7fd9ffc99ab1f2f2a61c89fe87963adc09f9e04fb878a3007c33ce123c(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    pipeline_parameter_list: typing.Optional[typing.Sequence[typing.Union[SageMakerPipelineParameter, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f492ba7877199e36fb5d299cbd93a8254f2a7ed12ec7c2a1a213be9399f002(
    *,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_execute_command: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    reference_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cdfb98c0bca4d09075fa6400ac5fceb88642531739e078397d8551c17a5f6b0(
    cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
    *,
    placement_constraints: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementConstraint]] = None,
    placement_strategies: typing.Optional[typing.Sequence[_aws_cdk_aws_ecs_ceddda9d.PlacementStrategy]] = None,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_execute_command: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    reference_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740ba283c77351f16257e62be68268db0ced00821d327d5a97d1b6e9f3fabd5b(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e931f353f803a008bac926a0f16b3c22d5cae32589b845b84974c4acbce3168(
    cluster: _aws_cdk_aws_ecs_ceddda9d.ICluster,
    *,
    assign_public_ip: typing.Optional[builtins.bool] = None,
    platform_version: typing.Optional[_aws_cdk_aws_ecs_ceddda9d.FargatePlatformVersion] = None,
    task_definition: _aws_cdk_aws_ecs_ceddda9d.TaskDefinition,
    capacity_provider_strategies: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_ecs_ceddda9d.CapacityProviderStrategy, typing.Dict[builtins.str, typing.Any]]]] = None,
    enable_ecs_managed_tags: typing.Optional[builtins.bool] = None,
    enable_execute_command: typing.Optional[builtins.bool] = None,
    group: typing.Optional[builtins.str] = None,
    propagate_tags: typing.Optional[builtins.bool] = None,
    reference_id: typing.Optional[builtins.str] = None,
    security_groups: typing.Optional[typing.Sequence[_aws_cdk_aws_ec2_ceddda9d.ISecurityGroup]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    task_count: typing.Optional[jsii.Number] = None,
    vpc_subnets: typing.Optional[typing.Union[_aws_cdk_aws_ec2_ceddda9d.SubnetSelection, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_aws_cdk_aws_sqs_ceddda9d.IQueue] = None,
    input: typing.Optional[_aws_cdk_aws_scheduler_alpha_61df44e1.ScheduleTargetInput] = None,
    max_event_age: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cabb218da3dcdf740cfc52e1ad263c6b7def347f5d466c25560b9436f302812(
    _schedule: _aws_cdk_aws_scheduler_alpha_61df44e1.ISchedule,
) -> None:
    """Type checking stubs"""
    pass
