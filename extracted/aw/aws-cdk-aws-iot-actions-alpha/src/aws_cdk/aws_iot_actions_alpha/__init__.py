r'''
# Actions for AWS IoT Rule

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

This library contains integration classes to send data to any number of
supported AWS Services. Instances of these classes should be passed to
`TopicRule` defined in `aws-cdk-lib/aws-iot`.

Currently supported are:

* Republish a message to another MQTT topic
* Invoke a Lambda function
* Put objects to a S3 bucket
* Put logs to CloudWatch Logs
* Capture CloudWatch metrics
* Change state for a CloudWatch alarm
* Put records to Kinesis Data stream
* Put records to Amazon Data Firehose stream
* Send messages to SQS queues
* Publish messages on SNS topics
* Write messages into columns of DynamoDB
* Put messages IoT Events input
* Send messages to HTTPS endpoints

## Republish a message to another MQTT topic

The code snippet below creates an AWS IoT Rule that republish a message to
another MQTT topic when it is triggered.

```python
iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
    actions=[
        actions.IotRepublishMqttAction("${topic()}/republish",
            quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
        )
    ]
)
```

## Invoke a Lambda function

The code snippet below creates an AWS IoT Rule that invoke a Lambda function
when it is triggered.

```python
func = lambda_.Function(self, "MyFunction",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    handler="index.handler",
    code=lambda_.Code.from_inline("""
            exports.handler = (event) => {
              console.log("It is test for lambda action of AWS IoT Rule.", event);
            };""")
)

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
    actions=[actions.LambdaFunctionAction(func)]
)
```

## Put objects to a S3 bucket

The code snippet below creates an AWS IoT Rule that puts objects to a S3 bucket
when it is triggered.

```python
bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[actions.S3PutObjectAction(bucket)]
)
```

The property `key` of `S3PutObjectAction` is given the value `${topic()}/${timestamp()}` by default. This `${topic()}`
and `${timestamp()}` is called Substitution templates. For more information see
[this documentation](https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html).
In above sample, `${topic()}` is replaced by a given MQTT topic as `device/001/data`. And `${timestamp()}` is replaced
by the number of the current timestamp in milliseconds as `1636289461203`. So if the MQTT broker receives an MQTT topic
`device/001/data` on `2021-11-07T00:00:00.000Z`, the S3 bucket object will be put to `device/001/data/1636243200000`.

You can also set specific `key` as following:

```python
bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.S3PutObjectAction(bucket,
            key="${year}/${month}/${day}/${topic(2)}"
        )
    ]
)
```

If you wanna set access control to the S3 bucket object, you can specify `accessControl` as following:

```python
bucket = s3.Bucket(self, "MyBucket")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.S3PutObjectAction(bucket,
            access_control=s3.BucketAccessControl.PUBLIC_READ
        )
    ]
)
```

## Put logs to CloudWatch Logs

The code snippet below creates an AWS IoT Rule that puts logs to CloudWatch Logs
when it is triggered.

```python
import aws_cdk.aws_logs as logs


log_group = logs.LogGroup(self, "MyLogGroup")

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[actions.CloudWatchLogsAction(log_group)]
)
```

## Capture CloudWatch metrics

The code snippet below creates an AWS IoT Rule that capture CloudWatch metrics
when it is triggered.

```python
topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, namespace, unit, value, timestamp FROM 'device/+/data'"),
    actions=[
        actions.CloudWatchPutMetricAction(
            metric_name="${topic(2)}",
            metric_namespace="${namespace}",
            metric_unit="${unit}",
            metric_value="${value}",
            metric_timestamp="${timestamp}"
        )
    ]
)
```

## Start Step Functions State Machine

The code snippet below creates an AWS IoT Rule that starts a Step Functions State Machine
when it is triggered.

```python
state_machine = stepfunctions.StateMachine(self, "SM",
    definition_body=stepfunctions.DefinitionBody.from_chainable(stepfunctions.Wait(self, "Hello", time=stepfunctions.WaitTime.duration(Duration.seconds(10))))
)

iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.StepFunctionsStateMachineAction(state_machine)
    ]
)
```

## Change the state of an Amazon CloudWatch alarm

The code snippet below creates an AWS IoT Rule that changes the state of an Amazon CloudWatch alarm when it is triggered:

```python
import aws_cdk.aws_cloudwatch as cloudwatch


metric = cloudwatch.Metric(
    namespace="MyNamespace",
    metric_name="MyMetric",
    dimensions_map={"MyDimension": "MyDimensionValue"}
)
alarm = cloudwatch.Alarm(self, "MyAlarm",
    metric=metric,
    threshold=100,
    evaluation_periods=3,
    datapoints_to_alarm=2
)

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
    actions=[
        actions.CloudWatchSetAlarmStateAction(alarm,
            reason="AWS Iot Rule action is triggered",
            alarm_state_to_set=cloudwatch.AlarmState.ALARM
        )
    ]
)
```

## Put records to Kinesis Data stream

The code snippet below creates an AWS IoT Rule that puts records to Kinesis Data
stream when it is triggered.

```python
import aws_cdk.aws_kinesis as kinesis


stream = kinesis.Stream(self, "MyStream")

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.KinesisPutRecordAction(stream,
            partition_key="${newuuid()}"
        )
    ]
)
```

## Put records to Amazon Data Firehose stream

The code snippet below creates an AWS IoT Rule that puts records to Put records
to Amazon Data Firehose stream when it is triggered.

```python
import aws_cdk.aws_kinesisfirehose as firehose


bucket = s3.Bucket(self, "MyBucket")
stream = firehose.DeliveryStream(self, "MyStream",
    destination=firehose.S3Bucket(bucket)
)

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.FirehosePutRecordAction(stream,
            batch_mode=True,
            record_separator=actions.FirehoseRecordSeparator.NEWLINE
        )
    ]
)
```

## Send messages to an SQS queue

The code snippet below creates an AWS IoT Rule that send messages
to an SQS queue when it is triggered:

```python
import aws_cdk.aws_sqs as sqs


queue = sqs.Queue(self, "MyQueue")

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.SqsQueueAction(queue,
            use_base64=True
        )
    ]
)
```

## Publish messages on an SNS topic

The code snippet below creates and AWS IoT Rule that publishes messages to an SNS topic when it is triggered:

```python
import aws_cdk.aws_sns as sns


topic = sns.Topic(self, "MyTopic")

topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
    actions=[
        actions.SnsTopicAction(topic,
            message_format=actions.SnsActionMessageFormat.JSON
        )
    ]
)
```

## Write attributes of a message to DynamoDB

The code snippet below creates an AWS IoT rule that writes all or part of an
MQTT message to DynamoDB using the DynamoDBv2 action.

```python
import aws_cdk.aws_dynamodb as dynamodb

# table: dynamodb.Table


topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.DynamoDBv2PutItemAction(table)
    ]
)
```

## Put messages IoT Events input

The code snippet below creates an AWS IoT Rule that puts messages
to an IoT Events input when it is triggered:

```python
import aws_cdk.aws_iotevents_alpha as iotevents
import aws_cdk.aws_iam as iam

# role: iam.IRole


input = iotevents.Input(self, "MyInput",
    attribute_json_paths=["payload.temperature", "payload.transactionId"]
)
topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
    actions=[
        actions.IotEventsPutMessageAction(input,
            batch_mode=True,  # optional property, default is 'false'
            message_id="${payload.transactionId}",  # optional property, default is a new UUID
            role=role
        )
    ]
)
```

## Send Messages to HTTPS Endpoints

The code snippet below creates an AWS IoT Rule that sends messages
to an HTTPS endpoint when it is triggered:

```python
topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
)

topic_rule.add_action(
    actions.HttpsAction("https://example.com/endpoint",
        confirmation_url="https://example.com",
        headers=[actions.HttpActionHeader(key="key0", value="value0"), actions.HttpActionHeader(key="key1", value="value1")
        ],
        auth=actions.HttpActionSigV4Auth(service_name="serviceName", signing_region="us-east-1")
    ))
```

## Write Data to Open Search Service

The code snippet below creates an AWS IoT Rule that writes data
to an Open Search Service when it is triggered:

```python
import aws_cdk.aws_opensearchservice as opensearch
# domain: opensearch.Domain


topic_rule = iot.TopicRule(self, "TopicRule",
    sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
)

topic_rule.add_action(actions.OpenSearchAction(domain,
    id="my-id",
    index="my-index",
    type="my-type"
))
```
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

import aws_cdk.aws_cloudwatch as _aws_cdk_aws_cloudwatch_ceddda9d
import aws_cdk.aws_dynamodb as _aws_cdk_aws_dynamodb_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_iot_alpha as _aws_cdk_aws_iot_alpha_eb933819
import aws_cdk.aws_iotevents_alpha as _aws_cdk_aws_iotevents_alpha_39cbd76e
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_opensearchservice as _aws_cdk_aws_opensearchservice_ceddda9d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class CloudWatchLogsAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CloudWatchLogsAction",
):
    '''(experimental) The action to send data to Amazon CloudWatch Logs.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_logs as logs
        
        
        log_group = logs.LogGroup(self, "MyLogGroup")
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp FROM 'device/+/data'"),
            error_action=actions.CloudWatchLogsAction(log_group)
        )
    '''

    def __init__(
        self,
        log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param log_group: The CloudWatch log group to which the action sends data.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1125f9dca9ec8ed30503b3089fce98893e99b37a4834cfd883136ea340ad05cb)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        props = CloudWatchLogsActionProps(role=role)

        jsii.create(self.__class__, self, [log_group, props])


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class CloudWatchPutMetricAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CloudWatchPutMetricAction",
):
    '''(experimental) The action to capture an Amazon CloudWatch metric.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, namespace, unit, value, timestamp FROM 'device/+/data'"),
            actions=[
                actions.CloudWatchPutMetricAction(
                    metric_name="${topic(2)}",
                    metric_namespace="${namespace}",
                    metric_unit="${unit}",
                    metric_value="${value}",
                    metric_timestamp="${timestamp}"
                )
            ]
        )
    '''

    def __init__(
        self,
        *,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param metric_name: (experimental) The CloudWatch metric name. Supports substitution templates.
        :param metric_namespace: (experimental) The CloudWatch metric namespace name. Supports substitution templates.
        :param metric_unit: (experimental) The metric unit supported by CloudWatch. Supports substitution templates.
        :param metric_value: (experimental) A string that contains the CloudWatch metric value. Supports substitution templates.
        :param metric_timestamp: (experimental) A string that contains the timestamp, expressed in seconds in Unix epoch time. Supports substitution templates. Default: - none -- Defaults to the current Unix epoch time.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        props = CloudWatchPutMetricActionProps(
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            metric_unit=metric_unit,
            metric_value=metric_value,
            metric_timestamp=metric_timestamp,
            role=role,
        )

        jsii.create(self.__class__, self, [props])


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class CloudWatchSetAlarmStateAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CloudWatchSetAlarmStateAction",
):
    '''(experimental) The action to change the state of an Amazon CloudWatch alarm.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_cloudwatch as cloudwatch
        
        
        metric = cloudwatch.Metric(
            namespace="MyNamespace",
            metric_name="MyMetric",
            dimensions_map={"MyDimension": "MyDimensionValue"}
        )
        alarm = cloudwatch.Alarm(self, "MyAlarm",
            metric=metric,
            threshold=100,
            evaluation_periods=3,
            datapoints_to_alarm=2
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
            actions=[
                actions.CloudWatchSetAlarmStateAction(alarm,
                    reason="AWS Iot Rule action is triggered",
                    alarm_state_to_set=cloudwatch.AlarmState.ALARM
                )
            ]
        )
    '''

    def __init__(
        self,
        alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
        *,
        alarm_state_to_set: _aws_cdk_aws_cloudwatch_ceddda9d.AlarmState,
        reason: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param alarm: -
        :param alarm_state_to_set: (experimental) The value of the alarm state to set.
        :param reason: (experimental) The reason for the alarm change. Default: None
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc507afa1602d7648fd445cf653eafff0694945ad00db2eb11461c754c2b00b)
            check_type(argname="argument alarm", value=alarm, expected_type=type_hints["alarm"])
        props = CloudWatchSetAlarmStateActionProps(
            alarm_state_to_set=alarm_state_to_set, reason=reason, role=role
        )

        jsii.create(self.__class__, self, [alarm, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CommonActionProps",
    jsii_struct_bases=[],
    name_mapping={"role": "role"},
)
class CommonActionProps:
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Common properties shared by Actions it access to AWS service.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_actions_alpha as iot_actions_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            common_action_props = iot_actions_alpha.CommonActionProps(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8c5f84dc199f2aa55e9c7b72978de6e47482c21c07fb8845141664e7ba4e7ce)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class DynamoDBv2PutItemAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.DynamoDBv2PutItemAction",
):
    '''(experimental) The action to put the record from an MQTT message to the DynamoDB table.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_dynamodb as dynamodb
        
        # table: dynamodb.Table
        
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.DynamoDBv2PutItemAction(table)
            ]
        )
    '''

    def __init__(
        self,
        table: _aws_cdk_aws_dynamodb_ceddda9d.ITable,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param table: the DynamoDB table in which to put the items.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9242ff0039c5f5f20a1fcc4613ee02b20617db70446ef5e7cbe185ebec5fa338)
            check_type(argname="argument table", value=table, expected_type=type_hints["table"])
        props = DynamoDBv2PutItemActionProps(role=role)

        jsii.create(self.__class__, self, [table, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.DynamoDBv2PutItemActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role"},
)
class DynamoDBv2PutItemActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for the dynamodb table.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_actions_alpha as iot_actions_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            dynamo_dBv2_put_item_action_props = iot_actions_alpha.DynamoDBv2PutItemActionProps(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5006dd434137a2ed9cdc6c97b24a6a3424c93db9f39d65c8aff4f62493513268)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DynamoDBv2PutItemActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class FirehosePutRecordAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.FirehosePutRecordAction",
):
    '''(experimental) The action to put the record from an MQTT message to the Amazon Data Firehose stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesisfirehose as firehose
        
        
        bucket = s3.Bucket(self, "MyBucket")
        stream = firehose.DeliveryStream(self, "MyStream",
            destination=firehose.S3Bucket(bucket)
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.FirehosePutRecordAction(stream,
                    batch_mode=True,
                    record_separator=actions.FirehoseRecordSeparator.NEWLINE
                )
            ]
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
        *,
        batch_mode: typing.Optional[builtins.bool] = None,
        record_separator: typing.Optional["FirehoseRecordSeparator"] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param stream: The Amazon Data Firehose stream to which to put records.
        :param batch_mode: (experimental) Whether to deliver the Amazon Data Firehose stream as a batch by using ``PutRecordBatch``. When batchMode is true and the rule's SQL statement evaluates to an Array, each Array element forms one record in the PutRecordBatch request. The resulting array can't have more than 500 records. Default: false
        :param record_separator: (experimental) A character separator that will be used to separate records written to the Amazon Data Firehose stream. Default: - none -- the stream does not use a separator
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b1862de154dea8afd9a05c2e43c9e12d06dd718f02f029ad7e9defe76176f5d)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = FirehosePutRecordActionProps(
            batch_mode=batch_mode, record_separator=record_separator, role=role
        )

        jsii.create(self.__class__, self, [stream, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.FirehosePutRecordActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "batch_mode": "batchMode",
        "record_separator": "recordSeparator",
    },
)
class FirehosePutRecordActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        batch_mode: typing.Optional[builtins.bool] = None,
        record_separator: typing.Optional["FirehoseRecordSeparator"] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for the Amazon Data Firehose stream.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param batch_mode: (experimental) Whether to deliver the Amazon Data Firehose stream as a batch by using ``PutRecordBatch``. When batchMode is true and the rule's SQL statement evaluates to an Array, each Array element forms one record in the PutRecordBatch request. The resulting array can't have more than 500 records. Default: false
        :param record_separator: (experimental) A character separator that will be used to separate records written to the Amazon Data Firehose stream. Default: - none -- the stream does not use a separator

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_kinesisfirehose as firehose
            
            
            bucket = s3.Bucket(self, "MyBucket")
            stream = firehose.DeliveryStream(self, "MyStream",
                destination=firehose.S3Bucket(bucket)
            )
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
                actions=[
                    actions.FirehosePutRecordAction(stream,
                        batch_mode=True,
                        record_separator=actions.FirehoseRecordSeparator.NEWLINE
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a372426adf9237fb413c0109f8f86481ab2cefcb2d867a7cd22fd0ac4160dd82)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument record_separator", value=record_separator, expected_type=type_hints["record_separator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if record_separator is not None:
            self._values["record_separator"] = record_separator

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def batch_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to deliver the Amazon Data Firehose stream as a batch by using ``PutRecordBatch``.

        When batchMode is true and the rule's SQL statement evaluates to an Array, each Array
        element forms one record in the PutRecordBatch request. The resulting array can't have
        more than 500 records.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def record_separator(self) -> typing.Optional["FirehoseRecordSeparator"]:
        '''(experimental) A character separator that will be used to separate records written to the Amazon Data Firehose stream.

        :default: - none -- the stream does not use a separator

        :stability: experimental
        '''
        result = self._values.get("record_separator")
        return typing.cast(typing.Optional["FirehoseRecordSeparator"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirehosePutRecordActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iot-actions-alpha.FirehoseRecordSeparator")
class FirehoseRecordSeparator(enum.Enum):
    '''(experimental) Record Separator to be used to separate records.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesisfirehose as firehose
        
        
        bucket = s3.Bucket(self, "MyBucket")
        stream = firehose.DeliveryStream(self, "MyStream",
            destination=firehose.S3Bucket(bucket)
        )
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.FirehosePutRecordAction(stream,
                    batch_mode=True,
                    record_separator=actions.FirehoseRecordSeparator.NEWLINE
                )
            ]
        )
    '''

    NEWLINE = "NEWLINE"
    '''(experimental) Separate by a new line.

    :stability: experimental
    '''
    TAB = "TAB"
    '''(experimental) Separate by a tab.

    :stability: experimental
    '''
    WINDOWS_NEWLINE = "WINDOWS_NEWLINE"
    '''(experimental) Separate by a windows new line.

    :stability: experimental
    '''
    COMMA = "COMMA"
    '''(experimental) Separate by a comma.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.HttpActionHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class HttpActionHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: (experimental) The HTTP header key.
        :param value: (experimental) The HTTP header value. Substitution templates are supported.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_actions_alpha as iot_actions_alpha
            
            http_action_header = iot_actions_alpha.HttpActionHeader(
                key="key",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca282425917f2fd79daa77c3313ac246d547984b2140f896e262c1ec5dbb9879)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) The HTTP header key.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) The HTTP header value.

        Substitution templates are supported.

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpActionHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.HttpActionSigV4Auth",
    jsii_struct_bases=[],
    name_mapping={"service_name": "serviceName", "signing_region": "signingRegion"},
)
class HttpActionSigV4Auth:
    def __init__(
        self,
        *,
        service_name: builtins.str,
        signing_region: builtins.str,
    ) -> None:
        '''
        :param service_name: (experimental) The service name.
        :param signing_region: (experimental) The signing region.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
            )
            
            topic_rule.add_action(
                actions.HttpsAction("https://example.com/endpoint",
                    confirmation_url="https://example.com",
                    headers=[actions.HttpActionHeader(key="key0", value="value0"), actions.HttpActionHeader(key="key1", value="value1")
                    ],
                    auth=actions.HttpActionSigV4Auth(service_name="serviceName", signing_region="us-east-1")
                ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b59e93ae19615b8937eb25644e8d247753f0996ddd5ee40af6b299f32e12bd3)
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument signing_region", value=signing_region, expected_type=type_hints["signing_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service_name": service_name,
            "signing_region": signing_region,
        }

    @builtins.property
    def service_name(self) -> builtins.str:
        '''(experimental) The service name.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def signing_region(self) -> builtins.str:
        '''(experimental) The signing region.

        :stability: experimental
        '''
        result = self._values.get("signing_region")
        assert result is not None, "Required property 'signing_region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpActionSigV4Auth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class HttpsAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.HttpsAction",
):
    '''(experimental) The action to send data from an MQTT message to a web application or service.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
        )
        
        topic_rule.add_action(
            actions.HttpsAction("https://example.com/endpoint",
                confirmation_url="https://example.com",
                headers=[actions.HttpActionHeader(key="key0", value="value0"), actions.HttpActionHeader(key="key1", value="value1")
                ],
                auth=actions.HttpActionSigV4Auth(service_name="serviceName", signing_region="us-east-1")
            ))
    '''

    def __init__(
        self,
        url: builtins.str,
        *,
        auth: typing.Optional[typing.Union[HttpActionSigV4Auth, typing.Dict[builtins.str, typing.Any]]] = None,
        confirmation_url: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Sequence[typing.Union[HttpActionHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param url: The url to which to send post request.
        :param auth: (experimental) Use Sigv4 authorization.
        :param confirmation_url: (experimental) If specified, AWS IoT uses the confirmation URL to create a matching topic rule destination.
        :param headers: (experimental) The headers to include in the HTTPS request to the endpoint.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c87b0804f95979b48d6a924424abe8ebf192fbcfebc6aecf6436690d1019d6ad)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        props = HttpsActionProps(
            auth=auth, confirmation_url=confirmation_url, headers=headers, role=role
        )

        jsii.create(self.__class__, self, [url, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.HttpsActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "auth": "auth",
        "confirmation_url": "confirmationUrl",
        "headers": "headers",
    },
)
class HttpsActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        auth: typing.Optional[typing.Union[HttpActionSigV4Auth, typing.Dict[builtins.str, typing.Any]]] = None,
        confirmation_url: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Sequence[typing.Union[HttpActionHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Configuration properties of an HTTPS action.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param auth: (experimental) Use Sigv4 authorization.
        :param confirmation_url: (experimental) If specified, AWS IoT uses the confirmation URL to create a matching topic rule destination.
        :param headers: (experimental) The headers to include in the HTTPS request to the endpoint.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/https-rule-action.html
        :stability: experimental
        :exampleMetadata: infused

        Example::

            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
            )
            
            topic_rule.add_action(
                actions.HttpsAction("https://example.com/endpoint",
                    confirmation_url="https://example.com",
                    headers=[actions.HttpActionHeader(key="key0", value="value0"), actions.HttpActionHeader(key="key1", value="value1")
                    ],
                    auth=actions.HttpActionSigV4Auth(service_name="serviceName", signing_region="us-east-1")
                ))
        '''
        if isinstance(auth, dict):
            auth = HttpActionSigV4Auth(**auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed57e014b0887a84984c84f8ad94782b2b5efe0e853a018ecb7cde520af055ac)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument confirmation_url", value=confirmation_url, expected_type=type_hints["confirmation_url"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if auth is not None:
            self._values["auth"] = auth
        if confirmation_url is not None:
            self._values["confirmation_url"] = confirmation_url
        if headers is not None:
            self._values["headers"] = headers

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def auth(self) -> typing.Optional[HttpActionSigV4Auth]:
        '''(experimental) Use Sigv4 authorization.

        :stability: experimental
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional[HttpActionSigV4Auth], result)

    @builtins.property
    def confirmation_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) If specified, AWS IoT uses the confirmation URL to create a matching topic rule destination.

        :stability: experimental
        '''
        result = self._values.get("confirmation_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(self) -> typing.Optional[typing.List[HttpActionHeader]]:
        '''(experimental) The headers to include in the HTTPS request to the endpoint.

        :stability: experimental
        '''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.List[HttpActionHeader]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class IotEventsPutMessageAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.IotEventsPutMessageAction",
):
    '''(experimental) The action to put the message from an MQTT message to the IoT Events input.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_iotevents_alpha as iotevents
        import aws_cdk.aws_iam as iam
        
        # role: iam.IRole
        
        
        input = iotevents.Input(self, "MyInput",
            attribute_json_paths=["payload.temperature", "payload.transactionId"]
        )
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.IotEventsPutMessageAction(input,
                    batch_mode=True,  # optional property, default is 'false'
                    message_id="${payload.transactionId}",  # optional property, default is a new UUID
                    role=role
                )
            ]
        )
    '''

    def __init__(
        self,
        input: _aws_cdk_aws_iotevents_alpha_39cbd76e.IInput,
        *,
        batch_mode: typing.Optional[builtins.bool] = None,
        message_id: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param input: The IoT Events input to put messages.
        :param batch_mode: (experimental) Whether to process the event actions as a batch. When batchMode is true, you can't specify a messageId. When batchMode is true and the rule SQL statement evaluates to an Array, each Array element is treated as a separate message when Events by calling BatchPutMessage. The resulting array can't have more than 10 messages. Default: false
        :param message_id: (experimental) The ID of the message. When batchMode is true, you can't specify a messageId--a new UUID value will be assigned. Assign a value to this property to ensure that only one input (message) with a given messageId will be processed by an AWS IoT Events detector. Default: - none -- a new UUID value will be assigned
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fd382f1f47362d144397e527978352f762c1785375ec37658992a8a487b4cf8)
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
        props = IotEventsPutMessageActionProps(
            batch_mode=batch_mode, message_id=message_id, role=role
        )

        jsii.create(self.__class__, self, [input, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.IotEventsPutMessageActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "batch_mode": "batchMode",
        "message_id": "messageId",
    },
)
class IotEventsPutMessageActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        batch_mode: typing.Optional[builtins.bool] = None,
        message_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for the IoT Events.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param batch_mode: (experimental) Whether to process the event actions as a batch. When batchMode is true, you can't specify a messageId. When batchMode is true and the rule SQL statement evaluates to an Array, each Array element is treated as a separate message when Events by calling BatchPutMessage. The resulting array can't have more than 10 messages. Default: false
        :param message_id: (experimental) The ID of the message. When batchMode is true, you can't specify a messageId--a new UUID value will be assigned. Assign a value to this property to ensure that only one input (message) with a given messageId will be processed by an AWS IoT Events detector. Default: - none -- a new UUID value will be assigned

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_iotevents_alpha as iotevents
            import aws_cdk.aws_iam as iam
            
            # role: iam.IRole
            
            
            input = iotevents.Input(self, "MyInput",
                attribute_json_paths=["payload.temperature", "payload.transactionId"]
            )
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
                actions=[
                    actions.IotEventsPutMessageAction(input,
                        batch_mode=True,  # optional property, default is 'false'
                        message_id="${payload.transactionId}",  # optional property, default is a new UUID
                        role=role
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc9e90430c80165cefadf2e647f22c5429762d648559fb693f79190265f6f91)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument batch_mode", value=batch_mode, expected_type=type_hints["batch_mode"])
            check_type(argname="argument message_id", value=message_id, expected_type=type_hints["message_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if batch_mode is not None:
            self._values["batch_mode"] = batch_mode
        if message_id is not None:
            self._values["message_id"] = message_id

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def batch_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to process the event actions as a batch.

        When batchMode is true, you can't specify a messageId.

        When batchMode is true and the rule SQL statement evaluates to an Array,
        each Array element is treated as a separate message when Events by calling BatchPutMessage.
        The resulting array can't have more than 10 messages.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("batch_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def message_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ID of the message.

        When batchMode is true, you can't specify a messageId--a new UUID value will be assigned.
        Assign a value to this property to ensure that only one input (message) with a given messageId will be processed by an AWS IoT Events detector.

        :default: - none -- a new UUID value will be assigned

        :stability: experimental
        '''
        result = self._values.get("message_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotEventsPutMessageActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class IotRepublishMqttAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.IotRepublishMqttAction",
):
    '''(experimental) The action to put the record from an MQTT message to republish another MQTT topic.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
            actions=[
                actions.IotRepublishMqttAction("${topic()}/republish",
                    quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
                )
            ]
        )
    '''

    def __init__(
        self,
        topic: builtins.str,
        *,
        quality_of_service: typing.Optional["MqttQualityOfService"] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param topic: The MQTT topic to which to republish the message.
        :param quality_of_service: (experimental) The Quality of Service (QoS) level to use when republishing messages. Default: MqttQualityOfService.ZERO_OR_MORE_TIMES
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39706bd98f00c288466b2a1f3248a337c500a5d9800d73998fb329410490355)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = IotRepublishMqttActionProps(
            quality_of_service=quality_of_service, role=role
        )

        jsii.create(self.__class__, self, [topic, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.IotRepublishMqttActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "quality_of_service": "qualityOfService"},
)
class IotRepublishMqttActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        quality_of_service: typing.Optional["MqttQualityOfService"] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action to republish MQTT messages.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param quality_of_service: (experimental) The Quality of Service (QoS) level to use when republishing messages. Default: MqttQualityOfService.ZERO_OR_MORE_TIMES

        :stability: experimental
        :exampleMetadata: infused

        Example::

            iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
                actions=[
                    actions.IotRepublishMqttAction("${topic()}/republish",
                        quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854cc7d880adf3faaf99230c4da2141389719c911cc9ff25daf3e31267da2ba7)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument quality_of_service", value=quality_of_service, expected_type=type_hints["quality_of_service"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if quality_of_service is not None:
            self._values["quality_of_service"] = quality_of_service

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def quality_of_service(self) -> typing.Optional["MqttQualityOfService"]:
        '''(experimental) The Quality of Service (QoS) level to use when republishing messages.

        :default: MqttQualityOfService.ZERO_OR_MORE_TIMES

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html#mqtt-qos
        :stability: experimental
        '''
        result = self._values.get("quality_of_service")
        return typing.cast(typing.Optional["MqttQualityOfService"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotRepublishMqttActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class KinesisPutRecordAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.KinesisPutRecordAction",
):
    '''(experimental) The action to put the record from an MQTT message to the Kinesis Data stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_kinesis as kinesis
        
        
        stream = kinesis.Stream(self, "MyStream")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.KinesisPutRecordAction(stream,
                    partition_key="${newuuid()}"
                )
            ]
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
        *,
        partition_key: builtins.str,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param stream: The Kinesis Data stream to which to put records.
        :param partition_key: (experimental) The partition key used to determine to which shard the data is written. The partition key is usually composed of an expression (for example, ${topic()} or ${timestamp()}).
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f906af38759ce5ba22880ad819a9e8e2eebfc2b90b06b2935a18ed5516ca8c)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        props = KinesisPutRecordActionProps(partition_key=partition_key, role=role)

        jsii.create(self.__class__, self, [stream, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.KinesisPutRecordActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "partition_key": "partitionKey"},
)
class KinesisPutRecordActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        partition_key: builtins.str,
    ) -> None:
        '''(experimental) Configuration properties of an action for the Kinesis Data stream.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param partition_key: (experimental) The partition key used to determine to which shard the data is written. The partition key is usually composed of an expression (for example, ${topic()} or ${timestamp()}).

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_kinesis as kinesis
            
            
            stream = kinesis.Stream(self, "MyStream")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
                actions=[
                    actions.KinesisPutRecordAction(stream,
                        partition_key="${newuuid()}"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42ab71684b75c91d7e19999242605bbbcf0ebeed49e9e93eb0a07ff42713e97d)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''(experimental) The partition key used to determine to which shard the data is written.

        The partition key is usually composed of an expression (for example, ${topic()} or ${timestamp()}).

        :see: https://docs.aws.amazon.com/kinesis/latest/APIReference/API_PutRecord.html#API_PutRecord_RequestParameters
        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisPutRecordActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class LambdaFunctionAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.LambdaFunctionAction",
):
    '''(experimental) The action to invoke an AWS Lambda function, passing in an MQTT message.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        func = lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_LATEST,
            handler="index.handler",
            code=lambda_.Code.from_inline("""
                    exports.handler = (event) => {
                      console.log("It is test for lambda action of AWS IoT Rule.", event);
                    };""")
        )
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
            actions=[actions.LambdaFunctionAction(func)]
        )
    '''

    def __init__(self, func: _aws_cdk_aws_lambda_ceddda9d.IFunction) -> None:
        '''
        :param func: The lambda function to be invoked by this action.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b93d28232c9e366b4b8112099c693914bd7bf1c15baab0bdc99040cab6073a3)
            check_type(argname="argument func", value=func, expected_type=type_hints["func"])
        jsii.create(self.__class__, self, [func])


@jsii.enum(jsii_type="@aws-cdk/aws-iot-actions-alpha.MqttQualityOfService")
class MqttQualityOfService(enum.Enum):
    '''(experimental) MQTT Quality of Service (QoS) indicates the level of assurance for delivery of an MQTT Message.

    :see: https://docs.aws.amazon.com/iot/latest/developerguide/mqtt.html#mqtt-qos
    :stability: experimental
    :exampleMetadata: infused

    Example::

        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, timestamp() as timestamp, temperature FROM 'device/+/data'"),
            actions=[
                actions.IotRepublishMqttAction("${topic()}/republish",
                    quality_of_service=actions.MqttQualityOfService.AT_LEAST_ONCE
                )
            ]
        )
    '''

    ZERO_OR_MORE_TIMES = "ZERO_OR_MORE_TIMES"
    '''(experimental) QoS level 0.

    Sent zero or more times.
    This level should be used for messages that are sent over reliable communication links or that can be missed without a problem.

    :stability: experimental
    '''
    AT_LEAST_ONCE = "AT_LEAST_ONCE"
    '''(experimental) QoS level 1.

    Sent at least one time, and then repeatedly until a PUBACK response is received.
    The message is not considered complete until the sender receives a PUBACK response to indicate successful delivery.

    :stability: experimental
    '''


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class OpenSearchAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.OpenSearchAction",
):
    '''(experimental) The action to write data to an Amazon OpenSearch Service domain.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_opensearchservice as opensearch
        # domain: opensearch.Domain
        
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
        )
        
        topic_rule.add_action(actions.OpenSearchAction(domain,
            id="my-id",
            index="my-index",
            type="my-type"
        ))
    '''

    def __init__(
        self,
        domain: _aws_cdk_aws_opensearchservice_ceddda9d.Domain,
        *,
        id: builtins.str,
        index: builtins.str,
        type: builtins.str,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param domain: -
        :param id: (experimental) The unique identifier for the document you are storing.
        :param index: (experimental) The OpenSearch index where you want to store your data.
        :param type: (experimental) The type of document you are storing.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3920392688b421d7e2aa469667b4ced037e78a50f767b308c0052982bae1ce)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
        props = OpenSearchActionProps(id=id, index=index, type=type, role=role)

        jsii.create(self.__class__, self, [domain, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.OpenSearchActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "id": "id", "index": "index", "type": "type"},
)
class OpenSearchActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        id: builtins.str,
        index: builtins.str,
        type: builtins.str,
    ) -> None:
        '''(experimental) Configuration properties of an action for Open Search.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param id: (experimental) The unique identifier for the document you are storing.
        :param index: (experimental) The OpenSearch index where you want to store your data.
        :param type: (experimental) The type of document you are storing.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_opensearchservice as opensearch
            # domain: opensearch.Domain
            
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'")
            )
            
            topic_rule.add_action(actions.OpenSearchAction(domain,
                id="my-id",
                index="my-index",
                type="my-type"
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49db1560a3ec547d00f9ceca770a6c6281883f28e417d7418f38eb83bd36f66f)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "index": index,
            "type": type,
        }
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) The unique identifier for the document you are storing.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def index(self) -> builtins.str:
        '''(experimental) The OpenSearch index where you want to store your data.

        :stability: experimental
        '''
        result = self._values.get("index")
        assert result is not None, "Required property 'index' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The type of document you are storing.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenSearchActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class S3PutObjectAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.S3PutObjectAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon S3 bucket.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        bucket = s3.Bucket(self, "MyBucket")
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.S3PutObjectAction(bucket,
                    key="${year}/${month}/${day}/${topic(2)}"
                )
            ]
        )
    '''

    def __init__(
        self,
        bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
        *,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        key: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param bucket: The Amazon S3 bucket to which to write data.
        :param access_control: (experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key. Default: None
        :param key: (experimental) The path to the file where the data is written. Supports substitution templates. Default: '${topic()}/${timestamp()}'
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bbbe8807f470409fee21688cbdca26b2d855abff863619511f33e2e6e54db53)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
        props = S3PutObjectActionProps(
            access_control=access_control, key=key, role=role
        )

        jsii.create(self.__class__, self, [bucket, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.S3PutObjectActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "access_control": "accessControl", "key": "key"},
)
class S3PutObjectActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
        key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for s3.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param access_control: (experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key. Default: None
        :param key: (experimental) The path to the file where the data is written. Supports substitution templates. Default: '${topic()}/${timestamp()}'

        :stability: experimental
        :exampleMetadata: infused

        Example::

            bucket = s3.Bucket(self, "MyBucket")
            
            iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.S3PutObjectAction(bucket,
                        key="${year}/${month}/${day}/${topic(2)}"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74be5bc61492b5d95f55ab5d587208fc038f41e2774a8ccd5f3222ed6bbe29cc)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument access_control", value=access_control, expected_type=type_hints["access_control"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if access_control is not None:
            self._values["access_control"] = access_control
        if key is not None:
            self._values["key"] = key

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def access_control(
        self,
    ) -> typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl]:
        '''(experimental) The Amazon S3 canned ACL that controls access to the object identified by the object key.

        :default: None

        :see: https://docs.aws.amazon.com/AmazonS3/latest/userguide/acl-overview.html#canned-acl
        :stability: experimental
        '''
        result = self._values.get("access_control")
        return typing.cast(typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl], result)

    @builtins.property
    def key(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the file where the data is written.

        Supports substitution templates.

        :default: '${topic()}/${timestamp()}'

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3PutObjectActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-iot-actions-alpha.SnsActionMessageFormat")
class SnsActionMessageFormat(enum.Enum):
    '''(experimental) SNS topic action message format options.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "MyTopic")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SnsTopicAction(topic,
                    message_format=actions.SnsActionMessageFormat.JSON
                )
            ]
        )
    '''

    RAW = "RAW"
    '''(experimental) RAW message format.

    :stability: experimental
    '''
    JSON = "JSON"
    '''(experimental) JSON message format.

    :stability: experimental
    '''


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class SnsTopicAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.SnsTopicAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon SNS topic.

    :see: https://docs.aws.amazon.com/iot/latest/developerguide/sns-rule-action.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sns as sns
        
        
        topic = sns.Topic(self, "MyTopic")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SnsTopicAction(topic,
                    message_format=actions.SnsActionMessageFormat.JSON
                )
            ]
        )
    '''

    def __init__(
        self,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        *,
        message_format: typing.Optional[SnsActionMessageFormat] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param topic: The Amazon SNS topic to publish data on. Must not be a FIFO topic.
        :param message_format: (experimental) The message format of the message to publish. SNS uses this setting to determine if the payload should be parsed and relevant platform-specific bits of the payload should be extracted. Default: SnsActionMessageFormat.RAW
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b9ac87541b719bdb6188fab91743d47e5baf5337b590a3c44eb0855d08373a)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        props = SnsTopicActionProps(message_format=message_format, role=role)

        jsii.create(self.__class__, self, [topic, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.SnsTopicActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "message_format": "messageFormat"},
)
class SnsTopicActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        message_format: typing.Optional[SnsActionMessageFormat] = None,
    ) -> None:
        '''(experimental) Configuration options for the SNS topic action.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param message_format: (experimental) The message format of the message to publish. SNS uses this setting to determine if the payload should be parsed and relevant platform-specific bits of the payload should be extracted. Default: SnsActionMessageFormat.RAW

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sns as sns
            
            
            topic = sns.Topic(self, "MyTopic")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.SnsTopicAction(topic,
                        message_format=actions.SnsActionMessageFormat.JSON
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4eda26cfe8f33e82924457f130b39bfe6d7f117623596e9d9ce154ce4e5108)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument message_format", value=message_format, expected_type=type_hints["message_format"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if message_format is not None:
            self._values["message_format"] = message_format

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def message_format(self) -> typing.Optional[SnsActionMessageFormat]:
        '''(experimental) The message format of the message to publish.

        SNS uses this setting to determine if the payload should be parsed and relevant platform-specific bits of the payload should be extracted.

        :default: SnsActionMessageFormat.RAW

        :see: https://docs.aws.amazon.com/sns/latest/dg/sns-message-and-json-formats.html
        :stability: experimental
        '''
        result = self._values.get("message_format")
        return typing.cast(typing.Optional[SnsActionMessageFormat], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTopicActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class SqsQueueAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.SqsQueueAction",
):
    '''(experimental) The action to write the data from an MQTT message to an Amazon SQS queue.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_sqs as sqs
        
        
        queue = sqs.Queue(self, "MyQueue")
        
        topic_rule = iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
            actions=[
                actions.SqsQueueAction(queue,
                    use_base64=True
                )
            ]
        )
    '''

    def __init__(
        self,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        *,
        use_base64: typing.Optional[builtins.bool] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param queue: The Amazon SQS queue to which to write data.
        :param use_base64: (experimental) Specifies whether to use Base64 encoding. Default: false
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d0c245d877114394d3e09acdcb174576e27f3f9cad8a863e5e7a424110d13bb)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        props = SqsQueueActionProps(use_base64=use_base64, role=role)

        jsii.create(self.__class__, self, [queue, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.SqsQueueActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "use_base64": "useBase64"},
)
class SqsQueueActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        use_base64: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for SQS.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param use_base64: (experimental) Specifies whether to use Base64 encoding. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_sqs as sqs
            
            
            queue = sqs.Queue(self, "MyQueue")
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, year, month, day FROM 'device/+/data'"),
                actions=[
                    actions.SqsQueueAction(queue,
                        use_base64=True
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5184a531fc369450e1313edec39213fa04a8fdc462b140ddad9b560aa8522ecc)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument use_base64", value=use_base64, expected_type=type_hints["use_base64"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if use_base64 is not None:
            self._values["use_base64"] = use_base64

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def use_base64(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether to use Base64 encoding.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("use_base64")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsQueueActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_iot_alpha_eb933819.IAction)
class StepFunctionsStateMachineAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-iot-actions-alpha.StepFunctionsStateMachineAction",
):
    '''(experimental) The action to put the record from an MQTT message to the Step Functions State Machine.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        state_machine = stepfunctions.StateMachine(self, "SM",
            definition_body=stepfunctions.DefinitionBody.from_chainable(stepfunctions.Wait(self, "Hello", time=stepfunctions.WaitTime.duration(Duration.seconds(10))))
        )
        
        iot.TopicRule(self, "TopicRule",
            sql=iot.IotSql.from_string_as_ver20160323("SELECT * FROM 'device/+/data'"),
            actions=[
                actions.StepFunctionsStateMachineAction(state_machine)
            ]
        )
    '''

    def __init__(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
        *,
        execution_name_prefix: typing.Optional[builtins.str] = None,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''
        :param state_machine: The Step Functions Start Machine which should be executed.
        :param execution_name_prefix: (experimental) Name of the state machine execution prefix. The name given to the state machine execution consists of this prefix followed by a UUID. Step Functions creates a unique name for each state machine execution if one is not provided. Default: : None - Step Functions creates a unique name for each state machine execution if one is not provided.
        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9380d6d32a8104c9950eb4b8f6ff7f68d3df1676feaa008cb1c42bea06d28f71)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        props = StepFunctionsStateMachineActionProps(
            execution_name_prefix=execution_name_prefix, role=role
        )

        jsii.create(self.__class__, self, [state_machine, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.StepFunctionsStateMachineActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role", "execution_name_prefix": "executionNamePrefix"},
)
class StepFunctionsStateMachineActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        execution_name_prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for the Step Functions State Machine.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param execution_name_prefix: (experimental) Name of the state machine execution prefix. The name given to the state machine execution consists of this prefix followed by a UUID. Step Functions creates a unique name for each state machine execution if one is not provided. Default: : None - Step Functions creates a unique name for each state machine execution if one is not provided.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_actions_alpha as iot_actions_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            step_functions_state_machine_action_props = iot_actions_alpha.StepFunctionsStateMachineActionProps(
                execution_name_prefix="executionNamePrefix",
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f99f17cd856c4c6aa85a9e9ea4651c1e04df5a16fcf1f0b96d0bc93128f6613)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument execution_name_prefix", value=execution_name_prefix, expected_type=type_hints["execution_name_prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role
        if execution_name_prefix is not None:
            self._values["execution_name_prefix"] = execution_name_prefix

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def execution_name_prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the state machine execution prefix.

        The name given to the state machine execution consists of this prefix followed by a UUID. Step Functions creates a unique name for each state machine execution if one is not provided.

        :default: : None - Step Functions creates a unique name for each state machine execution if one is not provided.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/stepfunctions-rule-action.html#stepfunctions-rule-action-parameters
        :stability: experimental
        '''
        result = self._values.get("execution_name_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StepFunctionsStateMachineActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CloudWatchLogsActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={"role": "role"},
)
class CloudWatchLogsActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch Logs.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_iot_actions_alpha as iot_actions_alpha
            from aws_cdk import aws_iam as iam
            
            # role: iam.Role
            
            cloud_watch_logs_action_props = iot_actions_alpha.CloudWatchLogsActionProps(
                role=role
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c62cf968ee8c708d0a13936857838acb01e16cd37283347a4eee11030644300)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchLogsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CloudWatchPutMetricActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "metric_unit": "metricUnit",
        "metric_value": "metricValue",
        "metric_timestamp": "metricTimestamp",
    },
)
class CloudWatchPutMetricActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        metric_unit: builtins.str,
        metric_value: builtins.str,
        metric_timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch metric.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param metric_name: (experimental) The CloudWatch metric name. Supports substitution templates.
        :param metric_namespace: (experimental) The CloudWatch metric namespace name. Supports substitution templates.
        :param metric_unit: (experimental) The metric unit supported by CloudWatch. Supports substitution templates.
        :param metric_value: (experimental) A string that contains the CloudWatch metric value. Supports substitution templates.
        :param metric_timestamp: (experimental) A string that contains the timestamp, expressed in seconds in Unix epoch time. Supports substitution templates. Default: - none -- Defaults to the current Unix epoch time.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id, namespace, unit, value, timestamp FROM 'device/+/data'"),
                actions=[
                    actions.CloudWatchPutMetricAction(
                        metric_name="${topic(2)}",
                        metric_namespace="${namespace}",
                        metric_unit="${unit}",
                        metric_value="${value}",
                        metric_timestamp="${timestamp}"
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b16a125b513c79322a639110dc70aa918ed56fa0cd214cf792b3ef851e59aa63)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument metric_unit", value=metric_unit, expected_type=type_hints["metric_unit"])
            check_type(argname="argument metric_value", value=metric_value, expected_type=type_hints["metric_value"])
            check_type(argname="argument metric_timestamp", value=metric_timestamp, expected_type=type_hints["metric_timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "metric_unit": metric_unit,
            "metric_value": metric_value,
        }
        if role is not None:
            self._values["role"] = role
        if metric_timestamp is not None:
            self._values["metric_timestamp"] = metric_timestamp

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''(experimental) The CloudWatch metric name.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''(experimental) The CloudWatch metric namespace name.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_unit(self) -> builtins.str:
        '''(experimental) The metric unit supported by CloudWatch.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_unit")
        assert result is not None, "Required property 'metric_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_value(self) -> builtins.str:
        '''(experimental) A string that contains the CloudWatch metric value.

        Supports substitution templates.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_value")
        assert result is not None, "Required property 'metric_value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_timestamp(self) -> typing.Optional[builtins.str]:
        '''(experimental) A string that contains the timestamp, expressed in seconds in Unix epoch time.

        Supports substitution templates.

        :default: - none -- Defaults to the current Unix epoch time.

        :see: https://docs.aws.amazon.com/iot/latest/developerguide/iot-substitution-templates.html
        :stability: experimental
        '''
        result = self._values.get("metric_timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchPutMetricActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-iot-actions-alpha.CloudWatchSetAlarmStateActionProps",
    jsii_struct_bases=[CommonActionProps],
    name_mapping={
        "role": "role",
        "alarm_state_to_set": "alarmStateToSet",
        "reason": "reason",
    },
)
class CloudWatchSetAlarmStateActionProps(CommonActionProps):
    def __init__(
        self,
        *,
        role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
        alarm_state_to_set: _aws_cdk_aws_cloudwatch_ceddda9d.AlarmState,
        reason: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Configuration properties of an action for CloudWatch alarm.

        :param role: (experimental) The IAM role that allows access to AWS service. Default: a new role will be created
        :param alarm_state_to_set: (experimental) The value of the alarm state to set.
        :param reason: (experimental) The reason for the alarm change. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_cloudwatch as cloudwatch
            
            
            metric = cloudwatch.Metric(
                namespace="MyNamespace",
                metric_name="MyMetric",
                dimensions_map={"MyDimension": "MyDimensionValue"}
            )
            alarm = cloudwatch.Alarm(self, "MyAlarm",
                metric=metric,
                threshold=100,
                evaluation_periods=3,
                datapoints_to_alarm=2
            )
            
            topic_rule = iot.TopicRule(self, "TopicRule",
                sql=iot.IotSql.from_string_as_ver20160323("SELECT topic(2) as device_id FROM 'device/+/data'"),
                actions=[
                    actions.CloudWatchSetAlarmStateAction(alarm,
                        reason="AWS Iot Rule action is triggered",
                        alarm_state_to_set=cloudwatch.AlarmState.ALARM
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4521229d0742486c73df92505118670df3e3699b0c09634f8986685d00c19833)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument alarm_state_to_set", value=alarm_state_to_set, expected_type=type_hints["alarm_state_to_set"])
            check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "alarm_state_to_set": alarm_state_to_set,
        }
        if role is not None:
            self._values["role"] = role
        if reason is not None:
            self._values["reason"] = reason

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole]:
        '''(experimental) The IAM role that allows access to AWS service.

        :default: a new role will be created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole], result)

    @builtins.property
    def alarm_state_to_set(self) -> _aws_cdk_aws_cloudwatch_ceddda9d.AlarmState:
        '''(experimental) The value of the alarm state to set.

        :stability: experimental
        '''
        result = self._values.get("alarm_state_to_set")
        assert result is not None, "Required property 'alarm_state_to_set' is missing"
        return typing.cast(_aws_cdk_aws_cloudwatch_ceddda9d.AlarmState, result)

    @builtins.property
    def reason(self) -> typing.Optional[builtins.str]:
        '''(experimental) The reason for the alarm change.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("reason")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchSetAlarmStateActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CloudWatchLogsAction",
    "CloudWatchLogsActionProps",
    "CloudWatchPutMetricAction",
    "CloudWatchPutMetricActionProps",
    "CloudWatchSetAlarmStateAction",
    "CloudWatchSetAlarmStateActionProps",
    "CommonActionProps",
    "DynamoDBv2PutItemAction",
    "DynamoDBv2PutItemActionProps",
    "FirehosePutRecordAction",
    "FirehosePutRecordActionProps",
    "FirehoseRecordSeparator",
    "HttpActionHeader",
    "HttpActionSigV4Auth",
    "HttpsAction",
    "HttpsActionProps",
    "IotEventsPutMessageAction",
    "IotEventsPutMessageActionProps",
    "IotRepublishMqttAction",
    "IotRepublishMqttActionProps",
    "KinesisPutRecordAction",
    "KinesisPutRecordActionProps",
    "LambdaFunctionAction",
    "MqttQualityOfService",
    "OpenSearchAction",
    "OpenSearchActionProps",
    "S3PutObjectAction",
    "S3PutObjectActionProps",
    "SnsActionMessageFormat",
    "SnsTopicAction",
    "SnsTopicActionProps",
    "SqsQueueAction",
    "SqsQueueActionProps",
    "StepFunctionsStateMachineAction",
    "StepFunctionsStateMachineActionProps",
]

publication.publish()

def _typecheckingstub__1125f9dca9ec8ed30503b3089fce98893e99b37a4834cfd883136ea340ad05cb(
    log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc507afa1602d7648fd445cf653eafff0694945ad00db2eb11461c754c2b00b(
    alarm: _aws_cdk_aws_cloudwatch_ceddda9d.IAlarm,
    *,
    alarm_state_to_set: _aws_cdk_aws_cloudwatch_ceddda9d.AlarmState,
    reason: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8c5f84dc199f2aa55e9c7b72978de6e47482c21c07fb8845141664e7ba4e7ce(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9242ff0039c5f5f20a1fcc4613ee02b20617db70446ef5e7cbe185ebec5fa338(
    table: _aws_cdk_aws_dynamodb_ceddda9d.ITable,
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5006dd434137a2ed9cdc6c97b24a6a3424c93db9f39d65c8aff4f62493513268(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1862de154dea8afd9a05c2e43c9e12d06dd718f02f029ad7e9defe76176f5d(
    stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
    *,
    batch_mode: typing.Optional[builtins.bool] = None,
    record_separator: typing.Optional[FirehoseRecordSeparator] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a372426adf9237fb413c0109f8f86481ab2cefcb2d867a7cd22fd0ac4160dd82(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    batch_mode: typing.Optional[builtins.bool] = None,
    record_separator: typing.Optional[FirehoseRecordSeparator] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca282425917f2fd79daa77c3313ac246d547984b2140f896e262c1ec5dbb9879(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b59e93ae19615b8937eb25644e8d247753f0996ddd5ee40af6b299f32e12bd3(
    *,
    service_name: builtins.str,
    signing_region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c87b0804f95979b48d6a924424abe8ebf192fbcfebc6aecf6436690d1019d6ad(
    url: builtins.str,
    *,
    auth: typing.Optional[typing.Union[HttpActionSigV4Auth, typing.Dict[builtins.str, typing.Any]]] = None,
    confirmation_url: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Sequence[typing.Union[HttpActionHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed57e014b0887a84984c84f8ad94782b2b5efe0e853a018ecb7cde520af055ac(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    auth: typing.Optional[typing.Union[HttpActionSigV4Auth, typing.Dict[builtins.str, typing.Any]]] = None,
    confirmation_url: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Sequence[typing.Union[HttpActionHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fd382f1f47362d144397e527978352f762c1785375ec37658992a8a487b4cf8(
    input: _aws_cdk_aws_iotevents_alpha_39cbd76e.IInput,
    *,
    batch_mode: typing.Optional[builtins.bool] = None,
    message_id: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc9e90430c80165cefadf2e647f22c5429762d648559fb693f79190265f6f91(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    batch_mode: typing.Optional[builtins.bool] = None,
    message_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39706bd98f00c288466b2a1f3248a337c500a5d9800d73998fb329410490355(
    topic: builtins.str,
    *,
    quality_of_service: typing.Optional[MqttQualityOfService] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854cc7d880adf3faaf99230c4da2141389719c911cc9ff25daf3e31267da2ba7(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    quality_of_service: typing.Optional[MqttQualityOfService] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f906af38759ce5ba22880ad819a9e8e2eebfc2b90b06b2935a18ed5516ca8c(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
    *,
    partition_key: builtins.str,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ab71684b75c91d7e19999242605bbbcf0ebeed49e9e93eb0a07ff42713e97d(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    partition_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b93d28232c9e366b4b8112099c693914bd7bf1c15baab0bdc99040cab6073a3(
    func: _aws_cdk_aws_lambda_ceddda9d.IFunction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3920392688b421d7e2aa469667b4ced037e78a50f767b308c0052982bae1ce(
    domain: _aws_cdk_aws_opensearchservice_ceddda9d.Domain,
    *,
    id: builtins.str,
    index: builtins.str,
    type: builtins.str,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49db1560a3ec547d00f9ceca770a6c6281883f28e417d7418f38eb83bd36f66f(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    id: builtins.str,
    index: builtins.str,
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bbbe8807f470409fee21688cbdca26b2d855abff863619511f33e2e6e54db53(
    bucket: _aws_cdk_aws_s3_ceddda9d.IBucket,
    *,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    key: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74be5bc61492b5d95f55ab5d587208fc038f41e2774a8ccd5f3222ed6bbe29cc(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    access_control: typing.Optional[_aws_cdk_aws_s3_ceddda9d.BucketAccessControl] = None,
    key: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b9ac87541b719bdb6188fab91743d47e5baf5337b590a3c44eb0855d08373a(
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    *,
    message_format: typing.Optional[SnsActionMessageFormat] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4eda26cfe8f33e82924457f130b39bfe6d7f117623596e9d9ce154ce4e5108(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    message_format: typing.Optional[SnsActionMessageFormat] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d0c245d877114394d3e09acdcb174576e27f3f9cad8a863e5e7a424110d13bb(
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    *,
    use_base64: typing.Optional[builtins.bool] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5184a531fc369450e1313edec39213fa04a8fdc462b140ddad9b560aa8522ecc(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    use_base64: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9380d6d32a8104c9950eb4b8f6ff7f68d3df1676feaa008cb1c42bea06d28f71(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
    *,
    execution_name_prefix: typing.Optional[builtins.str] = None,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f99f17cd856c4c6aa85a9e9ea4651c1e04df5a16fcf1f0b96d0bc93128f6613(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    execution_name_prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c62cf968ee8c708d0a13936857838acb01e16cd37283347a4eee11030644300(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b16a125b513c79322a639110dc70aa918ed56fa0cd214cf792b3ef851e59aa63(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    metric_unit: builtins.str,
    metric_value: builtins.str,
    metric_timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4521229d0742486c73df92505118670df3e3699b0c09634f8986685d00c19833(
    *,
    role: typing.Optional[_aws_cdk_aws_iam_ceddda9d.IRole] = None,
    alarm_state_to_set: _aws_cdk_aws_cloudwatch_ceddda9d.AlarmState,
    reason: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
