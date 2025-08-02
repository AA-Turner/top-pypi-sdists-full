r'''
# Amazon EventBridge Pipes Targets Construct Library

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

EventBridge Pipes Targets let you create a target for an EventBridge Pipe.

For more details see the [service documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-target.html).

## Targets

Pipe targets are the end point of an EventBridge Pipe. The following targets are supported:

* `targets.ApiDestinationTarget`: [Send event source to an EventBridge API destination](#amazon-eventbridge-api-destination)
* `targets.ApiGatewayTarget`: [Send event source to an API Gateway REST API](#amazon-api-gateway-rest-api)
* `targets.CloudWatchLogsTarget`: [Send event source to a CloudWatch Logs log group](#amazon-cloudwatch-logs-log-group)
* `targets.EventBridgeTarget`: [Send event source to an EventBridge event bus](#amazon-eventbridge-event-bus)
* `targets.FirehoseTarget`: [Send event source to an Amazon Data Firehose delivery stream](#amazon-data-firehose-delivery-stream)
* `targets.KinesisTarget`: [Send event source to a Kinesis data stream](#amazon-kinesis-data-stream)
* `targets.LambdaFunction`: [Send event source to a Lambda function](#aws-lambda-function)
* `targets.SageMakerTarget`: [Send event source to a SageMaker pipeline](#amazon-sagemaker-pipeline)
* `targets.SfnStateMachine`: [Invoke a Step Functions state machine from an event source](#aws-step-functions-state-machine)
* `targets.SnsTarget`: [Send event source to an SNS topic](#amazon-sns-topic)
* `targets.SqsTarget`: [Send event source to an SQS queue](#amazon-sqs-queue)

### Amazon EventBridge API Destination

An EventBridge API destination can be used as a target for a pipe.
The API destination will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# dest: events.ApiDestination


api_target = targets.ApiDestinationTarget(dest)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=api_target
)
```

The input to the target API destination can be transformed:

```python
# source_queue: sqs.Queue
# dest: events.ApiDestination


api_target = targets.ApiDestinationTarget(dest,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=api_target
)
```

### Amazon API Gateway Rest API

A REST API can be used as a target for a pipe.
The REST API will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue


fn = lambda_.Function(self, "MyFunc",
    handler="index.handler",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    code=lambda_.Code.from_inline("exports.handler = e => {}")
)

rest_api = api.LambdaRestApi(self, "MyRestAPI", handler=fn)
api_target = targets.ApiGatewayTarget(rest_api)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=api_target
)
```

The input to the target REST API can be transformed:

```python
# source_queue: sqs.Queue


fn = lambda_.Function(self, "MyFunc",
    handler="index.handler",
    runtime=lambda_.Runtime.NODEJS_LATEST,
    code=lambda_.Code.from_inline("exports.handler = e => {}")
)

rest_api = api.LambdaRestApi(self, "MyRestAPI", handler=fn)
api_target = targets.ApiGatewayTarget(rest_api,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=api_target
)
```

### Amazon CloudWatch Logs Log Group

A CloudWatch Logs log group can be used as a target for a pipe.
The log group will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_log_group: logs.LogGroup


log_group_target = targets.CloudWatchLogsTarget(target_log_group)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=log_group_target
)
```

The input to the target log group can be transformed:

```python
# source_queue: sqs.Queue
# target_log_group: logs.LogGroup


log_group_target = targets.CloudWatchLogsTarget(target_log_group,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=log_group_target
)
```

### Amazon EventBridge Event Bus

An EventBridge event bus can be used as a target for a pipe.
The event bus will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_event_bus: events.EventBus


event_bus_target = targets.EventBridgeTarget(target_event_bus)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=event_bus_target
)
```

The input to the target event bus can be transformed:

```python
# source_queue: sqs.Queue
# target_event_bus: events.EventBus


event_bus_target = targets.EventBridgeTarget(target_event_bus,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=event_bus_target
)
```

### Amazon Data Firehose Delivery Stream

An Amazon Data Firehose delivery stream can be used as a target for a pipe.
The delivery stream will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_delivery_stream: firehose.DeliveryStream


delivery_stream_target = targets.FirehoseTarget(target_delivery_stream)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=delivery_stream_target
)
```

The input to the target delivery stream can be transformed:

```python
# source_queue: sqs.Queue
# target_delivery_stream: firehose.DeliveryStream


delivery_stream_target = targets.FirehoseTarget(target_delivery_stream,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=delivery_stream_target
)
```

### Amazon Kinesis Data Stream

A Kinesis data stream can be used as a target for a pipe.
The data stream will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_stream: kinesis.Stream


stream_target = targets.KinesisTarget(target_stream,
    partition_key="pk"
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=stream_target
)
```

The input to the target data stream can be transformed:

```python
# source_queue: sqs.Queue
# target_stream: kinesis.Stream


stream_target = targets.KinesisTarget(target_stream,
    partition_key="pk",
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=stream_target
)
```

### AWS Lambda Function

A Lambda function can be used as a target for a pipe.
The Lambda function will be invoked with the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_function: lambda.IFunction


pipe_target = targets.LambdaFunction(target_function)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The target Lambda function is invoked synchronously by default. You can also choose to invoke the Lambda Function asynchronously by setting `invocationType` property to `FIRE_AND_FORGET`.

```python
# source_queue: sqs.Queue
# target_function: lambda.IFunction


pipe_target = targets.LambdaFunction(target_function,
    invocation_type=targets.LambdaFunctionInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The input to the target Lambda Function can be transformed:

```python
# source_queue: sqs.Queue
# target_function: lambda.IFunction


pipe_target = targets.LambdaFunction(target_function,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

### Amazon SageMaker Pipeline

A SageMaker pipeline can be used as a target for a pipe.
The pipeline will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_pipeline: sagemaker.IPipeline


pipeline_target = targets.SageMakerTarget(target_pipeline)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipeline_target
)
```

The input to the target pipeline can be transformed:

```python
# source_queue: sqs.Queue
# target_pipeline: sagemaker.IPipeline


pipeline_target = targets.SageMakerTarget(target_pipeline,
    input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipeline_target
)
```

### AWS Step Functions State Machine

A Step Functions state machine can be used as a target for a pipe.
The state machine will be invoked with the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

You can specify the invocation type when the target state machine is invoked:

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine,
    invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The input to the target state machine can be transformed:

```python
# source_queue: sqs.Queue
# target_state_machine: sfn.IStateMachine


pipe_target = targets.SfnStateMachine(target_state_machine,
    input_transformation=pipes.InputTransformation.from_object({"body": "<$.body>"}),
    invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

### Amazon SNS Topic

An SNS topic can be used as a target for a pipe.
The topic will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_topic: sns.Topic


pipe_target = targets.SnsTarget(target_topic)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The target input can be transformed:

```python
# source_queue: sqs.Queue
# target_topic: sns.Topic


pipe_target = targets.SnsTarget(target_topic,
    input_transformation=pipes.InputTransformation.from_object({
        "SomeKey": pipes.DynamicInput.from_event_path("$.body")
    })
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

### Amazon SQS Queue

An SQS queue can be used as a target for a pipe.
The queue will receive the (enriched/filtered) source payload.

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_target = targets.SqsTarget(target_queue)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
```

The target input can be transformed:

```python
# source_queue: sqs.Queue
# target_queue: sqs.Queue


pipe_target = targets.SqsTarget(target_queue,
    input_transformation=pipes.InputTransformation.from_object({
        "SomeKey": pipes.DynamicInput.from_event_path("$.body")
    })
)

pipe = pipes.Pipe(self, "Pipe",
    source=SqsSource(source_queue),
    target=pipe_target
)
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

import aws_cdk.aws_apigateway as _aws_cdk_aws_apigateway_ceddda9d
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import aws_cdk.aws_kinesis as _aws_cdk_aws_kinesis_ceddda9d
import aws_cdk.aws_kinesisfirehose as _aws_cdk_aws_kinesisfirehose_ceddda9d
import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_pipes_alpha as _aws_cdk_aws_pipes_alpha_c8863edb
import aws_cdk.aws_sagemaker as _aws_cdk_aws_sagemaker_ceddda9d
import aws_cdk.aws_sns as _aws_cdk_aws_sns_ceddda9d
import aws_cdk.aws_sqs as _aws_cdk_aws_sqs_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class ApiDestinationTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.ApiDestinationTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an EventBridge API destination.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # dest: events.ApiDestination
        
        
        api_target = targets.ApiDestinationTarget(dest)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=api_target
        )
    '''

    def __init__(
        self,
        destination: _aws_cdk_aws_events_ceddda9d.IApiDestination,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param destination: -
        :param header_parameters: (experimental) The headers to send as part of the request invoking the EventBridge API destination. The headers are merged with the headers from the API destination. If there are conflicts, the headers from the API destination take precedence. Default: - none
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param path_parameter_values: (experimental) The path parameter values used to populate the EventBridge API destination path wildcards ("*"). Default: - none
        :param query_string_parameters: (experimental) The query string keys/values that need to be sent as part of request invoking the EventBridge API destination. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b762a799798a21357cd00fa4018b3a9eda2236548bf228a1f4b9370069e45c6b)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
        parameters = ApiDestinationTargetParameters(
            header_parameters=header_parameters,
            input_transformation=input_transformation,
            path_parameter_values=path_parameter_values,
            query_string_parameters=query_string_parameters,
        )

        jsii.create(self.__class__, self, [destination, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15f5446848598b46d7e21498baa020fc7b812fc3b6eb34c784f77ebd1c7777b6)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101f6cc24d101109b7241b446d95db517c984148ec7ebe5b327a7369d9d2b36e)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.ApiDestinationTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "header_parameters": "headerParameters",
        "input_transformation": "inputTransformation",
        "path_parameter_values": "pathParameterValues",
        "query_string_parameters": "queryStringParameters",
    },
)
class ApiDestinationTargetParameters:
    def __init__(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) EventBridge API destination target properties.

        :param header_parameters: (experimental) The headers to send as part of the request invoking the EventBridge API destination. The headers are merged with the headers from the API destination. If there are conflicts, the headers from the API destination take precedence. Default: - none
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param path_parameter_values: (experimental) The path parameter values used to populate the EventBridge API destination path wildcards ("*"). Default: - none
        :param query_string_parameters: (experimental) The query string keys/values that need to be sent as part of request invoking the EventBridge API destination. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # dest: events.ApiDestination
            
            
            api_target = targets.ApiDestinationTarget(dest,
                input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=api_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__025d06f4a46f39d1a875d7c36d55d360fbf3fcbe6e5f5a5cddf35ddd9aee42ff)
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The headers to send as part of the request invoking the EventBridge API destination.

        The headers are merged with the headers from the API destination.
        If there are conflicts, the headers from the API destination take precedence.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-headerparameters
        :stability: experimental
        '''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The path parameter values used to populate the EventBridge API destination path wildcards ("*").

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-pathparametervalues
        :stability: experimental
        '''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The query string keys/values that need to be sent as part of request invoking the EventBridge API destination.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-querystringparameters
        :stability: experimental
        '''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiDestinationTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class ApiGatewayTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.ApiGatewayTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an EventBridge API destination.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        
        
        fn = lambda_.Function(self, "MyFunc",
            handler="index.handler",
            runtime=lambda_.Runtime.NODEJS_LATEST,
            code=lambda_.Code.from_inline("exports.handler = e => {}")
        )
        
        rest_api = api.LambdaRestApi(self, "MyRestAPI", handler=fn)
        api_target = targets.ApiGatewayTarget(rest_api)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=api_target
        )
    '''

    def __init__(
        self,
        rest_api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param rest_api: -
        :param header_parameters: (experimental) The headers to send as part of the request invoking the API Gateway REST API. Default: - none
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param method: (experimental) The method for API Gateway resource. Default: '*' - ANY
        :param path: (experimental) The path for the API Gateway resource. Default: '/'
        :param path_parameter_values: (experimental) The path parameter values used to populate the API Gateway REST API path wildcards ("*"). Default: - none
        :param query_string_parameters: (experimental) The query string keys/values that need to be sent as part of request invoking the API Gateway REST API. Default: - none
        :param stage: (experimental) The deployment stage for the API Gateway resource. Default: - the value of ``deploymentStage.stageName`` of target API Gateway resource.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e15ad0f139d014a109dd5303fc9486878c1b400e7e513ccb9a8a87125d75ac1)
            check_type(argname="argument rest_api", value=rest_api, expected_type=type_hints["rest_api"])
        parameters = ApiGatewayTargetParameters(
            header_parameters=header_parameters,
            input_transformation=input_transformation,
            method=method,
            path=path,
            path_parameter_values=path_parameter_values,
            query_string_parameters=query_string_parameters,
            stage=stage,
        )

        jsii.create(self.__class__, self, [rest_api, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8698d7a7df07c396878d1d2a9ff9924e96dee971f345f91bc9112379d5dbb7aa)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d057bbc43d070545a1e9ca80243840a882047958d27438c491a4c575c18a8d4)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.ApiGatewayTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "header_parameters": "headerParameters",
        "input_transformation": "inputTransformation",
        "method": "method",
        "path": "path",
        "path_parameter_values": "pathParameterValues",
        "query_string_parameters": "queryStringParameters",
        "stage": "stage",
    },
)
class ApiGatewayTargetParameters:
    def __init__(
        self,
        *,
        header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        method: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) API Gateway REST API target properties.

        :param header_parameters: (experimental) The headers to send as part of the request invoking the API Gateway REST API. Default: - none
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param method: (experimental) The method for API Gateway resource. Default: '*' - ANY
        :param path: (experimental) The path for the API Gateway resource. Default: '/'
        :param path_parameter_values: (experimental) The path parameter values used to populate the API Gateway REST API path wildcards ("*"). Default: - none
        :param query_string_parameters: (experimental) The query string keys/values that need to be sent as part of request invoking the API Gateway REST API. Default: - none
        :param stage: (experimental) The deployment stage for the API Gateway resource. Default: - the value of ``deploymentStage.stageName`` of target API Gateway resource.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            
            
            fn = lambda_.Function(self, "MyFunc",
                handler="index.handler",
                runtime=lambda_.Runtime.NODEJS_LATEST,
                code=lambda_.Code.from_inline("exports.handler = e => {}")
            )
            
            rest_api = api.LambdaRestApi(self, "MyRestAPI", handler=fn)
            api_target = targets.ApiGatewayTarget(rest_api,
                input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=api_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f9a7c8ea55fad77ccaaf83d42f65dd257c76fd5a3462b9cf41d7db2ba011f36)
            check_type(argname="argument header_parameters", value=header_parameters, expected_type=type_hints["header_parameters"])
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument path_parameter_values", value=path_parameter_values, expected_type=type_hints["path_parameter_values"])
            check_type(argname="argument query_string_parameters", value=query_string_parameters, expected_type=type_hints["query_string_parameters"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if header_parameters is not None:
            self._values["header_parameters"] = header_parameters
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if method is not None:
            self._values["method"] = method
        if path is not None:
            self._values["path"] = path
        if path_parameter_values is not None:
            self._values["path_parameter_values"] = path_parameter_values
        if query_string_parameters is not None:
            self._values["query_string_parameters"] = query_string_parameters
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def header_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The headers to send as part of the request invoking the API Gateway REST API.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-headerparameters
        :stability: experimental
        '''
        result = self._values.get("header_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def method(self) -> typing.Optional[builtins.str]:
        '''(experimental) The method for API Gateway resource.

        :default: '*' - ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path for the API Gateway resource.

        :default: '/'

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_parameter_values(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) The path parameter values used to populate the API Gateway REST API path wildcards ("*").

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-pathparametervalues
        :stability: experimental
        '''
        result = self._values.get("path_parameter_values")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def query_string_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) The query string keys/values that need to be sent as part of request invoking the API Gateway REST API.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargethttpparameters.html#cfn-pipes-pipe-pipetargethttpparameters-querystringparameters
        :stability: experimental
        '''
        result = self._values.get("query_string_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) The deployment stage for the API Gateway resource.

        :default: - the value of ``deploymentStage.stageName`` of target API Gateway resource.

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ApiGatewayTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class CloudWatchLogsTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.CloudWatchLogsTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to a CloudWatch Logs log group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_log_group: logs.LogGroup
        
        
        log_group_target = targets.CloudWatchLogsTarget(target_log_group)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=log_group_target
        )
    '''

    def __init__(
        self,
        log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param log_group: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param log_stream_name: (experimental) The name of the log stream. Default: - none
        :param timestamp: (experimental) The JSON path expression that references the timestamp in the payload. This is the time that the event occurred, as a JSON path expression in the payload. Default: - current time

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87a3c707060f0994026c179958d6d3540eaf4e8eb92f11ed0ae53479ff77747b)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
        parameters = CloudWatchLogsTargetParameters(
            input_transformation=input_transformation,
            log_stream_name=log_stream_name,
            timestamp=timestamp,
        )

        jsii.create(self.__class__, self, [log_group, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b4caba4536d2bc50043ac07604f33ea5052a0bf994892eb1259721cee5cc88)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e95f72b2e204de96800ebe704ae1ab435fb192f3a3094b41b708d1c85cbd73c)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.CloudWatchLogsTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "log_stream_name": "logStreamName",
        "timestamp": "timestamp",
    },
)
class CloudWatchLogsTargetParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        log_stream_name: typing.Optional[builtins.str] = None,
        timestamp: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) CloudWatch Logs target properties.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param log_stream_name: (experimental) The name of the log stream. Default: - none
        :param timestamp: (experimental) The JSON path expression that references the timestamp in the payload. This is the time that the event occurred, as a JSON path expression in the payload. Default: - current time

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_log_group: logs.LogGroup
            
            
            log_group_target = targets.CloudWatchLogsTarget(target_log_group,
                input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=log_group_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aea8c7328974fda0eeaeea6dfa20e4d97ba032e991fff491214b3ee3227fe56)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument log_stream_name", value=log_stream_name, expected_type=type_hints["log_stream_name"])
            check_type(argname="argument timestamp", value=timestamp, expected_type=type_hints["timestamp"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if log_stream_name is not None:
            self._values["log_stream_name"] = log_stream_name
        if timestamp is not None:
            self._values["timestamp"] = timestamp

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def log_stream_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the log stream.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetcloudwatchlogsparameters.html#cfn-pipes-pipe-pipetargetcloudwatchlogsparameters-logstreamname
        :stability: experimental
        '''
        result = self._values.get("log_stream_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timestamp(self) -> typing.Optional[builtins.str]:
        '''(experimental) The JSON path expression that references the timestamp in the payload.

        This is the time that the event occurred, as a JSON path expression in the payload.

        :default: - current time

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetcloudwatchlogsparameters.html#cfn-pipes-pipe-pipetargetcloudwatchlogsparameters-timestamp
        :stability: experimental

        Example::

            "$.data.timestamp"
        '''
        result = self._values.get("timestamp")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudWatchLogsTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class EventBridgeTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.EventBridgeTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an EventBridge event bus.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_event_bus: events.EventBus
        
        
        event_bus_target = targets.EventBridgeTarget(target_event_bus)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=event_bus_target
        )
    '''

    def __init__(
        self,
        event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
        *,
        detail_type: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param event_bus: -
        :param detail_type: (experimental) A free-form string used to decide what fields to expect in the event detail. Default: - none
        :param endpoint_id: (experimental) The URL subdomain of the endpoint. Default: - none
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param resources: (experimental) AWS resources, identified by Amazon Resource Name (ARN), which the event primarily concerns. Default: - none
        :param source: (experimental) The source of the event. Default: - none
        :param time: (experimental) The time stamp of the event, per RFC3339. Default: - the time stamp of the PutEvents call

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd5f2a302ff14aafe9a91c3941961788945c017f8a53ffc33bfc933dae449d7)
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
        parameters = EventBridgeTargetParameters(
            detail_type=detail_type,
            endpoint_id=endpoint_id,
            input_transformation=input_transformation,
            resources=resources,
            source=source,
            time=time,
        )

        jsii.create(self.__class__, self, [event_bus, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dc5381dbb58a999484f6e3518b5a6c8b829a5ce17294291f3ff550b697c75b6)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dac08d41b90eaf1bdeafc4d21d3d75c155bd699032fc8fa3ed8dbce70fbda8a)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.EventBridgeTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "detail_type": "detailType",
        "endpoint_id": "endpointId",
        "input_transformation": "inputTransformation",
        "resources": "resources",
        "source": "source",
        "time": "time",
    },
)
class EventBridgeTargetParameters:
    def __init__(
        self,
        *,
        detail_type: typing.Optional[builtins.str] = None,
        endpoint_id: typing.Optional[builtins.str] = None,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        source: typing.Optional[builtins.str] = None,
        time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) EventBridge target properties.

        :param detail_type: (experimental) A free-form string used to decide what fields to expect in the event detail. Default: - none
        :param endpoint_id: (experimental) The URL subdomain of the endpoint. Default: - none
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param resources: (experimental) AWS resources, identified by Amazon Resource Name (ARN), which the event primarily concerns. Default: - none
        :param source: (experimental) The source of the event. Default: - none
        :param time: (experimental) The time stamp of the event, per RFC3339. Default: - the time stamp of the PutEvents call

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_event_bus: events.EventBus
            
            
            event_bus_target = targets.EventBridgeTarget(target_event_bus,
                input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=event_bus_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c652c7e230ac3a39a9e6d126b21c25028f102e9114aa095161f6579b1e1509c9)
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument endpoint_id", value=endpoint_id, expected_type=type_hints["endpoint_id"])
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument time", value=time, expected_type=type_hints["time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if detail_type is not None:
            self._values["detail_type"] = detail_type
        if endpoint_id is not None:
            self._values["endpoint_id"] = endpoint_id
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if resources is not None:
            self._values["resources"] = resources
        if source is not None:
            self._values["source"] = source
        if time is not None:
            self._values["time"] = time

    @builtins.property
    def detail_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) A free-form string used to decide what fields to expect in the event detail.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-detailtype
        :stability: experimental
        '''
        result = self._values.get("detail_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The URL subdomain of the endpoint.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-endpointid
        :stability: experimental

        Example::

            # if the URL for the endpoint is https://abcde.veo.endpoints.event.amazonaws.com
            "abcde.veo"
        '''
        result = self._values.get("endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) AWS resources, identified by Amazon Resource Name (ARN), which the event primarily concerns.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-resources
        :stability: experimental
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''(experimental) The source of the event.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-source
        :stability: experimental
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def time(self) -> typing.Optional[builtins.str]:
        '''(experimental) The time stamp of the event, per RFC3339.

        :default: - the time stamp of the PutEvents call

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargeteventbridgeeventbusparameters.html#cfn-pipes-pipe-pipetargeteventbridgeeventbusparameters-time
        :stability: experimental
        '''
        result = self._values.get("time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventBridgeTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class FirehoseTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.FirehoseTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an Amazon Data Firehose delivery stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_delivery_stream: firehose.DeliveryStream
        
        
        delivery_stream_target = targets.FirehoseTarget(target_delivery_stream)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=delivery_stream_target
        )
    '''

    def __init__(
        self,
        delivery_stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    ) -> None:
        '''
        :param delivery_stream: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa24f4b8557f8e86e50f9d6d3622e3a5443d18a3dc3401a894f3e876ff1b7c9f)
            check_type(argname="argument delivery_stream", value=delivery_stream, expected_type=type_hints["delivery_stream"])
        parameters = FirehoseTargetParameters(
            input_transformation=input_transformation
        )

        jsii.create(self.__class__, self, [delivery_stream, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f40327fdd62e04438f1e3800c7d44de31a697b4b2fbec3a8195c928274bf2917)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60a83144ef51dd271df97917aaed2f6641b3b71f831e4c6429ccefd715c10acb)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.FirehoseTargetParameters",
    jsii_struct_bases=[],
    name_mapping={"input_transformation": "inputTransformation"},
)
class FirehoseTargetParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    ) -> None:
        '''(experimental) Amazon Data Firehose target properties.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_delivery_stream: firehose.DeliveryStream
            
            
            delivery_stream_target = targets.FirehoseTarget(target_delivery_stream,
                input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=delivery_stream_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__808904b90abd427fd2ee4a2ae827ce219dcd227f3caffac02492da40b33a3335)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirehoseTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class KinesisTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.KinesisTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to a Kinesis stream.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_stream: kinesis.Stream
        
        
        stream_target = targets.KinesisTarget(target_stream,
            partition_key="pk"
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=stream_target
        )
    '''

    def __init__(
        self,
        stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
        *,
        partition_key: builtins.str,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    ) -> None:
        '''
        :param stream: -
        :param partition_key: (experimental) Determines which shard in the stream the data record is assigned to.
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc59e982d2759c2ef126036110222e8013eeaccd5486d5c9c26bfe2c6621f71)
            check_type(argname="argument stream", value=stream, expected_type=type_hints["stream"])
        parameters = KinesisTargetParameters(
            partition_key=partition_key, input_transformation=input_transformation
        )

        jsii.create(self.__class__, self, [stream, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f970f3f72e49fc32284793ca07446060d2bc3c07ab5801e6a4885713c0a5043e)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662f8b99c351403129740758e207d639e2b87ff9d20585038a15d1a0beae4602)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.KinesisTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "partition_key": "partitionKey",
        "input_transformation": "inputTransformation",
    },
)
class KinesisTargetParameters:
    def __init__(
        self,
        *,
        partition_key: builtins.str,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    ) -> None:
        '''(experimental) Kinesis target properties.

        :param partition_key: (experimental) Determines which shard in the stream the data record is assigned to.
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_stream: kinesis.Stream
            
            
            stream_target = targets.KinesisTarget(target_stream,
                partition_key="pk"
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=stream_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d55b779022ed12b76a2a96f74564b9809b79ff8db3a5d80b82d2da75c909bc)
            check_type(argname="argument partition_key", value=partition_key, expected_type=type_hints["partition_key"])
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "partition_key": partition_key,
        }
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation

    @builtins.property
    def partition_key(self) -> builtins.str:
        '''(experimental) Determines which shard in the stream the data record is assigned to.

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetkinesisstreamparameters.html#cfn-pipes-pipe-pipetargetkinesisstreamparameters-partitionkey
        :stability: experimental
        '''
        result = self._values.get("partition_key")
        assert result is not None, "Required property 'partition_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KinesisTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class LambdaFunction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.LambdaFunction",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an AWS Lambda Function.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_function: lambda.IFunction
        
        
        pipe_target = targets.LambdaFunction(target_function,
            invocation_type=targets.LambdaFunctionInvocationType.FIRE_AND_FORGET
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=pipe_target
        )
    '''

    def __init__(
        self,
        lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        invocation_type: typing.Optional["LambdaFunctionInvocationType"] = None,
    ) -> None:
        '''
        :param lambda_function: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param invocation_type: (experimental) Specify whether to invoke the Lambda Function synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``). Default: LambdaFunctionInvocationType.REQUEST_RESPONSE

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a1971a86e36fda789596b1889d34f05a24d0af56485d6cc7775e421413e983)
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
        parameters = LambdaFunctionParameters(
            input_transformation=input_transformation, invocation_type=invocation_type
        )

        jsii.create(self.__class__, self, [lambda_function, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49c0c4e08bfa085b6c624f462b4aecf9de9070373a5ed3c8b452f887696f57b)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f1112c70cbeaab5de073103054ca171246994bd2ca3bf7e900fd053ef704ec)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-targets-alpha.LambdaFunctionInvocationType")
class LambdaFunctionInvocationType(enum.Enum):
    '''(experimental) InvocationType for invoking the Lambda Function.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetlambdafunctionparameters.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_function: lambda.IFunction
        
        
        pipe_target = targets.LambdaFunction(target_function,
            invocation_type=targets.LambdaFunctionInvocationType.FIRE_AND_FORGET
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=pipe_target
        )
    '''

    FIRE_AND_FORGET = "FIRE_AND_FORGET"
    '''(experimental) Invoke Lambda Function asynchronously (``Invoke``).

    ``InvocationType`` is set to ``Event`` on ``Invoke``, see https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html for more details.

    :stability: experimental
    '''
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''(experimental) Invoke Lambda Function synchronously (``Invoke``) and wait for the response.

    ``InvocationType`` is set to ``RequestResponse`` on ``Invoke``, see https://docs.aws.amazon.com/lambda/latest/api/API_Invoke.html for more details.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.LambdaFunctionParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "invocation_type": "invocationType",
    },
)
class LambdaFunctionParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        invocation_type: typing.Optional[LambdaFunctionInvocationType] = None,
    ) -> None:
        '''(experimental) Parameters for the LambdaFunction target.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param invocation_type: (experimental) Specify whether to invoke the Lambda Function synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``). Default: LambdaFunctionInvocationType.REQUEST_RESPONSE

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_function: lambda.IFunction
            
            
            pipe_target = targets.LambdaFunction(target_function,
                invocation_type=targets.LambdaFunctionInvocationType.FIRE_AND_FORGET
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=pipe_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efcb2dd78b06a69bdda91afa7262bba2f022e161d9bf26afc4973df9144e37c7)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[LambdaFunctionInvocationType]:
        '''(experimental) Specify whether to invoke the Lambda Function synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``).

        :default: LambdaFunctionInvocationType.REQUEST_RESPONSE

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetlambdafunctionparameters.html
        :stability: experimental
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[LambdaFunctionInvocationType], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaFunctionParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class SageMakerTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SageMakerTarget",
):
    '''(experimental) An EventBridge Pipes target that sends messages to a SageMaker pipeline.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_pipeline: sagemaker.IPipeline
        
        
        pipeline_target = targets.SageMakerTarget(target_pipeline)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=pipeline_target
        )
    '''

    def __init__(
        self,
        pipeline: _aws_cdk_aws_sagemaker_ceddda9d.IPipeline,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        pipeline_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param pipeline: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param pipeline_parameters: (experimental) List of parameter names and values for SageMaker Model Building Pipeline execution. The Name/Value pairs are passed to start execution of the pipeline. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9068e8d19ad384aa4fc6aaf64838b1a381ca58f34585b0881b32a9ae79894c0)
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
        parameters = SageMakerTargetParameters(
            input_transformation=input_transformation,
            pipeline_parameters=pipeline_parameters,
        )

        jsii.create(self.__class__, self, [pipeline, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2968c1c90580be034d611bd8a34535f92b850b769666bf0ce93892ea303d400e)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3306656fda7e928c663624e9e2d182a987712fc583b171738e0da0389de5a5cf)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SageMakerTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "pipeline_parameters": "pipelineParameters",
    },
)
class SageMakerTargetParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        pipeline_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) SageMaker target properties.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param pipeline_parameters: (experimental) List of parameter names and values for SageMaker Model Building Pipeline execution. The Name/Value pairs are passed to start execution of the pipeline. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_pipeline: sagemaker.IPipeline
            
            
            pipeline_target = targets.SageMakerTarget(target_pipeline,
                input_transformation=pipes.InputTransformation.from_object({"body": "👀"})
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=pipeline_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb2a7266259eb430fec90c0702673cf9cc26d488b7367fc21667063652448cd)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument pipeline_parameters", value=pipeline_parameters, expected_type=type_hints["pipeline_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if pipeline_parameters is not None:
            self._values["pipeline_parameters"] = pipeline_parameters

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def pipeline_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) List of parameter names and values for SageMaker Model Building Pipeline execution.

        The Name/Value pairs are passed to start execution of the pipeline.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsagemakerpipelineparameters.html#cfn-pipes-pipe-pipetargetsagemakerpipelineparameters-pipelineparameterlist
        :stability: experimental
        '''
        result = self._values.get("pipeline_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SageMakerTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class SfnStateMachine(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SfnStateMachine",
):
    '''(experimental) An EventBridge Pipes target that sends messages to an AWS Step Functions State Machine.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_state_machine: sfn.IStateMachine
        
        
        pipe_target = targets.SfnStateMachine(target_state_machine,
            invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=pipe_target
        )
    '''

    def __init__(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        invocation_type: typing.Optional["StateMachineInvocationType"] = None,
    ) -> None:
        '''
        :param state_machine: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param invocation_type: (experimental) Specify whether to invoke the State Machine synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``). Default: StateMachineInvocationType.FIRE_AND_FORGET

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cddabb332e0b60ec3973a3c36973508988408ffb44951b1b8dcc16215177367)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        parameters = SfnStateMachineParameters(
            input_transformation=input_transformation, invocation_type=invocation_type
        )

        jsii.create(self.__class__, self, [state_machine, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169a0f99db474ac2020c24c5f65dbcabf638d6c90b8d5dfee693056ea77477bd)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__861f71f9df52dbc34295d2606d532fa6d6f532e4a0b5feb1abca7e6c4c4ad3ab)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SfnStateMachineParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "invocation_type": "invocationType",
    },
)
class SfnStateMachineParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        invocation_type: typing.Optional["StateMachineInvocationType"] = None,
    ) -> None:
        '''(experimental) Parameters for the SfnStateMachine target.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param invocation_type: (experimental) Specify whether to invoke the State Machine synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``). Default: StateMachineInvocationType.FIRE_AND_FORGET

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_state_machine: sfn.IStateMachine
            
            
            pipe_target = targets.SfnStateMachine(target_state_machine,
                invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=pipe_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6897ef83f36ecfa9f0d5ac9e3856ed5d5408bb83b1937fe3cc5067697aa9126e)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def invocation_type(self) -> typing.Optional["StateMachineInvocationType"]:
        '''(experimental) Specify whether to invoke the State Machine synchronously (``REQUEST_RESPONSE``) or asynchronously (``FIRE_AND_FORGET``).

        :default: StateMachineInvocationType.FIRE_AND_FORGET

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagededuplicationid
        :stability: experimental
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional["StateMachineInvocationType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SfnStateMachineParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class SnsTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SnsTarget",
):
    '''(experimental) A EventBridge Pipes target that sends messages to an SNS topic.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_topic: sns.Topic
        
        
        pipe_target = targets.SnsTarget(target_topic)
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=pipe_target
        )
    '''

    def __init__(
        self,
        topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    ) -> None:
        '''
        :param topic: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dff8e8e5e6c94ac7dbe028e57bd14d8d684357b91a4076f91f77774b481be32c)
            check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
        parameters = SnsTargetParameters(input_transformation=input_transformation)

        jsii.create(self.__class__, self, [topic, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575ebc1e181b2c498bb9014e996cbb4c2e00c045ef61695c446ebc2f9c0997de)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba285ccb659836012dc2efe7a33ad7d63bcf01d46f2af06697f3500102235bc)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SnsTargetParameters",
    jsii_struct_bases=[],
    name_mapping={"input_transformation": "inputTransformation"},
)
class SnsTargetParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    ) -> None:
        '''(experimental) SNS target properties.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_topic: sns.Topic
            
            
            pipe_target = targets.SnsTarget(target_topic,
                input_transformation=pipes.InputTransformation.from_object({
                    "SomeKey": pipes.DynamicInput.from_event_path("$.body")
                })
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=pipe_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__088dd6196b4ebb18c1863de168ca261178b1203a3b528e4a37d4e3abec68ef52)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SnsTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_aws_pipes_alpha_c8863edb.ITarget)
class SqsTarget(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SqsTarget",
):
    '''(experimental) A EventBridge Pipes target that sends messages to an SQS queue.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_queue: sqs.Queue
        
        
        pipe_source = sources.SqsSource(source_queue,
            batch_size=10,
            maximum_batching_window=cdk.Duration.seconds(10)
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=pipe_source,
            target=SqsTarget(target_queue)
        )
    '''

    def __init__(
        self,
        queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param queue: -
        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param message_deduplication_id: (experimental) This parameter applies only to FIFO (first-in-first-out) queues. The token used for deduplication of sent messages. Default: - none
        :param message_group_id: (experimental) The FIFO message group ID to use as the target. Default: - none

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa7b503b3079d9e51045b3114396a73fc627aec339028fa488ab019eb604fff9)
            check_type(argname="argument queue", value=queue, expected_type=type_hints["queue"])
        parameters = SqsTargetParameters(
            input_transformation=input_transformation,
            message_deduplication_id=message_deduplication_id,
            message_group_id=message_group_id,
        )

        jsii.create(self.__class__, self, [queue, parameters])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
    ) -> _aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig:
        '''(experimental) Bind this target to a pipe.

        :param pipe: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5b7cde197ff34e185db774e7f6e4e787c10c737410018f2eae647c30c381734)
            check_type(argname="argument pipe", value=pipe, expected_type=type_hints["pipe"])
        return typing.cast(_aws_cdk_aws_pipes_alpha_c8863edb.TargetConfig, jsii.invoke(self, "bind", [pipe]))

    @jsii.member(jsii_name="grantPush")
    def grant_push(self, grantee: _aws_cdk_aws_iam_ceddda9d.IRole) -> None:
        '''(experimental) Grant the pipe role to push to the target.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bf7e2c97f60032a9e2b4a8926850651a42c588ee6eb5c9d5927f02ad257089f)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(None, jsii.invoke(self, "grantPush", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''(experimental) The ARN of the target resource.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-pipes-targets-alpha.SqsTargetParameters",
    jsii_struct_bases=[],
    name_mapping={
        "input_transformation": "inputTransformation",
        "message_deduplication_id": "messageDeduplicationId",
        "message_group_id": "messageGroupId",
    },
)
class SqsTargetParameters:
    def __init__(
        self,
        *,
        input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
        message_deduplication_id: typing.Optional[builtins.str] = None,
        message_group_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) SQS target properties.

        :param input_transformation: (experimental) The input transformation to apply to the message before sending it to the target. Default: - none
        :param message_deduplication_id: (experimental) This parameter applies only to FIFO (first-in-first-out) queues. The token used for deduplication of sent messages. Default: - none
        :param message_group_id: (experimental) The FIFO message group ID to use as the target. Default: - none

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # source_queue: sqs.Queue
            # target_queue: sqs.Queue
            
            
            pipe_target = targets.SqsTarget(target_queue,
                input_transformation=pipes.InputTransformation.from_object({
                    "SomeKey": pipes.DynamicInput.from_event_path("$.body")
                })
            )
            
            pipe = pipes.Pipe(self, "Pipe",
                source=SqsSource(source_queue),
                target=pipe_target
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860ddbc258740cac07f5dbaa48920ad737f4e849a942863e0e92606f15d6ec0f)
            check_type(argname="argument input_transformation", value=input_transformation, expected_type=type_hints["input_transformation"])
            check_type(argname="argument message_deduplication_id", value=message_deduplication_id, expected_type=type_hints["message_deduplication_id"])
            check_type(argname="argument message_group_id", value=message_group_id, expected_type=type_hints["message_group_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if input_transformation is not None:
            self._values["input_transformation"] = input_transformation
        if message_deduplication_id is not None:
            self._values["message_deduplication_id"] = message_deduplication_id
        if message_group_id is not None:
            self._values["message_group_id"] = message_group_id

    @builtins.property
    def input_transformation(
        self,
    ) -> typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation]:
        '''(experimental) The input transformation to apply to the message before sending it to the target.

        :default: - none

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetparameters.html#cfn-pipes-pipe-pipetargetparameters-inputtemplate
        :stability: experimental
        '''
        result = self._values.get("input_transformation")
        return typing.cast(typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation], result)

    @builtins.property
    def message_deduplication_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) This parameter applies only to FIFO (first-in-first-out) queues.

        The token used for deduplication of sent messages.

        :default: - none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagededuplicationid
        :stability: experimental
        '''
        result = self._values.get("message_deduplication_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def message_group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The FIFO message group ID to use as the target.

        :default: - none

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-pipes-pipe-pipetargetsqsqueueparameters.html#cfn-pipes-pipe-pipetargetsqsqueueparameters-messagegroupid
        :stability: experimental
        '''
        result = self._values.get("message_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqsTargetParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-pipes-targets-alpha.StateMachineInvocationType")
class StateMachineInvocationType(enum.Enum):
    '''(experimental) InvocationType for invoking the State Machine.

    :see: https://docs.aws.amazon.com/eventbridge/latest/pipes-reference/API_PipeTargetStateMachineParameters.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # source_queue: sqs.Queue
        # target_state_machine: sfn.IStateMachine
        
        
        pipe_target = targets.SfnStateMachine(target_state_machine,
            invocation_type=targets.StateMachineInvocationType.FIRE_AND_FORGET
        )
        
        pipe = pipes.Pipe(self, "Pipe",
            source=SqsSource(source_queue),
            target=pipe_target
        )
    '''

    FIRE_AND_FORGET = "FIRE_AND_FORGET"
    '''(experimental) Invoke StepFunction asynchronously (``StartExecution``).

    See https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartExecution.html for more details.

    :stability: experimental
    '''
    REQUEST_RESPONSE = "REQUEST_RESPONSE"
    '''(experimental) Invoke StepFunction synchronously (``StartSyncExecution``) and wait for the execution to complete.

    See https://docs.aws.amazon.com/step-functions/latest/apireference/API_StartSyncExecution.html for more details.

    :stability: experimental
    '''


__all__ = [
    "ApiDestinationTarget",
    "ApiDestinationTargetParameters",
    "ApiGatewayTarget",
    "ApiGatewayTargetParameters",
    "CloudWatchLogsTarget",
    "CloudWatchLogsTargetParameters",
    "EventBridgeTarget",
    "EventBridgeTargetParameters",
    "FirehoseTarget",
    "FirehoseTargetParameters",
    "KinesisTarget",
    "KinesisTargetParameters",
    "LambdaFunction",
    "LambdaFunctionInvocationType",
    "LambdaFunctionParameters",
    "SageMakerTarget",
    "SageMakerTargetParameters",
    "SfnStateMachine",
    "SfnStateMachineParameters",
    "SnsTarget",
    "SnsTargetParameters",
    "SqsTarget",
    "SqsTargetParameters",
    "StateMachineInvocationType",
]

publication.publish()

def _typecheckingstub__b762a799798a21357cd00fa4018b3a9eda2236548bf228a1f4b9370069e45c6b(
    destination: _aws_cdk_aws_events_ceddda9d.IApiDestination,
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15f5446848598b46d7e21498baa020fc7b812fc3b6eb34c784f77ebd1c7777b6(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101f6cc24d101109b7241b446d95db517c984148ec7ebe5b327a7369d9d2b36e(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__025d06f4a46f39d1a875d7c36d55d360fbf3fcbe6e5f5a5cddf35ddd9aee42ff(
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e15ad0f139d014a109dd5303fc9486878c1b400e7e513ccb9a8a87125d75ac1(
    rest_api: _aws_cdk_aws_apigateway_ceddda9d.IRestApi,
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8698d7a7df07c396878d1d2a9ff9924e96dee971f345f91bc9112379d5dbb7aa(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d057bbc43d070545a1e9ca80243840a882047958d27438c491a4c575c18a8d4(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9a7c8ea55fad77ccaaf83d42f65dd257c76fd5a3462b9cf41d7db2ba011f36(
    *,
    header_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    method: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    path_parameter_values: typing.Optional[typing.Sequence[builtins.str]] = None,
    query_string_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87a3c707060f0994026c179958d6d3540eaf4e8eb92f11ed0ae53479ff77747b(
    log_group: _aws_cdk_aws_logs_ceddda9d.ILogGroup,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b4caba4536d2bc50043ac07604f33ea5052a0bf994892eb1259721cee5cc88(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e95f72b2e204de96800ebe704ae1ab435fb192f3a3094b41b708d1c85cbd73c(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7aea8c7328974fda0eeaeea6dfa20e4d97ba032e991fff491214b3ee3227fe56(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    log_stream_name: typing.Optional[builtins.str] = None,
    timestamp: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd5f2a302ff14aafe9a91c3941961788945c017f8a53ffc33bfc933dae449d7(
    event_bus: _aws_cdk_aws_events_ceddda9d.IEventBus,
    *,
    detail_type: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dc5381dbb58a999484f6e3518b5a6c8b829a5ce17294291f3ff550b697c75b6(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dac08d41b90eaf1bdeafc4d21d3d75c155bd699032fc8fa3ed8dbce70fbda8a(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c652c7e230ac3a39a9e6d126b21c25028f102e9114aa095161f6579b1e1509c9(
    *,
    detail_type: typing.Optional[builtins.str] = None,
    endpoint_id: typing.Optional[builtins.str] = None,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    source: typing.Optional[builtins.str] = None,
    time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa24f4b8557f8e86e50f9d6d3622e3a5443d18a3dc3401a894f3e876ff1b7c9f(
    delivery_stream: _aws_cdk_aws_kinesisfirehose_ceddda9d.IDeliveryStream,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f40327fdd62e04438f1e3800c7d44de31a697b4b2fbec3a8195c928274bf2917(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60a83144ef51dd271df97917aaed2f6641b3b71f831e4c6429ccefd715c10acb(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__808904b90abd427fd2ee4a2ae827ce219dcd227f3caffac02492da40b33a3335(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc59e982d2759c2ef126036110222e8013eeaccd5486d5c9c26bfe2c6621f71(
    stream: _aws_cdk_aws_kinesis_ceddda9d.IStream,
    *,
    partition_key: builtins.str,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f970f3f72e49fc32284793ca07446060d2bc3c07ab5801e6a4885713c0a5043e(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662f8b99c351403129740758e207d639e2b87ff9d20585038a15d1a0beae4602(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d55b779022ed12b76a2a96f74564b9809b79ff8db3a5d80b82d2da75c909bc(
    *,
    partition_key: builtins.str,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a1971a86e36fda789596b1889d34f05a24d0af56485d6cc7775e421413e983(
    lambda_function: _aws_cdk_aws_lambda_ceddda9d.IFunction,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    invocation_type: typing.Optional[LambdaFunctionInvocationType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49c0c4e08bfa085b6c624f462b4aecf9de9070373a5ed3c8b452f887696f57b(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f1112c70cbeaab5de073103054ca171246994bd2ca3bf7e900fd053ef704ec(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efcb2dd78b06a69bdda91afa7262bba2f022e161d9bf26afc4973df9144e37c7(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    invocation_type: typing.Optional[LambdaFunctionInvocationType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9068e8d19ad384aa4fc6aaf64838b1a381ca58f34585b0881b32a9ae79894c0(
    pipeline: _aws_cdk_aws_sagemaker_ceddda9d.IPipeline,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    pipeline_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2968c1c90580be034d611bd8a34535f92b850b769666bf0ce93892ea303d400e(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3306656fda7e928c663624e9e2d182a987712fc583b171738e0da0389de5a5cf(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb2a7266259eb430fec90c0702673cf9cc26d488b7367fc21667063652448cd(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    pipeline_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cddabb332e0b60ec3973a3c36973508988408ffb44951b1b8dcc16215177367(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    invocation_type: typing.Optional[StateMachineInvocationType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169a0f99db474ac2020c24c5f65dbcabf638d6c90b8d5dfee693056ea77477bd(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__861f71f9df52dbc34295d2606d532fa6d6f532e4a0b5feb1abca7e6c4c4ad3ab(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6897ef83f36ecfa9f0d5ac9e3856ed5d5408bb83b1937fe3cc5067697aa9126e(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    invocation_type: typing.Optional[StateMachineInvocationType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff8e8e5e6c94ac7dbe028e57bd14d8d684357b91a4076f91f77774b481be32c(
    topic: _aws_cdk_aws_sns_ceddda9d.ITopic,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575ebc1e181b2c498bb9014e996cbb4c2e00c045ef61695c446ebc2f9c0997de(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba285ccb659836012dc2efe7a33ad7d63bcf01d46f2af06697f3500102235bc(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__088dd6196b4ebb18c1863de168ca261178b1203a3b528e4a37d4e3abec68ef52(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa7b503b3079d9e51045b3114396a73fc627aec339028fa488ab019eb604fff9(
    queue: _aws_cdk_aws_sqs_ceddda9d.IQueue,
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b7cde197ff34e185db774e7f6e4e787c10c737410018f2eae647c30c381734(
    pipe: _aws_cdk_aws_pipes_alpha_c8863edb.IPipe,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bf7e2c97f60032a9e2b4a8926850651a42c588ee6eb5c9d5927f02ad257089f(
    grantee: _aws_cdk_aws_iam_ceddda9d.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860ddbc258740cac07f5dbaa48920ad737f4e849a942863e0e92606f15d6ec0f(
    *,
    input_transformation: typing.Optional[_aws_cdk_aws_pipes_alpha_c8863edb.IInputTransformation] = None,
    message_deduplication_id: typing.Optional[builtins.str] = None,
    message_group_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
